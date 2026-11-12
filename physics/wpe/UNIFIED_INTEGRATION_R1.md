# Unified WPE Learn → Challenge integration R1

## Source and branch custody

Base: `main` at `e4429372dba6bc10ce63892c87ccbcdc78deca3c`, after merged PRs #26, #52 and #56. This branch does not reopen them. PR #55 remains **read-only**: its E06, E07 and E08 author-written *challenge definitions only* have been adapted into optional F01, F02 and F03 transfer variants.

| Existing lesson and first variant | Donor from PR #55 | Optional transfer model |
| --- | --- | --- |
| F01 · 3 kg cable, 54 N, 0.80 m | E06 challenge | 4 kg toy, 0.50 m contact and 0.80 m further flight; applied force 104 N, applied mechanical power 416 W |
| F02 · 37° ramp, 18 J up and 2 J back | E07 challenge | 45° incline with return speed 2v₀/3, kinetic coefficient μ = 5/13 |
| F03 · k=80 N/m, xᵢ=+0.05 m, new force −12 N | E08 challenge | k=50 N/m, xᵢ=−0.20 m, new force +15 N, new equilibrium +0.30 m and other turn +0.80 m |

The donor text, response fields, progressive hints, worked reconstruction, misconceptions, feedback and changed-condition challenges are encoded in `physics/wpe/focused-transfer-challenges.js`. The `focused-journeys.js` renderer and source-specific F Core1A conceptual explanations are retained; the E06–E08 pages, candidate register updates and source-pins from the divergent donor branch are **not merged**. Original 74-question coverage counts remain 3 focused / 18 targeted / 48 related / 5 missing. No source identity, stem, options, figure or answer key is rewritten. The pre-existing EX-M97 safeguard explicitly distinguishes applied toy/cable power at a moving force application point from the unverified real human-muscle interpretation: ground reaction × centre-of-mass speed is not automatically muscular power.

## Routes, local practice and trust boundaries

The chapter landing page offers one Learn → Challenge gateway, original Question Bank and Practice my skills. The gateway offers question-bound routing only after checking the original source ID, SHA-256 stem digest and existing `learning-coverage-r1.json` mapping. The 41 legacy `study-bridge.html` related practice links safely redirect or link **directly** to the existing C/E/F page. No iframe or duplicated content router is introduced. Unknown question IDs and unknown lesson pairings fail closed. All original direct lesson anchors remain functional.

Question Bank selections, written drafts, paper attempts and frozen first committed responses are stored under `g9:wpe:core2:attempt:v1:<source_id>`, linked to the immutable source stem hash. The author answer is never revealed automatically on reload, even if it was deliberately revealed before. `Resume`, `Start again` and `Clear saved practice` explicitly control local state with confirmation for destructive resets. The first F attempt retains its original `g9:wpe:focused:v1:<lesson>` key. Optional transfers use `g9:wpe:focused:v1:<lesson>:transfer` and cannot overwrite it. All existing five-foundation, C and E lesson keys remain unchanged. `g9:wpe:journey:v1` is only a locally stored resume pointer.

Browser local storage is not encrypted/secure, identities cannot be independently attested, static answer code can be inspected, and no semantic grading or academic admission is claimed.

## Validation and limitations

`tests/test_wpe_unified_integration_r1.py` independently checks source custody, no iframe elements, new versus old state keys and the two mathematical models and boundary variations of each transfer problem. `tools/wpe_unified_integration_r1_ui.py` uses real Chromium at 1280×800 and 390×844 to test EX-M79 → C03 → EX-M79, original drafts across navigation/reload, first-attempt freezing, gated solutions, progressive hints, misconception repair, changed physical conditions, independent transfer state, source return and reset. Existing Python and C/E/F/mini-lesson Chromium regressions run in the integration workflow.

These are software and numerical correctness checks, **not evidence of genuine student comprehension**. Direct observation of at least one unfamiliar challenge solved by a real student *without seeing its worked reconstruction first* remains a manual, consent-appropriate educational evaluation required before asserting a successful learning outcome. No QRT, adapter, Owner or academic approval is claimed.

Once this PR has merged and the three transfer variants are verified, propose closing **PR #55 as superseded by the integration PR**. Do not merge or close the donor prematurely. The separate five-missing-construction effort remains out of scope.
