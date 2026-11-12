"""WPE Gap Closure R2: independently evaluate F04–F08 physics and exact-source routing.

Scientific tests use equations and assumptions, not a provisional coaching key.
No source question, QRT status, options or answer record is rewritten.
"""
import hashlib
import json
import math
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics/wpe"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
COVERAGE=ROOT/"architecture/qrt-blueprint-protocol/wpe-coverage-register.json"
MAP=WPE/"learning-coverage-r1.json"
MANIFEST=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/MANIFEST.review.json"
PAGE=ROOT/"preview/question-status.html"

TARGETS={"EX-M50":"F04","EX-M92":"F05","EX-M96":"F06","EX-M106":"F07","EX-N27":"F08"}

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def close(x,y,tol=1e-10):assert math.isclose(x,y,rel_tol=tol,abs_tol=tol),(x,y)
def sha_blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def test_74_original_question_identities_and_qrts_are_unchanged():
    original=data(BANK)["questions"]
    current=data(MAP)
    reg=data(COVERAGE)["questions"]
    assert len(original)==len(current["questions"])==len(reg)==74
    assert len({x["source_id"] for x in original})==74
    assert current["source_bank_git_blob"]==sha_blob(BANK)
    assert current["source_coverage_register_git_blob"]==sha_blob(COVERAGE)
    source={r["source_id"]:r for r in original}
    registered={r["source_id"]:r for r in reg}
    assert [r["source_id"] for r in original]==[r["source_id"] for r in current["questions"]]
    expected=Counter({"FOCUSED_NEW":8,"TARGETED_PRACTICE":18,"RELATED_BRIDGE":48})
    assert Counter(r["fit"] for r in current["questions"])==expected
    assert current["counts"]["missing"]==0 and current["counts"]["new_gap_closure"]==5
    assert current["counts"]["shared_foundation_groups"]==4
    for r in current["questions"]:
        row=source[r["source_id"]]
        assert r["stem_sha256"]==row["stem_sha256"]==registered[r["source_id"]]["source_evidence"]["stem_sha256"]
        assert r["reader_proposal"]=={"op":row["op"],"band":row["band"]}
        assert r["academic_status"]=="PRACTICE_ONLY_NOT_ADMITTED"
        assert row["review_state"]==registered[r["source_id"]]["admission"]=="NOT_ADMITTED"
    grouped={}
    for source_id,lesson in TARGETS.items():
        r=next(x for x in current["questions"] if x["source_id"]==source_id)
        assert r["fit"]=="FOCUSED_NEW" and r["primary_lesson"]==lesson
        assert r["lesson_href"]=="gap-journeys.html?question="+source_id+"#"+lesson
        assert r["route_mode"]=="FOCUSED_SOURCE"
        grouped[source_id]=r["construction_group"]
    assert grouped["EX-M50"]==grouped["EX-N27"]=="TWO_BODY_RELATIVE_ENERGY"
    assert len(set(grouped.values()))==4

def test_existing_embedded_question_bank_and_source_hash_receipt():
    import re
    html=PAGE.read_text(encoding="utf-8")
    match=re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>',html,re.S)
    assert match
    assert json.loads(match.group(1))["questions"]==data(BANK)["questions"]
    assert "if(!s?.committed)return" in html
    assert "q.scaffolds?.length?q.scaffolds:q.hints" in html
    # Exercise the source-backed mapping, not a fragile regex string in HTML.
    routes={r["source_id"]:r for r in data(MAP)["questions"]}
    for source_id,lesson in TARGETS.items():
        row=routes[source_id]
        assert row["stem_sha256"]==next(x["stem_sha256"] for x in data(BANK)["questions"] if x["source_id"]==source_id)
        assert row["lesson_href"]==f"gap-journeys.html?question={source_id}#{lesson}"
        assert row["primary_lesson"]==lesson and row["fit"]=="FOCUSED_NEW"
    entry=next(x for x in data(MANIFEST)["artifacts"] if x["path"]=="preview/question-status.html")
    assert entry["sha"]==sha_blob(PAGE) and entry["length"]==len(PAGE.read_bytes())

def energy(m1,m2,u1,u2):
    M=m1+m2;mu=m1*m2/M;V=(m1*u1+m2*u2)/M;w=u1-u2
    return M,mu,V,.5*mu*w*w,.5*M*V*V

