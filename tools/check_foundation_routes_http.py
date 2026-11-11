"""Real HTTP Chromium smoke test for public-only 12.7-inch Foundation routes."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ROUTES=('physics/index.html','physics/foundation/index.html','exams/index.html','exams/nsejs/index.html')
VIEWPORTS=((1280,800),(1472,920),(800,1280))

def run():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True)
    worker.start()
    count=0
    try:
        base='http://127.0.0.1:'+str(server.server_address[1])
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
            try:
                for width,height in VIEWPORTS:
                    context=browser.new_context(viewport={'width':width,'height':height})
                    page=context.new_page()
                    errors=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    try:
                        for route in ROUTES:
                            response=page.goto(base+'/'+route,wait_until='load',timeout=15000)
                            assert response and response.status==200,(route,'HTTP')
                            assert page.locator('header.mast h1').count()==1,(route,'header')
                            assert page.locator('main.container').count()==1,(route,'main')
                            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'),(route,width,'overflow')
                            assert not errors,(route,errors)
                            count+=1
                        page.goto(base+'/physics/index.html',wait_until='load')
                        page.get_by_role('link',name='Open Physics Foundation').click()
                        assert page.url.endswith('/physics/foundation/index.html')
                        page.get_by_role('link',name='View NSEJS scope and status').click()
                        assert page.url.endswith('/exams/nsejs/index.html')
                    finally:context.close()
            finally:browser.close()
    finally:server.shutdown();server.server_close();worker.join(timeout=5)
    return count

if __name__=='__main__':
    print('PASS: '+str(run())+' synthetic-free public Foundation/NSEJS HTTP Chromium journeys (12.7-inch viewports)')
