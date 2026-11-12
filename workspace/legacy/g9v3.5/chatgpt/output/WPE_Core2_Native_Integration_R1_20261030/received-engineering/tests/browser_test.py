"""Chromium fixture-only interaction checks; never claims repo governed renderer QA."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from threading import Thread
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root/'outputs')))
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/SYNTHETIC_CORE2_GOLDEN.html'
log=[]
def check(name,cond):
    log.append({'case':name,'pass':bool(cond)})
    if not cond:raise AssertionError(name)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for mode in ('desktop','mobile'):
        ctx=browser.new_context(viewport={'width':1280 if mode=='desktop' else 390,'height':860},is_mobile=(mode=='mobile'),has_touch=(mode=='mobile'))
        page=ctx.new_page();page.set_content((root/"outputs"/"SYNTHETIC_CORE2_GOLDEN.html").read_text(encoding="utf8"))
        check(f'{mode}:before no solution DOM',page.locator('#solution').is_hidden() and page.locator('#answer-panel').is_hidden())
        check(f'{mode}:no answer in visible page', 'C — Zero work' not in page.locator('main').inner_text())
        check(f'{mode}:response type options',page.locator('input[name=answer]').count()==4)
        page.get_by_role('button',name='Commit attempt').click()
        check(f'{mode}:blank attempt rejected','Choose or enter' in page.locator('#result').inner_text())
        for i in range(3):
            page.get_by_role('button',name='Reveal next hint').click()
            check(f'{mode}:hint {i+1}',page.locator('.hint').count()==i+1 and page.locator('#solution').is_hidden())
        check(f'{mode}:hint ladder stops',page.get_by_role('button',name='Reveal next hint').is_disabled())
        page.locator('input[value=B]').check()
        page.get_by_role('button',name='Commit attempt').click()
        check(f'{mode}:wrong answer graded','incorrect' in page.locator('#result').inner_text())
        check(f'{mode}:solution visible after commit',page.locator('#solution').is_visible() and 'C — Zero work' in page.locator('#answer-summary').inner_text())
        check(f'{mode}:cannot reattempt',page.get_by_role('button',name='Commit attempt').is_disabled())
        page.close();page=ctx.new_page();page.set_content((root/'outputs'/'SYNTHETIC_CORE2_GOLDEN.html').read_text(encoding='utf8'));page.locator('input[value=C]').check();page.get_by_role('button',name='Commit attempt').click()
        check(f'{mode}:correct answer graded','correct' in page.locator('#result').inner_text())
        check(f'{mode}:no horizontal overflow',page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'))
        ctx.close()
    browser.close()
logpath=root/'outputs'/'BROWSER_TESTS.json';logpath.write_text(json.dumps({'browser':'Chromium','mode':'synthetic_local_fixture_only','results':log,'passed':sum(x['pass'] for x in log),'total':len(log)},indent=2)+'\n')
server.shutdown()
print(len(log),'browser assertions PASS')
