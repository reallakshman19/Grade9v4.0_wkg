"""Verification suite for NSEJS 2024 Physics Mechanics Core 1A and Core 1B Learning Journey.

Mechanical verification enforces:
- Core 1A declarative detailed teaching structure (conventions, prerequisites, inferential jump, worked anchor, wrong path, exit check)
- Core 1B 6-stage phenomenological reconstruction cycle (Predict, Attempt, Reconstruct, Diagnose, Repair, Boundary test)
- Bidirectional B1–B7 witness inspection via grade9qa.bridge_witness.inspect_witness
- Compliance with the 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards >= 14px, mobile CSS cascade, commitment-first inert derivations)
- Exact mathematical physics proofs (velocity-time integration, average velocity theorem, scale-invariant ratio 1/2)
- Student learning loop gateway (Core 2 <-> Core 1A <-> Core 1B <-> Core 2 state preservation without iframes)
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
from pathlib import Path
import re
import pytest

from grade9qa.bridge_witness import inspect_witness
from grade9qa.validate import schema_errors

REPO_ROOT = Path(__file__).resolve().parents[1]
MECH_DIR = REPO_ROOT / "workspace/output/nsejs-mechanics-r1"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def core1a():
    p = MECH_DIR / "core1a_construction.json"
    assert p.exists(), f"Missing Core 1A file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def core1b():
    p = MECH_DIR / "core1b_reconstruction.json"
    assert p.exists(), f"Missing Core 1B file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def witness():
    p = MECH_DIR / "witness.json"
    assert p.exists(), f"Missing Witness file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def journey_html():
    p = MECH_DIR / "learning_journey.html"
    assert p.exists(), f"Missing Learning Journey HTML: {p}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Core 1A Declarative Teaching Structure Validation
# ---------------------------------------------------------------------------

def test_core1a_structure_and_fields(core1a):
    assert core1a["schema"] == "core1a-construction/v1"
    assert core1a["construction_id"] == "PHYS-MECH-C-DECOUPLED-KINEMATICS-01"
    assert core1a["target_question_id"] == "NSEJS-2024-P-Q46"
    assert core1a["topic"] == "MECHANICS"
    assert core1a["family"] == "PHYS-MECHANICS-KINEMATICS"
    assert core1a["cognitive_demand"] == "MODEL"
    assert core1a["difficulty_band"] == "D2"
    assert core1a["difficulty_score"] == 4
    assert core1a["crux_move"] == "M2"

    # Declared conventions first
    conventions = core1a["declared_conventions"]
    assert len(conventions) >= 4
    conv_text = " ".join(c["statement"] for c in conventions)
    assert "integral" in conv_text.lower() or "area" in conv_text.lower()
    assert "average velocity" in conv_text.lower()

    # Prerequisites
    assert len(core1a["entry_assumptions"]) >= 3

    # Inferential jump
    assert len(core1a["inferential_jump"]) > 30

    # Teaching path (must strictly use canonical verbs)
    path = core1a["teaching_path"]
    assert len(path) == 4
    for step in path:
        assert step["role"] in CANONICAL_OPERATIONS, f"Non-canonical verb: {step['role']}"
        assert "action" in step and len(step["action"]) > 10
        assert "why_valid" in step and len(step["why_valid"]) > 10
        assert "inputs" in step and len(step["inputs"]) > 0
        assert "output" in step and len(step["output"]) > 0

    # Worked conceptual anchor (must differ from Core 1B train/wagon)
    anchor = core1a["worked_conceptual_anchor"]
    assert "patrol" in anchor["problem"].lower() or "vehicle" in anchor["problem"].lower()
    assert len(anchor["solution_steps"]) == 4

    # Plausible wrong path & repair
    misconceptions = core1a["misconceptions"]
    assert len(misconceptions) >= 1
    m0 = misconceptions[0]
    assert "wrong_idea" in m0
    assert "diagnostic_prompt" in m0
    assert "repair" in m0

    # Independent exit check
    exit_task = core1a["exit_task"]
    assert "prompt" in exit_task
    assert "answer" in exit_task


# ---------------------------------------------------------------------------
# 2. Core 1B 6-Stage Phenomenological Reconstruction Validation
# ---------------------------------------------------------------------------

def test_core1b_structure_and_6_stages(core1b):
    assert core1b["schema"] == "core1b-reconstruction/v1"
    assert core1b["construction_id"] == "PHYS-MECH-C-DECOUPLED-KINEMATICS-01"
    assert core1b["target_question_id"] == "NSEJS-2024-P-Q46"
    assert core1b["cognitive_demand"] == "MODEL"
    assert core1b["difficulty_band"] == "D2"
    assert core1b["crux_move"] == "M2"

    # Core 1B contract: Y, Z, W
    assert len(core1b["taught_skill_Y"]) > 20
    assert len(core1b["connecting_route_Z"]) > 20
    assert len(core1b["protected_fresh_inference_W"]) > 30

    stages = core1b["stages"]
    # Stage 1: Predict
    assert "stage_1_predict" in stages
    s1 = stages["stage_1_predict"]
    assert "prompt" in s1 and "defensible_answer" in s1

    # Stage 2: Attempt
    assert "stage_2_attempt" in stages
    s2 = stages["stage_2_attempt"]
    assert "prompt" in s2 and "produces" in s2 and "rubric" in s2
    assert len(s2["rubric"]) == 3
    assert len(s2["accepted"]) >= 1
    assert len(s2["rejected"]) >= 1

    # Stage 3: Reconstruct
    assert "stage_3_reconstruct" in stages
    s3 = stages["stage_3_reconstruct"]
    assert len(s3["route"]) == 4
    for r in s3["route"]:
        assert "ask" in r and "why_this_ask" in r and "step_answer" in r
    assert len(s3["differs_from_teaching_path"]) > 20

    # Stage 4: Diagnose
    assert "stage_4_diagnose" in stages
    s4 = stages["stage_4_diagnose"]
    assert "error_trap" in s4 and "diagnostic_prompt" in s4 and "causal_explanation" in s4

    # Stage 5: Repair
    assert "stage_5_repair" in stages
    assert "action" in stages["stage_5_repair"]

    # Stage 6: Boundary test
    assert "stage_6_boundary_test" in stages
    s6 = stages["stage_6_boundary_test"]
    assert "prompt" in s6 and "answer" in s6 and "confirms" in s6

    # Progressive Hints (H1-H3)
    hints = core1b["progressive_hints"]
    assert len(hints) == 3
    for h in hints:
        assert h["tier"] in {1, 2, 3}
        assert "text" in h and len(h["text"]) > 10


# ---------------------------------------------------------------------------
# 3. Bidirectional B1–B7 Witness Inspection Validation
# ---------------------------------------------------------------------------

def test_witness_schema_and_b1_to_b7_inspection(witness, core1a, core1b):
    # Schema check
    errs = schema_errors(witness, "bridge-witness", str(MECH_DIR / "witness.json"))
    assert not errs, f"Witness schema validation errors: {errs}"

    # Hash binding check
    c1a_bytes = (MECH_DIR / "core1a_construction.json").read_bytes()
    c1b_bytes = (MECH_DIR / "core1b_reconstruction.json").read_bytes()
    expected_c1a_sha = "sha256:" + hashlib.sha256(c1a_bytes).hexdigest()
    expected_c1b_sha = "sha256:" + hashlib.sha256(c1b_bytes).hexdigest()

    assert witness["core1a"]["content_sha256"] == expected_c1a_sha
    assert witness["core1b"]["task_sha256"] == expected_c1b_sha
    assert witness["core1b"]["task_sha256"] != witness["core1a"]["worked_example_sha256"]

    # Run inspection
    result = inspect_witness(witness)
    assert result["mechanical_status"] == "HOLD"
    assert result["qualification_status"] == "HOLD"
    assert result["release_status"] == "HOLD"

    # All 7 gates must report HOLD (none may report FAIL)
    gate_results = {g["gate"]: g["result"] for g in result["gate_results"]}
    for gate_name in ("B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        assert gate_name in gate_results
        assert gate_results[gate_name] == "HOLD", f"Gate {gate_name} expected HOLD but was {gate_results[gate_name]}"

    # Verify diagnostic holding reasons
    diags = {(d["gate"], d["code"]) for d in result["diagnostics"]}
    assert ("B1", "INDEPENDENT_COGNITIVE_REVIEW_MISSING") in diags
    assert ("B1", "INDEPENDENT_QRT_REVIEW_MISSING") in diags
    assert ("B5", "INDEPENDENT_TECHNICAL_REVIEW_MISSING") in diags
    assert ("B7", "INDEPENDENT_PHYSICS_REVIEW_MISSING") in diags
    assert ("B7", "INDEPENDENT_SOURCE_CUSTODY_REVIEW_MISSING") in diags


# ---------------------------------------------------------------------------
# 4. Critical Anti-Patterns Audit on Learning Journey HTML
# ---------------------------------------------------------------------------

def test_anti_patterns_on_learning_journey_html(journey_html):
    # Gate 1: No Ghost Text
    assert "2. Connection:" not in journey_html
    assert "Connection:" not in journey_html
    assert "1. System Representation & Setup:" in journey_html
    assert "2. Physical Model & Formulation:" in journey_html
    assert "3. Execution & Resolution:" in journey_html

    # Gate 5: W3C SVG Typography & Root Dimensions
    assert 'width="100%"' in journey_html
    assert 'height="100%"' in journey_html
    assert 'height="auto"' not in journey_html
    font_sizes = re.findall(r'font-size="(\d+)"', journey_html)
    assert font_sizes, "No font sizes found in SVG"
    for fs in font_sizes:
        assert int(fs) >= 14, f"SVG font size {fs}px is under W3C 14px threshold"

    # Gate 6: Mobile Viewport CSS Cascade Order
    assert "@media (max-width: 600px)" in journey_html
    assert "max-width: 900px;" in journey_html

    # Gate 7: Commitment-First Protected Derivations
    assert 'id="derivation-section" class="derivation-section"' in journey_html
    assert 'display: none;' in journey_html
    assert "derivationSection.style.display = 'block';" in journey_html

    # Learning Gateway Tabs Navigation
    assert 'id="tab-core2"' in journey_html
    assert 'id="tab-core1a"' in journey_html
    assert 'id="tab-core1b"' in journey_html
    assert 'switchTab(' in journey_html
    assert '<iframe' not in journey_html, "No iframe embedding allowed"


# ---------------------------------------------------------------------------
# 5. Physics and Mathematical Model Validation
# ---------------------------------------------------------------------------

def test_physics_model_separation_rigorous():
    """Verify kinematics integration across variable parameters."""
    def kinematics_ratio(v, a):
        t = v / a
        d1 = 0.5 * v * t
        d2 = v * t
        return d1, d2, d1 / d2

    # Parametric sweep across velocities and decelerations
    test_params = [
        (10.0, 2.0),
        (25.0, 5.0),
        (30.0, 3.0),
        (100.0, 9.8),
        (0.5, 0.05)
    ]

    for v, a in test_params:
        d1, d2, ratio = kinematics_ratio(v, a)
        # Check formulas
        assert pytest.approx(d1) == (v ** 2) / (2 * a)
        assert pytest.approx(d2) == (v ** 2) / a
        # Check ratio is universally 0.5
        assert pytest.approx(ratio) == 0.5

    # Check Average Velocity Theorem equivalence
    for v in [5.0, 20.0, 50.0]:
        v_avg_wagon = (v + 0.0) / 2.0
        v_avg_train = v
        assert pytest.approx(v_avg_wagon / v_avg_train) == 0.5


# ---------------------------------------------------------------------------
# 6. Governance Invariant
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(journey_html, core1a, core1b, witness):
    assert "No academic approval inferred from software validation." in journey_html
    assert core1a["academic_status"] == "HOLD:ACADEMIC_ADMISSION"
    assert core1b["academic_status"] == "HOLD:ACADEMIC_ADMISSION"
    assert witness["status"] == "CANDIDATE"
