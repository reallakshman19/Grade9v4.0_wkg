# NSEJS Physics Core2 R3 — Source, hash and QRT reconciliation

**Base:** PR #80 / `feat/multi-subject-core2-expansion-01`, before this change: `1443c339744af8e9e7b392da4ac07ca271afd55f`.

**Scope:** Core2/common question integrity only. Agent B remains owner of Core1A/B and B1–B7 reconstruction. This corrective work is CONTRIBUTOR/SELF_REVIEW; no independent academic acceptance is asserted.

## Decision ledger

| Aspect | Checked facts | Corrective behavior |
|---|---|---|
| Displayed Physics source inventory | 50 legacy source-claimed candidates | Historical `id` and `source_id` preserved; no copies or loss |
| Declared producer stem digests | 48 inconsistent, 2 consistent with displayed text | Preserve declared bytes separately; recompute observed SHA-256 and full question revisions in the committed integrity ledger |
| Machine integrity | Derived integrity ledger from canonical JSON + evidence JSON | Deterministic Python `--check`; browser checks both file SHA-256 digests plus each visible stem/revision, fails closed on tampering |
| Official paper/key cross-check | 11 source occurrences have paper locator and answer letter cross-checked against official IAPT source | Record a bounded locator/key status only; exact stem, options, diagram and republication rights remain HOLD |
| Incorrect official 2024 IDs | Two: 2024 Q1 / Q2 are Biology, not the candidate optics items | Mark both `OFFICIAL_ID_CONTRADICTED`; do not present as authenticated originals or erase old aliases |
| Remaining original-source claims | 37 of 50 have no independent source admission evidence in this workstream | `UNVERIFIED_SOURCE_CLAIM` with source/academic HOLD |
| Physics producer D3 nominations | 8, of which 4 score contradict the common five-factor band rules | Display both nominated and calculated rubric band, mark QRT conflict; never silently change the original proposal |
| Producer D4 claims | 0 | Do not invent D4 content or admission; approved topic/syllabus denominator still required |
| Candidate figure dependency | Five existing declared figures plus missing figure on the official 2024 Q34 graph question | Six candidate source-dependent cases cannot submit a purported first attempt without required depiction |
| Extra authored Physics practice | G9-AUTH-MECH-001 | Separate from 50 examination claims; remains QRT and science HOLD |

## Four QRT label/score contradictions

| Source ID | Producer label | Five-factor score | Score-based band |
|---|---|---:|---|
| NSEJS-19-OPT-02 | D3 | 2 | D1 |
| NSEJS-FND-ELEC-04 | D3 | 5 | D2 |
| NSEJS-FND-CIRC-01 | D3 | 5 | D2 |
| NSEJS-FND-CIRC-02 | D3 | 5 | D2 |

**Score consistency is not a cognitive-demand adjudication.** Even the four D3-nominated entries whose scores lie in range require independent reasoning/task and QRT review.

## Source cross-check

The following 2024 Code 51 question locators, candidate topic/stems at the meaningful problem level and official answer letters were checked against official paper/key evidence: Q22, Q33, Q34, Q36, Q37, Q42, Q43, Q44, Q46 and Q48. The 2023 convex-mirror item is official Code 51 Q43, not its inherited Q1 label.

Official sources: [IAPT 2024 paper](https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf), [IAPT 2024 final answer key](https://www.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf), [IAPT 2023 paper](https://www.iapt.org.in/images/nse_2023/NSEJS_2023_Set_51.pdf), [IAPT 2023 answer key](https://www.iapt.org.in/images/nse_2023/NSEJS_2023_TENTATIVE_ANSWER_KEY.pdf).

Original IAPT PDFs and examination figures are **not** imported or republished. A content-equivalent digital paraphrase is not a byte-exact exam transcription. The claimed 2024 Q1/Q2 optics identifiers are definitively contradicted by the official Biology items at those paper positions.

## Commands

```bash
python tools/build_nsejs_core2_corpus.py --check
python tools/build_nsejs_core2_integrity.py --check
python -m pytest tests/test_nsejs_core2_agent_a.py tests/test_nsejs_core2_integrity_r3.py -q
python tools/test_nsejs_core2_browser.py
```

`python tools/build_nsejs_core2_integrity.py --check --academic-gate` **must exit 4** while authenticity, QRT and admission remain unresolved. This is an intentional academic fail-closed gate, not a software test failure.

**Release:** A technically verified, candidate-only patch may be merged into PR #80's feature branch under Owner authorization. PR #80 is not authorized to merge into `main` or deploy until wider CI, rights, source and academic evidence are resolved.

**No academic approval inferred from software validation.**
