"""Source-neutral 18 Core1A/B supplementary learning and 40 Code51 paper locators.

The 18 missing original private/audited modules remain HOLD. Original IAPT
questions are linked, not reproduced or claimed authenticated. Math is excluded.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_nsejs_preview import build,LESSONS,GENERATORS
from nsejs_core1ab_public_coverage import public_coverage
from nsejs_source_practice_recovery import recovery_receipt,build_source_link_index
from nsejs_independent_core1_builder import validate_catalog,lesson_html,digest
from nsejs_2024_source_key_locators import official_locator_bank,KEY,SUBJECT_NUMBERS

@pytest.fixture
def ledger():
    return recovery_receipt(public_coverage(LESSONS,ROOT),GENERATORS)

@pytest.fixture
def keys():
    source=json.loads((ROOT/"docs/nsejs/official-iapt-source-locators-r1.json").read_text("utf-8"))
    return official_locator_bank(build_source_link_index(source))


def test_2024_publisher_40_item_source_locator_census_no_original_question_text(keys):
    assert keys["total_locator_records"]==40
    assert keys["subject_locator_counts"]=={"BIOLOGY":20,"CHEMISTRY":20}
    assert keys["questions_present_as_original_text"]==0
    assert keys["source_text_copied"] is False
    assert keys["academic_admission"]==keys["redistribution_review"]=="HOLD"
    assert keys["key_transcription_status"]=="PROVISIONAL_UNTIL_SECOND_REVIEW"
    assert set(x["question_number"] for x in keys["items"])==set(KEY)
    for subject,numbers in SUBJECT_NUMBERS.items():
        items=[x for x in keys["items"] if x["subject"]==subject]
        assert len(items)==20
        assert tuple(x["question_number"] for x in items)==numbers
        assert all(x["uid"].startswith(f"g9:NSEJS:2024:51:{subject}:") for x in items)
        assert all(x["source_custody"]==x["academic_admission"]=="HOLD" for x in items)
        assert all(x["source_question_text"] is None and x["source_figures"]==[] for x in items)
        for item in items:
            raw={k:v for k,v in item.items() if k!="revision_sha256"}
            assert item["revision_sha256"]==digest(raw)
            actual=item["publisher_key"]
            expected=KEY[item["question_number"]]
            assert actual==(list(expected) if expected!="DROP" else None)
            assert item["publisher_key_status"]==("DROP" if expected=="DROP" else "IAPT_TRANSCRIBED_PROVISIONAL")
            assert item["part"]==("A2" if item["question_number"]>=49 else "A1")
    q20=next(x for x in keys["items"] if x["question_number"]==20)
    assert q20["subject"]=="CHEMISTRY" and q20["publisher_key"] is None
    assert next(x for x in keys["items"] if x["question_number"]==49)["publisher_key"]==["A","B","D"]
    assert next(x for x in keys["items"] if x["question_number"]==53)["publisher_key"]==["A","B","C"]
    assert next(x for x in keys["items"] if x["question_number"]==55)["publisher_key"]==["A","D"]


@pytest.mark.parametrize("change",[
    "publisher_rights","paper_host","source_rewrite","wrong_drop",
    "unqualified_code","2024_source_promotion"
])
def test_paper_mapping_fails_closed_on_source_custody_changes(change):
    source=json.loads((ROOT/"docs/nsejs/official-iapt-source-locators-r1.json").read_text("utf-8"))
    index=build_source_link_index(source)
    row=index["years"][0]
    if change=="publisher_rights":index["redistribution_rights"]="APPROVED"
    if change=="paper_host":row["paper_url"]="https://other.example.org/2024.pdf"
    if change=="source_rewrite":row["key_url"]="https://www.iapt.org.in/changed.pdf"
    if change=="wrong_drop":row["dropped_question_numbers"]=[]
    if change=="unqualified_code":row["paper_code"]=52
    if change=="2024_source_promotion":row["source_authentication"]="PASS"
    with pytest.raises(ValueError):
        official_locator_bank(index)


def test_18_author_skill_replacements_are_exactly_scoped_to_missing_constructions(ledger):
    catalog=validate_catalog(ROOT,ledger)
    assert catalog["schema"]=="grade9-independent-core1-recovery-journeys/v1"
    assert catalog["supplemental_authored_skill_journeys"]==18
    assert catalog["original_audited_module_count_recovered"]==0
    assert catalog["original_18_modules_still_on_hold"]==18
    assert catalog["academic_admission"]==catalog["source_exam_admission"]=="HOLD"
    original=set(x["construction_id"] for x in ledger["items"] if x["public_route"] is None)
    assert original==set(x["construction"] for x in catalog["items"])
    assert sum(x["subject"]=="CHEMISTRY" for x in catalog["items"])==5
    assert sum(x["subject"]=="PHYSICS" for x in catalog["items"])==13
    assert all(x["source_question_claim"] is False and
               x["original_b1b7_audit_equivalence"] is False and
               x["academic_admission"]=="HOLD" for x in catalog["items"])
    assert all(len(x["steps"])==3 and len(x["revision_sha256"])==64 for x in catalog["items"])
    for item in catalog["items"]:
        raw={k:v for k,v in item.items() if k!="revision_sha256"}
        assert item["revision_sha256"]==digest(raw)
        html=lesson_html(item)
        assert "six-stage" in html.lower()
        assert "No academic approval inferred" in html
        assert 'data-recovery-slug="'+item["slug"]+'"' in html
        assert "<iframe" not in html.lower()


@pytest.mark.parametrize("case",["missing","different_subject","weak_content",
                                  "duplicate","pretend_academic","pretend_original"])
def test_18_author_catalog_rejects_fabricated_original_identity(ledger,monkeypatch,tmp_path,case):
    # Use the actual checked-in source in a clean temporary root, injecting
    # one malicious edit without mutating any real project input files.
    source=ROOT/"nsejs/content"
    dst=tmp_path/"nsejs/content";dst.mkdir(parents=True)
    srcnames=["independent-core1-recovery-chem.v1.json",
              "independent-core1-recovery-physics.v1.json"]
    for name in srcnames:
        doc=json.loads((source/name).read_text("utf-8"))
        if name.startswith("independent-core1-recovery-chem"):
            if case=="missing":doc["items"].pop()
            if case=="different_subject":doc["items"][0]["subject"]="BIOLOGY"
            if case=="weak_content":doc["items"][0]["challenge"]="?"
            if case=="duplicate":doc["items"][0]=deepcopy(doc["items"][1])
            if case=="pretend_academic":doc["academic_admission"]="PASS"
            if case=="pretend_original":doc["original_18_audit_equivalence"]=True
        (dst/name).write_text(json.dumps(doc),"utf-8")
    with pytest.raises(ValueError):
        validate_catalog(tmp_path,ledger)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    folder=tmp_path_factory.mktemp("g9-nsejs-paper-and-recovery")/"dist"
    return folder,build(folder)


def test_staged_40_source_locators_and_18_authored_learner_pages_are_reproducible(built):
    folder,manifest=built
    assert manifest["source_linked_recovery"]["2024_code51_subject_locator_count"]==40
    assert manifest["source_linked_recovery"]["official_original_question_bodies"]==0
    extra=manifest["independent_core1_supplements"]
    assert extra["new_independent_authored_supplements"]==18
    assert extra["original_missing_reproducible_modules"]==18
    assert extra["source_originals_recovered"]==0
    assert extra["academic_admission"]=="HOLD"
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    index=json.loads((folder/"nsejs/data/subject-paper-2024-code51.v1.json").read_text("utf-8"))
    assert index["total_locator_records"]==40
    catalog=json.loads((folder/"nsejs/data/independent-core1-recovery.v1.json").read_text("utf-8"))
    assert len(catalog["items"])==18
    for item in catalog["items"]:
        assert (folder/item["publication_route"]).is_file()
        assert item["publication_route"] in manifest["files"]
    for name in ("physics","chemistry"):
        index=(folder/f"nsejs/{name}/core1/index.html").read_text("utf-8")
        assert 'id="independent-core1-repairs"' in index
    recovery=(folder/"nsejs/core1-recovery.html").read_text("utf-8")
    assert recovery.count("NOT PUBLISHED · source and academic HOLD")==18
    assert recovery.count('href="../nsejs/')==18
    assert "NOT the 18 withheld source-bound modules" in recovery
    assert not list(folder.rglob("*.pdf"))
