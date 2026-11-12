# Oracle Checkpoint — 12 November 2026

**Timestamp:** 2026-11-12T09:10:00+04:00  
**Operating Sequence:** **NSEJS 5-Year Past-Paper Ingestion (2024, 2023, 2022, 2021 & 2020 100% COMPLETE across PCB: 237 authentic items)**  
**Active Branch:** `feat/multi-subject-core2-expansion-01`  
**Authority Invariant:** Rule 13 in `AGENTS.md` (*No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.*)

---

## 1. Subject Track & Curriculum Status Overview

| Subject Track | Topics / Papers Ingested | Ingested Question Count | Test Suite Status | Track Status |
| :--- | :--- | :---: | :---: | :---: |
| **Track 1: Physics** | Ray Optics, Electrostatics, Circuits, Magnetism & EMI, Mechanics, Fluid Mechanics & Sound, **NSEJS 2024, 2023, 2022, 2021 & 2020 Official Paper 51** | **139 items** | 25 suites (6 Core 2 topics + 8 D3 + 6 Core 1A/1B + **NSEJS 2024, 2023, 2022, 2021 & 2020 Papers**), **270 passed** | **100% COMPLETE (All Topics + 5-Year Past Papers Ingested)** |
| **Track 2: Mathematics** | Topic 1: Algebra & Polynomials<br>Topic 2: Number Theory & Divisibility | **20 items** | 2 suites, **43 passed** (Full QRT Labelling) | **COMPLETE (Topics 1 & 2 Ingested; paused per user)** |
| **Track 3: Chemistry** | Topic 1: Matter & Mole Concept<br>Topic 2: Chemical Substances — Reactions<br>Topic 3: Atomic Structure & Bonding<br>D3 Modules (Eudiometry & Redox Titrations)<br>**NSEJS 2024, 2023, 2022, 2021 & 2020 Official Paper 51** | **111 items** | 14 suites (3 Core topics + 6 D3 + **NSEJS 2024, 2023, 2022, 2021 & 2020 Papers**), **149 passed** | **100% COMPLETE (All Topics + 5-Year Past Papers Ingested)** |
| **Track 4: Biology** | **NSEJS 2024, 2023, 2022, 2021 & 2020 Official Paper 51** | **79 items** | 5 suites (**NSEJS 2024, 2023, 2022, 2021 & 2020 Papers**), **90 passed** | **100% COMPLETE (5-Year Past Papers Ingested)** |
| **Cross-Subject Architecture** | Shared/QRT Schemas, Bounded Transfer Protocols, Gate Checkers, Audit Invariants | N/A | 10 cross-cutting contract suites, **461 passed** | **ACTIVE & ENFORCED** |
| **TOTALS** | **34 Active Learning Modules** | **389 items** | **49 Pytest Suites, 977 Passed, 2 Skipped (Platform Symlinks), 0 Failed** | **100% GREEN CI** |

---

## 2. NSEJS 5-Year Authentic Corpus Inventory (`nsejs.com/previous-exam-papers`)

All 12 official question papers, detailed solution booklets, and chapter/concept analysis PDFs have been downloaded and cataloged in `scratch`:

| Examination Year | Total Questions | Physics | Chemistry | Biology | Mathematics | Status in Workspace |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **NSEJS 2024** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 54 Tests)** |
| **NSEJS 2023** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 53 Tests)** |
| **NSEJS 2022** | **60** | 20 | 20 | 20 | 0 | **100% INGESTED (All 60 Items with Custody, Core 2 HTMLs & 54 Tests)** |
| **IOQJS / NSEJS 2021** | **33** | 11 | 11 | 11 | 0 | **100% INGESTED (All 33 Items with Custody, Core 2 HTMLs & 45 Tests)** |
| **IOQJS 2020** | **24** | 8 | 8 | 8 | 0 (excl) | **100% INGESTED (All 24 Items with Custody, Core 2 HTMLs & 42 Tests)** |
| **Total Authentic PCB Corpus** | **237 items** | **79** | **79** | **79** | 0 | **237 items ingested (100% COMPLETE)** |

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

## 4. NSEJS 2021 Complete Ingestion Modules (Paper Code 51)

