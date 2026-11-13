"""Wave 2 readiness promotion may not weaken the accepted Wave 1 UNBUILT HOLD.

The original unbuilt source bridge remains immutable for Stage 1 regression.
The separate Wave 2 technical-preview bridge is accepted ONLY for an
authored lesson with exact matching UID, revision, ownership and task IDs.
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
    original = json.loads((ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json")
                          .read_text("utf-8"))
    preview = json.loads((ROOT / "nsejs/data/source-learning-bridge-tech-preview.v1.json")
                         .read_text("utf-8"))
    authored = json.loads((ROOT / "nsejs/data/mechanics-wpe-teaching-pilot.v1.json")
                          .read_text("utf-8"))
    source = json.loads((ROOT / "nsejs/data/physics-authored-practice-r1.json")
                        .read_text("utf-8"))
    return original, preview, authored, source


def test_original_unbuilt_bridge_remains_unpromoted():
    original, preview, authored, source = evidence()
    [source_record] = validate_bindings(original, source)
    assert original["route_status"] == "UNBUILT_TECHNICAL_PILOT"
    assert source_record["lesson_status"] == "PENDING_WAVE2"
    assert source_record["lesson_revision"] == "UNBUILT"
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_LESSON_NOT_READY"):
        validate(authored, original)


def test_ready_tech_preview_requires_exact_revision_source_and_hold():
    original, preview, authored, source = evidence()
    result = validate(authored, preview)
    [original_route] = validate_bindings(original, source)
    [candidate] = preview["routes"]
    for field in ("question_uid", "source_id", "content_revision_sha256",
                  "source_collection", "origin", "subject", "topic",
                  "lesson_id", "task_a_id", "task_b_id", "transfer_id"):
        assert candidate[field] == original_route[field]
    assert preview["preview_authority"] == "AUTHORED_TECHNICAL_ONLY_NOT_ACADEMIC_ADMISSION"
    assert preview["academic_admission"] == "HOLD"
    assert candidate["academic_admission"] == "HOLD"
    assert candidate["original_source_status"] == "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert candidate["lesson_status"] == "READY_FOR_TECHNICAL_PREVIEW"
    assert candidate["lesson_revision"] == authored["lesson"]["revision"]
    assert result["source_revision"] == candidate["content_revision_sha256"]
    assert authored["source_return"]["route_status"] == "TECHNICAL_PREVIEW"
    assert source["academic_release"] == "HOLD"
    assert source["source_claim"] == "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"


@pytest.mark.parametrize("dimension,value,code",[
    ("manifest_status", "UNBUILT_TECHNICAL_PILOT", "SOURCE_BRIDGE_LESSON_NOT_READY"),
    ("lesson_status", "PENDING_WAVE2", "SOURCE_BRIDGE_LESSON_NOT_READY"),
    ("lesson_revision", "obsolete-revision", "SOURCE_BRIDGE_LESSON_NOT_READY"),
    ("question_uid", "g9:PHYSICS:OTHER", "SOURCE_BRIDGE_ROUTE_MISSING_OR_DUPLICATED"),
    ("content_revision_sha256", "0"*64, "SOURCE_BRIDGE_REVISION_OR_OWNER_MISMATCH"),
    ("task_b_id", "WRONG-SECOND-TASK", "BRIDGE_TASK_ID_MISMATCH"),
])
def test_false_preview_promotion_rejected(dimension, value, code):
    _, preview, authored, _ = evidence()
    preview = deepcopy(preview)
    if dimension == "manifest_status":
        preview["route_status"] = value
    else:
        preview["routes"][0][dimension] = value
    with pytest.raises(ContractError, match=code):
        validate(authored, preview)


def test_duplicate_preview_route_rejected():
    _, preview, authored, _ = evidence()
    preview["routes"].append(deepcopy(preview["routes"][0]))
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_ROUTE_MISSING_OR_DUPLICATED"):
        validate(authored, preview)


def test_academic_promotion_and_falsified_exam_origin_rejected():
    _, preview, authored, source = evidence()
    preview["academic_admission"] = "PASS"
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_MANIFEST_UNTRUSTED"):
        validate(authored, preview)
    original, preview, authored, source = evidence()
    source["source_claim"] = "OFFICIAL_EXAM_PAPER"
    with pytest.raises(BindingError, match="UNAUTHORIZED_SOURCE_ORIGIN"):
        validate_bindings(original, source)


def test_source_byte_tampering_rejected_before_any_technical_preview_claim():
    original, preview, authored, source = evidence()
    source["questions"][0]["stem"] += " unsupported source alteration"
    with pytest.raises(BindingError, match="STALE_SOURCE_REVISION"):
        validate_bindings(original, source)


def test_full_lesson_file_is_hashed_by_browser_adapter_for_attempt_isolation():
    adapter = (ROOT / "nsejs/js/wpe-contract-adapter.js").read_text("utf-8")
    assert "const contractDigest = await sha256(data.raw);" in adapter
    assert "source.content_revision_sha256" in adapter
    assert "lesson.revision" in adapter
    assert "STORAGE_UNAVAILABLE_BEFORE_FIRST_ATTEMPT" in adapter
    assert 'bridgeUrl:"../data/source-learning-bridge-tech-preview.v1.json"' in adapter


def test_existing_wpe_runtime_source_is_not_modified():
    engine = (ROOT / "physics/wpe/gap-six-stage-engine.js").read_text("utf-8")
    assert "window.WPEGapJourneys=function" in engine
    assert 'const stages=["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"]' in engine
    assert 'const taskKey=id=>id+(variantOf[id]==="T2"?"-T2":"");' in engine
