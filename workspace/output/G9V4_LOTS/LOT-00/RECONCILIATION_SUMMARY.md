# Lot 00 Reconciliation Summary — Arithmetic and Status Analysis (Repaired B2 Edition)

**Date:** 2026-11-01  
**Scope:** Physics / WPE 79 Raw Source Records Reconciliation  
**Disposition:** PASS WITH FIXES for candidate inventory; HOLD for Lot 01 authorization and academic admission.

---

## 1. Candidate Identity & Deduplication Arithmetic

- **Raw source records:** Exactly **79** records exist in `registry.json` (`kind: "EXAM_CANDIDATE"`).
- **Candidate duplicate alias pair:**
  - Primary record: `EX-M4` (ExamSIDE ID, `collection: "JEE / AIEEE"`)
  - Candidate alias: `JEE-2026-04-05-S2-Q28` (NTA Pass 2 raw intake, `collection: "JEE / AIEEE"`)
  - Sitting: JEE Main 2026 Session 2 / 2026-04-05 / Shift 2 (Evening)
  - Options: Identical options `['20', '25', '30', '10']`
  - Stem: Punctuation and formatting variant ("A mass of 1 kg is kept on an/a inclined plane with 30°...")
  - *Governance designation:* **Candidate alias**, not proof of being the sole duplicate across all 79 or a fully authenticated NTA map.
- **Provisional distinct identities:** Exactly **78** distinct identities (pending independent cross-source authentication).

### Category Arithmetic: Raw Records (79) vs. Provisional Distinct Identities (78)

| Dimension | Raw Records (79) | Provisional Distinct Identities (78) | Deduplication Difference |
|---|---|---|---|
| **In-Scope (WPE)** | 66 | 65 | -1 (`JEE-2026-04-05-S2-Q28` merges into `EX-M4`) |
| **Prerequisite Bridge** | 8 | 8 | 0 (all unique) |
| **Out-of-Scope (Collision)** | 5 | 5 | 0 (all unique) |
| **Scope Total** | **79** | **78** | **-1** |
| | | | |
| **Verified Key (Inherited Claim)** | 1 (`WEP07-03`) | 1 (`WEP07-03`) | 0 |
| **Partial Key (Inherited Claim)** | 1 (`EX-M39`) | 1 (`EX-M39`) | 0 |
| **Unresolved Coaching Key** | 77 | 76 | -1 (both alias members unresolved) |
| **Key Status Total** | **79** | **78** | **-1** |
| | | | |
| **Text-Only (No Figure)** | 44 | 43 | -1 (both alias members text-only) |
| **Required Figure (Unresolved)** | 25 | 25 | 0 |
| **Required Figure (Retained)** | 10 | 10 | 0 |
| **Figure Status Total** | **79** | **78** | **-1** |
| | | | |
| **Conditional Leads** | 14 | 14 | 0 |
| **Unselected Candidates** | 65 | 64 | -1 (`JEE-2026-04-05-S2-Q28` unselected) |
| **Selection Total** | **79** | **78** | **-1** |
| | | | |
| **Stem Bound in Registry** | 74 | 73 | -1 |
| **Stem Not Bound in Registry** | 5 (`WEP07-01..05`) | 5 (`WEP07-01..05`) | 0 |
| **Text Binding Total** | **79** | **78** | **-1** |

---

## 2. 62-Item ExamSIDE Source Cross-Comparison Analysis

A comprehensive comparison was executed between the 62 `EX-` candidate records in `registry.json` and the 62 items in `examside-wpe-extract.json`:
- **Identifier correspondence:** Exactly 62/62 item IDs match (`M2` -> `EX-M2`, etc.).
- **Option lists & paper metadata:** Exactly 62/62 match.
- **Stem text comparison:**
  - **Exact verbatim matches:** Exactly **49/62** stems match character-for-character.
  - **Differing stems:** Exactly **13/62** stems differ (`EX-N8`, `EX-N11`, `EX-N19`, `EX-N21`, `EX-N26`, `EX-N27`, `EX-N30`, `EX-N31`, `EX-N34`, `EX-N38`, `EX-N39`, `EX-N41`, `EX-N42`).
  - **Root cause of difference:** In `examside-wpe-extract.json`, these 13 questions contain trailing web-scraper artifacts appended to numerical value questions: `\s*—\s*123456789\.0-\s*Answer\s*answer is.*`. In `registry.json`, this scraper suffix was cleanly stripped.
  - **Normalized match:** When normalizing by stripping the trailing scraper artifact, **62/62 stems match 100%**.
  - *Note:* These 62 records are not claimed as independently authenticated exam papers, but as accurately reconciled against the ExamSIDE extract source.

---

## 3. Five NSEP Extension Records Analysis (`TEXT_NOT_BOUND_IN_REGISTRY`)

Five candidate records originate from the NSEP extension:
- `WEP07-01` (NSEP 2024 code 61 Q4)
- `WEP07-02` (NSEP 2024 code 61 Q32)
- `WEP07-03` (NSEP 2025 code 61 Q57)
- `WEP07-04` (NSEP 2024 code 61 Q59)
- `WEP07-05` (NSEP 2019 code 61 Q19)

**Findings & Corrections:**
- All five records contain `stem: None` and `options: None` in `registry.json`, carrying active hold `EXACT_TEXT_EXTRACTION_NOT_COMPLETED`.
- In the initial run, the generator calculated the SHA-256 digest of the empty string (`e3b0c44...`).
- **Correction applied:** Stems are now explicitly recorded as `TEXT_NOT_BOUND_IN_REGISTRY` with `stem_sha256: null`. They require external official NSEP intake binding before question authoring.

---

## 4. Academic Key & Admission Governance

- **VERIFIED (1 item, `WEP07-03`):** Inherited claim from legacy review (IAPT official final answer key for NSEP 2025 code 61 Q57 confirms options a, b, c, d; 2 blind solves agree). Primary source receipts pending fresh independent review.
- **PARTIAL (1 item, `EX-M39`):** Inherited claim from legacy review (3 blind solves + coaching agree option B); NTA Session 1 official key mapping unverified; legacy dropped-question 533543501 risk noted as unconfirmed preliminary claim pending fresh primary-source investigation. Remains on HOLD.
- **UNRESOLVED (76 unique / 77 raw):** Supported only by third-party coaching explanations. Authentic NTA question ID-to-option ID chains have not been verified.
- **Admitted questions:** Exactly **0** (fail-closed zero admission gate strictly maintained).

---

No academic approval inferred from software validation.
