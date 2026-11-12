"""Public Pages must restore the school/NSEJS hub WITHOUT publishing private sources."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_reader_preview import build_preview,PAGES
from build_public_site_pages import PUBLIC_SHELL_FILES,HUB_PAGES,PUBLISHED_PREVIEW_PAGES

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for name in ("href","src"):
            if tag in ("a","script","link","img") and name in a and a[name]:
                self.links.append(a[name])

def test_preview_contains_exact_public_safe_subject_hub_allowlist(tmp_path):
    out=tmp_path/"dist"
    receipt=build_preview(out)
    assert receipt["status"]=="PUBLIC_SAFE_SUBJECT_HUB_WITH_SYNTHETIC_READER"
    assert receipt["academic_approval"]=="HOLD"
    assert receipt["nsejs_academic_approval"]=="HOLD"
    assert receipt["candidate_50_record_published"] is False
    assert receipt["source_question_published"] is False
    actual={p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
    assert actual=={"PUBLIC_PREVIEW_MANIFEST.json",*PAGES,*PUBLIC_SHELL_FILES}
    manifest=json.loads((out/"PUBLIC_PREVIEW_MANIFEST.json").read_text())
    assert set(manifest["files"])==actual-{"PUBLIC_PREVIEW_MANIFEST.json"}
    assert all(k not in actual for k in ("PRIVATE_REVIEW_MANIFEST.json",
        ".GRADE9_PRIVATE_REVIEW_ONLY",
        "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",
        "physics/wpe/question-bank.html","physics/wpe/learn-challenge.html"))
    for name in ("index.html","nsejs/index.html","nsejs/physics/index.html",
                 "nsejs/chemistry/index.html","nsejs/biology/index.html"):
        html=(out/name).read_text(encoding="utf-8")
        assert 'href=' in html and "NSEJS" in html
        assert "No academic" in html or "academic" in html.lower()
    assert "Synthetic question reader" not in (out/"index.html").read_text()
    assert "Choose your subject or NSEJS track" in (out/"index.html").read_text()
    assert "Synthetic " in (out/"preview/question-status.html").read_text()

def test_all_published_student_links_resolve_without_hidden_workspaces(tmp_path):
    out=tmp_path/"dist"
    build_preview(out)
    for name in (*HUB_PAGES,*PUBLISHED_PREVIEW_PAGES):
        p=out/name
        parser=Links()
        parser.feed(p.read_text(encoding="utf-8"))
        assert parser.links,("missing navigation",name)
        for raw in parser.links:
            parts=urlsplit(raw)
            if parts.scheme in ("https","mailto","tel") or raw.startswith("#"):
                continue
            assert not parts.scheme and not parts.netloc,(name,raw)
            # Resolve href and script relative to the page, not server root;
            # reject traversal outside package, absent files and workspace links.
            target=(p.parent / parts.path).resolve() if parts.path else p.resolve()
            assert target.is_relative_to(out.resolve()),(name,raw)
            assert target.is_file(),(name,raw)
    # Campus main and NSEJS headings link only to authored safe paths.
    home=(out/"index.html").read_text()
    assert 'href="nsejs/index.html"' in home
    nsejs=(out/"nsejs/index.html").read_text()
    assert 'href="physics/index.html"' in nsejs
    assert 'href="chemistry/index.html"' in nsejs
    assert 'href="biology/index.html"' in nsejs

def test_preview_is_deterministic_and_refuses_replacement(tmp_path):
    a,b=tmp_path/"a",tmp_path/"b"
    build_preview(a)
    build_preview(b)
    assert {p.relative_to(a).as_posix():p.read_bytes() for p in a.rglob("*") if p.is_file()}=={
        p.relative_to(b).as_posix():p.read_bytes() for p in b.rglob("*") if p.is_file()}
    with pytest.raises(ValueError,match="OUTPUT_MUST_BE_NEW"):
        build_preview(a)

def test_never_publish_to_workspace(tmp_path):
    from build_public_reader_preview import ROOT
    with pytest.raises(ValueError,match="OUTPUT_MUST_BE_NEW"):
        build_preview(ROOT/"workspace"/"should-not-publish")
