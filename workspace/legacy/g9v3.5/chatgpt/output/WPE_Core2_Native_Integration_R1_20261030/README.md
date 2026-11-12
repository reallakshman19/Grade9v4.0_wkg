# WPE-CORE2-NATIVE-INTEGRATION-R1

PRIVATE / SOURCE-BEARING / AUTHOR ENGINEERING CANDIDATE. Start with index.html. Open rendered/core2.html for 8 textbooks + 1 synthetic control; synthetic-rendered/core2.html is the strict control. The original textbook reader is retained under textbook-baseline/. No examination admission or independent QA is claimed.

## Rebuild in this Windows environment

Python with jsonschema and the pinned C:/CodeC/Grade9v3.5 runtime is required. No installation is included. Set PYTHONDONTWRITEBYTECODE=1 or use -B. From implementation/:

    python -B prepare_candidate.py
    python -B C:/CodeC/Grade9v3.5/Shared/tools/render_core.py build --manifest ../native/manifest.json --out ../rendered --draft --reference
    python -B C:/CodeC/Grade9v3.5/Shared/tools/render_core.py build --manifest ../native/synthetic-manifest.json --out ../synthetic-rendered --reference
    python -B test_integration.py
    python -B verify_builds.py

Run prepare_candidate.py without --retain for an already retained candidate. --retain reacquires the hash-checked original archives/baseline and is intended only for a new candidate. prepare_candidate.py rewrites candidate manifests and synthetic bindings intentionally; do not run it over a reviewed freeze without recording new hashes.

Browser protocol: serve this candidate only on loopback; use an isolated Playwright CLI Chrome session and implementation/browser_checks.js. It expects http://127.0.0.1:8785, saves screenshots to this original candidate path, and returns JSON. Adapt root/screenshot paths explicitly when moving the harness. It does not publish or contact chat agents. Stop the server and close only this task browser after checks.

## Distinct QA handoff

Read CONCEPT_NOTE.md, review/NATIVE_MAPPING.json, PRESERVATION_PINS.json, INTEGRATION_TESTS.json, BUILD_CONTROLS.json, BROWSER_CHECKS.json and both native render receipts. Replay the explicit failures. Check the eight-question bank byte identity; the only pre-existing package-field changes are title and representation asset paths, plus one appended synthetic representation. Confirm no real EX-* question enters the native selection.

The received 33-test engine is preserved under received-engineering/. Its synthetic fake witnesses prove structure only. Do not convert metadata eligibility into admission. Received original browser_test.py has a documented substring-oracle defect and Linux-specific browser path; current browser_checks.js supplies the corrected exact predicate and actual URL/keyboard checks. Do not claim the unchanged original browser script was rerun.

14 examination leads / 7 vacancies / 0 admissions. Owner review of engineering scope does not approve the complete Core2 product or waive Core1A/Core1B gates. D3.1 paused. Original worktree custody/cleanliness is not asserted; all product edits are confined to this separate local candidate.
