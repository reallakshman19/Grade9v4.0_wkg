"""Chromium walkthrough of direct WPE learning + source drafts + transfer variants.

Automated input is not an observation of a real child's independent understanding.
"""
from __future__ import annotations
from functools import partial
import http.server
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
VIEWPORTS=((1280,800),(390,844))
FOCUSED={"F01":"EX-M97","F02":"EX-N39","F03":"WEP07-01"}

def verify(ok,why):
    if not ok:raise AssertionError(why)

def server():
    service=http.server.ThreadingHTTPServer(("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=service.serve_forever,daemon=True).start()
    return service,"http://127.0.0.1:"+str(service.server_port)

def saved(page,key):
    return page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))",key)

def original_question_roundtrip(page,base):
    page.goto(base+"/preview/question-status.html?question=EX-M79")
    verify(page.locator(".qtitle").inner_text()=="EX-M79","Did not load original EX-M79")
    verify(page.locator("#solution-container .solution").count()==0,"Source answer exposed before attempt")
    page.locator('input[name="answer-option"][value="1"]').check()
    draft=saved(page,"g9:wpe:core2:attempt:v1:EX-M79")
    verify(draft["schema"]==1 and draft["selected"]==[1] and not draft["committed"],"MCQ draft not saved")
    page.reload()
    verify(page.locator('input[name="answer-option"][value="1"]').is_checked(),"Draft lost on refresh")
    verify(page.locator("#solution-container .solution").count()==0,"Answer revealed on refresh")
    tutor=page.locator('#interactive-lesson-links a[href*="d3d4-self-tutor.html?question=EX-M79#C03"]').first
    tutor.wait_for()
    tutor.click()
    verify(page.url.endswith("d3d4-self-tutor.html?question=EX-M79#C03"),"Exact C03 question binding lost")
    page.locator("#source-journey:not([hidden])").wait_for()
    verify("speed–distance" in page.locator("#source-journey-message").inner_text(),"EX-M79 contrast missing")
    verify(page.locator("iframe").count()==0,"C03 embedded iframe")
    page.locator("#source-journey-return").click()
    verify(page.locator(".qtitle").inner_text()=="EX-M79","Wrong source question on return")
    verify(page.locator('input[name="answer-option"][value="1"]').is_checked(),"Source draft lost across navigation")
    verify(page.locator("#solution-container .solution").count()==0,"Source solution auto-revealed")
    page.locator("#commit").click()
    committed=saved(page,"g9:wpe:core2:attempt:v1:EX-M79")
    verify(committed["committed"] and committed["first"]["selected"]==[1],"Frozen first source submission missing")
    page.reload()
    verify(page.locator("#commit").is_disabled(),"Committed answer not restored")
    verify(page.locator("#solution-container .solution").count()==0,"Committed answer should not auto-reveal")
    page.locator("#reveal").click()
    verify(page.locator("#solution-container .solution").count()==1,"Explicit reveal failed")
    page.reload()
    verify(page.locator("#solution-container .solution").count()==0,"Revealed author answer reopened automatically")
    page.locator("#start-question").click()
    # Browser confirm dialog is accepted explicitly by this simulated test.
    verify(page.locator("#commit").is_enabled(),"Start-again control did not reset source attempt")
    verify(saved(page,"g9:wpe:core2:attempt:v1:EX-M79") is None,"Reset did not erase this question")

def legacy_bridge_direct_navigation(page,base):
    page.goto(base+"/physics/wpe/study-bridge.html?question=EX-M79&lesson=C03")
    page.wait_for_url("**/d3d4-self-tutor.html?question=EX-M79#C03")
    verify(page.locator("iframe").count()==0,"Legacy C03 bridge embedded the lesson")
    page.goto(base+"/physics/wpe/study-bridge.html?question=EX-M97&lesson=F01&variant=transfer")
    page.wait_for_url("**/focused-journeys.html?question=EX-M97&variant=transfer#F01")
    verify(page.locator('[data-stage-root="F01"]').count()==1,"Legacy F01 transfer route lost")
    page.goto(base+"/physics/wpe/study-bridge.html?question=UNKNOWN-ID&lesson=C03")
    page.locator("#status").filter(has_text="could not be verified").wait_for()
    verify(page.locator("#direct").is_hidden(),"Unverified source bridge invented a lesson")

