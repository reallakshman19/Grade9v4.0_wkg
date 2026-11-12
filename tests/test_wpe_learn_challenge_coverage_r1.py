"""WPE Learn Challenge coverage R1: exact source map and independent physics.

This is software and scientific author QA, not official exam authentication
or a claim that the 74 questions have independently admitted QRT routes.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics"/"wpe"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
MANIFEST=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/MANIFEST.review.json"
COVERAGE=ROOT/"architecture/qrt-blueprint-protocol/wpe-coverage-register.json"
ROUTES=WPE/"reasoning-paths.review.json"
MAP=WPE/"learning-coverage-r1.json"
READER=ROOT/"preview/question-status.html"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10),(a,b)

def inputs():
    return load(BANK),load(COVERAGE),load(MAP),load(ROUTES)

def test_exact_74_custody_and_reconciliation_distinguishes_fits():
    bank,source,map_,routes=inputs()
    assert map_["schema"]=="wpe-learner-coverage-r1/v1"
    assert map_["source_bank_git_blob"]==git_blob(BANK)
    assert map_["source_coverage_register_git_blob"]==git_blob(COVERAGE)
    assert map_["source_reasoning_manifest_git_blob"]==git_blob(ROUTES)
    assert len(bank["questions"])==len(map_["questions"])==len(source["questions"])==74
    ids=[q["source_id"] for q in bank["questions"]]
    assert ids==[q["source_id"] for q in map_["questions"]]
    assert len(set(ids))==74
    by_id={r["source_id"]:r for r in bank["questions"]}
    source_map={r["source_id"]:r for r in source["questions"]}
    cnt=Counter(x["fit"] for x in map_["questions"])
    assert cnt==Counter({"FOCUSED_NEW":8,"TARGETED_PRACTICE":18,"RELATED_BRIDGE":48})
    assert map_["counts"]["total"]==74
    assert map_["counts"]["focused_new"]==8
    assert map_["counts"]["targeted"]==18
    assert map_["counts"]["related"]==48
    assert map_["counts"]["missing"]==0
    assert map_["counts"]["wrapped_related"]==41
    expected_new={"EX-M97":"F01","EX-N39":"F02","WEP07-01":"F03"}
    for row in map_["questions"]:
        id_=row["source_id"]
        assert row["stem_sha256"]==by_id[id_]["stem_sha256"]==source_map[id_]["source_evidence"]["stem_sha256"]
        assert row["reader_proposal"]=={"op":by_id[id_]["op"],"band":by_id[id_]["band"]}
        assert row["academic_status"]=="PRACTICE_ONLY_NOT_ADMITTED"
        assert by_id[id_]["review_state"]==source_map[id_]["admission"]=="NOT_ADMITTED"
        assert row["student_goal"] and row["teaching_limit"]
        if id_ in expected_new:
            assert row["fit"]=="FOCUSED_NEW" and row["primary_lesson"]==expected_new[id_]
            assert row["route_mode"]=="FOCUSED_SOURCE"
        if row["primary_lesson"]:
            assert row["primary_lesson"] in {f"C{i:02}" for i in range(1,9)} | {f"E{i:02}" for i in range(1,6)} | {f"F{i:02}" for i in range(1,9)}
            assert row["lesson_href"] and "question="+id_ in row["lesson_href"]
            assert row["source_href"].endswith("question="+id_)
            if row["route_mode"]=="BRIDGED_RELATED":
                assert row["lesson_href"].startswith("study-bridge.html?question="+id_+"&lesson=")
            if row["fit"]=="RELATED_BRIDGE":
                assert len(row["teaching_limit"])>=25, "Related practice must identify the remaining physical step"
        else:
            assert row["fit"]=="MISSING_CONSTRUCTION" and row["lesson_href"] is None
    assert not any(q["fit"]=="MISSING_CONSTRUCTION" for q in map_["questions"])
    assert {r["id"] for r in routes["constructions"]}=={f"WPE-C{i:02}" for i in range(1,9)} | {f"WPE-E{i:02}" for i in range(1,6)}
    assert all(r["approved_core1a_url"] is None for r in routes["constructions"])

def test_old_question_bank_data_and_answer_protection_remain_intact():
    html=READER.read_text(encoding="utf-8")
    import re
    match=re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>',html,re.S)
    assert match
    assert json.loads(match.group(1))["questions"]==load(BANK)["questions"]
    assert "if(!s?.committed)return" in html
    assert "q.scaffolds?.length?q.scaffolds:q.hints" in html
    assert "q.hints.filter(h=>!/crux move/i.test(h.text||''))" in html
    assert "learnerCoverage=fetch('../physics/wpe/learning-coverage-r1.json')" in html
    assert "showInteractiveLessonLinks(q)" in html
    manifest=load(MANIFEST)
    reader=next(x for x in manifest["artifacts"] if x["path"]=="preview/question-status.html")
    assert reader["sha"]==git_blob(READER)
    assert reader["length"]==len(READER.read_bytes())

def test_three_new_physics_models_are_correct_even_where_source_key_is_contested():
    # F01: original physically distinct force definitions. From flight, v²=2gh.
    m,g,s,h=70,10,.5,1
    v=math.sqrt(2*g*h)
    fnet=m*g*h/s
    fapplied=fnet+m*g
    close(v,math.sqrt(20))
    close(fnet,1400)
    close(fapplied,2100)
    close(fnet*v,1400*math.sqrt(20))  # kinetic-energy rate
    close(fapplied*v,2100*math.sqrt(20)) # force-delivered power
    assert fapplied*v>fnet*v
    assert math.isclose(fapplied*v-fnet*v,m*g*v)
    assert not math.isclose(fapplied*v,fnet*v)
    # New guide: lift 2 kg through 1 m under 30 N.
    close(math.sqrt(2*(30-20)*1/2),math.sqrt(10))
    close(30*math.sqrt(10),94.868329805)
    close(10*math.sqrt(10),31.6227766017)
    # Fresh: 3 kg, 54 N over .8 m.
    vf=math.sqrt(2*(54-30)*.8/3)
    close(vf,math.sqrt(12.8))
    close(54*vf,54*math.sqrt(12.8))
    close((54-30)*vf,24*math.sqrt(12.8))
    close(vf**2/(2*g),.64)
    # Boundary: 42 N, same mass and stroke.
    vb=math.sqrt(2*(42-30)*.8/3)
    close(vb,math.sqrt(6.4))
    close(42*vb,42*math.sqrt(6.4))
    close(vb*vb/(2*g),.32)

def test_ex_m97_qualifies_real_muscle_power_interpretation():
    focused=(WPE/"focused-journeys.js").read_text(encoding="utf-8")
    mapped=load(WPE/"learning-coverage-r1.json")
    row=next(x for x in mapped["questions"] if x["source_id"]=="EX-M97")
    # COM pseudo-work rate should not be asserted as power delivered at a stationary shoe.
    assert "ground contact can be stationary" in focused
    assert "pseudo-work rate" in focused
    assert "body-segment motion" in row["source_science_note"]
    assert "actual internal muscular power" in row["source_science_note"]

def test_round_trip_incline_signed_ledger_and_downhill_condition():
    # Original EX-N39: speeds v0 and v0/2 at theta 30 deg.
    theta=math.pi/6
    r=.5
    mu=(1-r*r)/(1+r*r)*math.tan(theta)
    close(mu,math.sqrt(3)/5)
    close(mu,.34641016151377546)
    assert mu<math.tan(theta)
    for r_ in [0,.25,.5,.8,1]:
        expected=math.tan(theta)*(1-r_*r_)/(1+r_*r_)
        close(expected,math.tan(theta)*(1-r_*r_)/(1+r_*r_))
    # Fresh at sin=3/5 cos=4/5, K0=18 and return K=2.
    m,g,sin,cos=2,10,3/5,4/5
    mu=.6
    distance=18/(m*g*(sin+mu*cos))
    close(distance,5/6)
    uphill_gravity=m*g*sin*distance
    friction_per_leg=mu*m*g*cos*distance
    close(uphill_gravity,10)
    close(friction_per_leg,8)
    close(uphill_gravity-friction_per_leg,2)
    close(math.sqrt(2/18),1/3)
    assert mu<sin/cos
    # Boundary 45 deg, same mu and K0; speed ratio is 1/2.
    fraction=(1-mu)/(1+mu)
    close(fraction,.25)
    close(math.sqrt(fraction),.5)
    close(18*fraction,4.5)
    # Limits: zero friction -> equal speed; mu approaching tan theta -> no downhill acceleration.
    close((sin-0)/(sin+0),1)
    assert math.isclose(sin-(sin/cos)*cos,0,abs_tol=1e-12)

def test_force_switched_spring_equilibrium_and_signed_energy():
    # Original WEP07-01: initial -xi, force switches to +2kxi, far turn +5xi.
    k,xi=100,.1
    start=-xi;new_force=2*k*xi;eq=new_force/k;far=2*eq-start
    close(eq,2*xi);close(far,5*xi)
    potential=lambda x:.5*k*x*x-new_force*x
    close(potential(start),potential(far))
    # Guide exact numbers.
    close(potential(-.1),2.5)
    close(potential(.5),2.5)
    # New fresh: initial extension +.05, force flips to -12.
    k=80;start=.05;new_force=-12
    eq=new_force/k;other=2*eq-start
    close(eq,-.15);close(other,-.35)
    u=lambda x:.5*k*x*x-new_force*x
    close(u(start),.7);close(u(other),.7)
    assert other<0  # compression, not 'extension' accidentally
    # Zero-force boundary restores centre x=0 and symmetric +/- .05 turns.
    close(2*0-start,-.05)
    assert abs(-.05)<abs(other)

def test_unmapped_pendulum_and_coupling_do_not_teach_false_model_equivalence():
    rows=load(WPE/"learning-coverage-r1.json")["questions"]
    m={x["source_id"]:x for x in rows}
    p=m["EX-M106"]
    assert p["fit"]=="FOCUSED_NEW" and p["has_source_caution"]
    assert "turning point" in p["source_science_note"]
    assert "Mg" in p["source_science_note"]
    assert "holding" in p["teaching_limit"] or "static balance" in p["teaching_limit"]
    w=m["EX-N27"]
    assert w["fit"]=="FOCUSED_NEW" and w["has_source_caution"]
    assert "10%" in w["source_science_note"] and "brake" in w["source_science_note"]
    assert "two-body" in w["teaching_limit"]

def test_focus_layout_first_answer_guard_and_existing_13_preserved():
    source=(WPE/"focused-journeys.js").read_text(encoding="utf-8")
    html=(WPE/"focused-journeys.html").read_text(encoding="utf-8")
    tile=(WPE/"learn-challenge.html").read_text(encoding="utf-8")
    index=(WPE/"question-coverage.html").read_text(encoding="utf-8")
    bridge=(WPE/"study-bridge.html").read_text(encoding="utf-8")
    assert source.count("      hints:[")==3
    assert source.count("      worked:[")==3
    assert source.count("      boundaryFields:[")==3
    assert "s.first={answers:{...values}" in source
    assert "s.boundary={...values" in source
    assert 's.exposure="HELPED_BEFORE_FIRST_ATTEMPT"' in source
    assert "feedback(field,value)" in source
    assert "localStorage.setItem" in source and "localStorage.removeItem" in source
    assert "innerHTML" not in source
    assert '<script src="focused-journeys.js" defer></script>' in html
    assert 'href="extension-learning.css"' in html
    assert 'id="question-routes"' in tile
    assert 'src="learn-challenge-coverage.js" defer' in tile
    assert tile.count('<article class="lesson"')==5
    assert "question-coverage-r1.js" in index
    assert "<iframe" not in bridge.lower()
    assert "location.replace(target.href)" in bridge
    assert "row.primary_lesson!==lesson" in bridge
    for p in ["d3d4-self-tutor.html","d3d4-self-tutor.js","extension-learning.html","extension-learning.js"]:
        assert (WPE/p).is_file()
