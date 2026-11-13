"""Wave 3 source→WPE lesson→exact authored Core2 return through real HTTP Chromium.

Tests are browser-only: the plain Python QA job must never silently collect
them without Playwright installed. They do not authenticate NSEJS exam papers.
"""
from __future__ import annotations

from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread
from urllib.parse import quote

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
UID = "g9:PHYSICS:G9-AUTH-MECH-001"
REV = "65eadfb0dfc06b4dc3c910ade26d5f5d005efea00be5d7c4f8128b3d45c29259"
ANCHOR = "question-G9-AUTH-MECH-001"


@pytest.fixture(scope="module")
def http_root():
    srv = ThreadingHTTPServer(("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    Thread(target=srv.serve_forever,daemon=True).start()
    try:
        yield "http://127.0.0.1:" + str(srv.server_port)
    finally:
        srv.shutdown()
        srv.server_close()


@pytest.fixture
def start(http_root):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        def open_one(path, *, width=1000, height=1600, override=None):
            ctx=browser.new_context(viewport={"width":width,"height":height},
                                    has_touch=True, is_mobile=True)
            page=ctx.new_page()
            errors=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.route("https://cdn.jsdelivr.net/**",
                       lambda route:route.fulfill(status=200,content_type="application/javascript",body=""))
            if override:
                def make_handler(payload):
                    def fulfill(route):
                        route.fulfill(status=200,content_type="application/json",
                                      body=json.dumps(payload))
                    return fulfill
                for fragment, data in override.items():
                    page.route("**/" + fragment, make_handler(data))
            response=page.goto(http_root + path, wait_until="domcontentloaded", timeout=30000)
            assert response.status == 200
            return ctx,page,errors
        yield open_one
        browser.close()


def return_path(*, revision=REV, uid=UID, fragment=ANCHOR):
    return ("/nsejs/physics/question-bank.html?topic=mechanics"
        + "&source_uid=" + quote(uid,safe="")
        + "&source_revision=" + revision + "#" + fragment)


@pytest.mark.parametrize("width,height",[(1000,1600),(1600,1000)])
def test_only_exact_authored_mechanics_card_has_learning_route(start,width,height):
    ctx,page,errors=start("/nsejs/physics/question-bank.html?topic=mechanics",
                          width=width,height=height)
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===11")
        page.locator("#nsejs-authored-learning-route a").wait_for(timeout=15000)
        assert page.locator("#nsejs-authored-learning-route").count()==1
        card=page.locator("article.card:has(#nsejs-authored-learning-route)")
        assert card.get_attribute("data-question-uid")==UID
        assert card.get_attribute("data-content-revision")==REV
        link=card.locator("a.nsejs-learning-touch-link")
        href=link.get_attribute("href")
        assert "source_uid="+quote(UID,safe="") in href
        assert "source_revision="+REV in href
        assert link.evaluate("n=>n.getBoundingClientRect().height")>=56
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4")
        assert page.locator("iframe").count()==0
        assert not errors,errors
        link.click()
        page.wait_for_url("**/nsejs/physics/learn-mechanics.html?**")
        page.locator("#nsejs-parity-status[data-state='PREVIEW']").wait_for(timeout=15000)
        assert page.locator("#nsejs-exact-source").inner_text().find("Authored Mechanics")>=0
    finally:
        ctx.close()


def test_return_exact_source_revision_is_focused_without_revealing_key(start):
    ctx,page,errors=start(return_path())
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===11")
        page.locator("#learning-return-status[data-state='PREVIEW']").wait_for(timeout=15000)
        target=page.locator("#"+ANCHOR)
        assert target.get_attribute("data-question-uid")==UID
        assert target.get_attribute("data-content-revision")==REV
        assert "nsejs-exact-source-return" in target.get_attribute("class")
        assert page.evaluate("document.activeElement.id")==ANCHOR
        assert target.locator(".answer:visible").count()==0
        assert target.get_by_role("button",name="Show explanation").is_disabled()
        assert "HOLD" in page.locator("#learning-return-status").inner_text()
        assert not errors,errors
    finally:
        ctx.close()


@pytest.mark.parametrize("revision,uid,fragment",[
    ("0"*64,UID,ANCHOR),
    (REV,"g9:PHYSICS:OTHER",ANCHOR),
    (REV,UID,"question-OTHER"),
])
def test_bad_return_never_focuses_a_different_card(start,revision,uid,fragment):
    ctx,page,errors=start(return_path(revision=revision,uid=uid,fragment=fragment))
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===11")
        page.locator("#learning-return-status[data-state='HOLD']").wait_for(timeout=15000)
        assert page.locator("#"+ANCHOR+".nsejs-exact-source-return").count()==0
        assert page.locator("#learning-return-status").inner_text().startswith("HOLD")
        assert page.locator(".answer:visible").count()==0
    finally:
        ctx.close()


def test_no_learner_link_for_other_50_unverified_corpus_items(start):
    ctx,page,errors=start("/nsejs/physics/question-bank.html?topic=optics")
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===10")
        page.wait_for_timeout(500)
        assert page.locator("#nsejs-authored-learning-route").count()==0
        assert page.locator("a.nsejs-learning-touch-link").count()==0
    finally:
        ctx.close()


@pytest.mark.parametrize("kind",["stale_source_stem","fake_admission","wrong_lesson_revision","duplicate_owner"])
def test_unsafe_author_source_or_route_is_rejected_not_linked(start,kind):
    original = json.loads((ROOT/"nsejs/data/physics-authored-practice-r1.json").read_text("utf-8"))
    bridge = json.loads((ROOT/"nsejs/data/source-learning-bridge-tech-preview.v1.json").read_text("utf-8"))
    lesson = json.loads((ROOT/"nsejs/data/mechanics-wpe-teaching-pilot.v1.json").read_text("utf-8"))
    overrides={}
    if kind=="stale_source_stem":
        original["questions"][0]["stem"]+=" injected"
        overrides["nsejs/data/physics-authored-practice-r1.json"]=original
    if kind=="fake_admission":
        bridge["academic_admission"]="PASS"
        overrides["nsejs/data/source-learning-bridge-tech-preview.v1.json"]=bridge
    if kind=="wrong_lesson_revision":
        bridge["routes"][0]["lesson_revision"]="obsolete"
        overrides["nsejs/data/source-learning-bridge-tech-preview.v1.json"]=bridge
    if kind=="duplicate_owner":
        bridge["routes"].append(deepcopy(bridge["routes"][0]))
        overrides["nsejs/data/source-learning-bridge-tech-preview.v1.json"]=bridge
    ctx,page,errors=start("/nsejs/physics/question-bank.html?topic=mechanics",override=overrides)
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===11")
        page.wait_for_timeout(700)
        assert page.locator("#nsejs-authored-learning-route").count()==0
        assert page.locator(".answer:visible").count()==0
    finally:
        ctx.close()


def test_malformed_encoded_return_fragment_fails_closed_without_script_exception(start):
    # Encoded return anchors are untrusted URL input. A bad escape must not
    # cause an unhandled URIError in the asynchronous observer callback.
    ctx,page,errors=start(return_path(fragment="question-%ZZ"))
    try:
        page.wait_for_function("document.querySelectorAll('article.card').length===11")
        page.locator("#learning-return-status[data-state='HOLD']").wait_for(timeout=15000)
        assert "invalid source UID, revision, topic or fragment" in page.locator(
            "#learning-return-status").inner_text()
        assert page.locator(".nsejs-exact-source-return").count()==0
        assert page.locator(".answer:visible").count()==0
        assert not errors,errors
    finally:
        ctx.close()


def test_conflicting_core2_uid_filter_blocks_return_even_when_revision_matches(start):
    # The reader optionally filters cards by ?uid. A conflicting UID must be
    # explicitly rejected; do not leave a pending/blank return status forever.
    path=return_path().replace("#"+ANCHOR,
        "&uid="+quote("g9:PHYSICS:WRONG",safe="")+"#"+ANCHOR)
    ctx,page,errors=start(path)
    try:
        page.locator("#learning-return-status[data-state='HOLD']").wait_for(timeout=15000)
        assert page.locator(".nsejs-exact-source-return").count()==0
        assert page.locator(".answer:visible").count()==0
        assert page.locator("#learning-return-status").inner_text().startswith("HOLD")
        assert not errors,errors
    finally:
        ctx.close()
