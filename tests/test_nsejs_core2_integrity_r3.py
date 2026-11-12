"""Core2 R3 hardening: displayed-data integrity is separate from original exam authenticity."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
import build_nsejs_core2_integrity as integrity

def get_data():
    data=(ROOT/"nsejs/data/physics-core2-candidates.v1.json").read_bytes()
    provenance=(ROOT/"nsejs/data/physics-core2-source-evidence.v1.json").read_bytes()
    committed=(ROOT/"nsejs/data/physics-core2-integrity.v1.json").read_bytes()
    return data,provenance,committed

def test_exact_reproducible_derived_integrity_manifest():
    candidates,source,ledger=get_data()
    expected=(json.dumps(integrity.derive(candidates,source),ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    assert ledger==expected, "Pinned public candidate integrity manifest differs from exact source bytes"
    assert integrity.derive(candidates,source)==json.loads(ledger)
    assert hashlib.sha256(candidates).hexdigest()==json.loads(ledger)["corpus_sha256"]
    assert hashlib.sha256(source).hexdigest()==json.loads(ledger)["provenance_sha256"]

def test_declared_hash_conflicts_preserved_not_laundered():
    candidates,source,ledger=get_data()
    r=json.loads(ledger)
    assert len(r["items"])==50
    assert sum(not q["declared_matches_observed"] for q in r["items"])==48
    assert len({x["question_uid"] for x in r["items"]})==50
    original=json.loads(candidates)
    for question,item in zip(original["questions"],r["items"]):
        assert item["producer_declared_stem_sha256"]==question["stem_sha256"]
        assert item["observed_stem_sha256"]==hashlib.sha256(question["stem"].encode("utf-8")).hexdigest()
        assert item["academic_admission"]=="NOT_ADMITTED"
        assert item["source_exact_fidelity"]=="HOLD"

def test_score_band_contradictions_remain_explicit_holds():
    r=json.loads(get_data()[2])
    bad={q["source_id"]:(q["producer_qrt_band"],q["score_based_band"]) for q in r["items"] if not q["qrt_nomination_consistent"]}
    assert bad=={
        "NSEJS-19-OPT-02":("D3","D1"),
        "NSEJS-FND-ELEC-04":("D3","D2"),
        "NSEJS-FND-CIRC-01":("D3","D2"),
        "NSEJS-FND-CIRC-02":("D3","D2"),
    }
    assert all(q["qrt_adjudication"]=="HOLD" for q in r["items"])
    assert not any(q["score_based_band"]=="D4" for q in r["items"])

def test_official_paper_custody_categories_and_missing_graph():
    r=json.loads(get_data()[2]);rows={x["source_id"]:x for x in r["items"]}
    assert sum(q["source_evidence_status"]=="LOCATOR_AND_KEY_CROSSCHECKED" for q in rows.values())==11
    assert sum(q["source_evidence_status"]=="OFFICIAL_ID_CONTRADICTED" for q in rows.values())==2
    assert sum(q["source_evidence_status"]=="UNVERIFIED_SOURCE_CLAIM" for q in rows.values())==37
    assert {x["source_id"] for x in rows.values() if x["figure_dependency_missing"]}=={
        "NSEJS-23-OPT-01","NSEJS-24-ELEC-01","NSEJS-24-CIRC-01",
        "NSEJS-24-MAG-01","NSEJS-24-MECH-01","NSEJS-24-MECH-07"
    }
    assert rows["NSEJS-24-MECH-07"]["official_paper_question"]==34
    assert rows["NSEJS-24-MECH-07"]["figure_dependency_missing"]
    assert {rows[x]["source_evidence_status"] for x in ("NSEJS-24-OPT-01","NSEJS-24-OPT-02")}=={"OFFICIAL_ID_CONTRADICTED"}

def test_modified_candidate_stem_breaks_manifest_without_source_rewrite():
    c,s,ledger=get_data()
    copy_source=json.loads(c)
    copy_source["questions"][0]["stem"]+=" tampered source"
    raw=(json.dumps(copy_source,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    altered=integrity.derive(raw,s)
    assert altered["corpus_sha256"]!=json.loads(ledger)["corpus_sha256"]
    assert altered["items"][0]["observed_stem_sha256"]!=json.loads(ledger)["items"][0]["observed_stem_sha256"]
    assert altered["items"][0]["producer_declared_stem_sha256"]==json.loads(ledger)["items"][0]["producer_declared_stem_sha256"]

def test_fake_official_key_is_rejected_by_builder():
    c,s,_=get_data()
    modified=json.loads(s)
    modified["source_ledger"][0]["official_key"]="D"
    try:
        integrity.derive(c,(json.dumps(modified)+"\n").encode("utf-8"))
        assert False,"Bad verified key was accepted"
    except ValueError as exc:
        assert "OFFICIAL_KEY_MAPPING_CONFLICT" in str(exc)

def test_invalid_evidence_identifier_is_rejected():
    c,s,_=get_data();modified=json.loads(s)
    modified["source_ledger"][0]["source_id"]="NOT-A-QUESTION"
    try:
        integrity.derive(c,(json.dumps(modified)+"\n").encode("utf-8"))
        assert False,"Unmapped source proof accepted"
    except ValueError as exc:
        assert "EVIDENCE_ID_CONFLICT" in str(exc)

def test_reader_requires_reconciled_manifest_and_shows_qrt_holds():
    js=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    for term in ("SOURCE_CONTENT_INTEGRITY_MISMATCH","SOURCE_ITEM_INTEGRITY_MISMATCH","QRT CONFLICT","SOURCE CLAIM INVALID","figure_dependency_missing","producer_declared_stem_sha256"):
        assert term in js
    assert "preview/question-status.html" not in js
