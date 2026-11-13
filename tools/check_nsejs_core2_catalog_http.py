#!/usr/bin/env python3
"""Real Chromium source-safe PCB Core2 catalog and subject notebook routes."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright


def check(site:Path)->None:
    root=site.resolve()
    manifest=json.loads((root/"PUBLIC_PREVIEW_MANIFEST.json").read_text("utf-8"))
    catalog=json.loads((root/"nsejs/core2/inventory.v1.json").read_text("utf-8"))
    assert manifest["core2_archive_metadata_only"]["module_count"]==45
    assert manifest["core2_archive_metadata_only"]["candidate_question_count"]==267
    assert manifest["core2_archive_metadata_only"]["original_exam_question_bodies_published"]==0
    assert catalog["academic_admission"]==catalog["redistribution_rights"]=="HOLD"
    assert catalog["public_student_modules_from_uploaded_zip"]==0
    assert catalog["source_custody_records_imported"]==0
    assert catalog["module_count"]==45
    assert len(catalog["items"])==45
    assert not any(row["subject"]=="MATHEMATICS" or "math" in row["slug"]
                   for row in catalog["items"])
    for name in ("nsejs/core2/index.html","nsejs/core2/inventory.v1.json",
                 "nsejs/core2/question-map.html","nsejs/core2/question-map.v1.json"):
        assert name in manifest["files"]
    canonical=json.loads((root/"nsejs/core2/question-map.v1.json").read_text("utf-8"))
    assert canonical["module_count"]==45
    assert canonical["candidate_question_count"]==267
    assert canonical["summary"]["missing_construction"]==241
    assert canonical["summary"]["topic_only_related"]==26
    assert canonical["source_originals_published"]==0
    server=ThreadingHTTPServer(("127.0.0.1",0),
          partial(SimpleHTTPRequestHandler,directory=str(root)))
    Thread(target=server.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(server.server_port)
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,height in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(
                    viewport={"width":width,"height":height},has_touch=True,is_mobile=True)
                # Check every existing related-only candidate route really resolves.
                # This does not classify any as sufficient teaching or source-original.
                routes={q["candidate_learning_route"] for q in canonical["questions"]
                        if q["candidate_learning_route"] is not None}
                assert len(routes)==26
                for relative in sorted(routes):
                    assert relative.startswith("nsejs/") and ".." not in relative
                    linked=ctx.request.get(base+"/"+relative,timeout=10000)
                    assert linked.status==200,relative
                page=ctx.new_page()
                errors=[]
                page.on("pageerror",lambda error:errors.append(str(error)))
                res=page.goto(base+"/nsejs/core2/index.html",
                              wait_until="domcontentloaded",timeout=30000)
                assert res and res.status==200
                assert page.get_by_role("heading",name="Core2 · candidate coverage and source-safe practice").count()==1
                assert page.locator("tbody tr").count()==45
                assert page.get_by_text("No Mathematics records included").count()==1
                assert page.locator("iframe").count()==0
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+5")
                # Open the new question-level source-neutral map with a real tap,
                # not a force-click, iframe or JavaScript-only navigation.
                page.get_by_role("link",name="Browse all 267 question occurrence IDs, provisional reasoning operations and missing learning constructions").click()
                page.wait_for_url("**/nsejs/core2/question-map.html")
                assert page.locator("details").count()==45
                assert page.locator("tbody tr").count()==267
                assert page.locator("a").filter(has_text="Related practice, NOT sufficient teaching").count()==26
                assert page.get_by_text("Mathematics excluded",exact=False).count()==1
                assert page.locator("iframe").count()==0
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+5")
                page.locator("details summary").first.click()
                assert page.locator("details[open]").count()==1
                page.goto(base+"/nsejs/core2/index.html",wait_until="domcontentloaded")
                for subject in ("physics","chemistry","biology"):
                    response=page.goto(base+f"/nsejs/{subject}/index.html",
                                       wait_until="domcontentloaded",timeout=25000)
                    assert response and response.status==200

                    # Regression for older topic cards that looked unchanged.
                    # The source-neutral ZIP census must be *visible in each
                    # subject page*, not hidden on a separate unrelated URL.
                    visible_counts={
                        "physics": (6,21,95),
                        "chemistry": (6,13,87),
                        "biology": (5,11,85),
                    }
                    card_count, module_count, q_count=visible_counts[subject]
                    cards=page.locator('[data-core2-zip-topic]')
                    assert cards.count()==card_count
                    overview=page.locator('#pcb-core2-zip-now-visible')
                    assert overview.count()==1
                    assert f"{module_count} {subject.title()} modules" in overview.inner_text()
                    assert f"{q_count} question IDs" in overview.inner_text()
                    assert "Source/rights/academic HOLD" in overview.inner_text()
                    assert page.locator("iframe").count()==0
                    # Genuine tablet tap on an actual card and its question-ID link;
                    # never force-click or open the URL programmatically.
                    topical=cards.first
                    expanding=topical.locator('details')
                    assert expanding.count()==1
                    expanding.locator('summary').click(timeout=10000)
                    a=expanding.locator('a').first
                    href=a.get_attribute("href")
                    assert href.startswith("../core2/question-map.html#module-")
                    a.click(timeout=10000)
                    page.wait_for_url("**/nsejs/core2/question-map.html#module-*")
                    target=href.split("#",1)[1]
                    assert page.locator(f'details[id="{target}"]').count()==1
                    # Return to subject landing to verify its existing core2
                    # buttons and full-register link were not replaced.
                    page.goto(base+f"/nsejs/{subject}/index.html",
                              wait_until="domcontentloaded",timeout=25000)
                    if subject=="physics":
                        assert page.locator('button[onclick^="openTopicQBank("]').count()==6
                        assert page.get_by_text("Open 10 candidate records",exact=False).count()==4

                    link=page.locator("#core2-archive-register a")
                    assert link.count()==1
                    assert link.get_attribute("href")==f"../core2/index.html#{subject}"
                    assert link.evaluate("el=>el.getBoundingClientRect().height")>=56
                    # Real interaction, no forced clicks or JS navigation.
                    # Catalog link is now near the top of the subject main.
                    assert link.bounding_box()["y"] < height
                    link.click(timeout=10000)
                    page.wait_for_url("**/nsejs/core2/index.html#"+subject)
                    assert page.locator("section#"+subject+" table tbody tr").count()==(
                        {"physics":21,"chemistry":13,"biology":11}[subject])
                    assert page.locator("section#"+subject+" a").count()==1
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+5")
                assert not errors,errors
                ctx.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print("PASS: Core2 PCB metadata-only catalog 45/267, zero original question bodies, two tablet orientations, Math excluded")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--site",type=Path,required=True)
    args=ap.parse_args()
    check(args.site)
