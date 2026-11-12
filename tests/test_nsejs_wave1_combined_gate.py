"""Wave 1 combined acceptance: contracts connect while unbuilt lessons remain held.

These tests use authored/source-neutral fixtures only. They DO NOT establish
Physics science correctness, an executable student route, or exam admission.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "nsejs/contracts"))
from source_learning_bridge import BindingError, validate_bindings
from wpe_learner_contract import ContractError, validate

def evidence():
    manifest = json.loads((ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json").read_text("utf-8"))
    source = json.loads((ROOT / "nsejs/data/physics-authored-practice-r1.json").read_text("utf-8"))
    fixture = json.loads((ROOT / "nsejs/contracts/fixtures/synthetic-wpe-learner.v1.json").read_text("utf-8"))
    return manifest, source, fixture

def synthetic_contract_at_real_identity(fixture, row):
    # Shape compatibility only; synthetic teaching is NOT accepted as the real lesson.
    lesson = deepcopy(fixture)
    lesson["source"]["question_uid"] = row["question_uid"]
    lesson["source"]["content_revision_sha256"] = row["content_revision_sha256"]
    lesson["source"]["origin"] = row["origin"]
    lesson["source_return"]["question_uid"] = row["question_uid"]
    lesson["source_return"]["content_revision_sha256"] = row["content_revision_sha256"]
    lesson["lesson"]["id"] = row["lesson_id"]
    lesson["lesson"]["topic"] = row["topic"]
    lesson["tasks"]["A"]["id"] = row["task_a_id"]
    lesson["tasks"]["B"]["id"] = row["task_b_id"]
    return lesson

def test_combined_real_source_binding_is_revision_bound_and_not_an_exam():
    manifest, source, _ = evidence()
    [route] = validate_bindings(manifest, source)
    assert route["source_id"] == "G9-AUTH-MECH-001"
    assert route["origin"] == "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert route["lesson_status"] == "PENDING_WAVE2"
    assert route["lesson_revision"] == "UNBUILT"
    assert manifest["academic_admission"] == source["academic_release"] == "HOLD"

def test_combined_unbuilt_lesson_is_refused_for_runtime():
    manifest, source, fixture = evidence()
    [route] = validate_bindings(manifest, source)
    lesson = synthetic_contract_at_real_identity(fixture, route)
    lesson["source_return"]["route_status"] = "TECHNICAL_PREVIEW"
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_LESSON_NOT_READY"):
        validate(lesson, manifest)

def test_combined_synced_preview_shape_is_compatible_but_not_academically_admitted():
    manifest, source, fixture = evidence()
    [route] = validate_bindings(manifest, source)
    lesson = synthetic_contract_at_real_identity(fixture, route)
    lesson["source_return"]["route_status"] = "TECHNICAL_PREVIEW"
    # Test only future structural compatibility; no actual lesson is published.
    manifest["route_status"] = "TECHNICAL_PREVIEW"
    route["lesson_status"] = "READY_FOR_TECHNICAL_PREVIEW"
    route["lesson_revision"] = lesson["lesson"]["revision"]
    result = validate(lesson, manifest)
    assert result["academic_admission"] == "HOLD"
    assert result["source_uid"] == route["question_uid"]

def test_combined_revision_substitution_refused():
    manifest, source, fixture = evidence()
    [route] = validate_bindings(manifest, source)
    lesson = synthetic_contract_at_real_identity(fixture, route)
    lesson["source"]["content_revision_sha256"] = "0" * 64
    with pytest.raises(ContractError, match="SOURCE_RETURN_IDENTITY_MISMATCH"):
        validate(lesson, manifest)
    source["questions"][0]["stem"] = "substituted content"
    with pytest.raises(BindingError, match="STALE_SOURCE_REVISION"):
        validate_bindings(manifest, source)

def test_combined_duplicate_source_route_refused():
    manifest, source, fixture = evidence()
    [route] = validate_bindings(manifest, source)
    lesson = synthetic_contract_at_real_identity(fixture, route)
    lesson["source_return"]["route_status"] = "TECHNICAL_PREVIEW"
    manifest["routes"].append(deepcopy(route))
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_ROUTE_MISSING_OR_DUPLICATED"):
        validate(lesson, manifest)
    with pytest.raises(BindingError, match="DUPLICATE_OR_MISMATCHED_QUESTION_UID"):
        validate_bindings(manifest, source)

def test_combined_attempt_ids_and_return_are_distinct():
    manifest, source, fixture = evidence()
    [route] = validate_bindings(manifest, source)
    lesson = synthetic_contract_at_real_identity(fixture, route)
    ids = {lesson["tasks"]["A"]["id"], lesson["tasks"]["B"]["id"], route["transfer_id"]}
    assert len(ids) == 3
    assert route["source_return"]["question_uid"] == lesson["source"]["question_uid"]
    assert route["source_return"]["content_revision_sha256"] == lesson["source"]["content_revision_sha256"]
