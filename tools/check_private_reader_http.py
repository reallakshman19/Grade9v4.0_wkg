"""Real HTTP Chromium acceptance for PUBLIC-SAFE SYNTHETIC reader fixtures.

This is a CI harness for builder integration; it is not evidence of the
unpublished private 50-record candidate, official examination authenticity,
or scientific correctness. No DOM/set_content fallback is allowed here.
"""
from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

from private_reader_integration import build


def run(chromium: str | None = None) -> dict:
    from test_private_reader_integration import fixture
    with tempfile.TemporaryDirectory(prefix='grade9-synthetic-reader-') as temp:
        root, pins, out = fixture(Path(temp))
        build(root, out, pins)

        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kw):
                super().__init__(*args, directory=str(out), **kw)
            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        port = server.server_address[1]
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = f'http://127.0.0.1:{port}'
        receipt = {'review_scope': 'SYNTHETIC_HTTP_INTEGRATION_ONLY',
                   'source_authenticity': 'NOT_APPLICABLE',
                   'candidate_50_reader_tested': False,
                   'academic_approval': 'HOLD',
                   'journeys': []}
        try:
            with sync_playwright() as p:
                opts = {'headless': True, 'args': ['--no-sandbox', '--disable-dev-shm-usage']}
                if chromium:
                    opts['executable_path'] = chromium
                browser = p.chromium.launch(**opts)
                try:
                    for viewport in ({'width': 1440, 'height': 900}, {'width': 390, 'height': 844}):
                        context = browser.new_context(viewport=viewport)
                        try:
                            page = context.new_page()
                            errs = []
                            page.on('pageerror', lambda e, o=errs: o.append(str(e)))
                            for path, expected in [('preview/question-status.html', 4),
                                                   ('modules/alpha/question-status.html', 2),
                                                   ('modules/beta/question-status.html', 2)]:
                                response = page.goto(f'{base}/{path}', wait_until='load', timeout=15000)
                                assert response and response.status == 200, f'{path}: HTTP 200 missing'
                                assert page.locator('#navlist .item').count() == expected, path
                                assert 'source-unverified candidate reader' in page.locator('header h1').inner_text().lower()
                                assert not errs, (path, errs)
                                if 'alpha' in path or path.startswith('preview/'):
                                    assert page.locator('#question-root svg circle').count() == 1, 'Actual SVG lost in generated HTML'
                                if 'beta' in path:
                                    assert page.locator('[data-figure-hold=true]').count() == 1
                                    assert page.locator('#commit-btn').count() == 0, 'Missing-media question must be withheld'
                                receipt['journeys'].append({'path': path,
                                                            'viewport': viewport['width'],
                                                            'http_status': response.status,
                                                            'js_errors': len(errs),
                                                            'result': 'PASS'})
                            # Combined view contains duplicate historical source IDs; scoped
                            # identities must not share the same on-page first-attempt state.
                            response = page.goto(f'{base}/preview/question-status.html', timeout=15000)
                            assert response and response.status == 200
                            ids = page.locator('#navlist .item')
                            assert ids.count() == 4
                            ids.nth(1).click()  # Alpha, no diagram
                            assert page.locator('#commit-btn').is_enabled()
                            page.locator('#commit-btn').click()
                            assert page.locator('#commit-btn').is_disabled()
                            ids.nth(3).click()  # Beta, same displayed question ID
                            assert page.locator('#commit-btn').is_enabled(), 'Cross-topic attempt leaked'
                            response = page.goto(f'{base}/index.html', timeout=15000)
                            assert response and response.status == 200
                            assert page.locator('a[href="preview/question-status.html"]').count() == 1
                            receipt['journeys'].append({'path':'cross-topic-identity-and-hub',
                                                        'viewport': viewport['width'],
                                                        'result':'PASS'})
                        finally:
                            context.close()
                finally:
                    browser.close()
        finally:
            server.shutdown();server.server_close();worker.join(timeout=5)
        receipt['http_chromium'] = 'PASS'
        return receipt


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--chromium', help='Explicit local executable; omitted uses Playwright-managed Chromium')
    ap.add_argument('--receipt', type=Path)
    args = ap.parse_args()
    receipt = run(args.chromium)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(f"PASS: {len(receipt['journeys'])} direct HTTP Chromium synthetic integration journeys")


if __name__ == '__main__':
    main()
