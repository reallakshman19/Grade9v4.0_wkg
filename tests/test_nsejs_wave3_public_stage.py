"""Fail-closed Pages staging for one additional authored WPE parity lesson.

This pilot is not part of the existing 8/26 Core1AB coverage count. This file
does not waive any private original-exam sources, QRT or academic review.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_nsejs_preview import (
    MECHANICS_WPE_PUBLIC, MECHANICS_WPE_UID, build,
    validate_mechanics_wpe_public_pilot
)
from source_learning_bridge import BindingError
from wpe_learner_contract import ContractError

FILES={
    "original": "nsejs/data/source-learning-bridge-pilot.v1.json",
    "preview": "nsejs/data/source-learning-bridge-tech-preview.v1.json",
    "lesson": "nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
    "source": "nsejs/data/physics-authored-practice-r1.json",
}


@pytest.fixture
def fixtures():
    return {k:json.loads((ROOT/p).read_text("utf-8")) for k,p in FILES.items()}


def approve(d):
    return validate_mechanics_wpe_public_pilot(
        d["original"],d["preview"],d["lesson"],d["source"])


def test_source_and_lesson_consistency_still_unadmitted(fixtures):
    result=approve(fixtures)
    assert result["source_uid"]==MECHANICS_WPE_UID
    assert result["source_authenticity"]=="AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert result["academic_approval"]=="HOLD"
    assert result["status"]=="AUTHORED_TECHNICAL_PREVIEW_ONLY"
    assert fixtures["original"]["routes"][0]["lesson_revision"]=="UNBUILT"
    assert fixtures["preview"]["routes"][0]["lesson_revision"]==fixtures["lesson"]["lesson"]["revision"]
    assert len(MECHANICS_WPE_PUBLIC)==5


@pytest.mark.parametrize("mutation",[
    "source_stem","source_answer","source_figures","source_authority",
    "original_custody","preview_admission","preview_route","preview_owner",
    "preview_stale_revision","preview_task_owner","lesson_mismatched_source",
    "lesson_missing_teaching"
])
def test_tampered_or_falsely_promoted_source_fails_closed(fixtures,mutation):
    d=deepcopy(fixtures)
    q=d["source"]["questions"][0]
    row=d["preview"]["routes"][0]
    if mutation=="source_stem":q["stem"]+=" changed"
    if mutation=="source_answer":q["answer"]="fabricated"
    if mutation=="source_figures":q["source_figures"]=["fabricated.svg"]
    if mutation=="source_authority":d["source"]["source_claim"]="OFFICIAL_EXAM"
    if mutation=="original_custody":d["original"]["routes"][0]["lesson_status"]="READY_FOR_TECHNICAL_PREVIEW"
    if mutation=="preview_admission":d["preview"]["academic_admission"]="PASS"
    if mutation=="preview_route":d["preview"]["route_status"]="UNBUILT_TECHNICAL_PILOT"
    if mutation=="preview_owner":row["lesson_id"]="OTHER-LESSON"
    if mutation=="preview_stale_revision":row["content_revision_sha256"]="0"*64
    if mutation=="preview_task_owner":row["task_b_id"]="WRONG-TASK"
    if mutation=="lesson_mismatched_source":d["lesson"]["source"]["content_revision_sha256"]="0"*64
    if mutation=="lesson_missing_teaching":d["lesson"]["lesson"]["core1a"]["guideSteps"]=[]
    with pytest.raises((ValueError, BindingError, ContractError)):
        approve(d)


@pytest.fixture(scope="module")
def staged(tmp_path_factory):
    stage=tmp_path_factory.mktemp("wpe-pages-stage")/"dist"
    manifest=build(stage)
    return stage,manifest


def test_generated_public_package_has_exact_five_pilot_assets(staged):
    stage, manifest=staged
    row=manifest["additional_authored_mechanics_wpe_parity_preview"]
    assert row["source_uid"]==MECHANICS_WPE_UID
    assert row["status"]=="AUTHORED_TECHNICAL_PREVIEW_ONLY"
    assert row["academic_approval"]=="HOLD"
    assert row["published"] is True
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    assert manifest["academic_approval"]==manifest["source_rights_review"]=="HOLD"
    for path in MECHANICS_WPE_PUBLIC:
        content=(stage/path).read_bytes()
        assert hashlib.sha256(content).hexdigest()==manifest["files"][path]
    assert not list(stage.rglob("*.pdf"))
    assert not list(stage.rglob("source-custody.json"))
    assert not list(stage.rglob("*.zip"))
    assert not any(p.startswith("workspace/") for p in manifest["files"])


def test_subject_route_is_bound_to_only_one_authored_lesson_and_no_iframe(staged):
    stage,manifest=staged
    page=(stage/"nsejs/physics/index.html").read_text("utf-8")
    assert page.count('id="nsejs-wpe-mechanics-parity"')==1
    assert page.count("Open authored Mechanics six-stage learner")==1
    assert "source_uid=g9:PHYSICS:G9-AUTH-MECH-001" in page
    assert manifest["additional_authored_mechanics_wpe_parity_preview"]["source_revision_sha256"] in page
    assert "UNVALIDATED · Academic HOLD" in page
    assert "<iframe" not in page.lower()
    learner=(stage/"nsejs/physics/learn-mechanics.html").read_text("utf-8")
    assert "gap-six-stage-engine.js" in learner
    assert "wpe-contract-adapter.js" in learner
    assert "<iframe" not in learner.lower()
