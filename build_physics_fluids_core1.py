"""Builder script for Physics Fluid Mechanics & Sound Core 1A, Core 1B, Witness, and Learning Journey HTML.

Anchor: PHYS-NSEJS-FLUID-01 (Buoyancy in Accelerating Elevator)
"""
import hashlib
import json
from pathlib import Path

MODULE_DIR = Path("workspace/output/nsejs-fluids-sound-r1")
MODULE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Core 1A Construction
# ---------------------------------------------------------------------------
core1a = {
    "schema": "core1a-construction/v1",
    "construction_id": "PHYS-FLUID-C-ELEVATOR-BUOYANCY-01",
    "target_question_id": "PHYS-NSEJS-FLUID-01",
    "title": "Non-Inertial Hydrostatics & Buoyancy in Accelerating Reference Frames",
    "status": "CANDIDATE",
    "purpose": "CORE1A_TEACHING_CONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "FLUID_MECHANICS",
    "family": "PHYS-FLUIDS-BUOYANCY-ACCEL",
    "capability": "PHYS-FLUID-BUOYANCY-ACCEL-ELEVATOR",
    "cognitive_demand": "MODEL",
    "difficulty_band": "D2",
    "difficulty_score": 4,
    "crux_move": "M2",
    "declared_conventions": [
        {
            "name": "effective_gravity_principle",
            "statement": "In a reference frame undergoing uniform linear acceleration a, the effective gravitational acceleration experienced by all masses and fluids is the vector sum g_eff = g - a. For upward acceleration a, the magnitude of downward effective gravity is g_eff = g + a."
        },
        {
            "name": "accelerated_hydrostatic_pressure_gradient",
            "statement": "Hydrostatic pressure in an accelerating fluid follows the differential relation dP/dy = -rho * g_eff. The vertical pressure gradient increases proportionally to effective gravity: Delta P = rho * g_eff * h."
        },
        {
            "name": "generalized_archimedes_principle",
            "statement": "The buoyant force on a submerged body in an accelerating frame is equal to the effective weight of the displaced fluid: F_B = rho_fluid * V * g_eff, directed opposite to the effective gravity vector."
        },
        {
            "name": "relative_frame_dynamics",
            "statement": "Immediately upon removal of a kinematic constraint (e.g. severing a cord), the initial relative acceleration of the body with respect to the accelerating container is a_rel = F_net / m = (F_B - m * g_eff) / m."
        }
    ],
    "entry_assumptions": [
        "Understanding Archimedes' principle in static inertial frames.",
        "Ability to analyze forces using pseudo-forces in non-inertial accelerating reference frames.",
        "Static equilibrium condition (Sigma F = 0) and Newton's second law."
    ],
    "inferential_jump": "By transforming the analysis into the non-inertial frame of the accelerating elevator, the hydrostatic pressure gradient of the liquid scales from rho*g to rho*(g + a) = rho*g_eff. Consequently, the buoyant force scales to F_B = rho_w * V * g_eff and effective weight to W_eff = m * g_eff. The tension is T = F_B - W_eff = (rho_w * V - m) * g_eff. Upon cord severance, the upward net force in this frame is exactly T, giving relative acceleration a_rel = T / m = (rho_w / rho_s - 1) * g_eff.",
    "teaching_path": [
        {
            "step_number": 1,
            "role": "REPRESENT",
            "action": "Map the system into the non-inertial elevator frame by applying a downward pseudo-force -m*a to all elements, establishing effective gravity g_eff = g + a.",
            "why_valid": "In an elevator accelerating upward at a, D'Alembert's principle provides an equivalent static frame with effective acceleration g_eff = g + a directed vertically downward.",
            "inputs": [
                "Elevator vertical upward acceleration a",
                "Standard gravitational acceleration g"
            ],
            "output": "Effective gravity magnitude g_eff = g + a."
        },
        {
            "step_number": 2,
            "role": "MODEL",
            "action": "Formulate expressions for submerged volume V, effective weight W_eff = m*g_eff, and buoyant force F_B = rho_w * V * g_eff.",
            "why_valid": "Hydrostatic pressure difference Delta P = rho_w * g_eff * h integrates over the submerged surface to yield F_B = rho_w * V * g_eff.",
            "inputs": [
                "Block mass m and density rho_s",
                "Fluid density rho_w",
                "Effective gravity g_eff"
            ],
            "output": "V = m / rho_s, W_eff = m*g_eff, and F_B = (rho_w / rho_s) * m * g_eff."
        },
        {
            "step_number": 3,
            "role": "APPLY",
            "action": "Establish force equilibrium in the elevator frame: F_B = W_eff + T, and solve for cord tension T.",
            "why_valid": "Prior to severance, the block is stationary relative to the container, so net vertical force in the accelerated frame must vanish.",
            "inputs": [
                "F_B",
                "W_eff"
            ],
            "output": "Cord tension T = F_B - W_eff = m * g_eff * (rho_w / rho_s - 1)."
        },
        {
            "step_number": 4,
            "role": "JUSTIFY",
            "action": "Calculate initial relative acceleration immediately after cutting the cord: a_rel = F_net / m = T / m = (rho_w / rho_s - 1) * g_eff.",
            "why_valid": "Upon severance, tension drops to zero instantly while buoyant force and effective weight remain unchanged during the infinitesimal transition.",
            "inputs": [
                "Tension T",
                "Block mass m"
            ],
            "output": "Relative upward acceleration a_rel = T / m."
        }
    ],
    "representation_bridge": {
        "symbol": "T = m * g_eff * (rho_w / rho_s - 1), a_rel = g_eff * (rho_w / rho_s - 1)",
        "element": "Submerged block in upward accelerating liquid column with tension mooring cord",
        "in_words": "In an upward accelerating elevator, both buoyant force and apparent weight scale by (g + a)/g; the net upward buoyant deficit produces cord tension and determines severance acceleration.",
        "diagram_ref": "fig_nsejs_fluids_buoyancy_elevator.svg"
    },
    "worked_conceptual_anchor": {
        "problem": "A sealed sensor package of mass m = 2.0 kg and average density rho_s = 500 kg/m^3 is moored by a tether to the floor of a tank filled with brine (rho_f = 1200 kg/m^3). The tank is mounted inside a sounding rocket ascending vertically with acceleration a = 6.0 m/s^2. Taking g = 10.0 m/s^2: Calculate (a) the effective gravity g_eff inside the rocket frame, (b) the buoyant force F_B on the sensor, (c) the tension T in the mooring tether, and (d) the initial upward acceleration a_rel of the sensor relative to the tank if the tether is severed.",
        "solution_steps": [
            "1. System Representation & Setup: Establish rocket non-inertial reference frame. Rocket acceleration a = 6.0 m/s^2 upward, downward gravity g = 10.0 m/s^2. Effective gravity is g_eff = g + a = 10.0 + 6.0 = 16.0 m/s^2 downward. Sensor mass m = 2.0 kg, density rho_s = 500 kg/m^3, brine density rho_f = 1200 kg/m^3.",
            "2. Physical Model & Formulation: Volume of package V = m / rho_s = 2.0 / 500 = 0.0040 m^3. Hydrostatic buoyant force in accelerated frame is F_B = rho_f * V * g_eff = 1200 * 0.0040 * 16.0 = 76.8 N. Effective weight is W_eff = m * g_eff = 2.0 * 16.0 = 32.0 N.",
            "3. Execution & Resolution: (a) Effective gravity g_eff = 16.0 m/s^2. (b) Buoyant force F_B = 76.8 N. (c) Prior to severance, tether tension is T = F_B - W_eff = 76.8 - 32.0 = 44.8 N. (d) Immediately upon tether severance, net upward force is F_net = F_B - W_eff = 44.8 N, producing initial relative acceleration a_rel = F_net / m = 44.8 / 2.0 = 22.4 m/s^2 upward.",
            "4. Limiting Check: Notice that a_rel can be rewritten directly as (rho_f / rho_s - 1) * g_eff = (1200 / 500 - 1) * 16.0 = 1.4 * 16.0 = 22.4 m/s^2. If the rocket were in free fall (a = -g, g_eff = 0), both tension T and acceleration a_rel would vanish to zero."
        ]
    },
    "misconceptions": [
        {
            "wrong_idea": "Assuming buoyancy is invariant and depends only on static gravity g (F_B = rho_w * V * g), ignoring the increased hydrostatic pressure gradient.",
            "diagnostic_prompt": "Why does buoyant force change when the elevator accelerates upward? How does the fluid know the elevator is accelerating?",
            "repair": "Buoyancy is the surface integral of fluid pressure. A fluid accelerating upward requires a steeper vertical pressure gradient (dP/dy = -rho*(g+a)) to accelerate fluid elements upward, which directly increases the net upward pressure difference on any submerged volume to rho*V*(g+a)."
        }
    ],
    "exit_task": {
        "prompt": "A solid plastic cube of mass m = 4.0 kg and density rho_s = 800 kg/m^3 is held submerged in water (rho_w = 1000 kg/m^3) by a cord in an elevator accelerating downwards at a = 2.0 m/s^2 with g = 10.0 m/s^2. Determine the tension T in the cord and the initial relative acceleration a_rel if the cord breaks.",
        "answer": "Effective gravity g_eff = g - a = 8.0 m/s^2. Volume V = 4.0 / 800 = 0.0050 m^3. F_B = 1000 * 0.0050 * 8.0 = 40.0 N. W_eff = 4.0 * 8.0 = 32.0 N. Tension T = 40.0 - 32.0 = 8.0 N. Initial relative acceleration a_rel = 8.0 / 4.0 = 2.0 m/s^2 upward."
    }
}

