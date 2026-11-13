#!/usr/bin/env python3
"""Restore verified owner-supplied Core2 output banks to a PRIVATE test checkout.

Never creates source-custody, SL1/SL2, Core1 evidence, or an academic release.
Accepts only a separately pinned ZIP, byte-exact manifest entries and a narrow
output-only path allowlist. Never commit the restored files to public Git.
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
from zipfile import BadZipFile, ZipFile

SHA = re.compile(r"[0-9a-f]{64}\Z")
MODULE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,120}\Z")
FILES = frozenset({"bank.json", "questions.json", "intake.json",
                  "core2_module.html", "question-status.html"})


class OutputRecoveryHold(RuntimeError):
    pass


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def _safe_member(name: str) -> None:
    if (not name or name.startswith("/") or "\\" in name or "\x00" in name
            or any(part in {"", ".", ".."} for part in name.split("/"))):
        raise OutputRecoveryHold("UNSAFE_BUNDLE_PATH:" + name)


def verify_bank_archive(archive_path: Path, expected_sha256: str) -> dict[str, bytes]:
    """Return only source-neutral output bytes; no writes until complete audit."""
    if not SHA.fullmatch(expected_sha256):
        raise OutputRecoveryHold("OWNER_ARCHIVE_SHA256_PIN_REQUIRED")
    if not archive_path.is_file() or sha_file(archive_path) != expected_sha256:
        raise OutputRecoveryHold("ARCHIVE_SHA256_MISMATCH")
    try:
        with ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if (len(infos) > 500 or len(names) != len(set(names))
                    or sum(info.file_size for info in infos) > 30_000_000):
                raise OutputRecoveryHold("BUNDLE_MEMBER_DUPLICATION_OR_SIZE")
            for info in infos:
                _safe_member(info.filename)
                if info.is_dir() or info.file_size > 2_000_000:
                    raise OutputRecoveryHold("BUNDLE_MEMBER_INVALID:" + info.filename)
                if stat.S_ISLNK(info.external_attr >> 16):
                    raise OutputRecoveryHold("BUNDLE_SYMLINK_FORBIDDEN")
            if "MANIFEST.json" not in names:
                raise OutputRecoveryHold("BUNDLE_MANIFEST_MISSING")
            manifest = json.loads(archive.read("MANIFEST.json"))
            if not isinstance(manifest, list) or not manifest:
                raise OutputRecoveryHold("BUNDLE_MANIFEST_INVALID")
            verified = set()
            output = {}
            for row in manifest:
                if not isinstance(row, dict):
                    raise OutputRecoveryHold("BUNDLE_MANIFEST_ROW_INVALID")
                name = row.get("archive_path")
                expected = row.get("sha256")
                size = row.get("bytes")
                if (not isinstance(name, str) or name in verified
                        or name not in names or not isinstance(expected, str)
                        or not SHA.fullmatch(expected)
                        or type(size) is not int or not 0 <= size <= 2_000_000):
                    raise OutputRecoveryHold("BUNDLE_MANIFEST_ROW_INVALID")
                _safe_member(name)
                verified.add(name)
                payload = archive.read(name)
                if sha_bytes(payload) != expected or len(payload) != size:
                    raise OutputRecoveryHold("BUNDLE_MEMBER_SHA256_MISMATCH:" + name)
                if name.startswith("individual_banks/"):
                    parts = name.split("/")
                    if len(parts) == 3 and MODULE.fullmatch(parts[1]) and parts[2] in FILES:
                        dest = f"workspace/output/{parts[1]}/{parts[2]}"
                        if dest in output:
                            raise OutputRecoveryHold("OUTPUT_DEST_COLLISION")
                        output[dest] = payload
                    elif len(parts) == 5 and parts[1] == "G9V4_LOTS":
                        # Already separate tracked outputs; do not replace.
                        continue
                    else:
                        raise OutputRecoveryHold("NONSTANDARD_OUTPUT_PATH:" + name)
                elif not (name in {"ALL_CORE2_QUESTIONS_AND_ANSWERS.json",
                                   "ALL_CORE2_QUESTIONS_AND_ANSWERS.md",
                                   "ALL_CORE2_QUESTIONS_AND_ANSWERS.html"}
                          or name in {"audit/5YEAR_NSEJS_CORPUS_AUDIT_REPORT.json",
                                      "audit/5YEAR_NSEJS_PLAYWRIGHT_AUDIT_REPORT.json"}):
                    raise OutputRecoveryHold("NONSTANDARD_OUTPUT_PATH:" + name)
            if set(names) - verified - {"MANIFEST.json", "README.md"}:
                raise OutputRecoveryHold("BUNDLE_UNLISTED_FILES")
            if not output:
                raise OutputRecoveryHold("NO_CORE2_OUTPUTS")
            return output
    except (BadZipFile, KeyError, OSError, json.JSONDecodeError) as exc:
        raise OutputRecoveryHold("BUNDLE_CORRUPT_OR_UNREADABLE") from exc


def preflight_destinations(root: Path, outputs: dict[str, bytes]) -> tuple[int, int]:
    root = root.resolve()
    if not root.is_dir():
        raise OutputRecoveryHold("TARGET_REPOSITORY_ROOT_MISSING")
    missing = verified_existing = 0
    for rel, data in outputs.items():
        dest = root / rel
        parent = dest
        while parent != root:
            if parent.is_symlink():
                raise OutputRecoveryHold("TARGET_SYMLINK_FORBIDDEN:" + rel)
            parent = parent.parent
        if not dest.resolve().is_relative_to(root):
            raise OutputRecoveryHold("TARGET_PATH_ESCAPES_REPO")
        if dest.exists():
            if not dest.is_file() or sha_file(dest) != sha_bytes(data):
                raise OutputRecoveryHold("TARGET_BYTE_CONFLICT:" + rel)
            verified_existing += 1
        else:
            missing += 1
    return missing, verified_existing


def restore(root: Path, outputs: dict[str, bytes]) -> dict:
    missing, existing = preflight_destinations(root, outputs)
    root = root.resolve()
    for rel, data in sorted(outputs.items()):
        dest = root / rel
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if (dest.is_symlink() or dest.parent.is_symlink()
                or not dest.parent.resolve().is_relative_to(root)):
            raise OutputRecoveryHold("TARGET_CHANGED_DURING_RESTORE")
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=dest.parent, delete=False) as handle:
                temporary = handle.name
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, dest)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
    return {"written": missing, "already_matching": existing}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive", type=Path, required=True)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--apply", action="store_true", help="Opt-in private local test workspace write")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    try:
        outputs = verify_bank_archive(args.archive, args.expected_sha256)
        missing, existing = preflight_destinations(args.root, outputs)
        result = {
            "schema": "grade9-core2-bank-output-recovery/v1",
            "archive_sha256": args.expected_sha256,
            "candidate_output_files": len(outputs),
            "modules": len({key.split("/")[2] for key in outputs}),
            "missing_before": missing,
            "already_verified": existing,
            "academic_approval": "HOLD",
            "source_custody": "NOT_PROVIDED",
            "smart_labelling_reports": "NOT_PROVIDED",
            "core1_evidence": "NOT_PROVIDED",
            "full_python_qa": "NOT_RUN",
            "status": "DRY_RUN_NO_FILES_WRITTEN",
        }
        if args.apply:
            result.update(restore(args.root, outputs))
            result["status"] = "PRIVATE_OUTPUT_ONLY_RESTORE_COMPLETE"
        if args.report:
            args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, OutputRecoveryHold) as exc:
        print("QA_SOURCE_CUSTODY_HOLD:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
