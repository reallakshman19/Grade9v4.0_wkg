"""Public-safe NSEJS coverage, official link-only and Q52 quarantine tests."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nsejs_core1ab_public_coverage import (
    public_coverage, render_official_sources, render_subject_index
)
from build_public_nsejs_preview import LESSONS, build


@pytest.fixture(scope="module")
def coverage():
    return public_coverage(LESSONS, root=ROOT)


def test_full_test_backed_inventory_has_eight_real_and_eighteen_missing(coverage):
    assert coverage["schema"] == "grade9-nsejs-public-core1ab-coverage/v1"
    assert coverage["tracked_constructions"] == 26
    assert coverage["owner_historical_reported_constructions"] == 27
    assert coverage["unidentified_historical_count"] == 1
    assert coverage["published_authored_preview_journeys"] == 8
    assert coverage["not_published_constructions"] == 18
    assert len(coverage["rows"]) == 26
    assert {x["construction_id"] for x in coverage["rows"]} == {
        x["construction_id"] for x in coverage["rows"]
    }
    assert all(x["academic_admission"] == "HOLD" for x in coverage["rows"])
    assert all(x["canonical_source_uid_admitted"] is None for x in coverage["rows"])
    assert all(x["original_exam_claim"] is False for x in coverage["rows"])


def test_subject_numbers_and_active_path_only_if_generated(coverage):
    counts = coverage["subject_breakdown"]
    assert counts == {
        "physics": {"tracked": 16, "published": 3},
        "chemistry": {"tracked": 7, "published": 2},
        "biology": {"tracked": 3, "published": 3},
    }
    active = [x for x in coverage["rows"] if x["route"]]
    disabled = [x for x in coverage["rows"] if not x["route"]]
    assert len(active) == 8 and len(disabled) == 18
    assert all(x["learner_status"] == "AUTHORED_PREVIEW_UNVALIDATED" for x in active)
    assert all(x["learner_status"] == "NOT_PUBLISHED" for x in disabled)
    assert all(x["engineering_note"] for x in disabled)
    assert all(not x["route"] for x in disabled)


def test_q52_bad_original_source_never_becomes_valid_association(coverage):
    row, = [x for x in coverage["rows"]
            if x["historical_target"] == "BIO-NSEJS-2024-B-Q52"]
    assert row["source_matching"] == "KNOWN_SOURCE_SUBSTITUTION"
    assert row["academic_admission"] == "HOLD"
    assert row["canonical_source_uid_admitted"] is None


@pytest.mark.parametrize("subject", ["physics", "chemistry", "biology"])
def test_each_subject_index_has_accessible_journeys_and_disabled_missing(subject, coverage):
    html = render_subject_index(subject, coverage)
    expected = coverage["subject_breakdown"][subject]
    assert html.count('class="lesson-link"') == expected["published"]
    assert html.count('class="not-ready"') == expected["tracked"]-expected["published"]
    assert "min-height:56px" in html
    assert "UNVALIDATED" in html and "Academic HOLD" in html
    assert "No academic approval inferred from software validation" in html
    assert not re.search(r'href="(?:\.\./)*workspace/', html)
    assert "<iframe" not in html.lower()


def test_official_source_page_is_link_only_and_allowlisted():
    html = render_official_sources(
        ROOT / "docs/nsejs/official-iapt-source-locators-r1.json"
    )
    assert html.count("Official paper (IAPT)") == 5
    assert html.count("Official key (IAPT)") == 5
    assert html.count("IAPT official archive") == 5
    assert "IOQJS_2020_21_PART_I" in html
    assert "2024" in html
    assert "rights" in html.lower() and "HOLD" in html
    assert "<iframe" not in html.lower() and "data:application/pdf" not in html


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    out = tmp_path_factory.mktemp("nsejs-preview-") / "dist"
    result = build(out)
    return out, result


def test_actual_build_contains_complete_coverage_and_no_fake_lesson_links(staged):
    out, manifest = staged
    coverage = json.loads(
        (out / "nsejs/data/core1ab-coverage.v1.json").read_text("utf-8")
    )
    assert coverage["published_authored_preview_journeys"] == 8
    assert coverage["not_published_constructions"] == 18
    for row in coverage["rows"]:
        if row["route"]:
            p = out / row["route"]
            assert p.is_file(), row["construction_id"]
            assert 'data-role="save-firstAttempt"' in p.read_text("utf-8")
        else:
            assert row["learner_status"] == "NOT_PUBLISHED"
    assert manifest["core1ab_authored_lesson_pages"] == 8
    assert manifest["core1ab_unpublished_constructions"] == 18
    assert manifest["official_sources_link_only"] is True
    assert (out / "nsejs/official-sources.html").is_file()
    assert not list(out.rglob("*.pdf"))
    assert not list(out.rglob("source-custody.json"))
    assert not list(out.rglob("bank.json"))


def test_public_build_links_source_page_and_subject_lists(staged):
    out, _ = staged
    for subject in ("", "physics", "chemistry", "biology"):
        page = out / ("nsejs/index.html" if not subject else f"nsejs/{subject}/index.html")
        html = page.read_text("utf-8")
        assert 'id="official-iapt-links"' in html
        assert "View official paper/key links" in html
        if subject:
            listing = out / f"nsejs/{subject}/core1/index.html"
            text = listing.read_text("utf-8")
            assert "Not published" in text or subject == "biology"
            assert "min-height:56px" in text
