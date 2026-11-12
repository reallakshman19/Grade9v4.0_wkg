# JEE Main Tile Validation Coverage Matrix: Work-Energy-Power (Pass 2)

Source Spine: `D:\CodeD\g9v3.5\wpe-pilot\syllabus\WPE-SPINE.md`
Artifact JSON: `jee-main-wpe-4ac47110.json` (SHA-256: `4AC471104F938A0876157DD606F13C30C2A6FB8A0B056C52FDC536F24B0F81CE`)

## 1. Coverage Matrix (IDs Only)

| Key Idea | Node | Title | Total Qs | D Bands (D1/D2/D3/D4) | G9 Flags (Solv/Given/Beyond) | Tile Test (Cov/Part/NotCov/Pend) | Gap? | Question IDs |
|---|---|---|---|---|---|---|---|---|
| WEP-01 | WPE-N01 | Work & dot product | 1 | 0/1/0/0 | 1/0/0 | 1/0/0/0 | NO | JEE-2026-04-04-S1-Q46 |
| WEP-02 | WPE-N02 | Variable-force work, spring | 1 | 0/1/0/0 | 1/0/0 | 0/1/0/0 | NO | JEE-2026-04-06-S2-Q29 |
| WEP-03 | WPE-N03 | Work-energy theorem | 1 | 0/1/0/0 | 1/0/0 | 0/0/0/1 | NO | JEE-2026-04-06-S1-Q28 |
| WEP-04 | WPE-N05 | Path independence | 0 | 0/0/0/0 | 0/0/0 | 0/0/0/0 | **GAP** | — |
| WEP-05 | WPE-N06 | Gravitational and elastic PE | 1 | 0/0/1/0 | 0/1/0 | 0/0/0/1 | NO | JEE-2026-04-02-S2-Q31 |
| WEP-06 | WPE-N07 | F = -dU/dx | 0 | 0/0/0/0 | 0/0/0 | 0/0/0/0 | **GAP** | — |
| WEP-07 | WPE-N08 | Conservation and turning points | 1 | 0/0/1/0 | 0/1/0 | 1/0/0/0 | NO | JEE-2026-04-02-S2-Q31 |
| WEP-08 | WPE-N10 | Power | 1 | 0/1/0/0 | 0/1/0 | 0/0/0/1 | NO | JEE-2026-04-04-S1-Q49 |
| WEP-09 | WPE-N09 | Friction work | 1 | 0/0/1/0 | 1/0/0 | 0/0/0/1 | NO | JEE-2026-04-05-S2-Q28 |
| WEP-10 | WPE-N04 | Momentum vs KE relation | 0 | 0/0/0/0 | 0/0/0 | 0/0/0/0 | **GAP** | — |

## 2. Revisit List (Cards for Oracle / OTM)

| Tile | Current File | Affected Questions | Status | Proposed Change |
|---|---|---|---|---|
| WEP-02 | `wep02-core1ab-a74b883f.json` | JEE-2026-04-06-S2-Q29 | PARTIAL | Widen the jump or add a cross-reference note indicating that work done by a position-dependent force/velocity \(v(x)\) can be evaluated directly via boundary kinetic energies \(W = \Delta K\) without explicit force integration or graph quadrature. |

## 3. Core2 Candidates (D3/D4 Officially Confirmed)

| Question ID | Key Idea | Demand | Band | G9 Flag | Official Paper Shift | Locator |
|---|---|---|---|---|---|---|
| JEE-2026-04-02-S2-Q31 | WEP-07 / WEP-05 | MULTISTEP_REASONING | D3 | G9_WITH_GIVEN | JEE Main 2026 Session 2, Shift 2 (2026-04-02 Evening) | Page 12, Item 31, Section A |
| JEE-2026-04-05-S2-Q28 | WEP-09 | MULTISTEP_REASONING | D3 | G9_SOLVABLE | JEE Main 2026 Session 2, Shift 2 (2026-04-05 Evening) | Page 11, Item 28, Section A |
