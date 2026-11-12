# QRT × Physics Blueprint × WPE — deterministic agent runbook

**Version:** operating playbook 1.0.0 · **Date:** 2026-11-03 · **Status:** author-exposed engineering methodology, **NOT an approved academic policy**.  
**Scope:** apply the repository's existing SL1 → SL2 → independent QRT → common Physics Blueprint + WPE topic adapter → Core1A/Core1B → B1–B7 → native/Owner gates. **D3/D4 first.** Physics-only: do **not** reuse these Physics rules in Mathematics or Chemistry.  
**Authority:** this is a reproducible execution aid for a low-capability agent, **not** a substitute for Shared/Owner/Oracle instructions, the actual Blueprint, academic reviewer, native skill, source custody or actual child testing. **NO_REAL_APPROVAL** is ever conferred by this document, a fixture, a Python test or a webpage.

[Architecture entry](../index.html) · [Readable protocol](index.html) · **[Core six-stage reasoning method](CORE_METHOD.md)** · [Pinned source manifest](source-pins.json) · [Golden cases](fixtures/golden-cases.json) · [Executable validator](verify_cases.py) · [Physics Blueprint v0.2.0](../../templates/physics-blueprint/physics-blueprint.D3-D4.json) · [Independent-review entry](../../docs/agent-entry/07-independent-review.md)

## 0. Non-negotiable preflight — read these in this order

For **authoring / planning agents** (already exposed to review history), read the actual files in the current commit:

1. `AGENTS.md`, `docs/product-scope.md`, `docs/agent-entry/CURRENT_CONCEPT_COMPANION.md`.
2. `docs/smart-skills-integration.md` (SL1/optional P1/SL2/QRT ownership); `docs/agent-entry/03-blueprint-adapters.md`.
3. `templates/physics-blueprint/physics-blueprint.D3-D4.json` **as the complete rule**, especially `common`, `levels`, `columns`, `cells` and `gap_note_shape`. Its status is **DRAFT_OWNER_REVIEW**, version **0.2.0**.
4. Actual WPE question inventory `workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json`, `physics/wpe/reasoning-paths.review.json`, `physics/wpe/d3d4-self-tutor.review.json`, `WPE_Source_to_Core1A_Concept/evidence/RECEIVED_selection_21_places.json` and `preview/batches/b07-qrt-evidence.json`.
5. Exact current source/adapter/version, only if supplied. If a source cannot be located or a path/hash does not match: **HOLD** and record the missing input.

**Exception: independent blind QRT reviewer.** Do **not** show this author-exposed guide, prior solutions, classification tables, golden fixtures, author labels, consolidated review reader, hints or checkpoint to a reviewer *before their sealed first pass*. Only an actually authorized dispatcher may give that reviewer exact, independently authenticated question/figure/source inputs, applicable rubric/Blueprint, task scope, seal destination and resource bound. Read `docs/agent-entry/07-independent-review.md`. If exposed, declare it. Never self-appoint or describe the review as blind.

**As-of snapshot, not timeless truth:** 74 displayed consolidated records; 22 labeled D3/D4 (17 D3 + 5 D4), all **NOT_ADMITTED**. Eight interactive reusable teaching constructions (C01–C08), five author-only targeted extensions (E01–E05), zero qualified learner routes. The separate 21-place exam pilot has 14 pending, 7 vacant, zero admitted; among its 14 candidates versus the selected reader: 3 agree, 8 conflict, 3 absent from *that reader*. The Physics Blueprint has 14 draft cells (D3/D4 × 7 operations). The selected approved WPE adapter is **UNSELECTED**. D1/D2 common Blueprint is not approved/specified here. **D3.1 is PAUSED.** Recompute counts when the pinned inventory changes.

## 1. Agent identity and output contract

Choose exactly one mode and **write it at the top of your output**:

| Mode | May read | Permitted work | Forbidden |
|---|---|---|---|
| `AUTHOR_EXPOSED` | Existing author reports, reader, packs, Blueprint and status history | Inventory, source-repair proposals, explanatory practice, candidate mappings, local checks | Calling own analysis blind QRT, granting source custody, picking adapter as approved, approving/releasing |
| `INDEPENDENT_QRT` | **Only** the separately dispatched source-only input plus approved task rubric *before seal* | Solve exact task, identify decisive move, competing operation, five-factor score and ambiguity, seal first pass | Reading author outcomes before seal; changing first-pass record after exposure; signing without authorized identity |
| `TECHNICAL_QA` | Native machine-check inputs, immutable artifacts and approval receipts if actually supplied | Hash/schema/graph/browser/physics checks, read-only reports | Treating PASS as academic approval, inventing signatures or filling missing receipts |

