#!/usr/bin/env python3
"""Verify the staged-only authored Mechanics WPE preview over actual local HTTP.

This does not verify a LIVE GitHub Pages deployment. It never claims an
original examination source or academic acceptance.
"""
from __future__ import annotations

import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


def check(site:Path)->None:
    site=site.resolve()
    manifest=json.loads((site/"PUBLIC_PREVIEW_MANIFEST.json").read_text("utf-8"))
    entry=manifest.get("additional_authored_mechanics_wpe_parity_preview",{})
    assert entry.get("status")=="AUTHORED_TECHNICAL_PREVIEW_ONLY"
    assert entry.get("academic_approval")=="HOLD"
    assert entry.get("source_authenticity")=="AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
    assert entry.get("published") is True
    for path in (
        "nsejs/physics/learn-mechanics.html",
        "nsejs/js/wpe-contract-adapter.js",
        "nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
        "nsejs/data/source-learning-bridge-tech-preview.v1.json",
        "nsejs/css/wpe-touch-parity.css",
    ):
        assert path in manifest["files"] and (site/path).is_file(),path
    server=ThreadingHTTPServer(("127.0.0.1",0),
        partial(SimpleHTTPRequestHandler,directory=str(site)))
    Thread(target=server.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(server.server_port)
    checked=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,height in [(1600,1000),(1000,1600)]:
                ctx=browser.new_context(viewport={"width":width,"height":height},
                                       has_touch=True,is_mobile=True)
                page=ctx.new_page()
                errors=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                page.route("https://cdn.jsdelivr.net/**",
                           lambda route:route.fulfill(status=200,
                               content_type="application/javascript",body=""))
                try:
                    response=page.goto(base+"/nsejs/physics/index.html",
                                       wait_until="domcontentloaded",timeout=20000)
                    assert response.status==200
                    section=page.locator("#nsejs-wpe-mechanics-parity")
                    assert section.count()==1
                    assert "HOLD" in section.inner_text()
                    link=section.get_by_role("link",name="Open authored Mechanics six-stage learner")
                    assert link.evaluate("(n)=>n.getBoundingClientRect().height")>=56
                    link.click()
                    page.wait_for_url("**/nsejs/physics/learn-mechanics.html?**")
                    page.locator("#nsejs-parity-status[data-state='PREVIEW']").wait_for(timeout=15000)
                    assert page.locator("#nsejs-exact-source").inner_text().find(
                           entry["source_revision_sha256"][:12])>=0
                    assert page.locator('.guide input[type="range"]').count()==1
                    assert page.locator(".stage-root [data-action='prediction']").count()==1
                    assert page.locator("iframe").count()==0
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4")
                    # A student must be able to enter through the REAL authored
                    # Core2 question, not only a disconnected preview tile.
                    bank=page.goto(base+"/nsejs/physics/question-bank.html?topic=mechanics",
                                   wait_until="domcontentloaded",timeout=20000)
                    assert bank.status==200
                    page.wait_for_function("document.querySelectorAll('article.card').length===11")
                    source=page.locator("#question-G9-AUTH-MECH-001")
                    route=source.locator("#nsejs-authored-learning-route a")
                    route.wait_for(timeout=15000)
                    assert page.locator("#nsejs-authored-learning-route").count()==1
                    assert "source_revision="+entry["source_revision_sha256"] in route.get_attribute("href")
                    route.click()
                    page.locator("#nsejs-parity-status[data-state='PREVIEW']").wait_for(timeout=15000)
                    assert page.locator("#nsejs-source-return").is_hidden()
                    if width==1000:
                        # Actual two-task completion is checked in the staged
                        # asset set, including no answer revelation before
                        # the first response for EACH independent problem.
                        lesson=json.loads((site/"nsejs/data/mechanics-wpe-teaching-pilot.v1.json").read_text("utf-8"))
                        def complete(task):
                            page.locator('.stage-root [data-field="prediction"]').fill(
                                "First choose the collision model and then the separate friction work.")
                            page.locator('.stage-root [data-action="prediction"]').click()
                            page.locator('.stage-root [data-action="attempt"]').wait_for()
                            for field in task["fields"]:
                                element=page.locator('.stage-root [data-field="'+field["id"]+'"]')
                                if field["type"]=="select":element.select_option(label=field["expected"])
                                elif field["type"]=="number":element.fill(str(field["expected"]))
                                else:element.fill("The model depends on external impulse and energy conditions.")
                            assert page.locator('.stage-root .worked').count()==0
                            page.locator('.stage-root [data-action="attempt"]').click()
                            page.locator('.stage-root [data-action="reconstruct"]').click()
                            page.locator('.stage-root [data-diagnosis]').select_option("explanation")
                            page.locator('.stage-root [data-field="why"]').fill(
                                "I must separate the momentum interval from the later friction interval.")
                            page.locator('.stage-root [data-action="diagnose"]').click()
                            page.locator('.stage-root [data-field="repair"]').fill(
                                "I corrected my assumptions and the separate work/energy calculation.")
                            page.locator('.stage-root [data-action="repair"]').click()
                            for field in task["boundaryFields"]:
                                element=page.locator('.stage-root [data-field="'+field["id"]+'"]')
                                if field["type"]=="select":element.select_option(label=field["expected"])
                                elif field["type"]=="number":element.fill(str(field["expected"]))
                                else:element.fill("Changing a physical assumption changes the equations.")
                            page.locator('.stage-root [data-action="boundary"]').click()
                        complete(lesson["tasks"]["A"])
                        assert page.locator("#nsejs-source-return").is_hidden()
                        page.locator('button[data-variant="T2"]').click()
                        assert page.locator('.stage-root [data-action="prediction"]').count()==1
                        complete(lesson["tasks"]["B"])
                        page.locator("#nsejs-source-return:visible").wait_for(timeout=15000)
                        page.locator("#nsejs-source-return").click()
                    else:
                        # Landscape verifies the returned exact source when
                        # no academic admission or attempt is inferred.
                        page.goto(base+"/nsejs/physics/question-bank.html?topic=mechanics"+
                             "&source_uid="+entry["source_uid"]+
                             "&source_revision="+entry["source_revision_sha256"]+
                             "#question-G9-AUTH-MECH-001",
                             wait_until="domcontentloaded",timeout=20000)
                    page.locator("#learning-return-status[data-state='PREVIEW']").wait_for(timeout=15000)
                    target=page.locator("#question-G9-AUTH-MECH-001")
                    assert "nsejs-exact-source-return" in target.get_attribute("class")
                    assert page.evaluate("document.activeElement.id")=="question-G9-AUTH-MECH-001"
                    assert target.locator(".answer:visible").count()==0
                    assert page.locator("iframe").count()==0
                    assert not errors,errors
                    checked+=1
                finally:
                    ctx.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print("PASS staged authored Mechanics WPE pilot:",checked,
          "touch orientations; SHA-bound source; Academic HOLD; not live Pages")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",type=Path,required=True)
    args=parser.parse_args()
    check(args.site)
