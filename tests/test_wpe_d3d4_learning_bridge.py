"""Proposed D3/D4 source-to-learning bridge invariants; NOT an academic/QRT test."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "WPE_Source_to_Core1A_Concept"
BRIDGE_PATH = BASE / "learning-bridge/P0_P1_CONSTRUCTION_BRIDGE.json"
SELECTION_PATH = BASE / "evidence/RECEIVED_selection_21_places.json"
READER_PATH = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_bridge_reconciles_current_selected_claims_without_promoting_them():
    bridge, selection, reader = map(load, (BRIDGE_PATH, SELECTION_PATH, READER_PATH))
    candidates = [p for p in selection["places"] if p["candidate_id"] is not None]
    source = {q["source_id"]: q for q in reader["questions"]}
    assert len(selection["places"]) == 21
    assert len(candidates) == 14
    assert len([p for p in selection["places"] if p["status"] == "VACANT"]) == 7
    assert selection["admitted"] == bridge["native_admissions"] == 0
    assert bridge["counts"]["pilot_places"] == len(selection["places"])
    assert bridge["counts"]["pending_candidates"] == len(candidates)
    assert {r["candidate_id"] for r in bridge["reconciliation"]} == {p["candidate_id"] for p in candidates}
    assert len(bridge["reconciliation"]) == 14

    for item in bridge["reconciliation"]:
        selected = next(p for p in candidates if p["candidate_id"] == item["candidate_id"])
        assert item["pilot_operation"] == selected["operation"]
        assert item["pilot_band"] == selected["band"]
        found = source.get(item["candidate_id"])
        expected = (
            "ABSENT_FROM_SELECTED_READER" if found is None
            else "AGREES_IN_READER"
            if found["op"] == selected["operation"] and found["band"] == selected["band"]
            else "CONFLICT_IN_READER"
        )
        assert item["comparison"] == expected
        assert item["academic_status"] == "PENDING__NO_AUTHORITY_TO_REPLACE"
    observed = {key: sum(r["comparison"] == status for r in bridge["reconciliation"])
                for key, status in (("reader_agree", "AGREES_IN_READER"),
                                    ("reader_conflicts", "CONFLICT_IN_READER"),
                                    ("reader_absent", "ABSENT_FROM_SELECTED_READER"))}
    assert observed == {k: bridge["counts"][k] for k in observed}
    assert observed == {"reader_agree": 3, "reader_conflicts": 8, "reader_absent": 3}
    assert {r["candidate_id"] for r in bridge["reconciliation"]
            if r["comparison"] == "ABSENT_FROM_SELECTED_READER"} == {"EX-M81", "EX-M44", "EX-M60"}


def test_eight_distinct_construction_specs_and_six_step_self_tutor_cycle():
    bridge = load(BRIDGE_PATH)
    specs = bridge["constructions"]
    assert len(specs) == 8
    assert len({row["id"] for row in specs}) == 8
    assert sum(row["priority"] == "P0" for row in specs) == 6
    assert sum(row["priority"] == "P1" for row in specs) == 2
    assert bridge["core1b_contract"] == ["PREDICT", "ATTEMPT", "RECONSTRUCT",
                                         "DIAGNOSE", "REPAIR", "BOUNDARY_TEST"]
    assert all(len(s["core1a"]) >= 4 and len(s["core1b"]) == 6 for s in specs)
    assert all(s["links"] and s["misconception"] and s["starting_foundation"] for s in specs)
    assert bridge["status"].endswith("NOT_ACADEMICALLY_ADMITTED")
    assert bridge["owner_approval"] is False
    assert bridge["qrt_approval"] is False

    for row in specs:
        if row["first_pair"]:
            pack = BASE / "learning-bridge" / row["first_pair"]
            content = pack.read_text(encoding="utf-8")
            assert "## Core1A" in content and "## Core1B" in content
            assert "Author-only reference" in content
            assert all(f"### {i:02d}" in content for i in range(1, 7))
            assert "Separation check" in content
            assert "\\\\(" not in content, "Markdown maths must not be double-escaped"


def test_eight_complete_author_packs_with_zero_academic_promotion():
    bridge = load(BRIDGE_PATH)
    p0 = [row for row in bridge["constructions"] if row["priority"] == "P0"]
    p1 = [row for row in bridge["constructions"] if row["priority"] == "P1"]
    assert len(p0) == 6 and len(p1) == 2
    assert all(row["first_pair"] for row in p0)
    assert all(row["first_pair"] for row in p1)
    inventory = bridge["pack_inventory"]
    assert inventory["p0_complete_draft_count"] == len(p0) == 6
    assert inventory["p1_complete_draft_count"] == len(p1) == 2
    assert inventory["all_eight_author_draft_count"] == 8
    assert set(inventory["p1_newly_drafted_in_batch"]) == {"WPE-C07", "WPE-C08"}
    assert inventory["source_qrt_owner_approval_changed"] is False
    assert inventory["student_website_modified"] is False
    assert inventory["official_source_stems_republished"] is False
    assert inventory["first_attempt_secure_delivery_claim"] is False
    for row in p0 + p1:
        pack = BASE / "learning-bridge" / row["first_pair"]
        content = pack.read_text(encoding="utf-8")
        assert "Child's key decision" in content, row["id"]
        assert "## Core1A" in content and "## Core1B" in content
        assert "## Author-only reference" in content
        assert "Separation check" in content
        assert "rubric" in content.casefold()
        assert all(f"### {i:02d}" in content for i in range(1, 7))
        assert "not for learner-facing pre-attempt delivery" in content
        assert "\\\\(" not in content, "Double-escaped maths cannot render as intended"


def test_numerical_answers_for_four_new_p0_packs():
    from math import isclose, sqrt

    checks = load(BRIDGE_PATH)["solution_checks"]
    assert set(checks) == {f"WPE-C0{i}" for i in range(3, 9)}
    close = lambda a, b: isclose(a, b, rel_tol=1e-11, abs_tol=1e-11)

    p = checks["WPE-C03"]
    for group_name in ("guide", "fresh"):
        group = p[group_name]
        m, u, power = group["mass_kg"], group["initial_m_s"], group["power_w"]
        for i, t in enumerate(group["time_s"]):
            K = 0.5 * m * u**2 + power * t
            speed = sqrt(2*K / m)
            assert close(group["speed_m_s"][i], speed)
            if group_name == "fresh":
                assert close(group["kinetic_j"][i], K)
    f = p["fresh"]
    boundary_K = 0.5*f["mass_kg"]*f["initial_m_s"]**2 + f["boundary_power_w"]*f["boundary_time_s"]
    assert close(f["boundary_speed_m_s"], sqrt(2*boundary_K/f["mass_kg"]))

    p = checks["WPE-C04"]
    for group_name in ("guide", "fresh"):
        group = p[group_name]
        linear_density = group["mass_kg"] / group["length_m"]
        def U(hanging):
            return -0.5 * linear_density * 10 * hanging**2
        assert close(group["lift_work_j"], U(group["final_hanging_m"]) - U(group["initial_hanging_m"]))
        if group_name == "fresh":
            assert close(group["boundary_lift_work_j"], U(group["boundary_final_hanging_m"]) - U(group["initial_hanging_m"]))

    p = checks["WPE-C05"]
    assert close(p["guide"]["force_rectangle_work_j"], 3*2)
    assert close(p["guide"]["potential_force_n"], -(3-9)/2)
    assert close(p["guide"]["displacement_time_velocity_m_s"], 6/3)
    assert close(p["fresh"]["force_position_triangle_work_j"], 0.5*4*8)
    assert close(p["fresh"]["potential_position_force_n"], -(8-2)/2)
    assert close(p["fresh"]["second_interval_velocity_m_s"], (16-4)/(5-2))
    assert close(p["fresh"]["boundary_force_time_impulse_n_s"], 0.5*4*8)

    p = checks["WPE-C06"]
    guide, fresh, g = p["guide"], p["fresh"], 10
    m, r, top = guide["mass_kg"], guide["radius_m"], guide["top_speed_m_s"]
    assert close(guide["top_tension_n"], m*top**2/r-m*g)
    v_bottom_squared = top**2+4*g*r
    assert close(guide["bottom_speed_squared"], v_bottom_squared)
    assert close(guide["bottom_tension_n"], m*v_bottom_squared/r+m*g)
    top2 = fresh["bottom_speed_m_s"]**2-4*g*fresh["radius_m"]
    assert close(fresh["top_speed_squared"], top2)
    T = fresh["mass_kg"]*top2/fresh["radius_m"] - fresh["mass_kg"]*g
    assert close(fresh["top_tension_n"], T)
    assert fresh["taut_string_possible"] is False and T < 0
    boundary_top2 = fresh["boundary_bottom_speed_m_s"]**2-4*g*fresh["radius_m"]
    assert close(fresh["boundary_top_speed_squared"], boundary_top2)
    assert close(fresh["boundary_top_tension_n"], fresh["mass_kg"]*boundary_top2/fresh["radius_m"] - fresh["mass_kg"]*g)
    assert close(fresh["minimum_bottom_speed_squared"], 5*g*fresh["radius_m"])


def test_foundational_teaching_remains_unadmitted_and_review_is_historical():
    bridge = load(BRIDGE_PATH)
    mapping = load(ROOT / "physics/wpe/learn-challenge-source-map.json")
    assert mapping["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert mapping["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert mapping["auth"]["qrt"] == "NOT_RUN"
    assert mapping["auth"]["owner"] == "PENDING"
    assert bridge["stale_review"]["conclusion"].startswith("REVIEW_SUPERSEDED")
    assert bridge["stale_review"]["reviewed_page_blob_sha"] != bridge["stale_review"]["current_page_blob_sha"]
    assert bridge["stale_review"]["reviewed_map_blob_sha"] != bridge["stale_review"]["current_map_blob_sha"]