**Required output per processed question (even for HOLD):** question ID; exact input source path/locator/hash or `UNKNOWN`; source figure/key/custody status; SL2 proposed operation and band with provenance; QRT status and evidence; five scores **only if actually available**; provisional or reviewed Blueprint cell; adapter exact version/hash or `UNSELECTED`; teaching link and status; source/academic/learning holds; next permitted action; any needed gap note. **Never silently omit a question.**

The primary typed row is [`schemas/question-route.schema.json`](schemas/question-route.schema.json). It is a **candidate audit record**, not native SL1/SL2 or Core2 and not an independent reviewer receipt. For source-only first-pass preparation use [`schemas/independent-first-pass.schema.json`](schemas/independent-first-pass.schema.json); for author tile planning use [`schemas/tile-build-plan.schema.json`](schemas/tile-build-plan.schema.json); for real common-rule insufficiency use [`schemas/blueprint-gap-note.schema.json`](schemas/blueprint-gap-note.schema.json). Field shape is necessary, never sufficient, for qualification.

### Explicit unknown-value policy

- No original paper / no exact graph → `source.custody=UNVERIFIED` or `READER_COPY_ONLY`; `figure=UNQUALIFIED` / `PENDING`. **Do not infer from a paraphrased question.**
- No official key → `key=PENDING`, even if a coaching answer appears plausible. A corroborated answer and admitted key are distinct.
- No independent first-pass record → `qrt.status=NOT_RUN`; operation/band/score/factors **null**, not five guessed zeros.
- Reviewed as D2 → leave `blueprint.candidate_cell=null`; **do not borrow D3**.
- Several WPE adapter versions → leave **UNSELECTED**; choose one only on actual Owner-approved exact hash receipt. Never merge snippets into a pretend selected adapter.
- Interactive practice exists → `learning.status=INTERACTIVE_PRACTICE`, `semantic_join=UNREVIEWED_PROPOSAL` unless independently checked. Not `QUALIFIED_TILE`.
- No genuine sealed answer or authentic first-attempt observation → do not claim independent DEMONSTRATED evidence. Missing P1 is optional and never blocks browsing a lesson.
- Never paste full copyrighted exam stems, figures, answer keys or personal student responses into fixtures or public reports. Use trustworthy locators and hashes.

## 2. One-question processing procedure — execute in order, no improvisation

**S0 — Load and label the mode.** Pin repository commit and file paths. Declare `AUTHOR_EXPOSED` unless properly dispatched for sealed independent review. Set all acceptance statuses `NOT_ADMITTED/HOLD` by default.

**S1 — Register the exact identity.** Find `source_id` in the canonical reader, not just a similarity match. Record category: exam, textbook or synthetic control; distinguish original item ID from page duplicate/display ID. For an exam, collect exact paper/date/shift/item/figure/key/conditions, and inspect whether all demand-bearing parts correspond. If unavailable, mark source HOLD. Use the authoritative source-custody contract, not merely a free-text citation.

**S2 — Preserve proposal status.** Read SL1 native source identity and SL2 **proposal** when available. Record proposed primary operation and band with its source. Do not treat a displayed badge or author reconciliation as QRT review. Read optional P1 only when a genuine saved pre-help response and its exposure log exist.

**S3 — Prepare QRT first pass without contamination.** When the source and authorized independent reviewer are available, dispatch the original problem and necessary figure **without** coaching answers, SL2 labels, reader conclusions, old QRT labels or author fixtures. Reviewer independently transcribes/solves, states conditions and shortest valid route, chooses one primary operation, explains a plausible competing operation, scores five factors with a specific evidence sentence each, records ambiguity, and seals immutable first-pass bytes/digest **before** later exposure. Record actual reviewer assignment and seal receipt. If there is no reviewer, report `NOT_RUN` or existing `FIRST_PASS_RECORDED`; do not simulate the receipt.

