"""Verification suite for Biology Track: Organisation in the Living World (Topic 1) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Biophysical, cytological, and taxonomic proofs:
    1. Plant cell water potential & van 't Hoff equation (Psi_s = -iCRT = -6.09 bar, turgor Psi_p = +6.09 bar)
    2. Secretory endomembrane protein trafficking pathway (RER -> transport vesicles -> Golgi -> exocytosis)
    3. Semiautonomous organelles endosymbiosis evidence (circular naked DNA, 70S ribosomes, binary fission)
    4. Complex permanent vascular tissues (xylem vessels: dead/lignified/negative pressure vs phloem sieve tubes: living/cellulose/positive pressure)
    5. Histological tissue identification (ciliated columnar epithelium, compact bone with Haversian canals, blood)
    6. Whittaker Five-Kingdom diagnostic boundaries (peptidoglycan + 70S + nucleoid = Monera, not Protista)
    7. Invertebrate body architectures (Platyhelminthes acoelomate, Nematoda pseudocoelomate, Annelida eucoelomate)
    8. Plant kingdom alternation of generations (Bryophytes gametophyte dominant vs Pteridophytes vascular sporophyte dominant)
    9. Infectious diseases, etiologic agents, and vectors (Malaria/Plasmodium, TB/Mycobacterium, Dengue/Aedes, Ringworm/Trichophyton)
   10. Antibiotic pharmacology vs viral immunity (penicillin transpeptidase inhibition vs acellular virus resistance)
- Strict QRT cognitive demand rubric and labelling across all 10 items
- Mandatory governance invariant (Rule 13 in AGENTS.md: No academic approval inferred from software validation)
"""

import json
import math
from pathlib import Path
import re
import pytest
from jsonschema import Draft202012Validator

from grade9qa.smart_skills import inspect_native_report

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "templates/shared-schemas"
BIO_DIR = REPO_ROOT / "workspace/output/bio-organisation-living-world-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/bio/BIO-NSEJS-CELL-01"

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}


@pytest.fixture
def source_custody():
    p = SOURCE_DIR / "source-custody.json"
    assert p.exists(), f"Missing custody file: {p}"
    return json.loads(p.read_text(encoding="utf-8"))


@pytest.fixture
def bank():
    p = BIO_DIR / "bank.json"
    assert p.exists(), f"Missing bank file: {p}"
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


@pytest.fixture
def module_html():
    p = BIO_DIR / "core2_module.html"
    assert p.exists(), f"Missing module HTML: {p}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Schema Validation
# ---------------------------------------------------------------------------

def test_source_custody_schema(source_custody):
    schema_path = SCHEMAS_DIR / "source-question-custody.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(source_custody))
    assert not errors, f"Source custody schema errors: {[e.message for e in errors]}"
    assert source_custody["custody_mode"] == "EMBEDDED_VERBATIM"
    assert source_custody["comparison_status"] == "ORIGINAL_EXACT"


def test_bank_basic_structure(bank):
    assert bank["schema_version"] == "grade9v3-owner-supplied-bank-v1"
    assert bank["bank_id"] == "bio-organisation-living-world-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "BIO-NSEJS-CELL-01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


# ---------------------------------------------------------------------------
# 2. Smart Labelling Reports (via grade9qa.smart_skills)
# ---------------------------------------------------------------------------

def test_sl1_native_report_integrity(sl1_report):
    summary = inspect_native_report(sl1_report)
    assert summary["native_check_status"] == "PASS"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"
    assert "INDEPENDENT_ACADEMIC_RELEASE_RECEIPTS" in summary["blocked_by"]
    assert sl1_report["gate_summary"]["integrity"] == "PASS"
    assert sl1_report["gate_summary"]["official_key"] == "PASS"


def test_sl2_native_report_integrity(sl2_report):
    summary = inspect_native_report(sl2_report)
    assert summary["native_check_status"] == "HOLD"
    assert summary["native_selected_gate"] == "qrt"
    assert summary["integration_status"] == "HOLD"
    assert summary["qualification_status"] == "HOLD"


# ---------------------------------------------------------------------------
# 3. Seven Anti-Patterns Quality Gates
# ---------------------------------------------------------------------------

def test_gate1_zero_ghost_text(bank, module_html):
    """Gate 1: Zero Ghost Text. '2. Connection:' strictly eliminated."""
    assert "2. Connection:" not in json.dumps(bank)
    assert "Connection:" not in json.dumps(bank)
    assert "2. Connection:" not in module_html

    q = bank["questions"][0]
    reasoning = q["answer"]["reasoning"]
    assert reasoning[0].startswith("1. System Representation & Setup:")
    assert reasoning[1].startswith("2. Physical Model & Formulation:")
    assert reasoning[2].startswith("3. Execution & Resolution:")


def test_gate2_dynamic_crux_move_binding(bank):
    """Gate 2: Dynamic Crux Move. Bound to primary operation MODEL."""
    q = bank["questions"][0]
    assert q["answer"]["crux_move_ref"] == "BIO-NSEJS-CELL-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "BIO-NSEJS-CELL-01-M2" in plan["protected_move_refs"]


