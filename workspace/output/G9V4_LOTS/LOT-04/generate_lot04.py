"""
LOT-04 Candidate Audit Generator (CP-4 Repaired)
Grade9 v4.0 - Batch A / Checkpoint 3 (CP-3)
Generates:
  - 5 x QUESTION_AUDIT.json (11 through 15) with exact registry stems and stem_sha256
  - 5 x source_only/<idx>/SOURCE_ONLY.json (sealed packets for blind physics solve)
  - review/index.html (responsive review dashboard)
  - Copies ROSTER_PRIVATE.json for portable archive self-containment
"""

import os
import shutil
import json
import hashlib
from datetime import datetime, timezone

BASE_DIR = os.path.abspath("workspace/output/G9V4_LOTS/LOT-04")
QUESTIONS_DIR = os.path.join(BASE_DIR, "questions")
SOURCE_ONLY_DIR = os.path.join(BASE_DIR, "source_only")
REVIEW_DIR = os.path.join(BASE_DIR, "review")

os.makedirs(QUESTIONS_DIR, exist_ok=True)
os.makedirs(SOURCE_ONLY_DIR, exist_ok=True)
os.makedirs(REVIEW_DIR, exist_ok=True)

BP_ID = "PHYS-QRT-BLUEPRINT"
BP_VER = "0.2.0"
BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"

ADAPTER_ID = "PHYS-TOPIC-WPE"
ADAPTER_VER = "0.1.0"
ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"

ROSTER_SRC = os.path.abspath("workspace/output/G9V4_LOTS/BATCH-A/ROSTER_PRIVATE.json")
with open(ROSTER_SRC, encoding="utf-8") as f:
    roster_json = json.load(f)
ROSTER_SHA = roster_json["roster_sha256"]

# Copy ROSTER_PRIVATE.json into LOT-04 directory for portable self-contained archive
shutil.copyfile(ROSTER_SRC, os.path.join(BASE_DIR, "ROSTER_PRIVATE.json"))

# Exact registry stems
stems_data = json.load(open("workspace/output/G9V4_LOTS/BATCH-A/exact_registry_stems.json", encoding="utf-8"))

