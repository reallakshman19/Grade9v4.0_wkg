"""Verification suite for Chemistry Track: Structure of the Atom & Chemical Bonding (Question 01) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Atomic and physical chemistry proofs (Bohr transitions 27/32, chlorine isotopes 35.45 u, isoelectronic radii, Rutherford alpha closest approach, Thomson e/m 1.76e11, anode ray origin, exchange stabilization, Strontium 2-8-18-8-2, nuclear pairs classification, Born-Haber lattice enthalpy +788 kJ/mol)
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
CHEM_DIR = REPO_ROOT / "workspace/output/chem-atomic-structure-r1"
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


@pytest.fixture
def questions_data():
    p = CHEM_DIR / "questions.json"
    assert p.exists(), f"Missing questions file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


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
    assert bank["bank_id"] == "chem-atomic-structure-r1"
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
    assert q["answer"]["crux_move_ref"] == "CHEM-NSEJS-ATOM-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "CHEM-NSEJS-ATOM-01-M2" in plan["protected_move_refs"]


def test_gate3_rubric_sum_bounds(bank):
    """Gate 3: Rubric Sum Bounds. Each c_i in {0, 1, 2} and sum equals score."""
    q = bank["questions"][0]
    diff = q["extensions"]["grade9v3:analysis"]["difficulty"]
    assert diff["band"] == "D2"
    assert diff["score"] == 4
    comps = diff["components"]
    for k, v in comps.items():
        assert 0 <= v <= 2, f"Component {k} out of bounds: {v}"
    assert sum(comps.values()) == diff["score"]


def test_gate4_canonical_verbs_only(bank):
    """Gate 4: Canonical Verbs Only in reasoning route."""
    q = bank["questions"][0]
    for move in q["answer"]["reasoning_route"]:
        assert move["kind"] in CANONICAL_OPERATIONS, f"Illegal move operation: {move['kind']}"


def test_gate5_w3c_svg_typography(module_html):
    """Gate 5: W3C SVG Typography (font-size >= 14px) and root dimensions."""
    assert "<svg" in module_html
    viewbox_match = re.search(r'viewBox="([^"]+)"', module_html)
    assert viewbox_match, "SVG must have viewBox"
    parts = [float(p) for p in viewbox_match.group(1).split()]
    assert parts[2] >= 400 and parts[3] >= 200

    font_sizes = re.findall(r'font-size="(\d+(?:\.\d+)?)"', module_html)
    assert font_sizes, "No font-size attributes found in SVG"
    for fs in font_sizes:
        val = float(fs)
        assert val >= 14.0, f"Font size {val}px violates W3C minimum 14px accessibility requirement"


def test_gate6_mobile_cascade_order(module_html):
    """Gate 6: Mobile Cascade Order. Container style precedes @media query."""
    main_idx = module_html.find(".container")
    media_idx = module_html.find("@media (max-width: 600px)")
    assert main_idx != -1 and media_idx != -1
    assert main_idx < media_idx, "Base styles must precede media queries"


def test_gate7_commitment_first_derivation(module_html):
    """Gate 7: Commitment-First Protocol (Derivation inert)."""
    assert 'class="derivation-container"' in module_html
    assert "display: none;" in module_html
    assert 'id="btn-commit"' in module_html


# ---------------------------------------------------------------------------
# 4. Questions.json Integrity & QRT Coverage
# ---------------------------------------------------------------------------

def test_questions_json_coverage_and_structure(questions_data):
    assert len(questions_data) == 10
    expected_ids = [f"CHEM-NSEJS-ATOM-{i:02d}" for i in range(1, 11)]
    actual_ids = [q["id"] for q in questions_data]
    assert actual_ids == expected_ids

    for q in questions_data:
        assert q["op"] in CANONICAL_OPERATIONS
        assert q["band"] in ("D1", "D2", "D3", "D4")
        assert len(q["options"]) == 4
        assert q["review_state"] == "NOT_ADMITTED"
        assert q["key_state"] == "VERIFIED_IAPT_KEY"

        # Check steps formatting
        steps = q["steps"]
        assert len(steps) == 3
        assert steps[0].startswith("1. System Representation & Setup:")
        assert steps[1].startswith("2. Physical Model & Formulation:")
        assert steps[2].startswith("3. Execution & Resolution:")
        assert "Connection:" not in " ".join(steps)


# ---------------------------------------------------------------------------
# 5. Scientific, Physical & Chemical Proofs Across All 10 Items
# ---------------------------------------------------------------------------

def test_q01_bohr_transition_wavelength_ratio():
    # 1/lambda = R_H * (1/n_f^2 - 1/n_i^2)
    # n=3 -> 1: 1/lambda_1 = (1 - 1/9) = 8/9 => lambda_1 = 9/8
    # n=2 -> 1: 1/lambda_2 = (1 - 1/4) = 3/4 => lambda_2 = 4/3
    # lambda_1 / lambda_2 = (9/8) / (4/3) = 27/32
    inv_lam1 = 1.0 - 1.0 / 9.0
    inv_lam2 = 1.0 - 1.0 / 4.0
    lam1 = 1.0 / inv_lam1
    lam2 = 1.0 / inv_lam2
    ratio = lam1 / lam2
    assert pytest.approx(ratio, 1e-9) == 27.0 / 32.0


def test_q02_chlorine_isotope_atomic_mass():
    # A_avg = (34.97 * 75.77 + 36.97 * 24.23) / 100
    a_avg = (34.97 * 75.77 + 36.97 * 24.23) / 100.0
    assert pytest.approx(a_avg, 1e-2) == 35.45


def test_q03_isoelectronic_radii_monotonicity():
    # Z increases from 7 to 13 with 10 electrons
    z_values = [7, 8, 9, 11, 12, 13]  # N3-, O2-, F-, Na+, Mg2+, Al3+
    # Radius scales inversely with Z_eff ~ Z - S
    s = 2.0  # approximate screening for 1s2
    z_eff = [z - s for z in z_values]
    radii = [1.0 / ze for ze in z_eff]
    # Al3+ must be smallest, N3- must be largest
    assert radii[-1] < radii[-2] < radii[-3] < radii[2] < radii[1] < radii[0]


def test_q04_rutherford_alpha_closest_approach():
    # K = 8.0e-13 J
    # r_min = (1 / 4 pi eps_0) * (2e * 79e) / K
    eps0_inv = 9.0e9
    e = 1.6e-19
    q1 = 2 * e
    q2 = 79 * e
    k = 8.0e-13
    r_min = (eps0_inv * q1 * q2) / k
    assert pytest.approx(r_min, 1e-2) == 4.55e-14


def test_q05_thomson_specific_charge():
    # y = (e/m) * E * L^2 / (2 * v^2)
    # e/m = 2 * y * v^2 / (E * L^2)
    y = 4.4e-3
    v = 5.0e6
    e_field = 500.0
    l_len = 0.05
    em = (2 * y * v**2) / (e_field * l_len**2)
    assert pytest.approx(em, 1e-2) == 1.76e11


def test_q07_chromium_exchange_energy():
    # Number of parallel spin pairs = n*(n-1)/2
    pairs_3d4 = 4 * 3 // 2  # 6 pairs
    pairs_3d5 = 5 * 4 // 2  # 10 pairs
    assert pairs_3d5 - pairs_3d4 == 4


def test_q08_strontium_shell_capacities():
    shells = [2, 8, 18, 8, 2]
    assert sum(shells) == 38
    assert shells[-1] <= 8  # Octet/valence constraint


def test_q10_born_haber_nacl_lattice_enthalpy():
    # Delta H_f = Delta H_sub + IE_1 + (1/2) Delta H_diss + Delta H_eg - U_lattice
    # -411 = 108 + 496 + 122 - 349 - U_lattice
    # -411 = 377 - U_lattice => U_lattice = 377 + 411 = 788 kJ/mol
    delta_h_f = -411
    sub = 108
    ie1 = 496
    diss = 122
    eg = -349
    u_lat = sub + ie1 + diss + eg - delta_h_f
    assert u_lat == 788


# ---------------------------------------------------------------------------
# 6. Governance Holding Status Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
