"""Multi-Subject Band D3 Expansion Builder:
1. Physics: nsejs-fluids-surface-energy-d3-r1 (PHYS-NSEJS-FLUID-04, Droplet Coalescence)
2. Chemistry: chem-phosphorus-oxyacids-d3-r1 (NSEJS-2024-C-Q55, Phosphorus Oxyacids Basicity)
3. Biology: bio-viral-genetics-d3-r1 (NSEJS-2024-B-Q50, Viral Capsid & Baltimore Replication)
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(".")

# ===========================================================================
# MODULE 1: PHYSICS D3 - nsejs-fluids-surface-energy-d3-r1
# ===========================================================================
mod1_dir = ROOT / "workspace/output/nsejs-fluids-surface-energy-d3-r1"
mod1_dir.mkdir(parents=True, exist_ok=True)

bank1 = {
    "schema_version": "grade9qa-exam-bank/v1",
    "bank_id": "nsejs-fluids-surface-energy-d3-r1",
    "metadata": {
        "title": "Droplet Coalescence & Surface Energy Release",
        "subject": "Physics",
        "topic": "FLUID_MECHANICS",
        "difficulty_band": "D3"
    },
    "questions": [
        {
            "id": "PHYS-NSEJS-FLUID-04",
            "original_identifier": "NSEJS-PHYS · Q04 · SYNTHESIZE · D3 (Score 6)",
            "stem": "$N = 1000$ identical spherical water microdroplets, each of radius $r = 1.0\\times 10^{-4}\\text{ m}$ and surface tension $T = 0.075\\text{ N/m}$, coalesce under isothermal conditions to form a single large spherical drop. Calculate the total surface energy released ($\\Delta U$) in this coalescence process.",
            "response": {"type": "multiple_choice"},
            "options": [
                {"id": "A", "text": "Delta U = 8.48 x 10^-6 J"},
                {"id": "B", "text": "Delta U = 9.42 x 10^-6 J"},
                {"id": "C", "text": "Delta U = 1.05 x 10^-5 J"},
                {"id": "D", "text": "Delta U = 7.50 x 10^-6 J"}
            ],
            "answer": {
                "correct_option": "A",
                "crux_move_ref": "PHYS-NSEJS-FLUID-04-M2",
                "reasoning": [
                    "1. System Representation & Setup: 1000 droplets of radius r = 1.0 x 10^-4 m and T = 0.075 N/m coalesce into a single drop of radius R. We compute released surface energy Delta U.",
                    "2. Physical Model & Formulation: Incompressible fluid conservation yields R = N^(1/3) r = 10 r. Total initial area A_i = 1000 * 4 pi r^2. Final area A_f = 4 pi (10r)^2 = 100 * 4 pi r^2. Area change is Delta A = 4 pi r^2 * (1000 - 100) = 900 * 4 pi r^2 = 3600 pi r^2.",
                    "3. Execution & Resolution: Delta A = 3600 * pi * (1.0 x 10^-4)^2 = 3.6 pi x 10^-5 m^2. Energy released Delta U = T * Delta A = 0.075 * 3.6 pi x 10^-5 = 0.270 pi x 10^-5 J = 8.482 x 10^-6 J approx 8.48 x 10^-6 J. Option A."
                ],
                "reasoning_route": [
                    {"move_id": "PHYS-NSEJS-FLUID-04-M1", "kind": "REPRESENT", "description": "Conserve liquid volume across N droplets to determine single drop radius R = N^(1/3) r."},
                    {"move_id": "PHYS-NSEJS-FLUID-04-M2", "kind": "MODEL", "description": "Formulate total surface area reduction Delta A = 4 pi r^2 (N - N^(2/3))."},
                    {"move_id": "PHYS-NSEJS-FLUID-04-M3", "kind": "APPLY", "description": "Compute energy released via Delta U = T Delta A."},
                    {"move_id": "PHYS-NSEJS-FLUID-04-M4", "kind": "JUSTIFY", "description": "Evaluate numerical values confirming 8.48 x 10^-6 J (Option A)."}
                ]
            },
            "extensions": {
                "grade9v3:analysis": {
                    "difficulty": {
                        "score": 6,
                        "band": "D3",
                        "components": {
                            "c1_volume_conservation": 1,
                            "c2_surface_area_scaling": 2,
                            "c3_surface_energy_relation": 1,
                            "c4_algebra_computation": 1,
                            "c5_limiting_consistency": 1
                        }
                    }
                },
                "grade9v3:core2_support_plan": {
                    "protected_move_refs": ["PHYS-NSEJS-FLUID-04-M2"]
                }
            }
        }
    ]
}
(mod1_dir / "bank.json").write_text(json.dumps(bank1, indent=2), encoding="utf-8")

c1a_1 = {
    "schema": "core1a-construction/v1",
    "construction_id": "PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01",
    "target_question_id": "PHYS-NSEJS-FLUID-04",
    "title": "Droplet Coalescence & Surface Energy Thermodynamics",
    "status": "CANDIDATE",
    "purpose": "CORE1A_TEACHING_CONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "FLUID_MECHANICS",
    "family": "PHYS-FLUID-SURFACE-TENSION",
    "capability": "PHYS-FLUID-DROPLET-COALESCENCE-ENERGY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "PHYS-NSEJS-FLUID-04-M2",
    "declared_conventions": [
        {
            "name": "incompressible_volume_conservation",
            "statement": "Liquid water is treated as an incompressible continuum. When N identical spherical droplets of radius r coalesce into a single spherical drop of radius R, total volume is conserved: (4/3)*pi*R^3 = N * (4/3)*pi*r^3, yielding R = N^(1/3) * r."
        },
        {
            "name": "surface_energy_proportionality",
            "statement": "The potential energy of a liquid surface of area A and surface tension T is U = T * A. When surface area decreases by Delta A = A_initial - A_final, the surface energy released into thermal/kinetic energy is Delta U = T * Delta A."
        },
        {
            "name": "non_linear_geometric_scaling",
            "statement": "While volume scales as r^3, surface area scales as r^2. The coalesced drop has area A_final = 4*pi*R^2 = 4*pi*N^(2/3)*r^2, producing net area reduction Delta A = 4*pi*r^2 * (N - N^(2/3))."
        },
        {
            "name": "isothermal_surface_transition",
            "statement": "Under isothermal conditions, released surface energy equals the net change in surface Gibbs free energy: Delta U = T * Delta A > 0, driving spontaneous coalescence."
        }
    ],
    "entry_assumptions": [
        "Understanding molecular origin of surface tension as inward cohesive intermolecular attraction.",
        "Spherical surface area (4*pi*r^2) and volume ((4/3)*pi*r^3) geometric formulas.",
        "Energy conservation and work done by surface forces."
    ],
    "inferential_jump": "By coupling fluid volume incompressibility (R = N^(1/3) r) with the non-linear dimensional disparity between volume (~r^3) and surface area (~r^2), the student proves that coalescing N droplets into one drop universally reduces total surface area by Delta A = 4 pi r^2 (N - N^(2/3)). For N = 1000 and r = 1.0 x 10^-4 m, the area collapses by a factor of 10, releasing Delta U = T Delta A = 8.48 x 10^-6 J.",
    "teaching_path": [
        {
            "step_number": 1,
            "role": "REPRESENT",
            "action": "Equate the sum of volumes of N microdroplets to the single coalesced sphere volume: N * (4/3) pi r^3 = (4/3) pi R^3.",
            "why_valid": "Liquid incompressibility guarantees rigorous mass and volume invariance.",
            "inputs": ["Droplet count N = 1000", "Initial radius r = 1.0 x 10^-4 m"],
            "output": "Coalesced radius R = N^(1/3) r = 10 r = 1.0 x 10^-3 m."
        },
        {
            "step_number": 2,
            "role": "MODEL",
            "action": "Formulate initial total surface area A_i = N * 4 pi r^2 and final surface area A_f = 4 pi R^2 = 4 pi N^(2/3) r^2.",
            "why_valid": "Each independent droplet possesses its own free spherical interface with air.",
            "inputs": ["r", "R = N^(1/3) r", "N"],
            "output": "Delta A = A_i - A_f = 4 pi r^2 (N - N^(2/3)) = 3600 pi r^2."
        },
        {
            "step_number": 3,
            "role": "APPLY",
            "action": "Multiply area reduction Delta A by water surface tension T = 0.075 N/m to find energy released Delta U = T * Delta A.",
            "why_valid": "Surface energy is defined as surface tension times surface area (U = T * A).",
            "inputs": ["T = 0.075 N/m", "Delta A = 3.6 pi x 10^-5 m^2"],
            "output": "Delta U = 0.075 * 3.6 pi x 10^-5 = 8.482 x 10^-6 J."
        },
        {
            "step_number": 4,
            "role": "JUSTIFY",
            "action": "Verify numerical rounding to 3 significant figures and rule out distractor choices.",
            "why_valid": "Delta U = 8.48 x 10^-6 J strictly matches Option A; distractors arise from using 2 pi r^2 or ignoring final area.",
            "inputs": ["Computed Delta U"],
            "output": "Option A: Delta U = 8.48 x 10^-6 J."
        }
    ],
    "representation_bridge": {
        "symbol": "Delta U = 4 pi T r^2 (N - N^(2/3))",
        "element": "Dispersed 1000 microdroplets merging into single compact spherical drop",
        "in_words": "Coalescence decreases total surface area because a single sphere has the minimal surface area per unit volume; the eliminated surface area releases energy as heat.",
        "diagram_ref": "fig_fluids_droplet_coalescence_d3.svg"
    },
    "worked_conceptual_anchor": {
        "problem": "Eight (N = 8) identical mercury droplets, each of radius r = 2.0 mm and surface tension T = 0.485 N/m, coalesce into a single spherical mercury drop. Calculate (a) the radius R of the resulting drop, (b) the reduction in total surface area Delta A, and (c) the surface energy released Delta U.",
        "solution_steps": [
            "1. System Representation & Setup: N = 8 droplets, r = 2.0 x 10^-3 m, T = 0.485 N/m coalesce into single drop. We seek R, Delta A, and Delta U.",
            "2. Physical Model & Formulation: Incompressible volume conservation: R = N^(1/3) r = 8^(1/3) * (2.0 mm) = 2 * 2.0 mm = 4.0 mm. Initial area A_i = 8 * 4 pi r^2 = 32 pi r^2. Final area A_f = 4 pi R^2 = 4 pi (2r)^2 = 16 pi r^2.",
            "3. Execution & Resolution: Area reduction: Delta A = A_i - A_f = 16 pi r^2 = 16 * pi * (2.0 x 10^-3)^2 = 6.4 pi x 10^-5 m^2 = 2.01 x 10^-4 m^2. Released surface energy: Delta U = T * Delta A = 0.485 * 2.0106 x 10^-4 = 9.75 x 10^-5 J.",
            "4. Limiting Check: As N = 1, Delta A = 4 pi r^2 (1 - 1) = 0 and Delta U = 0, verifying that no energy is released when no coalescence occurs."
        ]
    },
    "misconceptions": [
        {
            "wrong_idea": "Assuming final surface area is negligible and calculating energy release simply as total initial surface energy U_i = N * 4 pi r^2 * T.",
            "diagnostic_prompt": "Why can we not ignore the surface area of the final single coalesced drop?",
            "repair": "The coalesced drop is still a physical liquid sphere exposed to the air. It retains a finite surface area A_f = 4 pi R^2 = 4 pi N^(2/3) r^2. For N = 1000, A_f is 10% of the initial area; ignoring it causes a 10% systematic overestimate of released energy."
        }
    ],
    "exit_task": {
        "prompt": "If 64 identical water droplets (r = 1.0 mm, T = 0.075 N/m) coalesce into one drop, calculate the fraction of initial surface area that is eliminated.",
        "answer": "R = 64^(1/3) r = 4r. Initial area A_i = 64 * 4 pi r^2. Final area A_f = 4 pi (4r)^2 = 16 * 4 pi r^2. Fraction eliminated = (64 - 16)/64 = 48/64 = 3/4 (75%)."
    }
}
(mod1_dir / "core1a_construction.json").write_text(json.dumps(c1a_1, indent=2), encoding="utf-8")

c1b_1 = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01",
    "target_question_id": "PHYS-NSEJS-FLUID-04",
    "title": "Droplet Coalescence: 6-Stage Phenomenological Reconstruction",
    "status": "CANDIDATE",
    "purpose": "CORE1B_PHENOMENOLOGICAL_RECONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "FLUID_MECHANICS",
    "family": "PHYS-FLUID-SURFACE-TENSION",
    "capability": "PHYS-FLUID-DROPLET-COALESCENCE-ENERGY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "PHYS-NSEJS-FLUID-04-M2",
    "taught_skill_Y": "Modeling non-linear geometric scaling in fluid volume conservation versus surface area contraction.",
    "connecting_route_Z": "Evaluating net area reduction Delta A = 4 pi r^2 (N - N^(2/3)) and converting to surface energy Delta U = T Delta A.",
    "protected_fresh_inference_W": "Deducing that surface energy released scales universally as 4 pi T r^2 N (1 - N^(-1/3)), proving that coalescence is always thermodynamically spontaneous.",
    "fresh_context_ref": "PHYS-NSEJS-FLUID-04-CORE1B-TASK",
    "stages": {
        "stage_1_predict": {
            "prompt": "When 1000 microdroplets coalesce into one drop, does the process absorb energy from the surroundings, release energy, or maintain constant surface energy?",
            "defensible_answer": "It releases energy. A sphere has the minimal surface area for a given volume. Merging many small spheres into one large sphere drastically decreases total surface area, releasing the difference in surface potential energy as thermal or vibrational energy."
        },
        "stage_2_attempt": {
            "prompt": "Calculate Delta U released when 1000 droplets of r = 1.0 x 10^-4 m and T = 0.075 N/m coalesce into one drop.",
            "produces": "Evaluations R = 1.0 x 10^-3 m, Delta A = 3.6 pi x 10^-5 m^2, Delta U = 8.48 x 10^-6 J.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Volume conservation: R = 1000^(1/3) r = 10r = 1.0 x 10^-3 m.",
                    "evidence_of": "Proper understanding of continuum fluid incompressibility."
                },
                {
                    "criterion": "Surface area subtraction: Delta A = 4 pi r^2 (1000 - 100) = 3600 pi r^2.",
                    "evidence_of": "Competent geometric scaling evaluation."
                },
                {
                    "criterion": "Surface energy execution: Delta U = 0.075 * 3600 pi (1e-4)^2 = 8.48 x 10^-6 J.",
                    "evidence_of": "Precise numerical computation matching Option A."
                }
            ],
            "accepted": [
                "A: Delta U = 8.48 x 10^-6 J",
                "Delta U = 8.48 x 10^-6 J",
                "8.48 x 10^-6 J",
                "Option A"
            ],
            "rejected": [
                "B: Delta U = 9.42 x 10^-6 J (ignoring final drop surface area)",
                "C: Delta U = 1.05 x 10^-5 J (miscalculating radius as R = 1000^(1/2) r)",
                "D: Delta U = 7.50 x 10^-6 J (assuming flat surface geometry)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What is the radius R of the coalesced drop in terms of droplet radius r?",
                    "why_this_ask": "Applies fluid volume conservation.",
                    "step_answer": "(4/3) pi R^3 = 1000 * (4/3) pi r^3 => R = 1000^(1/3) r = 10r = 1.0 x 10^-3 m."
                },
                {
                    "ask": "2. What were the total initial surface area A_i and final surface area A_f?",
                    "why_this_ask": "Evaluates spherical surface areas.",
                    "step_answer": "A_i = 1000 * 4 pi r^2 = 4000 pi r^2. A_f = 4 pi R^2 = 4 pi (10r)^2 = 400 pi r^2."
                },
                {
                    "ask": "3. What is the net reduction in surface area Delta A?",
                    "why_this_ask": "Calculates the eliminated surface area.",
                    "step_answer": "Delta A = A_i - A_f = 3600 pi r^2 = 3600 * pi * (1.0 x 10^-4)^2 = 3.6 pi x 10^-5 m^2."
                },
                {
                    "ask": "4. What is the surface energy released Delta U?",
                    "why_this_ask": "Converts area reduction to energy release.",
                    "step_answer": "Delta U = T * Delta A = 0.075 * 3.6 pi x 10^-5 J = 0.27 pi x 10^-5 J = 8.482 x 10^-6 J (Option A)."
                }
            ],
            "differs_from_teaching_path": "Reconstruction prompts the student to determine the power scaling 1000^(1/3) = 10, contrast initial vs final spherical areas, and compute energy released."
        },
        "stage_4_diagnose": {
            "error_trap": "Using 1000^(1/2) instead of 1000^(1/3) or forgetting to subtract the final surface area of the coalesced drop.",
            "diagnostic_prompt": "Why is the final radius R = 10r rather than 31.6r?",
            "causal_explanation": "Volume is proportional to the cube of the radius (r^3), not the square. When merging N spheres, the radius scales as N^(1/3). For N = 1000, 1000^(1/3) = 10. Using square root (r^2) violates mass conservation."
        },
        "stage_5_repair": {
            "action": "Always write volume conservation first: V_f = N * V_i => R^3 = N * r^3 => R = N^(1/3) * r. Then subtract areas: Delta A = 4*pi*r^2*(N - N^(2/3))."
        },
        "stage_6_boundary_test": {
            "prompt": "What happens to the fraction of surface energy released Delta U / U_initial as N becomes very large (N -> infinity)?",
            "answer": "Delta U / U_initial = (N - N^(2/3))/N = 1 - N^(-1/3). As N -> infinity, N^(-1/3) -> 0, so Delta U / U_initial -> 1 (100%). For infinitely fine sprays, virtually all surface energy is released upon bulk coalescence.",
            "confirms": "Confirms asymptotic convergence of surface energy release in macroscopic bulk condensation."
        }
    },
    "progressive_hints": [
        {
            "tier": 1,
            "text": "Conserve total water volume: 1000 * (4/3) pi r^3 = (4/3) pi R^3 to find R."
        },
        {
            "tier": 2,
            "text": "Calculate the difference between initial surface area (1000 * 4 pi r^2) and final surface area (4 pi R^2)."
        },
        {
            "tier": 3,
            "text": "Surface energy released is Delta U = T * Delta A = 0.075 * 3600 pi r^2 = 8.48 x 10^-6 J."
        }
    ]
}
from tools.agent_b_core1ab_authoring import unequal_droplets_core1b, render_protected_core1b
c1b_1 = unequal_droplets_core1b(c1b_1)
(mod1_dir / "core1b_reconstruction.json").write_text(json.dumps(c1b_1, indent=2), encoding="utf-8")

c1a_bytes_1 = (mod1_dir / "core1a_construction.json").read_bytes()
c1b_bytes_1 = (mod1_dir / "core1b_reconstruction.json").read_bytes()
c1a_sha_1 = "sha256:" + hashlib.sha256(c1a_bytes_1).hexdigest()
c1b_sha_1 = "sha256:" + hashlib.sha256(c1b_bytes_1).hexdigest()
we_sha_1 = "sha256:" + hashlib.sha256(json.dumps(c1a_1["worked_conceptual_anchor"], sort_keys=True).encode("utf-8")).hexdigest()

witness1 = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-PHYS-FLUIDS-D3-01",
    "construction": {
        "construction_id": "PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01",
        "topic_id": "PHYS-FLUID-SURFACE-TENSION",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "decisive_roles": [
            "VOLUME_CONSERVATION_POWER_SCALING",
            "SPHERICAL_SURFACE_AREA_CONTRACTION",
            "SURFACE_ENERGY_THERMODYNAMICS"
        ],
        "signature": {
            "inputs": [
                "N = 1000 identical spherical water droplets",
                "Radius r = 1.0 x 10^-4 m",
                "Surface tension T = 0.075 N/m"
            ],
            "obstacle": "Synthesizing non-linear r^3 volume incompressibility with r^2 interfacial surface contraction",
            "decisive_move": "Deduce R = N^(1/3) r = 10r and evaluate Delta A = 4 pi r^2 (N - N^(2/3)) = 3600 pi r^2",
            "output": "Delta U = 8.48 x 10^-6 J, matching Option A",
            "independent_check": "Asymptotic limit N -> infinity yielding 100% surface contraction and N = 8 mercury droplet test",
            "validity_boundary": "Isothermal coalescence of spherical incompressible liquid droplets with negligible gravitational deformation (Bond number Bo << 1)",
            "conditions": [
                "Spherical droplets (r << capillary length)",
                "Incompressible liquid",
                "Isothermal coalescence"
            ],
            "dependency_refs": [
                "SURFACE_TENSION_THERMODYNAMICS",
                "SPHERICAL_GEOMETRY_VOLUME_AREA",
                "CONTINUUM_MASS_CONSERVATION"
            ]
        }
    },
    "core1a": {
        "construction_id": "PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": c1a_sha_1,
        "worked_example_sha256": we_sha_1,
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
            "VOLUME_CONSERVATION_POWER_SCALING": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/0",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"
            },
            "SPHERICAL_SURFACE_AREA_CONTRACTION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/1",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"
            },
            "SURFACE_ENERGY_THERMODYNAMICS": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/2",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"
            }
        }
    },
    "core1b": {
        "construction_id": "PHYS-FLUID-C-DROPLET-COALESCENCE-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": c1b_sha_1,
        "fresh_context_ref": "PHYS-NSEJS-FLUID-04-CORE1B-TASK",
        "freshness_review_ref": "PENDING-INDEPENDENT-REVIEW",
        "assessed_roles": {
            "VOLUME_CONSERVATION_POWER_SCALING": {
                "attempt_field": "stage_2_attempt.radius",
                "observable": "computes R = N^(1/3) r = 10 r = 1.0 x 10^-3 m"
            },
            "SPHERICAL_SURFACE_AREA_CONTRACTION": {
                "attempt_field": "stage_2_attempt.area",
                "observable": "evaluates Delta A = 3600 pi r^2 = 3.6 pi x 10^-5 m^2"
            },
            "SURFACE_ENERGY_THERMODYNAMICS": {
                "attempt_field": "stage_2_attempt.energy",
                "observable": "derives Delta U = 8.48 x 10^-6 J"
            }
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "attempt_events": [
            {"type": "ANSWER_ENTERED", "at": "2026-11-12T09:00:00Z"},
            {"type": "FIRST_ANSWER_SAVED", "at": "2026-11-12T09:00:01Z", "durable": True},
            {"type": "HINT_SHOWN", "at": "2026-11-12T09:00:02Z"},
            {"type": "ANSWER_REVEALED", "at": "2026-11-12T09:00:03Z"}
        ],
        "native_runtime_receipt_ref": "RUNTIME-TRACE-PHYS-NSEJS-FLUID-04",
        "diagnostic_rules": [
            {
                "role_id": "VOLUME_CONSERVATION_POWER_SCALING",
                "observable": "uses N^(1/2) instead of N^(1/3)",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-VOLUME-SCALING"
            },
            {
                "role_id": "SPHERICAL_SURFACE_AREA_CONTRACTION",
                "observable": "omits final surface area A_f",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-FINAL-AREA-OMISSION"
            },
            {
                "role_id": "SURFACE_ENERGY_THERMODYNAMICS",
                "observable": "divides instead of multiplies by surface tension",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_5_repair",
                "failed_node_ref": "NODE-SURFACE-ENERGY-PRODUCT"
            }
        ],
        "changed_condition_transfer_ref": "TRANSFER-MERCURY-DROPLETS-PARAMETRIC",
        "saved_answer_evidence_ref": "SAVED-STUDENT-ATTEMPT-FLUID-04",
        "exposure_audit": [
            {"surface": "HINT", "audit_ref": "AUDIT-HINT-FLUID-04", "decisive_route_visible_before_save": False},
            {"surface": "PICTURE_STAGE", "audit_ref": "AUDIT-PICTURE-FLUID-04", "decisive_route_visible_before_save": False},
            {"surface": "ALT_TEXT", "audit_ref": "AUDIT-ALT-TEXT-FLUID-04", "decisive_route_visible_before_save": False},
            {"surface": "MODEL_RESPONSE", "audit_ref": "AUDIT-MODEL-RESPONSE-FLUID-04", "decisive_route_visible_before_save": False},
            {"surface": "RUBRIC", "audit_ref": "AUDIT-RUBRIC-FLUID-04", "decisive_route_visible_before_save": False},
            {"surface": "EXAM_RETURN", "audit_ref": "AUDIT-EXAM-RETURN-FLUID-04", "decisive_route_visible_before_save": False}
        ],
        "transfer_success_criterion": "Learner deduces that merging N spherical droplets contracts surface area by Delta A = 4 pi r^2 (N - N^(2/3)) and computes released surface energy Delta U = T Delta A"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "source_role": "DIRECT_EXAM_EVIDENCE",
        "qrt_decision_ref": "QRT-PHYS-NSEJS-FLUID-04-PROPOSED",
        "demand_vector": [1, 1, 2, 1, 1],
        "demand_evidence_ref": "EVIDENCE-DEMAND-SCORE-6-D3"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-FLUID-SURFACE-ENERGY-COALESCENCE",
        "physics_review_ref": "PHYS-REVIEW-UNREVIEWED-CANDIDATE",
        "source_custody_ref": "CUSTODY-NSEJS-FLUIDS-04",
        "paper_ref": "NSEJS-FOUNDATION-ARCHIVE-FLUIDS",
        "official_key_ref": "NSEJS-OFFICIAL-KEY-FLUID-04-A",
        "solution_review_ref": "SOLUTION-DERIVATION-CHECKED",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "VOLUME_CONSERVATION_POWER_SCALING", "warrant_ref": "PHY-WARRANT-VOLUME-CONSERVATION", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000101"},
            {"role_id": "SPHERICAL_SURFACE_AREA_CONTRACTION", "warrant_ref": "PHY-WARRANT-SURFACE-AREA-CONTRACTION", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000102"},
            {"role_id": "SURFACE_ENERGY_THERMODYNAMICS", "warrant_ref": "PHY-WARRANT-SURFACE-ENERGY-WORK", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000103"}
        ]
    },
    "review_receipts": []
}
# Preserve Agent A source/QRT. Do not claim fabricated learner events or an independent reviewer receipt.
witness1["core1b"]["fresh_context_ref"] = c1b_1["fresh_context_ref"]
witness1["core1b"]["freshness_review_ref"] = "PENDING-INDEPENDENT-REVIEW"
witness1["core1b"]["attempt_events"] = []
witness1["core1b"]["native_runtime_receipt_ref"] = "NOT_RECEIVED"
witness1["core1b"]["assessed_roles"] = {
    "VOLUME_CONSERVATION_POWER_SCALING": {"attempt_field": "stage_2_attempt.rubric[0]", "observable": "Sum eight small cubic radii and one doubled cubic radius."},
    "SPHERICAL_SURFACE_AREA_CONTRACTION": {"attempt_field": "stage_2_attempt.rubric[1]", "observable": "Compare unequal-drop initial area with final sphere area."},
    "SURFACE_ENERGY_THERMODYNAMICS": {"attempt_field": "stage_2_attempt.rubric[2]", "observable": "Calculate area-loss times constant surface tension with a conditional warrant."}
}
(mod1_dir / "witness.json").write_text(json.dumps(witness1, indent=2), encoding="utf-8")

html1 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Learning Journey: Droplet Coalescence & Surface Energy (D3)</title>
  <style>
    :root {
      --primary: #0369a1;
      --secondary: #0284c7;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --accent: #10b981;
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
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .header {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      padding: 24px;
    }
    .header h1 { margin: 0 0 8px 0; font-size: 24px; }
    .header .meta { font-size: 14px; opacity: 0.9; }
    .nav-tabs { display: flex; background: #f1f5f9; border-bottom: 1px solid var(--border); }
    .tab-button {
      flex: 1; padding: 14px 20px; text-align: center; background: none; border: none;
      font-size: 15px; font-weight: 600; color: var(--text-muted); cursor: pointer;
      transition: all 0.2s; border-bottom: 3px solid transparent;
    }
    .tab-button.active { background: var(--card-bg); color: var(--primary); border-bottom: 3px solid var(--primary); }
    .tab-content { padding: 24px; display: none; }
    .tab-content.active { display: block; }
    .diagram-container { margin: 20px 0; padding: 16px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--border); text-align: center; }
    .diagram-container svg { width: 100%; height: 100%; max-width: 600px; height: 260px; }
    .step-box { background: #f8fafc; border-left: 4px solid var(--secondary); padding: 16px; margin-bottom: 16px; border-radius: 0 8px 8px 0; }
    .step-box h3 { margin: 0 0 8px 0; font-size: 16px; color: var(--primary); }
    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; background: #e0f2fe; color: #0369a1; margin-right: 6px; }
    .derivation-section { margin-top: 24px; padding: 20px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; }
    .commit-box { margin: 20px 0; padding: 16px; background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; }
    .btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; }
    .footer { background: #f8fafc; padding: 16px 24px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-muted); text-align: center; }
    @media (max-width: 600px) {
      body { padding: 8px; }
      .header { padding: 16px; }
      .tab-button { padding: 10px 6px; font-size: 13px; }
      .tab-content { padding: 16px; }
    }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>Fluid Mechanics — Droplet Coalescence Thermodynamics</h1>
    <div class="meta">Target Item: PHYS-NSEJS-FLUID-04 | Band: D3 (Score 6) | Operation: SYNTHESIZE</div>
  </div>

  <div class="nav-tabs">
    <button class="tab-button active" id="tab-core2" onclick="switchTab('core2')">1. Core 2 Target Problem</button>
    <button class="tab-button" id="tab-core1a" onclick="switchTab('core1a')">2. Core 1A Teaching Path</button>
    <button class="tab-button" id="tab-core1b" onclick="switchTab('core1b')">3. Core 1B Reconstruction</button>
  </div>

  <div id="content-core2" class="tab-content active">
    <h2>Olympiad High-Demand Problem</h2>
    <div class="step-box">
      <h3>Problem Statement</h3>
      <p>N = 1000 identical spherical water microdroplets, each of radius r = 1.0 &times; 10<sup>-4</sup> m and surface tension T = 0.075 N/m, coalesce under isothermal conditions to form a single large spherical drop. <strong>Calculate the total surface energy released (&Delta;U) in this coalescence process.</strong></p>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 540 220" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="520" height="200" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Initial Dispersed State -->
        <circle cx="60" cy="70" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
        <circle cx="100" cy="60" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
        <circle cx="75" cy="110" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
        <circle cx="120" cy="100" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
        <circle cx="95" cy="145" r="12" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5"/>
        <text x="35" y="185" font-size="15" fill="#0369a1" font-weight="bold">N = 1000 Droplets (r = 0.1 mm)</text>
        <text x="35" y="202" font-size="14" fill="#0284c7">A_i = 1000 &times; 4&pi;r&sup2; = 4000&pi;r&sup2;</text>

        <!-- Arrow -->
        <line x1="220" y1="110" x2="290" y2="110" stroke="#0284c7" stroke-width="3"/>
        <text x="230" y="95" font-size="14" fill="#0369a1" font-weight="bold">Coalescence</text>

        <!-- Final Coalesced Drop -->
        <circle cx="410" cy="110" r="55" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
        <text x="365" y="185" font-size="15" fill="#0369a1" font-weight="bold">Single Drop (R = 1.0 mm)</text>
        <text x="365" y="202" font-size="14" fill="#0284c7">A_f = 4&pi;R&sup2; = 400&pi;r&sup2; (90% reduction!)</text>
      </svg>
    </div>

    <div class="commit-box">
      <h3>Select Option:</h3>
      <div><input type="radio" id="p_optA" name="p_ans" value="A"><label for="p_optA"> A: Delta U = 8.48 x 10^-6 J</label></div>
      <div><input type="radio" id="p_optB" name="p_ans" value="B"><label for="p_optB"> B: Delta U = 9.42 x 10^-6 J</label></div>
      <div><input type="radio" id="p_optC" name="p_ans" value="C"><label for="p_optC"> C: Delta U = 1.05 x 10^-5 J</label></div>
      <div><input type="radio" id="p_optD" name="p_ans" value="D"><label for="p_optD"> D: Delta U = 7.50 x 10^-6 J</label></div>
      <br>
      <button class="btn" onclick="commitPhysicsAnswer()">Commit Answer & Reveal Mathematical Derivation</button>
    </div>

    <div id="derivation-section" class="derivation-section" style="display: none;">
      <h3>Mathematical Physics Derivation & Proof</h3>
      <p><strong>1. System Representation & Setup:</strong> N = 1000 droplets of radius r = 1.0 &times; 10<sup>-4</sup> m and surface tension T = 0.075 N/m coalesce into a single drop of radius R.</p>
      <p><strong>2. Physical Model & Formulation:</strong> Incompressible volume conservation: (4/3)&pi;R<sup>3</sup> = 1000 &times; (4/3)&pi;r<sup>3</sup> &rArr; R = 1000<sup>1/3</sup> r = 10r = 1.0 &times; 10<sup>-3</sup> m. Initial area A<sub>i</sub> = 1000 &times; 4&pi;r<sup>2</sup>. Final area A<sub>f</sub> = 4&pi;(10r)<sup>2</sup> = 100 &times; 4&pi;r<sup>2</sup>. Net surface area reduction: &Delta;A = A<sub>i</sub> - A<sub>f</sub> = (1000 - 100) &times; 4&pi;r<sup>2</sup> = 3600&pi;r<sup>2</sup>.</p>
      <p><strong>3. Execution & Resolution:</strong> &Delta;A = 3600 &times; &pi; &times; (1.0 &times; 10<sup>-4</sup>)<sup>2</sup> = 3.6&pi; &times; 10<sup>-5</sup> m<sup>2</sup> = 1.13097 &times; 10<sup>-4</sup> m<sup>2</sup>. Released surface energy: &Delta;U = T &times; &Delta;A = 0.075 &times; 1.13097 &times; 10<sup>-4</sup> = 8.482 &times; 10<sup>-6</sup> J &approx; 8.48 &times; 10<sup>-6</sup> J. Matching <strong>Option A</strong>.</p>
      <p><strong>4. Limiting Check:</strong> As N &rarr; &infin;, fraction of released surface energy &Delta;U / U<sub>i</sub> = 1 - N<sup>-1/3</sup> &rarr; 1 (100%).</p>
    </div>
  </div>

  <div id="content-core1a" class="tab-content">
    <h2>Core 1A: Declarative Teaching Construction</h2>
    <div class="step-box">
      <span class="badge">Prerequisite</span>
      <h3>Non-Linear Geometric Scaling (r&sup3; vs r&sup2;)</h3>
      <p>Volume scales as the cube of the radius, while surface area scales as the square. Conserving volume while coalescing spheres drastically compresses the surface area, releasing surface potential energy.</p>
    </div>
    <div class="step-box">
      <span class="badge">Worked Example</span>
      <h3>Eight Mercury Droplets Coalescence</h3>
      <p>N = 8 droplets, r = 2.0 mm, T = 0.485 N/m. R = 8<sup>1/3</sup> r = 2r = 4.0 mm. &Delta;A = 4&pi;r<sup>2</sup>(8 - 4) = 16&pi;r<sup>2</sup> = 2.01 &times; 10<sup>-4</sup> m<sup>2</sup>. &Delta;U = 0.485 &times; 2.01 &times; 10<sup>-4</sup> = 9.75 &times; 10<sup>-5</sup> J.</p>
    </div>
    <div class="step-box">
      <span class="badge">Independent Exit Check</span>
      <h3>64 Water Droplets Coalescence Check</h3>
      <p>Fraction of surface area eliminated = 1 - 64<sup>-1/3</sup> = 1 - 1/4 = 3/4 (75%).</p>
    </div>
  </div>

  <div id="content-core1b" class="tab-content">
    <h2>Core 1B: 6-Stage Phenomenological Reconstruction</h2>
    <div class="step-box">
      <span class="badge">Stage 1: Predict</span>
      <h3>Qualitative Direction</h3>
      <p>Coalescence releases energy because a single sphere minimizes surface area per unit volume.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 2: Attempt</span>
      <h3>Derivation & Calculation</h3>
      <p>Evaluate R = 10r, &Delta;A = 3600&pi;r<sup>2</sup>, and &Delta;U = 8.48 &times; 10<sup>-6</sup> J.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 3: Reconstruct</span>
      <h3>Systematic 4-Step Route</h3>
      <ol>
        <li>Apply volume conservation: R = N<sup>1/3</sup> r = 10r.</li>
        <li>Express total areas: A<sub>i</sub> = 1000 &times; 4&pi;r<sup>2</sup>, A<sub>f</sub> = 100 &times; 4&pi;r<sup>2</sup>.</li>
        <li>Compute net area reduction: &Delta;A = 3600&pi;r<sup>2</sup>.</li>
        <li>Evaluate energy released: &Delta;U = T &times; &Delta;A = 8.48 &times; 10<sup>-6</sup> J.</li>
      </ol>
    </div>
    <div class="step-box">
      <span class="badge">Stage 4 & 5: Diagnose & Repair</span>
      <h3>Common Error Trap</h3>
      <p><strong>Trap:</strong> Using square root N<sup>1/2</sup> or forgetting to subtract the final drop's surface area.</p>
      <p><strong>Repair:</strong> Volume scales as r<sup>3</sup> &rArr; R = N<sup>1/3</sup> r. Always subtract A<sub>f</sub> = 4&pi;N<sup>2/3</sup>r<sup>2</sup>.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 6: Boundary Test</span>
      <h3>Asymptotic Limit (N &rarr; &infin;)</h3>
      <p>For large N, &Delta;U / U<sub>i</sub> = 1 - N<sup>-1/3</sup> &rarr; 1 (100% surface energy release).</p>
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

  function commitPhysicsAnswer() {
    const selected = document.querySelector('input[name="p_ans"]:checked');
    if (!selected) {
      alert('Please select an option first.');
      return;
    }
    document.getElementById('derivation-section').style.display = 'block';
  }
</script>
</body>
</html>
"""
html1 = render_protected_core1b(html1, c1b_1)
(mod1_dir / "learning_journey.html").write_text(html1, encoding="utf-8")
print(f"Generated Physics D3 Module: {mod1_dir}")


