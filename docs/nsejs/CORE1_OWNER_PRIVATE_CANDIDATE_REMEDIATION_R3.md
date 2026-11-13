# Grade9 v4.0 — Owner Core1 private candidate correction R3

**Task:** G9V4-CORE1-CORE2-SCIENCE-CUSTODY-QA-R3  
**Original source checkout:** `main` at `0f6ca753f86d7df340f0d41955ae14ca52155344` (2026-11-13); **rebase base**: `ac6e632302b544c6ddec274864ff6ae279001cbb` after PR #115.  
**Mode:** PRIVATE_SOURCE_FIRST · SCIENCE_CANDIDATE · FAIL_CLOSED  
**Scope:** Physics, Chemistry and Biology only; mathematics out of this correction lane.

## Archive custody and identity

- Incoming Owner archive `G9V4_ALL_CORE1_MODULES_COMPLETE_20261113(1).zip`, SHA-256 `e5d389e8da62fc8c219373691f42ed93233814284bd15cb64a5ab8b5a5ade40f`.
- **27 folder names**, **26 unique construction IDs**: Physics 16; Chemistry 7; Biology 3.
- `chem-atomic-structure-r1` and `chem-atomic-bonding-r1` have identical A/B construction/witness/learner HTML but different source `bank.json`. They form **one identity with two distinct source-bank bindings**. No 27th unique construction should be invented.
- Original A explicit `CANDIDATE`: **19/27**; missing `status`: **8/27**. Original B and witness carry candidate statuses. R3 derivative normalizes A to 27 explicit `CANDIDATE`.
- 27 original `bank.json` remain byte-for-byte unmodified in the private derivative. Updated producer SHA links in 27 witnesses cover **54/54 Core1A/1B payloads**. Producer hashes confirm internal integrity only; **zero independent approval receipts**.
- Private derived candidate filename: `G9V4_CORE1_PRIVATE_CORRECTED_CANDIDATE_20261113.zip` and SHA-256 `1fb71fa9d91a33da693f952207f5a88a8da89e5afbb582004b02170c1b87a70b`. This ZIP is supplied separately to the Owner, **NOT committed to GitHub**.
- The original ZIP has an empty `MANIFEST.json` (`total_modules: 0`) and README placeholder `COMPUTING_SHA256`; the *derivative* manifest carries actual subject and alias counts. The original is left unchanged.

## Four reviewed science/source contradictions

| Owner folder | Candidate-level finding | R3 treatment | Admission |
| --- | --- | --- | --- |
| `chem-chemical-substances-r1` | Fresh B zinc task 2.035 g MO → 3.625 g Na2MO2 implies A≈63.35, not Zn 65.4 | Correct B product mass to **3.585 g**; derive 1.550A=101.37, A=65.4, acid volume **50.0 mL**. Original Core2 aluminium bank unchanged. | HOLD |
| `nsejs-optics-lens-mirror-d3-r1` | B rubric and reconstruction wrongly switched from f=10, u=-15, mirror x=20 to f=20, u=-30, mirror x=40 | Align on **v1=30 cm, final image x=+10 cm, magnification -2**. Original Core2 bank unchanged. | HOLD |
| `ioqjs-optics-conjugate-d3-r1` | B accepted **f=9 cm**, even though task asks object distances; incorrect difference-sign rubric | Accept **18 cm and 6 cm**; preserve 1/u1+1/u2=2/f; finite coincidence requires d>2f. Original Core2 bank unchanged. | HOLD |
| `nsejs-magnetism-r1` | The official IAPT Code 51 Q44 source figure is located, with provisional crosswalk to Code 54 Q28; original source-byte hash and reuse rights remain HOLD. Authored SVG gave away correct/incorrect labels precommit | Remove answer labels and caption leak from authored preview; explicitly label it **not the verified original**. Record Code 51 Q44 and Code 54 Q28 as distinct paper-code IDs and keep original figure byte custody and reproduction rights HOLD. | SOURCE FIGURE/KEY HOLD |

