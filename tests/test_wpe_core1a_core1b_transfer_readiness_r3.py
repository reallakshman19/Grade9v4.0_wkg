"""Independent academic/reasoning checks for F04–F08 R3, not learner certification.

Use explicit physics equations and limiting models independent of JS answer keys.
R2, source custody, PR #61 gateway and PR #55 donor files remain untouched.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import math
import re

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics/wpe"
BANK=ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
SOURCES={"EX-M50":"F04","EX-M92":"F05","EX-M96":"F06","EX-M106":"F07","EX-N27":"F08"}

def close(actual,expected,eps=1e-9):
    assert math.isclose(actual,expected,rel_tol=eps,abs_tol=eps),(actual,expected)
def kinetic(m1,m2,u1,u2):
    M=m1+m2
    mu=m1*m2/M
    V=(m1*u1+m2*u2)/M
    return .5*M*V**2,.5*mu*(u1-u2)**2,V,mu
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def test_original_custody_unmodified_and_only_source_specific_targets():
    cover=json.loads((WPE/"learning-coverage-r1.json").read_text(encoding="utf-8"))
    bank=json.loads(BANK.read_text(encoding="utf-8"))
    assert cover["source_bank_git_blob"]==blob(BANK)
    assert len(cover["questions"])==len(bank["questions"])==74
    rows={q["source_id"]:q for q in cover["questions"]}
    orig={q["source_id"]:q for q in bank["questions"]}
    assert rows.keys()==orig.keys()
    for source_id,lesson in SOURCES.items():
        row=rows[source_id]
        assert row["fit"]=="FOCUSED_NEW"
        assert row["primary_lesson"]==lesson
        assert row["stem_sha256"]==orig[source_id]["stem_sha256"]
        assert row["lesson_href"].endswith("#"+lesson)
        assert row["academic_status"]=="PRACTICE_ONLY_NOT_ADMITTED"
    assert rows["EX-M106"]["has_source_caution"] and rows["EX-N27"]["has_source_caution"]
    assert "turning" in rows["EX-M106"]["source_science_note"].lower()
    assert "10%" in rows["EX-N27"]["source_science_note"]

def test_f04_b_ice_skaters_available_internal_energy_and_preload_limit():
    # A on LEFT moving right, B on RIGHT moving left; relative compression.
    Kcom,Krel,V,mu=kinetic(2,4,+3,-1)
    close(V,1/3)
    close(mu,4/3)
    close(Kcom,1/3)
    close(Krel,32/3)
    close(Kcom+Krel,11)
    x=math.sqrt(2*Krel/24)
    close(x,math.sqrt(8/9))
    preload=.5*24*.2**2
    close(preload,.48)
    x_pre=math.sqrt(2*(Krel+preload)/24)
    close(x_pre,math.sqrt(209)/15)
    assert x_pre>x
    # Common boost (frame change) has no effect on spring maximum.
    for common in (-6,-1,0,5,12):
        _,available,_,_=kinetic(2,4,3+common,-1+common)
        close(available,Krel)
    # One-body-only moving original EX-M50 source check must not be copied.
    _,available,_,_=kinetic(.25,.25,1,0)
    close(math.sqrt(2*available/2),.25)
    close(kinetic(2,4,3,3)[1],0)
    assert math.sqrt(2*Krel/(24*100)) < x

def test_f05_b_measured_velocity_profile_not_endpoint_only():
    m,tip=3,6
    linear=lambda s:tip*s
    exact=.5*m*tip**2/3
    close(exact,18)
    close(linear(.25),1.5)
    six_mid=.5*(m/6)*sum(linear((j+.5)/6)**2 for j in range(6))
    close(six_mid,143/8)
    assert six_mid<exact
    for N in (2,4,6,32,256):
        approx=.5*(m/N)*sum(linear((j+.5)/N)**2 for j in range(N))
        assert approx<exact
    # Same endpoints, nonlinear wave-shaped field -> another integral.
    nonlinear=.5*m*tip**2/5
    close(nonlinear,10.8)
    close(2*nonlinear/tip**2,.6)
    assert nonlinear!=exact
    # Both ends translate at v: no 'one-sixth' shortcut.
    close(m*(tip**2+tip**2+tip**2)/6,.5*m*tip**2)

def test_f06_b_hydro_kinetic_flux_and_area_change_limit():
    rho,A,v,eta=1000,.25,2,.2
    flow=rho*A*v
    eps=.5*v**2
    wind=flow*eps
    electrical=eta*wind
    close(flow,500)
    close(eps,2)
    close(wind,1000)
    close(electrical,200)
    A2,v2=.10,3
    power2=.5*eta*rho*A2*v2**3
    close(power2,270)
    close(power2/electrical,1.35)
    close((A2/A)*(v2/v)**3,1.35)
    close(.5*eta*rho*A*0**3,0)
    # No head or hydraulic pressure energy included in this model.
    assert math.isclose(.5*eta*rho*(2*A)*v**3,2*electrical)

def test_f07_b_circle_turning_vs_static_and_variable_work():
    m,g,R=.5,10,2
    theta=math.pi/6
    dx=R*math.sin(theta)
    dh=R*(1-math.cos(theta))
    du=m*g*dh
    Fturn=du/dx
    Fstatic=m*g*math.tan(theta)
    close(dx,1)
    close(du,10-5*math.sqrt(3))
    close(Fturn,5*(2-math.sqrt(3)))
    close(Fstatic,5/math.sqrt(3))
    assert Fstatic>Fturn
    # Work of quasistatic F(theta)=mg*tan(theta) over dx=R*cos(theta)dtheta.
    work= m*g*R*(1-math.cos(theta))
    close(work,du)
    assert not math.isclose(Fstatic*dx,work)
    for small in (1e-4,1e-5):
        close(math.tan(small/2)/math.tan(small),.5,eps=1e-8)
    # Source 45° ambiguity remains physical, not just editorial.
    close(math.tan(math.pi/8),math.sqrt(2)-1)
    close(math.tan(math.pi/4),1)

def test_f08_b_spacecraft_relative_energy_and_underdetermination():
    Kcom,Krel,V,mu=kinetic(200,300,4,0)
    close(V,1.6)
    close(mu,120)
    close(Kcom,640)
    close(Krel,960)
    close(Kcom+Krel,1600)
    close(math.sqrt(2*Krel/9600),math.sqrt(.2))
    close(kinetic(200,300,4,4)[1],0)
    # Unknown external thruster can change relative energy: two possible
    # physically distinct external inputs yield different compression.
    x0=math.sqrt(2*Krel/9600)
    x_plus=math.sqrt(2*(Krel+200)/9600)
    x_minus=math.sqrt(2*(Krel-200)/9600)
    assert x_minus<x0<x_plus
    # Source coach assumes 10% WHOLE initial KE -> spring.
    k_conditional=2*(.1*.5*40000*20**2)/1**2
    close(k_conditional,1.6e6)
    assert k_conditional!=9600

def test_five_two_task_definitions_and_specific_model_decision_controls():
    src=(WPE/"gap-transfer-r3.js").read_text(encoding="utf-8")
    base=(WPE/"gap-journeys.js").read_text(encoding="utf-8")
    engine=(WPE/"gap-six-stage-engine.js").read_text(encoding="utf-8")
    html=(WPE/"gap-journeys.html").read_text(encoding="utf-8")
    assert len(re.findall(r"(?m)^F0[4-8]:\{",src))==5
    assert src.count('prediction:"')==5
    assert src.count('challenge:"UNFAMILIAR SETTING.')==5
    assert src.count('boundary:"CHANGED')==5
    assert src.count('worked:[')==5
    assert src.count('hints:[')==5
    assert src.count('boundaryFields:[')==5
    assert src.count('originalAssumption:assumption(')==5
    assert src.count('academic:{')==5
    for category in ["MODEL_CHOICE","INVALID_ASSUMPTION","SIGN_OR_REFERENCE_FRAME",
                     "SPATIAL_REPRESENTATION","GEOMETRY_AND_SIGN","CALCULATION_OR_UNITS"]:
        assert category in src or category in engine
    for id_ in SOURCES.values():
        assert id_+':{' in src
    assert 'r3.originalAssumption' in base
    assert 'd.transfer=r3.transfer' in base
    assert 'taskKey=id=>id+(variantOf[id]==="T2"?"-T2":"")' in engine
    assert 'localStorage.setItem(prefix+key,JSON.stringify(states[key]))' in engine
    assert 's.first={answers:{...values}' in engine
    assert 's.boundary={...values' in engine
    assert 's.first===null' in engine
    assert 'showStage(host,active,problem,focus)' in engine
    assert 'd.worked' in engine and 's.stage===2' in engine
    assert 's.hints.length<data.hints.length' in engine
    assert 's.helpHistory.push' in engine
    assert 'x.stem_sha256===found.stem_sha256' in engine
    assert 'typeof s.first.answers.reason==="string"' in engine
    assert 'src="gap-transfer-r3.js" defer' in html
    assert 'src="gap-transfer-r3.css"' not in html # CSS must use stylesheet link
    assert 'href="gap-transfer-r3.css"' in html
    assert "innerHTML" not in src and "innerHTML" not in engine
    assert "WPE_R3_CONTENT" in src
    assert "g9:wpe:gaps:v2:" in base

def test_no_pr61_integration_or_question_bank_file_writes_in_r3():
    # This is local path-scope guard for R3's new authored artifacts; the actual
    # changed-file list must still be separately checked on the PR head.
    for file in ("gap-transfer-r3.js","gap-transfer-r3.css",
                 "gap-journeys.js","gap-six-stage-engine.js","gap-journeys.html"):
        assert (WPE/file).is_file()
    assert (ROOT/"docs/wpe-r3-real-learner-observation-protocol.md").exists()
    assert (ROOT/"physics/wpe/reviews/WPE_CORE1A_CORE1B_TRANSFER_R3_AUDIT.md").exists()