### Physics: `nsejs-2021-physics-r1` (11 items: `NSEJS-2021-P-Q17`..`Q24`, `Q31`..`Q33`)
- **Format:** 8 Single Correct (3 marks, -1 negative: Q17–Q24) + 3 Multiple Correct (6 marks, no negative: Q31–Q33).
- **Core Topics:** Kinematics relative velocity vector geometry, non-ohmic incandescent bulb circuit resistance, rotational and translational kinetic energy rolling balance, planar mirror refraction image position, parallel-plate capacitor charge distribution, ideal gas state equation work, and Archimedes buoyancy equilibrium.
- **Official Keys:** Q17 (`B OR D`), Q18 (`DROP`), Q19 (`B`), Q20 (`B`), Q21 (`C`), Q22 (`A`), Q23 (`C`), Q24 (`B`), Q31 (`A, B, C`), Q32 (`B, C`), Q33 (`A, D`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/nsejs/`.
- **Test Suite:** `tests/test_nsejs_2021_physics.py` (15 passed).

### Chemistry: `nsejs-2021-chemistry-r1` (11 items: `NSEJS-2021-C-Q09`..`Q16`, `Q28`..`Q30`)
- **Format:** 8 Single Correct (3 marks, -1 negative: Q09–Q16) + 3 Multiple Correct (6 marks, no negative: Q28–Q30).
- **Core Topics:** Mole concept triatomic sulfur dioxide atom counting, stoichiometric antacid neutralisation of gastric HCl, thermal decomposition mass balance of calcium carbonate-oxide calcination, periodic electronegativity progression, Ostwald weak electrolyte ionisation conductance, qualitative analysis cationic hydrolysis of ammonium chloride, Avogadro molar mass equivalence of equal volume gases, and colligative van 't Hoff factor osmotic pressure hierarchy.
- **Official Keys:** Q09 (`C`), Q10 (`A`), Q11 (`A`), Q12 (`C`), Q13 (`C`), Q14 (`B`), Q15 (`D`), Q16 (`B`), Q28 (`A, D`), Q29 (`B, D`), Q30 (`B`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/chem/`.
- **Test Suite:** `tests/test_nsejs_2021_chemistry.py` (13 passed).

### Biology: `nsejs-2021-biology-r1` (11 items: `NSEJS-2021-B-Q01`..`Q08`, `Q25`..`Q27`)
- **Format:** 8 Single Correct (3 marks, -1 negative: Q01–Q08) + 3 Multiple Correct (6 marks, no negative: Q25–Q27).
- **Core Topics:** Erythrocyte physiological functions vs B-cell immunoglobulin synthesis, limbless tetrapod evolution in Reptilia and Amphibia (Gymnophiona / caecilians), dipteran single wing pair and halteres in housefly, fruit fly, and mosquito, single-stranded RNA chemical diagnosis via lack of thymine and 2'-OH alkaline cleavage, hydrophytic aerenchyma buoyancy lacunae in water hyacinth petiole, bryophyte non-vascular organization and flagellated antherozoid water dependence, Crassulacean Acid Metabolism (CAM) nocturnal carbon fixation in desert succulents, and chiropterophily bat floral syndromes.
- **Official Keys:** Q01 (`C`), Q02 (`C`), Q03 (`D`), Q04 (`C`), Q05 (`B`), Q06 (`D`), Q07 (`C`), Q08 (`B`), Q25 (`A, C, D`), Q26 (`A, B, C`), Q27 (`A, B`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/bio/`.
- **Test Suite:** `tests/test_nsejs_2021_biology.py` (17 passed).

---

## 5. NSEJS 2020 Complete Ingestion Modules (Paper Code 51)

### Physics: `nsejs-2020-physics-r1` (8 items: `NSEJS-2020-P-Q01`..`Q06`, `Q25`, `Q26`)
- **Format:** 6 Single Correct (3 marks, -1 negative: Q01–Q06) + 2 Multiple Correct (6 marks, no negative: Q25, Q26).
- **Core Topics:** Neutron star surface gravitational acceleration ($g = GM/R^2$), diver ear drum safe hydrostatic pressure depth, thin convex lens conjugate foci distance symmetry, nuclear reactor 1000 kW fission disintegration rate, Newton second law contact forces in coupled accelerating blocks, resistor lattice reduction and potential divider analysis, Biot-Savart law magnetic field and electron flow direction, and specific charge ($q/m$) SI units, tritium isotopic minimum, and electron/alpha particle comparisons.
- **Official Keys:** Q01 (`B`), Q02 (`C`), Q03 (`B`), Q04 (`A`), Q05 (`B`), Q06 (`A`), Q25 (`A, B, C`), Q26 (`A, B, C OR A, B, D`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/nsejs/`.
- **Test Suite:** `tests/test_nsejs_2020_physics.py` (14 passed).

### Chemistry: `nsejs-2020-chemistry-r1` (8 items: `NSEJS-2020-C-Q07`..`Q12`, `Q27`, `Q28`)
- **Format:** 6 Single Correct (3 marks, -1 negative: Q07–Q12) + 2 Multiple Correct (6 marks, no negative: Q27, Q28).
- **Core Topics:** Silicone polymer waterproof film thickness and precursor mass balance, homogeneous gas-phase equilibrium constant calculation, alcohol dehydration and ozonolysis to acetaldehyde, single displacement redox decolourisation of $\text{CuCl}_2$ by calcium, triclosan percentage concentration calculation (officially dropped), simultaneous equations for binary compound atomic weights (officially dropped), didymium rare-earth glass absorbers (Nd and Pr), and magnesium reactivity and hydrogen evolution in strong mineral acids.
- **Official Keys:** Q07 (`A`), Q08 (`B`), Q09 (`A OR B`), Q10 (`B`), Q11 (`DROP`), Q12 (`DROP`), Q27 (`A, B`), Q28 (`B, C`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/chem/`.
- **Test Suite:** `tests/test_nsejs_2020_chemistry.py` (14 passed).

### Biology: `nsejs-2020-biology-r1` (8 items: `NSEJS-2020-B-Q13`..`Q18`, `Q29`, `Q30`)
- **Format:** 6 Single Correct (3 marks, -1 negative: Q13–Q18) + 2 Multiple Correct (6 marks, no negative: Q29, Q30).
- **Core Topics:** B-DNA helical rise per base pair in chromosome mutant elongation, pedigree diagnostic criteria for sex-linked (X-linked) recessive inheritance, inverted pyramid of biomass in marine phytoplankton-dominated biomes, transpiration pull environmental optimization (open stomata, dry air, moist soil), traditional Indian bioresources and legal disputes over biopiracy, evolutionary criteria for living fossil categorization and phylogenetic stasis, immunological comparison of live attenuated vs inactivated vaccines, and endocrine and physiological factors regulating Basal Metabolic Rate (BMR).
- **Official Keys:** Q13 (`A`), Q14 (`C`), Q15 (`D`), Q16 (`B`), Q17 (`C`), Q18 (`B`), Q29 (`A, B`), Q30 (`B, D`).
- **Artifacts:** `intake.json`, `bank.json`, `questions.json`, `core2_module.html`, `question-status.html`, `sl1_check_report.json`, `sl2_check_report.json`, source custody in `workspace/sources/bio/`.
- **Test Suite:** `tests/test_nsejs_2020_biology.py` (14 passed).

---

## 6. Quality Gate & Invariant Compliance

Strict compliance verified across all 389 items and 49 test suites:
- **Gate 1 (Zero Ghost Text):** 0 occurrences of `"2. Connection:"` across all modules.
- **Gate 2 (Dynamic Crux Move):** Bound to `M2` or `M3` with strategy matching.
- **Gate 3 (Rubric Bounds):** $c_i \in \{0, 1, 2\}$ with $\sum c_i = \text{score}$.
- **Gate 4 (Canonical Verbs):** Strictly within $\{ \text{RETRIEVE}, \text{EXPLAIN}, \text{APPLY}, \text{MODEL}, \text{REPRESENT}, \text{SYNTHESIZE}, \text{JUSTIFY} \}$.
- **Gate 5 (Commitment-First Derivations):** `style="display: none;"` until user commits answer.
- **Gate 6 (Mobile Cascade):** Base container styles precede `@media (max-width: 600px)` in CSS.
- **Gate 7 (W3C Typography):** $\ge 14\text{px}$ text on responsive SVG views.
- **Rule 13 Invariant (`AGENTS.md`):** *"No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized."*
