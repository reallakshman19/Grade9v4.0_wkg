# Oracle Checkpoint — 12 November 2026

**Timestamp:** 2026-11-12T08:44:00+04:00  
**Operating Sequence:** **NSEJS 5-Year Past-Paper Ingestion (2024, 2023 & 2022 COMPLETE across PCB: 180 authentic items) $\to$ 2021 $\to$ 2020**  
**Active Branch:** `feat/multi-subject-core2-expansion-01`  
**Authority Invariant:** Rule 13 in `AGENTS.md` (*No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.*)

---

## 1. Subject Track & Curriculum Status Overview

| Subject Track | Topics / Papers Ingested | Ingested Question Count | Test Suite Status | Track Status |
| :--- | :--- | :---: | :---: | :---: |
| **Track 1: Physics** | Ray Optics, Electrostatics, Circuits, Magnetism & EMI, Mechanics, Fluid Mechanics & Sound, **NSEJS 2024, 2023 & 2022 Official Paper 51** | **120 items** | 23 suites (6 Core 2 topics + 8 D3 + 6 Core 1A/1B + **NSEJS 2024, 2023 & 2022 Papers**), **241 passed** | **100% COMPLETE (All Topics + 2024, 2023 & 2022 Official Papers Ingested)** |
| **Track 2: Mathematics** | Topic 1: Algebra & Polynomials<br>Topic 2: Number Theory & Divisibility | **20 items** | 2 suites, **43 passed** (Full QRT Labelling) | **COMPLETE (Topics 1 & 2 Ingested; paused per user)** |
| **Track 3: Chemistry** | Topic 1: Matter & Mole Concept<br>Topic 2: Chemical Substances — Reactions<br>Topic 3: Atomic Structure & Bonding<br>D3 Modules (Eudiometry & Redox Titrations)<br>**NSEJS 2024, 2023 & 2022 Official Paper 51** | **92 items** | 12 suites (3 Core topics + 6 D3 + **NSEJS 2024, 2023 & 2022 Papers**), **122 passed** | **100% COMPLETE (All Topics + 2024, 2023 & 2022 Official Papers Ingested)** |
| **Track 4: Biology** | **NSEJS 2024, 2023 & 2022 Official Paper 51** | **60 items** | 3 suites (**NSEJS 2024, 2023 & 2022 Papers**), **59 passed** | **100% COMPLETE (2024, 2023 & 2022 Official Papers Ingested)** |
| **Cross-Subject Architecture** | Shared/QRT Schemas, Bounded Transfer Protocols, Gate Checkers, Audit Invariants | N/A | 10 cross-cutting contract suites, **461 passed** | **ACTIVE & ENFORCED** |
| **TOTALS** | **28 Active Learning Modules** | **332 items** | **43 Pytest Suites, 890 Passed, 2 Skipped (Platform Symlinks), 0 Failed** | **100% GREEN CI** |

---

## 2. NSEJS 5-Year Authentic Corpus Inventory (`nsejs.com/previous-exam-papers`)

All 12 official question papers, detailed solution booklets, and chapter/concept analysis PDFs have been downloaded and cataloged in `scratch`:

| Examination Year | Total Questions | Physics | Chemistry | Biology | Mathematics | Status in Workspace |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **NSEJS 2024** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 54 Tests)** |
| **NSEJS 2023** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 53 Tests)** |
| **NSEJS 2022** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 54 Tests)** |
| **IOQJS / NSEJS 2021** | **33** | 11 | 11 | 11 | 0 | Downloaded (`nsejs_2021_*.pdf`), ready for extraction |
| **IOQJS 2020** | **24** | 8 | 8 | 8 | 0 (excl) | Downloaded (`nsejs_2020_*.pdf`), ready for extraction |
| **Total Authentic PCB Corpus** | **237 items** | **79** | **79** | **79** | 0 | **180 items ingested (75.9% complete); 57 items staged** |

---

## 3. NSEJS 2022 Complete Ingestion Modules (Paper Code 51)

