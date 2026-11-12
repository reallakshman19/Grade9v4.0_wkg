"""Chromium end-to-end: source → Core1A → different Core1B → source.

Desktop/mobile and three physics cases, plus full 74-question coverage.
Automated actions are NOT a real child's independently observed reasoning.
"""
from __future__ import annotations
from functools import partial
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
CASES=(
    ("EX-M97","F01","Net force T − mg","cablePower","86"),
    ("EX-N39","F02","Gravity and friction each cancel","mu","0.1"),
    ("WEP07-01","F03","Old equilibrium position","turn","-0.15"),
)
VIEWPORTS=((1280,800),(390,844))

def check(ok,msg):
    if not ok:raise AssertionError(msg)

def server():
    app=http.server.ThreadingHTTPServer(("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    app.daemon_threads=True
    threading.Thread(target=app.serve_forever,daemon=True).start()
    return app,"http://127.0.0.1:"+str(app.server_port)

def local(page,lesson):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))","g9:wpe:focused:v1:"+lesson)

def full_journey(browser,base,width,height,source,lesson,wrong_model,wrong_field,wrong_number):
    context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    try:
        page=context.new_page()
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base+"/preview/question-status.html?question="+source,wait_until="load")
        check(page.locator(".qtitle").inner_text()==source,lesson+" wrong original question")
        check(page.locator("#solution-container .solution").count()==0,lesson+" source answer revealed before attempt")
        direct=page.locator('#interactive-lesson-links a[href*="focused-journeys.html?question='+source+'#'+lesson+'"]')
        direct.wait_for(timeout=15000)
        check(direct.count()==1,lesson+" lacks a direct Question Bank link")
        direct.click()
        check(page.url.endswith("focused-journeys.html?question="+source+"#"+lesson),lesson+" source ID lost")
        page.locator("#source-journey:not([hidden])").wait_for(timeout=15000)
        check(page.locator("#source-return").get_attribute("href").endswith("question="+source),lesson+" return ID wrong")
        check(page.locator(".guide-steps li").count()==5,lesson+" teaching steps incomplete")
        guide=page.locator(".guide")
        check(guide.locator("svg").count()==1,lesson+" diagram missing")
        before=guide.locator(".model-readout").inner_text()
        guide.locator("#guide-slider").evaluate("(x)=>{x.value=x.min;x.dispatchEvent(new Event('input',{bubbles:true}));}")
        check(guide.locator(".model-readout").inner_text()!=before,lesson+" physics control does not change explanation")
        check(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),lesson+" horizontal overflow "+str(width))
        root=page.locator('[data-stage-root="'+lesson+'"]')
        check(root.locator(".stage-card h3").inner_text()=="1. Predict",lesson+" missing Predict")
        check(root.locator(".worked").count()==0,lesson+" worked answer leaked pre-attempt")
        root.locator('[data-action="prediction"]').click()
        check(root.locator(".stage-card h3").inner_text()=="1. Predict",lesson+" empty prediction accepted")
        root.locator('[data-field="prediction"]').fill("I predict this needs a specific force/energy model, but I need to test it.")
        root.locator('[data-action="prediction"]').click()
        check(root.locator(".stage-card h3").inner_text()=="2. Attempt",lesson+" missing Attempt")
        root.locator('[data-action="attempt"]').click()
        check(root.locator(".stage-card h3").inner_text()=="2. Attempt",lesson+" blank attempt accepted")
        root.locator('[data-field="model"]').select_option(label=wrong_model)
        root.locator('[data-field="'+wrong_field+'"]').fill(wrong_number)
        first_reason="My first physical model is "+wrong_model+". I am comparing forces and conditions before the calculation."
        root.locator('[data-field="reason"]').fill(first_reason)
        for number in range(1,4):
            root.locator('[data-action="hint"]').click()
            check(root.locator(".hint-list li").count()==number,lesson+" cue count wrong")
            check(root.locator(".worked").count()==0,lesson+" hint leaked fresh worked key")
            check(root.locator('[data-field="reason"]').input_value()==first_reason,lesson+" hint wiped the attempt")
        check(root.locator('[data-action="hint"]').is_disabled(),lesson+" cue beyond three")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(root.locator(".hint-list li").count()==3,lesson+" cues not restored")
        check(root.locator('[data-field="reason"]').input_value()==first_reason,lesson+" draft not persisted")
        check(root.locator('[data-field="model"]').input_value()==wrong_model,lesson+" model decision not persisted")
        root.locator('[data-action="attempt"]').click()
        check(root.locator(".stage-card h3").inner_text()=="3. Reconstruct",lesson+" wrong reconstruction stage")
        initial=local(page,lesson)["first"]
        check(initial["answers"]["reason"]==first_reason,lesson+" reasoning not frozen")
        check(initial["hintsUsed"]==3,lesson+" hints exposure not saved")
        check(len(initial["helpHistory"])==3,lesson+" hint order missing")
        check(local(page,lesson)["exposure"]=="HELPED_BEFORE_FIRST_ATTEMPT",lesson+" assisted attempt mislabeled")
        check(root.locator(".worked ol li").count()==4,lesson+" worked model incomplete")
        feedback=root.locator(".assessment").inner_text()
        check("Review this step" in feedback,lesson+" feedback not grounded in wrong model")
        if lesson=="F01":check("cable" in feedback.lower() and "net" in feedback.lower(),lesson+" missing applied/net distinction")
        if lesson=="F02":check("friction" in feedback.lower() and "both" in feedback.lower(),lesson+" missing two-leg correction")
        if lesson=="F03":check("instantaneously" in feedback.lower() or "force switch" in feedback.lower(),lesson+" missing switch continuity")
        root.locator('[data-action="reconstruct"]').click()
        check(root.locator(".stage-card h3").inner_text()=="4. Diagnose",lesson+" Diagnose missing")
        root.locator('[data-diagnosis]').select_option("model")
        root.locator('[data-field="why"]').fill("I selected the wrong force or energy model at the first step.")
        root.locator('[data-action="diagnose"]').click()
        check(root.locator(".stage-card h3").inner_text()=="5. Repair",lesson+" Repair missing")
        check(first_reason in root.locator(".snapshot").inner_text(),lesson+" original invisible while repairing")
        root.locator('[data-field="repair"]').fill("I corrected the first model choice and can now justify the equations from the physical conditions.")
        root.locator('[data-action="repair"]').click()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test",lesson+" boundary stage missing")
        check(root.locator(".stage-card .worked").count()==0,lesson+" changed-condition solution revealed early")
        root.locator('[data-action="boundary"]').click()
        check(root.locator(".worked").count()==0,lesson+" blank boundary worked response accepted")
        boundary_number=root.locator('[data-field]:not(textarea)').first
        boundary_number.fill("999")
        root.locator('[data-field="why"]').fill("The changed condition alters this physical term, so my new numerical prediction needs checking.")
        root.locator('[data-action="boundary"]').click()
        check(root.locator(".stage-card .worked").count()==1,lesson+" boundary check absent")
        check(root.locator(".assessment li.review").count()>=1,lesson+" changed-condition feedback not tied to wrong number")
        check(local(page,lesson)["first"]==initial,lesson+" first attempt overwritten")
        check(local(page,lesson)["boundary"]["why"],lesson+" boundary reasoning not saved")
        check(page.locator("#progress-label").inner_text().startswith("1 of 6"),lesson+" progress not updated")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(root.locator(".stage-card h3").inner_text()=="6. Boundary test",lesson+" boundary stage not persistent")
        check(local(page,lesson)["first"]==initial,lesson+" original attempt changed after reload")
        root.locator('[data-action="history"]').click()
        check(first_reason in root.locator(".history").inner_text(),lesson+" original reasoning not recoverable")
        root.locator(".return-original").first.click()
        check(page.locator(".qtitle").inner_text()==source,lesson+" wrong original on return")
        check(page.locator("#solution-container .solution").count()==0,lesson+" original answer automatically revealed")
        check(not errors,lesson+" JavaScript errors: "+repr(errors))
        print("PASS "+lesson+" "+source+" full six stages at "+str(width)+"x"+str(height))
    finally:
        context.close()