**S4 — Apply QRT band/operation, not wishful categorization.** Only after independent evidence: compare with SL2, classify agreement/disagreement and mark review/Owner decision pending when appropriate. Score on the *exact task*: five integers 0–2, exact total and band. D1 0–2, D2 3–5, D3 6–7, D4 8–10. No factor is a proxy for the band and no factor is scored twice. The **decisive act** defines one primary operation, not the most attractive formula name.

**S5 — Resolve Blueprint cell without promotion.** If verified/reviewed band is D1/D2: do not bind to D3/D4; mark `D1_D2_BLUEPRINT_SPEC_PENDING`. If there is *only an unreviewed D3/D4 SL2 proposal*, calculate a **candidate-only** cell from the seven-column order; never call it qualified. If actual independently reviewed D3/D4 band/operation exists, propose the corresponding cell, still HOLD until all additional selection/authority gates pass. Cross-check `cells[cell_id].template_ref == "QRT-<OPERATION>-<BAND>"`.

**S6 — Select the topic adapter only through authority.** Common Blueprint is Physics-wide and topic-neutral; all WPE bodies, laws, quantities, signs, figures, source anchors, misconceptions and exceptions go into the WPE adapter. Bind **one exact** adapter path/version/hash and its Owner selection receipt. If missing, use `UNSELECTED`. Never edit the common Blueprint to fit a WPE problem.

**S7 — Build teaching and independent reasoning.** Read [Core six-stage method](CORE_METHOD.md) first: define the taught skill, protected inference, evidence for each stage, and how help changes the independence claim. Audit whether Core1A teaches the *exact inferential jump*, prerequisite laws, conditions, units, sign/frame, diagrams, wrong path and check. Audit Core1B for a **fresh** attempt with an independent first model, honest H1/H2/H3, reconstruction, diagnosed cause from actual response, repair and changed-condition transfer. A completed C01–C08 practice lesson is usable learning help but not proof that an original question or D3/D4 MAIN task is fully covered.

**S8 — Test the Blueprint's complete tile shape.** A tile may have multiple topic-specific instances. Provide one Core1A construction per instance; one band-carrying MAIN Core1B cycle **mixing the instances**; and one Core1B cycle per instance, with truthful individual bands. Score each MAIN/instance/exam task independently. A D2 instance can teach a D4 MAIN but cannot be counted as a D4 exam original.

**S9 — Check B1–B7 and self-audits.** B1 target, B2 construction signature, B3 sufficient teaching, B4 distinct fresh reconstruction, B5 attempt protection, B6 evidence-based diagnosis/changed-condition transfer, B7 Physics/provenance. Verify laws and applicability, signs, force directions, graph axes, unit balance, limiting cases and diagram-to-scene correspondence. Run native input/schema/record binding checks with real artifact pins. A technical checker pass is **not** an independent academic receipt.

**S10 — Decide release honestly.** Publish a *practice preview* with clear warnings if allowed; do not publish an academic-accepted tile until source authenticity, independent QRT, Blueprint and selected adapter, B1–B7, native binder, and Owner approvals are all genuinely on record. Record hold code and next permitted action in the audit row. Finish by identifying whether this question fills a pilot *exam original* seat or merely teaches a prerequisite.

**S11 — Recheck after change.** When any source figure, original key, reviewer first pass, Blueprint version, adapter hash, curriculum condition, code, or question corpus changes, invalidate the dependent binding and rerun. Do not reuse an old review receipt for a new page/adapter SHA.

### Minimal repeatable loop for a low-thinking agent

```text
FOR each question_id in the pinned full inventory:
    read exact row, source and any SL1 native evidence
    IF original source/figure/key incomplete: record HOLD; do not guess
    copy SL2 proposed operation/band WITH "PROPOSED" label
    IF no authorized sealed independent QRT: qrt=NOT_RUN / prior recorded state; HOLD
    ELSE confirm sealed first pass, five score warrants and exposure audit
    IF independently reviewed D1/D2: no D3/D4 tile; mark D1_D2_SPEC_PENDING
    ELSE IF D3/D4 proposed only: compute candidate cell; mark UNADJUDICATED
    ELSE check operation×band against exact Blueprint cell
    IF approved Blueprint and exact selected WPE adapter not BOTH proven: HOLD
    map Core1A/Core1B evidence and B1-B7, but never promote from page presence
    write source→SL2→QRT→cell→adapter→learning→admission row
    IF any authority receipt absent: admission=NOT_ADMITTED
    append unresolved actions and process next question
END
assert every source question and every pilot seat is accounted for
```

