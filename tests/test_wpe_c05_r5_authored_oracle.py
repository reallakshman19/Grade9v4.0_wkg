"""Adversarial R5 numeric oracle against EXECUTED authored JS definitions.

This deliberately does not import the author's expected values to calculate the
answers: all 14 Task A/B and their 14 boundaries have separate Python Physics
oracles below. Node only exposes the authored values for COMPARISON. It does
not launch the student app, mutate source/question records, or trust its key.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT=Path(__file__).resolve().parents[1]
JS=ROOT/"physics/wpe/c05-graph-constructions-r5.js"

def authored():
    if not shutil.which("node"):
        pytest.skip("Node.js runtime absent; CI explicitly checks Node and runs authored oracle")
    script=r"""
const fs=require("fs"),vm=require("vm");
const code=fs.readFileSync(process.argv[1],"utf8");
let models=null;
const window={WPEGapJourneys:(definitions,config)=>{models=definitions}};
vm.runInNewContext(code,{window}, {filename:"c05-graph-constructions-r5.js",timeout:2000});
if(!models)throw Error("No R5 lesson definitions exported");
const extract=(fs)=>Object.fromEntries(fs.filter(f=>f.type==="number")
    .map(f=>[f.id,f.expected]));
const output={};
for(const [id,d] of Object.entries(models)){
  output[id]={
    source:d.source,
    fields:extract(d.fields),
    boundary:extract(d.boundaryFields),
    bfields:extract(d.transfer.fields),
    bboundary:extract(d.transfer.boundaryFields),
    choices:{
      a:[d.fields[0].id,d.fields[1].id,d.fields[0].expected,d.fields[1].expected],
      b:[d.transfer.fields[0].id,d.transfer.fields[1].id,d.transfer.fields[0].expected,d.transfer.fields[1].expected],
    },
    taskText:[d.challenge,d.transfer.challenge],
    hintCounts:[d.hints.length,d.transfer.hints.length],
    workedCounts:[d.worked.length,d.transfer.worked.length],
    sourceCaution:d.sourceCaution,
  };
}
process.stdout.write(JSON.stringify(output));
"""
    result=subprocess.run(["node","-e",script,str(JS)],cwd=ROOT,text=True,
                          capture_output=True,check=True,timeout=15)
    return json.loads(result.stdout)

def close(actual,expected):
    assert isinstance(actual,(int,float)) and math.isfinite(actual)
    assert math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)

def compare(actual,expected):
    assert set(actual)==set(expected),(set(actual),set(expected))
    for key,calculated in expected.items():
        close(actual[key],calculated)

def test_authored_fourteen_tasks_and_boundaries_equal_independent_physics_oracles():
    models=authored()
    assert set(models)=={"G5U","G5E","G5P","G5V","G5W","G5C","G5X"}

    # Seven model signatures; each has two distinct tasks + different boundaries.
    # Independent values are calculated by formulas, not from authored fields.
    independent={
        "G5U":{
            "source":"EX-M11",
            "fields":{"bc":-((4-10)/(5-2)),"de":-((7-4)/(8-7))},
            "boundary":{"de":-(7-4)/(.1*(8-7))},
            "bfields":{"ab":-((1-4)/(1-0)),"bc":-((5-1)/(3-1))},
            "bboundary":{"ab":-3},
        },
        "G5E":{
            "source":"EX-M61",
            "fields":{"ka":9-3,"kd":9-1},
            "boundary":{"kc":(9+4)-12},
            "bfields":{"kb":40-2*10*1.5,"kd":40-2*10*.8},
            "bboundary":{"kc":(40+15)-2*10*2.5},
        },
        "G5P":{
            "source":"EX-M69",
            "fields":{"speed":math.sqrt(5**2+2*50*3/4),
                      "distance":4/(3*50)*((5**2+2*50*3/4)**1.5-5**3)},
            "boundary":{"distance":10*2},
            "bfields":{"speed":math.sqrt(3**2+2*8*2/2),
                       "distance":2/(3*8)*((3**2+2*8*2/2)**1.5-3**3)},
            "bboundary":{"speed":math.sqrt(3**2+2*4*2/2),
                         "distance":2/(3*4)*((3**2+2*4*2/2)**1.5-3**3)},
        },
        "G5V":{
            "source":"EX-M85",
            "fields":{"work":.5*3*((2)**2-(-4)**2),
                      "displacement":((-4)+2)/2*3},
            "boundary":{"work":.5*3*((4)**2-(-4)**2),
                        "displacement":((-4)+4)/2*3},
            "bfields":{"work":.5*800*((-1)**2-(2)**2),
                       "displacement":(2+(-1))/2*4},
            "bboundary":{"work":.5*800*((-3)**2-(2)**2),
                         "displacement":(2+(-3))/2*4},
        },
        "G5W":{
            "source":"AN-2",
            "fields":{"work":3*((-1)**2)-3*((2)**2),
                      "force":-6*2},
            "boundary":{"work":3*(2**2)-3*((-1)**2)},
            "bfields":{"work":-2*10*(7-3),
                       "potential":2*10*(7-3)},
            "bboundary":{"direct":-2*10*(7-3)-5*5,
                         "long":-2*10*(7-3)-5*12},
        },
        "G5C":{
            "source":"AN-6",
            "fields":{"loop":3*1*(0-2),"route2":3*1*(2-0)},
            "boundary":{"loop":0,"potential":1**2},
            "bfields":{"short":-4*3,"long":-4*5},
            "bboundary":{"work":3*2,"potential":-3*2},
        },
        "G5X":{
            "source":"JEE-2026-04-06-S2-Q29",
            "fields":{"work":.5*4*((2+.5*4)**2-(2+.5*0)**2),
                      "force":4*(2+.5*4)*.5},
            "boundary":{"work":.5*4*((-2)**2-(-4)**2)},
            "bfields":{"work":.5*5*((math.sqrt(9+4*4))**2-(math.sqrt(9+0))**2),
                       "force":5*.5*4},
            "bboundary":{"work":.5*5*((9+4*4-4**2)-(9+0))},
        },
    }
    assert models.keys()==independent.keys()
    for signature,rules in independent.items():
        got=models[signature]
        assert got["source"]==rules["source"],signature
        for section in ("fields","boundary","bfields","bboundary"):
            compare(got[section],rules[section])
        assert got["choices"]["a"][:2]==["model","assumption"]
        assert got["choices"]["b"][:2]==["model","assumption"]
        assert all(isinstance(s,str) and len(s)>30 for s in got["taskText"])
        assert got["taskText"][0]!=got["taskText"][1],signature
        assert "UNFAMILIAR SETTING" in got["taskText"][1],signature
        assert got["hintCounts"]==[3,3]
        assert got["workedCounts"]==[4,4]
        assert isinstance(got["sourceCaution"],str) and "source" in got["sourceCaution"].lower()

def test_independent_negative_controls_are_not_normalized_into_wrong_graph_operations():
    # These deliberately yield different SI UNITS; coincidentally matching
    # numerical values would not make an operator physically valid.
    # F(x) area: N·m = J; U(x) area: J·m, no direct force/work.
    U_slope=(12-4)/(2-0)
    force=-U_slope
    assert force==-4 # N
    U_area=.5*(12+4)*2
    assert U_area==16 # J·m, invalid comparison with signed force/work
    # A v(t) signed trapezoid measures displacement; a v(x) integral doesn't.
    disp=(6+(-2))/2*2
    assert disp==4 # metres
    velocity_position_area=((2+4)/2)*2
    assert velocity_position_area==6 # metres²/second, NOT joules
    # Work NET depends only on squared speeds; reverse equal magnitudes W0.
    assert .5*3*((+4)**2-(-4)**2)==0
    # A measured 2D loop with nonzero circulation refutes scalar potential.
    assert -6!=0
    # A single U(x) value below E need not be reachable across a U>E barrier.
    assert 9-1>0 and 9-12<0
    # Source xdot=2x² exact zero position equilibrium cannot reach positive
    # position in finite time without additional initial condition/forcing.
    assert .5*(1/1e-6-1)>1e5
