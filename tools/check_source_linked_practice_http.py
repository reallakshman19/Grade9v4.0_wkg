#!/usr/bin/env python3
"""Actual generated Pages HTTP Chromium for Chemistry/Biology source-only practice.

No original question text is imported. All local attempts are unverified.
"""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


def check(site: Path) -> None:
    stage=site.resolve()
    manifest=json.loads((stage/"PUBLIC_PREVIEW_MANIFEST.json").read_text("utf-8"))
    assert manifest["source_linked_recovery"]["academic_admission"]=="HOLD"
    assert manifest["source_linked_recovery"]["question_bodies_published"]==0
    assert manifest["source_linked_recovery"]["core1_missing_reproducible_modules"]==18
    assert manifest["core1ab_unpublished_constructions"]==18
    assert manifest["academic_approval"]=="HOLD"
    for f in ("nsejs/biology/question-bank.html","nsejs/chemistry/question-bank.html",
              "nsejs/js/source-linked-exam-practice.js",
              "nsejs/data/source-linked-practice.v1.json","nsejs/data/core1-recovery.v1.json"):
        assert f in manifest["files"] and (stage/f).is_file(),f
    srv=ThreadingHTTPServer(("127.0.0.1",0),
          partial(SimpleHTTPRequestHandler,directory=str(stage)))
    Thread(target=srv.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(srv.server_port)
    checks=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,height in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(viewport={"width":width,"height":height},
                                        has_touch=True,is_mobile=True)
                page=ctx.new_page()
                page.route("https://cdn.jsdelivr.net/**",lambda route:
                    route.fulfill(status=200,content_type="application/javascript",body=""))
                errors=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                try:
                    for subject in ("chemistry","biology"):
                        response=page.goto(base+f"/nsejs/{subject}/index.html",
                                           wait_until="domcontentloaded",timeout=20000)
                        assert response.status==200
                        panel=page.locator("#source-linked-external-practice")
                        assert panel.count()==1 and "HOLD" in panel.inner_text()
                        panel.get_by_role("link",name="Open source-linked practice notebook").click()
                        page.wait_for_url("**/nsejs/"+subject+"/question-bank.html")
                        page.locator("#paper-practice-form:visible").wait_for(timeout=15000)
                        assert "not a complete NSEJS" in page.locator("body").inner_text()
                        assert page.locator(".paper-source-card").count()==5
                        assert page.locator("#paper-practice-form").get_attribute("hidden") is None
                        assert page.locator("iframe").count()==0
                        assert page.locator('a[href^="https://"][target="_blank"]').count()>=5
                        # The genuine official-source link is external; never an iframe.
                        assert page.locator('#source-year').input_value()=="2024"
                        single_q="21" if subject=="chemistry" else "11"
                        multi_q="53" if subject=="chemistry" else "49"
                        assert page.locator("#subject-questions .source-q-pick").count()==20
                        assert page.locator("#publisher-key-result").is_hidden()
                        page.locator('#source-question-number').fill("20")
                        if subject=="chemistry":
                            assert "DROPPED" in page.locator("#attempt-status").inner_text()
                        else:
                            assert "Choose one of" in page.locator("#attempt-status").inner_text()
                        assert page.locator("#save-first-response").is_disabled()
                        assert page.locator("#publisher-key-link").is_hidden()
                        page.locator('#source-question-number').fill(single_q)
                        assert page.locator('#practice-choices input[type="radio"]').count()==4
                        assert page.locator("#save-first-response").is_enabled()
                        assert page.locator("#publisher-key-result").is_hidden()
                        page.locator('#practice-choices input[value="B"]').check()
                        page.locator("#save-first-response").click()
                        assert page.locator("#attempt-status").get_attribute("data-status")=="SAVED_UNVERIFIED"
                        assert "No actual question was imported" in page.locator("#attempt-status").inner_text()
                        assert page.locator("#publisher-key-link").is_visible()
                        assert page.locator("#publisher-key-result").is_visible()
                        comparison=page.locator("#publisher-key-result").inner_text()
                        assert "Publisher" in comparison or "final key" in comparison
                        assert ("matches" if subject=="chemistry" else "differs") in comparison
                        assert page.locator("#save-first-response").is_disabled()
                        page.reload(wait_until="domcontentloaded")
                        page.locator("#paper-practice-form:visible").wait_for(timeout=15000)
                        page.locator('#source-question-number').fill(single_q)
                        assert page.locator("#attempt-status").get_attribute("data-status")=="SAVED_UNVERIFIED"
                        assert page.locator('#practice-choices input[value="B"]').is_checked()
                        page.locator('#source-question-number').fill(multi_q)
                        assert page.locator('#practice-choices input[type="checkbox"]').count()==4
                        page.locator('#practice-choices input[value="A"]').check()
                        page.locator('#practice-choices input[value="B"]').check()
                        if subject=="chemistry":
                            page.locator('#practice-choices input[value="C"]').check()
                        else:
                            page.locator('#practice-choices input[value="D"]').check()
                        page.locator("#save-first-response").click()
                        assert "matches" in page.locator("#publisher-key-result").inner_text()
                        assert "No actual question was imported" in page.locator("#attempt-status").inner_text()
                        assert page.locator("#save-first-response").is_disabled()
                        page.locator("#source-year").select_option("2023")
                        page.locator("#source-question-number").fill("21")
                        assert page.locator("#save-first-response").is_disabled()
                        assert "code/language" in page.locator("#attempt-status").inner_text().lower()
                        assert page.locator('#publisher-key-link').is_hidden()
                        assert page.locator("#publisher-key-result").is_hidden()
                        assert page.locator("#subject-questions").is_hidden()
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4")
                        # Distinct authored question bank must contain actual
                        # fresh Core1B prompts, not an empty page or source copies.
                        page.goto(base+f"/nsejs/{subject}/index.html",
                                  wait_until="domcontentloaded",timeout=20000)
                        authored_panel=page.locator("#authored-transfer-question-bank")
                        assert authored_panel.count()==1 and "HOLD" in authored_panel.inner_text()
                        authored_panel.get_by_role(
                            "link",name="Open authored transfer practice questions").click()
                        page.wait_for_url("**/nsejs/"+subject+"/authored-practice.html")
                        cards=page.locator(".practice-card")
                        cards.first.wait_for(timeout=15000)
                        assert cards.count()==(2 if subject=="chemistry" else 3)
                        assert page.locator("#authored-status").get_attribute(
                            "data-status")=="AUTHORED_TECHNICAL_ONLY"
                        first=cards.first
                        assert len(first.locator(".practice-prompt").inner_text())>55
                        assert first.locator(".author-worked li").count()==0
                        assert first.get_by_role("button",name="Show author's unreviewed reconstruction").is_disabled()
                        first.locator("textarea").fill(
                            "I will choose an independent physical model, test its assumptions and check the boundary.")
                        first.get_by_role("button",name="Save first independent response").click()
                        assert first.get_by_role("button",name="Show author's unreviewed reconstruction").is_enabled()
                        assert first.locator(".author-worked li").count()==0
                        page.reload(wait_until="domcontentloaded")
                        first=page.locator(".practice-card").first
                        first.locator("textarea:disabled").wait_for(timeout=15000)
                        assert first.locator(".author-worked li").count()==0
                        first.get_by_role("button",name="Show author's unreviewed reconstruction").click()
                        assert first.locator(".author-worked li").count()>=2
                        assert first.locator(".author-worked").is_visible()
                        assert "NOT academically reviewed" in first.locator(".author-worked").inner_text()
                        assert page.locator("iframe").count()==0
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4")
                        checks+=1
                    # No separate student answer corpus or source PDF is staged.
                    assert page.locator("iframe").count()==0
                    assert not errors,errors
                finally:
                    ctx.close()
            # Deny storage: first attempt cannot be declared SAVED.
            ctx=browser.new_context(viewport={"width":1000,"height":1600},
                                   is_mobile=True,has_touch=True)
            ctx.add_init_script(
                "Storage.prototype.setItem=function(){throw Error('blocked')};")
            page=ctx.new_page()
            page.goto(base+"/nsejs/chemistry/question-bank.html",
                      wait_until="domcontentloaded")
            page.locator("#paper-practice-form:visible").wait_for(timeout=15000)
            page.locator("#source-question-number").fill("21")
            page.locator('#practice-choices input[value="A"]').check()
            page.locator("#save-first-response").click()
            assert page.locator("#attempt-status").get_attribute("data-status")=="HOLD"
            assert page.locator("#publisher-key-link").is_hidden()
            assert "STORAGE" in page.locator("#attempt-status").inner_text()
            # Denied storage must also stop authored Core1B reconstruction.
            page.goto(base+"/nsejs/biology/authored-practice.html",wait_until="domcontentloaded")
            card=page.locator(".practice-card").first
            card.wait_for(timeout=15000)
            card.locator("textarea").fill(
                "I am separating the conceptual model from the boundary and independent verification.")
            card.get_by_role("button",name="Save first independent response").click()
            assert card.get_by_role("button",name="Show author's unreviewed reconstruction").is_disabled()
            assert card.locator(".author-worked li").count()==0
            assert "Storage denied" in card.inner_text()
            ctx.close()
            # A content-revision mismatch in the actual authored manifest
            # must not render or reveal any exercises.
            ctx=browser.new_context(viewport={"width":1000,"height":1600},
                                   has_touch=True,is_mobile=True)
            page=ctx.new_page()
            def tamper_authored(route):
                packet=json.loads((stage/"nsejs/data/authored-core1b-transfers.v1.json").read_text("utf-8"))
                packet["items"][0]["prompt"]+=" TAMPER"
                route.fulfill(status=200,content_type="application/json",body=json.dumps(packet))
            page.route("**/nsejs/data/authored-core1b-transfers.v1.json",tamper_authored)
            page.route("https://cdn.jsdelivr.net/**",lambda route:
                route.fulfill(status=200,content_type="application/javascript",body=""))
            page.goto(base+"/nsejs/chemistry/authored-practice.html",wait_until="domcontentloaded")
            page.locator('#authored-status[data-status="HOLD"]').wait_for(timeout=15000)
            assert "REAL_CONTENT_HASH_MISMATCH" in page.locator("#authored-status").inner_text()
            assert page.locator(".practice-card").count()==0
            ctx.close()
            browser.close()
    finally:
        srv.shutdown();srv.server_close()
    print("PASS source-only Chemistry/Biology practice:",checks,
          "touch orientations x subjects; no imported stems or grades; 18 Core1 recovery HOLD")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",required=True,type=Path)
    args=parser.parse_args()
    check(args.site)
