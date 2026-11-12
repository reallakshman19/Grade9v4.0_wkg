"""Joint Wave 2 HTTP Chromium proof using ACTUAL authored Mechanics lesson data.

No stubs for the lesson, original source or WPE engine. This is a technical
integration witness, not independent academic approval or observed mastery.
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
DATA = json.loads((ROOT / "nsejs/data/mechanics-wpe-teaching-pilot.v1.json")
                  .read_text("utf-8"))
UID = DATA["source"]["question_uid"]
REV = DATA["source"]["content_revision_sha256"]
ID = DATA["lesson"]["id"]


@pytest.fixture(scope="module")
def server():
    srv = ThreadingHTTPServer(("127.0.0.1", 0),
        partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
    Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield "http://127.0.0.1:" + str(srv.server_port)
    finally:
        srv.shutdown()
        srv.server_close()


def page_path(server):
    return (server + "/nsejs/physics/learn-mechanics.html?source_uid=" +
            quote(UID, safe="") + "&source_revision=" + quote(REV, safe=""))


def committed_record(page, suffix=""):
    return page.evaluate("""(o) => {
        const key = Object.keys(localStorage).find(k =>
          k.startsWith('g9:nsejs:wpe-parity:v1:') &&
          k.endsWith(':' + o.lesson + o.suffix));
        return key ? {key,record:JSON.parse(localStorage.getItem(key))}:null;
    }""", {"lesson":ID,"suffix":suffix})


def begin(page):
    page.locator("#nsejs-parity-status[data-state='PREVIEW']").wait_for(timeout=15000)
    page.locator('.stage-root [data-action="prediction"]').wait_for(timeout=15000)
    assert "academic HOLD" in page.locator("#nsejs-parity-status").inner_text()


def attempt(page, task, reason, *, help_first=False):
    page.locator('.stage-root [data-field="prediction"]').fill(
        "Predict from collision conditions and the later friction phase.")
    page.locator('.stage-root [data-action="prediction"]').click()
    page.locator('.stage-root [data-action="attempt"]').wait_for()
    if help_first:
        page.locator('.stage-root [data-action="hint"]').click()
    for field in task["fields"]:
        target = page.locator('.stage-root [data-field="' + field["id"] + '"]')
        if field["type"] == "select":
            target.select_option(label=field["expected"])
        elif field["type"] == "number":
            target.fill(str(field["expected"]))
        elif field["type"] == "textarea":
            target.fill(reason)
    assert page.locator('.stage-root .worked').count() == 0
    page.locator('.stage-root [data-action="attempt"]').click()
    page.locator('.stage-root [data-action="reconstruct"]').wait_for()
    assert page.locator('.stage-root .snapshot').count() == 1


def boundary(page, task):
    page.locator('.stage-root [data-action="reconstruct"]').click()
    page.locator('.stage-root [data-action="diagnose"]').wait_for()
    page.locator('.stage-root [data-diagnosis]').select_option("explanation")
    page.locator('.stage-root [data-field="why"]').fill(
        "Check which conservation statement applies to each physical interval.")
    page.locator('.stage-root [data-action="diagnose"]').click()
    page.locator('.stage-root [data-field="repair"]').fill(
        "My corrected method chooses the collision system first and computes separate braking work.")
    page.locator('.stage-root [data-action="repair"]').click()
    page.locator('.stage-root [data-action="boundary"]').wait_for()
    for field in task["boundaryFields"]:
        target = page.locator('.stage-root [data-field="' + field["id"] + '"]')
        if field["type"] == "select":
            target.select_option(label=field["expected"])
        elif field["type"] == "number":
            target.fill(str(field["expected"]))
        else:
            target.fill("The changed assumption requires a new model check, not a copied answer.")
    page.locator('.stage-root [data-action="boundary"]').click()
    page.locator('.stage-root .worked').wait_for()


@pytest.mark.parametrize("width,height", [(1000,1600),(1600,1000)])
def test_actual_authored_core1a_then_two_core1b_tasks_full_six_stages(
    server, width, height
):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width":width,"height":height},
                                      has_touch=True,is_mobile=True)
        page = context.new_page()
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        try:
            response=page.goto(page_path(server), wait_until="domcontentloaded",timeout=30000)
            assert response.status == 200
            begin(page)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 4"), (width,height)
            assert "3.2 m" in page.locator(".model-readout").inner_text()
            slider=page.locator(".guide input[type=range]")
            assert slider.count() == 1
            assert slider.evaluate("(el)=>el.getBoundingClientRect().height") >= 56
            slider.evaluate("""el => {
              el.value = '0.50'; el.dispatchEvent(new Event('input',{bubbles:true}));
            }""")
            assert "1.6 m" in page.locator(".model-readout").inner_text()
            assert page.locator("#nsejs-source-return").is_hidden()
            assert page.locator(".stage-root .worked").count()==0
            # Task A: inelastic, momentum, collision loss, friction, boundary μ=0
            attempt(page, DATA["tasks"]["A"],
                    "Task A: short impact momentum, 12 J inelastic loss, later 6 N friction.")
            record_a = committed_record(page)
            assert record_a is not None
            assert record_a["record"]["first"]["answers"]["reason"].startswith("Task A:")
            assert record_a["record"]["first"]["hintsUsed"] == 0
            page.reload(wait_until="domcontentloaded")
            page.locator('.stage-root [data-action="reconstruct"]').wait_for()
            assert "12 J inelastic loss" in page.locator('.stage-root .snapshot').inner_text()
            boundary(page, DATA["tasks"]["A"])
            assert page.locator("#nsejs-source-return").is_hidden()
            # Task B differs in model: equal-mass ELASTIC contact then inverse μ.
            page.locator('button[data-variant="T2"]').click()
            page.locator('.stage-root [data-action="prediction"]').wait_for()
            assert page.locator('.stage-root .worked').count()==0
            attempt(page, DATA["tasks"]["B"],
                    "Task B: elastic velocity exchange, then solve friction coefficient from stop distance.",
                    help_first=True)
            record_b = committed_record(page,"-T2")
            assert record_b is not None
            assert record_b["key"] != record_a["key"]
            assert record_b["record"]["first"]["hintsUsed"] == 1
            assert record_b["record"]["exposure"] == "HELPED_BEFORE_FIRST_ATTEMPT"
            assert committed_record(page)["record"]["first"] == record_a["record"]["first"]
            assert "do not grade explanations" in page.locator('.stage-root .assessment').inner_text().lower()
            assert "Your original explanation" in page.locator('.stage-root .snapshot').inner_text()
            boundary(page, DATA["tasks"]["B"])
            page.locator("#nsejs-source-return:visible").wait_for(timeout=15000)
            href=page.locator("#nsejs-source-return").get_attribute("href")
            assert "source_uid=" in href and quote(UID,safe="") in href
            assert REV in href and "question-G9-AUTH-MECH-001" in href
            page.reload(wait_until="domcontentloaded")
            page.locator("#nsejs-source-return:visible").wait_for(timeout=15000)
            assert not errors,errors
        finally:
            context.close()
            browser.close()


@pytest.mark.parametrize("case", ["missing_query","changed_question_revision",
                                   "corrupt_source_stem","tampered_task_id","storage_denial"])
def test_real_data_rejects_bad_identity_tampering_and_storage(server,case):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx=browser.new_context(viewport={"width":1000,"height":1600},has_touch=True,is_mobile=True)
        if case=="storage_denial":
            ctx.add_init_script("Storage.prototype.setItem=function(){throw new Error('DENIED')};")
        page=ctx.new_page()
        if case=="corrupt_source_stem":
            altered=json.loads((ROOT/"nsejs/data/physics-authored-practice-r1.json").read_text("utf-8"))
            altered["questions"][0]["stem"] += " tampered"
            page.route("**/nsejs/data/physics-authored-practice-r1.json",
                lambda request:request.fulfill(status=200,content_type="application/json",
                  body=json.dumps(altered)))
        if case=="tampered_task_id":
            altered=deepcopy(DATA)
            altered["tasks"]["B"]["id"]=altered["tasks"]["A"]["id"]
            page.route("**/nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
                lambda request:request.fulfill(status=200,content_type="application/json",
                  body=json.dumps(altered)))
        url=page_path(server)
        if case=="missing_query":url=server+"/nsejs/physics/learn-mechanics.html"
        if case=="changed_question_revision":url=url.replace(REV,"e"*64)
        try:
            page.goto(url,wait_until="domcontentloaded",timeout=30000)
            page.locator("#nsejs-parity-status[data-state='HOLD']").wait_for(timeout=15000)
            assert page.locator('.stage-root [data-action="attempt"]').count()==0
            assert page.locator("#nsejs-source-return").is_hidden()
        finally:
            ctx.close();browser.close()


def test_full_lesson_text_change_isolates_attempt_history(server):
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        ctx=browser.new_context(viewport={"width":1000,"height":1600})
        page=ctx.new_page()
        try:
            page.goto(page_path(server),wait_until="domcontentloaded")
            begin(page)
            attempt(page, DATA["tasks"]["A"],"Earlier committed practice must remain isolated.")
            prior=committed_record(page)
            assert prior and prior["record"]["stage"]==2
            edited=deepcopy(DATA)
            edited["tasks"]["A"]["challenge"] += " This instructional text was revised."
            page.route("**/nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
                lambda request:request.fulfill(status=200,content_type="application/json",
                  body=json.dumps(edited)))
            page.reload(wait_until="domcontentloaded")
            begin(page)
            assert page.locator('.stage-root [data-action="reconstruct"]').count()==0
            assert page.locator('.stage-root .snapshot').count()==0
            current=committed_record(page)
            assert current["key"] == prior["key"]  # old entry remains as history
            assert page.evaluate("Object.keys(localStorage).length")>=1
        finally:
            ctx.close();browser.close()


@pytest.mark.parametrize("phase", ["first_attempt", "boundary_attempt"])
def test_quota_rejects_real_payload_before_any_solution_reveal(server, phase):
    """A tiny storage probe can pass when real first/boundary record exceeds quota.

    WPE itself renders stage transitions after persist() fails. The adapter must
    precommit the full record, verify readback and stop the click on failure.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width":1000, "height":1600},
                                  has_touch=True, is_mobile=True)
        ctx.add_init_script("""() => {
          window.__blockActualAttempt = false;
          window.__blockActualBoundary = false;
          const original = Storage.prototype.setItem;
          Storage.prototype.setItem = function(key, value) {
            const scoped = String(key).startsWith('g9:nsejs:wpe-parity:v1:');
            const first = String(value).includes('"first":{');
            const boundary = String(value).includes('"boundary":{');
            if (scoped && ((window.__blockActualAttempt && first) ||
                           (window.__blockActualBoundary && boundary))) {
              throw new DOMException('Simulated attempt-key quota failure',
                                     'QuotaExceededError');
            }
            return original.call(this, key, value);
          };
        }""")
        page = ctx.new_page()
        try:
            page.goto(page_path(server), wait_until="domcontentloaded", timeout=30000)
            begin(page)
            if phase == "first_attempt":
                page.locator('.stage-root [data-field="prediction"]').fill(
                    "Separate collision momentum and later friction work.")
                page.locator('.stage-root [data-action="prediction"]').click()
                page.locator('.stage-root [data-action="attempt"]').wait_for()
                page.locator('.stage-root [data-field="model"]').select_option(
                    label=DATA["tasks"]["A"]["fields"][0]["expected"])
                page.locator('.stage-root [data-field="reason"]').fill(
                    "This is a meaningful attempted physical explanation.")
                # The small probe will still work; only the actual record fails.
                assert page.evaluate("""() => {
                  localStorage.setItem('g9:nsejs:wpe-storage-probe','ok');
                  return localStorage.getItem('g9:nsejs:wpe-storage-probe')==='ok';
                }""")
                page.evaluate("window.__blockActualAttempt = true")
                page.locator('.stage-root [data-action="attempt"]').click()
            else:
                attempt(page, DATA["tasks"]["A"],
                        "Before boundary, save the actual independent explanation.")
                page.locator('.stage-root [data-action="reconstruct"]').click()
                page.locator('.stage-root [data-diagnosis]').select_option("explanation")
                page.locator('.stage-root [data-field="why"]').fill(
                    "The first divergence was the conservation law.")
                page.locator('.stage-root [data-action="diagnose"]').click()
                page.locator('.stage-root [data-field="repair"]').fill(
                    "Use momentum at impact, friction after the impact.")
                page.locator('.stage-root [data-action="repair"]').click()
                page.locator('.stage-root [data-action="boundary"]').wait_for()
                for field in DATA["tasks"]["A"]["boundaryFields"]:
                    target = page.locator('.stage-root [data-field="'+field["id"]+'"]')
                    if field["type"] == "select":
                        target.select_option(label=field["expected"])
                    elif field["type"] == "number":
                        target.fill(str(field["expected"]))
                    else:
                        target.fill("The limiting case changes stopping behavior.")
                page.evaluate("window.__blockActualBoundary = true")
                page.locator('.stage-root [data-action="boundary"]').click()
            page.locator("#nsejs-parity-status[data-state='HOLD']").wait_for(timeout=10000)
            assert "ACTUAL_ATTEMPT_NOT_DURABLY_SAVED" in page.locator(
                "#nsejs-parity-status").inner_text()
            assert page.locator('.stage-root .worked').count() == 0
            assert page.locator("#nsejs-source-return").is_hidden()
            record = committed_record(page)
            assert record is not None
            if phase == "first_attempt":
                assert record["record"]["stage"] == 1
                assert record["record"]["first"] is None
            else:
                assert record["record"]["stage"] == 5
                assert record["record"]["boundary"] is None
        finally:
            ctx.close()
            browser.close()
