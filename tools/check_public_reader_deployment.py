"""Verify exact public-safe synthetic Pages bytes against local deployment pins.

No private handoff files and no academic qualification. Used AFTER Pages deploy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

PUBLIC_PAGES = {
    "index.html",
    "preview/question-status.html",
    "modules/alpha/question-status.html",
    "modules/beta/question-status.html",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(url: str, manifest_path: Path, attempts: int = 15, delay: float = 3) -> dict:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "reallakshman19.github.io":
        raise ValueError("UNTRUSTED_PUBLIC_URL")
    base = url if url.endswith("/") else url + "/"
    local_bytes = manifest_path.read_bytes()
    expected = json.loads(local_bytes)
    if (expected.get("status") != "SYNTHETIC_TECHNICAL_ONLY"
        or expected.get("academic_approval") != "HOLD"
        or expected.get("candidate_50_record_published") is not False
        or set(expected.get("files", {})) != PUBLIC_PAGES):
        raise ValueError("MANIFEST_NOT_SAFE_FOR_PUBLIC_RELEASE")
    observed_error = ""
    for attempt in range(attempts):
        try:
            def fetch(path: str) -> bytes:
                req = Request(urljoin(base, path), headers={
                    "Cache-Control": "no-cache", "User-Agent": "Grade9-tech-preview-integrity/1"
                })
                with urlopen(req, timeout=12) as response:
                    if response.status != 200:
                        raise RuntimeError("HTTP_NOT_200:" + path)
                    return response.read()
            remote_bytes = fetch("PUBLIC_PREVIEW_MANIFEST.json")
            if remote_bytes != local_bytes:
                raise ValueError("DEPLOYED_MANIFEST_NOT_CURRENT")
            for path, wanted in expected["files"].items():
                actual = fetch(path)
                if sha(actual) != wanted:
                    raise ValueError("LIVE_ARTIFACT_HASH_MISMATCH:" + path)
                if path == "index.html" and (
                    b"Synthetic question reader" not in actual
                    or b"Not an exam or academic release." not in actual):
                    raise ValueError("LIVE_HUB_DISCLAIMER_MISSING")
            return {"status": "PASS", "files": len(expected["files"]),
                    "academic_approval": "HOLD", "url": base}
        except Exception as exc:
            observed_error = type(exc).__name__ + ": " + str(exc)
            if attempt + 1 < attempts:
                time.sleep(delay)
    raise RuntimeError("LIVE_PAGES_NOT_VERIFIED:" + observed_error)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    result = check(args.url, args.manifest)
    print("PASS live Pages synthetic integrity:", result["files"], "files at", result["url"])


if __name__ == "__main__":
    main()
