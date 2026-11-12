"""Browser regression for the five independent WPE Learn → Challenge teaching candidates."""
from __future__ import annotations
import http.server
import json
import pathlib
import re
import socketserver
import subprocess
import sys
import time
from difflib import SequenceMatcher
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parents[1]
PORT=8768
URL=f"http://127.0.0.1:{PORT}/physics/wpe/learn-challenge.html"
MAP=ROOT/"physics/wpe/learn-challenge-source-map.json"
REVIEW=ROOT/"physics/wpe/learn-challenge-wpe01-review.json"
REVIEW_B34=ROOT/"physics/wpe/learn-challenge-wpe02-b3-b4-review.json"
ART=ROOT/"wpe-learn-challenge-screenshots"
ART.mkdir(exist_ok=True)
SIZES=[(1280,800),(1024,768),(900,1280),(800,1280),(390,844)]

def check(expr, message):
    if not expr: raise AssertionError(message)

def corpus():
    data=json.loads(MAP.read_text(encoding="utf-8"))
    check(len(data["program"])==5,"Expected exactly five subtopic records")
    check(len({x["id"] for x in data["program"]})==5,"Duplicate IDs")
    check(data["auth"]["native_core1a"]=="NOT_ACCEPTED" and data["auth"]["native_core1b"]=="NOT_ACCEPTED","Gate status changed")
    required={"Q7","Q9","Q10","Q11","Q12"}
    check(required.issubset({r["id"] for r in data["source_flags"]}),"Source scan review flags incomplete")
    for row in data["program"]:
        a=row["core1a"]["authored_question"]
        b=row["core1b"]["authored_question"]
        def normalize(s):return re.sub(r"\s+"," ",re.sub(r"[\d.]+","#",s.casefold())).strip()
        score=SequenceMatcher(None,normalize(a),normalize(b)).ratio()
        check(score<0.7,f"Potential cosmetic A/B duplication {row['id']}: {score:.2f}")
        check(len(row["core1b"]["change_of_conditions"])>40, f"Transfer description missing: {row['id']}")
        check(row["core1b"]["option_count"]==4,f"Four choices expected: {row['id']}")
    review=json.loads(REVIEW.read_text(encoding="utf-8"))
    check(data["technical_review"]["status"]=="TECHNICAL_REMEDIATION_ONLY__ACADEMIC_HOLD","Academic review state changed")
    check(review["academic_acceptance"] is False,"WPE-01 must not be marked as academic acceptance")
    check(len(review["witnesses"])==5,"Expected five technical witnesses")
    check(all(r["gate_status"]["B4"]=="REVIEW_REQUIRED" for r in review["witnesses"]),"Fresh reconstruction wrongly accepted")
    check(review["construction_gate_status"]["B5"]=="LIMITED_TECHNICAL_EVIDENCE","Client-side lock must not count as verified first-attempt record")
    b34=json.loads(REVIEW_B34.read_text(encoding="utf-8"))
    check(b34["result"]["B3"].startswith("HOLD") and b34["result"]["B4"].startswith("HOLD"),"B3/B4 reviewer hold silently cleared")
    check(b34["result"]["native_core1a"]=="NOT_ACCEPTED" and b34["result"]["native_core1b"]=="NOT_ACCEPTED","Native admissions changed")
    check(b34["role"].startswith("AUTHOR_EXPOSED"),"WPE-02 review must disclose author exposure")
    check(len(b34["per_construction"])==5,"Missing B3/B4 construction review")
    check({r["id"] for r in b34["per_construction"]}=={r["id"] for r in data["program"]},"B3/B4 review does not cover all existing pairs")
    check(all(r["B3"]["decision"]=="HOLD" and r["B4"]["decision"]=="HOLD" for r in b34["per_construction"]),"Per-construction admission hold cleared")
    check("Take g = 10 m/s²" in next(r for r in data["program"] if r["id"]=="energy-motion")["core1b"]["authored_question"],"Energy challenge missing self-contained g")
    check(data["author_exposed_b3_b4_review"]["status"].startswith("AUTHOR_EXPOSED"),"Missing WPE-02 provenance in source map")
    mom=next(row for row in data["program"] if row["id"]=="momentum-energy")
    check(mom["core1b"]["practice_revision"]==2,"Momentum challenge revision missing")
    check(mom["core1b"]["correct_option_index_AUTHOR_ONLY"]==2,"Momentum answer key not updated")
    check("both momentum and mass change" in mom["core1b"]["change_of_conditions"],"Challenge must change both variables")
    energy=next(row for row in data["program"] if row["id"]=="energy-motion")
    check(energy["core1b"]["practice_revision"]==2,"Energy challenge revision missing")
    check(energy["core1b"]["correct_option_index_AUTHOR_ONLY"]==1,"Energy answer key mismatch")
    check("hilltop 6 m high" in energy["core1b"]["authored_question"],"Independent hilltop challenge missing")
    check("20 m/s" in energy["core1a"]["walkthrough_steps"][3],"Vertical motion teaching absent")
    potential=next(row for row in data["program"] if row["id"]=="potential-force")
    check(potential["core1b"]["practice_revision"]==2,"Potential challenge revision missing")
    check(potential["core1b"]["correct_option_index_AUTHOR_ONLY"]==2,"Potential challenge correct answer not updated")
    check("three open sections" in potential["core1b"]["authored_question"],"Potential challenge must scope straight open intervals")
    check("flat" in potential["core1b"]["change_of_conditions"],"New condition/representation transfer not recorded")
    final=next(row for row in data["program"] if row["id"]=="momentum-fragments")
    check(final["core1b"]["practice_revision"]==2,"Topic 5 challenge revision missing")
    check(final["core1b"]["correct_option_index_AUTHOR_ONLY"]==2,"Topic 5 answer key incorrect")
    check("4 kg toy cart" in final["core1b"]["authored_question"],"Fresh moving-cart question missing")
    check("nonzero" in final["core1b"]["change_of_conditions"],"Moving-start reasoning transfer missing")
    batch=data["batch_completion"]
    check(batch["source_topic_complete_count"]==5 if "source_topic_complete_count" in batch else len(batch["topics"])==5,"Batch completion count mismatch")
    check(batch["release_role"]=="STUDENT_PRACTICE_PREVIEW_NOT_NATIVE_ACADEMIC_ADMISSION","Practice status changed")
    check({r["id"] for r in batch["topics"]}=={r["id"] for r in data["program"]},"Batch inventory incomplete")
    check(data["learner_facing_iteration"]["id"]=="WPE_TOPIC_05_PUSH_APART_ENERGY","Final learner iteration not updated")
    journey=data["student_journey_batch"]
    check(journey["id"]=="WPE_STUDENT_JOURNEY_5_TOPICS","Student practice batch record missing")
    check(journey["learner_testing"].startswith("AUTOMATED_SIMULATIONS_ONLY"),"Do not claim real student testing")
    check(journey["academic_admissions_changed"] is False,"Practice flow must not change academic admissions")
    print("PASS: five distinct question pairs, technical review, practice flow, and academic holds")

