"""WPE R2 source-routing acceptance in real desktop/mobile Chromium.

Source custody and technical behavior only; not a student-achievement or academic claim.
Existing six-stage suites separately check first attempts, staged hints and repairs.
"""
from __future__ import annotations

import copy
from functools import partial
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
COVERAGE=json.loads((ROOT/"physics/wpe/learning-coverage-r1.json").read_text(encoding="utf-8"))
BANK=json.loads((ROOT/"workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json").read_text(encoding="utf-8"))
GATE="/physics/wpe/learn-challenge.html"
CASES={"EX-M50":"F04","EX-M92":"F05","EX-M96":"F06","EX-M106":"F07","EX-N27":"F08"}
LEGACY=[r for r in COVERAGE["questions"] if r["lesson_href"].startswith("study-bridge.html")]
TARGET_PAGE=lambda lesson:("d3d4-self-tutor.html" if lesson.startswith("C") else
                           "extension-learning.html" if lesson.startswith("E") else
                           "focused-journeys.html" if int(lesson[1:])<=3 else
                           "gap-journeys.html")

def require(ok,why):
    if not ok:raise AssertionError(why)

def server():
    srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    srv.daemon_threads=True
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    return srv,f"http://127.0.0.1:{srv.server_port}"

def bound_url(row):
    return TARGET_PAGE(row["primary_lesson"])+"?question="+row["source_id"]+"#"+row["primary_lesson"]

def exhaustive_selector(page,base,width):
    page.goto(base+GATE)
    page.locator("#question-route-status").filter(has_text="of 74 source questions shown").wait_for(timeout=20000)
    require("48 related-only" in page.locator("#question-route-status").inner_text(),"Related-only cases not distinguished")
    require(page.locator(".skill-tabs [role=tab]").count()==4,"Published skill sub-tabs lost")
    expected={q["source_id"]:q["stem_sha256"] for q in BANK["questions"]}
    require(len(expected)==len(COVERAGE["questions"])==74,"Source inventory not unique")
    require(len(LEGACY)==41,"Legacy bridge inventory changed")
    for row in COVERAGE["questions"]:
        source=row["source_id"]
        require(row["stem_sha256"]==expected[source],source+" source hash mismatch")
        page.locator("#question-pick").select_option(source)
        require(source in page.locator("#question-plan h3").inner_text(),source+" selector lost identity")
        link=page.locator("#question-plan .primary-link")
        require(link.count()==1,source+" has no verified lesson link")
        require(link.get_attribute("href").endswith(bound_url(row)),source+" wrong direct target "+str(link.get_attribute("href")))
        require(page.locator("#question-plan .fit-explanation").count()==1,source+" missing fit distinction")
        if row["fit"]=="RELATED_BRIDGE":
            require("NOT the complete reasoning" in page.locator("#question-plan").inner_text(),source+" falsely claims complete teaching")
        require(page.locator("#question-plan .source-link").get_attribute("href").endswith("question="+source),source+" source return wrong")
    print(f"PASS {width}px: all 74 source selector routes and honest fit labels; 41 legacy direct resolutions")

def five_gap_roundtrips(page,base,width):
    for source,lesson in CASES.items():
        page.goto(base+GATE+"?question="+source+"#question-routes")
        link=page.locator("#question-plan .primary-link")
        link.wait_for()
        require(link.get_attribute("href").endswith("gap-journeys.html?question="+source+"#"+lesson),source+" invalid gap route")
        link.click()
        require(page.url.endswith("gap-journeys.html?question="+source+"#"+lesson),source+" wrong gap URL")
        page.locator("#source-journey:not([hidden])").wait_for()
        require(page.locator("#current-title").inner_text().startswith(lesson+" ·"),source+" wrong lesson")
        require(page.locator("#source-return").get_attribute("href").endswith("question="+source),source+" wrong source return")
        require(page.locator("iframe").count()==0,"An iframe was used")
        page.locator("#source-return").click()
        require(page.locator(".qtitle").inner_text()==source,source+" exact original question lost")
        require(page.locator("#solution-container .solution").count()==0,source+" original answer revealed early")
    print(f"PASS {width}px: five F04–F08 selector → journey → original round trips, zero answer leak")