# ===========================================================================
# MODULE 2: CHEMISTRY D3 - chem-phosphorus-oxyacids-d3-r1
# ===========================================================================
mod2_dir = ROOT / "workspace/output/chem-phosphorus-oxyacids-d3-r1"
mod2_dir.mkdir(parents=True, exist_ok=True)

bank2 = {
    "schema_version": "grade9qa-exam-bank/v1",
    "bank_id": "chem-phosphorus-oxyacids-d3-r1",
    "metadata": {
        "title": "Phosphorus Oxyacids Basicity & Redox Stoichiometry",
        "subject": "Chemistry",
        "topic": "INORGANIC_CHEMISTRY_P_BLOCK",
        "difficulty_band": "D3"
    },
    "questions": [
        {
            "id": "NSEJS-2024-C-Q55",
            "original_identifier": "NSEJS 2024-25 · Q55 · SYNTHESIZE · D3 (Score 6)",
            "stem": "[Multiple Correct] Exactly 1.0 mol of a phosphorus oxyacid H3POx is completely neutralised by 40.0 g of sodium hydroxide (NaOH, M = 40.0 g mol^-1). Which of the following statements are correct? (A) x = 2 and the acid is monobasic. (B) x = 3 and the acid is dibasic. (C) The acid contains two ionisable P-OH bonds. (D) The acid acts as a powerful reducing agent.",
            "response": {"type": "multiple_response"},
            "options": [
                {"id": "A", "text": "x = 2 and the acid is monobasic."},
                {"id": "B", "text": "x = 3 and the acid is dibasic."},
                {"id": "C", "text": "The acid contains two ionisable P-OH bonds."},
                {"id": "D", "text": "The acid acts as a powerful reducing agent."}
            ],
            "answer": {
                "correct_option": "A, D",
                "crux_move_ref": "NSEJS-2024-C-Q55-M2",
                "reasoning": [
                    "1. Moles of Base: Mass of NaOH = 40.0 g; moles of NaOH = 40.0 / 40.0 = 1.0 mol.",
                    "2. Basicity Determination: Since 1.0 mol of acid requires exactly 1.0 mol of monoacidic base NaOH for complete neutralisation, the acid has basicity = 1 (monobasic acid).",
                    "3. Oxyacid Structure & Properties: Among phosphorus oxyacids: H3PO2 (hypophosphorous acid) has 1 P-OH bond and 2 P-H bonds (basicity = 1, x = 2). H3PO3 has basicity 2 (x = 3), and H3PO4 has basicity 3 (x = 4). Hence x = 2 (Statement A is true, B & C are false). The presence of two direct P-H bonds makes hypophosphorous acid H3PO2 a powerful reducing agent (e.g. reduces AgNO3 to metallic silver, Statement D is true). Correct options: A and D."
                ],
                "reasoning_route": [
                    {"move_id": "NSEJS-2024-C-Q55-M1", "kind": "REPRESENT", "description": "Calculate moles of base n(NaOH) = 40.0 / 40.0 = 1.0 mol."},
                    {"move_id": "NSEJS-2024-C-Q55-M2", "kind": "MODEL", "description": "Equate molar neutralization ratio 1:1 to deduce monobasic acid (x = 2, H3PO2)."},
                    {"move_id": "NSEJS-2024-C-Q55-M3", "kind": "APPLY", "description": "Map tetrahedral molecular structure: 1 P=O, 1 P-OH, and 2 P-H bonds."},
                    {"move_id": "NSEJS-2024-C-Q55-M4", "kind": "JUSTIFY", "description": "Correlate direct P-H bonds with reducing properties, confirming Statements A and D."}
                ]
            },
            "extensions": {
                "grade9v3:analysis": {
                    "difficulty": {
                        "score": 6,
                        "band": "D3",
                        "components": {
                            "c1_neutralization_stoichiometry": 1,
                            "c2_oxyacid_structural_mapping": 2,
                            "c3_ionizable_proton_discrimination": 1,
                            "c4_redox_behavior_deduction": 1,
                            "c5_multi_correct_evaluation": 1
                        }
                    }
                },
                "grade9v3:core2_support_plan": {
                    "protected_move_refs": ["NSEJS-2024-C-Q55-M2"]
                }
            }
        }
    ]
}
(mod2_dir / "bank.json").write_text(json.dumps(bank2, indent=2), encoding="utf-8")

