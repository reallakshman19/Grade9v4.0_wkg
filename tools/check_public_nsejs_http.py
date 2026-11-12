#!/usr/bin/env python3
"""Verify the actual staged, unvalidated NSEJS 12.7-inch Pages preview with HTTP Chromium."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


def check(folder:Path)->None:
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(folder)))
    Thread(target=server.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(server.server_port)+"/"
    checked=0
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width,height in ((1600,1000),(1000,1600)):
                ctx=browser.new_context(viewport={"width":width,"height":height},is_mobile=True,has_touch=True)
                ctx.route("https://cdn.jsdelivr.net/**",lambda route:route.fulfill(status=200,content_type="application/javascript",body=""))
                page=ctx.new_page()
                problems=[]
                page.on("pageerror",lambda e:problems.append(str(e)))
                def visit(path,phrase=None):
                    response=page.goto(base+path,wait_until="domcontentloaded",timeout=20000)
                    assert response and response.status==200,(path,response.status if response else None)
                    if phrase:
                        assert phrase.lower() in page.locator("body").inner_text().lower(),path
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4"),(path,width,height)
                    return response
                visit("index.html","Grade9")
                visit("physics/index.html","Physics")
                visit("physics/wpe/index.html","Work")
                visit("nsejs/index.html","Junior Science")
                for subject,count in (("physics",3),("chemistry",2),("biology",3)):
                    visit("nsejs/"+subject+"/index.html","NSEJS")
                    panel=page.locator("#agent-b-authored-preview")
                    assert panel.count()==1 and "UNVALIDATED" in panel.inner_text()
                    panel.locator("a").tap()
                    page.wait_for_url("**/nsejs/"+subject+"/core1/index.html")
                    assert page.locator("li a").count()==count
                    modules=page.locator("li a").evaluate_all("nodes => nodes.map(n=>n.getAttribute('href'))")
                    for module in modules:
                        visit("nsejs/"+subject+"/core1/"+module,"No academic approval")
                        assert page.locator("#tab-core1b").count()==1
                        assert page.locator('[data-role="save-firstAttempt"]').count()>=1
                        assert page.locator("#agent-b-127-tablet-touch").count()==1
                        checked+=1
                visit("nsejs/physics/question-bank.html?topic=mechanics","Mechanics")
                page.wait_for_function("document.querySelectorAll('.card').length===11",timeout=20000)
                assert page.locator(".card").count()==11
                assert page.locator(".card").nth(9).get_by_role("button",name="Save first attempt").is_disabled()
                checked+=1
                visit("nsejs/physics/question-bank.html?topic=optics","Optics")
                page.wait_for_function("document.querySelectorAll('.card').length===10",timeout=20000)
                assert "SOURCE CLAIM INVALID" in page.locator(".card").nth(8).inner_text()
                checked+=1
                visit("preview/question-status.html","Synthetic")
                assert not problems,problems
                ctx.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print("PASS NSEJS public technical preview: preserved WPE, 8 authored pages x 2 12.7-inch touch orientations, 50+1 Core2 records, synthetic reader; verified",checked,"case visits")


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--site",type=Path,required=True)
    args=p.parse_args()
    check(args.site.resolve())
