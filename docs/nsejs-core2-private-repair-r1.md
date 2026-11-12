# NSEJS Core2 private 50-candidate handoff: technical repair R1

**Mode: AUTHOR_EXPOSED · SOURCE_NEUTRAL_PUBLIC_PR · ACADEMIC_HOLD.**

## Actual source, PR relationships and baseline

- New branch starts from main at d00ca8e07150b6c7128328cd185ecf9567fe6c2d (after merged PR #78).
- Private handoff: G9V4_PHYSICS_COMPLETE_HANDOFF_20261111.zip; actual byte SHA256 62f7c2174bd914a9070b68459403208c74be64351a313d87616df3fe52230ff6. It is not posted to public GitHub.
- [Issue #73](https://github.com/reallakshman19/Grade9v4.0/issues/73): the other contributor delivered five-then-nine-topic R3 private ZIP candidates, not a draft PR. The R3 ZIP bytes and original producer branch were not independently available for this execution. R3's 64 PASS are contributor-local, not GitHub exact-head CI or real HTTP Chromium.
- [Draft PR #75](https://github.com/reallakshman19/Grade9v4.0/pull/75) covers source-neutral R6 private-reader conversion built on the former #74 branch, for a different R5 private site. It already provides scoped aliases and revision-aware local attempts; this PR does NOT modify or duplicate PR #75's files. Reconcile before deploying both.
- PRs #72, #74, #78 are merged. Their old pre-merge baseline 2693cdf4 must not be treated as current main.

## Verified initial 50-candidate handoff defects

1. Its 103 listed files match SHA256/size inventory, but its 100% complete statement is author-submitted, not academic approval.
2. Combined reader has 50 rows but 48 bare IDs; NSEJS-2019-P-Q01 and NSEJS-2019-P-Q02 repeat across different subjects. Bare-ID navigation/state could silently select or overwrite the wrong attempt. All 50 topic/source/id tuples are unique.
3. Six original question explorers dereference data.assets[figName] without checking if data.assets exists. Five question pages have missing asset dependencies, causing first-question rendering errors; the Optics-only explorer is the exception.
4. Five anchor source-custody packets cannot independently authenticate 50 original question claims. The archive labels unverified keys as VERIFIED_IAPT_KEY, but independent custody remains HOLD.
5. Magnetism/Mechanics anchor factor scoring does not use canonical five QRT names; the native SL2 reports hold qrt, construction and release. The D1/D2 Blueprint is not an approved academic policy; D3/D4 is a draft.
6. All five module bank.json files contain one anchor each, not ten admitted native Core1A/Core1B constructions.

## Technical fix produced PRIVATELY; no exam contents published

A separate owner-downloadable PRIVATE repaired ZIP was produced locally from the source archive and byte-reconciled. It changes only six reader HTML runtimes, not their embedded original question datasets. It adds a private SHA receipt. Its learner UI:
- Uses fully scoped subject + source + item identity and requires explicit choice for ambiguous legacy aliases.
- Displays an explicit missing-diagram HOLD instead of throwing an exception or recreating the exam figure.
- Freezes nonblank original first-response state before hint and worked-answer reveal; stores revision-bound local attempts, separate reveal and hint events; refuses storage failure and stale-tab writes.
- Warns that local browser state is not secure, source/key authority is not verified, and none of the content is admitted. Original stems, options, key claims inside custody data, source hashes, diagrams, QRT labels and academic statuses remain untouched.

The repaired private viewer passed bounded Chromium DOM tests for all six pages using an explicitly injected storage polyfill. It did NOT pass real HTTP-origin Chrome locally: local navigation was blocked with ERR_BLOCKED_BY_ADMINISTRATOR. This technical viewer repair is NOT the distinct nine-topic R3 Core1B construction engine.

## This public-safe draft PR

This PR adds a recipient-pinned private handoff audit tool and synthetic-only unit/negative tests, no actual original exam source. The tool:
- Refuses a changed ZIP, unsafe path, duplicate member, symlink, or manifest hash mismatch.
- Detects ambiguous bare IDs without pretending two different subject questions are the same.
- Reports missing media, source packet coverage and unverified official-key claims without extracting originals into CI.
- Checks five canonical QRT factors, leaves independent academic adjudication NOT_RUN, and never promotes any course or source to admitted.
- Does not depend on or overwrite draft PR #75, and does not import the unreceived nine-topic R3 private candidate.

## Remaining gates

| Gate | State |
| --- | --- |
| Private 103-file archive original hash and manifest | PASS |
| Private source-neutral viewer six-page DOM tests | BOUNDED PASS; storage polyfill, not HTTP-origin |
| Exact public-source PR CI on synthetic fixtures | Revalidate at exact head |
| Actual private HTTP Chromium desktop/mobile | NOT_RUN |
| Authentic diagrams, official keys, figure rights, remaining source custody | HOLD |
| Independent source-only five-factor QRT for every claimed exam item | NOT_RUN |
| Nine-topic R3 corrected Core1B tasks and producer Git lineage | NOT_RECEIVED / HOLD |
| Verified Core1A sufficiency, fresh Core1B and B1-B7 per target | HOLD |
| Academic admission and student release | HOLD |

No claim of Physics syllabus completion or independent student mastery is authorized. Owner approval is required before merging, deploying or advertising qualified NSEJS content.
