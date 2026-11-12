# Oracle Checkpoint — 12 November 2026

**Timestamp:** 2026-11-12T06:12:00+04:00  
**Operating Sequence:** **NSEJS 5-Year Past-Paper Ingestion (2024 COMPLETE across PCB: 60 authentic items) $\to$ 2023 $\to$ 2022 $\to$ 2021 $\to$ 2020**  
**Active Branch:** `feat/multi-subject-core2-expansion-01`  
**Authority Invariant:** Rule 13 in `AGENTS.md` (*No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.*)

---

## 1. Subject Track & Curriculum Status Overview

| Subject Track | Topics / Papers Ingested | Ingested Question Count | Test Suite Status | Track Status |
| :--- | :--- | :---: | :---: | :---: |
| **Track 1: Physics** | Ray Optics, Electrostatics, Circuits, Magnetism & EMI, Mechanics, Fluid Mechanics & Sound, **NSEJS 2024 Official Paper 51** | **80 items** | 21 suites (6 Core 2 topics + 8 D3 + 6 Core 1A/1B + **NSEJS 2024 Paper**), **204 passed** | **100% COMPLETE (All Topics + 2024 Official Paper Ingested)** |
| **Track 2: Mathematics** | Topic 1: Algebra & Polynomials<br>Topic 2: Number Theory & Divisibility | **20 items** | 2 suites, **43 passed** (Full QRT Labelling) | **COMPLETE (Topics 1 & 2 Ingested; paused per user)** |
| **Track 3: Chemistry** | Topic 1: Matter & Mole Concept<br>Topic 2: Chemical Substances — Reactions<br>Topic 3: Atomic Structure & Bonding<br>D3 Modules (Eudiometry & Redox Titrations)<br>**NSEJS 2024 Official Paper 51** | **52 items** | 10 suites (3 Core topics + 2 D3 + 4 Core 1A/1B + **NSEJS 2024 Paper**), **136 passed** | **100% COMPLETE (All Topics + 2024 Official Paper Ingested)** |
| **Track 4: Biology** | Topic 1: Organisation in Living World<br>Topic 2: Life Processes<br>Topic 3: Environment & Resources<br>Topic 4: Genetics & Coordination<br>**NSEJS 2024 Official Paper 51** | **60 items** | 6 suites (4 Core topics + 1 Core 1A/1B + **NSEJS 2024 Paper**), **115 passed** | **100% COMPLETE (All Topics + 2024 Official Paper Ingested)** |
| **Active Test Suites** | **21 Distinct Subject/Topic Modules** | **212 items** | **37 suites, 498 passed** | **Active Pipeline (100% Green CI Across All Subject Tracks)** |

---

## 2. NSEJS 5-Year Authentic Corpus Inventory (`nsejs.com/previous-exam-papers`)

All 12 official question papers, detailed solution booklets, and chapter/concept analysis PDFs have been downloaded and cataloged in `scratch`:

| Examination Year | Total Questions | Physics | Chemistry | Biology | Mathematics | Status in Workspace |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **NSEJS 2024** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 54 Tests)** |
| **NSEJS 2023** | **60** | 20 | 20 | 20 | 0 | Downloaded (`nsejs_2023_*.pdf`), ready for extraction |
| **NSEJS 2022** | **60** | 20 | 20 | 20 | 0 | Downloaded (`nsejs_2022_*.pdf`), ready for extraction |
| **IOQJS / NSEJS 2021** | **33** | 11 | 11 | 11 | 0 | Downloaded (`nsejs_2021_*.pdf`), ready for extraction |
| **IOQJS 2020** | **24** | 8 | 8 | 8 | 0 (excl) | Downloaded (`nsejs_2020_*.pdf`), ready for extraction |
| **Total Authentic PCB Corpus** | **237 items** | **79** | **79** | **79** | 0 | **60 items ingested (25.3% complete); 177 items staged** |

---

## 3. NSEJS 2024 Complete Ingestion Modules