AUDIT_RECORDS = [
    {
        "sequence": 11,
        "task_identity": "Q-ID-11",
        "stable_id": "Q-PHY-WPE-JEEM-2024-04-05-S2-11",
        "source_id": "EX-M29",
        "lot": "LOT-04",
        "paper": "JEE Main 2024 (Online) 5th April Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M29"]["stem"],
        "stem_sha256": stems_data["EX-M29"]["sha256"],
        "source_hash": stems_data["EX-M29"]["sha256"],
        "source_record_digest": stems_data["EX-M29"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: t2/3", "B: t3/2", "C: t", "D: t2"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "CONSTANT_POWER_DISPLACEMENT_INTEGRAL",
            "initial_condition_status": "PHYSICAL_CONDITION_TO_VERIFY (Initial rest v(0)=0 assumed for integration; not explicitly stated in stem).",
            "assumed_parameters_from_coaching_figure": "None required (pure text). Body assumed to start from rest at t=0.",
            "derivation": "Constant power P = F * v = m * v * (dv/dt) = constant. Separating variables: v dv = (P/m) dt. Integrating both sides: 1/2 v^2 = (P/m) t => v = sqrt(2P/m) * t^(1/2). Since v = ds/dt: ds = sqrt(2P/m) * t^(1/2) dt. Integrating from rest: s = sqrt(2P/m) * (2/3 t^(3/2)) => s proportional to t^(3/2).",
            "predicted_option": "B: t3/2",
            "limiting_cases": "If acceleration were constant (constant force), P = F*a*t proportional to t, and s proportional to t^2. Under constant power, acceleration decreases as v increases, yielding s proportional to t^(3/2), which is intermediate between t and t^2."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Setting up the differential relation for constant power P = m v (dv/dt) and integrating twice to find displacement time scaling s proportional to t^(3/2).",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Constant mechanical power model P = F v."},
                    "representation_translation": {"score": 1, "evidence": "Converting rate of work statement into differential equation."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Two-stage integration: v(t) -> s(t)."},
                    "algebra_computational_load": {"score": 1, "evidence": "Power rule integration: int t^(1/2) dt = 2/3 t^(3/2)."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Trap of confusing velocity scaling t^(1/2) with displacement, or assuming constant acceleration t^2."}
                },
                "total": 5,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Assuming constant acceleration s proportional to t^2 (Option D)", "status": "HYPOTHESIS"},
                {"route": "Taking velocity relation v proportional to t^(1/2) and inverting to t^(2/3) (Option A)", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Verify official NTA answer key for 2024-04-05 S2."
    },
    {
        "sequence": 12,
        "task_identity": "Q-ID-12",
        "stable_id": "Q-PHY-WPE-JEEM-2024-01-29-S2-12",
        "source_id": "EX-M36",
        "lot": "LOT-04",
        "paper": "JEE Main 2024 (Online) 29th January Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M36"]["stem"],
        "stem_sha256": stems_data["EX-M36"]["sha256"],
        "source_hash": stems_data["EX-M36"]["sha256"],
        "source_record_digest": stems_data["EX-M36"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: 5 : 1", "B: 3 : 2", "C: 1 : 5", "D: 2 : 5"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1lsg9qpea/62f3b2e1-f2c4-419e-a727-6e93b7cd3116/4fc6bf20-c82e-11ee-8c6b-bfa4f1fff66a/file-6y3zli1lsg9qpeb.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "VERTICAL_CIRCLE_CRITICAL_SPEED_ENERGY_RATIO",
            "assumed_parameters_from_coaching_figure": "String length L, vertical circle in gravity field g. Lowest point A, uppermost point B at height 2L.",
            "derivation": "Condition to just complete vertical circle: string tension at apex B must satisfy T_B >= 0 => m v_B^2 / L = mg => v_B = sqrt(gL). By conservation of mechanical energy between bottom A and top B: 1/2 m v_A^2 = 1/2 m v_B^2 + mg(2L) = 1/2 m (gL) + 2mgL = 5/2 mgL => v_A = sqrt(5gL). Ratio of kinetic energies: (K.E)_A / (K.E)_B = (1/2 m v_A^2) / (1/2 m v_B^2) = (5/2 mgL) / (1/2 mgL) = 5 / 1 = 5 : 1.",
            "predicted_option": "A: 5 : 1",
            "limiting_cases": "If B were at height L (reaching horizontal), v_A^2 = v_B^2 + 2gL => ratio depends on apex speed. For complete circle apex B, critical ratio is exactly 5 : 1."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Applying the vertical circular motion boundary condition T_B >= 0 to determine apex kinetic energy and using energy conservation over height 2L.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Vertical circular motion threshold dynamics and energy conservation."},
                    "representation_translation": {"score": 1, "evidence": "Interpreting vertical circle diagram geometry."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Threshold condition -> energy conservation -> kinetic energy ratio."},
                    "algebra_computational_load": {"score": 0, "evidence": "Elementary integer ratio: 5 / 1."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Must avoid assuming v_B = 0 at the top (which would cause string slackening)."}
                },
                "total": 4,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "FREE_BODY_DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Assuming speed at top is zero v_B = 0 => ratio undefined / infinite", "status": "HYPOTHESIS"},
                {"route": "Taking reciprocal ratio (K.E)_B / (K.E)_A = 1 : 5 (Option C)", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (diagram needed to verify labels A and B and string configuration)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Source official NTA figure asset and master answer key for 2024-01-29 S2."
    },
    {
        "sequence": 13,
        "task_identity": "Q-ID-13",
        "stable_id": "Q-PHY-WPE-JEEM-2022-07-29-S1-13",
        "source_id": "EX-M47",
        "lot": "LOT-04",
        "paper": "JEE Main 2022 (Online) 29th July Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M47"]["stem"],
        "stem_sha256": stems_data["EX-M47"]["sha256"],
        "source_hash": stems_data["EX-M47"]["sha256"],
        "source_record_digest": stems_data["EX-M47"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: Zero", "B: (𝐸)/(2)", "C: (𝐸)/(4)", "D: E"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "PROJECTILE_PEAK_KINETIC_ENERGY",
            "assumed_parameters_from_coaching_figure": "None required (pure text). Zero air resistance.",
            "derivation": "Initial launch kinetic energy: E = 1/2 m v^2. At the highest point of projectile flight, the vertical velocity component is zero (v_y = 0), while horizontal velocity remains constant: v_x = v * cos(60 deg) = v * (1/2) = v/2. Kinetic energy at peak: E' = 1/2 m (v_x)^2 = 1/2 m (v/2)^2 = 1/4 (1/2 m v^2) = E/4.",
            "predicted_option": "C: (𝐸)/(4)",
            "limiting_cases": "If projected vertically (90 deg), KE at peak is zero (Option A). If projected horizontally (0 deg), KE at peak is E (Option D). For 60 deg, KE is E * cos^2(60 deg) = E/4."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "RETRIEVE",
            "crux": "Retrieving the constancy of horizontal velocity in 2D projectile motion and squaring the cosine factor: E_peak = E cos^2(60 deg) = E/4.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 0, "evidence": "Standard parabolic trajectory velocity resolution."},
                    "representation_translation": {"score": 0, "evidence": "Direct symbolic manipulation."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Identify horizontal speed -> compute kinetic energy."},
                    "algebra_computational_load": {"score": 0, "evidence": "Cos(60 deg) = 1/2, (1/2)^2 = 1/4."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Prevalent beginner misconception that speed or kinetic energy is zero at highest point."}
                },
                "total": 2,
                "band": "D1"
            },
            "demand_proposal": {
                "primary": "RETRIEVE",
                "secondary": ["APPLY"],
                "candidate_cell": "QRT-RETRIEVE-D1",
                "status": "PROPOSED"
            },
            "representation_requirements": ["EQUATION"],
            "independent_checks": ["LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Selecting Zero (Option A) due to conflating peak vertical velocity with total velocity", "status": "HYPOTHESIS"},
                {"route": "Omitting the square: E * cos(60 deg) = E/2 (Option B)", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D1 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Verify NTA master answer key for 2022-07-29 S1."
    },
    {
        "sequence": 14,
        "task_identity": "Q-ID-14",
        "stable_id": "Q-PHY-WPE-JEEM-2022-07-27-S1-14",
        "source_id": "EX-M49",
        "lot": "LOT-04",
        "paper": "JEE Main 2022 (Online) 27th July Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M49"]["stem"],
        "stem_sha256": stems_data["EX-M49"]["sha256"],
        "source_hash": stems_data["EX-M49"]["sha256"],
        "source_record_digest": stems_data["EX-M49"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: 1.25 W", "B: 2.5 W", "C: 6.25 W", "D: 12.5 W"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "VARIABLE_MASS_BELT_POWER_NUMERICAL",
            "assumed_parameters_from_coaching_figure": "None required (pure text). Sand dropped from rest vertically.",
            "derivation": "Mass rate dm/dt = 0.5 kg/s, belt velocity v = 5 m/s. The horizontal force required to accelerate newly dropped sand to belt speed is F = v * (dm/dt) = 5 m/s * 0.5 kg/s = 2.5 N. The power supplied by the motor to maintain constant velocity is P = F * v = 2.5 N * 5 m/s = 12.5 W.",
            "predicted_option": "D: 12.5 W",
            "limiting_cases": "Rate of gain of kinetic energy of sand is d(KE)/dt = 1/2 (dm/dt) v^2 = 1/2 (0.5)(25) = 6.25 W. An equal amount of power (6.25 W) is dissipated as heat in friction as the sand slips on the belt. Total power input by the motor must be 6.25 + 6.25 = 12.5 W."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Applying variable-mass force relation F = v(dm/dt) to calculate required external motor power P = F*v = v^2(dm/dt), recognizing that mechanical power is twice the rate of kinetic energy increase.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Variable-mass mechanics applied to steady conveyor belt."},
                    "representation_translation": {"score": 0, "evidence": "Direct text numerical translation."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Force from mass flow -> power from F*v."},
                    "algebra_computational_load": {"score": 0, "evidence": "Direct arithmetic: 5 * 0.5 * 5 = 12.5 W."},
                    "trap_exception_sensitivity": {"score": 2, "evidence": "Severe attractor trap: computing d(1/2 m v^2)/dt = 6.25 W (Option C) by ignoring frictional heat dissipation."}
                },
                "total": 4,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["EQUATION"],
            "independent_checks": ["UNITS", "ENERGY_LEDGER"],
            "wrong_route_hypotheses": [
                {"route": "Calculating pure rate of KE gain d(KE)/dt = 1/2 v^2 dm/dt = 6.25 W (Option C)", "status": "HYPOTHESIS"},
                {"route": "Dividing force by velocity instead of multiplying: 2.5 / 5 = 0.5 W", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Verify NTA master answer key for 2022-07-27 S1."
    },
    {
        "sequence": 15,
        "task_identity": "Q-ID-15",
        "stable_id": "Q-PHY-WPE-JEEM-2022-07-26-S1-15",
        "source_id": "EX-M50",
        "lot": "LOT-04",
        "paper": "JEE Main 2022 (Online) 26th July Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M50"]["stem"],
        "stem_sha256": stems_data["EX-M50"]["sha256"],
        "source_hash": stems_data["EX-M50"]["sha256"],
        "source_record_digest": stems_data["EX-M50"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: (𝑣)/(2√(2))", "B: (𝑣)/(2)", "C: (𝑣)/(4)", "D: (𝑣)/(√2)"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/1l6hyjitw/5b480b82-4ccb-4844-a465-4ee34620c9bb/52950d40-158f-11ed-abd2-c5f8c222b719/file-1l6hyjitx.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "TWO_BODY_SPRING_CENTER_OF_MASS_ENERGY",
            "assumed_parameters_from_coaching_figure": "Two identical blocks m = 250 g = 0.25 kg connected by horizontal spring k = 2 N/m on frictionless horizontal plane.",
            "derivation": "Initial total momentum: P = m(-v) + m(+v) = 0. The center of mass is stationary. At maximum spring elongation x_m, relative speed between the two blocks is zero, so both blocks are instantaneously at rest relative to the center of mass (v_1 = v_2 = 0). By conservation of mechanical energy: Total Initial KE = Maximum Spring Elastic PE => 1/2 m v^2 + 1/2 m v^2 = 1/2 k x_m^2 => m v^2 = 1/2 k x_m^2 => x_m = sqrt(2 m v^2 / k) = v * sqrt(2m / k). Substituting m = 0.25 kg and k = 2 N/m: x_m = v * sqrt(2 * 0.25 / 2) = v * sqrt(0.25) = v * 0.5 = v / 2.",
            "predicted_option": "B: (𝑣)/(2)",
            "limiting_cases": "If k -> infinity (rigid rod), x_m -> 0. If only one block were given velocity v (total momentum mv), V_cm = v/2, and internal KE = 1/2 mu v^2 = 1/4 m v^2, yielding x_m = v/(2*sqrt(2)) (Option A). With equal and opposite velocities, all initial KE is converted into spring PE, yielding x_m = v/2."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Setting up the coupled two-block spring energy ledger in the zero-momentum center of mass frame where total kinetic energy m*v^2 fully transfers into spring potential 1/2 k x_m^2.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Two-body symmetric oscillator energy conservation."},
                    "representation_translation": {"score": 1, "evidence": "Interpreting spring-mass schematic and opposite velocity arrows."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Center of mass rest condition -> full KE to PE transfer -> solve x_m."},
                    "algebra_computational_load": {"score": 0, "evidence": "Elementary square root: sqrt(0.25) = 0.5."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Must avoid accounting for only one block's kinetic energy (which gives Option D: v/sqrt(2))."}
                },
                "total": 4,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Accounting for only single block KE: 1/2 m v^2 = 1/2 k x^2 => x = v*sqrt(m/k) = v/sqrt(8) = v/(2*sqrt(2)) (Option A)", "status": "HYPOTHESIS"},
                {"route": "Forgetting the 1/2 on spring PE: m v^2 = k x^2 => x = v*sqrt(m/k) = v/sqrt(8)", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (diagram needed to confirm initial velocity vectors and spring anchoring)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Source official NTA figure asset and master answer key for 2022-07-26 S1."
    }
]

def build_html_dashboard(records):
    rows_html = []
    for r in records:
        bp_cell = r["blueprint_fit"]
        if isinstance(bp_cell, dict):
            bp_disp = f"<strong>{bp_cell['blueprint_id']}</strong><br><small>{bp_cell['cell']}</small>"
        else:
            bp_disp = f"<span class='badge badge-hold'>{bp_cell}</span>"
        
        blockers_list = "".join(f"<li>{b}</li>" for b in r["blockers"])
        
        rows_html.append(f"""
        <tr>
            <td class="col-seq"><strong>#{r['sequence']}</strong><br><small class="mono">{r['task_identity']}</small></td>
            <td class="col-source">
                <strong>{r['source_id']}</strong><br>
                <small class="text-muted">{r['paper']}</small><br>
                <span class="badge badge-source">{r['source_custody']}</span>
                <span class="badge badge-fig">{r['figure_status']}</span>
            </td>
            <td class="col-stem">
                <div class="stem-preview">{r['stem_text'][:160]}...</div>
                <details class="candidate-details">
                    <summary>View Full Candidate Solve & Reasoning</summary>
                    <div class="solve-box">
                        <p><strong>Predicted Option:</strong> {r['candidate_solve']['predicted_option']}</p>
                        <p><strong>Method:</strong> <code>{r['candidate_solve']['method']}</code></p>
                        <p><strong>Derivation:</strong> {r['candidate_solve']['derivation']}</p>
                        <p><strong>Limiting Cases:</strong> {r['candidate_solve']['limiting_cases']}</p>
                    </div>
                </details>
            </td>
            <td class="col-cog">
                <strong>{r['sl2']['decisive_operation']}</strong> ({r['sl2']['difficulty_evidence']['band']})<br>
                <small>Score: {r['sl2']['difficulty_evidence']['total']}/10</small><br>
                <span class="badge badge-prop">{r['sl2']['demand_proposal']['status']}</span>
            </td>
            <td class="col-bp">{bp_disp}</td>
            <td class="col-gates">
                <span class="badge badge-admission">{r['academic_admission']}</span>
                <ul class="blocker-list">
                    {blockers_list}
                </ul>
            </td>
        </tr>
        """)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade9 v4.0 — LOT-04 Source & Candidate Solve Audit (Questions 11–15)</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --text: #0f172a;
            --text-muted: #64748b;
            --primary: #2563eb;
            --danger: #b91c1c;
            --warning: #d97706;
            --success: #15803d;
            --neutral-bg: #f1f5f9;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 16px;
            font-size: 14px;
            min-width: 0;
            overflow-x: hidden;
        }}
        .container {{
            max-width: 1365px;
            margin: 0 auto;
            background: var(--surface);
            border-radius: 8px;
            border: 1px solid var(--border);
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            min-width: 0;
        }}
        header {{
            border-bottom: 2px solid var(--border);
            padding-bottom: 16px;
            margin-bottom: 20px;
        }}
        h1 {{ font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 6px; word-break: break-word; }}
        .header-meta {{
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .notice-banner {{
            background: #fffbeb;
            border-left: 4px solid var(--warning);
            padding: 12px 16px;
            margin-bottom: 20px;
            border-radius: 0 4px 4px 0;
            font-size: 13px;
            color: #92400e;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: var(--neutral-bg);
            padding: 14px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }}
        .metric-title {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }}
        .metric-val {{ font-size: 22px; font-weight: 700; margin-top: 4px; }}
        .metric-sub {{ font-size: 11px; color: var(--text-muted); margin-top: 2px; }}

        .table-wrapper {{
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 24px;
            -webkit-overflow-scrolling: touch;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            min-width: 800px;
        }}
        th, td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }}
        th {{
            background: #f8fafc;
            font-weight: 600;
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        .col-seq {{ width: 80px; }}
        .col-source {{ width: 200px; word-break: break-word; }}
        .col-stem {{ min-width: 280px; word-break: break-word; }}
        .col-cog {{ width: 140px; }}
        .col-bp {{ width: 140px; word-break: break-word; }}
        .col-gates {{ width: 260px; word-break: break-word; }}

        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin: 2px 0;
            word-break: break-all;
        }}
        .badge-admission {{ background: #fef2f2; color: var(--danger); border: 1px solid #fecaca; }}
        .badge-hold {{ background: #fff7ed; color: var(--warning); border: 1px solid #fed7aa; }}
        .badge-source {{ background: #eff6ff; color: var(--primary); }}
        .badge-fig {{ background: #f1f5f9; color: var(--text-muted); }}
        .badge-prop {{ background: #f3e8ff; color: #7e22ce; }}

        .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        .text-muted {{ color: var(--text-muted); }}
        .stem-preview {{ font-size: 13px; margin-bottom: 6px; color: #334155; }}
        .candidate-details {{ margin-top: 6px; font-size: 12px; }}
        .candidate-details summary {{ cursor: pointer; color: var(--primary); font-weight: 600; }}
        .solve-box {{
            background: #f8fafc;
            border: 1px solid var(--border);
            padding: 8px 12px;
            border-radius: 4px;
            margin-top: 6px;
        }}
        .solve-box p {{ margin: 4px 0; }}
        .blocker-list {{
            margin-top: 4px;
            padding-left: 16px;
            font-size: 11px;
            color: var(--danger);
        }}
        .blocker-list li {{ margin-bottom: 2px; }}
        footer {{
            border-top: 1px solid var(--border);
            padding-top: 16px;
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 8px; }}
            .container {{ padding: 12px; }}
            .metrics-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Grade9 v4.0 — LOT-04 Audit: Candidates 11–15</h1>
            <div class="header-meta">
                <span><strong>Batch:</strong> BATCH-A / CP-3</span>
                <span><strong>Scope:</strong> Physics / WPE</span>
                <span><strong>Audit Date:</strong> 2026-11-01</span>
                <span><strong>Roster SHA:</strong> <code class="mono">{ROSTER_SHA[:16]}...</code></span>
            </div>
        </header>

        <div class="notice-banner">
            <strong>Mandatory Governance Boundary:</strong> ZERO academic approvals inferred. All 5 candidates are marked <code>NOT_ADMITTED</code>. No learner cards constructed. Official answer keys and NTA source figures remain on HOLD.
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Candidates Audited</div>
                <div class="metric-val">5 / 5</div>
                <div class="metric-sub">Roster Seq 11–15 (100% accounted)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Academic Admissions</div>
                <div class="metric-val" style="color: var(--danger);">0</div>
                <div class="metric-sub">All gated on independent review</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Solve Status</div>
                <div class="metric-val">3 Derived / 2 Hold</div>
                <div class="metric-sub">Exposure: 5 EXPOSED (prior scrape)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Cognitive Proposals</div>
                <div class="metric-val">1 D1 / 4 D2</div>
                <div class="metric-sub">All 5 SL2 factors scored</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Blueprint Fit</div>
                <div class="metric-val">5 Pending (D1/D2)</div>
                <div class="metric-sub">Common teaching spec pending</div>
            </div>
        </div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th class="col-seq">Seq</th>
                        <th class="col-source">Source & Custody</th>
                        <th class="col-stem">Stem & Candidate Solve</th>
                        <th class="col-cog">SL2 Proposal</th>
                        <th class="col-bp">Blueprint / Adapter</th>
                        <th class="col-gates">Academic Gate & Blockers</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>

        <footer>
            <div>Produced by Local Coding Agent | Low-Discretion Autonomous Mode</div>
            <div>No academic approval inferred from software validation.</div>
        </footer>
    </div>
</body>
</html>
"""
    return html_content

def main():
    print("Writing LOT-04 files...")
    
    # 1. QUESTION_AUDIT.json and source-only sealed packets
    for r in AUDIT_RECORDS:
        idx_str = f"{r['sequence']:02d}"
        q_dir = os.path.join(QUESTIONS_DIR, idx_str)
        os.makedirs(q_dir, exist_ok=True)
        q_path = os.path.join(q_dir, "QUESTION_AUDIT.json")
        with open(q_path, "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2)
            
        # Source-only packet
        so_dir = os.path.join(SOURCE_ONLY_DIR, idx_str)
        os.makedirs(so_dir, exist_ok=True)
        so_path = os.path.join(so_dir, "SOURCE_ONLY.json")
        so_data = {
            "source_id": r["source_id"],
            "task_identity": r["task_identity"],
            "sequence": r["sequence"],
            "paper": r["paper"],
            "stem_text": r["stem_text"],
            "stem_sha256": r["stem_sha256"],
            "options": r["options"],
            "figure_reference": r["unbound_remote_figures"][0]["url"] if r["unbound_remote_figures"] else "NONE",
            "confidentiality_notice": "SEALED SOURCE-ONLY PACKET FOR BLIND INDEPENDENT REVIEW. Contains NO answers, keys, explanations, candidate solutions, SL2 factor scores, or prior review commentary."
        }
        with open(so_path, "w", encoding="utf-8") as f:
            json.dump(so_data, f, indent=2)

    # 2. review/index.html
    html_content = build_html_dashboard(AUDIT_RECORDS)
    index_path = os.path.join(REVIEW_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("  Generated audits, sealed packets, and dashboard.")

if __name__ == "__main__":
    main()