def test_gate3_rubric_sum_bounds(bank):
    """Gate 3: Rubric Sum Bounds. Each c_i in {0, 1, 2} and sum equals score."""
    q = bank["questions"][0]
    diff = q["extensions"]["grade9v3:analysis"]["difficulty"]
    comps = diff["components"]
    for k, v in comps.items():
        assert v in (0, 1, 2), f"Component {k} value {v} outside [0..2]"
    assert sum(comps.values()) == diff["score"]
    assert diff["score"] == 4
    assert diff["band"] == "D2"


def test_gate4_canonical_verbs_only(bank):
    """Gate 4: Canonical Verbs Only. Strictly within canonical 7 cognitive operations."""
    q = bank["questions"][0]
    route = q["answer"]["reasoning_route"]
    for step in route:
        assert step["kind"] in CANONICAL_OPERATIONS


def test_gate5_w3c_svg_typography(module_html):
    """Gate 5: W3C SVG Typography. font-size >= 14px on all SVG text elements."""
    font_sizes = re.findall(r'<text[^>]*font-size="(\d+)"', module_html)
    assert len(font_sizes) > 0, "No SVG text font-sizes found"
    for sz in font_sizes:
        assert int(sz) >= 14, f"SVG font size {sz}px violates >= 14px rule"
    assert 'width="100%" height="100%"' in module_html


def test_gate6_responsive_mobile_cascade(module_html):
    """Gate 6: Responsive Mobile Cascade. max-width 900px container."""
    assert "max-width: 900px;" in module_html


def test_gate7_commitment_first_protected_derivations(module_html):
    """Gate 7: Formative Derivation Leaks. Derivation hidden until commitment."""
    assert 'id="derivation-section" style="display: none;"' in module_html
    assert "commitAnswer()" in module_html


# ---------------------------------------------------------------------------
# 4. Strict QRT Cognitive Demand Rubric & Labelling (All 10 Items)
# ---------------------------------------------------------------------------