### Physics: `nsejs-2022-physics-r1` (20 items: `NSEJS-2022-P-Q33` to `Q48`, `Q57` to `Q60`)
- **Single Correct (Q33–Q48):**
  - `Q33`: Constant power kinetic energy integration ($t = K/P = 10\text{ s}$ [B]).
  - `Q34`: Leaking trolley horizontal momentum invariance ($v = 10\text{ m/s}$ [C]).
  - `Q35`: Piecewise $a-t$ kinematics ($s = 51\text{ m}, v = 6\text{ m/s}$ [A]).
  - `Q36`: Binary star gravitational mutual attraction ($v = \sqrt{GM/d}$ [A]).
  - `Q37`: Moving sound source echo timing ($350t = 1400 \implies t = 4.00\text{ s}$ [B]).
  - `Q38`: Dual-fluid hydrostatic flotation density ($\rho_s = 7.2\text{ g/cm}^3$ [C]).
  - `Q39`: Gravitational free fall and buoyant cycle duration ($T = 8\text{ s}$ [C]).
  - `Q40`: Specular reflection angle between two mirrors ($\theta = 60^\circ$ [B]).
  - `Q41`: Long solenoid magnetic field maximum at central point O ([C]).
  - `Q42`: Partition door differential hydrostatic thrust ($F = 39.2\text{ N} \approx 39\text{ N}$ [C]).
  - `Q43`: Negative charge Lorentz force vector direction (Upward [C]).
  - `Q44`: Raman effect inelastic photon scattering ([D]).
  - `Q45`: Uniform motion graphs (Official key DROP; retained for study [DROP]).
  - `Q46`: Three 60W bulbs power dissipation (Official key DROP; retained for study [DROP]).
  - `Q47`: Stretched wire resistance change (Official key DROP; retained for study [DROP]).
  - `Q48`: Sound speed temperature scaling percentage error (Official key DROP; retained for study [DROP]).
