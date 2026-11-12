"""Source-neutral Agent B UID binding and B1-B7 falsifiers.

All sample IDs are synthetic unless reading the immutable Agent A index snapshot.
"""
import importlib.util
import json
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "agent_b_core1ab_reconcile.py"
spec = importlib.util.spec_from_file_location("agent_b_core1ab_reconcile", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@pytest.fixture
def lookup():
    return mod.load_lookup()


def test_pinned_agent_a_interface_has_fifty_unapproved_unique_source_ids(lookup):
    rows=lookup["records"]
    assert len(rows) == 50
    assert len({r["source_id"] for r in rows}) == 50
    assert all(r["question_uid"] == "g9:PHYSICS:" + r["source_id"] for r in rows)
    assert all(r["qrt_adjudication"] == "HOLD" and r["academic_release"] == "NOT_ADMITTED" for r in rows)


def test_unique_displayed_label_is_not_canonical_binding(lookup):
    construction={"subject":"PHYSICS","target_question_id":"NSEJS-2023-P-Q01"}
    m=mod.match_uid(construction, lookup)
    assert m["match"]=="DISPLAYED_ALIAS_ONLY"
    assert m["uid"] is None
    assert m["candidates"] == ["g9:PHYSICS:NSEJS-23-OPT-01"]
    assert m["binding_status"]=="HOLD"


def test_exact_source_occurrence_still_requires_independent_admission(lookup):
    m=mod.match_uid({"subject":"PHYSICS","target_question_id":"NSEJS-23-OPT-01"},lookup)
    assert m["match"]=="EXACT_SOURCE_OCCURRENCE_ID"
    assert m["uid"] == "g9:PHYSICS:NSEJS-23-OPT-01"
    assert m["binding_status"]=="HOLD"


def test_displayed_id_collision_stays_ambiguous(lookup):
    m=mod.match_uid({"subject":"PHYSICS","target_question_id":"NSEJS-2019-P-Q02"},lookup)
    assert m["match"]=="AMBIGUOUS_DISPLAYED_ALIAS"
    assert m["uid"] is None
    assert len(m["candidates"]) >= 2


def test_agent_b_does_not_map_chemistry_using_physics_corpus(lookup):
    m=mod.match_uid({"subject":"CHEMISTRY","target_question_id":"NSEJS-2024-C-Q55"},lookup)
    assert m["match"]=="OUTSIDE_PHYSICS_LOOKUP"
    assert m["uid"] is None


@pytest.mark.parametrize("target",["PHYS-NSEJS-2024-P-Q57","PHYS-NSEJS-FLUID-04"])
def test_unlisted_authored_physics_does_not_claim_source_coverage(lookup,target):
    m=mod.match_uid({"subject":"PHYSICS","target_question_id":target},lookup)
    assert m["match"]=="UNMAPPED" and m["uid"] is None


def test_repo_scans_test_backed_constructions_without_authorship_guess(lookup):
    report=mod.census()
    assert report["test_backed_construction_count"] == 26
    assert report["owner_reported_count"] == 27
    assert report["count_discrepancy"] == 1
    assert report["count_discrepancy_status"] == "HOLD"
    assert len({x["construction_id"] for x in report["constructions"]}) == 26
    assert all(x["academic_status"] == "HOLD" for x in report["constructions"])
    assert all(x["B1"] == "HOLD" and x["B2"] == "HOLD" and x["B7"] == "HOLD"
               for x in report["constructions"])


def test_legacy_lens_and_fluid_repair_artifacts_can_still_be_unmapped(lookup):
    report=mod.census()
    selected = {x["construction_id"]: x for x in report["constructions"]}
    assert selected["PHYS-OPT-C-LENS-DISPLACEMENT-D3-01"]["match"] == "UNMAPPED"
    assert selected["PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01"]["match"] == "UNMAPPED"
    assert selected["PHYS-OPT-C-SCREW-LENS-01"]["match"] == "AMBIGUOUS_DISPLAYED_ALIAS"


def test_source_neutral_summary_never_exports_bank_stems(lookup):
    report=mod.census()
    s=json.dumps(report)
    assert '"stem"' not in s
    assert '"answer"' not in s
    assert '"options"' not in s
    assert 'No academic approval' not in s or report["release"]=="NOT_ADMITTED"


def test_missing_module_is_not_classified_as_teaching_pass(tmp_path):
    c={"construction_id":"PHYS-SYN-01","target_question_id":"SYN-Q-01"}
    r=mod._load_candidate(tmp_path/"missing",c)
    assert r["artifact"]=="NOT_RECEIVED"
    assert r["B3"]=="HOLD" and r["B4"]=="HOLD" and r["B5"]=="NOT_RUN"


def test_generation_attempt_does_not_turn_invalid_source_into_authenticity_pass(tmp_path,lookup):
    report=mod.census(generated_root=tmp_path/"absent")
    assert report["academic_admission"]=="HOLD"
    assert all(r["B7"]=="HOLD" for r in report["constructions"])


def test_weak_source_original_html_not_needed_for_uid_lookup(lookup):
    assert lookup["source_blob_sha"]
    assert lookup["source_head"]
    assert len(lookup["records"]) == 50
