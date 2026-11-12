"""Chromium QA for eight source-grounded WPE six-stage student practice journeys."""
from __future__ import annotations

import http.server
import json
import pathlib
import threading
from functools import partial

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = "/physics/wpe/d3d4-self-tutor.html"
VIEWPORTS = [(1280, 800), (1024, 768), (900, 1280), (800, 1280), (390, 844)]


def check(ok, msg):
    if not ok:
        raise AssertionError(msg)


def local_server():
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, "http://127.0.0.1:" + str(server.server_port)


def saved_state(page, lesson):
    key = "g9:wpe:d3d4:self-tutor:v1:" + lesson
    return page.evaluate("(key) => JSON.parse(localStorage.getItem(key))", key)


def root_for(page, lesson):
    return page.locator('[data-stage-root="' + lesson + '"]')


def fill_stage_one(page, lesson, answer):
    root = root_for(page, lesson)
    check(root.locator(".stage-card h4").inner_text() == "1. Predict", lesson+" predict stage missing")
    check(root.locator(".worked").count() == 0, lesson+" answer leaked before attempt")
    root.locator('[data-action="save-prediction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "1. Predict", lesson+" blank prediction unlocked")
    root.locator("textarea").fill("I think the moving object gains energy, but I want to check the forces.")
    root.locator('[data-action="save-prediction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "2. Attempt", lesson+" attempt not available")
    check(root.locator(".worked").count() == 0, lesson+" worked answer shown too early")
    root.locator('[data-action="lock-attempt"]').click()
    check(root.locator(".stage-card h4").inner_text() == "2. Attempt", lesson+" blank explanation unlocked")
    root.locator('[data-input="reason"]').fill(answer)
    if lesson == "C01":
        root.locator('[data-input="motor"]').select_option(label="Positive (+)")
        root.locator('[data-input="friction"]').select_option(label="Negative (−)")
        root.locator('[data-input="gravity"]').select_option(label="Positive (+)")  # deliberately incorrect reasoning
        root.locator('[data-input="normal"]').select_option(label="Zero (0)")
        root.locator('[data-input="netWork"]').fill("39")
        root.locator('[data-input="topSpeed"]').fill("5")
    elif lesson == "C02":
        root.locator('[data-input="boundary"]').select_option(label="At the far end of the rough strip")  # incorrect
        root.locator('[data-input="springEnergy"]').fill("1")
        root.locator('[data-input="finalSpeed"]').fill("1")
    elif lesson == "C03":
        root.locator('[data-input="powerMeaning"]').select_option(label="The force is always 18 N")  # incorrect
        root.locator('[data-input="initialEnergy"]').fill("0")  # forgot initial energy
        root.locator('[data-input="energyAt2"]').fill("36")
        root.locator('[data-input="speedAt2"]').fill("5")
        root.locator('[data-input="energyGraph"]').select_option(label="Straight rising line")
        root.locator('[data-input="speedGraph"]').select_option(label="Straight rising line")  # misconception
    elif lesson == "C04":
        root.locator('[data-input="massPerMetre"]').fill("0.5")
        root.locator('[data-input="startMass"]').fill("4")  # used total rope mass
        root.locator('[data-input="startDepth"]').fill("4")
        root.locator('[data-input="endMass"]').fill("4")
        root.locator('[data-input="helperWork"]').fill("80")
        root.locator('[data-input="modelChoice"]').select_option(label="The whole 4 kg rope in both states")
    elif lesson == "C05":
        root.locator('[data-input="graphR"]').select_option(label="Slope of the line")  # area/slope confusion
        root.locator('[data-input="workR"]').fill("2")
        root.locator('[data-input="graphS"]').select_option(label="Positive slope of the line")  # missing minus
        root.locator('[data-input="forceS"]').fill("3")
        root.locator('[data-input="graphT"]').select_option(label="Slope of the entire 0–5 s span")
        root.locator('[data-input="speedT"]').fill("3.2")
        root.locator('[data-input="unitChoice"]').select_option(label="J, N, m/s")
    elif lesson == "C06":
        root.locator('[data-input="topInward"]').select_option(label="Upward")  # incorrect inward arrow
        root.locator('[data-input="heightRise"]').fill("2")
        root.locator('[data-input="candidateSpeedSquared"]').fill("9")
        root.locator('[data-input="candidateSpeed"]').fill("3")
        root.locator('[data-input="energyPossible"]').select_option(label="Yes")
        root.locator('[data-input="radialEquation"]').select_option(label="T − mg = mv²/r")  # wrong top force signs
        root.locator('[data-input="topTension"]').fill("19")
        root.locator('[data-input="staysTaut"]').select_option(label="Yes")
    elif lesson == "C07":
        root.locator('[data-input="model"]').select_option(label="All chips ever collected on the belt")  # wrong model
        root.locator('[data-input="flowRate"]').fill("2")
        root.locator('[data-input="deltaVelocity"]').fill("4")  # ignores incoming speed
        root.locator('[data-input="pickupForce"]').fill("8")
        root.locator('[data-input="motorPower"]').fill("32")
        root.locator('[data-input="chipEnergy"]').fill("24")  # treats all motor power as kinetic
        root.locator('[data-input="energyModel"]').select_option(label="All to chips' kinetic energy")
    elif lesson == "C08":
        root.locator('[data-input="kBlue"]').fill("200")
        root.locator('[data-input="kGold"]').fill("400")
        root.locator('[data-input="testXChoice"]').select_option(label="Gold pad")
        root.locator('[data-input="xBlue"]').fill("0.25")
        root.locator('[data-input="xGold"]').fill("0.5")
        root.locator('[data-input="testYChoice"]').select_option(label="Gold pad")  # mistaken fixed-force ranking
        root.locator('[data-input="yBlue"]').fill("0.25")  # keeps 5 cm from Test X
        root.locator('[data-input="yGold"]').fill("0.5")
        root.locator('[data-input="control"]').select_option(label="Both tests fix compression")
    else:
        raise AssertionError("Unknown topic " + lesson)
    root.locator('[data-action="lock-attempt"]').click()
    check(root.locator(".stage-card h4").inner_text() == "3. Reconstruct", lesson+" first attempt not committed")
    check(root.locator(".worked").count() == 1, lesson+" worked reconstruction not available")
    state = saved_state(page, lesson)
    check(state["first"]["reason"] == answer, lesson+" first answer missing from storage")
    check(state["stage"] == 2, lesson+" stage not stored")
    check(root.locator(".snapshot").inner_text().find(answer) >= 0, lesson+" first model not displayed")
    return state["first"]


def finish_stages(page, lesson, first):
    root = root_for(page, lesson)
    page.reload(wait_until="load")
    root = root_for(page, lesson)
    check(root.locator(".stage-card h4").inner_text() == "3. Reconstruct", lesson+" first attempt lost after reload")
    check(saved_state(page, lesson)["first"] == first, lesson+" first snapshot changed after reload")
    check(root.locator(".rubric li").count() == 4, lesson+" reconstruction rubric incomplete")
    root.locator("[data-rubric]").first.check()
    root.locator('[data-action="save-reconstruction"]').click()
    check(root.locator(".stage-card h4").inner_text() == "4. Diagnose", lesson+" diagnosis missing")
    check(root.locator(".review-model").count() == 1, lesson+" no reusable worked model at diagnosis")
    check(root.locator(".review-model").evaluate("(e) => !e.open"), lesson+" model should start collapsed")
    root.locator(".review-model summary").click()
    check(root.locator(".review-model .worked").is_visible(), lesson+" cannot reopen worked reasoning")
    root.locator(".review-model summary").click()
    root.locator('[data-input="diagnosis"]').select_option(index=1)
    root.locator("[data-input$=diagnosisWhy]").fill("My first physics model needs a different boundary or work sign.")
    root.locator('[data-action="save-diagnosis"]').click()
    check(root.locator(".stage-card h4").inner_text() == "5. Repair", lesson+" repair missing")
    check(root.locator(".review-model").count() == 1, lesson+" no worked reasoning to consult in repair")
    check(root.locator(".review-model").evaluate("(e) => !e.open"), lesson+" repair reference must be optional")
    check(root.locator(".diagnostic-tip").count() == 1, lesson+" missing diagnosis-specific repair cue")
    root.locator("[data-input$='-repair']").fill("I corrected the first wrong model choice and now use the right energy ledger.")
    root.locator('[data-action="save-repair"]').click()
    check(root.locator(".stage-card h4").inner_text() == "6. Boundary test", lesson+" boundary stage missing")
    check(root.locator(".review-model").count() == 1, lesson+" cannot reopen prior model during boundary thinking")
    check(root.locator(".review-model").evaluate("(e) => !e.open"), lesson+" prior model not collapsed")
    check(root.locator(".worked").count() == 1 and not root.locator(".worked").is_visible(),
          lesson+" boundary worked check visible before attempt")
    root.locator("[data-input$='-boundary']").fill("I need to check whether energy remains positive at the new endpoint.")
    root.locator('[data-action="save-boundary"]').click()
    check(root.locator(".response-done").count() == 1, lesson+" completion missing")
    check(root.locator(".worked").count() == 1, lesson+" boundary worked check missing")
    state = saved_state(page, lesson)
    check(state["stage"] == 5 and bool(state["boundary"]), lesson+" boundary answer not saved")
    check(state["first"] == first, lesson+" original was overwritten by repair")
    check(bool(state["repair"]) and isinstance(state["diagnosis"], dict), lesson+" diagnosis/repair not stored")
    root.locator('[data-action="review-history"]').click()
    check(root.locator(".history .snapshot").count() == 2, lesson+" first/repair history not independently visible")
    check(first["reason"] in root.locator(".history").inner_text(), lesson+" first reasoning missing in history")
    check("I corrected" in root.locator(".history").inner_text(), lesson+" repair missing in history")
    return state


def run_viewport(browser, width, height, base):
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    try:
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        response = page.goto(base+PATH, wait_until="load")
        check(response is not None and response.status == 200, "Self-tutor page did not load")
        check(page.locator("article.unit").count() == 8, "Eight lessons missing")
        check(page.locator(".guide-steps").count() == 8, "Core1A guides missing")
        check(page.locator(".stage-root .step-list li").count() == 48, "All six stages not listed for eight lessons")
        check(page.locator("body").inner_text().find("This page does not grade explanations") != -1, "Non-grading learner note missing")
        check(page.locator("#overall-count").inner_text() == "0 of 8 challenges completed", "Initial progress incorrect")
        check(not errors, "JavaScript error on load: "+str(errors))
        check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 3"),
              "Horizontal page overflow at "+str(width))

        # Eight distinct first attempts; each deliberately includes a plausible conceptual mistake;
        # there is no automatic evaluation of the child's free-text explanation.
        first_c01 = fill_stage_one(page, "C01", "I counted the motor and gravity as helping uphill, maybe 39 joules.")
        check(saved_state(page, "C02") is None, "C01 saved the other topic unexpectedly")
        finish_stages(page, "C01", first_c01)
        check(page.locator("#overall-count").inner_text() == "1 of 8 challenges completed", "First completion not counted")
        first_c02 = fill_stage_one(page, "C02", "I think the spring might keep pushing into the rough strip.")
        finish_stages(page, "C02", first_c02)
        check(page.locator("#overall-count").inner_text() == "2 of 8 challenges completed", "Second completion not counted")
        first_c03 = fill_stage_one(page, "C03", "I think 18 watts means constant force and each second gives the same speed increase.")
        check("Kinetic energy" in root_for(page, "C03").locator(".worked").inner_text()
              or "kinetic energy" in root_for(page, "C03").locator(".worked").inner_text(),
              "C03 reconstruction does not explain power/energy relationship")
        finish_stages(page, "C03", first_c03)
        check(page.locator("#overall-count").inner_text() == "3 of 8 challenges completed",
              "Third completion not counted")
        first_c04 = fill_stage_one(page, "C04", "I used the whole four kilograms in both rope pictures instead of changing the hanging mass.")
        check("−40 J" in root_for(page, "C04").locator(".worked").inner_text(),
              "C04 worked model missing initial hanging potential")
        finish_stages(page, "C04", first_c04)
        check(page.locator("#overall-count").inner_text() == "4 of 8 challenges completed",
              "Fourth completion not counted")
        first_c05 = fill_stage_one(page, "C05",
            "I think the force graph slope is the work and the positive U slope means a positive force.")
        check("+16 J" in root_for(page, "C05").locator(".worked").inner_text(),
              "C05 worked reconstruction missing triangular force area")
        finish_stages(page, "C05", first_c05)
        check(page.locator("#overall-count").inner_text() == "5 of 8 challenges completed",
              "Fifth completion not counted")
        first_c06 = fill_stage_one(page, "C06",
            "The ball has enough energy to reach the top so its string surely stays taut.")
        check("−1 N" in root_for(page, "C06").locator(".worked").inner_text(),
              "C06 worked reconstruction missing physically impossible negative tension")
        finish_stages(page, "C06", first_c06)
        check(page.locator("#overall-count").inner_text() == "6 of 8 challenges completed",
              "Sixth completion not counted")
        first_c07 = fill_stage_one(page, "C07",
            "I used all the collected chips and forgot that arrivals already move at 1 m/s.")
        check("24 W" in root_for(page,"C07").locator(".worked").inner_text()
              and "15 W" in root_for(page,"C07").locator(".worked").inner_text()
              and "9 W" in root_for(page,"C07").locator(".worked").inner_text(),
              "C07 did not give separate power, kinetic gain and heat checks")
        finish_stages(page, "C07", first_c07)
        check(page.locator("#overall-count").inner_text() == "7 of 8 challenges completed",
              "Seventh completion not counted")
        first_c08 = fill_stage_one(page, "C08",
            "I thought the stiffer spring always stores more energy even with equal final force.")
        check("0.36 J" in root_for(page,"C08").locator(".worked").inner_text()
              and "0.18 J" in root_for(page,"C08").locator(".worked").inner_text(),
              "C08 missing different final-force energy comparison")
        finish_stages(page, "C08", first_c08)
        check(page.locator("#overall-count").inner_text() == "8 of 8 challenges completed",
              "Eighth completion not counted")
        page.reload(wait_until="load")
        check(page.locator("#overall-count").inner_text() == "8 of 8 challenges completed", "Completed progress not restored")
        initial_attempts = [
            ("C01",first_c01), ("C02",first_c02), ("C03",first_c03),
            ("C04",first_c04), ("C05",first_c05), ("C06",first_c06),
            ("C07",first_c07), ("C08",first_c08)
        ]
        for lesson, initial in initial_attempts:
            check(saved_state(page, lesson)["first"] == initial,
                  lesson+" first reasoning was modified after completing all eight lessons")
        check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 3"),
              "Page overflow after completion at "+str(width))
        check(not errors, "JavaScript runtime errors: "+str(errors))

        page.on("dialog", lambda d: d.accept())
        root_for(page, "C01").locator('[data-action="reset"]').click()
        check(saved_state(page, "C01") is None, "C01 reset did not clear local attempt")
        check(saved_state(page, "C02")["first"] == first_c02, "Reset of C01 cleared C02")
        check(page.locator("#overall-count").inner_text() == "7 of 8 challenges completed", "Reset progress incorrect")
        for lesson, initial in initial_attempts[1:]:
            check(saved_state(page, lesson)["first"] == initial,
                  "Resetting C01 unexpectedly cleared " + lesson + " attempt")
        print("PASS: %sx%s C01–C08 all stages, original answers, repair, changed conditions, storage, reset" % (width,height))
    finally:
        context.close()