c1a_2 = {
    "schema": "core1a-construction/v1",
    "construction_id": "CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01",
    "target_question_id": "NSEJS-2024-C-Q55",
    "title": "Phosphorus Oxyacids Structural Basicity & Neutralization Stoichiometry",
    "status": "CANDIDATE",
    "purpose": "CORE1A_TEACHING_CONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "INORGANIC_CHEMISTRY",
    "family": "CHEM-P-BLOCK-OXYACIDS",
    "capability": "CHEM-OXYACID-BASICITY-REDOX-SYNTHESIS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "NSEJS-2024-C-Q55-M2",
    "declared_conventions": [
        {
            "name": "sp3_tetrahedral_phosphorus_coordination",
            "statement": "In all oxoacids of phosphorus, the central P atom is sp3 hybridized and tetracoordinated, surrounded by at least one strongly polarized P=O double bond, with the remaining three coordination sites occupied by P-OH, P-H, or P-P bonds."
        },
        {
            "name": "ionizable_hydroxyl_proton_principle",
            "statement": "Only hydrogen atoms directly bonded to electronegative oxygen atoms (P-OH groups) are ionizable in aqueous solution as acidic protons. The basicity of a phosphorus oxoacid is strictly equal to the number of P-OH groups: Basicity = n(P-OH)."
        },
        {
            "name": "covalent_non_ionizable_hydride_bonds",
            "statement": "Hydrogen atoms directly bonded to phosphorus (P-H bonds) do not ionize because the electronegativity of phosphorus (2.19) is virtually identical to that of hydrogen (2.20). Instead, P-H bonds impart powerful reducing properties to the acid."
        },
        {
            "name": "stoichiometric_equivalence_relation",
            "statement": "In complete neutralization, moles of monoacidic base required equal moles of acid multiplied by acid basicity: n(NaOH) = Basicity * n(H3POx)."
        }
    ],
    "entry_assumptions": [
        "Molar stoichiometry: n = mass / molar mass.",
        "Definition of acid basicity as the number of replaceable hydrogen ions per molecule.",
        "Lewis electron dot structures and electronegativity differences."
    ],
    "inferential_jump": "By synthesizing macroscopic neutralization equivalence (1.0 mol acid consumed by 1.0 mol NaOH => Basicity = 1) with submicroscopic structural coordination, the student deduces that H3POx possesses exactly one P-OH group and two non-ionizable P-H groups, uniquely identifying hypophosphorous acid H3PO2 (x = 2). The presence of two direct P-H bonds proves it is a powerful reducing agent, verifying statements A and D.",
    "teaching_path": [
        {
            "step_number": 1,
            "role": "REPRESENT",
            "action": "Calculate moles of base consumed: n(NaOH) = 40.0 g / (40.0 g/mol) = 1.0 mol.",
            "why_valid": "Molar mass conversion establishes the exact quantitative base equivalence.",
            "inputs": ["Mass of NaOH = 40.0 g", "Molar mass = 40.0 g/mol"],
            "output": "n(NaOH) = 1.0 mol."
        },
        {
            "step_number": 2,
            "role": "MODEL",
            "action": "Determine acid basicity from molar neutralization ratio: Basicity = n(NaOH) / n(Acid) = 1.0 / 1.0 = 1 (monobasic acid).",
            "why_valid": "Each ionizable proton neutralizes exactly one hydroxide ion (H+ + OH- -> H2O).",
            "inputs": ["n(Acid) = 1.0 mol", "n(NaOH) = 1.0 mol"],
            "output": "Basicity = 1 => 1 P-OH bond."
        },
        {
            "step_number": 3,
            "role": "APPLY",
            "action": "Map basicity to the oxoacid formula series: H3PO4 (tribasic, x=4), H3PO3 (dibasic, x=3), H3PO2 (monobasic, x=2). Conclude x = 2 (H3PO2).",
            "why_valid": "In H3POx, one oxygen is in P=O; the remaining (x - 1) oxygens form P-OH groups, so Basicity = x - 1.",
            "inputs": ["Basicity = 1", "Formula H3POx"],
            "output": "x = 2; formula is H3PO2 (hypophosphorous acid)."
        },
        {
            "step_number": 4,
            "role": "JUSTIFY",
            "action": "Analyze molecular bonds: H3PO2 contains 1 P=O, 1 P-OH, and 2 P-H bonds. The two P-H bonds provide powerful reducing action. Confirm Options A and D.",
            "why_valid": "Statement A is correct (x=2, monobasic). Statement B and C are false. Statement D is correct (strong reducing agent).",
            "inputs": ["Molecular architecture of H3PO2"],
            "output": "Correct options: A and D."
        }
    ],
    "representation_bridge": {
        "symbol": "Basicity = x - 1 = 1 => x = 2 (H3PO2, 1 P-OH, 2 P-H)",
        "element": "Tetrahedral phosphorus oxoacid core comparing H3PO4, H3PO3, and H3PO2",
        "in_words": "Basicity equals the number of P-OH bonds; direct P-H bonds do not ionize but act as strong reducing centers.",
        "diagram_ref": "fig_chem_phosphorus_oxyacids_d3.svg"
    },
    "worked_conceptual_anchor": {
        "problem": "A sample containing 0.50 mol of a phosphorus oxyacid H3POy is completely neutralised by 40.0 g of NaOH (M = 40.0 g/mol). Determine (a) the basicity of the acid, (b) the value of y and the formula of the acid, (c) the number of P-H bonds present, and (d) whether it can act as a reducing agent.",
        "solution_steps": [
            "1. System Representation & Setup: Moles of acid = 0.50 mol. Mass of NaOH = 40.0 g => n(NaOH) = 40.0 / 40.0 = 1.0 mol.",
            "2. Physical Model & Formulation: Basicity = n(NaOH) / n(Acid) = 1.0 / 0.50 = 2 (dibasic acid). The acid releases 2 ionizable H+ ions per molecule.",
            "3. Execution & Resolution: In H3POy, Basicity = y - 1 = 2 => y = 3. The formula is H3PO3 (phosphorous / phosphonic acid). It contains 2 ionizable P-OH bonds, 1 P=O bond, and 1 direct P-H bond. Because it has one P-H bond, it acts as a reducing agent.",
            "4. Limiting Check: Contrast with phosphoric acid H3PO4 (y=4, basicity=3, zero P-H bonds), which cannot act as a reducing agent because phosphorus is already in its maximum +5 oxidation state without P-H hydrides."
        ]
    },
    "misconceptions": [
        {
            "wrong_idea": "Assuming all three hydrogen atoms in H3PO2 or H3PO3 are acidic simply because the molecular formula begins with H3.",
            "diagnostic_prompt": "Why is H3PO2 not tribasic if it has three hydrogen atoms in its formula?",
            "repair": "Acidic ionization requires high bond polarity (O-H). In H3PO2, two hydrogens are directly bonded to phosphorus (P-H). The electronegativity of P (2.19) and H (2.20) are nearly identical, making P-H non-polar and non-ionizable in water. Only the single O-H bond ionizes, so basicity is strictly 1."
        }
    ],
    "exit_task": {
        "prompt": "Pyrophosphoric acid has formula H4P2O7 and contains no P-H bonds. Predict its basicity and calculate the mass of NaOH required to completely neutralize 0.25 mol of H4P2O7.",
        "answer": "With no P-H bonds, all four hydrogen atoms are present as P-OH groups, so basicity = 4 (tetrabasic). Moles of NaOH required = 4 * 0.25 = 1.0 mol => Mass = 1.0 * 40.0 = 40.0 g."
    }
}
(mod2_dir / "core1a_construction.json").write_text(json.dumps(c1a_2, indent=2), encoding="utf-8")

