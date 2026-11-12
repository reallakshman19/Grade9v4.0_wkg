"""WPE source-question ↔ reasoning-route preview: provenance and fail-closed gates."""
from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"physics/wpe/reasoning-paths.review.json"
ROUTE_HTML=ROOT/"physics/wpe/reasoning-paths.html"
BRIDGE=ROOT/"WPE_Source_to_Core1A_Concept/learning-bridge/P0_P1_CONSTRUCTION_BRIDGE.json"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
PILOT=ROOT/"WPE_Source_to_Core1A_Concept/evidence/RECEIVED_selection_21_places.json"
FOUNDATIONS=ROOT/"physics/wpe/learn-challenge-source-map.json"
GUIDED=ROOT/"physics/wpe/learn-challenge.html"
READER=ROOT/"preview/question-status.html"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()

def test_review_route_pinned_to_exact_author_sources():
    a=load(MANIFEST)
    assert a["schema"]=="wpe-reasoning-route-preview/v1"
    assert a["policy"]=="REVIEW_NAVIGATION_ONLY__NOT_CANONICAL_PREREQUISITE"
    assert a["source_git_blobs"]=={
      "bridge":git_blob(BRIDGE),"bank":git_blob(BANK),
      "pilot":git_blob(PILOT),"foundation_map":git_blob(FOUNDATIONS)}
    assert a["academic"]=={
      "native_core1a":"NOT_ACCEPTED","native_core1b":"NOT_ACCEPTED",
      "qrt":"NOT_RUN","owner":"PENDING","admitted":0}
    assert a["counts"]=={
      "primary_constructions":8,"proposed_extensions":5,
      "author_packs":13,"missing_author_packs":0,
      "qualified_learner_routes":0,"pilot_candidates":14,
      "reader_agreements":3,"reader_conflicts":8,"reader_absent":3}
    assert all("LEARNING_PACK.md" not in x for x in (MANIFEST.read_text(),ROUTE_HTML.read_text()))

def test_all_author_routes_are_proposals_not_native_prerequisites():
    a=load(MANIFEST)
    b=load(BRIDGE)
    assert len(a["constructions"])==13
    originals=[*b["constructions"],*b["extensions_backlog"]]
    ids={q["source_id"] for q in load(BANK)["questions"]}
    for row,src in zip(a["constructions"],originals):
        assert row["title"]==(src.get("title") or src["topic"])
        assert [x["id"] for x in row["proposed_source_ids"]]==(src.get("links") or src["ids"])
        assert all(x["reader_present"]==(x["id"] in ids) for x in row["proposed_source_ids"])
        assert row["approved_core1a_url"] is None
        assert row["approved_core1b_url"] is None
        assert row["acceptance"]=="AUTHOR_DRAFT_ONLY"
    assert sum(x["authored_pack_present"] for x in a["constructions"])==13
    assert all(x["authored_pack_present"] for x in a["constructions"])
    assert a["constructions"][-1]["id"]=="WPE-E05"
    assert a["constructions"][-1]["approved_core1a_url"] is None
    assert a["constructions"][-1]["approved_core1b_url"] is None
    assert all(q["review_state"]=="NOT_ADMITTED" for q in load(BANK)["questions"])
    assert not any("primary_capability_ref" in q for q in load(BANK)["questions"])

def test_pilot_conflicts_and_absence_not_converted_into_approved_links():
    a=load(MANIFEST)
    p=load(PILOT)
    original=[x for x in p["places"] if x["candidate_id"]]
    assert len(a["pilot"])==len(original)==14
    assert all(x["id"]==y["candidate_id"] and x["academic_state"]=="NOT_ADMITTED" for x,y in zip(a["pilot"],original))
    assert [x["id"] for x in a["pilot"] if not x["reader_present"]]==["EX-M81","EX-M44","EX-M60"]
    assert [x["comparison"] for x in a["pilot"]].count("CONFLICT_IN_READER")==8
    assert [x["comparison"] for x in a["pilot"]].count("AGREES_IN_READER")==3
    q57=next(x for x in a["pilot"] if x["id"]=="WEP07-03")
    assert q57["proposed_constructions"]==["WPE-E01"]
    assert q57["comparison"]=="CONFLICT_IN_READER"

def test_reader_exact_id_and_attempt_guard_without_source_rewrite():
    html=READER.read_text(encoding="utf-8")
    m=re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>',html,re.S)
    assert m
    assert json.loads(m.group(1))["questions"]==load(BANK)["questions"]
    assert "qs.find(q=>q.source_id===requestedQuestion)" in html
    assert "keepQuestionInUrl()" in html
    assert "Unknown question link" in html
    assert "reasoning-paths.html?question=" in html
    assert "if(!s?.committed)return" in html
    assert "No official-key grading is claimed" in html
    guided=GUIDED.read_text(encoding="utf-8")
    assert 'id="reasoning-route-return"' in guided
    assert "Return to " in guided
    assert guided.count('<article class="lesson"')==5

def test_provisional_route_does_not_expose_author_only_content():
    html=ROUTE_HTML.read_text(encoding="utf-8")
    assert '0 academically admitted' in html
    assert 'NOT_ACCEPTED' in html
    assert "No source-bound route" in html
    assert "innerHTML" not in html
    assert "LEARNING_PACK.md" not in html
    assert "response.json()" in html
    assert "approved_core1a_url!==null" in html
    assert "approved_core1b_url!==null" in html