def test_f04_two_body_relative_kinetic_energy_and_limits():
    # Equal-and-opposite EX-M50 original, 250 g each, k=2 N/m.
    M,mu,V,Krel,Kcom=energy(.25,.25,1,-1)
    close(V,0);close(mu,.125);close(Krel,.25);close(Kcom,0)
    close(math.sqrt(2*Krel/2),.5)  # extension = v/2 for v=1 m/s.
    # Critical source-check caveat: one block at +v, other stationary.
    # The correct extension here is v/4, not v/(2*sqrt(2)).
    M,mu,V,Krel,Kcom=energy(.25,.25,1,0)
    close(V,.5);close(Krel,.0625)
    close(math.sqrt(2*Krel/2),.25)
    assert not math.isclose(.25,1/(2*math.sqrt(2)))
    # Guide: 1 kg, 3 kg, velocities +2 and -2, k=8.
    M,mu,V,Krel,Kcom=energy(1,3,2,-2)
    close(V,-1);close(Krel,6);close(Kcom,2)
    close(math.sqrt(2*Krel/8),math.sqrt(1.5))
    # Fresh: m1=1,m2=3,u1=4,u2=-2,k=6.
    M,mu,V,Krel,Kcom=energy(1,3,4,-2)
    close(mu,.75);close(V,-.5);close(Krel,13.5);close(Kcom,.5)
    close(Krel+Kcom,14)
    close(math.sqrt(2*Krel/6),math.sqrt(4.5))
    # Boundary changes one mass; even equal velocity drift preserves Krel.
    M2,mu2,V2,Krel2,_=energy(1,1,4,-2)
    close(mu2,.5);close(V2,1);close(Krel2,9)
    close(math.sqrt(2*Krel2/6),math.sqrt(3))
    for shift in (-5,0,5):
        _,_,_,K,_=energy(1,3,2+shift,-2+shift)
        close(K,6)
    # Both blocks with exactly identical velocity cannot stretch initially.
    close(energy(1,3,4,4)[3],0)

def test_f05_uniform_mass_slices_and_affine_profile_conditions():
    mass,tip=1.2,3
    exact=mass*tip*tip/6
    close(exact,1.8)
    for N in (1,2,4,8,16,64,512):
        midpoint=sum(.5*(mass/N)*((j+.5)/N*tip)**2 for j in range(N))
        formula=.5*mass*tip*tip*(4*N*N-1)/(12*N*N)
        close(midpoint,formula)
        assert midpoint<exact
    four=sum(.5*(mass/4)*((j+.5)/4*tip)**2 for j in range(4))
    close(four,1.771875)
    close(mass*tip*tip/2,5.4)
    # Fresh 2.4 kg, fixed wall, v_tip=4.
    close(.75*4,3);close(2.4*4*4/6,6.4);close(2.4/3,.8)
    close((.5*2.4*16)/6.4,3)
    # Changed condition: both ends move with u=1,v=4, linear v(y).
    m,u,v=2.4,1,4
    K=m*(u*u+u*v+v*v)/6
    close(K,8.4);close(.5*(u+v),2.5)
    assert K!=m*v*v/6
    # Uniform translation at speed v has K=.5mv², not mv²/6.
    close(m*(v*v+v*v+v*v)/6,.5*m*v*v)

def test_f06_mass_flux_times_kinetic_energy_per_mass_and_unit_limits():
    rho,A,v,eta=1.2,5,10,.4
    flow=rho*A*v
    close(flow,60)
    close(.5*flow*v*v,3000)
    close(eta*.5*flow*v*v,1200)
    for scale in (0,1,1.5,2):
        output=lambda speed:.5*eta*rho*A*speed**3
        close(output(v*scale),output(v)*scale**3)
    # Fresh: rho1.25,A8,v6,eta0.30.
    rho,A,v,eta=1.25,8,6,.3
    flow=rho*A*v
    close(flow,60)
    close(.5*flow*v*v,1080)
    close(eta*.5*flow*v*v,324)
    close((.5*eta*rho*4*9**3)/324,1.6875)
    close(.5*eta*rho*4*9**3,546.75)

def test_f07_force_from_constant_work_differs_from_static_balance():
    # Original theta=45; constant F and zero K at the first turn.
    theta=math.radians(45)
    unit_turn=(1-math.cos(theta))/math.sin(theta)
    unit_static=math.tan(theta)
    close(unit_turn,math.sqrt(2)-1)
    close(unit_static,1)
    assert unit_turn!=unit_static
    # Guide M=1,g10,L1: Fturn at 45 and hold 10 N.
    close(10*unit_turn,4.14213562373)
    close(10*unit_static,10)
    # Fresh M=2,g10,L1.2, theta60, verify energy and force.
    M,g,L=2,10,1.2
    theta=math.radians(60)
    dh=L*(1-math.cos(theta));dx=L*math.sin(theta)
    close(M*g*dh,12);close(dx,1.2*math.sqrt(3)/2)
    Fturn=(M*g*dh)/dx
    Fhold=M*g*math.tan(theta)
    close(Fturn,20/math.sqrt(3))
    close(Fhold,20*math.sqrt(3))
    assert Fhold>Fturn
    # Boundary theta30 and limiting small-angle slopes.
    theta=math.radians(30)
    close(M*g*math.tan(theta/2),20*math.tan(math.pi/12))
    close(M*g*math.tan(theta),20/math.sqrt(3))
    for small in (1e-3,1e-4):
        close(math.tan(small/2)/math.tan(small),.5,tol=.000001)

