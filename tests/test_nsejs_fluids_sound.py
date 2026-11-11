"""Verification suite for Physics Track: Fluid Mechanics, Sound & Thermal Physics (nsejs-fluids-sound-r1).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical and physical proofs:
    1. Buoyant force in accelerating frame (T = 24.0 N, a_rel = 8.0 m/s^2)
    2. Flotation in two immiscible liquids (40.0%, 20.0 cm submerged in water)
    3. Horizontal accelerating U-tube level difference (Delta h = 5.00 cm)
    4. Coalescence of 1000 droplets surface energy released (Delta U = 8.48e-6 J)
    5. Excess pressure ratio bubble in liquid vs soap bubble in air (1 : 1)
    6. Resonance tube speed of sound and radius (v = 340 m/s, r = 1.67 cm)
    7. Parallel cliff echo distance and 3rd echo time (D = 680 m, t3 = 4.00 s)
    8. Doppler echo frequency and beat frequency (f_echo = 675 Hz, f_beat = 75 Hz)
    9. Calorimetry ice-water thermal equilibrium (Tf = 10.0 deg C, 0 g ice remaining)
   10. Bimetallic strip radius of curvature (R = 2.50 m)
- Strict QRT cognitive demand rubric and labelling across all 10 items
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
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-fluids-sound-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/PHYS-NSEJS-FLUID-01"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def source_custody():
    p = SOURCE_DIR / "source-custody.json"
    assert p.exists(), f"Missing custody file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def bank():
    p = PHYS_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
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


@pytest.fixture
def module_html():
    p = PHYS_DIR / "core2_module.html"
    assert p.exists(), f"Missing module HTML: {p}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Schema Validation
# ---------------------------------------------------------------------------

def test_source_custody_schema(source_custody):
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(source_custody))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert source_custody["custody_mode"] == "EMBEDDED_VERBATIM"
    assert source_custody["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-fluids-sound-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "PHYS-NSEJS-FLUID-01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


# ---------------------------------------------------------------------------
# 2. Smart Labelling Reports (via grade9qa.smart_skills)
# ---------------------------------------------------------------------------

def test_sl1_native_report_integrity(sl1_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert "INDEPENDENT_ACADEMIC_RELEASE_RECEIPTS" in summary["blocked_by"]
    assert sl1_report["gate_summary"]["integrity"] == "PASS"
    assert sl1_report["gate_summary"]["official_key"] == "PASS"


def test_sl2_native_report_integrity(sl2_report):
    summary = inspect_native_report(sl2_report)
    assert summary["native_check_status"] == "HOLD"
    assert summary["native_selected_gate"] == "qrt"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"


# ---------------------------------------------------------------------------
# 3. Seven Anti-Patterns Quality Gates
# ---------------------------------------------------------------------------

def test_gate1_zero_ghost_text(bank, module_html):
    assert "2. Connection:" not in json.dumps(bank)
    assert "Connection:" not in json.dumps(bank)
    assert "2. Connection:" not in module_html

    q = bank["questions"][0]
    reasoning = q["answer"]["reasoning"]
    assert reasoning[0].startswith("1. System Representation & Setup:")
    assert reasoning[1].startswith("2. Physical Model & Formulation:")
    assert reasoning[2].startswith("3. Execution & Resolution:")


def test_gate2_dynamic_crux_move_binding(bank):
    q = bank["questions"][0]
    assert q["answer"]["crux_move_ref"] == "PHYS-NSEJS-FLUID-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "PHYS-NSEJS-FLUID-01-M2" in plan["protected_move_refs"]


def test_gate3_rubric_sum_bounds(bank):
    q = bank["questions"][0]
    diff = q["extensions"]["grade9v3:analysis"]["difficulty"]
    comps = diff["components"]
    for k, v in comps.items():
        assert v in (0, 1, 2), f"Component {k} value {v} outside [0..2]"
    assert sum(comps.values()) == diff["score"]
    assert diff["score"] == 4
    assert diff["band"] == "D2"


def test_gate4_canonical_verbs_only(bank):
    q = bank["questions"][0]
    route = q["answer"]["reasoning_route"]
    for step in route:
        assert step["kind"] in CANONICAL_OPERATIONS


def test_gate5_w3c_svg_typography(module_html):
    font_sizes = re.findall(r'<text[^>]*font-size="(\d+)"', module_html)
    assert len(font_sizes) > 0, "No SVG text font-sizes found"
    for sz in font_sizes:
        assert int(sz) >= 14, f"SVG font size {sz}px violates >= 14px rule"
    assert 'width="100%" height="100%"' in module_html


def test_gate6_responsive_mobile_cascade(module_html):
    assert "max-width: 900px;" in module_html


def test_gate7_commitment_first_protected_derivations(module_html):
    assert 'id="derivation-section" class="derivation" style="display: none;"' in module_html
    assert "commitAnswer()" in module_html


# ---------------------------------------------------------------------------
# 4. Strict QRT Cognitive Demand Rubric & Labelling (All 10 Items)
# ---------------------------------------------------------------------------

def test_physics_fluids_qrt_labelling_integrity():
    questions_file = PHYS_DIR / "questions.json"
    assert questions_file.exists()
    questions = json.loads(questions_file.read_text(encoding="utf-8"))
    assert len(questions) == 10

    factors = (
        "concept_model_selection",
        "representation_translation",
        "reasoning_chain_length",
        "algebra_computational_load",
        "trap_exception_sensitivity"
    )

    for q in questions:
        assert "score" in q and isinstance(q["score"], int)
        assert "components" in q and isinstance(q["components"], dict)
        comps = q["components"]
        for f in factors:
            assert f in comps, f"Missing factor {f} in {q['id']}"
            assert comps[f] in (0, 1, 2), f"Invalid {f} score {comps[f]} in {q['id']}"
        assert sum(comps[f] for f in factors) == q["score"], f"Sum != score in {q['id']}"

        assert q["op"] in CANONICAL_OPERATIONS, f"Non-canonical op {q['op']} in {q['id']}"
        assert "crux_move_ref" in q
        expected_crux = "M3" if q["op"] == "JUSTIFY" else "M2"
        assert q["crux_move_ref"].endswith(expected_crux), f"Mismatch crux for {q['op']} in {q['id']}"

        assert "2. Connection:" not in json.dumps(q)
        assert "Connection:" not in json.dumps(q)

        assert len(q["hints"]) == 3
        assert len(q["steps"]) == 3
        assert q["steps"][0].startswith("1. System Representation & Setup:")
        assert q["steps"][1].startswith("2. Physical Model & Formulation:")
        assert q["steps"][2].startswith("3. Execution & Resolution:")


# ---------------------------------------------------------------------------
# 5. Scientific & Mathematical Verification (All 10 Items)
# ---------------------------------------------------------------------------

def test_q01_buoyant_force_accelerating_elevator():
    rho_s = 600.0
    m = 3.0
    rho_w = 1000.0
    a = 2.0
    g = 10.0
    g_eff = g + a
    V = m / rho_s
    F_B = V * rho_w * g_eff
    W_eff = m * g_eff
    T = F_B - W_eff
    a_rel = (F_B - W_eff) / m
    assert math.isclose(T, 24.0, abs_tol=1e-5)
    assert math.isclose(a_rel, 8.0, abs_tol=1e-5)


def test_q02_floating_cylinder_immiscible_liquids():
    L = 50.0
    rho = 880.0
    rho1 = 800.0
    rho2 = 1000.0
    frac_water = (rho - rho1) / (rho2 - rho1)
    L2 = frac_water * L
    assert math.isclose(frac_water, 0.40, abs_tol=1e-5)
    assert math.isclose(L2, 20.0, abs_tol=1e-5)


def test_q03_horizontal_accelerating_utube():
    L = 20.0
    a = 2.45
    g = 9.80
    delta_h = (a / g) * L
    assert math.isclose(delta_h, 5.00, abs_tol=1e-5)


def test_q04_coalescence_surface_energy():
    N = 1000
    r = 1.0e-4
    T = 0.075
    R = (N ** (1 / 3)) * r
    delta_A = 4 * math.pi * (N * (r ** 2) - (R ** 2))
    delta_U = T * delta_A
    assert math.isclose(delta_U, 8.4823e-6, rel_tol=1e-3)


def test_q05_excess_pressure_bubble_vs_droplet():
    T = 0.050
    r1 = 2.0e-3
    r2 = 4.0e-3
    delta_P1 = 2 * T / r1
    delta_P2 = 4 * T / r2
    assert math.isclose(delta_P1, 50.0, abs_tol=1e-5)
    assert math.isclose(delta_P2, 50.0, abs_tol=1e-5)
    assert math.isclose(delta_P1 / delta_P2, 1.0, abs_tol=1e-5)


def test_q06_resonance_tube_end_correction():
    f = 500.0
    l1 = 0.160
    l2 = 0.500
    lam = 2 * (l2 - l1)
    v = f * lam
    e = lam / 4 - l1
    r = e / 0.6
    assert math.isclose(v, 340.0, abs_tol=1e-5)
    assert math.isclose(r * 100, 1.66667, rel_tol=1e-3)


def test_q07_parallel_cliff_echoes():
    v = 340.0
    t1 = 1.60
    t2 = 2.40
    d1 = v * t1 / 2
    d2 = v * t2 / 2
    D = d1 + d2
    t3 = t1 + t2
    assert math.isclose(D, 680.0, abs_tol=1e-5)
    assert math.isclose(t3, 4.00, abs_tol=1e-5)


def test_q08_doppler_echo_and_beats():
    v = 340.0
    v_s = 20.0
    f = 600.0
    f_echo = f * (v + v_s) / (v - v_s)
    f_beat = abs(f_echo - f)
    assert math.isclose(f_echo, 675.0, abs_tol=1e-5)
    assert math.isclose(f_beat, 75.0, abs_tol=1e-5)


def test_q09_calorimetry_ice_water():
    m_w = 200.0
    T_w = 57.5
    c_w = 4.20
    m_ice = 100.0
    T_ice = -10.0
    c_ice = 2.10
    L_f = 336.0

    Q_warm_ice = m_ice * c_ice * abs(T_ice)
    Q_melt_ice = m_ice * L_f
    Q_ice_to_liquid_0 = Q_warm_ice + Q_melt_ice

    # 200 * 4.2 * (57.5 - Tf) = 35700 + 100 * 4.2 * Tf
    # 840 * 57.5 - 840 Tf = 35700 + 420 Tf
    # 48300 - 35700 = 1260 Tf
    # 12600 = 1260 Tf => Tf = 10.0
    Tf = (m_w * c_w * T_w - Q_ice_to_liquid_0) / (m_w * c_w + m_ice * c_w)
    assert math.isclose(Tf, 10.0, abs_tol=1e-5)


def test_q10_bimetallic_strip_curvature():
    d = 2.0e-3
    alpha1 = 1.90e-5
    alpha2 = 1.10e-5
    delta_T = 100.0
    R = d / ((alpha1 - alpha2) * delta_T)
    assert math.isclose(R, 2.50, abs_tol=1e-5)


# ---------------------------------------------------------------------------
# 6. Universal Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_rule_13_governance_invariant(bank, sl1_report):
    assert bank["extensions"]["academic_status"] == "UNREVIEWED"
    assert bank["extensions"]["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert sl1_report["gate_summary"]["release"] == "HOLD"
    assert sl1_report["gate_summary"]["construction"] == "HOLD"
    assert sl1_report["gate_summary"]["qrt"] == "HOLD"
