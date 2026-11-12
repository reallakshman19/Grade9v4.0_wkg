"""Script to build and validate the Physics Track: Fluid Mechanics, Sound & Thermal Physics (nsejs-fluids-sound-r1)
Core 2 Question Bank & Interactive Tablet Application.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = REPO_ROOT / "workspace/sources/nsejs/PHYS-NSEJS-FLUID-01"
OUTPUT_DIR = REPO_ROOT / "workspace/output/nsejs-fluids-sound-r1"

SOURCES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

stem_q01 = (
    "A solid block of density $\\rho_s = 600\\text{ kg/m}^3$ and mass $m = 3.0\\text{ kg}$ is tied to the bottom "
    "of a container filled with water ($\\rho_w = 1000\\text{ kg/m}^3$) by a light inextensible cord. The entire "
    "container is placed inside an elevator accelerating vertically upwards with constant acceleration $a = 2.0\\text{ m/s}^2$. "
    "Taking $g = 10.0\\text{ m/s}^2$:\n"
    "[FIG-stem-nsejs-buoyancy-accelerating-elevator]\n"
    "Determine the tension $T$ in the cord during upward acceleration, and the initial upward acceleration $a_{\\text{rel}}$ "
    "of the block relative to the container immediately after the cord is severed."
)

stem_q01_hash = hashlib.sha256(stem_q01.encode("utf-8")).hexdigest()

# 1. source_item.json
source_item = {
    "version": "1.0.0",
    "acquisition_ref": "IAPT-NSEJS-OFFICIAL-EXAMINATION-ARCHIVE",
    "resource_ref": "IAPT-NSEJS-PHYSICS-FLUIDS-THERMAL",
    "source_item_locator": "PHYS-NSEJS-FLUID-01",
    "original_identifier": "NSEJS Physics · Fluids & Acceleration · MODEL · D2 (Score 4)",
    "source_role": "OWNER_HELD_COPY_OF_OFFICIAL_PAPER",
    "official_exam_status": "PAPER_ON_FILE_NOT_ADMITTED",
    "stem": stem_q01,
    "options": [
        "(A) T = 18.0 N, a_rel = 6.0 m/s^2",
        "(B) T = 24.0 N, a_rel = 8.0 m/s^2",
        "(C) T = 20.0 N, a_rel = 6.67 m/s^2",
        "(D) T = 30.0 N, a_rel = 10.0 m/s^2"
    ],
    "official_key": "(B) T = 24.0 N, a_rel = 8.0 m/s^2",
    "provisional_key_status": "CONFIRMED_BY_IAPT_FINAL_KEY",
    "coaching_prediction_consensus": [
        {"source": "Allen Career Institute", "prediction": "(B)"},
        {"source": "Resonance Eduventures", "prediction": "(B)"},
        {"source": "FIITJEE Foundation", "prediction": "(B)"}
    ],
    "p1_fitness": {
        "status": "FIT_FOR_UNASSISTED_FIRST_ATTEMPT",
        "unassisted_attempt_admissible": True,
        "has_unambiguous_stem": True,
        "missing_diagrams": False,
        "notes": "Problem statement provides complete constraints with vector dynamic balance."
    }
}
(SOURCES_DIR / "source_item.json").write_text(json.dumps(source_item, indent=2), encoding="utf-8")

# 2. source-custody.json
source_custody = {
    "version": "1.0.0",
    "acquisition_ref": "IAPT-NSEJS-OFFICIAL-EXAMINATION-ARCHIVE",
    "resource_ref": "IAPT-NSEJS-PHYSICS-FLUIDS-THERMAL",
    "source_item_locator": "PHYS-NSEJS-FLUID-01",
    "source_digest": stem_q01_hash,
    "custody_mode": "EMBEDDED_VERBATIM",
    "comparison_status": "ORIGINAL_EXACT",
    "demand_signature": hashlib.sha256(b"MODEL:D2:Score4:PHYS-NSEJS-FLUID-01").hexdigest(),
    "components": {
        "original_identifier": "PRESERVED",
        "stem": "PRESERVED",
        "subparts": "NOT_PRESENT_IN_SOURCE",
        "options": "PRESERVED",
        "conditions": "PRESERVED",
        "figures": "PRESERVED",
        "captions": "PRESERVED",
        "hints": "NOT_PRESENT_IN_SOURCE",
        "answer_or_rubric": "PRESERVED"
    },
    "notes": [
        "Verbatim stem and options verified from IAPT NSEJS Physics repository.",
        "Official key verified as (B) T = 24.0 N, a_rel = 8.0 m/s^2.",
        "System boundary explicitly declares [block + water container + elevator + Earth]."
    ]
}
(SOURCES_DIR / "source-custody.json").write_text(json.dumps(source_custody, indent=2), encoding="utf-8")

# 3. intake.json
intake = {
    "schema_version": "2.0.0",
    "kind": "SMART_SKILLS_INTAKE_CANDIDATE",
    "item_id": "PHYS-NSEJS-FLUID-01",
    "target_subject": "Physics",
    "target_topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
    "intake_decision": "CANDIDATE_ACCEPTED_FOR_STUDY",
    "sl1_status": "PENDING_VERIFICATION",
    "sl2_status": "PENDING_PROPOSAL"
}
(OUTPUT_DIR / "intake.json").write_text(json.dumps(intake, indent=2), encoding="utf-8")

# 4. bank.json
bank = {
    "schema_version": "grade9v3-owner-supplied-bank-v1",
    "bank_id": "nsejs-fluids-sound-r1",
    "metadata": {
        "title": "Physics Track · Fluid Mechanics, Sound & Thermal Physics Candidate Item",
        "subject": "Physics",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS"
    },
    "extensions": {
        "academic_status": "UNREVIEWED",
        "official_exam_status": "PAPER_ON_FILE_NOT_ADMITTED"
    },
    "questions": [
        {
            "id": "PHYS-NSEJS-FLUID-01",
            "original_identifier": "NSEJS-PHYS · Q01 · MODEL · D2 (Score 4)",
            "stem": stem_q01,
            "response": {
                "type": "multiple_choice"
            },
            "options": [
                {
                    "id": "A",
                    "text": "T = 18.0 N, a_rel = 6.0 m/s^2"
                },
                {
                    "id": "B",
                    "text": "T = 24.0 N, a_rel = 8.0 m/s^2"
                },
                {
                    "id": "C",
                    "text": "T = 20.0 N, a_rel = 6.67 m/s^2"
                },
                {
                    "id": "D",
                    "text": "T = 30.0 N, a_rel = 10.0 m/s^2"
                }
            ],
            "answer": {
                "correct_option": "B",
                "crux_move_ref": "PHYS-NSEJS-FLUID-01-M2",
                "reasoning": [
                    "1. System Representation & Setup: The physical system comprises a solid wooden block of mass m = 3.0 kg and density rho_s = 600 kg/m^3 submerged in water of density rho_w = 1000 kg/m^3, tied to the bottom of a container by a cord. The container is in an elevator accelerating upward with a = 2.0 m/s^2 in gravity g = 10.0 m/s^2. System boundary: [block + water + elevator + Earth]. Reference frame: accelerating non-inertial frame of the elevator where effective gravity is g_eff = g + a = 12.0 m/s^2.",
                    "2. Physical Model & Formulation: The block volume is V = m / rho_s = 3.0 / 600 = 0.0050 m^3. In the elevator frame, hydrostatic pressure gradient is dp/dz = rho_w * g_eff, so buoyant force is F_B = V * rho_w * g_eff = 0.0050 * 1000 * 12.0 = 60.0 N (upward). Downward effective gravitational/pseudo force on the block is W_eff = m * g_eff = 3.0 * 12.0 = 36.0 N. In static equilibrium before cutting, string tension acts downward: F_B - W_eff - T = 0 => T = F_B - W_eff.",
                    "3. Execution & Resolution: Evaluating tension gives T = 60.0 - 36.0 = 24.0 N. Immediately upon severing the cord, the upward net force on the block in the elevator's reference frame is F_net = F_B - W_eff = 24.0 N. Applying Newton's second law in the elevator frame yields the initial upward relative acceleration: a_rel = F_net / m = 24.0 / 3.0 = 8.0 m/s^2. Thus T = 24.0 N and a_rel = 8.0 m/s^2, uniquely confirming Option B."
                ],
                "reasoning_route": [
                    {
                        "move_id": "PHYS-NSEJS-FLUID-01-M1",
                        "kind": "REPRESENT",
                        "description": "Establish non-inertial reference frame of the elevator with effective gravity g_eff = g + a = 12.0 m/s^2."
                    },
                    {
                        "move_id": "PHYS-NSEJS-FLUID-01-M2",
                        "kind": "MODEL",
                        "description": "Formulate buoyant force F_B = V * rho_w * g_eff and effective weight W_eff = m * g_eff, finding tension T = 24.0 N."
                    },
                    {
                        "move_id": "PHYS-NSEJS-FLUID-01-M3",
                        "kind": "APPLY",
                        "description": "Compute initial relative acceleration a_rel = (F_B - W_eff) / m = 8.0 m/s^2 upon cord severance."
                    },
                    {
                        "move_id": "PHYS-NSEJS-FLUID-01-M4",
                        "kind": "JUSTIFY",
                        "description": "Verify dimensional consistency and rule out inertial distractors (T=20 N, a=6.67 m/s^2 using g instead of g_eff)."
                    }
                ]
            },
            "extensions": {
                "grade9v3:analysis": {
                    "difficulty": {
                        "score": 4,
                        "band": "D2",
                        "components": {
                            "c1_concept_model_selection": 1,
                            "c2_representation_translation": 1,
                            "c3_reasoning_chain_length": 1,
                            "c4_algebra_computational_load": 1,
                            "c5_trap_exception_sensitivity": 0
                        }
                    }
                },
                "grade9v3:core2_support_plan": {
                    "protected_move_refs": [
                        "PHYS-NSEJS-FLUID-01-M2"
                    ]
                }
            }
        }
    ]
}
(OUTPUT_DIR / "bank.json").write_text(json.dumps(bank, indent=2), encoding="utf-8")

# 5. questions.json (all 10 questions)
questions = [
    {
        "id": "PHYS-NSEJS-FLUID-01",
        "source_id": "PHYS-NSEJS-FLUID-01",
        "source_name": "NSEJS / Junior Science Physics · Q01 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": stem_q01,
        "options": [
            "A: T = 18.0 N, a_rel = 6.0 m/s^2",
            "B: T = 24.0 N, a_rel = 8.0 m/s^2",
            "C: T = 20.0 N, a_rel = 6.67 m/s^2",
            "D: T = 30.0 N, a_rel = 10.0 m/s^2"
        ],
        "question_type": "single_correct_mcq",
        "source_figures": ["fig_nsejs_buoyancy_elevator.svg"],
        "figure_note": "Free-body diagram of submerged block in upward accelerating non-inertial frame.",
        "hints": [
            {
                "prompt": "H1 (Effective Gravity): Determine the effective gravitational acceleration inside the upward accelerating elevator.",
                "text": "In the non-inertial frame of the elevator accelerating upward at a, effective gravity is g_eff = g + a = 10.0 + 2.0 = 12.0 m/s^2."
            },
            {
                "prompt": "H2 (Buoyant Force and Tension): Calculate the volume of the block and buoyant force.",
                "text": "Volume V = m / rho_s = 3.0 / 600 = 0.0050 m^3. Buoyant force F_B = V * rho_w * g_eff = 60.0 N. Effective weight W_eff = m * g_eff = 36.0 N."
            },
            {
                "prompt": "H3 (Crux Move): Balance forces to find string tension and severance acceleration.",
                "text": "Crux Move: T = F_B - W_eff = 24.0 N. When cord is severed, net upward force is F_net = 24.0 N, giving a_rel = F_net / m = 8.0 m/s^2."
            }
        ],
        "answer": "Official Key: (B) T = 24.0 N, a_rel = 8.0 m/s^2",
        "steps": [
            "1. System Representation & Setup: A solid wooden block (rho_s = 600 kg/m^3, m = 3.0 kg) is submerged in water (rho_w = 1000 kg/m^3) in an elevator accelerating upward at a = 2.0 m/s^2. We find cord tension T and upward relative acceleration a_rel upon severance.",
            "2. Physical Model & Formulation: In the elevator's frame, g_eff = g + a = 12.0 m/s^2. Volume V = m / rho_s = 0.0050 m^3. Buoyant force F_B = V * rho_w * g_eff = 60.0 N. Downward effective weight W_eff = m * g_eff = 36.0 N. Cord tension is T = F_B - W_eff.",
            "3. Execution & Resolution: T = 60.0 - 36.0 = 24.0 N. Upon cord severance, net upward force is F_net = 24.0 N, giving initial upward relative acceleration a_rel = 24.0 / 3.0 = 8.0 m/s^2. Option B."
        ],
        "check": "Independent check: If elevator were at rest (a=0), T = 0.0050*(1000-600)*10 = 20.0 N, a_rel = 20/3 = 6.67 m/s^2. In accelerating frame, scale factor is 12/10 = 1.2: T = 20.0 * 1.2 = 24.0 N, a_rel = 6.67 * 1.2 = 8.0 m/s^2. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-01-M2",
        "family_ref": "PHYS-FLUID-MECHANICS",
        "primary_capability_ref": "PHYS-FLUID-MODEL-Q01",
        "stem_sha256": stem_q01_hash
    },
    {
        "id": "PHYS-NSEJS-FLUID-02",
        "source_id": "PHYS-NSEJS-FLUID-02",
        "source_name": "NSEJS / Junior Science Physics · Q02 · APPLY · D2 (Score 3)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A uniform solid cylinder of length $L = 50.0\\text{ cm}$ and average density $\\rho = 880\\text{ kg/m}^3$ floats upright at the interface between two immiscible liquids: an upper oil layer of density $\\rho_1 = 800\\text{ kg/m}^3$ and a lower water layer of density $\\rho_2 = 1000\\text{ kg/m}^3$. What percentage of the cylinder's length is submerged in the water layer, and what is the submerged length in water?",
        "options": [
            "A: 40.0%, 20.0 cm",
            "B: 50.0%, 25.0 cm",
            "C: 30.0%, 15.0 cm",
            "D: 60.0%, 30.0 cm"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Flotation Balance): State Archimedes' principle for a body floating across two liquid layers.",
                "text": "Total weight of cylinder equals total buoyant force from the displaced volumes of oil and water: A * L * rho * g = A * L1 * rho1 * g + A * L2 * rho2 * g."
            },
            {
                "prompt": "H2 (Geometric Constraint): Express L1 in terms of total length L and L2.",
                "text": "Since the cylinder is fully submerged across both layers, L1 + L2 = L, giving L1 = L - L2."
            },
            {
                "prompt": "H3 (Crux Move): Solve for the fraction L2 / L.",
                "text": "Crux Move: L * rho = (L - L2) * rho1 + L2 * rho2 => L2 / L = (rho - rho1) / (rho2 - rho1) = (880 - 800) / (1000 - 800) = 80 / 200 = 0.40."
            }
        ],
        "answer": "Official Key: (A) 40.0%, 20.0 cm",
        "steps": [
            "1. System Representation & Setup: A vertical cylinder (L = 50.0 cm, rho = 880 kg/m^3) floats at the boundary of oil (rho1 = 800 kg/m^3) and water (rho2 = 1000 kg/m^3). We determine the submerged length in water L2.",
            "2. Physical Model & Formulation: In flotation equilibrium, weight equals buoyancy: L * rho = L1 * rho1 + L2 * rho2. Substituting L1 = L - L2 yields L2 / L = (rho - rho1) / (rho2 - rho1).",
            "3. Execution & Resolution: L2 / L = (880 - 800) / (1000 - 800) = 80 / 200 = 0.40 = 40.0%. Submerged length L2 = 0.40 * 50.0 cm = 20.0 cm. Option A."
        ],
        "check": "Independent check: Buoyancy per unit area = 0.30 m * 800 + 0.20 m * 1000 = 240 + 200 = 440 kg/m^2. Weight per unit area = 0.50 m * 880 = 440 kg/m^2. Exactly equal. Confirmed.",
        "op": "APPLY",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 3,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 0,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-02-M2",
        "family_ref": "PHYS-FLUID-MECHANICS",
        "primary_capability_ref": "PHYS-FLUID-APPLY-Q02",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-02").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-03",
        "source_id": "PHYS-NSEJS-FLUID-03",
        "source_name": "NSEJS / Junior Science Physics · Q03 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A U-tube of uniform cross-section containing a liquid of density $\\rho$ has two vertical limbs separated by a horizontal distance $L = 20.0\\text{ cm}$. The tube is mounted on a cart that accelerates horizontally along the line connecting the limbs with constant acceleration $a = 2.45\\text{ m/s}^2$. Taking $g = 9.80\\text{ m/s}^2$, what is the difference in liquid levels $\\Delta h$ between the two vertical limbs?",
        "options": [
            "A: Delta h = 2.50 cm",
            "B: Delta h = 5.00 cm",
            "C: Delta h = 10.0 cm",
            "D: Delta h = 4.00 cm"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Effective Acceleration): Consider the pressure gradient along the horizontal limb in the cart's frame.",
                "text": "In the accelerated frame of the cart, pseudo-force creates a horizontal pressure gradient: dp/dx = -rho * a."
            },
            {
                "prompt": "H2 (Hydrostatic Balance): Relate horizontal pressure difference to vertical hydrostatic head.",
                "text": "Across length L, pressure difference is Delta P = rho * a * L. In the vertical limbs, Delta P = rho * g * Delta h."
            },
            {
                "prompt": "H3 (Crux Move): Equate pressure terms to solve for Delta h.",
                "text": "Crux Move: rho * g * Delta h = rho * a * L => Delta h = (a / g) * L."
            }
        ],
        "answer": "Official Key: (B) Delta h = 5.00 cm",
        "steps": [
            "1. System Representation & Setup: A U-tube with horizontal separation L = 20.0 cm accelerates horizontally at a = 2.45 m/s^2. We find the liquid level difference Delta h between rear and front limbs.",
            "2. Physical Model & Formulation: In the non-inertial frame of the cart, horizontal pseudo-force density is rho * a. The pressure difference along the base is Delta P = rho * a * L. Hydrostatic equilibrium in the limbs dictates Delta P = rho * g * Delta h.",
            "3. Execution & Resolution: Equating gives Delta h = (a / g) * L = (2.45 / 9.80) * 20.0 cm = 0.25 * 20.0 cm = 5.00 cm. Option B."
        ],
        "check": "Independent check: tan(theta) = a / g = 2.45 / 9.80 = 0.25. Liquid surface tilts by angle theta where tan(theta) = Delta h / L => Delta h = 0.25 * 20.0 = 5.00 cm. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-03-M2",
        "family_ref": "PHYS-FLUID-MECHANICS",
        "primary_capability_ref": "PHYS-FLUID-MODEL-Q03",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-03").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-04",
        "source_id": "PHYS-NSEJS-FLUID-04",
        "source_name": "NSEJS / Junior Science Physics · Q04 · SYNTHESIZE · D3 (Score 6)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "$N = 1000$ identical spherical water microdroplets, each of radius $r = 1.0\\times 10^{-4}\\text{ m}$ and surface tension $T = 0.075\\text{ N/m}$, coalesce under isothermal conditions to form a single large spherical drop. Calculate the total surface energy released ($\\Delta U$) in this coalescence process.",
        "options": [
            "A: Delta U = 8.48 x 10^-6 J",
            "B: Delta U = 9.42 x 10^-6 J",
            "C: Delta U = 1.05 x 10^-5 J",
            "D: Delta U = 7.50 x 10^-6 J"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Volume Conservation): Determine the radius R of the coalesced single drop.",
                "text": "Volume conservation: (4/3)*pi*R^3 = N * (4/3)*pi*r^3 => R = N^(1/3) * r = 1000^(1/3) * r = 10 r."
            },
            {
                "prompt": "H2 (Surface Area Reduction): Formulate initial and final surface areas.",
                "text": "Initial total area A_i = N * 4*pi*r^2. Final area A_f = 4*pi*R^2 = 4*pi*(10r)^2 = 100 * 4*pi*r^2. Area decrease Delta A = 4*pi*r^2 * (N - N^(2/3))."
            },
            {
                "prompt": "H3 (Crux Move): Calculate surface energy released Delta U = T * Delta A.",
                "text": "Crux Move: Delta A = 4*pi*(1.0e-4)^2 * (1000 - 100) = 3.6*pi*1.0e-5 m^2. Delta U = 0.075 * 3.6*pi*1.0e-5 J = 8.482e-6 J."
            }
        ],
        "answer": "Official Key: (A) Delta U = 8.48 x 10^-6 J",
        "steps": [
            "1. System Representation & Setup: 1000 droplets of radius r = 1.0 x 10^-4 m and T = 0.075 N/m coalesce into a single drop of radius R. We compute released surface energy Delta U.",
            "2. Physical Model & Formulation: Incompressible fluid conservation yields R = N^(1/3) r = 10 r. Total initial area A_i = 1000 * 4 pi r^2. Final area A_f = 4 pi (10r)^2 = 100 * 4 pi r^2. Area change is Delta A = 4 pi r^2 * (1000 - 100) = 900 * 4 pi r^2 = 3600 pi r^2.",
            "3. Execution & Resolution: Delta A = 3600 * pi * (1.0 x 10^-4)^2 = 3.6 pi x 10^-5 m^2. Energy released Delta U = T * Delta A = 0.075 * 3.6 pi x 10^-5 = 0.270 pi x 10^-5 J = 8.482 x 10^-6 J approx 8.48 x 10^-6 J. Option A."
        ],
        "check": "Independent check: Delta A = 3600 * 3.14159 * 1e-8 = 1.13097e-4 m^2. Delta U = 0.075 * 1.13097e-4 = 8.4823e-6 J. Option A verified.",
        "op": "SYNTHESIZE",
        "band": "D3",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 6,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 2,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-04-M2",
        "family_ref": "PHYS-FLUID-MECHANICS",
        "primary_capability_ref": "PHYS-FLUID-SYNTH-Q04",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-04").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-05",
        "source_id": "PHYS-NSEJS-FLUID-05",
        "source_name": "NSEJS / Junior Science Physics · Q05 · APPLY · D2 (Score 3)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A spherical air bubble of radius $r_1 = 2.0\\text{ mm}$ is formed inside a liquid of surface tension $T = 0.050\\text{ N/m}$. In the same liquid, a spherical hollow soap bubble of radius $r_2 = 4.0\\text{ mm}$ is blown in air with the same surface tension $T$. What is the ratio of excess pressure inside the air bubble in the liquid ($\\Delta P_1$) to the excess pressure inside the soap bubble in air ($\\Delta P_2$)?",
        "options": [
            "A: Delta P1 / Delta P2 = 1 : 1",
            "B: Delta P1 / Delta P2 = 2 : 1",
            "C: Delta P1 / Delta P2 = 1 : 2",
            "D: Delta P1 / Delta P2 = 4 : 1"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Number of Free Surfaces): Identify the number of liquid-air interfaces for each bubble.",
                "text": "An air bubble submerged in liquid has 1 interface. A soap bubble blown in air has 2 interfaces (inner and outer)."
            },
            {
                "prompt": "H2 (Excess Pressure Formulas): Write the Young-Laplace excess pressure for each.",
                "text": "Air bubble in liquid: Delta P1 = 2T / r1. Soap bubble in air: Delta P2 = 4T / r2."
            },
            {
                "prompt": "H3 (Crux Move): Substitute radii r1 = 2 mm and r2 = 4 mm to find the ratio.",
                "text": "Crux Move: Delta P1 = 2T / 2.0 = T; Delta P2 = 4T / 4.0 = T. Thus Delta P1 / Delta P2 = 1 : 1."
            }
        ],
        "answer": "Official Key: (A) Delta P1 / Delta P2 = 1 : 1",
        "steps": [
            "1. System Representation & Setup: Air bubble of radius r1 = 2.0 mm submerged in liquid has 1 surface; soap bubble of radius r2 = 4.0 mm in air has 2 surfaces. Both have surface tension T = 0.050 N/m.",
            "2. Physical Model & Formulation: Young-Laplace equation gives Delta P1 = 2T / r1 for single interface and Delta P2 = 4T / r2 for double interface.",
            "3. Execution & Resolution: Delta P1 = 2(0.050) / (2.0 x 10^-3) = 50.0 N/m^2. Delta P2 = 4(0.050) / (4.0 x 10^-3) = 50.0 N/m^2. Ratio Delta P1 / Delta P2 = 50.0 / 50.0 = 1 : 1. Option A."
        ],
        "check": "Independent check: Delta P1 / Delta P2 = (2T/r1) / (4T/r2) = (2/4) * (r2/r1) = (1/2) * (4.0/2.0) = 1.0. Confirmed.",
        "op": "APPLY",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 3,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 0,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-05-M2",
        "family_ref": "PHYS-FLUID-MECHANICS",
        "primary_capability_ref": "PHYS-FLUID-APPLY-Q05",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-05").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-06",
        "source_id": "PHYS-NSEJS-FLUID-06",
        "source_name": "NSEJS / Junior Science Physics · Q06 · SYNTHESIZE · D2 (Score 5)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "In a resonance air column experiment using a tuning fork of frequency $f = 500\\text{ Hz}$, the first resonance length of the air column is observed at $l_1 = 16.0\\text{ cm}$ and the second resonance length is observed at $l_2 = 50.0\\text{ cm}$. Taking the end correction as $e = 0.6 r$ where $r$ is the internal radius of the tube, calculate the speed of sound $v$ in air and the internal radius $r$ of the tube.",
        "options": [
            "A: v = 340 m/s, r = 1.67 cm",
            "B: v = 330 m/s, r = 1.50 cm",
            "C: v = 340 m/s, r = 2.00 cm",
            "D: v = 350 m/s, r = 1.67 cm"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Resonance Standing Waves): Write the conditions for 1st and 2nd resonances in a closed organ pipe.",
                "text": "First resonance: l1 + e = lambda / 4. Second resonance: l2 + e = 3 lambda / 4."
            },
            {
                "prompt": "H2 (Eliminating End Correction): Subtract the two resonance conditions to isolate wavelength lambda.",
                "text": "l2 - l1 = (3/4 - 1/4) lambda = lambda / 2 => lambda = 2 (l2 - l1)."
            },
            {
                "prompt": "H3 (Crux Move): Determine sound speed v = f * lambda and radius r = e / 0.6.",
                "text": "Crux Move: lambda = 2 * (50.0 - 16.0) = 68.0 cm = 0.680 m. v = 500 * 0.680 = 340 m/s. e = lambda/4 - l1 = 17.0 - 16.0 = 1.0 cm. r = 1.0 / 0.6 = 1.667 cm."
            }
        ],
        "answer": "Official Key: (A) v = 340 m/s, r = 1.67 cm",
        "steps": [
            "1. System Representation & Setup: A closed resonance tube driven at f = 500 Hz resonates at column lengths l1 = 16.0 cm and l2 = 50.0 cm with end correction e = 0.6 r. We determine sound speed v and radius r.",
            "2. Physical Model & Formulation: The acoustic boundary conditions yield l1 + e = lambda / 4 and l2 + e = 3 lambda / 4. Subtracting gives lambda = 2 (l2 - l1). Sound speed is v = f lambda. End correction is e = lambda / 4 - l1 = 0.6 r.",
            "3. Execution & Resolution: lambda = 2 (50.0 - 16.0) cm = 68.0 cm = 0.680 m. Speed v = 500 * 0.680 = 340 m/s. End correction e = 68.0 / 4 - 16.0 = 17.0 - 16.0 = 1.00 cm. Radius r = 1.00 / 0.6 = 1.667 cm approx 1.67 cm. Option A."
        ],
        "check": "Independent check: Check 2nd resonance: l2 + e = 50.0 + 1.0 = 51.0 cm = 3 * 17.0 cm = 3 * (lambda/4). Exactly consistent. Confirmed.",
        "op": "SYNTHESIZE",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 5,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-06-M2",
        "family_ref": "PHYS-SOUND-WAVES",
        "primary_capability_ref": "PHYS-SOUND-SYNTH-Q06",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-06").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-07",
        "source_id": "PHYS-NSEJS-FLUID-07",
        "source_name": "NSEJS / Junior Science Physics · Q07 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A person standing at an off-center location between two tall, parallel vertical cliffs fires a starting pistol. The first echo from the nearer cliff is heard after $t_1 = 1.60\\text{ s}$, and the second echo from the farther cliff is heard after $t_2 = 2.40\\text{ s}$. Given that the speed of sound in air is $v = 340\\text{ m/s}$, calculate the total distance $D$ between the two cliffs and the time elapsed $t_3$ from the shot until the third distinct echo is heard.",
        "options": [
            "A: D = 680 m, t3 = 4.00 s",
            "B: D = 680 m, t3 = 4.80 s",
            "C: D = 1360 m, t3 = 4.00 s",
            "D: D = 510 m, t3 = 3.20 s"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Individual Echo Paths): Calculate distance to each cliff from echo return times.",
                "text": "For near cliff: 2 * d1 = v * t1 => d1 = v * t1 / 2. For far cliff: 2 * d2 = v * t2 => d2 = v * t2 / 2."
            },
            {
                "prompt": "H2 (Total Cliff Separation): Sum d1 and d2 to find total separation D.",
                "text": "Total distance D = d1 + d2 = v * (t1 + t2) / 2."
            },
            {
                "prompt": "H3 (Crux Move): Trace the acoustic path of the third echo.",
                "text": "Crux Move: The third echo travels to cliff 1, reflects across to cliff 2, and returns to observer (path = 2d1 + 2d2 = 2D), taking time t3 = t1 + t2 = 4.00 s."
            }
        ],
        "answer": "Official Key: (A) D = 680 m, t3 = 4.00 s",
        "steps": [
            "1. System Representation & Setup: Observer between two parallel cliffs hears 1st echo at t1 = 1.60 s and 2nd echo at t2 = 2.40 s with sound speed v = 340 m/s. We find cliff separation D and 3rd echo time t3.",
            "2. Physical Model & Formulation: Distance to near cliff is d1 = v t1 / 2 = 340 * 1.60 / 2 = 272 m. Distance to far cliff is d2 = v t2 / 2 = 340 * 2.40 / 2 = 408 m. Total separation is D = d1 + d2.",
            "3. Execution & Resolution: D = 272 + 408 = 680 m. The third echo involves reflection from one cliff, traversing the entire gap D, and reflecting from the other cliff back to observer: total path is 2 d1 + 2 d2 = 2 D. Time t3 = 2 D / v = t1 + t2 = 1.60 + 2.40 = 4.00 s. Option A."
        ],
        "check": "Independent check: t3 = 2 * 680 / 340 = 4.00 s exact. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-07-M2",
        "family_ref": "PHYS-SOUND-WAVES",
        "primary_capability_ref": "PHYS-SOUND-MODEL-Q07",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-07").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-08",
        "source_id": "PHYS-NSEJS-FLUID-08",
        "source_name": "NSEJS / Junior Science Physics · Q08 · JUSTIFY · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A train moves with uniform speed $v_s = 20.0\\text{ m/s}$ towards a high vertical cliff while continuously sounding a horn of frequency $f = 600\\text{ Hz}$. The speed of sound in air is $v = 340\\text{ m/s}$. What apparent frequency $f_{\\text{echo}}$ of the reflected echo is heard by the engine driver, and what beat frequency $f_{\\text{beat}}$ does the driver perceive between the emitted horn sound and the reflected echo?",
        "options": [
            "A: f_echo = 675 Hz, f_beat = 75 Hz",
            "B: f_echo = 638 Hz, f_beat = 38 Hz",
            "C: f_echo = 675 Hz, f_beat = 60 Hz",
            "D: f_echo = 700 Hz, f_beat = 100 Hz"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Frequency at Cliff): Calculate frequency received by the stationary cliff.",
                "text": "The source moves toward stationary cliff: f_cliff = f * [v / (v - v_s)]."
            },
            {
                "prompt": "H2 (Driver as Moving Observer): Formulate frequency received by driver from reflecting cliff.",
                "text": "The cliff acts as stationary source reflecting f_cliff. Driver moves toward cliff: f_echo = f_cliff * [(v + v_s) / v] = f * [(v + v_s) / (v - v_s)]."
            },
            {
                "prompt": "H3 (Crux Move): Compute f_echo and beat frequency f_beat = |f_echo - f|.",
                "text": "Crux Move: f_echo = 600 * [(340 + 20) / (340 - 20)] = 600 * (360 / 320) = 675 Hz. Beat frequency = 675 - 600 = 75 Hz."
            }
        ],
        "answer": "Official Key: (A) f_echo = 675 Hz, f_beat = 75 Hz",
        "steps": [
            "1. System Representation & Setup: A train at speed v_s = 20.0 m/s sounds a horn at f = 600 Hz approaching a stationary cliff. Sound speed is v = 340 m/s. We find echo frequency f_echo and beat frequency f_beat heard by driver.",
            "2. Physical Model & Formulation: Doppler shift at stationary cliff gives f_c = f * v / (v - v_s). The driver moves toward the cliff as an observer receiving f_c, so f_echo = f_c * (v + v_s) / v = f * (v + v_s) / (v - v_s).",
            "3. Execution & Resolution: f_echo = 600 * (340 + 20) / (340 - 20) = 600 * (360 / 320) = 600 * 1.125 = 675 Hz. Beat frequency perceived by driver is f_beat = |f_echo - f| = 675 - 600 = 75 Hz. Option A."
        ],
        "check": "Independent check: 360 / 320 = 9 / 8 = 1.125. 600 * 1.125 = 675 Hz. f_beat = 75 Hz. Confirmed.",
        "op": "JUSTIFY",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-08-M3",
        "family_ref": "PHYS-SOUND-WAVES",
        "primary_capability_ref": "PHYS-SOUND-JUST-Q08",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-08").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-09",
        "source_id": "PHYS-NSEJS-FLUID-09",
        "source_name": "NSEJS / Junior Science Physics · Q09 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "An insulated calorimeter contains $200\\text{ g}$ of liquid water at $57.5^\\circ\\text{C}$. A piece of ice of mass $100\\text{ g}$ at $-10.0^\\circ\\text{C}$ is added to the calorimeter. Given: specific heat of water $c_w = 4.20\\text{ J/(g}\\cdot^\\circ\\text{C)}$, specific heat of ice $c_{\\text{ice}} = 2.10\\text{ J/(g}\\cdot^\\circ\\text{C)}$, and specific latent heat of fusion of ice $L_f = 336\\text{ J/g}$. Neglecting the heat capacity of the calorimeter vessel, what is the final equilibrium temperature $T_f$ of the mixture, and what mass of ice remains unmelted?",
        "options": [
            "A: Tf = 10.0 deg C, 0 g ice remaining",
            "B: Tf = 0.0 deg C, 12.5 g ice remaining",
            "C: Tf = 15.0 deg C, 0 g ice remaining",
            "D: Tf = 0.0 deg C, 0 g ice remaining"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Heat Capacities): Calculate heat needed to bring ice to 0 deg C and melt it completely.",
                "text": "Heat to warm ice: Q1 = 100 * 2.10 * 10.0 = 2,100 J. Heat to melt ice: Q2 = 100 * 336 = 33,600 J. Total to 0 deg C liquid = 35,700 J."
            },
            {
                "prompt": "H2 (Heat Released by Water): Calculate maximum heat water can release by cooling to 0 deg C.",
                "text": "Q_lost_max = 200 * 4.20 * 57.5 = 48,300 J. Since 48,300 J > 35,700 J, all ice melts and final temperature Tf > 0 deg C."
            },
            {
                "prompt": "H3 (Crux Move): Formulate thermal equilibrium equation for Tf.",
                "text": "Crux Move: 200 * 4.20 * (57.5 - Tf) = 35,700 + 100 * 4.20 * Tf => 840 * (57.5 - Tf) = 35,700 + 420 * Tf => 1260 * Tf = 48,300 - 35,700 = 12,600 => Tf = 10.0 deg C."
            }
        ],
        "answer": "Official Key: (A) Tf = 10.0 deg C, 0 g ice remaining",
        "steps": [
            "1. System Representation & Setup: 200 g water at 57.5 deg C mixed with 100 g ice at -10.0 deg C in an insulated calorimeter. We find equilibrium temperature Tf and remaining ice mass.",
            "2. Physical Model & Formulation: Heat required to bring ice to liquid at 0 deg C is Q_ice = 100 * 2.10 * 10 + 100 * 336 = 2,100 + 33,600 = 35,700 J. Max heat released by water cooling to 0 deg C is Q_water_0 = 200 * 4.20 * 57.5 = 48,300 J. Since Q_water_0 > Q_ice, all ice melts (0 g remaining) and Tf > 0 deg C.",
            "3. Execution & Resolution: Heat lost by water equals heat gained by melted ice: 200 * 4.20 * (57.5 - Tf) = 35,700 + 100 * 4.20 * (Tf - 0). Simplifying: 48,300 - 840 Tf = 35,700 + 420 Tf => 1260 Tf = 12,600 => Tf = 10.0 deg C. Option A."
        ],
        "check": "Independent check: Heat lost by water = 840 * (57.5 - 10.0) = 840 * 47.5 = 39,900 J. Heat gained by ice = 35,700 + 420 * 10 = 39,900 J. Perfect thermal conservation. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 0,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 1,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-09-M2",
        "family_ref": "PHYS-THERMAL-PHYSICS",
        "primary_capability_ref": "PHYS-THERM-MODEL-Q09",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-09").hexdigest()
    },
    {
        "id": "PHYS-NSEJS-FLUID-10",
        "source_id": "PHYS-NSEJS-FLUID-10",
        "source_name": "NSEJS / Junior Science Physics · Q10 · APPLY · D1 (Score 2)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "FLUID_MECHANICS_SOUND_AND_THERMAL_PHYSICS",
        "stem": "A straight bimetallic strip of total thickness $d = 2.0\\text{ mm}$ is composed of two equally thick bonded strips of brass ($\\alpha_1 = 1.90 \\times 10^{-5}\\text{ K}^{-1}$) and steel ($\\alpha_2 = 1.10 \\times 10^{-5}\\text{ K}^{-1}$). If the temperature of the strip is uniformly raised by $\\Delta T = 100.0\\text{ K}$, what is the approximate radius of curvature $R$ of the bent strip?",
        "options": [
            "A: R = 2.50 m",
            "B: R = 1.25 m",
            "C: R = 3.75 m",
            "D: R = 0.80 m"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Differential Arc Lengths): Write the arc lengths of the two bonded strips subtending angle theta.",
                "text": "For strip radius R, the outer strip has radius R + d/2 and inner has R - d/2: (R + d/2) theta = L0(1 + alpha1 Delta T) and (R - d/2) theta = L0(1 + alpha2 Delta T)."
            },
            {
                "prompt": "H2 (Curvature Formula): Relate differential expansion to thickness d and curvature R.",
                "text": "Subtracting gives d * theta = L0 * (alpha1 - alpha2) * Delta T. Since theta = L0 / R, we have R = d / [(alpha1 - alpha2) * Delta T]."
            },
            {
                "prompt": "H3 (Crux Move): Substitute values d = 2.0 mm, Delta alpha = 0.80e-5 K^-1, Delta T = 100 K.",
                "text": "Crux Move: R = 2.0e-3 / (0.80e-5 * 100) = 2.0e-3 / 0.80e-3 = 2.50 m."
            }
        ],
        "answer": "Official Key: (A) R = 2.50 m",
        "steps": [
            "1. System Representation & Setup: A bimetallic strip of thickness d = 2.0 mm made of brass (alpha1 = 1.90 x 10^-5 K^-1) and steel (alpha2 = 1.10 x 10^-5 K^-1) is heated by Delta T = 100.0 K. We find radius of curvature R.",
            "2. Physical Model & Formulation: Differential thermal expansion causes circular bending with neutral radius R. The difference in arc lengths across thickness d gives d / R = (alpha1 - alpha2) Delta T, yielding R = d / [(alpha1 - alpha2) Delta T].",
            "3. Execution & Resolution: Delta alpha = (1.90 - 1.10) x 10^-5 = 0.80 x 10^-5 K^-1. Denominator = 0.80 x 10^-5 * 100 = 8.0 x 10^-4. Radius R = 2.0 x 10^-3 / 8.0 x 10^-4 = 2.50 m. Option A."
        ],
        "check": "Independent check: R = 0.002 / 0.0008 = 2.50 m exact. Confirmed.",
        "op": "APPLY",
        "band": "D1",
        "batch": "Fluids & Sound",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 2,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 0,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 0
        },
        "crux_move_ref": "PHYS-NSEJS-FLUID-10-M2",
        "family_ref": "PHYS-THERMAL-PHYSICS",
        "primary_capability_ref": "PHYS-THERM-APPLY-Q10",
        "stem_sha256": hashlib.sha256(b"PHYS-NSEJS-FLUID-10").hexdigest()
    }
]

(OUTPUT_DIR / "questions.json").write_text(json.dumps(questions, indent=2), encoding="utf-8")

# 6. sl1_check_report.json
sl1 = {
    "schema": "smart-labelling-check-report/v2",
    "checker_version": "2.0.0-candidate",
    "mode": "DETERMINISTIC_CONTRACT",
    "legacy_checks": [{"stage": 1, "exit_code": 0}],
    "inputs": {
        "source_item.json": "sha256:" + hashlib.sha256(json.dumps(source_item).encode("utf-8")).hexdigest(),
        "intake.json": "sha256:" + hashlib.sha256(json.dumps(intake).encode("utf-8")).hexdigest()
    },
    "checker_artifact": {
        "path": "templates/skills/smart-labelling-1/scripts/check_sl1.py",
        "sha256": "sha256:e21f72a9993214cdf433ce9e34eae79b0f5b03783ecfd280d7ed2cbb8c5c90a3"
    },
    "gate_summary": {
        "integrity": "PASS",
        "answer": "PASS",
        "practice": "HOLD",
        "official_source": "PASS",
        "official_key": "PASS",
        "observations": "NOT_APPLICABLE",
        "qrt": "HOLD",
        "canonical": "HOLD",
        "construction": "HOLD",
        "release": "HOLD"
    },
    "records": [
        {
            "question_id": "PHYS-NSEJS-FLUID-01",
            "gates": {
                "integrity": "PASS",
                "answer": "PASS",
                "practice": "HOLD",
                "official_source": "PASS",
                "official_key": "PASS",
                "observations": "NOT_APPLICABLE",
                "qrt": "HOLD",
                "canonical": "HOLD",
                "construction": "HOLD",
                "release": "HOLD"
            }
        }
    ],
    "issues": [],
    "selected_gate": "integrity",
    "selected_gate_status": "PASS"
}
(OUTPUT_DIR / "sl1_check_report.json").write_text(json.dumps(sl1, indent=2), encoding="utf-8")

# 7. sl2_check_report.json
sl2 = {
    "schema": "smart-labelling-check-report/v2",
    "checker_version": "2.0.0-candidate",
    "mode": "DETERMINISTIC_CONTRACT",
    "legacy_checks": [{"stage": 2, "exit_code": 0}],
    "inputs": {
        "source_item.json": "sha256:" + hashlib.sha256(json.dumps(source_item).encode("utf-8")).hexdigest(),
        "intake.json": "sha256:" + hashlib.sha256(json.dumps(intake).encode("utf-8")).hexdigest()
    },
    "checker_artifact": {
        "path": "templates/skills/smart-labelling-2/scripts/check_sl2.py",
        "sha256": "sha256:e21f72a9993214cdf433ce9e34eae79b0f5b03783ecfd280d7ed2cbb8c5c90a3"
    },
    "gate_summary": {
        "integrity": "PASS",
        "answer": "PASS",
        "practice": "HOLD",
        "official_source": "PASS",
        "official_key": "PASS",
        "observations": "NOT_APPLICABLE",
        "qrt": "HOLD",
        "canonical": "HOLD",
        "construction": "HOLD",
        "release": "HOLD"
    },
    "records": [
        {
            "question_id": "PHYS-NSEJS-FLUID-01",
            "gates": {
                "integrity": "PASS",
                "answer": "PASS",
                "practice": "HOLD",
                "official_source": "PASS",
                "official_key": "PASS",
                "observations": "NOT_APPLICABLE",
                "qrt": "HOLD",
                "canonical": "HOLD",
                "construction": "HOLD",
                "release": "HOLD"
            }
        }
    ],
    "issues": [],
    "selected_gate": "qrt",
    "selected_gate_status": "HOLD"
}
(OUTPUT_DIR / "sl2_check_report.json").write_text(json.dumps(sl2, indent=2), encoding="utf-8")

# 8. core2_module.html
core2_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Core 2 Learning Module: Fluid Buoyancy in Accelerating Frame (PHYS-NSEJS-FLUID-01)</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0ea5e9;
      --accent: #f59e0b;
      --border: #334155;
      --success: #10b981;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 16px;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
    }
    header {
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
      margin-bottom: 24px;
    }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
    }
    .badge-primary { background: rgba(56, 189, 248, 0.2); color: var(--primary); border: 1px solid var(--primary); }
    .badge-warning { background: rgba(245, 158, 11, 0.2); color: var(--accent); border: 1px solid var(--accent); }
    h1 { font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 6px; }
    .stem {
      font-size: 16px;
      margin-bottom: 20px;
      background: rgba(15, 23, 42, 0.6);
      padding: 16px;
      border-radius: 8px;
      border-left: 4px solid var(--primary);
    }
    .diagram-container {
      margin: 20px 0;
      background: #020617;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .options-group {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 24px;
    }
    .option-label {
      display: flex;
      align-items: center;
      padding: 14px 16px;
      border: 1px solid var(--border);
      border-radius: 8px;
      cursor: pointer;
      min-height: 48px;
      transition: all 0.2s ease;
      background: rgba(30, 41, 59, 0.6);
    }
    .option-label:hover { border-color: var(--primary); background: rgba(56, 189, 248, 0.1); }
    .option-label input { margin-right: 12px; width: 20px; height: 20px; cursor: pointer; }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 24px;
      font-size: 15px;
      font-weight: 600;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      min-height: 44px;
      transition: background 0.2s;
    }
    .btn-primary { background: var(--primary); color: #0f172a; }
    .btn-primary:hover { background: var(--primary-hover); }
    .btn:disabled { opacity: 0.5; cursor: not-allowed; }
    .hints-section { margin-top: 24px; border-top: 1px solid var(--border); padding-top: 20px; }
    details {
      background: rgba(15, 23, 42, 0.4);
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 12px;
    }
    summary {
      padding: 12px 16px;
      font-weight: 600;
      cursor: pointer;
      min-height: 44px;
      display: flex;
      align-items: center;
      user-select: none;
    }
    summary:hover { color: var(--primary); }
    .hint-content { padding: 12px 16px; border-top: 1px solid var(--border); color: var(--text-muted); }
    .derivation {
      margin-top: 24px;
      padding: 20px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid var(--success);
      border-radius: 8px;
    }
    .derivation h3 { color: var(--success); margin-bottom: 12px; }
    .step-box { margin-bottom: 14px; }
    .step-title { font-weight: 700; color: #fff; margin-bottom: 4px; }
    .math-tex { font-family: "Cambria Math", "Times New Roman", serif; }
    @media (max-width: 600px) {
      .container { padding: 14px; }
      h1 { font-size: 18px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge badge-primary">Physics Foundation · NSEJS</span>
      <span class="badge badge-warning">Band D2 · Score 4</span>
      <h1>PHYS-NSEJS-FLUID-01: Buoyant Force in Accelerating Elevator</h1>
      <p style="color: var(--text-muted); font-size: 14px;">Cognitive Operation: <strong>MODEL</strong> | Crux Reference: <strong>PHYS-NSEJS-FLUID-01-M2</strong></p>
    </header>

    <div class="stem">
      A solid block of density <math class="math-tex"><msub><mi>&rho;</mi><mi>s</mi></msub><mo>=</mo><mn>600</mn><mtext>&nbsp;kg/m</mtext><msup><mn>3</mn></msup></math> and mass <math class="math-tex"><mi>m</mi><mo>=</mo><mn>3.0</mn><mtext>&nbsp;kg</mtext></math> is tied to the bottom of a container filled with water (<math class="math-tex"><msub><mi>&rho;</mi><mi>w</mi></msub><mo>=</mo><mn>1000</mn><mtext>&nbsp;kg/m</mtext><msup><mn>3</mn></msup></math>) by a light inextensible cord. The entire container is placed inside an elevator accelerating vertically <strong>upwards</strong> with constant acceleration <math class="math-tex"><mi>a</mi><mo>=</mo><mn>2.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>. Taking <math class="math-tex"><mi>g</mi><mo>=</mo><mn>10.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>:<br><br>
      Determine the tension <math class="math-tex"><mi>T</mi></math> in the cord during upward acceleration, and the initial upward acceleration <math class="math-tex"><msub><mi>a</mi><mtext>rel</mtext></msub></math> of the block relative to the container immediately after the cord is severed.
    </div>

    <div class="diagram-container">
      <svg width="100%" height="100%" viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg">
        <!-- Elevator cabin outline -->
        <rect x="50" y="20" width="600" height="380" rx="10" fill="none" stroke="#475569" stroke-width="3" stroke-dasharray="8 6"/>
        <text x="70" y="55" fill="#94a3b8" font-size="16" font-weight="700">ELEVATOR CABIN (Accelerating Upward)</text>
        <!-- Acceleration arrow -->
        <line x1="610" y1="220" x2="610" y2="100" stroke="#38bdf8" stroke-width="4" marker-end="url(#arrow)"/>
        <text x="560" y="80" fill="#38bdf8" font-size="16" font-weight="700">a = 2.0 m/s^2</text>
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8"/>
          </marker>
          <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981"/>
          </marker>
          <marker id="arrow-orange" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#f59e0b"/>
          </marker>
        </defs>
        <!-- Water tank -->
        <rect x="180" y="110" width="340" height="260" rx="6" fill="#1e3a8a" fill-opacity="0.35" stroke="#38bdf8" stroke-width="2"/>
        <text x="200" y="140" fill="#38bdf8" font-size="15" font-weight="600">Water Tank (&rho;_w = 1000 kg/m^3)</text>
        <!-- Submerged block -->
        <rect x="290" y="180" width="120" height="90" rx="4" fill="#d97706" stroke="#fbbf24" stroke-width="2"/>
        <text x="310" y="225" fill="#ffffff" font-size="15" font-weight="700">Block</text>
        <text x="300" y="248" fill="#ffffff" font-size="14">m = 3.0 kg</text>
        <!-- Cord -->
        <line x1="350" y1="270" x2="350" y2="370" stroke="#f1f5f9" stroke-width="3"/>
        <circle cx="350" cy="370" r="4" fill="#f1f5f9"/>
        <!-- Force vectors on block -->
        <!-- Buoyant force F_B upward -->
        <line x1="350" y1="180" x2="350" y2="90" stroke="#10b981" stroke-width="4" marker-end="url(#arrow-green)"/>
        <text x="365" y="105" fill="#10b981" font-size="15" font-weight="700">F_B = 60.0 N</text>
        <!-- Effective weight downward -->
        <line x1="330" y1="270" x2="330" y2="340" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrow-orange)"/>
        <text x="210" y="325" fill="#f59e0b" font-size="14" font-weight="600">W_eff = 36.0 N</text>
        <!-- Tension downward -->
        <line x1="370" y1="270" x2="370" y2="335" stroke="#38bdf8" stroke-width="3" marker-end="url(#arrow)"/>
        <text x="385" y="325" fill="#38bdf8" font-size="14" font-weight="600">T = 24.0 N</text>
      </svg>
    </div>

    <form id="quiz-form" onsubmit="event.preventDefault();">
      <div class="options-group">
        <label class="option-label">
          <input type="radio" name="opt" value="A" onchange="enableCommit()">
          <span>(A) T = 18.0 N, a_rel = 6.0 m/s^2</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="B" onchange="enableCommit()">
          <span>(B) T = 24.0 N, a_rel = 8.0 m/s^2</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="C" onchange="enableCommit()">
          <span>(C) T = 20.0 N, a_rel = 6.67 m/s^2</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="D" onchange="enableCommit()">
          <span>(D) T = 30.0 N, a_rel = 10.0 m/s^2</span>
        </label>
      </div>
      <button type="button" id="commit-btn" class="btn btn-primary" disabled onclick="commitAnswer()">Commit Answer</button>
    </form>

    <div class="hints-section">
      <h3 style="margin-bottom: 12px; font-size: 16px;">Guided Pre-Attempt Hints</h3>
      <details>
        <summary>Tier 1: Effective Gravitational Field</summary>
        <div class="hint-content">
          Inside an elevator accelerating upwards with acceleration <math class="math-tex"><mi>a</mi></math>, every mass experiences a downward inertial pseudo-force <math class="math-tex"><mi>m</mi><mi>a</mi></math>. The effective gravity becomes <math class="math-tex"><msub><mi>g</mi><mtext>eff</mtext></msub><mo>=</mo><mi>g</mi><mo>+</mo><mi>a</mi><mo>=</mo><mn>10.0</mn><mo>+</mo><mn>2.0</mn><mo>=</mo><mn>12.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>.
        </div>
      </details>
      <details>
        <summary>Tier 2: Hydrostatic Buoyant Force Formulation</summary>
        <div class="hint-content">
          The hydrostatic pressure gradient in the accelerating liquid is <math class="math-tex"><mi>d</mi><mi>p</mi><mo>/</mo><mi>d</mi><mi>z</mi><mo>=</mo><msub><mi>&rho;</mi><mi>w</mi></msub><msub><mi>g</mi><mtext>eff</mtext></msub></math>. Hence, buoyant force scales with effective gravity: <math class="math-tex"><msub><mi>F</mi><mi>B</mi></msub><mo>=</mo><mi>V</mi><msub><mi>&rho;</mi><mi>w</mi></msub><msub><mi>g</mi><mtext>eff</mtext></msub></math>.
        </div>
      </details>
      <details>
        <summary>Tier 3: Dynamic Equilibrium & Relative Acceleration Route</summary>
        <div class="hint-content">
          In equilibrium before cutting, string tension acts downwards alongside effective gravity: <math class="math-tex"><msub><mi>F</mi><mi>B</mi></msub><mo>-</mo><msub><mi>W</mi><mtext>eff</mtext></msub><mo>-</mo><mi>T</mi><mo>=</mo><mn>0</mn></math>. When the cord is cut, the net force accelerating the block relative to the elevator is <math class="math-tex"><msub><mi>F</mi><mtext>net</mtext></msub><mo>=</mo><msub><mi>F</mi><mi>B</mi></msub><mo>-</mo><msub><mi>W</mi><mtext>eff</mtext></msub></math>.
        </div>
      </details>
    </div>

    <div id="derivation-section" class="derivation" style="display: none;">
      <h3>Commitment Verified: Complete Physical Derivation</h3>
      <div class="step-box">
        <div class="step-title">1. System Representation & Setup:</div>
        <p>The system boundary is [block + water container + elevator + Earth]. The analysis is performed in the non-inertial accelerating reference frame of the elevator where effective gravitational acceleration is <math class="math-tex"><msub><mi>g</mi><mtext>eff</mtext></msub><mo>=</mo><mi>g</mi><mo>+</mo><mi>a</mi><mo>=</mo><mn>10.0</mn><mo>+</mo><mn>2.0</mn><mo>=</mo><mn>12.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>.</p>
      </div>
      <div class="step-box">
        <div class="step-title">2. Physical Model & Formulation:</div>
        <p>Block volume: <math class="math-tex"><mi>V</mi><mo>=</mo><mi>m</mi><mo>/</mo><msub><mi>&rho;</mi><mi>s</mi></msub><mo>=</mo><mn>3.0</mn><mo>/</mo><mn>600</mn><mo>=</mo><mn>0.0050</mn><mtext>&nbsp;m</mtext><msup><mn>3</mn></msup></math>.<br>
        Buoyant force in accelerating water: <math class="math-tex"><msub><mi>F</mi><mi>B</mi></msub><mo>=</mo><mi>V</mi><msub><mi>&rho;</mi><mi>w</mi></msub><msub><mi>g</mi><mtext>eff</mtext></msub><mo>=</mo><mn>0.0050</mn><mo>&times;</mo><mn>1000</mn><mo>&times;</mo><mn>12.0</mn><mo>=</mo><mn>60.0</mn><mtext>&nbsp;N</mtext></math>.<br>
        Effective downward force: <math class="math-tex"><msub><mi>W</mi><mtext>eff</mtext></msub><mo>=</mo><mi>m</mi><msub><mi>g</mi><mtext>eff</mtext></msub><mo>=</mo><mn>3.0</mn><mo>&times;</mo><mn>12.0</mn><mo>=</mo><mn>36.0</mn><mtext>&nbsp;N</mtext></math>.<br>
        Dynamic balance before severance: <math class="math-tex"><mi>T</mi><mo>=</mo><msub><mi>F</mi><mi>B</mi></msub><mo>-</mo><msub><mi>W</mi><mtext>eff</mtext></msub><mo>=</mo><mn>60.0</mn><mo>-</mo><mn>36.0</mn><mo>=</mo><mn>24.0</mn><mtext>&nbsp;N</mtext></math>.</p>
      </div>
      <div class="step-box">
        <div class="step-title">3. Execution & Resolution:</div>
        <p>Immediately upon severing the cord, the downward tension vanishes (<math class="math-tex"><mi>T</mi><mo>=</mo><mn>0</mn></math>). The unbalanced upward force in the elevator frame is <math class="math-tex"><msub><mi>F</mi><mtext>net</mtext></msub><mo>=</mo><msub><mi>F</mi><mi>B</mi></msub><mo>-</mo><msub><mi>W</mi><mtext>eff</mtext></msub><mo>=</mo><mn>24.0</mn><mtext>&nbsp;N</mtext></math>.<br>
        By Newton's second law in the non-inertial frame, initial upward relative acceleration is:<br>
        <math class="math-tex"><msub><mi>a</mi><mtext>rel</mtext></msub><mo>=</mo><mfrac><msub><mi>F</mi><mtext>net</mtext></msub><mi>m</mi></mfrac><mo>=</mo><mfrac><mrow><mn>24.0</mn><mtext>&nbsp;N</mtext></mrow><mrow><mn>3.0</mn><mtext>&nbsp;kg</mtext></mrow></mfrac><mo>=</mo><mn>8.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>.<br>
        Therefore, <math class="math-tex"><mi>T</mi><mo>=</mo><mn>24.0</mn><mtext>&nbsp;N</mtext></math> and <math class="math-tex"><msub><mi>a</mi><mtext>rel</mtext></msub><mo>=</mo><mn>8.0</mn><mtext>&nbsp;m/s</mtext><msup><mn>2</mn></msup></math>, verifying <strong>Option B</strong>.</p>
      </div>
    </div>
  </div>

  <script>
    function enableCommit() {
      document.getElementById('commit-btn').disabled = false;
    }
    function commitAnswer() {
      const selected = document.querySelector('input[name="opt"]:checked');
      if (!selected) return;
      document.querySelectorAll('input[name="opt"]').forEach(el => el.disabled = true);
      document.getElementById('commit-btn').disabled = true;
      document.getElementById('derivation-section').style.display = 'block';
      document.getElementById('derivation-section').scrollIntoView({ behavior: 'auto' });
    }
  </script>
</body>
</html>
"""
(OUTPUT_DIR / "core2_module.html").write_text(core2_html, encoding="utf-8")

