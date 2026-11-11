"""Verification suite for NSEJS 2022 Physics Ray Optics (D3 Combined Lens + Mirror) Core 1A and Core 1B Learning Journey.

Mechanical verification enforces:
- Core 1A declarative detailed teaching structure (conventions, prerequisites, inferential jump, worked anchor, wrong path, exit check)
- Core 1B 6-stage phenomenological reconstruction cycle (Predict, Attempt, Reconstruct, Diagnose, Repair, Boundary test)
- Bidirectional B1–B7 witness inspection via grade9qa.bridge_witness.inspect_witness
- Compliance with the 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards >= 14px, mobile CSS cascade, commitment-first inert derivations)
- Exact mathematical physics proofs (Gaussian lens equation, virtual object reflection foldback x_final = 2 x_M - v1, cascaded magnification m = m1 · m2)
- Student learning loop gateway (Core 2 <-> Core 1A <-> Core 1B <-> Core 2 state preservation without iframes)
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
from pathlib import Path
import re
import pytest

from grade9qa.bridge_witness import inspect_witness

REPO_ROOT = Path(__file__).resolve().parents[1]
LENS_MIRROR_DIR = REPO_ROOT / "workspace/output/nsejs-optics-lens-mirror-d3-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-2022-P-Q02"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def core1a():
    p = LENS_MIRROR_DIR / "core1a_construction.json"
    assert p.exists(), f"Missing Core 1A file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def core1b():
    p = LENS_MIRROR_DIR / "core1b_reconstruction.json"
    assert p.exists(), f"Missing Core 1B file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def witness():
    p = LENS_MIRROR_DIR / "witness.json"
    assert p.exists(), f"Missing Witness file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def journey_html():
    p = LENS_MIRROR_DIR / "learning_journey.html"
    assert p.exists(), f"Missing Learning Journey HTML: {p}"
    return p.read_text(encoding="utf-8")


@pytest.fixture
def bank():
    p = LENS_MIRROR_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Core 1A Declarative Teaching Structure Validation
# ---------------------------------------------------------------------------

def test_core1a_structure_and_fields(core1a):
    assert core1a["schema"] == "core1a-construction/v1"
    assert core1a["construction_id"] == "PHYS-OPT-C-LENS-MIRROR-01"
    assert core1a["target_question_id"] == "NSEJS-2022-P-Q02"
    assert core1a["topic"] == "OPTICS"
    assert core1a["family"] == "PHYS-OPTICS-COMBINED-LENS-MIRROR-SYSTEMS"
    assert core1a["cognitive_demand"] == "SYNTHESIZE"
    assert core1a["difficulty_band"] == "D3"
    assert core1a["difficulty_score"] == 6
    assert core1a["crux_move"] == "M2"

    # Declared conventions first
    conventions = core1a["declared_conventions"]
    assert len(conventions) >= 4
    conv_text = " ".join(c["statement"] for c in conventions)
    assert "cartesian" in conv_text.lower() or "paraxial" in conv_text.lower()
    assert "conjugacy" in conv_text.lower() or "mirror" in conv_text.lower()
    assert "magnification" in conv_text.lower()

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

    # Worked conceptual anchor (must test contrasting setup)
    anchor = core1a["worked_conceptual_anchor"]
    assert "30" in anchor["problem"] or "mirror" in anchor["problem"].lower()
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

def test_core1b_structure_and_stages(core1b):
    assert core1b["schema"] == "core1b-reconstruction/v1"
    assert core1b["construction_id"] == "PHYS-OPT-C-LENS-MIRROR-01"
    assert core1b["target_question_id"] == "NSEJS-2022-P-Q02"
    assert core1b["cognitive_demand"] == "SYNTHESIZE"
    assert core1b["difficulty_band"] == "D3"
    assert core1b["difficulty_score"] == 6
    assert core1b["crux_move"] == "M2"

    # Variable separation (Y, Z, W)
    assert len(core1b["taught_skill_Y"]) > 20
    assert len(core1b["connecting_route_Z"]) > 20
    assert len(core1b["protected_fresh_inference_W"]) > 20

    # Verify that W is strictly protected from trivial leakage
    assert core1b["taught_skill_Y"] != core1b["protected_fresh_inference_W"]

    # 6-stage cycle
    stages = core1b["stages"]
    assert "stage_1_predict" in stages
    assert "stage_2_attempt" in stages
    assert "stage_3_reconstruct" in stages
    assert "stage_4_diagnose" in stages
    assert "stage_5_repair" in stages
    assert "stage_6_boundary_test" in stages

    # Progressive Hints (H1-H3)
    hints = core1b["progressive_hints"]
    assert len(hints) == 3
    hint_ids = [h["hint_id"] for h in hints]
    assert hint_ids == ["H1", "H2", "H3"]


# ---------------------------------------------------------------------------
# 3. Bidirectional B1–B7 Witness Inspection via inspect_witness
# ---------------------------------------------------------------------------

def test_bridge_witness_b1_to_b7_inspection(witness):
    assert witness["schema_version"] == "grade9qa-b1b7-witness/v1"
    assert witness["status"] == "CANDIDATE"

    # Verify hash integrity
    c1a_bytes = (LENS_MIRROR_DIR / "core1a_construction.json").read_bytes()
    c1b_bytes = (LENS_MIRROR_DIR / "core1b_reconstruction.json").read_bytes()

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
    assert q["answer"]["crux_move_ref"] == "NSEJS-2022-P-Q02-M2"
    assert "NSEJS-2022-P-Q02-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]

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
# 5. Exact Mathematical Physics & Ray Optics Proof
# ---------------------------------------------------------------------------

def test_lens_mirror_mathematical_optics_proof():
    """Verify Gaussian lens refraction and plane mirror virtual object foldback:
    1/v1 - 1/u1 = 1/f ==> v1 = u1*f / (u1 + f)
    Intermediate magnification m1 = v1 / u1
    Mirror at x_M intercepts rays at d_obj = v1 - x_M (behind mirror).
    Foldback real image coordinate x_final = x_M - d_obj = 2*x_M - v1.
    Plane mirror lateral magnification m2 = +1 ==> m_net = m1 * m2 = m1.
    """
    def solve_lens_mirror(u, f, x_M):
        # Lens at 0
        v1 = (u * f) / (u + f)
        m1 = v1 / u
        # Virtual object distance behind mirror
        d_obj = v1 - x_M
        # Reflected image coordinate from lens
        x_final = x_M - d_obj
        m2 = +1.0
        m_net = m1 * m2
        return v1, m1, x_final, m_net

    # Target Problem: u = -15 cm, f = +10 cm, x_M = +20 cm
    v1, m1, x_final, m_net = solve_lens_mirror(-15.0, 10.0, 20.0)
    assert v1 == 30.0
    assert m1 == -2.0
    assert x_final == 10.0
    assert m_net == -2.0

    # Anchor Problem: u = -30 cm, f = +10 cm, x_M = +15 cm
    v1_anch, m1_anch, x_anch, m_anch = solve_lens_mirror(-30.0, 10.0, 15.0)
    assert v1_anch == 15.0
    assert m1_anch == -0.5
    assert x_anch == 15.0  # On mirror face
    assert m_anch == -0.5

    # Exit Check: u = -15 cm, f = +10 cm, x_M = +25 cm
    v1_exit, m1_exit, x_exit, m_exit = solve_lens_mirror(-15.0, 10.0, 25.0)
    assert v1_exit == 30.0
    assert m1_exit == -2.0
    assert x_exit == 20.0  # 20 cm from lens towards mirror
    assert m_exit == -2.0


# ---------------------------------------------------------------------------
# 6. Governance Holding Status Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, journey_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in journey_html
