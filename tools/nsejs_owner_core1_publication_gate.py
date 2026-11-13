"""Validate owner-provided 2026-11-13 private Core1 candidate receipt.

This is a source-neutral hash/inventory receipt ONLY. The original private
bank stems, original PDF/images and authored A/B bytes MUST NEVER be staged
for public Pages. An authentic file hash is not independent science approval.
"""
from __future__ import annotations
import json
from pathlib import Path

SCHEMA="grade9-nsejs-owner-core1-private-archive-reconciliation/v2"
PIN="e5d389e8da62fc8c219373691f42ed93233814284bd15cb64a5ab8b5a5ade40f"
EXPECTED_BLOCKERS={
    "CHEM_MOLAR_MASS_INCONSISTENT",
    "OPTICS_IMAGE_POSITION_CONFLICT",
    "MISSING_4_PANEL_DIAGRAM_EVIDENCE",
    "OPTICS_ACCEPTANCE_CONTRADICTION",
}

def custody_receipt(path: Path,catalog: dict,recovery: dict)->dict:
    data=json.loads(path.read_text("utf8"))
    if (data.get("schema")!=SCHEMA or data.get("source_archive_sha256")!=PIN
        or data.get("archived_module_directories")!=27
        or data.get("unique_construction_ids")!=26
        or data.get("unpublished_source_bound_candidates")!=18
        or data.get("already_staged_technical_preview_lessons")!=8
        or data.get("original_manifest_declared_modules")!=0
        or data.get("original_manifest_is_inconsistent") is not True
        or data.get("original_source_file_count")!=0
        or data.get("witness_byte_hash_matched_core1a")!=27
        or data.get("witness_byte_hash_matched_core1b")!=27
        or data.get("source_fidelity")!="HOLD"
        or data.get("independent_science_review")!="HOLD"
        or data.get("academic_admission")!="HOLD"
        or data.get("original_modules_publication")!="NOT_AUTHORIZED"
        or data.get("rights_to_redistribute_original_exam_material")!="NOT_VERIFIED"
        or data.get("private_restore_gate")!="SOURCE_CUSTODY_REQUIRED_DO_NOT_BYPASS"
        or data.get("full_repository_qa")!="FAIL_MISSING_PRIVATE_SOURCES_AND_OUTPUTS"):
        raise ValueError("UNQUALIFIED_OWNER_CORE1_OR_SOURCE_PUBLICATION_CLAIM")
    alias=data.get("duplicate_alias",{})
    if (alias.get("construction_id")!="CHEM-ATOM-C-BOHR-TRANSITIONS-01"
        or alias.get("alias")!="chem-atomic-bonding-r1"
        or alias.get("canonical")!="chem-atomic-structure-r1"
        or alias.get("canonical_a_b_witness_html_byte_identical") is not True):
        raise ValueError("DUPLICATED_CONSTRUCTION_ALIAS_NOT_RECONCILED")
    original={r["construction_id"] for r in recovery.get("items",[]) if r["public_route"] is None}
    supplements={r["construction"] for r in catalog.get("items",[])}
    if(len(original)!=18 or supplements!=original or
       catalog.get("original_18_modules_still_on_hold")!=18 or
       catalog.get("original_audited_module_count_recovered")!=0):
        raise ValueError("ORIGINAL_AND_SUPPLEMENTAL_CENSUS_NOT_SEPARATE")
    rows=data.get("candidates")
    if not isinstance(rows,list) or len(rows)!=18 or (
        {x["construction_id"] for x in rows}!=original or
        len({x["slug"] for x in rows})!=18):
        raise ValueError("OWNER_ARCHIVE_CANDIDATE_IDENTITY_MISMATCH")
    flags=set()
    for item in rows:
        if (item.get("subject") not in {"CHEMISTRY","PHYSICS"} or
            item.get("candidate_file_integrity")!="PRODUCER_SHA256_MATCH" or
            item.get("original_source_custody")!="HOLD" or
            item.get("academic_admission")!="HOLD" or
            item.get("original_publication")!="NOT_AUTHORIZED" or
            item.get("safe_public_alternative")!="INDEPENDENT_SOURCE_NEUTRAL_SUPPLEMENTAL_TECHNICAL_PREVIEW"):
            raise ValueError("CANDIDATE_SOURCE_OR_ACADEMIC_FALSE_PROMOTION")
        if item.get("science_issue"):
            flags.add(item["science_issue"])
        supplemental=next((r for r in catalog["items"] if r["construction"]==item["construction_id"]),None)
        if supplemental is None or supplemental.get("subject")!=item["subject"]:
            raise ValueError("CANDIDATE_SUBJECT_DOES_NOT_MATCH_AUTHOR_REPAIR")
    if(flags!=EXPECTED_BLOCKERS or set(data.get("known_blockers",{}))!=EXPECTED_BLOCKERS):
        raise ValueError("SCIENCE_BLOCKER_LOST_OR_UNPINNED")
    return data
