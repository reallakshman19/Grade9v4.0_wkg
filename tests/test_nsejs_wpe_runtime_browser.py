"""Actual HTTP Chromium tests of the existing WPE engine through NSEJS adapter.

The fixture adapts a clearly synthetic contract to the checked-in AUTHORED
Mechanics source UID for technical routing tests only. It does NOT constitute
independent scientific acceptance of the Wave 2 Mechanics authored lesson.
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
LESSON_ID = "G9-NSEJS-AUTH-MECH-001-CORE1"


@pytest.fixture(scope="module")
def server():
    server = ThreadingHTTPServer(("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port)
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture
def fixture_data():
    bridge = json.loads((ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json")
                        .read_text("utf-8"))
    assert len(bridge["routes"]) == 1
    route = bridge["routes"][0]
    src = json.loads((ROOT / "nsejs/data/physics-authored-practice-r1.json")
                     .read_text("utf-8"))
    c = json.loads((ROOT / "nsejs/contracts/fixtures/synthetic-wpe-learner.v1.json")
                   .read_text("utf-8"))
    c["source"] = {
        "question_uid": route["question_uid"],
        "content_revision_sha256":route["content_revision_sha256"],
        "origin":"AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM",
        "academic_admission":"HOLD",
    }
    c["lesson"]["id"] = LESSON_ID
    c["lesson"]["revision"] = "synthetic-browser-technical-only-r1"
    c["lesson"]["title"] = "Synthetic WPE adapter browser witness"
    c["lesson"]["short"] = "Synthetic model and two tasks"
    c["lesson"]["sourceCaution"] = "Synthetic-only WPE adapter test, not an exam or scientific acceptance."
    c["lesson"]["core1a"]["model"]["label"] = "Synthetic friction control"
    c["lesson"]["core1a"]["model"]["value"] = 4
    c["lesson"]["core1a"]["academic"] = {
        "decision":"Select the correct system.",
        "observe":"Use the slider as a practice model.",
        "validity":"Synthetic-only WPE adapter test.",
        "limit":"Do not infer official exam mastery.",
        "sourceBoundary":"Authored practice, HOLD.",
    }
    c["tasks"]["A"]["id"] = route["task_a_id"]
    c["tasks"]["B"]["id"] = route["task_b_id"]
    c["source_return"] = {
        "page":route["source_return"]["page"],
        "topic":"mechanics",
        "question_uid":route["question_uid"],
        "content_revision_sha256":route["content_revision_sha256"],
        "route_status":"UNBUILT",
    }
    return c, src, route


@pytest.fixture
def open_page(server, fixture_data):
    c, src, route = fixture_data
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        def open_one(*, width=1000, height=1600, changed_source=None,
                     storage_denied=False, uid=None, revision=None):
            context = browser.new_context(viewport={"width":width,"height":height},
                                          has_touch=True, is_mobile=True)
            if storage_denied:
                context.add_init_script(
                    "Storage.prototype.setItem = function(){throw new Error('storage denied')};")
            page = context.new_page()
            errors = []
            page.on("pageerror",lambda error: errors.append(str(error)))
            modified = deepcopy(changed_source) if changed_source is not None else src
            page.route("**/nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
                lambda request: request.fulfill(
                    status=200, content_type="application/json",
                    body=json.dumps(c, separators=(",",":"))))
            page.route("**/nsejs/data/physics-authored-practice-r1.json",
                lambda request: request.fulfill(
                    status=200, content_type="application/json",
                    body=json.dumps(modified, separators=(",",":"))))
            params = "?source_uid=" + quote(uid if uid is not None else route["question_uid"],safe="")
            params += "&source_revision=" + quote(
                revision if revision is not None else route["content_revision_sha256"],safe="")
            page.goto(server + "/nsejs/physics/learn-mechanics.html" + params,
                      wait_until="domcontentloaded", timeout=30000)
            return context, page, errors
        yield open_one
        browser.close()


def wait_ready(page):
    page.locator("#nsejs-parity-status[data-state='PREVIEW']").wait_for(timeout=15000)
    page.locator('.stage-root button[data-action="prediction"]').wait_for(timeout=15000)


def save_prediction(page, text="I will choose the governing physical system."):
    page.locator('.stage-root [data-field="prediction"]').fill(text)
    page.locator('.stage-root [data-action="prediction"]').click()
    page.locator('.stage-root [data-action="attempt"]').wait_for()


def save_attempt(page, task, reason="The chosen model follows from the physical conditions."):
    option = next(x["expected"] for x in task["fields"] if x["id"] == "model")
    page.locator('.stage-root [data-field="model"]').select_option(label=option)
    page.locator('.stage-root [data-field="reason"]').fill(reason)
    assert page.locator('.stage-root .worked').count() == 0
    page.locator('.stage-root [data-action="attempt"]').click()
    page.locator('.stage-root [data-action="reconstruct"]').wait_for()
    assert page.locator('.stage-root .worked').count() >= 1


def finish_boundary(page, task):
    page.locator('.stage-root [data-action="reconstruct"]').click()
    page.locator('.stage-root [data-action="diagnose"]').wait_for()
    page.locator('.stage-root [data-diagnosis]').select_option("explanation")
    page.locator('.stage-root [data-field="why"]').fill("I must review the assumptions behind the model.")
    page.locator('.stage-root [data-action="diagnose"]').click()
    page.locator('.stage-root [data-field="repair"]').fill(
        "I now separate the valid physical intervals and justify the units.")
    page.locator('.stage-root [data-action="repair"]').click()
    page.locator('.stage-root [data-action="boundary"]').wait_for()
    option = next(x["expected"] for x in task["boundaryFields"] if x["id"] == "model")
    page.locator('.stage-root [data-field="model"]').select_option(label=option)
    page.locator('.stage-root [data-field="why"]').fill(
        "The changed condition requires an adjusted governing equation.")
    page.locator('.stage-root [data-action="boundary"]').click()
    page.locator('.stage-root .worked').wait_for()


@pytest.mark.parametrize("width,height", [(1000,1600),(1600,1000)])
def test_real_chromium_two_independent_six_stage_tasks_and_exact_return(
    open_page, fixture_data, width, height
):
    contract, src, route = fixture_data
    context, page, errors = open_page(width=width, height=height)
    try:
        wait_ready(page)
        assert page.locator("#nsejs-exact-source").inner_text().find("Authored Mechanics") >= 0
        assert page.locator("#nsejs-source-return").is_hidden()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4")
        assert page.locator(".guide svg").count() == 1
        assert page.locator(".guide input[type=range]").count() == 1
        save_prediction(page)
        save_attempt(page, contract["tasks"]["A"], "Task A first explanation: friction does work.")
        initial = page.evaluate("""id => {
           const key=Object.keys(localStorage).find(k=>k.endsWith(':'+id));
           return JSON.parse(localStorage.getItem(key)).first.answers.reason;
        }""", LESSON_ID)
        assert "Task A first explanation" in initial
        page.reload(wait_until="domcontentloaded")
        page.locator('.stage-root [data-action="reconstruct"]').wait_for()
        assert "Task A first explanation" in page.locator('.stage-root .snapshot').inner_text()
        finish_boundary(page,contract["tasks"]["A"])
        assert page.locator("#nsejs-source-return").is_hidden()
        page.locator('button[data-variant="T2"]').click()
        page.locator('.stage-root [data-action="prediction"]').wait_for()
        assert page.locator('.stage-root .worked').count() == 0
        save_prediction(page,"Task B independent prediction")
        page.locator('.stage-root [data-action="hint"]').click()
        save_attempt(page,contract["tasks"]["B"],"Task B model is different, and hints were exposed.")
        second = page.evaluate("""id => {
          const key=Object.keys(localStorage).find(k=>k.endsWith(':'+id+'-T2'));
          return JSON.parse(localStorage.getItem(key));
        }""", LESSON_ID)
        assert second["first"]["hintsUsed"] == 1
        assert second["first"]["answers"]["reason"] != initial
        assert second["exposure"] == "HELPED_BEFORE_FIRST_ATTEMPT"
        finish_boundary(page,contract["tasks"]["B"])
        page.locator("#nsejs-source-return:visible").wait_for()
        link = page.locator("#nsejs-source-return").get_attribute("href")
        assert route["source_id"] in link
        assert route["content_revision_sha256"] in link
        assert "source_uid=" in link and "source_revision=" in link
        assert not errors,errors
    finally:
        context.close()


@pytest.mark.parametrize("error_mode", ["bad_uid","bad_revision","missing_source","figure_tamper","storage_denied"])
def test_bad_source_storage_and_tampering_never_reveal_answers(
    open_page, fixture_data, error_mode
):
    contract, src, route = fixture_data
    options = {}
    if error_mode == "bad_uid": options["uid"] = "g9:PHYSICS:NONEXISTENT"
    if error_mode == "bad_revision": options["revision"] = "f" * 64
    if error_mode == "missing_source":
        changed = deepcopy(src)
        changed["questions"] = []
        options["changed_source"] = changed
    if error_mode == "figure_tamper":
        changed = deepcopy(src)
        changed["questions"][0]["source_figures"] = ["missing-original-figure.svg"]
        options["changed_source"] = changed
    if error_mode == "storage_denied": options["storage_denied"] = True
    context, page, errors = open_page(**options)
    try:
        page.locator("#nsejs-parity-status[data-state='HOLD']").wait_for(timeout=15000)
        assert page.locator('.stage-root [data-action="attempt"]').count() == 0
        assert page.locator('.stage-root .worked').count() == 0
        assert page.locator("#nsejs-source-return").is_hidden()
    finally:
        context.close()
