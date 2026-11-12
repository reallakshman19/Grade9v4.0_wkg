"""WPE R2 actual Chromium: five source-bound unfamiliar six-stage challenges.

Desktop 1280px and mobile 390px: source to guided construction to independent
model choice, help exposure, attempt, response-grounded feedback, repair,
changed condition, reload and exact original question without answer reveal.
"""
from __future__ import annotations
from functools import partial
import http.server
import threading
from playwright.sync_api import sync_playwright

ROOT=__import__("pathlib").Path(__file__).resolve().parents[1]
CASE_DATA=(
  ("EX-M50","F04","Total kinetic energy of both blocks","extension","1"),
  ("EX-M92","F05","Every coil moves at the tip speed","energy","12"),
  ("EX-M96","F06","A fixed packet of mass with energy∝v² only","output","200"),
  ("EX-M106","F07","Both require static tangential balance","constant","30"),
  ("EX-N27","F08","Automatically 10% of their total kinetic energy","compression","1.5"),
)
SIZES=((1280,800),(390,844))
PREFIX="g9:wpe:gaps:v2:"

def require(condition,message):
    if not condition:raise AssertionError(message)

def serve():
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT))
    )
    server.daemon_threads=True
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,"http://127.0.0.1:"+str(server.server_port)

def record(page,lesson):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))",PREFIX+lesson)

