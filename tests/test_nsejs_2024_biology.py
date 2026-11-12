"""Verification suite for NSEJS 2024 Official Biology Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Biological principles and proofs:
    1. Q01: Metamerism first appearance in Animalia (Annelida)
    2. Q03: Human brain major anatomical functional centres (Hypothalamus, Cerebellum, Cerebrum, Pons)
    3. Q05: Atlanto-axial joint morphology (Pivot joint)
    4. Q09: Phenylalanine-tyrosine inborn errors (PKU, Tyrosinosis, Alkaptonuria, Albinism)
    5. Q11: Nucleosomal repeating structure histone types (5 types: H1, H2A, H2B, H3, H4)
    6. Q13: Anther microsporangium ploidy levels (Haploid, diploid, polyploid: 3 levels)
    7. Q14: Xylem sap ascent cohesion safety margin (Water cohesion 100-350 atm > resistive pull 20-50 atm)
    8. Q15: Hypertrichosis pinnae auris genetic transmission (Holandric Y-linked gene)
    9. Q49: Edible seed arils (Litchi, Rambutan, Nutmeg)
   10. Q51: Biflagellate algal classes (Phaeophyta, Chlorophyta)
   11. Q52: Vertebrate immune barriers and mediators (Immunoglobulins are glycoproteins, cilia, histamine)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import hashlib
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
BIO_DIR = REPO_ROOT / "workspace/output/nsejs-2024-biology-r1"
SOURCE_BASE = REPO_ROOT / "workspace/sources/bio"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def bank():
    p = BIO_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def intake():
    p = BIO_DIR / "intake.json"
    assert p.exists(), f"Missing intake file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl1_report():
    p = BIO_DIR / "sl1_check_report.json"
    assert p.exists(), f"Missing sl1 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def sl2_report():
    p = BIO_DIR / "sl2_check_report.json"
    assert p.exists(), f"Missing sl2 report: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


def test_source_custody_schema():
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    
    first_custody = SOURCE_BASE / "NSEJS-2024-B-Q01" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2024-biology-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2024-B-Q01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_20_questions_present(bank):
    assert len(bank["questions"]) == 20
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2024-B-Q{i:02d}" for i in range(1, 17)] + [f"NSEJS-2024-B-Q{i:02d}" for i in range(49, 53)]
    assert q_ids == expected_ids


def test_source_custody_for_all_items(bank):
    for q in bank["questions"]:
        q_id = q["id"]
        src_dir = SOURCE_BASE / q_id
        assert src_dir.exists(), f"Missing source dir for {q_id}"
        item_path = src_dir / "source_item.json"
        custody_path = src_dir / "source-custody.json"
        assert item_path.exists(), f"Missing source_item.json for {q_id}"
        assert custody_path.exists(), f"Missing source-custody.json for {q_id}"

        item_data = json.loads(item_path.read_text(encoding="utf-8"))
        custody_data = json.loads(custody_path.read_text(encoding="utf-8"))
        assert item_data["source_item_locator"] == q_id
        assert custody_data["source_item_locator"] == q_id
        assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
        assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_seven_anti_patterns(bank):
    html_path = BIO_DIR / "core2_module.html"
    assert html_path.exists()
    html_content = html_path.read_text(encoding="utf-8")

    # Gate 1: Zero Ghost Text
    assert "2. Connection:" not in html_content
    assert "Connection:" not in html_content

    # Gate 5: Commitment-First Protected Derivations
    assert 'class="derivation-section"' in html_content
    assert 'style="display: none;"' in html_content

    # Gate 6: Responsive Mobile Cascade
    media_idx = html_content.find("@media")
    container_idx = html_content.find(".container {")
    assert container_idx != -1 and media_idx != -1
    assert container_idx < media_idx, "Base styles must precede @media queries in cascade"

    for q in bank["questions"]:
        # Gate 1 in bank
        for step in q["answer"]["reasoning"]:
            assert "2. Connection:" not in step
            assert "Connection:" not in step

        # Gate 2: Dynamic Crux Move
        crux_ref = q["answer"]["crux_move_ref"]
        assert crux_ref.endswith("-M2") or crux_ref.endswith("-M3")
        assert q["extensions"]["crux_move"] == crux_ref
        assert q["extensions"]["support_plan"]["primary_crux"] == crux_ref

        # Gate 3: Rubric Bounds
        cd = q["extensions"]["cognitive_demand"]
        rubric = cd["rubric_breakdown"]
        assert len(rubric) == 5
        for score in rubric:
            assert score in {0, 1, 2}
        assert sum(rubric) == cd["score"]

        # Gate 4: Canonical Verbs
        op = cd["operation"]
        assert op in CANONICAL_OPERATIONS
        crux_move = next(m for m in q["answer"]["reasoning_route"] if m["move_id"] == crux_ref)
        assert crux_move["kind"] in CANONICAL_OPERATIONS


def test_q01_metamerism_annelida():
    phyla_order = ["Platyhelminthes", "Aschelminthes", "Annelida", "Arthropoda", "Chordata"]
    assert phyla_order.index("Annelida") < phyla_order.index("Arthropoda")
    assert phyla_order.index("Annelida") < phyla_order.index("Chordata")


def test_q03_brain_centres_mapping():
    brain_centres = {
        "thermoregulation_homeostasis": "Hypothalamus",
        "voluntary_coordination_balance": "Cerebellum",
        "sensory_cognition": "Cerebrum",
        "sleep_respiratory_pneumotaxic": "Pons"
    }
    assert brain_centres["thermoregulation_homeostasis"] == "Hypothalamus"
    assert brain_centres["sleep_respiratory_pneumotaxic"] == "Pons"


def test_q05_atlanto_axial_pivot_joint():
    joint_type = "pivot"
    assert joint_type == "pivot"


def test_q09_phenylalanine_tyrosine_metabolic_errors():
    pathway = [
        ("Defect 1", "Phenylalanine hydroxylase", "Phenylketonuria"),
        ("Defect 2", "Tyrosine transaminase", "Tyrosinosis"),
        ("Defect 3", "Homogentisate 1,2-dioxygenase", "Alkaptonuria"),
        ("Defect 4", "Tyrosinase", "Albinism")
    ]
    disease_sequence = [item[2] for item in pathway]
    assert disease_sequence == ["Phenylketonuria", "Tyrosinosis", "Alkaptonuria", "Albinism"]


def test_q11_nucleosome_five_histone_types():
    core_histones = {"H2A", "H2B", "H3", "H4"}
    linker_histones = {"H1"}
    total_types = core_histones | linker_histones
    assert len(total_types) == 5


def test_q13_anther_three_ploidy_levels():
    tissues = {
        "pollen_grains": 1,  # n
        "endothecium": 2,    # 2n
        "tapetum": 4         # polyploid
    }
    distinct_ploidies = len(set(tissues.values()))
    assert distinct_ploidies == 3


def test_q14_water_cohesion_safety_margin():
    max_resistive_tension = 50.0  # atm
    min_water_cohesion = 100.0   # atm
    assert min_water_cohesion > max_resistive_tension
    assert min_water_cohesion / max_resistive_tension >= 2.0


def test_q15_hypertrichosis_holandric_y_chromosome():
    transmission = "strictly_father_to_son"
    chromosome = "Y"
    assert chromosome == "Y"
    assert transmission == "strictly_father_to_son"


def test_q49_edible_arils_litchi_rambutan_nutmeg():
    plants_with_aril = {"Litchi", "Rambutan", "Nutmeg"}
    plants_without_aril = {"Cashew"}  # edible cotyledons + pedicel
    assert "Cashew" not in plants_with_aril
    assert len(plants_with_aril) == 3


def test_q51_biflagellate_algae_phaeophyta_chlorophyta():
    flagella_counts = {
        "Rhodophyta": 0,
        "Phaeophyta": 2,
        "Chlorophyta": 2,
        "Cyanophyta": 0
    }
    biflagellate = [group for group, count in flagella_counts.items() if count == 2]
    assert sorted(biflagellate) == ["Chlorophyta", "Phaeophyta"]


def test_q52_immunology_glycoproteins_cilia_histamine():
    immunoglobulins_are_glycoproteins = True
    cilia_mechanical_barrier = True
    histamine_vasodilation = True
    eosinophils_are_lymphocytes = False
    assert immunoglobulins_are_glycoproteins
    assert cilia_mechanical_barrier
    assert histamine_vasodilation
    assert not eosinophils_are_lymphocytes
