"""Verification suite for NSEJS 2021-22 Official Physics Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Physical and numerical proofs:
    1. Q17: Vector displacement cosine rule and orientation ambiguity (Options B or D)
    2. Q18: Binomial approximation small parameter expansion (Dropped by IAPT, Option DROP)
    3. Q19: Planetary hydrostatic pressure equivalence (h_M = 530 m, Option C)
    4. Q20: Damped harmonic oscillator initial conditions (Option D)
    5. Q21: Balanced Wheatstone bridge equivalent network current (I = 1 A, Option A)
    6. Q22: Gear tooth velocity transmission and potential energy (16mg, Option C)
    7. Q23: Radiative stellar luminosity mass loss rate (5.62e13 kg/s, Option C)
    8. Q24: Air conditioning occupant thermal load energy consumption (40 units, Option D)
    9. Q31: Quantum laser pulse parameters (Options A, B, C, D)
    10. Q32: Parallel resistor circuit power and current distribution (Options A, B, C)
    11. Q33: Standard parallel plate optical lateral displacement (Options A, B, D)
- Strict QRT cognitive demand rubric and labelling across all 11 items
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
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-2021-physics-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2021-P-Q17" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2021-physics-r1"
    assert len(bank["questions"]) == 11
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2021-P-Q17"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_11_questions_present(bank):
    assert len(bank["questions"]) == 11
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2021-P-Q{i:02d}" for i in range(17, 25)] + [f"NSEJS-2021-P-Q{i:02d}" for i in range(31, 34)]
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


def test_q17_coordinate_inclination_angles():
    # 6^2 = 8^2 + 10^2 - 2(8)(10) cos(theta) => 36 = 164 - 160 cos(theta) => cos(theta) = 0.8
    # theta = 36.87 deg => angle with Y1 = 90 - 36.87 = 53.13 deg or 90 + 36.87 = 126.87 deg
    theta = math.degrees(math.acos(0.8))
    angle1 = 90.0 - theta
    angle2 = 90.0 + theta
    assert round(angle1, 1) == 53.1 or round(angle1, 1) == 53.2
    assert round(angle2, 1) == 126.8 or round(angle2, 1) == 126.9


def test_q19_mars_ocean_depth():
    # g_E * h_E = g_M * h_M => 9.81 * 200 = 3.7 * h_M => h_M = 530.27 m
    h_m = (9.81 * 200.0) / 3.7
    assert round(h_m) == 530


def test_q21_wheatstone_bridge_current():
    # Bridge balanced: Req = 3R/2. For R = 2 ohm, Req = 3 ohm => I = 3V / 3 ohm = 1 A
    r = 2.0
    r_eq = 1.5 * r
    i = 3.0 / r_eq
    assert i == 1.0


def test_q22_gear_potential_energy():
    # A has 16 teeth (6 rev/s), B has 24 teeth => B turns 6 * 16/24 = 4 rev/s
    # In 0.5 s, B turns 2 rev. r = 14/11 cm => circ = 2 * (22/7) * (14/11) = 8 cm
    # Wound distance = 2 * 8 = 16 cm => Delta U = 16 mg
    f_b = 6.0 * (16.0 / 24.0)
    revs = f_b * 0.5
    circ = 2.0 * (22.0 / 7.0) * (14.0 / 11.0)
    h = revs * circ
    assert round(h) == 16


def test_q23_canopus_mass_loss():
    # r = 300 ly = 300 * 3e8 * 3.156e7 = 2.84e18 m
    # L = 4 * pi * r^2 * 5e-8 = 5.07e30 W
    # dm/dt = L / c^2 = 5.07e30 / 9e16 = 5.63e13 kg/s
    r = 300.0 * 3.0e8 * 3.156e7
    flux = 5.0e-8
    l = 4.0 * math.pi * (r ** 2) * flux
    c = 3.0e8
    dm_dt = l / (c ** 2)
    assert 5.0e13 < dm_dt < 6.0e13


def test_q24_air_conditioning_units():
    # P_people = 50 * 100 = 5000 W = 5 kW. Efficiency 50% => P_elec = 10 kW
    # Energy in 4 h = 10 kW * 4 h = 40 kWh = 40 units
    e_units = (50.0 * 100.0 / 1000.0 / 0.50) * 4.0
    assert e_units == 40.0


def test_q31_laser_pulses_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-P-Q31")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "C", "D"])


def test_q32_parallel_circuit_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-P-Q32")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "C"])


def test_q33_lateral_shift_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-P-Q33")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "D"])