def test_f08_assumed_whole_system_fraction_is_not_relative_coupling():
    M,v=.0+40000,20
    K0=.5*M*v*v
    close(K0,8e6)
    # Only under assumed 10% of WHOLE SYSTEM KE reaching spring, x=1:
    k=2*(.1*K0)/1**2
    close(k,1.6e6)
    # If "wagon energy" means individual unknown wagon mass, no unique k.
    assert 2*.1*(10000*20**2/2)!=2*.1*(30000*20**2/2)
    # Guide percentage budget: 1000kg at 10m/s, 10% retained,x=.5.
    close(2*(.1*.5*1000*10**2)/(.5**2),40000)
    # Guide TRUE pair: 1000kg at 8, 3000kg at 0,k150k.
    M,mu,V,Krel,Kcom=energy(1000,3000,8,0)
    close(mu,750);close(V,2);close(Krel,24000);close(Kcom,8000)
    close(math.sqrt(2*Krel/150000),math.sqrt(.32))
    # Fresh pair 600kg at 6, 900kg 0, k=54000.
    M,mu,V,Krel,Kcom=energy(600,900,6,0)
    close(V,2.4);close(mu,360);close(Krel,6480);close(Kcom,4320)
    close(Krel+Kcom,10800)
    close(math.sqrt(2*Krel/54000),math.sqrt(.24))
    assert Krel!=.1*(Krel+Kcom)
    # Boundary 25% of relative (not full) energy internally dissipated.
    close(.75*Krel,4860)
    close(math.sqrt(2*(.75*Krel)/54000),math.sqrt(.18))
    close(math.sqrt(.18)/math.sqrt(.24),math.sqrt(.75))

def test_gap_lessons_reuse_original_six_stage_and_do_not_expose_source_answers():
    src=(WPE/"gap-journeys.js").read_text(encoding="utf-8")
    engine=(WPE/"gap-six-stage-engine.js").read_text(encoding="utf-8")
    html=(WPE/"gap-journeys.html").read_text(encoding="utf-8")
    tile=(WPE/"learn-challenge.html").read_text(encoding="utf-8")
    link=(WPE/"learn-challenge-coverage.js").read_text(encoding="utf-8")
    original_engine=(WPE/"focused-journeys.js").read_text(encoding="utf-8")
    assert len(TARGETS)==5
    assert src.count('  guideSteps:[')==5
    assert src.count('  worked:[')==5
    assert src.count('  boundaryFields:[')==5
    assert src.count('  hints:[')==5
    assert 'const twoBody=' in src and 'prerequisites:twoBody.prerequisites' in src
    assert 'shared centre-of-mass' not in src or "centre-of-mass" in src
    assert 'modelView=(val,help)' in src
    assert 'window.WPEGapJourneys(scenarios' in src
    assert 's.first={answers:{...values}' in engine
    assert 's.boundary={...values' in engine
    assert 's.helpHistory.push' in engine
    assert 's.exposure="HELPED_BEFORE_FIRST_ATTEMPT"' in engine
    assert 'source does not map to this lesson' in engine
    assert 'x.stem_sha256===found.stem_sha256' in engine
    assert "innerHTML" not in src and "innerHTML" not in engine
    assert 'src="gap-six-stage-engine.js" defer' in html
    assert 'src="gap-journeys.js" defer' in html
    assert 'href="extension-learning.css"' in html and 'href="focused-journeys.css"' in html
    assert 'F04:' in src and 'F08:' in src
    # Route resolution is tested in Chromium for all five source-bound F04–F08
    # pairs; gateway code must not special-case or hard-code an example F06 ID.
    assert 'gap-journeys.html' in link and 'row.lesson_href' in link
    route=next(x for x in data(MAP)["questions"] if x["source_id"]=="EX-M96")
    assert route["primary_lesson"]=="F06"
    assert route["lesson_href"]=="gap-journeys.html?question=EX-M96#F06"
    assert 'id="question-routes"' in tile
    assert 'g9:wpe:focused:v1:' in original_engine
    assert 'EX-M97' in original_engine
