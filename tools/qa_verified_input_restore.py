#!/usr/bin/env python3
"""Restore an OWNER-PINNED private QA workspace bundle; never fabricate sources.

This is an opt-in *local* tool. It does not fetch private exam papers, publish
source files, or grant academic admission. Both ZIP and manifest SHA-256 values
MUST be supplied independently by the Owner. A complete checksum and path
audit occurs before any file is written. The subsequent FULL pytest gate is
still required; restoring bytes alone does not constitute qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from zipfile import ZipFile, BadZipFile

DIGEST = re.compile(r"[0-9a-f]{64}\Z")
MAX_FILES = 20000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 1024 * 1024 * 1024
SAFE_SUFFIXES = frozenset({
    ".json", ".html", ".htm", ".txt", ".md", ".csv", ".xml",
    ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".yaml", ".yml",
})


class PrivateInputError(RuntimeError):
    """Missing, unauthenticated or potentially unsafe workspace input."""


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(raw: object) -> str:
    if not isinstance(raw, str) or "\\" in raw or "\x00" in raw:
        raise PrivateInputError("UNSAFE_PRIVATE_BUNDLE_PATH")
    segments = raw.split("/")
    if (len(segments) < 4 or segments[0] != "workspace"
        or segments[1] not in {"sources", "output"}
        or any(p in {"", ".", ".."} for p in segments)
        or Path(raw).suffix.lower() not in SAFE_SUFFIXES):
        raise PrivateInputError("UNSAFE_PRIVATE_BUNDLE_PATH:" + raw)
    return raw


def validate_bundle(bundle: Path, manifest: Path, bundle_sha256: str,
                    manifest_sha256: str, root: Path) -> dict:
    """Return verified payloads; never write until the complete audit passes."""
    if not DIGEST.fullmatch(bundle_sha256) or not DIGEST.fullmatch(manifest_sha256):
        raise PrivateInputError("OWNER_SHA256_PINS_REQUIRED")
    if not bundle.is_file() or not manifest.is_file():
        raise PrivateInputError("OWNER_PRIVATE_INPUT_ARCHIVE_OR_MANIFEST_MISSING")
    if file_sha(bundle) != bundle_sha256:
        raise PrivateInputError("PRIVATE_BUNDLE_SHA256_MISMATCH")
    if file_sha(manifest) != manifest_sha256:
        raise PrivateInputError("PRIVATE_MANIFEST_SHA256_MISMATCH")
    try:
        record = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PrivateInputError("PRIVATE_MANIFEST_NOT_VALID_JSON") from exc
    if (not isinstance(record, dict) or
        record.get("schema") != "grade9-private-qa-input-bundle/v1" or
        record.get("academic_approval") != "HOLD" or
        not isinstance(record.get("files"), dict)):
        raise PrivateInputError("PRIVATE_MANIFEST_ADMISSION_OR_SCHEMA_INVALID")
    files = record["files"]
    if not files or len(files) > MAX_FILES:
        raise PrivateInputError("PRIVATE_MANIFEST_FILE_COUNT_INVALID")
    if not any(p.startswith("workspace/sources/") for p in files):
        raise PrivateInputError("NO_PRIVATE_SOURCE_CUSTODY_IN_BUNDLE")
    for p, digest in files.items():
        safe_path(p)
        if not isinstance(digest, str) or not DIGEST.fullmatch(digest):
            raise PrivateInputError("PRIVATE_FILE_DIGEST_INVALID:" + p)
    root = root.resolve()
    if not root.is_dir():
        raise PrivateInputError("TARGET_REPOSITORY_ROOT_MISSING")
    # Never redirect source writes through a symlink, even if its target would
    # otherwise appear to be inside the checkout.
    payloads = {}
    total_bytes = 0
    try:
        with ZipFile(bundle) as zf:
            infos = [entry for entry in zf.infolist() if not entry.is_dir()]
            if len(infos) != len(files) or len({x.filename for x in infos}) != len(infos):
                raise PrivateInputError("PRIVATE_ARCHIVE_FILE_SET_OR_DUPLICATES_INVALID")
            if {x.filename for x in infos} != set(files):
                raise PrivateInputError("PRIVATE_ARCHIVE_CONTENTS_NOT_MANIFEST_PINNED")
            for entry in infos:
                p = safe_path(entry.filename)
                mode = (entry.external_attr >> 16) & 0xffff
                if stat.S_ISLNK(mode):
                    raise PrivateInputError("PRIVATE_ARCHIVE_SYMLINK_FORBIDDEN:" + p)
                total_bytes += entry.file_size
                if (entry.file_size > MAX_FILE_BYTES or
                    total_bytes > MAX_TOTAL_BYTES):
                    raise PrivateInputError("PRIVATE_ARCHIVE_TOO_LARGE")
                payload = zf.read(entry)
                if hashlib.sha256(payload).hexdigest() != files[p]:
                    raise PrivateInputError("PRIVATE_FILE_SHA256_MISMATCH:" + p)
                target = root / p
                for parent in (target, *target.parents):
                    if parent == root:
                        break
                    if parent.is_symlink():
                        raise PrivateInputError("WORKSPACE_SYMLINK_FORBIDDEN:" + p)
                if not target.resolve().is_relative_to(root):
                    raise PrivateInputError("WORKSPACE_PATH_ESCAPE:" + p)
                if target.exists() and file_sha(target) != files[p]:
                    raise PrivateInputError("EXISTING_WORKSPACE_BYTES_CONFLICT:" + p)
                payloads[p] = payload
    except (OSError, BadZipFile, KeyError) as exc:
        raise PrivateInputError("PRIVATE_BUNDLE_UNREADABLE_OR_INCOMPLETE") from exc
    return {"files": payloads, "count": len(payloads),
            "bytes": total_bytes, "root": root, "academic_approval": "HOLD"}


def restore(result: dict) -> dict:
    root = result["root"]
    # All path and digest checks were completed by validate_bundle.
    for relative, payload in sorted(result["files"].items()):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        # Recheck against time-of-check/time-of-use path substitutions.
        if (not target.parent.resolve().is_relative_to(root) or
            any(p.is_symlink() for p in target.parents if p != root) or
            target.is_symlink()):
            raise PrivateInputError("WORKSPACE_CHANGED_BEFORE_RESTORE:" + relative)
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(payload).hexdigest():
                raise PrivateInputError("EXISTING_WORKSPACE_BYTES_CONFLICT:" + relative)
            continue
        name = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
                name = handle.name
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(name, target)
        finally:
            if name and os.path.exists(name):
                os.unlink(name)
    return {"status": "PRIVATE_WORKSPACE_BYTES_RESTORED_FOR_TESTING",
            "files": result["count"], "bytes": result["bytes"],
            "academic_approval": "HOLD", "full_python_qa": "NOT_YET_RUN"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--expected-bundle-sha256", required=True)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--restore", action="store_true",
                        help="Explicitly write only after full checksum preflight.")
    opts = parser.parse_args()
    try:
        audit = validate_bundle(opts.bundle, opts.manifest,
                                opts.expected_bundle_sha256,
                                opts.expected_manifest_sha256,
                                opts.root)
        outcome = restore(audit) if opts.restore else {
            "status": "PINNED_PRIVATE_BUNDLE_VERIFIED_NO_WRITE",
            "files": audit["count"], "bytes": audit["bytes"],
            "academic_approval": "HOLD", "full_python_qa": "NOT_YET_RUN",
        }
        print(json.dumps(outcome, sort_keys=True))
        return 0
    except PrivateInputError as exc:
        print("PRIVATE_WORKSPACE_HOLD:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
