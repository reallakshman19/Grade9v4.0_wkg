"""NSEJS-only Agent A tests. Uses the public candidate source already tracked in PR 80."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("nsejs_core2_audit",ROOT/"tools/nsejs_core2_audit.py")
audit=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=audit
spec.loader.exec_module(audit)
def questions():return audit.source_questions(audit.SOURCE.read_text(encoding="utf-8"))

def test_legacy_physics_census_and_qrt_nominations():
    q=questions();r=audit.summary(q)
    assert len(q)==50 and not audit.validate(q)
    assert r["producer_band_nominations"]=={"D1":10,"D2":32,"D3":8}
    assert r["topics"]["MECHANICS"]["D3_nominated"]==0
    assert sum(x["D4_nominated"] for x in r["topics"].values())==0
    assert r["authenticated_originals"]==0 and r["qrt_academic_release"]=="HOLD"

def test_source_namespace_resolves_repeated_original_id():
    q=questions()
    assert audit.summary(q)["repeated_display_ids"]==["NSEJS-2019-P-Q01","NSEJS-2019-P-Q02"]
    assert len({audit.uid(x) for x in q})==50

def test_stem_mutation_invalidates_full_revision():
    q=questions()[0].copy();rev=audit.revision(q);q["stem"]+=" alteration"
    assert audit.revision(q)!=rev

def test_option_and_answer_mutations_invalidate_full_revision():
    original=questions()[0];rev=audit.revision(original)
    assert audit.revision({**original,"options":list(reversed(original["options"]))})!=rev
    assert audit.revision({**original,"answer":"CHANGED"})!=rev

def test_figure_reference_mutation_invalidates_full_revision():
    q=questions()[0];assert audit.revision({**q,"source_figures":["changed.svg"]})!=audit.revision(q)

def test_duplicate_internal_uid_rejected():
    q=questions()[:2]
    assert "CANONICAL_UID_COLLISION" in audit.validate([q[0],{**q[1],"source_id":q[0]["source_id"]}])

def test_qrt_score_and_factor_mutations_rejected():
    q=questions()[0]
    assert any("QRT_FACTOR_SUM_MISMATCH" in x for x in audit.validate([{**q,"score":q["score"]+1}]))
    assert any("QRT_FACTOR_RANGE_INVALID" in x for x in audit.validate([{**q,"components":{**q["components"],"concept_model_selection":9}}]))

def test_existing_declared_stem_hashes_are_untrusted():
    q=questions()
    assert len(audit.stem_mismatches(q))>0
    assert audit.stem_mismatches([{**q[0],"stem":"tampered"}])==[q[0]["source_id"]]

def test_physics_reader_routes_and_separated_core1():
    page=(ROOT/"nsejs/physics/index.html").read_text(encoding="utf-8")
    runtime=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert (ROOT/"nsejs/physics/question-bank.html").is_file()
    assert 'window.location.href = "question-bank.html?topic="' in page
    assert not re.search(r'href="#[^"]+-core1[ab]"',page)
    assert 'crypto.subtle.digest' in runtime and "NOT_ADMITTED" in runtime

def test_required_figures_stay_not_received():
    r=audit.rows(questions())
    a=[x for x in r if x["figure_refs"]]
    assert len(a)==5 and all(x["figure_custody"]=="NOT_RECEIVED" for x in a)
    assert all(x["source_authenticity"]=="UNKNOWN_SOURCE" for x in r)


def test_nsejs_common_navigation_targets_exist():
    pages = [
        ROOT/"nsejs/index.html",ROOT/"nsejs/physics/index.html",
        ROOT/"nsejs/chemistry/index.html",ROOT/"nsejs/biology/index.html"
    ]
    for page in pages:
        html=page.read_text(encoding="utf-8")
        nav=re.search(r'<nav class="tabs"[^>]*>([\s\S]*?)</nav>',html)
        assert nav, page
        for href in re.findall(r'href="([^"]+)"',nav.group(1)):
            link=(page.parent/href).resolve()
            assert link.is_file(), (page,href)
        assert not re.search(r'href="#[^"]+-core1[ab]"',html),page


def test_unavailable_chemistry_biology_banks_are_not_false_clickable():
    for subject, count in (("chemistry",6),("biology",5)):
        html=(ROOT/"nsejs"/subject/"index.html").read_text(encoding="utf-8")
        assert html.count("Bank unavailable (source HOLD)") == count
        assert html.count('disabled title="No verified public source-backed question bank available"') == count
        assert "if (btn) btn.disabled = false;" not in html


def test_physics_hub_sample_does_not_claim_saved_first_attempt():
    html=(ROOT/"nsejs/physics/index.html").read_text(encoding="utf-8")
    assert "Source-indexed Physics candidate bank" in html
    assert 'class="q-item-card' not in html
    assert "if (btn) btn.disabled = false;" not in html
    assert 'window.location.href = "question-bank.html?topic="' in html


def test_original_authored_mechanics_topup_keeps_provenance_and_physics_correct():
    import json
    source=ROOT/"nsejs/data/physics-authored-practice-r1.json"
    manifest=json.loads(source.read_text(encoding="utf-8"))
    assert manifest["academic_release"]=="HOLD"
    assert manifest["source_claim"]=="AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert len(manifest["questions"])==1
    q=manifest["questions"][0]
    assert q["id"]=="G9-AUTH-MECH-001"
    assert q["category"]=="AUTHORED_PRACTICE"
    assert q["review_state"]=="NOT_ADMITTED"
    assert q["qrt_adjudication"]=="HOLD"
    assert q["science_review"]=="HOLD"
    assert q["score"]==sum(q["components"].values())==7
    v=8.0;mu=0.25;g=10.0
    post=v/2.0
    stopping=post**2/(2*mu*g)
    assert stopping==3.2
    assert q["answer"]=="C: 3.2 m"
    assert audit.uid(q) not in {audit.uid(x) for x in questions()}


def test_duplicate_hub_question_viewers_removed():
    for subject in ("physics","chemistry","biology"):
        html=(ROOT/"nsejs"/subject/"index.html").read_text(encoding="utf-8")
        assert 'class="q-item-card' not in html
        assert "function revealDerivation(" not in html
    assert (ROOT/"nsejs/physics/question-bank.html").is_file()


def test_qrt_d3_mislabels_are_reported_and_not_silently_reclassified():
    mismatches=audit.band_score_mismatches(questions())
    assert {(x["source_id"],x["rubric_score_band"]) for x in mismatches}=={
        ("NSEJS-19-OPT-02","D1"),
        ("NSEJS-FND-ELEC-04","D2"),
        ("NSEJS-FND-CIRC-01","D2"),
        ("NSEJS-FND-CIRC-02","D2"),
    }
    assert all(x["nominated_band"]=="D3" and x["adjudication"]=="HOLD" for x in mismatches)
    assert audit.summary(questions())["rubric_band_mismatch_count"]==4


def test_corpus_builder_is_reproducible_and_detects_source_mutations():
    import json
    import hashlib
    import importlib.util
    source=(ROOT/"nsejs/data/legacy-physics-candidate-source.html").read_bytes()
    corpus=json.loads((ROOT/"nsejs/data/physics-core2-candidates.v1.json").read_text(encoding="utf-8"))
    module_spec=importlib.util.spec_from_file_location("core2_candidate_builder",ROOT/"tools/build_nsejs_core2_corpus.py")
    builder=importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    compiled=builder.compile_corpus(source,corpus["known_paper_locator_corrections"])
    assert compiled==corpus
    assert builder.generated_bytes(compiled)==builder.generated_bytes(
        builder.compile_corpus(source,corpus["known_paper_locator_corrections"]))
    tampered=source.replace(b"An ant is sitting on the principal axis",b"An ant is jumping on the principal axis",1)
    assert builder.compile_corpus(tampered,corpus["known_paper_locator_corrections"])!=corpus


def test_five_official_locator_corrections_preserve_historical_ids():
    import json
    corpus=json.loads((ROOT/"nsejs/data/physics-core2-candidates.v1.json").read_text(encoding="utf-8"))
    corrections=corpus["known_paper_locator_corrections"]
    assert [(sid,corrections[sid]["official_question_no"],corrections[sid]["official_option"])
        for sid in ("NSEJS-23-OPT-01","NSEJS-24-ELEC-01","NSEJS-24-CIRC-01",
                    "NSEJS-24-MAG-01","NSEJS-24-MECH-01")]==[
        ("NSEJS-23-OPT-01",43,"B"),("NSEJS-24-ELEC-01",22,"A"),
        ("NSEJS-24-CIRC-01",42,"D"),("NSEJS-24-MAG-01",44,"D"),
        ("NSEJS-24-MECH-01",46,"B")]
    assert len(corpus["questions"])==50
    assert all(q["review_state"]=="NOT_ADMITTED" for q in corpus["questions"])
    assert all(x["evidence_status"]=="OFFICIAL_PAPER_LOCATOR_AND_KEY_CHECKED" for x in corrections.values())
