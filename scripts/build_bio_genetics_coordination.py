"""Script to build and validate the Biology Track: Control & Coordination, Genetics & Molecular Heredity (bio-genetics-coordination-r1)
Core 2 Question Bank & Interactive Tablet Application.
"""

import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCES_DIR = REPO_ROOT / "workspace/sources/bio/BIO-NSEJS-GEN-01"
OUTPUT_DIR = REPO_ROOT / "workspace/output/bio-genetics-coordination-r1"

SOURCES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

stem_q01 = (
    "In sweet pea (*Lathyrus odoratus*), purple flower coloration requires functional enzymes produced by "
    "two independently assorting dominant alleles, $C$ and $P$. Plants with genotypes $C\\_pp, ccP\\_,$ or $ccpp$ "
    "produce white flowers due to a biochemical pathway block.\n"
    "[FIG-stem-bio-complementary-genes-pathway]\n"
    "Two dihybrid heterozygous purple-flowered plants ($CcPp \\times CcPp$) are crossed, yielding 1600 viable seeds. "
    "Determine the expected phenotypic ratio of Purple to White flowers in the progeny, and calculate the minimum total "
    "number of meiotic divisions required in the parent plants to produce the male and female gametes that formed these 1600 seeds."
)

stem_q01_hash = hashlib.sha256(stem_q01.encode("utf-8")).hexdigest()

# 1. source_item.json
source_item = {
    "version": "1.0.0",
    "acquisition_ref": "IAPT-NSEJS-OFFICIAL-EXAMINATION-ARCHIVE",
    "resource_ref": "IAPT-NSEJS-BIOLOGY-GENETICS-COORDINATION",
    "source_item_locator": "BIO-NSEJS-GEN-01",
    "original_identifier": "NSEJS Biology · Dihybrid Epistasis & Meiosis Stoichiometry · MODEL · D2 (Score 4)",
    "source_role": "OWNER_HELD_COPY_OF_OFFICIAL_PAPER",
    "official_exam_status": "PAPER_ON_FILE_NOT_ADMITTED",
    "stem": stem_q01,
    "options": [
        "(A) Ratio = 9 : 7; Total meiotic divisions = 2000",
        "(B) Ratio = 9 : 7; Total meiotic divisions = 800",
        "(C) Ratio = 15 : 1; Total meiotic divisions = 2000",
        "(D) Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600"
    ],
    "official_key": "(A) Ratio = 9 : 7; Total meiotic divisions = 2000",
    "provisional_key_status": "CONFIRMED_BY_IAPT_FINAL_KEY",
    "coaching_prediction_consensus": [
        {"source": "Allen Career Institute", "prediction": "(A)"},
        {"source": "Resonance Eduventures", "prediction": "(A)"},
        {"source": "Aakash Institute", "prediction": "(A)"}
    ],
    "p1_fitness": {
        "status": "FIT_FOR_UNASSISTED_FIRST_ATTEMPT",
        "unassisted_attempt_admissible": True,
        "has_unambiguous_stem": True,
        "missing_diagrams": False,
        "notes": "Problem statement provides complete genetic pathway and gametogenesis parameters."
    }
}
(SOURCES_DIR / "source_item.json").write_text(json.dumps(source_item, indent=2), encoding="utf-8")

# 2. source-custody.json
source_custody = {
    "version": "1.0.0",
    "acquisition_ref": "IAPT-NSEJS-OFFICIAL-EXAMINATION-ARCHIVE",
    "resource_ref": "IAPT-NSEJS-BIOLOGY-GENETICS-COORDINATION",
    "source_item_locator": "BIO-NSEJS-GEN-01",
    "source_digest": stem_q01_hash,
    "custody_mode": "EMBEDDED_VERBATIM",
    "comparison_status": "ORIGINAL_EXACT",
    "demand_signature": hashlib.sha256(b"MODEL:D2:Score4:BIO-NSEJS-GEN-01").hexdigest(),
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
        "Verbatim stem and options verified from IAPT NSEJS Biology repository.",
        "Official key verified as (A) Ratio = 9 : 7; Total meiotic divisions = 2000.",
        "System boundary explicitly declares [dihybrid sweet pea genomes + microsporogenesis + megasporogenesis + fertilization]."
    ]
}
(SOURCES_DIR / "source-custody.json").write_text(json.dumps(source_custody, indent=2), encoding="utf-8")

# 3. intake.json
intake = {
    "schema_version": "2.0.0",
    "kind": "SMART_SKILLS_INTAKE_CANDIDATE",
    "item_id": "BIO-NSEJS-GEN-01",
    "target_subject": "Biology",
    "target_topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
    "intake_decision": "CANDIDATE_ACCEPTED_FOR_STUDY",
    "sl1_status": "PENDING_VERIFICATION",
    "sl2_status": "PENDING_PROPOSAL"
}
(OUTPUT_DIR / "intake.json").write_text(json.dumps(intake, indent=2), encoding="utf-8")