def test(browser):
    for w,h in SIZES:
        context=browser.new_context(viewport={"width":w,"height":h},device_scale_factor=1)
        page=context.new_page()
        errors=[]
        page.on("pageerror", lambda e:errors.append(str(e)))
        result=page.goto(URL,wait_until="load",timeout=25000)
        check(result and result.status==200,f"Failed to load at {w}")
        cards=page.locator("article.lesson")
        check(cards.count()==5, f"Expected five lesson cards at {w}")
        check(page.locator(".guide-panel").count()==5 and page.locator(".challenge-panel").count()==5,"Missing Core1A / Core1B panels")
        check(page.locator(".topic-visual svg").count()==5,"Original explanatory diagrams missing")
        check(page.locator(".reason-tip").count()==5,"Topic-specific reasoning prompts missing")
        check(page.locator(".concept-mini").count()==1,"Sign-of-work teaching contrasts missing")
        check(page.locator(".lesson-next").count()==5,"Next-topic links missing")
        check(page.locator("#practice-progress-label").inner_text()=="0 of 5 worked checks viewed","Initial practice progress wrong")
        check(page.locator(".contents .topic-status").count()==5,"Topic practice badges missing")
        guide=page.locator(".guide-panel")
        check("single two-kilogram trolley" in guide.nth(1).locator("svg").get_attribute("aria-label"),"Momentum guide diagram still shows challenge carts")
        check("single energy line that descends" in guide.nth(3).locator("svg").get_attribute("aria-label"),"Potential guide diagram still previews challenge slopes")
        check("two carts separate from rest" in guide.nth(4).locator("figcaption").inner_text(),"Fragment guide diagram still previews moving parent")
        check("60 J" not in guide.nth(2).locator("svg").text_content(),"Core1A visual leaks ridge answer")
        check("Take g = 10 m/s²" in cards.nth(2).locator(".challenge-panel .scenario").inner_text(),"Independent energy challenge omitted gravity assumption")
        check("WPE-02 B3/B4 author-exposed review" in page.locator("#separation").inner_text(),"B3/B4 review record not linked")
        check(not errors,f"JS errors at {w}: {errors}")
        wide=page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(wide<=2,f"Horizontal overflow {wide}px at {w}")
        card=cards.first
        check(card.locator(".solution-area").inner_text().strip()=="","Answer in initial live DOM")
        check(card.locator('[data-action="hint"]').is_disabled(),"Hints should initially be locked")
        check(card.locator('[data-action="solution"]').is_disabled(),"Solution should initially be locked")
        card.locator('[data-action="lock"]').click()
        check("Choose an answer" in card.locator(".feedback").inner_text(),"Must require an answer")
        card.locator('input[type=radio]').first.check()
        card.locator('[data-action="lock"]').click()
        check("short sentence" in card.locator(".feedback").inner_text(),"Must require reasoning")
        card.locator(".reason").fill("Both resistance forces oppose motion, so their work is negative.")
        card.locator('[data-action="lock"]').click()
        check(card.locator('[data-action="lock"]').is_disabled(),"Attempt not locked")
        check(card.locator('[data-action="hint"]').is_enabled(),"Hint 1 locked after attempt")
        check(card.locator('[data-action="solution"]').is_enabled(),"Worked check should be optional after locking")
        check("first try saved" in card.locator(".lesson-progress").inner_text(),"First try status missing")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:work-sign')") is not None,"Locked attempt not saved locally")
        page.reload(wait_until="load")
        check(card.locator('[data-action="lock"]').is_disabled(),"First attempt lock failed to survive reload")
        check("Both resistance forces" in card.locator(".reason").input_value(),"Reason failed to survive reload")
        check(card.locator('[data-action="hint"]').is_enabled(),"Hints not restored after reload")
        check(card.locator(".solution-area").is_hidden(),"Solution must be hidden")
        card.locator('[data-action="hint"]').click()
        check(card.locator(".hint-area p").count()==1,"Hint 1 missing")
        page.reload(wait_until="load")
        check(card.locator(".hint-area p").count()==1,"Hint 1 lost or duplicated after reload")
        check(card.locator('[data-action="solution"]').is_enabled(),"Worked check should remain available after one optional hint")
        card.locator('[data-action="hint"]').click()
        check(card.locator(".hint-area p").count()==2,"Hint 2 missing")
        check(card.locator('[data-action="solution"]').is_enabled(),"Solution should be available after both hints")
        card.locator('[data-action="solution"]').click()
        check(card.locator(".solution-area").is_visible(),"Worked check not revealed")
        check("−32 J" in card.locator(".solution-area").inner_text(),"Incorrect work solution")
        check(card.locator(".solution-area ul li").count()==2,"Student self-check prompts missing")
        check("1 of 5 worked checks viewed" in page.locator("#practice-progress-label").inner_text(),"Progress did not advance after worked check")
        check(card.locator(".lesson-progress").inner_text().endswith("worked check viewed"),"Per-topic viewed status missing")
        check(card.locator(".choice input:checked").is_disabled(),"First attempt answer should remain locked")
        page.reload(wait_until="load")
        check(card.locator(".solution-area").is_visible(),"Solution reveal was not restored")
        check("Changed-condition reflection" in card.locator(".solution-area").inner_text(),"Missing transfer reflection")
        # verify other cards remain unmodified until user interacts with each
        for i in range(1,5):
            row=cards.nth(i)
            check(row.locator('[data-action="lock"]').is_enabled(),f"Card {i+1} unexpectedly locked")
            check(row.locator(".solution-area").is_hidden(),f"Card {i+1} accidentally leaked solution")
        momentum=cards.nth(1)
        check("toy trolley" in momentum.locator(".guide-panel .scenario").inner_text(),"Kid-friendly momentum guide missing")
        check(momentum.locator(".pattern-table tbody tr").count()==4,"K versus p comparison table incomplete")
        check("both" in momentum.locator(".transfer-note").inner_text().lower(),"Two-variable warning missing")
        check("two mystery toy carts" in momentum.locator(".challenge-panel h3").inner_text(),"New cart challenge not shown")
        check("Cart B has twice as much" in momentum.locator(".choice").nth(2).inner_text(),"Option C not aligned")
        momentum.locator('input[type="radio"]').nth(2).check()
        momentum.locator(".reason").fill("I used kinetic energy equals momentum squared divided by twice the mass for both toy carts.")
        momentum.locator('[data-action="lock"]').click()
        check(momentum.locator('[data-action="lock"]').is_disabled(),"Momentum attempt failed to lock")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:momentum-energy-r2')") is not None,"Revised momentum attempt not saved with revision")
        check(momentum.locator('[data-action="solution"]').is_enabled(),"Child should be allowed to check without using hints")
        momentum.locator('[data-action="solution"]').click()
        check(momentum.locator(".hint-area").is_hidden(),"Optional hints appeared without student asking")
        check("Cart B has twice" in momentum.locator(".solution-area").inner_text(),"Incorrect new momentum answer")
        page.reload(wait_until="load")
        check("Cart B has twice" in cards.nth(1).locator(".solution-area").inner_text(),"Revised momentum worked check not restored")
        check("2 of 5 worked checks viewed" in page.locator("#practice-progress-label").inner_text(),"Progress did not restore after direct check")
        cards.nth(1).locator('[data-action="reset"]').click()
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:momentum-energy-r2')") is None,"Momentum revision saved state was not cleared")
        energy=cards.nth(2)
        check("2 kg toy cart" in energy.locator(".guide-panel .scenario").inner_text(),"New energy guide not shown")
        check(energy.locator(".energy-pattern tbody tr").count()==4,"Height/energy table missing rows")
        check("K can be zero" in energy.locator(".energy-pattern").inner_text(),"Turning-point teaching missing")
        check("velocity" in energy.locator(".transfer-note").inner_text(),"Vertical-time comparison missing")
        check("can the cart reach the flag?" in energy.locator(".challenge-panel h3").inner_text().lower(),"New hilltop challenge not shown")
        check("The cart lacks the energy" in energy.locator(".choice").nth(1).inner_text(),"Hilltop answer option B missing")
        energy.locator('input[type="radio"]').nth(1).check()
        energy.locator(".reason").fill("The total energy must be at least the potential energy at every point, including the hilltop.")
        energy.locator('[data-action="lock"]').click()
        check(energy.locator('[data-action="lock"]').is_disabled(),"Energy first attempt was not locked")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:energy-motion-r2')") is not None,"New energy attempt not saved with question revision")
        energy.locator('[data-action="hint"]').click()
        energy.locator('[data-action="hint"]').click()
        energy.locator('[data-action="solution"]').click()
        check("60 J" in energy.locator(".solution-area").inner_text(),"Hilltop calculation missing from worked check")
        page.reload(wait_until="load")
        check("cart cannot reach the flag" in cards.nth(2).locator(".solution-area").inner_text(),"Energy worked check did not survive reload")
        cards.nth(2).locator('[data-action="reset"]').click()
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:energy-motion-r2')") is None,"Energy saved attempt not cleared")
        potential=cards.nth(3)
        check("sloping energy line" in potential.locator(".guide-panel h3").inner_text(),"Potential energy guide not refreshed")
        check(potential.locator(".slope-rules tbody tr").count()==3,"Missing rising-flat-falling slope guide")
        check("opposite" in potential.locator(".transfer-note").inner_text().lower() or "minus sign" in potential.locator(".transfer-note").inner_text().lower(),"Negative-gradient teaching missing")
        check(potential.locator(".challenge-visual svg").count()==1,"Distinct challenge graph missing")
        check("four positions" in potential.locator(".challenge-panel .scenario").inner_text(),"New challenge stem missing")
        check("−4 N, 0 N, +3 N" in potential.locator(".choice").nth(2).inner_text(),"Correct three-interval option C missing")
        check(potential.locator(".solution-area").is_hidden(),"Potential answer leaked into initial visible DOM")
        potential.locator('input[type="radio"]').nth(2).check()
        potential.locator(".reason").fill("The force equals minus the potential energy slope on every straight interval; the flat interval is zero.")
        potential.locator('[data-action="lock"]').click()
        check(potential.locator('[data-action="lock"]').is_disabled(),"Potential first attempt not locked")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:potential-force-r2')") is not None,"Potential updated answer not saved under revision")
        potential.locator('[data-action="hint"]').click()
        potential.locator('[data-action="hint"]').click()
        potential.locator('[data-action="solution"]').click()
        check("Choice C is correct" in potential.locator(".solution-area").inner_text(),"Potential-force worked check does not match key")
        page.reload(wait_until="load")
        check("Choice C is correct" in cards.nth(3).locator(".solution-area").inner_text(),"Revised potential answer lost after reload")
        cards.nth(3).locator('[data-action="reset"]').click()
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:potential-force-r2')") is None,"Potential attempt was not cleared")
        final=cards.nth(4)
        check("spring-powered toy carts" in final.locator(".guide-panel h3").inner_text(),"Final toy-cart guide not shown")
        check(final.locator(".momentum-summary tbody tr").count()==2,"Momentum/energy conservation table missing")
        check("Total momentum" in final.locator(".momentum-summary").inner_text(),"Momentum distinction missing")
        check("Total kinetic energy" in final.locator(".momentum-summary").inner_text(),"Energy distinction missing")
        check("already rolling right" in final.locator(".challenge-panel .scenario").inner_text(),"Moving-start challenge not shown")
        check("+2 m/s (right); kinetic energy increases by 6 J" in final.locator(".choice").nth(2).inner_text(),"Topic 5 option C mismatches result")
        check(final.locator(".hint-area").is_hidden() and final.locator(".solution-area").is_hidden(),"Topic 5 solution exposed before attempt")
        final.locator('input[type="radio"]').nth(2).check()
        final.locator(".reason").fill("The initial momentum is 12 kg m/s and the two outgoing carts must share it, so the heavy cart has velocity two metres per second.")
        final.locator('[data-action="lock"]').click()
        check(final.locator('[data-action="lock"]').is_disabled(),"Topic 5 initial response not locked")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:momentum-fragments-r2')") is not None,"Topic 5 attempt not saved")
        final.locator('[data-action="hint"]').click()
        final.locator('[data-action="hint"]').click()
        final.locator('[data-action="solution"]').click()
        check("Total kinetic energy increases by 6 J" in final.locator(".solution-area").inner_text(),"Topic 5 worked check incorrect")
        page.reload(wait_until="load")
        check("Choice C is correct" in cards.nth(4).locator(".solution-area").inner_text(),"Final challenge solution not restored after reload")
        cards.nth(4).locator('[data-action="reset"]').click()
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:momentum-fragments-r2')") is None,"Final challenge storage not cleared")
        check(page.locator("#learning-path-ready").is_visible(),"Five-topic student exploration summary missing")
        check(page.locator("#learning-path-ready a").count()==2,"Student start/finish links not found")
        if w in (1280,1024,900,800):
            page.screenshot(path=str(ART/f"learn-challenge-{w}x{h}.png"),full_page=False)
        card.locator('[data-action="reset"]').click()
        check(card.locator('[data-action="lock"]').is_enabled(),"Clear saved attempt did not reset form")
        check(page.evaluate("localStorage.getItem('g9:wpe:learn-challenge:v2:work-sign')") is None,"Clear saved attempt left local record behind")
        check(card.locator(".solution-area").is_hidden(),"Clear saved attempt left answer visible")
        print(f"PASS: {w}x{h} layout, interaction, answer protection")
        context.close()

