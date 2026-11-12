# WPE D3/D4 — source-to-learning bridge (author proposal)

**2026-11-02 · Existing Core1A/Core1B practice is NOT a D3/D4 coverage demonstration.** This folder supplies a missing middle layer between selected difficult question *themes* and the reasoning a child must first learn. These are newly authored instructional proposals, **not** original examination questions, QRT findings, native academic admissions, or a new learner webpage.

## Learner-readiness protocol (not yet conducted)

The existing [eight-skill interactive self-tutor](../../physics/wpe/d3d4-self-tutor.html) now has an [observation protocol](LEARNER_OBSERVATION_PROTOCOL.md) for a supervised student session. This is a **prepared procedure, not a claim of observed outcomes**. The software checks first-attempt persistence, optional hints, available worked reasoning during self-repair, and untouched native admission flags. Any genuine student feedback must be recorded anonymously according to appropriate school/family permission and kept distinct from automated simulations.

## Verified against this repository snapshot

| Item | Observed |
|---|---:|
| R1 pilot places | 21 |
| Pending candidate IDs | 14 |
| Vacant places | 7 |
| Admitted examination items | **0** |
| Pilot candidates whose proposed operation and D-band both match the consolidated review reader | **3** |
| Pilot candidates whose operation or D-band conflicts with the consolidated review reader | **8** |
| Pilot candidate IDs absent from that reader | **3** |

**Important nuance:** eight classification conflicts are *disagreements between two unapproved records*, **not corrected QRT classifications**. `EX-M81`, `EX-M44` and `EX-M60` are absent from the consolidated reader, not necessarily absent from every source package. `WEP07-03` has a substantive D2/D4 and operation conflict; its source/key and original multi-selection nature need separate custody and review. Existing pilot slots are left untouched.

The exact pilot selections and reader classifications are compared side by side in [P0_P1_CONSTRUCTION_BRIDGE.json](P0_P1_CONSTRUCTION_BRIDGE.json). That JSON also pins the Git *blob SHAs* of the four inputs examined. Disagreements remain in an explicit `CONFLICT_IN_READER` state, not an automatically “fixed” classification.

## Eight reusable constructions, not eight exam-question copies

| Priority | Construction | Source-theme link examples | Ready-to-author status |
|---|---|---|---|
| P0 | WPE-C01 · Multi-force work–energy ledger | EX-M105, EX-M24, TB-WPE-ILL-02 | **Full guided + fresh-task author pack** |
| P0 | WPE-C02 · Spring contact and motion phases | EX-M24, TB-WPE-ILL-12, EX-M18 | **Full guided + fresh-task author pack** |
| P0 | WPE-C03 · Constant power and changing speed | EX-M62, EX-M79, EX-M69 | **Full guided + fresh-task author pack** |
| P0 | WPE-C04 · Distributed mass / centre of mass | EX-M73, WEP07-02, TB-WPE-ILL-11 | **Full guided + fresh-task author pack** |
| P0 | WPE-C05 · Graph: area, slope, or time shape | EX-M56, EX-M61, EX-M69 | **Full guided + fresh-task author pack**; original exam graphs still unqualified |
| P0 | WPE-C06 · Vertical circle and contact constraint | EX-M39, EX-N31, EX-M18, EX-M6 | **Full guided + fresh-task author pack** |
| P1 | WPE-C07 · Conveyor and mass flow | EX-M16 | **Full guided + fresh-task author pack** |
| P1 | WPE-C08 · Springs at fixed force vs extension | EX-M101 | **Full guided + fresh-task author pack** |

Source-theme links after the R1 selection are *proposals*, not independently verified operation-level QRT joins. The matrix deliberately avoids claiming that a specific exam stem matches a construction without original-question confirmation.

## Eight usable Core1A/Core1B author packs — six P0 and two P1

