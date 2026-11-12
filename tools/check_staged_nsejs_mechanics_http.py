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
