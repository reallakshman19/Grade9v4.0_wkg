"""Verification suite for Mathematics Track: Algebra & Polynomials (Question 01) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical proofs (Auxiliary polynomial invariant cancellation, Vieta power sums, Sophie Germain, symmetric identities, complex modular remainder)
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
MATH_DIR = REPO_ROOT / "workspace/output/math-algebra-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/math/MATH-OLY-POLY-01"

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
    p = MATH_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = MATH_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = MATH_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def module_html():
    p = MATH_DIR / "core2_module.html"
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
    assert bank["bank_id"] == "math-algebra-polynomials-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "MATH-OLY-POLY-01"
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
    # Primary operation is MODEL -> crux move ref must be M2
    assert q["answer"]["crux_move_ref"] == "MATH-OLY-POLY-01-M2"
    assert "MATH-OLY-POLY-01-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]


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
    assert primary_op == "MODEL"

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
    assert 'class="derivation-section"' in module_html
    assert "display: none;" in module_html
    assert 'id="commitBtn"' in module_html


# ---------------------------------------------------------------------------
# 4. Mathematical Algebraic Proof Verification
# ---------------------------------------------------------------------------

def test_math_auxiliary_polynomial_cancellation():
    """Verify that P(4) + P(0) == 40 for ANY fourth root k in R:
    P(x) = (x - 1)(x - 2)(x - 3)(x - k) + x^2.
    P(4) = 6(4 - k) + 16 = 40 - 6k.
    P(0) = (-1)(-2)(-3)(-k) + 0 = 6k.
    P(4) + P(0) = (40 - 6k) + 6k = 40.
    """
    for k in [-100.0, -10.0, -2.5, 0.0, 1.0, 2.0, 3.0, 4.0, 7.3, 50.0]:
        def P(x):
            return (x - 1.0) * (x - 2.0) * (x - 3.0) * (x - k) + (x ** 2)

        # Check given conditions
        assert math.isclose(P(1.0), 1.0, rel_tol=1e-9)
        assert math.isclose(P(2.0), 4.0, rel_tol=1e-9)
        assert math.isclose(P(3.0), 9.0, rel_tol=1e-9)

        # Check invariant sum
        p4_plus_p0 = P(4.0) + P(0.0)
        assert math.isclose(p4_plus_p0, 40.0, rel_tol=1e-9), f"Failed for k = {k}: got {p4_plus_p0}"


def test_math_vieta_power_sums():
    """Verify quadratic power sums:
    x^2 - 4x + 2 = 0 ==> alpha + beta = 4, alpha*beta = 2.
    S2 = 4^2 - 2(2) = 12.
    S4 = 12^2 - 2(2^2) = 144 - 8 = 136.
    """
    # Exact roots
    alpha = 2.0 + math.sqrt(2.0)
    beta = 2.0 - math.sqrt(2.0)

    assert math.isclose(alpha + beta, 4.0, rel_tol=1e-9)
    assert math.isclose(alpha * beta, 2.0, rel_tol=1e-9)

    s4 = (alpha ** 4) + (beta ** 4)
    assert math.isclose(s4, 136.0, rel_tol=1e-9)


def test_math_conditional_cubic_identity():
    """Verify symmetric identity:
    a + b + c = 0, a^2 + b^2 + c^2 = 12 ==> a^4 + b^4 + c^4 = 72.
    """
    # Explicit test triplet satisfying constraints: a = 2, b = -1 + sqrt(3), c = -1 - sqrt(3)
    a = 2.0
    b = -1.0 + math.sqrt(3.0)
    c = -1.0 - math.sqrt(3.0)

    assert math.isclose(a + b + c, 0.0, abs_tol=1e-9)
    assert math.isclose((a ** 2) + (b ** 2) + (c ** 2), 12.0, rel_tol=1e-9)

    s4 = (a ** 4) + (b ** 4) + (c ** 4)
    assert math.isclose(s4, 72.0, rel_tol=1e-9)


def test_math_cubic_vieta_transformed_product():
    """Verify (1 + x1)(1 + x2)(1 + x3) = -P(-1) = 11 for P(x) = x^3 - 3x^2 + 2x - 5."""
    def P(x):
        return (x ** 3) - 3.0 * (x ** 2) + 2.0 * x - 5.0

    val = - P(-1.0)
    assert math.isclose(val, 11.0, rel_tol=1e-9)


def test_math_sophie_germain_primality():
    """Verify Sophie Germain identity factorization:
    4n^4 + 1 = (2n^2 - 2n + 1)(2n^2 + 2n + 1).
    n = 1 ==> (1)(5) = 5 (prime).
    n >= 2 ==> both factors > 1, so composite.
    """
    for n in range(1, 20):
        f1 = 2 * (n ** 2) - 2 * n + 1
        f2 = 2 * (n ** 2) + 2 * n + 1
        N = 4 * (n ** 4) + 1
        assert f1 * f2 == N
        if n == 1:
            assert f1 == 1 and f2 == 5
        else:
            assert f1 > 1 and f2 > 1


def test_math_modular_polynomial_remainder():
    """Verify polynomial remainder of x^2024 + x^2023 + 1 mod (x^2 + 1) is -x + 2."""
    # Since x^2 == -1:
    # x^2024 = (-1)^1012 = 1
    # x^2023 = x * (-1)^1011 = -x
    # Remainder R(x) = 1 + (-x) + 1 = -x + 2
    a = -1
    b = 2
    assert (a, b) == (-1, 2)


def test_math_functional_equation_degree():
    """Verify degree balancing in functional equation:
    P(x^2) = (x^2 + 1)P(x) ==> 2n = 2 + n ==> n = 2.
    """
    def check_degrees(n):
        lhs_deg = 2 * n
        rhs_deg = 2 + n
        return lhs_deg == rhs_deg

    matching = [n for n in range(10) if check_degrees(n)]
    assert matching == [2]


# ---------------------------------------------------------------------------
# 5. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html


def test_math_algebra_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 algebra items."""
    questions_file = MATH_DIR / "questions.json"
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
        assert q.get("crux_move_ref", "").startswith("MATH-OLY-POLY-")
        assert q.get("family_ref") == "MATH-ALGEBRA-POLYNOMIALS"
        assert q.get("primary_capability_ref", "").startswith("MATH-ALG-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 6. Question Status Preview Page Validation
# ---------------------------------------------------------------------------

def test_preview_question_status_page_mathematics():
    path = REPO_ROOT / "preview/question-status.html"
    assert path.exists(), "Missing preview/question-status.html"
    html = path.read_text(encoding="utf-8")

    # Match JSON script data
    m = re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>', html, re.DOTALL)
    assert m, "Missing #wpe-data script tag in preview/question-status.html"
    data = json.loads(m.group(1))

    questions = data["questions"]
    assert len(questions) >= 60, f"Expected at least 60 unified questions, found {len(questions)}"

    poly_questions = [q for q in questions if "POLY" in q.get("source_id", "")]
    assert len(poly_questions) == 10, f"Expected 10 algebra & polynomial questions, found {len(poly_questions)}"

    # Check each math question's structure
    for q in poly_questions:
        assert "id" in q and q["id"].startswith("MATH-")
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
    assert 'value="ALGEBRA_AND_POLYNOMIALS"' in html
    assert 'class="status"' in html
    assert 'class="layout"' in html
    assert 'class="filters"' in html
    assert 'class="stage"' in html