def test_child_journeys(browser):
    context=browser.new_context(viewport={"width":390,"height":844},device_scale_factor=1)
    try:
        page=context.new_page()
        page.goto(URL,wait_until="load")
        cards=page.locator("article.lesson")
        wrong_options=[1,0,0,0,0]
        for idx,wrong in enumerate(wrong_options):
            row=cards.nth(idx)
            check(row.locator('[data-action="solution"]').is_disabled(),f"Topic {idx+1} revealed before a first attempt")
            row.locator('input[type="radio"]').nth(wrong).check()
            row.locator(".reason").fill("I chose this answer because I am checking the idea in the question, but I may have missed a rule.")
            row.locator('[data-action="lock"]').click()
            check(row.locator('[data-action="solution"]').is_enabled(),f"Topic {idx+1} incorrectly forces hints")
            row.locator('[data-action="solution"]').click()
            output=row.locator(".solution-area").inner_text()
            check("One possible mix-up:" in output,f"Topic {idx+1} missing misconception feedback")
            check("Check your own explanation:" in output,f"Topic {idx+1} missing reasoning self-check")
            check("Changed-condition reflection:" in output,f"Topic {idx+1} missing transfer reflection")
            check(row.locator(".solution-area ul li").count()==2,f"Topic {idx+1} self-check items incomplete")
        check(page.locator("#practice-progress-label").inner_text()=="5 of 5 worked checks viewed","All-five practice progress incorrect")
        check(page.locator(".contents .topic-status").filter(has_text="Worked check viewed").count()==5,"Five topic statuses incorrect")
        page.reload(wait_until="load")
        check(page.locator("#practice-progress-label").inner_text()=="5 of 5 worked checks viewed","Practice progress failed to restore after reload")
        for idx in range(5):
            cards.nth(idx).locator('[data-action="reset"]').click()
        check(page.locator("#practice-progress-label").inner_text()=="0 of 5 worked checks viewed","Practice progress failed to reset")
        check(page.locator(".contents .topic-status").filter(has_text="Not started").count()==5,"Cleared topic statuses incorrect")
        print("PASS: five incorrect-choice feedback journeys, optional hints and restored progress")
    finally:
        context.close()


