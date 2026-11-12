#!/usr/bin/env python3
"""HTTP Chromium smoke/negative test for Agent A NSEJS Core2 only (not academic review)."""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "/nsejs/physics/"


def execute():
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = "http://127.0.0.1:" + str(server.server_port)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1366, "height": 900})
            # Browser functionality must work when external math-render CDN is unavailable.
            # Actual mathematical typography needs a separate network-enabled visual check.
            context.route("https://cdn.jsdelivr.net/**", lambda route: route.fulfill(
                status=200, content_type="application/javascript", body=""))
            page = context.new_page()
            page_errors = []
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            for topic in ("optics","electrostatics","circuits","magnetism","mechanics"):
                page.goto(base+BASE+"question-bank.html?topic="+topic, wait_until="domcontentloaded")
                page.wait_for_function("document.querySelectorAll('.card').length === 10")
                assert page.locator(".card").count() == 10, topic
                assert "10 candidate records" in page.locator("#status").inner_text(), topic
                assert page.locator("span.status").count() == 10, topic
            page.goto(base+BASE+"question-bank.html?topic=optics",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 10")
            figure_card = page.locator(".card").first
            assert "source-fidelity HOLD" in figure_card.inner_text()
            assert figure_card.get_by_role("button",name="Save first attempt").is_disabled()
            practice_card = page.locator(".card").nth(1)
            assert practice_card.locator(".answer").is_hidden()
            practice_card.locator(".options input").first.check()
            practice_card.get_by_role("button",name="Save first attempt").click()
            assert "saved locally" in practice_card.inner_text()
            assert practice_card.locator(".answer").is_hidden()
            practice_card.get_by_role("button",name="Show explanation").click()
            assert practice_card.locator(".answer").is_visible()
            page.reload(wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 10")
            restored = page.locator(".card").nth(1)
            assert restored.get_by_role("button",name="Save first attempt").is_disabled()
            assert restored.get_by_role("button",name="Show explanation").is_enabled()
            assert restored.locator(".answer").is_hidden()
            page.goto(base+BASE+"question-bank.html?topic=fluids",wait_until="domcontentloaded")
            page.wait_for_function("'No source-backed' in document.querySelector('#questions').textContent")
            assert page.locator(".card").count() == 0
            page.goto(base+BASE+"question-bank.html?topic=optics&uid=unknown",wait_until="domcontentloaded")
            page.wait_for_function("'Requested question UID not found' in document.querySelector('#questions').textContent")
            page.goto(base+BASE+"index.html",wait_until="domcontentloaded")
            page.get_by_role("button",name="Open 10 candidate records").first.click()
            page.wait_for_url("**/question-bank.html?topic=optics")
            page.wait_for_function("document.querySelectorAll('.card').length === 10")
            assert not page_errors, page_errors
            mobile = browser.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True)
            mobile.route("https://cdn.jsdelivr.net/**", lambda route:route.fulfill(
                status=200,content_type="application/javascript",body=""))
            mp = mobile.new_page()
            mp.goto(base+BASE+"question-bank.html?topic=mechanics",wait_until="domcontentloaded")
            mp.wait_for_function("document.querySelectorAll('.card').length === 10")
            assert mp.locator(".card").count()==10
            assert mp.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")
            print("PASS: 5 topic banks, 50 candidate records, figure HOLD, commit/reveal/reload, fluids HOLD, unknown UID, navigation, 390x844")
            mobile.close();context.close();browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    execute()
