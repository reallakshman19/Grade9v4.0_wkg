"""Exact generated Core1B corrections from public-safe source-neutral builders.

Does not assert Physics/QRT independent approval or source authenticity.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    work = tmp_path_factory.mktemp("agent_b_generated")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO) + os.pathsep + env.get("PYTHONPATH", "")
    for filename in ("build_d3_batch2_modules.py", "build_d3_expansion_modules.py", "build_physics_fluids_core1.py", "build_bio_genetics_core1.py"):
        target = work / filename
        shutil.copyfile(REPO / filename, target)
        p = subprocess.run([sys.executable, str(target)], cwd=work, env=env,
                           capture_output=True, text=True, timeout=40)
        assert p.returncode == 0, p.stdout[-1500:] + p.stderr[-4000:]
    return work / "workspace" / "output"


def _read(generated, module, name):
    return json.loads((generated / module / (name + ".json")).read_text(encoding="utf-8"))


def test_source_banks_and_qrts_remain_owned_by_agent_a(generated):
    lens = _read(generated, "nsejs-optics-displacement-d3-r1", "bank")
    fluid = _read(generated, "nsejs-fluids-surface-energy-d3-r1", "bank")
    assert lens["questions"][0]["id"] == "PHYS-NSEJS-2024-P-Q57"
    assert "D = 75 cm" in lens["questions"][0]["stem"]
    assert fluid["questions"][0]["id"] == "PHYS-NSEJS-FLUID-04"
    assert "1000" in fluid["questions"][0]["stem"]
    for module in ("nsejs-optics-displacement-d3-r1", "nsejs-fluids-surface-energy-d3-r1"):
        witness = _read(generated, module, "witness")
        assert witness["status"] == "CANDIDATE"
        assert not witness.get("review_receipts")


def test_lens_reconstruction_uses_inverse_measurement(generated):
    b = _read(generated, "nsejs-optics-displacement-d3-r1", "core1b_reconstruction")
    assert "PRACTICE" in b["fresh_context_ref"]
    prompt = b["stages"]["stage_2_attempt"]["prompt"]
    assert "96 cm" in prompt and "48 cm" in prompt and "75 cm" not in prompt
    assert len(b["stages"]["stage_3_reconstruct"]["route"]) == 4
    assert len(b["stages"]["stage_2_attempt"]["rubric"]) == 3
    assert all(token not in b["progressive_hints"][2]["text"] for token in ("18 cm", "24 cm", "72 cm"))
    D, d = 96, 48
    f = (D*D-d*d)/(4*D)
    x1, x2 = (D-d)/2, (D+d)/2
    assert (f, x1, x2, (D-x1)/x1, (D-x2)/x2) == (18, 24, 72, 3, 1/3)
    assert 70 < 4*f


def test_unequal_droplet_reconstruction_is_independent(generated):
    b = _read(generated, "nsejs-fluids-surface-energy-d3-r1", "core1b_reconstruction")
    p = b["stages"]["stage_2_attempt"]["prompt"]
    assert "Eight water drops" in p and "one water drop of radius 2 mm" in p
    assert "1000" not in p and "8.48" not in p
    assert len(b["stages"]["stage_3_reconstruct"]["route"]) == 4
    assert len(b["stages"]["stage_2_attempt"]["rubric"]) == 3
    assert "5.1124" not in b["progressive_hints"][2]["text"]
    import math
    r, gamma = .001, .072
    before = 4*math.pi*(8*r*r+(2*r)**2)
    R = (8*r**3+(2*r)**3)**(1/3)
    lost = before-4*math.pi*R*R
    assert math.isclose(lost, 7.1004967641686e-5, rel_tol=1e-10)
    assert math.isclose(gamma*lost, 5.112357670201392e-6, rel_tol=1e-10)


def test_witness_hashes_and_b4_mappings_bound_to_new_tasks(generated):
    for module in ("nsejs-optics-displacement-d3-r1", "nsejs-fluids-surface-energy-d3-r1"):
        b = _read(generated, module, "core1b_reconstruction")
        witness = _read(generated, module, "witness")
        raw = (generated / module / "core1b_reconstruction.json").read_bytes()
        assert witness["core1b"]["task_sha256"] == "sha256:" + hashlib.sha256(raw).hexdigest()
        assert witness["core1b"]["fresh_context_ref"] == b["fresh_context_ref"]
        assert "PENDING" in witness["core1b"]["freshness_review_ref"]
        for role, evidence in witness["core1b"]["assessed_roles"].items():
            assert "stage_2_attempt.rubric[" in evidence["attempt_field"]
            idx = int(evidence["attempt_field"].split("[", 1)[1].split("]", 1)[0])
            assert idx < len(b["stages"]["stage_2_attempt"]["rubric"])


def test_fluid_runtime_reconstruction_is_separately_gated(generated):
    html = (generated / "nsejs-fluids-surface-energy-d3-r1" / "learning_journey.html").read_text(encoding="utf-8")
    assert 'data-agent-b-core1b' in html
    assert 'data-role="model-host" hidden' in html
    assert 'data-role="save-firstAttempt"' in html
    assert 'data-role="save-prediction"' in html
    assert 'data-role="save-transfer"' in html
    assert 'id="derivation-section" class="derivation-section"' in html  # Core2 unchanged
    assert "localStorage.getItem(key)!==priorRaw" in html
    assert "Attempt could not be saved and verified" in html
    assert "<iframe" not in html.lower()


def test_no_fake_native_runtime_receipts(generated):
    witness = _read(generated, "nsejs-fluids-surface-energy-d3-r1", "witness")
    assert witness["core1b"]["attempt_events"] == []
    assert witness["core1b"]["native_runtime_receipt_ref"] == "NOT_RECEIVED"
    assert witness["assessment"]["qrt_decision_ref"]  # producer-owned, not reviewed here


def test_generated_lens_learner_is_source_neutral_and_protected(generated):
    html = (generated / "nsejs-optics-displacement-d3-r1" / "learning_journey.html").read_text(encoding="utf-8")
    assert 'id="tab-core1b"' in html
    assert 'id="tab-core1a"' in html
    assert 'id="tab-core2"' in html
    assert "No original-answer or QRT approval" in html
    assert "Core1A physical construction" in html
    assert "Stage 1" in html and "Stage 2" in html
    assert 'data-agent-b-core1b' in html
    assert 'data-role="model-host" hidden' in html
    assert 'data-role="save-firstAttempt"' in html
    assert 'data-role="save-transfer"' in html
    assert "96 cm" in html and "48 cm" in html
    assert "18 cm" in html  # present in inert script data, not pre-attempt visible prose
    assert "localStorage.getItem(key)!==priorRaw" in html
    assert "Agent A" in html
    assert "<iframe" not in html.lower()


def test_eight_reproducible_b1b7_candidates_have_generated_attempt_controls(generated):
    slugs = [
        "nsejs-optics-displacement-d3-r1",
        "nsejs-fluids-surface-energy-d3-r1",
        "chem-electronic-structure-d3-r1",
        "bio-immunology-defense-d3-r1",
        "chem-phosphorus-oxyacids-d3-r1",
        "bio-viral-genetics-d3-r1",
        "bio-genetics-coordination-r1",
        "nsejs-fluids-sound-r1",
    ]
    for slug in slugs:
        module = generated / slug
        a = json.loads((module / "core1a_construction.json").read_text(encoding="utf-8"))
        b = json.loads((module / "core1b_reconstruction.json").read_text(encoding="utf-8"))
        w = json.loads((module / "witness.json").read_text(encoding="utf-8"))
        page = (module / "learning_journey.html").read_text(encoding="utf-8")
        assert a["construction_id"] == b["construction_id"] == w["construction"]["construction_id"], slug
        assert a["target_question_id"] == b["target_question_id"], slug
        assert a["academic_status"] == b["academic_status"] == "HOLD:ACADEMIC_ADMISSION", slug
        assert w["status"] == "CANDIDATE", slug
        assert not w["review_receipts"], slug
        assert 'data-agent-b-core1b' in page, slug
        assert 'data-role="model-host" hidden' in page, slug
        assert 'data-role="save-firstAttempt"' in page, slug
        assert 'data-role="save-transfer"' in page, slug
        assert "<iframe" not in page.lower(), slug
        raw = (module / "core1b_reconstruction.json").read_bytes()
        assert w["core1b"]["task_sha256"] == "sha256:" + hashlib.sha256(raw).hexdigest(), slug


def test_all_generated_core1b_hints_do_not_give_final_science_answer_before_attempt(generated):
    genetics = _read(generated, "bio-genetics-coordination-r1", "core1b_reconstruction")
    chem = _read(generated, "chem-phosphorus-oxyacids-d3-r1", "core1b_reconstruction")
    viral = _read(generated, "bio-viral-genetics-d3-r1", "core1b_reconstruction")
    assert "2000" not in genetics["progressive_hints"][-1]["text"]
    assert "Option A" not in chem["progressive_hints"][-1]["text"]
    assert "Statements C and D" not in viral["progressive_hints"][-1]["text"]
    for slug in ("nsejs-fluids-sound-r1", "bio-genetics-coordination-r1",
                 "chem-phosphorus-oxyacids-d3-r1", "bio-viral-genetics-d3-r1"):
        w = _read(generated, slug, "witness")
        assert w["core1b"]["attempt_events"] == [], slug
        assert w["core1b"]["native_runtime_receipt_ref"] == "NOT_RECEIVED", slug


def test_scandium_topup_is_new_ionization_inference_not_original_neutral_question(generated):
    a = _read(generated, "chem-electronic-structure-d3-r1", "core1a_construction")
    b = _read(generated, "chem-electronic-structure-d3-r1", "core1b_reconstruction")
    assert "4s" in a["misconceptions"][-1]["repair"]
    assert b["fresh_context_ref"].startswith("AB-PRACTICE")
    assert "Sc2+" in b["stages"]["stage_2_attempt"]["prompt"]
    assert "Sc3+" in b["stages"]["stage_2_attempt"]["prompt"]
    assert len(b["stages"]["stage_2_attempt"]["rubric"]) == 3
    assert len(b["stages"]["stage_3_reconstruct"]["route"]) == 4
    assert "0 unpaired" not in b["progressive_hints"][-1]["text"]


def test_immunity_topup_does_not_invent_original_source_or_universal_innate_loss(generated):
    a = _read(generated, "bio-immunology-defense-d3-r1", "core1a_construction")
    b = _read(generated, "bio-immunology-defense-d3-r1", "core1b_reconstruction")
    assert any("memory B cells" in m.get("wrong_idea", "") for m in a["misconceptions"])
    assert b["fresh_context_ref"].startswith("AB-PRACTICE")
    assert "intact neutrophils" in b["stages"]["stage_2_attempt"]["prompt"]
    assert len(b["stages"]["stage_3_reconstruct"]["route"]) == 4
    assert "neutrophils" in b["stages"]["stage_6_boundary_test"]["prompt"]
    assert any("helminth" in m.get("repair", "").lower() for m in a["misconceptions"])