This procedure **does not require a blocked academic gate to stop a child's practice**. Independent examination qualification and student-facing explanatory practice have separate output statuses.

## 3. Seven operation columns and their observable evidence

The canonical `column_order` is:

| # | Column | What decides the task | Required evidence of learner move |
|---|---|---|---|
| 1 | **RETRIEVE** | Classify or reconstruct a fact by its defining condition | Correct verdict **and** the deciding condition, not familiar wording |
| 2 | **EXPLAIN** | Explain a phenomenon from physical causes | Warranted links, not just the outcome or a formula quote |
| 3 | **APPLY** | Execute a known procedure with valid mapping | Applicability, mapping, result **and** independent check |
| 4 | **MODEL** | Choose governing law/system/variables/assumptions | Defended model choice and assumption check, not merely a number |
| 5 | **REPRESENT** | Translate words/graph/diagram/equations | State invariant, correspondences and back-translation |
| 6 | **SYNTHESIZE** | Connect dependent ideas in the right order | Name the bridge and order, with independent invariant/second-route check |
| 7 | **JUSTIFY** | Establish claim via formal physical warrants | Law, conditions, complete argument and boundary countercheck |

Do **not** confuse columns because a question *contains* a graph, *mentions* a formula or has an elaborate answer. The primary column is the decision whose success actually determines the task. Use each column's `boundary` and `evidence_criterion` from the Blueprint rather than inventing new definitions.

| Band | Five-factor score | Core1B protected work |
|---|---|---|
| D1 | 0–2 | Basic fact/procedure; outside this D3/D4 Blueprint |
| D2 | 3–5 | Straightforward application; outside this D3/D4 Blueprint |
| **D3** | **6–7** | The learner bridges at least two dependent concepts/representations, with one material link left for them |
| **D4** | **8–10** | The learner must choose a nonobvious strategy, explain an exception or transfer to unfamiliar conditions; do not reveal the decisive abstraction before the attempt |

**Formula for a candidate-only cell:** `<BAND>.<OPERATION_INDEX>`. For example `MODEL/D3 → D3.4`, `SYNTHESIZE/D3 → D3.6`, `JUSTIFY/D4 → D4.7`. The Physics tile identity adds `PHY-WPE-`: `PHY-WPE-D3.4`. A string match does **not** approve this cell or resume paused D3.1.

## 4. How to use the actual Blueprint and WPE adapter

1. Read the **common Physics Blueprint v0.2.0** from `templates/physics-blueprint/physics-blueprint.D3-D4.json`. Verify `blueprint_id=PHYS-QRT-BLUEPRINT`, version, `column_order`, 14 `cells`, status `DRAFT_OWNER_REVIEW`; **do not** locally change it.
2. Derive candidate cell as above; read `levels[D3|D4]`, `columns[1..7]` and `cells[cell_id]` together. They define band, operation, hints, diagrams, protected decision and evidence criterion. The resolved template is `templates/physics-blueprint/physics-blueprint.D3-D4.resolved.v0.2.0.json` but must not be interpreted as extra approval.
3. Only an approved exact WPE adapter (if selected later) can fill the Physics-agnostic template with topic facts, laws, conditions, instances, diagrams and sourced exam anchors. **Today none is approved/selected.** Six reported candidate variants had five distinct hashes in the prior audit; do not silently merge them.
4. Each student tile must have: (a) exact exam question at START **only if authenticated** (otherwise “no exam question yet”), (b) Core1A conventions/prerequisites/build/fully worked *different* anchor/wrong path/exit check, (c) Core1B MAIN + instance six-stage cycles, (d) protected return to the exam answer only after attempt, (e) hidden-by-default source/custody view.
5. Hints H1 CLARIFY, H2 CORRELATE and H3 OPEN_THE_WAY cannot contain the learner's protected step W or answer. Pictures have S1/S2/S3 meaning checks and phase-specific reveal controls. Static JavaScript is *not* secure answer concealment: distinguish UI gating from an independently protected exam assessment.
6. A true common-rule gap is reported using [Blueprint gap-note schema](schemas/blueprint-gap-note.schema.json), not patched in topic content. Include exact missing slot, candidate cell, instance, versions, why adapter cannot express it and suggested cross-topic change. Oracle/Owner decide `ACCEPTED`, `REJECTED` or `ADAPTER_CAN_HOLD_IT`; until then leave `PENDING`. See `common.gap_note_shape` for the governing fields.

