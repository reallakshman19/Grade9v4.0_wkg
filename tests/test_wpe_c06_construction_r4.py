"""WPE C06 R4 source-and-physics tests: independent equations and negative models.

No official exam key is authenticated by this test. Every question retains its
original 74-bank stem/option/key and RELATED_BRIDGE classification.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics/wpe"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
MAP=WPE/"learning-coverage-r1.json"
SOURCE_IDS=["EX-M18","EX-M39","EX-N31","EX-M36","EX-N11","EX-M6"]
QUALIFIED={"EX-M18":"C6S","EX-M39":"C6A","EX-N31":"C6H","EX-M36":"C6T","EX-N11":"C6W"}

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def approx(a,b,eps=1e-7):assert math.isclose(a,b,abs_tol=eps,rel_tol=eps),(a,b)
def blob(path):
    bits=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(bits)).encode()+b"\0"+bits).hexdigest()

def test_original_74_bank_and_related_only_source_status_are_unchanged():
    b=data(BANK);m=data(MAP)
    assert len(b["questions"])==len(m["questions"])==74
    assert m["source_bank_git_blob"]==blob(BANK)
    assert {q["source_id"] for q in b["questions"]}=={q["source_id"] for q in m["questions"]}
    original={q["source_id"]:q for q in b["questions"]}
    routes={q["source_id"]:q for q in m["questions"]}
    for source_id in SOURCE_IDS:
        old=original[source_id];cur=routes[source_id]
        assert old["stem_sha256"]==cur["stem_sha256"]
        assert cur["primary_lesson"]=="C06"
        assert cur["fit"]=="RELATED_BRIDGE"
        assert cur["academic_status"]=="PRACTICE_ONLY_NOT_ADMITTED"
        assert old["key_state"].startswith("HOLD")
        assert old["review_state"]=="NOT_ADMITTED"
        assert old["source_figures"] and old["figure_note"].startswith("Author-produced")
        assert old["stem"] and isinstance(old["options"],list)
    assert m["counts"]["total"]==74
    assert m["counts"]["focused_new"]==8 and m["counts"]["targeted"]==18
    assert m["counts"]["related"]==48 and m["counts"]["missing"]==0
    assert Counter(x["fit"] for x in m["questions"])=={
        "FOCUSED_NEW":8,"TARGETED_PRACTICE":18,"RELATED_BRIDGE":48
    }

def test_existing_c06_is_only_a_taut_string_prerequisite_not_a_coverage_certificate():
    s=(WPE/"d3d4-self-tutor.js").read_text(encoding="utf-8")
    assert 'title: "Stay on the circle?"' in s
    assert "T + mg = mv²/r" in s
    assert "negative tension" in s.lower()
    assert "v²/r" in s
    assert "T_B" not in s or "T + mg" in s
    js=(WPE/"c06-constructions-r4.js").read_text(encoding="utf-8")
    audit=(WPE/"reviews/WPE_C06_CONSTRUCTION_R4_AUDIT.md").read_text(encoding="utf-8")
    assert "EX-M6" in audit and "NO C6 CONTACT CONSTRUCTION/NO QUALIFICATION" in audit
    assert 'source:"EX-M6"' not in js
    for code in ("C6S","C6A","C6H","C6T","C6W"):
        assert "const "+code+"={" in js
        assert "const "+code+"={" in js
    assert "window.WPEGapJourneys(scenarios" in js
    assert "gap-six-stage-engine.js" in (WPE/"c06-constructions-r4.html").read_text(encoding="utf-8")
    assert "g9:wpe:c06-r4:v1:" in js
    assert "g9:wpe:gaps:v2:" not in js
    for hold in ("FIGURE MISMATCH HOLD","FIGURE + PHYSICS HOLD","RELATED_BRIDGE","B1","B2","B3","B4","B5","B6","B7"):
        assert hold in audit

def test_source_figure_mismatch_and_uncertain_provenance_are_not_hidden():
    bank={x["source_id"]:x for x in data(BANK)["questions"]}
    fig=(ROOT/"workspace/output/G9V4_LOTS/CORE2_BATCH_01/assets/fig_q09_bead_wire_spring.svg").read_text(encoding="utf-8")
    assert "Anchor O" in fig
    assert 'cy="50"' in fig
    assert "bottom of the hoop" in bank["EX-M18"]["stem"]
    assert "FIGURE CUSTODY HOLD" in " ".join(bank["EX-M6"]["flags"])
    assert "KEY/PHYSICS HOLD" in " ".join(bank["EX-M6"]["flags"])
    gate=(WPE/"c06-source-r4.js").read_text(encoding="utf-8")
    assert 'route.fit!=="RELATED_BRIDGE"' in gate
    assert 'route.academic_status!=="PRACTICE_ONLY_NOT_ADMITTED"' in gate
    assert 'original.stem_sha256!==route.stem_sha256' in gate
    assert 'route.primary_lesson!=="C06"' in gate
    assert "EX-M6" in (WPE/"c06-constructions-r4.html").read_text(encoding="utf-8")
    assert "EX-M6" not in gate.split("const mapping=")[1].split(";")[0]

def test_c6s_chord_energy_both_endpoints_contact_and_inaccessible_limit():
    g=10
    # Guided: 2kg R1, k10, side->theta120, natural R
    m,R,k,ell=2,1,10,1
    di=math.sqrt(2)*R;df=R
    gravity=m*g*R/2
    spring=.5*k*((di-ell)**2-(df-ell)**2)
    vg=math.sqrt(2*(gravity+spring)/m)
    approx(gravity,10)
    approx(spring,5*(math.sqrt(2)-1)**2)
    approx(vg,math.sqrt(10+5*(math.sqrt(2)-1)**2))
    # Task A: R2, m1, k8, theta60 -> theta120.
    m,R,k=1,2,8
    di=math.sqrt(3)*R;df=R
    U0=.5*k*(di-R)**2
    approx(U0,16*(math.sqrt(3)-1)**2)
    speed=math.sqrt(2*(m*g*R+U0)/m)
    approx(speed,math.sqrt(2*(20+16*(math.sqrt(3)-1)**2)))
    # New rest length 1.5R: both Ui AND Uf need to be computed.
    ell=1.5*R
    Ui=.5*k*(di-ell)**2;Uf=.5*k*(df-ell)**2
    vb=math.sqrt(2*(m*g*R+Ui-Uf)/m)
    approx(Uf,4)
    assert vb<speed and vb>0
    # Unfamiliar horizontal robot: left->top, right peg.
    energy=.5*20*(2-math.sqrt(2))**2
    approx(energy,10*(2-math.sqrt(2))**2)
    approx(math.sqrt(2*energy/2),math.sqrt(energy))
    assert energy<2*10*1 # vertical lift: robot cannot reach without more energy
    approx(20-energy,20-10*(2-math.sqrt(2))**2)
    # Rest spring force at zero gravity cannot appear from gravity.
    assert energy>0

def test_c6a_perpendicular_acceleration_and_false_zero_speed_model():
    g=10
    angle=math.pi/3
    aext=g*math.sin(angle)
    abot=2*g*(1-math.cos(angle))
    approx(aext,5*math.sqrt(3))
    approx(abot,10)
    # Task A 45 deg: extreme > bottom; L cancels at same release angle.
    a45ext=g*math.sin(math.pi/4)
    a45bot=2*g*(1-math.cos(math.pi/4))
    approx(a45ext,10/math.sqrt(2))
    approx(a45bot,20*(1-1/math.sqrt(2)))
    assert a45ext>a45bot>0
    for L in (.8,1.6,10):
        v2=2*g*L*(1-math.cos(math.pi/4))
        approx(v2/L,a45bot)
    # Task B: smooth roller at theta30, v4, radius2.
    ar=4**2/2;at=g*math.sin(math.pi/6)
    approx(ar,8);approx(at,5)
    approx(math.hypot(ar,at),math.sqrt(89))
    assert ar!=math.hypot(ar,at)
    assert ar+at!=math.hypot(ar,at)
    # Change R while v and theta same.
    approx(math.hypot(16,at),math.sqrt(281))
    approx(g*math.sin(0),0)

def test_c6h_exterior_dome_normal_sign_detachment_and_launch_limit():
    m,R,g=2,4,10
    u2=20
    Ntop=m*(g-u2/R)
    approx(Ntop,10)
    cos=(u2+2*g*R)/(3*g*R)
    approx(cos,5/6)
    height=R*cos
    approx(height,10/3)
    v2=u2+2*g*R*(1-cos)
    approx(m*g*cos-m*v2/R,0)
    assert v2>0
    # At u2=gR, Ntop=0 at crown; above it requires impossible N<0.
    approx(m*(g-g*R/R),0)
    assert m*(g-(1.1*g*R)/R)<0
    # B: start θ60 from rest; detachment at cosθ=2cosθ0/3.
    R=3
    cos0=.5
    det=2*cos0/3
    approx(det,1/3)
    approx(R*det,1)
    approx(2*10*R*(cos0-det),10)
    # Boundary start θ30 from rest
    approx(R*(2*math.cos(math.pi/6)/3),math.sqrt(3))
    # A captive groove could support a negative radial reaction; dome cannot.
    assert det<cos0

def test_c6t_taut_string_vs_captive_rail_and_velocity_threshold():
    L,g=1.5,10
    u=9
    top_v2=u*u-4*g*L
    approx(top_v2,21)
    approx(top_v2/L-g,4) # 1kg top T=4N
    approx(math.sqrt(5*g*L),math.sqrt(75))
    # A: m2 L2 u11
    m,L,u=2,2,11
    v2=u*u-4*g*L
    approx(v2,41)
    approx(m*(v2/L-g),21)
    assert u*u>5*g*L
    # Lower speed u=sqrt90 -> energy allows top but T is impossible.
    v2=90-4*g*L
    approx(v2,10)
    approx(m*(v2/L-g),-10)
    assert v2>0
    # B captive groove, m1 R2, u²=90: top guide outward/upwards 5N.
    R=2;v2=90-4*g*R
    approx(v2,10)
    inward=m*0+v2/R # m=1 for B
    approx(g-inward,5)
    approx(inward-g,-5) # hypothetical 1kg string T
    # Strict string threshold not inherited by a two-sided track.
    assert 4*g*R<90<5*g*R

def test_c6w_total_tube_work_vs_local_variable_drag():
    # Guide 2kg, top speed6, bottom rest, R.5, g10
    m,R,g,ui,uf=2,.5,10,6,0
    dK=.5*m*(uf**2-ui**2);Wg=m*g*2*R
    approx(dK,-36);approx(Wg,20);approx(dK-Wg,-56)
    # A: m.5 R1, top10 bottom2
    m,R,ui,uf=.5,1,10,2
    dK=.5*m*(uf**2-ui**2);Wg=m*g*2*R
    approx(dK,-24);approx(Wg,10);approx(dK-Wg,-34)
    # Same height: gravity zero for any number of loops
    for loops in (0,1,5,100):
        approx(m*g*(R-R),0)
        approx(-.5*m*10**2,-25)
    # B: measured f(s)=2+s newtons, s metres, 0..4.
    Wf=-(2*4+(.5*4**2))
    approx(Wf,-16)
    Ki=.5*1*8**2;Kf=Ki+Wf
    approx(Ki,32);approx(Kf,16)
    approx(math.sqrt(2*Kf),math.sqrt(32))
    # changed force law constant3 N, same distance.
    approx(-3*4,-12)
    approx(math.sqrt(2*(Ki-12)),math.sqrt(40))
    assert Wf != -2*4 # cannot freeze a variable measured drag at initial value

def arc_ratio(lambda_,N=12000):
    # R=g=1 and source P's horizontal component is v.
    # Midpoint quadrature avoids a nonintegrable false endpoint singularity.
    a,b=math.pi/4,math.pi
    step=(b-a)/N
    total=0
    for i in range(N):
        phi=a+(i+.5)*step
        val=2*lambda_+2*(math.sin(phi)-1/math.sqrt(2))
        if val<=0:return None
        total+=1/math.sqrt(val)
    return math.sqrt(lambda_)*step*total/2

def test_ex_m6_travel_time_negative_control_and_figure_hold():
    source=next(x for x in data(BANK)["questions"] if x["source_id"]=="EX-M6")
    assert "coaching" in source["answer"].lower()
    assert "not a verified universal" in source["answer"].lower()
    assert "FIGURE CUSTODY HOLD" in " ".join(source["flags"])
    assert "KEY/PHYSICS HOLD" in " ".join(source["flags"])
    # Assumed phiS=45 degrees; two admissible trajectories reverse ordering.
    threshold=1/math.sqrt(2)
    assert .708>threshold and 1>threshold
    slow=arc_ratio(.708)
    fast=arc_ratio(1.)
    assert slow is not None and fast is not None
    assert 1.008<slow<1.011,(slow,fast)
    assert .863<fast<.866,(slow,fast)
    assert slow>1 and fast<1
    assert arc_ratio(.70) is None
    # At gravity off, the ratio is 3pi/(8sqrt2), less than one.
    approx(3*math.pi/(8*math.sqrt(2)),.8330405509,eps=.000001)

def test_ten_independent_six_stage_tasks_and_no_automatic_admission():
    js=(WPE/"c06-constructions-r4.js").read_text(encoding="utf-8")
    html=(WPE/"c06-constructions-r4.html").read_text(encoding="utf-8")
    route=(WPE/"c06-source-r4.js").read_text(encoding="utf-8")
    engine=(WPE/"gap-six-stage-engine.js").read_text(encoding="utf-8")
    assert js.count("prediction:")>=10
    assert js.count("challenge:")>=10
    assert js.count("boundary:")>=10
    assert js.count("hints:[")>=10
    assert js.count("worked:[")>=10
    assert js.count("transfer:task({")==5
    assert "fields:[o.model,o.assumption,...o.numbers,reason(o.reason)]" in js
    assert "boundaryFields:[o.boundaryModel" in js
    assert 's.first={answers:{...values}' in engine
    assert 's.boundary={...values' in engine
    assert "variantOf[id]" in engine
    assert 'taskKey=id=>id+(variantOf[id]==="T2"?"-T2":"")' in engine
    assert 's.hints.push(idx)' in engine
    assert 's.first===null' in engine
    assert 's.stage===2' in engine and "Worked reconstruction" in engine
    assert "source=EX-M18#C6S" in html
    assert "source=EX-N11#C6W" in html
    assert "EX-M6" in html and "EX-M6" not in js.split("const scenarios=")[1].split(";")[0]
    assert 'new URLSearchParams(location.search).get("source")' in route
    assert "No return is inferred" in route
    assert "innerHTML" not in js and "innerHTML" not in route


def test_c6s_horizontal_robot_initial_equilibrium_and_perturbation_limit():
    """An exact-rest antipodal point has no tangential spring force.
    The positive-energy release is a perturbation limit, not spontaneous motion."""
    src=(WPE/"c06-constructions-r4.js").read_text(encoding="utf-8")
    for phrase in ("UNSTABLE equilibrium","vanishingly small tangential perturbation",
                   "no motion starts","limiting perturbed trajectory"):
        assert phrase in src
    R=1
    def chord(angle):
        return math.sqrt((R-R*math.cos(angle))**2+(R*math.sin(angle))**2)
    spring_U=lambda angle: .5*20*(chord(angle)-math.sqrt(2))**2
    eps=1e-5
    # Negative derivative is the tangential spring force at the antipode.
    deriv=(spring_U(math.pi+eps)-spring_U(math.pi-eps))/(2*eps*R)
    approx(deriv,0,eps=1e-8)
    target=spring_U(math.pi)-spring_U(math.pi/2)
    approx(target,10*(2-math.sqrt(2))**2)
    for delta in (.01,.001,.0001):
        available=spring_U(math.pi-delta)-spring_U(math.pi/2)
        assert 0<available<target
    assert abs(spring_U(math.pi-.0001)-spring_U(math.pi))<1e-7


def test_c6h_crown_exact_rest_is_not_spontaneous_release():
    """The classic h=2R/3 sliding result requires a perturbation limit.
    Exact symmetric rest on a frictionless dome has no tangent gravity."""
    src=(WPE/"c06-constructions-r4.js").read_text(encoding="utf-8")
    assert "Exact unperturbed rest would remain at the unstable equilibrium" in src
    assert "vanishing downhill perturbation" in src
    assert "vanishing-perturbation crown-rest LIMIT" in src
    g,R=10,5
    approx(g*math.sin(0),0)
    heights=[R*2*math.cos(theta0)/3 for theta0 in (.1,.01,.001)]
    assert heights[0]<heights[1]<heights[2]<2*R/3
    assert abs(heights[-1]-2*R/3)<2e-6
