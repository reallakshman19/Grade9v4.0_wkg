"""Real Chromium, desktop and mobile: Question -> extension -> new challenge -> Question.

Exercises all five independent six-stage student journeys and keeps the old
C01-C08/browser suites untouched. These are automated interactions, not claims
of real child testing or scientific approval.
"""
from __future__ import annotations
from functools import partial
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
VIEWPORTS=((1280,800),(390,844))
SOURCES={
    "E01":["WEP07-03","EX-M109"],
    "E02":["TB-WPE-ILL-05","TB-WPE-ILL-06"],
    "E03":["EX-N34"],
    "E04":["EX-M82"],
    "E05":["EX-M89"],
}
PROMPT={
    "E01":"Both valleys look low. I am testing whether the middle lets me walk all the way across.",
    "E02":"I think the backward force acts against the forward velocity so I need a negative contribution.",
    "E03":"I will stop counting spring force at the contact boundary, then find projectile flight time.",
    "E04":"I will change the retained fraction after impact one and count each rise and fall.",
    "E05":"I need the area for potential change and the force height for inward acceleration.",
}

def require(ok,msg):
    if not ok:raise AssertionError(msg)

def server():
    svc=http.server.ThreadingHTTPServer(("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    svc.daemon_threads=True
    threading.Thread(target=svc.serve_forever,daemon=True).start()
    return svc,"http://127.0.0.1:"+str(svc.server_port)

def state(page,lesson):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))","g9:wpe:extensions:v1:"+lesson)

def round_trip(page,base,lesson,source):
    # Existing Question Bank answer protection must still apply.
    page.goto(base+"/preview/question-status.html?question="+source,wait_until="load")
    require(page.locator(".qtitle").inner_text()==source,lesson+": source ID missing")
    require(page.locator("#solution-container .solution").count()==0,lesson+": original solution exposed")
    page.locator('a[href*="reasoning-paths.html?question="]').first.click()
    require("reasoning-paths.html?question="+source in page.url,lesson+": exact ID lost on route")
    card=page.locator("#WPE-"+lesson)
    link=card.locator('a[href*="extension-learning.html?question='+source+'#'+lesson+'"]')
    link.wait_for(timeout=10000)
    require(link.count()==1,lesson+": extension source-bound route absent")
    link.click()
    require(page.url.endswith("extension-learning.html?question="+source+"#"+lesson),lesson+": wrong destination")
    page.locator("#source-journey:not([hidden])").wait_for()
    require(page.locator("#source-return").get_attribute("href").endswith("question="+source),lesson+": return link ID changed")
    require(page.locator('[data-stage-root="'+lesson+'"]').count()==1,lesson+": missing stage root")
    guide=page.locator(".guide")
    require(guide.locator(".guide-steps li").count()==5,lesson+": incomplete Core1A")
    require(guide.locator("svg").count()==1 and guide.locator(".visual-controls input").count()==1,lesson+": interactive diagram missing")
    slider=guide.locator("#guide-slider")
    original=guide.locator(".model-readout").inner_text()
    slider.evaluate("(el)=>{el.value=el.value===el.min?el.max:el.min;el.dispatchEvent(new Event(\'input\',{bubbles:true}));}")
    require(guide.locator(".model-readout").inner_text()!=original,lesson+": visual not interactive")
    require(page.evaluate("document.documentElement.scrollWidth<=window.innerWidth+3"),lesson+": horizontal page overflow")
    root=page.locator('[data-stage-root="'+lesson+'"]')
    require(root.locator(".stage-card h3").inner_text()=="1. Predict",lesson+": no prediction")
    require(root.locator(".worked").count()==0,lesson+": fresh solution visible before attempt")
    root.locator('[data-action="save-prediction"]').click()
    require(root.locator(".stage-card h3").inner_text()=="1. Predict",lesson+": blank prediction accepted")
    root.locator('[data-field="prediction"]').fill("I will predict the result, then check the model boundary.")
    root.locator('[data-action="save-prediction"]').click()
    require(root.locator(".stage-card h3").inner_text()=="2. Attempt",lesson+": no independent attempt")
    require(root.locator(".worked").count()==0,lesson+": worked key pre-attempt")
    root.locator('[data-action="save-attempt"]').click()
    require(root.locator(".stage-card h3").inner_text()=="2. Attempt",lesson+": blank reasoning accepted")
    root.locator('[data-field="reason"]').fill(PROMPT[lesson])
    # Hints must not overwrite the attempt or leak the worked reconstruction.
    for n in range(1,4):
        root.locator('[data-action="hint"]').click()
        require(root.locator(".hint-list li").count()==n,lesson+": hint progression "+str(n))
        require(root.locator(".worked").count()==0,lesson+": answer leaked with hint")
        require(root.locator('[data-field="reason"]').input_value()==PROMPT[lesson],lesson+": hint erased reasoning")
    require(root.locator('[data-action="hint"]').is_disabled(),lesson+": extra hint enabled")
    page.reload(wait_until="load")
    page.locator("#source-journey:not([hidden])").wait_for()
    require(root.locator(".hint-list li").count()==3,lesson+": hints not restored")
    require(root.locator('[data-field="reason"]').input_value()==PROMPT[lesson],lesson+": original draft not preserved on reload")
    root.locator('[data-action="save-attempt"]').click()
    require(root.locator(".stage-card h3").inner_text()=="3. Reconstruct",lesson+": worked model not unlocked")
    original_first=state(page,lesson)["first"]
    require(original_first["reason"]==PROMPT[lesson],lesson+": first reasoning changed")
    require(root.locator(".worked ol li").count()==4,lesson+": worked reconstruction incomplete")
    root.locator('[data-action="save-check"]').click()
    require(root.locator(".stage-card h3").inner_text()=="4. Diagnose",lesson+": diagnosis stage missing")
    root.locator('[data-diagnosis]').select_option("0")
    root.locator('[data-field="why"]').fill("I need to review which quantity or boundary I selected.")
    root.locator('[data-action="save-diagnosis"]').click()
    require(root.locator(".stage-card h3").inner_text()=="5. Repair",lesson+": repair missing")
    require(PROMPT[lesson] in root.locator(".snapshot").inner_text(),lesson+": original not visible during repair")
    root.locator('[data-field="repair"]').fill("I repaired my first model: I must check the physical conditions before choosing an equation.")
    root.locator('[data-action="save-repair"]').click()
    require(root.locator(".stage-card h3").inner_text()=="6. Boundary test",lesson+": boundary missing")
    require(root.locator(".stage-card .worked").count()==0,lesson+": boundary solution appeared before boundary attempt")
    root.locator('[data-action="save-boundary"]').click()
    require(root.locator(".stage-card .worked").count()==0,lesson+": blank boundary response accepted")
    root.locator('[data-field="boundary"]').fill("The changed condition changes one piece of the model; I will recompute and check why.")
    root.locator('[data-action="save-boundary"]').click()
    require(root.locator(".stage-card .worked").count()==1,lesson+": boundary worked check missing")
    require(state(page,lesson)["first"]==original_first,lesson+": first attempt overwritten by repair/boundary")
    require(state(page,lesson)["boundary"],lesson+": changed-condition reasoning not saved")
    require("1 of 5" in page.locator("#extension-progress").inner_text(),lesson+": completed state not counted")
    page.reload(wait_until="load")
    page.locator("#source-journey:not([hidden])").wait_for()
    require(state(page,lesson)["first"]==original_first,lesson+": first attempt lost on reload")
    require(root.locator(".stage-card h3").inner_text()=="6. Boundary test",lesson+": stage not restored")
    root.locator('[data-action="history"]').click()
    require(PROMPT[lesson] in root.locator(".history").inner_text(),lesson+": original history not visible")
    root.locator(".return-original").first.click()
    require(page.locator(".qtitle").inner_text()==source,lesson+": wrong source on return")
    require(page.locator("#solution-container .solution").count()==0,lesson+": returning revealed source answer")

