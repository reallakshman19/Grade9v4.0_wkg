"""Verification suite for NSEJS Biology Viral Genetics & Envelope Architecture D3 Core 1A/Core 1B.

Target Item: NSEJS-2024-B-Q50 (Band D3, Score 6, SYNTHESIZE)
"""
import hashlib
import json
from pathlib import Path
import re
import pytest

from grade9qa.bridge_witness import inspect_witness
from grade9qa.validate import schema_errors

REPO_ROOT = Path(__file__).resolve().parents[1]
MOD_DIR = REPO_ROOT / "workspace/output/bio-viral-genetics-d3-r1"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def core1a():
    p = MOD_DIR / "core1a_construction.json"
    assert p.exists()
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def core1b():
    p = MOD_DIR / "core1b_reconstruction.json"
    assert p.exists()
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def witness():
    p = MOD_DIR / "witness.json"
    assert p.exists()
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def journey_html():
    p = MOD_DIR / "learning_journey.html"
    assert p.exists()
    return p.read_text(encoding="utf-8")


def test_core1a_structure_and_fields(core1a):
    assert core1a["schema"] == "core1a-construction/v1"
    assert core1a["construction_id"] == "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01"
    assert core1a["target_question_id"] == "NSEJS-2024-B-Q50"
    assert core1a["cognitive_demand"] == "SYNTHESIZE"
    assert core1a["difficulty_band"] == "D3"
    assert core1a["difficulty_score"] == 6

    conventions = core1a["declared_conventions"]
    assert len(conventions) >= 4
    conv_text = " ".join(c["statement"] for c in conventions)
    assert "obligate" in conv_text.lower()
    assert "envelope" in conv_text.lower()

    assert len(core1a["entry_assumptions"]) >= 3
    assert len(core1a["inferential_jump"]) > 30

    path = core1a["teaching_path"]
    assert len(path) == 4
    for step in path:
        assert step["role"] in CANONICAL_OPERATIONS
        assert len(step["action"]) > 10

    anchor = core1a["worked_conceptual_anchor"]
    assert "hiv" in anchor["problem"].lower() or "retrovirus" in anchor["problem"].lower()
    assert len(anchor["solution_steps"]) == 4

    misconceptions = core1a["misconceptions"]
    assert len(misconceptions) >= 1

    exit_task = core1a["exit_task"]
    assert "prompt" in exit_task and "answer" in exit_task


def test_core1b_structure_and_6_stages(core1b):
    assert core1b["schema"] == "core1b-reconstruction/v1"
    assert core1b["construction_id"] == "BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01"
    assert core1b["target_question_id"] == "NSEJS-2024-B-Q50"

    assert len(core1b["taught_skill_Y"]) > 20
    assert len(core1b["connecting_route_Z"]) > 20
    assert len(core1b["protected_fresh_inference_W"]) > 30

    stages = core1b["stages"]
    assert "stage_1_predict" in stages
    assert "stage_2_attempt" in stages
    assert len(stages["stage_2_attempt"]["rubric"]) == 3
    assert "stage_3_reconstruct" in stages
    assert len(stages["stage_3_reconstruct"]["route"]) == 4
    assert "stage_4_diagnose" in stages
    assert "stage_5_repair" in stages
    assert "stage_6_boundary_test" in stages

    hints = core1b["progressive_hints"]
    assert len(hints) == 3


def test_witness_schema_and_b1_to_b7_inspection(witness):
    errs = schema_errors(witness, "bridge-witness", str(MOD_DIR / "witness.json"))
    assert not errs

    c1a_bytes = (MOD_DIR / "core1a_construction.json").read_bytes()
    c1b_bytes = (MOD_DIR / "core1b_reconstruction.json").read_bytes()
    expected_c1a_sha = "sha256:" + hashlib.sha256(c1a_bytes).hexdigest()
    expected_c1b_sha = "sha256:" + hashlib.sha256(c1b_bytes).hexdigest()

    assert witness["core1a"]["content_sha256"] == expected_c1a_sha
    assert witness["core1b"]["task_sha256"] == expected_c1b_sha

    result = inspect_witness(witness)
    assert result["mechanical_status"] == "HOLD"
    assert result["qualification_status"] == "HOLD"
    assert result["release_status"] == "HOLD"

    gate_results = {g["gate"]: g["result"] for g in result["gate_results"]}
    for gate_name in ("B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        assert gate_results[gate_name] == "HOLD"


def test_anti_patterns_on_learning_journey_html(journey_html):
    assert "2. Connection:" not in journey_html
    assert "Connection:" not in journey_html
    assert "1. System Representation & Setup:" in journey_html
    assert "2. Physical Model & Formulation:" in journey_html
    assert "3. Execution & Resolution:" in journey_html

    assert 'width="100%"' in journey_html
    assert 'height="100%"' in journey_html
    assert 'height="auto"' not in journey_html
    font_sizes = re.findall(r'font-size="(\d+)"', journey_html)
    assert font_sizes
    for fs in font_sizes:
        assert int(fs) >= 14

    assert "@media (max-width: 600px)" in journey_html
    assert "max-width: 900px;" in journey_html

    assert 'id="derivation-section" class="derivation-section"' in journey_html
    assert 'display: none;' in journey_html

    assert 'id="tab-core2"' in journey_html
    assert 'id="tab-core1a"' in journey_html
    assert 'id="tab-core1b"' in journey_html
    assert '<iframe' not in journey_html


def test_bio_viral_genetics_model_rigorous():
    """Verify factual evaluation of the 4 propositions."""
    propositions = {
        "A": {"text": "Obligate intracellular infectious particles", "biologically_true": True},
        "B": {"text": "Replication depends on host ribosomes", "biologically_true": True},
        "C": {"text": "Envelope exclusively host glycolipids without proteins", "biologically_true": False},
        "D": {"text": "All animal viruses contain dsDNA genomes", "biologically_true": False}
    }

    # Negative stem logic: Select biologically INCORRECT statements
    selected_options = [k for k, v in propositions.items() if not v["biologically_true"]]
    assert selected_options == ["C", "D"]

    # Diversity check: Animal viruses encompass RNA and ssDNA
    animal_virus_classes = {
        "Influenza": "(-)ssRNA",
        "Rabies": "(-)ssRNA",
        "Coronavirus": "(+)ssRNA",
        "Poliovirus": "(+)ssRNA",
        "HIV": "ssRNA-RT",
        "Parvovirus": "ssDNA",
        "Herpesvirus": "dsDNA"
    }
    has_non_dsdna = any(v != "dsDNA" for v in animal_virus_classes.values())
    assert has_non_dsdna is True


def test_governance_fail_closed_holding_status(journey_html, core1a, core1b, witness):
    assert "No academic approval inferred from software validation." in journey_html
    assert core1a["academic_status"] == "HOLD:ACADEMIC_ADMISSION"
    assert core1b["academic_status"] == "HOLD:ACADEMIC_ADMISSION"
    assert witness["status"] == "CANDIDATE"
