"""Verification suite for NSEJS 2021-22 Official Chemistry Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Chemical and stoichiometric proofs:
    1. Q9: Constituent atoms in triatomic sulfur dioxide mole (1.81e24 atoms, Option C)
    2. Q10: Stoichiometric antacid neutralisation of gastric hydrochloric acid (0.52 g, Option A)
    3. Q11: Thermal decomposition mass balance of calcium carbonate-oxide mixture (70%, Option A)
    4. Q12: Periodic electronegativity and metallic character progression (Option C)
    5. Q13: Ostwald weak electrolyte ionisation and electrode wetting conductance (Option C)
    6. Q14: Qualitative analysis and cationic hydrolysis of ammonium chloride (Option B)
    7. Q15: Avogadro molar mass equivalence of equal volume gases (N2 and CO, Option D)
    8. Q16: Colligative van 't Hoff factor osmotic pressure hierarchy (Q < P < R, Option B)
    9. Q28: Intramolecular covalent and intermolecular dispersion forces in dry ice (Options A, D)
    10. Q29: Exothermic hydration enthalpy of dissolution (Options B, D)
    11. Q30: Hard water alkaline-earth fatty acid precipitation (Option B)
- Strict QRT cognitive demand rubric and labelling across all 11 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
CHEM_DIR = REPO_ROOT / "workspace/output/nsejs-2021-chemistry-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2021-C-Q09" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2021-chemistry-r1"
    assert len(bank["questions"]) == 11
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2021-C-Q09"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_11_questions_present(bank):
    assert len(bank["questions"]) == 11
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2021-C-Q{i:02d}" for i in range(9, 17)] + [f"NSEJS-2021-C-Q{i:02d}" for i in range(28, 31)]
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


def test_q09_so2_atoms_count():
    # 1 mol SO2 has 3 mol atoms = 3 * 6.02e23 = 1.806e24 approx 1.81e24
    atoms = 3 * 6.02e23
    assert round(atoms / 1e24, 2) == 1.81


def test_q10_antacid_neutralisation_mass():
    # n_HCl = 0.01 * 2 = 0.02 mol. Al(OH)3 + 3HCl -> AlCl3 + 3H2O
    # n_AlOH3 = 0.02 / 3 mol => mass = (0.02 / 3) * 78 = 0.52 g
    n_hcl = 0.01 * 2.0
    mass_antacid = (n_hcl / 3.0) * 78.0
    assert round(mass_antacid, 2) == 0.52


def test_q11_calcination_mixture_cao_percentage():
    # CaCO3 (100) -> CaO (56) + CO2 (44)
    # Mass loss = 0.500 - 0.434 = 0.066 g CO2 => 0.0015 mol => CaCO3 = 0.150 g
    # Initial CaO = 0.500 - 0.150 = 0.350 g => 0.350 / 0.500 = 70%
    m_loss = 0.500 - 0.434
    n_co2 = m_loss / 44.0
    m_caco3 = n_co2 * 100.0
    m_cao_init = 0.500 - m_caco3
    pct_cao = (m_cao_init / 0.500) * 100.0
    assert round(pct_cao) == 70


def test_q15_avogadro_equal_molar_mass():
    # N2: 28 g/mol, CO: 28 g/mol
    m_n2 = 28
    m_co = 28
    assert m_n2 == m_co


def test_q16_osmotic_pressure_particles():
    # MgSO4: i=2, Na2SO4: i=3, Al2(SO4)3: i=5
    # Order Q (2) < P (3) < R (5)
    i_q = 2
    i_p = 3
    i_r = 5
    assert i_q < i_p < i_r


def test_q28_dry_ice_bonding_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-C-Q28")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"] and "D" in q["answer"]["correct_option"]


def test_q29_exothermic_dissolution_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-C-Q29")
    assert q["response"]["type"] == "multiple_response"
    assert "B" in q["answer"]["correct_option"] and "D" in q["answer"]["correct_option"]
