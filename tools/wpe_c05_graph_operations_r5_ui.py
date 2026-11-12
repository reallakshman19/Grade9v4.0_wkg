"""C05 R5 real Chromium. Seven graph signatures, two independent six-stage A/B journeys each.
Source candidates stay RELATED_BRIDGE; no original answer is automatically shown.
"""
from __future__ import annotations
from functools import partial
from pathlib import Path
import http.server,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="g9:wpe:c05-r5:v1:"
CASES=[
 ("EX-M11","G5U","Rank potential heights at the vertices"),
 ("EX-M61","G5E","Force is the area under U(x)"),
 ("EX-M69","G5P","Use constant acceleration a=P/m"),
 ("EX-M85","G5V","Area under v(t) is work measured in joules"),
 ("AN-2","G5W","W_by=−∫Fdx always"),
 ("AN-6","G5C","Force depends on y, so it must be conservative"),
 ("JEE-2026-04-06-S2-Q29","G5X","Integrate area directly below v(x) for work")
]
SIZES=((1280,800),(390,844))
def require(condition,message):
    if not condition:raise AssertionError(message)
def serve():
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    server.daemon_threads=True
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,"http://127.0.0.1:"+str(server.server_port)
def storage(page,key):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))",PREFIX+key)
def first(page,key):
    obj=storage(page,key)
    return obj["first"] if obj is not None else None

def make_prediction(root,text):
    root.locator('[data-field="prediction"]').fill(text)
    root.locator('[data-action="prediction"]').click()
    require(root.locator(".stage-card h3").inner_text()=="2. Attempt","Prediction→attempt gate missing")

def wrong_response(root,prefix):
    root.locator('[data-field="model"]').select_option(index=2)
    root.locator('[data-field="assumption"]').select_option(index=2)
    numerics=root.locator('.stage-card input[type="number"][data-field]')
    require(numerics.count()>=1,"No independently assessed numeric graph inference")
    numerics.first.fill("999")
    explanation=prefix+" I chose a tempting model; I need to test which graph operation and conservation rule is physically allowed."
    root.locator('[data-field="reason"]').fill(explanation)
    return explanation