def written_question_draft(page,base):
    page.goto(base+"/preview/question-status.html?question=EX-N39")
    verify(page.locator(".qtitle").inner_text()=="EX-N39","Numerical original question not selected")
    page.locator("#free-answer").fill("Use two signed friction ledgers; I must decide which forces dissipate energy.")
    stored=saved(page,"g9:wpe:core2:attempt:v1:EX-N39")
    verify("two signed friction" in stored["response"] and not stored["committed"],"Written draft not saved")
    page.goto(base+"/physics/wpe/learn-challenge.html?question=EX-N39#question-routes")
    page.locator('#question-plan .primary-link[href*="focused-journeys.html?question=EX-N39#F02"]').wait_for()
    page.locator("#journey-resume").wait_for()
    page.goto(base+"/preview/question-status.html?question=EX-N39")
    verify("two signed friction" in page.locator("#free-answer").input_value(),"Written draft not restored after navigation")
    verify(page.locator("#solution-container .solution").count()==0,"Free-text draft revealed source answer")
    page.locator("#commit").click()
    verify(page.locator("#commit").is_disabled(),"Written attempt not committed")
    page.reload()
    verify(saved(page,"g9:wpe:core2:attempt:v1:EX-N39")["first"]["response"].startswith("Use two signed"),"Committed written original not preserved")
    verify(page.locator("#solution-container .solution").count()==0,"Committed numerical response auto-revealed")

def finish_challenge(root):
    root.locator('[data-field="prediction"]').fill("I will choose forces and use the phase boundary first.")
    root.locator('[data-action="prediction"]').click()
    verify(root.locator(".worked").count()==0,"Fresh answer exposed before attempt")
    root.locator('[data-field="reason"]').fill("I must compare forces, signed work, assumptions and the switch between phases.")
    root.locator('[data-field="model"]').select_option(index=2) # intentionally wrong for misconception feedback
    for count in (1,2,3):
        root.locator('[data-action="hint"]').click()
        verify(root.locator(".hint-list li").count()==count,"Hints not progressive")
        verify(root.locator(".worked").count()==0,"Reconstruction exposed by a hint")
    verify("compare forces" in root.locator('[data-field="reason"]').input_value(),"Hint erased reasoning draft")
    root.locator('[data-action="attempt"]').click()
    verify(root.locator(".worked").count()==1,"Reconstruction not gated by first attempt")
    verify(root.locator(".assessment .review").count()>=1,"Incorrect selection has no targeted feedback")
    first_text=root.locator(".snapshot").inner_text()
    root.locator('[data-action="reconstruct"]').click()
    root.locator("[data-diagnosis]").select_option("model")
    root.locator('[data-field="why"]').fill("I confused a net force with the force supplying work.")
    root.locator('[data-action="diagnose"]').click()
    root.locator('[data-field="repair"]').fill("I will use the applied force for delivered power and subtract weight for dK/dt.")
    root.locator('[data-action="repair"]').click()
    verify("compare forces" in root.locator(".snapshot").inner_text(),"First attempt overwritten by repair")
    root.locator('[data-field="why"]').fill("Changing the physical input changes the rate; the phase boundary is still distinct.")
    verify(root.locator(".worked").count()==0,"Boundary check exposed before boundary attempt")
    root.locator('[data-action="boundary"]').click()
    verify(root.locator(".worked").count()==1,"Boundary reconstruction failed after commit")
    verify("compare forces" in root.locator(".snapshot").inner_text(),"First attempt overwritten by boundary")
    return first_text