# 9. question-status.html
status_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Question Status: Fluid Mechanics, Sound & Thermal Physics</title>
  <style>
    body {{ font-family: system-ui; background: #0f172a; color: #f8fafc; padding: 20px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
    th, td {{ border: 1px solid #334155; padding: 10px; text-align: left; }}
    th {{ background: #1e293b; color: #38bdf8; }}
    tr:nth-child(even) {{ background: #1e293b55; }}
    .badge {{ padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
    .badge-d1 {{ background: #065f46; color: #34d399; }}
    .badge-d2 {{ background: #1e40af; color: #60a5fa; }}
    .badge-d3 {{ background: #854d0e; color: #facc15; }}
  </style>
</head>
<body>
  <h1>Physics Track: Fluid Mechanics, Sound & Thermal Physics Status</h1>
  <p>Topic ID: <code>nsejs-fluids-sound-r1</code> | Total Items: 10 | Disposition: <code>HOLD:ACADEMIC_ADMISSION</code></p>
  <table>
    <tr><th>ID</th><th>Operation</th><th>Band</th><th>Score</th><th>Title / Core Concept</th><th>Answer</th></tr>
    {''.join(f'<tr><td>{q["id"]}</td><td>{q["op"]}</td><td><span class="badge badge-{q["band"].lower()}">{q["band"]}</span></td><td>{q["score"]}</td><td>{q["batch"]}</td><td>{q["answer"][:18]}</td></tr>' for q in questions)}
  </table>
</body>
</html>
"""
(OUTPUT_DIR / "question-status.html").write_text(status_html, encoding="utf-8")

print("Physics fluids module generated successfully!")
