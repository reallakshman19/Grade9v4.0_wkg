# WPE Core2 — R2 engineering handoff (public-safe)

**Governing published WBS:** G9v3.5 **R6 / 4.3 / 4.3.2** (native Core2 fidelity). Historical coding origin: R5/4.2/4.2.1; this handoff aligns it to the newer active WBS. No second WBS created.

**State:** SELF_ASSESSED / SYNTHETIC_ONLY / PREPARED_NOT_TRANSFERRED / NO INDEPENDENT ACADEMIC ADMISSIONS. This ZIP does not contain actual R1 examination stems/options, reviewer proposals or protected source PDFs.

## Contents

- `src/` — standalone proposed admission, R1 projection, package and synthetic learner-rendering modules.
- `tests/` — 33 Python unit tests plus 26 Chromium interactions against synthetic HTML.
- `fixtures/synthetic_question.json` — invented trolley perpendicular-force test fixture; NOT an original exam item.
- `outputs/` — synthetic preview, HTML and browser assertion receipt.
- `HANDOFF_STATUS.json` and logs — current source WBS/PR96, test record, no admissions.

## Builder task — ONE bounded integration slice

1. On the exact current Grade9v3.5 source checkout, inspect `Shared/roles/CORE2.md`, `Shared/tools/core2_v2.py`, `Shared/tools/render_core.py`, `Shared/tools/web_blueprint_contract.py`, canonical package schema and existing product manifest; keep all native source/SL1/SL2 identities unchanged.
2. Reconcile the proposed `src/core2_engine.py` with existing native admission/rights/renderer contracts. Treat this as candidate code, not as an authorized replacement of the repo's implementation.
3. Produce ONE **synthetic-only** native golden fixture with the governed renderer; test missing official key, duplicate alias, D2 substitution, figure absence, disclosed reviewer exposure and stale adapter digest as negative cases.
4. Demonstrate attempt, ordered hints, solution gating, keyboard/mobile and strict quality tests on actual native output. Record runner versions and exact PR head; do not claim a live learner exercise from synthetic tests.
5. Return a source-bound PR/diff, regression results, academic/rights HOLDs, exact byte evidence, and a separate independent-QA request. Keep real WPE question 21/21 admission and Owner approval separate.

**Stop:** No mutation of original exam questions, native SL1/SL2, project coordination mode, approved adapter, admission or Owner acceptance. Distinct Physics review is still required. No agent has been appointed or begun this task by this ZIP.

## Run isolated candidate tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python tests/browser_test.py
PYTHONPATH=src python src/build_core2.py fixture --question fixtures/synthetic_question.json --out outputs/SYNTHETIC_CORE2_GOLDEN.html
```

Browser tests require the Playwright Python package and Chromium at `/usr/bin/chromium`. They run `set_content` only; native deployed browser, PDF, accessibility audit and security review remain NOT_RUN.

## Source and remote evidence

- Progress Page PR #96: https://github.com/reallakshman19/progress-page/pull/96 (merged, `c2235832566245452b29395b75ea4d0a4aeab4cd`)
- Public-safe R2 status: https://github.com/reallakshman19/CoordinatorLandingpage/issues/1#issuecomment-6521619329
- Independent academic research fixture review request (separate scope): https://github.com/reallakshman19/Grade9v3.5/issues/313

## Transport

This ZIP is **local for the Owner**, not yet a cross-agent delivery. Follow `Common/skills/agent-work/ARTIFACT_RELAY.md`: public-safe Common immutable payload first, or authorized private Drive; receiver must actually download, hash and inspect the permitted bytes. `sandbox:` alone is not transfer. No implicit `Cycle now`, no activated g9v35 Cycle, no merger or release authority.