def complete_diagnosis_repair_boundary(root,prefix):
    require(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","Expected committed first response")
    root.locator('[data-action="reconstruct"]').click()
    require(root.locator(".stage-card h3").inner_text()=="4. Diagnose","No diagnosis stage")
    root.locator('[data-diagnosis]').select_option("model")
    root.locator('[data-field="why"]').fill(prefix+" My model lacked the right physical direction, assumption or work term.")
    root.locator('[data-action="diagnose"]').click()
    require(root.locator(".stage-card h3").inner_text()=="5. Repair","No repair stage")
    root.locator('[data-field="repair"]').fill(prefix+" I will specify axes, units, work actor and valid energy/derivative ledger before calculating.")
    root.locator('[data-action="repair"]').click()
    require(root.locator(".stage-card h3").inner_text()=="6. Boundary test","No changed-condition transfer")
    require(root.locator(".worked").count()==0,"Changed-condition worked answer leaked BEFORE commitment")
    root.locator('[data-field="why"]').fill(prefix+" The modified physical condition changes which model or energy term is allowed.")
    root.locator('[data-action="boundary"]').click()
    require(root.locator(".worked").count()==0,"No-model boundary still revealed worked answer")
    require("Choose the changed-condition physical model" in root.locator("[data-notice]").inner_text(),
            "Boundary should require a model choice before worked solution")
    root.locator('[data-field="model"]').select_option(index=2)
    nums=root.locator('.stage-card input[type="number"][data-field]')
    require(nums.count()>=1,"Boundary lacks numeric or feasible-energy witness")
    nums.first.fill("999")
    root.locator('[data-action="boundary"]').click()
    require(root.locator(".worked").count()==1,"Committed boundary failed to reveal physical reconstruction")
    require(root.locator(".assessment li.review").count()>=1,"Incorrect chosen model/number falsely praised")
    require(root.locator(".stage-card h3").inner_text()=="6. Boundary test","Stage moved on after boundary")

def journey(browser,base,size,source,code,bad_choice):
    width,height=size
    ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    errors=[]
    try:
        page=ctx.new_page()
        page.on("pageerror",lambda e:errors.append(str(e)))
        url=base+"/physics/wpe/c05-graph-constructions-r5.html?source="+source+"#"+code
        page.goto(url,wait_until="load")
        page.locator("#candidate-source:not([hidden])").wait_for(timeout=15000)
        return_link=page.locator("#candidate-source-return")
        return_link.wait_for(state="visible",timeout=15000)
        require(return_link.get_attribute("href").endswith("question="+source),"Wrong original source return")
        require("RELATED" in page.locator("#candidate-source-message").inner_text(),
                "Candidate route promoted without academic authority")
        require(page.locator(".guide-steps li").count()==5,"Incomplete Core1A worked teaching")
        require(page.locator(".academic-observations dt").count()==3,"No observed model validity/limit conditions")
        require(page.locator(".guide svg").count()==1,"Missing scientific model illustration")
        require(page.locator(".worked").count()==0,"Core1B answer leaked at load")
        before=page.locator(".model-readout").inner_text()
        page.locator("#guide-slider").evaluate("(n)=>{n.value=n.min;n.dispatchEvent(new Event('input',{bubbles:true}));}")
        after=page.locator(".model-readout").inner_text()
        require(before!=after,"Physical model visualization did not respond")
        require(page.locator("[data-variant='T1']").get_attribute("aria-pressed")=="true",
                "Original Task A not default")
        root=page.locator('[data-stage-root="'+code+'"]')
        require(root.locator(".stage-card h3").inner_text()=="1. Predict","Initial prediction stage missing")
        root.locator('[data-action="prediction"]').click()
        require(root.locator(".stage-card h3").inner_text()=="1. Predict",
                "Blank prediction passed attempt protection")
        make_prediction(root,"A: I will compare graph axes, signed operations and model preconditions before substituting.")
        require(root.locator(".worked").count()==0,"Worked Task A shown before attempt")
        root.locator('[data-action="attempt"]').click()
        require(root.locator(".stage-card h3").inner_text()=="2. Attempt","Blank Task A attempt committed")
        Atext=wrong_response(root,"Task A")
        root.locator('[data-action="attempt"]').click()
        require(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","Task A not committed")
        Afirst=first(page,code)
        require(Afirst and Afirst["answers"]["reason"]==Atext,"Original A first answer was not frozen")
        require(Afirst["hintsUsed"]==0,"Original A should have no pre-answer help")
        require(root.locator(".worked ol li").count()==4,"Incomplete Task A worked steps")
        require("MODEL_CHOICE" in root.locator(".assessment").inner_text(),"A wrong-model feedback missing")
        require("INVALID_ASSUMPTION" in root.locator(".assessment").inner_text(),"A assumption feedback missing")
        # B begins entirely fresh, not inheriting A's answer or stage.
        page.locator("[data-variant='T2']").click()
        require(root.locator(".stage-card h3").inner_text()=="1. Predict","B inherited A's stage")
        require(first(page,code+"-T2") is None,"B initial answer was fabricated from A")
        require(root.locator(".worked").count()==0,"Worked B leaked before first commitment")
        make_prediction(root,"B: an unfamiliar setting changes model conditions, not just its numerical constants.")
        Btext=wrong_response(root,"Task B")
        for count in (1,2,3):
            root.locator('[data-action="hint"]').click()
            require(root.locator(".hint-list li").count()==count,"Hint exposure not incremental")
            require(root.locator(".worked").count()==0,"A hint exposed Task B's full solution")
            require(root.locator('[data-field="reason"]').input_value()==Btext,"Hint erased written thinking")
        require(root.locator('[data-action="hint"]').is_disabled(),"More than 3 cues allowed")
        # Switch and reload—distinct first records and drafts must not leak across tasks.
        page.locator("[data-variant='T1']").click()
        require(first(page,code)==Afirst,"Task B altered A first response")
        require(root.locator(".stage-card h3").inner_text()=="3. Reconstruct","A stage lost after task switch")
        page.locator("[data-variant='T2']").click()
        require(root.locator(".stage-card h3").inner_text()=="2. Attempt","B draft not restored")
        require(root.locator('[data-field="reason"]').input_value()==Btext,"B draft not recovered")
        page.reload(wait_until="load")
        page.locator("#candidate-source-return").wait_for(state="visible",timeout=15000)
        require(page.locator("[data-variant='T2']").get_attribute("aria-pressed")=="true",
                "B selected task lost on reload")
        require(root.locator(".worked").count()==0,"Reload leaked B answer")
        require(root.locator('[data-field="reason"]').input_value()==Btext,"B saved draft lost")
        root.locator('[data-action="attempt"]').click()
        Bfirst=first(page,code+"-T2")
        require(Bfirst is not None and Bfirst["answers"]["reason"]==Btext,"B first thinking missing")
        require(Bfirst["hintsUsed"]==3 and len(Bfirst["helpHistory"])==3,"B optional cue history missing")
        require(storage(page,code+"-T2")["exposure"]=="HELPED_BEFORE_FIRST_ATTEMPT","Hinted task marked independent")
        feedback=root.locator(".assessment").inner_text()
        require("MODEL_CHOICE" in feedback and "INVALID_ASSUMPTION" in feedback,
                "B wrong model and invalid assumption not specifically diagnosed")
        require(root.locator(".worked ol li").count()==4,"B worked derivation incomplete")
        complete_diagnosis_repair_boundary(root,"Task B")
        require(first(page,code+"-T2")==Bfirst and first(page,code)==Afirst,
                "B changed-condition result overwrote first attempt")
        require(page.locator("#transfer-progress-label").inner_text().startswith("1 of 7"),
                "B completion not represented separately")
        # A must still reach its own boundary without reusing B work.
        page.locator("[data-variant='T1']").click()
        complete_diagnosis_repair_boundary(root,"Task A")
        require(first(page,code)==Afirst and first(page,code+"-T2")==Bfirst,
                "A completion overwrote independent task first response")
        require(page.locator("#progress-label").inner_text().startswith("1 of 7"),
                "A completion progress missing")
        # Finally both six-stage completions persist through refresh.
        page.reload(wait_until="load")
        page.locator("#candidate-source-return").wait_for(state="visible",timeout=15000)
        require(first(page,code)==Afirst and first(page,code+"-T2")==Bfirst,
                "Separate A/B first attempts lost on reload")
        require(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),
                "Unacceptable horizontal overflow at "+str(width))
        page.locator("#candidate-source-return").click()
        page.locator(".qtitle").wait_for(timeout=15000)
        require(page.locator(".qtitle").inner_text()==source,"Original exact question identity lost")
        require(page.locator("#solution-container .solution").count()==0,
                "Question Bank original answer automatically revealed")
        require(not errors,"Uncaught page JavaScript errors "+repr(errors))
        print("PASS "+code+" "+source+" Task A+B distinct 6-stage paths, related-only source return without answered source "+str(width)+"x"+str(height))
    finally:
        ctx.close()

def refusals(browser,base,size):
    width,height=size
    context=browser.new_context(viewport={"width":width,"height":height})
    try:
        page=context.new_page()
        for source,code in (
            ("EX-M6","G5U"), # other-family question cannot be promoted
            ("UNKNOWN","G5E"),
            ("EX-M11","G5V"), # correct source but WRONG graph signature
        ):
            page.goto(base+"/physics/wpe/c05-graph-constructions-r5.html?source="+source+"#"+code)
            page.locator("#candidate-source:not([hidden])").wait_for()
            require(page.locator("#candidate-source-return").is_hidden(),
                    "Invented a source link for unqualified or mismatched candidate "+source)
        print("PASS source-custody refusals including EX-M6 and mismatched graph models "+str(width)+"x"+str(height))
    finally:
        context.close()

def main():
    app,base=serve()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for size in SIZES:
                    for source,code,wrong in CASES:journey(browser,base,size,source,code,wrong)
                    refusals(browser,base,size)
            finally:browser.close()
    finally:app.shutdown();app.server_close()
if __name__=="__main__":main()
