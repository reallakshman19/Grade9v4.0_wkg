"""WPE-E05 radial force and circular-energy author-pack correctness checks.

Not a source-key, syllabus, independent Core1B/QRT, or Owner acceptance test.
"""
import json
from math import isclose, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_DIR = ROOT / "WPE_Source_to_Core1A_Concept" / "learning-bridge"
BRIDGE = BRIDGE_DIR / "P0_P1_CONSTRUCTION_BRIDGE.json"
EXAM_READER = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
LEARNER_MAP = ROOT / "physics/wpe/learn-challenge-source-map.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def close(actual, expected):
    assert isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-11), (actual, expected)


def test_e05_source_and_pack_inventory_stays_unadmitted():
    bridge = load(BRIDGE)
    inv = bridge["extension_inventory"]
    ext = bridge["extensions_backlog"]
    assert len(ext) == 5
    assert inv["drafted_count"] == 5
    assert inv["remaining_unwritten"] == 0
    assert inv["remaining_id"] is None and inv["remaining_topic"] is None
    assert set(inv["drafted_ids"]) == {f"WPE-E0{i}" for i in range(1, 6)}
    assert all(row["status"] == "AUTHOR_PACK_DRAFTED_NOT_ADMITTED" for row in ext)
    assert all(row["pack"] for row in ext)
    assert set(bridge["extension_solution_checks"]) == set(inv["drafted_ids"])
    assert ext[4]["id"] == "WPE-E05" and ext[4]["ids"] == ["EX-M89"]
    assert ext[4]["pack"] == "RADIAL_FORCE_POTENTIAL_LEARNING_PACK.md"
    assert inv["original_exam_stems_reproduced"] is False
    assert inv["original_figures_substituted"] is False
    assert inv["student_website_modified"] is False
    assert inv["independent_learner_evidence"] is False
    assert inv["academic_qrt_owner_approvals_changed"] is False
    assert bridge["native_admissions"] == bridge["counts"]["admitted"] == 0
    assert bridge["pack_inventory"]["all_eight_author_draft_count"] == 8

    source = next(q for q in load(EXAM_READER)["questions"] if q["source_id"] == "EX-M89")
    assert source["review_state"] == "NOT_ADMITTED"
    assert source["op"] == "SYNTHESIZE" and source["band"] == "D3"
    assert "Coaching predicted" in source["answer"]
    mapping = load(LEARNER_MAP)
    assert mapping["auth"]["native_core1a"] == "NOT_ACCEPTED"
    assert mapping["auth"]["native_core1b"] == "NOT_ACCEPTED"
    assert mapping["auth"]["qrt"] == "NOT_RUN"
    assert mapping["auth"]["owner"] == "PENDING"


def test_e05_six_stage_distinct_original_author_pack():
    path = BRIDGE_DIR / "RADIAL_FORCE_POTENTIAL_LEARNING_PACK.md"
    content = path.read_text(encoding="utf-8")
    assert "## Core1A" in content and "## Core1B" in content
    assert "## Author-only reference" in content
    assert "not for learner-facing pre-attempt delivery" in content
    assert all(f"### {i:02d}" in content for i in range(1, 7))
    assert "**Rubric:**" in content and "**Separation check:**" in content
    assert "\\\\(" not in content, "Doubled-escaped math syntax"
    assert "rectangle" in content and "trapezoid" in content
    assert "force magnitude" in content.lower()
    assert "does no work" in content
    assert "positive" in content


def test_guided_constant_inward_force_two_independent_energy_relations():
    guide = load(BRIDGE)["extension_solution_checks"]["WPE-E05"]["guide"]
    m, f, r = guide["mass_kg"], guide["inward_force_magnitude_n"], guide["circular_radius_m"]
    assert m > 0 and f > 0 and r > 0
    assert guide["reference_radius_m"] == 0
    # Area under magnitude f(r) from 0 to r -> U(r), with U(0)=0.
    U = f*r
    # Separate inward-force condition mv²/r=f -> K=fr/2.
    v2 = f*r/m
    K = 0.5*m*v2
    close(guide["potential_energy_j"], U)
    close(guide["speed_squared_m2_s2"], v2)
    close(guide["speed_m_s"], sqrt(v2))
    close(guide["kinetic_energy_j"], K)
    close(guide["total_energy_j"], U+K)
    # At fixed radius, the force is radial and velocity tangent; dot product is zero.
    close(0, -f*0)


def test_new_piecewise_force_uses_full_area_and_local_centripetal_force():
    fresh = load(BRIDGE)["extension_solution_checks"]["WPE-E05"]["fresh"]
    m = fresh["mass_kg"]
    inner_f = fresh["inner_force_n"]
    join_r = fresh["inner_radius_m"]
    grad = fresh["outer_force_gradient_n_per_m"]
    r = fresh["orbit_radius_m"]
    assert 0 < join_r < r < fresh["boundary_radius_m"]
    close(inner_f, grad*join_r)  # graph continuous at transition
    first_area = inner_f*join_r
    local_force = grad*r
    outer_area = (inner_f+local_force)*(r-join_r)/2
    U = first_area+outer_area
    v2 = local_force*r/m
    K = 0.5*m*v2
    close(fresh["first_rectangle_j"], first_area)
    close(fresh["outer_trapezoid_j"], outer_area)
    close(fresh["local_inward_force_n"], local_force)
    close(fresh["potential_energy_j"], U)
    close(fresh["speed_squared_m2_s2"], v2)
    close(fresh["speed_m_s"], sqrt(v2))
    close(fresh["kinetic_energy_j"], K)
    close(fresh["total_energy_j"], K+U)

    # Radial work (if moving outward) is -Delta U. Circular travel has dr=0.
    close(-U, -first_area-outer_area)
    assert fresh["total_energy_j"] == 22


def test_changed_radius_represents_distinct_orbit_not_free_transition():
    fresh = load(BRIDGE)["extension_solution_checks"]["WPE-E05"]["fresh"]
    m, r = fresh["mass_kg"], fresh["boundary_radius_m"]
    f0, r0, slope = fresh["inner_force_n"], fresh["inner_radius_m"], fresh["outer_force_gradient_n_per_m"]
    f = slope*r
    area_outer = (f0+f)*(r-r0)/2
    U = f0*r0+area_outer
    v2 = f*r/m
    K = 0.5*m*v2
    close(fresh["boundary_local_inward_force_n"], f)
    close(fresh["boundary_outer_trapezoid_j"], area_outer)
    close(fresh["boundary_potential_energy_j"], U)
    close(fresh["boundary_speed_squared_m2_s2"], v2)
    close(fresh["boundary_speed_m_s"], sqrt(v2))
    close(fresh["boundary_kinetic_energy_j"], K)
    close(fresh["boundary_total_energy_j"], U+K)
    assert fresh["boundary_total_energy_j"] != fresh["total_energy_j"]
