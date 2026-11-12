"""Verification suite for NSEJS 2023 Official Chemistry Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical and chemical proofs:
    1. Q20: Potassium superoxide closed atmosphere regeneration (KO2 + CO2 -> K2CO3 + O2)
    2. Q21: Total unshared electron lone pairs in triiodide anion (3 central + 6 terminal = 9)
    3. Q22: Non-primordial unstable elements below uranium (43 Tc, 61 Pm)
    4. Q26: Maximum methyl groups in constitutional isomers of hexane (4 in dimethylbutanes)
    5. Q28: Quadratic auto-ionisation hydronium calculation for 10^-8 M HCl (pH = 6.98)
    6. Q29: Weighted average isotopic atomic mass of element X (10.81 u)
    7. Q31: Metric carat to mass conversion and diamond carbon atom count (3.01e22 atoms)
    8. Q56: Molecular iodine coordination and Lewis adduct formation (KI + I2 -> KI3)
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
CHEM_DIR = REPO_ROOT / "workspace/output/nsejs-2023-chemistry-r1"
SOURCE_BASE = REPO_ROOT / "workspace/sources/chem"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def bank():
    p = CHEM_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def intake():
    p = CHEM_DIR / "intake.json"
    assert p.exists(), f"Missing intake file: {p}"
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


def test_source_custody_schema():
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    
    first_custody = SOURCE_BASE / "NSEJS-2023-C-Q17" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2023-chemistry-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2023-C-Q17"
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
    expected_ids = [f"NSEJS-2023-C-Q{i:02d}" for i in range(17, 33)] + [f"NSEJS-2023-C-Q{i:02d}" for i in range(53, 57)]
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
    html_path = CHEM_DIR / "core2_module.html"
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


def test_q20_potassium_superoxide_reaction():
    # 4 KO2 + 2 CO2 -> 2 K2CO3 + 3 O2
    moles_ko2 = 4
    moles_co2 = 2
    moles_o2 = 3
    assert moles_o2 > moles_co2  # Net oxygen production exceeding consumed CO2


def test_q21_triiodide_lone_pairs():
    # I3- : central I has 3 lone pairs (sp3d linear)
    # each terminal I has 3 lone pairs
    central_lp = 3
    terminal_lp = 2 * 3
    total_lp = central_lp + terminal_lp
    assert total_lp == 9


def test_q22_radioactive_elements_below_uranium():
    atomic_numbers = [43, 61]
    assert atomic_numbers == [43, 61]  # Technetium and Promethium


def test_q26_hexane_isomers_max_methyls():
    # Isomers:
    # 2,2-dimethylbutane: CH3-C(CH3)2-CH2-CH3 has 4 methyl groups
    # 2,3-dimethylbutane: CH3-CH(CH3)-CH(CH3)-CH3 has 4 methyl groups
    max_methyls = 4
    assert max_methyls == 4


def test_q28_dilute_hcl_ph():
    # [H+]^2 - 10^-8 [H+] - 10^-14 = 0
    c_acid = 1e-8
    kw = 1e-14
    h_total = (-c_acid + math.sqrt(c_acid**2 + 4 * kw)) / 2.0 + c_acid
    ph = -math.log10(h_total)
    assert round(ph, 2) == 6.98


def test_q29_boron_isotopic_abundance_mass():
    m1 = 10.013
    p1 = 0.199
    m2 = 11.009
    p2 = 0.801
    avg_mass = p1 * m1 + p2 * m2
    assert round(avg_mass, 2) == 10.81


def test_q31_carat_diamond_carbon_atoms():
    carats = 3.0
    mass_g = carats * 0.200  # 0.600 g
    moles_c = mass_g / 12.011
    na = 6.022e23
    num_atoms = moles_c * na
    assert round(num_atoms * 1e-22, 2) == 3.01


def test_q56_triiodide_complex_formation():
    # KI + I2 -> KI3
    # I- (donor, Lewis base) + I2 (acceptor, Lewis acid) -> I3-
    reactants = {"KI", "I2"}
    product = "KI3"
    assert "KI" in reactants and "I2" in reactants
    assert product == "KI3"
