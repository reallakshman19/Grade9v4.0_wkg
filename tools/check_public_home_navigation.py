"""Actual Chromium navigation audit of the exact PUBLIC GitHub Pages build.

Covers restored student homepage, separated school/NSEJS subjects, legacy WPE
public example, and kept synthetic-only reader. Does not promote academic work.
"""
from __future__ import annotations
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import http.server
import sys

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_public_reader_preview import build_preview

VIEWPORTS=((1280,800),(390,844))
def ok(condition,description):
    if not condition:
        raise AssertionError(description)

def serve(folder):
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(folder)))
    Thread(target=server.serve_forever,daemon=True).start()
    return server,"http://127.0.0.1:"+str(server.server_port)

def check(browser,base,width,height):
    ctx=browser.new_context(viewport={"width":width,"height":height})
    try:
        page=ctx.new_page()
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))

        def go(path,expected_heading):
            response=page.goto(base+"/"+path,wait_until="load")
            ok(response is not None and response.status==200,"HTTP not 200 at "+path)
            ok(expected_heading.lower() in page.locator("h1").inner_text().lower(),
               "Wrong page heading at "+path+": "+page.locator("h1").inner_text())
            ok(page.evaluate("document.documentElement.scrollWidth<=innerWidth+4"),
               "horizontal overflow at "+path+" in "+str(width))
        go("index.html","Choose your subject or NSEJS track")
        tabs=page.locator(".tabs")
        ok(tabs.locator("a").count()==5,"Five site tabs not present")
        ok(tabs.get_by_role("link",name="NSEJS").count()==1,"Dedicated NSEJS tab missing")
        ok(tabs.get_by_role("link",name="Physics").count()==1,
           "Existing School Physics tab missing")
        tabs.get_by_role("link",name="NSEJS").click()
        ok(page.url.endswith("/nsejs/index.html"),"NSEJS top-level tab routed incorrectly")
        ok("Junior Science" in page.locator("h1").inner_text(),"Not NSEJS subject directory")
        ok(page.locator(".cards .card").count()==3,"NSEJS requires three science subjects")
        for subject in ("Physics","Chemistry","Biology"):
            ok(page.locator(".cards .card h2",has_text=subject).count()==1,
               "NSEJS subject entry absent: "+subject)
        for subject,heading in (
            ("physics","Physics Foundation"),("chemistry","Chemistry"),
            ("biology","Biology")
        ):
            go("nsejs/"+subject+"/index.html",heading)
            ok("NSEJS" in page.locator("nav.tabs").inner_text(),"NSEJS tab lost in child")
            if subject!="physics":
                ok("NOT" in page.locator(".status").inner_text().upper() or "no admitted" in page.locator(".status").inner_text().lower(),
                   subject+" unexpectedly suggests qualified content")
        go("physics/index.html","Physics chapters")
        go("mathematics/index.html","Mathematics")
        go("chemistry/index.html","Chemistry")
        go("architecture/index.html","Architecture")
        go("physics/wpe/index.html","Work, Power & Energy")
        # Original pedagogical demonstration (not the protected exam bank).
        go("preview/physics-wpe.html","Learn Work, Power & Energy")
        ok(page.locator("nav.public-safe-nav a").filter(has_text="NSEJS").count()==1,
           "NSEJS global link absent on preview")
        go("preview/practice.html","Try a question")
        ok(page.locator("nav.public-safe-nav").count()==1,
           "Preview has duplicated navigations")
        go("preview/question-status.html","")  # synthetic JS reader
        ok("Synthetic" in page.content(),"Synthetic technical example replaced with real source")
        ok(not errors,"Browser JavaScript exceptions: "+str(errors))
        print("PASS public home, 5 school/NSEJS tabs, three NSEJS sciences, WPE/practice/synthetic reader",
              str(width)+"x"+str(height))
    finally:ctx.close()

def main():
    with TemporaryDirectory(prefix="g9-public-home-check-") as tmp:
        dest=Path(tmp)/"site"
        build_preview(dest)
        server,base=serve(dest)
        try:
            with sync_playwright() as playwright:
                browser=playwright.chromium.launch(headless=True)
                try:
                    for width,height in VIEWPORTS:
                        check(browser,base,width,height)
                finally:browser.close()
        finally:server.shutdown();server.server_close()
if __name__=="__main__":main()