def focus_variants(page,base):
    page.goto(base+"/physics/wpe/focused-journeys.html?question=EX-M97#F01")
    page.locator("#source-journey:not([hidden])").wait_for()
    verify(page.locator("#source-return").is_visible(),"F01 exact source return absent")
    verify(page.locator("iframe").count()==0,"F01 iframe")
    root=page.locator('[data-stage-root="F01"]')
    verify(root.locator(".worked").count()==0,"F01 answer visible before challenge")
    finish_challenge(root)
    first=saved(page,"g9:wpe:focused:v1:F01")
    verify(first["first"]["answers"]["model"]=="Net force T − mg","First F01 choice not frozen")
    extra=root.locator('a:has-text("Try another challenge")')
    verify(extra.count()==1,"Optional second challenge not offered")
    extra.click()
    verify("variant=transfer" in page.url and page.url.endswith("#F01"),"Transfer URL lost lesson or variant")
    root=page.locator('[data-stage-root="F01"]')
    verify(root.locator(".worked").count()==0,"Transfer reconstruction exposed first")
    root.locator('[data-field="prediction"]').fill("The flight height sets launch speed; contact work includes gravity.")
    root.locator('[data-action="prediction"]').click()
    verify("4 kg toy" in root.locator(".stage-card").inner_text(),"Donor F01 toy prompt missing")
    root.locator('[data-field="model"]').select_option("Net accelerating force only")
    root.locator('[data-field="reason"]').fill("I will check two phases but I initially chose net power.")
    root.locator('[data-action="hint"]').click()
    verify(root.locator(".hint-list li").count()==1,"Donor hint missing")
    page.reload()
    root=page.locator('[data-stage-root="F01"]')
    verify(root.locator('[data-field="reason"]').input_value().startswith("I will check"),"Transfer draft not restored")
    root.locator('[data-action="attempt"]').click()
    verify("104" in root.locator(".worked").inner_text() and "416" in root.locator(".worked").inner_text(),"E06 model not reconstructed")
    verify("Power delivered" in root.locator(".assessment").inner_text(),"E06 error-specific feedback absent")
    second=saved(page,"g9:wpe:focused:v1:F01:transfer")
    verify(second["first"]["answers"]["model"]=="Net accelerating force only","Transfer first model not saved")
    verify(saved(page,"g9:wpe:focused:v1:F01")["first"]==first["first"],"Optional transfer overwrote first challenge")
    page.locator("#source-return").click()
    verify(page.locator(".qtitle").inner_text()=="EX-M97","Transfer returned to wrong source")
    verify(page.locator("#solution-container .solution").count()==0,"Transfer navigation exposed source key")
    # Distinct F02/F03 variant states and direct source IDs.
    for id_,source in (("F02","EX-N39"),("F03","WEP07-01")):
        page.goto(base+"/physics/wpe/focused-journeys.html?question="+source+"&variant=transfer#"+id_)
        root=page.locator('[data-stage-root="'+id_+'"]')
        verify(root.locator(".worked").count()==0,id_+" reconstruction before attempt")
        root.locator('[data-field="prediction"]').fill("I must choose the correct post-change physical model.")
        root.locator('[data-action="prediction"]').click()
        root.locator('[data-field="model"]').select_option(index=1)
        root.locator('[data-field="reason"]').fill("I will apply a phase-specific force or effective-energy model.")
        root.locator('[data-action="attempt"]').click()
        worked=root.locator(".worked").inner_text()
        verify(("5/13" in worked) if id_=="F02" else ("0.80" in worked and "0.30" in worked),id_+" donor result missing")
        verify(saved(page,"g9:wpe:focused:v1:"+id_+":transfer")["first"] is not None,id_+" independent attempt not saved")
        original=saved(page,"g9:wpe:focused:v1:"+id_)
        verify(original is None or original["first"] is None,id_+" first variant unexpectedly changed")
        verify(page.locator("#source-return").get_attribute("href").endswith("question="+source),id_+" source ID lost")
        verify(page.locator("iframe").count()==0,id_+" iframe")

    page.goto(base+"/physics/wpe/learn-challenge.html#practice-manager")
    page.locator("#question-route-status").filter(has_text="of 74 source questions shown").wait_for()
    page.locator("#journey-clear").click()
    verify(saved(page,"g9:wpe:focused:v1:F01") is None,"Lesson clear left first focused attempt")
    verify(saved(page,"g9:wpe:focused:v1:F01:transfer") is None,"Lesson clear left transfer focused attempt")
    verify(saved(page,"g9:wpe:focused:v1:F02:transfer") is None,"Lesson clear left another transfer")
    verify(saved(page,"g9:wpe:core2:attempt:v1:EX-N39")["committed"],"Lesson clear erased original source attempt")

def main():
    service,base=server()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for width,height in VIEWPORTS:
                    context=browser.new_context(viewport={"width":width,"height":height},accept_downloads=False)
                    try:
                        page=context.new_page()
                        page.on("dialog",lambda dialog:dialog.accept())
                        errors=[]
                        page.on("pageerror",lambda error:errors.append(str(error)))
                        original_question_roundtrip(page,base)
                        legacy_bridge_direct_navigation(page,base)
                        written_question_draft(page,base)
                        focus_variants(page,base)
                        verify(page.evaluate("document.documentElement.scrollWidth<=innerWidth+4"),"Mobile horizontal overflow")
                        verify(not errors,"Browser JS exceptions: "+repr(errors))
                        print("PASS unified WPE source and transfer routes at",width,height)
                    finally:context.close()
            finally:browser.close()
    finally:service.shutdown()
if __name__=="__main__":main()