**D3.1 note:** the `templates/physics-blueprint/subtiles/physics-blueprint.D3.v0.2.1.json` is also draft and does not resume D3.1. A sub-tile splits *ideas* for coverage without inventing an eighth cognitive column.

**Implemented P0 working inventory:** [search the 74-question WPE QRT × Blueprint × learning register](wpe-coverage.html) or [inspect its pinned JSON](wpe-coverage-register.json). The 21-place original-exam pilot is an independent overlay; source and QRT holds remain explicitly unadmitted.

## 5. D3/D4-first priority queue; keep different denominators separate

| Priority | Actual queue | Completion test |
|---|---|---|
| **P0** | Exact source figure/key/custody and disputed QRT operation/band for all selected D3/D4 candidates | Each exact task has provenance, QRT disposition or explicit HOLD |
| **P0** | Build **74-row** question→concept→QRT→tile register, including 21-place pilot overlay and dedup without dropping identities | 74 unique question records accounted for; 21 pilot places retained; counts reconcile |
| **P1** | Interactive versions of **E01–E05**, currently author-only | Six linked D3 questions gain usable practice *without* academic promotion |
| **P1** | Write original student constructions for **EX-M97**, **EX-N39** and **WEP07-01** | Three unmapped D3 source-theme rows gain truthful proposed learning links |
| **P1** | Re-audit 13 currently linked D3/D4 questions for exact inference vs merely related prerequisite | Each link tagged `RELATED`, `EXACT_INFERENCE_REVIEWED` or `UNQUALIFIED`; no blanket coverage claims |
| **P2** | Remaining lower-band/unmapped question bank rows using suitable D1/D2 rules when approved | No unaccounted question; never force into D3/D4 |
| **P2** | Fill original 21-place exam target after authenticated source + independent QRT | Three qualifying distinct originals per operation across D3/D4; no double counting |

**Known evidence caveat:** current reader's 22 *proposed* D3/D4 include 13 interactive links, 6 author-pack-only links, 3 unmapped. These 22 labels are not final QRT. A different 21-place pilot currently has 14 proposed leads and 7 vacancies. The 14 Blueprint **cells** represent seven cognitive operations at two bands. These are **three different denominators**; never add them as equivalent acceptance counts.

## 6. Golden examples — follow the exact evidence, not the desired label

These six [machine-checked documentary cases](fixtures/golden-cases.json) contain **no original exam stems**, no reviewer signatures and **no admission**:

| Fixture | Verified repository evidence | Required agent decision |
|---|---|---|
| **G01 · EX-M62** | Consolidated reader currently proposes **MODEL/D3**; B07 preserves an independent first-pass **APPLY/D2 (4 points)**. B07's separate *prior-author proposal* was APPLY/D3. | Preserve all three provenance layers; no D3 cell; mark D1/D2 specification pending and classification disagreement. C03 interactive practice is only a related help route. |
| **G02 · WEP07-03** | Pilot conditionally nominates **JUSTIFY/D4**; B07 records **APPLY/D2 (5 points)**. Public IAPT key a,b,c,d corroboration does not resolve QRT classification or full source authority. | **No D4.7 assignment.** Record conflict and separate source/key/Owner holds; E01 remains author-only. |
| **G03 · EX-M16** | Reader **MODEL/D3**, no admitted independent QRT; C07 is interactive practice. | Candidate `D3.4` **for planning only**, QRT NOT_RUN, Blueprint draft, adapter unselected, admission HOLD. |
| **G04 · EX-M109** | Reader **SYNTHESIZE/D3**, E01 exists as author-only pack. | Candidate `D3.6` for planning only; do not call it interactive or academically covered. |
| **G05 · EX-M97** | Reader **SYNTHESIZE/D3**, no mapped construction. | Record true learning gap. Candidate `D3.6`, QRT and original source pending. |
| **G06 · EX-M79** | Reader proposes APPLY/D3; B07 says contested/unadjudicated and exposed to author assessments. | Candidate `D3.3` is NOT a QRT decision; seek properly assigned independent source-only review. |

