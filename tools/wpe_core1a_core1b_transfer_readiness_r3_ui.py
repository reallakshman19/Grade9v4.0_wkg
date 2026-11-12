"""R3 real Chromium: independent A/T2 first attempts, wrong-model diagnosis,
fresh unfamiliar setting, source exactness, changed-condition transfer.
Runs at desktop and mobile; human learner mastery remains NOT_RUN.
"""
from __future__ import annotations
from pathlib import Path
import http.server
import threading
from functools import partial
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="g9:wpe:gaps:v2:"
CASES=[
 ("EX-M50","F04","Total kinetic energy because both skaters stop","Friction removes an unknown fraction, but we may ignore it","com","-1"),
 ("EX-M92","F05","Entire cord at the 6 m/s tip speed","An arbitrary standing wave still has linear internal speeds","quarter","6"),
 ("EX-M96","F06","Kinetic energy of one fixed water packet irrespective of time","Water also descends an unknown vertical head that we ignore when computing TOTAL power","flow","300"),
 ("EX-M106","F07","Tangential static balance in both cases because speed is zero at the turn","Track normal performs positive work while the bead moves","rise","10"),
 ("EX-N27","F08","Ten percent of whole-system kinetic energy by the original wagon rule","Thrusters may supply unknown outside work but do not change relative motion","com","-1.6")
]

def check(ok,message):
    if not ok:raise AssertionError(message)

def server():
    app=http.server.ThreadingHTTPServer(("127.0.0.1",0),
            partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    app.daemon_threads=True
    threading.Thread(target=app.serve_forever,daemon=True).start()
    return app,"http://127.0.0.1:"+str(app.server_port)

def state(page,key):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))",PREFIX+key)

