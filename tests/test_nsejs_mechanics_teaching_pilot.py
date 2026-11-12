"""Independent numerical and semantic checks of the authored Mechanics pilot.

These are scientific arithmetic controls on an AUTHORED-PRACTICE technical lesson,
NOT admission of an original NSEJS paper or observed student mastery.
"""
from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "nsejs/contracts"))
sys.path.insert(0, str(ROOT / "tools"))
from wpe_learner_contract import ContractError, validate
from source_learning_bridge import validate_bindings

LESSON = ROOT / "nsejs/data/mechanics-wpe-teaching-pilot.v1.json"
SOURCE = ROOT / "nsejs/data/physics-authored-practice-r1.json"
BRIDGE = ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json"


def sticking_v(m1: float, u1: float, m2: float, u2: float) -> float:
    return (m1 * u1 + m2 * u2) / (m1 + m2)


def kinetic_energy(m: float, v: float) -> float:
    return 0.5 * m * v * v


def stopping_distance(v: float, mu: float, g: float) -> float:
    if mu == 0:
        return math.inf
    return v * v / (2 * mu * g)


def equal_mass_restitution(u: float, e: float) -> tuple[float, float]:
    # Equal masses with B initially stationary: momentum vA+vB=u,
    # coefficient of restitution e=(vB-vA)/u.
    return u * (1 - e) / 2, u * (1 + e) / 2


def expected(task: dict, field_id: str):
    row, = [f for f in task["fields"] if f["id"] == field_id]
    return row["expected"]


@pytest.fixture
def data():
    return json.loads(LESSON.read_text("utf-8"))


def test_contract_and_source_bridge_match_authored_evidence(data):
    bridge = json.loads(BRIDGE.read_text("utf-8"))
    collection = json.loads(SOURCE.read_text("utf-8"))
    routes = validate_bindings(bridge, collection)
    assert len(routes) == 1
    result = validate(data, routes[0])
    assert result["academic_admission"] == "HOLD"
    assert result["source_uid"] == "g9:PHYSICS:G9-AUTH-MECH-001"
    assert data["source"]["origin"] == "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert data["source_return"]["route_status"] == "UNBUILT"


def test_original_source_answer_matches_independent_two_stage_model(data):
    p = data["lesson"]["reference_physics"]["original"]
    v = sticking_v(p["m1_kg"], p["u1_mps"], p["m2_kg"], p["u2_mps"])
    assert v == pytest.approx(4.0)
    distance = stopping_distance(v, p["mu"], p["g_mps2"])
    assert distance == pytest.approx(3.2)
    assert p["joined_speed_mps"] == pytest.approx(v)
    assert p["stopping_distance_m"] == pytest.approx(distance)
    question, = json.loads(SOURCE.read_text("utf-8"))["questions"]
    assert question["answer"] == "C: 3.2 m"
    assert question["qrt_adjudication"] == "HOLD"
    assert question["science_review"] == "HOLD"


def test_original_collision_kinetic_energy_lost_not_counted_twice(data):
    p = data["lesson"]["reference_physics"]["original"]
    m = p["m1_kg"]
    before = kinetic_energy(m, p["u1_mps"])
    after = kinetic_energy(2 * m, p["joined_speed_mps"])
    loss = before - after
    assert (before, after, loss) == pytest.approx((32, 16, 16))
    assert loss == p["collision_energy_loss_per_m_kg_j"]
    friction = p["mu"] * (2 * m) * p["g_mps2"]
    assert after == pytest.approx(friction * p["stopping_distance_m"])
    assert not math.isclose(before, after)
    assert not math.isclose(before, friction * p["stopping_distance_m"])


@pytest.mark.parametrize("mu", [0.1, 0.2, 0.25, 0.4, 0.6])
def test_core1a_slider_uses_positive_mu_and_monotonic_distance(data, mu):
    model = data["lesson"]["core1a"]["model"]
    assert model["kind"] == "SLIDER_MODEL"
    assert model["min"] <= mu <= model["max"]
    v = sticking_v(1, 8, 1, 0)
    d = stopping_distance(v, mu, 10)
    assert d > 0
    assert stopping_distance(v, 2 * mu, 10) == pytest.approx(d / 2)
    if mu == 0.25:
        assert d == pytest.approx(3.2)


def test_zero_mu_no_finite_stopping_distance(data):
    assert stopping_distance(4, 0, 10) == math.inf
    assert stopping_distance(4, 0.000001, 10) > 10000
    [choice] = [f for f in data["tasks"]["A"]["boundaryFields"] if f["id"] == "model"]
    assert "No finite stopping distance" in choice["expected"]


