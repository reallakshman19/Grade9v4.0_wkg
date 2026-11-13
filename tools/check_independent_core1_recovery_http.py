#!/usr/bin/env python3
"""Actual staged HTTP Chromium: 18 independently authored Core1 six-stage repairs.

Preserves historical 18 original-source modules on HOLD. Covers each real route,
two independent first attempts, reload, source revision tamper and storage denial.
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
    catalog=json.loads((stage/"nsejs/data/independent-core1-recovery.v1.json").read_text("utf-8"))
    assert manifest["core1ab_authored_lesson_pages"]==8
    assert manifest["core1ab_unpublished_constructions"]==18
    assert manifest["independent_core1_supplements"]["new_independent_authored_supplements"]==18
    assert manifest["independent_core1_supplements"]["source_originals_recovered"]==0
    assert catalog["original_18_modules_still_on_hold"]==18
    assert catalog["academic_admission"]=="HOLD"
    assert len(catalog["items"])==18
    for row in catalog["items"]:
        assert row["publication_route"] in manifest["files"]
    server=ThreadingHTTPServer(("127.0.0.1",0),
          partial(SimpleHTTPRequestHandler,directory=str(stage)))
    Thread(target=server.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(server.server_port)
    total=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,height,items in ((1000,1600,catalog["items"]),
                                       (1600,1000,catalog["items"][::5])):
                ctx=browser.new_context(viewport={"width":width,"height":height},
                                        has_touch=True,is_mobile=True)
                page=ctx.new_page()
                errors=[]
                page.on("pageerror",lambda error:errors.append(str(error)))
                for lesson in items:
                    response=page.goto(base+"/"+lesson["publication_route"],
                                       wait_until="domcontentloaded",timeout=25000)
                    assert response.status==200
                    root=page.locator("#recovery-lesson")
                    root.locator('[data-status="AUTHORED_TECHNICAL_ONLY"]').wait_for(timeout=15000)
                    assert root.locator(".stage").count()==2
                    assert root.locator("textarea").count()==1
                    assert root.locator("li").count()==0
                    assert root.get_by_role("button",name="3. Reconstruct").is_disabled()
                    assert root.get_by_role("button",name="6. Boundary test").is_disabled()
                    assert page.locator("iframe").count()==0
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+5")
                    root.get_by_role("textbox",name="First independent Core1B reasoning").fill(
                        "I select the governing physical or chemical model, solve the given transfer and verify its boundary.")
                    root.get_by_role("button",name="Save first Core1B response").click()
                    root.locator('[data-status="SAVED"]').wait_for()
                    assert root.locator(".stage").count()==2
                    assert root.get_by_role("button",name="3. Reconstruct").is_enabled()
                    root.get_by_role("button",name="3. Reconstruct").click()
                    assert root.locator(".stage").count()==3
                    assert root.locator("ol li").count()==3
                    root.get_by_role("button",name="4. Diagnose").click()
                    root.get_by_role("button",name="5. Repair").click()
                    root.get_by_role("button",name="6. Boundary test").click()
                    assert root.locator(".stage").count()==6
                    boundary=root.locator(".stage").last
                    assert boundary.get_by_role("button",name="Show authored boundary explanation").is_disabled()
                    boundary.get_by_role("textbox",name="Unseen boundary answer").fill(
                        "I alter the boundary assumption, recompute the relationship, and check physical validity.")
                    boundary.get_by_role("button",name="Save boundary response").click()
                    assert boundary.get_by_role("button",name="Show authored boundary explanation").is_enabled()
                    boundary.get_by_role("button",name="Show authored boundary explanation").click()
                    assert lesson["boundaryAnswer"] in boundary.inner_text()
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+5")
                    total+=1
                assert not errors,errors
                ctx.close()
            # Persisted first response survives refresh and is revision-scoped.
            row=catalog["items"][0]
            ctx=browser.new_context(viewport={"width":1000,"height":1600},
                                    has_touch=True,is_mobile=True)
            page=ctx.new_page()
            page.goto(base+"/"+row["publication_route"],wait_until="domcontentloaded")
            page.locator('[data-status="AUTHORED_TECHNICAL_ONLY"]').wait_for()
            page.get_by_role("textbox",name="First independent Core1B reasoning").fill(
                "Independent first reasoning establishes a model, computes evidence and checks the boundary.")
            page.get_by_role("button",name="Save first Core1B response").click()
            assert page.get_by_role("button",name="3. Reconstruct").is_enabled()
            page.reload(wait_until="domcontentloaded")
            page.locator('[data-status="AUTHORED_TECHNICAL_ONLY"]').wait_for()
            assert page.get_by_role("button",name="3. Reconstruct").is_enabled()
            assert page.locator("#recovery-lesson ol li").count()==0
            ctx.close()
            # Storage denied = no author explanation and no fake first-attempt receipt.
            ctx=browser.new_context(viewport={"width":1000,"height":1600},
                                    has_touch=True,is_mobile=True)
            ctx.add_init_script("Storage.prototype.setItem=function(){throw Error('Denied')};")
            page=ctx.new_page()
            page.goto(base+"/"+row["publication_route"],wait_until="domcontentloaded")
            page.locator('[data-status="AUTHORED_TECHNICAL_ONLY"]').wait_for()
            page.get_by_role("textbox",name="First independent Core1B reasoning").fill(
                "Use a correct model, independent solution and the relevant physical boundary.")
            page.get_by_role("button",name="Save first Core1B response").click()
            assert page.locator('[data-status="SAVE_FAILED"]').count()==1
            assert page.get_by_role("button",name="3. Reconstruct").is_disabled()
            assert page.locator("#recovery-lesson ol li").count()==0
            ctx.close()
            # Tamper the real lesson data; a changed field with old SHA must
            # result in HOLD before any stage or solution is constructed.
            ctx=browser.new_context(viewport={"width":1000,"height":1600},
                                    has_touch=True,is_mobile=True)
            page=ctx.new_page()
            def tamper(route):
                clone=json.loads((stage/"nsejs/data/independent-core1-recovery.v1.json").read_text("utf-8"))
                clone["items"][0]["worked"]+=" malicious unreviewed change"
                route.fulfill(status=200,content_type="application/json",
                              body=json.dumps(clone))
            page.route("**/nsejs/data/independent-core1-recovery.v1.json",tamper)
            page.goto(base+"/"+row["publication_route"],wait_until="domcontentloaded")
            page.locator('[data-status="HOLD"]').wait_for(timeout=15000)
            assert "AUTHORED_FULL_ITEM_HASH_MISMATCH" in page.locator("#recovery-status").inner_text()
            assert page.locator(".stage").count()==0
            ctx.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print("PASS staged independent source-neutral Core1 repair:",total,
          "real HTTP Chromium learner journeys, storage/revision guards, 18 originals HOLD")


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--site",required=True,type=Path)
    args=parser.parse_args()
    check(args.site)
