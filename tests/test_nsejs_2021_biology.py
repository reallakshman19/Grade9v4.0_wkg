"""Verification suite for NSEJS 2021-22 Official Biology Paper (Paper Code 51).

Mechanical validation ensures compliance with:
- Canonical schemas (source question custody)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, responsive cascade)
- Biological and physiological proofs:
    1. Q1: Erythrocyte functions vs B-cell immunoglobulin synthesis (Option C)
    2. Q2: Limbless tetrapod evolution in Reptilia (snakes) and Amphibia (Gymnophiona / caecilians) (Option C)
    3. Q3: Dipteran single wing pair and halteres in housefly, fruit fly, mosquito (Option D)
    4. Q4: Single-stranded RNA chemical diagnosis via lack of thymine and alkaline 2'-OH cleavage (Option C)
    5. Q5: Hydrophytic aerenchyma buoyancy lacunae in water hyacinth (Eichhornia) petiole (Option B)
    6. Q6: Bryophyte non-vascular organization and flagellated antherozoid water dependence (Option D)
    7. Q7: Crassulacean Acid Metabolism (CAM) nocturnal carbon fixation in desert succulents (Option C)
    8. Q8: Chiropterophily floral syndrome adaptations for bat pollination (Option B)
    9. Q25: Virology misconceptions: cellularity, DNA vs RNA types, replication infidelity (Options A, C, D)
    10. Q26: Frontal lobe lesions: Broca's expressive dysphasia, anosmia, and gait apraxia (Options A, B, C)
    11. Q27: Dynamic cytoskeletal motility drivers: actin and alpha-tubulin (Options A, B)
- Strict QRT cognitive demand rubric and labelling across all 11 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
BIO_DIR = REPO_ROOT / "workspace/output/nsejs-2021-biology-r1"
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

    first_custody = SOURCE_BASE / "NSEJS-2021-B-Q01" / "source-custody.json"
    custody_data = json.loads(first_custody.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(custody_data))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert custody_data["custody_mode"] == "EMBEDDED_VERBATIM"
    assert custody_data["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "nsejs-2021-biology-r1"
    assert len(bank["questions"]) == 11
    q = bank["questions"][0]
    assert q["id"] == "NSEJS-2021-B-Q01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


def test_reports_and_invariants(sl1_report, sl2_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert sl2_report["disposition"] == "HOLD:ACADEMIC_ADMISSION"
    assert "No academic approval inferred from software validation" in sl2_report["rule13_invariant"]


def test_all_11_questions_present(bank):
    assert len(bank["questions"]) == 11
    q_ids = [q["id"] for q in bank["questions"]]
    expected_ids = [f"NSEJS-2021-B-Q{i:02d}" for i in range(1, 9)] + [f"NSEJS-2021-B-Q{i:02d}" for i in range(25, 28)]
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


def test_q01_erythrocyte_function(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q01")
    assert q["answer"]["correct_option"] == "C"
    assert "immunoglobulins" in q["answer"]["reasoning"][1].lower()


def test_q02_limbless_vertebrates(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q02")
    assert q["answer"]["correct_option"] == "C"
    assert "amphibia" in q["answer"]["reasoning"][1].lower()
    assert "reptilia" in q["answer"]["reasoning"][1].lower()


def test_q03_diptera_wings(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q03")
    assert q["answer"]["correct_option"] == "D"
    assert "halteres" in q["answer"]["reasoning"][1].lower()


def test_q04_ss_rna_features(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q04")
    assert q["answer"]["correct_option"] == "C"
    assert "uracil" in q["answer"]["reasoning"][1].lower()


def test_q05_aerenchyma_water_hyacinth(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q05")
    assert q["answer"]["correct_option"] == "B"
    assert "aerenchyma" in q["answer"]["reasoning"][1].lower()


def test_q06_bryophyte_features(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q06")
    assert q["answer"]["correct_option"] == "D"


def test_q07_cam_photosynthesis(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q07")
    assert q["answer"]["correct_option"] == "C"
    assert "crassulacean" in q["answer"]["reasoning"][1].lower()


def test_q08_chiropterophily_bats(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q08")
    assert q["answer"]["correct_option"] == "B"
    assert "bats" in q["answer"]["reasoning"][2].lower()


def test_q25_virology_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q25")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"]
    assert "C" in q["answer"]["correct_option"]
    assert "D" in q["answer"]["correct_option"]


def test_q26_frontal_lobe_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q26")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"]
    assert "B" in q["answer"]["correct_option"]
    assert "C" in q["answer"]["correct_option"]


def test_q27_cytoskeleton_motility_multiple_choice(bank):
    q = next(item for item in bank["questions"] if item["id"] == "NSEJS-2021-B-Q27")
    assert q["response"]["type"] == "multiple_response"
    assert "A" in q["answer"]["correct_option"]
    assert "B" in q["answer"]["correct_option"]