def journey(browser,base,width,height,source,lesson,wrong_model,wrong_field,wrong_number):
    ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    try:
        page=ctx.new_page();errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base+"/preview/question-status.html?question="+source,wait_until="load")
        require(page.locator(".qtitle").inner_text()==source,"Initial Question Bank identity wrong")
        require(page.locator("#solution-container .solution").count()==0,source+" original answer leaked")
        jump=page.locator('#interactive-lesson-links a[href*="gap-journeys.html?question='+source+'#'+lesson+'"]')
        jump.wait_for(timeout=16000)
        require(jump.count()==1,source+" lacks a single direct source-to-learning link")
        jump.click()
        require(page.url.endswith("gap-journeys.html?question="+source+"#"+lesson),source+" misrouted")
        page.locator(".lesson-title").wait_for(timeout=15000)
        require(page.locator(".lesson-title").count()==1,
                "New journey failed to initialize: "+repr(errors)+" body="+page.locator("body").inner_text()[:400])
        require(not errors,"New journey page errors: "+repr(errors))
        page.locator("#source-journey:not([hidden])").wait_for(timeout=15000)
        require(page.locator("#source-return").get_attribute("href").endswith("question="+source),
                "Wrong return target")
        require(page.locator(".guide-steps li").count()==5,"Incomplete Core1A guided derivation")
        guide=page.locator(".guide")
        require(guide.locator("svg").count()==1,"Missing physics diagram")
        original=guide.locator(".model-readout").inner_text()
        guide.locator("#guide-slider").evaluate(
            "(n)=>{n.value=n.min;n.dispatchEvent(new Event('input',{bubbles:true}));}"
        )
        changed=guide.locator(".model-readout").inner_text()
        require(changed!=original,"Interactive visual model did not update")
        require(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),
                "Horizontal overflow at "+str(width))
        root=page.locator('[data-stage-root="'+lesson+'"]')
        require(root.locator(".stage-card h3").inner_text()=="1. Predict","Predict not first")
        require(root.locator(".worked").count()==0,"Solution showed before learner's attempt")
        root.locator('[data-action="prediction"]').click()
        require(root.locator(".stage-card h3").inner_text()=="1. Predict","Empty prediction passed")
        prediction="I want to choose the energy owner before applying any memorized formula."
        root.locator('[data-field="prediction"]').fill(prediction)
        root.locator('[data-action="prediction"]').click()
        require(root.locator(".stage-card h3").inner_text()=="2. Attempt","Attempt gate wrong")
        root.locator('[data-action="attempt"]').click()
        require(root.locator(".stage-card h3").inner_text()=="2. Attempt","Empty initial attempt accepted")
        root.locator('[data-field="model"]').select_option(label=wrong_model)
        root.locator('[data-field="'+wrong_field+'"]').fill(wrong_number)
        reason="First reasoning: "+wrong_model+"; I need to check the boundary and the assumptions."
        root.locator('[data-field="reason"]').fill(reason)
        for index in range(1,4):
            root.locator('[data-action="hint"]').click()
            require(root.locator(".hint-list li").count()==index,"Progressive hint not shown")
            require(root.locator(".worked").count()==0,"Fresh solution leaked during hints")
            require(root.locator('[data-field="reason"]').input_value()==reason,"Hint erased own reasoning")
        require(root.locator('[data-action="hint"]').is_disabled(),"Additional hint beyond 3")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for(timeout=15000)
        require(root.locator(".hint-list li").count()==3,"Hint history not recovered on reload")
        require(root.locator('[data-field="reason"]').input_value()==reason,"Draft work lost on reload")
        require(root.locator('[data-field="model"]').input_value()==wrong_model,"Model not restored")
        root.locator('[data-action="attempt"]').click()
        require(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","Reconstruction missing")
        first=record(page,lesson)["first"]
        require(first["answers"]["reason"]==reason,"Immutable first attempt not captured")
        require(first["hintsUsed"]==3 and len(first["helpHistory"])==3,"Hint assistance not recorded")
        require(record(page,lesson)["exposure"]=="HELPED_BEFORE_FIRST_ATTEMPT",
                "Helped attempt mislabeled independent")
        require(root.locator(".worked ol li").count()==4,"Worked explanation not complete")
        feedback=root.locator(".assessment").inner_text()
        require("Review this step" in feedback,"Feedback not based on wrong first response")
        if lesson=="F04": require("centre-of-mass" in feedback.lower() or "relative" in feedback.lower(),"F04 model diagnosis poor")
        if lesson=="F05": require("fixed" in feedback.lower() or "affine" in feedback.lower(),"F05 model diagnosis poor")
        if lesson=="F06": require("moving" in feedback.lower() or "longer" in feedback.lower(),"F06 model diagnosis poor")
        if lesson=="F07": require("turning" in feedback.lower() or "equilibrium" in feedback.lower(),"F07 model diagnosis poor")
        if lesson=="F08": require("relative" in feedback.lower() or "dissipation" in feedback.lower(),"F08 model diagnosis poor")
        root.locator('[data-action="reconstruct"]').click()
        require(root.locator(".stage-card h3").inner_text()=="4. Diagnose","Diagnosis skipped")
        root.locator('[data-diagnosis]').select_option("model")
        root.locator('[data-field="why"]').fill("I used a source-independent shortcut rather than checking this situation's actual model.")
        root.locator('[data-action="diagnose"]').click()
        require(root.locator(".stage-card h3").inner_text()=="5. Repair","Repair skipped")
        require(reason in root.locator(".snapshot").inner_text(),"Repair did not show preserved first work")
        root.locator('[data-field="repair"]').fill(
            "I now identify the correct energy owner, constraints and phase, then build the governing relation."
        )
        root.locator('[data-action="repair"]').click()
        require(root.locator(".stage-card h3").inner_text()=="6. Boundary test","Boundary transfer not offered")
        require(root.locator(".worked").count()==0,"Boundary answer shown before changed-condition attempt")
        root.locator('[data-action="boundary"]').click()
        require(root.locator(".worked").count()==0,"Blank boundary response exposed solution")
        root.locator('[data-field]:not(textarea)').first.fill("999")
        root.locator('[data-field="why"]').fill("Under the changed physical condition, the initial shortcut no longer applies unchanged.")
        root.locator('[data-action="boundary"]').click()
        require(root.locator(".worked").count()==1,"No boundary worked explanation")
        require(root.locator(".assessment li.review").count()>=1,
                "Incorrect changed-condition numerical answer was praised")
        require(record(page,lesson)["first"]==first,"Original independent model overwritten")
        require(record(page,lesson)["boundary"]["why"],"Changed-condition thinking not stored")
        require(page.locator("#progress-label").inner_text().startswith("1 of 5"),
                "Gap-closure progress not tied to actual changed-condition attempt")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        require(root.locator(".stage-card h3").inner_text()=="6. Boundary test","Committed stage did not persist")
        require(record(page,lesson)["first"]==first,"First attempt changed after reload")
        root.locator('[data-action="history"]').click()
        require(reason in root.locator(".history").inner_text(),"First reasoning not recoverable")
        root.locator(".return-original").first.click()
        require(page.locator(".qtitle").inner_text()==source,"Source identity lost on return")
        require(page.locator("#solution-container .solution").count()==0,"Original source key revealed automatically")
        require(not errors,"JS page errors: "+repr(errors))
        print("PASS "+lesson+" "+source+" 6-stage guided + unfamiliar boundary + exact return "+str(width)+"x"+str(height))
    finally:
        ctx.close()

def global_navigation(browser,base,width,height):
    ctx=browser.new_context(viewport={"width":width,"height":height})
    try:
        page=ctx.new_page();errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base+"/physics/wpe/learn-challenge.html?question=EX-M50#question-routes")
        title=page.locator("#question-plan h3");title.wait_for()
        for q,lesson,*_ in CASE_DATA:
            page.locator("#question-pick").select_option(q)
            require(q in title.inner_text(),q+" not selectable by exact source ID")
            link=page.locator("#question-plan .primary-link")
            require(link.count()==1,q+" missing source-bound primary learning link")
            require("gap-journeys.html?question="+q+"#"+lesson in link.get_attribute("href"),
                    q+" wrong primary challenge")
        page.goto(base+"/physics/wpe/question-coverage.html")
        page.locator("#table-status").filter(has_text="74 of 74").wait_for()
        require(page.locator("#rows tr").count()==74,"74-entry coverage missing")
        for cat,n in (("focused",8),("targeted",18),("related",48),("missing",0)):
            page.locator("#filter").select_option(cat)
            require(page.locator("#rows tr").count()==n,cat+" count mismatched")
        page.locator("#filter").select_option("all")
        page.locator("#search").fill("EX-M106")
        require(page.locator("#rows tr").count()==1,"EX-M106 coverage duplicate")
        note=page.locator("#rows tr").inner_text()
        require("static" in note.lower() and "turning" in note.lower(),
                "Ambiguous pendulum source wording was hidden")
        page.locator("#search").fill("EX-N27")
        require(page.locator("#rows tr").count()==1,"EX-N27 coverage duplicate")
        note=page.locator("#rows tr").inner_text()
        require("whole-system" in note.lower() and "two-body" in note.lower(),
                "Conditional shock-absorber model hidden")
        # No false source association when the selected lesson doesn't belong to ID.
        page.goto(base+"/physics/wpe/gap-journeys.html?question=EX-M50#F05")
        page.locator("#source-journey:not([hidden])").wait_for()
        require(page.locator("#source-return").is_hidden(),"Mismatched lesson created a fake source return")
        page.goto(base+"/physics/wpe/gap-journeys.html?question=UNKNOWN-ID#F04")
        page.locator("#source-journey:not([hidden])").wait_for()
        require(page.locator("#source-return").is_hidden(),"Unknown source returned to fake question")
        require(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),
                "Gap lesson overflow on "+str(width))
        require(not errors,"Global JS errors: "+repr(errors))
        print("PASS 74 exact route coverage and two source ambiguities at "+str(width)+"px")
    finally:
        ctx.close()

def main():
    server,base=serve()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for width,height in SIZES:
                    for q in CASE_DATA:journey(browser,base,width,height,*q)
                    global_navigation(browser,base,width,height)
            finally:browser.close()
    finally:server.shutdown();server.server_close()

if __name__=="__main__":main()
