"""Independent Chromium checks for WPE Foundations/C/E/F sub-tabs.
The UI check does not grade student understanding or repair unrelated source routing.
"""
from __future__ import annotations

from functools import partial
import http.server
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

def check(ok,why):
    if not ok:
        raise AssertionError(why)

def run(browser,base,width,height):
    page=browser.new_page(viewport={"width":width,"height":height})
    page.goto(base+"/physics/wpe/learn-challenge.html")
    tabs=page.locator(".skill-tabs [role=tab]")
    panels=page.locator(".skill-tabpanel")
    check(tabs.count()==4,"Expected exactly four sub-tabs")
    check(panels.count()==4,"Expected exactly four panels")
    check(page.locator("#skill-tab-foundations").get_attribute("aria-selected")=="true","Foundations should be active initially")
    check(page.locator(".skill-tabpanel:visible").count()==1,"Only one panel should appear")
    check(page.locator("#skill-panel-foundations .skill-entry").count()==5,"Missing foundation link")

    page.locator("#skill-tab-c").click()
    check(page.locator("#skill-panel-c .skill-entry:visible").count()==8,"C tab missing a lesson")
    check(not page.locator("#skill-panel-e").is_visible(),"E panel remained visible")

    page.locator("#skill-tab-c").focus()
    page.keyboard.press("ArrowRight")
    check(page.locator("#skill-tab-e").get_attribute("aria-selected")=="true","Right arrow did not activate E")
    check(page.locator("#skill-tab-e").evaluate("(el)=>el===document.activeElement"),"Focus did not follow keyboard tab selection")
    check(page.locator("#skill-panel-e .skill-entry:visible").count()==5,"E tab missing a lesson")

    page.keyboard.press("End")
    check(page.locator("#skill-tab-f").get_attribute("aria-selected")=="true","End did not activate F")
    check(page.locator("#skill-panel-f .skill-entry:visible").count()==8,"F tab missing F04–F08")
    check(page.locator("#skill-panel-f .skill-finding-label").filter(has_text="Integration finding:").count()==5,"Five integration findings not visible")
    for i in range(4,9):
        id_=f"F{i:02}"
        link=page.locator(f'#skill-panel-f a[href="gap-journeys.html#{id_}"]')
        check(link.count()==1,f"Missing {id_} deep link")
        with page.expect_navigation():
            link.click()
        check(page.locator("#current-title").inner_text().startswith(id_+" ·"),f"{id_} linked to the wrong journey")
        page.go_back()
        page.locator("#skill-tab-f").click()
        check(page.locator("#skill-panel-f").is_visible(),"F panel did not recover after browser back")

    page.locator("#skill-tab-f").focus()
    page.keyboard.press("Home")
    check(page.locator("#skill-tab-foundations").get_attribute("aria-selected")=="true","Home did not activate Foundations")
    page.keyboard.press("ArrowLeft")
    check(page.locator("#skill-tab-f").get_attribute("aria-selected")=="true","Left arrow did not wrap to F")

    page.goto(base+"/physics/wpe/learn-challenge.html#skill-panel-f")
    check(page.locator("#skill-tab-f").get_attribute("aria-selected")=="true","F deep link did not select F tab")
    check(page.locator(".skill-tabpanel:visible").count()==1,"Deep link did not hide other panels")
    check(page.locator("iframe").count()==0,"Skill selector unexpectedly embedded an iframe")
    print(f"PASS skill tabs, keys, findings and five direct gap journeys at {width}x{height}")
    page.close()

def main():
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for width,height in ((1280,800),(390,844)):
                    run(browser,base,width,height)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__=="__main__":
    main()