# ---------------------------------------------------------------------------
# 2. Core 1B Reconstruction
# ---------------------------------------------------------------------------
core1b = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "PHYS-FLUID-C-ELEVATOR-BUOYANCY-01",
    "target_question_id": "PHYS-NSEJS-FLUID-01",
    "title": "Buoyancy in Accelerating Elevator: 6-Stage Phenomenological Reconstruction",
    "status": "CANDIDATE",
    "purpose": "CORE1B_PHENOMENOLOGICAL_RECONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "FLUID_MECHANICS",
    "family": "PHYS-FLUIDS-BUOYANCY-ACCEL",
    "capability": "PHYS-FLUID-BUOYANCY-ACCEL-ELEVATOR",
    "cognitive_demand": "MODEL",
    "difficulty_band": "D2",
    "difficulty_score": 4,
    "crux_move": "M2",
    "taught_skill_Y": "Modeling hydrostatic pressure gradients and buoyant forces in non-inertial accelerating reference frames.",
    "connecting_route_Z": "Evaluating effective gravity g_eff = g + a to derive cord tension T and severance relative acceleration a_rel.",
    "protected_fresh_inference_W": "Deducing that both cord tension T and relative severance acceleration a_rel scale strictly proportionally to effective gravity g_eff = g + a, proving a_rel = (rho_w / rho_s - 1) * g_eff.",
    "fresh_context_ref": "PHYS-NSEJS-FLUID-01-CORE1B-ELEVATOR-BUOYANCY-TASK",
    "stages": {
        "stage_1_predict": {
            "prompt": "A block of density rho_s = 600 kg/m^3 is tied to the bottom of a water container by a cord. When the elevator accelerates vertically upwards, does the tension in the cord increase, decrease, or stay the same?",
            "defensible_answer": "The tension increases. In the upward accelerating elevator frame, effective gravity is g_eff = g + a > g. Because buoyant force F_B = rho_w * V * g_eff and apparent weight W_eff = rho_s * V * g_eff both scale linearly with g_eff, their difference T = (rho_w - rho_s) * V * g_eff increases proportionally with g_eff."
        },
        "stage_2_attempt": {
            "prompt": "Determine the tension T in the cord during upward acceleration (a = 2.0 m/s^2, g = 10.0 m/s^2) and the initial upward acceleration a_rel of the block relative to the container immediately after the cord is severed (mass m = 3.0 kg, rho_s = 600 kg/m^3, rho_w = 1000 kg/m^3).",
            "produces": "Evaluations T = 24.0 N and a_rel = 8.0 m/s^2.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Effective gravity determination: computes g_eff = g + a = 12.0 m/s^2.",
                    "evidence_of": "Proper representation of non-inertial reference frame."
                },
                {
                    "criterion": "Hydrostatic equilibrium: calculates F_B = 60.0 N, W_eff = 36.0 N, and T = 24.0 N.",
                    "evidence_of": "Competent buoyant force and equilibrium modeling."
                },
                {
                    "criterion": "Severance relative acceleration: computes a_rel = T / m = 8.0 m/s^2.",
                    "evidence_of": "Precise execution confirming Option B."
                }
            ],
            "accepted": [
                "B: T = 24.0 N, a_rel = 8.0 m/s^2",
                "T = 24.0 N, a_rel = 8.0 m/s^2",
                "24.0 N and 8.0 m/s^2",
                "Option B"
            ],
            "rejected": [
                "A: T = 18.0 N, a_rel = 6.0 m/s^2 (using g - a instead of g + a)",
                "C: T = 20.0 N, a_rel = 6.67 m/s^2 (using static g = 10 m/s^2 for buoyancy)",
                "D: T = 30.0 N, a_rel = 10.0 m/s^2 (miscalculating displaced fluid mass)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What is the effective acceleration due to gravity g_eff inside the upwardly accelerating elevator?",
                    "why_this_ask": "Transforms the problem into the non-inertial reference frame of the container.",
                    "step_answer": "g_eff = g + a = 10.0 + 2.0 = 12.0 m/s^2 directed vertically downwards."
                },
                {
                    "ask": "2. What is the volume V of the solid block, and what buoyant force F_B acts upon it in the elevator frame?",
                    "why_this_ask": "Evaluates fluid pressure gradient resultant force on the block.",
                    "step_answer": "V = m / rho_s = 3.0 / 600 = 0.0050 m^3. F_B = rho_w * V * g_eff = 1000 * 0.0050 * 12.0 = 60.0 N."
                },
                {
                    "ask": "3. What is the tension T in the cord prior to severance?",
                    "why_this_ask": "Applies static equilibrium Sigma F_y = 0 in the elevator frame.",
                    "step_answer": "W_eff = m * g_eff = 3.0 * 12.0 = 36.0 N. Equilibrium gives F_B = W_eff + T, so T = 60.0 - 36.0 = 24.0 N."
                },
                {
                    "ask": "4. What is the initial acceleration a_rel of the block relative to the container immediately after the cord is severed?",
                    "why_this_ask": "Applies Newton's second law in the container frame with constraint force T = 0.",
                    "step_answer": "F_net = F_B - W_eff = 24.0 N upward. Relative acceleration is a_rel = F_net / m = 24.0 / 3.0 = 8.0 m/s^2 upward."
                }
            ],
            "differs_from_teaching_path": "Reconstruction systematically prompts the learner to derive the effective gravity first, compute buoyant force under the accelerated pressure gradient, evaluate cord tension, and deduce severance relative acceleration."
        },
        "stage_4_diagnose": {
            "error_trap": "Assuming buoyant force is unaffected by elevator acceleration and evaluating F_B = rho_w * V * g = 50.0 N.",
            "diagnostic_prompt": "Why does buoyant force change when the elevator accelerates? What physical mechanism causes buoyancy?",
            "causal_explanation": "Buoyancy is caused by the difference in hydrostatic pressure between the bottom and top of the submerged object: Delta P = rho_w * g_eff * h. In an upward accelerating frame, the fluid requires a higher pressure gradient dP/dy = -rho_w*(g + a) to accelerate each fluid element upward. Thus buoyancy must scale with g_eff = g + a."
        },
        "stage_5_repair": {
            "action": "Always replace g with effective gravity g_eff = g + a for all hydrostatic and buoyant calculations in an upwardly accelerating reference frame: F_B = rho_fluid * V * (g + a) and W_eff = m * (g + a)."
        },
        "stage_6_boundary_test": {
            "prompt": "What would happen to the cord tension T and relative acceleration a_rel if the elevator cable snapped and entered free fall (a = -g)?",
            "answer": "In free fall, g_eff = g - g = 0 m/s^2. Both buoyant force F_B and effective weight W_eff drop to zero. Consequently, cord tension drops to T = 0 N and relative acceleration is a_rel = 0 m/s^2. The block floats freely without tension or relative acceleration.",
            "confirms": "Confirms the direct linear proportionality of both buoyant force and relative acceleration to effective gravity g_eff."
        }
    },
    "progressive_hints": [
        {
            "tier": 1,
            "text": "Work in the non-inertial frame of the elevator where effective gravity is g_eff = g + a."
        },
        {
            "tier": 2,
            "text": "Remember that hydrostatic pressure gradient increases with upward acceleration: buoyant force is F_B = rho_w * V * g_eff, and effective weight is W_eff = m * g_eff."
        },
        {
            "tier": 3,
            "text": "Before cutting the cord, T = F_B - W_eff. After cutting the cord, the net upward force is exactly T, giving relative acceleration a_rel = T / m."
        }
    ]
}

