# Private reader integration — source-preserving technical harness

**Review-only infrastructure. SELF_REVIEW. No academic approval inferred from software validation.**

## Purpose and scope

The Python builder at tools/private_reader_integration.py reconstructs a private candidate review reader from recipient-verified local snapshots. It preserves original input bytes, checks original-to-aggregate question identity, collects available SVG assets from modules, withholds questions whose required figures are absent through the input reader's checked HOLD behavior, and creates deterministic private review output. It is not a Shared/Core2 source authority, Physics correctness evaluator, QRT approver, exam original authenticator, or publisher.

**This branch contains no private candidate question text, source paper images, answer keys, candidate figure bytes, or the generated private 50-record HTML.** The historical Physics handoff ZIP is separate private source custody. Its original producer Git ancestry is NOT VERIFIED; a ZIP hash is not a Git head. Do not commit the private manifest or generated HTML. The branch's Git ancestry is from the public Grade9 baseline, not from the missing producer head.

## Private execution

Given a private source directory and independent per-file hashes, prepare a local manifest outside the repository:

- version: 1
- review_only: true
- aggregate: path, sha256 (64 lowercase hex), count
- modules: entries with slug, topic, path, sha256, count
- expected_missing_figures: nonnegative integer, observed from source inventory

Illustrative synthetic manifest:

    {
      "version": 1,
      "review_only": true,
      "aggregate": {
        "path": "preview/question-status.html",
        "sha256": "<real 64-character digest>",
        "count": 4
      },
      "modules": [
        {
          "slug": "synthetic-module",
          "topic": "SYNTHETIC_TOPIC",
          "path": "modules/synthetic-module/question-status.html",
          "sha256": "<real 64-character digest>",
          "count": 4
        }
      ],
      "expected_missing_figures": 0
    }

Run:

    python tools/private_reader_integration.py \
      --root /path/to/private-candidate \
      --manifest /path/to/private-manifest.json \
      --out /path/to/private-review-output

The output must be outside the source tree, and an existing output must carry the builder's marker. Release is always forbidden: --publish fails closed. Private review output must never be copied into a public site merely because technical tests pass.

## Public CI

Run:

    python -m pytest -q tests/test_private_reader_integration.py
    python -m playwright install chromium
    python tools/check_private_reader_http.py

The test fixture generates *synthetic* questions, including reused historical display IDs, one candidate SVG and an unavailable required figure. Python checks include source mutation, re-pinned semantic conflict, asset collision, unsafe SVG, output ownership, source traversal, inventory mutation, deterministic rebuild and attempted public publication.

The browser test serves generated synthetic pages over real HTTP, requires browser page.goto to succeed at desktop/mobile sizes, checks figure/HOLD states, scoped attempt separation and the directory links. It deliberately has no DOM-only fallback. The workflow never packages private content.

## 12.7-inch reader display target

The presentation-only stylesheet `tools/private_reader_12p7.css` is included in every generated private review question page by the deterministic builder. Primary viewport contracts are 1280×800 and 1472×920 CSS pixels (landscape 16:10 scaling); 800×1280 tests full-size portrait tablet behavior. These are representative CSS viewports, not a claim about the exact device's native resolution. The portrait question picker is bounded and scrollable so the first question is visible without scrolling through all 50 navigation items. The original question/answer/figure payload is unchanged. Smartphone HTTP coverage is not required for this task, and its absence must not be described as a mobile PASS.

## R6 learner-state integration (private-review only)

`tools/private_reader_r6.py` implements optional, fail-closed revision-scoped
local practice storage and explicit disambiguation of repeated legacy IDs.
Run `private_reader_integration.py --r6` to apply the patch during a private
build. It rejects incompatible templates rather than silently retaining
the old attempt handling. No private candidate material is committed.

The public CI additionally checks synthetic question/figure revisions and runs
the R6 localStorage contract against a served HTTP origin on 12.7-inch
landscape/tablet viewports. This test does not establish private candidate
HTTP acceptance or secure examination-grade first attempts.

**These synthetic CI tests do not qualify the private 50-record candidate's HTTP browser execution.** That still needs a separately authorized private runner, with a verified recipient source manifest, real Chromium over HTTP, original question-to-output reconciliation and observed saved-state/deep-link behavior.

## Approval boundaries

- Candidate module/source bytes: private and independently verified in separate receipts, not uploaded here.
- Original exam authenticity: UNKNOWN_SOURCE.
- Scientific and answer-key review: HOLD.
- Shared/SL1/SL2/QRT qualification: HOLD.
- Merge and GitHub Pages deployment: NOT_AUTHORIZED.

A distinct reviewer must test the actual new Git commit before acceptance. The existing three-subject navigation and WPE modules are unchanged.

No academic approval inferred from software validation.
