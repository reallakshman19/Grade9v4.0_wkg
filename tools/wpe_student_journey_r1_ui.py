"""Question Bank → suggested C03 tutor → independent challenge → exact EX-M79 return.
Synthetic browser interactions only; no learner mastery or academic admission claim.
"""
from __future__ import annotations
from functools import partial
import http.server
import json
import math
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = ((1280, 800), (390, 844))

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def server():
    svc = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=svc.serve_forever, daemon=True).start()
    return svc, "http://127.0.0.1:" + str(svc.server_port)

def check_model_conditions():
    # Constant NET power, nonzero initial speed, no dissipation.
    m, v0, p = 3., 2., 18.
    K0 = m*v0*v0/2
    require(K0 == 6., "Incorrect starting energy")
    require(math.isclose(math.sqrt(2*(K0+p*2)/m), math.sqrt(28)), "C03 after 2 s wrong")
    require(math.isclose(math.sqrt(2*(K0+p*6)/m), math.sqrt(76)), "C03 after 6 s wrong")
    require(math.isclose(math.sqrt(2*(K0+9*2)/m), 4), "C03 half-power boundary wrong")
    # EX-M79 supplies v proportional to sqrt(distance), not constant power:
    # for s(t) with v=c sqrt(s), v(t) is proportional to t, so K(t) grows as t².
    c=3.
    def s(t): return (c*t/2)**2
    def speed(t): return c*math.sqrt(s(t))
    require(math.isclose(speed(4)/speed(2), 2), "EX-M79 speed law misinterpreted")
    require(math.isclose(speed(4)**2/speed(2)**2, 4), "EX-M79 energy-time law misinterpreted")
    require(not math.isclose((speed(4)**2-speed(2)**2), (speed(2)**2-speed(0)**2)), "EX-M79 wrongly treated as constant-power")
    # C04 uniform hanging-mass change, frictionless quasi-static:
    lam, g=0.5, 10.
    U=lambda L:-lam*g*L*L/2
    require(U(2)-U(4)==30 and U(0)-U(4)==40, "C04 changing centre of mass wrong")

def browser_roundtrip(browser, base, width, height):
    ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
    try:
        page=ctx.new_page(); errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(base+"/preview/question-status.html?question=EX-M79")
        require(page.locator(".qtitle").inner_text()=="EX-M79","Source question did not load")
        require(page.locator("#solution-container .solution").count()==0,"Source answer appeared before attempt")
        tutor=page.locator('#interactive-lesson-links a[href="../physics/wpe/d3d4-self-tutor.html?question=EX-M79#C03"]')
        tutor.wait_for()
        require(tutor.count()==1,"Exact source question lacks direct C03 tutor link")
        tutor.click()
        require(page.url.endswith("d3d4-self-tutor.html?question=EX-M79#C03"),"Tutor lost source identity")
        page.locator("#source-journey:not([hidden])").wait_for()
        require("speed–distance" in page.locator("#source-journey-message").inner_text(),"EX-M79 model contrast not shown")
        require(page.locator("#source-journey-return").get_attribute("href").endswith("question=EX-M79"),"Incorrect return ID")
        root=page.locator('[data-stage-root="C03"]')
        require(root.locator(".stage-card h4").inner_text()=="1. Predict","C03 initial step wrong")
        require(root.locator(".worked").count()==0,"Worked answer in initial challenge")
        root.locator("textarea").fill("Power is energy per time, so speed need not rise linearly.")
        root.locator('[data-action="save-prediction"]').click()
        require(root.locator(".stage-card h4").inner_text()=="2. Attempt","C03 attempt was not reached")
        require(root.locator(".worked").count()==0,"Answer in the DOM before attempt")
        root.locator('[data-input="reason"]').fill("I will start from the energy at t=0 and compare the graph slopes.")
        for i in range(3):
            root.locator('[data-action="next-hint"]').click()
            require(root.locator(".hint-text").count()==i+1,"Hints not revealed progressively")
            require(root.locator(".worked").count()==0,"Hint leaked worked reconstruction")
            require("I will start" in root.locator('[data-input="reason"]').input_value(),"Hint click erased first attempt")
        require(root.locator('[data-action="next-hint"]').is_disabled(),"Hints should stop after third")
        root.locator('[data-action="lock-attempt"]').click()
        require(root.locator(".stage-card h4").inner_text()=="3. Reconstruct","C03 attempt not committed")
        require(root.locator(".worked").count()==1,"Worked reconstruction missing after attempt")
        first=page.evaluate('JSON.parse(localStorage.getItem("g9:wpe:d3d4:self-tutor:v1:C03"))')
        require(first["hintsUsed"]==3 and "energy at t=0" in first["first"]["reason"],"First attempt or hints lost")
        root.locator('[data-action="save-reconstruction"]').click()
        root.locator('[data-input="diagnosis"]').select_option(label="I forgot the starting kinetic energy.")
        root.locator('[data-input$="diagnosisWhy"]').fill("I had treated the starting energy as zero.")
        root.locator('[data-action="save-diagnosis"]').click()
        require("K₀" in root.locator(".diagnostic-tip").inner_text(),"Diagnosis lacks specific repair guidance")
        root.locator('[data-input$="repair"]').fill("I must add K0 before using the square-root speed law.")
        root.locator('[data-action="save-repair"]').click()
        require(root.locator(".review-model").count()==1,"Earlier worked model should be available to review")
        require(root.locator(".review-model").evaluate("(e) => !e.open"),"Earlier worked model opened without asking")
        require(root.locator(".stage-card > .worked").count()==0,"Changed-condition answer shown before boundary attempt")
        root.locator('[data-input$="boundary"]').fill("Halving power lowers the energy gain, but does not make acceleration fixed.")
        root.locator('[data-action="save-boundary"]').click()
        require("4 m/s" in root.locator(".worked").inner_text(),"Changed-condition scientific check wrong")
        require(page.locator("#overall-count").inner_text().startswith("1 of"),"Challenge progress missing")
        page.reload(wait_until="load")
        page.locator("#source-journey:not([hidden])").wait_for()
        require(root.locator(".stage-card h4").inner_text()=="6. Boundary test","Committed stages not persisted")
        root.locator('[data-action="review-history"]').click()
        require("energy at t=0" in root.locator(".history .snapshot").first.inner_text(),"First model not preserved")
        require(page.evaluate("document.documentElement.scrollWidth<=innerWidth+3"),f"Horizontal overflow at {width}")
        root.locator("a.return-original").click()
        require(page.locator(".qtitle").inner_text()=="EX-M79","Returned to wrong question")
        require(page.locator("#solution-container .solution").count()==0,"Return exposed original solution")
        # All 74 source records appear exactly once; reported gaps are based on existing mappings.
        page.goto(base+"/physics/wpe/question-coverage.html")
        page.locator("#table-status").filter(has_text="74 of 74").wait_for()
        require(page.locator("#rows tr").count()==74,"Not all source questions covered")
        page.locator("#filter").select_option("targeted")
        require(page.locator("#rows tr").count()==18,"Incorrect close-practice match count")
        page.locator("#filter").select_option("focused")
        require(page.locator("#rows tr").count()==8,"Incorrect eight-journey coverage")
        page.locator("#filter").select_option("related")
        require(page.locator("#rows tr").count()==48,"Incorrect related-only bridge count")
        page.locator("#filter").select_option("missing")
        require(page.locator("#rows tr").count()==0,"Unexpected remaining missing-construction count")
        page.locator("#filter").select_option("all")
        page.locator("#search").fill("EX-M101")
        require(page.locator("#rows tr").count()==1,"Spring source coverage missing")
        spring_skill=page.locator("#rows tr").inner_text().lower()
        require("equal final equilibrium force" in spring_skill and "equal extension" in spring_skill,
                "EX-M101 map still teaches the wrong model")
        require("conservative vector field" not in spring_skill,
                "Wrong imported crux still appears in spring coverage")
        page.locator("#search").fill("EX-M79")
        require(page.locator("#rows tr").count()==1,"Coverage search ambiguous")
        require("speed–distance" in page.locator("#rows tr").inner_text(),"EX-M79 reasoning capability inaccurate")
        require(not errors,f"Browser JS errors at {width}: {errors}")
        print(f"PASS: {width}×{height} question, C03 six-stage learner journey, three hints, specific feedback, return, 74-row coverage")
    finally: ctx.close()

