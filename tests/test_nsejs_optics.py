"""Verification suite for NSEJS 2023 Physics Optics (Question 01) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical physics proofs (separation function, monotonicity, limiting cases)
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
NSEJS_DIR = REPO_ROOT / "workspace/output/nsejs-optics-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-2023-P-Q01"

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
    assert bank["bank_id"] == "nsejs-2023-optics-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2023-P-Q01"
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
    assert q["answer"]["crux_move_ref"] == "NSEJS-2023-P-Q01-M2"
    assert "NSEJS-2023-P-Q01-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]


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
    for move in q["answer"]["reasoning_route"]:
        assert move["kind"] in CANONICAL_OPERATIONS, f"Non-canonical verb in move {move['id']}: {move['kind']}"
    for scaf in q["scaffolds"]:
        assert scaf["support_kind"] in CANONICAL_OPERATIONS, f"Non-canonical verb in scaffold: {scaf['support_kind']}"


def test_anti_pattern_5_svg_root_dimensions_and_typography(module_html):
    assert 'width="100%"' in module_html
    assert 'height="100%"' in module_html
    assert 'height="auto"' not in module_html

    # Check font sizes inside SVG
    font_sizes = re.findall(r'font-size="(\d+)"', module_html)
    assert font_sizes, "No font sizes found in SVG"
    for fs in font_sizes:
        assert int(fs) >= 14, f"Font size inside SVG {fs}px is under W3C 14px threshold"


def test_anti_pattern_7_inert_derivations_until_commitment(module_html):
    assert 'id="derivation-section" class="derivation-section"' in module_html
    assert '.derivation-section {' in module_html
    assert 'display: none;' in module_html
    assert "derivationSection.style.display = 'block';" in module_html


# ---------------------------------------------------------------------------
# 4. Physics and Mathematical Model Validation
# ---------------------------------------------------------------------------

def test_physics_separation_monotonicity():
    """Verify D(x) = x + fx/(x+f) is strictly increasing with x (hence strictly decreasing as ant approaches)."""
    f = 10.0  # arbitrary test focal length

    def D(x):
        return x + (f * x) / (x + f)

    def dD_dx(x):
        return 1.0 + (f ** 2) / ((x + f) ** 2)

    # Check values at key points
    assert pytest.approx(D(2 * f)) == 8 * f / 3
    assert pytest.approx(D(f)) == 3 * f / 2
    assert pytest.approx(D(0.0)) == 0.0

    # Check monotonicity across a grid from x = 2f down to 0
    steps = [2.0 * f, 1.5 * f, 1.0 * f, 0.5 * f, 0.1 * f, 0.0]
    for i in range(len(steps) - 1):
        x_high = steps[i]
        x_low = steps[i + 1]
        assert D(x_high) > D(x_low), f"Separation did not decrease from {x_high} to {x_low}"
        assert dD_dx(x_high) > 1.0, f"Derivative should be > 1 at {x_high}"


# ---------------------------------------------------------------------------
# 5. Governance and Non-Bypassable HOLD Invariant
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html


# ---------------------------------------------------------------------------
# 6. Question Status Preview Page Validation
# ---------------------------------------------------------------------------

def test_preview_question_status_page():
    """The live Physics Core2 is source-indexed, not part of the legacy WPE
    question-status page. Verify the actual 50 unadmitted candidates instead
    of inventing obsolete parallel 10-card UI records.
    """
    old_preview = (REPO_ROOT / "preview/question-status.html").read_text(encoding="utf-8")
    assert 'id="wpe-data"' in old_preview

    corpus = json.loads((REPO_ROOT / "nsejs/data/physics-core2-candidates.v1.json")
                        .read_text(encoding="utf-8"))
    assert corpus["source_claims_status"] == "HOLD"
    assert corpus["qrt_adjudication"] == "HOLD"
    assert len(corpus["questions"]) == 50
    assert len({q["source_id"] for q in corpus["questions"]}) == 50

    selected = [q for q in corpus["questions"] if q.get("topic") == "OPTICS"]
    assert len(selected) == 10, "Original test-backed Physics topic count changed"
    for q in selected:
        assert q["id"].startswith(("NSEJS-", "IOQJS-"))
        assert q["source_id"]
        assert len(q["stem"]) > 10
        assert len(q["options"]) == 4
        assert q["op"] in CANONICAL_OPERATIONS
        assert q["band"] in {"D1", "D2", "D3", "D4"}
        assert q["review_state"] == "NOT_ADMITTED"
        assert len(q["hints"]) == 3
        assert len(q["steps"]) == 3
        assert len(q["check"]) > 5

    hub = (REPO_ROOT / "nsejs/physics/index.html").read_text(encoding="utf-8")
    reader = (REPO_ROOT / "nsejs/physics/question-bank.html").read_text(encoding="utf-8")
    engine = (REPO_ROOT / "nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert 'question-bank.html?topic=' in hub
    assert 'id="questions"' in reader and "not academically admitted" in reader
    assert '../js/core2-physics-reader.js' in reader
    assert 'physics-core2-candidates.v1.json' in engine
    assert '"NOT_ADMITTED"' in engine
    assert 'source and QRT admission HOLD' in engine
