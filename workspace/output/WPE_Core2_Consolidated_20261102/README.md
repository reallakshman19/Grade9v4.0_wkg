# Core-2 — WPE consolidated review candidate

**Date:** 2026-11-02. **Role:** CORE2 (source question custody). **Status:** NOT_ADMITTED.

## Deployment and architecture
- Public review rendering: `preview/question-status.html` (Core-2).
- Former metadata-only status tracker: `preview/question-status-archive.html`, retained for historical continuity.
- Candidate source question projection: `native-candidate/selected_bank.review.json` (NOT a certified Shared native bank.json).
- Derived SVG diagrams: `native-candidate/assets.review.json`; these are candidate author/reference representations, not official-figure-certified.
- Review receipts: `review/dedup_decisions.json`, `review/audit_flags.csv`, `review/build_checks.json`, and `MANIFEST.review.json`.

## Counts and duplicates
70 uploaded source master records were reconciled with the linked R1/R2/R3/native readers. Five duplicate or near-equivalent displays were suppressed, not deleted from original custody: EX-M4, EX-M29, EX-M64, EX-M120, EX-M84. The displayed bank is **65 selected master entries + 8 textbook entries = 73 source-backed display entries**, plus one separately marked synthetic control. This is NOT 73 verified examination originals. WEP07-03 / NSEP Q57 occurs once with multiple selection. Proposed D2/D4 classification conflict remains unreviewed.

## Custody and authority
The selected bank uses custom schema `wpe-core2-consolidated-review-v1`; it is not validated against native Shared Core2. The original Owner-provided package and excluded original records remain in the supplied archive. Suppressing a display never proves two distinct exam identities are the same.

Original exam/question source and keys, diagrams, rights, independent scientific and QRT review, subject adapter and learner release remain unresolved. Public webpage placement is an engineering review action, not academic admission or student-release approval. Answers are embedded in the local HTML; attempt flow is not cryptographic answer secrecy.

## Input provenance
- Owner-supplied master package SHA-256 `fe7e29e1463c92dcde795155826308c945f9abdff08b930655c7ea82647c3fc8`.
- R3 reader blob `fa8bed33593bfc1a33997285173bfc635f6dfb3e`; R2 `8d21dd069b6161da5ba8e912236520aa4916dc82`; R1 corrected `2e8f1b39c756241289915c102fddd6f2becdca9a`.
- Native textbook-bank reference blob `5cb2a9ca070fb7410835d6a9c40c18ad7c78f2be`.

## Promotion conditions
Independently verify each source/question/key/figure/rights item and QRT demand where claimed, resolve scientific holds, qualify subject adapter/native schema and the learner runtime, and require explicit Owner release approval. Do not infer academic qualification from a successful render.
