"""QRT × Physics Blueprint low-thinking agent protocol: golden case tests.

Software checks here cannot certify independent QRT, source authenticity, native
lesson quality, or Owner authorization. All fixtures are author-exposed.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import runpy

import pytest
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
PROTOCOL=ROOT/"architecture"/"qrt-blueprint-protocol"
FIXTURES=PROTOCOL/"fixtures"
SCHEMAS=PROTOCOL/"schemas"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(kind, obj):
    schema=load(SCHEMAS/f"{kind}.schema.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(obj)


def test_every_schema_valid_draft_2020_12():
    names=["question-route","independent-first-pass","tile-build-plan","blueprint-gap-note"]
    for name in names:
        s=load(SCHEMAS/f"{name}.schema.json")
        Draft202012Validator.check_schema(s)
        assert s["$schema"].endswith("2020-12/schema")
        assert s["additionalProperties"] is False
        assert "description" in s


def test_golden_question_records_are_structurally_valid_and_fail_closed():
    bundle=load(FIXTURES/"golden-cases.json")
    assert bundle["schema"]=="g9v4-qrt-blueprint-golden-cases/v1"
    assert bundle["source_authority"]=="AUTHOR_EXPOSED_DOCUMENTARY_EXAMPLES_NOT_BLIND_QRT"
    assert len(bundle["cases"])==6
    assert len(bundle["negative_controls"])==5
    assert [c["id"] for c in bundle["cases"]]==["G01","G02","G03","G04","G05","G06"]
    for c in bundle["cases"]:
        validate("question-route",c["route"])
        assert c["route"]["fixture_not_evidence"] is True
        assert c["route"]["admission"]["status"]=="NOT_ADMITTED"
        assert c["route"]["blueprint"]["status"]=="DRAFT_OWNER_REVIEW"
        assert c["route"]["adapter"]["status"]=="UNSELECTED"
        assert c["route"]["qrt"]["reviewer_receipt"] is None
        assert c["expect"]["release"]=="HOLD"


def test_executable_examples_recompute_cells_and_reject_forged_promotion():
    runner=runpy.run_path(str(PROTOCOL/"verify_cases.py"))
    report=runner["run"]()
    assert report["status"]=="PASS"
    assert report["scope"]=="STRUCTURAL_AND_DOCUMENTARY_ONLY_NO_APPROVAL"
    assert len(report["positive_cases"])==6
    assert len(report["negative_controls"])==5
    assert all(x["release"]=="HOLD" for x in report["positive_cases"])
    assert next(x for x in report["positive_cases"] if x["case"]=="G03")["candidate_cell"]=="D3.4"
    assert next(x for x in report["positive_cases"] if x["case"]=="G04")["candidate_cell"]=="D3.6"
    assert next(x for x in report["positive_cases"] if x["case"]=="G01")["candidate_cell"] is None

    # Even if a client inserts approved-looking text, this program must not
    # synthesize a reviewer signature or issue a release.
    sample=deepcopy(load(FIXTURES/"golden-cases.json")["cases"][2]["route"])
    sample["admission"]["status"]="ADMITTED"
    sample["admission"]["owner_receipt"]="FORGED_STRING"
    sample["admission"]["native_core2_receipt"]="FORGED_STRING"
    out=runner["evaluate"](sample)
    assert out["release"]=="HOLD" and "NO_TRUSTED_RECEIPTS" in out["holds"]
    assert out["verified_independently"] is False


def test_invalid_schema_shape_does_not_silently_coerce_values():
    runner=runpy.run_path(str(PROTOCOL/"verify_cases.py"))
    row=deepcopy(load(FIXTURES/"golden-cases.json")["cases"][2]["route"])
    row["sl2"]["band"]="D5"
    with pytest.raises(ValueError):
        runner["evaluate"](row)
    row2=deepcopy(load(FIXTURES/"golden-cases.json")["cases"][0]["route"])
    row2["qrt"]["factors"]["concept_model_selection"]["score"]="1"
    with pytest.raises(ValueError):
        runner["evaluate"](row2)


def test_first_pass_packet_is_explicitly_unready_and_training_score_unsealed():
    sample=load(FIXTURES/"source-only-packet-NOT-READY.json")
    training=load(FIXTURES/"synthetic-qrt-scoring-NOT-EVIDENCE.json")
    validate("independent-first-pass",sample)
    validate("independent-first-pass",training)
    assert sample["record_role"]=="SOURCE_ONLY_PACKET"
    assert sample["first_pass"] is None
    assert sample["source"]["key_visibility"]=="WITHHELD_IN_FIRST_PASS"
    assert sample["reviewer_assignment"]["independently_assigned"] is False
    assert training["record_role"]=="TRAINING_EXAMPLE_NOT_EVIDENCE"
    assert training["seal"]["status"]=="NOT_SEALED"
    assert training["admission"]=="NOT_GRANTED_BY_THIS_RECORD"
    assert training["first_pass"]["total"]==sum(
        x["score"] for x in training["first_pass"]["factors"].values())
    assert 6<=training["first_pass"]["total"]<=7


def test_tile_plan_uses_main_and_per_instance_cycles_without_claiming_authority():
    plan=load(FIXTURES/"illustrative-D3.4-tile-plan-NOT-APPROVED.json")
    validate("tile-build-plan",plan)
    assert plan["tile_id"]=="PHY-WPE-D3.4"
    assert plan["blueprint"]["status"]=="DRAFT_OWNER_REVIEW"
    assert plan["adapter"]["status"]=="UNSELECTED"
    assert plan["release"]["status"]=="AUTHOR_DRAFT_ONLY"
    assert plan["main_cycle"]["kind"]=="MAIN"
    instance_ids={x["id"] for x in plan["instances"]}
    assert len(instance_ids)==2
    assert set(plan["main_cycle"]["instance_refs"])==instance_ids
    assert {tuple(x["instance_refs"]) for x in plan["instance_cycles"]}=={
        (i,) for i in instance_ids
    }
    assert plan["main_cycle"]["band_check"]["claimed_band"]=="D3"
    assert plan["main_cycle"]["band_check"]["total"]==6
    for cyc in [plan["main_cycle"],*plan["instance_cycles"]]:
        assert cyc["attempt"]["first_answer_saved_before_reveal"] is True
        assert cyc["band_check"]["status"]=="PROPOSED"
        assert cyc["band_check"]["total"]==sum(
            x["score"] for x in cyc["band_check"]["factors"].values()
        )
    assert all(x["status"]=="NOT_RUN" for x in plan["b1_b7"].values())


def test_gap_note_requires_versioned_escalation_without_approval():
    gap=load(FIXTURES/"hypothetical-blueprint-gap-NOT-SUBMITTED.json")
    validate("blueprint-gap-note",gap)
    assert gap["oracle_decision"]=="PENDING"
    assert gap["oracle_receipt"] is None
    assert "TRAINING" in gap["builder"]


def test_architecture_links_and_honest_source_baseline():
    index=(ROOT/"architecture/index.html").read_text(encoding="utf-8")
    page=(PROTOCOL/"index.html").read_text(encoding="utf-8")
    runbook=(PROTOCOL/"RUNBOOK.md").read_text(encoding="utf-8")
    assert 'href="qrt-blueprint-protocol/index.html"' in index
    assert 'href="RUNBOOK.md"' in page
    assert 'href="fixtures/golden-cases.json"' in page
    assert "D3.1" in runbook and "PAUSED" in runbook
    assert "NO_REAL_APPROVAL" in runbook
    assert "QRT" in runbook and "Blueprint" in runbook and "WPE" in runbook
    assert 'href="source-pins.json"' in page
    pins=load(PROTOCOL/"source-pins.json")
    assert len(pins["sources"])==6
    assert pins["sources"]["question_reader"]["record_count"]==74
    blueprint=load(ROOT/"templates/physics-blueprint/physics-blueprint.D3-D4.json")
    assert blueprint["status"]=="DRAFT_OWNER_REVIEW"
    assert blueprint["version"]=="0.2.0"
    assert len(blueprint["cells"])==14
    assert len(blueprint["column_order"])==7
    reader=load(ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json")
    assert len(reader["questions"])==74
    assert sum(q["band"] in ("D3","D4") for q in reader["questions"])==22


def test_core_six_stage_fixture_matches_blueprint_and_b1_b7():
    method=load(FIXTURES/"six-stage-core-method.json")
    bp=load(ROOT/"templates/physics-blueprint/physics-blueprint.D3-D4.json")
    expected=[x["id"] for x in bp["common"]["page_anatomy"]["core1b"]["sections"]]
    assert [x["key"] for x in method["stages"]]==expected
    assert len(expected)==6
    assert method["blueprint"]["version"]==bp["version"]
    assert method["status"]=="AUTHOR_EXPOSED_TRAINING_NOT_QRT_NOT_LEARNER_EVIDENCE"
    assert set(method["method"]["evidence_states"])==set(
        bp["common"]["evidence_record"]["observation_states"])
    assert all(x["principle"] and x["expected_evidence"] and x["failure"]
               for x in method["stages"])
    assert {k for x in method["stages"] for k in x["witness"]}=={
        "B1","B2","B3","B4","B5","B6","B7"}


def test_core_method_examples_and_architecture_links():
    m=load(FIXTURES/"six-stage-core-method.json")
    c=m["examples"]["conveyor"]
    for name,total in (("core1a",4),("fresh",24),("boundary",2)):
        row=c[name]
        assert row["motor_W"]==total
        assert row["motor_W"]==row["kinetic_W"]+row["heat_W"]
    v=m["examples"]["vertical_circle"]
    assert v["top_tension_N"]==-1 and v["boundary_top_tension_N"]==14
    page=(PROTOCOL/"index.html").read_text(encoding="utf-8")
    guide=(PROTOCOL/"CORE_METHOD.md").read_text(encoding="utf-8")
    home=(ROOT/"architecture/index.html").read_text(encoding="utf-8")
    assert 'id="core-method"' in page
    assert 'href="CORE_METHOD.md"' in page
    assert 'href="qrt-blueprint-protocol/CORE_METHOD.md"' in home
    for stage in ("Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"):
        assert stage in page and stage in guide
    assert "Core1A" in guide and "Core1B" in guide and "UNCERTAIN" in guide
