# Oracle Checkpoint — 11 November 2026

**Timestamp:** 2026-11-11T19:30:00+04:00  
**Operating Sequence:** **Physics (100% COMPLETE: Core 2 + Core 1A/1B) $\to$ Mathematics (Topics 1 & 2 COMPLETE) $\to$ Chemistry (Topics 1 & 2 COMPLETE: Sections I & II) $\to$ Biology**  
**Active Branch:** `feat/chem-matter-reactions-intake-01`  
**Authority Invariant:** Rule 13 in `AGENTS.md` (*No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.*)

---

## 1. Subject Track & Curriculum Status Overview

| Subject Track | Topics Ingested | Ingested Question Count | Test Suite Status | Track Status |
| :--- | :--- | :---: | :---: | :---: |
| **Track 1: Physics** | Ray Optics, Electrostatics, Circuits, Magnetism & EMI, Mechanics | **50 items** | 10 suites (Core 2 + Core 1), 106 passed | **100% COMPLETE (Full Loop)** |
| **Track 2: Mathematics** | Topic 1: Algebra & Polynomials<br>Topic 2: Number Theory & Divisibility | **20 items** | 2 suites, 43 passed (Full QRT Labelling) | **COMPLETE (Topics 1 & 2 Ingested)** |
| **Track 3: Chemistry** | Topic 1: Section I (Matter, Solutions & Mole Concept)<br>Topic 2: Section II (Chemical Substances — Nature & Behaviour) | **20 items** | 2 suites, 46 passed (Full QRT Labelling) | **SECTIONS I & II COMPLETE** |
| **Track 4: Biology** | Living World, Life Processes, Environment, Resources, Food | 0 items | — | Next on deck |
| **Active Test Suites** | **9 Distinct Subject/Topic Modules** | **90 items** | **14 suites, 213 passed** | **Active Pipeline** |

---

## 2. Chemistry Track: Topic 2 (Section II: Chemical Substances — Nature & Behaviour)

- **Anchor Item:** `CHEM-NSEJS-REACT-01`
  - **Stem:** A pure metal oxide sample containing $1.02\text{ g}$ of $M_2\text{O}_3$ reacts completely with excess aqueous $\text{NaOH}$ to yield $1.64\text{ g}$ of anhydrous sodium meta-metalate ($\text{Na}M\text{O}_2$). The same oxide dissolves in $0.50\text{ M } \text{HCl}$ to form $M\text{Cl}_3$. Evaluates metal identity $M$ and required volume of $0.50\text{ M } \text{HCl}$.
  - **Operation:** `MODEL` (Band D2, Score 4). Crux move dynamically bound to `CHEM-NSEJS-REACT-01-M2`.
  - **Resolution:** Reaction with $\text{NaOH}$: $M_2\text{O}_3 + 2\text{NaOH} \to 2\text{Na}M\text{O}_2 + \text{H}_2\text{O}$. Molar masses: $M_2\text{O}_3 = 2A + 48.0\text{ g/mol}$; $\text{Na}M\text{O}_2 = A + 55.0\text{ g/mol}$. Mole ratio yields $A = 27.0\text{ u}$, identifying metal $M$ as Aluminium ($\text{Al}$). Reaction with $\text{HCl}$: $\text{Al}_2\text{O}_3 + 6\text{HCl} \to 2\text{AlCl}_3 + 3\text{H}_2\text{O}$. Moles of oxide $= 0.010\text{ mol} \implies 0.060\text{ mol } \text{HCl} \implies V = 0.060 / 0.50 = 0.120\text{ L} = 120\text{ mL}$ (Option B).