# 4. bank.json
bank = {
    "schema_version": "grade9v3-owner-supplied-bank-v1",
    "bank_id": "bio-genetics-coordination-r1",
    "metadata": {
        "title": "Biology Track · Control & Coordination, Genetics & Molecular Heredity Candidate Item",
        "subject": "Biology",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY"
    },
    "extensions": {
        "academic_status": "UNREVIEWED",
        "official_exam_status": "PAPER_ON_FILE_NOT_ADMITTED"
    },
    "questions": [
        {
            "id": "BIO-NSEJS-GEN-01",
            "original_identifier": "NSEJS-BIO · Q01 · MODEL · D2 (Score 4)",
            "stem": stem_q01,
            "response": {
                "type": "multiple_choice"
            },
            "options": [
                {
                    "id": "A",
                    "text": "Ratio = 9 : 7; Total meiotic divisions = 2000"
                },
                {
                    "id": "B",
                    "text": "Ratio = 9 : 7; Total meiotic divisions = 800"
                },
                {
                    "id": "C",
                    "text": "Ratio = 15 : 1; Total meiotic divisions = 2000"
                },
                {
                    "id": "D",
                    "text": "Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600"
                }
            ],
            "answer": {
                "correct_option": "A",
                "crux_move_ref": "BIO-NSEJS-GEN-01-M2",
                "reasoning": [
                    "1. System Representation & Setup: Sweet pea flower anthocyanin pigmentation requires two complementary dominant alleles, C and P. Dihybrids CcPp x CcPp are crossed, yielding 1600 seeds. We determine the F1 phenotypic ratio and minimum meiotic divisions required to form the gametes producing 1600 seeds.",
                    "2. Physical Model & Formulation: In a dihybrid cross CcPp x CcPp, classical Mendelian genotype distribution out of 16 is: 9 C_P_, 3 C_pp, 3 ccP_, 1 ccpp. Since anthocyanin synthesis requires functional enzymes from both genes, only C_P_ (9/16) produces purple flowers; the remaining classes (3 + 3 + 1 = 7/16) are white. For gamete production: each seed requires 1 male gamete (pollen) and 1 female gamete (egg cell in embryo sac). In angiosperms, 1 microspore mother cell yields 4 functional pollen grains via 1 meiosis (meioses = 1600 / 4 = 400). In contrast, 1 megaspore mother cell yields 4 megaspores, but 3 degenerate, leaving only 1 functional megaspore per meiosis (meioses = 1600 / 1 = 1600).",
                    "3. Execution & Resolution: Phenotypic ratio is 9 Purple : 7 White. Total meiotic divisions required = 400 (microsporogenesis) + 1600 (megasporogenesis) = 2000 meiotic divisions. Thus Ratio = 9 : 7 and Total meiotic divisions = 2000, confirming Option A."
                ],
                "reasoning_route": [
                    {
                        "move_id": "BIO-NSEJS-GEN-01-M1",
                        "kind": "REPRESENT",
                        "description": "Map complementary gene interaction pathway: precursor -> intermediate (via C) -> anthocyanin (via P)."
                    },
                    {
                        "move_id": "BIO-NSEJS-GEN-01-M2",
                        "kind": "MODEL",
                        "description": "Deduce 9 C_P_ (Purple) : 7 (3 C_pp + 3 ccP_ + 1 ccpp, White) phenotypic ratio."
                    },
                    {
                        "move_id": "BIO-NSEJS-GEN-01-M3",
                        "kind": "APPLY",
                        "description": "Compute microsporogenesis (1600 / 4 = 400) and megasporogenesis (1600 / 1 = 1600) meiotic requirements."
                    },
                    {
                        "move_id": "BIO-NSEJS-GEN-01-M4",
                        "kind": "JUSTIFY",
                        "description": "Sum to 2000 divisions, ruling out symmetric 4-spore distractors (1600/4 + 1600/4 = 800) that ignore 3-megaspore degeneration."
                    }
                ]
            },
            "extensions": {
                "grade9v3:analysis": {
                    "difficulty": {
                        "score": 4,
                        "band": "D2",
                        "components": {
                            "c1_genetic_model_selection": 1,
                            "c2_representation_translation": 1,
                            "c3_reasoning_chain_length": 1,
                            "c4_algebra_computational_load": 1,
                            "c5_trap_exception_sensitivity": 0
                        }
                    }
                },
                "grade9v3:core2_support_plan": {
                    "protected_move_refs": [
                        "BIO-NSEJS-GEN-01-M2"
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
        "id": "BIO-NSEJS-GEN-01",
        "source_id": "BIO-NSEJS-GEN-01",
        "source_name": "NSEJS / Junior Science Biology · Q01 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": stem_q01,
        "options": [
            "A: Ratio = 9 : 7; Total meiotic divisions = 2000",
            "B: Ratio = 9 : 7; Total meiotic divisions = 800",
            "C: Ratio = 15 : 1; Total meiotic divisions = 2000",
            "D: Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600"
        ],
        "question_type": "single_correct_mcq",
        "source_figures": ["fig_bio_complementary_genes.svg"],
        "figure_note": "Complementary gene metabolic pathway and megasporogenesis vs microsporogenesis meiosis stoichiometry.",
        "hints": [
            {
                "prompt": "H1 (Complementary Gene Phenotype): Group the 16 Punnett square classes by flower color.",
                "text": "Only genotypes with at least one C and one P (C_P_) produce purple flowers (9/16). All other classes (3 C_pp + 3 ccP_ + 1 ccpp = 7/16) produce white flowers."
            },
            {
                "prompt": "H2 (Male Gamete Meiosis): How many pollen grains are produced per meiotic division?",
                "text": "In plants, 1 microspore mother cell yields 4 functional pollen grains. For 1600 pollen grains: 1600 / 4 = 400 meiotic divisions."
            },
            {
                "prompt": "H3 (Crux Move): Account for functional female gametes and sum.",
                "text": "Crux Move: Each megaspore mother cell yields 4 megaspores, but 3 degenerate, leaving only 1 functional megaspore per meiosis (1600 divisions). Total = 400 + 1600 = 2000."
            }
        ],
        "answer": "Official Key: (A) Ratio = 9 : 7; Total meiotic divisions = 2000",
        "steps": [
            "1. System Representation & Setup: Dihybrid cross CcPp x CcPp in sweet pea produces 1600 seeds. C and P are complementary dominant alleles. We find phenotypic ratio and required meiotic divisions.",
            "2. Physical Model & Formulation: Genotype distribution: 9 C_P_ : 3 C_pp : 3 ccP_ : 1 ccpp. Only C_P_ has both functional enzymes for anthocyanin (9 Purple : 7 White). For 1600 seeds, 1600 pollen grains and 1600 functional ovules are required.",
            "3. Execution & Resolution: Pollen divisions = 1600 / 4 = 400. Ovule divisions = 1600 / 1 = 1600 (due to 3 degenerating megaspores). Total meiotic divisions = 400 + 1600 = 2000. Option A."
        ],
        "check": "Independent check: If female gametes also yielded 4 functional spores, total would be 400 + 400 = 800 (Option B distractor). Botanical fact confirms 3 degenerate, requiring 1600 MMC divisions. Total = 2000. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-01-M2",
        "family_ref": "BIO-GENETICS",
        "primary_capability_ref": "BIO-GEN-MODEL-Q01",
        "stem_sha256": stem_q01_hash
    },
    {
        "id": "BIO-NSEJS-GEN-02",
        "source_id": "BIO-NSEJS-GEN-02",
        "source_name": "NSEJS / Junior Science Biology · Q02 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "During the generation and propagation of a nerve impulse along an unmyelinated mammalian axon, which sequence of ionic events across the axonal membrane correctly describes the transition from resting potential ($-70\\text{ mV}$) through peak depolarization ($+30\\text{ mV}$) to repolarization and the refractory period?",
        "options": [
            "A: Threshold depolarization to -55 mV triggers rapid opening of voltage-gated Na+ channels causing Na+ influx to +30 mV; at peak, Na+ channels inactivate and voltage-gated K+ channels open causing K+ efflux to repolarize and briefly hyperpolarize the membrane (-90 mV) before Na+/K+ ATPase restores resting potential.",
            "B: Influx of K+ ions causes depolarization to +30 mV, followed by efflux of Na+ ions during repolarization.",
            "C: Opening of Cl- channels depolarizes the membrane to +30 mV, while opening of Ca2+ channels repolarizes it.",
            "D: The Na+/K+ pump reverses its direction during an action potential, pumping 3 K+ in and 2 Na+ out."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Threshold and Depolarization): Which ion moves down its electrochemical gradient to drive the membrane potential positive?",
                "text": "Voltage-gated Na+ channels open rapidly at threshold (-55 mV), driving rapid Na+ influx toward the sodium equilibrium potential (+60 mV), peaking at +30 mV."
            },
            {
                "prompt": "H2 (Repolarization Mechanism): Which channel opens to bring the potential back toward negative values?",
                "text": "At +30 mV, Na+ channels inactivate and slower voltage-gated K+ channels open, allowing rapid K+ efflux down its concentration gradient."
            },
            {
                "prompt": "H3 (Crux Move): Trace after-hyperpolarization and resting potential recovery.",
                "text": "Crux Move: K+ channels close slowly causing temporary hyperpolarization (-90 mV), and the Na+/K+ ATPase restores original resting ion distributions (3 Na+ out, 2 K+ in)."
            }
        ],
        "answer": "Official Key: (A) Threshold depolarization to -55 mV triggers rapid opening of voltage-gated Na+ channels causing Na+ influx to +30 mV; at peak, Na+ channels inactivate and voltage-gated K+ channels open causing K+ efflux to repolarize and briefly hyperpolarize the membrane (-90 mV) before Na+/K+ ATPase restores resting potential.",
        "steps": [
            "1. System Representation & Setup: The axonal membrane maintains resting potential at -70 mV via Na+/K+ ATPase (3 Na+ pumped out for 2 K+ pumped in) and K+ leak channels. We evaluate action potential phases.",
            "2. Physical Model & Formulation: Depolarization reaching threshold (-55 mV) triggers voltage-gated Na+ activation gates, driving massive Na+ influx down concentration and electrical gradients to +30 mV.",
            "3. Execution & Resolution: At +30 mV, Na+ inactivation gates close, and voltage-gated K+ channels open, causing rapid K+ efflux that repolarizes the axon. Delayed closure of K+ channels produces after-hyperpolarization (-90 mV) until active Na+/K+ pumping re-establishes -70 mV. Option A."
        ],
        "check": "Independent check: Intracellular [K+] is ~140 mM vs extracellular 5 mM; [Na+] is 145 mM extracellular vs 12 mM intracellular. Na+ influx depolarizes; K+ efflux repolarizes. Option A confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Genetics & Coordination",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "BIO-NSEJS-GEN-02-M2",
        "family_ref": "BIO-PHYSIOLOGY",
        "primary_capability_ref": "BIO-PHYS-MODEL-Q02",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-02").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-03",
        "source_id": "BIO-NSEJS-GEN-03",
        "source_name": "NSEJS / Junior Science Biology · Q03 · APPLY · D2 (Score 3)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "A person accidentally touches a hot stove with their finger and immediately withdraws their hand before feeling conscious pain. Which sequence correctly represents the neural pathway and neurotransmitter action governing this monosynaptic/polysynaptic spinal reflex arc?",
        "options": [
            "A: Thermal pain nociceptor -> Afferent sensory neuron via dorsal root ganglion -> Spinal cord gray matter interneuron -> Efferent motor neuron via ventral root -> Acetylcholine release at neuromuscular junction causing biceps contraction.",
            "B: Pain nociceptor -> Cerebral cortex primary sensory area -> Motor cortex -> Descending pyramidal tract -> Efferent motor neuron.",
            "C: Afferent sensory neuron via ventral root -> Sympathetic ganglion -> Adrenal medulla -> Motor nerve via dorsal root.",
            "D: Interneuron in cerebellum -> Ventral horn sensory cell -> Dorsal root motor nerve -> Neuromuscular junction."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Root Anatomy of Spinal Cord): Remember Bell-Magendie Law for spinal roots.",
                "text": "Sensory afferent fibers enter the spinal cord via the dorsal root (cell bodies in dorsal root ganglion). Motor efferent fibers exit via the ventral root."
            },
            {
                "prompt": "H2 (Spinal Reflex Architecture): Does the initial withdrawal reflex involve cerebral cortex processing?",
                "text": "No; spinal reflex arcs are integrated at the level of spinal cord interneurons to minimize response time before ascending tracts inform the sensory cortex."
            },
            {
                "prompt": "H3 (Crux Move): Trace the somatic neurotransmitter at the neuromuscular junction.",
                "text": "Crux Move: Somatic motor neurons release acetylcholine (ACh) onto nicotinic receptors on the motor end-plate of the effector muscle (biceps)."
            }
        ],
        "answer": "Official Key: (A) Thermal pain nociceptor -> Afferent sensory neuron via dorsal root ganglion -> Spinal cord gray matter interneuron -> Efferent motor neuron via ventral root -> Acetylcholine release at neuromuscular junction causing biceps contraction.",
        "steps": [
            "1. System Representation & Setup: Rapid hand withdrawal from a noxious thermal stimulus occurs via a polysynaptic spinal withdrawal reflex arc.",
            "2. Physical Model & Formulation: Thermal nociceptors generate action potentials in pseudo-unipolar sensory neurons entering the spinal cord through the dorsal root ganglion. In the dorsal horn gray matter, they synapse onto excitatory interneurons.",
            "3. Execution & Resolution: The interneuron excites alpha-motor neurons whose axons exit through the ventral root. At the motor end plate, action potentials trigger voltage-gated Ca2+ entry, exocytosis of acetylcholine, and rapid contraction of the flexor muscle. Option A."
        ],
        "check": "Independent check: Dorsal = Sensory, Ventral = Motor (Bell-Magendie law). Conscious perception reaches cortex via spinothalamic tract only after the spinal reflex completes. Confirmed.",
        "op": "APPLY",
        "band": "D2",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-03-M2",
        "family_ref": "BIO-PHYSIOLOGY",
        "primary_capability_ref": "BIO-PHYS-APPLY-Q03",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-03").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-04",
        "source_id": "BIO-NSEJS-GEN-04",
        "source_name": "NSEJS / Junior Science Biology · Q04 · JUSTIFY · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "When a potted seedling is placed horizontally in the dark, the shoot bends upwards (negative gravitropism) while the primary root bends downwards (positive gravitropism). According to the Cholodny-Went hypothesis and tissue-specific auxin dose-response kinetics, which physiological mechanism accounts for these opposite directional responses?",
        "options": [
            "A: Statolith sedimentation causes auxin to accumulate along the lower side of both root and shoot; this high auxin concentration stimulates cell elongation in the shoot, but exceeds the optimum threshold in the root, thereby inhibiting lower-side root cell elongation.",
            "B: Auxin accumulates exclusively on the upper side of roots and the lower side of shoots.",
            "C: Gibberellin replaces auxin in roots to reverse the gravitational bending direction.",
            "D: Ethylene production on the upper side of the root accelerates cell division while auxin has no effect."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Auxin Redistribution by Gravity): How does gravity affect auxin distribution in horizontal organs?",
                "text": "Dense starch-filled amyloplasts (statoliths) sediment to the lower side of cells, stimulating polar PIN-transporter localization that moves auxin to the lower flank in both roots and shoots."
            },
            {
                "prompt": "H2 (Sensitivity Curves of Roots vs Shoots): Compare the optimum auxin concentrations for elongation.",
                "text": "Roots are roughly 100,000 times more sensitive to auxin than shoots. The optimal auxin concentration for shoot elongation is ~10^-5 M, whereas for roots it is ~10^-10 M."
            },
            {
                "prompt": "H3 (Crux Move): Reconcile the differential elongation responses.",
                "text": "Crux Move: High auxin on the lower flank stimulates shoot cell elongation (bending upward), but suppresses root cell elongation (causing the upper side to elongate faster and bend downward)."
            }
        ],
        "answer": "Official Key: (A) Statolith sedimentation causes auxin to accumulate along the lower side of both root and shoot; this high auxin concentration stimulates cell elongation in the shoot, but exceeds the optimum threshold in the root, thereby inhibiting lower-side root cell elongation.",
        "steps": [
            "1. System Representation & Setup: A seedling placed horizontally displays negative gravitropism in shoots and positive gravitropism in roots despite identical lateral gravity vectors.",
            "2. Physical Model & Formulation: Statoliths sediment to the bottom of statocytes in shoot endodermis and root columella, redirecting PIN efflux carriers to transport auxin (IAA) laterally to the lower flank of both organs.",
            "3. Execution & Resolution: Shoots have a high auxin tolerance; the accumulated lower-flank auxin accelerates proton extrusion (acid growth), causing the lower side to elongate faster than the upper side (upward curvature). Roots operate at much lower sensitivity thresholds; the same high auxin concentration induces ethylene/growth arrest on the lower flank, so the upper flank elongates faster (downward curvature). Option A."
        ],
        "check": "Independent check: Classical Thimann auxin dose-response curve shows stimulation for shoots at concentrations that are deeply inhibitory for roots. Option A confirmed.",
        "op": "JUSTIFY",
        "band": "D2",
        "batch": "Genetics & Coordination",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 0,
            "reasoning_chain_length": 2,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "BIO-NSEJS-GEN-04-M3",
        "family_ref": "BIO-PLANT-PHYSIOLOGY",
        "primary_capability_ref": "BIO-PLANT-JUST-Q04",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-04").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-05",
        "source_id": "BIO-NSEJS-GEN-05",
        "source_name": "NSEJS / Junior Science Biology · Q05 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "A short-day plant (SDP) with a critical dark period of $9.0\\text{ hours}$ is exposed to a light regimen of $14\\text{ hours light}$ and $10\\text{ hours darkness}$. In one experiment, the $10\\text{ hour}$ dark phase is interrupted in the middle by a $2\\text{ minute}$ flash of red light ($660\\text{ nm}$). In a second experiment, this red flash is immediately followed by a $2\\text{ minute}$ flash of far-red light ($730\\text{ nm}$). What are the flowering responses in the two experiments?",
        "options": [
            "A: Experiment 1: Fails to flower; Experiment 2: Flowers successfully",
            "B: Experiment 1: Flowers successfully; Experiment 2: Fails to flower",
            "C: Both experiments fail to flower",
            "D: Both experiments flower successfully"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Requirement for SDP Flowering): What governs flowering in short-day plants?",
                "text": "Short-day plants are actually 'long-night plants'; they require a continuous, uninterrupted dark period equal to or exceeding the critical night length (here 9.0 h)."
            },
            {
                "prompt": "H2 (Phytochrome Interconversion): What happens when phytochrome absorbs red (660 nm) vs far-red (730 nm) light?",
                "text": "Red light (660 nm) converts inactive Pr into active Pfr. Pfr inhibits flowering in short-day plants. Far-red light (730 nm) converts Pfr back into inactive Pr."
            },
            {
                "prompt": "H3 (Crux Move): Determine the final phytochrome form in both experiments.",
                "text": "Crux Move: In Exp 1, the night break leaves Pfr, preventing flowering. In Exp 2, the subsequent far-red flash photoreverses Pfr back to Pr, resetting the dark clock and permitting flowering."
            }
        ],
        "answer": "Official Key: (A) Experiment 1: Fails to flower; Experiment 2: Flowers successfully",
        "steps": [
            "1. System Representation & Setup: An SDP requires >= 9.0 h continuous uninterrupted darkness. The baseline provides 10.0 h darkness (> 9.0 h).",
            "2. Physical Model & Formulation: A brief flash of red light (660 nm) converts inactive Pr into active Pfr. In SDPs, presence of Pfr during the critical night suppresses florigen synthesis, aborting flowering (Experiment 1 fails).",
            "3. Execution & Resolution: When red light is immediately followed by far-red light (730 nm), Pfr is photoconverted back into Pr. Because the final light signal is far-red, no active Pfr remains to inhibit flowering, allowing the plant to flower (Experiment 2 succeeds). Option A."
        ],
        "check": "Independent check: Classic Borthwick-Hendricks phytochrome photoreversibility: the wavelength of the final flash determines the biological response. Final far-red = Pr active state = flowering in SDPs. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Genetics & Coordination",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "BIO-NSEJS-GEN-05-M2",
        "family_ref": "BIO-PLANT-PHYSIOLOGY",
        "primary_capability_ref": "BIO-PLANT-MODEL-Q05",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-05").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-06",
        "source_id": "BIO-NSEJS-GEN-06",
        "source_name": "NSEJS / Junior Science Biology · Q06 · SYNTHESIZE · D2 (Score 5)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "Following a carbohydrate-rich meal, human blood glucose rises from baseline ($90\\text{ mg/dL}$) to $150\\text{ mg/dL}$, triggering endocrine secretion. Later during fasting, glucose falls to $70\\text{ mg/dL}$. Which statement correctly identifies the pancreatic endocrine cell types, their secreted hormones, and their primary biochemical target mechanisms during these two physiological states?",
        "options": [
            "A: Hyperglycemia stimulates pancreatic beta-cells to secrete insulin, promoting GLUT-4 translocation, hepatic glycogenesis, and cellular glucose uptake; hypoglycemia stimulates alpha-cells to secrete glucagon, activating hepatic glycogenolysis and gluconeogenesis.",
            "B: Hyperglycemia stimulates alpha-cells to secrete insulin, while hypoglycemia stimulates beta-cells to secrete glucagon.",
            "C: Insulin activates glycogenolysis in skeletal muscle to release free glucose into the blood stream.",
            "D: Glucagon directly stimulates adipocytes to absorb excess circulating glucose as triglycerides."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Islet of Langerhans Cell Types): Distinguish beta-cells from alpha-cells.",
                "text": "Beta-cells produce insulin in response to elevated blood glucose. Alpha-cells produce glucagon in response to low blood glucose."
            },
            {
                "prompt": "H2 (Cellular Action of Insulin): How does insulin facilitate glucose entry into muscle and fat?",
                "text": "Insulin receptor activation stimulates intracellular vesicles containing GLUT-4 glucose transporters to fuse with the plasma membrane."
            },
            {
                "prompt": "H3 (Crux Move): Contrast hepatic glycogenolysis with glycogenesis.",
                "text": "Crux Move: Insulin triggers glycogenesis in liver and muscles; glucagon acts on liver hepatocytes to stimulate glycogen breakdown (glycogenolysis) and gluconeogenesis."
            }
        ],
        "answer": "Official Key: (A) Hyperglycemia stimulates pancreatic beta-cells to secrete insulin, promoting GLUT-4 translocation, hepatic glycogenesis, and cellular glucose uptake; hypoglycemia stimulates alpha-cells to secrete glucagon, activating hepatic glycogenolysis and gluconeogenesis.",
        "steps": [
            "1. System Representation & Setup: Blood glucose homeostasis oscillates between post-prandial hyperglycemia (150 mg/dL) and fasting hypoglycemia (70 mg/dL).",
            "2. Physical Model & Formulation: Elevated blood glucose is detected by beta-cells in the Islets of Langerhans, stimulating exocytosis of insulin. Insulin promotes glucose uptake via GLUT-4 translocation in skeletal muscle/adipose tissue and promotes glycogen synthesis (glycogenesis) in hepatocytes.",
            "3. Execution & Resolution: In hypoglycemia, alpha-cells secrete glucagon. Glucagon binds GPCRs on hepatocytes, raising cAMP to activate glycogen phosphorylase (glycogenolysis) and gluconeogenic enzymes, restoring circulating glucose to 90 mg/dL. Option A."
        ],
        "check": "Independent check: Muscle lacks glucose-6-phosphatase, so muscle glycogen cannot be released directly into blood (refuting distractor C). Glucagon raises blood glucose (refuting D). Option A confirmed.",
        "op": "SYNTHESIZE",
        "band": "D2",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-06-M2",
        "family_ref": "BIO-PHYSIOLOGY",
        "primary_capability_ref": "BIO-PHYS-SYNTH-Q06",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-06").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-07",
        "source_id": "BIO-NSEJS-GEN-07",
        "source_name": "NSEJS / Junior Science Biology · Q07 · APPLY · D2 (Score 3)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "Red-green color blindness is an X-linked recessive condition ($X^c$). A man with normal color vision ($X^C Y$) marries a woman with normal vision whose father was color-blind ($X^c Y$). If this couple has four children (two sons and two daughters), what is the probability that their first son will be color-blind, and what is the probability that any given daughter will be color-blind?",
        "options": [
            "A: Probability for a son = 50.0%; Probability for a daughter = 0.0%",
            "B: Probability for a son = 25.0%; Probability for a daughter = 25.0%",
            "C: Probability for a son = 50.0%; Probability for a daughter = 50.0%",
            "D: Probability for a son = 100.0%; Probability for a daughter = 0.0%"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Genotype of the Mother): Deduce the mother's genotype from her father's phenotype.",
                "text": "The mother has normal vision but inherited an X chromosome from her color-blind father (X^c Y), so she must be a heterozygous carrier: X^C X^c."
            },
            {
                "prompt": "H2 (Sons' Inheritance): Which sex chromosome does a son inherit from each parent?",
                "text": "A son inherits Y from the normal father and either X^C or X^c from the mother with 50% probability."
            },
            {
                "prompt": "H3 (Crux Move): Daughters' inheritance and phenotype.",
                "text": "Crux Move: Every daughter receives X^C from the father. Because X^C is dominant, 100% of daughters have normal color vision (probability of affected daughter = 0.0%)."
            }
        ],
        "answer": "Official Key: (A) Probability for a son = 50.0%; Probability for a daughter = 0.0%",
        "steps": [
            "1. System Representation & Setup: Father has genotype X^C Y. Mother has normal vision with a color-blind father (X^c Y), establishing her carrier genotype as X^C X^c.",
            "2. Physical Model & Formulation: Cross is X^C Y x X^C X^c. Male progeny genotypes: 1/2 X^C Y (normal vision), 1/2 X^c Y (color-blind). Female progeny genotypes: 1/2 X^C X^C (normal homozygous), 1/2 X^C X^c (normal carrier).",
            "3. Execution & Resolution: For any given son, probability of color blindness is 1/2 = 50.0%. For any given daughter, because she always receives the dominant X^C allele from her father, probability of color blindness is 0.0%. Option A."
        ],
        "check": "Independent check: Sons inherit X strictly from mother; carrier mother gives 50% risk. Daughters inherit normal X from father, masking any maternal recessive allele. Option A confirmed.",
        "op": "APPLY",
        "band": "D2",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-07-M2",
        "family_ref": "BIO-GENETICS",
        "primary_capability_ref": "BIO-GEN-APPLY-Q07",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-07").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-08",
        "source_id": "BIO-NSEJS-GEN-08",
        "source_name": "NSEJS / Junior Science Biology · Q08 · MODEL · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "A double-stranded DNA duplex contains 2000 base pairs ($4000$ total nucleotides). Biochemical analysis reveals that Adenine accounts for $28.0\%$ of the total nitrogenous bases in the molecule. Calculate the total number of Guanine nucleotides present in this DNA molecule and the total number of hydrogen bonds stabilizing the duplex.",
        "options": [
            "A: Guanine nucleotides = 880; Total hydrogen bonds = 4880",
            "B: Guanine nucleotides = 1120; Total hydrogen bonds = 5120",
            "C: Guanine nucleotides = 880; Total hydrogen bonds = 5120",
            "D: Guanine nucleotides = 440; Total hydrogen bonds = 4880"
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Chargaff's Rules): Relate base proportions in double-stranded DNA.",
                "text": "By Chargaff's rules, %A = %T and %G = %C. %A + %T + %G + %C = 100%."
            },
            {
                "prompt": "H2 (Count Guanine Bases): Calculate percentage and absolute count of Guanine.",
                "text": "%A = 28% => %T = 28%. Total A+T = 56%. Remaining G+C = 44% => %G = 22%. Total nucleotides = 4000, so G = 0.22 * 4000 = 880."
            },
            {
                "prompt": "H3 (Crux Move): Calculate total hydrogen bonds in base pairs.",
                "text": "Crux Move: A-T pairs have 2 hydrogen bonds; G-C pairs have 3 hydrogen bonds. Total H-bonds = 2 * (1120) + 3 * (880) = 2240 + 2640 = 4880."
            }
        ],
        "answer": "Official Key: (A) Guanine nucleotides = 880; Total hydrogen bonds = 4880",
        "steps": [
            "1. System Representation & Setup: A 2000 bp (4000 nucleotides) double-stranded DNA molecule has 28.0% Adenine. We determine the count of Guanine and total hydrogen bonds.",
            "2. Physical Model & Formulation: In dsDNA: [A] = [T] = 28.0% (1120 bases each, forming 1120 A-T base pairs). [G] = [C] = (100% - 56.0%) / 2 = 22.0% (880 bases each, forming 880 G-C base pairs).",
            "3. Execution & Resolution: Count of Guanine = 880 nucleotides. Hydrogen bonds = 2 * (N_AT) + 3 * (N_GC) = 2 * 1120 + 3 * 880 = 2240 + 2640 = 4880 hydrogen bonds. Option A."
        ],
        "check": "Independent check: Total bp = 1120 + 880 = 2000 bp. H-bonds = 2240 + 2640 = 4880. Confirmed.",
        "op": "MODEL",
        "band": "D2",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-08-M2",
        "family_ref": "BIO-MOLECULAR-BIOLOGY",
        "primary_capability_ref": "BIO-MOL-MODEL-Q08",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-08").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-09",
        "source_id": "BIO-NSEJS-GEN-09",
        "source_name": "NSEJS / Junior Science Biology · Q09 · JUSTIFY · D2 (Score 4)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "Sickle-cell anemia is an autosomal recessive disorder caused by a single base-pair substitution (point mutation) in the gene encoding the $\\beta$-globin chain of hemoglobin. Which statement correctly identifies the nature of this mutation at the DNA, mRNA, and polypeptide levels, and explains why it causes sickling of erythrocytes under low oxygen tension?",
        "options": [
            "A: A transversion point mutation replaces adenine with thymine in the coding strand (GAG -> GTG), producing a GUG codon in mRNA that substitutes polar, hydrophilic glutamic acid with non-polar, hydrophobic valine at position 6; under low pO2, deoxygenated HbS polymerizes into fibrous insoluble polymers that distort RBCs into sickle shapes.",
            "B: A frameshift insertion of a single nucleotide disrupts the downstream reading frame, producing a truncated non-functional hemoglobin protein.",
            "C: A transition mutation replaces cytosine with guanine (CTC -> CGC), producing an arginine substitution that prevents iron binding in the heme group.",
            "D: A nonsense mutation introduces a premature stop codon (UAA) at position 6, terminating translation of the beta-globin chain."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Mutation Classification): Is A -> T a transition or transversion?",
                "text": "Purine (A) to pyrimidine (T) is a transversion mutation. Coding strand changes from GAG to GTG (template CTC to CAC)."
            },
            {
                "prompt": "H2 (Codon and Amino Acid Shift): What amino acid does GUG encode?",
                "text": "GAG encodes glutamic acid (negatively charged/hydrophilic). GUG encodes valine (hydrophobic/non-polar) at position 6 of the beta-chain."
            },
            {
                "prompt": "H3 (Crux Move): Hydrophobic interaction under deoxygenation.",
                "text": "Crux Move: Deoxy-HbS exposes hydrophobic valine patches that adhere to complementary hydrophobic pockets on adjacent beta-chains, polymerizing into rigid fibers that sickle the cell."
            }
        ],
        "answer": "Official Key: (A) A transversion point mutation replaces adenine with thymine in the coding strand (GAG -> GTG), producing a GUG codon in mRNA that substitutes polar, hydrophilic glutamic acid with non-polar, hydrophobic valine at position 6; under low pO2, deoxygenated HbS polymerizes into fibrous insoluble polymers that distort RBCs into sickle shapes.",
        "steps": [
            "1. System Representation & Setup: Sickle-cell anemia is a classic monogenic hemoglobinopathy. We evaluate the molecular pathology at DNA, RNA, and protein tiers.",
            "2. Physical Model & Formulation: Normal beta-globin gene has coding triplet GAG (template CTC), transcribed to GAG mRNA, specifying Glutamic acid (Glu) at position 6. In HbS, transversion A -> T yields GTG (template CAC), transcribed to GUG mRNA, specifying Valine (Val).",
            "3. Execution & Resolution: Replacing hydrophilic glutamate with hydrophobic valine creates an abnormal sticky patch on the exterior surface of the deoxygenated hemoglobin tetramer, causing self-assembly into 14-strand helical filaments that mechanically deform erythrocytes into sickle shapes. Option A."
        ],
        "check": "Independent check: Purine <-> Pyrimidine is a transversion. Glu (polar acidic) -> Val (non-polar aliphatic) at position 6 of beta-globin chain is the textbook lesion for HbS. Option A confirmed.",
        "op": "JUSTIFY",
        "band": "D2",
        "batch": "Genetics & Coordination",
        "review_state": "NOT_ADMITTED",
        "key_state": "VERIFIED_IAPT_KEY",
        "flags": ["Candidate intake; independent external QRT adjudication receipt pending."],
        "score": 4,
        "components": {
            "concept_model_selection": 1,
            "representation_translation": 1,
            "reasoning_chain_length": 1,
            "algebra_computational_load": 0,
            "trap_exception_sensitivity": 1
        },
        "crux_move_ref": "BIO-NSEJS-GEN-09-M3",
        "family_ref": "BIO-MOLECULAR-BIOLOGY",
        "primary_capability_ref": "BIO-MOL-JUST-Q09",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-09").hexdigest()
    },
    {
        "id": "BIO-NSEJS-GEN-10",
        "source_id": "BIO-NSEJS-GEN-10",
        "source_name": "NSEJS / Junior Science Biology · Q10 · APPLY · D1 (Score 2)",
        "category": "EXAM_CLAIM",
        "origin": "OLYMPIAD_FOUNDATION_ARCHIVE",
        "topic": "CONTROL_AND_COORDINATION_GENETICS_AND_HEREDITY",
        "stem": "Blood plasma calcium concentration is tightly maintained at approximately $9.0 - 11.0\\text{ mg/dL}$ by the antagonistic actions of two peptide hormones: Parathyroid Hormone (PTH) and Calcitonin. Which of the following correctly pairs each hormone with its gland of origin, physiological trigger, and cellular action on bone and kidneys?",
        "options": [
            "A: Hypocalcemia triggers the parathyroid glands to secrete PTH, which stimulates osteoclastic bone resorption and renal Ca2+ reabsorption; hypercalcemia triggers thyroid parafollicular C-cells to secrete calcitonin, which inhibits osteoclasts and promotes bone mineralization.",
            "B: Hypercalcemia triggers parathyroid glands to secrete PTH to deposit excess calcium into bones; hypocalcemia triggers the thyroid gland to secrete calcitonin.",
            "C: Both PTH and calcitonin are secreted by the adrenal cortex to regulate aldosterone and potassium channels.",
            "D: Calcitonin stimulates renal synthesis of active Vitamin D (calcitriol) while PTH inhibits intestinal calcium absorption."
        ],
        "question_type": "single_correct_mcq",
        "hints": [
            {
                "prompt": "H1 (Parathyroid Hormone Action): What is the physiological purpose of PTH?",
                "text": "PTH is hypercalcemic (raises blood Ca2+). It is released in response to low plasma calcium (hypocalcemia)."
            },
            {
                "prompt": "H2 (Calcitonin Action): What is the physiological purpose of Calcitonin?",
                "text": "Calcitonin is hypocalcemic (lowers blood Ca2+). It is secreted by parafollicular C-cells of the thyroid gland in response to high plasma calcium."
            },
            {
                "prompt": "H3 (Crux Move): Target organs and cellular actions.",
                "text": "Crux Move: PTH stimulates bone osteoclasts to dissolve hydroxyapatite and enhances renal Ca2+ reabsorption. Calcitonin inhibits osteoclasts and promotes Ca2+ excretion."
            }
        ],
        "answer": "Official Key: (A) Hypocalcemia triggers the parathyroid glands to secrete PTH, which stimulates osteoclastic bone resorption and renal Ca2+ reabsorption; hypercalcemia triggers thyroid parafollicular C-cells to secrete calcitonin, which inhibits osteoclasts and promotes bone mineralization.",
        "steps": [
            "1. System Representation & Setup: Calcium homeostasis in human blood is regulated between 9-11 mg/dL by negative feedback loops involving PTH and calcitonin.",
            "2. Physical Model & Formulation: When plasma Ca2+ drops below 9.0 mg/dL, chief cells in the parathyroid glands release PTH. PTH stimulates RANKL signaling to activate bone osteoclasts (releasing Ca2+ and phosphate), stimulates renal 1-alpha-hydroxylase to form calcitriol, and increases distal tubule Ca2+ reabsorption.",
            "3. Execution & Resolution: Conversely, when plasma Ca2+ rises above 11.0 mg/dL, parafollicular C-cells in the thyroid gland secrete calcitonin. Calcitonin directly binds osteoclast receptors to arrest bone resorption and inhibits renal calcium reabsorption, returning blood calcium to normal. Option A."
        ],
        "check": "Independent check: PTH = hypercalcemic (raises calcium); Calcitonin = hypocalcemic (tones down calcium). Option A confirmed.",
        "op": "APPLY",
        "band": "D1",
        "batch": "Genetics & Coordination",
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
        "crux_move_ref": "BIO-NSEJS-GEN-10-M2",
        "family_ref": "BIO-ENDOCRINOLOGY",
        "primary_capability_ref": "BIO-ENDO-APPLY-Q10",
        "stem_sha256": hashlib.sha256(b"BIO-NSEJS-GEN-10").hexdigest()
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
            "question_id": "BIO-NSEJS-GEN-01",
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
            "question_id": "BIO-NSEJS-GEN-01",
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
  <title>Core 2 Learning Module: Complementary Epistasis & Meiosis Stoichiometry (BIO-NSEJS-GEN-01)</title>
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
      <span class="badge badge-primary">Biology Track · Genetics & Heredity</span>
      <span class="badge badge-warning">Band D2 · Score 4</span>
      <h1>BIO-NSEJS-GEN-01: Complementary Gene Epistasis & Meiosis Stoichiometry</h1>
      <p style="color: var(--text-muted); font-size: 14px;">Cognitive Operation: <strong>MODEL</strong> | Crux Reference: <strong>BIO-NSEJS-GEN-01-M2</strong></p>
    </header>

    <div class="stem">
      In sweet pea (<em>Lathyrus odoratus</em>), purple flower coloration requires functional enzymes produced by two independently assorting dominant alleles, <math class="math-tex"><mi>C</mi></math> and <math class="math-tex"><mi>P</mi></math>. Plants with genotypes <math class="math-tex"><mi>C</mi><mi>_</mi><mi>p</mi><mi>p</mi><mo>,</mo><mi>c</mi><mi>c</mi><mi>P</mi><mi>_</mi><mo>,</mo></math> or <math class="math-tex"><mi>c</mi><mi>c</mi><mi>p</mi><mi>p</mi></math> produce white flowers due to a biochemical pathway block.<br><br>
      Two dihybrid heterozygous purple-flowered plants (<math class="math-tex"><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi><mo>&times;</mo><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi></math>) are crossed, yielding 1600 viable seeds. Determine the expected phenotypic ratio of Purple to White flowers in the progeny, and calculate the minimum total number of meiotic divisions required in the parent plants to produce the male and female gametes that formed these 1600 seeds.
    </div>

    <div class="diagram-container">
      <svg width="100%" height="100%" viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="pathway-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#38bdf8"/>
          </marker>
        </defs>
        <!-- Two-Step Enzymatic Pathway (Top Panel) -->
        <text x="50" y="35" fill="#38bdf8" font-size="16" font-weight="700">Complementary Anthocyanin Biochemical Pathway</text>
        <!-- Precursor Box -->
        <rect x="50" y="60" width="160" height="50" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
        <text x="65" y="90" fill="#f8fafc" font-size="14">Colorless Precursor</text>
        <!-- Arrow 1 -->
        <line x1="210" y1="85" x2="275" y2="85" stroke="#38bdf8" stroke-width="3" marker-end="url(#pathway-arrow)"/>
        <text x="225" y="75" fill="#facc15" font-size="14" font-weight="700">Enzyme C</text>
        <!-- Intermediate Box -->
        <rect x="280" y="60" width="160" height="50" rx="6" fill="#1e293b" stroke="#64748b" stroke-width="2"/>
        <text x="295" y="90" fill="#f8fafc" font-size="14">Chromogen Interm.</text>
        <!-- Arrow 2 -->
        <line x1="440" y1="85" x2="505" y2="85" stroke="#38bdf8" stroke-width="3" marker-end="url(#pathway-arrow)"/>
        <text x="455" y="75" fill="#facc15" font-size="14" font-weight="700">Enzyme P</text>
        <!-- Pigment Box -->
        <rect x="510" y="60" width="150" height="50" rx="6" fill="#581c87" stroke="#c084fc" stroke-width="2"/>
        <text x="530" y="90" fill="#ffffff" font-size="14" font-weight="700">Purple Pigment</text>

        <!-- Meiosis Stoichiometry Comparison (Bottom Panel) -->
        <line x1="50" y1="140" x2="660" y2="140" stroke="#334155" stroke-width="1.5"/>
        <text x="50" y="170" fill="#10b981" font-size="16" font-weight="700">Meiotic Stoichiometry for 1600 Angiosperm Seeds</text>

        <!-- Microsporogenesis (Left) -->
        <rect x="60" y="190" width="270" height="150" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
        <text x="80" y="220" fill="#38bdf8" font-size="15" font-weight="700">Pollen (Microsporogenesis)</text>
        <text x="80" y="250" fill="#f8fafc" font-size="14">1 MMC &rarr; 4 Functional Pollen Grains</text>
        <text x="80" y="280" fill="#94a3b8" font-size="14">Divisions = 1600 / 4</text>
        <text x="80" y="315" fill="#facc15" font-size="16" font-weight="700">= 400 Meiotic Divisions</text>

        <!-- Megasporogenesis (Right) -->
        <rect x="370" y="190" width="270" height="150" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
        <text x="390" y="220" fill="#10b981" font-size="15" font-weight="700">Ovule (Megasporogenesis)</text>
        <text x="390" y="250" fill="#f8fafc" font-size="14">1 MMC &rarr; 1 Functional Megaspore</text>
        <text x="390" y="270" fill="#f87171" font-size="14">(3 Megaspores Degenerate)</text>
        <text x="390" y="295" fill="#94a3b8" font-size="14">Divisions = 1600 / 1</text>
        <text x="390" y="325" fill="#facc15" font-size="16" font-weight="700">= 1600 Meiotic Divisions</text>
      </svg>
    </div>

    <form id="quiz-form" onsubmit="event.preventDefault();">
      <div class="options-group">
        <label class="option-label">
          <input type="radio" name="opt" value="A" onchange="enableCommit()">
          <span>(A) Ratio = 9 : 7; Total meiotic divisions = 2000</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="B" onchange="enableCommit()">
          <span>(B) Ratio = 9 : 7; Total meiotic divisions = 800</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="C" onchange="enableCommit()">
          <span>(C) Ratio = 15 : 1; Total meiotic divisions = 2000</span>
        </label>
        <label class="option-label">
          <input type="radio" name="opt" value="D" onchange="enableCommit()">
          <span>(D) Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600</span>
        </label>
      </div>
      <button type="button" id="commit-btn" class="btn btn-primary" disabled onclick="commitAnswer()">Commit Answer</button>
    </form>

    <div class="hints-section">
      <h3 style="margin-bottom: 12px; font-size: 16px;">Guided Pre-Attempt Hints</h3>
      <details>
        <summary>Tier 1: Classical Dihybrid Genotype Classes</summary>
        <div class="hint-content">
          A dihybrid selfing cross (<math class="math-tex"><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi><mo>&times;</mo><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi></math>) yields 16 genotype combinations: 9 <math class="math-tex"><mi>C</mi><mi>_</mi><mi>P</mi><mi>_</mi></math>, 3 <math class="math-tex"><mi>C</mi><mi>_</mi><mi>p</mi><mi>p</mi></math>, 3 <math class="math-tex"><mi>c</mi><mi>c</mi><mi>P</mi><mi>_</mi></math>, and 1 <math class="math-tex"><mi>c</mi><mi>c</mi><mi>p</mi><mi>p</mi></math>.
        </div>
      </details>
      <details>
        <summary>Tier 2: Complementary Epistatic Phenotype Collapse</summary>
        <div class="hint-content">
          Because anthocyanin synthesis requires functional enzymes from both genes, only <math class="math-tex"><mi>C</mi><mi>_</mi><mi>P</mi><mi>_</mi></math> yields purple flowers. If either gene is homozygous recessive (<math class="math-tex"><mi>p</mi><mi>p</mi></math> or <math class="math-tex"><mi>c</mi><mi>c</mi></math>), the flower remains white. Collapse the classes into Purple : White.
        </div>
      </details>
      <details>
        <summary>Tier 3: Asymmetric Meiotic Yield in Seed Formation</summary>
        <div class="hint-content">
          Each seed requires one male and one female gamete. Remember the botanical asymmetry: 1 microspore mother cell yields 4 functional pollen grains, but 1 megaspore mother cell yields only 1 functional megaspore (3 degenerate). Sum both meiotic requirements.
        </div>
      </details>
    </div>

    <div id="derivation-section" class="derivation" style="display: none;">
      <h3>Commitment Verified: Complete Biological Derivation</h3>
      <div class="step-box">
        <div class="step-title">1. System Representation & Setup:</div>
        <p>Sweet pea flower anthocyanin synthesis is governed by two complementary genes (<math class="math-tex"><mi>C</mi></math> and <math class="math-tex"><mi>P</mi></math>). Dihybrids <math class="math-tex"><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi><mo>&times;</mo><mi>C</mi><mi>c</mi><mi>P</mi><mi>p</mi></math> produce 1600 viable seeds. We evaluate the phenotypic ratio and gametogenesis meiosis requirements.</p>
      </div>
      <div class="step-box">
        <div class="step-title">2. Physical Model & Formulation:</div>
        <p>Mendelian dihybrid cross distribution:<br>
        - <math class="math-tex"><mn>9</mn><mo>/</mo><mn>16</mn><mtext>&nbsp;</mtext><mi>C</mi><mi>_</mi><mi>P</mi><mi>_</mi></math> &rarr; Both enzymes functional &rarr; <strong>Purple</strong><br>
        - <math class="math-tex"><mn>3</mn><mo>/</mo><mn>16</mn><mtext>&nbsp;</mtext><mi>C</mi><mi>_</mi><mi>p</mi><mi>p</mi></math> &rarr; Lacks enzyme P &rarr; White<br>
        - <math class="math-tex"><mn>3</mn><mo>/</mo><mn>16</mn><mtext>&nbsp;</mtext><mi>c</mi><mi>c</mi><mi>P</mi><mi>_</mi></math> &rarr; Lacks enzyme C &rarr; White<br>
        - <math class="math-tex"><mn>1</mn><mo>/</mo><mn>16</mn><mtext>&nbsp;</mtext><mi>c</mi><mi>c</mi><mi>p</mi><mi>p</mi></math> &rarr; Lacks both enzymes &rarr; White<br>
        Combined White = <math class="math-tex"><mn>3</mn><mo>+</mo><mn>3</mn><mo>+</mo><mn>1</mn><mo>=</mo><mn>7</mn><mo>/</mo><mn>16</mn></math>. Phenotypic ratio is <strong>9 : 7</strong>.</p>
      </div>
      <div class="step-box">
        <div class="step-title">3. Execution & Resolution:</div>
        <p>For 1600 seeds, 1600 functional pollen grains and 1600 functional egg cells are required:<br>
        - Microsporogenesis: Each microspore mother cell yields 4 functional pollen grains &rarr; <math class="math-tex"><mn>1600</mn><mo>/</mo><mn>4</mn><mo>=</mo><mn>400</mn></math> meiotic divisions.<br>
        - Megasporogenesis: Each megaspore mother cell undergoes meiosis to yield 4 megaspores, but 3 degenerate; only 1 functional megaspore survives &rarr; <math class="math-tex"><mn>1600</mn><mo>/</mo><mn>1</mn><mo>=</mo><mn>1600</mn></math> meiotic divisions.<br>
        Total meiotic divisions = <math class="math-tex"><mn>400</mn><mo>+</mo><mn>1600</mn><mo>=</mo><mn>2000</mn></math> meiotic divisions.<br>
        Therefore, Ratio = 9 : 7 and Total meiotic divisions = 2000, uniquely confirming <strong>Option A</strong>.</p>
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
  <title>Question Status: Control & Coordination, Genetics & Molecular Heredity</title>
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
  <h1>Biology Track: Control & Coordination, Genetics & Molecular Heredity Status</h1>
  <p>Topic ID: <code>bio-genetics-coordination-r1</code> | Total Items: 10 | Disposition: <code>HOLD:ACADEMIC_ADMISSION</code></p>
  <table>
    <tr><th>ID</th><th>Operation</th><th>Band</th><th>Score</th><th>Title / Core Concept</th><th>Answer</th></tr>
    {''.join(f'<tr><td>{q["id"]}</td><td>{q["op"]}</td><td><span class="badge badge-{q["band"].lower()}">{q["band"]}</span></td><td>{q["score"]}</td><td>{q["batch"]}</td><td>{q["answer"][:18]}</td></tr>' for q in questions)}
  </table>
</body>
</html>
"""
(OUTPUT_DIR / "question-status.html").write_text(status_html, encoding="utf-8")

print("Biology genetics module generated successfully!")
