---
name: source-to-core1a
description: Prepare evidence-bearing Core1A construction handoffs from book, syllabus and reference sources, joined to reviewed SL2/QRT requirements when available. Use for non-question-bank labelling and source-to-teaching preparation; it does not replace SL1/SL2, qualify Physics, or render a course.
metadata:
  version: 0.2.0-candidate
---

# Source to Core1A

Produce a usable, inspectable preparation record rather than a topic summary or a lesson-shaped placeholder. Preserve exact source passages and distinguish source claims, canonical candidates, reviewed requirements and author inferences. This is a companion preparation/binding skill, not Smart Labelling 3.

For a chapter/spine or multiple source units, use [the R2 protocol](references/protocol-r2.md) and [R2 record contract](references/record-contract-r2.md). They account for the actual source denominator and retain missing warrants without inventing a canonical match. The ten-node WPE example is `examples/wpe-source-program/program.json`; open its `index.html` for linked author dossiers. All ten are unqualified preparation candidates, not accepted lessons.

For an existing v1 single handoff, use [the R1 protocol](references/protocol.md) and [v1 contract](references/record-contract.md); its checker and work-direction example remain compatible. Do not silently migrate schema meaning. For native output boundaries and real failure controls, read [benchmarks](references/benchmarks.md).

## Prepare the evidence

1. Identify the actual source role: syllabus/scope, exposition, definition, derivation, example, figure, practice or exam original. Folder names and book “JEE” badges do not establish exam identity. Keep duplicates/version relations; do not inflate coverage.
2. Pin source bytes. Bind claims to exact lines or JSON pointers, preserving original content. For scans, record the page/region actually inspected and transcription limits. A generated SVG is a derived redraw, not the printed figure. Remote or absent assets remain missing.
3. Map the source unit to the existing syllabus node, microtopic, capability and conditions. A syllabus defines intended scope, not scientific truth. A candidate library is not qualified merely because a reference resolves.
4. State what construction must be taught: inputs, obstacle, output, decisive bridge, prerequisites, conventions and dependency roles. For each consequential role identify supporting passage, proposed warrant, reason, boundary and check. An extracted solution is evidence for an author, not a completed fresh Core1A worked example.
5. Join separately to available SL2/QRT requirements by exact task/dependency identity and capability. Do not infer operation/demand for a book section, invent an exam question, copy a prior score, or demand optional P1. A missing reviewed question leaves the join pending; source preparation can continue.
6. Preserve gaps as authoring obligations: missing warrant, representation correspondence, fresh worked example, wrong-route hypothesis, independent check, or reverse-direction construction. Mark prerequisites/support that will not be assessed. Do not call a proposed repair an observed learner misconception.

## Deliver and check

For R2, write `core1a-source-program/v1` with `core1a-source-handoff/v2` records and retained relative assets. Run:

```text
python -B scripts/check_program.py examples/wpe-source-program/program.json --expected-sha256 EXPECTED_PROGRAM_SHA256
python -B scripts/render_program.py examples/wpe-source-program/program.json --expected-sha256 EXPECTED_PROGRAM_SHA256
```

Take the expected program digest from the separate delivery/pin receipt. Without it, the whole-program trust remains SELF_DECLARED_PROGRAM_ONLY even when per-record pins agree. The checker accounts for every retained source line and every actual spine node, source byte/span identity, record/pin hashes, review-target digests, missing warrant groups, reference/DAG consistency and native property targets. The renderer emits an author catalogue plus linked dossiers; it does not emit a learner course.

For retained v1 records, run:

```text
python -B scripts/check_handoff.py examples/wpe-work-direction/handoff.json
```

For an externally pinned run, add `--trusted-pins examples/wpe-work-direction/source-pins.json --trusted-pins-sha256 EXPECTED_SHA256`, taking the expected digest from the separate trusted receipt. Otherwise the report explicitly records self-declared source identity. See the record contract for this trust boundary.

For an author-readable dossier (not a learner lesson), run `scripts/render_handoff.py HANDOFF --out EXAMPLE_FOLDER/index.html`. Output must stay within the handoff folder.

The checkers perform local reference/hash/span/dependency checks only. A zero exit means **mechanical preparation integrity**, with Core1A authoring still HOLD. They cannot verify Physics, adjudicate QRT, authenticate a reviewer, validate picture semantics or authorize a course. Neither version has a promotion command. R2 emits version-bound review requests; a qualified-science or reviewed-SL2 consumer must use genuine external native evidence. Do not insert approval flags to simulate that consumer.

Return the record, exact evidence, check report, native-field authoring obligations, unresolved issues and next consumer. Keep learner pages separate from this author dossier. Use the existing package/bank/manifest contracts when later authoring is authorized; this sidecar is not a native package, native source-interpretation receipt or replacement Blueprint.

Preserve the actual Owner gates. For WPE: prepare in parallel, then completed Core2 approval before Core1A construction; Core1A approval before Core1B. D3.1 remains paused. Installation, remote writes, original edits and agent creation require their actual authorization; a skill invocation grants none.
