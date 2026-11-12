"""Real HTTP Chromium journeys for a SYNTHETIC source-neutral Core2 legacy reader.

Never loads a private question, real key or copyrighted exam diagram. Checks that
the same production patcher refuses ambiguous links, protects first answers and
handles missing media, disabled storage, refresh and navigation on two viewports.
"""
from __future__ import annotations
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from nsejs_core2_handoff_guard import patch_reader

def demand(condition,msg):
    if not condition: raise AssertionError(msg)

def run_one(browser,base,width,height):
    context=browser.new_context(viewport={'width':width,'height':height})
    try:
        page=context.new_page()
        failures=[]
        page.on('pageerror',lambda e:failures.append(str(e)))
        res=page.goto(base+'/preview/question-status.html',wait_until='load')
        demand(res is not None and res.status==200,'HTTP synthetic fixture failed')
        demand(page.locator('.item').count()==2,'Two source-neutral subject records missing')
        demand(page.locator('#commit-btn').count()==1,'Reader runtime crashed')
        demand(page.locator('#reveal-btn').is_disabled(),'Solution is visible before first attempt')
        demand(page.locator('.hint').count()==0,'Hint content visible before frozen original attempt')
        demand('REQUIRED DIAGRAM UNAVAILABLE' in page.locator('#question-root').inner_text(),
               'Missing diagram was hidden/invented or caused exception')
        demand('KEY AUTHORITY HOLD' in page.locator('#question-root').inner_text(),
               'Unverified official key was promoted')
        page.locator('input[name="answer-option"][value="A"]').check()
        page.locator('#commit-btn').click()
        demand(page.locator('#commit-btn').is_disabled(),'Saved first answer not frozen')
        demand(not page.locator('#reveal-btn').is_disabled(),'Saved first answer did not unlock reveal')
        page.reload()
        demand(page.locator('#commit-btn').is_disabled(),'Reload lost first source-specific attempt')
        demand(page.locator('input[name="answer-option"][value="A"]').is_checked(),
               'Reload changed original answer')
        demand(page.locator('.hint').count()==3,'Hints not gated after saved first attempt')
        page.locator('#reveal-btn').click()
        demand(len(page.locator('#solution-container').inner_text())>0,'No committed reveal')
        page.reload()
        demand(page.locator('#reveal-btn').is_disabled() and
               page.locator('#solution-container').inner_text(),
               'Separate reveal state lost on reload')
        # Same bare ID, but another subject/source: it must still require an attempt.
        page.locator('.item').nth(1).click()
        demand(not page.locator('#commit-btn').is_disabled(),'Different source inherited prior commitment')
        demand(page.locator('#reveal-btn').is_disabled(),'Other question inherited solution')
        demand('SYN-B' in page.locator('#question-root').inner_text(),'Wrong topic selected')
        page.go_back(wait_until='load')
        demand(not failures,'Browser JS errors: '+repr(failures))
        print('PASS desktop/mobile full first-attempt, reload, reveal and second-scope journey',
              str(width)+'x'+str(height))
    finally:context.close()

def ambiguous_and_storage_negatives(browser,base):
    context=browser.new_context()
    try:
        p=context.new_page()
        p.goto(base+'/preview/question-status.html?question=SYN-DUP-ID')
        demand(p.locator('.disambiguate').count()==2,
               'Legacy repeated ID silently resolved without subject choice')
        demand(p.locator('#commit-btn').count()==0,'Ambiguous link displayed an answer form')
        p.locator('.disambiguate').nth(1).click()
        demand('SYN-B' in p.locator('#question-root').inner_text(),
               'Explicit legacy subject selection ignored')
        # Reopened another context with browser-local storage unavailable.
        no=browser.new_context()
        try:
            page=no.new_page()
            page.add_init_script("Storage.prototype.setItem=function(){throw Error('storage denied');};")
            page.goto(base+'/preview/question-status.html')
            page.locator('input[name="answer-option"][value="B"]').check()
            page.locator('#commit-btn').click()
            demand(not page.locator('#commit-btn').is_disabled(),
                   'Storage denial falsely counted as saved original answer')
            demand(page.locator('#reveal-btn').is_disabled(),
                   'Storage denial leaked author solution')
            demand('SAVE FAILED' in page.locator('#commit-note').inner_text(),
                   'Storage failure not disclosed')
        finally:no.close()
        # Check stale form in another simulated tab that changed the scoped key.
        stale=browser.new_context()
        try:
            q=stale.new_page()
            q.goto(base+'/preview/question-status.html')
            q.locator('input[name="answer-option"][value="A"]').check()
            q.evaluate("""()=>{
              const ids=JSON.parse(document.getElementById('g9-nsejs-private-core2-revisions').textContent);
              const name='ALPHA::SYN-A::SYN-DUP-ID';
              const key='g9:nsejs:core2:private:v1:'+encodeURIComponent(name)+':'+ids[name];
              localStorage.setItem(key,'{"version":999,"mock":"stale"}');
            }""")
            q.locator('#commit-btn').click()
            demand('SAVE FAILED' in q.locator('#commit-note').inner_text(),
                   'Stale local source state overwrote another revision')
            demand(q.locator('#reveal-btn').is_disabled(),'Stale attempt revealed answer')
        finally:stale.close()
        print('PASS ambiguous short links, storage denial and stale overwrite refused')
    finally:context.close()

def main():
    with TemporaryDirectory(prefix='g9-syn-private-core2-') as temp:
        folder=Path(temp)
        (folder/'preview').mkdir()
        src=(ROOT/'tests/fixtures/nsejs_core2_legacy_synthetic.html').read_text()
        html,stats=patch_reader(src)
        demand(stats['question_count']==2 and stats['unscoped_count']==1,'Wrong synthetic record fixture')
        (folder/'preview/question-status.html').write_text(html,encoding='utf-8')
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(folder)))
        thread=Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            base='http://127.0.0.1:'+str(server.server_port)
            with sync_playwright() as playwright:
                browser=playwright.chromium.launch(headless=True)
                try:
                    for width,height in ((1366,768),(390,844)):
                        run_one(browser,base,width,height)
                    ambiguous_and_storage_negatives(browser,base)
                finally:browser.close()
        finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
