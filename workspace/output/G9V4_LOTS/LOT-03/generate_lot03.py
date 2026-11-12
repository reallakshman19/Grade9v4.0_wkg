"""
LOT-03 Candidate Audit Generator (CP-4 Repaired)
Grade9 v4.0 - Batch A / Checkpoint 2 (CP-2)
Generates:
  - 5 x QUESTION_AUDIT.json (06 through 10) with exact registry stems and stem_sha256
  - 5 x source_only/<idx>/SOURCE_ONLY.json (sealed packets for blind physics solve)
  - review/index.html (responsive review dashboard with SOURCE_FIDELITY_REPAIR alert for EX-M18)
  - Copies ROSTER_PRIVATE.json for portable archive self-containment
"""

import os
import shutil
import json
import hashlib
from datetime import datetime, timezone

BASE_DIR = os.path.abspath("workspace/output/G9V4_LOTS/LOT-03")
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

# Copy ROSTER_PRIVATE.json into LOT-03 directory for portable self-contained archive
shutil.copyfile(ROSTER_SRC, os.path.join(BASE_DIR, "ROSTER_PRIVATE.json"))

# Exact registry stems
stems_data = json.load(open("workspace/output/G9V4_LOTS/BATCH-A/exact_registry_stems.json", encoding="utf-8"))

