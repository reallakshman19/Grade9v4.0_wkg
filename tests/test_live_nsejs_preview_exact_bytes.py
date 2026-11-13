"""No-network exact-byte Pages publish and negative-control tests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_live_nsejs_preview import (PreviewVerificationError, check_live,
                                      load_local_manifest, verify_local,
                                      _base_url)

BASE = "https://reallakshman19.github.io/Grade9v4.0/"
FILES = ("index.html", "physics/wpe/index.html", "nsejs/index.html",
         "nsejs/physics/question-bank.html",
         "nsejs/js/core2-physics-reader.js")


@pytest.fixture
def site(tmp_path):
    root = tmp_path / "dist"
    root.mkdir()
    (root / ".nojekyll").write_text("", "utf-8")
    payloads = {name: ("original exact asset: " + name).encode() for name in FILES}
    for name, blob in payloads.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)
    manifest = {
        "status": "GRADE9_NSEJS_UNVALIDATED_TECHNICAL_PREVIEW",
        "academic_approval": "HOLD",
        "source_rights_review": "HOLD",
        "core1ab_authored_lesson_pages": 8,
        "school_wpe_preserved": True,
        "existing_synthetic_reader_preserved": True,
        "files": {name: hashlib.sha256(blob).hexdigest()
                  for name, blob in payloads.items()},
    }
    path = root / "PUBLIC_PREVIEW_MANIFEST.json"
    path.write_text(json.dumps(manifest, sort_keys=True) + "\n", "utf-8")
    remote = {BASE + name: blob for name, blob in payloads.items()}
    remote[BASE + path.name] = path.read_bytes()
    return root, path, remote


def ok_fetch(remote):
    def get(url):
        if url not in remote:
            raise PreviewVerificationError("HTTP_STATUS_404:" + url)
        return remote[url]
    return get


def test_success_requires_manifest_and_all_asset_bytes(site):
    _, manifest, remote = site
    assert verify_local(manifest)["academic_approval"] == "HOLD"
    result = check_live(BASE, manifest, attempts=1, fetch=ok_fetch(remote))
    assert result["status"] == "PASS"
    assert result["files"] == len(FILES)


def test_404_live_manifest_remains_fail_closed_even_when_home_is_live(site):
    _, manifest, remote = site
    remote.pop(BASE + manifest.name)
    with pytest.raises(PreviewVerificationError, match="HTTP_STATUS_404.*HOMEPAGE_HTTP_200"):
        check_live(BASE, manifest, attempts=2, delay=0, fetch=ok_fetch(remote), sleep=lambda _: None)


def test_stale_remote_manifest_rejected(site):
    _, manifest, remote = site
    remote[BASE + manifest.name] = b'{"status":"stale"}'
    with pytest.raises(PreviewVerificationError, match="PAGES_REVISION_MISMATCH"):
        check_live(BASE, manifest, attempts=1, fetch=ok_fetch(remote))


def test_corrupted_remote_asset_rejected(site):
    _, manifest, remote = site
    remote[BASE + "nsejs/index.html"] += b"tampered"
    with pytest.raises(PreviewVerificationError, match="PAGES_FILE_HASH_MISMATCH:nsejs/index.html"):
        check_live(BASE, manifest, attempts=1, fetch=ok_fetch(remote))


def test_missing_remote_asset_rejected(site):
    _, manifest, remote = site
    del remote[BASE + "physics/wpe/index.html"]
    with pytest.raises(PreviewVerificationError, match="HTTP_STATUS_404"):
        check_live(BASE, manifest, attempts=1, fetch=ok_fetch(remote))


def test_local_package_must_match_manifest_before_upload(site):
    root, manifest, remote = site
    (root / "nsejs/index.html").write_bytes(b"wrong")
    with pytest.raises(PreviewVerificationError, match="LOCAL_MANIFEST_ASSET_HASH_MISMATCH"):
        check_live(BASE, manifest, attempts=1, fetch=ok_fetch(remote))


def test_nojekyll_must_be_in_staged_artifact(site):
    root, manifest, _ = site
    (root / ".nojekyll").unlink()
    with pytest.raises(PreviewVerificationError, match="LOCAL_NOJEKYLL_SENTINEL_MISSING"):
        verify_local(manifest)


@pytest.mark.parametrize("bad", [
    "http://reallakshman19.github.io/Grade9v4.0/",
    "https://attacker.invalid/Grade9v4.0/",
    "https://reallakshman19.github.io/OtherRepo/",
    "https://reallakshman19.github.io/Grade9v4.0/?bypass=1",
    "https://reallakshman19.github.io/Grade9v4.0/#wrong",
    "https://reallakshman19.github.io/Grade9v4.0/../",
])
def test_wrong_pages_root_rejected(bad):
    with pytest.raises(PreviewVerificationError, match="PAGES_URL_NOT_THE_EXPECTED_PROJECT_ROOT"):
        _base_url(bad)


def test_unsafe_manifest_paths_and_hashes_rejected(site):
    _, path, _ = site
    data = json.loads(path.read_text("utf-8"))
    data["files"]["../private.json"] = "b"*64
    path.write_text(json.dumps(data), "utf-8")
    with pytest.raises(PreviewVerificationError, match="MANIFEST_FILE_MAP_INVALID"):
        load_local_manifest(path)


def test_manifest_must_preserve_academic_hold(site):
    _, path, _ = site
    data = json.loads(path.read_text("utf-8"))
    data["academic_approval"] = "PASS"
    path.write_text(json.dumps(data), "utf-8")
    with pytest.raises(PreviewVerificationError, match="DEPLOY_MANIFEST_ADMISSION_OR_SCOPE_INVALID"):
        load_local_manifest(path)


def test_bounded_retry_can_observe_delayed_publication(site):
    _, path, remote = site
    hits = []
    def delayed(url):
        if url.endswith("PUBLIC_PREVIEW_MANIFEST.json") and not hits:
            hits.append("404")
            raise PreviewVerificationError("HTTP_STATUS_404:" + url)
        return ok_fetch(remote)(url)
    result = check_live(BASE, path, attempts=2, delay=0, fetch=delayed, sleep=lambda _:None)
    assert result["status"] == "PASS"
    assert hits == ["404"]


def test_invalid_retry_bounds_rejected(site):
    _, path, remote = site
    with pytest.raises(PreviewVerificationError, match="INVALID_RETRY_BOUNDS"):
        check_live(BASE, path, attempts=0, fetch=ok_fetch(remote))
