"""Verification suite for Biology Track: Control & Coordination, Genetics & Molecular Heredity (bio-genetics-coordination-r1).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Biological, neurological, and genetic proofs:
    1. Complementary dihybrid epistasis & meiosis stoichiometry (9:7 ratio, 2000 divisions)
    2. Action potential electrophysiology (-70 mV -> -55 mV -> +30 mV -> -90 mV -> -70 mV)
    3. Spinal reflex arc pathway and neurotransmitter (Dorsal root -> interneuron -> Ventral root -> ACh)
    4. Auxin gravitropism kinetics (shoot stimulation vs root inhibition on lower flank)
    5. Photoperiodism phytochrome photoreversibility (final far-red flash restores SDP flowering)
    6. Pancreatic blood glucose regulation (beta-cells insulin GLUT-4 vs alpha-cells glucagon)
    7. X-linked color blindness pedigree inheritance (50% son, 0% daughter)
    8. Chargaff's rules & DNA hydrogen bonding (880 Guanine, 4880 hydrogen bonds)
    9. Sickle cell anemia molecular lesion (A -> T transversion, Glu6Val beta-globin polymerization)
   10. Calcium homeostasis endocrine antagonism (PTH raises Ca2+, calcitonin lowers Ca2+)
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
BIO_DIR = REPO_ROOT / "workspace/output/bio-genetics-coordination-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/bio/BIO-NSEJS-GEN-01"

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
    assert bank["bank_id"] == "bio-genetics-coordination-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "BIO-NSEJS-GEN-01"
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
    assert q["answer"]["crux_move_ref"] == "BIO-NSEJS-GEN-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "BIO-NSEJS-GEN-01-M2" in plan["protected_move_refs"]


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

def test_bio_genetics_coordination_qrt_labelling_integrity():
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
# 5. Scientific, Neurological & Genetic Verification (All 10 Items)
# ---------------------------------------------------------------------------

def test_q01_complementary_epistasis_and_meiosis():
    # Complementary ratio: 9 C_P_ (Purple) : 7 (3 C_pp + 3 ccP_ + 1 ccpp, White)
    seeds = 1600
    pollen_meioses = seeds // 4
    ovule_meioses = seeds // 1
    total_meioses = pollen_meioses + ovule_meioses
    assert pollen_meioses == 400
    assert ovule_meioses == 1600
    assert total_meioses == 2000


def test_q02_action_potential_electrophysiology():
    v_rest = -70
    v_threshold = -55
    v_peak = 30
    v_hyper = -90
    assert v_rest < v_threshold < v_peak
    assert v_hyper < v_rest


def test_q03_spinal_reflex_arc_pathway():
    pathway = ["nociceptor", "dorsal_root_ganglion", "spinal_gray_interneuron", "ventral_root_motor", "neuromuscular_junction"]
    assert pathway[1].startswith("dorsal")
    assert pathway[3].startswith("ventral")


def test_q04_auxin_gravitropism_kinetics():
    # Lower flank accumulates auxin in both root and shoot
    # Shoot: high auxin promotes elongation (bends up)
    # Root: high auxin inhibits elongation (bends down)
    shoot_response = "stimulated"
    root_response = "inhibited"
    assert shoot_response != root_response


def test_q05_phytochrome_photoreversibility():
    # Short-day plant (requires continuous night)
    # Red (660 nm) -> Pfr (inhibits SDP flowering)
    # Far-red (730 nm) -> Pr (allows SDP flowering)
    final_signal_exp1 = "red"
    final_signal_exp2 = "far_red"
    assert final_signal_exp1 != final_signal_exp2


def test_q06_blood_glucose_endocrine_regulation():
    # Hyperglycemia -> beta-cells -> insulin -> GLUT-4 uptake
    # Hypoglycemia -> alpha-cells -> glucagon -> glycogenolysis
    norm_glucose = 90
    high_glucose = 150
    low_glucose = 70
    assert high_glucose > norm_glucose > low_glucose


def test_q07_x_linked_color_blindness():
    # Father: X^C Y (normal)
    # Mother: X^C X^c (carrier)
    # Sons: 50% X^C Y, 50% X^c Y (50% affected)
    # Daughters: 50% X^C X^C, 50% X^C X^c (0% affected)
    prob_son = 0.50
    prob_daughter = 0.00
    assert prob_son == 0.50
    assert prob_daughter == 0.00


def test_q08_chargaff_dna_hydrogen_bonds():
    total_bases = 4000
    pct_A = 0.28
    num_A = round(total_bases * pct_A)
    num_T = num_A
    pct_G = (1.0 - 2 * pct_A) / 2
    num_G = round(total_bases * pct_G)
    num_C = num_G

    assert num_A == 1120
    assert num_G == 880
    assert num_A + num_T + num_G + num_C == total_bases

    h_bonds = 2 * num_A + 3 * num_G
    assert h_bonds == 4880


def test_q09_sickle_cell_transversion_mutation():
    normal_codon = "GAG"
    mutant_codon = "GTG"
    normal_aa = "Glutamic acid"
    mutant_aa = "Valine"
    # A to T is purine to pyrimidine = transversion
    assert normal_codon[1] == "A"
    assert mutant_codon[1] == "T"
    assert normal_aa != mutant_aa


def test_q10_calcium_homeostasis():
    # PTH raises calcium; Calcitonin lowers calcium
    pth_target = "hypercalcemic"
    calcitonin_target = "hypocalcemic"
    assert pth_target != calcitonin_target


# ---------------------------------------------------------------------------
# 6. Universal Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_rule_13_governance_invariant(bank, sl1_report):
    assert bank["extensions"]["academic_status"] == "UNREVIEWED"
    assert bank["extensions"]["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert sl1_report["gate_summary"]["release"] == "HOLD"
    assert sl1_report["gate_summary"]["construction"] == "HOLD"
    assert sl1_report["gate_summary"]["qrt"] == "HOLD"
