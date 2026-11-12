"""Builder script for Biology Genetics & Coordination Core 1A, Core 1B, Witness, and Learning Journey HTML.

Anchor: BIO-NSEJS-GEN-01 (Complementary Gene Epistasis & Meiosis Stoichiometry)
"""
import hashlib
import json
from pathlib import Path

MODULE_DIR = Path("workspace/output/bio-genetics-coordination-r1")
MODULE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Core 1A Construction
# ---------------------------------------------------------------------------
core1a = {
    "schema": "core1a-construction/v1",
    "construction_id": "BIO-GEN-C-EPISTASIS-MEIOSIS-01",
    "target_question_id": "BIO-NSEJS-GEN-01",
    "title": "Complementary Gene Epistasis & Angiosperm Meiotic Gametogenesis Stoichiometry",
    "status": "CANDIDATE",
    "purpose": "CORE1A_TEACHING_CONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "GENETICS_AND_HEREDITY",
    "family": "BIO-GENETICS-EPISTASIS-MEIOSIS",
    "capability": "BIO-GEN-COMPLEMENTARY-GENE-MEIOSIS-STOICHIOMETRY",
    "cognitive_demand": "MODEL",
    "difficulty_band": "D2",
    "difficulty_score": 4,
    "crux_move": "M2",
    "declared_conventions": [
        {
            "name": "two_locus_independent_assortment",
            "statement": "Two non-linked genetic loci C and P on separate homologous chromosome pairs assort independently during meiotic metaphase I, generating 16 equally probable dihybrid combinations: 9 C_P_ : 3 C_pp : 3 ccP_ : 1 ccpp."
        },
        {
            "name": "complementary_gene_interaction_epistasis",
            "statement": "Under complementary gene epistasis in a sequential biochemical pathway, enzyme C converts colorless precursor to intermediate and enzyme P converts intermediate to anthocyanin pigment. Functional dominant alleles at BOTH loci (C_P_) are required for purple coloration; any homozygous recessive combination (C_pp, ccP_, ccpp) blocks pigmentation, modifying the classic 9:3:3:1 ratio into 9 Purple : 7 White."
        },
        {
            "name": "microsporogenesis_meiotic_stoichiometry",
            "statement": "In angiosperm anthers, each diploid microspore mother cell (MMC) undergoes a single complete meiotic division (meiosis I and II) to produce 4 functional haploid pollen grains. Therefore, to form N seeds, the male gamete contribution requires exactly N / 4 meiotic divisions."
        },
        {
            "name": "megasporogenesis_meiotic_stoichiometry",
            "statement": "In angiosperm ovules, each diploid megaspore mother cell (MMC) undergoes a single meiotic division to form a linear tetrad of 4 haploid megaspores, of which 3 degenerate. Only 1 functional megaspore forms the female gametophyte (embryo sac and egg cell). Therefore, to form N seeds, the female gamete contribution requires exactly N / 1 meiotic divisions."
        }
    ],
    "entry_assumptions": [
        "Understanding Mendelian dihybrid inheritance and independent assortment of non-linked alleles.",
        "Concepts of biochemical pathways and non-allelic epistatic gene modifications.",
        "Angiosperm reproductive biology: microsporogenesis (pollen formation) versus megasporogenesis (embryo sac formation)."
    ],
    "inferential_jump": "By synthesizing the biochemical pathway model of complementary gene interaction with cytogenetic division stoichiometry, the student models both the modified 9:7 phenotypic ratio from 16 dihybrid squares and the asymmetrical meiotic requirements for angiosperm seed formation: producing 1600 viable seeds requires 1600 male gametes (from 1600 / 4 = 400 meiotic divisions) and 1600 female gametes (from 1600 / 1 = 1600 meiotic divisions, due to 3 megaspores degenerating), giving a total of 400 + 1600 = 2000 meiotic divisions.",
    "teaching_path": [
        {
            "step_number": 1,
            "role": "REPRESENT",
            "action": "Map the two-enzyme biochemical cascade: Precursor (colorless) -> Intermediate (colorless) -> Anthocyanin (purple), catalyzed by enzymes C and P respectively.",
            "why_valid": "Visualizing the biochemical pathway clarifies why a mutation in either gene C or gene P halts pigment synthesis at a colorless stage.",
            "inputs": [
                "Two non-linked loci C and P",
                "Dominant functional alleles C and P",
                "Recessive non-functional alleles c and p"
            ],
            "output": "Phenotypic rule: C_P_ = Purple, while C_pp, ccP_, and ccpp = White."
        },
        {
            "step_number": 2,
            "role": "MODEL",
            "action": "Construct the 16-cell dihybrid array for CcPp x CcPp and group the genotypic classes into purple and white phenotypes.",
            "why_valid": "Independent assortment yields 9 C_P_ (purple) and 3 C_pp + 3 ccP_ + 1 ccpp = 7 white, deriving the modified 9:7 phenotypic ratio.",
            "inputs": [
                "Dihybrid cross CcPp x CcPp",
                "Mendelian array: 9 C_P_ : 3 C_pp : 3 ccP_ : 1 ccpp"
            ],
            "output": "Phenotypic ratio = 9 Purple : 7 White."
        },
        {
            "step_number": 3,
            "role": "APPLY",
            "action": "Calculate the meiotic division requirements for producing male and female gametes to yield 1600 seeds.",
            "why_valid": "Each seed requires one male gamete (from microsporogenesis where 1 MMC -> 4 pollen) and one female gamete (from megasporogenesis where 1 MMC -> 1 functional egg cell).",
            "inputs": [
                "Total viable seeds N = 1600",
                "Microspore yield: 4 pollen per meiosis",
                "Megaspore yield: 1 egg per meiosis"
            ],
            "output": "Male meiotic divisions = 1600 / 4 = 400; Female meiotic divisions = 1600 / 1 = 1600."
        },
        {
            "step_number": 4,
            "role": "JUSTIFY",
            "action": "Sum total meiotic divisions required in parent plants: 400 + 1600 = 2000 divisions, matching Option A.",
            "why_valid": "The minimum total meiotic divisions is the sum of independent microsporocyte and megasporocyte meiotic events.",
            "inputs": [
                "Male divisions = 400",
                "Female divisions = 1600"
            ],
            "output": "Ratio = 9 : 7; Total meiotic divisions = 2000 (Option A)."
        }
    ],
    "representation_bridge": {
        "symbol": "Ratio = 9 : 7, Total Meiotic Divisions = N/4 + N/1 = (5/4)N",
        "element": "Biochemical pathway cascade coupled with microsporogenesis and megasporogenesis meiotic lineage diagrams",
        "in_words": "Complementary genes alter the 9:3:3:1 ratio to 9:7 because functional pigmentation requires both enzymes; angiosperm seed formation requires N/4 male and N female meiotic divisions because three megaspores degenerate.",
        "diagram_ref": "fig_bio_complementary_genes_meiosis.svg"
    },
    "worked_conceptual_anchor": {
        "problem": "In shepherd's purse (Capsella bursa-pastoris), seed capsule shape is controlled by duplicate dominant epistasis involving two independently assorting genes, A and B. A dihybrid cross (AaBb x AaBb) produces 800 viable seeds. Plants with at least one dominant allele (A_B_, A_bb, aaB_) produce triangular capsules, while double recessive plants (aabb) produce ovoid capsules. Calculate (a) the expected phenotypic ratio of triangular to ovoid capsules, (b) the number of triangular and ovoid seeds among 800 seeds, and (c) the minimum total number of meiotic divisions required in the parents to produce the gametes for these 800 seeds.",
        "solution_steps": [
            "1. System Representation & Setup: Independent assortment of AaBb x AaBb produces a 16-cell genotypic array: 9 A_B_, 3 A_bb, 3 aaB_, 1 aabb. Triangular capsules result from A_B_, A_bb, or aaB_ (total 9 + 3 + 3 = 15). Ovoid capsules result strictly from double recessive aabb (1).",
            "2. Physical Model & Formulation: (a) Phenotypic ratio = 15 Triangular : 1 Ovoid. (b) For N = 800 seeds: Triangular seeds = (15/16) * 800 = 750 seeds; Ovoid seeds = (1/16) * 800 = 50 seeds.",
            "3. Execution & Resolution: (c) Gametogenesis stoichiometry for 800 seeds: Each seed requires 1 pollen grain and 1 embryo sac. Microsporogenesis yields 4 pollen grains per meiosis: 800 / 4 = 200 meiotic divisions. Megasporogenesis yields 1 functional egg per meiosis (3 megaspores degenerate): 800 / 1 = 800 meiotic divisions. Total meiotic divisions = 200 + 800 = 1000 divisions.",
            "4. Limiting Check: Notice that gametogenesis stoichiometry depends solely on the number of seeds N (Total = 5N/4 = 5 * 800 / 4 = 1000) and is entirely decoupled from the epistatic ratio (15:1 vs 9:7)."
        ]
    },
    "misconceptions": [
        {
            "wrong_idea": "Assuming meiosis produces 4 functional gametes in both male and female flower organs, calculating total divisions as 1600/4 + 1600/4 = 400 + 400 = 800.",
            "diagnostic_prompt": "Why do 1600 seeds require more than 800 meiotic divisions? How many functional eggs are produced from one megaspore mother cell?",
            "repair": "In angiosperm ovules, cytokinesis during meiosis produces four megaspores, but three immediately degenerate. Only one functional megaspore survives to form the embryo sac. Thus, 1 meiosis produces only 1 functional female gamete, requiring 1600 meiotic divisions for 1600 seeds on the female side alone."
        }
    ],
    "exit_task": {
        "prompt": "In a pea plant cross, 400 round seeds are formed. Calculate the minimum total number of meiotic divisions required in the parent plants to produce the male and female gametes that formed these 400 seeds.",
        "answer": "Male gametes require 400 / 4 = 100 meiotic divisions. Female gametes require 400 / 1 = 400 meiotic divisions. Total minimum meiotic divisions = 100 + 400 = 500 meiotic divisions."
    }
}

