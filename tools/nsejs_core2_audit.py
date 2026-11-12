#!/usr/bin/env python3
"""NSEJS Physics Core2 source-indexed audit: mechanical evidence only; no academic PASS."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "preview/question-status.html"
TOPICS = ("OPTICS","ELECTROSTATICS","CURRENT_ELECTRICITY","MAGNETISM_AND_EMI","MECHANICS")
FACTORS = ("concept_model_selection","representation_translation","reasoning_chain_length",
           "algebra_computational_load","trap_exception_sensitivity")

def source_questions(html: str) -> list[dict]:
    match = re.search(r'<script\s+id="wpe-data"\s+type="application/json">([\s\S]*?)</script>', html)
    if not match:
        raise ValueError("SOURCE_PAYLOAD_MISSING")
    parsed = json.loads(match.group(1))
    if not isinstance(parsed.get("questions"), list):
        raise ValueError("QUESTION_LIST_MISSING")
    return [q for q in parsed["questions"] if q.get("topic") in TOPICS]

def uid(q: dict) -> str:
    s = q.get("source_id")
    if not isinstance(s,str) or not s.strip():
        raise ValueError("SOURCE_ID_MISSING")
    return "g9:PHYSICS:" + s

def canonical_payload(q: dict) -> dict:
    """Keep key order in sync with core2-physics-reader.js revisionPayload."""
    return {"uid":uid(q),"source_id":q["source_id"],"original_id":q.get("id"),
            "stem":q.get("stem"),"options":q.get("options"),"answer":q.get("answer"),
            "question_type":q.get("question_type"),"figures":q.get("source_figures") or [],
            "figure_note":q.get("figure_note") or "","reasoning":q.get("steps") or [],
            "boundary":q.get("check") or ""}

def revision(q: dict) -> str:
    canonical = json.dumps(canonical_payload(q),ensure_ascii=False,separators=(",",":"),allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def stem_digest(q: dict) -> str:
    return hashlib.sha256(q.get("stem","").encode("utf-8")).hexdigest()

def validate(questions: list[dict]) -> list[str]:
    problems, identities = [], []
    for i,q in enumerate(questions):
        label = q.get("source_id") or "row-"+str(i)
        try:
            identities.append(uid(q))
        except ValueError:
            problems.append("SOURCE_ID_MISSING:"+label)
        if not q.get("id") or not q.get("stem") or not q.get("options"):
            problems.append("INCOMPLETE_QUESTION:"+label)
        if len(q.get("options") or []) != 4:
            problems.append("OPTION_COUNT_NOT_FOUR:"+label)
        factors = q.get("components")
        if not isinstance(factors,dict) or set(factors)!=set(FACTORS):
            problems.append("QRT_FACTORS_MISSING:"+label)
        elif not all(type(v) is int and 0 <= v <= 2 for v in factors.values()):
            problems.append("QRT_FACTOR_RANGE_INVALID:"+label)
        elif sum(factors.values()) != q.get("score"):
            problems.append("QRT_FACTOR_SUM_MISMATCH:"+label)
        if q.get("band") not in ("D1","D2","D3","D4"):
            problems.append("QRT_BAND_MISSING:"+label)
    if len(identities)!=len(set(identities)):
        problems.append("CANONICAL_UID_COLLISION")
    return problems

def stem_mismatches(questions: list[dict]) -> list[str]:
    return [q["source_id"] for q in questions if q.get("stem_sha256")!=stem_digest(q)]

def rows(questions: list[dict]) -> list[dict]:
    result=[]
    for q in questions:
        figures=q.get("source_figures") or []
        r={"question_uid":uid(q),"source_id":q["source_id"],"displayed_id":q.get("id"),
           "topic":q.get("topic"),"provenance_claim":q.get("category","UNKNOWN"),
           "operation_nomination":q.get("op"),"band_nomination":q.get("band"),
           "score_nomination":q.get("score"),"figure_refs":"|".join(figures),
           "figure_custody":"NOT_RECEIVED" if figures else "NOT_APPLICABLE",
           "declared_stem_sha256":q.get("stem_sha256"),"computed_stem_sha256":stem_digest(q),
           "stem_digest_matches":stem_digest(q)==q.get("stem_sha256"),
           "full_content_revision":revision(q),
           "source_authenticity":"UNKNOWN_SOURCE","key_authenticity":"UNKNOWN_SOURCE",
           "qrt_adjudication":"HOLD","academic_release":"NOT_ADMITTED"}
        for f in FACTORS:r[f]=(q.get("components") or {}).get(f)
        result.append(r)
    return result

def summary(questions: list[dict]) -> dict:
    bands=collections.Counter(q.get("band") for q in questions)
    names=collections.Counter(q.get("id") for q in questions)
    return {"scope":"PHYSICS_CANDIDATE_ONLY","candidate_questions":len(questions),
            "unique_internal_uids":len({uid(q) for q in questions}),
            "distinct_displayed_ids":len(names),
            "repeated_display_ids":sorted(k for k,n in names.items() if n>1),
            "producer_band_nominations":dict(sorted(bands.items())),
            "topics":{t:{"count":sum(q["topic"]==t for q in questions),
                         "D3_nominated":sum(q["topic"]==t and q.get("band")=="D3" for q in questions),
                         "D4_nominated":sum(q["topic"]==t and q.get("band")=="D4" for q in questions)}
                      for t in TOPICS},
            "declared_stem_hash_mismatches":stem_mismatches(questions),
            "missing_verified_original_figures":sum(bool(q.get("source_figures")) for q in questions),
            "source_paper_denominator":"NOT_RECEIVED","authenticated_originals":0,
            "independently_qualified_D3_D4":0,"qrt_academic_release":"HOLD"}

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,default=SOURCE)
    ap.add_argument("--census",type=Path)
    ap.add_argument("--json",type=Path)
    ap.add_argument("--strict-digest",action="store_true")
    args=ap.parse_args()
    try:
        q=source_questions(args.source.read_text(encoding="utf-8"))
        problems=validate(q)
        report=summary(q)
        report["structural_problems"]=problems
        if args.census:
            data=rows(q);args.census.parent.mkdir(parents=True,exist_ok=True)
            with args.census.open("w",encoding="utf-8",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
        if args.json:
            args.json.parent.mkdir(parents=True,exist_ok=True)
            args.json.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(report,indent=2))
        return 2 if problems else (3 if args.strict_digest and stem_mismatches(q) else 0)
    except (ValueError,KeyError,OSError,TypeError) as exc:
        print("NSEJS_CORE2_AUDIT_FAILURE:"+str(exc),file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
