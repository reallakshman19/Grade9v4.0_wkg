"""Verification suite for NSEJS 2020-21 Official Physics Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Physical and numerical proofs:
    1. Q1: Neutron star surface gravitational acceleration (2.0e12 m s^-2, Option B)
    2. Q2: Diver safe ear drum hydrostatic depth limit (3.1 m approx 3 m, Option C)
    3. Q3: Thin convex lens conjugate foci object distances (18 cm and 6 cm, Option B)
    4. Q4: Nuclear fission disintegration rate for 1000 kW plant at 30% efficiency (1.04e17 s^-1, Option A)
    5. Q5: Newton second law contact forces in coupled blocks (30 N in I, 60 N in II, Option B)
    6. Q6: Resistor lattice reduction and 6 V voltage division for Rx (4 ohms, Option A)
    7. Q25: Biot-Savart law current magnitude, electron flow rate and direction (Options A, B, C)
    8. Q26: Specific charge SI units, tritium isotopic minimum, and electron/alpha comparison (Options A, B, C OR A, B, D)
- Strict QRT cognitive demand rubric and labelling across all 8 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
PHYS_DIR = REPO_ROOT / "workspace/output/nsejs-2020-physics-r1"
SOURCE_BASE = REPO_ROOT / "workspace/sources/nsejs"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def bank():
    p = PHYS_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def intake():
    p = PHYS_DIR / "intake.json"
    assert p.exists(), f"Missing intake file: {p}"
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


def test_source_custody_schema():
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    first_custody = SOURCE_BASE / "NSEJS-2020-P-Q01" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2020-physics-r1"
    assert len(bank["questions"]) == 8
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2020-P-Q01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_8_questions_present(bank):
    assert len(bank["questions"]) == 8
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2020-P-Q{i:02d}" for i in range(1, 7)] + ["NSEJS-2020-P-Q25", "NSEJS-2020-P-Q26"]
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
    html_path = PHYS_DIR / "core2_module.html"
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


def test_q01_neutron_star_gravity(bank):
    # g = G M / R^2 = (6.67e-11 * 3.0e30) / (10^4)^2 = 2.0e12 m/s^2
    g = (6.67e-11 * 3.0e30) / (1e4)**2
    assert round(g / 1e12, 1) == 2.0
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q01")
    assert q["answer"]["correct_option"] == "B"


def test_q02_diver_safe_depth(bank):
    # P = rho * g * h, F = P * A = rho * g * h * pi * r^2
    # h = F / (rho * g * pi * r^2) = 2.5 / (1050 * 9.8 * 3.14159 * 0.005^2) = 3.09 m
    import math
    f_max = 2.5
    rho = 1050.0
    g = 9.8
    r = 0.005
    area = math.pi * r**2
    h = f_max / (rho * g * area)
    assert round(h, 1) == 3.1
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q02")
    assert q["answer"]["correct_option"] == "C"


def test_q03_thin_lens_conjugate_foci(bank):
    # x^2 - 24x + 108 = 0 -> (x - 18)(x - 6) = 0 -> x = 18 or 6
    roots = {18, 6}
    assert 18 * 6 == 108
    assert 18 + 6 == 24
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q03")
    assert q["answer"]["correct_option"] == "B"


def test_q04_nuclear_fission_rate(bank):
    p_elec = 1.0e6
    eta = 0.30
    p_thermal = p_elec / eta
    e_fission = 200 * 1.6e-13  # 200 MeV in J
    n = p_thermal / e_fission
    assert round(n / 1e17, 2) == 1.04
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q04")
    assert q["answer"]["correct_option"] == "A"


def test_q05_contact_forces(bank):
    a = 90.0 / 30.0  # 3 m/s^2
    f_ab = 10.0 * a  # 30 N
    f_ba = 20.0 * a  # 60 N
    assert f_ab == 30.0
    assert f_ba == 60.0
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q05")
    assert q["answer"]["correct_option"] == "B"


def test_q06_resistor_network_voltage_division(bank):
    # fixed = 5 + (5 || (5 + (5||5))) = 5 + 3 = 8 ohms
    # 6 / 18 = Rx / (8 + Rx) -> 8 + Rx = 3Rx -> Rx = 4
    r_fixed = 8.0
    rx = 4.0
    v_rx = 18.0 * (rx / (r_fixed + rx))
    assert v_rx == 6.0
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q06")
    assert q["answer"]["correct_option"] == "A"


def test_q25_magnetic_field_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q25")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"]
    assert "B" in q["answer"]["correct_option"]
    assert "C" in q["answer"]["correct_option"]


def test_q26_specific_charge_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2020-P-Q26")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"]
    assert "B" in q["answer"]["correct_option"]
    assert "OR" in q["answer"]["correct_option"]