def test_wpe_learning_route(browser):
    """Cross-page browser smoke, not independent academic or learner evidence."""
    root=f"http://127.0.0.1:{PORT}"
    wrapper=(ROOT/"physics/wpe/question-bank.html").read_text(encoding="utf-8")
    check("location.replace(" in wrapper and "preview/question-status.html" in wrapper,
          "Existing full-width Question Bank redirect changed")
    for width,height in ((1024,768),(390,844)):
        context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
        try:
            page=context.new_page()
            errors=[]
            page.on("pageerror",lambda err:errors.append(str(err)))
            response=page.goto(root+"/physics/wpe/index.html",wait_until="load")
            check(response is not None and response.status==200,"WPE hub unavailable")
            page.locator('.quicklinks a[href="learn-challenge.html"]').click()
            check("/physics/wpe/learn-challenge.html" in page.url,"Guided path inaccessible from hub")
            check(page.locator("article.lesson").count()==5,"Five guided topic pairs lost")
            check(page.locator("#wpe-related-pages a").count()==5,"Related pages navigation incomplete")
            page.locator("details.review-metadata summary").click()
            page.locator('#wpe-related-pages a[href="../../preview/physics-wpe.html"]').click()
            check("/preview/physics-wpe.html" in page.url,"Foundation inaccessible")
            check(page.locator("#wpe-learning-route").count()==1,"Foundation route missing")
            page.locator('#wpe-learning-route a[href="../physics/wpe/learn-challenge.html#potential-force"]').click()
            check(page.url.endswith("/physics/wpe/learn-challenge.html#potential-force"),"Concept deep link lost")
            check(page.locator("#potential-force").count()==1,"Linked concept anchor missing")
            page.locator("details.review-metadata summary").click()
            page.locator('#wpe-related-pages a[href="../../preview/practice.html"]').click()
            check("/preview/practice.html" in page.url,"Spring practice inaccessible")
            check(page.locator("#btn-reveal-solution").is_hidden(),"Spring solution exposed before attempt")
            check(page.locator('#wpe-learning-route a[href="../physics/wpe/question-bank.html"]').count()==1,
                  "Spring practice missing Question Bank entry")
            # The public bank wrapper intentionally redirects to GitHub Pages; exercise its
            # real local target directly to keep the preview test self-contained and offline.
            response=page.goto(root+"/preview/question-status.html",wait_until="load")
            check(response is not None and response.status==200,"Full-width bank missing")
            check("0 academically admitted" in page.locator("header").inner_text(),"Source hold missing")
            page.locator('.c2-chapterbar a[href="../physics/wpe/index.html"]').first.click()
            check("/physics/wpe/index.html" in page.url,"Bank cannot return to WPE hub")
            page.locator('.quicklinks a[href="../../preview/batches/reader.html"]').click()
            check("/preview/batches/reader.html" in page.url,"Technical examples inaccessible")
            check(page.locator(".disclose").count()==1,"Examples disclosure missing")
            check(page.locator('nav[aria-label="Collection navigation"] a[href="../../physics/wpe/learn-challenge.html"]').count()==1,
                  "Examples guided return missing")
            check(not errors,f"Route page JavaScript errors at {width}: {errors}")
            check(page.evaluate("document.documentElement.scrollWidth - innerWidth") <= 2,
                  f"Technical reader overflow at {width}")
        finally:
            context.close()
    print("PASS: WPE five-surface learning route, anchored return, disclosure and attempt gates.")