def verify_source_inventory(page,base):
    # All seven exact existing candidate-source references can open the right E route.
    for id_,sources in SOURCES.items():
        for source in sources:
            page.goto(base+"/physics/wpe/reasoning-paths.html?question="+source)
            link=page.locator("#WPE-"+id_+' a[href*="extension-learning.html?question='+source+'#'+id_+'"]')
            link.wait_for()
            require(link.count()==1,id_+" "+source+": missing original link")
    page.goto(base+"/physics/wpe/extension-learning.html?question=EX-M82#E01")
    page.locator("#source-journey:not([hidden])").wait_for()
    require(page.locator("#source-return").is_hidden(),"Mismatched extension/source created return link")
    page.goto(base+"/physics/wpe/extension-learning.html?question=NOT-IN-BANK#E01")
    page.locator("#source-journey:not([hidden])").wait_for()
    require(page.locator("#source-return").is_hidden(),"Unknown source created return link")

def main():
    svc,base=server()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for width,height in VIEWPORTS:
                    for lesson,sources in SOURCES.items():
                        context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
                        try:
                            page=context.new_page()
                            errors=[]
                            page.on("pageerror",lambda err:errors.append(str(err)))
                            round_trip(page,base,lesson,sources[0])
                            require(not errors,lesson+" JS errors: "+repr(errors))
                            print("PASS: "+lesson+" complete six-stage and source return at "+str(width)+"px")
                        finally:
                            context.close()
                context=browser.new_context()
                try:verify_source_inventory(context.new_page(),base)
                finally:context.close()
                print("PASS: seven exact source links; unmatched source IDs refused")
            finally:
                browser.close()
    finally:
        svc.shutdown();svc.server_close()

if __name__=="__main__":
    main()
