"""Architecture page is a usable inline concept and agent guidebook, with the old content intact."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "architecture" / "index.html"
CHAPTERS = [
    "guide-concept", "guide-two-routes", "guide-preflight", "guide-procedure",
    "guide-construction", "guide-example", "guide-gates", "guide-delivery",
]

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
    def handle_starttag(self, name, attrs):
        self.nodes.append((name, dict(attrs)))

def test_inline_concept_and_working_procedure_are_not_link_only():
    source = PAGE.read_text(encoding="utf-8")
    parser = Elements()
    parser.feed(source)
    ids = [attrs.get("id") for _, attrs in parser.nodes]
    assert ids.count("agent-guidebook") == 1
    assert all(ids.count(chapter) == 1 for chapter in CHAPTERS)
    assert source.index('id="agent-guidebook"') < source.index('id="previous-architecture"')
    for chapter in CHAPTERS:
        section = source.split('id="' + chapter + '"', 1)[1].split('</section>', 1)[0]
        assert len(section) > 950, chapter
    for label in ("Route A — exact question", "Route B — source exposition",
                  "S0 — Pin the task", "S9 — Verify and deliver", "B1 · Target",
                  "B7 · Physics / provenance", "six-stage", "HELP", "EX-M79",
                  "EX-M97", "HOLD", "NOT_RUN", "No academic approval inferred"):
        if label == "HELP":
            assert "Help is optional" in source
        else:
            assert label in source, label
    assert "author-exposed material" in source
    assert "source-only packet" in source
    assert "No iframe" in source or "Do not use iframes" in source
    assert not any(tag == "iframe" for tag, _ in parser.nodes)

def test_references_and_on_page_navigation_are_all_resolvable():
    source = PAGE.read_text(encoding="utf-8")
    new = source.split('<section class="arch-guide"', 1)[1].split('<details class="legacy-archive"', 1)[0]
    parser = Elements()
    parser.feed(new)
    ids = {a.get("id") for _, a in parser.nodes}
    links = [a["href"] for n, a in parser.nodes if n == "a" and "href" in a]
    assert len(links) >= 10
    for href in links:
        if href.startswith("#"):
            assert href[1:] in ids, href
        else:
            u = urlsplit(href)
            assert not u.scheme and not u.netloc
            assert (PAGE.parent / unquote(u.path)).resolve().is_file(), href

def test_previous_guidebook_and_architecture_archive_are_still_present():
    html = PAGE.read_text(encoding="utf-8")
    assert html.count('<details class="legacy-archive" id="previous-architecture">') == 1
    archive = html.split('<div class="legacy-content">', 1)[1].split('</details>', 1)[0]
    assert archive.count('<article class="card">') == 9
    for term in ("Production checklist · Core2 tablet QA",
                 "QRT × Physics Blueprint: a repeatable decision protocol",
                 "Explore the learning blueprint",
                 "Suggested reading sequence (not the independent-review packet)"):
        assert term in archive
    assert "guidebook.html" in archive
    assert "concept-report-v4.html" in archive


def test_architecture_current_wpe_r2_counts_match_source_map():
    import json
    page = PAGE.read_text(encoding="utf-8")
    map_data = json.loads((ROOT / "physics/wpe/learning-coverage-r1.json").read_text(encoding="utf-8"))
    assert map_data["counts"]["total"] == 74
    assert (map_data["counts"]["focused_new"], map_data["counts"]["targeted"],
            map_data["counts"]["related"], map_data["counts"]["missing"]) == (8, 18, 48, 0)
    new = page.split('<details class="legacy-archive"', 1)[0]
    assert "21 C/E/F journeys" in new
    assert "F04–F08 · Additional focused journeys" in new
    assert 'href="../physics/wpe/gap-journeys.html?question=EX-M50#F04"' in new
    assert "48 related-only bridges" in new
    assert "16 C/E/F journeys" not in new
    assert 'id="agent-guidebook"' in new
