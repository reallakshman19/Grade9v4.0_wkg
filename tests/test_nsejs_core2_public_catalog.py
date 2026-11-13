"""Core2 source-safe archive metadata; NEVER an original-exam publication gate.

Owner-uploaded private ZIP remains outside GitHub and Pages. Math excluded.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from nsejs_core2_public_catalog import (registry,validate,render,publish,
    expose_zip_coverage_in_subject_cards,TOPIC_FILE_GROUPS)


def test_archive_core2_inventory_counts_exact_and_no_mathematics():
    doc=registry()
    validate(doc)
    assert doc["module_count"]==45
    assert doc["candidate_question_count"]==267
    assert doc["subjects"]=={
        "PHYSICS":{"modules":21,"candidates":95},
        "CHEMISTRY":{"modules":13,"candidates":87},
        "BIOLOGY":{"modules":11,"candidates":85}}
    assert len(doc["items"])==45
    assert len({x["slug"] for x in doc["items"]})==45
    assert not any("math" in x["slug"] for x in doc["items"])
    assert all(x["public_question_text"] is False and
               x["student_question_route"] is None and
               x["source_custody"]=="SOURCE_CUSTODY_NOT_ESTABLISHED" and
               x["academic_admission"]=="HOLD" for x in doc["items"])
    assert doc["original_exam_question_bodies_published"]==0
    assert doc["source_custody_records_imported"]==0
    assert doc["public_student_modules_from_uploaded_zip"]==0


@pytest.mark.parametrize("tamper",[
    "approve","rights","add_math","add_stem","fake_route","change_count","duplicate"
])
def test_public_register_rejects_privately_fabricated_admission(tamper):
    doc=deepcopy(registry())
    if tamper=="approve":doc["academic_admission"]="PASS"
    if tamper=="rights":doc["redistribution_rights"]="CLEARED"
    if tamper=="add_math":
        doc["items"].append({"slug":"math-unknown","subject":"MATHEMATICS"})
    if tamper=="add_stem":doc["items"][0]["question_body"]="Unverified original"
    if tamper=="fake_route":doc["items"][0]["student_question_route"]="core2/private-question.html"
    if tamper=="change_count":doc["items"][0]["unverified_candidate_question_count"]=100
    if tamper=="duplicate":doc["items"][0]=deepcopy(doc["items"][1])
    with pytest.raises(ValueError,match="UNAPPROVED_CORE2_METADATA"):
        validate(doc)


def test_render_is_source_safe_explicit_and_links_only_to_existing_public_routes():
    doc=registry()
    page=render(doc)
    assert "No Mathematics records included" in page
    assert "No question text or approved learner route" in page
    assert "Source and academic HOLD" in page
    assert page.count("<tr>")==48  # 45 data rows + 3 table headers
    assert 'href="../chemistry/question-bank.html"' in page
    assert 'href="../biology/question-bank.html"' in page
    assert 'href="../physics/question-bank.html"' in page
    assert "workspace/sources/" not in page
    assert "<iframe" not in page.lower()
    assert "unverified original exam" not in page.lower()
    assert doc["source_archive_sha256"] not in page  # fingerprint not user-visible


def test_publish_metadata_only_into_stage_and_subject_navigation(tmp_path):
    stage=tmp_path/"public"
    for name in ("physics","chemistry","biology"):
        root=stage/"nsejs"/name
        root.mkdir(parents=True)
        (root/"index.html").write_text(
            '<!doctype html><html><body><main class="tablet-container">'+name+'</main></body></html>',encoding="utf-8")
    info=publish(stage)
    assert info=={"status":"METADATA_CATALOG_ONLY","module_count":45,
                  "candidate_question_count":267,
                  "original_exam_question_bodies_published":0,
                  "academic_admission":"HOLD","redistribution_rights":"HOLD"}
    catalog=json.loads((stage/"nsejs/core2/inventory.v1.json").read_text("utf-8"))
    validate(catalog)
    assert (stage/"nsejs/core2/index.html").is_file()
    for name in ("physics","chemistry","biology"):
        html=(stage/"nsejs"/name/"index.html").read_text("utf-8")
        assert html.count('id="core2-archive-register"')==1
        assert f'href="../core2/index.html#{name}"' in html
        assert "SOURCE" not in html or "HOLD" in html
    with pytest.raises(ValueError,match="CORE2_REGISTER_DUPLICATE"):
        publish(stage)
    assert not list(stage.rglob("*.pdf"))
    assert not list(stage.rglob("bank.json"))
    assert not list(stage.rglob("*math*"))


def test_existing_subject_cards_show_new_zip_question_map_without_replacing_old_bank():
    """Regression for screenshots still showing only Open 10 candidate records."""
    catalog = registry()
    expectations = {
        "physics": (6, 21, 95, 16),
        "chemistry": (6, 13, 87, 8),
        "biology": (5, 11, 85, 6),
    }
    byslug = {m["slug"] for m in catalog["items"]}
    for subject, (cards, modules, questions, topical) in expectations.items():
        original = (ROOT/"nsejs"/subject/"index.html").read_text("utf-8")
        assert original.count('<div class="topics-grid-12-7">') == 1
        updated = expose_zip_coverage_in_subject_cards(original,subject,catalog)
        assert updated.count('id="pcb-core2-zip-now-visible"') == 1
        assert updated.count('class="core2-zip-topic-preview"') == cards
        assert f'{modules} {subject.title()} modules · {questions} question IDs indexed' in updated
        assert f'Browse all {questions} source-held question IDs' in updated
        assert f'href="../core2/question-map.html#{subject}"' in updated
        assert 'Metadata only · Source/rights/academic HOLD' in updated
        assert 'not</em> the existing topic-button question records' in updated
        # The existing reader buttons must remain intact; no implied replacement.
        if subject == "physics":
            assert updated.count("Open 10 candidate records") == 4
            assert 'Open 11 candidate records (1 authored)' in updated
            assert 'No public bank (HOLD)' in updated
            assert updated.count("onclick=\"openTopicQBank(") == 6
        module_links = [slug for _, slugs in TOPIC_FILE_GROUPS[subject] for slug in slugs]
        assert len(set(module_links)) == len(module_links) == topical
        assert set(module_links).issubset(byslug)
        for slug in module_links:
            assert updated.count(f'href="../core2/question-map.html#module-{slug}"') == 1
        assert "original exam questions and answer keys are not published" not in updated
        assert 'No full ZIP stems, figures, keys or solutions are published' in updated
        assert '<iframe' not in updated.lower()


def test_card_publication_fail_closed_if_core2_topic_dom_changed():
    source = (ROOT/"nsejs"/"physics"/"index.html").read_text("utf-8")
    assert source.count('<article class="topic-card-tab">') == 6
    broken=source.replace('class="topics-grid-12-7"', 'class="topics-grid-12-7"') \
                 .replace('<span class="core-name">Question Bank</span>',
                          '<span class="core-name">Bank</span>', 1)
    with pytest.raises(ValueError, match="CORE2_TOPIC_CARD_ANCHOR_CHANGED"):
        expose_zip_coverage_in_subject_cards(broken,"physics",registry())
    with pytest.raises(ValueError, match="CORE2_TOPIC_CARD_STRUCTURE_CHANGED"):
        expose_zip_coverage_in_subject_cards(
            source.replace('</article>', '</article></article>', 1)
                  .replace('<article class="topic-card-tab">', '', 1),
            "physics",registry())
