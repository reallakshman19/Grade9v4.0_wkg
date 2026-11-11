"""Verification suite for NSEJS 2024 Physics Electrostatics (Question 06) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical physics proofs (Coulomb inversion, carrier quantization, Avogadro stoichiometry)
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
from pathlib import Path
import re
import pytest
from jsonschema import Draft202012Validator

from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
NSEJS_DIR = REPO_ROOT / "workspace/output/nsejs-electrostatics-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-2024-P-Q06"

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
    p = NSEJS_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = NSEJS_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = NSEJS_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def module_html():
    p = NSEJS_DIR / "core2_module.html"
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
    assert bank["bank_id"] == "nsejs-2024-electrostatics-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2024-P-Q06"
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


def test_sl2_native_report_qrt_proposal(sl2_report):
    summary = inspect_native_report(sl2_report)
    assert summary["native_check_status"] == "HOLD"
    assert summary["integration_status"] == "HOLD"
    assert sl2_report["selected_gate"] == "qrt"
    assert sl2_report["selected_gate_status"] == "HOLD"


# ---------------------------------------------------------------------------
# 3. The 7 Critical Anti-Patterns Audit
# ---------------------------------------------------------------------------

def test_anti_pattern_1_no_ghost_text(bank):
    q = bank["questions"][0]
    reasoning_text = " ".join(q["answer"]["reasoning"])
    assert "2. Connection:" not in reasoning_text
    assert "Connection:" not in reasoning_text
    assert "1. System Representation & Setup:" in q["answer"]["reasoning"][0]
    assert "2. Physical Model & Formulation:" in q["answer"]["reasoning"][1]
    assert "3. Execution & Resolution:" in q["answer"]["reasoning"][2]


def test_anti_pattern_2_dynamic_crux_move(bank):
    q = bank["questions"][0]
    # Primary operation is SYNTHESIZE -> crux move ref must be M2
    assert q["answer"]["crux_move_ref"] == "NSEJS-2024-P-Q06-M2"
    assert "NSEJS-2024-P-Q06-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]


def test_anti_pattern_3_rubric_sum_bounds(bank):
    q = bank["questions"][0]
    diff = q["extensions"]["grade9v3:analysis"]["difficulty"]
    comps = diff["components"]
    for k, v in comps.items():
        assert 0 <= v <= 2, f"Component {k} out of bounds: {v}"
    total = sum(comps.values())
    assert total == diff["score"], f"Sum {total} != score {diff['score']}"
    assert diff["score"] == 4
    assert diff["band"] == "D2"


def test_anti_pattern_4_canonical_verbs_only(bank):
    q = bank["questions"][0]
    orig_id = q["original_identifier"]
    match = re.search(r"·\s*([A-Z]+)\s*·", orig_id)
    assert match, "Could not extract primary operation from original_identifier"
    primary_op = match.group(1)
    assert primary_op in CANONICAL_OPERATIONS, f"Illegal operation: {primary_op}"
    assert primary_op == "SYNTHESIZE"

    for move in q["answer"]["reasoning_route"]:
        assert move["kind"] in CANONICAL_OPERATIONS, f"Illegal move operation: {move['kind']}"


def test_anti_pattern_5_svg_root_dimensions_and_typography(module_html):
    assert "<svg" in module_html, "Missing SVG in core2_module.html"
    viewbox_match = re.search(r'viewBox="([^"]+)"', module_html)
    assert viewbox_match, "SVG must have viewBox"
    parts = [float(p) for p in viewbox_match.group(1).split()]
    assert len(parts) == 4
    w, h = parts[2], parts[3]
    assert w >= 400 and h >= 180, f"SVG viewBox {w}x{h} too small"

    # W3C Typography check: font-size >= 14px on mobile
    font_sizes = re.findall(r'font-size="(\d+(?:\.\d+)?)"', module_html)
    assert font_sizes, "No font-size attributes found in SVG"
    for fs in font_sizes:
        val = float(fs)
        assert val >= 14.0, f"Font size {val}px violates W3C minimum 14px accessibility requirement"


def test_anti_pattern_7_inert_derivations_until_commitment(module_html):
    # Derivation section must have display: none; initially
    assert 'class="derivation-section"' in module_html
    assert "display: none;" in module_html
    # Must contain commit button
    assert 'id="commitBtn"' in module_html


# ---------------------------------------------------------------------------
# 4. Mathematical Physics Verification
# ---------------------------------------------------------------------------

def test_physics_coulomb_charge_inversion():
    """Verify charge inversion: F = K * q^2 / r^2 ==> q = r * sqrt(F / K)."""
    import math
    F = 1.0e-5  # N
    r = 0.01    # m (1 cm)
    K = 9.0e9   # N m^2 / C^2

    q = r * math.sqrt(F / K)
    expected_q = (1.0 / 3.0) * 1.0e-9  # C
    assert math.isclose(q, expected_q, rel_tol=1e-6)
    assert math.isclose(q, 3.333333e-10, rel_tol=1e-5)


def test_physics_electron_carrier_quantization():
    """Verify carrier quantization: n_e = q / e."""
    import math
    q = (1.0 / 3.0) * 1.0e-9
    e = 1.6e-19
    n_e = q / e
    expected_ne = 1e10 / 4.8
    assert math.isclose(n_e, expected_ne, rel_tol=1e-6)
    assert math.isclose(n_e, 2.083333e9, rel_tol=1e-5)


def test_physics_stoichiometry_and_carrier_ratio():
    """Verify stoichiometric calculation and final ratio R = n_e / n_atoms."""
    import math
    m = 1.0       # g
    M = 12.0      # g/mol
    N_A = 6.022e23 # mol^-1

    n_atoms = (m / M) * N_A
    assert math.isclose(n_atoms, 5.018333e22, rel_tol=1e-5)

    n_e = ( (1.0 / 3.0) * 1.0e-9 ) / 1.6e-19
    ratio = n_e / n_atoms

    # Option (A): 4.15 * 10^-14
    expected_ratio = 4.15143e-14
    assert math.isclose(ratio, expected_ratio, rel_tol=1e-4)
    assert f"{ratio:.2e}" == "4.15e-14"


# ---------------------------------------------------------------------------
# 5. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html


# ---------------------------------------------------------------------------
# 6. Question Status Preview Page Validation
# ---------------------------------------------------------------------------

def test_preview_question_status_page_electrostatics():
    path = REPO_ROOT / "preview/question-status.html"
    assert path.exists(), "Missing preview/question-status.html"
    html = path.read_text(encoding="utf-8")

    # Match JSON script data
    m = re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>', html, re.DOTALL)
    assert m, "Missing #wpe-data script tag in preview/question-status.html"
    data = json.loads(m.group(1))

    questions = data["questions"]
    assert len(questions) == 20, f"Expected 20 unified questions, found {len(questions)}"

    elec_questions = [q for q in questions if "ELEC" in q.get("source_id", "")]
    assert len(elec_questions) == 10, f"Expected 10 electrostatics questions, found {len(elec_questions)}"

    # Check each electrostatics question's structure
    for q in elec_questions:
        assert "id" in q and q["id"].startswith("NSEJS-")
        assert "source_id" in q
        assert "stem" in q and len(q["stem"]) > 10
        assert "options" in q and len(q["options"]) == 4
        assert "op" in q and q["op"] in CANONICAL_OPERATIONS
        assert "band" in q and q["band"] in {"D1", "D2", "D3", "D4"}
        assert q["review_state"] == "NOT_ADMITTED"
        assert "hints" in q and len(q["hints"]) == 3
        assert "steps" in q and len(q["steps"]) == 3
        assert "check" in q and len(q["check"]) > 5

    # Check UI & Governance elements
    assert "HOLD · NO ACADEMIC APPROVAL INFERRED FROM SOFTWARE VALIDATION" in html
    assert 'id="topic"' in html
    assert 'class="status"' in html
    assert 'class="layout"' in html
    assert 'class="filters"' in html
    assert 'class="stage"' in html