**Negative controls:** N01 fake admission, N02 operation/cell mismatch, N03 D2 forced into D3, N04 wrong factor sum, N05 author pack forged as a qualified tile. Every control must produce a HOLD reason, not pass silently. The fixtures' factor entries paraphrase **B07's numeric scores** but explicitly say their per-factor warrants are **not supplied**; the fixture does not fabricate them as independent findings.

### Guided example trace 1 — EX-M16, step by step

```text
mode: AUTHOR_EXPOSED
id: EX-M16
identity: source reader record present; official key unresolved
SL2/read-side proposal: MODEL / D3 (PROPOSED)
independent QRT: NOT_RUN; no reviewer receipt
provisional route: D3.4 = column 4 MODEL, D3 (CANDIDATE ONLY)
Blueprint: 0.2.0 DRAFT_OWNER_REVIEW
selected WPE adapter: UNSELECTED
learning: C07 INTERACTIVE_PRACTICE, unreviewed semantic source join
academic status: NOT_ADMITTED
next action: authenticate source/key; independently review operation and band;
             then select Blueprint/adapter through Owner and inspect B1–B7
```

The presence of a conveyor lesson or a candidate `D3.4` does **not** answer whether EX-M16's *exact published task* genuinely requires the same steps; the original source's speed-dependent flow law must be checked independently.

### Guided example trace 2 — WEP07-03 disputed D4 nomination

```text
mode: AUTHOR_EXPOSED
id: WEP07-03
pilot proposal: JUSTIFY / D4 (pending)
consolidated reader: APPLY / D2 (not admitted)
B07 recorded independent first pass: APPLY / D2; factor scores 1,0,2,1,1 = 5
QRT final decision: NOT_GRANTED (first pass is not Owner admission)
Blueprint D3/D4 cell: NONE; D1/D2 SPEC_PENDING
learning: E01 AUTHOR_PACK_ONLY, source-theme proposal
status: HOLD; never fill D4.7 to satisfy a quota
```

When paper/key and reviewer comparison are unresolved, **carry both claims** and their actual evidence paths. Do not “correct” the pilot in place and do not silently treat key agreement as difficulty agreement.

### Hypothetical no-approval tile and gap-note examples

- [D3.4 author tile-plan](fixtures/illustrative-D3.4-tile-plan-NOT-APPROVED.json): shows two topic instances, a **MAIN** band-carrying challenge and two lower-band instance cycles, with B1–B7 `NOT_RUN`, adapter `UNSELECTED`, **AUTHOR_DRAFT_ONLY**. It is **not** the official native tile-pack schema.
- [Source-only packet — NOT READY](fixtures/source-only-packet-NOT-READY.json): necessary source identity/figure not authenticated, first pass null and reviewer assignment false. **Do not dispatch** this file to a blind reviewer as if ready.
- [Invented scoring example — NOT EVIDENCE](fixtures/synthetic-qrt-scoring-NOT-EVIDENCE.json): a synthetic task with visible five-factor arithmetic; **not sealed**, not independent, not exam evidence.
- [Hypothetical gap-note — NOT SUBMITTED](fixtures/hypothetical-blueprint-gap-NOT-SUBMITTED.json): demonstrates the required escalation fields with `oracle_decision=PENDING`, not a real claim that the current common Blueprint is defective.

## 7. Run automated checks and interpret results correctly

After a clone with the normal project dev dependencies installed:

```bash
python architecture/qrt-blueprint-protocol/verify_cases.py
python -m pytest -q tests/test_qrt_blueprint_agent_protocol.py
python -m pytest -q tests/test_qrt_binding.py
```

The validator checks: JSON Schema Draft 2020-12 shapes; exact 14-cell Blueprint order/status; 74-record reader count; B07-recorded factors/operation/band; WEP07 pilot nomination; arithmetic sums; candidate cell derivation; six golden HOLD cases; five negative nonpromotion controls.

Expected scope string is `STRUCTURAL_AND_DOCUMENTARY_ONLY_NO_APPROVAL`. Technical `PASS` means *the controls and examples remain internally consistent*. It does not authenticate exam papers, establish a blind reviewer, choose the adapter, prove a child's first response or authorize native release.

