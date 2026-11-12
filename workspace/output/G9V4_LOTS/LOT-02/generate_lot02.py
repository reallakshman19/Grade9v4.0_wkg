"""
LOT-02 Candidate Audit Generator (CP-4 Repaired)
Grade9 v4.0 - Batch A / Checkpoint 1 (CP-1)
Generates:
  - 5 x QUESTION_AUDIT.json (01 through 05) with stem_sha256 and source_record_digest
  - 5 x source_only/<idx>/SOURCE_ONLY.json (sealed packets for blind physics solve)
  - review/index.html (responsive review dashboard)
  - Copies ROSTER_PRIVATE.json for portable archive self-containment
"""

import os
import shutil
import json
import hashlib
from datetime import datetime, timezone

BASE_DIR = os.path.abspath("workspace/output/G9V4_LOTS/LOT-02")
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

# Copy ROSTER_PRIVATE.json into LOT-02 directory for portable self-contained archive
shutil.copyfile(ROSTER_SRC, os.path.join(BASE_DIR, "ROSTER_PRIVATE.json"))

# Exact registry stems
stems_data = json.load(open("workspace/output/G9V4_LOTS/BATCH-A/exact_registry_stems.json", encoding="utf-8"))

AUDIT_RECORDS = [
    {
        "sequence": 1,
        "task_identity": "Q-ID-01",
        "stable_id": "Q-PHY-WPE-JEEM-2026-04-06-S2-01",
        "source_id": "EX-M2",
        "lot": "LOT-02",
        "paper": "JEE Main 2026 (Online) 6th April Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M2"]["stem"],
        "stem_sha256": stems_data["EX-M2"]["sha256"],
        "source_hash": stems_data["EX-M2"]["sha256"],
        "source_record_digest": stems_data["EX-M2"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: 7.74", "B: 7.20", "C: 6.55", "D: 4.50"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1mo4fpv2y/9e0021cb-81a5-42b5-9355-64909243bdc1/33773fa0-3b33-11f1-8c42-c7a7a182458c/file-6y3zli1mo4fpv2z.webp?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "WORK_ENERGY_TWO_BODY_PULLEY",
            "assumed_parameters_from_coaching_figure": "Opposing suspended mass m = 2 kg, released from rest at height h = 6 m for M = 6 kg.",
            "derivation": "Conservation of mechanical energy for connected two-body system: Delta K = W_net => 1/2(M+m)v^2 = (M-m)gh => v = sqrt(2(M-m)gh / (M+m)) = sqrt(2(6-2)(10)(6)/(6+2)) = sqrt(480/8) = sqrt(60) approx 7.74596 m/s.",
            "predicted_option": "A: 7.74",
            "limiting_cases": "If m = M, v = 0 (equilibrium). If m = 0, v = sqrt(2gh) = sqrt(120) approx 10.95 m/s. Bound: 0 < 7.746 < 10.95 m/s."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Setting up the coupled two-body kinetic energy ledger where both bodies move at identical instantaneous speed v while one descends and the other ascends.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Standard coupled Atwood work-energy model."},
                    "representation_translation": {"score": 1, "evidence": "Interpreting pulley system schematic to assign mass parameters."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Combined kinetic energy and potential energy ledger to speed."},
                    "algebra_computational_load": {"score": 1, "evidence": "Square root approximation: sqrt(60) approx 7.74."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Must avoid treating 6 kg mass as unconstrained free fall."}
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
            "representation_requirements": ["DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Single body free fall v = sqrt(2gh) = sqrt(120) = 10.95 m/s", "status": "HYPOTHESIS"},
                {"route": "Omitting m in kinetic energy denominator v = sqrt(2(M-m)gh / M) = 8.94 m/s", "status": "HYPOTHESIS"}
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
            "HOLD:FIGURE_UNRESOLVED (opposing mass value m=2kg not in stem; unbound remote figure)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Secure local copy of NTA original PDF figure and master answer key sheet."
    },
    {
        "sequence": 2,
        "task_identity": "Q-ID-02",
        "stable_id": "Q-PHY-WPE-JEEM-2026-04-05-S2-02",
        "source_id": "EX-M4",
        "lot": "LOT-02",
        "paper": "JEE Main 2026 (Online) 5th April Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "VERIFIED_TEXT_ONLY",
        "stem_text": stems_data["EX-M4"]["stem"],
        "stem_sha256": stems_data["EX-M4"]["sha256"],
        "source_hash": stems_data["EX-M4"]["sha256"],
        "source_record_digest": stems_data["EX-M4"]["sha256"],
        "duplicate_parent": "PRIMARY_PARENT_OF_ALIAS:JEE-2026-04-05-S2-Q28",
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "VERIFIED_NONE_REQUIRED",
        "options": ["A: 20", "B: 25", "C: 30", "D: 10"],
        "unbound_remote_figures": [],
        "solve_exposure": "EXPOSED",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "STATIC_FRICTION_FRAME_TRANSLATION",
            "assumed_parameters_from_coaching_figure": "None required (pure text).",
            "derivation": "Block rests on incline at theta = 30 deg. Tangential gravity balance gives static friction f_s = mg sin(30 deg) = 1 * 10 * 0.5 = 5 N directed up the incline. The incline assembly translates vertically upward at constant v = 4 m/s for t = 2 s, so vertical displacement s_y = 4 * 2 = 8 m. Since acceleration a = 0, dynamic equilibrium holds and f_s remains 5 N up the incline. Incline angle is 30 deg to horizontal, so friction vector angle to vertical is 60 deg (or angle to horizontal is 30 deg). Vertical component of static friction f_s,y = f_s * sin(30 deg) = 5 * 0.5 = 2.5 N. Work done by friction W = f_s,y * s_y = 2.5 N * 8 m = 20 J.",
            "predicted_option": "A: 20",
            "limiting_cases": "If theta = 0 deg, f_s = 0 => W = 0 J. If theta -> 90 deg, normal force -> 0 (block falls). For theta = 30 deg, W = 20 J."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Recognizing that static friction can perform non-zero work in an inertial frame when the contact boundary translates, and projecting friction onto the displacement vector.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Equilibrium static friction and definition of work W = F . s."},
                    "representation_translation": {"score": 1, "evidence": "Resolving inclined vector into vertical motion coordinate."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Equilibrium force -> vertical component -> displacement dot product."},
                    "algebra_computational_load": {"score": 0, "evidence": "Direct arithmetic: 5 * 0.5 * 8 = 20 J."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Overcoming the pervasive misconception that static friction never does work."}
                },
                "total": 4,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["EXPLAIN"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["FREE_BODY_DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Claiming W = 0 because static friction does no work relative to the surface", "status": "HYPOTHESIS"},
                {"route": "Using full magnitude without projecting W = f_s * s = 5 * 8 = 40 J", "status": "HYPOTHESIS"},
                {"route": "Projecting using cos(30) instead of sin(30): W = 5 * cos(30) * 8 = 34.6 J", "status": "HYPOTHESIS"}
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
        "next_action": "Verify NTA master question paper and official answer key for 2026-04-05 S2."
    },
    {
        "sequence": 3,
        "task_identity": "Q-ID-03",
        "stable_id": "Q-PHY-WPE-JEEM-2026-01-23-S2-03",
        "source_id": "EX-M6",
        "lot": "LOT-02",
        "paper": "JEE Main 2026 (Online) 23rd January Evening Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M6"]["stem"],
        "stem_sha256": stems_data["EX-M6"]["sha256"],
        "source_hash": stems_data["EX-M6"]["sha256"],
        "source_record_digest": stems_data["EX-M6"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: 𝑡_𝑃<𝑡_𝑄", "B: 𝑡_𝑃=𝑡_𝑄", "C: 𝑡_𝑃>1.25𝑡_𝑄", "D: 𝑡_𝑃>𝑡_𝑄"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1ml8w2ix5/e5f6479c-ae49-4514-841d-fa273d0828c4/a21e2390-0241-11f1-88dd-c7214e4b90e3/file-6y3zli1ml8w2ix6.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "COMPARATIVE_TRAJECTORY_TIME_INTEGRAL",
            "assumed_parameters_from_coaching_figure": "Geometric configuration of S, C, ACB in vertical plane with downward gravity.",
            "derivation": "Bead Q traverses straight chord AB of length 2R with uniform horizontal velocity v: t_Q = 2R/v. Bead P traverses curved semi-circular wire ACB. Under gravity, as P descends below AB, mechanical energy conservation gives v_P(theta) = sqrt(v_0^2 + 2gy) > v. However, the path length is pi*R approx 3.14 R, whereas AB is 2R. Whether t_P < t_Q depends on the exact initial point S, the ratio v^2/(gR), and whether the horizontal velocity component remains greater than v throughout. In the coaching solution, t_P < t_Q (Option A) is asserted based on average horizontal speed enhancement, but without the exact figure and rigorous bound, the result cannot be conclusively certified.",
            "predicted_option": "A: 𝑡_𝑃<𝑡_𝑄 (coaching proposal)",
            "limiting_cases": "If g -> 0, path ACB is longer (pi*R > 2R) with constant speed v, so t_P = pi*R/v > 2R/v = t_Q. If g is very large, descent velocity becomes extremely high, driving t_P -> 0, so t_P < t_Q. Crossover depends sensitively on v^2/(gR)."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "JUSTIFY",
            "crux": "Analyzing the trade-off between increased path length along a circular arc versus increased speed from gravitational potential energy conversion.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Non-uniform circular dynamics under gravity vs uniform rectilinear kinematics."},
                    "representation_translation": {"score": 2, "evidence": "Spatial trajectory mapping, speed profile comparison, and integral time evaluation."},
                    "reasoning_chain_length": {"score": 2, "evidence": "Multi-step qualitative and quantitative trajectory integration analysis."},
                    "algebra_computational_load": {"score": 1, "evidence": "Inequality comparison of path integrals vs uniform velocity."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Common misconception that straight line always minimizes travel time (tautochrone/brachistochrone contrast)."}
                },
                "total": 8,
                "band": "D4"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["MODEL"],
                "candidate_cell": "QRT-JUSTIFY-D4",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "GRAPH", "EQUATION"],
            "independent_checks": ["LIMITING_CASE", "COUNTEREXAMPLE"],
            "wrong_route_hypotheses": [
                {"route": "Naive geometric path length comparison pi*R > 2R leading to t_P > t_Q", "status": "HYPOTHESIS"},
                {"route": "Assuming horizontal velocity component remains strictly v throughout circular motion", "status": "HYPOTHESIS"}
            ]
        },
        "qrt": "UNREVIEWED",
        "blueprint_fit": {
            "blueprint_id": BP_ID,
            "version": BP_VER,
            "sha256": BP_SHA,
            "cell": "QRT-JUSTIFY-D4"
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
            "HOLD:FIGURE_UNRESOLVED (diagram needed to verify location of S, C, orientation of track)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:B2_INDEPENDENT_PENDING (requires blind expert derivation of integral bound)"
        ],
        "next_action": "Source official NTA figure and assign blind B2 solve for limiting case verification."
    },
    {
        "sequence": 4,
        "task_identity": "Q-ID-04",
        "stable_id": "Q-PHY-WPE-JEEM-2026-01-23-S1-04",
        "source_id": "EX-M7",
        "lot": "LOT-02",
        "paper": "JEE Main 2026 (Online) 23rd January Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M7"]["stem"],
        "stem_sha256": stems_data["EX-M7"]["sha256"],
        "source_hash": stems_data["EX-M7"]["sha256"],
        "source_record_digest": stems_data["EX-M7"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: 3:4", "B: 1:4", "C: 2:3", "D: 1:2"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1mlutkti1/ec272730-93fd-443e-becd-35ed913d1e41/21c14490-0e51-11f1-97f7-91791681dff2/file-6y3zli1mlutkti2.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "PROJECTILE_ENERGY_DECOMPOSITION",
            "assumed_parameters_from_coaching_figure": "Figure identifies B as apex (maximum height) and C as impact ground point on launch level.",
            "derivation": "Initial launch KE at A: K_A = K = 1/2 m u^2. At apex B, vertical velocity is zero; speed is horizontal component v_B = u cos(60 deg) = u/2. Kinetic energy at B: K_B = 1/2 m (u/2)^2 = K/4. At ground impact C, speed is restored to u: K_C = K. Difference in KE between B and C: Delta K_BC = K_C - K_B = K - K/4 = 3/4 K. Ratio to KE at A: Delta K_BC / K_A = (3/4 K) / K = 3/4 = 3:4.",
            "predicted_option": "A: 3:4",
            "limiting_cases": "If launch angle theta = 0 deg, v_B = u => Delta K = 0. If theta = 90 deg, v_B = 0 => Delta K = K => ratio 1:1. For 60 deg, ratio is sin^2(60 deg) = 3/4."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Decomposing projectile kinetic energy into horizontal and vertical components to find apex energy retention K_B = K cos^2(theta).",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Standard 2D projectile kinetic energy model."},
                    "representation_translation": {"score": 1, "evidence": "Reading labeled trajectory points A, B, C from schematic."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Determine K_B, K_C, calculate difference, form ratio."},
                    "algebra_computational_load": {"score": 0, "evidence": "Elementary ratio: 1 - 1/4 = 3/4."},
                    "trap_exception_sensitivity": {"score": 0, "evidence": "Direct application without subtle boundary traps."}
                },
                "total": 3,
                "band": "D2"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["REPRESENT"],
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "representation_requirements": ["DIAGRAM", "EQUATION"],
            "independent_checks": ["UNITS", "LIMITING_CASE"],
            "wrong_route_hypotheses": [
                {"route": "Using vertical velocity component directly as ratio K_B/K_A = 1/4 (selecting B: 1:4)", "status": "HYPOTHESIS"},
                {"route": "Confusing cos(60) with sin(60) leading to ratio 1/4 or 1/2", "status": "HYPOTHESIS"}
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
            "HOLD:FIGURE_UNRESOLVED (points B and C defined on diagram, unbound remote URL)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Source official NTA figure to verify labels of B and C."
    },
    {
        "sequence": 5,
        "task_identity": "Q-ID-05",
        "stable_id": "Q-PHY-WPE-JEEM-2026-01-23-S1-05",
        "source_id": "EX-M8",
        "lot": "LOT-02",
        "paper": "JEE Main 2026 (Online) 23rd January Morning Shift",
        "source_type": "SCRAPED_EXTRACT_EXAMGOAL",
        "source_custody": "PARTIAL",
        "stem_text": stems_data["EX-M8"]["stem"],
        "stem_sha256": stems_data["EX-M8"]["sha256"],
        "source_hash": stems_data["EX-M8"]["sha256"],
        "source_record_digest": stems_data["EX-M8"]["sha256"],
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "options": ["A: 4𝐸", "B: 2𝐸", "C: (4)/(3)𝐸", "D: 3𝐸"],
        "unbound_remote_figures": [
            {
                "role": "stem",
                "url": "https://app-content.cdn.examgoal.net/fly/1000/image/6y3zli1ml8vt218/e17e76ef-50e7-40d1-8a90-305fa9cdbe3e/9aca7cc0-0240-11f1-88dd-c7214e4b90e3/file-6y3zli1ml8vt219.png?format=png"
            }
        ],
        "solve_exposure": "EXPOSED",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "SPRING_STATIC_EQUILIBRIUM_ENERGY",
            "assumed_parameters_from_coaching_figure": "Figure depicts two separate vertical suspensions from a rigid ceiling under gravity.",
            "derivation": "In vertical static equilibrium, spring tension equals suspended weight: k x = mg => x = mg / k. Elastic potential energy stored: U = 1/2 k x^2 = (mg)^2 / (2k). For spring A: m_A = 100 g, stiffness k_A => E_A = E = (m_A g)^2 / (2 k_A). For spring B: m_B = 200 g = 2 m_A, stiffness k_B = 4/3 k_A. Energy stored in B: E_B = (m_B g)^2 / (2 k_B) = (2 m_A g)^2 / (2 * (4/3) k_A) = (4 / (4/3)) * [ (m_A g)^2 / (2 k_A) ] = 3 E_A = 3E.",
            "predicted_option": "D: 3𝐸",
            "limiting_cases": "If m_B = m_A and k_B = k_A, E_B = E. If k_B -> infinity, E_B -> 0. With m ratio 2 and k ratio 4/3, factor is 2^2 / (4/3) = 3."
        },
        "sl2": {
            "mode": "QUESTION",
            "status": "UNREVIEWED",
            "decisive_operation": "APPLY",
            "crux": "Expressing elastic potential energy in terms of static gravitational force U = F^2 / (2k) to exploit scaling with mass squared and inverse spring constant.",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Hooke's law static equilibrium and elastic potential energy formula."},
                    "representation_translation": {"score": 1, "evidence": "Interpreting two separate vertical spring-mass assemblies."},
                    "reasoning_chain_length": {"score": 1, "evidence": "Equilibrium condition -> energy equation -> algebraic scaling ratio."},
                    "algebra_computational_load": {"score": 0, "evidence": "Simple fraction arithmetic: 4 / (4/3) = 3."},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Must avoid assuming identical extensions x or direct proportionality U proportional to k."}
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
                {"route": "Assuming equal extension x => E_B/E_A = k_B/k_A = 4/3 (Option C)", "status": "HYPOTHESIS"},
                {"route": "Linear mass scaling 2 / (4/3) = 1.5 E", "status": "HYPOTHESIS"},
                {"route": "Ignoring spring stiffness ratio => 4E (Option A)", "status": "HYPOTHESIS"}
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
            "HOLD:FIGURE_UNRESOLVED (diagram needed to verify separate suspension topology)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Source official NTA figure and verify master answer key."
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
    <title>Grade9 v4.0 — LOT-02 Source & Candidate Solve Audit (Questions 1–5)</title>
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
            <h1>Grade9 v4.0 — LOT-02 Audit: Candidates 1–5</h1>
            <div class="header-meta">
                <span><strong>Batch:</strong> BATCH-A / CP-1</span>
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
                <div class="metric-sub">Roster Seq 1–5 (100% accounted)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Academic Admissions</div>
                <div class="metric-val" style="color: var(--danger);">0</div>
                <div class="metric-sub">All gated on independent review</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Solve Status</div>
                <div class="metric-val">1 Derived / 4 Hold</div>
                <div class="metric-sub">Exposure: 5 EXPOSED (prior scrape)</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Cognitive Proposals</div>
                <div class="metric-val">4 D2 / 1 D4</div>
                <div class="metric-sub">All 5 SL2 factors scored</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Blueprint Fit</div>
                <div class="metric-val">4 Pending / 1 Pinned</div>
                <div class="metric-sub">QRT-JUSTIFY-D4 pinned for EX-M6</div>
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
    print("Writing LOT-02 files...")
    
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
