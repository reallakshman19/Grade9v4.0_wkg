"""Real Chromium formative feedback, first-attempt persistence and academic HOLD.

Actual 50 historical candidate keys are producer-proposed, not authenticated.
Multiple-correct controls are TEST-ONLY injected authored practices, never
committed to Git or represented as actual NSEJS questions.
"""
from __future__ import annotations

from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def server():
    srv=ThreadingHTTPServer(("127.0.0.1",0),
        partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    Thread(target=srv.serve_forever,daemon=True).start()
    try:
        yield "http://127.0.0.1:"+str(srv.server_port)
    finally:
        srv.shutdown()
        srv.server_close()


@pytest.fixture
def launch(server):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        def start(topic="optics",*,storage_denied=False,extra=None):
            context=browser.new_context(viewport={"width":1000,"height":1600},
                has_touch=True,is_mobile=True)
            if storage_denied:
                context.add_init_script(
                    "Storage.prototype.setItem=function(){throw Error('Quota denied')};")
            page=context.new_page()
            errors=[]
            page.on("pageerror",lambda error:errors.append(str(error)))
            page.route("https://cdn.jsdelivr.net/**",
                lambda route:route.fulfill(status=200,content_type="application/javascript",body=""))
            if extra is not None:
                def authored(route):
                    route.fulfill(status=200,content_type="application/json",
                                  body=json.dumps(extra))
                page.route("**/nsejs/data/physics-authored-practice-r1.json",authored)
            response=page.goto(server+"/nsejs/physics/question-bank.html?topic="+topic,
                               wait_until="domcontentloaded",timeout=30000)
            assert response.status==200
            page.locator("article.card").first.wait_for(timeout=15000)
            return context,page,errors
        yield start
        browser.close()


@pytest.mark.parametrize("choice,expected,cls",[
    ("B","matches","proposal-match"),
    ("A","differs","proposal-diff"),
])
def test_producer_proposal_visible_only_after_saved_first_response(launch,choice,expected,cls):
    context,page,errors=launch()
    try:
        card=page.locator("#question-NSEJS-23-OPT-02")
        card.wait_for(timeout=15000)
        assert card.locator(".producer-proposal-feedback:visible").count()==0
        assert card.locator(".options .proposal-match").count()==0
        assert card.locator(".answer:visible").count()==0
        assert card.get_by_role("button",name="Show explanation").is_disabled()
        card.locator('input[value="'+choice+'"]').check()
        card.get_by_role("button",name="Save first attempt").click()
        note=card.locator(".producer-proposal-feedback:visible")
        note.wait_for()
        assert "UNVALIDATED" in note.inner_text()
        assert "not a verified answer key" in note.inner_text().lower()
        assert expected in note.inner_text()
        assert card.locator('.options label.'+cls+' input[value="'+choice+'"]').count()==1
        assert card.get_by_role("button",name="Show explanation").is_enabled()
        assert card.locator(".answer:visible").count()==0
        page.reload(wait_until="domcontentloaded")
        card=page.locator("#question-NSEJS-23-OPT-02")
        card.locator(".producer-proposal-feedback:visible").wait_for(timeout=15000)
        assert card.locator('input[value="'+choice+'"]').is_checked()
        assert card.locator(".answer:visible").count()==0
        assert card.locator(".producer-proposal-feedback").inner_text().find("not a verified answer key")>=0
        assert not errors,errors
    finally:
        context.close()


def test_storage_denial_cannot_show_comparison_or_explanation(launch):
    context,page,errors=launch(storage_denied=True)
    try:
        card=page.locator("#question-NSEJS-23-OPT-02")
        card.locator('input[value="B"]').check()
        card.get_by_role("button",name="Save first attempt").click()
        assert card.get_by_role("button",name="Show explanation").is_disabled()
        assert card.locator(".producer-proposal-feedback:visible").count()==0
        assert "NOT SAVED" in card.locator(".actions").inner_text()
        assert card.locator(".answer:visible").count()==0
        assert not errors,errors
    finally:
        context.close()


def synthetic_multi():
    data=json.loads((ROOT/"nsejs/data/physics-authored-practice-r1.json").read_text("utf-8"))
    for tag,key in [("MULTI","Official Key: (A) and (C)"),
                    ("AMBIG","Producer response unreviewed")]:
        q=deepcopy(data["questions"][0])
        q["source_id"]=q["id"]="G9-TEST-"+tag+"-NOT-PUBLISHED"
        q["question_type"]="multiple_correct_mcq"
        q["topic"]="MECHANICS"
        q["stem"]="Synthetic test-only options, not an exam item."
        q["options"]=["A: Option Alpha","B: Option Beta","C: Option Gamma","D: Option Delta"]
        q["answer"]=key
        q["steps"]=["Synthetic testing only; not assessed."]
        q["check"]="Synthetic boundary test only."
        q["source_figures"]=[]
        data["questions"].append(q)
    return data


def test_synthetic_multiple_answer_overlap_is_not_partial_marking(launch):
    context,page,errors=launch(topic="mechanics",extra=synthetic_multi())
    try:
        card=page.locator("#question-G9-TEST-MULTI-NOT-PUBLISHED")
        card.wait_for(timeout=15000)
        assert card.locator('input[type="checkbox"]').count()==4
        assert card.locator(".producer-proposal-feedback:visible").count()==0
        card.locator('input[value="A"]').check()
        card.locator('input[value="B"]').check()
        card.get_by_role("button",name="Save first attempt").click()
        msg=card.locator(".producer-proposal-feedback")
        msg.wait_for(state="visible")
        assert "1 of 2 proposed options selected; 1 additional selected" in msg.inner_text()
        assert "not partial credit or a score" in msg.inner_text().lower()
        assert card.locator('.options label.proposal-match input[value="A"]').count()==1
        assert card.locator('.options label.proposal-diff input[value="B"]').count()==1
        assert card.locator('.options label.proposal-not-selected input[value="C"]').count()==1
        assert card.locator(".answer:visible").count()==0
        card2=page.locator("#question-G9-TEST-AMBIG-NOT-PUBLISHED")
        card2.locator('input[value="A"]').check()
        card2.get_by_role("button",name="Save first attempt").click()
        assert "No reliable producer-option comparison" in card2.locator(
            ".producer-proposal-feedback").inner_text()
        assert card2.locator(".options label.proposal-match").count()==0
        assert not errors,errors
    finally:
        context.close()
