"""Architecture Core1A/1B authoring manual: in-page teaching, source authority and science gates."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "architecture/index.html"
BOOK = ROOT / "architecture/guidebook.html"
BLUEPRINT = ROOT / "templates/physics-blueprint/physics-blueprint.D3-D4.json"
MAP = ROOT / "physics/wpe/learning-coverage-r1.json"
RUNBOOK = ROOT / "architecture/qrt-blueprint-protocol/RUNBOOK.md"

HOME_NEW = ("guide-author-decision","guide-qrt-binding","guide-science-tests")
BOOK_NEW = ("author-workbench","qrt-practice","blueprint-practice","core1a-studio",
            "core1b-studio","science-cases","test-studio","release-checklist")

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags=[]
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag,dict(attrs)))

def parsed(s):
    p=Inspector();p.feed(s);return p.tags

def section(s, id):
    return s.split(f'id="{id}"',1)[1].split("</section>",1)[0]

def test_agent_playbook_is_substantive_and_navigable_in_both_pages():
    for file, ids, min_chars in ((HOME,HOME_NEW,1050),(BOOK,BOOK_NEW,1700)):
        s=file.read_text(encoding="utf-8")
        tags=parsed(s)
        present=[a.get("id") for _,a in tags if a.get("id")]
        for sid in ids:
            assert present.count(sid)==1, (file,sid)
            assert len(section(s,sid))>min_chars, (file,sid)
            assert any(t=="a" and a.get("href")==f"#{sid}" for t,a in tags), (file,sid)
        assert not any(t=="iframe" for t,_ in tags), file
    assert HOME.read_text(encoding="utf-8").index('id="agent-guidebook"') < HOME.read_text(encoding="utf-8").index('id="previous-architecture"')

def test_new_guidebook_links_to_real_local_sources_and_anchors():
    for file,ids in ((HOME,HOME_NEW),(BOOK,BOOK_NEW)):
        s=file.read_text(encoding="utf-8")
        tags=parsed(s)
        all_ids={a["id"] for _,a in tags if a.get("id")}
        for sid in ids:
            snippet=section(s,sid)
            p=parsed(snippet)
            for tag,a in p:
                if tag!="a" or not a.get("href"):continue
                href=a["href"]
                url=urlsplit(href)
                if url.scheme:continue
                if not url.path:
                    assert url.fragment in all_ids, (file,sid,href)
                else:
                    target=(file.parent/unquote(url.path)).resolve()
                    assert target.is_file(), (file,sid,href)
                    if url.fragment and target.suffix==".html":
                        targets={attr["id"] for _,attr in parsed(target.read_text(encoding="utf-8")) if attr.get("id")}
                        assert url.fragment in targets, (file,sid,href)

def test_qrt_blueprint_adapter_role_separation_matches_actual_draft():
    h=HOME.read_text(encoding="utf-8")
    b=BOOK.read_text(encoding="utf-8")
    data=json.loads(BLUEPRINT.read_text(encoding="utf-8"))
    assert data["blueprint_id"]=="PHYS-QRT-BLUEPRINT"
    assert data["status"]=="DRAFT_OWNER_REVIEW"
    assert len(data["cells"])==14
    assert len(data["column_order"])==7
    assert [str(x).upper() for x in data["column_order"]]==["RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"]
    assert "D3.4" in data["cells"] and "D4.7" in data["cells"]
    for required in ("D3.4","D4.7","DRAFT_OWNER_REVIEW","UNSELECTED","D1/D2",
                     "source-only","five factors","RETRIEVE","JUSTIFY","MAIN","instance"):
        assert required.lower() in (h+b).lower(), required
    assert "AUTHOR_EXPOSED" in RUNBOOK.read_text(encoding="utf-8")
    assert "INDEPENDENT_QRT" in RUNBOOK.read_text(encoding="utf-8")
    assert "No academic approval inferred from software validation" in h+b

def test_core1a_core1b_explicit_decisions_and_adversarial_science():
    h=HOME.read_text(encoding="utf-8")
    b=BOOK.read_text(encoding="utf-8")
    for value in ("Conventions","Before you start","Build the idea","Worked anchor",
                  "Plausible wrong path","Close the idea","Y","Z","W","H1","H2","H3",
                  "B1–B7","first attempt","changed-condition","negative",
                  "vanishing-perturbation","C6S","C6H","C6W","EX-M6","F05",
                  "source_id","NOT_RUN","HOLD"):
        assert value.lower() in (h+b).lower(), value
    assert "20 browser paths" in b
    assert "python -m pytest -q" in b
    assert "still contains an iframe" not in h
    assert "uses a verified full-page link" in h
    assert "Blind" in b or "blind" in b

def test_archive_and_unchanged_coverage_admission_status():
    h=HOME.read_text(encoding="utf-8")
    archive=h.split('<div class="legacy-content">',1)[1].split("</details>",1)[0]
    assert archive.count('<article class="card">')==9
    assert h.count('<details class="legacy-archive" id="previous-architecture">')==1
    assert '<details class="legacy-archive" id="previous-architecture" open' not in h
    assert "QRT × Physics Blueprint: a repeatable decision protocol" in archive
    c=json.loads(MAP.read_text(encoding="utf-8"))["counts"]
    assert (c["total"],c["focused_new"],c["targeted"],c["related"],c["missing"])==(74,8,18,48,0)
    assert "48 related-only bridges" in h
