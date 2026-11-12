"""Fail-closed six-stage WPE data contract checks for future NSEJS adapters."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "nsejs/contracts"))
from wpe_learner_contract import ContractError, STAGES, namespace, validate

FIXTURE = ROOT / "nsejs/contracts/fixtures/synthetic-wpe-learner.v1.json"


@pytest.fixture
def lesson():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def fails(data, code, bridge=None):
    with pytest.raises(ContractError, match=code):
        validate(data, bridge)


def test_six_stage_synthetic_fixture_validates(lesson):
    result = validate(lesson)
    assert result["engine"] == "window.WPEGapJourneys"
    assert result["stages"] == list(STAGES)
    assert result["variants"] == ["T1", "T2"]
    assert result["storage_prefix"].startswith("g9:nsejs:wpe-parity:v1:")
    assert result["academic_admission"] == "HOLD"
    assert lesson["tasks"]["A"]["reasoning_demand"] != lesson["tasks"]["B"]["reasoning_demand"]


def test_full_revision_and_lesson_isolation(lesson):
    current = namespace(lesson)
    changed = deepcopy(lesson)
    changed["source"]["content_revision_sha256"] = "b"*64
    assert namespace(changed) != current
    changed = deepcopy(lesson)
    changed["lesson"]["revision"] = "synthetic-r2"
    assert namespace(changed) != current
    changed = deepcopy(lesson)
    changed["source"]["question_uid"] = "g9:PHYSICS:G9-SYN-UNIT-002"
    assert namespace(changed) != current


def test_t1_t2_storage_and_first_response_separation(lesson):
    # Mirrors existing WPEGapJourneys key selection; new runtime is NOT created.
    prefix = namespace(lesson)
    lesson_id = lesson["lesson"]["id"]
    a = prefix + lesson_id
    b = prefix + lesson_id + "-T2"
    assert a != b
    assert lesson["tasks"]["A"]["id"] != lesson["tasks"]["B"]["id"]
    assert lesson["tasks"]["A"]["first_attempt_policy"] == "SAVE_BEFORE_REVEAL"
    assert lesson["tasks"]["B"]["first_attempt_policy"] == "SAVE_BEFORE_REVEAL"


@pytest.mark.parametrize("field,value,error", [
    ("schema", "v0", "CONTRACT_SCHEMA_UNRECOGNIZED"),
    ("engine", "NSEJSIndependentEngine", "COMPETING_ENGINE_NOT_ALLOWED"),
    ("stages", ["Predict", "Reconstruct"], "SIX_STAGE_ORDER_INVALID"),
    ("subject", "HISTORY", "SUBJECT_UNSUPPORTED"),
    ("academic_admission", "PASS", "ACADEMIC_HOLD_REQUIRED"),
])
def test_contract_scope_fail_closed(lesson, field, value, error):
    lesson[field] = value
    fails(lesson, error)


@pytest.mark.parametrize("field,value,error", [
    ("question_uid", "g9:CHEMISTRY:FAKE", "SOURCE_UID_SUBJECT_MISMATCH"),
    ("content_revision_sha256", "digest", "SOURCE_REVISION_SHA256_REQUIRED"),
    ("origin", "OFFICIAL_NSEJS_EXAM", "FALSE_OR_UNKNOWN_ORIGIN"),
    ("academic_admission", "PASS", "SOURCE_ACADEMIC_HOLD_REQUIRED"),
])
def test_source_binding_required(lesson, field, value, error):
    lesson["source"][field] = value
    fails(lesson, error)


@pytest.mark.parametrize("field,value,error", [
    ("id", "bad/id", "LESSON_ID_INVALID"),
    ("revision", "UNBUILT", "LESSON_REVISION_REQUIRED_FOR_RUNTIME"),
    ("engine_adapter", "NSEJS_NEW_ENGINE", "COMPETING_ADAPTER_NOT_ALLOWED"),
])
def test_lesson_runtime_contract_required(lesson, field, value, error):
    lesson["lesson"][field] = value
    fails(lesson, error)


def test_guided_teaching_really_has_five_steps_and_model(lesson):
    lesson["lesson"]["core1a"]["guideSteps"] = [["Just answer", "No model"]]
    fails(lesson, "FIVE_GUIDED_STEPS_REQUIRED")
    lesson = json.loads(FIXTURE.read_text("utf-8"))
    lesson["lesson"]["core1a"]["model"] = {"kind": "ANSWER_KEY"}
    fails(lesson, "INTERACTIVE_MODEL_DECLARATION_REQUIRED")


@pytest.mark.parametrize("key,value,error", [
    ("id", "G9-SYN-UNIT-001-A", "CROSS_TASK_ATTEMPT_ID_COLLISION"),
    ("challenge", None, "TASK_FIELD_MISSING"),
    ("first_attempt_policy", "REVEAL_ANYTIME", "PREMATURE_REVEAL_POLICY"),
    ("written_response_grading", "AUTO_GRADE_TEXT", "UNSUPPORTED_FREE_TEXT_AUTOGRADING"),
])
def test_task_b_independence_and_no_reveal(lesson, key, value, error):
    lesson["tasks"]["B"][key] = value
    fails(lesson, error)


def test_reworded_numbers_not_genuine_transfer(lesson):
    lesson["tasks"]["B"]["reasoning_demand"] = lesson["tasks"]["A"]["reasoning_demand"]
    fails(lesson, "TASK_B_IS_NOT_COGNITIVELY_DISTINCT")


def test_attempt_model_and_written_explanation_required(lesson):
    lesson["tasks"]["A"]["fields"] = [f for f in lesson["tasks"]["A"]["fields"]
                                     if f["id"] != "reason"]
    fails(lesson, "STUDENT_MODEL_AND_EXPLANATION_REQUIRED")
    lesson = json.loads(FIXTURE.read_text("utf-8"))
    for f in lesson["tasks"]["B"]["fields"]:
        if f["id"] == "reason":
            f["type"] = "number"
            f["expected"], f["tol"], f["mistake"] = 0, 0, "cannot auto-grade reasoning"
    fails(lesson, "WRITTEN_EXPLANATION_MUST_NOT_BE_AUTO_GRADED")


def test_duplicate_field_and_hint_violation(lesson):
    lesson["tasks"]["A"]["fields"].append(deepcopy(lesson["tasks"]["A"]["fields"][0]))
    fails(lesson, "DUPLICATE_FIELD_ID")
    lesson = json.loads(FIXTURE.read_text("utf-8"))
    lesson["tasks"]["A"]["hints"] = []
    fails(lesson, "PROGRESSIVE_HINTS_REQUIRED")


def test_return_identity_fails_closed(lesson):
    lesson["source_return"]["content_revision_sha256"] = "c"*64
    fails(lesson, "SOURCE_RETURN_IDENTITY_MISMATCH")
    lesson = json.loads(FIXTURE.read_text("utf-8"))
    lesson["source_return"]["route_status"] = "ACADEMICALLY_ADMITTED"
    fails(lesson, "SOURCE_RETURN_UNREVIEWED_PROMOTION")


def test_bridge_owner_revision_and_task_gate(lesson):
    bridge = {"question_uid":lesson["source"]["question_uid"],
              "content_revision_sha256":lesson["source"]["content_revision_sha256"],
              "lesson_id":lesson["lesson"]["id"],
              "source_return":{"content_revision_sha256":lesson["source"]["content_revision_sha256"]},
              "task_a_id":lesson["tasks"]["A"]["id"],
              "task_b_id":lesson["tasks"]["B"]["id"]}
    assert validate(lesson, bridge)["academic_admission"] == "HOLD"
    bridge["task_b_id"] = "WRONG-TASK"
    fails(lesson, "BRIDGE_TASK_ID_MISMATCH", bridge)


@pytest.mark.parametrize("subject", ["PHYSICS", "CHEMISTRY", "BIOLOGY"])
def test_subject_neutral_shape(subject, lesson):
    lesson["subject"] = subject
    lesson["source"]["question_uid"] = "g9:" + subject + ":G9-SYN-UNIT-001"
    lesson["source_return"]["question_uid"] = lesson["source"]["question_uid"]
    assert validate(lesson)["source_uid"].startswith("g9:" + subject + ":")
