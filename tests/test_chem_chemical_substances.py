"""Verification suite for Chemistry Track: Chemical Substances — Nature & Behaviour (Topic 2) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Chemical, stoichiometric, and periodic proofs:
    1. Amphoteric oxide dual dissolution (Al2O3 + NaOH -> NaAlO2, Al2O3 + HCl -> AlCl3)
    2. Reactivity series displacement ordering (Q > P > S > R)
    3. Redox balancing of Cu + HNO3 -> Cu(NO3)2 + NO + H2O (3:2 ratio, sum of coeff = 20)
    4. Acid-base neutralization pH calculation (100 mL 0.10 M HCl + 100 mL 0.08 M NaOH -> pH = 2.00)
    5. Gypsum to Plaster of Paris partial dehydration (17.20 g -> 14.50 g POP + 2.70 g H2O)
    6. Sodium bicarbonate thermal decomposition (16.80 g -> 10.60 g Na2CO3 + 2.24 L CO2 STP)
    7. Butane structural isomers and complete combustion (2 isomers, 14.56 L O2 STP)
    8. Fischer esterification yield calculation (6.00 g acid + 4.60 g alcohol at 75% -> 6.60 g ester)
    9. Isoelectronic ionic radii ordering by nuclear charge (Mg2+ < Na+ < F- < O2-)
   10. Second period first ionization energy anomalies (Li < B < Be < C < O < N < F < Ne)
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
CHEM_DIR = REPO_ROOT / "workspace/output/chem-chemical-substances-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/chem/CHEM-NSEJS-REACT-01"

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
    assert bank["bank_id"] == "chem-chemical-substances-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "CHEM-NSEJS-REACT-01"
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
    assert q["answer"]["crux_move_ref"] == "CHEM-NSEJS-REACT-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "CHEM-NSEJS-REACT-01-M2" in plan["protected_move_refs"]


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

def test_chem_chemical_substances_qrt_labelling_integrity():
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
        assert q.get("crux_move_ref", "").startswith("CHEM-NSEJS-REACT-")
        assert q.get("family_ref", "").startswith("CHEM-")
        assert q.get("primary_capability_ref", "").startswith("CHEM-REACT-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Scientific & Chemical Truths
# ---------------------------------------------------------------------------

def test_amphoteric_oxide_dissolution_and_neutralization():
    """Verify Al2O3 + 2 NaOH -> 2 NaAlO2 + H2O and Al2O3 + 6 HCl -> 2 AlCl3 + 3 H2O:
    1.02 g / 102.0 g/mol = 0.010 mol Al2O3.
    Yields 0.020 mol NaAlO2 = 0.020 * 82.0 = 1.64 g.
    Dissolution in HCl requires 6 * 0.010 = 0.060 mol HCl.
    Volume of 0.50 M HCl = 0.060 / 0.50 = 0.120 L = 120 mL.
    """
    m_sample = 1.02
    # Solving 2.04(A + 55) = 1.64(2A + 48)
    # 2.04 A + 112.2 = 3.28 A + 78.72 => 1.24 A = 33.48 => A = 27.0
    A = (112.2 - 78.72) / (3.28 - 2.04)
    assert round(A, 1) == 27.0  # Aluminium

    mw_al2o3 = 2 * A + 3 * 16.0
    assert math.isclose(mw_al2o3, 102.0, rel_tol=1e-9)
    n_oxide = m_sample / mw_al2o3
    assert math.isclose(n_oxide, 0.010, rel_tol=1e-9)

    # NaOH product
    mw_naalo2 = 23.0 + A + 2 * 16.0
    assert math.isclose(mw_naalo2, 82.0, rel_tol=1e-9)
    mass_naalo2 = 2 * n_oxide * mw_naalo2
    assert math.isclose(mass_naalo2, 1.64, rel_tol=1e-9)

    # HCl volume
    n_hcl = 6 * n_oxide
    assert math.isclose(n_hcl, 0.060, rel_tol=1e-9)
    v_hcl_ml = (n_hcl / 0.50) * 1000.0
    assert math.isclose(v_hcl_ml, 120.0, rel_tol=1e-9)


def test_reactivity_series_displacement():
    """Verify displacement logic:
    Q displaces P, R, S => Q > P, R, S
    P displaces R, S => P > R, S
    S displaces R => S > R
    Combined: Q > P > S > R
    """
    order = ["Q", "P", "S", "R"]
    # Check pairwise conditions
    assert order.index("Q") < order.index("P")
    assert order.index("Q") < order.index("R")
    assert order.index("Q") < order.index("S")
    assert order.index("P") < order.index("R")
    assert order.index("P") < order.index("S")
    assert order.index("S") < order.index("R")


def test_redox_stoichiometry_copper_nitric_acid():
    """Verify balanced equation:
    3 Cu + 8 HNO3 -> 3 Cu(NO3)2 + 2 NO + 4 H2O
    Oxidized atoms: 3 (Cu: 0 -> +2)
    Reduced molecules: 2 (HNO3 -> NO: +5 -> +2)
    Ratio = 3 : 2.
    Sum of coefficients = 3 + 8 + 3 + 2 + 4 = 20.
    """
    coeff_cu = 3
    coeff_hno3 = 8
    coeff_cu_no3_2 = 3
    coeff_no = 2
    coeff_h2o = 4

    # Atom balances
    assert coeff_cu == coeff_cu_no3_2  # Cu: 3 = 3
    assert coeff_hno3 == 2 * coeff_h2o  # H: 8 = 8
    assert coeff_hno3 == 2 * coeff_cu_no3_2 + coeff_no  # N: 8 = 6 + 2 = 8
    assert 3 * coeff_hno3 == 6 * coeff_cu_no3_2 + coeff_no + coeff_h2o  # O: 24 = 18 + 2 + 4 = 24

    ratio = (coeff_cu, coeff_no)
    assert ratio == (3, 2)
    assert coeff_cu + coeff_hno3 + coeff_cu_no3_2 + coeff_no + coeff_h2o == 20


def test_acid_base_neutralization_ph():
    """Verify pH of mixture of 100 mL 0.100 M HCl and 100 mL 0.080 M NaOH:
    mmol H+ = 10.0; mmol OH- = 8.0.
    Excess mmol H+ = 2.0 in 200.0 mL => [H+] = 0.010 M.
    pH = -log10(0.010) = 2.00.
    """
    mmol_h = 100.0 * 0.100
    mmol_oh = 100.0 * 0.080
    excess_h = mmol_h - mmol_oh
    assert excess_h == 2.0
    v_total = 100.0 + 100.0
    conc_h = excess_h / v_total
    assert conc_h == 0.010
    ph = -math.log10(conc_h)
    assert round(ph, 2) == 2.00


def test_gypsum_to_plaster_of_paris():
    """Verify 17.20 g gypsum dehydration:
    CaSO4.2H2O -> CaSO4.0.5H2O + 1.5 H2O.
    17.20 g = 0.100 mol.
    Mass POP = 0.100 * 145.0 = 14.50 g.
    Mass water = 0.100 * 1.5 * 18.0 = 2.70 g.
    """
    mw_gypsum = 40.0 + 32.0 + 4 * 16.0 + 2 * 18.0  # 172.0
    mw_pop = 40.0 + 32.0 + 4 * 16.0 + 0.5 * 18.0   # 145.0
    n_gypsum = 17.20 / mw_gypsum
    assert math.isclose(n_gypsum, 0.100, rel_tol=1e-9)

    mass_pop = n_gypsum * mw_pop
    mass_h2o = n_gypsum * 1.5 * 18.0
    assert math.isclose(mass_pop, 14.50, rel_tol=1e-9)
    assert math.isclose(mass_h2o, 2.70, rel_tol=1e-9)
    assert math.isclose(mass_pop + mass_h2o, 17.20, rel_tol=1e-9)


def test_sodium_bicarbonate_thermal_decomposition():
    """Verify 16.80 g NaHCO3 decomposition:
    2 NaHCO3 -> Na2CO3 + H2O + CO2.
    0.200 mol NaHCO3 -> 0.100 mol Na2CO3 (10.60 g) + 0.100 mol CO2 (2.24 L STP).
    """
    mw_nahco3 = 23.0 + 1.0 + 12.0 + 3 * 16.0  # 84.0
    mw_na2co3 = 2 * 23.0 + 12.0 + 3 * 16.0     # 106.0
    n_nahco3 = 16.80 / mw_nahco3
    assert math.isclose(n_nahco3, 0.200, rel_tol=1e-9)

    n_products = n_nahco3 / 2.0
    assert math.isclose(n_products, 0.100, rel_tol=1e-9)
    mass_na2co3 = n_products * mw_na2co3
    assert math.isclose(mass_na2co3, 10.60, rel_tol=1e-9)
    vol_co2_stp = n_products * 22.4
    assert round(vol_co2_stp, 2) == 2.24


def test_butane_isomers_and_combustion():
    """Verify butane C4H10 (58.0 g/mol):
    Structural isomers: 2 (n-butane, isobutane).
    C4H10 + 6.5 O2 -> 4 CO2 + 5 H2O.
    5.80 g = 0.100 mol => 0.650 mol O2 => 0.650 * 22.4 L = 14.56 L STP.
    """
    mw_butane = 4 * 12.0 + 10 * 1.0
    assert mw_butane == 58.0
    n_butane = 5.80 / mw_butane
    assert math.isclose(n_butane, 0.100, rel_tol=1e-9)

    n_o2 = n_butane * 6.5
    assert math.isclose(n_o2, 0.650, rel_tol=1e-9)
    vol_o2_stp = n_o2 * 22.4
    assert round(vol_o2_stp, 2) == 14.56


def test_esterification_reaction_yield():
    """Verify 6.00 g CH3COOH + 4.60 g C2H5OH at 75.0% yield:
    0.100 mol acid + 0.100 mol alcohol.
    Theoretical yield = 0.100 mol ethyl ethanoate = 0.100 * 88.0 = 8.80 g.
    Actual yield = 8.80 * 0.75 = 6.60 g.
    """
    n_acid = 6.00 / 60.0
    n_alc = 4.60 / 46.0
    assert math.isclose(n_acid, 0.100, rel_tol=1e-9)
    assert math.isclose(n_alc, 0.100, rel_tol=1e-9)
    mw_ester = 4 * 12.0 + 8 * 1.0 + 2 * 16.0
    assert mw_ester == 88.0

    mass_actual = 0.100 * mw_ester * 0.75
    assert math.isclose(mass_actual, 6.60, rel_tol=1e-9)


def test_isoelectronic_radii_ordering():
    """Verify isoelectronic ionic radii order:
    Mg2+ (Z=12) < Na+ (Z=11) < F- (Z=9) < O2- (Z=8).
    All possess 10 electrons.
    """
    species = [("Mg2+", 12), ("Na+", 11), ("F-", 9), ("O2-", 8)]
    # Decreasing Z corresponds to increasing radius
    sorted_by_radius = [s[0] for s in sorted(species, key=lambda x: -x[1])]
    assert sorted_by_radius == ["Mg2+", "Na+", "F-", "O2-"]


def test_period2_ionization_energy_anomalies():
    """Verify second period IE1 order with anomalies:
    Li < B < Be < C < O < N < F < Ne.
    Be (2s2) > B (2s2 2p1) and N (2p3) > O (2p4).
    """
    empirical_ie1 = {
        "Li": 520,
        "B": 801,
        "Be": 899,
        "C": 1086,
        "O": 1314,
        "N": 1402,
        "F": 1681,
        "Ne": 2081
    }
    sorted_elements = sorted(empirical_ie1.keys(), key=lambda el: empirical_ie1[el])
    expected_order = ["Li", "B", "Be", "C", "O", "N", "F", "Ne"]
    assert sorted_elements == expected_order
    assert empirical_ie1["Be"] > empirical_ie1["B"]
    assert empirical_ie1["N"] > empirical_ie1["O"]


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
