#!/usr/bin/env python3
"""Deterministic NSEJS Physics candidate-data integrity and source-evidence builder.

Keeps producer-declared hashes and QRT bands unchanged. Computes observed
display hashes and mechanically consistent rubric bands. This checks source
data *integrity* and ledger relationships, not original-paper authenticity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "nsejs/data/physics-core2-candidates.v1.json"
EVIDENCE = ROOT / "nsejs/data/physics-core2-source-evidence.v1.json"
OUTPUT = ROOT / "nsejs/data/physics-core2-integrity.v1.json"
BANDS = {"D1": (0,2), "D2": (3,5), "D3": (6,7), "D4": (8,10)}

from nsejs_core2_audit import revision, validate

def sha(data: bytes)->str:
    return hashlib.sha256(data).hexdigest()

def grade(score):
    if type(score) is not int:
        return "INVALID_SCORE"
    return next((name for name,(lo,hi) in BANDS.items() if lo<=score<=hi), "INVALID_SCORE")

def derive(corpus_bytes:bytes, evidence_bytes:bytes)->dict:
    corpus=json.loads(corpus_bytes)
    evidence=json.loads(evidence_bytes)
    if corpus.get("schema_version")!="grade9-nsejs-physics-core2-candidate-corpus/v1":
        raise ValueError("UNSUPPORTED_CORPUS")
    if evidence.get("schema_version")!="grade9-nsejs-physics-source-evidence/v1":
        raise ValueError("UNSUPPORTED_EVIDENCE")
    questions=corpus.get("questions")
    if not isinstance(questions,list) or len(questions)!=50:
        raise ValueError("CORPUS_NOT_50")
    if problems:=validate(questions):
        raise ValueError("CORPUS_SHAPE_INVALID:"+str(problems))
    question_ids={q["source_id"] for q in questions}
    official={r["source_id"]:r for r in evidence.get("source_ledger",[])}
    invalid={r["source_id"]:r for r in evidence.get("known_false_exam_locators",[])}
    if len(official)!=len(evidence.get("source_ledger",[])) or len(invalid)!=len(evidence.get("known_false_exam_locators",[])):
        raise ValueError("EVIDENCE_ID_DUPLICATE")
    if not (set(official)|set(invalid)) <= question_ids or set(official)&set(invalid):
        raise ValueError("EVIDENCE_ID_CONFLICT")
    records=[]
    for q in questions:
        sid=q["source_id"]
        checked=official.get(sid)
        contradiction=invalid.get(sid)
        if checked:
            m=re.search(r"\(([A-D])\)",q.get("answer",""),re.I)
            if not m or m.group(1).upper()!=checked["official_key"]:
                raise ValueError("OFFICIAL_KEY_MAPPING_CONFLICT:"+sid)
        observed=sha(q["stem"].encode("utf-8"))
        missing=bool(q.get("source_figures")) or bool(checked and checked.get("requires_original_figure"))
        records.append({
            "question_uid":"g9:PHYSICS:"+sid,
            "source_id":sid,
            "historical_display_id":q["id"],
            "producer_declared_stem_sha256":q.get("stem_sha256"),
            "observed_stem_sha256":observed,
            "declared_matches_observed":q.get("stem_sha256")==observed,
            "observed_question_revision_sha256":revision(q),
            "source_evidence_status":(
                "OFFICIAL_ID_CONTRADICTED" if contradiction else
                "LOCATOR_AND_KEY_CROSSCHECKED" if checked else
                "UNVERIFIED_SOURCE_CLAIM"
            ),
            "official_paper_year":checked["paper_year"] if checked else None,
            "official_paper_code":checked["paper_code"] if checked else None,
            "official_paper_question":checked["question_no"] if checked else None,
            "figure_dependency_missing":missing,
            "producer_qrt_band":q["band"],
            "producer_qrt_operation":q["op"],
            "five_factor_score":q["score"],
            "score_based_band":grade(q["score"]),
            "qrt_nomination_consistent":q["band"]==grade(q["score"]),
            "qrt_adjudication":"HOLD",
            "source_exact_fidelity":"HOLD",
            "academic_admission":"NOT_ADMITTED",
        })
    return {
        "schema_version":"grade9-nsejs-physics-core2-integrity/v1",
        "corpus_path":"nsejs/data/physics-core2-candidates.v1.json",
        "provenance_path":"nsejs/data/physics-core2-source-evidence.v1.json",
        "corpus_sha256":sha(corpus_bytes),
        "provenance_sha256":sha(evidence_bytes),
        "source_claims":"UNQUALIFIED_CANDIDATE_ONLY",
        "source_digest_policy":"RECORDED_PRODUCER_CLAIM_VS_CURRENT_DISPLAY_DIGEST; NO_CANONICAL_EXAM_AUTHENTICATION",
        "qrt_band_policy":"PRODUCER_NOMINATION_RETAINED; SCORE_BAND_IS_MECHANICAL_DIAGNOSTIC_ONLY",
        "academic_admission":"HOLD",
        "items":records
    }

def census(ledger:dict)->dict:
    items=ledger["items"]
    return {
        "questions":len(items),
        "producer_stem_digest_conflicts":sum(not r["declared_matches_observed"] for r in items),
        "qrt_rubric_contradictions":sum(not r["qrt_nomination_consistent"] for r in items),
        "checked_paper_locators":sum(r["source_evidence_status"]=="LOCATOR_AND_KEY_CROSSCHECKED" for r in items),
        "contradicted_paper_locators":sum(r["source_evidence_status"]=="OFFICIAL_ID_CONTRADICTED" for r in items),
        "unverified_source_claims":sum(r["source_evidence_status"]=="UNVERIFIED_SOURCE_CLAIM" for r in items),
        "blocked_figures":sum(r["figure_dependency_missing"] for r in items),
        "admissions":sum(r["academic_admission"]=="ADMITTED" for r in items),
        "qualified_d4":0
    }

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--write",action="store_true")
    p.add_argument("--academic-gate",action="store_true")
    args=p.parse_args()
    try:
        derived=derive(CANDIDATES.read_bytes(), EVIDENCE.read_bytes())
        expected=(json.dumps(derived,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
        if args.write:
            OUTPUT.write_bytes(expected)
        if args.check and OUTPUT.read_bytes()!=expected:
            print("FAIL_CLOSED: INTEGRITY_LEDGER_STALE_OR_TAMPERED",file=sys.stderr)
            return 2
        stats=census(derived)
        print(json.dumps(stats,indent=2))
        if args.academic_gate:
            if stats["producer_stem_digest_conflicts"] or stats["qrt_rubric_contradictions"] or stats["unverified_source_claims"] or stats["contradicted_paper_locators"] or stats["admissions"]<stats["questions"]:
                print("ACADEMIC_HOLD: No source or QRT admission is implied",file=sys.stderr)
                return 4
        print("PASS: exact observed-data integrity and deterministic canonical ledger (academic HOLD)")
        return 0
    except (ValueError,TypeError,KeyError,OSError,UnicodeError) as ex:
        print("FAIL_CLOSED: "+str(ex),file=sys.stderr)
        return 2

if __name__=="__main__":raise SystemExit(main())