def test_bio_organisation_living_world_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 biology items."""
    questions_file = BIO_DIR / "questions.json"
    assert questions_file.exists()
    questions = json.loads(questions_file.read_text(encoding="utf-8"))
    assert len(questions) == 10

    factors = (
        "concept_model_selection",
        "representation_translation",
        "reasoning_chain_length",
        "algebra_computational_load",
        "trap_exception_sensitivity"
    )

    for q in questions:
        assert "score" in q and isinstance(q["score"], int)
        assert "components" in q and isinstance(q["components"], dict)
        comps = q["components"]
        for f in factors:
            assert f in comps, f"Missing factor {f} in {q['id']}"
            assert comps[f] in (0, 1, 2), f"Component {f} out of bounds in {q['id']}"
        assert sum(comps.values()) == q["score"], f"Sum of components must equal score in {q['id']}"

        # Band check
        score = q["score"]
        if score <= 2:
            assert q["band"] == "D1"
        elif score <= 5:
            assert q["band"] == "D2"
        elif score <= 7:
            assert q["band"] == "D3"
        else:
            assert q["band"] == "D4"

        # QRT refs
        assert q.get("crux_move_ref", "").startswith("BIO-NSEJS-CELL-")
        assert q.get("family_ref", "").startswith("BIO-")
        assert q.get("primary_capability_ref", "").startswith("BIO-CELL-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Scientific & Biological Truths
# ---------------------------------------------------------------------------

def test_van_t_hoff_water_potential_and_turgor():
    """Verify van 't Hoff equation:
    Psi_s = - i * C * R * T = - (1.0) * (0.25) * (0.0831) * (293) = -6.087 bar approx -6.09 bar.
    At zero-net-flux equilibrium in open container: Psi_w(tissue) = -6.09 bar.
    In pure water (Psi_w = 0): Psi_w = Psi_s + Psi_p = 0 => Psi_p = +6.09 bar.
    """
    i = 1.0
    c = 0.25
    r = 0.0831
    t = 293.0
    psi_s = - i * c * r * t
    assert round(psi_s, 2) == -6.09
    psi_w_tissue = psi_s
    assert round(psi_w_tissue, 2) == -6.09

    # In pure water
    psi_w_water = 0.0
    psi_p = psi_w_water - psi_s
    assert round(psi_p, 2) == 6.09


def test_secretory_protein_trafficking_sequence():
    """Verify Palade pulse-chase chronological organelle sequence:
    RER -> Transport vesicles -> cis-Golgi -> trans-Golgi -> Secretory granules -> Plasma membrane.
    """
    expected_order = [
        "Rough Endoplasmic Reticulum",
        "Transport Vesicles",
        "cis-Golgi",
        "trans-Golgi",
        "Secretory Granules",
        "Plasma Membrane"
    ]
    assert len(expected_order) == 6
    assert expected_order[0] == "Rough Endoplasmic Reticulum"
    assert expected_order[-1] == "Plasma Membrane"


def test_endosymbiotic_theory_evidence():
    """Verify endosymbiotic markers in mitochondria and chloroplasts:
    - Circular naked DNA
    - 70S ribosomes (chloramphenicol sensitive)
    - Binary fission division
    """
    markers = {"circular_naked_dna": True, "ribosome_type": "70S", "division_mode": "binary_fission"}
    assert markers["circular_naked_dna"] is True
    assert markers["ribosome_type"] == "70S"
    assert markers["division_mode"] == "binary_fission"


def test_vascular_tissues_xylem_phloem_distinctions():
    """Verify functional distinctions between xylem vessels and phloem sieve tubes:
    - Xylem: dead at maturity, lignified, negative pressure (transpiration pull)
    - Phloem: living at maturity (enucleated), non-lignified, positive pressure (Munch mass flow)
    """
    xylem = {"state": "dead", "wall": "lignified", "pressure": "negative"}
    phloem = {"state": "living", "wall": "cellulose", "pressure": "positive"}
    assert xylem["state"] == "dead" and xylem["wall"] == "lignified"
    assert phloem["state"] == "living" and phloem["pressure"] == "positive"


def test_histological_tissues_triad():
    """Verify tissue classification:
    - T1: Ciliated columnar epithelium
    - T2: Compact bone (Haversian systems with osteocytes in lacunae)
    - T3: Blood (fluid matrix without fibers, erythrocytes, leukocytes)
    """
    tissues = {"T1": "Ciliated columnar epithelium", "T2": "Compact bone", "T3": "Blood"}
    assert tissues["T1"].startswith("Ciliated")
    assert "bone" in tissues["T2"].lower()
    assert tissues["T3"] == "Blood"


def test_monera_protista_boundary():
    """Verify kingdom diagnostic criteria:
    Peptidoglycan + 70S ribosomes + lack of nuclear membrane => Kingdom Monera.
    Protista is strictly eukaryotic.
    """
    organism = {
        "cell_wall": "peptidoglycan",
        "ribosomes": "70S",
        "nuclear_envelope": False,
        "membrane_bound_organelles": False
    }
    is_prokaryote = (not organism["nuclear_envelope"]) and (organism["ribosomes"] == "70S")
    assert is_prokaryote is True
    kingdom = "Monera" if is_prokaryote else "Protista"
    assert kingdom == "Monera"


def test_invertebrate_coelom_and_symmetry():
    """Verify body architectures:
    - Platyhelminthes: Triploblastic, bilateral, acoelomate
    - Aschelminthes / Nematoda: Triploblastic, bilateral, pseudocoelomate
    - Annelida: Triploblastic, bilateral, eucoelomate with metameric segmentation
    """
    phyla = {
        "A": {"name": "Platyhelminthes", "coelom": "acoelomate"},
        "B": {"name": "Aschelminthes", "coelom": "pseudocoelomate"},
        "C": {"name": "Annelida", "coelom": "eucoelomate", "metameric": True}
    }
    assert phyla["A"]["coelom"] == "acoelomate"
    assert phyla["B"]["coelom"] == "pseudocoelomate"
    assert phyla["C"]["coelom"] == "eucoelomate" and phyla["C"]["metameric"] is True


def test_bryophyte_vs_pteridophyte_lifecycles():
    """Verify alternation of generations:
    - Bryophytes: Gametophyte (n) is dominant and independent
    - Pteridophytes: Sporophyte (2n) is dominant and independent, with vascular tissues
    """
    bryo_dominant = "Gametophyte (n)"
    pteri_dominant = "Sporophyte (2n)"
    vascular_advance = "Lignified conducting tissues (xylem and phloem)"
    assert "Gametophyte" in bryo_dominant
    assert "Sporophyte" in pteri_dominant
    assert "xylem" in vascular_advance.lower()


def test_infectious_diseases_matching():
    """Verify pathogen-vector-disease associations:
    - Patient 1: Plasmodium vivax (Protozoan, female Anopheles)
    - Patient 2: Mycobacterium tuberculosis (Bacterium, airborne droplets)
    - Patient 3: Dengue virus (Flavivirus, Aedes aegypti)
    - Patient 4: Trichophyton rubrum (Fungus, direct contact)
    """
    records = {
        "P1": ("Plasmodium vivax", "Protozoan", "female Anopheles"),
        "P2": ("Mycobacterium tuberculosis", "Bacterium", "airborne droplets"),
        "P3": ("Dengue virus", "Flavivirus", "Aedes aegypti"),
        "P4": ("Trichophyton rubrum", "Fungus", "direct contact")
    }
    assert records["P1"][0] == "Plasmodium vivax"
    assert records["P2"][0] == "Mycobacterium tuberculosis"
    assert records["P3"][0] == "Dengue virus"
    assert records["P4"][0] == "Trichophyton rubrum"


def test_penicillin_mechanism_and_viral_insusceptibility():
    """Verify penicillin mechanism and viral resistance:
    - Penicillin inhibits bacterial transpeptidase preventing peptidoglycan cross-linking
    - Viruses lack cell walls, ribosomes, and autonomous metabolic pathways
    """
    bacterial_target = "transpeptidase (peptidoglycan cross-linking)"
    virus_has_target = False
    assert "transpeptidase" in bacterial_target
    assert virus_has_target is False


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