def other_topic_links(browser,base):
    ctx=browser.new_context(viewport={"width":390,"height":844})
    try:
        page=ctx.new_page()
        cases=[("EX-M105","C01"),("EX-M24","C02"),("EX-M73","C04"),("EX-M16","C07"),("EX-M101","C08")]
        for q,lesson in cases:
            page.goto(base+f"/physics/wpe/reasoning-paths.html?question={q}")
            page.locator("#route-status").filter(has_text=q).wait_for()
            page.locator(f'#WPE-{lesson} a[href="d3d4-self-tutor.html?question={q}#{lesson}"]').click()
            page.locator("#source-journey:not([hidden])").wait_for()
            root=page.locator(f'[data-stage-root="{lesson}"]')
            root.locator("textarea").fill("I predict a physical model change is important.")
            root.locator('[data-action="save-prediction"]').click()
            require(root.locator('[data-action="next-hint"]').count()==1,"Optional hint absent for "+lesson)
            root.locator('[data-action="next-hint"]').click()
            require(root.locator(".worked").count()==0,"Hint leaked the answer for "+lesson)
            page.locator("#source-journey-return").click()
            require(page.locator(".qtitle").inner_text()==q,"Other topic returned to wrong question")
        # PR26 supplies science-specific authored cues while preserving the original source hints.
        # The renderer must use those cues, not the old hardcoded EX-M101 override.
        page.goto(base+"/preview/question-status.html?question=EX-M101")
        require(page.locator(".qtitle").inner_text()=="EX-M101","Spring comparison source unavailable")
        page.locator('.hint').first.locator('summary').click()
        first_cue=page.locator('.hint').first.inner_text().lower()
        require(all(word in first_cue for word in ("spring","stiffness","force")),
                "EX-M101 missing tailored controlled-variable study cue")
        require("path independence" not in first_cue and "conservative" not in first_cue,
                "Unrelated source hint leaked into EX-M101 pre-attempt guidance")
        require(page.locator("#solution-container .solution").count()==0,
                "Spring explanation leaked before a committed attempt")
        page.locator('input[name="answer-option"]').first.check()
        page.locator("#commit").click()
        page.locator("#reveal").click()
        explained=page.locator("#solution-container").inner_text().lower()
        require("same force" in explained and "same extension" in explained
                and "k1<k2" in "".join(explained.split()),
                "EX-M101 solution must infer spring stiffness and reverse the comparison")
        require("conservative-vector-field" not in explained,
                "Irrelevant imported explanation still shown")
        page.goto(base+"/physics/wpe/d3d4-self-tutor.html?question=EX-M81#C03")
        require(page.locator("#source-journey").is_hidden(),"Absent question got a false return link")
        print("PASS: C01, C02, C04, C07 and C08 source navigation, optional hints, and absent-ID refusal")
    finally:ctx.close()

def main():
    check_model_conditions()
    svc,base=server()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for w,h in VIEWPORTS:browser_roundtrip(browser,base,w,h)
                other_topic_links(browser,base)
            finally:browser.close()
    finally:svc.shutdown();svc.server_close()

if __name__=="__main__":main()
