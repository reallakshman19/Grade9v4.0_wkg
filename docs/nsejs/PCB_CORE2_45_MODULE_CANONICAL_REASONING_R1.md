# NSEJS PCB Core2 R1 — Canonical question identity and reasoning map

Task: `G9V4-NSEJS-PCB-CORE2-45-CANONICAL-QRT-MAP-R1`  
Scope: Physics, Chemistry, Biology only. Mathematics excluded.  
Mode: `OWNER_ZIP_BYTES_VERIFIED · SOURCE_NEUTRAL_PUBLIC_METADATA · QRT_NOT_RUN · ACADEMIC_HOLD`

## Owner source and source-neutral snapshot

Owner ZIP: `G9V4_ALL_CORE2_QA_BANKS_20261113.zip`  
Archive SHA-256: `f590bb80577143eb4a31c3fb8e58599ef722a624cdbde5774b88405f89f2ce51`

Independent private ZIP audit: **210 members, 208/208 manifest-listed file sizes + SHA-256 MATCH**. Its 47 banks include two Mathematics modules deliberately excluded from this task.

The public `nsejs/data/pcb-core2-identity-map.v1.json` has **45/45 PCB modules and 267/267 question occurrences**, identified with module-scoped UIDs of the form `g9:pcb:<subject>:<module-slug>:<ordinal>`. Each entry retains an SHA-256 over the **entire private question JSON value**, including data withheld from public Git. A separate SHA-256 of its parent bank binds bank-level bytes. The public map contains no original exam stems, choices, figures, keys, worked solutions or confidential source records.

| Subject | Modules | Question occurrences |
|---|---:|---:|
| Physics | 21 | 95 |
| Chemistry | 13 | 87 |
| Biology | 11 | 85 |
| **Total** | **45** | **267** |

External source labels are **not** canonical unique keys. There are **263 distinct labels**, and these four labels are shared between different question bytes:

- `NSEJS-2024-B-Q50`
- `CHEM-NSEJS-ATOM-01`
- `NSEJS-2024-C-Q55`
- `NSEJS-2024-P-Q46`

All eight affected occurrences remain separate and explicitly flagged, not silently deduplicated. The owner must determine whether they are variants, source-alias errors or unrelated candidates.

## Proposed question-to-reasoning map

Each question entry records `proposed_qrt_operation`, `proposed_crux_ref`, `proposed_crux_kind`, unresolved figure/key/source/rights states, and independently established reasoning/learning readiness. The proposals originate from the Owner ZIP, **not** an independent reviewer. **Five** records disagree between proposed operation and crux-kind. **Thirteen** entries refer to figures without independently verified original figure bytes.

| Construction fit | Occurrences | Meaning |
|---|---:|---|
| `RELATED_ONLY_UNVERIFIED` | 26 | A matching module/topic has authored practice: 8 existing Core1 authored previews and 18 separately authored supplemental skill journeys. Topic-level similarity only — **not** B1–B7 teaching sufficiency |
| `MISSING_CONSTRUCTION` | 241 | No exact/task-matched published Core1A/B construction established from the available code and archive |
| Independently qualified exact learner return | **0** | No native authenticated exact question → sufficient teaching → fresh practice → same source return accepted |
| **Total** | **267** | Every row accounted for |

Of the missing 241, 237 correspond to historical 2020–2024 module rows and four are standalone topical questions without a directly matching authored-preview module. Do not replace a missing exact-source route with a generic skill URL.

## Code and source requirements

- `tools/nsejs_pcb_identity_map.py`: validates complete 45/267 public metadata against hard-coded governance and a complete canonical SHA-256 of the source-neutral owner reconciliation. It checks subject membership, UID/ordinal collisions, 4 duplicate aliases, 5 QRT conflicts, 13 figure holds, 26/241 fit categories, current eight authored previews and 18 standalone supplemental source catalogs. Stages `nsejs/core2/question-map.html` and `question-map.v1.json` with no original question content.
- `tools/reconcile_pcb_core2_owner_zip.py`: **private checkout only**. Rechecks the pinned ZIP SHA-256 and full member manifest, recomputes per-question SHA-256 from actual private question values and compares all 267 identities and parent bank bytes with the source-neutral checked-in map. **Its PASS is only a byte/metadata receipt**.
- `tests/test_nsejs_pcb_identity_map.py`: synthetic-negative academic/source/identity/rights tests and exact 45/267 completeness. No actual examination stems in test files.
- `tools/check_nsejs_core2_catalog_http.py`: real staged HTTP Chromium tests at 12.7-inch portrait/landscape check the new 267-ID question-level map, module sections, 26 related-only routes, no iframes and visible HOLDs.

Private replay:

```sh
python tools/reconcile_pcb_core2_owner_zip.py \
  --zip /private/G9V4_ALL_CORE2_QA_BANKS_20261113.zip \
  --root /private/Grade9v4.0 \
  --report /private/pcb-core2-identity-replay.json
```

No ZIP is uploaded to GitHub Actions or GitHub Pages. The source-free public registry is independently reproducible from a securely held Owner archive.

## Academic/engineering follow-up

1. **Source identity and rights:** obtain official paper/code/language/edition and full stem/figure/key custody for each candidate; reconcile repeated external labels individually. Unavailable or contradicted source claims remain HOLD.
2. **Independent QRT:** after a separate authorized reviewer receives source-only material *before author guidebook exposure*, resolve the five proposed operation/crux discrepancies and the exact missing learner-owned inference. Do not turn producer labels or score bands into QRT approvals.
3. **Construction and B1–B7:** establish evidence of target operation, sufficient Core1A model teaching, truly independent Core1B task, saved first attempts, diagnosis/repair, transfer and source return. Reclassify the current 26 related-only suggestions only with actual per-question review.
4. **Regression/release:** run all unfiltered Python QA plus real browser tests on exact candidate head. Technical preview may be staged without promoting original exams, rights or academic status. Full QA previously has missing private source and SL/Core1 outputs; retain those failures until actual evidence is restored.

**Explicit distinction:** 45 module names and 267 question identities can be technically *indexed* while 45/45 complete uploaded original Core2 banks remain **unpublished**. No claim of 267 admitted exam items, 267 completed lessons, qualified mastery, or full Python QA PASS is permitted.