The first three are bounded **authored candidate repairs**, not independent academic adjudications. Magnetism remains unresolved until authenticated official four-panel artwork, orientation and key provenance are reviewed.


### Official 2024 magnetism locator — independently checked public evidence, NOT custody approval

The publicly indexed [IAPT NSEJS 2024 paper, code 51](https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf) includes the four-panel induction question at **Q44** (printed page 10). The [IAPT final answer key](https://www.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf) states **code 51 Q44 = D** and separately **code 54 Q28 = D**. An [Aakash code 54 worked-paper image](https://dcx0p3on5z8dw.cloudfront.net/Aakash/s3fs-public/pdf_management_files/target_solutions/NSEJS_2024_Answers-and-Solutions_Final.pdf) shows the same four-panel wording at **Q28**. This explains the supplied bank's `NSEJS-2024-P-Q28` while correcting its witness's older code-51/Q28 conflation. 

**Gate remains HOLD:** a web-viewable official source locator/figure and key table are now verified, but the raw official PDF bytes could not be retrieved and SHA-pinned in private custody, redistribution permission is unverified, panel-by-panel independent scientific audit is NOT_RUN, and the original bank is not source-approved. The derivative witness records these facts and retains `source_paper_bytes_sha256: null`. Do not embed the official four-panel diagram in public GitHub Pages without authorized rights.

## R3.1 after PR #115 — canonical Core1 ⇄ Core2 private-source lineage

PR [#115](https://github.com/reallakshman19/Grade9v4.0/pull/115) merged to main at `ac6e632302b544c6ddec274864ff6ae279001cbb`. It established a digest-only public Core2 identity map for **45 PCB modules and 267 question occurrences**. It did *not* publish original paper questions or independently admit source/QRT.

A fresh **private local byte replay**, using the 27 original `bank.json` files retained in the corrected Core1 ZIP and the public PR115 digest registry, confirmed:

- **27/27** raw bank SHA-256 digests match PR115's `source_bank_sha256`.
- **27/27** full-question canonical SHA-256 revisions match PR115's `content_revision_sha256`.
- **27/27** source bank bytes are identical to the uncorrected Owner Core1 archive.
- Every original bank maps to a distinct module-scoped `g9:pcb:<subject>:<slug>:001` UID.
- **26** corresponding PR115 entries are only `RELATED_ONLY_UNVERIFIED`, while `chem-atomic-bonding-r1` is `MISSING_CONSTRUCTION`; that is the second source question bound to the same Chemistry Core1 construction, not another unique Core1.
- PR115's full corpus still has **241 missing constructions** and **zero** independently qualified source-bound learning routes. These figures do not describe missing *folder identities*.
- Four conflicting external source labels, five producer operation/crux disagreements and thirteen figure-custody HOLDS remain in the full 267 record map.

Private receipt generated outside GitHub: `G9V4_CORE1_PR115_PRIVATE_SOURCE_LINEAGE_20261113.json`, 27 entries. **Do not commit the receipt if its retention and redistribution scope is not authorized.** Hash continuity establishes a join, not original-paper authenticity, source usage rights, independent QRT, scientific correctness or B1–B7 teaching sufficiency.

The audit tool now optionally validates these links directly against PR115's strict, immutable public registry via `--core2-repository-root .`, including negative controls for source-byte, question-revision, canonical UID, academic state and falsely qualified learning routes.

## Audit tool / private replay

The public repository contains `tools/audit_nsejs_owner_core1_private_zip.py`. It requires **no committed private data**. Execute it only where the private archives are authorized:

```sh
python tools/audit_nsejs_owner_core1_private_zip.py \
  --original /private/G9V4_ALL_CORE1_MODULES_COMPLETE_20261113.zip \
  --candidate /private/G9V4_CORE1_PRIVATE_CORRECTED_CANDIDATE_20261113.zip \
  --original-sha256 e5d389e8da62fc8c219373691f42ed93233814284bd15cb64a5ab8b5a5ade40f \
  --candidate-sha256 1fb71fa9d91a33da693f952207f5a88a8da89e5afbb582004b02170c1b87a70b \
  --core2-repository-root /private/Grade9v4.0 \
  --json-out /private/core1-candidate-r3-receipt.json
```

The tool checks all 27 A/B/status records, 54 producer hashes, 27 original bank comparisons, alias identity, four narrow defect invariants and source/academic HOLD. When the PR115 registry is supplied, it also verifies all 27 raw bank and full-question revision hashes, 27 canonical UIDs and the distinct 26 related / one missing teaching classifications. Its success means **technical derivative invariants only**.

### Original archived HTML B5/B6 readiness is NOT established

A static audit of the **27 private original `learning_journey.html`** files (distinct from the 18 public supplemental pages) found **0/27** references to browser storage APIs (`localStorage`, `sessionStorage` or `indexedDB`). Only **17/27** have recognizable textual markers for all six stages. Many use a simple `commitAnswer()` reveal action without a durable protected first response. Static text inspection is not an E2E behavioral test, but it identifies a B5/B6 blocker that cannot be cleared by the green 18-supplement Chromium workflow. Candidate originals remain **HOLD** pending real staged six-stage state/attempt/hint/diagnosis/repair/boundary checks and actual Chromium.

## B1–B7 source-specific qualification

All 26 unique originals still need a source-bound academic binder with B1 target, B2 exact reasoning signature, B3 teaching sufficiency, B4 independent new inference, B5 protected attempts/help, B6 causal diagnosis and changed-condition transfer, B7 scientific/source/figure warranty. Source-only first-pass independent QRT reviewers **must not** be given author-exposed reasoning or this science correction in advance. A self-authored witness is not a reviewer receipt.

Required private source custody for original Core2: authorized paper/source bytes, original figures and orientation, official key provenance, question UID and revision digest, rights to use/redistribute, independent subject review; otherwise mark `HOLD` / `NOT_RUN`. Do **not** publish original source ZIP, drawings, stems, answer keys or private generated QA outputs in public Git history or Pages.

## Exact-head technical QA and release

For merged `main` SHA `0f6ca753f86d`:

- GitHub Actions [public-safe Pages and 12.7-inch Chromium](https://github.com/reallakshman19/Grade9v4.0/actions/runs/43369538815): **PASS** for published *supplemental* routes, catalog and staged learner, including deployment.
- GitHub Actions [unchanged full Python QA](https://github.com/reallakshman19/Grade9v4.0/actions/runs/43369538835): **FAIL** in both Python 3.11 and 3.12. Existing diagnostic identifies **at least 30 missing private source paths and 187 output paths**, with historical 26 failures and 424 errors. These are lower-bound paths, not content-count equivalences.
- The local private ZIP HTTP Chromium attempt was **NOT_RUN / ENVIRONMENT_BLOCKED**: this session's browser refused all navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. There is **no claim of 27 original candidate pages passing**.
- All original source/figure/QRT and academic release decisions: **HOLD**.

### Remaining acceptance work

1. Obtain authorized original exam source and figure/key bytes privately, with rights and custody hashes. Keep candidate corrections separate from the original source.
2. Independently review all 26 source-bound B1–B7 binders; secure source-only QRT and actual task-specific academic acceptance.
3. Restore verified private `workspace/sources` and generate `workspace/output` using approved builders, not placeholders; rerun **unchanged** full Python suite on the exact final head (3.11 and 3.12).
4. Run **actual original-27** HTTP Chromium tests at 1600×1000 and 1000×1600 with touch, keyboard, saved first attempts, hints/exposure, refresh, source return, negative source/revision, and blocked-storage behavior. A working static page alone is not B1–B7.
5. Verify changed-file scope, exact-head CI, the Pages artifact/manifest and live assets before declaring any public technical deployment. Original academic promotion remains separate.
6. Reconcile stacked stale draft PRs #109/#112 against their now-merged technical-preview content; do not replay duplicate private work or merge an old diverged head.

**Release decision:** candidate corrections documented, private replay independently auditable; original-source academic publication **NOT AUTHORIZED**. No academic approval inferred from software validation.
