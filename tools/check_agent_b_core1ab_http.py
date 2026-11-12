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
        script = root / "build_d3_expansion_modules.py"
        shutil.copyfile(ROOT / script.name, script)
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
        r = subprocess.run([sys.executable, str(script)], cwd=root, env=env, capture_output=True,
                           text=True, timeout=40)
        _check(r.returncode == 0, "Original source-safe builder failed: " + r.stderr[-2000:])
        url_path = "/workspace/output/nsejs-fluids-surface-energy-d3-r1/learning_journey.html"

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
                        _check(page.locator('[data-hint-text="1"]').inner_text().strip() != "", "Hint did not reveal")
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