### Physics: `nsejs-2024-physics-r1` (20 items: `NSEJS-2024-P-Q33` to `Q48`, `Q57` to `Q60`)
- **Single Correct (Q33–Q48):**
  - `Q33`: Kinematics acceleration comparison (Train = $12.0\text{ m/s}^2$ [D]).
  - `Q34`: Transverse wave snapshot ($A = 2.0\text{ cm}, v = 100\text{ m/s}$ [C]).
  - `Q35`: Immiscible fluid flotation submerged fraction ($(\sigma - \rho_1)/(\rho_2 - \rho_1)$ [C]).
  - `Q36`: Rectilinear motion Newton's laws (S1 and S3 correct [B]).
  - `Q37`: Circular motion kinematics ($v = 6.28\text{ m/s}, a_c = 78.9\text{ m/s}^2$ [C]).
  - `Q38`: Hydrostatic paradox pressure and thrust ($P_A=P_B=P_C, F_A=F_B=F_C$ [D]).
  - `Q39`: Concave mirror ant image motion (Only S3 is correct [C]).
  - `Q40`: Non-unit of electric current ($\text{V}/(\text{C}\cdot\text{m})$ [D]).
  - `Q41`: Mass-energy equivalence of 1 u ($931\text{ MeV}$ [C]).
  - `Q42`: Tetrahedral resistor network equivalent resistance ($R_{\text{eq}} = 6\,\Omega$ [D]).
  - `Q43`: Momentum ratio for equal kinetic energies ($p_1:p_2 = 1:2$ [B]).
  - `Q44`: Electromagnetic induction Lenz's law cases (Cases i, ii, iv [D]).
  - `Q45`: Kettle filament dimensional scaling ($t' = 3\text{ min}$ [C]).
  - `Q46`: Train wagon uniform retardation stopping ratio ($d_1/d_2 = 1/2$ [B]).
  - `Q47`: Myopic far point correction lens power ($P = -0.4\text{ D}$ [D]).
  - `Q48`: Surface gravitational acceleration ratio ($g_1:g_2 = 2:1$ [B]).
- **Multiple Correct (Q57–Q60):**
  - `Q57`: Convex lens conjugate foci ($u = 15\text{ cm}$ or $60\text{ cm}$, magnified/diminished; [A, B, C, D]).
  - `Q58`: Circuit with real voltmeter ($R_V = 6\text{ k}\Omega$; $V = 8\text{ V}, I = 6\text{ mA}, P = 24\text{ mW}$; [A, C, D]).
  - `Q59`: Moving train whistle echo ($t = 20/3\text{ s} = 1/9\text{ min}, d' = 1000\text{ m}, \lambda = 60\text{ cm}$; [A, B, C, D]).
  - `Q60`: Athletes velocity-time graphs (Equal distances $= 5.0\text{ km}$, Dinesh $a = 40\text{ km/h}^2$; [B, C]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody files in `workspace/sources/nsejs/`.
- **Test Suite:** `tests/test_nsejs_2024_physics.py` (21 passed).

### Chemistry: `nsejs-2024-chemistry-r1` (20 items: `NSEJS-2024-C-Q17` to `Q32`, `Q53` to `Q56`)
- **Single Correct (Q17–Q32):**
  - `Q17`: Milk density mixture ($\rho_{\text{skim}} = 1038.96\text{ kg/m}^3$ [C]).
  - `Q18`: Sodium nitrate mass calculation ($m = 12.94\text{ g}$ [D]).
  - `Q19`: Geminal diiodide tetrahedral chord length ($d = 3.43\text{ \AA}$ [D]).
  - `Q20`: Periodic trends in oxides (Official key DROP; retained for study [D]).
  - `Q21`: Electron gas moles per kilogram ($[100 / (6.02 \times 9.11)] \times 10^6\text{ mol}$ [B]).
  - `Q22`: Carbon-12 Coulombic force excess electron ratio ($4.15 \times 10^{-14}$ [A]).
  - `Q23`: Periodic properties column matching (D, D, B, A [A]).
  - `Q24`: Fahrenheit to Celsius fever conversion ($102.6^\circ\text{F} = 39.2^\circ\text{C}$ [C]).
  - `Q25`: Pure water auto-ionisation at $70^\circ\text{C}$ (pH decreases, neutral [D]).
  - `Q26`: Hydronium concentration from pH 8.26 ($5.5 \times 10^{-9}\text{ M}$ [C]).
  - `Q27`: Geometrical isomer boiling points ($T_A < T_B$ [A]).
  - `Q28`: Material intrinsic tensile strength (Graphene [C]).
  - `Q29`: Group 13 inert pair effect ($\text{B}^{3+}, \text{Tl}^+$ [C]).
  - `Q30`: Automobile airbag propellant ($\text{NaN}_3$ [A]).
  - `Q31`: Paramagnetic MRI contrast agent ($\text{Gd}$ [B]).
  - `Q32`: Fischer esterification $^{18}\text{O}$ labelling (Carbonyl oxygen [B]).
- **Multiple Correct (Q53–Q56):**
  - `Q53`: Medicinal colloids (Argyrol, Sulfur sol, Milk of magnesia; [A, B, C]).
  - `Q54`: Nitrogen reduction processes ($\text{NO}_2 \to \text{NO}_2^-$, $\text{NO}_3^- \to \text{NH}_4^+$; [C, D]).
  - `Q55`: Phosphorus oxyacid basicity ($x = 2$, monobasic, reducing agent; [A, D]).
  - `Q56`: Scandium electronic configuration ($1\text{ unpaired}, 1\text{ }d\text{-electron}, 12\text{ }p\text{-electrons}$; [A, B, C]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody files in `workspace/sources/chem/`.
- **Test Suite:** `tests/test_nsejs_2024_chemistry.py` (16 passed).

### Biology: `nsejs-2024-biology-r1` (20 items: `NSEJS-2024-B-Q01` to `Q16`, `Q49` to `Q52`)
- **Single Correct (Q01–Q16):**
  - `Q01`: Metamerism first evolutionary appearance (Annelida [D]).
  - `Q02`: Human evolution fossil stages (Australopithecus and Homo habilis [C]).
  - `Q03`: Brain functional centres (Hypothalamus, Cerebellum, Cerebrum, Pons [B]).
  - `Q04`: Systemic insecticide for sap-sucking insects (Metasystox [C]).
  - `Q05`: Atlanto-axial joint morphology (Pivot joint [A]).
  - `Q06`: Zoological structures matching (Hexacanth, Renette, Respiratory tree, Piloerectum [C]).
  - `Q07`: Openings between tympanic cavity and auditory capsule (Fenestra ovalis and rotunda [D]).
  - `Q08`: Bharat Stage emission norms in India (BS-VI [A]).
  - `Q09`: Phenylalanine-tyrosine inborn metabolic errors (PKU, Tyrosinosis, Alkaptonuria, Albinism [A]).
  - `Q10`: Plant morphology matching (Wheat, Banyan, Banana, Pine [C]).
  - `Q11`: Chromatin nucleosome histone types (5 types: H1, H2A, H2B, H3, H4 [C]).
  - `Q12`: Scotopic retinal rod photoreceptor adaptation (Both A and R true, R explains A [A]).
  - `Q13`: Anther microsporangium ploidy levels (Haploid, diploid, polyploid: 3 levels [D]).
  - `Q14`: Water column cohesive tensile strength ($100\text{ to }350\text{ atm}$ [A]).
  - `Q15`: Hypertrichosis pinnae auris inheritance (Holandric Y-linked gene [C]).
  - `Q16`: Stratospheric ozone protection treaty (Montreal Protocol [B]).
- **Multiple Correct (Q49–Q52):**
  - `Q49`: Edible seed arils (Litchi, Rambutan, Nutmeg; [A, B, D]).
  - `Q50`: Incorrect statements regarding viruses (Envelope glycolipid-only, all dsDNA; [C, D]).
  - `Q51`: Biflagellate algal classes (Phaeophyta, Chlorophyta; [B, C]).
  - `Q52`: Immune defenses (Immunoglobulins glycoproteins, cilia, histamine; [A, C, D]).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody files in `workspace/sources/bio/`.
- **Test Suite:** `tests/test_nsejs_2024_biology.py` (17 passed).

---

## 4. Quality Gate & Invariant Compliance

Strict compliance verified across all 212 items and 37 test suites:
- **Gate 1 (Zero Ghost Text):** 0 occurrences of `"2. Connection:"` across all modules.
- **Gate 2 (Dynamic Crux Move):** Bound to `M2` or `M3` with strategy matching.
- **Gate 3 (Rubric Bounds):** $c_i \in \{0, 1, 2\}$ with $\sum c_i = \text{score}$.
- **Gate 4 (Canonical Verbs):** Strictly within $\{ \text{RETRIEVE}, \text{EXPLAIN}, \text{APPLY}, \text{MODEL}, \text{REPRESENT}, \text{SYNTHESIZE}, \text{JUSTIFY} \}$.
- **Gate 5 (Commitment-First Derivations):** `style="display: none;"` until user commits answer.
- **Gate 6 (Mobile Cascade):** Base container styles precede `@media (max-width: 600px)` in CSS.
- **Gate 7 (W3C Typography):** $\ge 14\text{px}$ text on responsive SVG views.
- **Rule 13 Invariant (`AGENTS.md`):** *"No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized."*