- [WPE-C01 — Multi-force ledger](MULTIFORCE_LEDGER_LEARNING_PACK.md): guide = horizontal box with motor pull/friction; genuinely new task = scooter up a ramp requiring motor, friction, gravity and normal-force decisions.
- [WPE-C02 — Spring contact](SPRING_CONTACT_LEARNING_PACK.md): guide = spring launch followed by a smooth region; genuinely new task = spring launch **then a rough strip** with changed equations after loss of contact.
- [WPE-C03 — Constant power](CONSTANT_POWER_LEARNING_PACK.md): guide = 2 kg toy sled, already moving, energy input at fixed power; fresh task = different trolley and power, model the kinetic-energy, speed and distance graph shapes with a changed-power boundary. Optional rest-start (\(s\propto t^{3/2}\)) derivation is explicitly advanced/idealized.
- [WPE-C04 — Hanging chain](DISTRIBUTED_MASS_LEARNING_PACK.md): guide = lift the hanging half of a chain fully onto a table; fresh task = pull a different rope only partway, recomputing both changing hanging masses and centres of mass.
- [WPE-C05 — Graph decisions](GRAPH_OPERATION_LEARNING_PACK.md): guide = one rectangle work graph, one potential slope and one displacement slope; fresh task = a force-area triangle, rising energy line and a piecewise position–time slope, plus a force–time impulse boundary.
- [WPE-C06 — Vertical circle](VERTICAL_CIRCLE_LEARNING_PACK.md): guide = given top speed, calculate tension and bottom speed; fresh task = given bottom speed, use energy **and** top radial-force constraints to detect an impossible negative string tension and test a corrected speed.
- [WPE-C07 — Conveyor momentum and motor power](CONVEYOR_MOMENTUM_POWER_LEARNING_PACK.md): guide = a steady stream of stationary sand caught by a moving belt; fresh task = already-moving wood chips arriving at a **belt-speed-dependent feed rate**, with separate momentum, motor power, kinetic-energy gain and frictional heating.
- [WPE-C08 — Spring energy with different controls](SPRING_CONTROLLED_VARIABLE_LEARNING_PACK.md): guide = compare equal extension against equal final force using known stiffnesses; fresh task = infer **unknown stiffnesses from force/extension observations**, then reconstruct both controlled-variable energy comparisons and a doubled-force test.

All eight author packs contain **six Core1B stages**: Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary test. All reserve a separate independent task with an **author-only worked reference** and an explanation rubric. Those reference answers are in repository documentation only: **do not embed them into a public pre-attempt client bundle or claim secure answer protection from a static page**.

For a student, the essential format is:

> **Before help:** “What do you predict? Draw or describe your model. Solve the new case and explain the decisive decision.”  
> **After the saved attempt:** “Compare each step, find the first model error, repair it, then test one changed physical condition.”

This is more than selecting MCQ options or writing eight arbitrary characters. It permits playful, age-appropriate open reasoning while keeping an honest distinction between guided teaching and independently witnessed reconstruction.

## Eight-pack completion — evidence boundaries

The construction inventory in [P0_P1_CONSTRUCTION_BRIDGE.json](P0_P1_CONSTRUCTION_BRIDGE.json) marks **six P0 and two P1 drafted packs (eight total)** and records independently recalculable numerical answer checks. The included tests independently recompute six numerical answer sets (C03–C08), check all eight guided/challenge documents and exercise the full six-stage structure rather than merely checking that files exist. This does not constitute academic validation, real child testing, or secured answer delivery.

**Grade-9 curriculum caution:** constant-power time/distance calculus, advanced tension analysis and variable-mass momentum-flow energy accounting are scaffolded or labeled as advanced extensions, not assumed prerequisites for every student. Use graph and energy reasoning first. A vertical-circle challenge may require explicit prior teaching of radial acceleration and string constraints; do not label it accessible solely on the basis of the foundational energy lesson.

**Source custody caution:** EX-M56/61/69 original graphs are not qualified by these newly authored example descriptions. Reader and selection conflicts remain exactly as recorded. Nothing in the pack verifies a source figure or official answer key.

## Five targeted D3/D4 extension drafts (WPE-E01–E05)

The earlier eight reusable construction packs are still intact. Five **source-theme extensions** are now separately drafted as child-facing *author specifications*, not inserted into the public student page. Each includes **Core1A guided learning → a distinct Core1B open-response challenge → Predict / Attempt / Reconstruct / Diagnose / Repair / Boundary test → author-only criteria**.

