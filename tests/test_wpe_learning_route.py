"""Navigation-only WPE integration checks; never claim question or learner admission."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "physics/wpe/index.html": ("quicklinks", 9),
    "physics/wpe/learn-challenge.html": ("wpe-related-pages", 5),
    "preview/physics-wpe.html": ("wpe-learning-route", 5),
    "preview/practice.html": ("wpe-learning-route", 5),
    "preview/batches/reader.html": ("Collection navigation", 4),
}

class NavLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.links = []
        self.ids = set()
        self.target_name = None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "nav" and (d.get("id") == self.target_name or
                             d.get("class") == self.target_name or
                             d.get("aria-label") == self.target_name):
            self.depth += 1
        elif tag == "nav" and self.depth:
            self.depth += 1
        if tag == "a" and self.depth and d.get("href"):
            self.links.append(d["href"])
    def handle_endtag(self, tag):
        if tag == "nav" and self.depth:
            self.depth -= 1

def parsed(path, target_name=None):
    doc = NavLinks()
    doc.target_name = target_name
    doc.feed((ROOT / path).read_text(encoding="utf-8"))
    return doc

def test_navigation_links_resolve_to_existing_pages_and_anchors():
    expected = {
        "physics/wpe/index.html": ("learn-challenge.html", "question-coverage.html", "extension-learning.html"),
        "physics/wpe/learn-challenge.html": ("index.html", "question-bank.html"),
        "preview/physics-wpe.html": ("../physics/wpe/learn-challenge.html#potential-force",),
        "preview/practice.html": ("../physics/wpe/learn-challenge.html#energy-motion",),
        "preview/batches/reader.html": ("../../physics/wpe/learn-challenge.html",),
    }
    for src, (nav, count) in ROUTES.items():
        links = parsed(src, nav).links
        assert len(links) == count, (src, links)
        for required in expected[src]:
            assert required in links, (src, required)
        for href in links:
            url = urlsplit(href)
            assert not url.scheme, (src, href, "unexpected offsite route")
            target = ((ROOT / src).parent / unquote(url.path)).resolve()
            assert target.is_relative_to(ROOT) and target.is_file(), (src, href)
            if url.fragment:
                assert url.fragment in parsed(target.relative_to(ROOT)).ids, (src, href)

def test_only_authored_learner_navigation_changed():
    hub = (ROOT / "physics/wpe/index.html").read_text(encoding="utf-8")
    guided = (ROOT / "physics/wpe/learn-challenge.html").read_text(encoding="utf-8")
    practice = (ROOT / "preview/practice.html").read_text(encoding="utf-8")
    examples = (ROOT / "preview/batches/reader.html").read_text(encoding="utf-8")
    assert "Primary guided path" in hub
    assert "not yet a native Core1A/Core1B-approved course" in hub
    assert guided.count('<article class="lesson"') == 5
    assert "Academic admissions: 0" in guided
    assert "not a verified exam question" in practice
    assert "ZERO ACADEMIC ADMISSIONS" in examples
    assert "NOT NATIVE CORE2/CORE1A" in examples
    assert 'id="btn-reveal-solution"' in practice and 'id="panel-solution"' in practice

def test_full_width_question_bank_redirect_and_custody_unchanged():
    wrapper = (ROOT / "physics/wpe/question-bank.html").read_text(encoding="utf-8")
    reader = (ROOT / "preview/question-status.html").read_text(encoding="utf-8")
    assert 'location.replace("https://reallakshman19.github.io/Grade9v4.0/preview/question-status.html"+location.search+location.hash)' in wrapper
    assert 'href="../physics/wpe/index.html"' in reader
    assert "0 academically admitted" in reader
    assert "if(!s?.committed)return" in reader