def test_wpe_question_reasoning_return(browser):
    """One source-ID route round trip; no academic acceptance or learner mastery inferred."""
    root=f"http://127.0.0.1:{PORT}"
    for width,height in ((1024,768),(390,844)):
        context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
        try:
            page=context.new_page()
            errors=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            result=page.goto(root+"/preview/question-status.html?question=EX-M79",wait_until="load")
            check(result is not None and result.status==200,"Question reader not accessible")
            check(page.locator(".qtitle").inner_text()=="EX-M79","Exact question ID link failed")
            check(page.locator("#solution-container .solution").count()==0,"Question solution visible before attempt")
            page.locator('.source-note a[href*="reasoning-paths.html?question=EX-M79"]').click()
            page.locator("#route-status").filter(has_text="EX-M79").wait_for()
            check(page.locator('#WPE-C03[data-match="yes"]').count()==1,"Constant-power author theme not identified")
            check("0 academically admitted" in page.locator(".route-alert").inner_text(),"Academic admission warning absent")
            page.locator('#WPE-C03 a[href*="learn-challenge.html?question=EX-M79#energy-motion"]').click()
            check(page.url.endswith("learn-challenge.html?question=EX-M79#energy-motion"),"Foundation link lost question context")
            check(page.locator("#energy-motion").count()==1,"Foundation anchor missing")
            page.locator("details.review-metadata summary").click()
            page.locator('#reasoning-route-return a[href*="question-status.html?question=EX-M79"]').click()
            check(page.locator(".qtitle").inner_text()=="EX-M79","Return did not select exact question")
            check(page.locator("#solution-container .solution").count()==0,"Return exposed solution")
            page.goto(root+"/preview/question-status.html?question=UNKNOWN-QUESTION",wait_until="load")
            check("Unknown question link" in page.locator("#route-status").inner_text(),"Unknown question failed-open")
            check(page.locator(".qtitle").inner_text()!="UNKNOWN-QUESTION","Invented question selected")
            page.goto(root+"/physics/wpe/reasoning-paths.html?question=EX-M81",wait_until="load")
            page.locator("#route-status").filter(has_text="absent from the 74-entry").wait_for()
            check(page.locator("#return-links a").count()==0,"Absent reader record got a return link")
            page.goto(root+"/physics/wpe/reasoning-paths.html?question=WEP07-03",wait_until="load")
            page.locator("#route-status").filter(has_text="WEP07-03").wait_for()
            check(page.locator('#WPE-E01[data-match="yes"]').count()==1,"WEP07-03 author extension not linked")
            check(page.locator('#WPE-E01 .route-links a[href*="learn-challenge"]').count()==0,
                  "Unapproved extension got a false foundation lesson")
            check(not errors,f"Reasoning-route browser errors at {width}: {errors}")
            check(page.evaluate("document.documentElement.scrollWidth-innerWidth")<=2,
                  f"Reasoning-route horizontal overflow at {width}")
        finally:
            context.close()
    print("PASS: question → provisional route → existing foundation → same question; invalid/absent ID and answer leakage blocked.")


