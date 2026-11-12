# WPE Phase 2 · Exact-question reasoning route · 2 Nov 2026

**Owner directive:** “proceed after all integration, check status and take over.” This is the site-integration takeover of already-authored WPE D3/D4 construction materials. Existing author packs are **not** rewritten.

**Source base:** `727c6f8758c31c34aa44af47f24477799ad5b107`; reconciled with E05 main commit `a90c34cffed8f108413973a5b12c25ecf09c8ca7`. Exact Git blob pins are embedded in `reasoning-paths.review.json` for the author bridge, consolidated reader, 21-place pilot and foundation source map.

## Actual implementation

- **13 proposed reasoning themes**: eight C01–C08 constructions and five E01–E05 extensions. **13 author-drafted guided/fresh pairs** present in the reconciled source package, with E05 now authored; **zero** qualified Core1A/Core1B learner destinations.
- A **read-only route index** `reasoning-paths.html` shows provisional source-theme links and existing five foundational lesson anchors where separately named in the source bridge. It never links to or embeds author-only Markdown worked references.
- The existing `preview/question-status.html` recognizes `?question=SOURCE_ID` only by exact comparison to its embedded 74-entry candidate bank. Other navigation updates the URL without changing a source question or answer. Unknown values cannot create phantom records.
- The Question Bank now offers a clearly **review-only** topic-route link, even for questions without a proposed mapping. The index explicitly reports missing associations, source records absent from the bank and unqualified routes.
- From a mapped foundation demonstration at `learn-challenge.html?question=SOURCE_ID#existing-anchor`, the learner can return to the **same** source candidate in the full-width Question Bank. Neither academic admission nor independent mastery is inferred.
- A minimal WPE chapter-hub link exposes the route preview without replacing the five working learner surfaces.

## Scientific and governance boundaries

- All 74 original stems, options, figure references, embedded question JSON, source `hints[]`, author answers and answer-reveal state machine remain byte-for-byte unchanged in this PR.
- Eight pilot operation/band disagreements remain open, three proposed IDs are absent from the reader, and seven pilot selection slots are vacant. All source candidates remain `NOT_ADMITTED`.
- C01–C08 and E01–E05 are **author proposal drafts**; all 13 remain NOT_ACCEPTED. `primary_capability_ref` and `prerequisite_microtopic_refs` remain missing; do not invent canonical joins.
- The five already-public foundation demonstrations remain technical candidates with their existing JS keys, not secure independent assessment. The eight plus five authored pack answers are **not published in this new route**.
- `question-bank.html` retains its full-width redirect, forwarding `?question=` to the reader.
- Open [PR #26](https://github.com/reallakshman19/Grade9v4.0/pull/26) also changes `preview/question-status.html`; it must be explicitly reconciled with this URL-only navigation patch before either is merged over the other. No silent overwrite.

## Required evidence

- `python -m pytest -q` to check source SHA pins, counts, nonadmission, exact embedded bank parity, unmapped/absent behavior and 13-route proposal integrity.
- `python tools/wpe_learn_challenge_ui.py` to check desktop and mobile: EX-M79 question → C03 provisional association → `#energy-motion` foundation → return EX-M79; invalid ID refusal; missing EX-M81 link refusal; WEP07-03 mapped to E01 **without** inventing a foundation link; and no answer reveal before attempt.
- Existing Preview UI QA covers general mobile and original spring-practice behavior.
- **CI outcomes NOT_RUN until GitHub actions report exact-head results; independent non-author review NOT_RUN.**

**No academic approval inferred from software validation. No learner release.**
