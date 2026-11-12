"""Source→learning bridge contract tests. Never certify source/academic approval."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from source_learning_bridge import BindingError, content_revision, validate_bindings


@pytest.fixture
def evidence():
    mapping = json.loads((ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json").read_text("utf-8"))
    source = json.loads((ROOT / "nsejs/data/physics-authored-practice-r1.json").read_text("utf-8"))
    return mapping, source


def held(mapping, source, match):
    with pytest.raises(BindingError, match=match):
        validate_bindings(mapping, source)


def test_actual_authored_pilot_uses_current_reader_revision(evidence):
    mapping, source = evidence
    [route] = validate_bindings(mapping, source)
    [q] = [q for q in source["questions"] if q["source_id"] == route["source_id"]]
    assert route["content_revision_sha256"] == content_revision(q)
    assert route["question_uid"] == "g9:PHYSICS:G9-AUTH-MECH-001"
    assert route["origin"] == source["source_claim"] == "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert route["lesson_status"] == "PENDING_WAVE2"
    assert route["lesson_revision"] == "UNBUILT"
    assert source["academic_release"] == mapping["academic_admission"] == "HOLD"
    assert len({route["task_a_id"], route["task_b_id"], route["transfer_id"]}) == 3
    assert route["source_return"]["content_revision_sha256"] == route["content_revision_sha256"]


@pytest.mark.parametrize("field,value", [
    ("stem", "Tampered question stem"),
    ("options", ["A: 99", "B: 0"]),
    ("answer", "C: 6.4 m"),
    ("steps", ["unapproved replacement derivation"]),
    ("check", "unapproved boundary replacement"),
    ("source_figures", ["missing-source-figure.svg"]),
])
def test_question_display_change_invalidates_revision(evidence, field, value):
    mapping, source = evidence
    source["questions"][0][field] = value
    held(mapping, source, "STALE_SOURCE_REVISION")


def test_duplicate_source_id_rejected(evidence):
    mapping, source = evidence
    source["questions"].append(deepcopy(source["questions"][0]))
    held(mapping, source, "DUPLICATE_SOURCE_ID")


def test_duplicate_route_rejected(evidence):
    mapping, source = evidence
    mapping["routes"].append(deepcopy(mapping["routes"][0]))
    held(mapping, source, "DUPLICATE_OR_MISMATCHED_QUESTION_UID")


@pytest.mark.parametrize("field,value,error", [
    ("question_uid", "g9:PHYSICS:ANOTHER-QUESTION", "DUPLICATE_OR_MISMATCHED_QUESTION_UID"),
    ("source_id", "G9-AUTH-MECH-404", "UNKNOWN_SOURCE_ID"),
    ("source_collection", "nsejs/data/official-exam.json", "SOURCE_COLLECTION_MISMATCH"),
    ("origin", "VERIFIED_NSEJS_EXAM", "FALSE_EXAM_PROVENANCE"),
    ("subject", "CHEMISTRY", "SUBJECT_OR_TOPIC_MISMATCH"),
    ("topic", "OPTICS", "SUBJECT_OR_TOPIC_MISMATCH"),
    ("content_revision_sha256", "0"*64, "STALE_SOURCE_REVISION"),
    ("lesson_revision", "admitted-v1", "UNVERIFIED_LESSON_MUST_NOT_BE_PUBLISHED"),
    ("lesson_status", "PUBLISHED", "UNVERIFIED_LESSON_MUST_NOT_BE_PUBLISHED"),
    ("reasoning_operation", "APPLY", "REASONING_OR_PREREQUISITE_MISMATCH"),
    ("task_b_id", "G9-NSEJS-AUTH-MECH-001-A", "SHARED_ATTEMPT_OR_TRANSFER_ID"),
    ("transfer_id", "G9-NSEJS-AUTH-MECH-001-A", "SHARED_ATTEMPT_OR_TRANSFER_ID"),
])
def test_bad_route_fails_closed(evidence, field, value, error):
    mapping, source = evidence
    mapping["routes"][0][field] = value
    held(mapping, source, error)


def test_return_question_or_revision_substitution_rejected(evidence):
    original = deepcopy(original)
    mapping, source = deepcopy(original)
    mapping["routes"][0]["source_return"]["question_uid"] = "g9:PHYSICS:WRONG"
    held(mapping, source, "SOURCE_RETURN_REVISION_MISMATCH")
    mapping, source = deepcopy(original)
    mapping["routes"][0]["source_return"]["content_revision_sha256"] = "0"*64
    held(mapping, source, "SOURCE_RETURN_REVISION_MISMATCH")


def test_academic_or_reader_contract_promotion_rejected(evidence):
    original = deepcopy(original)
    mapping, source = deepcopy(original)
    source["source_claim"] = "OFFICIAL_NSEJS_EXAM"
    held(mapping, source, "UNAUTHORIZED_SOURCE_ORIGIN")
    mapping, source = deepcopy(original)
    mapping["source_revision_algorithm"] = "unexpected/v2"
    held(mapping, source, "INCOMPATIBLE_CONTENT_REVISION_ALGORITHM")
    mapping, source = deepcopy(original)
    mapping["academic_admission"] = "PASS"
    held(mapping, source, "ACADEMIC_ADMISSION_MUST_REMAIN_HOLD")


def test_topic_change_or_lesson_attempt_alias_rejected(evidence):
    original = deepcopy(original)
    mapping, source = deepcopy(original)
    source["questions"][0]["topic"] = "OPTICS"
    held(mapping, source, "SOURCE_PROVENANCE_OR_TOPIC_INVALID")
    mapping, source = deepcopy(original)
    mapping["routes"][0]["lesson_id"] = mapping["routes"][0]["task_a_id"]
    held(mapping, source, "SHARED_ATTEMPT_OR_TRANSFER_ID")