| Extension | Learning decision | Source-theme references | Status |
|---|---|---|---|
| [E01 — Potential wells and reachable regions](POTENTIAL_WELLS_LEARNING_PACK.md) | Decide **which connected regions** satisfy `E ≥ U`; do not confuse a low destination with a passable route | WEP07-03, EX-M109 | Drafted, not admitted |
| [E02 — Instantaneous power](INSTANTANEOUS_POWER_LEARNING_PACK.md) | Use **force along velocity** at that instant rather than magnitude-only multiplication or time-average work | TB-WPE-ILL-05/06 | Drafted, not admitted |
| [E03 — Spring → projectile](SPRING_PROJECTILE_TRANSITION_LEARNING_PACK.md) | Switch model at the **end of spring contact**, then determine horizontal flight and vertical fall separately | EX-N34 | Drafted, not admitted |
| [E04 — Dissipative bounces](DISSIPATIVE_BOUNCES_LEARNING_PACK.md) | Transfer impact **energy-retention fractions** to rebound heights, distinguish speed ratios, and count both travel directions | EX-M82 | Drafted, not admitted |
| [E05 — Radial force and potential energy](RADIAL_FORCE_POTENTIAL_LEARNING_PACK.md) | Use **area under inward-force magnitude versus radius** to find potential, then the **local inward force** for circular speed; distinguish the potential comparison from work along an orbit | EX-M89 | Drafted, not admitted |

**Scope and scientific cautions:**
- **WEP07-03:** its potential/well task has an unresolved operation/demand-band conflict (D2 vs D4). E01 deliberately uses a **different** well with two disconnected accessible regions; no exam source is reclassified.
- **TB-WPE-ILL-05:** the original bottom-power problem omits initial speed. E02 uses fully specified instantaneous speeds and does not infer a missing source condition. Its diagonal-vector question is an advanced supported extension.
- **EX-N34:** the original figure is not independently qualified here. E03 uses **new** horizontal launcher conditions with contact-only friction and a separate flight phase. No substitute drawing is presented as an original image.
- **EX-M82:** E04 uses a *first-impact versus later-impact* retention change; the source's original single retention ratio and predicted answer remain outside the new task.
- **EX-M89 / radial-force potential:** the reader lists SYNTHESIZE/D3 and a coaching-predicted answer, **not** an independently qualified answer key. E05 uses a new **piecewise inward-force graph**, a two-area potential calculation and separate circular-orbit states rather than reproducing the original quadratic force law. Its advanced centripetal-force prerequisite must be taught.

The inventory and machine-check values appear in [P0_P1_CONSTRUCTION_BRIDGE.json](P0_P1_CONSTRUCTION_BRIDGE.json) under `extension_inventory` and `extension_solution_checks`. The independent `tests/test_wpe_d3d4_extensions.py` recomputes turning-point inequalities, signed power, spring/contact flight and geometric bounces; `tests/test_wpe_d3d4_radial_force.py` checks the radial potential and circular-force cases. These are *mathematical correctness checks*, not student testing, independent B3/B4/QRT qualification or secure answer containment.

## The current five foundational pairs remain distinct

The previous five pairs teach work sign, momentum/kinetic energy, energy reachability, potential-energy slope and spring-driven cart momentum. They remain useful foundations but do **not** establish the missing D3/D4 constructions above.

The earlier B3/B4 review (`physics/wpe/learn-challenge-wpe02-b3-b4-review.json`) references older page/map blob SHAs. The exact current page/map SHAs differ. **That review is historical, not a current acceptance finding**; it must not be quietly reused as a contemporary PASS or FAIL.

## Usage and limits

1. All **eight P0/P1 constructions** now have guided and independent learning-pack drafts. Check scientific assumptions and curriculum prerequisites before using an authored pack with a child. The packages do not alter the existing source bank.
2. Keep Core1A and Core1B in separate learner stages. Preserve a child's prediction, model and first calculation before revealing the author-only solution. Prompt for diagnosis, repair and a boundary test rather than treating a chosen MCQ option as enough.
3. The **two P1 packs and five targeted extension packs** are now drafted. Teach advanced flow, vectors, analytic wells and geometric series only with the necessary scaffolding; writing a difficult author pack does not make the learning age-accessible by itself. Radial-force potential is now drafted, with an explicit radial-force and circular-motion prerequisite; it is not academically admitted.
4. Resolve the pilot/source-reader classification discrepancies **as a separate provenance task**, without blocking clearly labeled preparatory teaching drafts or calling those drafts admission evidence.
5. If a native assessment or release is intended, complete the existing independent subject/QRT, curriculum adapter, paper/key custody and Owner requirements before claiming acceptance.

The page `physics/wpe/learn-challenge.html` and pilot `RECEIVED_selection_21_places.json` are **not modified by this bridge**. No academic approvals, scores or coverage cells have been created.
