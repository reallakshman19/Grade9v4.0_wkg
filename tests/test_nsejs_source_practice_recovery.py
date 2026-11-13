"""NSEJS recovery gates: source-linked paper notes and exactly 18 missing builds.

No source paper text, private PDF, official key, invented question body,
academic promotion or mathematics change is required or allowed.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_nsejs_preview import LESSONS, GENERATORS, build
from nsejs_core1ab_public_coverage import public_coverage
from nsejs_source_practice_recovery import (
    build_source_link_index,recovery_receipt,render_core1_recovery,
    SCHEMA,ORIGIN
)


@pytest.fixture
def sources():
    return json.loads((ROOT/"docs/nsejs/official-iapt-source-locators-r1.json").read_text("utf-8"))


def test_source_linked_is_real_paper_index_not_fabricated_bank(sources):
    manifest=build_source_link_index(sources)
    assert manifest["schema"]==SCHEMA
    assert manifest["source_authority"]==ORIGIN
    assert manifest["subjects"]==["CHEMISTRY","BIOLOGY"]
    assert manifest["academic_admission"]=="HOLD"
    assert manifest["redistribution_rights"]=="HOLD"
    assert manifest["question_count_claimed"]==0
    assert manifest["actual_question_bodies"]==0
    assert len(manifest["years"])==5
    assert len({y["year"] for y in manifest["years"]})==5
    assert all(y["source_authentication"]=="HOLD" for y in manifest["years"])
    assert all(y["question_text_present"] is False and
               y["official_answer_values_present"] is False for y in manifest["years"])
    assert all(y["paper_url"].startswith(("https://iapt.org.in/",
                 "https://www.iapt.org.in/")) for y in manifest["years"])
    assert manifest["years"][0]["year"]==2024
    yr=manifest["years"][0]
    assert yr["paper_code"]==51 and yr["supported_question_range"]==[1,60]
    assert yr["multi_answer_range"]==[49,60]
    assert yr["dropped_question_numbers"]==[20]
    assert yr["attempt_eligibility"]=="UNVERIFIED_LOCAL_NOTES_ONLY_CODE51"
    assert all(y["attempt_eligibility"]=="LINK_ONLY_SOURCE_SCOPE_HOLD" for y in manifest["years"][1:])


@pytest.mark.parametrize("mutate",[
    "official_authority","duplicate_year","wrong_host","ftp_link",
    "source_claim","official_source_already_imported","false_authenticated",
    "drop_removed","2024_A2_wrong","2024_code_wrong"
])
def test_custody_source_manipulations_fail_closed(sources,mutate):
    source=deepcopy(sources)
    year=next(y for y in source["years"] if y["year"]==2024)
    if mutate=="official_authority":source["source_admission"]="APPROVED"
    if mutate=="duplicate_year":source["years"][0]["year"]=2021
    if mutate=="wrong_host":year["official_paper_url"]="https://example.com/paper.pdf"
    if mutate=="ftp_link":year["official_final_key_url"]="http://iapt.org.in/key.pdf"
    if mutate=="source_claim":source["copyright_and_redistribution"]="APPROVED"
    if mutate=="official_source_already_imported":year["source_bytes_imported"]=True
    if mutate=="false_authenticated":year["independently_authenticated"]=True
    if mutate=="drop_removed":year["known_final_key_exception"]={}
    if mutate=="2024_A2_wrong":year["part_A2_format"]="SINGLE_CHOICE"
    if mutate=="2024_code_wrong":year["paper_code"]=0
    with pytest.raises(ValueError):
        build_source_link_index(source)


def test_recovery_register_precisely_identifies_all_18_misrepresented_as_done():
    coverage=public_coverage(LESSONS,ROOT)
    report=recovery_receipt(coverage,GENERATORS)
    assert report["schema"]=="grade9-nsejs-core1-recovery/v1"
    assert (report["tracked"],report["existing_technical_previews"],
            report["missing_reproducible_previews"])==(26,8,18)
    assert report["academic_admission"]=="HOLD"
    assert report["owner_reported_extra_construction_unidentified"]==1
    missing=[x for x in report["items"] if x["public_route"] is None]
    assert len(missing)==18
    assert all(x["academic_admission"]=="HOLD" and
               x["canonical_source_uid"] is None and
               x["original_exam_claim"] is False for x in report["items"])
    assert all(x["technical_state"]=="MISSING_CHECKED_IN_REPRODUCIBLE_BUILD" for x in missing)
    assert all(len(x["needed_before_technical_preview"])==7 for x in missing)
    assert all(not x["public_route"] for x in missing)
    page=render_core1_recovery(report)
    assert page.count("NOT PUBLISHED · source and academic HOLD")==18
    assert "27th item lacks a test-backed construction identity" in page
    assert "<iframe" not in page.lower()


@pytest.mark.parametrize("mutation",["wrong_count","fake_academic","duplicate","fake_source"])
def test_recovery_cannot_promote_or_erase_18_holds(mutation):
    coverage=deepcopy(public_coverage(LESSONS,ROOT))
    if mutation=="wrong_count":coverage["not_published_constructions"]=0
    if mutation=="fake_academic":coverage["academic_admission"]="PASS"
    if mutation=="duplicate":coverage["rows"][1]["construction_id"]=coverage["rows"][0]["construction_id"]
    if mutation=="fake_source":coverage["rows"][1]["original_exam_claim"]=True
    with pytest.raises(ValueError):
        recovery_receipt(coverage,GENERATORS)


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    stage=tmp_path_factory.mktemp("paper-linked-nsejs")/"dist"
    manifest=build(stage)
    return stage,manifest


def test_exact_public_package_contains_working_notebook_and_recovery_not_official_paper(staged):
    dist,manifest=staged
    scope=manifest["source_linked_recovery"]
    assert scope["source_linked_paper_notebooks"]==2
    assert scope["source_paper_count"]==5
    assert scope["question_bodies_published"]==0
    assert scope["core1_missing_reproducible_modules"]==18
    assert scope["academic_admission"]=="HOLD"
    index=json.loads((dist/"nsejs/data/source-linked-practice.v1.json").read_text("utf-8"))
    assert index["question_count_claimed"]==0
    recovery=json.loads((dist/"nsejs/data/core1-recovery.v1.json").read_text("utf-8"))
    assert recovery["missing_reproducible_previews"]==18
    assert (dist/"nsejs/core1-recovery.html").is_file()
    for subject in ("chemistry","biology"):
        hub=(dist/f"nsejs/{subject}/index.html").read_text("utf-8")
        assert hub.count('id="source-linked-external-practice"')==1
        assert 'href="question-bank.html"' in hub
        assert "not a verified" in hub.lower()
        reader=dist/f"nsejs/{subject}/question-bank.html"
        assert reader.is_file()
        html=reader.read_text("utf-8")
        assert "Source HOLD" in html
        assert f'data-paper-subject="{subject.upper()}"' in html
        assert "not a complete NSEJS" in html
        assert "<iframe" not in html.lower()
    assert (dist/"nsejs/js/source-linked-exam-practice.js").is_file()
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    assert manifest["academic_approval"]==manifest["source_rights_review"]=="HOLD"
    for forbidden in ["workspace/sources","source-custody.json"]:
        assert not any(forbidden in name for name in manifest["files"])
    assert not list(dist.rglob("*.pdf"))


def test_authored_core1b_transfer_bank_uses_only_five_fresh_builder_prompts(staged):
    dist,manifest=staged
    path=dist/"nsejs/data/authored-core1b-transfers.v1.json"
    assert path.is_file()
    bank=json.loads(path.read_text("utf-8"))
    assert bank["schema"]=="grade9-nsejs-authored-core1b-practice/v1"
    assert bank["source_origin"]=="GRADE9_ORIGINAL_CORE1B_TRANSFER_NOT_OFFICIAL_NSEJS"
    assert bank["academic_admission"]=="HOLD"
    assert bank["source_exam_authenticated"] is False
    assert bank["official_exam_questions_published"]==0
    assert bank["copy_of_original_exam_stem"] is False
    assert bank["authored_transfer_count"]==5
    assert len(bank["items"])==5
    assert len({item["uid"] for item in bank["items"]})==5
    for subject,expected in (("CHEMISTRY",2),("BIOLOGY",3)):
        items=[x for x in bank["items"] if x["subject"]==subject]
        assert len(items)==expected
        reader=dist/f"nsejs/{subject.lower()}/authored-practice.html"
        assert reader.is_file()
        body=reader.read_text("utf-8")
        assert "Authored Core1B transfer practice" in body
        assert "NOT</strong> official NSEJS questions" in body
        assert "<iframe" not in body.lower()
        hub=(dist/f"nsejs/{subject.lower()}/index.html").read_text("utf-8")
        assert hub.count('id="authored-transfer-question-bank"')==1
        assert 'href="authored-practice.html"' in hub
        for q in items:
            assert q["academic_admission"]=="HOLD"
            assert q["independent_science_review"]=="HOLD"
            assert q["original_exam_question"] is False
            assert q["source_origin"]==bank["source_origin"]
            assert len(q["prompt"])>=55
            assert len(q["reconstruction"])>=2
            assert len(q["boundary_author_response"])>=25
            assert "AUTHENTIC-EXAM" not in q["fresh_task_ref"].upper()
            assert q["lesson_route"] in manifest["files"]
            assert len(q["revision_sha256"])==64
    assert "nsejs/js/authored-transfer-practice.js" in manifest["files"]
    assert "nsejs/data/authored-core1b-transfers.v1.json" in manifest["files"]
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