def legacy_roundtrips(page,base,width):
    for row in LEGACY:
        source,lesson=row["source_id"],row["primary_lesson"]
        page.goto(base+GATE+"?question="+source+"#question-routes")
        link=page.locator("#question-plan .primary-link")
        link.wait_for()
        require(link.get_attribute("href").endswith(bound_url(row)),source+" legacy route did not canonicalize")
        link.click()
        require(page.url.endswith(bound_url(row)),source+" failed legacy direct lesson")
        require(page.locator("iframe").count()==0,source+" legacy iframe")
        page.locator("#source-journey:not([hidden])").wait_for()
        # Some C/E lessons use a slightly different return control.
        ret=page.locator("#source-journey-return") if lesson.startswith("C") else page.locator("#source-return")
        require(ret.count()==1 and ret.is_visible(),source+" missing verified source return")
        ret.click()
        require(page.locator(".qtitle").inner_text()==source,source+" legacy return mismatched")
        require(page.locator("#solution-container .solution").count()==0,source+" legacy link leaked original answer")
    print(f"PASS {width}px: all {len(LEGACY)} legacy bridge records open original lessons directly and return without iframe")

def mismatch_and_tamper(browser,base,width,height):
    cases=[
      "https://example.invalid/gap-journeys.html?question=EX-M96#F06",
      "gap-journeys.html?question=EX-M50#F06",
      "focused-journeys.html?question=EX-M96#F06",
      "gap-journeys.html?question=EX-M96#F05",
      "gap-journeys.html?question=EX-M96&unexpected=1#F06",
      "gap-journeys.html?question=EX-M96&question=EX-M96#F06",
      "../gap-journeys.html?question=EX-M96#F06",
      "study-bridge.html?question=EX-M96&lesson=F05"
    ]
    for poisoned in cases:
        ctx=browser.new_context(viewport={"width":width,"height":height})
        page=ctx.new_page()
        changed=copy.deepcopy(COVERAGE)
        row=next(x for x in changed["questions"] if x["source_id"]=="EX-M96")
        row["lesson_href"]=poisoned
        payload=json.dumps(changed)
        page.route("**/physics/wpe/learning-coverage-r1.json",lambda route:
                   route.fulfill(status=200,content_type="application/json",body=payload))
        page.goto(base+GATE+"?question=EX-M96#question-routes")
        page.locator("#question-plan h3").wait_for()
        require(page.locator("#question-plan .primary-link").count()==0,"Untrusted lesson route was accepted: "+poisoned)
        require(page.locator("#question-plan .no-lesson").count()==1,"Tampered route did not fail closed")
        ctx.close()
    for url in ("gap-journeys.html?question=EX-M50#F05","gap-journeys.html?question=UNKNOWN-ID#F04"):
        ctx=browser.new_context(viewport={"width":width,"height":height})
        page=ctx.new_page()
        page.goto(base+"/physics/wpe/"+url)
        page.locator("#source-journey:not([hidden])").wait_for()
        require(page.locator("#source-return").is_hidden(),"Wrong pairing inferred an original return: "+url)
        ctx.close()
    print(f"PASS {width}px: 8 poisoned URLs rejected and gap journey source mismatch refused")

def reader_gap_links(page,base,width):
    for source,lesson in CASES.items():
        page.goto(base+"/preview/question-status.html?question="+source)
        require(page.locator(".qtitle").inner_text()==source,"Reader failed source")
        link=page.locator(f'#interactive-lesson-links a[href*="gap-journeys.html?question={source}#{lesson}"]')
        link.wait_for(timeout=15000)
        require(link.count()==1,source+" reader missing direct gap lesson")
        require(page.locator("#solution-container .solution").count()==0,source+" reader exposed answer")
    print(f"PASS {width}px: original reader links all five source-bound gap journeys")

def main():
    srv,base=server()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for width,height in ((1280,800),(390,844)):
                    ctx=browser.new_context(viewport={"width":width,"height":height})
                    page=ctx.new_page()
                    exhaustive_selector(page,base,width)
                    five_gap_roundtrips(page,base,width)
                    legacy_roundtrips(page,base,width)
                    reader_gap_links(page,base,width)
                    ctx.close()
                    mismatch_and_tamper(browser,base,width,height)
            finally:browser.close()
    finally:srv.shutdown();srv.server_close()

if __name__=="__main__":main()
