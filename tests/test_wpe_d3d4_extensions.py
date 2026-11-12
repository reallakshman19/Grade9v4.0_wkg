"""Numerical and boundary checks for four WPE D3/D4 learning extension drafts.

These checks verify authored calculations and source-status separation, NOT academic
admission, independent learner success, or original examination key validity.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_DIR = ROOT / "WPE_Source_to_Core1A_Concept" / "learning-bridge"
BRIDGE = BRIDGE_DIR / "P0_P1_CONSTRUCTION_BRIDGE.json"
MAP = ROOT / "physics" / "wpe" / "learn-challenge-source-map.json"
READER = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def close(actual, expected):
    assert math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-11), (actual, expected)


def test_extension_inventory_and_six_stage_authored_separation():
    bridge = load(BRIDGE)
    ext = bridge["extension_inventory"]
    rows = bridge["extensions_backlog"]
    assert ext["drafted_count"] == 5 and ext["remaining_unwritten"] == 0
    assert ext["drafted_ids"] == ["WPE-E01", "WPE-E02", "WPE-E03", "WPE-E04", "WPE-E05"]
    assert len(rows) == 5
    assert len([r for r in rows if r["status"] == "AUTHOR_PACK_DRAFTED_NOT_ADMITTED"]) == 5
    assert set(bridge["extension_solution_checks"]) == set(ext["drafted_ids"])
    assert ext["original_exam_stems_reproduced"] is False
    assert ext["original_figures_substituted"] is False
    assert ext["student_website_modified"] is False
    assert ext["independent_learner_evidence"] is False
    assert ext["academic_qrt_owner_approvals_changed"] is False
    assert bridge["pack_inventory"]["all_eight_author_draft_count"] == 8
    assert len(bridge["constructions"]) == 8

    for row in rows:
        assert row["id"] in ext["drafted_ids"]
        pack = (BRIDGE_DIR / row["pack"]).read_text(encoding="utf-8")
        assert "## Core1A" in pack and "## Core1B" in pack, row["id"]
        assert "## Author-only reference" in pack, row["id"]
        assert all(f"### {i:02d}" in pack for i in range(1, 7)), row["id"]
        assert "Rubric:" in pack
        assert "Separation check:" in pack
        assert "not for learner-facing pre-attempt delivery" in pack
        assert "\\\\(" not in pack, "Double-escaped maths must not be introduced"
    assert rows[4]["topic"] == "Radial-force potential"
    assert rows[4]["status"] == "AUTHOR_PACK_DRAFTED_NOT_ADMITTED"


def test_source_references_retain_pending_and_under_specified_flags():
    bridge = load(BRIDGE)
    reader = load(READER)
    records = {q["source_id"]: q for q in reader["questions"]}
    ids = {id_ for row in bridge["extensions_backlog"][:4] for id_ in row["ids"]}
    assert ids == {"WEP07-03", "EX-M109", "TB-WPE-ILL-05", "TB-WPE-ILL-06", "EX-N34", "EX-M82"}
    assert all(records[x]["review_state"] == "NOT_ADMITTED" for x in ids)
    assert records["WEP07-03"]["band"] == "D2"
    assert any("initial speed" in f.lower() for f in records["TB-WPE-ILL-05"]["flags"])
    current_map = load(MAP)
    assert current_map["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert current_map["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert current_map["auth"]["qrt"] == "NOT_RUN"
    assert bridge["native_admissions"] == 0


def test_energy_well_accessible_intervals_and_barrier():
    data = load(BRIDGE)["extension_solution_checks"]["WPE-E01"]
    g, f = data["guide"], data["fresh"]
    m, energy = g["mass_kg"], g["total_energy_j"]
    U = lambda x: (x - g["bowl_center_m"])**2
    for x in (g["turns_m"][0], g["turns_m"][1]):
        close(U(x), energy)
    close(g["kinetic_j_at_center"], energy-U(g["bowl_center_m"]))
    close(g["max_speed_m_s"], math.sqrt(2*g["kinetic_j_at_center"]/m))
    assert g["low_energy_allowed_m"] == [1, 3]

    allowed = f["allowed_x_bounds_m"]
    close(allowed[0], -math.sqrt(7))
    close(allowed[1], -1)
    close(allowed[2], 1)
    close(allowed[3], math.sqrt(7))
    potential = lambda x: (x*x-4)**2
    for x in allowed:
        close(potential(x), f["total_energy_j"])
    close(potential(f["barrier_x_m"]), f["barrier_u_j"])
    assert f["barrier_u_j"] > f["total_energy_j"] and f["crossing_possible"] is False
    for x in f["valleys_x_m"]:
        close(potential(x), 0)
    close(f["maximum_speed_m_s"], math.sqrt(2*f["total_energy_j"]/f["mass_kg"]))
    close(f["boundary_center_speed_m_s"],
          math.sqrt(2*(f["boundary_total_energy_j"]-f["barrier_u_j"])/f["mass_kg"]))


def test_instantaneous_power_component_and_boundary():
    data = load(BRIDGE)["extension_solution_checks"]["WPE-E02"]
    g, f = data["guide"], data["fresh"]
    close(g["pull_power_w"], g["velocity_m_s"] * g["pull_n"])
    close(g["resistance_power_w"], g["velocity_m_s"] * g["resistance_n"])
    close(g["net_power_w"], g["pull_power_w"]+g["resistance_power_w"])
    close(g["opposite_net_power_w"], g["opposite_velocity_m_s"] *
          (g["pull_n"]+g["resistance_n"]))
    close(f["motor_power_w"], f["motor_right_n"]*f["v_right_m_s"])
    close(f["drag_power_w"], f["drag_left_n"]*f["v_right_m_s"]+
          f["drag_back_n"]*f["v_forward_m_s"])
    net_x = f["motor_right_n"]+f["drag_left_n"]
    close(f["net_power_w"], net_x*f["v_right_m_s"]+
          f["drag_back_n"]*f["v_forward_m_s"])
    close(f["boundary_net_power_w"], net_x*f["boundary_v_right_m_s"]+
          f["drag_back_n"]*f["boundary_v_forward_m_s"])
    assert net_x > 0 and f["drag_back_n"] < 0
    assert f["boundary_v_forward_m_s"] > 0 and f["boundary_net_power_w"] == 0


def test_spring_contact_then_horizontal_projectile():
    data = load(BRIDGE)["extension_solution_checks"]["WPE-E03"]
    g, f = data["guide"], data["fresh"]
    close(g["spring_energy_j"], 0.5*g["spring_k_n_m"]*g["compression_m"]**2)
    close(g["launch_speed_m_s"],
          math.sqrt(2*g["spring_energy_j"]/g["puck_mass_kg"]))
    close(g["other_ball_flight_time_s"],
          math.sqrt(2*g["other_ball_height_m"]/g["gravity_m_s2"]))
    close(g["other_ball_range_m"],
          g["other_ball_initial_horizontal_speed_m_s"]*g["other_ball_flight_time_s"])
    close(f["spring_energy_j"], 0.5*f["spring_k_n_m"]*f["compression_m"]**2)
    close(f["contact_friction_work_j"], -f["contact_friction_n"]*f["compression_m"])
    close(f["launch_kinetic_j"], f["spring_energy_j"]+f["contact_friction_work_j"])
    close(f["launch_speed_m_s"], math.sqrt(2*f["launch_kinetic_j"]/f["mass_kg"]))
    close(f["flight_time_s"], math.sqrt(2*f["height_m"]/f["gravity_m_s2"]))
    close(f["range_m"], f["launch_speed_m_s"]*f["flight_time_s"])
    close(f["boundary_launch_speed_m_s"], math.sqrt(2*f["spring_energy_j"]/f["mass_kg"]))
    close(f["boundary_flight_time_s"], f["flight_time_s"])
    close(f["boundary_range_m"], f["boundary_launch_speed_m_s"]*f["boundary_flight_time_s"])
    assert f["boundary_range_m"] > f["range_m"]


def test_bounce_change_of_retention_and_geometric_distance():
    data = load(BRIDGE)["extension_solution_checks"]["WPE-E04"]
    g, f = data["guide"], data["fresh"]
    h = g["initial_height_m"]
    r = g["retained_energy_fraction"]
    for i, hi in enumerate(g["first_three_rebound_heights_m"], start=1):
        close(hi, h*r**i)
    close(g["total_distance_m"], h+2*h*r/(1-r))
    close(g["speed_ratio"], math.sqrt(r))
    assert 0 < r < 1
    h, r0, r1 = f["initial_height_m"], f["first_impact_retention"], f["later_impact_retention"]
    first = h*r0
    for i, hi in enumerate(f["first_three_rebound_heights_m"]):
        close(hi, first*r1**i)
    close(f["total_distance_m"], h+2*first/(1-r1))
    close(f["first_speed_ratio"], math.sqrt(r0))
    boundary_r = f["boundary_all_impacts_retention"]
    close(f["boundary_total_distance_m"], h+2*h*boundary_r/(1-boundary_r))
    assert f["boundary_total_distance_m"] > f["total_distance_m"]