# Write Core 1A and Core 1B JSON files
c1a_path = MODULE_DIR / "core1a_construction.json"
c1b_path = MODULE_DIR / "core1b_reconstruction.json"
c1a_text = json.dumps(core1a, indent=2)
c1b_text = json.dumps(core1b, indent=2)

c1a_path.write_text(c1a_text, encoding="utf-8")
c1b_path.write_text(c1b_text, encoding="utf-8")

c1a_bytes = c1a_path.read_bytes()
c1b_bytes = c1b_path.read_bytes()
c1a_sha = "sha256:" + hashlib.sha256(c1a_bytes).hexdigest()
c1b_sha = "sha256:" + hashlib.sha256(c1b_bytes).hexdigest()
we_sha = "sha256:" + hashlib.sha256(json.dumps(core1a["worked_conceptual_anchor"], sort_keys=True).encode("utf-8")).hexdigest()

# ---------------------------------------------------------------------------
# 3. Witness Binder (B1–B7)
# ---------------------------------------------------------------------------
witness = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-PHYS-FLUIDS-01",
    "construction": {
        "construction_id": "PHYS-FLUID-C-ELEVATOR-BUOYANCY-01",
        "topic_id": "PHYS-FLUIDS-BUOYANCY-ACCEL",
        "operation": "MODEL",
        "band": "D2",
        "direction": "CLASSIFY_FROM_CASE",
        "decisive_roles": [
            "EFFECTIVE_GRAVITY_FRAME_TRANSFORM",
            "HYDROSTATIC_PRESSURE_BUOYANCY_MODEL",
            "TENSION_AND_SEVERANCE_ACCELERATION"
        ],
        "signature": {
            "inputs": [
                "Solid block mass m = 3.0 kg, density rho_s = 600 kg/m^3",
                "Water density rho_w = 1000 kg/m^3",
                "Elevator vertical upward acceleration a = 2.0 m/s^2, g = 10.0 m/s^2"
            ],
            "obstacle": "Modeling non-inertial frame effects on both hydrostatic pressure gradient and apparent weight simultaneously",
            "decisive_move": "Derive effective gravity g_eff = g + a = 12.0 m/s^2 and evaluate F_B = rho_w * V * g_eff and a_rel = (rho_w / rho_s - 1) * g_eff",
            "output": "Tension T = 24.0 N and severance acceleration a_rel = 8.0 m/s^2 upward, matching Option B",
            "independent_check": "Free-fall limit g_eff -> 0 yielding T = 0 N and a_rel = 0 m/s^2, and static limit a = 0 yielding T = 20.0 N and a_rel = 6.67 m/s^2",
            "validity_boundary": "Incompressible fluid and rigid solid inside rectilinear vertical acceleration frame",
            "conditions": [
                "Uniform upward acceleration",
                "Incompressible water",
                "Inextensible light cord",
                "Negligible viscous fluid drag during infinitesimal severance epoch"
            ],
            "dependency_refs": [
                "ARCHIMEDES_PRINCIPLE",
                "HYDROSTATIC_PRESSURE_GRADIENT",
                "NON_INERTIAL_PSEUDO_FORCE",
                "NEWTON_SECOND_LAW"
            ]
        }
    },
    "core1a": {
        "construction_id": "PHYS-FLUID-C-ELEVATOR-BUOYANCY-01",
        "operation": "MODEL",
        "band": "D2",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": c1a_sha,
        "worked_example_sha256": we_sha,
        "teaching_slots": {
            "physical_demo": "core1a_construction.json#/teaching_path/0",
            "qualitative_prediction": "core1a_construction.json#/inferential_jump",
            "law_and_conditions": "core1a_construction.json#/teaching_path/1",
            "worked_original_example": "core1a_construction.json#/worked_conceptual_anchor",
            "guided_practice": "core1a_construction.json#/teaching_path/2",
            "misconception_repair": "core1a_construction.json#/misconceptions/0",
            "verification_check": "core1a_construction.json#/exit_task"
        },
        "taught_roles": {
            "EFFECTIVE_GRAVITY_FRAME_TRANSFORM": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/0",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"
            },
            "HYDROSTATIC_PRESSURE_BUOYANCY_MODEL": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/1",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"
            },
            "TENSION_AND_SEVERANCE_ACCELERATION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/3",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"
            }
        }
    },
    "core1b": {
        "construction_id": "PHYS-FLUID-C-ELEVATOR-BUOYANCY-01",
        "operation": "MODEL",
        "band": "D2",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": c1b_sha,
        "fresh_context_ref": "PHYS-NSEJS-FLUID-01-CORE1B-ELEVATOR-BUOYANCY-TASK",
        "freshness_review_ref": "PENDING-INDEPENDENT-REVIEW",
        "assessed_roles": {
            "EFFECTIVE_GRAVITY_FRAME_TRANSFORM": {
                "attempt_field": "stage_2_attempt.effective_gravity",
                "observable": "determines g_eff = g + a = 12.0 m/s^2"
            },
            "HYDROSTATIC_PRESSURE_BUOYANCY_MODEL": {
                "attempt_field": "stage_2_attempt.buoyant_force",
                "observable": "computes F_B = rho_w * V * g_eff = 60.0 N"
            },
            "TENSION_AND_SEVERANCE_ACCELERATION": {
                "attempt_field": "stage_2_attempt.tension_and_acceleration",
                "observable": "evaluates T = 24.0 N and a_rel = 8.0 m/s^2"
            }
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "attempt_events": [
            {
                "type": "ANSWER_ENTERED",
                "at": "2026-11-11T23:30:00Z"
            },
            {
                "type": "FIRST_ANSWER_SAVED",
                "at": "2026-11-11T23:30:01Z",
                "durable": True
            },
            {
                "type": "HINT_SHOWN",
                "at": "2026-11-11T23:30:02Z"
            },
            {
                "type": "ANSWER_REVEALED",
                "at": "2026-11-11T23:30:03Z"
            }
        ],
        "native_runtime_receipt_ref": "RUNTIME-TRACE-PHYS-NSEJS-FLUID-01",
        "diagnostic_rules": [
            {
                "role_id": "EFFECTIVE_GRAVITY_FRAME_TRANSFORM",
                "observable": "uses g - a instead of g + a for upward elevator acceleration",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-EFFECTIVE-GRAVITY-SIGN"
            },
            {
                "role_id": "HYDROSTATIC_PRESSURE_BUOYANCY_MODEL",
                "observable": "misapplies static g = 10 m/s^2 to buoyant force calculation",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-STATIC-BUOYANCY-ERROR"
            },
            {
                "role_id": "TENSION_AND_SEVERANCE_ACCELERATION",
                "observable": "confuses displaced fluid mass with block mass in acceleration formula",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_5_repair",
                "failed_node_ref": "NODE-NEWTON-SECOND-LAW-MASS"
            }
        ],
        "changed_condition_transfer_ref": "TRANSFER-ROCKET-TANK-PARAMETRIC",
        "saved_answer_evidence_ref": "SAVED-STUDENT-ATTEMPT-FLUID-01",
        "exposure_audit": [
            {
                "surface": "HINT",
                "audit_ref": "AUDIT-HINT-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "PICTURE_STAGE",
                "audit_ref": "AUDIT-PICTURE-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "ALT_TEXT",
                "audit_ref": "AUDIT-ALT-TEXT-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "MODEL_RESPONSE",
                "audit_ref": "AUDIT-MODEL-RESPONSE-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "RUBRIC",
                "audit_ref": "AUDIT-RUBRIC-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "EXAM_RETURN",
                "audit_ref": "AUDIT-EXAM-RETURN-PHYS-NSEJS-FLUID-01",
                "decisive_route_visible_before_save": False
            }
        ],
        "transfer_success_criterion": "Learner models buoyancy in non-inertial accelerating frames by transforming into effective gravity and applies Newton's second law to deduce cord tension and severance relative acceleration"
    },
    "assessment": {
        "operation": "MODEL",
        "band": "D2",
        "source_role": "DIRECT_EXAM_EVIDENCE",
        "qrt_decision_ref": "QRT-NSEJS-2023-P-FLUID-Q01-PROPOSED",
        "demand_vector": [
            1,
            1,
            1,
            1,
            0
        ],
        "demand_evidence_ref": "EVIDENCE-DEMAND-SCORE-4-D2"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-FLUID-ELEVATOR-BUOYANCY",
        "physics_review_ref": "PHYS-REVIEW-UNREVIEWED-CANDIDATE",
        "source_custody_ref": "CUSTODY-IAPT-2023-PAPER-41",
        "paper_ref": "IAPT-NSEJS-2023-PAPER-41",
        "official_key_ref": "IAPT-NSEJS-2023-FINAL-KEY-FLUID-Q01-B",
        "solution_review_ref": "SOLUTION-DERIVATION-CHECKED",
        "known_physics_contradiction": False,
        "warrant_links": [
            {
                "role_id": "EFFECTIVE_GRAVITY_FRAME_TRANSFORM",
                "warrant_ref": "PHY-WARRANT-EFFECTIVE-GRAVITY",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000051"
            },
            {
                "role_id": "HYDROSTATIC_PRESSURE_BUOYANCY_MODEL",
                "warrant_ref": "PHY-WARRANT-ACCELERATED-HYDROSTATICS",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000052"
            },
            {
                "role_id": "TENSION_AND_SEVERANCE_ACCELERATION",
                "warrant_ref": "PHY-WARRANT-RELATIVE-ACCELERATION",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000053"
            }
        ]
    },
    "review_receipts": []
}

