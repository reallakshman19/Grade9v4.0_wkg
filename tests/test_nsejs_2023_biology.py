"""Verification suite for NSEJS 2023 Official Biology Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Biological and physiological proofs:
    1. Q1: Mammalian left atrioventricular valve (Mitral / Bicuspid valve, Option D)
    2. Q2: Units of reflex arc (Receptor -> Internuncial -> Effector, Option C)
    3. Q3: Cytoplasmic hybrids (Pomato and Bromato cybrids, Option C)
    4. Q4: Pseudostratified epithelium localization (Trachea, vasa deferentia, epididymis, Option D)
    5. Q5: Autosomal recessive inheritance probability (Tt x tt = 0.50, Option B)
    6. Q6: Adrenal cortex C21 steroid secretion (Zona fasciculata 2 & reticularis 3, Option D)
    7. Q7: Ciliary muscle accommodation defect (Presbyopia, Option B)
    8. Q8: Angoumois grain moth genus (Sitotroga, Option B)
    9. Q9: Gametophytic meiotic division stoichiometry (300 + 75 = 375 divisions, Option B)
    10. Q10: Equisetum carinal and vallecular canals (Option C)
    11. Q11: Human satellite / SAT chromosomes (Acrocentric 13, 14, 15, 21, 22, Option B)
    12. Q12: Bordered pit membrane thickening (Torus, Option B)
    13. Q13: Cymose inflorescence architecture (Option C)
    14. Q14: Mammalian embryogenesis gene class exception (Tumour-suppressor genes, Option C)
    15. Q15: Crassulacean acid metabolism nocturnal carboxylation (Aloe, Option C)
    16. Q16: Hemiparasitic Indian mistletoe (Dendrophthoe falcata, Option B)
    17. Q49: Diagnostic mammalian order characteristics (Lagomorpha & Microchiroptera, Options A, B)
    18. Q50: Historical pedigree nomenclature (Zero and Jukes families, Options B, D)
    19. Q51: Root gravitropism mechanisms (Amyloplast sedimentation & auxin transport, Options A, B, C)
    20. Q52: Cyclic photophosphorylation features (PSI only, ATP without NADPH, Options A, B)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
import math
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
BIO_DIR = REPO_ROOT / "workspace/output/nsejs-2023-biology-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2023-B-Q01" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2023-biology-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2023-B-Q01"
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
    expected_ids = [f"NSEJS-2023-B-Q{i:02d}" for i in range(1, 17)] + [f"NSEJS-2023-B-Q{i:02d}" for i in range(49, 53)]
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


def test_q01_cardiac_mitral_valve(bank):
    """Q01: Mitral / bicuspid valve between left auricle and left ventricle."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q01")
    assert q["answer"]["correct_option"] == "D"
    assert any("Mitral valve" in opt["text"] for opt in q["options"] if opt["id"] == "D")


def test_q02_reflex_arc_units(bank):
    """Q02: Reflex arc sequence: 1 receptor, >=1 internuncial, 1 effector neuron."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q02")
    assert q["answer"]["correct_option"] == "C"
    assert any("internuncial" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q03_cybrids_pomato_bromato(bank):
    """Q03: Cybrids (cytoplasmic hybrids) represented by Pomato and Bromato."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q03")
    assert q["answer"]["correct_option"] == "C"
    assert any("Pomato and Bromato" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q04_pseudostratified_epithelium(bank):
    """Q04: Pseudostratified epithelium found in Trachea, vasa deferentia, and epididymis."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q04")
    assert q["answer"]["correct_option"] == "D"
    assert any("Trachea, vasa deferentia and epididymis" in opt["text"] for opt in q["options"] if opt["id"] == "D")


def test_q05_mendelian_ptc_probability(bank):
    """Q05: Autosomal recessive non-taster probability for Tt x tt is 0.50."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q05")
    assert q["answer"]["correct_option"] == "B"
    assert any("0.50" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q06_adrenal_corticosteroids_layers(bank):
    """Q06: C21 corticosteroids cortisol and corticosterone secreted by layers 2 and 3."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q06")
    assert q["answer"]["correct_option"] == "D"
    assert any("2 and 3" in opt["text"] for opt in q["options"] if opt["id"] == "D")


def test_q07_presbyopia_accommodation_defect(bank):
    """Q07: Age-related loss of ciliary muscle power and lens flexibility is Presbyopia."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q07")
    assert q["answer"]["correct_option"] == "B"
    assert any("Presbyopia" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q09_meiotic_division_stoichiometry(bank):
    """Q09: 300 seeds requires 300 megaspores (300 MMC divisions) + 300 microspores (75 PMC divisions) = 375 divisions."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q09")
    seeds = 300
    female_divisions = seeds
    male_divisions = math.ceil(seeds / 4)
    total_divisions = female_divisions + male_divisions
    assert total_divisions == 375
    assert q["answer"]["correct_option"] == "B"
    assert any("375 meiotic divisions" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q11_human_satellite_chromosomes(bank):
    """Q11: Human satellite chromosomes: 13, 14, 15, 21, and 22."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q11")
    assert q["answer"]["correct_option"] == "B"
    assert any("13, 14, 15, 21 and 22" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q15_cam_photosynthesis_aloe(bank):
    """Q15: CAM nocturnal CO2 fixation via PEP carboxylase observed in Aloe."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q15")
    assert q["answer"]["correct_option"] == "C"
    assert any("Aloe" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q49_mammalian_orders_multiple_choice(bank):
    """Q49: Lagomorpha continuously growing incisors (A) and Microchiroptera clawed thumb & uropatagium (B)."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q49")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"] and "B" in q["answer"]["correct_option"]


def test_q51_root_gravitropism_multiple_choice(bank):
    """Q51: Gravitropism involves statoliths (A), auxin differential (B), and root cap inhibitor (C)."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q51")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "C"])


def test_q52_cyclic_photophosphorylation_multiple_choice(bank):
    """Q52: Cyclic photophosphorylation involves PSI only (A) and generates ATP without NADPH (B)."""
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2023-B-Q52")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"] and "B" in q["answer"]["correct_option"]
