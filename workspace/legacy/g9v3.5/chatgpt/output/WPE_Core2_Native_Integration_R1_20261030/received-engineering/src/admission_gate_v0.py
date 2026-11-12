"""WPE Core2 proposed *preflight* gate (separate new return; never edits native SL1/SL2).

This is NOT the native R2 validator, an authentication service, or academic admission.
Evidence signatures, official provenance and reviewer independence require human verification.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from typing import Any

OPS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
FACTORS = ("concept_model_selection", "representation_translation", "reasoning_chain_length", "algebra_computational_load", "trap_exception_sensitivity")
BANDS = {0:"D1",1:"D1",2:"D1",3:"D2",4:"D2",5:"D2",6:"D3",7:"D3",8:"D4",9:"D4",10:"D4"}


def digest_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()).hexdigest()


def dependency_fingerprint(r:dict) -> str:
    """Proposed product preflight fingerprint; does NOT replace native SL1/SL2 digest."""
    s=r.get("source",{}); c=r.get("curriculum",{});
    return digest_json({
        "canonical_id":r.get("canonical_id"),
        "question_digest":s.get("question_digest"),
        "options_digest":s.get("options_digest"),
        "figure_digests":s.get("figure_digests",[]),
        "paper_sha256":s.get("official_paper",{}).get("artifact_sha256"),
        "key_sha256":s.get("official_key",{}).get("artifact_sha256"),
        "answer_claim_digest":s.get("inherited_answer_digest"),
        "rubric_sha256":c.get("rubric_sha256"),
        "blueprint_sha256":c.get("blueprint_sha256"),
        "adapter_sha256":c.get("adapter_sha256"),
    })


def _witness_valid(w:Any) -> bool:
    return isinstance(w,dict) and w.get("upstream_status")=="AUTHENTICATED" and all(
        isinstance(w.get(key),str) and bool(w[key].strip()) for key in
        ("artifact_sha256", "locator", "source_authority", "witness_ref", "artifact_ref")
    ) and len(w["artifact_sha256"])==64


def evaluate_candidate(r:dict) -> dict:
    """A human-reviewable technical preflight, *not* conferral of academic approval."""
    errors=[]; s=r.get("source",{}); c=r.get("curriculum",{}); a=r.get("assessment",{}); g=r.get("governance",{});
    ident=r.get("canonical_id")
    def need(test:bool, reason:str):
        if not test: errors.append(reason)
    need(bool(ident),"IDENTITY_MISSING")
    need(not r.get("duplicate_of"),"ALIAS_NOT_PRIMARY")
    need(r.get("origin")=="EXAM_ORIGINAL_AUTHENTICATED", "EXAM_AUTHENTICITY_UNPROVEN")
    need(r.get("source_role")=="DIRECT_EXAM", "NOT_DIRECT_EXAM_EVIDENCE")
    need(bool(s.get("question_digest")), "QUESTION_DIGEST_MISSING")
    need(bool(s.get("options_digest")), "OPTIONS_DIGEST_MISSING")
    paper=s.get("official_paper")
    key=s.get("official_key")
    need(_witness_valid(paper),"OFFICIAL_PAPER_CUSTODY_OPEN")
    need(_witness_valid(key),"OFFICIAL_KEY_CUSTODY_OPEN")
    if _witness_valid(paper) and _witness_valid(key):
        need(paper["artifact_ref"]!=key["artifact_ref"], "PAPER_AND_KEY_NOT_DISTINCT")
        need(paper["witness_ref"]!=key["witness_ref"], "PAPER_AND_KEY_WITNESS_NOT_DISTINCT")
    need(s.get("required_figures_bound") is True, "ORIGINAL_FIGURE_OR_OPTIONS_UNBOUND")
    if s.get("requires_figure") is True:
        need(bool(s.get("figure_digests")), "REQUIRED_FIGURE_DIGEST_MISSING")
    need(s.get("answer_reconciliation")=="AGREED_VERSIONED", "ANSWER_CLAIM_OR_KEY_DISPUTE_OPEN")
    need(bool(s.get("inherited_answer_digest")), "INHERITED_ANSWER_NOT_PRESERVED")
    need(c.get("adapter_owner_approved") is True and bool(c.get("adapter_owner_approval_ref")), "ADAPTER_AUTHORITY_OPEN")
    for k in ("rubric_sha256", "blueprint_sha256", "adapter_sha256"):
        need(isinstance(c.get(k),str) and len(c[k])==64, f"{k.upper()}_UNPINNED")
    need(c.get("semantic_cell_resolved") is True, "CURRICULUM_CELL_UNRESOLVED")
    need(bool(c.get("capability_ref")), "CAPABILITY_REF_MISSING")
    need(bool(g.get("owner_execution_authorization_ref")), "EXECUTION_AUTHORITY_MISSING")
    need(bool(g.get("reviewer_appointment_ref")), "REVIEWER_NOT_APPOINTED")
    need(bool(g.get("reviewer_identity")) and g.get("reviewer_identity")!=g.get("author_identity"), "REVIEWER_NOT_DISTINCT")
    need(g.get("reviewer_exposed_to_author_proposals") is False, "BLIND_REVIEW_NOT_ESTABLISHED")
    need(bool(g.get("reviewer_attestation_ref")) and bool(g.get("first_pass_record_ref")), "REVIEW_FIRST_PASS_NOT_SEALED")
    need(a.get("subject_sha256")==dependency_fingerprint(r), "REVIEW_SUBJECT_FINGERPRINT_STALE")
    scores=a.get("factors",{}); evidence=a.get("factor_evidence",{})
    need(set(scores)==set(FACTORS) and all(type(scores.get(f)) is int and 0<=scores[f]<=2 for f in FACTORS), "SL2_FACTORS_INVALID")
    need(all(isinstance(evidence.get(f),str) and len(evidence[f].strip())>=12 for f in FACTORS),"SL2_FACTOR_EVIDENCE_INCOMPLETE")
    if set(scores)==set(FACTORS) and all(type(scores.get(f)) is int and 0<=scores[f]<=2 for f in FACTORS):
        total=sum(scores.values()); band=BANDS[total]
        need(a.get("total")==total,"SL2_TOTAL_MISMATCH")
        need(a.get("band")==band,"SL2_BAND_MISMATCH")
        need(total>=6,"D1_D2_CANNOT_COUNT")
    else:
        total=None; band=None
    need(a.get("primary_operation") in OPS,"PRIMARY_OPERATION_INVALID")
    need(a.get("independent_solution_recorded") is True,"INDEPENDENT_SOLUTION_MISSING")
    need(bool(a.get("decisive_move_evidence")),"COGNITIVE_CRUX_NOT_EVIDENCED")
    need(bool(a.get("competing_classifications_recorded")),"COMPETING_OPERATIONS_NOT_RECORDED")
    need(g.get("qrt_adjudication")=="ADMITTED" and bool(g.get("qrt_adjudication_ref")),"QRT_ADMISSION_MISSING")
    need(a.get("primary_operation")==g.get("primary_counting_operation"),"COUNTING_HOME_OPERATION_CONFLICT")
    need(g.get("owner_core2_acceptance")=="APPROVED" and bool(g.get("owner_core2_acceptance_ref")), "OWNER_CORE2_ACCEPTANCE_MISSING")
    return {"id":ident, "preflight":"HOLD" if errors else "METADATA_PRECHECK_ONLY", "reasons":sorted(set(errors)),
            "score":total,"band":band,"primary_operation":a.get("primary_operation"),
            "meaning":"Even METADATA_PRECHECK_ONLY never authenticates evidence, grants admission or authorizes release."}


def evaluate_selection(records:list[dict]) -> dict:
    results=[evaluate_candidate(r) for r in records]
    ids=[r.get("canonical_id") for r in records]
    count=Counter(r.get("assessment",{}).get("primary_operation") for r in records)
    errors=[]
    if len(records)!=21: errors.append("REQUIRES_21_PRIMARY_SELECTIONS")
    if len(ids)!=len(set(ids)): errors.append("DUPLICATE_COUNTING_ID")
    for op in OPS:
        if count[op]!=3: errors.append("OPERATION_QUOTA_NOT_MET:"+op)
    if any(x["preflight"]!="METADATA_PRECHECK_ONLY" for x in results): errors.append("ITEMS_ON_HOLD")
    return {"selection_preflight":"HOLD" if errors else "METADATA_PRECHECK_ONLY", "errors":errors,
            "records":results,"counts_by_operation":{k:count[k] for k in OPS},
            "academic_admission":"NOT_DETERMINED_BY_CODE", "owner_approval":"NOT_DETERMINED_BY_CODE"}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output");args=p.parse_args()
    obj=json.load(open(args.input,encoding="utf8"))
    result=evaluate_selection(obj["records"] if isinstance(obj,dict) else obj)
    output=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output: open(args.output,"w",encoding="utf8").write(output+"\n")
    else:print(output)
    raise SystemExit(0 if result["selection_preflight"]=="METADATA_PRECHECK_ONLY" else 2)
