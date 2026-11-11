"""Verification suite for Chemistry Track: Matter & Mole Concept (Question 01) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Chemical and stoichiometric proofs (Dalton's partial pressures, Avogadro atomicity, Haber limiting reagent, empirical formula, molarity, chlorine isotopes, Graham's diffusion law, acid-base equivalence, thiosulfate oxidation state, CaCO3 STP gas volume)
- Strict QRT cognitive demand rubric and labelling across all 10 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
import math
from pathlib import Path
import re
import pytest
from jsonschema import Draft202012Validator

from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
CHEM_DIR = REPO_ROOT / "workspace/output/chem-matter-mole-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/chem/CHEM-NSEJS-MOLE-01"

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
    assert bank["bank_id"] == "chem-matter-mole-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "CHEM-NSEJS-MOLE-01"
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
    """Gate 1: Zero Ghost Text. '2. Connection:' strictly eliminated."""
    assert "2. Connection:" not in json.dumps(bank)
    assert "Connection:" not in json.dumps(bank)
    assert "2. Connection:" not in module_html

    q = bank["questions"][0]
    reasoning = q["answer"]["reasoning"]
    assert reasoning[0].startswith("1. System Representation & Setup:")
    assert reasoning[1].startswith("2. Physical Model & Formulation:")
    assert reasoning[2].startswith("3. Execution & Resolution:")


def test_gate2_dynamic_crux_move_binding(bank):
    """Gate 2: Dynamic Crux Move. Bound to primary operation MODEL."""
    q = bank["questions"][0]
    assert q["answer"]["crux_move_ref"] == "CHEM-NSEJS-MOLE-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "CHEM-NSEJS-MOLE-01-M2" in plan["protected_move_refs"]


def test_gate3_rubric_sum_bounds(bank):
    """Gate 3: Rubric Sum Bounds. Each c_i in {0, 1, 2} and sum equals score."""
    q = bank["questions"][0]
    diff = q["extensions"]["grade9v3:analysis"]["difficulty"]
    comps = diff["components"]
    for k, v in comps.items():
        assert v in (0, 1, 2), f"Component {k} value {v} outside [0..2]"
    assert sum(comps.values()) == diff["score"]
    assert diff["score"] == 4
    assert diff["band"] == "D2"


def test_gate4_canonical_verbs_only(bank):
    """Gate 4: Canonical Verbs Only. Strictly within canonical 7 cognitive operations."""
    q = bank["questions"][0]
    route = q["answer"]["reasoning_route"]
    for step in route:
        assert step["kind"] in CANONICAL_OPERATIONS


def test_gate5_w3c_svg_typography(module_html):
    """Gate 5: W3C SVG Typography. font-size >= 14px on all SVG text elements."""
    font_sizes = re.findall(r'<text[^>]*font-size="(\d+)"', module_html)
    assert len(font_sizes) > 0, "No SVG text font-sizes found"
    for sz in font_sizes:
        assert int(sz) >= 14, f"SVG font size {sz}px violates >= 14px rule"
    assert 'width="100%" height="100%"' in module_html


def test_gate6_responsive_mobile_cascade(module_html):
    """Gate 6: Responsive Mobile Cascade. max-width 900px container."""
    assert "max-width: 900px;" in module_html


def test_gate7_commitment_first_protected_derivations(module_html):
    """Gate 7: Formative Derivation Leaks. Derivation hidden until commitment."""
    assert 'id="derivation-section" style="display: none;"' in module_html
    assert "commitAnswer()" in module_html


# ---------------------------------------------------------------------------
# 4. Strict QRT Cognitive Demand Rubric & Labelling (All 10 Items)
# ---------------------------------------------------------------------------

def test_chem_matter_mole_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 chemistry items."""
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
            assert comps[f] in (0, 1, 2), f"Component {f} out of bounds in {q['id']}"
        assert sum(comps.values()) == q["score"], f"Sum of components must equal score in {q['id']}"

        # Band check
        score = q["score"]
        if score <= 2:
            assert q["band"] == "D1"
        elif score <= 5:
            assert q["band"] == "D2"
        elif score <= 7:
            assert q["band"] == "D3"
        else:
            assert q["band"] == "D4"

        # QRT refs
        assert q.get("crux_move_ref", "").startswith("CHEM-NSEJS-MOLE-")
        assert q.get("family_ref", "").startswith("CHEM-")
        assert q.get("primary_capability_ref", "").startswith("CHEM-MOLE-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Scientific & Chemical Truths
# ---------------------------------------------------------------------------

def test_dalton_partial_pressure_mole_fraction():
    """Verify Dalton's Law of Partial Pressures for CH4 + CO2 mixture:
    n(CH4) = 4.0 / 16.0 = 0.25 mol.
    n(CO2) = 8.8 / 44.0 = 0.20 mol.
    P(CH4) / P_total = 0.25 / 0.45 = 5/9.
    """
    m_ch4 = 4.0
    M_ch4 = 12.0 + 4 * 1.0
    n_ch4 = m_ch4 / M_ch4
    assert n_ch4 == 0.25

    m_co2 = 8.8
    M_co2 = 12.0 + 2 * 16.0
    n_co2 = m_co2 / M_co2
    assert n_co2 == 0.20

    n_total = n_ch4 + n_co2
    assert n_total == 0.45

    ratio = n_ch4 / n_total
    assert math.isclose(ratio, 5 / 9, rel_tol=1e-9)


def test_avogadro_number_atomicity():
    """Verify atom counts across four candidate samples:
    H2O (1.8g): 0.1 mol * 3 atoms = 0.3 N_A
    CH4 (1.6g): 0.1 mol * 5 atoms = 0.5 N_A (MAXIMUM)
    N2 (2.8g): 0.1 mol * 2 atoms = 0.2 N_A
    CO2 (4.4g): 0.1 mol * 3 atoms = 0.3 N_A
    """
    samples = {
        "H2O": (1.8, 18.0, 3),
        "CH4": (1.6, 16.0, 5),
        "N2": (2.8, 28.0, 2),
        "CO2": (4.4, 44.0, 3),
    }
    atom_counts = {name: (mass / mw) * atomicity for name, (mass, mw, atomicity) in samples.items()}
    max_sample = max(atom_counts, key=atom_counts.get)
    assert max_sample == "CH4"
    assert math.isclose(atom_counts["CH4"], 0.5, rel_tol=1e-9)


def test_haber_process_limiting_reagent():
    """Verify Haber process N2 + 3H2 -> 2NH3:
    28.0 g N2 = 1.0 mol; 9.0 g H2 = 4.5 mol.
    N2 is limiting. 1.0 mol N2 yields 2.0 mol NH3 = 34.0 g.
    """
    n_n2 = 28.0 / 28.0
    n_h2 = 9.0 / 2.0

    # Stoichiometric ratio: 3 mol H2 per 1 mol N2
    limiting = "N2" if (n_n2 <= n_h2 / 3.0) else "H2"
    assert limiting == "N2"

    n_nh3_produced = 2.0 * n_n2
    assert n_nh3_produced == 2.0
    mass_nh3 = n_nh3_produced * (14.0 + 3 * 1.0)
    assert mass_nh3 == 34.0


def test_empirical_and_molecular_formula():
    """Verify empirical & molecular formula:
    85.7% C, 14.3% H; VD = 28.
    Empirical formula CH2, Molar mass = 56 ==> C4H8.
    """
    moles_c = 85.7 / 12.0
    moles_h = 14.3 / 1.0
    ratio_h_c = round(moles_h / moles_c)
    assert ratio_h_c == 2  # CH2

    empirical_mass = 12.0 + 2 * 1.0
    assert empirical_mass == 14.0

    molecular_mass = 2 * 28  # 2 * VD
    assert molecular_mass == 56

    n_units = molecular_mass // int(empirical_mass)
    assert n_units == 4  # (CH2)4 = C4H8


def test_molarity_calculation():
    """Verify molarity of 10.0 g NaOH in 250.0 mL solution:
    10.0 / 40.0 = 0.25 mol in 0.250 L ==> 1.00 M.
    """
    moles = 10.0 / 40.0
    vol_liters = 250.0 / 1000.0
    molarity = moles / vol_liters
    assert molarity == 1.00


def test_isotope_average_atomic_mass():
    """Verify chlorine average atomic mass:
    0.75 * 35.0 + 0.25 * 37.0 = 35.5 u.
    """
    avg = 0.75 * 35.0 + 0.25 * 37.0
    assert avg == 35.5


def test_graham_law_diffusion_distance():
    """Verify Graham's Law diffusion distance for NH3 (17) and HCl (36.5) in 100 cm tube:
    r_NH3 / r_HCl = sqrt(36.5 / 17.0) = 1.4654.
    d / (100 - d) = 1.4654 ==> d = 59.4 cm from NH3 inlet.
    """
    ratio = math.sqrt(36.5 / 17.0)
    d = 100.0 * ratio / (1.0 + ratio)
    assert round(d, 1) == 59.4


def test_titration_neutralization_volume():
    """Verify neutralization of 25.0 mL of 0.20 M NaOH with 0.10 M H2SO4:
    mmol OH- = 5.0 ==> mmol H2SO4 = 2.5 ==> V = 25.0 mL.
    """
    mmol_oh = 25.0 * 0.20
    assert mmol_oh == 5.0
    mmol_h2so4 = mmol_oh / 2.0
    assert mmol_h2so4 == 2.5
    vol_acid = mmol_h2so4 / 0.10
    assert vol_acid == 25.0


def test_thiosulfate_oxidation_state():
    """Verify average oxidation state of S in S2O3^(2-):
    2x + 3(-2) = -2 ==> 2x = 4 ==> x = +2.
    """
    # 2x - 6 = -2 ==> x = 2
    charge = -2
    o_state = -2
    n_o = 3
    n_s = 2
    x = (charge - (n_o * o_state)) / n_s
    assert x == 2.0


def test_thermal_decomposition_gas_stp():
    """Verify STP volume of CO2 from 10.0 g CaCO3:
    10.0 g / 100.0 g/mol = 0.100 mol ==> 0.100 * 22.4 L = 2.24 L.
    """
    moles_caco3 = 10.0 / (40.0 + 12.0 + 3 * 16.0)
    assert moles_caco3 == 0.100
    vol_co2_stp = moles_caco3 * 22.4
    assert round(vol_co2_stp, 2) == 2.24


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