- **10 Ingested Items with Strict QRT Rubric Labelling:**
  1. `CHEM-NSEJS-REACT-01`: Amphoteric Oxides & Stoichiometric Neutralization ($M=\text{Al}, V=120\text{ mL}$) [`MODEL`, `D2`, Score 4, Crux: `M2`]
  2. `CHEM-NSEJS-REACT-02`: Activity Series & Metal Displacement Reactions ($Q > P > S > R$; Metal $Q$) [`JUSTIFY`, `D1`, Score 2, Crux: `M2`]
  3. `CHEM-NSEJS-REACT-03`: Redox Stoichiometry & Nitric Acid Oxidation ($3\text{Cu} + 8\text{HNO}_3$, Ratio $3:2$, Sum 20) [`SYNTHESIZE`, `D2`, Score 4, Crux: `M2`]
  4. `CHEM-NSEJS-REACT-04`: Acid-Base Neutralization & Mixture pH ($100\text{ mL } 0.10\text{ M } \text{HCl} + 100\text{ mL } 0.08\text{ M } \text{NaOH} \implies \text{pH} = 2.00$) [`APPLY`, `D2`, Score 3, Crux: `M2`]
  5. `CHEM-NSEJS-REACT-05`: Chemistry of Salts & Water of Crystallization ($17.20\text{ g Gypsum} \to 14.50\text{ g POP} + 2.70\text{ g } \text{H}_2\text{O}$) [`MODEL`, `D2`, Score 4, Crux: `M2`]
  6. `CHEM-NSEJS-REACT-06`: Baking Soda Thermal Decomposition ($16.80\text{ g } \text{NaHCO}_3 \to 10.60\text{ g } \text{Na}_2\text{CO}_3 + 2.24\text{ L } \text{CO}_2$) [`APPLY`, `D2`, Score 3, Crux: `M2`]
  7. `CHEM-NSEJS-REACT-07`: Carbon Compounds — Hydrocarbon Isomers & Combustion ($2\text{ isomers}, 14.56\text{ L } \text{O}_2$) [`MODEL`, `D2`, Score 4, Crux: `M2`]
  8. `CHEM-NSEJS-REACT-08`: Functional Groups & Esterification Yield ($6.00\text{ g Acid} + 4.60\text{ g Alcohol} \to 6.60\text{ g Ester}$) [`SYNTHESIZE`, `D2`, Score 4, Crux: `M2`]
  9. `CHEM-NSEJS-REACT-09`: Periodic Table — Isoelectronic Species Radii ($\text{Mg}^{2+} < \text{Na}^+ < \text{F}^- < \text{O}^{2-}$) [`EXPLAIN`, `D1`, Score 2, Crux: `M2`]
  10. `CHEM-NSEJS-REACT-10`: Periodic Trends & First Ionization Energy Anomalies ($\text{Li} < \text{B} < \text{Be} < \text{C} < \text{O} < \text{N} < \text{F} < \text{Ne}$) [`JUSTIFY`, `D2`, Score 4, Crux: `M3`]
- **Custody Packet:** [`workspace/sources/chem/CHEM-NSEJS-REACT-01/`](file:///D:/CodeD/grade9v4/workspace/sources/chem/CHEM-NSEJS-REACT-01/) (`source_item.json`, `source-custody.json`).
- **Module Assets:** [`workspace/output/chem-chemical-substances-r1/`](file:///D:/CodeD/grade9v4/workspace/output/chem-chemical-substances-r1/) (`intake.json`, `bank.json`, `sl1_check_report.json`, `sl2_check_report.json`, `questions.json`, `core2_module.html`, `question-status.html`).
- **Interactive Module:** Featuring W3C SVG typography ($\ge 14\text{px}$) of the amphoteric oxide dual alkaline/acid dissolution pathways and commitment-first protected derivation.
- **Verification Suite:** [`tests/test_chem_chemical_substances.py`](file:///D:/CodeD/grade9v4/tests/test_chem_chemical_substances.py) — **23 passed in 0.15s**.

---

## 3. Seven Anti-Patterns Quality Gate Compliance

Strict compliance verified across all modules:
- **Gate 1 (Zero Ghost Text):** 0 occurrences of `"2. Connection:"` or `"Connection:"`.
- **Gate 2 (Dynamic Crux Move):** Crux references bound to primary cognitive operation.
- **Gate 3 (Rubric Sum Bounds):** $c_i \in \{0, 1, 2\}$ with $\sum c_i = \text{score}$ across all 20 chemistry questions.
- **Gate 4 (Canonical Verbs Only):** Primary operations strictly use $\{ \text{RETRIEVE}, \text{EXPLAIN}, \text{APPLY}, \text{MODEL}, \text{REPRESENT}, \text{SYNTHESIZE}, \text{JUSTIFY} \}$.
- **Gate 5 (W3C SVG Typography):** `font-size >= 14px` on all text, responsive viewBox, root `width="100%" height="100%"`.
- **Gate 6 (Responsive Mobile Cascade):** `max-width 900px`, mobile-safe.
- **Gate 7 (Commitment-First Protected Derivations):** `display: none;` until candidate answer is committed.

---

## 4. Verification Results Across Active Test Suites

```powershell
$files = Get-ChildItem tests/test_nsejs_*.py, tests/test_math_*.py, tests/test_chem_*.py | ForEach-Object FullName
python -m pytest $files -v
```
**Topic Suites Result:** `213 passed in 0.64s` (124 Physics + 43 Mathematics + 46 Chemistry)  
**Governance Invariant:** PASS across all modules (`HOLD:ACADEMIC_ADMISSION` / `NOT_ADMITTED`).

---

## 5. Next Steps for Curriculum Sequence

1. **Chemistry Track Phase 3 (Optional Core 1A/1B):** Author Core 1A physical construction and Core 1B reconstruction for chemistry anchors (`CHEM-NSEJS-MOLE-01` and `CHEM-NSEJS-REACT-01`).
2. **Transition to Track 4: Biology Track:**
   - Section III: Organisation in the Living World (Cell structure, tissues, diversity, diseases).
   - Section IV: Life Processes (Nutrition, respiration, excretion, nervous/hormonal control, genetics).
   - Sections VIII–X: Environment, Natural Resources, Food Production.
