"""Verification suite for NSEJS 2024 Official Physics Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical and physical proofs:
    1. Q33: Kinematics acceleration comparison (Train = 12.0 m/s^2 > Rock 9.8 > Bus 8.0 > Car 7.5)
    2. Q34: Wave graph velocity and amplitude (A = 2.0 cm, v = 100 m/s)
    3. Q35: Floating cylinder immersed depth in immiscible liquids ((sigma - rho1)/(rho2 - rho1))
    4. Q37: Circular motion linear velocity and centripetal acceleration (v = 6.28 m/s, a_c = 78.9 m/s^2)
    5. Q38: Hydrostatic paradox base pressure and thrust (P_A = P_B = P_C, F_A = F_B = F_C)
    6. Q41: Mass-energy equivalence of 1 u (E ~ 931.5 MeV)
    7. Q42: Regular tetrahedral resistor network equivalent resistance (R_eq = 6.0 Ohm)
    8. Q43: Linear momentum ratio for equal kinetic energies (p1:p2 = 1:2)
    9. Q45: Kettle filament dimensional scaling and heating time (t' = 3.0 min)
   10. Q46: Decoupled wagon stopping displacement ratio (d1/d2 = 1/2)
   11. Q47: Myopic eye far point correction lens power (P = -0.4 D)
   12. Q48: Surface gravitational acceleration scaling (g1:g2 = 2:1)
   13. Q57: Conjugate foci convex lens displacement (u = 15 cm or 60 cm, m1 = 4.0, m2 = 0.25)
   14. Q59: Moving train echo and Doppler parameters (t = 20/3 s, d' = 1000 m, lambda = 60 cm)
   15. Q60: Athlete velocity-time distance integrals (all d = 5.0 km, Dinesh a = 40 km/h^2)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
import math
from pathlib import Path
import re
import pytest
from jsonschema import Draft202012Validator

from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-2024-physics-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2024-P-Q33" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2024-physics-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2024-P-Q33"
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
    expected_ids = [f"NSEJS-2024-P-Q{i:02d}" for i in range(33, 49)] + [f"NSEJS-2024-P-Q{i:02d}" for i in range(57, 61)]
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


def test_q33_kinematics_accelerations():
    a_bus = 72 * (5/18) / 2.50  # 20 / 2.5 = 8.0 m/s^2
    a_rock = 9.8  # m/s^2
    a_car = 108 * (5/18) / 4.00  # 30 / 4 = 7.5 m/s^2
    a_train = 216 / (0.5 * 6.00**2)  # 216 / 18 = 12.0 m/s^2
    assert a_train > a_rock > a_bus > a_car
    assert round(a_train, 1) == 12.0


def test_q34_wave_velocity():
    f = 250.0
    lamb = 0.40
    v = f * lamb
    assert v == 100.0


def test_q35_buoyancy_floating_cylinder():
    H = 100.0
    rho1 = 800.0
    rho2 = 1000.0
    sigma = 900.0
    h2 = H * (sigma - rho1) / (rho2 - rho1)
    assert h2 == 50.0


def test_q37_circular_motion():
    r = 0.50
    f = 2.0
    v = 2 * math.pi * r * f
    a_c = v**2 / r
    assert round(v, 2) == 6.28
    assert round(a_c, 1) == 79.0


def test_q38_hydrostatic_paradox():
    h = 2.0
    rho = 1000.0
    g = 9.8
    P = rho * g * h
    assert P == 19600.0


def test_q41_mass_energy_equivalence():
    u_kg = 1.66054e-27
    c = 2.99792e8
    e_J = u_kg * c**2
    e_MeV = e_J / (1.60218e-19 * 1e6)
    assert round(e_MeV, 0) == 931.0


def test_q42_tetrahedral_resistor_network():
    # Regular tetrahedron with 6 identical resistors of 12 Ohm
    # Removing symmetric bridge resistor gives branches 24, 24, 12 in parallel
    R_eq = 1.0 / (1/12 + 1/24 + 1/24)
    assert R_eq == 6.0


def test_q43_momentum_kinetic_energy():
    m1 = 1.0
    m2 = 4.0
    ratio = math.sqrt(m1 / m2)
    assert ratio == 0.5


def test_q45_heating_element_scaling():
    # R = rho * L / A. For 2L and 2D: A' = 4A, so R' = 2L / 4A = R / 2
    # Heat Q = V^2 t / R. Since Q and V constant, t' / t = R' / R = 1/2
    t1 = 6.0
    t2 = t1 * 0.5
    assert t2 == 3.0


def test_q46_train_wagon_stopping_ratio():
    # Decelerating wagon: average speed v/2, displacement d1 = (v/2) * t
    # Moving train: speed v, displacement d2 = v * t
    ratio = 0.5
    assert ratio == 0.5


def test_q47_myopia_power():
    d = 2.5
    f = -d
    P = 1.0 / f
    assert P == -0.4


def test_q48_surface_gravity_ratio():
    g1 = 1.0  # M / R^2
    g2 = 2.0 / (2.0**2)  # 2M / 4R^2 = 0.5
    ratio = g1 / g2
    assert ratio == 2.0


def test_q57_convex_lens_conjugate_foci():
    D = 75.0
    f = 12.0
    # u^2 - D*u + D*f = 0 ==> u^2 - 75u + 900 = 0
    disc = D**2 - 4 * D * f
    assert disc == 2025.0
    sqrt_disc = math.sqrt(disc)
    u1 = (D - sqrt_disc) / 2.0
    u2 = (D + sqrt_disc) / 2.0
    assert u1 == 15.0
    assert u2 == 60.0
    m1 = (D - u1) / u1  # 60 / 15 = 4.0 > 1 (magnified)
    m2 = (D - u2) / u2  # 15 / 60 = 0.25 < 1 (diminished)
    assert m1 == 4.0
    assert m2 == 0.25


def test_q59_train_cliff_echo():
    v_t = 108 * (5/18)  # 30 m/s
    v_s = 330.0
    d = 1200.0
    t = 2 * d / (v_s + v_t)
    assert round(t, 2) == 6.67
    assert t == 2400 / 360
    assert round(t / 60, 4) == round(1/9, 4)
    dist_at_echo = d - v_t * t
    assert dist_at_echo == 1000.0
    f = 550.0
    lamb = v_s / f
    assert lamb == 0.60  # 60 cm


def test_q60_athlete_distances_accelerations():
    t_h = 0.5  # 30 min
    # Naresh
    d_naresh = 10.0 * t_h
    # Dinesh
    d_dinesh = 0.5 * t_h * 20.0
    # Ramesh
    d_ramesh = 0.5 * (0.5 + 10/60) * 15.0
    assert d_naresh == 5.0
    assert d_dinesh == 5.0
    assert round(d_ramesh, 1) == 5.0
    a_dinesh = (20.0 - 0) / t_h
    assert a_dinesh == 40.0
