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
    for name in ("nsejs/core2/index.html","nsejs/core2/inventory.v1.json"):
        assert name in manifest["files"]
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
                for subject in ("physics","chemistry","biology"):
                    response=page.goto(base+f"/nsejs/{subject}/index.html",
                                       wait_until="domcontentloaded",timeout=25000)
                    assert response and response.status==200
                    link=page.locator("#core2-archive-register a")
                    assert link.count()==1
                    assert link.get_attribute("href")==f"../core2/index.html#{subject}"
                    assert link.evaluate("el=>el.getBoundingClientRect().height")>=56
                    link.click()
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
