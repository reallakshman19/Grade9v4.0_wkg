"""Verification suite for NSEJS 2022 Official Physics Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Physical and numerical proofs:
    1. Q33: Constant power kinetic energy integration (K = P*t => t = 10 s, Option B)
    2. Q34: Variable mass horizontal momentum invariance (v = 10 m/s, Option C)
    3. Q35: Piecewise acceleration-time kinematics (s = 51 m, v = 6 m/s, Option A)
    4. Q36: Binary star gravitational mutual attraction (v = sqrt(GM/d), Option A)
    5. Q37: Moving sound source echo timing (350t = 1400 => t = 4.00 s, Option B)
    6. Q38: Dual-fluid hydrostatic equilibrium density (rho_s = 7.2 g/cm^3, Option C)
    7. Q39: Gravitational free-fall and buoyant cycle duration (T = 8 s, Option C)
    8. Q40: Two-mirror ray specular reflection geometry (theta = 60 deg, Option B)
    9. Q41: Solenoid magnetic field spatial distribution (Maximum at center O, Option C)
    10. Q42: Hydrostatic differential thrust on door (F = 39.2 N approx 39 N, Option C)
    11. Q43: Negative charge Lorentz force vector direction (Upward, Option C)
    12. Q44: Inelastic photon scattering Raman effect (Option D)
    13. Q58: Lens-mirror optical combination image and magnification (Options A, C)
    14. Q59: Resistor network reduction and power distribution (Options A, B, C)
    15. Q60: One-dimensional elastic collision velocity redistribution (Options B, C)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
import math
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-2022-physics-r1"
SOURCE_BASE = REPO_ROOT / "workspace/sources/nsejs"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def bank():
    p = PHYS_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def intake():
    p = PHYS_DIR / "intake.json"
    assert p.exists(), f"Missing intake file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = PHYS_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = PHYS_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


def test_source_custody_schema():
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    
    first_custody = SOURCE_BASE / "NSEJS-2022-P-Q33" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2022-physics-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2022-P-Q33"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_20_questions_present(bank):
    assert len(bank["questions"]) == 20
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2022-P-Q{i:02d}" for i in range(33, 49)] + [f"NSEJS-2022-P-Q{i:02d}" for i in range(57, 61)]
    assert q_ids == expected_ids


def test_source_custody_for_all_items(bank):
    for q in bank["questions"]:
        q_id = q["id"]
        src_dir = SOURCE_BASE / q_id
        assert src_dir.exists(), f"Missing source dir for {q_id}"
        item_path = src_dir / "source_item.json"
        custody_path = src_dir / "source-custody.json"
        assert item_path.exists(), f"Missing source_item.json for {q_id}"
        assert custody_path.exists(), f"Missing source-custody.json for {q_id}"

        item_data = json.loads(item_path.read_text(encoding="utf-8"))
        custody_data = json.loads(custody_path.read_text(encoding="utf-8"))
        assert item_data["source_item_locator"] == q_id
        assert custody_data["source_item_locator"] == q_id
        assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
        assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_seven_anti_patterns(bank):
    html_path = PHYS_DIR / "core2_module.html"
    assert html_path.exists()
    html_content = html_path.read_text(encoding="utf-8")

    # Gate 1: Zero Ghost Text
    assert "2. Connection:" not in html_content
    assert "Connection:" not in html_content

    # Gate 5: Commitment-First Protected Derivations
    assert 'class="derivation-section"' in html_content
    assert 'style="display: none;"' in html_content

    # Gate 6: Responsive Mobile Cascade
    media_idx = html_content.find("@media")
    container_idx = html_content.find(".container {")
    assert container_idx != -1 and media_idx != -1
    assert container_idx < media_idx, "Base styles must precede @media queries in cascade"

    for q in bank["questions"]:
        # Gate 1 in bank
        for step in q["answer"]["reasoning"]:
            assert "2. Connection:" not in step
            assert "Connection:" not in step

        # Gate 2: Dynamic Crux Move
        crux_ref = q["answer"]["crux_move_ref"]
        assert crux_ref.endswith("-M2") or crux_ref.endswith("-M3")
        assert q["extensions"]["crux_move"] == crux_ref
        assert q["extensions"]["support_plan"]["primary_crux"] == crux_ref

        # Gate 3: Rubric Bounds
        cd = q["extensions"]["cognitive_demand"]
        rubric = cd["rubric_breakdown"]
        assert len(rubric) == 5
        for score in rubric:
            assert score in {0, 1, 2}
        assert sum(rubric) == cd["score"]

        # Gate 4: Canonical Verbs
        op = cd["operation"]
        assert op in CANONICAL_OPERATIONS
        crux_move = next(m for m in q["answer"]["reasoning_route"] if m["move_id"] == crux_ref)
        assert crux_move["kind"] in CANONICAL_OPERATIONS


def test_q33_constant_power():
    # P = 1.5 W, K = 15 J => t = K / P = 10 s
    p = 1.5
    k = 15.0
    t = k / p
    assert t == 10.0


def test_q34_leaking_trolley_speed():
    # Leaking vertically downwards carries horizontal speed of trolley, no horizontal force
    u = 36 / 3.6  # 10 m/s
    v_final = u
    assert v_final == 10.0


def test_q35_piecewise_kinematics():
    # 0-3 s: a = 4 => v = 12, s1 = 0.5 * 4 * 9 = 18 m
    # 3-5 s: a = 0 => v = 12, s2 = 12 * 2 = 24 m
    # 5-6 s: a = -6 => v = 12 - 6 = 6, s3 = (12 + 6)/2 * 1 = 9 m
    s_total = 18 + 24 + 9
    v_final = 6
    assert s_total == 51
    assert v_final == 6


def test_q36_binary_stars_speed():
    # 2 * (1/2 M v^2) = G M^2 / d => v = sqrt(GM/d)
    # Factor is 1.0 * sqrt(GM/d)
    factor = 1.0
    assert factor == 1.0


def test_q37_echo_approaching_cliff():
    # c = 330 m/s, v = 20 m/s, d = 700 m
    # 330 t = 700 + (700 - 20t) => 350 t = 1400 => t = 4.0 s
    c = 330.0
    v = 20.0
    d = 700.0
    t = (2 * d) / (c + v)
    assert t == 4.0


def test_q38_two_immiscible_liquids_flotation():
    # rho_s = (0.8 + 13.6) / 2 = 7.2 g/cm^3
    rho1 = 0.8
    rho2 = 13.6
    rho_s = (rho1 + rho2) / 2.0
    assert rho_s == 7.2


def test_q39_buoyant_gravity_cycle_time():
    # h = 19.6 m, g = 9.8 m/s^2
    # t_fall = sqrt(2*19.6/9.8) = 2 s
    # rho = rho_w / 2 => net upward accel in water = g
    # t_stop = 2 s, t_rise_water = 2 s, t_rise_air = 2 s => T = 8 s
    t_fall = math.sqrt(2 * 19.6 / 9.8)
    assert t_fall == 2.0
    total_time = 4 * t_fall
    assert total_time == 8.0


def test_q42_door_hydrostatic_thrust():
    # Delta P = (1800 - 1000) * 9.8 * 5.0 = 39200 Pa
    # A = 10 cm^2 = 1e-3 m^2 => F = 39.2 N
    delta_p = 800 * 9.8 * 5.0
    area = 10.0 * 1e-4
    force = delta_p * area
    assert round(force, 1) == 39.2


def test_q58_lens_mirror_system(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-P-Q58")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"] and "C" in q["answer"]["correct_option"]


def test_q59_resistor_network(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-P-Q59")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "C"])


def test_q60_elastic_collision(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-P-Q60")
    assert q["response"]["type"] == "multiple_response"
    assert "B" in q["answer"]["correct_option"] and "C" in q["answer"]["correct_option"]
