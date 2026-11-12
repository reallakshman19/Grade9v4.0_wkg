"""Physics and route tests for E01–E05 interactive practice.

The equations are independently rederived here; this is software QA, not
academic certification or grading of a child's written explanations.
"""
from __future__ import annotations
import json
import math
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WPE=ROOT/"physics"/"wpe"
BRIDGE=ROOT/"WPE_Source_to_Core1A_Concept"/"learning-bridge"/"P0_P1_CONSTRUCTION_BRIDGE.json"
PACKS=ROOT/"WPE_Source_to_Core1A_Concept"/"learning-bridge"
READER=ROOT/"workspace"/"output"/"WPE_Core2_Consolidated_20261102"/"native-candidate"/"selected_bank.review.json"
EXPECTED={
    "E01":("POTENTIAL_WELLS_LEARNING_PACK.md",{"WEP07-03","EX-M109"}),
    "E02":("INSTANTANEOUS_POWER_LEARNING_PACK.md",{"TB-WPE-ILL-05","TB-WPE-ILL-06"}),
    "E03":("SPRING_PROJECTILE_TRANSITION_LEARNING_PACK.md",{"EX-N34"}),
    "E04":("DISSIPATIVE_BOUNCES_LEARNING_PACK.md",{"EX-M82"}),
    "E05":("RADIAL_FORCE_POTENTIAL_LEARNING_PACK.md",{"EX-M89"}),
}

def close(a,b):
    assert math.isclose(a,b,abs_tol=1e-10,rel_tol=1e-10),(a,b)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_all_five_are_distinct_from_c01_c08_and_reference_existing_packs():
    script=(WPE/"extension-learning.js").read_text(encoding="utf-8")
    page=(WPE/"extension-learning.html").read_text(encoding="utf-8")
    css=(WPE/"extension-learning.css").read_text(encoding="utf-8")
    routes=load(WPE/"reasoning-paths.review.json")["constructions"]
    bridge=load(BRIDGE)["extensions_backlog"]
    reader={q["source_id"] for q in load(READER)["questions"]}
    assert len(bridge)==5
    assert set(EXPECTED)=={"E01","E02","E03","E04","E05"}
    assert all((PACKS/p).is_file() for p,_ in EXPECTED.values())
    for id_,(pack,ids) in EXPECTED.items():
        assert f"    {id_}: {{" in script
        row=next(x for x in routes if x["id"]=="WPE-"+id_)
        assert set(x["id"] for x in row["proposed_source_ids"])==ids
        assert all(x["reader_present"] for x in row["proposed_source_ids"])
        assert ids<=reader
        assert bridge[int(id_[-1])-1]["status"]=="AUTHOR_PACK_DRAFTED_NOT_ADMITTED"
        text=(PACKS/pack).read_text(encoding="utf-8")
        assert "## Core1A" in text and "## Core1B" in text
    assert 'src="extension-learning.js"' in page
    assert 'href="extension-learning.css"' in page
    assert 'id="lesson-surface"' in page
    assert "extension-learning.html" in (WPE/"index.html").read_text(encoding="utf-8")
    route_html=(WPE/"reasoning-paths.html").read_text(encoding="utf-8")
    assert "extension-learning.html" in route_html
    assert "route.proposed_source_ids.some(s=>s.id===id&&s.reader_present)" in route_html
    assert "No interactive student lesson yet" not in route_html
    assert "@media(max-width:520px)" in css
    assert "d3d4-self-tutor.js" not in script  # independent feature, no C lesson rewrite

def test_first_attempt_before_reconstruction_and_changed_condition_gate():
    script=(WPE/"extension-learning.js").read_text(encoding="utf-8")
    assert "s.first={...values};s.attemptDraft={};s.stage=2" in script
    assert "s.boundary=val" in script
    assert "s.repair=val;s.stage=5" in script
    assert "s.first" in script and "window.confirm" in script
    assert "s.hintsUsed=Math.min(config.hints.length,s.hintsUsed+1)" in script
    assert "localStorage.setItem" in script
    assert 'if(s.stage===2)' in script
    assert 'if(s.stage===5)' in script
    assert 'if(s.boundary===null)' in script
    assert "innerHTML" not in script  # no raw text-to-HTML injection
    for id_ in EXPECTED:
        assert f"{id_}:" in script
    assert script.count('visual:"')==5
    assert "sourceId" in script and "reader_present" in script

