"""Contract gate for NSEJS data driving the existing WPEGapJourneys engine.

This is validation and namespace derivation, NOT an independent learning runtime.
Scientific correctness, observed student mastery and original-exam admission are
outside this contract. No code here modifies the WPE engine.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote

STAGES = ("Predict", "Attempt", "Reconstruct", "Diagnose", "Repair", "Boundary test")
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{2,79}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SUBJECTS = frozenset({"PHYSICS", "CHEMISTRY", "BIOLOGY"})
TYPES = frozenset({"select", "number", "textarea"})


class ContractError(ValueError):
    """Unusable or unsafe learner-contract payload."""


def _need(condition: bool, code: str) -> None:
    if not condition:
        raise ContractError(code)


def _text(value, code: str) -> str:
    _need(isinstance(value, str) and bool(value.strip()), code)
    return value


def namespace(data: dict) -> str:
    """Revision isolation: no old attempts silently reused after content changes."""
    source = data["source"]
    lesson = data["lesson"]
    raw = "\0".join((data["subject"], source["question_uid"],
                     source["content_revision_sha256"], lesson["id"],
                     lesson["revision"]))
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    # WPEGapJourneys expects a storagePrefix; it appends lesson and '-T2'.
    return "g9:nsejs:wpe-parity:v1:" + digest + ":"


def _check_fields(fields: object, context: str) -> None:
    _need(isinstance(fields, list) and len(fields) >= 2, "FIELDS_MISSING:" + context)
    ids = []
    for field in fields:
        _need(isinstance(field, dict), "FIELD_NOT_OBJECT:" + context)
        identifier = field.get("id")
        _need(isinstance(identifier, str) and bool(SAFE_ID.fullmatch(identifier)),
              "FIELD_ID_INVALID:" + context)
        ids.append(identifier)
        _text(field.get("label"), "FIELD_LABEL_MISSING:" + context)
        kind = field.get("type")
        _need(kind in TYPES, "FIELD_TYPE_UNSUPPORTED:" + context)
        if kind == "select":
            choices = field.get("choices")
            _need(isinstance(choices, list) and len(choices) >= 3
                  and all(isinstance(x, str) and x.strip() for x in choices)
                  and len(choices) == len(set(choices)), "SELECT_CHOICES_INVALID:" + context)
            _need(field.get("expected") in choices, "SELECT_EXPECTED_NOT_IN_CHOICES:" + context)
            _text(field.get("mistake"), "MODEL_DIAGNOSIS_MISSING:" + context)
        if kind == "number":
            _need(type(field.get("expected")) in (int, float)
                  and type(field.get("tol")) in (int, float)
                  and 0 <= field["tol"] < float("inf"), "NUMERIC_EXPECTATION_INVALID:" + context)
            _text(field.get("mistake"), "NUMERIC_DIAGNOSIS_MISSING:" + context)
    _need(len(ids) == len(set(ids)), "DUPLICATE_FIELD_ID:" + context)
    _need("model" in ids and "reason" in ids if context != "boundary" else
          "model" in ids and "why" in ids,
          "STUDENT_MODEL_AND_EXPLANATION_REQUIRED:" + context)
    for key in ("reason", "why"):
        if key in ids:
            _need(next(x["type"] for x in fields if x["id"] == key) == "textarea",
                  "WRITTEN_EXPLANATION_MUST_NOT_BE_AUTO_GRADED:" + context)


def _check_task(task: dict, name: str) -> None:
    _need(isinstance(task, dict), "TASK_NOT_OBJECT:" + name)
    for field in ("id", "prediction", "challenge", "boundary", "boundaryCheck",
                  "reasoning_demand"):
        _text(task.get(field), "TASK_FIELD_MISSING:" + name + ":" + field)
    _need(bool(SAFE_ID.fullmatch(task["id"])), "TASK_ID_INVALID:" + name)
    _need(isinstance(task.get("hints"), list) and len(task["hints"]) >= 2
          and all(isinstance(h, str) and h.strip() for h in task["hints"]),
          "PROGRESSIVE_HINTS_REQUIRED:" + name)
    worked = task.get("worked")
    _need(isinstance(worked, list) and len(worked) >= 3
          and all(isinstance(x, list) and len(x) == 2
                  and all(isinstance(y, str) and y.strip() for y in x)
                  for x in worked), "WORKED_RECONSTRUCTION_INVALID:" + name)
    _check_fields(task.get("fields"), "attempt")
    _check_fields(task.get("boundaryFields"), "boundary")
    _need(task.get("first_attempt_policy") == "SAVE_BEFORE_REVEAL",
          "PREMATURE_REVEAL_POLICY")
    _need(task.get("written_response_grading") == "UNASSESSED",
          "UNSUPPORTED_FREE_TEXT_AUTOGRADING")


def validate(data: dict, bridge: dict | None = None) -> dict:
    _need(isinstance(data, dict), "CONTRACT_NOT_OBJECT")
    _need(data.get("schema") == "grade9-nsejs-wpe-learner-contract/v1",
          "CONTRACT_SCHEMA_UNRECOGNIZED")
    _need(data.get("engine") == "window.WPEGapJourneys",
          "COMPETING_ENGINE_NOT_ALLOWED")
    _need(data.get("stages") == list(STAGES), "SIX_STAGE_ORDER_INVALID")
    _need(data.get("subject") in SUBJECTS, "SUBJECT_UNSUPPORTED")
    _need(data.get("academic_admission") == "HOLD", "ACADEMIC_HOLD_REQUIRED")
    source, lesson, tasks = data.get("source"), data.get("lesson"), data.get("tasks")
    _need(isinstance(source, dict) and isinstance(lesson, dict)
          and isinstance(tasks, dict), "SOURCE_LESSON_TASKS_REQUIRED")
    uid = _text(source.get("question_uid"), "SOURCE_UID_REQUIRED")
    _need(uid.startswith("g9:" + data["subject"] + ":"), "SOURCE_UID_SUBJECT_MISMATCH")
    revision = source.get("content_revision_sha256")
    _need(isinstance(revision, str) and bool(SHA256.fullmatch(revision)),
          "SOURCE_REVISION_SHA256_REQUIRED")
    _need(source.get("origin") in {"AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM",
                                    "UNQUALIFIED_CANDIDATE_ONLY"},
          "FALSE_OR_UNKNOWN_ORIGIN")
    _need(source.get("academic_admission") == "HOLD",
          "SOURCE_ACADEMIC_HOLD_REQUIRED")
    for key in ("id", "revision", "topic"):
        _text(lesson.get(key), "LESSON_FIELD_MISSING:" + key)
    _need(bool(SAFE_ID.fullmatch(lesson["id"])), "LESSON_ID_INVALID")
    _need(lesson.get("revision") != "UNBUILT", "LESSON_REVISION_REQUIRED_FOR_RUNTIME")
    _need(lesson.get("engine_adapter") == "WPE_SCENARIO_DATA_ONLY",
          "COMPETING_ADAPTER_NOT_ALLOWED")
    guide = lesson.get("core1a")
    _need(isinstance(guide, dict), "GUIDED_CORE1A_REQUIRED")
    for key in ("prerequisites", "core", "guide", "wrong", "conditions", "question"):
        _text(guide.get(key), "CORE1A_FIELD_MISSING:" + key)
    steps = guide.get("guideSteps")
    _need(isinstance(steps, list) and len(steps) >= 5
          and all(isinstance(item, list) and len(item) == 2
                  and all(isinstance(s, str) and s.strip() for s in item)
                  for item in steps), "FIVE_GUIDED_STEPS_REQUIRED")
    model = guide.get("model")
    _need(isinstance(model, dict) and model.get("kind") in
          {"SLIDER_MODEL", "TABULATED_MODEL", "DIAGRAM_PARAMETERS"},
          "INTERACTIVE_MODEL_DECLARATION_REQUIRED")
    _need(set(tasks) == {"A", "B"}, "TWO_TASK_VARIANTS_REQUIRED")
    _check_task(tasks["A"], "A")
    _check_task(tasks["B"], "B")
    _need(tasks["A"]["id"] != tasks["B"]["id"], "CROSS_TASK_ATTEMPT_ID_COLLISION")
    _need(tasks["A"]["challenge"] != tasks["B"]["challenge"] and
          tasks["A"]["reasoning_demand"] != tasks["B"]["reasoning_demand"],
          "TASK_B_IS_NOT_COGNITIVELY_DISTINCT")
    _need(tasks["A"]["boundary"] != tasks["B"]["boundary"],
          "CHANGED_CONDITION_TRANSFER_NOT_DISTINCT")
    route = data.get("source_return")
    _need(isinstance(route, dict)
          and route.get("question_uid") == uid
          and route.get("content_revision_sha256") == revision,
          "SOURCE_RETURN_IDENTITY_MISMATCH")
    _need(route.get("route_status") in {"UNBUILT", "TECHNICAL_PREVIEW"},
          "SOURCE_RETURN_UNREVIEWED_PROMOTION")
    if bridge is not None:
        _need(bridge.get("question_uid") == uid and
              bridge.get("content_revision_sha256") == revision and
              bridge.get("lesson_id") == lesson["id"] and
              bridge.get("source_return", {}).get("content_revision_sha256") == revision,
              "SOURCE_BRIDGE_REVISION_OR_OWNER_MISMATCH")
        _need(tasks["A"]["id"] == bridge.get("task_a_id") and
              tasks["B"]["id"] == bridge.get("task_b_id"), "BRIDGE_TASK_ID_MISMATCH")
    return {"schema": data["schema"], "engine": data["engine"],
            "source_uid": uid, "source_revision": revision,
            "storage_prefix": namespace(data), "variants": ["T1", "T2"],
            "stages": list(STAGES), "academic_admission": "HOLD"}


def load_and_validate(path: str | Path, bridge_path: str | Path | None = None) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    bridge = json.loads(Path(bridge_path).read_text(encoding="utf-8")) if bridge_path else None
    return validate(data, bridge)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    print(json.dumps(load_and_validate(args.contract), sort_keys=True, indent=2))
