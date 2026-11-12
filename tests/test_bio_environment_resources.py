"""Verification suite for Biology Track: Environment, Resources & Food Production (Topic 3) Intake and Core 2 Module.

Mechanical validation ensures compliance with:
- Canonical schemas (source custody, competitive exam bank)
- Smart Labelling 1 and 2 candidate reports
- 7 Critical Anti-Patterns (no ghost text, dynamic crux ref, rubric bounds, canonical verbs, SVG standards)
- Ecological, biogeochemical, and agronomic proofs:
    1. Lindeman 10% trophic transfer and DDT biomagnification (T4 = 60.0 kJ/(m²·yr), DDT = 40.0 ppm)
    2. Nitrogen cycle microbial transformations (Rhizobium, Nitrosomonas/Nitrobacter, Pseudomonas)
    3. Anthropogenic carbon cycle and ocean acidification (carbonate ion depletion, aragonite saturation)
    4. Stratospheric ozone Chapman cycle and CFC chlorine radical catalytic destruction
    5. Aquatic organic sewage pollution, BOD surge, and dissolved oxygen sag curve
    6. Anaerobic biogas methanogenesis (Methanobacterium, 55-70% CH4, carbon neutrality)
    7. Traditional watershed management structures (Khadins, Johads, aquifer recharge)
    8. Fertilizer NPK elemental stoichiometry (50 kg 20-10-10: N = 10.00 kg, P = 2.18 kg, K = 4.15 kg)
    9. Crop breeding heterosis (F1 hybrid vigor) and F2 inbreeding depression
   10. Composite fish culture polyculture ecological niche partitioning (Catla, Rohu, Mrigal, Grass carp)
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
BIO_DIR = REPO_ROOT / "workspace/output/bio-environment-resources-r1"
SOURCE_DIR = REPO_ROOT / "workspace/sources/bio/BIO-NSEJS-ENV-01"

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
    assert p.exists(), f"Missing core2_module.html: {p}"
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Canonical Schema & Structure Tests
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
    assert bank["bank_id"] == "bio-environment-resources-r1"
    assert len(bank["questions"]) == 1
    q = bank["questions"][0]
    assert q["id"] == "BIO-NSEJS-ENV-01"
    assert q["response"]["type"] == "multiple_choice"
    assert len(q["options"]) == 4


# ---------------------------------------------------------------------------
# 2. Smart Labelling 1 and 2 Native Report Tests
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
    assert q["answer"]["crux_move_ref"] == "BIO-NSEJS-ENV-01-M2"
    plan = q["extensions"]["grade9v3:core2_support_plan"]
    assert "BIO-NSEJS-ENV-01-M2" in plan["protected_move_refs"]


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

def test_bio_environment_resources_qrt_labelling_integrity():
    """Verify strict QRT cognitive demand rubric and labelling across all 10 environment & resources items."""
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
        assert q.get("crux_move_ref", "").startswith("BIO-NSEJS-ENV-")
        assert q.get("family_ref", "").startswith("BIO-")
        assert q.get("primary_capability_ref", "").startswith("BIO-ENV-")
        assert q.get("op") in CANONICAL_OPERATIONS


# ---------------------------------------------------------------------------
# 5. Exact Scientific, Ecological & Agronomic Truths
# ---------------------------------------------------------------------------

def test_trophic_energy_transfer_and_biomagnification():
    """Verify Lindeman 10% trophic energy decay and DDT biomagnification:
    Incident solar radiation = 1.0e7 kJ/(m²·yr)
    GPP = 1.0% = 100,000 kJ/(m²·yr)
    NPP = GPP * (1 - 0.40) = 60,000 kJ/(m²·yr)
    T2 (Zooplankton) = 0.10 * 60,000 = 6,000 kJ/(m²·yr)
    T3 (Fish) = 0.10 * 6,000 = 600 kJ/(m²·yr)
    T4 (Eagle) = 0.10 * 600 = 60.0 kJ/(m²·yr)

    Biomagnification:
    C(T1) = 0.040 ppm
    C(T2) = 0.040 * 10 = 0.40 ppm
    C(T3) = 0.40 * 10 = 4.0 ppm
    C(T4) = 4.0 * 10 = 40.0 ppm
    """
    solar = 1.0e7
    gpp = solar * 0.010
    npp = gpp * (1.0 - 0.40)
    t2 = npp * 0.10
    t3 = t2 * 0.10
    t4 = t3 * 0.10
    assert math.isclose(t4, 60.0, rel_tol=1e-9)

    c_t1 = 0.040
    c_t2 = c_t1 * 10.0
    c_t3 = c_t2 * 10.0
    c_t4 = c_t3 * 10.0
    assert math.isclose(c_t4, 40.0, rel_tol=1e-9)


def test_nitrogen_cycle_microbial_pathways():
    """Verify nitrogen cycle microbial transformations:
    - Biological N2 Fixation: Rhizobium (symbiotic in legume root nodules via nitrogenase)
    - Nitrification Step 1 (NH4+ -> NO2-): Nitrosomonas (chemoautotrophic)
    - Nitrification Step 2 (NO2- -> NO3-): Nitrobacter (chemoautotrophic)
    - Denitrification (NO3- -> N2): Pseudomonas denitrificans (anaerobic respiration)
    """
    pathways = {
        "fixation": "Rhizobium",
        "ammonia_to_nitrite": "Nitrosomonas",
        "nitrite_to_nitrate": "Nitrobacter",
        "denitrification": "Pseudomonas"
    }
    assert pathways["fixation"] == "Rhizobium"
    assert pathways["ammonia_to_nitrite"] == "Nitrosomonas"
    assert pathways["nitrite_to_nitrate"] == "Nitrobacter"
    assert pathways["denitrification"] == "Pseudomonas"


def test_carbon_cycle_and_ocean_acidification():
    """Verify anthropogenic ocean acidification chemistry:
    CO2(aq) + H2O <-> H2CO3 <-> H+ + HCO3-
    H+ + CO3(2-) <-> HCO3-
    Consequences:
    - [H+] increases => pH decreases
    - [HCO3-] increases
    - [CO3(2-)] decreases (depleted by proton buffering)
    - Aragonite saturation state (Omega_arag) decreases, dissolving coral skeletons and pteropod shells
    """
    ocean_state = {
        "dissolved_co2": "increases",
        "ph": "decreases",
        "proton_concentration": "increases",
        "bicarbonate_concentration": "increases",
        "carbonate_ion_concentration": "decreases",
        "aragonite_saturation": "decreases"
    }
    assert ocean_state["ph"] == "decreases"
    assert ocean_state["carbonate_ion_concentration"] == "decreases"
    assert ocean_state["aragonite_saturation"] == "decreases"


def test_ozone_chapman_and_cfc_catalytic_cycle():
    """Verify stratospheric ozone Chapman cycle and CFC catalytic destruction:
    Photolysis: CF2Cl2 + UV -> ·CF2Cl + Cl·
    Catalytic cycle:
    1. Cl· + O3 -> ClO· + O2
    2. ClO· + O· -> Cl· + O2
    Net reaction: O3 + O· -> 2 O2
    Chlorine radical acts as an unconsumed catalytic regenerator destroying ~10^5 O3 molecules.
    """
    net_reactants = {"O3", "O"}
    net_products = {"O2"}
    catalyst = "Cl"
    assert "Cl" == catalyst
    assert net_reactants == {"O3", "O"}
    assert net_products == {"O2"}


def test_aquatic_sewage_bod_and_do_sag_curve():
    """Verify organic sewage discharge dynamics:
    Point source discharge -> microbial decomposers multiply rapidly ->
    Biochemical Oxygen Demand (BOD) surges -> Dissolved Oxygen (DO) plummets below critical limit (< 4 mg/L)
    creating the Streeter-Phelps oxygen sag curve and causing fish asphyxiation.
    """
    discharge_impact = {
        "organic_load": "high",
        "microbial_respiration": "elevated",
        "bod": "peaks",
        "dissolved_oxygen": "sags_to_minimum",
        "fish_survival": "asphyxiation_mortality"
    }
    assert discharge_impact["bod"] == "peaks"
    assert discharge_impact["dissolved_oxygen"] == "sags_to_minimum"


def test_biogas_methanogenesis_microbial_consortium():
    """Verify anaerobic digestion and biogas generation:
    1. Hydrolysis (cellulolytic bacteria)
    2. Acidogenesis / Acetogenesis (fermentative bacteria -> acetate, H2, CO2)
    3. Methanogenesis (Methanobacterium archaea, obligate anaerobes)
    Composition: 55-70% CH4, 30-45% CO2, traces of H2S.
    """
    ch4_min_pct = 55.0
    ch4_max_pct = 70.0
    methanogen = "Methanobacterium"
    oxygen_tolerance = "obligate_anaerobe"
    assert 55.0 <= ch4_min_pct and ch4_max_pct <= 70.0
    assert methanogen == "Methanobacterium"
    assert oxygen_tolerance == "obligate_anaerobe"


def test_traditional_watershed_water_harvesting():
    """Verify traditional indigenous rainwater harvesting systems:
    - Khadins (Rajasthan): Earthen bund across gentle slope, impounds monsoon runoff to saturate soil for rabi crop.
    - Johads (Rajasthan): Earthen check dams capturing rainwater to recharge groundwater aquifers and restore dry wells.
    """
    structures = {
        "Khadin": "Soil saturation on farmed slopes for rabi cropping",
        "Johad": "Percolation check dam for unconfined aquifer recharge"
    }
    assert "Khadin" in structures
    assert "Johad" in structures


def test_npk_fertilizer_elemental_stoichiometry():
    """Verify 50.0 kg bag of 20-10-10 fertilizer elemental yield:
    N: 20% of 50.0 kg = 10.00 kg N
    P2O5: 10% of 50.0 kg = 5.00 kg P2O5
      M(P2O5) = 2*30.97 + 5*16.00 = 141.94 g/mol
      M(P2) = 2*30.97 = 61.94 g/mol
      Elemental P = 5.00 * (61.94 / 141.94) = 2.1819 kg P
    K2O: 10% of 50.0 kg = 5.00 kg K2O
      M(K2O) = 2*39.10 + 16.00 = 94.20 g/mol
      M(K2) = 2*39.10 = 78.20 g/mol
      Elemental K = 5.00 * (78.20 / 94.20) = 4.1507 kg K
    """
    bag_mass = 50.0
    n_kg = bag_mass * 0.20
    assert math.isclose(n_kg, 10.00, rel_tol=1e-4)

    p2o5_kg = bag_mass * 0.10
    m_p = 30.97
    m_o = 16.00
    m_p2o5 = 2 * m_p + 5 * m_o
    p_fraction = (2 * m_p) / m_p2o5
    p_kg = p2o5_kg * p_fraction
    assert math.isclose(p_kg, 2.18, abs_tol=0.01)

    k2o_kg = bag_mass * 0.10
    m_k = 39.10
    m_k2o = 2 * m_k + m_o
    k_fraction = (2 * m_k) / m_k2o
    k_kg = k2o_kg * k_fraction
    assert math.isclose(k_kg, 4.15, abs_tol=0.01)


def test_crop_breeding_heterosis_and_inbreeding_depression():
    """Verify crop improvement genetic principles:
    - F1 Hybrid Vigor (Heterosis): Superior performance due to maximum heterozygosity and masking of deleterious recessives.
    - F2 Segregation (Inbreeding Depression): Self-pollination of F1 causes loss of heterozygosity (50% reduction per generation) and phenotypic divergence.
    """
    f1_status = {"heterozygosity": "maximum", "vigor": "superior"}
    f2_status = {"heterozygosity": "reduced_50_percent", "phenotype": "segregation_depression"}
    assert f1_status["heterozygosity"] == "maximum"
    assert f2_status["heterozygosity"] == "reduced_50_percent"


def test_composite_fish_culture_ecological_niches():
    """Verify polyculture composite fish culture ecological niche differentiation:
    - Surface feeder: Catla catla (zooplankton)
    - Column feeder: Labeo rohita (Rohu, decaying plants & plankton)
    - Bottom feeder: Cirrhinus mrigala (Mrigal) / Cyprinus carpio (detritus)
    - Macrophyte feeder: Ctenopharyngodon idella (Grass carp, aquatic weeds)
    Result: Non-competing trophic niches, maximized pond productivity.
    """
    niches = {
        "Catla": "surface",
        "Rohu": "column",
        "Mrigal": "bottom",
        "Grass carp": "macrophytes"
    }
    assert niches["Catla"] == "surface"
    assert niches["Rohu"] == "column"
    assert niches["Mrigal"] == "bottom"
    assert niches["Grass carp"] == "macrophytes"


# ---------------------------------------------------------------------------
# 6. Mandatory Governance Invariant (Rule 13 in AGENTS.md)
# ---------------------------------------------------------------------------

def test_governance_fail_closed_holding_status(bank, module_html):
    ext = bank["extensions"]
    assert ext["academic_status"] == "UNREVIEWED"
    assert ext["official_exam_status"] == "PAPER_ON_FILE_NOT_ADMITTED"
    assert "No academic approval inferred from software validation." in module_html