def test_partial_draft_resume_and_late_topic_hints(browser, base):
    """A child can leave and return before committing. The first locked try stays separate."""
    context=browser.new_context(viewport={"width":390,"height":844})
    try:
        page=context.new_page()
        errors=[]
        page.on("pageerror",lambda e: errors.append(str(e)))
        response=page.goto(base+PATH,wait_until="load")
        check(response and response.status==200,"Draft-resume page failed")
        root=root_for(page,"C08")
        root.locator("textarea").fill("I predict Gold always wins, but I need to compare the two tests.")
        partial=saved_state(page,"C08")
        check(partial["stage"]==0 and "Gold always wins" in partial["predictionDraft"],
              "Typing in prediction is not saved locally")
        page.reload(wait_until="load")
        root=root_for(page,"C08")
        check("Gold always wins" in root.locator("textarea").input_value(),
              "Uncommitted prediction lost after reload")
        root.locator('[data-action="save-prediction"]').click()
        check(root.locator(".stage-card h4").inner_text()=="2. Attempt","Could not enter attempt")
        root.locator('[data-input="kBlue"]').fill("210")
        root.locator('[data-input="testYChoice"]').select_option(label="Gold pad")
        root.locator('[data-input="reason"]').fill("My unfinished first theory is that Gold has more energy in every test.")
        draft=saved_state(page,"C08")
        check(draft["stage"]==1 and draft["first"] is None,
              "Uncommitted first attempt incorrectly treated as locked")
        check(draft["draft"]["kBlue"]=="210" and draft["draft"]["testYChoice"]=="Gold pad",
              "Field values were not saved in draft")
        check("Gold has more energy" in draft["draft"]["reason"],
              "Written reasoning not preserved in draft")
        check(root.locator(".worked").count()==0,"Worked answer leaked into draft stage")
        root.locator('[data-action="next-hint"]').click()
        check("Hint 1:" in root.locator(".progressive-hints").inner_text(),
              "Optional first hint missing for C08")
        check(root.locator(".worked").count()==0,"C08 optional hint leaked worked answer")
        page.reload(wait_until="load")
        root=root_for(page,"C08")
        check(root.locator('[data-input="kBlue"]').input_value()=="210","Draft numeric value lost on reload")
        check(root.locator('[data-input="testYChoice"]').input_value()=="Gold pad","Draft choice lost on reload")
        check("Gold has more energy" in root.locator('[data-input="reason"]').input_value(),
              "Draft explanation lost on reload")
        check("Hint 1:" in root.locator(".progressive-hints").inner_text(),
              "Previously requested hint disappeared on reload")
        root.locator('[data-action="next-hint"]').click()
        check("Hint 2:" in root.locator(".progressive-hints").inner_text(),
              "Second optional hint missing for C08")
        root.locator('[data-action="lock-attempt"]').click()
        state=saved_state(page,"C08")
        check(state["draft"] is None and state["first"]["kBlue"]=="210",
              "Committing did not preserve the original answer and clear draft")
        original=state["first"].copy()
        page.reload(wait_until="load")
        root=root_for(page,"C08")
        check(root.locator(".stage-card h4").inner_text()=="3. Reconstruct",
              "Committed original incorrectly returned to draft stage")
        root.locator('[data-action="save-reconstruction"]').click()
        check(root.locator(".review-model").count()==1,"Model not available to re-check during diagnosis")
        root.locator('[data-input="diagnosis"]').select_option(index=2)
        root.locator('[data-action="save-diagnosis"]').click()
        check(root.locator(".diagnostic-tip").count()==1,"No misconception-specific repair cue")
        root.locator(".review-model summary").click()
        check(root.locator(".review-model .worked").is_visible(),"Cannot open worked explanation in repair")
        root.locator('[data-input$="-repair"]').fill(
            "My repaired model holds final force fixed in Y, so I must calculate new compressions.")
        root.locator('[data-action="save-repair"]').click()
        check(saved_state(page,"C08")["first"]==original,
              "Repair unexpectedly overwrote first response")
        # The next topic and pre-existing local key remain untouched.
        check(saved_state(page,"C07") is None,"C08 writing changed C07 state")
        check(not errors,"JavaScript error in draft resume: "+str(errors))
        print("PASS: partial prediction and attempt drafts, C08 hint persistence, repair reference, immutable first try")
    finally:
        context.close()


def main():
    server, base = local_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for width,height in VIEWPORTS:
                    run_viewport(browser,width,height,base)
                test_partial_draft_resume_and_late_topic_hints(browser,base)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