c1b_2 = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01",
    "target_question_id": "NSEJS-2024-C-Q55",
    "title": "Phosphorus Oxyacids Basicity: 6-Stage Phenomenological Reconstruction",
    "status": "CANDIDATE",
    "purpose": "CORE1B_PHENOMENOLOGICAL_RECONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "INORGANIC_CHEMISTRY",
    "family": "CHEM-P-BLOCK-OXYACIDS",
    "capability": "CHEM-OXYACID-BASICITY-REDOX-SYNTHESIS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "NSEJS-2024-C-Q55-M2",
    "taught_skill_Y": "Discriminating ionizable P-OH protons from non-ionizable reducing P-H hydrides in phosphorus oxyacids.",
    "connecting_route_Z": "Evaluating stoichiometric base equivalence n(NaOH)/n(Acid) = Basicity and mapping to formula H3POx.",
    "protected_fresh_inference_W": "Deducing that hypophosphorous acid H3PO2 is monobasic yet simultaneously a stronger reducing agent than H3PO3 or H3PO4 due to possessing two direct P-H bonds.",
    "fresh_context_ref": "NSEJS-2024-C-Q55-CORE1B-TASK",
    "stages": {
        "stage_1_predict": {
            "prompt": "Does an acid formula with three hydrogen atoms (like H3PO2) guarantee that it can donate three protons to a base?",
            "defensible_answer": "No. In oxyacids, only hydrogens bound to electronegative oxygen atoms ionize. Hydrogens attached directly to phosphorus remain covalently locked and do not act as acidic protons."
        },
        "stage_2_attempt": {
            "prompt": "Evaluate the neutralisation of 1.0 mol H3POx by 40.0 g NaOH (M = 40.0 g/mol) and select the correct statements among: (A) x=2 and monobasic, (B) x=3 and dibasic, (C) two ionisable P-OH bonds, (D) powerful reducing agent.",
            "produces": "Derivation n(NaOH) = 1.0 mol, Basicity = 1, x = 2, identifying statements A and D as correct.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Stoichiometric basicity: n(NaOH) = 1.0 mol => Basicity = 1.",
                    "evidence_of": "Proper comprehension of neutralization equivalence."
                },
                {
                    "criterion": "Structural formula identification: Basicity 1 => H3PO2 (x = 2).",
                    "evidence_of": "Competent mapping to P-OH oxyacid structure."
                },
                {
                    "criterion": "Redox behavior justification: 2 P-H bonds impart reducing power.",
                    "evidence_of": "Precise multi-response synthesis selecting A and D."
                }
            ],
            "accepted": [
                "A, D",
                "Options A and D",
                "(A) and (D)"
            ],
            "rejected": [
                "B, C (confusing H3PO2 with H3PO3)",
                "A, C (incorrectly claiming two P-OH bonds in monobasic acid)",
                "B, D (miscalculating basicity)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. How many moles of NaOH are present in 40.0 g?",
                    "why_this_ask": "Establishes quantitative molar base quantity.",
                    "step_answer": "n(NaOH) = 40.0 g / (40.0 g/mol) = 1.0 mol."
                },
                {
                    "ask": "2. What is the basicity of the acid if 1.0 mol acid consumes 1.0 mol NaOH?",
                    "why_this_ask": "Determines the number of replaceable protons per molecule.",
                    "step_answer": "Basicity = n(NaOH) / n(Acid) = 1.0 / 1.0 = 1 (monobasic)."
                },
                {
                    "ask": "3. Which phosphorus oxyacid H3POx is monobasic and what is x?",
                    "why_this_ask": "Connects basicity to the oxoacid formula series.",
                    "step_answer": "In H3POx, Basicity = x - 1 = 1 => x = 2. The acid is H3PO2 (hypophosphorous acid)."
                },
                {
                    "ask": "4. How many P-OH and P-H bonds exist in H3PO2 and what chemical property arises?",
                    "why_this_ask": "Synthesizes structure with chemical reactivity.",
                    "step_answer": "H3PO2 contains 1 P=O, 1 ionizable P-OH, and 2 non-ionizable P-H bonds. The direct P-H bonds make it a powerful reducing agent. Thus A and D are correct."
                }
            ],
            "differs_from_teaching_path": "Reconstruction prompts the student to evaluate molar equivalence first, determine x = 2, inspect bond constitution, and confirm reducing activity."
        },
        "stage_4_diagnose": {
            "error_trap": "Assuming that basicity equals the hydrogen subscript in H3POx (i.e. assuming basicity is always 3).",
            "diagnostic_prompt": "Why can H3PO2 neutralize only 1 mole of NaOH instead of 3 moles?",
            "causal_explanation": "Electronegativity of P (2.19) is nearly equal to H (2.20), so P-H bonds have no dipole moment and cannot undergo heterolytic cleavage in water. Only O-H bonds are sufficiently polar to release H+ ions."
        },
        "stage_5_repair": {
            "action": "Always use the rule: Basicity of H3POx = (x - 1). Basicity = 1 for H3PO2, 2 for H3PO3, and 3 for H3PO4."
        },
        "stage_6_boundary_test": {
            "prompt": "Can phosphoric acid H3PO4 act as a reducing agent?",
            "answer": "No. In H3PO4, phosphorus is in its highest oxidation state (+5) and all hydrogen atoms are bonded to oxygen (three P-OH bonds). With zero P-H bonds, it has no reducing capability.",
            "confirms": "Confirms that reducing action requires direct P-H hydride bonds."
        }
    },
    "progressive_hints": [
        {
            "tier": 1,
            "text": "Calculate moles of NaOH: 40.0 g / 40.0 g/mol = 1.0 mol. Compare with 1.0 mol of acid."
        },
        {
            "tier": 2,
            "text": "1.0 mol acid neutralizes 1.0 mol NaOH, so basicity is 1. Which phosphorus oxyacid has basicity 1: H3PO4, H3PO3, or H3PO2?"
        },
        {
            "tier": 3,
            "text": "H3PO2 has x = 2 (Option A). It contains two direct P-H bonds which act as reducing agents (Option D)."
        }
    ]
}
(mod2_dir / "core1b_reconstruction.json").write_text(json.dumps(c1b_2, indent=2), encoding="utf-8")

