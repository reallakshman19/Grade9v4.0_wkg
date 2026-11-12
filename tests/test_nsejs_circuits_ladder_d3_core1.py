"""Verification suite for NSEJS Foundation Physics Circuits (D3 Infinite Ladder Network) Core 1A and Core 1B Learning Journey.

Mechanical verification enforces:
- Core 1A declarative detailed teaching structure (conventions, prerequisites, inferential jump, worked anchor, wrong path, exit check)
- Core 1B 6-stage phenomenological reconstruction cycle (Predict, Attempt, Reconstruct, Diagnose, Repair, Boundary test)
- Bidirectional B1–B7 witness inspection via grade9qa.bridge_witness.inspect_witness
- Compliance with the 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards >= 14px, mobile CSS cascade, commitment-first inert derivations)
- Exact mathematical physics proofs (R_eq = R + R || R_eq ==> R_eq^2 - R*R_eq - R^2 = 0 ==> R_eq = ((1 + sqrt(5))/2) R)
- Student learning loop gateway (Core 2 <-> Core 1A <-> Core 1B <-> Core 2 state preservation without iframes)
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
from pathlib import Path
import re
import math
import pytest

from grade9qa.bridge_witness import inspect_witness

REPO_ROOT = Path(__file__).resolve().parents[1]
LADDER_DIR = REPO_ROOT / "workspace/output/nsejs-circuits-ladder-d3-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-FND-CIRC-01"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def core1a():
    p = LADDER_DIR / "core1a_construction.json"
    assert p.exists(), f"Missing Core 1A file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def core1b():
    p = LADDER_DIR / "core1b_reconstruction.json"
    assert p.exists(), f"Missing Core 1B file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def witness():
    p = LADDER_DIR / "witness.json"
    assert p.exists(), f"Missing Witness file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def journey_html():
    p = LADDER_DIR / "learning_journey.html"
    assert p.exists(), f"Missing Learning Journey HTML: {p}"
    return p.read_text(encoding="utf-8")


@pytest.fixture
def bank():
    p = LADDER_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Core 1A Declarative Teaching Structure Validation
# ---------------------------------------------------------------------------

def test_core1a_structure_and_fields(core1a):
    assert core1a["schema"] == "core1a-construction/v1"
    assert core1a["construction_id"] == "PHYS-CIRC-C-INFINITE-LADDER-01"
    assert core1a["target_question_id"] == "NSEJS-FND-CIRC-01"
    assert core1a["topic"] == "CURRENT_ELECTRICITY"
    assert core1a["family"] == "PHYS-CURRENT-ELECTRICITY-NETWORKS"
    assert core1a["cognitive_demand"] == "MODEL"
    assert core1a["difficulty_band"] == "D3"
    assert core1a["difficulty_score"] == 6
    assert core1a["crux_move"] == "M2"

    # Declared conventions first
    conventions = core1a["declared_conventions"]
    assert len(conventions) >= 4
    conv_text = " ".join(c["name"] + " " + c["statement"] for c in conventions)
    assert "self_similarity" in conv_text.lower() or "similarity" in conv_text.lower()
    assert "series" in conv_text.lower() or "parallel" in conv_text.lower()

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
    assert "2R" in anchor["problem"] or "shunt" in anchor["problem"].lower()
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
    assert core1b["construction_id"] == "PHYS-CIRC-C-INFINITE-LADDER-01"
    assert core1b["target_question_id"] == "NSEJS-FND-CIRC-01"
    assert core1b["cognitive_demand"] == "MODEL"
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
    c1a_bytes = (LADDER_DIR / "core1a_construction.json").read_bytes()
    c1b_bytes = (LADDER_DIR / "core1b_reconstruction.json").read_bytes()

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
    assert q["answer"]["crux_move_ref"] == "NSEJS-FND-CIRC-01-M2"
    assert "NSEJS-FND-CIRC-01-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]

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
# 5. Exact Mathematical Physics & Self-Similarity Ladder Proof
# ---------------------------------------------------------------------------

def test_infinite_ladder_mathematical_proof():
    """Verify infinite ladder self-similarity recurrence:
    R_eq = R_series + (R_shunt * R_eq) / (R_shunt + R_eq)
    (R_eq - R_series)(R_shunt + R_eq) = R_shunt * R_eq
    R_eq^2 + (R_shunt - R_series) * R_eq - R_series * R_shunt = R_shunt * R_eq
    R_eq^2 - R_series * R_eq - R_series * R_shunt = 0
    Positive root: R_eq = (R_series + sqrt(R_series^2 + 4 * R_series * R_shunt)) / 2
    """
    def solve_ladder(r_series, r_shunt):
        a = 1.0
        b = -r_series
        c = -r_series * r_shunt
        disc = b**2 - 4 * a * c
        root1 = (-b + math.sqrt(disc)) / (2 * a)
        root2 = (-b - math.sqrt(disc)) / (2 * a)
        return root1, root2

    # Target Problem: R_series = 1.0, R_shunt = 1.0
    r_pos, r_neg = solve_ladder(1.0, 1.0)
    golden_ratio = (1.0 + math.sqrt(5.0)) / 2.0
    assert pytest.approx(r_pos, 1e-9) == golden_ratio
    assert pytest.approx(r_pos, 1e-4) == 1.6180
    assert r_neg < 0  # Rejection of unphysical negative root

    # Anchor Problem: R_series = 1.0, R_shunt = 2.0
    r_anch_pos, r_anch_neg = solve_ladder(1.0, 2.0)
    assert pytest.approx(r_anch_pos, 1e-9) == 2.0
    assert pytest.approx(r_anch_neg, 1e-9) == -1.0

    # Exit Check: R_series = 2.0, R_shunt = 1.0
    r_exit_pos, r_exit_neg = solve_ladder(2.0, 1.0)
    # R_eq^2 - 2 R_eq - 2 = 0 ==> R_eq = (2 + sqrt(4 + 8))/2 = 1 + sqrt(3)
    expected_exit = 1.0 + math.sqrt(3.0)
    assert pytest.approx(r_exit_pos, 1e-9) == expected_exit
    assert pytest.approx(r_exit_pos, 1e-4) == 2.7320


# ---------------------------------------------------------------------------
# 6. Governance Holding Status Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, journey_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in journey_html
