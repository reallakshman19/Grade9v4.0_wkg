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
                expected = 11 if topic == "mechanics" else 10
                page.goto(base+BASE+"question-bank.html?topic="+topic, wait_until="domcontentloaded")
                page.wait_for_function("(n) => document.querySelectorAll('.card').length === n", arg=expected)
                assert page.locator(".card").count() == expected, topic
                assert str(expected)+" candidate records" in page.locator("#status").inner_text(), topic
                assert page.locator("span.status").count() == expected, topic
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
            assert "Producer-proposed answer (not independently verified):" in practice_card.locator(".answer").inner_text()
            assert "Official Key:" not in practice_card.locator(".answer").inner_text()
            page.reload(wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 10")
            restored = page.locator(".card").nth(1)
            assert restored.get_by_role("button",name="Save first attempt").is_disabled()
            assert restored.get_by_role("button",name="Show explanation").is_enabled()
            assert restored.locator(".answer").is_hidden()
            # Distinct identity deep link, not the ambiguous historical displayed ID.
            page.goto(base+BASE+"question-bank.html?topic=optics&uid=g9%3APHYSICS%3ANSEJS-23-OPT-02",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 1")
            assert "NSEJS-23-OPT-02" in page.locator(".card").inner_text()
            # Failed storage must never be reported as successfully saved.
            denied = browser.new_context(viewport={"width": 1280, "height": 800})
            denied.route("https://cdn.jsdelivr.net/**",lambda route:route.fulfill(
                status=200,content_type="application/javascript",body=""))
            denied.add_init_script("Storage.prototype.setItem = function() { throw new Error('denied'); }")
            denied_page = denied.new_page()
            denied_page.goto(base+BASE+"question-bank.html?topic=optics",wait_until="domcontentloaded")
            denied_page.wait_for_function("document.querySelectorAll('.card').length === 10")
            denied_card = denied_page.locator(".card").nth(1)
            denied_card.locator(".options input").first.check()
            denied_card.get_by_role("button",name="Save first attempt").click()
            assert "NOT SAVED" in denied_card.inner_text()
            assert "saved locally" not in denied_card.inner_text()
            denied.close()
            # Original official Q34 is graph-dependent; the source candidate omitted its figure metadata.
            page.goto(base+BASE+"question-bank.html?topic=mechanics",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 11")
            graph_card = page.locator(".card").nth(9)
            assert "NSEJS-24-MECH-07" in graph_card.inner_text()
            assert graph_card.get_by_role("button",name="Save first attempt").is_disabled()
            assert "official examination figure/graph" in graph_card.inner_text()
            # Expose inherited invalid 2024 source IDs instead of showing them as official.
            page.goto(base+BASE+"question-bank.html?topic=optics",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelectorAll('.card').length === 10")
            assert page.locator(".card").nth(8).inner_text().find("SOURCE CLAIM INVALID") >= 0
            assert page.locator(".card").nth(9).inner_text().find("SOURCE CLAIM INVALID") >= 0
            assert "QRT CONFLICT" in page.locator(".card").nth(7).inner_text()
            # Tamper the canonical JSON but leave its ledger untouched; fail closed, no questions shown.
            def mutate_corpus(route):
                original = route.fetch()
                tampered = original.text().replace("An ant is sitting on the principal axis","An ant is tumbling on the principal axis",1)
                route.fulfill(status=200,content_type="application/json",body=tampered)
            page.route("**/nsejs/data/physics-core2-candidates.v1.json", mutate_corpus)
            page.goto(base+BASE+"question-bank.html?topic=optics",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelector('#status').textContent.includes('SOURCE_CONTENT_INTEGRITY_MISMATCH')")
            assert page.locator(".card").count()==0
            page.unroute("**/nsejs/data/physics-core2-candidates.v1.json")
            page.goto(base+BASE+"question-bank.html?topic=fluids",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelector('#questions').textContent.includes('No source-backed')")
            assert page.locator(".card").count() == 0
            page.goto(base+BASE+"question-bank.html?topic=optics&uid=unknown",wait_until="domcontentloaded")
            page.wait_for_function("document.querySelector('#questions').textContent.includes('Requested question UID not found')")
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
            mp.wait_for_function("document.querySelectorAll('.card').length === 11")
            assert mp.locator(".card").count()==11
            assert "Authored practice ID: G9-AUTH-MECH-001" in mp.locator(".card").last.inner_text()
            assert mp.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")
            print("PASS: 5 topic banks, 50 source-claimed + 1 authored record, figure HOLD, commit/reveal/reload, deep link, storage denial, fluids HOLD, unknown UID, navigation, 390x844")
            mobile.close();context.close();browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    execute()