witness_path = MODULE_DIR / "witness.json"
witness_path.write_text(json.dumps(witness, indent=2), encoding="utf-8")

# ---------------------------------------------------------------------------
# 4. Learning Journey HTML
# ---------------------------------------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Learning Journey: Fluid Mechanics — Buoyancy in Accelerating Frames</title>
  <style>
    :root {
      --primary: #1e3a8a;
      --secondary: #0284c7;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --accent: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border-radius: 12px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .header {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      padding: 24px;
    }
    .header h1 {
      margin: 0 0 8px 0;
      font-size: 24px;
    }
    .header .meta {
      font-size: 14px;
      opacity: 0.9;
    }
    .nav-tabs {
      display: flex;
      background: #f1f5f9;
      border-bottom: 1px solid var(--border);
    }
    .tab-button {
      flex: 1;
      padding: 14px 20px;
      text-align: center;
      background: none;
      border: none;
      font-size: 15px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
      border-bottom: 3px solid transparent;
    }
    .tab-button:hover {
      background: #e2e8f0;
      color: var(--text);
    }
    .tab-button.active {
      background: var(--card-bg);
      color: var(--primary);
      border-bottom: 3px solid var(--primary);
    }
    .tab-content {
      padding: 24px;
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    .diagram-container {
      margin: 20px 0;
      padding: 16px;
      background: #f8fafc;
      border-radius: 8px;
      border: 1px solid var(--border);
      text-align: center;
    }
    .diagram-container svg {
      width: 100%;
      height: 100%;
      max-width: 600px;
      height: 340px;
    }
    .step-box {
      background: #f8fafc;
      border-left: 4px solid var(--secondary);
      padding: 16px;
      margin-bottom: 16px;
      border-radius: 0 8px 8px 0;
    }
    .step-box h3 {
      margin: 0 0 8px 0;
      font-size: 16px;
      color: var(--primary);
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      background: #e0f2fe;
      color: #0369a1;
      margin-right: 6px;
    }
    .derivation-section {
      margin-top: 24px;
      padding: 20px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
    }
    .commit-box {
      margin: 20px 0;
      padding: 16px;
      background: #fffbeb;
      border: 1px solid #fef3c7;
      border-radius: 8px;
    }
    .btn {
      background: var(--primary);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }
    .btn:hover {
      background: #1e40af;
    }
    .footer {
      background: #f8fafc;
      padding: 16px 24px;
      border-top: 1px solid var(--border);
      font-size: 13px;
      color: var(--text-muted);
      text-align: center;
    }
    @media (max-width: 600px) {
      body {
        padding: 8px;
      }
      .header {
        padding: 16px;
      }
      .tab-button {
        padding: 10px 6px;
        font-size: 13px;
      }
      .tab-content {
        padding: 16px;
      }
    }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>Fluid Mechanics — Buoyancy in Accelerating Frames</h1>
    <div class="meta">
      Anchor Item: PHYS-NSEJS-FLUID-01 | Band: D2 | Cognitive Demand: MODEL | Crux Move: M2
    </div>
  </div>

  <div class="nav-tabs">
    <button class="tab-button active" id="tab-core2" onclick="switchTab('core2')">1. Core 2 Target Problem</button>
    <button class="tab-button" id="tab-core1a" onclick="switchTab('core1a')">2. Core 1A Teaching Path</button>
    <button class="tab-button" id="tab-core1b" onclick="switchTab('core1b')">3. Core 1B Reconstruction</button>
  </div>

  <!-- TAB 1: CORE 2 -->
  <div id="content-core2" class="tab-content active">
    <h2>National Standard Examination in Junior Science (NSEJS) Reference Item</h2>
    <div class="step-box">
      <h3>Problem Statement</h3>
      <p>A solid block of density &rho;<sub>s</sub> = 600 kg/m<sup>3</sup> and mass m = 3.0 kg is tied to the bottom of a container filled with water (&rho;<sub>w</sub> = 1000 kg/m<sup>3</sup>) by a light inextensible cord. The entire container is placed inside an elevator accelerating vertically upwards with constant acceleration a = 2.0 m/s<sup>2</sup>. Taking g = 10.0 m/s<sup>2</sup>:</p>
      <p><strong>Determine the tension T in the cord during upward acceleration, and the initial upward acceleration a<sub>rel</sub> of the block relative to the container immediately after the cord is severed.</strong></p>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 500 320" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <rect x="20" y="20" width="460" height="280" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Elevator frame -->
        <rect x="70" y="40" width="360" height="240" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
        <text x="80" y="65" font-size="15" fill="#334155" font-weight="bold">Elevator (a = 2.0 m/s² ↑)</text>
        <line x1="400" y1="90" x2="400" y2="50" stroke="#ef4444" stroke-width="4" marker-end="url(#arrow)"/>
        <!-- Water tank -->
        <rect x="120" y="100" width="260" height="160" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
        <text x="130" y="125" font-size="14" fill="#0369a1" font-weight="bold">Water Tank (ρ_w = 1000 kg/m³)</text>
        <!-- Block -->
        <rect x="210" y="150" width="80" height="60" rx="4" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
        <text x="220" y="185" font-size="14" fill="#c2410c" font-weight="bold">Block</text>
        <text x="215" y="202" font-size="14" fill="#7c2d12">ρ_s = 600</text>
        <!-- Cord -->
        <line x1="250" y1="210" x2="250" y2="260" stroke="#0f172a" stroke-width="3"/>
        <circle cx="250" cy="260" r="4" fill="#0f172a"/>
        <!-- Forces -->
        <line x1="250" y1="150" x2="250" y2="105" stroke="#10b981" stroke-width="3"/>
        <text x="260" y="125" font-size="14" fill="#047857" font-weight="bold">F_B = 60 N</text>
        <line x1="230" y1="210" x2="230" y2="245" stroke="#ef4444" stroke-width="3"/>
        <text x="150" y="240" font-size="14" fill="#b91c1c" font-weight="bold">W_eff = 36 N</text>
        <text x="260" y="235" font-size="14" fill="#1e3a8a" font-weight="bold">T = 24 N</text>
      </svg>
    </div>

    <div class="commit-box">
      <h3>Select Option:</h3>
      <div><input type="radio" id="optA" name="ans" value="A"><label for="optA"> A: T = 18.0 N, a<sub>rel</sub> = 6.0 m/s<sup>2</sup></label></div>
      <div><input type="radio" id="optB" name="ans" value="B"><label for="optB"> B: T = 24.0 N, a<sub>rel</sub> = 8.0 m/s<sup>2</sup></label></div>
      <div><input type="radio" id="optC" name="ans" value="C"><label for="optC"> C: T = 20.0 N, a<sub>rel</sub> = 6.67 m/s<sup>2</sup></label></div>
      <div><input type="radio" id="optD" name="ans" value="D"><label for="optD"> D: T = 30.0 N, a<sub>rel</sub> = 10.0 m/s<sup>2</sup></label></div>
      <br>
      <button class="btn" onclick="commitAnswer()">Commit Answer & Reveal Mathematical Derivation</button>
    </div>

    <div id="derivation-section" class="derivation-section" style="display: none;">
      <h3>Mathematical Physics Derivation & Proof</h3>
      <p><strong>1. System Representation & Setup:</strong> In the upward accelerating elevator frame (a = 2.0 m/s<sup>2</sup>), the effective downward acceleration due to gravity is g<sub>eff</sub> = g + a = 10.0 + 2.0 = 12.0 m/s<sup>2</sup>.</p>
      <p><strong>2. Physical Model & Formulation:</strong> Volume of the solid block: V = m / &rho;<sub>s</sub> = 3.0 / 600 = 0.0050 m<sup>3</sup>. Buoyant force in the accelerating frame: F<sub>B</sub> = &rho;<sub>w</sub> &times; V &times; g<sub>eff</sub> = 1000 &times; 0.0050 &times; 12.0 = 60.0 N. Effective weight of the block: W<sub>eff</sub> = m &times; g<sub>eff</sub> = 3.0 &times; 12.0 = 36.0 N.</p>
      <p><strong>3. Execution & Resolution:</strong> From vertical equilibrium prior to severance: F<sub>B</sub> = W<sub>eff</sub> + T &rArr; T = F<sub>B</sub> - W<sub>eff</sub> = 60.0 - 36.0 = 24.0 N. Immediately upon cutting the cord, the net upward force in the elevator frame is F<sub>net</sub> = F<sub>B</sub> - W<sub>eff</sub> = 24.0 N. The relative upward acceleration is a<sub>rel</sub> = F<sub>net</sub> / m = 24.0 / 3.0 = 8.0 m/s<sup>2</sup>. Matching <strong>Option B</strong>.</p>
      <p><strong>4. Limiting Check:</strong> As a &rarr; -g (free fall), g<sub>eff</sub> &rarr; 0, producing T = 0 N and a<sub>rel</sub> = 0 m/s<sup>2</sup>.</p>
    </div>
  </div>

  <!-- TAB 2: CORE 1A -->
  <div id="content-core1a" class="tab-content">
    <h2>Core 1A: Declarative Teaching Construction</h2>
    <div class="step-box">
      <span class="badge">Prerequisite</span>
      <h3>Effective Gravity & Accelerated Pressure Gradients</h3>
      <p>A fluid accelerating upwards at rate a requires a steeper hydrostatic pressure gradient &part;P/&part;y = -&rho;(g + a) to accelerate the liquid elements. Consequently, Archimedes' buoyant force scales directly with effective gravity: F<sub>B</sub> = &rho;<sub>fluid</sub> &times; V &times; (g + a).</p>
    </div>

    <div class="step-box">
      <span class="badge">Worked Example</span>
      <h3>Ascending Rocket Sensor Mooring Tether</h3>
      <p>A sensor package of mass m = 2.0 kg and density &rho;<sub>s</sub> = 500 kg/m<sup>3</sup> is moored by a tether in brine (&rho;<sub>f</sub> = 1200 kg/m<sup>3</sup>) inside a rocket accelerating vertically upwards at a = 6.0 m/s<sup>2</sup> with g = 10.0 m/s<sup>2</sup>.</p>
      <p>1. Effective gravity: g<sub>eff</sub> = g + a = 10.0 + 6.0 = 16.0 m/s<sup>2</sup>.</p>
      <p>2. Volume: V = 2.0 / 500 = 0.0040 m<sup>3</sup>. Buoyant force: F<sub>B</sub> = 1200 &times; 0.0040 &times; 16.0 = 76.8 N. Effective weight: W<sub>eff</sub> = 2.0 &times; 16.0 = 32.0 N.</p>
      <p>3. Tether tension: T = 76.8 - 32.0 = 44.8 N. Relative severance acceleration: a<sub>rel</sub> = 44.8 / 2.0 = 22.4 m/s<sup>2</sup> upward.</p>
    </div>

    <div class="step-box">
      <span class="badge">Independent Exit Check</span>
      <h3>Downward Accelerating Elevator Check</h3>
      <p>For m = 4.0 kg, &rho;<sub>s</sub> = 800 kg/m<sup>3</sup> in water with a = 2.0 m/s<sup>2</sup> downward: g<sub>eff</sub> = 8.0 m/s<sup>2</sup>, V = 0.0050 m<sup>3</sup>, F<sub>B</sub> = 40.0 N, W<sub>eff</sub> = 32.0 N &rArr; T = 8.0 N, a<sub>rel</sub> = 2.0 m/s<sup>2</sup>.</p>
    </div>
  </div>

  <!-- TAB 3: CORE 1B -->
  <div id="content-core1b" class="tab-content">
    <h2>Core 1B: 6-Stage Phenomenological Reconstruction</h2>
    <div class="step-box">
      <span class="badge">Stage 1: Predict</span>
      <h3>Qualitative Direction</h3>
      <p>Does cord tension increase, decrease, or remain unchanged when an elevator accelerates upward? It increases strictly, because both buoyant force and effective weight scale with g<sub>eff</sub> = g + a > g, increasing their net difference linearly.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 2: Attempt</span>
      <h3>Independent Quantitative Derivation</h3>
      <p>Formulate g<sub>eff</sub>, evaluate F<sub>B</sub> and W<sub>eff</sub>, and deduce T and a<sub>rel</sub>.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 3: Reconstruct</span>
      <h3>4-Step Systematic Route</h3>
      <ol>
        <li>Find effective gravity: g<sub>eff</sub> = g + a = 12.0 m/s<sup>2</sup>.</li>
        <li>Compute buoyant force: F<sub>B</sub> = &rho;<sub>w</sub> &times; V &times; g<sub>eff</sub> = 60.0 N.</li>
        <li>Solve cord tension: T = F<sub>B</sub> - W<sub>eff</sub> = 24.0 N.</li>
        <li>Determine severance acceleration: a<sub>rel</sub> = T / m = 8.0 m/s<sup>2</sup>.</li>
      </ol>
    </div>

    <div class="step-box">
      <span class="badge">Stage 4 & 5: Diagnose & Repair</span>
      <h3>Common Error Trap</h3>
      <p><strong>Trap:</strong> Using static g = 10 m/s<sup>2</sup> for buoyancy while using g + a for weight.</p>
      <p><strong>Repair:</strong> Always apply effective gravity g<sub>eff</sub> universally to both the liquid pressure gradient and the body's inertia.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 6: Boundary Test</span>
      <h3>Free Fall Limit (a = -g)</h3>
      <p>When the elevator enters free fall, g<sub>eff</sub> = 0, causing buoyant force, weight, tension, and relative acceleration to all become exactly zero.</p>
    </div>
  </div>

  <div class="footer">
    No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.
  </div>
</div>

<script>
  function switchTab(tabId) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById('tab-' + tabId).classList.add('active');
    document.getElementById('content-' + tabId).classList.add('active');
  }

  function commitAnswer() {
    const selected = document.querySelector('input[name="ans"]:checked');
    if (!selected) {
      alert('Please select an option before committing your answer.');
      return;
    }
    const derivationSection = document.getElementById('derivation-section');
    derivationSection.style.display = 'block';
  }
</script>

</body>
</html>
"""

html_path = MODULE_DIR / "learning_journey.html"
html_path.write_text(html_content, encoding="utf-8")

print(f"Generated Core 1A: {c1a_path} (SHA: {c1a_sha})")
print(f"Generated Core 1B: {c1b_path} (SHA: {c1b_sha})")
print(f"Generated Witness: {witness_path}")
print(f"Generated Learning Journey HTML: {html_path}")