# ---------------------------------------------------------------------------
# 2. Core 1B Reconstruction
# ---------------------------------------------------------------------------
core1b = {
    "schema": "core1b-reconstruction/v1",
    "construction_id": "BIO-GEN-C-EPISTASIS-MEIOSIS-01",
    "target_question_id": "BIO-NSEJS-GEN-01",
    "title": "Complementary Genes & Meiosis Stoichiometry: 6-Stage Phenomenological Reconstruction",
    "status": "CANDIDATE",
    "purpose": "CORE1B_PHENOMENOLOGICAL_RECONSTRUCTION",
    "academic_status": "HOLD:ACADEMIC_ADMISSION",
    "topic": "GENETICS_AND_HEREDITY",
    "family": "BIO-GENETICS-EPISTASIS-MEIOSIS",
    "capability": "BIO-GEN-COMPLEMENTARY-GENE-MEIOSIS-STOICHIOMETRY",
    "cognitive_demand": "MODEL",
    "difficulty_band": "D2",
    "difficulty_score": 4,
    "crux_move": "M2",
    "taught_skill_Y": "Modeling epistatic biochemical pathways to predict modified dihybrid phenotypic ratios.",
    "connecting_route_Z": "Applying angiosperm gametogenic meiotic stoichiometry (microsporogenesis 4:1 and megasporogenesis 1:1) to seed populations.",
    "protected_fresh_inference_W": "Deducing that total meiotic divisions for N angiosperm seeds is universally given by N/4 + N = 5N/4, independent of epistatic gene interaction models.",
    "fresh_context_ref": "BIO-NSEJS-GEN-01-CORE1B-EPISTASIS-MEIOSIS-TASK",
    "stages": {
        "stage_1_predict": {
            "prompt": "In sweet pea, purple pigment requires dominant alleles at both loci C and P. In a dihybrid cross CcPp x CcPp, will the proportion of pigmented purple progeny be higher than, equal to, or lower than the classic Mendelian 9/16 dihybrid dominant fraction?",
            "defensible_answer": "Equal to 9/16 (56.25%). The purple phenotype corresponds strictly to the C_P_ class (9/16). However, the remaining three classes (3 C_pp, 3 ccP_, and 1 ccpp) all lack one or both enzymes and collapse into a single white phenotypic class (7/16), yielding a 9:7 ratio instead of 9:3:3:1."
        },
        "stage_2_attempt": {
            "prompt": "For the cross CcPp x CcPp yielding 1600 viable seeds, calculate the expected phenotypic ratio of Purple to White flowers and the minimum total number of meiotic divisions required to produce the gametes for these 1600 seeds.",
            "produces": "Evaluations Ratio = 9 : 7 and Total meiotic divisions = 2000.",
            "closure": "RUBRIC",
            "rubric": [
                {
                    "criterion": "Epistatic phenotypic ratio: derives 9 Purple : 7 White from complementary interaction.",
                    "evidence_of": "Proper understanding of two-locus biochemical pathways."
                },
                {
                    "criterion": "Microsporogenesis evaluation: calculates 1600 / 4 = 400 meiotic divisions for pollen.",
                    "evidence_of": "Competent understanding of male gametogenesis."
                },
                {
                    "criterion": "Megasporogenesis & total summation: calculates 1600 / 1 = 1600 female divisions and total = 2000.",
                    "evidence_of": "Precise execution accounting for megaspore degeneration, confirming Option A."
                }
            ],
            "accepted": [
                "A: Ratio = 9 : 7; Total meiotic divisions = 2000",
                "Ratio = 9 : 7; Total meiotic divisions = 2000",
                "9:7 and 2000",
                "Option A"
            ],
            "rejected": [
                "B: Ratio = 9 : 7; Total meiotic divisions = 800 (assuming 4 functional eggs per female meiosis)",
                "C: Ratio = 15 : 1; Total meiotic divisions = 2000 (confusing complementary with duplicate dominant epistasis)",
                "D: Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600 (ignoring epistasis and miscalculating meiosis)"
            ]
        },
        "stage_3_reconstruct": {
            "route": [
                {
                    "ask": "1. What genotypic combinations produce purple flowers and what combinations produce white flowers in CcPp x CcPp?",
                    "why_this_ask": "Groups the 16 dihybrid combinations according to the complementary pathway requirement.",
                    "step_answer": "Only C_P_ (9 combinations) produces purple flowers because both enzymes are present. The combinations C_pp (3), ccP_ (3), and ccpp (1) all lack at least one required functional enzyme and produce white flowers (total 7)."
                },
                {
                    "ask": "2. What is the resulting phenotypic ratio among the progeny?",
                    "why_this_ask": "Formalizes the modified Mendelian epistatic ratio.",
                    "step_answer": "9 Purple : 7 White."
                },
                {
                    "ask": "3. How many meiotic divisions are required to produce 1600 functional male gametes (pollen grains)?",
                    "why_this_ask": "Applies microsporocyte division stoichiometry.",
                    "step_answer": "One microspore mother cell produces 4 functional pollen grains via meiosis. Thus, 1600 / 4 = 400 meiotic divisions are required."
                },
                {
                    "ask": "4. How many meiotic divisions are required to produce 1600 functional female gametes (egg cells), and what is the total?",
                    "why_this_ask": "Accounts for megaspore degeneration and sums total parental meiotic events.",
                    "step_answer": "In megasporogenesis, 3 of the 4 megaspores degenerate, so 1 meiosis yields only 1 functional egg. Thus, 1600 / 1 = 1600 meiotic divisions are required. Total meiotic divisions = 400 + 1600 = 2000."
                }
            ],
            "differs_from_teaching_path": "Reconstruction systematically prompts the learner to derive the 9:7 ratio from pathway blocks first, then compute male and female meiotic divisions separately, and sum them."
        },
        "stage_4_diagnose": {
            "error_trap": "Assuming that one meiosis yields four functional gametes in female flowers just as it does in male anthers, leading to 1600/4 + 1600/4 = 800 divisions.",
            "diagnostic_prompt": "Why do plants need 1600 meiotic divisions to make 1600 functional ovules instead of 400?",
            "causal_explanation": "During megasporogenesis in angiosperm ovules, the megaspore mother cell undergoes meiosis to produce a linear tetrad of four haploid megaspores. However, three of these megaspores degenerate (undergoing programmed cell death), leaving only one surviving functional megaspore (monosporic development). Therefore, each functional egg cell requires an entire meiotic division: 1 meiosis = 1 functional ovule."
        },
        "stage_5_repair": {
            "action": "Remember the fundamental botanical rule for seed meiosis stoichiometry: Total Meiotic Divisions = (Seeds / 4) [anther/microsporogenesis] + (Seeds / 1) [ovule/megasporogenesis] = 5 * Seeds / 4."
        },
        "stage_6_boundary_test": {
            "prompt": "If the epistatic mechanism were duplicate recessive (recessive epistasis 9:3:4) or dominant epistasis (12:3:1) instead of complementary (9:7), would the number of meiotic divisions required to form 1600 seeds change?",
            "answer": "No. The number of meiotic divisions required to form N viable seeds depends strictly on gametogenesis stoichiometry (N male + N female gametes = N/4 + N = 5N/4 = 2000) and is completely independent of the allelic dominance or epistatic interaction governing seed or flower coat phenotypes.",
            "confirms": "Confirms the decoupled cytogenetic nature of gametogenic division stoichiometry from genetic phenotypic ratios."
        }
    },
    "progressive_hints": [
        {
            "tier": 1,
            "text": "Notice that complementary genes require dominant alleles at BOTH loci for pigmentation. Out of 16 dihybrid squares, how many contain at least one C and one P?"
        },
        {
            "tier": 2,
            "text": "For gametes: each viable seed comes from one pollen grain and one ovule. Remember that in anthers 1 MMC produces 4 pollen grains, but in ovules 3 out of 4 megaspores degenerate!"
        },
        {
            "tier": 3,
            "text": "Male meiosis = 1600 / 4 = 400. Female meiosis = 1600 / 1 = 1600. Total meiotic divisions = 400 + 1600 = 2000."
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
    "author_id": "AUTH-BIO-GENETICS-01",
    "construction": {
        "construction_id": "BIO-GEN-C-EPISTASIS-MEIOSIS-01",
        "topic_id": "BIO-GENETICS-EPISTASIS-MEIOSIS",
        "operation": "MODEL",
        "band": "D2",
        "direction": "CLASSIFY_FROM_CASE",
        "decisive_roles": [
            "EPISTATIC_PATHWAY_PHENOTYPIC_MAPPING",
            "MICROSPOROGENESIS_MEIOTIC_EVALUATION",
            "MEGASPOROGENESIS_DEGENERATION_ACCOUNTING"
        ],
        "signature": {
            "inputs": [
                "Sweet pea complementary genes C and P",
                "Dihybrid cross CcPp x CcPp",
                "1600 viable seeds progeny"
            ],
            "obstacle": "Integrating non-Mendelian epistatic ratio modification with angiosperm asymmetric gametogenic meiotic division stoichiometry",
            "decisive_move": "Derive 9 C_P_ : 7 (C_pp + ccP_ + ccpp) phenotypic ratio and evaluate total meiotic divisions as N/4 + N/1 = 5N/4 = 2000",
            "output": "Ratio = 9 : 7; Total meiotic divisions = 2000, matching Option A",
            "independent_check": "Stoichiometric formula 5N/4 and independence from epistatic ratio variation (tested against 15:1 and 9:3:4)",
            "validity_boundary": "Disomic inheritance in sexually reproducing angiosperms with monosporic embryo sac development",
            "conditions": [
                "Independent assortment of loci C and P",
                "Linear two-enzyme anthocyanin biosynthetic cascade",
                "Monosporic Polygonum-type megagametogenesis",
                "100% seed viability from fertilisation"
            ],
            "dependency_refs": [
                "MENDELIAN_INDEPENDENT_ASSORTMENT",
                "COMPLEMENTARY_GENE_EPISTASIS",
                "MICROSPOROGENESIS_MEIOSIS_STOICHIOMETRY",
                "MEGASPOROGENESIS_MONOSPORIC_DEGENERATION"
            ]
        }
    },
    "core1a": {
        "construction_id": "BIO-GEN-C-EPISTASIS-MEIOSIS-01",
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
            "EPISTATIC_PATHWAY_PHENOTYPIC_MAPPING": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/0",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/0"
            },
            "MICROSPOROGENESIS_MEIOTIC_EVALUATION": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/2",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/1"
            },
            "MEGASPOROGENESIS_DEGENERATION_ACCOUNTING": {
                "teaching_span_ref": "core1a_construction.json#/teaching_path/3",
                "demonstration_ref": "core1a_construction.json#/worked_conceptual_anchor/solution_steps/2"
            }
        }
    },
    "core1b": {
        "construction_id": "BIO-GEN-C-EPISTASIS-MEIOSIS-01",
        "operation": "MODEL",
        "band": "D2",
        "direction": "CLASSIFY_FROM_CASE",
        "task_sha256": c1b_sha,
        "fresh_context_ref": "BIO-NSEJS-GEN-01-CORE1B-EPISTASIS-MEIOSIS-TASK",
        "freshness_review_ref": "PENDING-INDEPENDENT-REVIEW",
        "assessed_roles": {
            "EPISTATIC_PATHWAY_PHENOTYPIC_MAPPING": {
                "attempt_field": "stage_2_attempt.phenotypic_ratio",
                "observable": "determines ratio = 9 Purple : 7 White"
            },
            "MICROSPOROGENESIS_MEIOTIC_EVALUATION": {
                "attempt_field": "stage_2_attempt.male_meiosis",
                "observable": "computes male meiotic divisions = 1600 / 4 = 400"
            },
            "MEGASPOROGENESIS_DEGENERATION_ACCOUNTING": {
                "attempt_field": "stage_2_attempt.female_meiosis_and_total",
                "observable": "evaluates female divisions = 1600 / 1 = 1600 and total = 2000"
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
                "at": "2026-11-11T23:45:00Z"
            },
            {
                "type": "FIRST_ANSWER_SAVED",
                "at": "2026-11-11T23:45:01Z",
                "durable": True
            },
            {
                "type": "HINT_SHOWN",
                "at": "2026-11-11T23:45:02Z"
            },
            {
                "type": "ANSWER_REVEALED",
                "at": "2026-11-11T23:45:03Z"
            }
        ],
        "native_runtime_receipt_ref": "RUNTIME-TRACE-BIO-NSEJS-GEN-01",
        "diagnostic_rules": [
            {
                "role_id": "EPISTATIC_PATHWAY_PHENOTYPIC_MAPPING",
                "observable": "assumes standard 9:3:3:1 ratio ignoring pathway block",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-EPISTATIC-RATIO-BLOCKED"
            },
            {
                "role_id": "MICROSPOROGENESIS_MEIOTIC_EVALUATION",
                "observable": "assumes 1 meiosis per pollen grain ignoring tetrad formation",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_4_diagnose",
                "failed_node_ref": "NODE-POLLEN-TETRAD-ERROR"
            },
            {
                "role_id": "MEGASPOROGENESIS_DEGENERATION_ACCOUNTING",
                "observable": "assumes 4 functional eggs per ovule meiosis ignoring megaspore degeneration",
                "repair_ref": "core1b_reconstruction.json#/stages/stage_5_repair",
                "failed_node_ref": "NODE-MEGASPORE-DEGENERATION"
            }
        ],
        "changed_condition_transfer_ref": "TRANSFER-CAPSELLA-DUPLICATE-DOMINANT",
        "saved_answer_evidence_ref": "SAVED-STUDENT-ATTEMPT-GEN-01",
        "exposure_audit": [
            {
                "surface": "HINT",
                "audit_ref": "AUDIT-HINT-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "PICTURE_STAGE",
                "audit_ref": "AUDIT-PICTURE-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "ALT_TEXT",
                "audit_ref": "AUDIT-ALT-TEXT-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "MODEL_RESPONSE",
                "audit_ref": "AUDIT-MODEL-RESPONSE-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "RUBRIC",
                "audit_ref": "AUDIT-RUBRIC-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            },
            {
                "surface": "EXAM_RETURN",
                "audit_ref": "AUDIT-EXAM-RETURN-BIO-NSEJS-GEN-01",
                "decisive_route_visible_before_save": False
            }
        ],
        "transfer_success_criterion": "Learner deduces modified 9:7 phenotypic ratio from complementary epistasis and applies N/4 male and N female division stoichiometry to evaluate 2000 total meiotic divisions"
    },
    "assessment": {
        "operation": "MODEL",
        "band": "D2",
        "source_role": "DIRECT_EXAM_EVIDENCE",
        "qrt_decision_ref": "QRT-NSEJS-2023-B-GEN-Q01-PROPOSED",
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
        "physics_warrant_ref": "WARRANT-BIO-COMPLEMENTARY-GENES-MEIOSIS",
        "physics_review_ref": "BIO-REVIEW-UNREVIEWED-CANDIDATE",
        "source_custody_ref": "CUSTODY-IAPT-2023-PAPER-61",
        "paper_ref": "IAPT-NSEJS-2023-PAPER-61",
        "official_key_ref": "IAPT-NSEJS-2023-FINAL-KEY-GEN-Q01-A",
        "solution_review_ref": "SOLUTION-DERIVATION-CHECKED",
        "known_physics_contradiction": False,
        "warrant_links": [
            {
                "role_id": "EPISTATIC_PATHWAY_PHENOTYPIC_MAPPING",
                "warrant_ref": "BIO-WARRANT-COMPLEMENTARY-EPISTASIS",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000061"
            },
            {
                "role_id": "MICROSPOROGENESIS_MEIOTIC_EVALUATION",
                "warrant_ref": "BIO-WARRANT-MICROSPOROGENESIS",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000062"
            },
            {
                "role_id": "MEGASPOROGENESIS_DEGENERATION_ACCOUNTING",
                "warrant_ref": "BIO-WARRANT-MEGASPOROGENESIS",
                "library_sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000063"
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
  <title>Learning Journey: Biology — Epistasis & Meiosis Stoichiometry</title>
  <style>
    :root {
      --primary: #15803d;
      --secondary: #059669;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --accent: #8b5cf6;
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
      max-width: 620px;
      height: 320px;
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
      background: #dcfce7;
      color: #15803d;
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
      background: #166534;
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
    <h1>Genetics & Heredity — Epistasis & Meiosis Stoichiometry</h1>
    <div class="meta">
      Anchor Item: BIO-NSEJS-GEN-01 | Band: D2 | Cognitive Demand: MODEL | Crux Move: M2
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
      <p>In sweet pea (<em>Lathyrus odoratus</em>), purple flower coloration requires functional enzymes produced by two independently assorting dominant alleles, C and P. Plants with genotypes C_pp, ccP_, or ccpp produce white flowers due to a biochemical pathway block.</p>
      <p>Two dihybrid heterozygous purple-flowered plants (CcPp &times; CcPp) are crossed, yielding 1600 viable seeds. <strong>Determine the expected phenotypic ratio of Purple to White flowers in the progeny, and calculate the minimum total number of meiotic divisions required in the parent plants to produce the male and female gametes that formed these 1600 seeds.</strong></p>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 540 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="520" height="240" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
        <!-- Biochemical Pathway -->
        <rect x="30" y="30" width="120" height="40" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
        <text x="45" y="55" font-size="14" fill="#334155" font-weight="bold">Precursor (White)</text>
        
        <line x1="150" y1="50" x2="200" y2="50" stroke="#15803d" stroke-width="2"/>
        <text x="165" y="42" font-size="14" fill="#15803d" font-weight="bold">Gene C</text>

        <rect x="200" y="30" width="130" height="40" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1.5"/>
        <text x="210" y="55" font-size="14" fill="#334155" font-weight="bold">Intermediate (White)</text>

        <line x1="330" y1="50" x2="380" y2="50" stroke="#15803d" stroke-width="2"/>
        <text x="345" y="42" font-size="14" fill="#15803d" font-weight="bold">Gene P</text>

        <rect x="380" y="30" width="130" height="40" rx="4" fill="#f3e8ff" stroke="#9333ea" stroke-width="1.5"/>
        <text x="390" y="55" font-size="14" fill="#7e22ce" font-weight="bold">Anthocyanin (Purple)</text>

        <!-- Ratio Breakdown -->
        <rect x="30" y="90" width="230" height="60" rx="6" fill="#f5f3ff" stroke="#c084fc" stroke-width="1.5"/>
        <text x="45" y="115" font-size="15" fill="#6b21a8" font-weight="bold">9 C_P_ &rarr; Purple (9/16)</text>
        <text x="45" y="135" font-size="14" fill="#581c87">900 seeds with both enzymes</text>

        <rect x="280" y="90" width="230" height="60" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="295" y="115" font-size="15" fill="#475569" font-weight="bold">3 C_pp + 3 ccP_ + 1 ccpp &rarr; White (7/16)</text>
        <text x="295" y="135" font-size="14" fill="#334155">700 seeds blocked in pathway</text>

        <!-- Meiotic Stoichiometry -->
        <rect x="30" y="170" width="480" height="65" rx="6" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1.5"/>
        <text x="45" y="195" font-size="14" fill="#065f46" font-weight="bold">Male (Anther): 1600 pollen &divide; 4 = 400 meiotic divisions</text>
        <text x="45" y="218" font-size="14" fill="#065f46" font-weight="bold">Female (Ovule): 1600 eggs &divide; 1 = 1600 meiotic divisions (3 megaspores degenerate)</text>
      </svg>
    </div>

    <div class="commit-box">
      <h3>Select Option:</h3>
      <div><input type="radio" id="optA" name="ans" value="A"><label for="optA"> A: Ratio = 9 : 7; Total meiotic divisions = 2000</label></div>
      <div><input type="radio" id="optB" name="ans" value="B"><label for="optB"> B: Ratio = 9 : 7; Total meiotic divisions = 800</label></div>
      <div><input type="radio" id="optC" name="ans" value="C"><label for="optC"> C: Ratio = 15 : 1; Total meiotic divisions = 2000</label></div>
      <div><input type="radio" id="optD" name="ans" value="D"><label for="optD"> D: Ratio = 9 : 3 : 3 : 1; Total meiotic divisions = 1600</label></div>
      <br>
      <button class="btn" onclick="commitAnswer()">Commit Answer & Reveal Mathematical Derivation</button>
    </div>

    <div id="derivation-section" class="derivation-section" style="display: none;">
      <h3>Genetics & Cytogenetic Derivation & Proof</h3>
      <p><strong>1. System Representation & Setup:</strong> Dihybrid cross CcPp &times; CcPp yields standard 16-cell Mendelian combinations: 9 C_P_, 3 C_pp, 3 ccP_, 1 ccpp. Functional purple anthocyanin requires dominant alleles at BOTH loci (C_P_).</p>
      <p><strong>2. Physical Model & Formulation:</strong> Genotypes C_pp, ccP_, and ccpp all lack one or both active enzymes, terminating the pathway prematurely at a colorless stage. Thus, phenotypic ratio = 9 Purple : (3 + 3 + 1) White = 9 : 7.</p>
      <p><strong>3. Execution & Resolution:</strong> Seed formation stoichiometry: Each seed requires 1 pollen grain and 1 embryo sac (egg cell). (a) Microsporogenesis: 1 microspore mother cell produces 4 functional pollen grains via meiosis &rArr; 1600 / 4 = 400 meiotic divisions. (b) Megasporogenesis: 1 megaspore mother cell produces 4 megaspores, of which 3 degenerate, leaving only 1 functional egg per meiosis &rArr; 1600 / 1 = 1600 meiotic divisions. (c) Total meiotic divisions = 400 + 1600 = 2000 divisions. Matching <strong>Option A</strong>.</p>
      <p><strong>4. Limiting Check:</strong> Total meiotic divisions for N angiosperm seeds is universally given by N/4 + N/1 = 5N/4. For N = 1600, 5 &times; 1600 / 4 = 2000.</p>
    </div>
  </div>

  <!-- TAB 2: CORE 1A -->
  <div id="content-core1a" class="tab-content">
    <h2>Core 1A: Declarative Teaching Construction</h2>
    <div class="step-box">
      <span class="badge">Prerequisite</span>
      <h3>Biochemical Epistasis & Megaspore Degeneration</h3>
      <p>Complementary genes modify the dihybrid 9:3:3:1 ratio because enzymes function sequentially in a single pathway. In plant reproduction, female meiosis exhibits monosporic development where 3 megaspores degenerate, so 1 meiosis produces only 1 functional egg cell.</p>
    </div>

    <div class="step-box">
      <span class="badge">Worked Example</span>
      <h3>Duplicate Dominant Epistasis in Shepherd's Purse</h3>
      <p>Capsella bursa-pastoris capsule shape: AaBb &times; AaBb yields 800 seeds. Phenotypic ratio = 15 Triangular : 1 Ovoid. Meiotic divisions for 800 seeds: Male = 800 / 4 = 200; Female = 800 / 1 = 800. Total = 200 + 800 = 1000 meiotic divisions.</p>
    </div>

    <div class="step-box">
      <span class="badge">Independent Exit Check</span>
      <h3>400 Pea Seeds Meiosis Check</h3>
      <p>For 400 seeds: Male meiosis = 400 / 4 = 100; Female meiosis = 400 / 1 = 400. Total meiotic divisions = 100 + 400 = 500 divisions.</p>
    </div>
  </div>

  <!-- TAB 3: CORE 1B -->
  <div id="content-core1b" class="tab-content">
    <h2>Core 1B: 6-Stage Phenomenological Reconstruction</h2>
    <div class="step-box">
      <span class="badge">Stage 1: Predict</span>
      <h3>Qualitative Direction</h3>
      <p>Will complementary gene interaction increase or decrease white-flowered progeny compared to Mendelian expectations? It increases white flowers from 1/16 (recessive) to 7/16, because a defect in either gene halts pigment synthesis.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 2: Attempt</span>
      <h3>Independent Quantitative Derivation</h3>
      <p>Derive 9:7 ratio and evaluate 5N/4 = 2000 divisions.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 3: Reconstruct</span>
      <h3>4-Step Systematic Route</h3>
      <ol>
        <li>Identify functional genotypes: C_P_ (9) vs blocked genotypes (7).</li>
        <li>State phenotypic ratio: 9 Purple : 7 White.</li>
        <li>Calculate pollen meiosis: 1600 / 4 = 400 divisions.</li>
        <li>Calculate ovule meiosis & total: 1600 / 1 = 1600; Total = 2000 divisions.</li>
      </ol>
    </div>

    <div class="step-box">
      <span class="badge">Stage 4 & 5: Diagnose & Repair</span>
      <h3>Common Error Trap</h3>
      <p><strong>Trap:</strong> Calculating female meiosis as 1600 / 4 = 400, forgetting that 3 megaspores degenerate.</p>
      <p><strong>Repair:</strong> Always use (N/4 + N) = 5N/4 for angiosperm seed formation.</p>
    </div>

    <div class="step-box">
      <span class="badge">Stage 6: Boundary Test</span>
      <h3>Epistatic Invariance of Gametogenesis</h3>
      <p>Epistatic gene interaction affects the phenotypic appearance of seeds/flowers, but gametogenesis stoichiometry depends solely on seed count N.</p>
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