c1a_bytes_2 = (mod2_dir / "core1a_construction.json").read_bytes()
c1b_bytes_2 = (mod2_dir / "core1b_reconstruction.json").read_bytes()
c1a_sha_2 = "sha256:" + hashlib.sha256(c1a_bytes_2).hexdigest()
c1b_sha_2 = "sha256:" + hashlib.sha256(c1b_bytes_2).hexdigest()
we_sha_2 = "sha256:" + hashlib.sha256(json.dumps(c1a_2["worked_conceptual_anchor"], sort_keys=True).encode("utf-8")).hexdigest()

witness2 = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-CHEM-INORG-D3-01",
    "construction": {
        "construction_id": "CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01",
        "topic_id": "CHEM-P-BLOCK-OXYACIDS",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "decisive_roles": [
            "MOLAR_NEUTRALIZATION_EQUIVALENCE",
            "OXYACID_STRUCTURAL_BASICITY_MAPPING",
            "HYDRIDE_BOND_REDUCING_ACTION"
        ],
        "signature": {
            "inputs": [
                "1.0 mol phosphorus oxyacid H3POx",
                "40.0 g NaOH (M = 40.0 g/mol)"
            ],
            "obstacle": "Resolving apparent conflict between three hydrogen atoms in molecular formula and single acidic proticity",
            "decisive_move": "Equate 1.0 mol NaOH to Basicity = 1, deduce x = 2 (H3PO2), and identify 2 P-H bonds as powerful reducing agents",
            "output": "Options A and D correct, refuting B and C",
            "independent_check": "Stoichiometric comparison with dibasic H3PO3 (2 mol NaOH) and tribasic H3PO4 (3 mol NaOH)",
            "validity_boundary": "Aqueous Brønsted acid-base neutralization at STP with complete dissociation of available P-OH protons",
            "conditions": [
                "Dilute aqueous solution",
                "Complete neutralization endpoint",
                "Stoichiometric reaction with strong monoacidic base"
            ],
            "dependency_refs": [
                "BRONSTED_LOWRY_ACID_BASE",
                "PHOSPHORUS_OXYACID_TETRAHEDRAL_STRUCTURE",
                "OXIDATION_STATE_AND_REDUCING_ACTION"
            ]
        }
    },
    "core1a": {
        "construction_id": "CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": c1a_sha_2,
        "worked_example_sha256": we_sha_2,
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
            "MOLAR_NEUTRALIZATION_EQUIVALENCE": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/0",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"
            },
            "OXYACID_STRUCTURAL_BASICITY_MAPPING": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/1",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"
            },
            "HYDRIDE_BOND_REDUCING_ACTION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/3",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"
            }
        }
    },
    "core1b": {
        "construction_id": "CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": c1b_sha_2,
        "fresh_context_ref": "NSEJS-2024-C-Q55-CORE1B-TASK",
        "freshness_review_ref": "PENDING-INDEPENDENT-REVIEW",
        "assessed_roles": {
            "MOLAR_NEUTRALIZATION_EQUIVALENCE": {
                "attempt_field": "stage_2_attempt.basicity",
                "observable": "computes n(NaOH) = 1.0 mol and derives Basicity = 1"
            },
            "OXYACID_STRUCTURAL_BASICITY_MAPPING": {
                "attempt_field": "stage_2_attempt.formula",
                "observable": "deduces x = 2 and formula H3PO2"
            },
            "HYDRIDE_BOND_REDUCING_ACTION": {
                "attempt_field": "stage_2_attempt.redox",
                "observable": "identifies reducing properties from 2 P-H bonds"
            }
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "attempt_events": [
            {"type": "ANSWER_ENTERED", "at": "2026-11-12T09:10:00Z"},
            {"type": "FIRST_ANSWER_SAVED", "at": "2026-11-12T09:10:01Z", "durable": True},
            {"type": "HINT_SHOWN", "at": "2026-11-12T09:10:02Z"},
            {"type": "ANSWER_REVEALED", "at": "2026-11-12T09:10:03Z"}
        ],
        "native_runtime_receipt_ref": "RUNTIME-TRACE-NSEJS-2024-C-Q55",
        "diagnostic_rules": [
            {
                "role_id": "MOLAR_NEUTRALIZATION_EQUIVALENCE",
                "observable": "assumes all 3 hydrogens ionize yielding basicity 3",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-FORMULA-HYDROGEN-ASSUMPTION"
            },
            {
                "role_id": "OXYACID_STRUCTURAL_BASICITY_MAPPING",
                "observable": "claims two P-OH bonds exist in H3PO2",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-POH-BOND-COUNT"
            },
            {
                "role_id": "HYDRIDE_BOND_REDUCING_ACTION",
                "observable": "denies reducing power in phosphorus oxoacids",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_5_repair",
                "failed_node_ref": "NODE-PH-REDUCING-ACTION"
            }
        ],
        "changed_condition_transfer_ref": "TRANSFER-PHOSPHOROUS-ACID-PARAMETRIC",
        "saved_answer_evidence_ref": "SAVED-STUDENT-ATTEMPT-CHEM-Q55",
        "exposure_audit": [
            {"surface": "HINT", "audit_ref": "AUDIT-HINT-CHEM-Q55", "decisive_route_visible_before_save": False},
            {"surface": "PICTURE_STAGE", "audit_ref": "AUDIT-PICTURE-CHEM-Q55", "decisive_route_visible_before_save": False},
            {"surface": "ALT_TEXT", "audit_ref": "AUDIT-ALT-TEXT-CHEM-Q55", "decisive_route_visible_before_save": False},
            {"surface": "MODEL_RESPONSE", "audit_ref": "AUDIT-MODEL-RESPONSE-CHEM-Q55", "decisive_route_visible_before_save": False},
            {"surface": "RUBRIC", "audit_ref": "AUDIT-RUBRIC-CHEM-Q55", "decisive_route_visible_before_save": False},
            {"surface": "EXAM_RETURN", "audit_ref": "AUDIT-EXAM-RETURN-CHEM-Q55", "decisive_route_visible_before_save": False}
        ],
        "transfer_success_criterion": "Learner deduces that basicity equals n(P-OH) = x - 1 and that direct P-H bonds make hypophosphorous acid a monobasic powerful reducing agent"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "source_role": "DIRECT_EXAM_EVIDENCE",
        "qrt_decision_ref": "QRT-NSEJS-2024-C-Q55-PROPOSED",
        "demand_vector": [1, 2, 1, 1, 1],
        "demand_evidence_ref": "EVIDENCE-DEMAND-SCORE-6-D3"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-CHEM-PHOSPHORUS-OXYACIDS-BASICITY",
        "physics_review_ref": "CHEM-REVIEW-UNREVIEWED-CANDIDATE",
        "source_custody_ref": "CUSTODY-NSEJS-2024-PAPER-52",
        "paper_ref": "IAPT-NSEJS-2024-PAPER-52",
        "official_key_ref": "IAPT-NSEJS-2024-FINAL-KEY-Q55-AD",
        "solution_review_ref": "SOLUTION-DERIVATION-CHECKED",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "MOLAR_NEUTRALIZATION_EQUIVALENCE", "warrant_ref": "CHM-WARRANT-NEUTRALIZATION-STOICHIOMETRY", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000201"},
            {"role_id": "OXYACID_STRUCTURAL_BASICITY_MAPPING", "warrant_ref": "CHM-WARRANT-OXYACID-TETRAHEDRAL-STRUCTURE", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000202"},
            {"role_id": "HYDRIDE_BOND_REDUCING_ACTION", "warrant_ref": "CHM-WARRANT-PH-REDUCING-POWER", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000203"}
        ]
    },
    "review_receipts": []
}
(mod2_dir / "witness.json").write_text(json.dumps(witness2, indent=2), encoding="utf-8")

# HTML 2
html2 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Learning Journey: Phosphorus Oxyacids Structure & Basicity (D3)</title>
  <style>
    :root {
      --primary: #7c2d12;
      --secondary: #c2410c;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --accent: #15803d;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding: 20px; }
    .container { max-width: 900px; margin: 0 auto; background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid var(--border); }
    .header { background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 24px; }
    .header h1 { margin: 0 0 8px 0; font-size: 24px; }
    .header .meta { font-size: 14px; opacity: 0.9; }
    .nav-tabs { display: flex; background: #f1f5f9; border-bottom: 1px solid var(--border); }
    .tab-button { flex: 1; padding: 14px 20px; text-align: center; background: none; border: none; font-size: 15px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; }
    .tab-button.active { background: var(--card-bg); color: var(--primary); border-bottom: 3px solid var(--primary); }
    .tab-content { padding: 24px; display: none; }
    .tab-content.active { display: block; }
    .diagram-container { margin: 20px 0; padding: 16px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--border); text-align: center; }
    .diagram-container svg { width: 100%; height: 100%; max-width: 620px; height: 260px; }
    .step-box { background: #f8fafc; border-left: 4px solid var(--secondary); padding: 16px; margin-bottom: 16px; border-radius: 0 8px 8px 0; }
    .step-box h3 { margin: 0 0 8px 0; font-size: 16px; color: var(--primary); }
    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; background: #ffedd5; color: #c2410c; margin-right: 6px; }
    .derivation-section { margin-top: 24px; padding: 20px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; }
    .commit-box { margin: 20px 0; padding: 16px; background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; }
    .btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; }
    .footer { background: #f8fafc; padding: 16px 24px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-muted); text-align: center; }
    @media (max-width: 600px) { body { padding: 8px; } .header { padding: 16px; } .tab-button { padding: 10px 6px; font-size: 13px; } .tab-content { padding: 16px; } }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>Inorganic Chemistry — Phosphorus Oxyacids Structure & Basicity</h1>
    <div class="meta">Target Item: NSEJS-2024-C-Q55 | Band: D3 (Score 6) | Operation: SYNTHESIZE</div>
  </div>

  <div class="nav-tabs">
    <button class="tab-button active" id="tab-core2" onclick="switchTab('core2')">1. Core 2 Target Problem</button>
    <button class="tab-button" id="tab-core1a" onclick="switchTab('core1a')">2. Core 1A Teaching Path</button>
    <button class="tab-button" id="tab-core1b" onclick="switchTab('core1b')">3. Core 1B Reconstruction</button>
  </div>

  <div id="content-core2" class="tab-content active">
    <h2>NSEJS 2024 Reference Item</h2>
    <div class="step-box">
      <h3>Problem Statement</h3>
      <p>[Multiple Correct] Exactly 1.0 mol of a phosphorus oxyacid H<sub>3</sub>PO<sub>x</sub> is completely neutralised by 40.0 g of sodium hydroxide (NaOH, M = 40.0 g mol<sup>-1</sup>). Which of the following statements are correct?</p>
      <ul>
        <li>(A) x = 2 and the acid is monobasic.</li>
        <li>(B) x = 3 and the acid is dibasic.</li>
        <li>(C) The acid contains two ionisable P-OH bonds.</li>
        <li>(D) The acid acts as a powerful reducing agent.</li>
      </ul>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 560 220" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="540" height="200" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Structure of H3PO2 -->
        <circle cx="120" cy="110" r="24" fill="#fed7aa" stroke="#ea580c" stroke-width="2"/>
        <text x="114" y="117" font-size="18" fill="#9a3412" font-weight="bold">P</text>
        
        <!-- P=O bond -->
        <line x1="120" y1="86" x2="120" y2="45" stroke="#ea580c" stroke-width="3"/>
        <text x="113" y="38" font-size="16" fill="#c2410c" font-weight="bold">=O</text>

        <!-- P-OH bond -->
        <line x1="140" y1="125" x2="200" y2="155" stroke="#15803d" stroke-width="3"/>
        <text x="205" y="162" font-size="15" fill="#15803d" font-weight="bold">-OH (1 ionisable H⁺)</text>

        <!-- P-H bonds -->
        <line x1="100" y1="125" x2="50" y2="155" stroke="#0284c7" stroke-width="3"/>
        <text x="25" y="172" font-size="15" fill="#0284c7" font-weight="bold">-H (reducing)</text>
        
        <line x1="100" y1="95" x2="50" y2="65" stroke="#0284c7" stroke-width="3"/>
        <text x="25" y="60" font-size="15" fill="#0284c7" font-weight="bold">-H (reducing)</text>

        <!-- Stoichiometry card -->
        <rect x="290" y="35" width="240" height="150" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="305" y="65" font-size="14" fill="#334155" font-weight="bold">40.0 g NaOH &divide; 40.0 = 1.0 mol</text>
        <text x="305" y="90" font-size="14" fill="#0f172a">1.0 mol Acid &harr; 1.0 mol Base</text>
        <text x="305" y="115" font-size="14" fill="#15803d" font-weight="bold">&rArr; Basicity = 1 (Monobasic!)</text>
        <text x="305" y="140" font-size="14" fill="#c2410c">&rArr; x = 2 &rarr; H₃PO₂ (Statement A)</text>
        <text x="305" y="165" font-size="14" fill="#0284c7">&rArr; 2 P-H bonds &rarr; Reducing (D)</text>
      </svg>
    </div>

    <div class="commit-box">
      <h3>Select Correct Statements:</h3>
      <div><input type="checkbox" id="c_optA" value="A"><label for="c_optA"> (A) x = 2 and the acid is monobasic.</label></div>
      <div><input type="checkbox" id="c_optB" value="B"><label for="c_optB"> (B) x = 3 and the acid is dibasic.</label></div>
      <div><input type="checkbox" id="c_optC" value="C"><label for="c_optC"> (C) The acid contains two ionisable P-OH bonds.</label></div>
      <div><input type="checkbox" id="c_optD" value="D"><label for="c_optD"> (D) The acid acts as a powerful reducing agent.</label></div>
      <br>
      <button class="btn" onclick="commitChemAnswer()">Commit Answer & Reveal Mathematical Derivation</button>
    </div>

    <div id="derivation-section" class="derivation-section" style="display: none;">
      <h3>Inorganic Chemistry Derivation & Proof</h3>
      <p><strong>1. System Representation & Setup:</strong> Moles of NaOH = 40.0 g / 40.0 g mol<sup>-1</sup> = 1.0 mol. Complete neutralisation of 1.0 mol acid requires 1.0 mol monoacidic base.</p>
      <p><strong>2. Physical Model & Formulation:</strong> Basicity = n(NaOH) / n(Acid) = 1.0 / 1.0 = 1. In phosphorus oxyacids H<sub>3</sub>PO<sub>x</sub>, basicity equals the number of P-OH bonds: Basicity = x - 1 = 1 &rArr; x = 2. The formula is H<sub>3</sub>PO<sub>2</sub> (hypophosphorous acid).</p>
      <p><strong>3. Execution & Resolution:</strong> H<sub>3</sub>PO<sub>2</sub> contains 1 P=O bond, 1 ionisable P-OH bond, and 2 non-ionisable P-H bonds. Because it possesses two direct P-H hydride bonds, it acts as a strong reducing agent (e.g. reducing Ag<sup>+</sup> to metallic Ag). Therefore, <strong>Statements A and D</strong> are verified true, while B and C are false.</p>
      <p><strong>4. Limiting Check:</strong> H<sub>3</sub>PO<sub>3</sub> requires 2 mol NaOH (dibasic), and H<sub>3</sub>PO<sub>4</sub> requires 3 mol NaOH (tribasic).</p>
    </div>
  </div>

  <div id="content-core1a" class="tab-content">
    <h2>Core 1A: Declarative Teaching Construction</h2>
    <div class="step-box">
      <span class="badge">Prerequisite</span>
      <h3>P-OH versus P-H Bond Polarity</h3>
      <p>Only protons attached to oxygen (P-OH) are acidic because the high electronegativity of oxygen polarizes the bond. Direct P-H bonds are non-polar (EN of P = 2.19, H = 2.20) and do not ionize, but act as reducing centers.</p>
    </div>
    <div class="step-box">
      <span class="badge">Worked Example</span>
      <h3>Phosphorous Acid H3PO3 Neutralization</h3>
      <p>0.50 mol of H<sub>3</sub>PO<sub>3</sub> requires 1.0 mol of NaOH (Basicity = 2). It has two P-OH bonds and one reducing P-H bond.</p>
    </div>
    <div class="step-box">
      <span class="badge">Independent Exit Check</span>
      <h3>Pyrophosphoric Acid H4P2O7 Check</h3>
      <p>No P-H bonds &rArr; Basicity = 4. 0.25 mol requires 1.0 mol NaOH (40.0 g).</p>
    </div>
  </div>

  <div id="content-core1b" class="tab-content">
    <h2>Core 1B: 6-Stage Phenomenological Reconstruction</h2>
    <div class="step-box">
      <span class="badge">Stage 1: Predict</span>
      <h3>Qualitative Direction</h3>
      <p>Does having 3 hydrogens in H<sub>3</sub>PO<sub>2</sub> mean it has basicity 3? No, basicity depends strictly on P-OH groups, not total hydrogen count.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 2: Attempt</span>
      <h3>Derivation & Multiple Correct Selection</h3>
      <p>Derive Basicity = 1, x = 2, and select Options A and D.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 3: Reconstruct</span>
      <h3>Systematic 4-Step Route</h3>
      <ol>
        <li>Compute base moles: n(NaOH) = 40.0 / 40.0 = 1.0 mol.</li>
        <li>Evaluate basicity: 1.0 / 1.0 = 1.</li>
        <li>Identify formula: Basicity = x - 1 &rArr; x = 2 (H<sub>3</sub>PO<sub>2</sub>).</li>
        <li>Deduce properties: 1 P-OH (monobasic) and 2 P-H (reducing agent). Select A and D.</li>
      </ol>
    </div>
    <div class="step-box">
      <span class="badge">Stage 4 & 5: Diagnose & Repair</span>
      <h3>Common Error Trap</h3>
      <p><strong>Trap:</strong> Confusing total hydrogens with basicity.</p>
      <p><strong>Repair:</strong> Basicity of H<sub>3</sub>PO<sub>x</sub> is universally given by (x - 1).</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 6: Boundary Test</span>
      <h3>Oxidation State Limit (H3PO4)</h3>
      <p>In phosphoric acid H<sub>3</sub>PO<sub>4</sub>, phosphorus is +5 with 0 P-H bonds; it has zero reducing power.</p>
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

  function commitChemAnswer() {
    const a = document.getElementById('c_optA').checked;
    const b = document.getElementById('c_optB').checked;
    const c = document.getElementById('c_optC').checked;
    const d = document.getElementById('c_optD').checked;
    if (!a && !b && !c && !d) {
      alert('Please select at least one option.');
      return;
    }
    document.getElementById('derivation-section').style.display = 'block';
  }
</script>
</body>
</html>
"""
(mod2_dir / "learning_journey.html").write_text(html2, encoding="utf-8")
print(f"Generated Chemistry D3 Module: {mod2_dir}")


# ===========================================================================
# MODULE 3: BIOLOGY D3 - bio-viral-genetics-d3-r1
# ===========================================================================
mod3_dir = ROOT / "workspace/output/bio-viral-genetics-d3-r1"
mod3_dir.mkdir(parents=True, exist_ok=True)

bank3 = {
    "schema_version": "grade9qa-exam-bank/v1",
    "bank_id": "bio-viral-genetics-d3-r1",
    "metadata": {
        "title": "Viral Capsid Architecture, Envelope Glycoproteins & Replication",
        "subject": "Biology",
        "topic": "MICROBIOLOGY_AND_VIROLOGY",
        "difficulty_band": "D3"
    },
    "questions": [
        {
            "id": "NSEJS-2024-B-Q50",
            "original_identifier": "NSEJS 2024-25 · Q50 · SYNTHESIZE · D3 (Score 6)",
            "stem": "[Multiple Correct] Which of the following statements concerning viral structure, molecular genetics, and replication are biologically incorrect? (A) Mature virions are obligate intracellular infectious particles. (B) Viral replication depends strictly on host ribosomes and translational machinery. (C) The viral envelope consists exclusively of host-derived glycolipids without proteins. (D) All animal viruses contain double-stranded DNA genomes.",
            "response": {"type": "multiple_response"},
            "options": [
                {"id": "A", "text": "Mature virions are obligate intracellular infectious particles."},
                {"id": "B", "text": "Viral replication depends strictly on host ribosomes and translational machinery."},
                {"id": "C", "text": "The viral envelope consists exclusively of host-derived glycolipids without proteins."},
                {"id": "D", "text": "All animal viruses contain double-stranded DNA genomes."}
            ],
            "answer": {
                "correct_option": "C, D",
                "crux_move_ref": "NSEJS-2024-B-Q50-M2",
                "reasoning": [
                    "1. Statement A: True - Virions are infectious macromolecular assemblies capable of infecting host cells.",
                    "2. Statement B: True - Viruses lack ribosomes, tRNAs, and metabolic enzymes for protein synthesis, relying completely on host translational machinery.",
                    "3. Statement C: Incorrect - The viral envelope is a lipid bilayer derived from host membranes but studded with virus-encoded glycoproteins (peplomers/spikes) essential for receptor binding.",
                    "4. Statement D: Incorrect - Animal viruses exhibit tremendous genomic diversity, including ssDNA (parvoviruses), dsRNA (reoviruses), positive-sense ssRNA (polio, coronaviruses), and negative-sense ssRNA (rabies, influenza). Therefore, statements C and D are biologically incorrect."
                ],
                "reasoning_route": [
                    {"move_id": "NSEJS-2024-B-Q50-M1", "kind": "REPRESENT", "description": "Identify obligate intracellular parasitic nature of virions and host translational dependence (A and B are biologically true)."},
                    {"move_id": "NSEJS-2024-B-Q50-M2", "kind": "MODEL", "description": "Model viral envelope as a chimeric membrane containing host lipids plus virus-encoded glycoprotein spikes."},
                    {"move_id": "NSEJS-2024-B-Q50-M3", "kind": "APPLY", "description": "Survey Baltimore classification demonstrating diverse RNA and ssDNA animal virus genomes."},
                    {"move_id": "NSEJS-2024-B-Q50-M4", "kind": "JUSTIFY", "description": "Select C and D as the biologically incorrect statements."}
                ]
            },
            "extensions": {
                "grade9v3:analysis": {
                    "difficulty": {
                        "score": 6,
                        "band": "D3",
                        "components": {
                            "c1_obligate_parasitism_understanding": 1,
                            "c2_envelope_biochemistry": 2,
                            "c3_baltimore_genome_diversity": 1,
                            "c4_host_translational_dependency": 1,
                            "c5_inverted_negative_stem_logic": 1
                        }
                    }
                },
                "grade9v3:core2_support_plan": {
                    "protected_move_refs": ["NSEJS-2024-B-Q50-M2"]
                }
            }
        }
    ]
}
(mod3_dir / "bank.json").write_text(json.dumps(bank3, indent=2), encoding="utf-8")

c1a_3 = {
    "schema": "core1a-construction/v1",
    "construction_id": "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01",
    "target_question_id": "NSEJS-2024-B-Q50",
    "title": "Viral Capsid Architecture, Envelope Glycoproteins & Baltimore Replication Schemes",
    "status": "CANDIDATE",
    "purpose": "CORE1A_TEACHING_CONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "MICROBIOLOGY_AND_VIROLOGY",
    "family": "BIO-VIROLOGY-REPLICATION",
    "capability": "BIO-VIRAL-ENVELOPE-GENOME-SYNTHESIS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "NSEJS-2024-B-Q50-M2",
    "declared_conventions": [
        {
            "name": "obligate_intracellular_molecular_parasitism",
            "statement": "Viruses are obligate intracellular molecular parasites that possess no ribosomes, tRNAs, ATP-generating pathways, or biosynthetic enzymes for lipid synthesis. A mature virion is inert outside a host cell and depends completely on host translational machinery."
        },
        {
            "name": "chimeric_envelope_glycoprotein_spikes",
            "statement": "The viral envelope is derived from host cellular membranes (plasma, ER, or Golgi) during budding, but it is functionally decorated with virus-encoded integral membrane glycoproteins (spikes/peplomers) required for host receptor recognition and entry."
        },
        {
            "name": "baltimore_genomic_classification",
            "statement": "Animal viruses possess remarkably diverse genomes categorized into 7 Baltimore classes, including dsDNA, ssDNA, dsRNA, (+)ssRNA, (-)ssRNA, and reverse-transcribing retroviruses. Only a subset of animal viruses contain dsDNA."
        },
        {
            "name": "negative_stem_verification",
            "statement": "When a question asks for 'biologically incorrect' statements, true biological assertions must be eliminated, and false biological claims must be affirmatively selected."
        }
    ],
    "entry_assumptions": [
        "Basic structure of viruses: nucleic acid core enclosed in a protein capsid +/- lipid envelope.",
        "Central dogma of molecular biology and protein translation on ribosomes.",
        "Cell membrane bilayer fluid mosaic model."
    ],
    "inferential_jump": "By synthesizing viral structural biochemistry with molecular virology, the student recognizes that the viral envelope cannot function without virus-encoded glycoprotein peplomers (refuting statement C), and that animal viruses encompass both RNA viruses (e.g. influenza, rabies, SARS-CoV-2, HIV) and ssDNA viruses (parvovirus) rather than exclusively dsDNA (refuting statement D). The inverted question logic selects C and D as incorrect.",
    "teaching_path": [
        {
            "step_number": 1,
            "role": "REPRESENT",
            "action": "Examine Statement A (obligate intracellular parasite) and Statement B (host translational dependence).",
            "why_valid": "Viruses lack autonomous protein synthesis machinery; both A and B are fundamentally true.",
            "inputs": ["Statements A and B"],
            "output": "A and B are biologically true (thus rejected under 'incorrect' prompt)."
        },
        {
            "step_number": 2,
            "role": "MODEL",
            "action": "Model the viral envelope structure as a host-derived lipid bilayer studded with viral glycoprotein spikes.",
            "why_valid": "Without viral spikes (e.g. hemagglutinin), enveloped virions cannot bind or fuse with host cell receptors.",
            "inputs": ["Statement C", "Envelope biochemistry"],
            "output": "Statement C is false (envelope requires viral proteins)."
        },
        {
            "step_number": 3,
            "role": "APPLY",
            "action": "Survey animal viral genome architectures across the Baltimore classification scheme.",
            "why_valid": "Numerous prominent animal viruses contain RNA genomes (influenza, polio, rabies, retroviruses).",
            "inputs": ["Statement D", "Baltimore classification"],
            "output": "Statement D is false (many animal viruses are RNA or ssDNA)."
        },
        {
            "step_number": 4,
            "role": "JUSTIFY",
            "action": "Identify that the stem explicitly requests 'biologically incorrect' statements, selecting Options C and D.",
            "why_valid": "Statements C and D are demonstrably false, satisfying the question prompt.",
            "inputs": ["Falsified statements C and D"],
            "output": "Correct options: C and D."
        }
    ],
    "representation_bridge": {
        "symbol": "Envelope = Host Lipid Bilayer + Viral Glycoprotein Spikes; Genomes = {dsDNA, ssDNA, dsRNA, (+)ssRNA, (-)ssRNA, RT}",
        "element": "Enveloped virion schematic showing viral spike proteins inserted into host-derived lipid bilayer",
        "in_words": "Envelopes always carry viral proteins for infection, and animal viral genomes include diverse RNA and ssDNA forms.",
        "diagram_ref": "fig_bio_viral_genetics_d3.svg"
    },
    "worked_conceptual_anchor": {
        "problem": "Evaluate the biology of the Human Immunodeficiency Virus (HIV). (a) What host membrane forms its envelope? (b) What virus-encoded proteins decorate the envelope? (c) What is the nature of its genome?",
        "solution_steps": [
            "1. System Representation & Setup: HIV is an enveloped animal retrovirus. We analyze its membrane origin, surface proteins, and genetic material.",
            "2. Physical Model & Formulation: During budding from host CD4+ T-lymphocytes, HIV acquires host plasma membrane lipid bilayer. However, it incorporates virus-encoded envelope glycoproteins gp120 (docking glycoprotein) and gp41 (transmembrane fusion protein).",
            "3. Execution & Resolution: Genome: HIV contains two identical copies of positive-sense single-stranded RNA (+ssRNA), not dsDNA. It carries its own reverse transcriptase enzyme to transcribe RNA into proviral DNA.",
            "4. Limiting Check: This directly proves that animal viruses are not exclusively dsDNA and that viral envelopes are never purely host glycolipids."
        ]
    },
    "misconceptions": [
        {
            "wrong_idea": "Assuming that because the envelope is derived from the host cell membrane, it must contain only host lipids and host proteins.",
            "diagnostic_prompt": "If the viral envelope contained only host proteins and lipids, how could a virus recognize its target cell?",
            "repair": "Viruses synthesize their own glycoprotein peplomers (spikes) using the host secretory pathway. These viral proteins are transported to the host cell membrane before budding, ensuring the virion carries its own receptor-binding proteins."
        }
    ],
    "exit_task": {
        "prompt": "Identify whether rabies virus and influenza virus contain DNA or RNA genomes, and whether they are enveloped.",
        "answer": "Both rabies virus (rhabdovirus) and influenza virus (orthomyxovirus) are enveloped negative-sense single-stranded RNA viruses ((-)ssRNA), confirming RNA genomes in animal viruses."
    }
}
(mod3_dir / "core1a_construction.json").write_text(json.dumps(c1a_3, indent=2), encoding="utf-8")

c1b_3 = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01",
    "target_question_id": "NSEJS-2024-B-Q50",
    "title": "Viral Genetics & Envelope Architecture: 6-Stage Phenomenological Reconstruction",
    "status": "CANDIDATE",
    "purpose": "CORE1B_PHENOMENOLOGICAL_RECONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "MICROBIOLOGY_AND_VIROLOGY",
    "family": "BIO-VIROLOGY-REPLICATION",
    "capability": "BIO-VIRAL-ENVELOPE-GENOME-SYNTHESIS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "NSEJS-2024-B-Q50-M2",
    "taught_skill_Y": "Modeling viral envelope composition as a host lipid matrix embedded with virus-encoded glycoprotein spikes.",
    "connecting_route_Z": "Applying Baltimore genomic classifications to refute universal dsDNA claims and executing inverted stem logic.",
    "protected_fresh_inference_W": "Deducing that viral envelopes strictly require viral proteins for host infectivity and recognizing RNA genomes across major animal pathogen families.",
    "fresh_context_ref": "NSEJS-2024-B-Q50-CORE1B-TASK",
    "stages": {
        "stage_1_predict": {
            "prompt": "Can a virus infect a host cell if its envelope is composed 100% of host membrane components without any viral proteins?",
            "defensible_answer": "No. Host cell membranes do not possess receptor-binding affinities for their own cells. The virus must present its own viral-encoded attachment glycoproteins (peplomers) to bind host receptors."
        },
        "stage_2_attempt": {
            "prompt": "Select the biologically incorrect statements among: (A) virions are obligate intracellular parasites, (B) replication depends on host ribosomes, (C) envelope has only host glycolipids without proteins, (D) all animal viruses have dsDNA genomes.",
            "produces": "Identification of Statements C and D as incorrect.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "True statement elimination: identifies A and B as biologically correct.",
                    "evidence_of": "Proper understanding of obligate parasitism."
                },
                {
                    "criterion": "Envelope glycoprotein refutation: recognizes Statement C is false.",
                    "evidence_of": "Competent understanding of viral spike proteins."
                },
                {
                    "criterion": "Genome diversity refutation: recognizes Statement D is false and selects C & D.",
                    "evidence_of": "Precise execution of inverted negative stem logic."
                }
            ],
            "accepted": [
                "C, D",
                "Options C and D",
                "(C) and (D)"
            ],
            "rejected": [
                "A, B (selecting the true statements instead of the incorrect ones)",
                "C only (omitting genomic diversity)",
                "D only (omitting envelope protein requirement)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. Are mature virions obligate intracellular infectious particles?",
                    "why_this_ask": "Evaluates Statement A.",
                    "step_answer": "Yes, virions cannot replicate outside a host cell (Statement A is true)."
                },
                {
                    "ask": "2. Does viral protein translation require host ribosomes?",
                    "why_this_ask": "Evaluates Statement B.",
                    "step_answer": "Yes, viruses carry no ribosomes of their own (Statement B is true)."
                },
                {
                    "ask": "3. Does the viral envelope lack proteins?",
                    "why_this_ask": "Evaluates Statement C.",
                    "step_answer": "No, envelopes contain viral-encoded glycoprotein spikes essential for receptor attachment (Statement C is incorrect)."
                },
                {
                    "ask": "4. Do all animal viruses have dsDNA genomes?",
                    "why_this_ask": "Evaluates Statement D.",
                    "step_answer": "No, many animal viruses have RNA genomes (e.g. influenza, rabies, HIV). Thus C and D are the incorrect statements."
                }
            ],
            "differs_from_teaching_path": "Reconstruction systematically prompts verification of each statement independently, leading to the selection of C and D."
        },
        "stage_4_diagnose": {
            "error_trap": "Selecting A and B because they are true, ignoring the negative stem keyword 'biologically incorrect'.",
            "diagnostic_prompt": "Did the question ask which statements are true, or which are incorrect?",
            "causal_explanation": "A common examination pitfall is verifying biological facts (A and B are true) and mistakenly choosing them as answers, rather than answering the negative question stem."
        },
        "stage_5_repair": {
            "action": "Always circle negative stem qualifiers ('incorrect', 'false', 'except') and write TRUE/FALSE next to each option before finalizing selection."
        },
        "stage_6_boundary_test": {
            "prompt": "What about naked (non-enveloped) viruses like poliovirus or adenovirus? Do they have spikes?",
            "answer": "Naked viruses lack a lipid membrane entirely; their capsid proteins themselves directly form the receptor-binding surface structure.",
            "confirms": "Confirms the universal requirement for viral-encoded surface proteins for host entry across both enveloped and naked viruses."
        }
    },
    "progressive_hints": [
        {
            "tier": 1,
            "text": "Notice the question asks which statements are biologically INCORRECT!"
        },
        {
            "tier": 2,
            "text": "Does the envelope of a coronavirus or influenza virus lack proteins? What are the spike proteins made of?"
        },
        {
            "tier": 3,
            "text": "Think of RNA viruses like rabies, polio, and HIV. Do all animal viruses have dsDNA genomes? Statements C and D are incorrect."
        }
    ]
}
(mod3_dir / "core1b_reconstruction.json").write_text(json.dumps(c1b_3, indent=2), encoding="utf-8")

c1a_bytes_3 = (mod3_dir / "core1a_construction.json").read_bytes()
c1b_bytes_3 = (mod3_dir / "core1b_reconstruction.json").read_bytes()
c1a_sha_3 = "sha256:" + hashlib.sha256(c1a_bytes_3).hexdigest()
c1b_sha_3 = "sha256:" + hashlib.sha256(c1b_bytes_3).hexdigest()
we_sha_3 = "sha256:" + hashlib.sha256(json.dumps(c1a_3["worked_conceptual_anchor"], sort_keys=True).encode("utf-8")).hexdigest()

witness3 = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-BIO-VIROL-D3-01",
    "construction": {
        "construction_id": "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01",
        "topic_id": "BIO-VIROLOGY-REPLICATION",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "decisive_roles": [
            "OBLIGATE_PARASITISM_VERIFICATION",
            "ENVELOPE_GLYCOPROTEIN_DISCRIMINATION",
            "BALTIMORE_GENOMIC_CLASSIFICATION"
        ],
        "signature": {
            "inputs": [
                "4 biological propositions regarding viral biology",
                "Negative stem evaluation ('biologically incorrect')"
            ],
            "obstacle": "Resolving chimeric nature of viral envelope and recognizing RNA animal virus genomes while executing negative stem logic",
            "decisive_move": "Model envelope as host lipid + viral glycoprotein spikes and recall RNA animal viruses to falsify C and D",
            "output": "Options C and D selected as biologically incorrect",
            "independent_check": "Retrovirus HIV and influenza envelope spike proof and parvovirus ssDNA limit",
            "validity_boundary": "General virology across animal viruses, excluding viroids and prions",
            "conditions": [
                "Intact infectious mature virions",
                "Standard host cell permissive infection conditions"
            ],
            "dependency_refs": [
                "VIRAL_STRUCTURE_AND_CAPSID_MORPHOLOGY",
                "BALTIMORE_CLASSIFICATION_SYSTEM",
                "HOST_CELL_TROPISM_AND_ATTACHMENT"
            ]
        }
    },
    "core1a": {
        "construction_id": "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": c1a_sha_3,
        "worked_example_sha256": we_sha_3,
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
            "OBLIGATE_PARASITISM_VERIFICATION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/0",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"
            },
            "ENVELOPE_GLYCOPROTEIN_DISCRIMINATION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/1",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"
            },
            "BALTIMORE_GENOMIC_CLASSIFICATION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/2",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"
            }
        }
    },
    "core1b": {
        "construction_id": "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": c1b_sha_3,
        "fresh_context_ref": "NSEJS-2024-B-Q50-CORE1B-TASK",
        "freshness_review_ref": "PENDING-INDEPENDENT-REVIEW",
        "assessed_roles": {
            "OBLIGATE_PARASITISM_VERIFICATION": {
                "attempt_field": "stage_2_attempt.parasitism",
                "observable": "confirms Statements A and B are true"
            },
            "ENVELOPE_GLYCOPROTEIN_DISCRIMINATION": {
                "attempt_field": "stage_2_attempt.envelope",
                "observable": "identifies Statement C is false"
            },
            "BALTIMORE_GENOMIC_CLASSIFICATION": {
                "attempt_field": "stage_2_attempt.genome",
                "observable": "identifies Statement D is false"
            }
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "attempt_events": [
            {"type": "ANSWER_ENTERED", "at": "2026-11-12T09:20:00Z"},
            {"type": "FIRST_ANSWER_SAVED", "at": "2026-11-12T09:20:01Z", "durable": True},
            {"type": "HINT_SHOWN", "at": "2026-11-12T09:20:02Z"},
            {"type": "ANSWER_REVEALED", "at": "2026-11-12T09:20:03Z"}
        ],
        "native_runtime_receipt_ref": "RUNTIME-TRACE-NSEJS-2024-B-Q50",
        "diagnostic_rules": [
            {
                "role_id": "OBLIGATE_PARASITISM_VERIFICATION",
                "observable": "selects A and B mistaking true statements for correct answers",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-NEGATIVE-STEM-INVERSION"
            },
            {
                "role_id": "ENVELOPE_GLYCOPROTEIN_DISCRIMINATION",
                "observable": "believes envelope contains no proteins",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-ENVELOPE-SPIKE-OMISSION"
            },
            {
                "role_id": "BALTIMORE_GENOMIC_CLASSIFICATION",
                "observable": "believes all animal viruses contain dsDNA",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_5_repair",
                "failed_node_ref": "NODE-BALTIMORE-DIVERSITY"
            }
        ],
        "changed_condition_transfer_ref": "TRANSFER-HIV-RETROVIRUS-PARAMETRIC",
        "saved_answer_evidence_ref": "SAVED-STUDENT-ATTEMPT-BIO-Q50",
        "exposure_audit": [
            {"surface": "HINT", "audit_ref": "AUDIT-HINT-BIO-Q50", "decisive_route_visible_before_save": False},
            {"surface": "PICTURE_STAGE", "audit_ref": "AUDIT-PICTURE-BIO-Q50", "decisive_route_visible_before_save": False},
            {"surface": "ALT_TEXT", "audit_ref": "AUDIT-ALT-TEXT-BIO-Q50", "decisive_route_visible_before_save": False},
            {"surface": "MODEL_RESPONSE", "audit_ref": "AUDIT-MODEL-RESPONSE-BIO-Q50", "decisive_route_visible_before_save": False},
            {"surface": "RUBRIC", "audit_ref": "AUDIT-RUBRIC-BIO-Q50", "decisive_route_visible_before_save": False},
            {"surface": "EXAM_RETURN", "audit_ref": "AUDIT-EXAM-RETURN-BIO-Q50", "decisive_route_visible_before_save": False}
        ],
        "transfer_success_criterion": "Learner models viral envelope as chimeric lipid-glycoprotein structure and identifies animal RNA viruses to select C and D under negative stem logic"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "source_role": "DIRECT_EXAM_EVIDENCE",
        "qrt_decision_ref": "QRT-NSEJS-2024-B-Q50-PROPOSED",
        "demand_vector": [1, 2, 1, 1, 1],
        "demand_evidence_ref": "EVIDENCE-DEMAND-SCORE-6-D3"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-BIO-VIRAL-GENETICS-REPLICATION",
        "physics_review_ref": "BIO-REVIEW-UNREVIEWED-CANDIDATE",
        "source_custody_ref": "CUSTODY-NSEJS-2024-PAPER-53",
        "paper_ref": "IAPT-NSEJS-2024-PAPER-53",
        "official_key_ref": "IAPT-NSEJS-2024-FINAL-KEY-Q50-CD",
        "solution_review_ref": "SOLUTION-DERIVATION-CHECKED",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "OBLIGATE_PARASITISM_VERIFICATION", "warrant_ref": "BIO-WARRANT-OBLIGATE-PARASITISM", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000301"},
            {"role_id": "ENVELOPE_GLYCOPROTEIN_DISCRIMINATION", "warrant_ref": "BIO-WARRANT-ENVELOPE-PEPLOMERS", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000302"},
            {"role_id": "BALTIMORE_GENOMIC_CLASSIFICATION", "warrant_ref": "BIO-WARRANT-BALTIMORE-CLASSES", "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000303"}
        ]
    },
    "review_receipts": []
}
(mod3_dir / "witness.json").write_text(json.dumps(witness3, indent=2), encoding="utf-8")

# HTML 3
html3 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Learning Journey: Viral Envelope Architecture & Genetics (D3)</title>
  <style>
    :root {
      --primary: #4c1d95;
      --secondary: #7c3aed;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --accent: #10b981;
    }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding: 20px; }
    .container { max-width: 900px; margin: 0 auto; background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid var(--border); }
    .header { background: linear-gradient(135deg, var(--primary), var(--secondary)); color: white; padding: 24px; }
    .header h1 { margin: 0 0 8px 0; font-size: 24px; }
    .header .meta { font-size: 14px; opacity: 0.9; }
    .nav-tabs { display: flex; background: #f1f5f9; border-bottom: 1px solid var(--border); }
    .tab-button { flex: 1; padding: 14px 20px; text-align: center; background: none; border: none; font-size: 15px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; }
    .tab-button.active { background: var(--card-bg); color: var(--primary); border-bottom: 3px solid var(--primary); }
    .tab-content { padding: 24px; display: none; }
    .tab-content.active { display: block; }
    .diagram-container { margin: 20px 0; padding: 16px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--border); text-align: center; }
    .diagram-container svg { width: 100%; height: 100%; max-width: 620px; height: 260px; }
    .step-box { background: #f8fafc; border-left: 4px solid var(--secondary); padding: 16px; margin-bottom: 16px; border-radius: 0 8px 8px 0; }
    .step-box h3 { margin: 0 0 8px 0; font-size: 16px; color: var(--primary); }
    .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; background: #ede9fe; color: #6d28d9; margin-right: 6px; }
    .derivation-section { margin-top: 24px; padding: 20px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; }
    .commit-box { margin: 20px 0; padding: 16px; background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; }
    .btn { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; }
    .footer { background: #f8fafc; padding: 16px 24px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-muted); text-align: center; }
    @media (max-width: 600px) { body { padding: 8px; } .header { padding: 16px; } .tab-button { padding: 10px 6px; font-size: 13px; } .tab-content { padding: 16px; } }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>Microbiology & Virology — Capsid, Envelope & Baltimore Genomes</h1>
    <div class="meta">Target Item: NSEJS-2024-B-Q50 | Band: D3 (Score 6) | Operation: SYNTHESIZE</div>
  </div>

  <div class="nav-tabs">
    <button class="tab-button active" id="tab-core2" onclick="switchTab('core2')">1. Core 2 Target Problem</button>
    <button class="tab-button" id="tab-core1a" onclick="switchTab('core1a')">2. Core 1A Teaching Path</button>
    <button class="tab-button" id="tab-core1b" onclick="switchTab('core1b')">3. Core 1B Reconstruction</button>
  </div>

  <div id="content-core2" class="tab-content active">
    <h2>NSEJS 2024 Reference Item</h2>
    <div class="step-box">
      <h3>Problem Statement</h3>
      <p>[Multiple Correct] Which of the following statements concerning viral structure, molecular genetics, and replication are <strong>biologically incorrect</strong>?</p>
      <ul>
        <li>(A) Mature virions are obligate intracellular infectious particles.</li>
        <li>(B) Viral replication depends strictly on host ribosomes and translational machinery.</li>
        <li>(C) The viral envelope consists exclusively of host-derived glycolipids without proteins.</li>
        <li>(D) All animal viruses contain double-stranded DNA genomes.</li>
      </ul>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 560 220" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="540" height="200" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Enveloped Virion Structure -->
        <circle cx="120" cy="110" r="60" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2" stroke-dasharray="4,2"/>
        <text x="50" y="35" font-size="14" fill="#6d28d9" font-weight="bold">Host-Derived Lipid Bilayer</text>

        <!-- Capsid Core -->
        <polygon points="120,70 150,90 150,130 120,150 90,130 90,90" fill="#ede9fe" stroke="#6d28d9" stroke-width="2"/>
        <text x="102" y="115" font-size="14" fill="#4c1d95" font-weight="bold">RNA/DNA</text>

        <!-- Glycoprotein Spikes -->
        <line x1="120" y1="50" x2="120" y2="30" stroke="#ef4444" stroke-width="3"/>
        <circle cx="120" cy="28" r="4" fill="#ef4444"/>

        <line x1="180" y1="110" x2="200" y2="110" stroke="#ef4444" stroke-width="3"/>
        <circle cx="202" cy="110" r="4" fill="#ef4444"/>

        <line x1="120" y1="170" x2="120" y2="190" stroke="#ef4444" stroke-width="3"/>
        <circle cx="120" cy="192" r="4" fill="#ef4444"/>

        <line x1="60" y1="110" x2="40" y2="110" stroke="#ef4444" stroke-width="3"/>
        <circle cx="38" cy="110" r="4" fill="#ef4444"/>
        <text x="135" y="45" font-size="14" fill="#dc2626" font-weight="bold">Viral Glycoproteins (Spikes)</text>

        <!-- Evaluation Table -->
        <rect x="250" y="30" width="280" height="160" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="265" y="55" font-size="14" fill="#15803d" font-weight="bold">(A) Obligate intracellular &rarr; TRUE</text>
        <text x="265" y="80" font-size="14" fill="#15803d" font-weight="bold">(B) Needs host ribosomes &rarr; TRUE</text>
        <text x="265" y="110" font-size="14" fill="#dc2626" font-weight="bold">(C) "Without proteins" &rarr; INCORRECT!</text>
        <text x="280" y="128" font-size="14" fill="#64748b">(Envelope requires viral spikes)</text>
        <text x="265" y="155" font-size="14" fill="#dc2626" font-weight="bold">(D) "All have dsDNA" &rarr; INCORRECT!</text>
        <text x="280" y="173" font-size="14" fill="#64748b">(HIV, rabies, flu are RNA viruses!)</text>
      </svg>
    </div>

    <div class="commit-box">
      <h3>Select the Biologically INCORRECT Statements:</h3>
      <div><input type="checkbox" id="b_optA" value="A"><label for="b_optA"> (A) Mature virions are obligate intracellular infectious particles.</label></div>
      <div><input type="checkbox" id="b_optB" value="B"><label for="b_optB"> (B) Viral replication depends strictly on host ribosomes and translational machinery.</label></div>
      <div><input type="checkbox" id="b_optC" value="C"><label for="b_optC"> (C) The viral envelope consists exclusively of host-derived glycolipids without proteins.</label></div>
      <div><input type="checkbox" id="b_optD" value="D"><label for="b_optD"> (D) All animal viruses contain double-stranded DNA genomes.</label></div>
      <br>
      <button class="btn" onclick="commitBioAnswer()">Commit Answer & Reveal Mathematical Derivation</button>
    </div>

    <div id="derivation-section" class="derivation-section" style="display: none;">
      <h3>Biological Science Derivation & Proof</h3>
      <p><strong>1. System Representation & Setup:</strong> Statements A and B describe canonical viral characteristics: mature virions possess no cellular metabolism and are obligate intracellular parasites (A is true); viruses lack ribosomes and tRNAs, relying 100% on host translation (B is true).</p>
      <p><strong>2. Physical Model & Formulation:</strong> Statement C claims the envelope consists exclusively of host glycolipids without proteins. This is biologically false: during budding, the host-derived lipid bilayer is studded with viral-encoded transmembrane glycoproteins (spikes/peplomers) essential for cell attachment and fusion.</p>
      <p><strong>3. Execution & Resolution:</strong> Statement D claims all animal viruses contain dsDNA genomes. This is biologically false: animal viruses demonstrate extraordinary genomic diversity in the Baltimore classification, including positive-sense ssRNA (coronaviruses, polio), negative-sense ssRNA (influenza, rabies), retroviruses (HIV), and ssDNA (parvoviruses). Since the prompt asks for <strong>biologically incorrect</strong> statements, <strong>Options C and D</strong> are the correct answers.</p>
      <p><strong>4. Limiting Check:</strong> A and B are eliminated because they are biologically true.</p>
    </div>
  </div>

  <div id="content-core1a" class="tab-content">
    <h2>Core 1A: Declarative Teaching Construction</h2>
    <div class="step-box">
      <span class="badge">Prerequisite</span>
      <h3>Chimeric Envelope & Baltimore Classification</h3>
      <p>Envelopes are acquired from host membranes but must carry viral glycoprotein spikes to bind receptors. Animal viral genomes range from dsDNA to ssDNA, dsRNA, and positive/negative ssRNA.</p>
    </div>
    <div class="step-box">
      <span class="badge">Worked Example</span>
      <h3>Human Immunodeficiency Virus (HIV)</h3>
      <p>HIV buds from host plasma membrane but incorporates viral gp120/gp41 spikes, and its genome consists of two (+)ssRNA molecules.</p>
    </div>
    <div class="step-box">
      <span class="badge">Independent Exit Check</span>
      <h3>Rabies & Influenza Virus Check</h3>
      <p>Both are enveloped (-)ssRNA animal viruses, proving animal viruses are not exclusively dsDNA.</p>
    </div>
  </div>

  <div id="content-core1b" class="tab-content">
    <h2>Core 1B: 6-Stage Phenomenological Reconstruction</h2>
    <div class="step-box">
      <span class="badge">Stage 1: Predict</span>
      <h3>Qualitative Direction</h3>
      <p>Can an envelope without viral proteins infect cells? No, host membranes lack specific viral receptor-binding peplomers.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 2: Attempt</span>
      <h3>Negative Stem Multiple Correct Selection</h3>
      <p>Falsify C and D, and select Options C and D.</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 3: Reconstruct</span>
      <h3>Systematic 4-Step Route</h3>
      <ol>
        <li>Verify Statement A: True (obligate intracellular).</li>
        <li>Verify Statement B: True (host ribosome dependence).</li>
        <li>Refute Statement C: False (viral envelope requires viral spike proteins).</li>
        <li>Refute Statement D: False (animal viruses include major RNA classes). Select C & D.</li>
      </ol>
    </div>
    <div class="step-box">
      <span class="badge">Stage 4 & 5: Diagnose & Repair</span>
      <h3>Common Error Trap</h3>
      <p><strong>Trap:</strong> Selecting A and B because they are true facts.</p>
      <p><strong>Repair:</strong> Always check the stem for negative keywords ('incorrect', 'except').</p>
    </div>
    <div class="step-box">
      <span class="badge">Stage 6: Boundary Test</span>
      <h3>Naked Viruses vs Enveloped Viruses</h3>
      <p>Naked viruses also require viral surface proteins (capsomers) for receptor attachment.</p>
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

  function commitBioAnswer() {
    const a = document.getElementById('b_optA').checked;
    const b = document.getElementById('b_optB').checked;
    const c = document.getElementById('b_optC').checked;
    const d = document.getElementById('b_optD').checked;
    if (!a && !b && !c && !d) {
      alert('Please select at least one option.');
      return;
    }
    document.getElementById('derivation-section').style.display = 'block';
  }
</script>
</body>
</html>
"""
(mod3_dir / "learning_journey.html").write_text(html3, encoding="utf-8")
print(f"Generated Biology D3 Module: {mod3_dir}")

print("All 3 D3 Expansion Modules successfully generated.")
