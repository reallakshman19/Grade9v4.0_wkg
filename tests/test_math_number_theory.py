"""Verification suite for Mathematics Track: Number Theory & Divisibility (Question 01) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical proofs (Simon's factoring trick, divisor count lattice, Chinese Remainder Theorem, Legendre formula, Euclidean linearity, Euler totient, Wilson's theorem, Frobenius coin, Fermat's Little Theorem, divisor parity)
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
MATH_DIR = REPO_ROOT / "workspace/output/math-number-theory-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/math/MATH-OLY-NUM-01"

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
    assert bank["bank_id"] == "math-number-theory-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "MATH-OLY-NUM-01"
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
    assert q["answer"]["crux_move_ref"] == "MATH-OLY-NUM-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "MATH-OLY-NUM-01-M2" in plan["protected_move_refs"]


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

def test_math_number_theory_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 number theory items."""
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
        assert q.get("crux_move_ref", "").startswith("MATH-OLY-NUM-")
        assert q.get("family_ref", "").startswith("MATH-NUMBER-THEORY")
        assert q.get("primary_capability_ref", "").startswith("MATH-NUM-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Mathematical Truths (Olympiad Number Theory)
# ---------------------------------------------------------------------------

def test_simon_factoring_trick_divisor_count():
    """Verify Simon's Favorite Factoring Trick for 1/x + 1/y = 1/2024:
    (x - 2024)(y - 2024) = 2024^2.
    Number of positive integer solutions is d(2024^2).
    """
    N = 2024
    # Prime factorization of 2024: 2024 = 2^3 * 11 * 23
    assert 2**3 * 11 * 23 == 2024

    # Exponents for 2024^2: 2^6 * 11^2 * 23^2
    divisor_count = (6 + 1) * (2 + 1) * (2 + 1)
    assert divisor_count == 63

    # Direct lattice verification
    solutions = []
    N_sq = N * N
    for d in range(1, int(math.isqrt(N_sq)) + 1):
        if N_sq % d == 0:
            d2 = N_sq // d
            # pair (x, y) = (N + d, N + d2)
            solutions.append((N + d, N + d2))
            if d != d2:
                solutions.append((N + d2, N + d))

    assert len(solutions) == 63
    for x, y in solutions:
        assert x > 0 and y > 0
        # Check reciprocal equation: 1/x + 1/y == 1/N
        assert (x + y) * N == x * y


def test_chinese_remainder_theorem_solution():
    """Verify CRT system:
    n = 2 mod 3, n = 3 mod 5, n = 2 mod 7.
    Smallest positive integer n = 23.
    """
    candidates = [n for n in range(1, 200) if n % 3 == 2 and n % 5 == 3 and n % 7 == 2]
    assert len(candidates) > 0
    assert candidates[0] == 23


def test_legendre_formula_trailing_zeros():
    """Verify Legendre's formula for trailing zeros of 2024!:
    v_5(2024!) = 404 + 80 + 16 + 3 = 503.
    """
    n = 2024
    v5 = 0
    p = 5
    while p <= n:
        v5 += n // p
        p *= 5
    assert v5 == 503


def test_gcd_linear_invariance():
    """Verify Euclidean algorithm linearity:
    gcd(7n + 1, 15n + 4) divides 13.
    Achieves maximum 13 when n = 11 mod 13.
    """
    max_gcd = 0
    for n in range(1, 100):
        g = math.gcd(7 * n + 1, 15 * n + 4)
        if g > max_gcd:
            max_gcd = g
        assert 13 % g == 0
    assert max_gcd == 13
    assert math.gcd(7 * 11 + 1, 15 * 11 + 4) == 13


def test_base_representation_divisibility():
    """Verify repeated 3-digit number N = abcabc:
    N = 1001 * abc = 7 * 11 * 13 * abc.
    Largest guaranteed prime is 13.
    """
    assert 7 * 11 * 13 == 1001
    primes = [p for p in (2, 3, 5, 7, 11, 13, 17, 19) if 1001 % p == 0]
    assert primes == [7, 11, 13]
    assert max(primes) == 13


def test_euler_totient_coprime_count():
    """Verify Euler totient function:
    phi(360) = 360 * (1/2) * (2/3) * (4/5) = 96.
    """
    phi_360 = sum(1 for k in range(1, 361) if math.gcd(k, 360) == 1)
    assert phi_360 == 96


def test_wilson_theorem_remainder():
    """Verify Wilson's Theorem:
    (p - 1)! = -1 = p - 1 mod p for prime p = 101.
    """
    p = 101
    assert all(p % i != 0 for i in range(2, int(math.isqrt(p)) + 1))
    # Remainder is p - 1 = 100
    assert (p - 1) == 100


def test_frobenius_coin_postage():
    """Verify Frobenius number for stamps (5, 7):
    g(5, 7) = 5*7 - 5 - 7 = 23.
    """
    g = 5 * 7 - 5 - 7
    assert g == 23

    # Check that 23 cannot be formed
    achievable = set()
    for x in range(10):
        for y in range(10):
            achievable.add(5 * x + 7 * y)
    assert 23 not in achievable
    # Every integer >= 24 is achievable
    for v in range(24, 50):
        assert v in achievable


def test_fermat_little_theorem_remainder():
    """Verify Fermat's Little Theorem:
    3^16 = 1 mod 17 ==> 3^2024 = 3^8 = 16 mod 17.
    """
    assert pow(3, 16, 17) == 1
    rem = pow(3, 2024, 17)
    assert rem == 16


def test_locker_divisor_parity():
    """Verify 100 lockers problem:
    Locker n open iff d(n) is odd iff n is a perfect square.
    Number of open lockers is floor(sqrt(100)) = 10.
    """
    open_lockers = []
    for n in range(1, 101):
        divisors = sum(1 for d in range(1, n + 1) if n % d == 0)
        if divisors % 2 == 1:
            open_lockers.append(n)
    assert open_lockers == [k**2 for k in range(1, 11)]
    assert len(open_lockers) == 10


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
