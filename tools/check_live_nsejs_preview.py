#!/usr/bin/env python3
"""Fail-closed exact-byte NSEJS technical-preview checker for local and live Pages.

The deployed revision is accepted only when the remote manifest bytes match
the local staged manifest AND every manifest-pinned asset hashes correctly.
A successful deploy-pages action or HTTP 200 homepage alone is never a PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

EXPECTED_HOST = "reallakshman19.github.io"
EXPECTED_PREFIX = "/Grade9v4.0/"
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
SAFE_PATH = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\Z")


class PreviewVerificationError(ValueError):
    """No trustworthy exact-byte evidence for the requested published revision."""


def _fail(message: str) -> None:
    raise PreviewVerificationError(message)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _base_url(url: str) -> str:
    parts = urlsplit(url)
    if (parts.scheme != "https" or parts.netloc != EXPECTED_HOST or
            parts.query or parts.fragment or
            parts.path.rstrip("/") != EXPECTED_PREFIX.rstrip("/")):
        _fail("PAGES_URL_NOT_THE_EXPECTED_PROJECT_ROOT:" + url)
    return "https://" + EXPECTED_HOST + EXPECTED_PREFIX


def _safe_path(value: str) -> bool:
    return (isinstance(value, str) and bool(SAFE_PATH.fullmatch(value))
            and all(part not in (".", "..") for part in value.split("/"))
            and value not in ("PUBLIC_PREVIEW_MANIFEST.json", ".nojekyll"))


def load_local_manifest(path: Path) -> tuple[bytes, dict]:
    try:
        local_bytes = path.read_bytes()
        expected = json.loads(local_bytes)
    except (OSError, ValueError) as exc:
        raise PreviewVerificationError("LOCAL_MANIFEST_UNREADABLE") from exc
    if not isinstance(expected, dict):
        _fail("LOCAL_MANIFEST_NOT_OBJECT")
    if (expected.get("status") != "GRADE9_NSEJS_UNVALIDATED_TECHNICAL_PREVIEW"
        or expected.get("academic_approval") != "HOLD"
        or expected.get("source_rights_review") != "HOLD"
        or expected.get("core1ab_authored_lesson_pages") != 8
        or expected.get("school_wpe_preserved") is not True
        or expected.get("existing_synthetic_reader_preserved") is not True):
        _fail("DEPLOY_MANIFEST_ADMISSION_OR_SCOPE_INVALID")
    files = expected.get("files")
    if (not isinstance(files, dict) or not files
        or any(not _safe_path(p) or not isinstance(d, str)
               or not DIGEST.fullmatch(d) for p, d in files.items())):
        _fail("MANIFEST_FILE_MAP_INVALID")
    required = {"index.html", "physics/wpe/index.html",
                "nsejs/index.html", "nsejs/physics/question-bank.html",
                "nsejs/js/core2-physics-reader.js"}
    if not required.issubset(files):
        _fail("REQUIRED_SCHOOL_WPE_NSEJS_ASSETS_MISSING")
    return local_bytes, expected


def verify_local(path: Path) -> dict:
    """Verify the exact package that upload-pages-artifact will receive."""
    manifest_bytes, expected = load_local_manifest(path)
    root = path.resolve().parent
    if not (root / ".nojekyll").is_file():
        _fail("LOCAL_NOJEKYLL_SENTINEL_MISSING")
    if _sha(path.read_bytes()) != _sha(manifest_bytes):
        _fail("LOCAL_MANIFEST_CHANGED_DURING_VERIFICATION")
    for name, digest in expected["files"].items():
        target = root / name
        if not target.is_file() or not target.resolve().is_relative_to(root):
            _fail("LOCAL_MANIFEST_ASSET_MISSING:" + name)
        if _sha(target.read_bytes()) != digest:
            _fail("LOCAL_MANIFEST_ASSET_HASH_MISMATCH:" + name)
    return {"files": len(expected["files"]), "manifest_sha256": _sha(manifest_bytes),
            "academic_approval": "HOLD", "package": "EXACT_LOCAL_BYTES_PASS"}


def download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "Grade9-NSEJS-exact-byte-Pages/2",
                                "Cache-Control": "no-cache, no-store",
                                "Pragma": "no-cache"})
    try:
        with urlopen(req, timeout=20) as response:
            if response.status != 200:
                _fail("HTTP_STATUS_" + str(response.status) + ":" + url)
            return response.read()
    except HTTPError as exc:
        raise PreviewVerificationError(
            "HTTP_STATUS_" + str(exc.code) + ":" + url) from exc
    except OSError as exc:
        raise PreviewVerificationError(
            "PUBLIC_URL_FETCH_FAILED:" + url + ":" + str(exc)) from exc


def check_live(url: str, path: Path, attempts: int = 24, delay: float = 5.0,
               fetch=download, sleep=time.sleep) -> dict:
    """Deterministic, dependency-injected verification for mocked HTTP tests."""
    if attempts < 1 or attempts > 100 or delay < 0 or delay > 30:
        _fail("INVALID_RETRY_BOUNDS")
    base = _base_url(url)
    # A missing/mutated local staging package cannot establish a deployment pin.
    verified = verify_local(path)
    manifest_bytes, expected = load_local_manifest(path)
    last = "NOT_CHECKED"
    for attempt in range(attempts):
        try:
            remote = fetch(base + "PUBLIC_PREVIEW_MANIFEST.json")
            if remote != manifest_bytes:
                _fail("PAGES_REVISION_MISMATCH:live_manifest_is_not_the_uploaded_revision")
            for name, digest in expected["files"].items():
                if _sha(fetch(base + name)) != digest:
                    _fail("PAGES_FILE_HASH_MISMATCH:" + name)
            return {"status": "PASS", "base": base, "files": verified["files"],
                    "manifest_sha256": verified["manifest_sha256"],
                    "academic_approval": "HOLD"}
        except Exception as exc:
            last = str(exc)
            if attempt < attempts - 1:
                sleep(delay)
    # Diagnostic requests NEVER convert a failure to PASS.
    diagnosis = "HOMEPAGE_NOT_TESTED"
    try:
        home = fetch(base + "index.html")
        diagnosis = "HOMEPAGE_HTTP_200_" + str(len(home)) + "_BYTES"
    except Exception as exc:
        diagnosis = "HOMEPAGE_UNAVAILABLE:" + str(exc)
    _fail("LIVE_PAGES_VALIDATION_FAILED:" + last + "; " + diagnosis +
          "; inspect Pages custom-domain/project path and deployment publication; "
          "the local artifact's presence does not prove CDN publication")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", help="Expected real GitHub Pages project root")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--verify-local", action="store_true",
                    help="Check staged exact bytes without performing a Pages deployment")
    ap.add_argument("--attempts", type=int, default=24)
    ap.add_argument("--delay", type=float, default=5.0)
    args = ap.parse_args()
    try:
        if args.verify_local:
            result = verify_local(args.manifest)
            print("PASS exact local Pages payload:", result["files"],
                  "hash-matched assets; academic HOLD")
        else:
            if not args.url:
                _fail("PAGES_URL_REQUIRED")
            result = check_live(args.url, args.manifest, args.attempts, args.delay)
            print("PASS exact live GitHub Pages preview:", result["base"],
                  result["files"], "hash-matched assets; academic HOLD")
    except PreviewVerificationError as exc:
        print("FAIL_CLOSED:", exc)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
