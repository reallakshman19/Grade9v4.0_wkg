"""WPE Core2 source-to-product prototype (local candidate, no production authority).

Retains inherited question representations. This engine NEVER authenticates an
exam, confers independent academic review, or grants Owner release. It validates
metadata, delegates custody/academic decisions to external named records, and
fails closed on absent evidence. Uses a derived fingerprint, not SL1/SL2 digests.
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

OPS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
FACTORS = ("concept_model_selection", "representation_translation", "reasoning_chain_length", "algebra_computational_load", "trap_exception_sensitivity")
BANDS = {i: ("D1" if i <= 2 else "D2" if i <= 5 else "D3" if i <= 7 else "D4") for i in range(11)}
HEX64 = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$", re.I)
STAGES = ("ORIENT", "CONNECT", "NEXT_MOVE")


def canonical_digest(v: Any) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def sha_ok(value: Any) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def fingerprint(r: dict) -> str:
    """Derived acceptance subject. Explicitly NOT native SL1/SL2 digest semantics."""
    s, c, a, q = (r.get(x) or {} for x in ("source", "curriculum", "assessment", "question"))
    return canonical_digest({
        "id": r.get("canonical_id"), "question": q,
        "question_digest": s.get("question_digest"), "options_digest": s.get("options_digest"),
        "figures": s.get("figure_digests", []), "paper": s.get("official_paper"),
        "key": s.get("official_key"), "answer_versions": s.get("answer_versions"),
        "blueprint": c.get("blueprint_sha256"), "adapter": c.get("adapter_sha256"),
        "rubric": c.get("rubric_sha256"), "capability": c.get("capability_ref"),
        "concept": c.get("microtopic_ref"), "score": a.get("factors"),
        "primary": a.get("primary_operation"), "grade_policy": r.get("grading_policy"),
    })


def _witness(w: Any) -> bool:
    return isinstance(w, dict) and w.get("upstream_status") == "AUTHENTICATED" and all(
        bool(w.get(f)) for f in ("artifact_ref", "artifact_sha256", "witness_ref", "locator", "source_authority")
    ) and sha_ok(w.get("artifact_sha256"))


def _source_question(q: dict) -> list[str]:
    e = []
    def req(t, label):
        if not t: e.append(label)
    req(isinstance(q, dict), "QUESTION_NOT_OBJECT")
    if not isinstance(q, dict): return e
    for k in ("id", "stem", "original_identifier", "origin"):
        req(isinstance(q.get(k), str) and bool(q[k].strip()), "QUESTION_" + k.upper() + "_MISSING")
    req(q.get("origin") in ("EXAM_ORIGINAL", "OWNER_SUPPLIED", "AUTHORED_TECHNICAL_FIXTURE"), "QUESTION_ORIGIN_INVALID")
    typ = (q.get("extensions") or {}).get("wpe:response_type")
    req(typ in ("SINGLE_CHOICE", "MULTIPLE_CHOICE", "NUMERIC", "TEXT"), "RESPONSE_TYPE_MISSING")
    opts = q.get("options")
    if typ in ("SINGLE_CHOICE", "MULTIPLE_CHOICE"):
        req(isinstance(opts, list) and len(opts) >= 2, "MCQ_OPTIONS_MISSING")
        if isinstance(opts, list):
            strings = [(x.get("id") if isinstance(x, dict) else None) for x in opts]
            req(all(isinstance(x, str) and x.strip() for x in strings) and len(set(strings)) == len(strings), "OPTION_IDS_INVALID")
    for name in ("subparts", "conditions", "figure_refs", "hints", "scaffolds"):
        req(isinstance(q.get(name), list), "QUESTION_"+name.upper()+"_INVALID")
    return e


def evaluate_record(r: dict) -> dict:
    reasons: list[str] = []
    def req(t, code):
        if not t: reasons.append(code)
    s, c, a, g, q = (r.get(x) or {} for x in ("source", "curriculum", "assessment", "governance", "question"))
    ident = r.get("canonical_id")
    req(isinstance(ident,str) and bool(ident), "IDENTITY_MISSING")
    req(not r.get("duplicate_of"), "DUPLICATE_ALIAS_NOT_PRIMARY")
    req(r.get("origin") == "EXAM_ORIGINAL_AUTHENTICATED", "ORIGINAL_AUTHENTICITY_OPEN")
    req(r.get("source_role") == "DIRECT_EXAM", "DIRECT_EXAM_NOT_ESTABLISHED")
    reasons += _source_question(q)
    req(q.get("origin") == "EXAM_ORIGINAL", "NON_EXAM_SOURCE_CANNOT_COUNT")
    req(q.get("id") == ident, "IDENTITY_QUESTION_MISMATCH")
    req(sha_ok(s.get("question_digest")) and s.get("question_digest", "").split(":")[-1] == canonical_digest({k:q.get(k) for k in ("stem","subparts","conditions","original_identifier")}), "SOURCE_TEXT_DIGEST_MISMATCH")
    req(sha_ok(s.get("options_digest")) and s.get("options_digest", "").split(":")[-1] == canonical_digest(q.get("options")), "SOURCE_OPTION_DIGEST_MISMATCH")
    # This compiler emits embedded verbatim text. Other lawful custody modes need
    # a different external-reference projection, never a silent verbatim copy.
    req(s.get("custody_mode") == "EMBEDDED_VERBATIM", "EXTERNAL_REFERENCE_CUSTODY_NOT_IMPLEMENTED")
    req(s.get("rights_status") == "AUTHORIZED_TO_EMBED" and bool(s.get("rights_authorization_ref")), "SOURCE_REPRODUCTION_RIGHTS_OPEN")
    req(_witness(s.get("official_paper")), "OFFICIAL_PAPER_CUSTODY_OPEN")
    req(_witness(s.get("official_key")), "OFFICIAL_KEY_CUSTODY_OPEN")
    if _witness(s.get("official_paper")) and _witness(s.get("official_key")):
        req(s["official_paper"]["witness_ref"] != s["official_key"]["witness_ref"], "PAPER_KEY_WITNESSES_NOT_DISTINCT")
    required = q.get("figure_refs") or []
    req(s.get("required_figures_bound") is True, "SOURCE_FIGURES_OR_OPTIONS_UNBOUND")
    req(len(s.get("figure_digests") or []) == len(required) and all(sha_ok(x) for x in (s.get("figure_digests") or [])), "FIGURE_DIGESTS_INCOMPLETE")
    versions=s.get("answer_versions") or {}
    req(bool(versions.get("inherited_claim_digest")) and sha_ok(versions.get("inherited_claim_digest")),"INHERITED_ANSWER_MISSING")
    req(bool(versions.get("official_claim_digest")) and sha_ok(versions.get("official_claim_digest")),"OFFICIAL_ANSWER_MISSING")
    req(versions.get("reconciliation") == "AGREED_VERSIONED", "ANSWER_RECONCILIATION_OPEN")
    req(bool(versions.get("reconciliation_ref")), "ANSWER_RECONCILIATION_UNBOUND")
    for fld in ("blueprint_sha256","adapter_sha256","rubric_sha256"):
        req(sha_ok(c.get(fld)), "PIN_MISSING_"+fld.upper())
    req(c.get("adapter_owner_approved") is True and bool(c.get("adapter_owner_approval_ref")), "ADAPTER_AUTHORITY_OPEN")
    req(c.get("semantic_cell_resolved") is True and bool(c.get("cell_ref")), "QRT_CELL_NOT_RESOLVED")
    req(bool(c.get("capability_ref")) and bool(c.get("microtopic_ref")),"CANONICAL_CURRICULUM_REF_MISSING")
    op=a.get("primary_operation")
    req(op in OPS,"OPERATION_INVALID")
    scores=a.get("factors") or {}
    ok_scores=isinstance(scores,dict) and set(scores)==set(FACTORS) and all(type(scores[f]) is int and 0 <= scores[f] <= 2 for f in FACTORS)
    req(ok_scores,"SL2_FACTOR_VALUES_INVALID")
    total=sum(scores.values()) if ok_scores else None
    band=BANDS[total] if total is not None else None
    req(total is not None and total >= 6,"NOT_D3_D4")
    req(a.get("total")==total and a.get("band")==band, "SL2_BAND_SCORE_MISMATCH")
    explanations=a.get("factor_evidence") or {}
    req(all(isinstance(explanations.get(f),str) and len(explanations[f].strip()) >= 12 for f in FACTORS),"SL2_EVIDENCE_MISSING")
    req(bool(a.get("independent_solution_ref")),"INDEPENDENT_SOLUTION_MISSING")
    req(bool(a.get("decisive_move_evidence")),"DECISIVE_MOVE_MISSING")
    req(isinstance(a.get("competing_operations"),list),"COMPETING_OPERATIONS_MISSING")
    req(a.get("subject_sha256")==fingerprint(r),"ASSESSMENT_SUBJECT_STALE")
    req(bool(g.get("owner_execution_authorization_ref")),"EXECUTION_AUTHORITY_OPEN")
    req(bool(g.get("reviewer_appointment_ref")),"REVIEWER_APPOINTMENT_OPEN")
    req(bool(g.get("reviewer_identity")) and g.get("reviewer_identity") != g.get("author_identity"),"REVIEWER_INDEPENDENCE_OPEN")
    # Exposure is disclosed, not erased: a different principal may evaluate exposed questions.
    req(g.get("reviewer_exposure_disclosed") is True,"REVIEWER_EXPOSURE_UNDISCLOSED")
    req(bool(g.get("reviewer_first_pass_ref")) and bool(g.get("reviewer_attestation_ref")),"REVIEW_FIRST_PASS_UNBOUND")
    req(g.get("qrt_adjudication")=="ADMITTED" and bool(g.get("qrt_adjudication_ref")),"QRT_ADMISSION_OPEN")
    req(g.get("primary_counting_operation")==op,"COUNTING_HOME_MISMATCH")
    grade=r.get("grading_policy") or {}
    req(grade.get("type")==(q.get("extensions") or {}).get("wpe:response_type"),"GRADING_TYPE_MISMATCH")
    if grade.get("type") in ("SINGLE_CHOICE","MULTIPLE_CHOICE"):
        options={x["id"] for x in (q.get("options") or []) if isinstance(x,dict) and isinstance(x.get("id"),str)}
        valid=grade.get("correct_ids")
        req(isinstance(valid,list) and bool(valid) and set(valid)<=options and len(set(valid))==len(valid),"ANSWER_OPTION_ID_INVALID")
        req(not (grade["type"]=="SINGLE_CHOICE" and isinstance(valid,list) and len(valid)!=1),"SINGLE_CHOICE_KEY_INVALID")
    if grade.get("type")=="NUMERIC":
        req(isinstance(grade.get("exact_value"),(int,float)) and type(grade.get("exact_value")) is not bool,"NUMERIC_KEY_INVALID")
        req(isinstance(grade.get("tolerance"),(int,float)) and grade.get("tolerance") >= 0,"NUMERIC_TOLERANCE_UNBOUND")
    if grade.get("type")=="TEXT":
        req(grade.get("grading_mode")=="HUMAN_REVIEW", "TEXT_AUTO_GRADING_FORBIDDEN")
    for i,h in enumerate(q.get("scaffolds") or []):
        if not isinstance(h,dict) or h.get("reveals") not in ("CONCEPT","METHOD") or h.get("availability") not in ("PRE_ATTEMPT_SAFE", "AFTER_ATTEMPT", "POST_SOLUTION"):
            reasons.append(f"INVALID_SCAFFOLD_{i}")
        elif h.get("availability")=="PRE_ATTEMPT_SAFE" and h.get("completes_protected_move"):
            reasons.append(f"PROTECTED_CRUX_LEAK_{i}")
    return {"id":ident,"state":"BLOCKED" if reasons else "BUILD_ELIGIBLE_METADATA_ONLY", "reasons":sorted(set(reasons)),"score":total,"band":band,"operation":op,"fingerprint":fingerprint(r)}


def evaluate_selection(records: list[dict]) -> dict:
    out=[evaluate_record(r) for r in records]
    groups=Counter(r.get("assessment",{}).get("primary_operation") for r in records)
    ids=[r.get("canonical_id") for r in records]
    errors=[]
    if len(records)!=21: errors.append("SELECTION_NOT_21")
    if len(ids)!=len(set(ids)): errors.append("DUPLICATE_PRIMARY_COUNT")
    if any(r.get("duplicate_of") for r in records): errors.append("ALIAS_COUNTED_AS_PRIMARY")
    for op in OPS:
        if groups[op] != 3: errors.append(f"OPERATION_QUOTA:{op}")
    if any(x["state"]!="BUILD_ELIGIBLE_METADATA_ONLY" for x in out): errors.append("ITEMS_BLOCKED")
    return {"state":"BLOCKED" if errors else "BUILD_ELIGIBLE_METADATA_ONLY","errors":errors,"by_operation":{k:groups[k] for k in OPS},"items":out,"academic_verification":"EXTERNAL","owner_release":"NOT_EVALUATED"}


def verify_assets(records: list[dict], assets_root: str | None = None) -> None:
    """Check every referenced original figure against local bytes, never URLs.

    A reference may be a relative file path within assets_root. An external-only
    reference is not eligible for embedding in this local product builder.
    """
    from pathlib import Path
    for r in records:
        q=r.get("question") or {}
        figs=q.get("figure_refs") or []
        if not figs: continue
        if not assets_root: raise ValueError("ORIGINAL_ASSET_ROOT_MISSING:"+str(r.get("canonical_id")))
        base=Path(assets_root).resolve()
        digests=(r.get("source") or {}).get("figure_digests") or []
        for rel,digest in zip(figs,digests):
            if not isinstance(rel,str) or rel.startswith(('http:', 'https:', '/', '\\')):
                raise ValueError("EXTERNAL_OR_ABSOLUTE_ASSET_NOT_EMBEDDED:"+str(rel))
            path=(base/rel).resolve()
            if not path.is_relative_to(base) or not path.is_file():
                raise ValueError("ORIGINAL_ASSET_MISSING_OR_TRAVERSAL:"+str(rel))
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest.split(':')[-1]:
                raise ValueError("ORIGINAL_ASSET_HASH_MISMATCH:"+str(rel))


def make_derived_package(records: list[dict], library: dict, existing_manifest: dict, bank_meta: dict, *, assets_root: str | None = None) -> dict:
    """Pure build transform. Called only after verified external review package.

    Produces a *candidate* bank and a cloned library whose existing content and
    review enums are left untouched. Does not mutate native original records.
    """
    outcome=evaluate_selection(records)
    if outcome["state"]!="BUILD_ELIGIBLE_METADATA_ONLY":
        raise ValueError("CANNOT_BUILD:"+",".join(outcome["errors"]))
    verify_assets(records, assets_root)
    if library.get("subject")!="Physics" or existing_manifest.get("schema")!="product-manifest/v1":
        raise ValueError("LIBRARY_OR_MANIFEST_NOT_NATIVE")
    ids={r["canonical_id"] for r in records}
    preserved_ids={q.get("id") for q in library.get("questions", [])}
    if ids & preserved_ids: raise ValueError("QUESTION_ID_COLLIDES_WITH_NATIVE_LIBRARY")
    for r in records:
        refs={x.get("id") for x in library.get("capabilities",[])}
        if r["curriculum"]["capability_ref"] not in refs:
            raise ValueError("UNRESOLVED_CAPABILITY_REF:"+r["canonical_id"])
        micro={x.get("id") for x in library.get("microtopics",[])}
        if r["curriculum"]["microtopic_ref"] not in micro:
            raise ValueError("UNRESOLVED_MICROTOPIC_REF:"+r["canonical_id"])
    bank={"manifest_id":"WPE-CORE2-21-DERIVED-CANDIDATE","version":"0.1.0",
          "acquisition_ref":bank_meta.get("acquisition_ref"),"target_package":bank_meta.get("target_package"),
          "inspector_id":bank_meta.get("inspector_id"),"inspection_sections":[],"access_status":"ITEMS_REFERENCED",
          "resource":bank_meta.get("resource"),"extensions":{"wpe:derived_no_admission_authority":True,"wpe:selection_validation":outcome},
          "questions":[],"resources":deepcopy(bank_meta.get("resources") or []),"last_checked":bank_meta.get("last_checked")}
    for r in records:
        q=deepcopy(r["question"])
        q["status"]="CANDIDATE"  # never self-promote native library status
        q["extensions"]={**q.get("extensions",{}),"wpe:admission_ref":r["governance"]["qrt_adjudication_ref"],
                       "wpe:source_identity":r["canonical_id"],"wpe:review_subject_fingerprint":fingerprint(r),
                       "wpe:primary_operation":r["assessment"]["primary_operation"],
                       "wpe:band":r["assessment"]["band"],"wpe:construction_seed":r.get("construction_seed"),
                       "wpe:source_custody":deepcopy(r["source"])}
        bank["questions"].append(q)
    m=deepcopy(existing_manifest)
    if m.get("selection",{}).get("core2"):
        raise ValueError("WPE_NATIVE_MANIFEST_NOT_EMPTY_STOP")
    m["selection"]["core2"]=[r["canonical_id"] for r in records]
    m["bank_refs"]=[bank_meta["target_package"]]
    # Authoritative package (records) remains byte-for-byte equivalent in meaning, not edited.
    return {"manifest.json":m,"bank.json":bank,"records.json":deepcopy(library),"validation":outcome}