When real native data is available, follow `docs/smart-skills-integration.md` for separately trusted SL1/SL2 gate reports and `src/grade9qa/qrt_binding.py` for read-only native alignment diagnostics. The latter deliberately retains HOLDs even if a supplied JSON report claims PASS without trusted provenance.

## 8. Final delivery checklist (a low-thinking agent must fill every row)

| Question | If NO, write |
|---|---|
| Did I identify the exact source record and all demand-bearing figures, options and conditions? | `SOURCE_CUSTODY_PENDING` |
| Are key provenance and correctness separated from the source? | `KEY_PENDING` |
| Am I citing the SL2 *proposal* instead of calling it QRT? | `SL2_PROPOSAL_ONLY` |
| Is an independently authorized sealed first pass actually present, with exposure declared? | `QRT_NOT_RUN` / `FIRST_PASS_ONLY` |
| Does five-factor evidence add to its actual D-band, and does the decisive act match its operation? | `QRT_SCORE_OR_OPERATION_CONFLICT` |
| Is D3/D4 supported rather than merely proposed, or is a D1/D2 HOLD explicit? | `D1_D2_SPEC_PENDING` |
| Does the common Blueprint cell exist at the exact version and remain approved? | `BLUEPRINT_DRAFT` |
| Is one exact approved WPE adapter path/version/hash selected and bound? | `ADAPTER_UNSELECTED` |
| Does Core1A teach the decisive inference with scientific warrants, and Core1B independently reconstruct it? | `B3_OR_B4_NOT_PROVEN` |
| Are pre-help answers protected and genuine learner error diagnoses based on a saved response? | `B5_OR_B6_NOT_PROVEN` |
| Do B1–B7, native checks, independent academic review and Owner acceptance have real receipts? | `OWNER_OR_NATIVE_HOLD` |
| Did I keep question-bank coverage, 21 pilot seats and 14 Blueprint cells in distinct counts? | `INVENTORY_INCONSISTENT` |
| Did I retain useful child practice even while exam/academic work is held? | `PRACTICE_SEPARATE_FROM_ADMISSION` |

**Default terminal result:** `NOT_ADMITTED` with an exact next permitted action. Never fill `APPROVED`, `DEMONSTRATED`, `SEALED`, `SOURCE_VERIFIED`, `OWNER_ACCEPTED` or `QRT_INDEPENDENT` without real independent evidence and authority. Stop the **admission**, not the learner's progress.

## 9. Source references (existing authority, not replaced)

- [Current Physics D3/D4 Blueprint](../../templates/physics-blueprint/physics-blueprint.D3-D4.json): common band rules, seven operations, 14 cells, MAIN/instance cycles, H1–H3 and `gap_note_shape`.
- [Resolved candidate Blueprint](../../templates/physics-blueprint/physics-blueprint.D3-D4.resolved.v0.2.0.json): machine-expanded candidate, not an approval.
- [Physics D3 subtiles draft](../../templates/physics-blueprint/subtiles/physics-blueprint.D3.v0.2.1.json): does not authorize resuming D3.1.
- [SL1/SL2 and QRT integration](../../docs/smart-skills-integration.md); [independent first-pass exception](../../docs/agent-entry/07-independent-review.md); [current concept companion](../../docs/agent-entry/CURRENT_CONCEPT_COMPANION.md).
- [Existing native QRT binding checker](../../src/grade9qa/qrt_binding.py) and its tests.
- [B07 actual recorded first-pass statuses](../../preview/batches/b07-qrt-evidence.json), [current 21-place pilot selection](../../WPE_Source_to_Core1A_Concept/evidence/RECEIVED_selection_21_places.json), [WPE source-to-learning matrix](../../physics/wpe/reasoning-paths.review.json).
- [Current eight interactive learning journeys](../../physics/wpe/d3d4-self-tutor.html), [WPE author packs](../../WPE_Source_to_Core1A_Concept/learning-bridge/README.md), [separate learner observation protocol](../../WPE_Source_to_Core1A_Concept/learning-bridge/LEARNER_OBSERVATION_PROTOCOL.md).

**If the requested task or source is not supported by these authorities, write the limitation and HOLD it; do not fill the gap from plausible general knowledge.**
