"""
Unit Test Suite for 12.7" Tablet Optimized NSEJS Pages
Verifies:
1. Removal of tile "Work, Power & Energy" from nsejs/physics/index.html
2. Topic tiles and Cores sub-tiles for Physics, Chemistry, Biology
3. Mandatory {Unvalidated} label on Core 2 question banks and questions
4. Rule 13 governance notices
"""

import pytest
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture
def physics_html():
    p = REPO_ROOT / "nsejs" / "physics" / "index.html"
    assert p.exists(), "Missing nsejs/physics/index.html"
    return p.read_text(encoding="utf-8")

@pytest.fixture
def chemistry_html():
    p = REPO_ROOT / "nsejs" / "chemistry" / "index.html"
    assert p.exists(), "Missing nsejs/chemistry/index.html"
    return p.read_text(encoding="utf-8")

@pytest.fixture
def biology_html():
    p = REPO_ROOT / "nsejs" / "biology" / "index.html"
    assert p.exists(), "Missing nsejs/biology/index.html"
    return p.read_text(encoding="utf-8")

@pytest.fixture
def hub_html():
    p = REPO_ROOT / "nsejs" / "index.html"
    assert p.exists(), "Missing nsejs/index.html"
    return p.read_text(encoding="utf-8")

def test_physics_wpe_tile_removed(physics_html):
    # Rule: remove tile "Work, Power & Energy"
    assert "Work, Power & Energy" not in physics_html
    assert "Work, Power &amp; Energy" not in physics_html
    assert "physics-wpe.html" not in physics_html

def test_physics_topics_and_cores(physics_html):
    # 6 Physics topics
    assert "Ray Optics" in physics_html
    assert "Mechanics &amp; Kinematics" in physics_html or "Mechanics & Kinematics" in physics_html
    assert "Current Electricity" in physics_html
    assert "Electrostatics" in physics_html
    assert "Magnetism" in physics_html
    assert "Fluid Mechanics" in physics_html

    # Cores present
    assert "Core 2" in physics_html
    assert "Core 1A" in physics_html
    assert "Core 1B" in physics_html

    # Mandatory {Unvalidated} labels
    assert "{Unvalidated}" in physics_html
    assert physics_html.count("{Unvalidated}") >= 6

def test_chemistry_topics_and_cores(chemistry_html):
    # Chemistry topics
    assert "Matter, States &amp; Mole Concept" in chemistry_html or "Matter, States & Mole Concept" in chemistry_html
    assert "Chemical Substances" in chemistry_html
    assert "Atomic Structure" in chemistry_html
    assert "Acids, Bases" in chemistry_html
    assert "Redox Reactions" in chemistry_html
    assert "Eudiometry" in chemistry_html

    # Cores and {Unvalidated}
    assert "Core 2" in chemistry_html
    assert "{Unvalidated}" in chemistry_html
    assert chemistry_html.count("{Unvalidated}") >= 6

def test_biology_topics_and_cores(biology_html):
    # Biology topics
    assert "Cell Biology" in biology_html
    assert "Life Processes" in biology_html
    assert "Control &amp; Endocrine" in biology_html or "Control & Endocrine" in biology_html
    assert "Reproduction &amp; Mendelian" in biology_html or "Reproduction & Mendelian" in biology_html
    assert "Ecology" in biology_html

    # Cores and {Unvalidated}
    assert "Core 2" in biology_html
    assert "{Unvalidated}" in biology_html
    assert biology_html.count("{Unvalidated}") >= 5

def test_rule13_governance_notice(physics_html, chemistry_html, biology_html, hub_html):
    for html in (physics_html, chemistry_html, biology_html, hub_html):
        assert "Rule 13 Invariant" in html
        assert "No academic approval inferred from software validation" in html
        assert "{Unvalidated}" in html

def test_tablet_12_7_constraints(physics_html, chemistry_html, biology_html):
    for html in (physics_html, chemistry_html, biology_html):
        assert "tablet-12-7.css" in html
        assert "topics-grid-12-7" in html
