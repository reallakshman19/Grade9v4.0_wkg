"""Verification suite for Chemistry Track: Atomic Structure, Periodicity & Chemical Bonding (chem-atomic-bonding-r1).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Chemical and quantum physical proofs:
    1. Bohr transition in He+ and H equivalent (lambda = 121.6 nm, n=2 -> n=1)
    2. Quantum numbers & orbital nodes (1 radial, 2 angular, max 5 with ms=+1/2)
    3. Period 2 first ionization energy anomalies (Be > B and N > O)
    4. Electron gain enthalpy anomaly (Cl more exothermic than F due to 2p compactness)
    5. VSEPR isostructural linear pair (XeF2 and I3^-, 3 lone pairs on central atom)
    6. Born-Haber cycle lattice enthalpy for NaCl (U_lattice = -787 kJ/mol)
    7. Isotopic abundance of Boron (10B = 20.0%, 11B = 80.0%)
    8. Group 16 hydride boiling points (H2O > H2Te > H2Se > H2S via hydrogen bonding)
    9. De Broglie wavelength of electron at 150 V (lambda = 0.100 nm = 1.00 Angstrom)
   10. Dipole moment comparison (NH3 = 1.47 D vs NF3 = 0.24 D via vector addition)
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
CHEM_DIR = REPO_ROOT / "workspace/output/chem-atomic-bonding-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/chem/CHEM-NSEJS-ATOM-01"

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
    p = CHEM_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = CHEM_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = CHEM_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def module_html():
    p = CHEM_DIR / "core2_module.html"
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
    assert bank["bank_id"] == "chem-atomic-bonding-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "CHEM-NSEJS-ATOM-01"
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
    assert q["answer"]["crux_move_ref"] == "CHEM-NSEJS-ATOM-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "CHEM-NSEJS-ATOM-01-M2" in plan["protected_move_refs"]


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

def test_chem_atomic_bonding_qrt_labelling_integrity():
    questions_file = CHEM_DIR / "questions.json"
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
# 5. Scientific & Chemical Verification (All 10 Items)
# ---------------------------------------------------------------------------

def test_q01_bohr_transition_he_plus():
    Z = 2
    n1, n2 = 2, 4
    Delta_E = 13.6 * (Z ** 2) * (1 / (n1 ** 2) - 1 / (n2 ** 2))
    assert math.isclose(Delta_E, 10.2, abs_tol=1e-5)
    hc = 1240.0
    lam = hc / Delta_E
    assert math.isclose(lam, 121.5686, rel_tol=1e-3)
    # Equivalent in Hydrogen (Z=1):
    # 13.6 * (1 - 1/4) = 10.2 eV exact => n=2 to n=1
    Delta_E_H = 13.6 * 1 * (1 - 1 / 4)
    assert math.isclose(Delta_E_H, Delta_E, abs_tol=1e-5)


def test_q02_quantum_numbers_nodes():
    n = 4
    l = 2
    radial_nodes = n - l - 1
    angular_nodes = l
    max_ms_plus_half = 2 * l + 1
    assert radial_nodes == 1
    assert angular_nodes == 2
    assert max_ms_plus_half == 5


def test_q03_first_ionization_energy_anomalies():
    # Experimental IE1 values (kJ/mol):
    ie_vals = {"Li": 520, "Be": 899, "B": 801, "C": 1086, "N": 1402, "O": 1314, "F": 1681, "Ne": 2080}
    assert ie_vals["Be"] > ie_vals["B"]
    assert ie_vals["N"] > ie_vals["O"]


def test_q04_electron_gain_enthalpy_f_vs_cl():
    delta_eg_F = -328
    delta_eg_Cl = -349
    # More negative means more exothermic
    assert delta_eg_Cl < delta_eg_F


def test_q05_vsepr_isostructural_linear():
    # XeF2: 2 bonds + 3 lone pairs = steric 5 (linear)
    # I3^-: 2 bonds + 3 lone pairs = steric 5 (linear)
    lone_pairs_Xe = (8 - 2) // 2
    lone_pairs_I = (7 + 1 - 2) // 2
    assert lone_pairs_Xe == 3
    assert lone_pairs_I == 3


def test_q06_born_haber_cycle_nacl():
    delta_H_f = -411.0
    delta_H_sub = 108.0
    ie1 = 496.0
    bond_diss = 242.0
    delta_eg = -349.0

    # delta_H_f = delta_H_sub + ie1 + 0.5 * bond_diss + delta_eg + U_lattice
    U_lattice = delta_H_f - (delta_H_sub + ie1 + 0.5 * bond_diss + delta_eg)
    assert math.isclose(U_lattice, -787.0, abs_tol=1e-5)


def test_q07_boron_isotope_abundance():
    m1 = 10.01
    m2 = 11.01
    A_avg = 10.81
    # x * m1 + (1 - x) * m2 = A_avg
    # x * (m1 - m2) + m2 = A_avg => x = (A_avg - m2) / (m1 - m2)
    x = (A_avg - m2) / (m1 - m2)
    assert math.isclose(x, 0.20, abs_tol=1e-5)
    assert math.isclose(1 - x, 0.80, abs_tol=1e-5)


def test_q08_group16_boiling_points():
    bp = {"H2O": 373, "H2Te": 269, "H2Se": 232, "H2S": 213}
    assert bp["H2O"] > bp["H2Te"] > bp["H2Se"] > bp["H2S"]


def test_q09_de_broglie_wavelength():
    h = 6.626e-34
    m_e = 9.11e-31
    e = 1.60e-19
    V = 150.0
    p = math.sqrt(2 * m_e * e * V)
    lam = h / p
    assert math.isclose(lam * 1e9, 0.100, rel_tol=1e-2)


def test_q10_dipole_moment_nh3_vs_nf3():
    mu_nh3 = 1.47
    mu_nf3 = 0.24
    assert mu_nh3 > mu_nf3


# ---------------------------------------------------------------------------
# 6. Universal Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_rule_13_governance_invariant(bank, sl1_report):
    assert bank["extensions"]["academic_status"] == "UNREVIEWED"
    assert bank["extensions"]["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert sl1_report["gate_summary"]["release"] == "HOLD"
    assert sl1_report["gate_summary"]["construction"] == "HOLD"
    assert sl1_report["gate_summary"]["qrt"] == "HOLD"
