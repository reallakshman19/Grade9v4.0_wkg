"""Verification suite for NSEJS 2022 Physics Ray Optics (D3 Prism) Core 1A and Core 1B Learning Journey.

Mechanical verification enforces:
- Core 1A declarative detailed teaching structure (conventions, prerequisites, inferential jump, worked anchor, wrong path, exit check)
- Core 1B 6-stage phenomenological reconstruction cycle (Predict, Attempt, Reconstruct, Diagnose, Repair, Boundary test)
- Bidirectional B1–B7 witness inspection via grade9qa.bridge_witness.inspect_witness
- Compliance with the 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards >= 14px, mobile CSS cascade, commitment-first inert derivations)
- Exact mathematical geometry and ray optics proofs (recurrence relation (2n + 1)A = 180 deg, n = 1 anchor 60 deg, n = 2 target 36 deg, n = 3 fresh practice 25.71 deg)
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
PRISM_DIR = REPO_ROOT / "workspace/output/nsejs-optics-prism-d3-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-2022-P-Q01"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def core1a():
    p = PRISM_DIR / "core1a_construction.json"
    assert p.exists(), f"Missing Core 1A file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def core1b():
    p = PRISM_DIR / "core1b_reconstruction.json"
    assert p.exists(), f"Missing Core 1B file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def witness():
    p = PRISM_DIR / "witness.json"
    assert p.exists(), f"Missing Witness file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def journey_html():
    p = PRISM_DIR / "learning_journey.html"
    assert p.exists(), f"Missing Learning Journey HTML: {p}"
    return p.read_text(encoding="utf-8")


@pytest.fixture
def bank():
    p = PRISM_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Core 1A Declarative Teaching Structure Validation
# ---------------------------------------------------------------------------

def test_core1a_structure_and_fields(core1a):
    assert core1a["schema"] == "core1a-construction/v1"
    assert core1a["construction_id"] == "PHYS-OPT-C-PRISM-SILVERED-01"
    assert core1a["target_question_id"] == "NSEJS-2022-P-Q01"
    assert core1a["topic"] == "OPTICS"
    assert core1a["family"] == "PHYS-OPTICS-PRISMS-INTERNAL-REFLECTION"
    assert core1a["cognitive_demand"] == "SYNTHESIZE"
    assert core1a["difficulty_band"] == "D3"
    assert core1a["difficulty_score"] == 6
    assert core1a["crux_move"] == "M2"

    # Declared conventions first
    conventions = core1a["declared_conventions"]
    assert len(conventions) >= 4
    conv_text = " ".join(c["statement"] for c in conventions)
    assert "specular" in conv_text.lower() or "reflection" in conv_text.lower()
    assert "normal" in conv_text.lower()
    assert "isosceles" in conv_text.lower()

    # Prerequisites
    assert len(core1a["entry_assumptions"]) >= 4

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

    # Worked conceptual anchor (must test contrasting 1-reflection equilateral case)
    anchor = core1a["worked_conceptual_anchor"]
    assert "equilateral" in anchor["problem"].lower() or "60" in anchor["problem"]
    assert len(anchor["solution_steps"]) == 4

    # Misconceptions
    misconceptions = core1a["misconception_diagnostics"]
    assert len(misconceptions) >= 2
    for m in misconceptions:
        assert "misconception" in m
        assert "root_cause" in m
        assert "repair" in m

    # Independent exit check
    exit_chk = core1a["exit_check"]
    assert "question" in exit_chk and "answer" in exit_chk and "verification" in exit_chk


# ---------------------------------------------------------------------------
# 2. Core 1B 6-Stage Phenomenological Reconstruction Validation
# ---------------------------------------------------------------------------

def test_core1b_structure_and_6_stages(core1b):
    assert core1b["schema"] == "core1b-reconstruction/v1"
    assert core1b["construction_id"] == "PHYS-OPT-C-PRISM-SILVERED-01"
    assert core1b["target_question_id"] == "NSEJS-2022-P-Q01"
    assert core1b["cognitive_demand"] == "SYNTHESIZE"
    assert core1b["difficulty_band"] == "D3"
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
    errs = schema_errors(witness, "bridge-witness", str(PRISM_DIR / "witness.json"))
    assert not errs, f"Witness schema validation errors: {errs}"

    # Hash binding check
    c1a_bytes = (PRISM_DIR / "core1a_construction.json").read_bytes()
    c1b_bytes = (PRISM_DIR / "core1b_reconstruction.json").read_bytes()
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

    # Verify all 7 gates B1-B7 are present and evaluated to HOLD
    gate_results = result["gate_results"]
    assert len(gate_results) == 7
    for g in gate_results:
        assert g["result"] == "HOLD", f"Gate {g['gate']} did not report HOLD: {g}"
        assert g["review_authority"] in ("UNVERIFIED", "HOLD")


# ---------------------------------------------------------------------------
# 4. Seven Anti-Patterns Quality Gate Compliance
# ---------------------------------------------------------------------------

def test_anti_patterns_compliance(journey_html, bank):
    q = bank["questions"][0]

    # Gate 1: No Ghost Text
    reasoning_text = " ".join(q["answer"]["reasoning"])
    assert "Connection:" not in reasoning_text
    assert "2. Connection:" not in reasoning_text
    assert "1. System Representation & Setup:" in journey_html
    assert "2. Physical Model & Formulation:" in journey_html
    assert "3. Execution & Resolution:" in journey_html

    # Gate 2: Dynamic Crux Binding
    assert q["answer"]["crux_move_ref"] == "NSEJS-2022-P-Q01-M2"
    assert "NSEJS-2022-P-Q01-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]

    # Gate 3: Rubric Sum Bounds (D3, Score 6)
    diff = q["difficulty"]
    comps = diff["components"]
    for k, v in comps.items():
        assert 0 <= v <= 2, f"Component {k} out of bounds: {v}"
    assert sum(comps.values()) == diff["score"]
    assert diff["score"] == 6
    assert diff["band"] == "D3"

    # Gate 4: Canonical Verbs Only
    for move in q["answer"]["reasoning_route"]:
        assert move["kind"] in CANONICAL_OPERATIONS, f"Illegal move operation: {move['kind']}"

    # Gate 5: W3C SVG Typography (font-size >= 14px) and root dimensions
    assert "<svg" in journey_html
    viewbox_match = re.search(r'viewBox="([^"]+)"', journey_html)
    assert viewbox_match, "SVG must have viewBox"
    parts = [float(p) for p in viewbox_match.group(1).split()]
    assert parts[2] >= 400 and parts[3] >= 200

    font_sizes = re.findall(r'font-size="(\d+(?:\.\d+)?)"', journey_html)
    assert font_sizes, "No font-size attributes found in SVG"
    for fs in font_sizes:
        val = float(fs)
        assert val >= 14.0, f"Font size {val}px violates W3C minimum 14px accessibility requirement"

    # Gate 6: Mobile Cascade Order
    desktop_idx = journey_html.find(".journey-container")
    media_idx = journey_html.find("@media (max-width: 600px)")
    assert desktop_idx < media_idx, "Base styles must precede media queries"

    # Gate 7: Commitment-First Protocol (Derivation inert)
    assert 'class="derivation-section"' in journey_html
    assert "display: none;" in journey_html
    assert 'id="commitC2"' in journey_html


# ---------------------------------------------------------------------------
# 5. Exact Mathematical Geometry & Ray Optics Physics Proof
# ---------------------------------------------------------------------------

def test_prism_multi_reflection_mathematical_proof():
    """Verify that for n internal reflections before normal emergence:
    Base angle satisfies B = n A.
    Isosceles closure gives A + 2B = 180 deg ==> A + 2(n A) = 180 deg ==> (2n + 1)A = 180 deg.
    """
    def compute_apex_angle(n):
        return 180.0 / (2 * n + 1)

    # n = 1 (Worked Anchor case: Equilateral prism)
    a1 = compute_apex_angle(1)
    assert a1 == 60.0
    b1 = 1 * a1
    assert a1 + 2 * b1 == 180.0

    # n = 2 (Target NSEJS-2022-P-Q01 problem)
    a2 = compute_apex_angle(2)
    assert a2 == 36.0
    b2 = 2 * a2  # 72.0 deg
    assert b2 == 72.0
    assert a2 + 2 * b2 == 180.0

    # n = 3 (Core 1B Fresh Challenge)
    a3 = compute_apex_angle(3)
    assert pytest.approx(a3, 1e-4) == 180.0 / 7  # 25.7142857 deg
    b3 = 3 * a3
    assert pytest.approx(a3 + 2 * b3, 1e-4) == 180.0


# ---------------------------------------------------------------------------
# 6. Governance Holding Status Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, journey_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in journey_html
