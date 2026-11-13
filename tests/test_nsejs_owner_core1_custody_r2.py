"""Owner Core1 uploaded archive receipt: do not confuse byte-exact originals
with the 18 source-neutral technical skill-preview replacements.

The owner's original ZIP is PRIVATE and deliberately absent from public Git.
This suite checks the source-neutral immutable inventory, four science holds,
and the actual generated Pages payload.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from nsejs_owner_core1_publication_gate import custody_receipt,PIN,EXPECTED_BLOCKERS
from nsejs_core1ab_public_coverage import public_coverage
from nsejs_source_practice_recovery import recovery_receipt
from nsejs_independent_core1_builder import validate_catalog
from build_public_nsejs_preview import LESSONS,GENERATORS,build

@pytest.fixture
def original():
    return recovery_receipt(public_coverage(LESSONS,ROOT),GENERATORS)

@pytest.fixture
def catalog(original):
    return validate_catalog(ROOT,original)

@pytest.fixture
def owner():
    return json.loads((ROOT/"docs/nsejs/core1-owner-candidate-custody-r2.json").read_text("utf8"))

def store(tmp_path,owner):
    path=tmp_path/"candidate.json"
    path.write_text(json.dumps(owner),encoding="utf8")
    return path

def test_exact_private_candidate_receipt_26_unique_18_originals_still_hold(owner,original,catalog,tmp_path):
    evidence=custody_receipt(store(tmp_path,owner),catalog,original)
    assert evidence["source_archive_sha256"]==PIN
    assert evidence["archived_module_directories"]==27
    assert evidence["unique_construction_ids"]==26
    assert evidence["unpublished_source_bound_candidates"]==18
    assert evidence["original_source_file_count"]==0
    assert evidence["witness_byte_hash_matched_core1a"]==27
    assert evidence["witness_byte_hash_matched_core1b"]==27
    assert evidence["original_modules_publication"]=="NOT_AUTHORIZED"
    assert evidence["academic_admission"]==evidence["independent_science_review"]=="HOLD"
    assert {r["science_issue"] for r in evidence["candidates"] if r["science_issue"]}==EXPECTED_BLOCKERS
    assert len(set(x["construction_id"] for x in evidence["candidates"]))==18
    assert {x["construction_id"] for x in evidence["candidates"]}=={
        x["construction"] for x in catalog["items"]}
    assert all(x["original_publication"]=="NOT_AUTHORIZED" for x in evidence["candidates"])
    assert all(x["science_issue"] in EXPECTED_BLOCKERS|{None} for x in evidence["candidates"])

@pytest.mark.parametrize("tamper",[
    "source_claim","publication_approved","science_approved","rights_approved",
    "source_custody_count","remove_blocker","change_archive_sha","duplicate_candidate",
    "alias_fabrication","remove_candidate","wrong_subject","false_candidate_approval"
])
def test_owner_archive_false_promotion_or_lost_science_blocker_fails_closed(
    owner,original,catalog,tmp_path,tamper):
    source=deepcopy(owner)
    if tamper=="source_claim":source["source_fidelity"]="PASS"
    if tamper=="publication_approved":source["original_modules_publication"]="APPROVED"
    if tamper=="science_approved":source["independent_science_review"]="PASS"
    if tamper=="rights_approved":source["rights_to_redistribute_original_exam_material"]="APPROVED"
    if tamper=="source_custody_count":source["original_source_file_count"]=30
    if tamper=="remove_blocker":source["known_blockers"].pop(next(iter(source["known_blockers"])))
    if tamper=="change_archive_sha":source["source_archive_sha256"]="a"*64
    if tamper=="duplicate_candidate":source["candidates"][0]=deepcopy(source["candidates"][1])
    if tamper=="alias_fabrication":source["duplicate_alias"]["canonical"]="another-module"
    if tamper=="remove_candidate":source["candidates"].pop()
    if tamper=="wrong_subject":source["candidates"][0]["subject"]="BIOLOGY"
    if tamper=="false_candidate_approval":source["candidates"][0]["academic_admission"]="PASS"
    with pytest.raises(ValueError):
        custody_receipt(store(tmp_path,source),catalog,original)

@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    folder=tmp_path_factory.mktemp("owner-core1-source-neutral")/"site"
    return folder,build(folder)

def test_site_stages_18_nonoriginal_authored_technical_lessons_and_safe_owner_receipt(staged):
    folder,manifest=staged
    supplement=manifest["independent_core1_supplements"]
    assert supplement["new_independent_authored_supplements"]==18
    assert supplement["source_originals_recovered"]==0
    assert supplement["original_missing_reproducible_modules"]==18
    assert supplement["owner_private_archive_candidate_count"]==18
    assert supplement["owner_original_source_custody"]=="HOLD"
    assert supplement["owner_science_blocker_count"]==4
    assert supplement["owner_candidate_receipt"] in manifest["files"]
    onstage=json.loads((folder/supplement["owner_candidate_receipt"]).read_text("utf8"))
    assert len(onstage["candidates"])==18
    assert onstage["academic_admission"]=="HOLD"
    text=(folder/"nsejs/core1-recovery.html").read_text("utf8")
    assert text.count("NOT PUBLISHED · source and academic HOLD")==18
    assert 'id="owner-private-core1-candidate-receipt"' in text
    assert "NEW source-neutral" in text
    assert "Four explicit science/source contradictions" in text
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    assert not list(folder.rglob("bank.json"))
    assert not list(folder.rglob("source-custody.json"))
    assert not list(folder.rglob("*.pdf"))
    assert not list(folder.rglob("*.zip"))
    assert not list(folder.rglob("core1a_construction.json"))
    assert not list(folder.rglob("core1b_reconstruction.json"))