def test_task_a_science_energy_and_units(data):
    p = data["lesson"]["reference_physics"]["task_a"]
    V = sticking_v(p["m1_kg"], p["u1_mps"], p["m2_kg"], p["u2_mps"])
    before = kinetic_energy(p["m1_kg"], p["u1_mps"])
    after = kinetic_energy(p["m1_kg"] + p["m2_kg"], V)
    force = p["mu"] * (p["m1_kg"] + p["m2_kg"]) * p["g_mps2"]
    d = after / force
    assert (V, before, after, before-after, force, d) == pytest.approx((4, 36, 24, 12, 6, 4))
    assert expected(data["tasks"]["A"], "speed") == V
    assert expected(data["tasks"]["A"], "loss") == before - after
    assert expected(data["tasks"]["A"], "distance") == d
    assert "m/s" in next(x["label"] for x in data["tasks"]["A"]["fields"] if x["id"] == "speed")
    assert "(J)" in next(x["label"] for x in data["tasks"]["A"]["fields"] if x["id"] == "loss")
    assert "(m)" in next(x["label"] for x in data["tasks"]["A"]["fields"] if x["id"] == "distance")


def test_task_b_elastic_collision_is_not_original_sticking_model(data):
    p = data["lesson"]["reference_physics"]["task_b"]
    a, b = equal_mass_restitution(p["u1_mps"], 1)
    assert (a, b) == pytest.approx((0, 6))
    assert b != sticking_v(1, p["u1_mps"], 1, 0)
    before = kinetic_energy(1, p["u1_mps"])
    after = kinetic_energy(1, a) + kinetic_energy(1, b)
    assert after == before == 18
    inferred_mu = b*b/(2 * p["g_mps2"] * p["observed_stop_m"])
    assert inferred_mu == pytest.approx(0.2)
    assert expected(data["tasks"]["B"], "speed") == pytest.approx(b)
    assert expected(data["tasks"]["B"], "mu") == pytest.approx(inferred_mu)
    assert "dimensionless" in next(x["label"] for x in data["tasks"]["B"]["fields"] if x["id"] == "mu")
    wrong_sticking_mu = (p["u1_mps"] / 2)**2/(2*p["g_mps2"]*p["observed_stop_m"])
    assert wrong_sticking_mu == pytest.approx(0.05)
    assert wrong_sticking_mu != inferred_mu


def test_task_b_nonelastic_boundary_requires_restitution_model(data):
    p = data["lesson"]["reference_physics"]["task_b"]
    e = p["e_boundary"]
    a, b = equal_mass_restitution(p["u1_mps"], e)
    assert (a, b) == pytest.approx((1.5, 4.5))
    mu = b*b/(2*p["g_mps2"]*p["observed_stop_m"])
    assert mu == pytest.approx(p["b_boundary_mu"])
    assert mu == pytest.approx(0.1125)
    boundary = data["tasks"]["B"]["boundaryFields"]
    assert next(x["expected"] for x in boundary if x["id"] == "speed") == pytest.approx(b)
    assert next(x["expected"] for x in boundary if x["id"] == "mu") == pytest.approx(mu)


def test_task_a_b_demand_is_different_and_feedback_is_answer_specific(data):
    a, b = data["tasks"]["A"], data["tasks"]["B"]
    assert a["reasoning_demand"] != b["reasoning_demand"]
    assert "ELASTIC" in b["challenge"]
    assert "sticks" in a["challenge"]
    assert a["id"] != b["id"]
    assert "stick" in next(x["mistake"] for x in b["fields"] if x["id"] == "model").lower()
    assert all(len(task["hints"]) >= 2 for task in (a, b))
    assert all(len(task["worked"]) >= 5 for task in (a, b))
    assert all(task["written_response_grading"] == "UNASSESSED" for task in (a, b))


def test_revision_and_task_collision_negatives(data):
    bad = deepcopy(data)
    bad["source"]["content_revision_sha256"] = "0"*64
    with pytest.raises(ContractError, match="SOURCE_BRIDGE_REVISION_OR_OWNER_MISMATCH"):
        route = json.loads(BRIDGE.read_text("utf-8"))["routes"][0]
        validate(bad, route)
    bad = deepcopy(data)
    bad["tasks"]["B"]["id"] = bad["tasks"]["A"]["id"]
    with pytest.raises(ContractError, match="CROSS_TASK_ATTEMPT_ID_COLLISION"):
        validate(bad)
    bad = deepcopy(data)
    bad["tasks"]["B"]["reasoning_demand"] = bad["tasks"]["A"]["reasoning_demand"]
    with pytest.raises(ContractError, match="TASK_B_IS_NOT_COGNITIVELY_DISTINCT"):
        validate(bad)


@pytest.mark.parametrize("subject", ["CHEMISTRY", "BIOLOGY"])
def test_science_lesson_never_masquerades_as_other_subject(data, subject):
    bad = deepcopy(data)
    bad["subject"] = subject
    with pytest.raises(ContractError, match="SOURCE_UID_SUBJECT_MISMATCH"):
        validate(bad)
