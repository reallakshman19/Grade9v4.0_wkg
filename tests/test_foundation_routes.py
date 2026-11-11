"""Public-only Foundation/NSEJS directory: no private reader or exam bank."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT=Path(__file__).resolve().parents[1]
ROUTES=['physics/index.html','physics/foundation/index.html','exams/index.html','exams/nsejs/index.html']

class Links(HTMLParser):
    def __init__(self):super().__init__();self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            href=dict(attrs).get('href','')
            if href:self.hrefs.append(href)

def test_public_routes_and_local_links_resolve():
    for route in ROUTES:
        file=ROOT/route
        assert file.is_file(),route
        page=file.read_text(encoding='utf-8')
        assert 'name="viewport"' in page
        assert 'content="width=device-width,initial-scale=1"' in page
        assert 'private_review_site' not in page
        assert 'question-status.html' not in page
        assert '<iframe' not in page
        parser=Links();parser.feed(page)
        for href in parser.hrefs:
            parts=urlparse(href)
            if parts.scheme in ('https','mailto'):continue
            assert not parts.netloc
            local=(file.parent/unquote(parts.path)).resolve()
            assert local.is_relative_to(ROOT),href
            assert local.is_file(),(route,href)

def test_scope_and_subject_ownership():
    landing=(ROOT/'physics/index.html').read_text()
    assert 'foundation/index.html' in landing
    assert '../exams/nsejs/index.html' in landing
    foundation=(ROOT/'physics/foundation/index.html').read_text()
    assert '../wpe/index.html' in foundation
    exam=(ROOT/'exams/nsejs/index.html').read_text()
    assert all(s in exam for s in ('Physics','Chemistry','Biology'))
    assert 'not complete NSEJS preparation' in exam
    assert 'No private practice reader is linked' in exam
    for route in ROUTES:
        page=(ROOT/route).read_text()
        assert 'Mathematics' in page and 'Chemistry' in page and 'Architecture' in page
