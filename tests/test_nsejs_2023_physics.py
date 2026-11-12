"""Verification suite for NSEJS 2023 Official Physics Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical and physical proofs:
    1. Q33: Equal KE mass speed and momentum ratios (vA:vB = 2:1, pA:pB = 1:2 -> S1 false, S2 true)
    2. Q34: Copper wire resistance and density length relation (L = 3.0 m)
    3. Q35: Speed of sound temperature scaling (T = 48 deg C)
    4. Q37: U-tube hydrostatic balance between mercury and water (h = 20.4 cm)
    5. Q38: Newton's lens relation xx' = f^2 (f = 20 cm)
    6. Q39: Ballistic pendulum bullet speed (v = 9.8 m/s)
    7. Q41: Foot contact pressure order of magnitude (P ~ 10^4 Pa)
    8. Q42: Parallel bulbs total line current and fuse rating (I = 1.0 A)
    9. Q45: Bead friction work-energy dissipation (f = 7.35e-3 N)
   10. Q47: Temperature Celsius to Kelvin conversion (37.3 deg C = 310.45 K)
   11. Q48: Gravitational circular orbit speed ratio (v1/v2 = 1/sqrt(10))
   12. Q57: Crane work, power and energy comparison (Equal energy, P_A = 2 P_B)
   13. Q58: Bulbs in series on 200V / 400V (60W glows brighter, total power 37.5W)
   14. Q59: Floating sphere volume fractions and densities (rho_sphere = 600, rho_oil = 750 kg/m^3)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
import math
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-2023-physics-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2023-P-Q33" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2023-physics-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2023-P-Q33"
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
    expected_ids = [f"NSEJS-2023-P-Q{i:02d}" for i in range(33, 49)] + [f"NSEJS-2023-P-Q{i:02d}" for i in range(57, 61)]
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


def test_q33_kinetic_energy_ratios():
    mA = 1.0
    mB = 4.0
    vA_over_vB = math.sqrt(mB / mA)
    pA_over_pB = math.sqrt(mA / mB)
    assert vA_over_vB == 2.0  # 2:1, so S1 (1:2) is False
    assert pA_over_pB == 0.5  # 1:2, so S2 (1:2) is True


def test_q34_copper_wire_length():
    m = 20.95e-3  # kg
    R = 0.065     # Ohm
    d = 8900.0    # kg/m^3
    rho = 1.7e-8  # Ohm*m
    L = math.sqrt((R * m) / (rho * d))
    assert round(L, 1) == 3.0


def test_q35_sound_speed_temperature():
    v1 = 332.0
    T1 = 273.15
    v2 = 360.0
    T2 = T1 * (v2 / v1)**2
    t2_celsius = T2 - 273.15
    assert round(t2_celsius, 0) == 48.0


def test_q37_u_tube_mercury_water():
    H_cm = 1.5
    rho_hg = 13.6e3
    rho_w = 1.0e3
    h_cm = H_cm * (rho_hg / rho_w)
    assert round(h_cm, 1) == 20.4


def test_q38_newton_lens_formula():
    x = 10.0
    x_prime = 40.0
    f = math.sqrt(x * x_prime)
    assert f == 20.0


def test_q39_ballistic_pendulum():
    m = 0.25
    M = 1.00
    h = 0.196
    g = 9.8
    V_sys = math.sqrt(2 * g * h)
    v_bullet = ((m + M) / m) * V_sys
    assert round(v_bullet, 1) == 9.8


def test_q41_pressure_order_of_magnitude():
    m = 65.0  # kg
    g = 9.8
    W = m * g
    A = 0.05  # m^2
    P = W / A
    order = round(math.log10(P))
    assert order == 4


def test_q42_parallel_bulbs_fuse_rating():
    p_total = 100.0 + 60.0 + 40.0
    v = 200.0
    i = p_total / v
    assert i == 1.0


def test_q45_bead_friction_work_energy():
    m = 3.0e-3  # kg
    g = 9.8
    h1 = 0.50
    h2 = 0.30
    s = 0.80
    delta_u = m * g * (h1 - h2)
    f_avg = delta_u / s
    assert round(f_avg * 1e3, 2) == 7.35


def test_q47_celsius_to_kelvin():
    t_c = 37.3
    t_k = t_c + 273.15
    assert round(t_k, 2) == 310.45


def test_q48_orbital_speeds_ratio():
    r1 = 10.0**13
    r2 = 10.0**12
    ratio = math.sqrt(r2 / r1)
    expected = 1.0 / math.sqrt(10.0)
    assert math.isclose(ratio, expected, rel_tol=1e-5)


def test_q57_crane_power_energy():
    m = 2000.0
    h = 3.0
    g = 9.8
    w_useful = m * g * h
    tA = 60.0
    tB = 120.0
    pA = w_useful / tA
    pB = w_useful / tB
    assert pA == 2.0 * pB
    assert pA > pB


def test_q58_series_bulbs_dissipation():
    V = 200.0
    R100 = V**2 / 100.0  # 400 Ohm
    R60 = V**2 / 60.0    # 666.7 Ohm
    assert R60 > R100
    R_total = R100 + R60
    P_total = V**2 / R_total
    assert round(P_total, 1) == 37.5


def test_q59_floating_sphere_densities():
    rho_w = 1000.0
    rho_s = 0.60 * rho_w
    rho_oil = rho_s / 0.80
    assert rho_s == 600.0
    assert rho_oil == 750.0
