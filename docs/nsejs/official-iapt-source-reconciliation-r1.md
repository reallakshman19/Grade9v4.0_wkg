# NSEJS 2020–2024 — official IAPT source recovery and Code 51 spot check

Mode: CONTRIBUTOR / SELF_REVIEW · SOURCE_FIRST · NO ORIGINAL REPUBLICATION · ACADEMIC_HOLD
Verified as of 12 November 2026. **9/10 official IAPT paper/key PDF files were retrieved and hashed from their actual bytes in private GitHub Actions memory.** Exact per-file SHA, size and page count appear in `official-2020-2024-raw-byte-custody-r1.json`. Reproduction rights, figure and question source fidelity remain NOT_VERIFIED.

## Official IAPT archive links

| Exam cycle | Official archive | Paper link | Key link | Current qualification |
|---|---|---|---|---|
| 2020–21 IOQJS Part I | https://iapt.org.in/ioq-2020-21-part-i/ | https://iapt.org.in/images/nse_2020/IOQJS%20PART%20I%202020-21.pdf (indexed original; live HTTP 404) | https://iapt.org.in/wp-content/uploads/Final-Answer-key-IOQJS-2020-21Part-I.pdf | Official key shows Q1–32; do not mislabel this as ordinary NSEJS |
| 2021–22 IOQJS Part I | https://iapt.org.in/nse-2021-22/ | https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i.pdf | https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i_answer_key.pdf | Official raw paper/key PDF bytes hashed; science/rights not reviewed |
| 2022–23 NSEJS | https://iapt.org.in/nse-2022-23/ | https://iapt.org.in/wp-content/uploads/nsejs_2022_23_part_i.pdf | https://iapt.org.in/wp-content/uploads/nsejs-2022-final-answer-key.pdf | Official 13,436,882-byte paper and key PDF successfully SHA-256 hashed in CI; source/rights not reviewed |
| 2023–24 NSEJS | https://iapt.org.in/nse-2023-24/ | https://iapt.org.in/wp-content/uploads/NSEJS_2023_Set_51.pdf | https://iapt.org.in/wp-content/uploads/NSEJS_2023_TENTATIVE_ANSWER_KEY.pdf | Paper/key PDF bytes hashed; archive FINAL vs filename TENTATIVE needs independent publication identity review |
| 2024–25 NSEJS Code 51 | https://iapt.org.in/nse-2024-25/ | https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf | https://www.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf | Official paper first and printed page 12 visually inspected; final key text examined |

These official URLs now have **verified raw-byte SHA-256 custody for nine files**, including both 2024 Code 51 documents. The 2020–21 paper has an indexed original IAPT URL but remains HTTP 404 live. CI retrieved official PDFs privately and uploaded **hashes only**, never original files. Missing gates remain figure fidelity, republication rights, item-by-item original comparison, and native source-bank construction. Do not use OCR to invent diagrams, keys or original content.

## Exam format and key constraints verified from Code 51 (2024)

- Q1–48 are single-correct; Q49–60 are multiple-correct.
- Official final key marks Q20 DROP in Code 51. Do not grade that question with an invented ordinary option.
- Five bounded source-to-module spot checks (not full source authentication):

| Original IAPT item | Observed subject/theme | Official Code 51 key | Existing proposed module | Spot-check conclusion |
|---|---|---|---|---|
| Q50 | Virus statement evaluation | C,D | BIO-VIROL-C-CAPSID-ENVELOPE-GENOMES-D3-01 | Original locator found; text/figure/key custody not admitted |
| Q52 | Antibody, eosinophil, ciliary barrier, B-cell surface immunoglobulins | A,C,D | BIO-IMMUN-C-VERTEBRATE-DEFENSE-D3-01 | **P0 SOURCE CONTRADICTION:** authored bank substitutes histamine for original B-cell IgM/IgD option D, changes option B wording/meaning |
| Q55 | Phosphorus oxyacid | A,D | CHEM-INORG-C-PHOSPHORUS-OXYACIDS-D3-01 | Original locator found; full text/figure digest not checked |
| Q56 | Scandium electrons | A,B,C | CHEM-ATOM-C-ELECTRONIC-POPULATION-D3-01 | Original locator found; full text/figure digest not checked |
| Q57 | Lens displacement D=75 cm, f=12 cm | A,B,C,D | PHYS-OPT-C-LENS-DISPLACEMENT-D3-01 | Numerical source anchors, theme, original diagram visually checked against paper page 12; academic approval HOLD |

### Why Q52 is critical

In repository file build_d3_batch2_modules.py, the authored mod3_bank claims the NSEJS-2024-B-Q52 source identity but option D discusses histamine; the official Q52 option D tests B-cell surface IgM/IgD, not histamine. The authored answer letters A,C,D happen to match the IAPT final key, masking the source substitution. **A matching set of answer letters cannot prove verbatim examination content.**

Agent A owns native original bank, canonical UID and original exam registry. Do not silently rewrite that original or promote a synthetic biology question as source-exact. Agent B may correct its own Core1A teaching to cover B-cell surface receptors and eosinophil lineage, but source question admission stays HOLD.

### Completion sequence

1. Retain and reproducibly verify the nine official PDF-byte SHA receipts; recover the 2020–21 Code 51 paper from an authorized IAPT source or owner-supplied original, and separately determine publication rights.
2. Compare source stem, four options, key, paper code and figures item-by-item (Q52 first); preserve the difference record.
3. Source-preserving native Core2 builder, exact-UID/content-revision binding and true multiple-choice responses for Code 51 A2.
4. Reconcile Core1A concept and Core1B fresh W against accepted paper UID/cognitive roles, then independent B1–B7 subject review.
5. Keep public Pages technical preview UNVALIDATED; no merge, deployment or academic approval from this receipt.

Rule 13: No academic approval inferred from software validation.

## Exact-head source byte receipt

- [Official IAPT PDF-byte CI run #43229165198](https://github.com/reallakshman19/Grade9v4.0/actions/runs/43229165198): nine actual PDF byte receipts, one live archived 2020 paper HTTP 404. Contents not published in artifacts.
- Raw-byte custody metadata: `docs/nsejs/official-2020-2024-raw-byte-custody-r1.json` (nine SHA256 digests and one missing-bytes record).
- 2024 Code 51 known original-question data errors remain source-owner review findings; a PDF SHA does not prove candidate stem/figure/answer equivalence.
- **Rights:** IAPT allows public linking to its papers, but I could not locate express permission to copy the full exam into this public repository. Default is LINK_ONLY_UNTIL_WRITTEN_AUTHORIZATION, not a claimed license.
