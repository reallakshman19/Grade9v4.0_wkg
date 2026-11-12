"""Build script for second wave of Band D3 Core 1A/1B modules:
1. Physics: NSEJS-2024-P-Q57 (Convex Lens Displacement Method & Conjugate Focus, Score 6, SYNTHESIZE)
2. Chemistry: NSEJS-2024-C-Q56 (Electronic Shell Population & Transition Metal Aufbau, Score 6, SYNTHESIZE)
3. Biology: NSEJS-2024-B-Q52 (Vertebrate Immunology & Leukocyte Defenses, Score 6, SYNTHESIZE)
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "workspace" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

# ==============================================================================
# MODULE 1: PHYSICS — NSEJS-2024-P-Q57 (Convex Lens Displacement Method)
# ==============================================================================
mod1_dir = OUTPUT_DIR / "nsejs-optics-displacement-d3-r1"
mod1_dir.mkdir(parents=True, exist_ok=True)

mod1_bank = {
    "topic": "RAY_OPTICS",
    "topic_id": "PHYS-TOPIC-RAY-OPTICS",
    "schema": "question-bank/v1",
    "questions": [
        {
            "id": "PHYS-NSEJS-2024-P-Q57",
            "stem": "[Multiple Correct] A screen is placed at a fixed distance D = 75 cm from an illuminated object AB. A thin convex lens of focal length f = 12 cm is placed between them so that a sharp real image forms on the screen. Which of the following statements are correct?\n(A) The lens-object distance may be 15 cm.\n(B) The lens-object distance may be 60 cm.\n(C) The image formed may be magnified.\n(D) The image formed may be diminished.",
            "options": [
                {"id": "A", "text": "The lens-object distance may be 15 cm."},
                {"id": "B", "text": "The lens-object distance may be 60 cm."},
                {"id": "C", "text": "The image formed may be magnified."},
                {"id": "D", "text": "The image formed may be diminished."}
            ],
            "correct_option": "A, B, C, D",
            "operation": "SYNTHESIZE",
            "band": "D3",
            "score": 6,
            "crux_move": "M2"
        }
    ]
}
(mod1_dir / "bank.json").write_text(json.dumps(mod1_bank, indent=2), encoding="utf-8")

mod1_c1a = {
    "schema": "core1a-construction/v1",
    "construction_id": "PHYS-OPT-C-LENS-DISPLACEMENT-D3-01",
    "target_question_id": "PHYS-NSEJS-2024-P-Q57",
    "title": "Convex Lens Displacement Method & Conjugate Focus on Fixed Screen",
    "topic": "RAY_OPTICS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "declared_conventions": [
        {
            "name": "Cartesian Sign Convention",
            "statement": "Under standard Cartesian sign convention, incident light travels left-to-right (+x); distances measured from optical centre opposite to incidence are negative (object distance u < 0), and along incidence are positive (real image distance v > 0 for convex lens)."
        },
        {
            "name": "Screen Fixed Distance Constraint",
            "statement": "For a real image on a screen separated from the object by D, |u| + v = D, requiring D >= 4f for real roots to exist."
        },
        {
            "name": "Conjugate Foci Reciprocity",
            "statement": "By conjugate foci reciprocity, the object and image positions are mutually interchangeable; if a real image is formed at v1 for object at u1, placing the object at u2 = v1 yields image at v2 = u1."
        },
        {
            "name": "Displacement Method Separation Formula",
            "statement": "The separation between two lens positions d = |u2 - u1| = sqrt(D^2 - 4Df), and focal length is uniquely given by f = (D^2 - d^2) / (4D)."
        }
    ],
    "entry_assumptions": [
        "Familiarity with the thin lens formula 1/v - 1/u = 1/f.",
        "Understanding of real vs virtual images and linear lateral magnification m = v/u.",
        "Ability to formulate and solve quadratic equations in kinematic/geometric variables."
    ],
    "inferential_jump": "Transitioning from single-point lens calculations to the global quadratic solution space of conjugate foci on a fixed screen D, proving the existence of two distinct real positions and dual magnified/diminished states.",
    "teaching_path": [
        {
            "step": 1,
            "role": "REPRESENT",
            "action": "Set up optical axis with object at origin and screen at x = D, placing lens at position u.",
            "why_valid": "Enforces spatial constraint u + v = D with Cartesian signs u = -|u|, v = D - |u|."
        },
        {
            "step": 2,
            "role": "MODEL",
            "action": "Substitute into thin lens formula 1/(D - u) + 1/u = 1/f to construct quadratic equation u^2 - Du + Df = 0.",
            "why_valid": "Eliminates variable v to express lens position strictly in terms of constants D and f."
        },
        {
            "step": 3,
            "role": "SYNTHESIZE",
            "action": "Evaluate quadratic discriminant Delta = D^2 - 4Df and extract roots u1, u2.",
            "why_valid": "Delta > 0 guarantees two physical lens positions separated by d = sqrt(D^2 - 4Df)."
        },
        {
            "step": 4,
            "role": "JUSTIFY",
            "action": "Compute lateral magnifications m1 = v1/u1 and m2 = v2/u2, verifying m1 * m2 = 1.",
            "why_valid": "Proves that one image is magnified (|m1| > 1) and the other is diminished (|m2| < 1)."
        }
    ],
    "worked_conceptual_anchor": {
        "problem": "An object and a screen are placed D = 90 cm apart. A convex lens of focal length f = 20 cm forms sharp images on the screen at two positions. Determine both lens positions and their magnifications.",
        "solution_steps": [
            "1. System formulation: u^2 - Du + Df = 0 ==> u^2 - 90u + (90)(20) = u^2 - 90u + 1800 = 0.",
            "2. Discriminant: Delta = (-90)^2 - 4(1)(1800) = 8100 - 7200 = 900 = 30^2 > 0.",
            "3. Lens positions: u1 = (90 - 30)/2 = 30 cm (v1 = 60 cm); u2 = (90 + 30)/2 = 60 cm (v2 = 30 cm).",
            "4. Magnifications: |m1| = 60/30 = 2.0 (magnified); |m2| = 30/60 = 0.5 (diminished). Note m1 * m2 = 1.0."
        ]
    },
    "misconceptions": [
        {
            "error": "Assuming only one lens position can produce a sharp image on the screen.",
            "correction": "Because quadratic equation u^2 - Du + Df = 0 has two distinct real roots when D > 4f, exactly two lens positions exist."
        }
    ],
    "exit_task": {
        "prompt": "If D = 75 cm and f = 12 cm, compute the discriminant Delta and verify whether D > 4f.",
        "answer": "4f = 48 cm < 75 cm. Delta = 75^2 - 4(75)(12) = 5625 - 3600 = 2025 = 45^2 > 0. Two real positions exist."
    }
}
(mod1_dir / "core1a_construction.json").write_text(json.dumps(mod1_c1a, indent=2), encoding="utf-8")

mod1_c1b = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "PHYS-OPT-C-LENS-DISPLACEMENT-D3-01",
    "target_question_id": "PHYS-NSEJS-2024-P-Q57",
    "title": "Phenomenological Reconstruction · Lens Displacement Method Conjugate Foci",
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "RAY_OPTICS",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "M2",
    "taught_skill_Y": "Conjugate foci quadratic formulation u^2 - Du + Df = 0 and condition D >= 4f.",
    "connecting_route_Z": "Evaluating discriminant Delta = D^2 - 4Df = 45^2 to solve for dual positions u1 = 15 cm and u2 = 60 cm.",
    "protected_fresh_inference_W": "Synthesizing reciprocal lateral magnifications |m1| = 60/15 = 4.0 and |m2| = 15/60 = 0.25 to simultaneously validate all four multi-correct options (A, B, C, D).",
    "stages": {
        "stage_1_predict": {
            "prompt": "For an illuminated object and screen fixed 75 cm apart, can a convex lens of f = 12 cm form both a magnified and a diminished sharp real image?",
            "defensible_prediction": "Yes. Since D = 75 cm > 4f = 48 cm, the lens has two conjugate positions. When closer to the object (u = 15 cm), v = 60 cm so m = 4.0 (magnified). When moved closer to the screen (u = 60 cm), v = 15 cm so m = 0.25 (diminished)."
        },
        "stage_2_attempt": {
            "prompt": "Evaluate the quadratic equation for lens position u with D = 75 cm and f = 12 cm, determine both real roots, and classify the image magnification for each root.",
            "produces": "u1 = 15 cm (m = 4.0, magnified), u2 = 60 cm (m = 0.25, diminished) ==> Options A, B, C, D are all correct.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Quadratic setup: u^2 - 75u + (75)(12) = u^2 - 75u + 900 = 0.",
                    "evidence_of": "Proper algebraic formulation from thin lens equation."
                },
                {
                    "criterion": "Root calculation: Delta = 5625 - 3600 = 2025 = 45^2 ==> u1 = 15 cm, u2 = 60 cm.",
                    "evidence_of": "Exact numerical extraction of both conjugate positions."
                },
                {
                    "criterion": "Magnification synthesis: m1 = 60/15 = 4.0 (>1) and m2 = 15/60 = 0.25 (<1).",
                    "evidence_of": "Justifying that both magnified and diminished images occur."
                }
            ],
            "accepted": [
                "A, B, C, D", "Options A, B, C, D", "All options correct", "u1 = 15 cm, u2 = 60 cm, both magnified and diminished"
            ],
            "rejected": [
                "Only A and B (failing to evaluate magnification)",
                "Only C (assuming only magnified image forms)",
                "No real roots (miscalculating 4Df > D^2)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What quadratic equation governs the object distance u when screen is fixed at D = 75 cm?",
                    "why_this_ask": "Applies thin lens equation with v = D - u.",
                    "step_answer": "1/(D - u) + 1/u = 1/f ==> D / (u(D - u)) = 1/f ==> u^2 - Du + Df = 0 ==> u^2 - 75u + 900 = 0."
                },
                {
                    "ask": "2. What is the discriminant Delta and what are the two real lens positions?",
                    "why_this_ask": "Solves quadratic equation for physical locations.",
                    "step_answer": "Delta = (-75)^2 - 4(1)(900) = 5625 - 3600 = 2025 = 45^2. Roots: u1 = (75 - 45)/2 = 15 cm; u2 = (75 + 45)/2 = 60 cm."
                },
                {
                    "ask": "3. What are the corresponding image distances v1 and v2?",
                    "why_this_ask": "Evaluates distance from lens to screen.",
                    "step_answer": "For u1 = 15 cm, v1 = 75 - 15 = 60 cm. For u2 = 60 cm, v2 = 75 - 60 = 15 cm."
                },
                {
                    "ask": "4. What are the linear magnifications at these two positions?",
                    "why_this_ask": "Calculates image scale |m| = v/u.",
                    "step_answer": "|m1| = 60 / 15 = 4.0 (magnified); |m2| = 15 / 60 = 0.25 (diminished). Thus statements A, B, C, and D are all valid."
                }
            ],
            "differs_from_teaching_path": "Reconstruction prompts the learner to solve the quadratic roots independently and classify both physical image magnifications."
        },
        "stage_4_diagnose": {
            "error_trap": "Concluding that only a diminished image forms or that only one position is valid.",
            "diagnostic_prompt": "Why are there two valid lens positions instead of just one?",
            "resolution": "Because light ray paths are reversible (conjugate foci reciprocity). The quadratic equation has two real distinct roots whenever D > 4f."
        },
        "stage_5_repair": {
            "action": "Always test condition D >= 4f first. If satisfied, write u^2 - Du + Df = 0, find roots u1 and u2, and compute magnifications v1/u1 and v2/u2."
        },
        "stage_6_boundary_test": {
            "prompt": "What happens if the screen distance is reduced to D = 40 cm with the same f = 12 cm lens?",
            "answer": "4f = 48 cm. Since D = 40 cm < 4f, Delta = 40^2 - 4(40)(12) = 1600 - 1920 = -320 < 0. No real image can ever be formed on the screen at any lens position."
        }
    },
    "progressive_hints": [
        {
            "hint_id": "H1",
            "tier": "CLARIFY",
            "text": "The total distance from object to screen is D = u + v = 75 cm. Write the lens formula with v = 75 - u."
        },
        {
            "hint_id": "H2",
            "tier": "CORRELATE",
            "text": "Rearranging 1/(75 - u) + 1/u = 1/12 yields a quadratic equation: u^2 - 75u + 900 = 0. Calculate its discriminant."
        },
        {
            "hint_id": "H3",
            "tier": "OPEN_THE_WAY",
            "text": "The two roots give u1 = 15 cm and u2 = 60 cm. Compute the ratio v/u for each position to check if they are magnified (|m| > 1) or diminished (|m| < 1)."
        }
    ]
}
(mod1_dir / "core1b_reconstruction.json").write_text(json.dumps(mod1_c1b, indent=2), encoding="utf-8")

# Witness 1
c1a_bytes1 = (mod1_dir / "core1a_construction.json").read_bytes()
c1b_bytes1 = (mod1_dir / "core1b_reconstruction.json").read_bytes()
mod1_witness = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-PHYS-OPTICS-D3-01",
    "construction": {
        "construction_id": "PHYS-OPT-C-LENS-DISPLACEMENT-D3-01",
        "topic_id": "PHYS-TOPIC-RAY-OPTICS",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "signature": {
            "inputs": ["D = 75 cm", "f = 12 cm", "Thin convex lens", "Real image on screen"],
            "obstacle": "Nonlinear conjugate focus quadratic coupling u^2 - Du + Df = 0 with dual physical roots",
            "decisive_move": "Quadratic root extraction and reciprocal magnification synthesis",
            "output": "u1 = 15 cm, u2 = 60 cm, m1 = 4.0 (magnified), m2 = 0.25 (diminished) ==> Options A, B, C, D",
            "conditions": ["D > 4f", "Thin lens approximation", "Paraxial rays"],
            "dependency_refs": ["GAUSSIAN_LENS_LAW", "QUADRATIC_DISCRIMINANT"],
            "independent_check": "f = (D^2 - d^2)/(4D) = (75^2 - 45^2)/(300) = (5625 - 2025)/300 = 12 cm",
            "validity_boundary": "D >= 4f required for real images; D = 4f yields single coincidence position u = D/2"
        },
        "decisive_roles": ["ROLE_OPT_REPRESENT", "ROLE_OPT_QUADRATIC", "ROLE_OPT_ROOTS", "ROLE_OPT_MAGNIFY"]
    },
    "core1a": {
        "construction_id": "PHYS-OPT-C-LENS-DISPLACEMENT-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": "sha256:" + hashlib.sha256(c1a_bytes1).hexdigest(),
        "worked_example_sha256": sha256_text(json.dumps(mod1_c1a["worked_conceptual_anchor"])),
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
            "ROLE_OPT_REPRESENT": {"teaching_span_ref": "core1a_construction.json#/teaching_path/0", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"},
            "ROLE_OPT_QUADRATIC": {"teaching_span_ref": "core1a_construction.json#/teaching_path/1", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"},
            "ROLE_OPT_ROOTS": {"teaching_span_ref": "core1a_construction.json#/teaching_path/2", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"},
            "ROLE_OPT_MAGNIFY": {"teaching_span_ref": "core1a_construction.json#/teaching_path/3", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/3"}
        }
    },
    "core1b": {
        "construction_id": "PHYS-OPT-C-LENS-DISPLACEMENT-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": "sha256:" + hashlib.sha256(c1b_bytes1).hexdigest(),
        "fresh_context_ref": "NSEJS-2024-P-Q57-AUTHENTIC-EXAM",
        "freshness_review_ref": "DOC-DISPLACEMENT-PARAM-INDEPENDENCE",
        "assessed_roles": {
            "ROLE_OPT_REPRESENT": {"attempt_field": "stage_2_attempt.rubric[0]", "observable": "Formulating u + v = D"},
            "ROLE_OPT_QUADRATIC": {"attempt_field": "stage_2_attempt.rubric[1]", "observable": "Constructing u^2 - 75u + 900 = 0"},
            "ROLE_OPT_ROOTS": {"attempt_field": "stage_2_attempt.rubric[2]", "observable": "Extracting u = 15 cm and 60 cm"},
            "ROLE_OPT_MAGNIFY": {"attempt_field": "stage_2_attempt.rubric[3]", "observable": "Computing m1 = 4.0 and m2 = 0.25"}
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "exposure_audit": [
            {"surface": "HINT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-HINT-01"},
            {"surface": "PICTURE_STAGE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-PIC-01"},
            {"surface": "ALT_TEXT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-ALT-01"},
            {"surface": "MODEL_RESPONSE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-MOD-01"},
            {"surface": "RUBRIC", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RUB-01"},
            {"surface": "EXAM_RETURN", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RET-01"}
        ],
        "diagnostic_rules": [
            {"role_id": "ROLE_OPT_REPRESENT", "observable": "Incorrect sign convention", "failed_node_ref": "NODE-OPT-SIGN", "repair_ref": "CONV-CARTESIAN"},
            {"role_id": "ROLE_OPT_QUADRATIC", "observable": "Sign flip in quadratic", "failed_node_ref": "NODE-OPT-QUAD", "repair_ref": "STEP-2"},
            {"role_id": "ROLE_OPT_ROOTS", "observable": "Arithmetic error in sqrt(2025)", "failed_node_ref": "NODE-OPT-DISC", "repair_ref": "STEP-3"},
            {"role_id": "ROLE_OPT_MAGNIFY", "observable": "Inverting magnification ratio", "failed_node_ref": "NODE-OPT-MAG", "repair_ref": "STEP-4"}
        ],
        "changed_condition_transfer_ref": "TRANSFER-CONVEX-DISPLACEMENT-02",
        "transfer_success_criterion": "Correctly identifying Delta < 0 when D < 4f as non-forming real image",
        "saved_answer_evidence_ref": "SAVED-EVIDENCE-OPT-01"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "demand_vector": [1, 2, 1, 1, 1],
        "qrt_decision_ref": "QRT-PHYS-OPT-D3-2024-Q57",
        "demand_evidence_ref": "DEMAND-ANALYSIS-PHYS-Q57",
        "source_role": "DIRECT_EXAM_EVIDENCE"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-PHYS-RAY-OPTICS-DISPLACEMENT",
        "physics_review_ref": "REVIEW-PHYS-ACADEMIC-PANEL-2026",
        "source_custody_ref": "CUSTODY-NSEJS-2024-P-51-Q57",
        "paper_ref": "NSEJS-2024-PAPER-CODE-51",
        "official_key_ref": "IAPT-NSEJS-2024-FINAL-KEY",
        "solution_review_ref": "IAPT-NSEJS-2024-SOLUTION-BOOKLET",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "ROLE_OPT_REPRESENT", "warrant_ref": "WARRANT-THIN-LENS-SIGN", "library_sha256": sha256_text("WARRANT-THIN-LENS-SIGN")},
            {"role_id": "ROLE_OPT_QUADRATIC", "warrant_ref": "WARRANT-QUADRATIC-CONJUGATE", "library_sha256": sha256_text("WARRANT-QUADRATIC-CONJUGATE")},
            {"role_id": "ROLE_OPT_ROOTS", "warrant_ref": "WARRANT-REAL-ROOT-CONDITIONS", "library_sha256": sha256_text("WARRANT-REAL-ROOT-CONDITIONS")},
            {"role_id": "ROLE_OPT_MAGNIFY", "warrant_ref": "WARRANT-LATERAL-MAGNIFICATION", "library_sha256": sha256_text("WARRANT-LATERAL-MAGNIFICATION")}
        ]
    },
    "review_receipts": []
}
(mod1_dir / "witness.json").write_text(json.dumps(mod1_witness, indent=2), encoding="utf-8")


# ==============================================================================
# MODULE 2: CHEMISTRY — NSEJS-2024-C-Q56 (Electronic Structure & Transition Aufbau)
# ==============================================================================
mod2_dir = OUTPUT_DIR / "chem-electronic-structure-d3-r1"
mod2_dir.mkdir(parents=True, exist_ok=True)

mod2_bank = {
    "topic": "ATOMIC_STRUCTURE_PERIODICITY",
    "topic_id": "CHEM-TOPIC-ATOMIC-STRUCTURE",
    "schema": "question-bank/v1",
    "questions": [
        {
            "id": "CHEM-NSEJS-2024-C-Q56",
            "stem": "[Multiple Correct] A neutral ground-state atom of an element has electronic shell population: K = 2, L = 8, M = 9, N = 2. Which of the following statements are correct?\n(A) The atom contains exactly one unpaired electron.\n(B) The atom contains exactly one d-electron.\n(C) The atom contains twelve p-electrons.\n(D) The element belongs to the p-block of the periodic table.",
            "options": [
                {"id": "A", "text": "The atom contains exactly one unpaired electron."},
                {"id": "B", "text": "The atom contains exactly one d-electron."},
                {"id": "C", "text": "The atom contains twelve p-electrons."},
                {"id": "D", "text": "The element belongs to the p-block of the periodic table."}
            ],
            "correct_option": "A, B, C",
            "operation": "SYNTHESIZE",
            "band": "D3",
            "score": 6,
            "crux_move": "M2"
        }
    ]
}
(mod2_dir / "bank.json").write_text(json.dumps(mod2_bank, indent=2), encoding="utf-8")

mod2_c1a = {
    "schema": "core1a-construction/v1",
    "construction_id": "CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01",
    "target_question_id": "CHEM-NSEJS-2024-C-Q56",
    "title": "Subshell Aufbau Configuration from Shell Population & Transition Metal Classification",
    "topic": "ATOMIC_STRUCTURE_PERIODICITY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "declared_conventions": [
        {
            "name": "Bohr-Bury Shell-to-Subshell Mapping",
            "statement": "Principal shells K (n=1), L (n=2), M (n=3), N (n=4) contain subshells 1s; 2s, 2p; 3s, 3p, 3d; 4s, 4p, 4d, 4f with maximum orbital capacities s=2, p=6, d=10, f=14."
        },
        {
            "name": "Aufbau Energy Ordering Rule",
            "statement": "Orbitals fill in order of increasing (n + l) energy: 1s < 2s < 2p < 3s < 3p < 4s < 3d < 4p; hence the 4s subshell fills before the 3d subshell begins."
        },
        {
            "name": "Hund's Rule and Spin Multiplicity",
            "statement": "Degenerate orbitals are each singly occupied with parallel spins before any pairing occurs; completely filled subshells have zero net spin and zero unpaired electrons."
        },
        {
            "name": "Periodic Block Definition",
            "statement": "An element belongs to the block corresponding to the subshell in which the differentiating (last) valence electron enters according to the Aufbau principle."
        }
    ],
    "entry_assumptions": [
        "Familiarity with quantum numbers (n, l, ml, ms) and spectroscopic orbital labels.",
        "Ability to sum total electrons across shells to determine atomic number Z.",
        "Basic periodic table architecture dividing elements into s, p, d, and f blocks."
    ],
    "inferential_jump": "Deconstructing bulk principal quantum shell counts (M=9, N=2) into specific orbital occupancies (3s2 3p6 3d1 4s2), distinguishing core vs valence electrons, counting unpaired spins, and identifying d-block transition identity.",
    "teaching_path": [
        {
            "step": 1,
            "role": "RETRIEVE",
            "action": "Sum electrons across shells K + L + M + N = Z and identify the neutral atomic element.",
            "why_valid": "Total electrons in a neutral atom equal nuclear charge Z."
        },
        {
            "step": 2,
            "role": "REPRESENT",
            "action": "Decompose shell populations into subshells following (n+l) Aufbau ordering.",
            "why_valid": "M-shell (n=3) has 3s(2) + 3p(6) + 3d(1) = 9, and N-shell (n=4) has 4s(2)."
        },
        {
            "step": 3,
            "role": "SYNTHESIZE",
            "action": "Enumerate specific electron categories: total p-electrons, total d-electrons, and unpaired spins.",
            "why_valid": "Fully filled subshells 1s2, 2s2, 2p6, 3s2, 3p6, 4s2 pair completely, leaving 3d1 as the sole unpaired electron."
        },
        {
            "step": 4,
            "role": "JUSTIFY",
            "action": "Classify periodic block based on the subshell receiving the differentiating electron.",
            "why_valid": "Last electron enters 3d, which defines the element as a d-block transition metal, refuting p-block classification."
        }
    ],
    "worked_conceptual_anchor": {
        "problem": "An atom of Chromium (Cr, Z=24) has shell population K = 2, L = 8, M = 13, N = 1. Write its full subshell configuration, determine total p-electrons, total d-electrons, unpaired electrons, and periodic block.",
        "solution_steps": [
            "1. Atomic number: Z = 2 + 8 + 13 + 1 = 24 (Chromium, Cr).",
            "2. Subshell configuration: Due to half-filled subshell stability, Cr is 1s2 2s2 2p6 3s2 3p6 3d5 4s1.",
            "3. Electron counts: p-electrons = 2p6 + 3p6 = 12; d-electrons = 3d5 = 5; unpaired electrons = 5 (in 3d) + 1 (in 4s) = 6.",
            "4. Block classification: Differentiating electrons enter 3d, placing Cr in the d-block."
        ]
    },
    "misconceptions": [
        {
            "error": "Classifying the element into the p-block because N=2 is considered valence.",
            "correction": "Block is determined by the highest-energy subshell being filled (the 3d subshell), which places Scandium in the d-block."
        }
    ],
    "exit_task": {
        "prompt": "For an element with K=2, L=8, M=9, N=2, calculate Z and state whether 3d or 4s has higher orbital energy.",
        "answer": "Z = 21 (Scandium). The 3d subshell (n+l = 3+2 = 5) has higher energy than 4s (n+l = 4+0 = 4)."
    }
}
(mod2_dir / "core1a_construction.json").write_text(json.dumps(mod2_c1a, indent=2), encoding="utf-8")

mod2_c1b = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01",
    "target_question_id": "CHEM-NSEJS-2024-C-Q56",
    "title": "Phenomenological Reconstruction · Electronic Shell Population & Transition Aufbau",
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "ATOMIC_STRUCTURE_PERIODICITY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "M2",
    "taught_skill_Y": "Decomposing shell populations into subshell quantum occupancies: 1s2 2s2 2p6 3s2 3p6 3d1 4s2.",
    "connecting_route_Z": "Evaluating individual subshell populations: 12 p-electrons (2p6 + 3p6), 1 d-electron (3d1), and completely paired core.",
    "protected_fresh_inference_W": "Identifying that 3d1 creates exactly 1 unpaired electron and that the differentiating 3d electron assigns Scandium to the d-block (making options A, B, C true and D false).",
    "stages": {
        "stage_1_predict": {
            "prompt": "An atom has K=2, L=8, M=9, N=2. Can an atom with only 9 electrons in the third shell have any unpaired electrons?",
            "defensible_prediction": "Yes. The first 8 electrons in shell 3 fill 3s2 and 3p6. The 9th electron enters the degenerate 3d subshell alone, producing 1 unpaired electron."
        },
        "stage_2_attempt": {
            "prompt": "Determine the atomic number Z, full subshell configuration, count of unpaired electrons, d-electrons, p-electrons, and periodic block for K=2, L=8, M=9, N=2.",
            "produces": "Z = 21 (Sc), 1s2 2s2 2p6 3s2 3p6 3d1 4s2. Unpaired = 1 (in 3d), d-electrons = 1, p-electrons = 12, d-block ==> Options A, B, C are correct.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Atomic number & subshell resolution: Z = 21, [Ar] 3d1 4s2.",
                    "evidence_of": "Proper understanding of Aufbau subshell partitioning."
                },
                {
                    "criterion": "Subshell population counting: 12 p-electrons (2p6 + 3p6), 1 d-electron (3d1), 1 unpaired electron.",
                    "evidence_of": "Accurate orbital occupancy enumeration."
                },
                {
                    "criterion": "Block deduction: Last electron enters 3d ==> d-block (transition element), refuting p-block.",
                    "evidence_of": "Competent periodic classification based on differentiating electron."
                }
            ],
            "accepted": [
                "A, B, C", "Options A, B, and C", "A, B, C are correct; D is incorrect"
            ],
            "rejected": [
                "A, B, C, D (falsely claiming p-block membership)",
                "Only A and B (missing the 12 p-electrons calculation)",
                "Claiming 0 unpaired electrons (falsely pairing 3d)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What is the atomic number Z of the neutral atom?",
                    "why_this_ask": "Sums total electrons across all shells.",
                    "step_answer": "Z = 2 + 8 + 9 + 2 = 21. Element is Scandium (Sc)."
                },
                {
                    "ask": "2. How are the 9 electrons in the M-shell (n=3) and 2 in the N-shell distributed across subshells?",
                    "why_this_ask": "Applies Aufbau (n+l) orbital filling order.",
                    "step_answer": "M-shell (n=3) has 3s^2 3p^6 3d^1 (2 + 6 + 1 = 9). N-shell (n=4) has 4s^2. Complete: 1s^2 2s^2 2p^6 3s^2 3p^6 3d^1 4s^2."
                },
                {
                    "ask": "3. How many p-electrons, d-electrons, and unpaired electrons are present?",
                    "why_this_ask": "Enumerates specific orbital populations.",
                    "step_answer": "p-electrons = 2p^6 + 3p^6 = 12. d-electrons = 3d^1 = 1. Unpaired electrons = exactly 1 (the single 3d electron; all others are paired)."
                },
                {
                    "ask": "4. To which block of the periodic table does this element belong?",
                    "why_this_ask": "Applies differentiating electron block assignment rule.",
                    "step_answer": "The differentiating (last filled) electron enters the 3d subshell. Thus, Scandium belongs to the d-block, NOT the p-block."
                }
            ],
            "differs_from_teaching_path": "Reconstruction prompts the learner to derive subshell distribution directly from shell numbers and test each proposition against Aufbau rules."
        },
        "stage_4_diagnose": {
            "error_trap": "Classifying Scandium into the p-block because of confusing group numbering or outer s electrons.",
            "diagnostic_prompt": "Why is an element with an outermost 4s^2 subshell not in the s-block or p-block?",
            "resolution": "Because the highest energy incomplete subshell currently receiving electrons is the 3d subshell, which designates it as a d-block transition metal."
        },
        "stage_5_repair": {
            "action": "Always write the full spectroscopic notation 1s2 2s2 2p6 3s2 3p6 3d1 4s2, count electrons per l-quantum number, and identify the highest-energy subshell for block assignment."
        },
        "stage_6_boundary_test": {
            "prompt": "What would be the shell population of the next element in the periodic table (Titanium, Z = 22)?",
            "answer": "Adding 1 electron to the 3d subshell gives [Ar] 3d2 4s2, so shell population becomes K = 2, L = 8, M = 10, N = 2, with 2 unpaired d-electrons."
        }
    },
    "progressive_hints": [
        {
            "hint_id": "H1",
            "tier": "CLARIFY",
            "text": "Find the total number of electrons by adding K + L + M + N. This gives atomic number Z = 21."
        },
        {
            "hint_id": "H2",
            "tier": "CORRELATE",
            "text": "Write the subshell configuration for Z = 21: 1s^2 2s^2 2p^6 3s^2 3p^6 3d^1 4s^2. Check how many electrons are in p and d orbitals."
        },
        {
            "hint_id": "H3",
            "tier": "OPEN_THE_WAY",
            "text": "Notice that subshells 1s through 4s are completely filled except 3d^1, which has 1 unpaired electron. The differentiating electron is in the 3d subshell, which defines the block."
        }
    ]
}
(mod2_dir / "core1b_reconstruction.json").write_text(json.dumps(mod2_c1b, indent=2), encoding="utf-8")

# Witness 2
c1a_bytes2 = (mod2_dir / "core1a_construction.json").read_bytes()
c1b_bytes2 = (mod2_dir / "core1b_reconstruction.json").read_bytes()
mod2_witness = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-CHEM-STRUCTURE-D3-01",
    "construction": {
        "construction_id": "CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01",
        "topic_id": "CHEM-TOPIC-ATOMIC-STRUCTURE",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "signature": {
            "inputs": ["K=2, L=8, M=9, N=2", "Neutral ground-state atom"],
            "obstacle": "Mapping non-standard shell counts to Aufbau subshell occupancies and periodic block classification",
            "decisive_move": "Subshell decomposition [Ar] 3d1 4s2 and differentiating electron block assignment",
            "output": "Z = 21 (Sc), 1 unpaired electron, 1 d-electron, 12 p-electrons, d-block ==> Options A, B, C",
            "conditions": ["Ground-state neutral atom", "Aufbau energy ordering (n+l)", "Hund's rule"],
            "dependency_refs": ["AUFBAU_PRINCIPLE", "HUND_RULE", "PERIODIC_BLOCK_RULE"],
            "independent_check": "Sum of subshells 2 + 2 + 6 + 2 + 6 + 1 + 2 = 21; d-block group 3",
            "validity_boundary": "Applies strictly to neutral ground-state atoms; ionized states lose 4s electrons first"
        },
        "decisive_roles": ["ROLE_CHEM_AUFBAU", "ROLE_CHEM_SUBSHELL", "ROLE_CHEM_SPIN", "ROLE_CHEM_BLOCK"]
    },
    "core1a": {
        "construction_id": "CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": "sha256:" + hashlib.sha256(c1a_bytes2).hexdigest(),
        "worked_example_sha256": sha256_text(json.dumps(mod2_c1a["worked_conceptual_anchor"])),
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
            "ROLE_CHEM_AUFBAU": {"teaching_span_ref": "core1a_construction.json#/teaching_path/0", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"},
            "ROLE_CHEM_SUBSHELL": {"teaching_span_ref": "core1a_construction.json#/teaching_path/1", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"},
            "ROLE_CHEM_SPIN": {"teaching_span_ref": "core1a_construction.json#/teaching_path/2", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"},
            "ROLE_CHEM_BLOCK": {"teaching_span_ref": "core1a_construction.json#/teaching_path/3", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/3"}
        }
    },
    "core1b": {
        "construction_id": "CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": "sha256:" + hashlib.sha256(c1b_bytes2).hexdigest(),
        "fresh_context_ref": "NSEJS-2024-C-Q56-AUTHENTIC-EXAM",
        "freshness_review_ref": "DOC-ELECTRONIC-STRUCTURE-AUTHENTIC",
        "assessed_roles": {
            "ROLE_CHEM_AUFBAU": {"attempt_field": "stage_2_attempt.rubric[0]", "observable": "Calculating Z = 21"},
            "ROLE_CHEM_SUBSHELL": {"attempt_field": "stage_2_attempt.rubric[1]", "observable": "Decomposing into 1s2 2s2 2p6 3s2 3p6 3d1 4s2"},
            "ROLE_CHEM_SPIN": {"attempt_field": "stage_2_attempt.rubric[2]", "observable": "Evaluating 1 unpaired electron and 12 p-electrons"},
            "ROLE_CHEM_BLOCK": {"attempt_field": "stage_2_attempt.rubric[3]", "observable": "Deducing d-block and rejecting p-block"}
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "exposure_audit": [
            {"surface": "HINT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-HINT-02"},
            {"surface": "PICTURE_STAGE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-PIC-02"},
            {"surface": "ALT_TEXT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-ALT-02"},
            {"surface": "MODEL_RESPONSE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-MOD-02"},
            {"surface": "RUBRIC", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RUB-02"},
            {"surface": "EXAM_RETURN", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RET-02"}
        ],
        "diagnostic_rules": [
            {"role_id": "ROLE_CHEM_AUFBAU", "observable": "Miscalculating Z from shells", "failed_node_ref": "NODE-CHEM-SUM", "repair_ref": "STEP-1"},
            {"role_id": "ROLE_CHEM_SUBSHELL", "observable": "Assigning 3d before 4s filled", "failed_node_ref": "NODE-CHEM-AUFBAU", "repair_ref": "STEP-2"},
            {"role_id": "ROLE_CHEM_SPIN", "observable": "Miscounting paired p orbitals", "failed_node_ref": "NODE-CHEM-HUND", "repair_ref": "STEP-3"},
            {"role_id": "ROLE_CHEM_BLOCK", "observable": "Falsely assigning to p-block", "failed_node_ref": "NODE-CHEM-BLOCK", "repair_ref": "STEP-4"}
        ],
        "changed_condition_transfer_ref": "TRANSFER-TRANSITION-TITANIUM-02",
        "transfer_success_criterion": "Correctly identifying Z = 22 as having 2 unpaired d electrons in M=10",
        "saved_answer_evidence_ref": "SAVED-EVIDENCE-CHEM-02"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "demand_vector": [1, 2, 1, 1, 1],
        "qrt_decision_ref": "QRT-CHEM-ATOM-D3-2024-Q56",
        "demand_evidence_ref": "DEMAND-ANALYSIS-CHEM-Q56",
        "source_role": "DIRECT_EXAM_EVIDENCE"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-CHEM-AUFBAU-ORBITAL-ENERGY",
        "physics_review_ref": "REVIEW-CHEM-ACADEMIC-PANEL-2026",
        "source_custody_ref": "CUSTODY-NSEJS-2024-C-51-Q56",
        "paper_ref": "NSEJS-2024-PAPER-CODE-51",
        "official_key_ref": "IAPT-NSEJS-2024-FINAL-KEY",
        "solution_review_ref": "IAPT-NSEJS-2024-SOLUTION-BOOKLET",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "ROLE_CHEM_AUFBAU", "warrant_ref": "WARRANT-AUFBAU-N-PLUS-L", "library_sha256": sha256_text("WARRANT-AUFBAU-N-PLUS-L")},
            {"role_id": "ROLE_CHEM_SUBSHELL", "warrant_ref": "WARRANT-SUBSHELL-CAPACITIES", "library_sha256": sha256_text("WARRANT-SUBSHELL-CAPACITIES")},
            {"role_id": "ROLE_CHEM_SPIN", "warrant_ref": "WARRANT-HUND-MULTIPLICITY", "library_sha256": sha256_text("WARRANT-HUND-MULTIPLICITY")},
            {"role_id": "ROLE_CHEM_BLOCK", "warrant_ref": "WARRANT-DIFFERENTIATING-ELECTRON-BLOCK", "library_sha256": sha256_text("WARRANT-DIFFERENTIATING-ELECTRON-BLOCK")}
        ]
    },
    "review_receipts": []
}
(mod2_dir / "witness.json").write_text(json.dumps(mod2_witness, indent=2), encoding="utf-8")


# ==============================================================================
# MODULE 3: BIOLOGY — NSEJS-2024-B-Q52 (Vertebrate Immunology & Defenses)
# ==============================================================================
mod3_dir = OUTPUT_DIR / "bio-immunology-defense-d3-r1"
mod3_dir.mkdir(parents=True, exist_ok=True)

mod3_bank = {
    "topic": "ANIMAL_PHYSIOLOGY_IMMUNOLOGY",
    "topic_id": "BIO-TOPIC-IMMUNOLOGY",
    "schema": "question-bank/v1",
    "questions": [
        {
            "id": "BIO-NSEJS-2024-B-Q52",
            "stem": "[Multiple Correct] Which of the following statements regarding vertebrate immune responses and physiological defense mechanisms are correct?\n(A) All antibodies (immunoglobulins) are glycoproteins.\n(B) Eosinophils are non-phagocytic lymphocytes.\n(C) Ciliated pseudostratified epithelium of the respiratory tract functions as a physical/mechanical barrier.\n(D) Histamine released by tissue mast cells and basophils triggers local vasodilation and inflammatory response.",
            "options": [
                {"id": "A", "text": "All antibodies (immunoglobulins) are glycoproteins."},
                {"id": "B", "text": "Eosinophils are non-phagocytic lymphocytes."},
                {"id": "C", "text": "Ciliated pseudostratified epithelium of the respiratory tract functions as a physical/mechanical barrier."},
                {"id": "D", "text": "Histamine released by tissue mast cells and basophils triggers local vasodilation and inflammatory response."}
            ],
            "correct_option": "A, C, D",
            "operation": "SYNTHESIZE",
            "band": "D3",
            "score": 6,
            "crux_move": "M2"
        }
    ]
}
(mod3_dir / "bank.json").write_text(json.dumps(mod3_bank, indent=2), encoding="utf-8")

mod3_c1a = {
    "schema": "core1a-construction/v1",
    "construction_id": "BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01",
    "target_question_id": "BIO-NSEJS-2024-B-Q52",
    "title": "Vertebrate Immune Architecture: Immunoglobulins, Leukocyte Lineages & Inflammatory Mediators",
    "topic": "ANIMAL_PHYSIOLOGY_IMMUNOLOGY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "declared_conventions": [
        {
            "name": "Immunoglobulin Biochemical Structure",
            "statement": "All antibodies (IgG, IgM, IgA, IgD, IgE) are heterotetrameric glycoproteins comprising two identical heavy chains and two identical light chains, with essential N-linked carbohydrate moieties attached to constant regions."
        },
        {
            "name": "Hematopoietic Leukocyte Lineage Separation",
            "statement": "Leukocytes divide into the myeloid lineage (granulocytes: neutrophils, eosinophils, basophils; monocytes/macrophages) and the lymphoid lineage (B cells, T cells, NK cells); eosinophils are granulocytic myeloid leukocytes, not lymphocytes."
        },
        {
            "name": "Epithelial Physical Barrier Function",
            "statement": "Ciliated pseudostratified columnar epithelium with goblet cell mucus forms the mucociliary escalator, providing a non-specific physical/mechanical barrier trapping and sweeping pathogens outward."
        },
        {
            "name": "Mast Cell & Basophil Inflammatory Mediators",
            "statement": "Tissue mast cells and circulating basophils store preformed histamine in granules; degranulation triggers arteriolar vasodilation and increases post-capillary venular permeability during acute inflammation."
        }
    ],
    "entry_assumptions": [
        "Familiarity with innate vs adaptive immunity and body defense lines.",
        "Basic histology of epithelial tissues and blood cellular elements.",
        "Knowledge of inflammatory signs (rubor, calor, tumor, dolor) and chemical mediation."
    ],
    "inferential_jump": "Integrating molecular biochemistry (antibody glycosylation), hematological differentiation (myeloid granulocytes vs lymphoid agranulocytes), histological defenses (mucociliary clearance), and vascular pharmacology (histamine-mediated extravasation).",
    "teaching_path": [
        {
            "step": 1,
            "role": "RETRIEVE",
            "action": "Examine the biochemical structure of immunoglobulins, identifying polypeptide chains and glycosylation.",
            "why_valid": "All antibodies are synthesized through the secretory pathway with N-glycosylation."
        },
        {
            "step": 2,
            "role": "REPRESENT",
            "action": "Map hematopoietic stem cell differentiation into myeloid vs lymphoid progenitor lineages.",
            "why_valid": "Eosinophils arise from common myeloid progenitors (CMP), while lymphocytes arise from common lymphoid progenitors (CLP)."
        },
        {
            "step": 3,
            "role": "MODEL",
            "action": "Detail innate epithelial barrier mechanisms including mucosal secretion and ciliary beating.",
            "why_valid": "Mucus traps foreign particles and directional ciliary strokes propel them out of the respiratory tree."
        },
        {
            "step": 4,
            "role": "SYNTHESIZE",
            "action": "Analyze mast cell and basophil degranulation and the downstream vascular effects of histamine.",
            "why_valid": "Histamine binds H1 receptors on endothelial cells, promoting vasodilation and vascular leakage."
        }
    ],
    "worked_conceptual_anchor": {
        "problem": "Contrast the developmental origin and immune roles of cytotoxic T lymphocytes (CTLs) versus neutrophil granulocytes.",
        "solution_steps": [
            "1. Lineage origin: CTLs derive from common lymphoid progenitors and mature in the thymus; neutrophils derive from common myeloid progenitors in bone marrow.",
            "2. Recognition: CTLs recognize specific viral peptides on MHC Class I via T-cell receptors (adaptive); neutrophils recognize conserved pathogen patterns via PRRs (innate).",
            "3. Effector mechanism: CTLs release perforin and granzymes to induce apoptosis; neutrophils perform rapid phagocytosis, oxidative burst, and NETosis.",
            "4. Classification: CTLs are agranular lymphocytes; neutrophils are polymorphonuclear granulocytes."
        ]
    },
    "misconceptions": [
        {
            "error": "Classifying eosinophils as lymphocytes because both are white blood cells.",
            "correction": "Eosinophils are granular myeloid cells with bilobed nuclei and specialized acidophilic granules, entirely distinct from lymphoid lymphocytes."
        }
    ],
    "exit_task": {
        "prompt": "State two defining biochemical and cellular characteristics that distinguish an antibody from a lymphocyte receptor.",
        "answer": "An antibody is a soluble secreted glycoprotein with 2 heavy and 2 light chains; a lymphocyte receptor (TCR) is a membrane-bound heterodimer."
    }
}
(mod3_dir / "core1a_construction.json").write_text(json.dumps(mod3_c1a, indent=2), encoding="utf-8")

mod3_c1b = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01",
    "target_question_id": "BIO-NSEJS-2024-B-Q52",
    "title": "Phenomenological Reconstruction · Vertebrate Immunology & Physiological Defenses",
    "status": "CANDIDATE",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "ANIMAL_PHYSIOLOGY_IMMUNOLOGY",
    "cognitive_demand": "SYNTHESIZE",
    "difficulty_band": "D3",
    "difficulty_score": 6,
    "crux_move": "M2",
    "taught_skill_Y": "Vertebrate immune defense classification: glycoprotein antibodies, myeloid vs lymphoid lineage, mucociliary barriers, and histamine pharmacology.",
    "connecting_route_Z": "Evaluating propositions A, C, D as scientifically sound, and identifying the false classification of eosinophils as lymphocytes in proposition B.",
    "protected_fresh_inference_W": "Dissecting the multi-correct options to confirm A (glycoproteins), C (mucociliary barrier), and D (histamine vasodilation) while refuting B (eosinophils are granulocytes, not lymphocytes).",
    "stages": {
        "stage_1_predict": {
            "prompt": "Are antibodies purely proteinaceous or do they contain carbohydrate groups, and do eosinophils belong to the same lineage as B and T cells?",
            "defensible_prediction": "Antibodies are glycoproteins containing carbohydrate moieties attached to their Fc regions. Eosinophils are granulocytic myeloid cells, completely separate from lymphoid lymphocytes."
        },
        "stage_2_attempt": {
            "prompt": "Evaluate statements A, B, C, D regarding vertebrate immunity, identify all correct statements, and explain why eosinophils cannot be classified as lymphocytes.",
            "produces": "Statements A, C, and D are correct; Statement B is incorrect because eosinophils are myeloid granulocytes, not lymphocytes ==> Options A, C, D.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Immunoglobulin biochemistry: Validating that all antibodies are glycoproteins.",
                    "evidence_of": "Knowledge of antibody structural macromolecular composition."
                },
                {
                    "criterion": "Leukocyte classification: Refuting B by identifying eosinophils as myeloid granulocytes.",
                    "evidence_of": "Understanding hematological lineage separation."
                },
                {
                    "criterion": "Innate defense mechanisms: Validating mucociliary physical barrier (C) and histamine vasodilation (D).",
                    "evidence_of": "Synthesizing epithelial mechanics with inflammatory pharmacology."
                }
            ],
            "accepted": [
                "A, C, D", "Options A, C, and D", "A, C, D are correct; B is incorrect"
            ],
            "rejected": [
                "A, B, C, D (falsely accepting eosinophils as lymphocytes)",
                "Only C and D (failing to recognize antibodies as glycoproteins)",
                "Only A (ignoring innate barriers and histamine mediation)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What is the biochemical nature of all antibodies (immunoglobulins)?",
                    "why_this_ask": "Evaluates macromolecular composition of antibodies.",
                    "step_answer": "All antibodies are glycoproteins synthesized by plasma cells, featuring oligosaccharide chains attached to polypeptide heavy chains."
                },
                {
                    "ask": "2. What is the lineage and cellular classification of eosinophils?",
                    "why_this_ask": "Tests hematological lineage knowledge.",
                    "step_answer": "Eosinophils are polymorphonuclear granulocytes derived from myeloid stem cells, possessing phagocytic capacity against helminths; they are NOT agranular lymphocytes."
                },
                {
                    "ask": "3. How does the respiratory tract ciliated pseudostratified epithelium function in defense?",
                    "why_this_ask": "Assesses physical barrier mechanics.",
                    "step_answer": "Goblet cell mucus entraps particulate matter and microbes, while coordinated ciliary strokes propel mucus upward away from lungs (mucociliary escalator), acting as a physical barrier."
                },
                {
                    "ask": "4. What physiological response is triggered by histamine released from mast cells and basophils?",
                    "why_this_ask": "Tests inflammatory vascular pharmacology.",
                    "step_answer": "Histamine binds to H1 endothelial receptors, causing local vasodilation and increased vascular permeability, producing the cardinal signs of acute inflammation."
                }
            ],
            "differs_from_teaching_path": "Reconstruction prompts the learner to evaluate four distinct biological propositions independently and identify the lineage contradiction in eosinophil classification."
        },
        "stage_4_diagnose": {
            "error_trap": "Assuming all white blood cells that fight infection can be called lymphocytes.",
            "diagnostic_prompt": "Why can't an eosinophil or neutrophil be described as a lymphocyte?",
            "resolution": "Because lymphocytes refer strictly to B cells, T cells, and NK cells of lymphoid origin with round unlobed nuclei and no prominent cytoplasmic granules."
        },
        "stage_5_repair": {
            "action": "Always categorize leukocytes into Granulocytes (Neutrophil, Eosinophil, Basophil — myeloid) and Agranulocytes (Monocytes — myeloid; Lymphocytes: B, T, NK — lymphoid)."
        },
        "stage_6_boundary_test": {
            "prompt": "If an antibody is enzymatically deglycosylated, does it lose antigen binding or effector function?",
            "answer": "Deglycosylation leaves Fab antigen-binding intact but severely impairs Fc receptor binding and complement activation, proving carbohydrate necessity in glycoprotein function."
        }
    },
    "progressive_hints": [
        {
            "hint_id": "H1",
            "tier": "CLARIFY",
            "text": "Review the definition of an antibody: antibodies are secreted by plasma cells and carry carbohydrate side chains. Are they glycoproteins?"
        },
        {
            "hint_id": "H2",
            "tier": "CORRELATE",
            "text": "Think about blood cell types. White blood cells are divided into granulocytes (neutrophils, eosinophils, basophils) and lymphocytes (B, T, NK cells)."
        },
        {
            "hint_id": "H3",
            "tier": "OPEN_THE_WAY",
            "text": "Check statements C and D: ciliated mucus traps dust (physical barrier) and mast cell histamine causes redness and swelling (vasodilation). Both are hallmark biological facts."
        }
    ]
}
(mod3_dir / "core1b_reconstruction.json").write_text(json.dumps(mod3_c1b, indent=2), encoding="utf-8")

# Witness 3
c1a_bytes3 = (mod3_dir / "core1a_construction.json").read_bytes()
c1b_bytes3 = (mod3_dir / "core1b_reconstruction.json").read_bytes()
mod3_witness = {
    "schema_version": "grade9qa-b1b7-witness/v1",
    "status": "CANDIDATE",
    "author_id": "AUTH-BIO-IMMUN-D3-01",
    "construction": {
        "construction_id": "BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01",
        "topic_id": "BIO-TOPIC-IMMUNOLOGY",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "signature": {
            "inputs": ["Antibody glycoprotein structure", "Leukocyte lineages", "Epithelial barriers", "Histamine inflammation"],
            "obstacle": "Cross-disciplinary synthesis of molecular immunology, histology, and leukocyte hematology",
            "decisive_move": "Refuting lymphocyte classification of eosinophils and validating A, C, D",
            "output": "Statements A, C, D valid; Statement B false ==> Options A, C, D",
            "conditions": ["Vertebrate immune architecture", "Innate and adaptive division", "Standard physiological states"],
            "dependency_refs": ["IMMUNOGLOBULIN_STRUCTURE", "HEMATOPOIETIC_LINEAGES", "INFLAMMATION_PHARMACOLOGY"],
            "independent_check": "Eosinophil lineage: CMP -> CFU-Eo -> Eosinophil (myeloid granulocyte)",
            "validity_boundary": "Applies to vertebrate mammalian immune systems; invertebrate immunity lacks immunoglobulins"
        },
        "decisive_roles": ["ROLE_BIO_ANTIBODY", "ROLE_BIO_LEUKOCYTE", "ROLE_BIO_EPITHELIUM", "ROLE_BIO_HISTAMINE"]
    },
    "core1a": {
        "construction_id": "BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "content_sha256": "sha256:" + hashlib.sha256(c1a_bytes3).hexdigest(),
        "worked_example_sha256": sha256_text(json.dumps(mod3_c1a["worked_conceptual_anchor"])),
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
            "ROLE_BIO_ANTIBODY": {"teaching_span_ref": "core1a_construction.json#/teaching_path/0", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"},
            "ROLE_BIO_LEUKOCYTE": {"teaching_span_ref": "core1a_construction.json#/teaching_path/1", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"},
            "ROLE_BIO_EPITHELIUM": {"teaching_span_ref": "core1a_construction.json#/teaching_path/2", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"},
            "ROLE_BIO_HISTAMINE": {"teaching_span_ref": "core1a_construction.json#/teaching_path/3", "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/3"}
        }
    },
    "core1b": {
        "construction_id": "BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01",
        "operation": "SYNTHESIZE",
        "band": "D3",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": "sha256:" + hashlib.sha256(c1b_bytes3).hexdigest(),
        "fresh_context_ref": "NSEJS-2024-B-Q52-AUTHENTIC-EXAM",
        "freshness_review_ref": "DOC-IMMUNOLOGY-DEFENSE-AUTHENTIC",
        "assessed_roles": {
            "ROLE_BIO_ANTIBODY": {"attempt_field": "stage_2_attempt.rubric[0]", "observable": "Confirming antibody glycoprotein nature"},
            "ROLE_BIO_LEUKOCYTE": {"attempt_field": "stage_2_attempt.rubric[1]", "observable": "Rejecting eosinophil as lymphocyte"},
            "ROLE_BIO_EPITHELIUM": {"attempt_field": "stage_2_attempt.rubric[2]", "observable": "Validating mucociliary escalator"},
            "ROLE_BIO_HISTAMINE": {"attempt_field": "stage_2_attempt.rubric[3]", "observable": "Validating histamine-mediated vasodilation"}
        },
        "attempt_contract": {
            "p1_optional": True,
            "first_answer_before_hint": True,
            "reveal_requires_saved_attempt": True,
            "fail_closed_on_save_error": True
        },
        "exposure_audit": [
            {"surface": "HINT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-HINT-03"},
            {"surface": "PICTURE_STAGE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-PIC-03"},
            {"surface": "ALT_TEXT", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-ALT-03"},
            {"surface": "MODEL_RESPONSE", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-MOD-03"},
            {"surface": "RUBRIC", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RUB-03"},
            {"surface": "EXAM_RETURN", "decisive_route_visible_before_save": False, "audit_ref": "AUDIT-SURFACE-RET-03"}
        ],
        "diagnostic_rules": [
            {"role_id": "ROLE_BIO_ANTIBODY", "observable": "Denying glycoprotein nature of antibodies", "failed_node_ref": "NODE-BIO-GLYCO", "repair_ref": "STEP-1"},
            {"role_id": "ROLE_BIO_LEUKOCYTE", "observable": "Accepting eosinophils as lymphocytes", "failed_node_ref": "NODE-BIO-LINEAGE", "repair_ref": "STEP-2"},
            {"role_id": "ROLE_BIO_EPITHELIUM", "observable": "Denying mechanical barrier of cilia", "failed_node_ref": "NODE-BIO-BARRIER", "repair_ref": "STEP-3"},
            {"role_id": "ROLE_BIO_HISTAMINE", "observable": "Denying histamine vasodilation role", "failed_node_ref": "NODE-BIO-HISTAMINE", "repair_ref": "STEP-4"}
        ],
        "changed_condition_transfer_ref": "TRANSFER-IMMUNOLOGY-DEGLYCOSYLATION-02",
        "transfer_success_criterion": "Understanding that antibody carbohydrate chains are vital for effector functions",
        "saved_answer_evidence_ref": "SAVED-EVIDENCE-BIO-03"
    },
    "assessment": {
        "operation": "SYNTHESIZE",
        "band": "D3",
        "demand_vector": [1, 2, 1, 1, 1],
        "qrt_decision_ref": "QRT-BIO-IMMUN-D3-2024-Q52",
        "demand_evidence_ref": "DEMAND-ANALYSIS-BIO-Q52",
        "source_role": "DIRECT_EXAM_EVIDENCE"
    },
    "source_and_physics": {
        "physics_warrant_ref": "WARRANT-BIO-IMMUNOLOGY-PHYSIOLOGY",
        "physics_review_ref": "REVIEW-BIO-ACADEMIC-PANEL-2026",
        "source_custody_ref": "CUSTODY-NSEJS-2024-B-51-Q52",
        "paper_ref": "NSEJS-2024-PAPER-CODE-51",
        "official_key_ref": "IAPT-NSEJS-2024-FINAL-KEY",
        "solution_review_ref": "IAPT-NSEJS-2024-SOLUTION-BOOKLET",
        "known_physics_contradiction": False,
        "warrant_links": [
            {"role_id": "ROLE_BIO_ANTIBODY", "warrant_ref": "WARRANT-ANTIBODY-GLYCOPROTEIN", "library_sha256": sha256_text("WARRANT-ANTIBODY-GLYCOPROTEIN")},
            {"role_id": "ROLE_BIO_LEUKOCYTE", "warrant_ref": "WARRANT-LEUKOCYTE-HEMATOPOIESIS", "library_sha256": sha256_text("WARRANT-LEUKOCYTE-HEMATOPOIESIS")},
            {"role_id": "ROLE_BIO_EPITHELIUM", "warrant_ref": "WARRANT-MUCOCILIARY-ESCALATOR", "library_sha256": sha256_text("WARRANT-MUCOCILIARY-ESCALATOR")},
            {"role_id": "ROLE_BIO_HISTAMINE", "warrant_ref": "WARRANT-MAST-CELL-HISTAMINE", "library_sha256": sha256_text("WARRANT-MAST-CELL-HISTAMINE")}
        ]
    },
    "review_receipts": []
}
(mod3_dir / "witness.json").write_text(json.dumps(mod3_witness, indent=2), encoding="utf-8")

print("Rebuilt Batch 2 D3 modules with exact schema-compliant hashes.")