def test_case(browser,base,screen,source,lesson,wrong_model,wrong_assumption,wrong_numeric,wrong_number):
    width,height=screen
    context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    errors=[]
    try:
        page=context.new_page();page.on("pageerror",lambda error:errors.append(str(error)))
        page.goto(base+"/physics/wpe/gap-journeys.html?question="+source+"#"+lesson,wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for(timeout=15000)
        check(page.locator("#source-return").get_attribute("href").endswith("question="+source),
              "Wrong verified source return")
        check(page.locator(".academic-checkpoint").count()==1,lesson+" scientific Core1A checkpoint absent")
        check(page.locator(".academic-observations dt").count()==3,"No visible validity/limit/observable checks")
        check(page.locator(".guide-steps li").count()==5,"Existing Core1A derivation removed")
        check(page.locator(".guide svg").count()==1,"Existing interactive physics visual missing")
        check(page.locator(".worked").count()==0,"Worked transfer answer leaked before first attempt")
        check(page.locator('#progress-label').count()==1,"Prior progress and lesson route changed")
        check(page.locator("#transfer-progress-label").count()==1,"Second task progress absent")
        check(page.locator("[data-variant='T1']").get_attribute("aria-pressed")=="true","Task A should default")
        # Move a guided observable and ensure its physical readout changes.
        before=page.locator(".model-readout").inner_text()
        page.locator("#guide-slider").evaluate("(n)=>{n.value=n.min;n.dispatchEvent(new Event('input',{bubbles:true}));}")
        after=page.locator(".model-readout").inner_text()
        check(before!=after,"Core1A visual slider does not show a physical change")
        # Independent unfamiliar setting B.
        page.locator("[data-variant='T2']").click()
        root=page.locator('[data-stage-root="'+lesson+'"]')
        check(root.locator(".stage-card h3").inner_text()=="1. Predict","T2 prediction must start locked")
        check(root.locator(".worked").count()==0,"T2 answer present before prediction")
        check(state(page,lesson+"-T2") is None or state(page,lesson+"-T2")["first"] is None,"Uncommitted T2 has a forged first answer")
        prediction="I need the system boundary, assumptions and signed velocities before choosing an equation."
        root.locator('[data-field="prediction"]').fill(prediction)
        root.locator('[data-action="prediction"]').click()
        check(root.locator(".stage-card h3").inner_text()=="2. Attempt","T2 attempt missing")
        check(root.locator(".worked").count()==0,"Solution shown during T2 attempt")
        # Require wrong model + wrong assumption + wrong representation/arithmetic
        # to produce item-specific feedback only AFTER commitment.
        root.locator('[data-field="model"]').select_option(label=wrong_model)
        root.locator('[data-field="assumption"]').select_option(label=wrong_assumption)
        root.locator('[data-field="'+wrong_numeric+'"]').fill(wrong_number)
        reasoning="I chose "+wrong_model+" but need to check why that model applies."
        root.locator('[data-field="reason"]').fill(reasoning)
        for i in range(1,4):
            root.locator('[data-action="hint"]').click()
            check(root.locator(".hint-list li").count()==i,"Progressive hint "+str(i)+" missing")
            check(root.locator(".worked").count()==0,"Worked reconstruction revealed through hint")
            check(root.locator('[data-field="reason"]').input_value()==reasoning,"Hint reset original reasoning")
        check(root.locator('[data-action="hint"]').is_disabled(),"Exposed more than three cues")
        # Switching tasks must not leak a B answer and must not copy B's draft into A.
        page.locator("[data-variant='T1']").click()
        check(root.locator(".stage-card h3").inner_text()=="1. Predict","B state contaminated A")
        check(root.locator(".worked").count()==0,"Switching B→A leaked an answer")
        check(state(page,lesson) is None or state(page,lesson)["first"] is None,"A first answer invented by B work")
        page.locator("[data-variant='T2']").click()
        check(root.locator('[data-field="reason"]').input_value()==reasoning,"B draft lost after switching")
        check(root.locator(".hint-list li").count()==3,"B hint exposure lost after switching")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(page.locator("[data-variant='T2']").get_attribute("aria-pressed")=="true","T2 selection lost on reload")
        check(root.locator('[data-field="reason"]').input_value()==reasoning,"B saved draft lost on reload")
        check(root.locator(".worked").count()==0,"B solution leaked after reload")
        root.locator('[data-action="attempt"]').click()
        check(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","B first attempt not committed")
        Bfirst=state(page,lesson+"-T2")["first"]
        check(Bfirst["answers"]["reason"]==reasoning,"B first reasoning not saved")
        check(Bfirst["answers"]["model"]==wrong_model,"B model choice not frozen")
        check(Bfirst["answers"]["assumption"]==wrong_assumption,"B assumption not frozen")
        check(Bfirst["hintsUsed"]==3 and len(Bfirst["helpHistory"])==3,"Helped B attempt not correctly labeled")
        check(state(page,lesson+"-T2")["exposure"]=="HELPED_BEFORE_FIRST_ATTEMPT","B hint status lost")
        feedback=root.locator(".assessment").inner_text()
        check("MODEL_CHOICE" in feedback,"No specific wrong-model diagnosis")
        check("INVALID_ASSUMPTION" in feedback,"No specific invalid-assumption diagnosis")
        check("SIGN_OR_" in feedback or "SPATIAL_" in feedback or "GEOMETRY_" in feedback or "AREA_AND_RATE_" in feedback or "CALCULATION_OR_UNITS" in feedback,
              "No specific numerical/representation diagnosis")
        check(root.locator(".worked ol li").count()==4,"B worked derivation incomplete")
        # Commit Task A separately with no hints, while preserving B immutable.
        page.locator("[data-variant='T1']").click()
        check(root.locator(".stage-card h3").inner_text()=="1. Predict","A not independent of B")
        root.locator('[data-field="prediction"]').fill("Compare the centre of mass, model limits, and physical operation.")
        root.locator('[data-action="prediction"]').click()
        root.locator('[data-field="model"]').select_option(index=1)
        root.locator('[data-field="assumption"]').select_option(index=1)
        root.locator('[data-field="reason"]').fill("This is my separate Task A first model explanation.")
        root.locator('[data-action="attempt"]').click()
        Afirst=state(page,lesson)["first"]
        check(Afirst is not None and Afirst["hintsUsed"]==0,"A unassisted first attempt not independent")
        check(Afirst["answers"]["reason"]!=""+Bfirst["answers"]["reason"],"A and B attempts copied")
        page.locator("[data-variant='T2']").click()
        check(state(page,lesson+"-T2")["first"]==Bfirst,"B first answer modified by A attempt")
        check(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","B stage reset by A")
        # Diagnose, repair, and attempt physical changed condition before seeing solution.
        root.locator('[data-action="reconstruct"]').click()
        check(root.locator(".stage-card h3").inner_text()=="4. Diagnose","T2 diagnosis not offered")
        root.locator('[data-diagnosis]').select_option("model")
        root.locator('[data-field="why"]').fill("I used the wrong system boundary and physical assumptions.")
        root.locator('[data-action="diagnose"]').click()
        check(root.locator(".stage-card h3").inner_text()=="5. Repair","T2 repair not offered")
        root.locator('[data-field="repair"]').fill("I must identify the right energy owner, sign conventions and limiting conditions.")
        root.locator('[data-action="repair"]').click()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test","T2 transfer boundary skipped")
        check(root.locator(".worked").count()==0,"Boundary answer shown before model commitment")
        root.locator('[data-field="why"]').fill("Changed system conditions require changing the energy or work model.")
        root.locator('[data-action="boundary"]').click()
        check(root.locator(".worked").count()==0,"Blank changed-condition model revealed answer")
        check("Choose the changed-condition physical model" in root.locator('[data-notice]').inner_text(),
              "T2 boundary model gate missing")
        root.locator('[data-field="model"]').select_option(index=2)
        numeric=root.locator('.stage-card input[type="number"][data-field]')
        if numeric.count():numeric.first.fill("999")
        root.locator('[data-action="boundary"]').click()
        check(root.locator(".worked").count()==1,"No B changed-condition check after commitment")
        check(root.locator(".assessment li.review").count()>=1,"Wrong boundary model falsely praised")
        check(state(page,lesson+"-T2")["first"]==Bfirst,"Changed-condition answer overwrote first B attempt")
        check(state(page,lesson)["first"]==Afirst,"Changed-condition B overwrote first A attempt")
        check(page.locator("#transfer-progress-label").inner_text().startswith("1 of 5"),"B completed progress wrong")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test","Committed B stage not recovered")
        check(state(page,lesson+"-T2")["first"]==Bfirst and state(page,lesson)["first"]==Afirst,
              "Separate committed answers not persistent")
        check(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),
              "R3 horizontal overflow at "+str(width))
        # Independently finish original Task A on this SAME device after B.
        # No common gateway or legacy main route selector is assumed here.
        page.locator("[data-variant='T1']").click()
        check(root.locator(".stage-card h3").inner_text()=="3. Reconstruct",
              "Task A committed step changed after Task B completion")
        root.locator('[data-action="reconstruct"]').click()
        check(root.locator(".stage-card h3").inner_text()=="4. Diagnose","A diagnosis stage missing")
        root.locator('[data-diagnosis]').select_option("model")
        root.locator('[data-field="why"]').fill("I checked the separate Task A force/energy owner and assumptions.")
        root.locator('[data-action="diagnose"]').click()
        check(root.locator(".stage-card h3").inner_text()=="5. Repair","A repair stage missing")
        root.locator('[data-field="repair"]').fill("I now know which physical ledger and limiting case to check.")
        root.locator('[data-action="repair"]').click()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test","A boundary stage missing")
        check(root.locator(".worked").count()==0,"Original Task A boundary leaked before attempt")
        boundary_numeric=root.locator('.stage-card input[type="number"][data-field]')
        if boundary_numeric.count():boundary_numeric.first.fill("999")
        root.locator('[data-field="why"]').fill("An altered condition requires a new physical decision and revised calculation.")
        root.locator('[data-action="boundary"]').click()
        check(root.locator(".worked").count()==1,"Original Task A worked boundary not unlocked after attempt")
        check(state(page,lesson)["first"]==Afirst,"Original A first attempt overwritten during repair")
        check(state(page,lesson+"-T2")["first"]==Bfirst,"Original B first attempt overwritten during A repair")
        check(page.locator("#progress-label").inner_text().startswith("1 of 5"),"Original A progress missing")
        page.locator("[data-variant='T2']").click()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test","B stage no longer complete")
        check(state(page,lesson+"-T2")["first"]==Bfirst,"B first attempt changed")
        root.locator(".return-original").first.click()
        check(page.locator(".qtitle").inner_text()==source,"Exact source not recovered after R3")
        check(page.locator("#solution-container .solution").count()==0,"Original source answer automatically revealed")
        check(not errors,"Browser errors "+repr(errors))
        print("PASS R3 "+lesson+" "+source+" two complete six-stage tasks + separate immutable first attempts "+str(width)+"x"+str(height))
    finally:
        context.close()

def main():
    app,base=server()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for screen in ((1280,800),(390,844)):
                    for c in CASES:test_case(browser,base,screen,*c)
            finally:browser.close()
    finally:app.shutdown();app.server_close()

if __name__=="__main__":main()
