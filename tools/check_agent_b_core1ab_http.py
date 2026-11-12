"""Exact generated Agent B HTTP Chromium verification, not independent science approval."""
from __future__ import annotations

import http.server
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]


def _check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    from playwright.sync_api import sync_playwright

    with tempfile.TemporaryDirectory(prefix="agent_b_http_") as temp:
        root = Path(temp)
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        for name in ("build_d3_expansion_modules.py", "build_d3_batch2_modules.py"):
            script = root / name
            shutil.copyfile(ROOT / name, script)
            r = subprocess.run([sys.executable, str(script)], cwd=root, env=env, capture_output=True,
                               text=True, timeout=40)
            _check(r.returncode == 0, "Source-safe builder failed: " + name + ": " + r.stderr[-2000:])
        url_path = "/workspace/output/nsejs-fluids-surface-energy-d3-r1/learning_journey.html"
        lens_path = "/workspace/output/nsejs-optics-displacement-d3-r1/learning_journey.html"

        class Quiet(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(root), **kwargs)
            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Quiet)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        cases = 0
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
                try:
                    for size in ((1366, 768), (390, 844)):
                        ctx = browser.new_context(viewport={"width": size[0], "height": size[1]})
                        page = ctx.new_page()
                        js_errors = []
                        page.on("pageerror", lambda e: js_errors.append(str(e)))
                        response = page.goto(f"http://127.0.0.1:{port}"+url_path, wait_until="load", timeout=15000)
                        _check(response is not None and response.status == 200, "HTTP navigation failed")
                        page.locator("#tab-core1b").click()
                        root_selector = "#content-core1b[data-agent-b-core1b]"
                        _check(page.locator(root_selector).count() == 1, "No protected Core1B panel")
                        _check(not page.locator('[data-role="model-host"]').is_visible(), "Model visible before attempt")
                        _check("5.1124" not in page.locator(root_selector).inner_text(), "Work answer leaked before attempt")

                        page.locator('[data-hint="1"]').click()
                        _check(page.locator('[data-hint-text="1"]').inner_text().strip() != "", "Hint did not reveal; status=" + page.locator('[data-role="status"]').inner_text() + "; js=" + repr(js_errors))
                        page.locator('[data-role="prediction-input"]').fill("The large drop contributes eight small-drop volumes.")
                        page.locator('[data-role="save-prediction"]').click()
                        page.reload(wait_until="load")
                        page.locator("#tab-core1b").click()
                        _check(page.locator('[data-role="save-prediction"]').is_disabled(), "Prediction not restored")

                        stale_tab = ctx.new_page()
                        stale_tab.goto(f"http://127.0.0.1:{port}"+url_path, wait_until="load", timeout=15000)
                        stale_tab.locator("#tab-core1b").click()
                        page.locator('[data-role="firstAttempt-input"]').fill(
                            "R^3=8r^3+(2r)^3=16r^3; Ai=4pi(12)r^2 and Af=4pi(16^(2/3))r^2.")
                        page.locator('[data-role="save-firstAttempt"]').click()
                        _check(page.locator('[data-role="model-host"]').is_visible(), "Reconstruction did not unlock")
                        _check(page.locator('[data-role="save-firstAttempt"]').is_disabled(), "Original attempt not frozen")
                        _check(page.locator('[data-role="model-host"]').inner_text().count("5.1124") > 0,
                               "Corrected reconstruction did not render")
                        _check("Another tab" in stale_tab.locator('[data-role="status"]').inner_text(),
                               "Stale tab was not invalidated")

                        page.reload(wait_until="load")
                        page.locator("#tab-core1b").click()
                        _check(page.locator('[data-role="model-host"]').is_visible(), "Reconstruction not restored")
                        _check(page.locator('[data-role="save-firstAttempt"]').is_disabled(), "Attempt could be replaced")
                        page.locator('[data-role="diagnosis-input"]').fill("First mistake: treated unequal radii as equal.")
                        page.locator('[data-role="save-diagnosis"]').click()
                        _check(page.locator('[data-role="repair-stage"]').is_visible(), "Repair not gated by diagnosis")
                        page.locator('[data-role="repair-input"]').fill("Add cubic radii separately and subtract final area.")
                        page.locator('[data-role="save-repair"]').click()
                        _check(page.locator('[data-role="transfer-stage"]').is_visible(), "Changed-condition task not available")
                        page.locator('[data-role="transfer-input"]').fill("For ten equal drops, R^3=10r^3.")
                        page.locator('[data-role="save-transfer"]').click()
                        _check(page.locator('[data-role="boundary-answer"]').is_visible(), "Boundary model remained hidden")
                        page.reload(wait_until="load")
                        page.locator("#tab-core1b").click()
                        _check(page.locator('[data-role="save-transfer"]').is_disabled(), "Transfer attempt not durable")
                        _check(not js_errors, "JavaScript runtime exceptions: "+repr(js_errors))
                        _check(page.locator("iframe").count() == 0, "Iframe unsupported")
                        _check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
                               "Horizontal viewport overflow")
                        cases += 1
                        ctx.close()

                    for size in ((1366, 768), (390, 844)):
                        ctx = browser.new_context(viewport={"width": size[0], "height": size[1]})
                        page = ctx.new_page()
                        js_errors = []
                        page.on("pageerror", lambda e: js_errors.append(str(e)))
                        response = page.goto(f"http://127.0.0.1:{port}"+lens_path, wait_until="load", timeout=15000)
                        _check(response is not None and response.status == 200, "Lens HTTP learner navigation failed")
                        page.locator("#tab-core2").click()
                        _check("Agent A" in page.locator("#content-core2").inner_text(), "Core2 ownership status missing")
                        page.locator("#tab-core1a").click()
                        _check("Core1A physical construction" in page.locator("#content-core1a").inner_text(),
                               "Lens Core1A teaching not rendered")
                        page.locator("#tab-core1b").click()
                        _check(not page.locator('[data-role="model-host"]').is_visible(),
                               "Lens reconstruction shown without first attempt")
                        _check("18 cm" not in page.locator("#content-core1b").inner_text(),
                               "Lens focal answer leaked in attempt or hints")
                        page.locator('[data-hint="3"]').click()
                        _check("18 cm" not in page.locator("#content-core1b").inner_text(),
                               "Lens H3 reveals final focal length")
                        page.locator('[data-role="prediction-input"]').fill(
                            "Conjugate positions measure the root separation, not the focal length.")
                        page.locator('[data-role="save-prediction"]').click()
                        page.locator('[data-role="firstAttempt-input"]').fill(
                            "D=96, d=48 so product=(D^2-d^2)/4=1728 and f=1728/96=18 cm.")
                        page.locator('[data-role="save-firstAttempt"]').click()
                        _check(page.locator('[data-role="model-host"]').is_visible(), "Lens reconstruction not gated correctly")
                        _check(page.locator('[data-role="save-firstAttempt"]').is_disabled(), "Lens attempt not frozen")
                        _check("18 cm" in page.locator('[data-role="model-host"]').inner_text(),
                               "Lens independent reconstruction missing")
                        page.reload(wait_until="load")
                        page.locator("#tab-core1b").click()
                        _check(page.locator('[data-role="model-host"]').is_visible(), "Lens saved attempt not restored")
                        _check(page.locator('[data-role="save-firstAttempt"]').is_disabled(), "Lens attempt can be overwritten")
                        page.locator('[data-role="diagnosis-input"]').fill("Confused measured displacement with focal length.")
                        page.locator('[data-role="save-diagnosis"]').click()
                        page.locator('[data-role="repair-input"]').fill("Use root sum and difference first.")
                        page.locator('[data-role="save-repair"]').click()
                        page.locator('[data-role="transfer-input"]').fill("D=70 is smaller than 4f=72.")
                        page.locator('[data-role="save-transfer"]').click()
                        _check(page.locator('[data-role="boundary-answer"]').is_visible(),
                               "Lens transfer feedback not gated")
                        page.goto(f"http://127.0.0.1:{port}"+url_path, wait_until="load", timeout=15000)
                        page.locator("#tab-core1b").click()
                        _check(not page.locator('[data-role="model-host"]').is_visible(),
                               "A lens attempt incorrectly unlocked droplet reconstruction")
                        page.go_back(wait_until="load")
                        page.locator("#tab-core1b").click()
                        _check(page.locator('[data-role="model-host"]').is_visible(),
                               "Lens attempt not preserved after return navigation")
                        _check(page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
                               "Lens mobile/desktop horizontal overflow")
                        _check(not js_errors, "Lens JS errors "+repr(js_errors))
                        cases += 1
                        ctx.close()

                    denied = browser.new_context(viewport={"width": 390, "height": 844})
                    denied.add_init_script("""(() => {
                        const original = Storage.prototype.setItem;
                        Storage.prototype.setItem = function(k,v) {
                            if(String(k).startsWith('g9v4:agent-b:')) throw new DOMException('Blocked','QuotaExceededError');
                            return original.call(this,k,v);
                        };
                    })()""")
                    page = denied.new_page()
                    page.goto(f"http://127.0.0.1:{port}"+url_path, wait_until="load", timeout=15000)
                    page.locator("#tab-core1b").click()
                    _check("unavailable" in page.locator('[data-role="status"]').inner_text(),
                           "Storage denial not disclosed")
                    _check(page.locator('[data-role="save-firstAttempt"]').is_disabled(), "Denied storage enabled submit")
                    _check(not page.locator('[data-role="model-host"]').is_visible(), "Denied storage leaked answer")
                    cases += 1
                    denied.close()
                finally:
                    browser.close()
        finally:
            server.shutdown()
            server.server_close()
    print(f"PASS: {cases} real HTTP Chromium Agent B learner cases (desktop/mobile/storage denial)")


if __name__ == "__main__":
    main()
