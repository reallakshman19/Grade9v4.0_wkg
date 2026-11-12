"""R5 C05 academic-only Physics checks: independent numerical laws and negatives.

Source custody, source options, answer keys, QRT status and route classifications
remain unchanged. Passing equations does not authenticate any exam figure/key.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPE = ROOT / "physics/wpe"
BANK = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json"
MAP = WPE / "learning-coverage-r1.json"
IDS = ["EX-M11","EX-M61","EX-M69","EX-M85","AN-2","AN-6","JEE-2026-04-06-S2-Q29"]
CONSTRUCTIONS = {"EX-M11":"G5U","EX-M61":"G5E","EX-M69":"G5P","EX-M85":"G5V",
                 "AN-2":"G5W","AN-6":"G5C","JEE-2026-04-06-S2-Q29":"G5X"}

def read(path): return json.loads(path.read_text(encoding="utf-8"))
def near(a,b,tol=1e-7): assert math.isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b)
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def test_all_seven_original_records_and_74_custody_are_untouched_related_only():
    b,m=read(BANK),read(MAP)
    assert len(b["questions"])==len(m["questions"])==74
    assert m["source_bank_git_blob"]==blob(BANK)
    bk={r["source_id"]:r for r in b["questions"]}
    mp={r["source_id"]:r for r in m["questions"]}
    assert bk.keys()==mp.keys()
    for sid in IDS:
        original,route=bk[sid],mp[sid]
        assert original["stem_sha256"]==route["stem_sha256"]
        assert original["stem"] and original["source_name"] and isinstance(original["options"],list)
        assert original["key_state"].startswith("HOLD") and original["review_state"]=="NOT_ADMITTED"
        assert route["fit"]=="RELATED_BRIDGE"
        assert route["primary_lesson"]=="C05"
        assert route["academic_status"]=="PRACTICE_ONLY_NOT_ADMITTED"
        assert route["reader_proposal"]["op"]==original["op"]
        assert route["reader_proposal"]["band"]==original["band"]
    assert m["counts"]=={
        "total":74,"focused_new":8,"targeted":18,"related":48,"missing":0,
        "wrapped_related":41,"new_gap_closure":5,"shared_foundation_groups":4
    }
    assert Counter(x["fit"] for x in m["questions"])=={
        "FOCUSED_NEW":8,"TARGETED_PRACTICE":18,"RELATED_BRIDGE":48
    }

def test_original_figure_authority_and_option_gaps_are_not_invented():
    bank={r["source_id"]:r for r in read(BANK)["questions"]}
    f11=(ROOT/"workspace/output/G9V4_LOTS/CORE2_BATCH_01/assets/fig_q06_potential_curve.svg").read_text(encoding="utf-8")
    f61=(ROOT/"workspace/output/G9V4_LOTS/CORE2_BATCH_02/assets/fig_q17_potential_curve.svg").read_text(encoding="utf-8")
    f85=(ROOT/"workspace/output/G9V4_LOTS/CORE2_BATCH_02/assets/fig_q30_vt_graph.svg").read_text(encoding="utf-8")
    assert "Stable" in f11 and "Unstable" in f11
    assert "Slope_AB" in " ".join(bank["EX-M11"]["steps"])
    assert bank["EX-M11"]["figure_note"].startswith("Author-produced")
    assert "E_mech = 8 J" in f61
    assert bank["EX-M61"]["figure_note"].startswith("Author-produced")
    assert "50" in f85 and "40" in f85
    assert bank["EX-M85"]["figure_note"].startswith("Author-produced")
    assert bank["EX-M69"]["source_figures"]==[]
    assert len(bank["EX-M69"]["options"])==4
    assert all("[FIG-options-" in o for o in bank["EX-M69"]["options"])
    assert "FIGURE_UNRESOLVED" in bank["EX-M69"]["answer"]
    assert bank["AN-2"]["source_figures"]==[] and bank["AN-6"]["source_figures"]==[]
    assert bank["JEE-2026-04-06-S2-Q29"]["source_figures"]==[]
    audit=(WPE/"reviews/WPE_C05_GRAPH_OPERATIONS_R5_AUDIT.md").read_text(encoding="utf-8")
    for claim in ("EX-M11","EX-M61","EX-M69","EX-M85","AN-2","AN-6",
                  "JEE-2026-04-06-S2-Q29","B1","B2","B3","B4","B5","B6","B7",
                  "HOLD","RELATED_BRIDGE","NOT_RUN"):
        assert claim in audit
    assert "original figure" in audit.lower()

def test_g5u_multi_segment_signed_force_and_absolute_slope_negative_operator():
    # Guided independent synthetic points, all axes x metres U joules.
    p=[(0,0),(1,6),(3,2),(5,2),(7,8)]
    slopes=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(p,p[1:])]
    assert slopes==[6,-2,0,3]
    forces=[-z for z in slopes]
    assert forces==[-6,2,0,-3]
    assert sorted(range(4),key=lambda i:abs(forces[i]),reverse=True)==[0,3,1,2]
    # Task A (not source): AB5,BC-2,CD0,DE+3 J/m.
    p=[(0,0),(2,10),(5,4),(7,4),(8,7)]
    slopes=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(p,p[1:])]
    assert slopes==[5,-2,0,3]
    assert [-s for s in slopes]==[-5,2,0,-3]
    assert sorted(range(4),key=lambda i:abs(slopes[i]),reverse=True)==[0,3,1,2]
    # Changing tick length from 1m to .1m scales every force tenfold.
    near(-slopes[3]/.1,-30)
    # Task B: 1 mJ/mm is 1 Newton, including SIGN.
    near((1e-3)/(1e-3),1)
    p=[(0,4),(1,1),(3,5),(5,5)]
    assert [(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(p,p[1:])]==[-3,2,0]
    assert [3,-2,0]==[-(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(p,p[1:])]
    near(-3,-(3)) # reversed axis changes signed force only

def test_g5e_local_kinetic_energy_is_not_automatic_path_access():
    E=12
    U=[12,12,4,16,8] # Guided synthetic continuous piecewise profile
    K=[E-z for z in U]
    assert K==[0,0,8,-4,4]
    near(math.sqrt(2*8/1),4)
    assert K[3]<0 and K[4]>0
    # At U=E on flat plateau: K=0, zero conservative force along it.
    near(-((12-12)/(1-0)),0)
    # Task A synthetic potential from A->D contains U12>E9 barrier.
    E=9
    K={key:E-u for key,u in {"A":3,"B":9,"C":12,"D":1}.items()}
    assert K=={"A":6,"B":0,"C":-3,"D":8}
    assert K["D"]>=0 and K["C"]<0 # D locally allowed, not accessible from A
    assert 13-12==1 # changed external +4 J removes barrier
    # Task B height profile: 2kg g10, gravitational potential
    U={key:2*10*h for key,h in {"A":.5,"B":1.5,"C":2.5,"D":.8}.items()}
    assert U=={"A":10,"B":30,"C":50,"D":16}
    assert 40-U["B"]==10 and 40-U["D"]==24
    assert 40-U["C"]<0 # hill impassable
    assert 55-U["C"]==5 # +15J motor work before hill

def test_g5p_constant_mechanical_power_time_integration_and_start_singularity():
    # Guided P18, m4, u0 (formal t>0 solution).
    P,m=18,4
    coefficient=2*P/m
    near(coefficient,9)
    for t in (.25,1,4):
        v=math.sqrt(coefficient*t)
        s=(2/3)*math.sqrt(coefficient)*t**1.5
        near(v,3*math.sqrt(t))
        near(s,2*t**1.5)
    near(2*4**1.5,16)
    near(3*math.sqrt(4),6)
    a1=P/(m*(3*math.sqrt(.01)))
    a2=P/(m*(3*math.sqrt(.0001)))
    assert a2>a1 and a2>100 # finite P at near-zero speed requires divergent acceleration
    # Task A nonzero start, P50 m4 u5, 3 sec.
    P,m,u,t=50,4,5,3
    v2=u*u+2*P*t/m
    near(v2,100)
    near(math.sqrt(v2),10)
    distance=m/(3*P)*(v2**1.5-u**3)
    near(distance,70/3)
    near(10*2,20) # switched-off power: uniform 10m/s for 2s
    # B nonzero u3, m2 P8 for2 sec
    P,m,u,t=8,2,3,2
    end=u*u+2*P*t/m
    near(end,25)
    near(m/(3*P)*(end**1.5-u**3),49/6)
    # Boundary efficiency50% -> Puseful4; speed²17 and distance
    P=4
    end=u*u+2*P*t/m
    near(end,17)
    near(m/(3*P)*(end**1.5-u**3),(17*math.sqrt(17)-27)/6)
    # Constant power is NOT constant force as speed changes: F=P/v.
    assert 8/3 != 8/5

def test_g5v_velocity_time_area_displacement_but_work_is_endpoint_deltaK():
    # Guided v(t)=6-4t, m5, t0..2.
    m,vi,vf,dt=5,6,-2,2
    near(.5*m*(vf*vf-vi*vi),-80)
    near((vi+vf)/2*dt,4)
    assert -80!=4
    # A m3, initial-4 final+2 in3 sec.
    m,vi,vf,dt=3,-4,2,3
    near(.5*m*(vf**2-vi**2),-18)
    near((vi+vf)*dt/2,-3)
    # A changed final+4 means same speed magnitudes but signed area cancels.
    near(.5*m*(4**2-(-4)**2),0)
    near((-4+4)*3/2,0)
    # B elevator m800, initial+2 final-1 -> net work-1200, displacement+2.
    m,vi,vf,dt=800,2,-1,4
    near(.5*m*(vf**2-vi**2),-1200)
    near((vi+vf)*dt/2,2)
    near(.5*m*((-3)**2-vi**2),2000)
    near((vi-3)*dt/2,-2)
    assert .5*m*(vf**2-vi**2)<0 and vf<0 # not a negative KE

def test_g5w_force_x_signed_area_and_conservative_work_sign():
    # Guided spring F=-4x N, x1->3; U=2x² J.
    W=-2*(3**2-1**2)
    dU=2*(3**2-1**2)
    near(W,-16)
    near(dU,16)
    near(W,-dU)
    # A U=3x², x-1 to2, F=-6x.
    Ui=3*(-1)**2;Uf=3*(2)**2
    near(Ui-Uf,-9)
    near(-3*(2**2-(-1)**2),-9)
    near(-6*2,-12)
    near(Uf-Ui,9) # reverse endpoint work
    # B m2, g10, 3m to7m: gravity work-80 for ANY route
    Wg=-(2*10)*(7-3)
    near(Wg,-80)
    near(-Wg,80)
    # Measured additional -5N across different lengths 5m and12m.
    near(Wg-5*5,-105)
    near(Wg-5*12,-140)
    assert Wg-25 != Wg-60

def test_g5c_closed_loop_and_two_open_paths_disprove_single_valued_potential():
    # Guided F=(2y,0), rectangle x0..2 and y0..h.
    for h in (.25,1,2):
        Wtop=2*h*(-2)
        near(Wtop,-4*h)
        assert Wtop!=0
    # Height=0 gives degenerate loop with W0, not proof of conservativity.
    near(-4*0,0)
    # Task A F=(3y,0) rectangle, counterclockwise upper edge left.
    near(3*1*(0-2),-6)
    # Same A to B: bottom then right gives0; left then top gives+6J.
    near(3*0*2,0)
    near(3*1*2,6)
    # Boundary F_y=-2y -> U=y² and closed loop0.
    near(1**2,1)
    near((-1**2)+1**2,0)
    # B 4N sliding resistance on lengths 3 and5, same endpoints.
    near(-4*3,-12)
    near(-4*5,-20)
    assert -4*3 != -4*5
    # Change to uniform conservative F_x=+3N, Δx2.
    near(3*2,6)
    near(-3*2,-6) # U(2), with U(0)=0

def test_g5x_velocity_position_endpoint_work_chain_rule_and_initial_equilibrium():
    # Guided m2, v(x)=1+x from x1 to3, nonzero initial speed.
    m=2
    vi,vf=1+1,1+3
    near(.5*m*(vf**2-vi**2),12)
    near(m*(1+3)*1,8) # F at x3
    near((2*3+3**2)-(2*1+1**2),12) # ∫2(1+x)dx
    # A m4, v=2+.5x on 0..4
    m=4
    near(.5*m*((2+.5*4)**2-2**2),24)
    near(m*(2+.5*4)*.5,8)
    near((4*4+.5*4**2),24)
    # Independent reverse velocity negative: start -4 at x4, finish -2 at x0.
    near(.5*m*((-2)**2-(-4)**2),-24)
    # B m5, v=√(9+4x), x0..4, v² 9→25
    m=5
    near(.5*m*(25-9),40)
    near(.5*m*4,10) # m * v dv/dx = m/2 * derivative(v²)
    near(10*4,40)
    # Changed spatial profile v²=9+4x−x² has equal endpoint speeds.
    near(.5*m*((9+16-16)-9),0)
    near(10*4-2.5*4**2,0) # signed F=(10−5x) integral
    assert 10!=0 and 10-5*4 <0
    # Source law dx/dt = 2x² with x(0)=0: no finite-time spontaneous
    # departure; time from epsilon->1 grows as 1/(2epsilon).
    duration=lambda eps:.5*(1/eps-1)
    assert duration(.0001)>duration(.01)>duration(.1)>0
    assert 2*0**2==0
    near(.5*1*((2*5**2)**2-0),1250) # only the formal endpoint W
    assert "(m/s)" not in "2x²" # dimensional coefficient must carry units

def test_fourteen_distinct_a_b_tasks_gates_and_no_source_admission():
    js=(WPE/"c05-graph-constructions-r5.js").read_text(encoding="utf-8")
    html=(WPE/"c05-graph-constructions-r5.html").read_text(encoding="utf-8")
    src=(WPE/"c05-source-r5.js").read_text(encoding="utf-8")
    engine=(WPE/"gap-six-stage-engine.js").read_text(encoding="utf-8")
    assert all("const "+name+"={" in js for name in CONSTRUCTIONS.values())
    assert all('source:"'+sid+'"' in js for sid in IDS)
    assert js.count("transfer:task({")==7
    assert js.count("...task({")==7
    assert js.count("hints:[")==14
    assert js.count("worked:[")==14
    assert js.count("guideSteps:[")==7
    assert js.count("academic:{")==7
    assert js.count("prediction:")>=14
    assert js.count("boundary:")>=14
    assert "fields:[o.model,o.assumption,...o.numbers,reason(o.reason)]" in js
    assert "boundaryFields:[o.boundaryModel" in js
    assert 'source:"EX-M69"' in js and "[FIG-options-*]" in js
    assert 'g9:wpe:c05-r5:v1:' in js
    assert 'g9:wpe:c06-r4:v1:' not in js and 'g9:wpe:gaps:v2:' not in js
    assert "window.WPEGapJourneys(signatures" in js
    assert "innerHTML" not in js and "innerHTML" not in src
    assert 's.first={answers:{...values}' in engine
    assert 's.boundary={...values' in engine
    assert 'taskKey=id=>id+(variantOf[id]==="T2"?"-T2":"")' in engine
    assert 's.first===null' in engine and 's.hints.push(idx)' in engine
    assert 'src="gap-six-stage-engine.js"' in html
    assert 'src="c05-source-r5.js"' in html
    assert 'src="c05-graph-constructions-r5.js"' in html
    assert len([x for x in IDS if ("source="+x) in html])==7
    assert "new URLSearchParams(location.search).get(\"source\")" in src
    for claim in ('row.primary_lesson!=="C05"','row.fit!=="RELATED_BRIDGE"',
                  'row.academic_status!=="PRACTICE_ONLY_NOT_ADMITTED"',
                  'row.stem_sha256!==original.stem_sha256'):
        assert claim in src
    assert "source_figures" not in js # no source-original graph reproduced
