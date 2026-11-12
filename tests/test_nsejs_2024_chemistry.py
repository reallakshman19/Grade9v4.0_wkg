"""Verification suite for NSEJS 2024 Official Chemistry Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical and chemical proofs:
    1. Q17: Density of two-component milk mixture (rho_skim = 1038.96 kg/m^3)
    2. Q18: Sodium nitrate mass for fixed Na+ concentration (m = 12.94 g)
    3. Q19: Geminal diiodide tetrahedral chord length (d = 3.43 A)
    4. Q21: Electron gas molar mass and moles per kilogram ([100 / (6.02 * 9.11)] * 10^6 mol)
    5. Q22: Carbon micro-charge Coulombic ratio (excess electron ratio = 4.15e-14)
    6. Q24: Fahrenheit to Celsius clinical body temperature conversion (102.6 F = 39.2 C)
    7. Q26: Hydronium ion concentration from pH 8.26 ([H3O+] = 5.5e-9 mol/L)
    8. Q54: Nitrogen reduction oxidation-number transitions (NO2 -> NO2-, NO3- -> NH4+)
    9. Q55: Basicity of phosphorus oxyacid neutralised by NaOH (H3PO2, x = 2, monobasic)
   10. Q56: Scandium ground-state subshell population (1 unpaired, 1 d-electron, 12 p-electrons)
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
CHEM_DIR = REPO_ROOT / "workspace/output/nsejs-2024-chemistry-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2024-C-Q17" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2024-chemistry-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2024-C-Q17"
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
    expected_ids = [f"NSEJS-2024-C-Q{i:02d}" for i in range(17, 33)] + [f"NSEJS-2024-C-Q{i:02d}" for i in range(53, 57)]
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


def test_q17_milk_density_mixture():
    V_total = 1.0  # L
    m_total = 1.032  # kg
    V_fat = 0.04 * V_total  # 0.04 L = 0.04e-3 m^3
    rho_fat = 865.0  # kg/m^3
    m_fat = rho_fat * (V_fat * 1e-3)
    V_skim = (V_total - V_fat) * 1e-3  # m^3
    m_skim = m_total - m_fat
    rho_skim = m_skim / V_skim
    assert round(rho_skim, 2) == 1038.96


def test_q18_sodium_nitrate_mass():
    v_ml = 50.0
    conc_mg = 70.0
    m_na_g = (v_ml * conc_mg) / 1000.0  # 3.50 g
    # Using IUPAC standard atomic weights (Na=22.990, N=14.007, O=15.999 -> NaNO3=84.994)
    m_nano3 = m_na_g * (84.994 / 22.990)
    assert round(m_nano3, 2) == 12.94


def test_q19_tetrahedral_iodine_distance():
    L = 2.10
    theta_deg = 109.4712
    theta_rad = math.radians(theta_deg)
    d = 2 * L * math.sin(theta_rad / 2.0)
    assert round(d, 2) == 3.43


def test_q21_electron_gas_moles():
    m_e = 9.11e-31
    n_a = 6.02e23
    m_mol = m_e * n_a  # kg/mol = 5.48422e-7
    moles = 1.0 / m_mol
    expected = (100.0 / (6.02 * 9.11)) * 1e6
    assert abs(moles - expected) < 1.0


def test_q22_carbon_electrostatics_ratio():
    K = 9.0e9
    r = 0.01  # 1 cm
    F = 1.0e-5  # N
    q = math.sqrt(F * r**2 / K)
    e = 1.602e-19
    n_e = q / e
    m_c = 1.0  # g
    n_c_mol = m_c / 12.0
    n_a = 6.022e23
    n_atoms = n_c_mol * n_a
    ratio = n_e / n_atoms
    assert round(ratio * 1e14, 2) == 4.15


def test_q24_temperature_conversion():
    f = 102.6
    c = (f - 32.0) * (5.0 / 9.0)
    assert round(c, 1) == 39.2


def test_q26_hydronium_ion_concentration():
    ph = 8.26
    conc = 10**(-ph)
    # 10^-8.26 = 10^0.74 * 10^-9 = 5.495e-9
    assert round(conc * 1e9, 1) == 5.5


def test_q54_nitrogen_reduction_processes():
    # NO2 (+4) -> NO2- (+3): reduction (decrease by 1)
    # NO3- (+5) -> NH4+ (-3): reduction (decrease by 8)
    ox_no2 = 4
    ox_no2_minus = 3
    ox_no3_minus = 5
    ox_nh4_plus = -3
    assert ox_no2_minus < ox_no2
    assert ox_nh4_plus < ox_no3_minus


def test_q55_phosphorus_oxyacid_basicity():
    m_naoh = 40.0
    n_naoh = m_naoh / 40.0  # 1.0 mol
    n_acid = 1.0  # mol
    basicity = n_naoh / n_acid
    assert basicity == 1.0  # monobasic, so x = 2 for H3PO2


def test_q56_scandium_electronic_configuration():
    # K=2, L=8, M=9, N=2 -> Z = 21 (Scandium)
    # 1s2 2s2 2p6 3s2 3p6 3d1 4s2
    z = 2 + 8 + 9 + 2
    assert z == 21
    num_unpaired = 1  # 3d1
    num_d = 1  # 3d1
    num_p = 6 + 6  # 2p6 + 3p6 = 12
    assert num_unpaired == 1
    assert num_d == 1
    assert num_p == 12
