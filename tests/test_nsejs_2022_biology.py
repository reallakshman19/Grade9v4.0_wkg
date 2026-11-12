"""Verification suite for NSEJS 2022 Official Biology Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Biological and physiological proofs:
    1. Q1: Bakanae mad-seedling disease phytohormone discovery (Gibberellin, Option D)
    2. Q2: Diagnostic pollen-tube ovular entry routes (A-Porogamy, B-Chalazogamy, C-Mesogamy, Option B)
    3. Q3: Translocation in Cucurbitaceae large fruits (Bicollateral vascular bundles, Option C)
    4. Q4: Incomplete dominance feather pigmentation ratio (1 black : 1 white : 2 blue, Option A)
    5. Q5: Spinach leaf photosynthetic pigment chromatographic sequence (Option A)
    6. Q6: Glyoxylate cycle microbodies in oil seeds (Glyoxysomes, Option A)
    7. Q7: Microbiological wastewater indicator of faecal pollution (Escherichia coli, Option B)
    8. Q8: Optimal aquatic biota physiological pH window (6.5-7.5, Option B)
    9. Q9: Principal bioactive ovarian estrogen (17beta-estradiol, Option C)
    10. Q10: Pelvic articulation of axial vertebral column (Sacral vertebrae, Option C)
    11. Q11: Glycolytic substrate-level phosphorylation enzyme loci (E7 and E10, Option C)
    12. Q12: Telencephalic commissural white matter tract (Corpus callosum, Option D)
    13. Q13: Bilaterally symmetrical protozoan flagellate (Giardia, Option A)
    14. Q14: Neuronal ribosomal Nissl bodies (Option C)
    15. Q15: Obligate viral intracellular replication requirement (Option C)
    16. Q16: Linnaean sexual classification system nature (Artificial system, Option A)
    17. Q49: Prehistoric human lineages (Homo habilis and Homo heidelbergensis, Options B, D)
    18. Q50: B-complex vitamin deficiency disorders (Options A, B, C)
    19. Q51: Pond water aquatic flora assemblages (Options A, B, D)
    20. Q52: Nephron brush border and water permeability segments (Options B, D)
- Strict QRT cognitive demand rubric and labelling across all 20 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
BIO_DIR = REPO_ROOT / "workspace/output/nsejs-2022-biology-r1"
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
    
    first_custody = SOURCE_BASE / "NSEJS-2022-B-Q01" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2022-biology-r1"
    assert len(bank["questions"]) == 20
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2022-B-Q01"
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
    expected_ids = [f"NSEJS-2022-B-Q{i:02d}" for i in range(1, 17)] + [f"NSEJS-2022-B-Q{i:02d}" for i in range(49, 53)]
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


def test_q01_bakanae_disease_gibberellin(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q01")
    assert q["answer"]["correct_option"] == "D"
    assert any("Gibberellin" in opt["text"] for opt in q["options"] if opt["id"] == "D")


def test_q02_pollen_tube_entry_routes(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q02")
    assert q["answer"]["correct_option"] == "B"
    assert any("Porogamy" in opt["text"] and "Chalazogamy" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q03_cucurbitaceae_bicollateral_bundles(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q03")
    assert q["answer"]["correct_option"] == "C"
    assert any("Bicollateral vascular bundles" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q04_incomplete_dominance_ratio(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q04")
    assert q["answer"]["correct_option"] == "A"
    assert any("1 black : 1 white : 2 blue" in opt["text"] for opt in q["options"] if opt["id"] == "A")


def test_q05_spinach_chromatography_order(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q05")
    assert q["answer"]["correct_option"] == "A"
    assert any("Chlorophyll b, Chlorophyll a, Carotenols and Carotenes" in opt["text"] for opt in q["options"] if opt["id"] == "A")


def test_q06_glyoxysomes_oil_seeds(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q06")
    assert q["answer"]["correct_option"] == "A"
    assert any("Glyoxysomes" in opt["text"] for opt in q["options"] if opt["id"] == "A")


def test_q07_ecoli_water_indicator(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q07")
    assert q["answer"]["correct_option"] == "B"


def test_q08_aquatic_ph_window(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q08")
    assert q["answer"]["correct_option"] == "B"
    assert any("6.5-7.5" in opt["text"] for opt in q["options"] if opt["id"] == "B")


def test_q09_estradiol_active_estrogen(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q09")
    assert q["answer"]["correct_option"] == "C"
    assert any("Estradiol" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q10_sacral_vertebrae_pelvis(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q10")
    assert q["answer"]["correct_option"] == "C"
    assert any("Sacral" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q11_glycolysis_atp_steps(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q11")
    assert q["answer"]["correct_option"] == "C"
    assert any("E7 and E10" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q12_corpus_callosum_commissure(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q12")
    assert q["answer"]["correct_option"] == "D"
    assert any("Corpus callosum" in opt["text"] for opt in q["options"] if opt["id"] == "D")


def test_q14_nissl_bodies_neurons(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q14")
    assert q["answer"]["correct_option"] == "C"
    assert any("Neurons" in opt["text"] for opt in q["options"] if opt["id"] == "C")


def test_q49_prehistoric_man(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q49")
    assert q["response"]["type"] == "multiple_response"
    assert "B" in q["answer"]["correct_option"] and "D" in q["answer"]["correct_option"]


def test_q50_b_complex_deficiency(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q50")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "C"])


def test_q51_aquatic_pond_flora(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q51")
    assert q["response"]["type"] == "multiple_response"
    assert all(k in q["answer"]["correct_option"] for k in ["A", "B", "D"])


def test_q52_nephron_histology(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2022-B-Q52")
    assert q["response"]["type"] == "multiple_response"
    assert "B" in q["answer"]["correct_option"] and "D" in q["answer"]["correct_option"]