def test_e01_allowed_but_unreachable_connected_regions():
    # Guided parabola: U=(x-2)^2, m=2 kg, E=4 J.
    u=lambda x:(x-2)**2
    assert [u(x) for x in range(5)]==[4,1,0,1,4]
    assert [4-u(x) for x in range(5)]==[0,3,4,3,0]
    close(math.sqrt(2*(4-u(2))/2),2)
    assert [x for x in range(5) if u(x)<=1]==[1,2,3]
    # Fresh quartic: energy 9; NOT enough to cross U(0)=16.
    v=lambda x:(x*x-4)**2
    bounds=[-math.sqrt(7),-1,1,math.sqrt(7)]
    for x in bounds:close(v(x),9)
    assert v(2)==v(-2)==0 and v(0)==16
    assert v(0)>9  # disconnection, despite low destination
    close(math.sqrt(2*9/2),3)
    close(math.sqrt(2*(17-v(0))/2),1)
    assert (17-v(0))>0 and (9-v(0))<0
    # E=16 exactly is a separatrix; never equate U<=E to guaranteed
    # finite-time crossing at an unstable equilibrium.
    assert v(0)==16

def test_e02_signed_instantaneous_and_zero_power_nonzero_force():
    pull,resist,v=6,-2,3
    close(pull*v,18)
    close(resist*v,-6)
    close((pull+resist)*v,12)
    close((pull+resist)*(-v),-12)
    motor=(6,0)
    drag=(-2,-1)
    velocity=(3,4)
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    close(dot(motor,velocity),18)
    close(dot(drag,velocity),-10)
    net=(motor[0]+drag[0],motor[1]+drag[1])
    close(dot(net,velocity),8)
    close(math.hypot(*net)*math.hypot(*velocity),5*math.sqrt(17))
    assert not math.isclose(5*math.sqrt(17),8)
    boundary=(1,4)
    assert dot(net,boundary)==0 and math.hypot(*net)>0 and math.hypot(*boundary)>0

def test_e03_contact_friction_only_and_projectile_limits():
    mass,k,x,f,h,g=.5,125,.2,2.5,1.25,10
    spring=.5*k*x*x
    work=-f*x
    launch=spring+work
    t=math.sqrt(2*h/g)
    close(spring,2.5);close(work,-.5);close(launch,2)
    v=math.sqrt(2*launch/mass)
    close(v,math.sqrt(8))
    close(t,.5);close(v*t,math.sqrt(2))
    v_free=math.sqrt(2*spring/mass)
    close(v_free,math.sqrt(10));close(v_free*t,math.sqrt(10)/2)
    assert t==.5 and v_free*t>v*t
    # No projectile when contact friction consumes all spring energy;
    # speed is not a real number for a negative launch energy.
    assert spring-f*x>0
    close(spring/(x),12.5)  # friction threshold for nonnegative launch K
    # Guided model A and model B are deliberately different objects.
    close(.5*100*.2**2,2)
    close(math.sqrt(2*2/1),2)
    close(3*math.sqrt(2*1.25/10),1.5)

def test_e04_energy_speed_and_geometric_bounce_factors():
    h=2
    retained=.25
    heights=[h*retained**n for n in (1,2,3)]
    assert heights==[.5,.125,.03125]
    close(math.sqrt(retained),.5)
    close(h+2*h*retained/(1-retained),10/3)
    r0,r1=.75,.5
    first=h*r0
    close(first,1.5);close(first*r1,.75);close(first*r1*r1,.375)
    close(h+2*first/(1-r1),8)
    close(math.sqrt(r0),math.sqrt(3)/2)
    close(h+2*h*.75/(1-.75),14)
    assert h+2*h*.75/(1-.75)>h+2*first/(1-r1)
    close(h+2*h*0/(1-0),h)  # r=0: no rebound
    assert h+2*h*.99/(1-.99)>h+2*h*.5/(1-.5)  # ideal r→1 grows

def test_e05_force_potential_area_local_centripetal_and_work_sign():
    force,mass,r=3,1,2
    delta_u=force*r
    assert delta_u==6
    close(mass*(math.sqrt(force*r/mass))**2/r,force)
    close(.5*mass*(force*r/mass),3)
    close(delta_u+3,9)
    # The signed radial force would produce negative radial work.
    close(-force*r,-delta_u)
    def f(radius):return 4 if radius<=2 else 4+2*(radius-2)
    u3=4*2+(.5*(f(2)+f(3))*(3-2))
    close(u3,13)
    close(f(3),6)
    v3=math.sqrt(f(3)*3/2)
    close(v3,3)
    k3=.5*2*v3*v3
    close(k3,9);close(u3+k3,22)
    u4=8+.5*(f(2)+f(4))*2
    close(u4,20)
    v4=math.sqrt(f(4)*4/2)
    close(v4,4);close(.5*2*v4*v4,16)
    close(u4+.5*2*v4*v4,36)
    assert u4+.5*2*v4*v4 != u3+k3
    # Tangential v and inward F are orthogonal, so no work per lap.
    assert sum(a*b for a,b in zip((-6,0),(0,3)))==0