- **Multiple Correct (Q57–Q60):**
  - `Q57`: Spring balance Atwood machine (Official key DROP; retained for study [DROP]).
  - `Q58`: Lens-mirror optical combination image and magnification ([A, C]).
  - `Q59`: Symmetric resistor network reduction ($I = 1.5\text{ A}, V_{AB} = 7.5\text{ V}, P_{R0} = 2.25\text{ W}$; [A, B, C]).
  - `Q60`: One-dimensional elastic collision ($v_1 = 0, v_2 = +18\text{ m/s}$; [B, C]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/nsejs/`.
- **Test Suite:** `tests/test_nsejs_2022_physics.py` (17 passed).

### Chemistry: `nsejs-2022-chemistry-r1` (20 items: `NSEJS-2022-C-Q17` to `Q32`, `Q53` to `Q56`)
- **Single Correct (Q17–Q32):**
  - `Q17`: Heterolytic cleavage of hydroxyl O-H bond in methanoic acid ([D]).
  - `Q18`: Chemical compound diversity ranking ($N_1 > N_2 > N_4 > N_3$ [B]).
  - `Q19`: Heaviest non-radioactive stable nuclide (Lead-208 [B]).
  - `Q20`: Mole fraction dilution calculation ($x_{\text{urea}} = 0.029$ [C]).
  - `Q21`: Graham's effusion law stoichiometry for $\text{Ni(CO)}_x$ ($x = 3.9$ [A]).
  - `Q22`: Dipole moment percent ionic character of $\text{LiH}$ ($76.8\%$ [C]).
  - `Q23`: Carbonate mixture stoichiometric neutralisation ($11\% \text{ MgCO}_3$ [B]).
  - `Q24`: Total carbon oxidation state sum in toluene ($-8$ [D]).
  - `Q25`: Average oxidation state of oxygen in $[\text{O}_2]^+$ ($+1/2$ [C]).
  - `Q26`: Tertiary allylic radical abstraction of $\text{H}_c$ ([C]).
  - `Q27`: Degree of unsaturation impossible structure for $\text{C}_{10}\text{H}_{16}$ (Two triple bonds [A]).
  - `Q28`: Interstitial hydrogen gas adsorption by Palladium ([C]).
  - `Q29`: Paramagnetic $d^1$ vanadyl sulfate $\text{VOSO}_4$ ([C]).
  - `Q30`: Dehydration gas analysis mole ratio ($4:1$ [B]).
  - `Q31`: Hydrogenic degenerate energy levels ($3s = 3p = 3d > 2s$ [A]).
  - `Q32`: Semipermeable membrane solute barrier (No brown colour on either side [D]).
- **Multiple Correct (Q53–Q56):**
  - `Q53`: Weak base strong acid salt hydrolysis for $0.01\text{ M NH}_4\text{Cl}$ ([B, C, D]).
  - `Q54`: Metallurgy of aluminium amphoteric leaching (Official key DROP; retained for study [DROP]).
  - `Q55`: Periodicity ionisation enthalpy anomalies (Official key DROP; retained for study [DROP]).
  - `Q56`: Vapour pressure connected containers (Official key DROP; retained for study [DROP]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/chem/`.
- **Test Suite:** `tests/test_nsejs_2022_chemistry.py` (14 passed).

### Biology: `nsejs-2022-biology-r1` (20 items: `NSEJS-2022-B-Q01` to `Q16`, `Q49` to `Q52`)
- **Single Correct (Q01–Q16):**
  - `Q01`: Bakanae mad-seedling disease phytohormone discovery (Gibberellin [D]).
  - `Q02`: Diagnostic pollen-tube ovular entry routes (A-Porogamy, B-Chalazogamy, C-Mesogamy [B]).
  - `Q03`: Cucurbitaceae large fruits translocation (Bicollateral vascular bundles [C]).
  - `Q04`: Incomplete dominance feather pigmentation ratio ($1\text{ black} : 1\text{ white} : 2\text{ blue}$ [A]).
  - `Q05`: Spinach leaf photosynthetic pigment chromatographic sequence ([A]).
  - `Q06`: Glyoxylate cycle microbodies in germinating oil seeds (Glyoxysomes [A]).
  - `Q07`: Microbiological wastewater indicator of faecal pollution (Escherichia coli [B]).
  - `Q08`: Optimal aquatic biota physiological pH window ($6.5\text{--}7.5$ [B]).
  - `Q09`: Principal bioactive ovarian estrogen (17beta-estradiol [C]).
  - `Q10`: Pelvic articulation of axial vertebral column (Sacral vertebrae [C]).
  - `Q11`: Glycolytic substrate-level phosphorylation enzyme loci ($E_7\text{ and }E_{10}$ [C]).
  - `Q12`: Telencephalic commissural white matter tract (Corpus callosum [D]).
  - `Q13`: Bilaterally symmetrical diplomonad flagellate (Giardia [A]).
  - `Q14`: Neuronal ribosomal protein-synthesizing Nissl bodies ([C]).
  - `Q15`: Obligate intracellular viral replication requirement ([C]).
  - `Q16`: Linnaean sexual classification system nature (Artificial system [A]).
- **Multiple Correct (Q49–Q52):**
  - `Q49`: Prehistoric human evolutionary lineages (Homo habilis and Homo heidelbergensis; [B, D]).
  - `Q50`: B-complex vitamin deficiency disorders (Beri-beri & Pellagra, Dermatitis & Wernicke-Korsakoff, Cheilosis & Pernicious anaemia; [A, B, C]).
  - `Q51`: Pond water aquatic flora assemblages (Groups A, B, and D; [A, B, D]).
  - `Q52`: Nephron brush border and differential water permeability (PCT brush border 1 & segments 2, 3, 6; [B, D]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/bio/`.
- **Test Suite:** `tests/test_nsejs_2022_biology.py` (23 passed).

---

## 4. Quality Gate & Invariant Compliance

Strict compliance verified across all 332 items and 43 test suites:
- **Gate 1 (Zero Ghost Text):** 0 occurrences of `"2. Connection:"` across all modules.
- **Gate 2 (Dynamic Crux Move):** Bound to `M2` or `M3` with strategy matching.
- **Gate 3 (Rubric Bounds):** $c_i \in \{0, 1, 2\}$ with $\sum c_i = \text{score}$.
- **Gate 4 (Canonical Verbs):** Strictly within $\{ \text{RETRIEVE}, \text{EXPLAIN}, \text{APPLY}, \text{MODEL}, \text{REPRESENT}, \text{SYNTHESIZE}, \text{JUSTIFY} \}$.
- **Gate 5 (Commitment-First Derivations):** `style="display: none;"` until user commits answer.
- **Gate 6 (Mobile Cascade):** Base container styles precede `@media (max-width: 600px)` in CSS.
- **Gate 7 (W3C Typography):** $\ge 14\text{px}$ text on responsive SVG views.
- **Rule 13 Invariant (`AGENTS.md`):** *"No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized."*
