"""Independent numerical cross-checks for authored P1 WPE packs; not QRT certification."""
import json
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "WPE_Source_to_Core1A_Concept/learning-bridge/P0_P1_CONSTRUCTION_BRIDGE.json"


def checks():
    return json.loads(BRIDGE.read_text(encoding="utf-8"))["solution_checks"]


def eq(left, right):
    assert isclose(left, right, rel_tol=1e-11, abs_tol=1e-11), (left, right)


def conveyor(rate, u, v, force, motor, kinetic, heat):
    assert rate > 0 and 0 <= u < v
    calculated_force = rate * (v - u)
    eq(force, calculated_force)
    eq(motor, calculated_force * v)
    eq(kinetic, 0.5 * rate * (v*v - u*u))
    eq(heat, 0.5 * rate * (v-u)**2)
    eq(motor, kinetic+heat)


def test_conveyor_guide_and_variable_flow_example():
    g = checks()["WPE-C07"]["guide"]
    conveyor(g["mass_flow_kg_s"], g["incoming_speed_m_s"], g["belt_speed_m_s"],
             g["force_n"], g["motor_power_w"], g["kinetic_gain_w"], g["slip_heat_w"])
    eq(g["boundary_incoming_speed_m_s"], g["belt_speed_m_s"])
    eq(g["boundary_pickup_force_n"], g["mass_flow_kg_s"] *
       (g["belt_speed_m_s"] - g["boundary_incoming_speed_m_s"]))
    eq(g["variable_feeder_flow_kg_s"], 0.5 * g["variable_feeder_speed_m_s"])
    eq(g["variable_feeder_power_w"], g["variable_feeder_flow_kg_s"] *
       g["variable_feeder_speed_m_s"]**2)


def test_conveyor_fresh_nonzero_arrival_and_changed_belt_speed():
    f = checks()["WPE-C07"]["fresh"]
    eq(f["mass_flow_kg_s"], f["flow_coefficient_kg_m"] * f["belt_speed_m_s"])
    conveyor(f["mass_flow_kg_s"], f["incoming_speed_m_s"], f["belt_speed_m_s"],
             f["force_n"], f["motor_power_w"], f["kinetic_gain_w"], f["slip_heat_w"])
    eq(f["boundary_mass_flow_kg_s"], f["flow_coefficient_kg_m"] *
       f["boundary_belt_speed_m_s"])
    conveyor(f["boundary_mass_flow_kg_s"], f["incoming_speed_m_s"],
             f["boundary_belt_speed_m_s"], f["boundary_force_n"],
             f["boundary_motor_power_w"], f["boundary_kinetic_gain_w"],
             f["boundary_slip_heat_w"])


def test_spring_controlled_variables_guide_and_reversal():
    g = checks()["WPE-C08"]["guide"]
    spring_constants = [g["spring_a_k_n_m"], g["spring_b_k_n_m"]]
    for i, stiffness in enumerate(spring_constants):
        eq(g["extension_energy_j"][i], 0.5 * stiffness * g["equal_extension_m"]**2)
        eq(g["force_energy_j"][i], g["equal_final_force_n"]**2 / (2*stiffness))
    assert g["extension_energy_j"][0] < g["extension_energy_j"][1]
    assert g["force_energy_j"][0] > g["force_energy_j"][1]


def test_spring_fresh_inferred_k_and_doubled_force():
    f = checks()["WPE-C08"]["fresh"]
    inferred = [force/f["measurement_extension_m"] for force in f["measurement_force_n"]]
    for i, stiffness in enumerate(inferred):
        eq(f["derived_k_n_m"][i], stiffness)
        eq(f["extension_energy_j"][i], 0.5 * stiffness * f["equal_extension_m"]**2)
        eq(f["force_energy_j"][i], f["equal_final_force_n"]**2 / (2*stiffness))
        eq(f["boundary_force_energy_j"][i], f["boundary_force_n"]**2 / (2*stiffness))
        eq(f["boundary_force_energy_j"][i] / f["force_energy_j"][i],
           f["force_doubling_energy_factor"])
    assert f["extension_energy_j"][0] < f["extension_energy_j"][1]
    assert f["force_energy_j"][0] > f["force_energy_j"][1]
    assert f["boundary_force_energy_j"][0] > f["boundary_force_energy_j"][1]
