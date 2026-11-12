"""Verification suite for NSEJS 2024 Physics Mechanics & Dynamics (Question 46) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Mathematical physics proofs (kinematic integrations, acceleration ranking, circular dynamics, Atwood machines, gravitation, sound harmonics)
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
NSEJS_DIR = REPO_ROOT / "workspace/output/nsejs-mechanics-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/nsejs/NSEJS-2024-P-Q46"

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
    assert bank["bank_id"] == "nsejs-2024-mechanics-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2024-P-Q46"
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
    assert q["answer"]["crux_move_ref"] == "NSEJS-2024-P-Q46-M2"
    assert "NSEJS-2024-P-Q46-M2" in q["extensions"]["grade9v3:core2_support_plan"]["protected_move_refs"]


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
# 4. Mathematical Physics Verification
# ---------------------------------------------------------------------------

def test_physics_decoupled_wagon_kinematics():
    """Verify decoupled wagon uniformly retarding vs train moving at constant speed:
    v_wagon(t) = v - a*t ==> t_stop = v / a.
    d1 = int_0^(v/a) (v - a*t) dt = v^2 / (2a) = (1/2) * v * t_stop.
    d2 = int_0^(v/a) v dt = v * (v / a) = v^2 / a = v * t_stop.
    d1 / d2 = (1/2 * v * t) / (v * t) = 1/2.
    """
    v = 25.0   # m/s
    a = 2.5    # m/s^2

    t_stop = v / a
    d1 = (v ** 2) / (2.0 * a)
    d2 = v * t_stop

    ratio = d1 / d2
    assert math.isclose(ratio, 0.5, rel_tol=1e-9)

    # Average velocity check
    v_avg_wagon = (v + 0.0) / 2.0
    v_avg_train = v
    assert math.isclose(v_avg_wagon / v_avg_train, 0.5, rel_tol=1e-9)


def test_physics_acceleration_comparison():
    """Verify ranking of 4 constant-acceleration motions:
    (a) Bus: 72 km/h (20 m/s) to 0 in 2.5 s ==> |a| = 8.0 m/s^2.
    (b) Rock: Free fall ==> g = 9.8 m/s^2.
    (c) Car: 0 to 108 km/h (30 m/s) in 4.0 s ==> a = 7.5 m/s^2.
    (d) Train: 0 to 216 m in 6.0 s ==> 216 = 1/2 a (36) ==> a = 12.0 m/s^2.
    Largest magnitude is Train: 12.0 m/s^2.
    """
    a_bus = 20.0 / 2.5
    a_rock = 9.8
    a_car = 30.0 / 4.0
    a_train = 2.0 * 216.0 / (6.0 ** 2)

    assert math.isclose(a_bus, 8.0, rel_tol=1e-9)
    assert math.isclose(a_rock, 9.8, rel_tol=1e-9)
    assert math.isclose(a_car, 7.5, rel_tol=1e-9)
    assert math.isclose(a_train, 12.0, rel_tol=1e-9)

    # Train has strictly the largest magnitude
    assert a_train > a_rock > a_bus > a_car


def test_physics_circular_motion_kinematics():
    """Verify uniform circular motion:
    Diameter D = 14 cm ==> R = 0.07 m.
    Arc of 45 deg swept in 0.02 s.
    Fraction of revolution = 45 / 360 = 1/8.
    Period T = 8 * 0.02 = 0.16 s ==> f = 1 / T = 6.25 Hz.
    Speed v = 2 * pi * R * f = 2 * (22/7) * 0.07 * 6.25 = 2.75 m/s.
    """
    D = 0.14
    R = D / 2.0
    delta_theta_deg = 45.0
    delta_t = 0.02

    f = (delta_theta_deg / 360.0) / delta_t
    assert math.isclose(f, 6.25, rel_tol=1e-9)

    pi_approx = 22.0 / 7.0
    v = 2.0 * pi_approx * R * f
    assert math.isclose(v, 2.75, rel_tol=1e-9)


def test_physics_atwood_machine_dynamics():
    """Verify Atwood machine dynamics:
    m1 = 3 kg, m2 = 1 kg, g = 9.8 m/s^2.
    a = (m1 - m2) / (m1 + m2) * g = 2/4 * 9.8 = 4.9 m/s^2.
    T = 2 * m1 * m2 / (m1 + m2) * g = 6/4 * 9.8 = 14.7 N.
    """
    m1, m2 = 3.0, 1.0
    g = 9.8

    a = (m1 - m2) / (m1 + m2) * g
    T = 2.0 * m1 * m2 / (m1 + m2) * g

    assert math.isclose(a, 4.9, rel_tol=1e-9)
    assert math.isclose(T, 14.7, rel_tol=1e-9)


def test_physics_planetary_gravity_scaling():
    """Verify surface gravity ratio for two spherical planets:
    g1 = G M / R^2
    g2 = G (2M) / (2R)^2 = G (2M) / (4 R^2) = (1/2) g1
    ==> g1 / g2 = 2 : 1.
    """
    M, R = 1.0, 1.0
    G = 1.0

    g1 = G * M / (R ** 2)
    g2 = G * (2.0 * M) / ((2.0 * R) ** 2)

    ratio = g1 / g2
    assert math.isclose(ratio, 2.0, rel_tol=1e-9)


def test_physics_equal_ke_momentum_ratio():
    """Verify momentum ratio for particles with equal kinetic energy:
    p = sqrt(2 m K) ==> p1 / p2 = sqrt(m1 / m2).
    m1 = 1 kg, m2 = 4 kg ==> p1 / p2 = sqrt(1 / 4) = 1/2.
    """
    m1, m2 = 1.0, 4.0
    K = 100.0

    p1 = math.sqrt(2.0 * m1 * K)
    p2 = math.sqrt(2.0 * m2 * K)

    assert math.isclose(p1 / p2, 0.5, rel_tol=1e-9)


def test_physics_sound_wave_wavelength_and_travel():
    """Verify sound wave properties:
    v = 360 m/s.
    Crest at x = 10 cm, adjacent trough at x = 30 cm ==> lambda / 2 = 20 cm ==> lambda = 40 cm = 0.4 m.
    f = v / lambda = 360 / 0.4 = 900 Hz.
    In 4.5 s: distance = 360 * 4.5 = 1620 m = 1.62 km.
    In 0.01 s: shift = 360 * 0.01 = 3.6 m = 360 cm = 9 * 40 cm = 9 lambda.
    Phase is invariant mod 2*pi, so trough remains at original coordinates, NOT at x = 20 cm or 40 cm.
    """
    v = 360.0
    crest_x = 0.10
    trough_x = 0.30

    half_lambda = trough_x - crest_x
    wavelength = 2.0 * half_lambda
    assert math.isclose(wavelength, 0.40, rel_tol=1e-9)

    f = v / wavelength
    assert math.isclose(f, 900.0, rel_tol=1e-9)

    dist_4_5s = v * 4.5
    assert math.isclose(dist_4_5s, 1620.0, rel_tol=1e-9)

    shift_0_01s = v * 0.01
    assert math.isclose(shift_0_01s / wavelength, 9.0, rel_tol=1e-9)


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

def test_preview_question_status_page_mechanics():
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

    selected = [q for q in corpus["questions"] if q.get("topic") == "MECHANICS"]
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
