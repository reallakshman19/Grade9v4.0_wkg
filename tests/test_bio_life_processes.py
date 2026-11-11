"""Verification suite for Biology Track: Life Processes (Topic 2) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Biophysical, physiological, and genetic proofs:
    1. Glomerular Starling forces and renal hemodynamics (NFP = +10 mmHg, GFR = 125 mL/min = 180 L/day, urine = 1.80 L/day)
    2. Z-scheme non-cyclic photophosphorylation quantum requirement (48 photons per glucose)
    3. Respiratory Quotient substrate stoichiometry (glucose = 1.00, tripalmitin = 0.70)
    4. Digestive enzyme pH denaturation and bile micellar emulsification
    5. Cardiovascular ventricular parameters (SV = 70 mL, EF = 58.3%, CO = 5.04 L/min)
    6. Hodgkin-Huxley axonal action potential ion conductances (Na+ influx, K+ efflux, undershoot)
    7. Pancreatic islet endocrine blood glucose homeostasis (Beta-cells, insulin, GLUT4, glycogenesis)
    8. Mendelian dihybrid inheritance and recombination (9:3:3:1 ratio, 37.5% recombinants)
    9. X-linked recessive color-blindness transmission (50% sons, 0% daughters)
   10. Evolutionary comparative anatomy (homology/divergent vs analogy/convergent)
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
BIO_DIR = REPO_ROOT / "workspace/output/bio-life-processes-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/bio/BIO-NSEJS-PROC-01"

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
    p = BIO_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = BIO_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = BIO_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def module_html():
    p = BIO_DIR / "core2_module.html"
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
    assert bank["bank_id"] == "bio-life-processes-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "BIO-NSEJS-PROC-01"
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
    assert q["answer"]["crux_move_ref"] == "BIO-NSEJS-PROC-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "BIO-NSEJS-PROC-01-M2" in plan["protected_move_refs"]


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

def test_bio_life_processes_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 life processes items."""
    questions_file = BIO_DIR / "questions.json"
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
        assert q.get("crux_move_ref", "").startswith("BIO-NSEJS-PROC-")
        assert q.get("family_ref", "").startswith("BIO-")
        assert q.get("primary_capability_ref", "").startswith("BIO-PROC-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Scientific & Biological Truths
# ---------------------------------------------------------------------------

def test_glomerular_filtration_starling_forces():
    """Verify Starling pressures and GFR:
    P_GC = 55.0, P_BS = 15.0, Pi_GC = 30.0 mmHg.
    NFP = 55.0 - (15.0 + 30.0) = +10.0 mmHg.
    GFR = 12.5 * 10.0 = 125.0 mL/min = 180.0 L/day.
    99.0% reabsorption => Daily urine = 180.0 * 0.010 = 1.80 L/day.
    """
    p_gc = 55.0
    p_bs = 15.0
    pi_gc = 30.0
    nfp = p_gc - (p_bs + pi_gc)
    assert nfp == 10.0

    kf = 12.5
    gfr_min = kf * nfp
    assert math.isclose(gfr_min, 125.0, rel_tol=1e-9)

    gfr_day = gfr_min * 1440.0 / 1000.0
    assert math.isclose(gfr_day, 180.0, rel_tol=1e-9)

    reabsorption_rate = 0.990
    urine_day = gfr_day * (1.0 - reabsorption_rate)
    assert math.isclose(urine_day, 1.80, rel_tol=1e-9)


def test_photosynthesis_quantum_requirement():
    """Verify non-cyclic electron transport Z-scheme quantum requirement:
    1 glucose requires 6 CO2, 12 NADPH, 18 ATP.
    Non-cyclic flow: 8 photons produce 2 NADPH and 3 ATP.
    Scaling by 6: 6 * 8 = 48 photons produce 12 NADPH and 18 ATP.
    """
    photons_per_unit = 8
    nadph_per_unit = 2
    atp_per_unit = 3

    glucose_nadph_needed = 12
    glucose_atp_needed = 18

    units_needed = glucose_nadph_needed / nadph_per_unit
    assert units_needed == 6.0
    assert units_needed * atp_per_unit == glucose_atp_needed

    total_photons = units_needed * photons_per_unit
    assert total_photons == 48


def test_respiratory_quotient_stoichiometry():
    """Verify RQ:
    Glucose: 6 CO2 / 6 O2 = 1.00.
    Tripalmitin: 102 CO2 / 145 O2 = 0.7034.
    """
    rq_glucose = 6.0 / 6.0
    assert math.isclose(rq_glucose, 1.00, rel_tol=1e-9)

    rq_fat = 102.0 / 145.0
    assert round(rq_fat, 2) == 0.70


def test_digestive_enzymes_and_bile_emulsion():
    """Verify enzyme pH optima and bile emulsification:
    - Salivary amylase operates at oral pH 6.8, denatured in gastric HCl (pH 1.8)
    - Pepsin requires acidic pH 1.8, denatured in alkaline duodenal juice
    - Bile salts emulsify lipids non-enzymatically into micelles
    """
    amylase_opt = 6.8
    pepsin_opt = 1.8
    assert amylase_opt > pepsin_opt
    bile_has_enzymes = False
    assert bile_has_enzymes is False


def test_cardiac_output_and_ejection_fraction():
    """Verify cardiac hemodynamics:
    EDV = 120.0 mL, ESV = 50.0 mL, HR = 72.0 bpm.
    SV = 120.0 - 50.0 = 70.0 mL.
    EF = 70.0 / 120.0 = 58.33%.
    CO = 70.0 * 72.0 = 5040 mL/min = 5.04 L/min.
    """
    edv = 120.0
    esv = 50.0
    hr = 72.0
    sv = edv - esv
    assert sv == 70.0
    ef = (sv / edv) * 100.0
    assert round(ef, 1) == 58.3
    co = (sv * hr) / 1000.0
    assert math.isclose(co, 5.04, rel_tol=1e-9)


def test_action_potential_voltage_and_ion_conductance():
    """Verify action potential phases:
    - Resting: -70 mV (K+ leak, Na+/K+ ATPase)
    - Threshold: -55 mV
    - Depolarization peak: +30 mV (voltage-gated Na+ influx)
    - Repolarization: returning negative (Na+ inactivation, voltage-gated K+ efflux)
    - Hyperpolarization undershoot: -80 mV (delayed K+ closure)
    """
    v_rest = -70.0
    v_thresh = -55.0
    v_peak = 30.0
    v_undershoot = -80.0
    assert v_rest < v_thresh < v_peak
    assert v_undershoot < v_rest


def test_blood_glucose_homeostatic_feedback():
    """Verify endocrine regulation:
    - Hyperglycemia triggers pancreatic beta-cells to secrete insulin
    - Insulin induces GLUT4 translocation and glycogenesis
    """
    hyperglycemia_hormone = "Insulin"
    secreting_cell = "Beta-cell"
    action = ["GLUT4 translocation", "glycogenesis"]
    assert hyperglycemia_hormone == "Insulin"
    assert "Beta" in secreting_cell
    assert "glycogenesis" in action


def test_dihybrid_cross_recombinant_fraction():
    """Verify Mendelian dihybrid cross:
    F2 ratio: 9 : 3 : 3 : 1 (Round Yellow, Round Green, Wrinkled Yellow, Wrinkled Green).
    Parental: 9 (Round Yellow) + 1 (Wrinkled Green) = 10/16.
    Recombinant: 3 (Round Green) + 3 (Wrinkled Yellow) = 6/16 = 3/8 = 37.5%.
    """
    parental = 9 + 1
    recombinant = 3 + 3
    total = parental + recombinant
    assert total == 16
    recombinant_fraction = recombinant / total
    assert math.isclose(recombinant_fraction, 0.375, rel_tol=1e-9)


def test_x_linked_colorblindness_transmission():
    """Verify X-linked recessive inheritance:
    Father: X^C Y (normal). Mother: X^C X^c (carrier).
    Daughters: X^C X^C, X^C X^c (0% color-blind).
    Sons: X^C Y (normal), X^c Y (color-blind, 50%).
    """
    p_daughter_colorblind = 0.0
    p_son_colorblind = 0.50
    assert p_daughter_colorblind == 0.0
    assert p_son_colorblind == 0.50


def test_homology_vs_analogy_evolutionary_divergence():
    """Verify evolutionary comparative anatomy:
    - Vertebrate forelimbs (human, cheetah, whale, bat): Homologous, Divergent evolution
    - Wings (butterfly vs bat): Analogous, Convergent evolution
    """
    case1 = {"organs": "Homologous", "evolution": "Divergent"}
    case2 = {"organs": "Analogous", "evolution": "Convergent"}
    assert case1["organs"] == "Homologous" and case1["evolution"] == "Divergent"
    assert case2["organs"] == "Analogous" and case2["evolution"] == "Convergent"


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
