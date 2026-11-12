# Lot 01 Source & Official-Key Investigation Report: EX-M39 (Repaired B2 Edition)

**Date:** 2026-11-01  
**Target Item:** Local Source ID `EX-M39` (Registry Record #12 / Task Identity `Q-ID-12`)  
**Exam Sitting:** JEE Main 2024 (Online), 27 January, Shift 2 (Evening)  
**Investigation Scope:** Vertical Swing Acceleration Dynamics  
**Final Disposition:** **PARTIAL (NTA_OPTION_TEXT_BINDING_NOT_VERIFIED) &rarr; HOLD (Academic Admission & Learner Card Authoring Blocked)**

---

## 1. Candidate Identification & Custody

- **Registry Record:** `workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data/registry.json`
- **Extract Record:** `workspace/legacy/g9v3.5/qrt/sources/examside-wpe-extract.json` (`/items/12`, id: `M39`)
- **Sitting:** JEE Main 2024, Session 1, 27-01-2024 Shift 2 (Evening)
- **Question Type:** Single-Correct MCQ
- **Stem Digest:** SHA-256 `cfa7368ff62d1c68f2fe15fa57659bb29d2110c950c45da62fcb5e7d598b5071` (228 chars)
- **Figures:** None in stem or options.
- **Current Scope Role:** `PREREQUISITE_BRIDGE` (circular dynamics bridge; not WPE direct-exam coverage).

---

## 2. Updated Four-Link Official Source Chain Audit

Following B2 independent review findings, material secondary provenance was incorporated:

| Link | Segment | Primary / Secondary Evidence Reference | Status | Findings & Specific Precision |
| :--- | :--- | :--- | :--- | :--- |
| **Link 1** | Stem &rarr; Exam Sitting | ExamSIDE extract `/items/12`; multiple secondary coaching compilations | **SUPPORTED** | Stem wording matched across registry, ExamSIDE, ALLEN (Q38), Cracku (Q4), Collegedunia (Q38), and Matrix Academy (Q8). Original-paper custody still pending. |
| **Link 2** | Stem &rarr; NTA Question ID | Matrix Academy, JEE Main 27-01-2024 Shift 2 Physics, p. 4 (`https://www.matrixedu.in/assets/default/physics/27_jan_shift2_2024.pdf`) | **THIRD_PARTY_ID_MAPPING_FOUND** | Matrix Question 8 displays the exact swing stem and explicitly labels it with **NTA Question ID 533543498**. Original NTA master paper / candidate response sheet custody not checked. |
| **Link 3** | NTA Q-ID &rarr; NTA Option ID | NTA Official Final Answer Key Notice as on 12 Feb 2024, p. 2 (`https://jeemain.nta.ac.in/images/Final_Answer_Key_P1_12022024.pdf`) | **VERIFIED FOR GIVEN ID** | NTA official key confirms for 27-01-2024 Shift Second Physics: **Question ID 533543498 &rarr; Correct NTA Option ID 5335431726**. |
| **Link 4** | Official Option ID &rarr; Math Expression | Authentic candidate response sheet with Option IDs | **PARTIAL (NTA_OPTION_TEXT_BINDING_NOT_VERIFIED)** | Matrix places the derived expression $\theta = 2\tan^{-1}(1/2)$ at Choice (1), whereas Owner extract places it at Choice (B). Matrix does not print the specific NTA Option IDs assigned to each mathematical expression. Option ID cannot be inferred from position; authentic response sheet needed. |

### Resolution of Dropped Question ID 533543501
- In Matrix Academy's question paper, **Question 6** displays the separate **bullet-penetration into wooden block question** and labels it with **NTA Question ID 533543501** (marked bonus by Matrix).
- In the NTA Final Answer Key Notice, **Question ID 533543501 is marked "Drop"**.
- **Conclusion:** Matrix independently associates dropped ID `533543501` with the bullet-penetration problem, providing **strong counterevidence** that the swing question is NOT the dropped item. The obsolete "unruled risk" label is removed.

---

## 3. Cognitive (QRT) & Physics Blueprint Assessment

- **Proposed Cognitive Classification:** `SYNTHESIZE · D3` (Demand: Multi-step reasoning; Score: 7/10 per B2 review factors: Concept 2, Representation 1, Chain 2, Algebra 1, Trap 1).
  - Decisive reasoning move: Coordinate two points in circular trajectory by equating extreme-point tangential acceleration ($a_t = g\sin\theta$) with lowest-point centripetal acceleration ($a_c = 2g(1-\cos\theta)$) linked by conservation of mechanical energy ($v^2 = 2gL(1-\cos\theta)$).
  - Derived result: $\theta = 2\tan^{-1}(1/2)$, independently derived by B2 and confirmed by 3 coaching solves.
- **Physics Blueprint Reference:** `workspace/subjects/physics/blueprints/physics-blueprint.D3-D4.resolved.v0.2.0.json` (SHA-256 `AC32DC93...`), Cell `D3.6` (`QRT-SYNTHESIZE-D3`).
- **Adapter Fit:** `HOLD:ADAPTER_PIN`. The root draft WPE adapter does not qualify vertical circular dynamics as a native core operation.

---

## 4. Execution Stop Gate & Policy Adherence

Per Lot 01 instructions:
> *"Stop before learner-card construction if PARTIAL, NOT_FOUND or FAIL. Preserve an evidence page and HOLD; do not use coaching's answer as the official key."*

- **Learner Card Authoring:** **BLOCKED / NOT AUTHORIZED**. No `rendered/core2.html` card was created.
- **Academic Admission:** **NOT_ADMITTED** (0 admitted).
- **Public PR Status:** **NOT_CREATED / HOLD:BASE_NOT_READY**. PR #22 remains an unmerged draft.

---

## 5. Outstanding Owner Decisions

1. **Source-Chain Acceptance:** Decide whether the Matrix Academy third-party ID mapping (`533543498`) plus NTA Final Key (`5335431726`) is sufficient, or if authentic NTA candidate response-sheet custody is required to verify option-ID-to-text binding (`NTA_OPTION_TEXT_BINDING_NOT_VERIFIED`).
2. **Scope Determination:** Explicitly authorize whether `EX-M39` remains `PREREQUISITE_BRIDGE` or enters an expanded circular dynamics adapter.
3. **Adapter Selection:** Approve / pin topic adapter accommodating multi-step circular dynamics.
4. **PR Base Selection:** Authorize a stable base branch before opening a new public draft PR.
5. **Authoring Authorization:** Explicitly grant authorization before any student learner card is built.

*No academic approval inferred from software validation.*
