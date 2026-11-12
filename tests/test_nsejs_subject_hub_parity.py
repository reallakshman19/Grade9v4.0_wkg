"""Subject-hub parity gates for existing authored NSEJS technical previews.

No mathematics preview assertion, private workspace source, new Core2 Chemistry/
Biology bank or expansion of the 8/26 public Core1 construction count is made.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_nsejs_preview import LESSONS, build

EXPECTED={
    "chemistry":{
        2:"chem-electronic-structure-d3-r1",
        3:"chem-phosphorus-oxyacids-d3-r1",
    },
    "biology":{
        0:"bio-viral-genetics-d3-r1",
        1:"bio-immunology-defense-d3-r1",
        2:"bio-genetics-coordination-r1",
    },
}
TOPIC_COUNT={"chemistry":6,"biology":5}


@pytest.mark.parametrize("subject",("chemistry","biology"))
def test_source_hubs_have_mathjax_and_only_authored_lesson_routes(subject):
    html=(ROOT/f"nsejs/{subject}/index.html").read_text("utf-8")
    head=html.split("</head>",1)[0]
    assert "window.MathJax" in head
    assert r"['\\(', '\\)']" in head
    assert "cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" in head
    assert head.index("window.MathJax") < head.index("tex-svg.js")
    assert "Academic HOLD" in html and "Core2 question banks remain unavailable" in html
    topics=re.findall(r'<article class="topic-card-tab">([\s\S]*?)</article>',html)
    assert len(topics)==TOPIC_COUNT[subject]
    for index,topic in enumerate(topics):
        published=EXPECTED[subject].get(index)
        links=re.findall(r'href="core1/([A-Za-z0-9-]+)/index.html"',topic)
        if published:
            assert links==[published,published],(subject,index,links)
            assert "Open authored Core1A + Core1B" in topic
            assert "UNVALIDATED" not in topic.upper() or "{Unvalidated}" in topic
        else:
            assert links==[],(subject,index,links)
            assert topic.count('href="core1/index.html"')==2
            assert "Not published · see Core1 coverage" in topic
        assert 'disabled title="No verified public source-backed question bank available"' in topic
        assert "Bank unavailable (source HOLD)" in topic
    assert sorted(EXPECTED[subject].values())==sorted(LESSONS[subject])
    assert html.count('class="core1-lesson-link"')==2*len(LESSONS[subject])
    assert "<iframe" not in html.lower()


@pytest.mark.parametrize("subject,formula",[
    ("chemistry",r"\(H_3PO_2\)"),
    ("chemistry",r"\(H_3PO_3\)"),
    ("biology",r"\(C_3/C_4\)")
])
def test_visible_formula_delimiters_are_mathjax_compatible(subject,formula):
    html=(ROOT/f"nsejs/{subject}/index.html").read_text("utf-8")
    assert formula in html
    assert "<script" in html and "MathJax" in html


def test_no_unverified_chemistry_or_biology_core2_bank_created():
    for subject in EXPECTED:
        assert not (ROOT/f"nsejs/{subject}/question-bank.html").exists()
        html=(ROOT/f"nsejs/{subject}/index.html").read_text("utf-8")
        assert "source verification pending" in html
        assert "No reproducible public source-backed question bank" in html
        assert not re.search(r'href="question-bank.html',html)


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    dist=tmp_path_factory.mktemp("subject-hubs")/"dist"
    return dist,build(dist)


def test_published_generated_pages_are_linked_with_source_holds(staged):
    dist,manifest=staged
    coverage=json.loads((dist/"nsejs/data/core1ab-coverage.v1.json").read_text("utf-8"))
    assert coverage["published_authored_preview_journeys"]==8
    assert coverage["not_published_constructions"]==18
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    assert all(item["academic_admission"]=="HOLD" for item in coverage["rows"])
    for subject,topic_links in EXPECTED.items():
        hub=(dist/f"nsejs/{subject}/index.html").read_text("utf-8")
        assert "window.MathJax" in hub
        for slug in topic_links.values():
            assert f'href="core1/{slug}/index.html"' in hub
            lesson=dist/f"nsejs/{subject}/core1/{slug}/index.html"
            assert lesson.is_file(),slug
            body=lesson.read_text("utf-8")
            assert 'data-role="save-firstAttempt"' in body
            assert "No academic approval inferred" in body
        assert (dist/f"nsejs/{subject}/core1/index.html").is_file()
    assert not list(dist.rglob("*.pdf"))