def coverage_and_bridges(browser,base,width,height):
    context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    try:
        page=context.new_page();errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base+"/physics/wpe/learn-challenge.html?question=EX-M97#question-routes")
        plan=page.locator("#question-plan h3");plan.wait_for()
        check("EX-M97" in plan.inner_text(),"Tile did not select exact question")
        check(page.locator('#question-plan a[href*="focused-journeys.html?question=EX-M97#F01"]').count()==1,"Tile lacks F01")
        check("net" in page.locator("#question-plan").inner_text().lower(),"Source ambiguity not explained")
        page.locator("#question-pick").select_option("EX-M96")
        check("EX-M96" in plan.inner_text(),"Question selector did not change")
        check("F06" in page.locator("#question-plan").inner_text(),"Wind energy flow lesson not connected")
        check(page.locator("#question-plan .primary-link").count()==1,"Exact-source wind lesson missing")
        page.locator("#question-pick").select_option("EX-M11")
        check("C05" in page.locator("#question-plan").inner_text(),"Related C05 bridge missing")
        bridge=page.locator('#question-plan .primary-link')
        check("d3d4-self-tutor.html?question=EX-M11#C05" in bridge.get_attribute("href"),"Wrong direct source-bound URL")
        bridge.click()
        check(page.url.endswith("d3d4-self-tutor.html?question=EX-M11#C05"),"Existing C05 lesson not reached directly")
        check(page.locator("iframe").count()==0,"Iframe embedding is prohibited")
        page.locator("#source-journey:not([hidden])").wait_for()
        check("EX-M11" in page.locator("#source-journey-title").inner_text(),"Related source ID lost")
        page.locator("#source-journey-return").click()
        check(page.locator(".qtitle").inner_text()=="EX-M11","Related bridge return wrong")
        check(page.locator("#solution-container .solution").count()==0,"Bridge revealed source answer")
        page.goto(base+"/physics/wpe/question-coverage.html")
        page.locator("#table-status").filter(has_text="74 of 74").wait_for()
        check(page.locator("#rows tr").count()==74,"Not 74 exact coverage entries")
        for f,n in (("focused",8),("targeted",18),("related",48),("missing",0)):
            page.locator("#filter").select_option(f)
            check(page.locator("#rows tr").count()==n,f+" expected "+str(n))
        page.locator("#filter").select_option("all")
        page.locator("#search").fill("EX-M101")
        check(page.locator("#rows tr").count()==1,"Spring control source not unique")
        entry=page.locator("#rows tr").inner_text()
        check("equal final equilibrium force" in entry and "equal extension" in entry,"Spring source teaching mismatch")
        page.locator("#search").fill("EX-M79")
        check("speed–distance" in page.locator("#rows tr").inner_text(),"EX-M79 source reasoning lost")
        check(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),"Mobile coverage horizontal overflow")
        # Wrong source/lesson pairing must never invent a return link.
        page.goto(base+"/physics/wpe/focused-journeys.html?question=EX-M97#F02")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(page.locator("#source-return").is_hidden(),"Mismatched lesson returned to EX-M97")
        page.goto(base+"/physics/wpe/focused-journeys.html?question=UNKNOWN-ID#F01")
        page.locator("#source-journey:not([hidden])").wait_for()
        check(page.locator("#source-return").is_hidden(),"Unknown ID created a phantom return")
        check(not errors,"Supplementary browser errors: "+repr(errors))
        print("PASS 74-question coverage, new/related/missing fit, bridge and mismatch refusal "+str(width))
    finally:
        context.close()

def main():
    app,base=server()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for width,height in VIEWPORTS:
                    for args in CASES:
                        full_journey(browser,base,width,height,*args)
                    coverage_and_bridges(browser,base,width,height)
            finally:
                browser.close()
    finally:
        app.shutdown();app.server_close()

if __name__=="__main__":
    main()
