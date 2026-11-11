"""Real HTTP Chromium for synthetic-only R6 scoped links/attempts (12.7-inch)."""
from __future__ import annotations
import sys
import tempfile
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_private_reader_r6 import fixture
from private_reader_r6 import upgrade_site

VIEWPORTS=((1280,800),(1472,920),(800,1280))


def run():
    journeys=[]
    with tempfile.TemporaryDirectory(prefix='g9-r6-synthetic-') as tmp:
        src,out=fixture(Path(tmp))
        receipt=upgrade_site(src,out)
        assert receipt['academic_approval']=='HOLD'
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(out),**kwargs)
            def log_message(self,*args):pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            base=f'http://127.0.0.1:{server.server_address[1]}/preview/question-status.html'
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
                try:
                    for w,h in VIEWPORTS:
                        ctx=browser.new_context(viewport={'width':w,'height':h})
                        page=ctx.new_page()
                        errors=[]
                        page.on('pageerror',lambda e,acc=errors: acc.append(str(e)))
                        response=page.goto(base+'?question=DUPLICATE-ID',wait_until='load',timeout=15000)
                        assert response is not None and response.status==200
                        assert page.locator('.choose-legacy').count()==2,'Ambiguous alias silently resolved'
                        assert page.locator('#commit-btn').count()==0
                        page.locator('.choose-legacy').nth(1).click()
                        assert 'Synthetic energy problem B' in page.locator('h2').inner_text()
                        assert page.locator('#commit-btn').is_enabled()
                        assert 'BETA' in page.url
                        page.locator('.hint summary').click()
                        page.locator('input[name="answer-option"]').first.check()
                        page.locator('#commit-btn').click()
                        assert 'saved in this browser' in page.locator('#commit-note').inner_text().lower()
                        state=page.evaluate("() => JSON.parse(Object.values(localStorage).find(v=>v.includes('firstAttempt')) || '{}')")
                        assert state.get('committed') is True
                        assert state['firstAttempt']['assisted'] is True
                        assert page.locator('#commit-btn').is_disabled()
                        page.reload(wait_until='load')
                        assert page.locator('#commit-btn').is_disabled(),'First attempt not preserved'
                        assert 'restored' in page.locator('#commit-note').inner_text().lower()
                        page.locator('#navlist .item').first.click()
                        assert page.locator('#commit-btn').is_enabled(),'Cross-topic attempt contamination'
                        assert not errors,errors
                        journeys.append((w,'scoped alias + saved attempt + hint + cross-topic'))
                        ctx.close()
                    blocked=browser.new_context(viewport={'width':1280,'height':800})
                    blocked.add_init_script("""(() => {
                      const original=Storage.prototype.setItem;
                      Storage.prototype.setItem=function(k,v) {
                        if(k.startsWith('g9:private:practice:v3:'))
                          throw new DOMException('Denied','QuotaExceededError');
                        return original.call(this,k,v);
                      };
                    })()""")
                    page=blocked.new_page()
                    r=page.goto(base,wait_until='load',timeout=15000)
                    assert r is not None and r.status==200
                    page.locator('input[name="answer-option"]').first.check()
                    page.locator('#commit-btn').click()
                    assert 'not saved' in page.locator('#commit-note').inner_text().lower()
                    page.reload(wait_until='load')
                    assert page.locator('#commit-btn').is_enabled()
                    journeys.append((1280,'storage denial NO SAVE'))
                    blocked.close()
                finally:browser.close()
        finally:
            server.shutdown();server.server_close();thread.join(timeout=5)
    return journeys

if __name__=='__main__':
    j=run()
    print(f'PASS: {len(j)} synthetic direct HTTP Chromium R6 journeys (three 12.7-inch viewports + storage denial)')