AUDIT_RECORDS = [
    {
        "sequence": 6,
        "task_identity": "Q-ID-06",
        "stable_id": "Q-PHY-WPE-JEEM-2026-01-21-S1-06",
        "source_id": "EX-M11",
        "lot": "LOT-03",
        "paper": "JEE Main 2026 (Online) 21st January Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M11"]["stem"],
        "stem_sha256": stems_data["EX-M11"]["sha256"],
        "source_hash": stems_data["EX-M11"]["sha256"],
        "source_record_digest": stems_data["EX-M11"]["sha256"],
        "interpretation": "Rank force magnitudes |F| = |-dV/dx| from highest to lowest across regions AB, BC, CD, DE based on graph slopes.",
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": [
            "A: 𝐹_𝐵𝐶>𝐹_𝐴𝐵>𝐹_𝐷𝐸>𝐹_𝐶𝐷",
            "B: 𝐹_𝐵𝐶>𝐹_𝐶𝐷>𝐹_𝐷𝐸>𝐹_𝐴𝐵",
            "C: 𝐹_𝐶𝐷>𝐹_𝐴𝐵>𝐹_𝐵𝐶>𝐹_𝐷𝐸",
            "D: 𝐹_𝐶𝐷>𝐹_𝐷𝐸>𝐹_𝐴𝐵>𝐹_𝐵𝐶"
        ],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1ml8b57ie/549f4be0-42f3-4404-b29b-42ccf8e0d8a7/cd04ee60-01ef-11f1-bb8c-db351d97a854/file-6y3zli1ml8b57if.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "POTENTIAL_GRADIENT_SLOPE_RANKING",
            "assumed_parameters_from_coaching_figure": "V(x) piece-wise linear segments: AB from (0,0) to (1,1); BC from (1,1) to (2,4); CD from (2,4) to (4,4); DE from (4,4) to (6,3).",
            "derivation": "Conservative force magnitude is given by |F| = |-dV/dx| = |slope|. Slope_AB = (1-0)/(1-0) = 1 => |F_AB| = 1. Slope_BC = (4-1)/(2-1) = 3 => |F_BC| = 3. Slope_CD = (4-4)/(4-2) = 0 => |F_CD| = 0. Slope_DE = (3-4)/(6-4) = -0.5 => |F_DE| = 0.5. Descending rank: |F_BC| (3) > |F_AB| (1) > |F_DE| (0.5) > |F_CD| (0).",
            "predicted_option": "A: 𝐹_𝐵𝐶>𝐹_𝐴𝐵>𝐹_𝐷𝐸>𝐹_𝐶𝐷",
            "limiting_cases": "Flat region CD has zero slope, hence minimum force (0). Steeper segment BC has maximum slope (3). Rank order is strictly determined by geometric steepness."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "REPRESENT",
            "crux": "Translating graph slopes of potential energy V(x) to conservative force magnitudes |F| = |dV/dx| and ordering piecewise segments.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Connection between conservative force and potential gradient."},
                    "representation_translation": {"score": 1, "evidence": "Extracting coordinates and calculating slopes from piecewise graph."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Calculate four segment slopes and order descendingly."},
                    "algebra_computational_load": {"score": 0, "evidence": "Elementary slope ratios: 3, 1, 0.5, 0."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Magnitude requested, so negative slope in DE becomes positive 0.5, exceeding flat CD."}
                },
                "total": 4,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "REPRESENT",
                "secondary": ["APPLY"],
                "candidate_cell": "QRT-REPRESENT-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["GRAPH", "EQUATION"],
            "independent_checks": ["SIGN", "ROUND_TRIP"],
            "wrong_route_hypotheses": [
                {"route": "Confusing force magnitude with potential energy value (ranking by V instead of slope)", "status": "HYPOTHESIS"},
                {"route": "Retaining negative sign for DE slope (-0.5 < 0) placing DE below CD", "status": "HYPOTHESIS"}
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
            "HOLD:FIGURE_UNRESOLVED (graph coordinates and segment labels require local verified asset)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Secure official NTA exam graph asset and verify master answer key."
    },
    {
        "sequence": 7,
        "task_identity": "Q-ID-07",
        "stable_id": "Q-PHY-WPE-JEEM-2025-04-04-S2-07",
        "source_id": "EX-M14",
        "lot": "LOT-03",
        "paper": "JEE Main 2025 (Online) 4th April Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M14"]["stem"],
        "stem_sha256": stems_data["EX-M14"]["sha256"],
        "source_hash": stems_data["EX-M14"]["sha256"],
        "source_record_digest": stems_data["EX-M14"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: 490 J", "B: 970 J", "C: 735 J", "D: 245 J"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "WORK_EXT_DYNAMIC_EQUILIBRIUM",
            "gravity_value_status": "PAPER_CONVENTION_TO_VERIFY (g = 9.8 m/s^2 imported by coaching solution; not explicitly stated in stem).",
            "assumed_parameters_from_coaching_figure": "None required (pure text). g = 9.8 m/s^2 taken as convention.",
            "derivation": "Let pulling force be F at 45 deg above horizontal. Vertical equilibrium: N + F sin(45 deg) = mg => N = mg - F/sqrt(2). Friction force f_k = mu * N = mu * (mg - F/sqrt(2)). Uniform velocity implies zero acceleration: F cos(45 deg) = f_k => F/sqrt(2) = mu * [mg - F/sqrt(2)] => F/sqrt(2) * (1 + mu) = mu * mg. With m = 25 kg, g = 9.8 m/s^2, mu = 0.25: F/sqrt(2) * (1.25) = 0.25 * (25 * 9.8) = 61.25 => F/sqrt(2) = 61.25 / 1.25 = 49 N. Work done by applied force over displacement s = 5 m: W = F * s * cos(45 deg) = (F/sqrt(2)) * s = 49 N * 5 m = 245 J.",
            "predicted_option": "D: 245 J",
            "limiting_cases": "If mu = 0, F = 0 => W = 0 J. If s = 0, W = 0 J. Direct energy balance: work by applied force equals thermal dissipation by kinetic friction over 5 m: W = f_k * s = 49 * 5 = 245 J."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Incorporating the vertical component of the pulling force into the normal reaction reduction and calculating work done at uniform velocity.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Dynamic equilibrium with inclined pulling force and friction."},
                    "representation_translation": {"score": 1, "evidence": "Translating force balance along two orthogonal axes."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Normal force -> friction -> pulling force -> work calculation."},
                    "algebra_computational_load": {"score": 1, "evidence": "Linear equation with decimals: 61.25 / 1.25 = 49, 49 * 5 = 245."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Trap of setting N = mg without subtracting vertical component of pull."}
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
            "representation_requirements": ["FREE_BODY_DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE", "ENERGY_LEDGER"],
            "wrong_route_hypotheses": [
                {"route": "Using unreduced normal force N = mg = 245 N => f_k = 61.25 N => W = 61.25 * 5 / cos(45) or 306 J", "status": "HYPOTHESIS"},
                {"route": "Omitting cos(45) in work computation W = F * s = 49 * sqrt(2) * 5 = 346 J", "status": "HYPOTHESIS"}
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
        "next_action": "Verify NTA master question paper and official answer key for 2025-04-04 S2."
    },
    {
        "sequence": 8,
        "task_identity": "Q-ID-08",
        "stable_id": "Q-PHY-WPE-JEEM-2025-01-29-S2-08",
        "source_id": "EX-M16",
        "lot": "LOT-03",
        "paper": "JEE Main 2025 (Online) 29th January Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M16"]["stem"],
        "stem_sha256": stems_data["EX-M16"]["sha256"],
        "source_hash": stems_data["EX-M16"]["sha256"],
        "source_record_digest": stems_data["EX-M16"]["sha256"],
        "next_scope_recommendation": "PROPOSED_NEXT_TEXT_ONLY_D3_CANDIDATE: Recommended for next scoping decision by Owner. Requires independent blind physics solve and NTA official key verification before any Core2 authoring.",
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: P ∝√(𝑣)", "B: P ∝𝑣", "C: 𝑃^(2)∝𝑣^(3)", "D: 𝑃^(2)∝𝑣^(5)"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "VARIABLE_MASS_BELT_POWER_PROPORTIONALITY",
            "assumed_parameters_from_coaching_figure": "None required (pure text). Constant speed v, sand dropped from rest relative to ground.",
            "derivation": "Rate of mass addition: dm/dt = k * v^(1/2). To maintain constant speed v, the force required to accelerate newly dropped sand from rest to speed v is F = v * (dm/dt) = v * (k * v^(1/2)) = k * v^(3/2). Total power delivered to the belt: P = F * v = (k * v^(3/2)) * v = k * v^(5/2). Squaring both sides to eliminate fractional powers: P^2 = k^2 * v^5, which implies P^2 proportional to v^5.",
            "predicted_option": "D: 𝑃^(2)∝𝑣^(5)",
            "limiting_cases": "If dm/dt were constant (independent of v), P = v^2 (dm/dt) => P proportional to v^2 => P^2 proportional to v^4. With dm/dt proportional to v^(1/2), P proportional to v^(5/2) => P^2 proportional to v^5."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "MODEL",
            "crux": "Modeling variable-mass thrust F = v(dm/dt) and input power P = F*v = v^2(dm/dt) under velocity-dependent mass flux dm/dt proportional to v^(1/2).",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Variable-mass dynamics and continuous conveyor belt mechanical power."},
                    "representation_translation": {"score": 1, "evidence": "Converting proportionality statement to power scaling law."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Force formulation -> power multiplication -> squaring operation."},
                    "algebra_computational_load": {"score": 1, "evidence": "Index laws: v * v^(1/2) * v = v^(5/2), (v^(5/2))^2 = v^5."},
                    "trap_exception_sensitivity": {"score": 2, "evidence": "Critical trap: confusing rate of KE increase (1/2 v^2 dm/dt) with motor power input (v^2 dm/dt)."}
                },
                "total": 7,
                "band": "D3"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "candidate_cell": "QRT-MODEL-D3",
                "status": "PROPOSED"
            },
            "representation_requirements": ["EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Using rate of change of KE: P = d(1/2 m v^2)/dt = 1/2 v^2 (dm/dt) = 1/2 k v^(5/2) (gives same power scaling, but conceptually flawed by missing inelastic dissipation)", "status": "HYPOTHESIS"},
                {"route": "Setting F = (dm/dt) => P = F*v = v^(3/2) => P^2 proportional to v^3 (Option C)", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": {
            "blueprint_id": BP_ID,
            "version": BP_VER,
            "sha256": BP_SHA,
            "cell": "QRT-MODEL-D3"
        },
        "adapter_fit": {
            "adapter_id": ADAPTER_ID,
            "version": ADAPTER_VER,
            "sha256": ADAPTER_SHA,
            "topic": "WPE"
        },
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:B2_INDEPENDENT_PENDING (requires independent confirmation of variable-mass power model)"
        ],
        "next_action": "Verify official NTA key and submit source-only packet for B2 blind solve."
    },
    {
        "sequence": 9,
        "task_identity": "Q-ID-09",
        "stable_id": "Q-PHY-WPE-JEEM-2025-01-28-S1-09",
        "source_id": "EX-M18",
        "lot": "LOT-03",
        "paper": "JEE Main 2025 (Online) 28th January Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M18"]["stem"],
        "stem_sha256": stems_data["EX-M18"]["sha256"],
        "source_hash": stems_data["EX-M18"]["sha256"],
        "source_record_digest": stems_data["EX-M18"]["sha256"],
        "source_fidelity_repair_note": "SOURCE_FIDELITY_REPAIR: Stem text restored verbatim from registry.json. Previous scrape inverted spring anchor to top and corrupted geometry. Original geometry: spring (k, unstretched length R) attached to bottom of vertical circular hoop (radius R). Bead released from top (y1 = 2R, spring length 2R, extension x1 = R). Bead moves until spring length becomes R (forming an equilateral triangle with bottom anchor and circle center; central angle 60 deg from vertical bottom, height y2 = R - R cos(60 deg) = R/2, drop Delta h = 3R/2). Spring relaxes to extension x2 = 0. Potential energy loss: Delta U_grav = mg(3R/2) and Delta U_spring = 1/2 k R^2. By energy conservation: 1/2 m v^2 = 3/2 mgR + 1/2 k R^2 => v^2 = 3gR + k R^2 / m => v = sqrt(3gR + k R^2 / m) [Option B]. Preserved on HOLD awaiting verified official diagram asset and key.",
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": [
            "A: √(2𝑅𝑔+(kR2)/(m))",
            "B: √(3Rg+(kR2)/(m))",
            "C: √(2Rg+(4kR^(2))/(m))",
            "D: 2√(gR+(kR2)/(m))"
        ],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/jaoe38c1m6vv01hf/d6172690-de16-4d80-a7c2-533f6e78297f/3c278440-e5ec-11ef-ac74-491aa7357b34/file-jaoe38c1m6vv01hg.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "CIRCULAR_HOOP_BOTTOM_SPRING_GRAVITY_ENERGY",
            "reviewer_exposure_status": "EXPOSED_REFERENCE_SOLVE (Reviewer exposure has occurred; this is an exposed reference solve, NOT an independent blind solution).",
            "assumed_parameters_from_coaching_figure": "Bead on vertical circular hoop (radius R). Spring (stiffness k, unstretched length R) attached to bottom of hoop. Bead released from top.",
            "derivation": "Initial state (top of hoop): y1 = 2R, spring length = 2R, extension x1 = 2R - R = R, v1 = 0. Final state (length of spring becomes R): spring anchor at bottom (0,0), hoop center at (0,R), bead at P on circle. Since distance from bottom to P is R, and from center to P is R, triangle formed by bottom anchor, center, and P is equilateral with side R. The angle at center from downward vertical is 60 deg. Height of P: y2 = R - R cos(60 deg) = R - R/2 = R/2. Height drop: Delta h = y1 - y2 = 2R - R/2 = 3R/2. Final spring extension x2 = R - R = 0 (spring is unstretched). Energy conservation: 1/2 m v^2 = mg(Delta h) + 1/2 k x1^2 - 1/2 k x2^2 = mg(3R/2) + 1/2 k R^2 - 0 = 3/2 mgR + 1/2 k R^2. Multiplying by 2/m: v^2 = 3gR + (k R^2 / m) => v = sqrt(3gR + (k R^2 / m)).",
            "predicted_option": "B: √(3Rg+(kR2)/(m))",
            "limiting_cases": "If k = 0 (pure gravity), v = sqrt(2 g Delta h) = sqrt(2 g * 3R/2) = sqrt(3gR). If g = 0 (pure spring), v = sqrt(k R^2 / m). Both conservative forces lose potential energy simultaneously, yielding Option B."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "MODEL",
            "crux": "Modeling the simultaneous relaxation of an extended bottom-anchored spring and gravitational descent on a circular constraint using equilateral triangle geometry.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Simultaneous conservative potential energies (gravity + bottom Hookean spring) on circular constraint."},
                    "representation_translation": {"score": 2, "evidence": "Geometric resolution of equilateral triangle to find angle (60 deg) and height drop (3R/2)."},
                    "reasoning_chain_length": {"score": 2, "evidence": "Initial geometry -> final geometry -> energy conservation -> velocity solution."},
                    "algebra_computational_load": {"score": 1, "evidence": "Quadratic expression and square root formatting."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Equilibrium length is R, so elongation at top is 2R - R = R, not 2R; spring relaxes to zero elongation."}
                },
                "total": 8,
                "band": "D4"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "candidate_cell": "QRT-MODEL-D4",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Using top spring anchor which leads to energy subtraction or sign contradiction", "status": "HYPOTHESIS"},
                {"route": "Using Delta h = 2R instead of 3/2 R leading to Option D", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": {
            "blueprint_id": BP_ID,
            "version": BP_VER,
            "sha256": BP_SHA,
            "cell": "QRT-MODEL-D4"
        },
        "adapter_fit": {
            "adapter_id": ADAPTER_ID,
            "version": ADAPTER_VER,
            "sha256": ADAPTER_SHA,
            "topic": "WPE"
        },
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (diagram needed to verify exact location and angle of position A)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:B2_INDEPENDENT_PENDING (requires verified authentic diagram before candidate solve can be qualified)"
        ],
        "next_action": "Source official NTA figure asset and assign B2 unexposed solve."
    },
    {
        "sequence": 10,
        "task_identity": "Q-ID-10",
        "stable_id": "Q-PHY-WPE-JEEM-2024-04-08-S2-10",
        "source_id": "EX-M24",
        "lot": "LOT-03",
        "paper": "JEE Main 2024 (Online) 8th April Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M24"]["stem"],
        "stem_sha256": stems_data["EX-M24"]["sha256"],
        "source_hash": stems_data["EX-M24"]["sha256"],
        "source_record_digest": stems_data["EX-M24"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: √(6)m", "B: √(5)m", "C: 1m", "D: 2m"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/1lv3g4i1f/1efcf294-a9a1-4376-836b-324bcbe1c57f/bbe3ea30-fc85-11ee-97a5-e951feb71c60/file-1lv3g4i1g.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "WORK_ENERGY_THEOREM_INCLINE_SPRING_FRICTION",
            "assumed_parameters_from_coaching_figure": "All parameters (m=5 kg, h=5 m, mu=0.5, k=100 N/m or equivalent) are embedded inside figure, completely absent from text stem.",
            "derivation": "Work-energy theorem between release point and maximum compression x: W_grav + W_fric + W_spring = Delta K = 0. From coaching extract calculation: W_grav = 5 * 10 * 5 = 250 J; W_fric = -0.5 * 5 * 10 * x = -25x; W_spring = -1/2 * k * x^2 = -50 x^2 (assuming k=100 N/m). Equation: 250 - 25x - 50x^2 = 0 => 50x^2 + 25x - 250 = 0 => 2x^2 + x - 10 = 0 => (2x + 5)(x - 2) = 0 => x = 2 m.",
            "predicted_option": "D: 2m",
            "limiting_cases": "If mu = 0, 50x^2 = 250 => x^2 = 5 => x = sqrt(5) m (Option B). With friction present, energy is dissipated, leading to quadratic equation root x = 2 m."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Formulating the complete work-energy equation incorporating gravitational potential loss, non-conservative frictional dissipation, and spring potential gain to solve a quadratic in spring compression x.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Work-energy theorem combining conservative and dissipative mechanisms on an incline."},
                    "representation_translation": {"score": 2, "evidence": "Crucial requirement: entire problem parameter set resides in the diagram."},
                    "reasoning_chain_length": {"score": 2, "evidence": "Identify forces -> integrate over path (d + x) -> formulate quadratic -> physical root."},
                    "algebra_computational_load": {"score": 1, "evidence": "Factoring quadratic: 2x^2 + x - 10 = 0 => x = 2."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Frictional dissipation occurs along entire sliding distance including spring compression x."}
                },
                "total": 8,
                "band": "D4"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-APPLY-D4",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "FREE_BODY_DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Ignoring friction dissipation entirely: 1/2 k x^2 = mgh => x = sqrt(5) m (Option B)", "status": "HYPOTHESIS"},
                {"route": "Ignoring spring compression in friction path: W_fric = mu mg cos(theta) * d", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": {
            "blueprint_id": BP_ID,
            "version": BP_VER,
            "sha256": BP_SHA,
            "cell": "QRT-APPLY-D4"
        },
        "adapter_fit": {
            "adapter_id": ADAPTER_ID,
            "version": ADAPTER_VER,
            "sha256": ADAPTER_SHA,
            "topic": "WPE"
        },
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_REVIEW",
        "b2_blind_status": "NOT_RUN",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (stem is entirely incomplete without diagram containing all numerical parameters)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:B2_INDEPENDENT_PENDING (requires verified diagram before candidate solve can be qualified)"
        ],
        "next_action": "Source official NTA original diagram asset for JEE Main 2024-04-08 S2."
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
        
        fidelity_alert = ""
        if "source_fidelity_repair_note" in r:
            fidelity_alert = f"<div class='repair-alert'><strong>SOURCE FIDELITY REPAIR:</strong> {r['source_fidelity_repair_note']}</div>"
            
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
                {fidelity_alert}
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
    <title>Grade9 v4.0 — LOT-03 Source & Candidate Solve Audit (Questions 6–10)</title>
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
        .repair-alert {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: var(--danger);
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 11px;
            margin: 6px 0;
            word-break: break-word;
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
            <h1>Grade9 v4.0 — LOT-03 Audit: Candidates 6–10</h1>
            <div class="header-meta">
                <span><strong>Batch:</strong> BATCH-A / CP-2</span>
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
                <div class="metric-sub">Roster Seq 6–10 (100% accounted)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Academic Admissions</div>
                <div class="metric-val" style="color: var(--danger);">0</div>
                <div class="metric-sub">All gated on independent review</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Solve Status</div>
                <div class="metric-val">2 Derived / 3 Hold</div>
                <div class="metric-sub">Exposure: 5 EXPOSED (prior scrape)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Cognitive Proposals</div>
                <div class="metric-val">2 D2 / 1 D3 / 2 D4</div>
                <div class="metric-sub">All 5 SL2 factors scored</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Blueprint Fit</div>
                <div class="metric-val">2 Pending / 3 Pinned</div>
                <div class="metric-sub">D3/D4 pinned to PHYS-QRT-BLUEPRINT</div>
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
    print("Writing LOT-03 files...")
    
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