def test_wpe_core2_r2_hint_safety(browser):
    """Batched candidate cue renderer check; never an academic science approval."""
    bank=json.loads((ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json").read_text(encoding="utf-8"))
    questions={q["source_id"]:q for q in bank["questions"]}
    curated=questions["EX-M8"]
    raw=questions["EX-M69"]
    check(len(curated["scaffolds"])==2 and len(curated["hints"])==3,
          "EX-M8 source/cue inventory changed")
    check(not raw.get("scaffolds") and len(raw["hints"])==3,
          "EX-M69 raw-hint inventory changed")
    for width,height in ((1024,768),(390,844)):
        ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
        try:
            page=ctx.new_page()
            errors=[]
            page.on("pageerror",lambda err:errors.append(str(err)))
            response=page.goto(f"http://127.0.0.1:{PORT}/preview/question-status.html?question=EX-M8",wait_until="load")
            check(response is not None and response.status==200,"Authored-cue reader unavailable")
            check(page.locator(".qtitle").inner_text()=="EX-M8","EX-M8 direct source link failed")
            hints=page.locator("#question-root details.hint")
            check(hints.count()==2,"EX-M8 must show exactly two new student-safe cues")
            displayed=" ".join(hints.nth(i).text_content() or "" for i in range(hints.count()))
            check(all(s["text"] in displayed for s in curated["scaffolds"]),
                  "EX-M8 curated cue not displayed")
            check(all(h["text"] not in displayed for h in curated["hints"]),
                  "EX-M8 raw source hint leaked in place of curated cue")
            check("crux move:" not in displayed.lower(),"EX-M8 Crux Move leaked")
            check(page.locator("#solution-container .solution").count()==0,"EX-M8 answer leaked before attempt")
            page.locator('.source-note a[href*="reasoning-paths.html?question=EX-M8"]').click()
            page.locator("#route-status").filter(has_text="No source-bound route exists for EX-M8").wait_for()
            check(page.locator("#return-links a").count()==0,
                  "Unmapped EX-M8 must not get an invented proposed prerequisite route")
            response=page.goto(f"http://127.0.0.1:{PORT}/preview/question-status.html?question=EX-M69",wait_until="load")
            check(response is not None and response.status==200,"Unscaffolded-hint reader unavailable")
            check(page.locator(".qtitle").inner_text()=="EX-M69","EX-M69 direct link failed")
            hints=page.locator("#question-root details.hint")
            check(hints.count()==2,"EX-M69 must defer exactly one explicit Crux Move hint")
            displayed=" ".join(hints.nth(i).text_content() or "" for i in range(hints.count()))
            check("crux move:" not in displayed.lower(),"EX-M69 method spoiler leaked")
            check(all(h["text"] in displayed for h in raw["hints"] if "crux move" not in h["text"].lower()),
                  "Remaining source hints incorrectly removed")
            check(page.locator("#solution-container .solution").count()==0,"EX-M69 answer leaked before attempt")
            page.locator('.source-note a[href*="reasoning-paths.html?question=EX-M69"]').click()
            page.locator("#route-status").filter(has_text="EX-M69").wait_for()
            check(page.locator('#WPE-C03[data-match="yes"]').count()==1,"Mapped author theme C03 missing")
            page.locator('#return-links a[href*="question-status.html?question=EX-M69"]').click()
            check(page.locator(".qtitle").inner_text()=="EX-M69","Mapped EX-M69 return lost exact source")
            check(page.locator("#question-root details.hint").count()==2,"EX-M69 hint deferral lost after return")
            check(page.locator("#solution-container .solution").count()==0,"EX-M69 answer leaked after return")
            check(not errors,f"Hint safety JavaScript errors at {width}: {errors}")
            check(page.evaluate("document.documentElement.scrollWidth-innerWidth")<=2,
                  f"Candidate hint reader horizontal overflow at {width}")
        finally:
            ctx.close()
    print("PASS: EX-M8 curated cues and EX-M69 Crux Move deferral, exact-question return and no pre-attempt answer at desktop/mobile.")

def main():
    corpus()
    server=subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        import urllib.request
        for _ in range(60):
            try: urllib.request.urlopen(URL,timeout=0.4);break
            except Exception: time.sleep(.2)
        else: raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try:
                test(browser)
                test_child_journeys(browser)
                test_wpe_learning_route(browser)
                test_wpe_question_reasoning_return(browser)
                test_wpe_core2_r2_hint_safety(browser)
            finally:browser.close()
        print("PASS: Five authored pairs and five viewport browser checks.")
    finally:
        server.terminate();server.wait(timeout=8)

if __name__=="__main__":main()
