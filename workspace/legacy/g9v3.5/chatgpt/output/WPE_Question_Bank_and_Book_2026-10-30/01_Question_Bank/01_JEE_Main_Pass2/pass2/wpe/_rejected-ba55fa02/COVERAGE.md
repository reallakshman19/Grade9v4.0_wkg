# JEE Main Tile Validation Coverage Matrix: Work-Energy-Power (Pass 2)

Source Spine: `D:\CodeD\g9v3.5\wpe-pilot\syllabus\WPE-SPINE.md`
Artifact JSON: `jee-main-wpe-ba55fa02.json` (SHA-256: `ba55fa02cfb94e6311d0d315a6a9d980a7a2f3ee011f579b8f171e75c727e973`)

## 1. Coverage Matrix (IDs Only)

| Key Idea | Node | Title | Total Qs | D Bands (D1/D2/D3/D4) | G9 Flags (Solv/Given/Beyond) | Tile Test (Cov/Part/NotCov/Pend) | Gap? | Question IDs |
|---|---|---|---|---|---|---|---|---|
| WEP-01 | WPE-N01 | Work & dot product | 1 | 0/1/0/0 | 1/0/0 | 0/0/0/1 | NO | JEE-2025-04-04-S2-Q07 |
| WEP-02 | WPE-N02 | Variable-force work, spring | 2 | 1/1/0/0 | 1/0/1 | 0/0/0/2 | NO | JEE-2025-01-23-S1-Q10, JEE-2023-01-24-S1-Q05 |
| WEP-03 | WPE-N03 | Work-energy theorem | 2 | 1/0/1/0 | 2/0/0 | 0/0/0/2 | NO | JEE-2025-04-06-S1-Q03, JEE-2023-04-08-S2-Q03 |
| WEP-04 | WPE-N05 | Path independence | 2 | 2/0/0/0 | 2/0/0 | 0/0/0/2 | NO | JEE-2025-04-07-S2-Q05, JEE-2025-01-22-S2-Q02 |
| WEP-05 | WPE-N06 | Gravitational and elastic PE | 0 | 0/0/0/0 | 0/0/0 | 0/0/0/0 | **GAP** | — |
| WEP-06 | WPE-N07 | F = -dU/dx | 2 | 1/1/0/0 | 1/1/0 | 0/0/0/2 | NO | JEE-2024-01-29-S1-Q02, JEE-2025-01-21-S1-Q01 |
| WEP-07 | WPE-N08 | Conservation and turning points | 2 | 0/1/1/0 | 1/1/0 | 1/1/0/0 | NO | JEE-2025-01-28-S1-Q09, JEE-2024-01-29-S2-Q04 |
| WEP-08 | WPE-N10 | Power | 3 | 0/2/1/0 | 1/1/1 | 0/0/0/3 | NO | JEE-2025-01-29-S2-Q08, JEE-2025-04-07-S1-Q06, JEE-2023-04-06-S2-Q01 |
| WEP-09 | WPE-N09 | Friction work | 2 | 1/1/0/0 | 2/0/0 | 0/0/0/2 | NO | JEE-2024-01-29-S1-Q03, JEE-2024-04-05-S2-Q04 |
| WEP-10 | WPE-N04 | Momentum vs KE relation | 3 | 2/1/0/0 | 3/0/0 | 0/0/0/3 | NO | JEE-2024-01-27-S1-Q01, JEE-2023-04-08-S1-Q02, JEE-2023-04-08-S2-Q04 |

## 2. Revisit List (Cards for Oracle / OTM)

| Tile | Current File | Affected Questions | Status | Proposed Change |
|---|---|---|---|---|
| WEP-07 | `wep07-core1ab-d04e98dc.json` | JEE-2024-01-29-S2-Q04 | PARTIAL | Widen the shared inferential jump beyond strictly conservative motion intervals to explicitly include proportional / fractional non-conservative dissipation: E_f = (1 - \eta) E_i (or delegate non-conservative losses to WEP-03). |

## 3. Core2 Candidates (D3/D4 Officially Confirmed)

| Question ID | Key Idea | Demand | Band | G9 Flag | Official Paper Shift | Locator |
|---|---|---|---|---|---|---|
| JEE-2025-01-28-S1-Q09 | WEP-07 | SYNTHESIZE | D3 | G9_WITH_GIVEN | JEE Main 2025 Session 1, Shift 1 (2025-01-28 Morning) | Page 7, Item 19 (vertical circular hoop with bottom spring anchor) |
| JEE-2025-01-29-S2-Q08 | WEP-08 | MODEL | D3 | G9_WITH_GIVEN | JEE Main 2025 Session 1, Shift 2 (2025-01-29 Evening) | Page 11, Item 24 (sand conveyor belt) |
| JEE-2023-04-08-S2-Q03 | WEP-03 | SYNTHESIZE | D3 | G9_SOLVABLE | JEE Main 2023 Session 2, Shift 2 (2023-04-08 Evening) | Page 9, Section B Item 22 (bullet embedded in rough block) |
