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
from nsejs_core2_public_catalog import registry,validate,render,publish


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
            '<!doctype html><html><body><main>'+name+'</main></body></html>',encoding="utf-8")
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
