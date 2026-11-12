"""Public preview must be an explicit synthetic-only package."""
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_public_reader_preview import build_preview, PAGES


def test_preview_contains_only_public_allowlist(tmp_path):
    out = tmp_path / "dist"
    receipt = build_preview(out)
    assert receipt["status"] == "SYNTHETIC_TECHNICAL_ONLY"
    assert receipt["academic_approval"] == "HOLD"
    assert receipt["candidate_50_record_published"] is False
    actual = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
    assert actual == {".nojekyll", "index.html", "PUBLIC_PREVIEW_MANIFEST.json", *PAGES}
    home = (out / "index.html").read_text()
    assert "Not an exam or academic release" in home
    assert "Synthetic question reader" in home
    assert not (out / "PRIVATE_REVIEW_MANIFEST.json").exists()
    assert not (out / ".GRADE9_PRIVATE_REVIEW_ONLY").exists()


def test_preview_is_deterministic_and_refuses_replacement(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    build_preview(a)
    build_preview(b)
    assert {p.relative_to(a).as_posix():p.read_bytes() for p in a.rglob("*") if p.is_file()} == {
        p.relative_to(b).as_posix():p.read_bytes() for p in b.rglob("*") if p.is_file()}
    with pytest.raises(ValueError, match="OUTPUT_MUST_BE_NEW"):
        build_preview(a)


def test_never_publish_to_workspace(tmp_path):
    from build_public_reader_preview import ROOT
    with pytest.raises(ValueError, match="OUTPUT_MUST_BE_NEW"):
        build_preview(ROOT / "workspace" / "should-not-publish")
