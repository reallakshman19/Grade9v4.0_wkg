"""Student-facing Core tile map; old architecture content stays preserved and collapsed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "architecture" / "index.html"

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
    def handle_starttag(self, name, attrs):
        self.tags.append((name, dict(attrs)))

def test_tile_mapping_and_no_iframes():
    html = PAGE.read_text(encoding="utf-8")
    parser = Elements()
    parser.feed(html)
    assert not any(name == "iframe" for name, _ in parser.tags)
    for item in ("core-role-map", "core1a-role", "core1b-role", "core2-role", "previous-architecture"):
        assert sum(attrs.get("id") == item for _, attrs in parser.tags) == 1
    assert "Learn → Challenge is the way in—not a fourth Core." in html
    assert "Core1A + Core1B" in html and "Core2" in html
    assert "PR #55" in html and "planned" in html
    assert "No iframe integration:" in html
    details = [attrs for name, attrs in parser.tags if name == "details" and attrs.get("id") == "previous-architecture"]
    assert len(details) == 1 and "open" not in details[0]
    assert sum(name == "summary" for name, _ in parser.tags) >= 1

def test_old_architecture_material_is_preserved_in_disclosure():
    html = PAGE.read_text(encoding="utf-8")
    archive = html.split('<div class="legacy-content">', 1)[1].split('</details>', 1)[0]
    assert archive.count('<article class="card">') == 9
    assert html.count('Production checklist · Core2 tablet QA') == 1
    assert html.count('<article class="card">') == 9
    for text in (
        "Production checklist · Core2 tablet QA",
        "Start with the guidebook",
        "QRT × Physics Blueprint: a repeatable decision protocol",
        "Authority boundary",
        "Explore the learning blueprint",
        "Suggested reading sequence (not the independent-review packet)",
        "Scope & authority", "Intake & custody", "WPE review examples",
    ):
        assert text in archive
    assert archive.strip().startswith('<section class="panel"')

def test_new_learning_links_are_direct_local_destinations():
    html = PAGE.read_text(encoding="utf-8")
    new = html.split('<section class="core-map"', 1)[1].split('<details class="legacy-archive"', 1)[0]
    parser = Elements()
    parser.feed(new)
    links = [attrs["href"] for name, attrs in parser.tags if name == "a" and "href" in attrs]
    ids = {attrs.get("id") for _, attrs in parser.tags if attrs.get("id")}
    assert len(links) >= 10
    for href in links:
        if href.startswith("#"):
            assert href[1:] in ids, href
            continue
        if href.startswith("https://"):
            assert "github.com/reallakshman19/Grade9v4.0/pull/55" in href
            continue
        split = urlsplit(href)
        assert split.scheme == "" and not split.netloc
        assert not href.startswith("//")
        assert (PAGE.parent / unquote(split.path)).resolve().is_file(), href
