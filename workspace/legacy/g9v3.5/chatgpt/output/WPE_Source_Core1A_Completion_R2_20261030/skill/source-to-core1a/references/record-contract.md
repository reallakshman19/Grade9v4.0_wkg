# `core1a-source-handoff/v1` — derived preparation record

This is a candidate sidecar profile, not a canonical or renderer-native schema. UTF-8 JSON only; duplicate keys and nonfinite numbers are errors. Paths resolve relative to `handoff.json`; no URLs, absolute paths, traversal or symlink escapes. Source hashes are lowercase SHA-256 of original bytes. Unit digests use `sha256:` plus SHA-256 of canonical JSON (`sort_keys=True`, `ensure_ascii=False`, separators `,` and `:`) of the unit content.

## Fields

| Field | Meaning |
|---|---|
| `schema`, `id`, `status`, `purpose` | Fixed schema; stable ID; CANDIDATE; CORE1A_PREPARATION |
| `sources[]` | Unique id, relative path, SHA-256, role and authority. Roles: BOOK_TEXT, SOURCE_SCAN, DERIVED_FIGURE, CANONICAL_CANDIDATE, NATIVE_CONTRACT, SYLLABUS, QUESTION_EVIDENCE. R1 authority is explicit and never VERIFIED. |
| `units[]` | Unique id, source_ref, kind LINES or JSON_POINTER, locator, exact content and content digest. Lines are one-based/inclusive and joined with LF. JSON pointers use RFC6901 escaping; exact canonical value/type must match. |
| `claims[]` | Unique id, statement, nonempty source unit refs, conditions, disputes; fixed UNREVIEWED qualification. Statements are interpretations bound to evidence, not mechanically proved paraphrases. |
| `binding` | Syllabus node and exact syllabus table-row unit, microtopic ID, capability ID, library unit and relation units. The checker checks node membership and pinned library values; semantic scope correspondence remains review work. |
| `construction` | Input/output roles, obstacle, decisive move, entry assumptions/conventions, required step roles, dependencies, claim refs and warrant refs; representation requirements; worked-example, boundary, wrong-route and independent-check requirements. These describe work to author, not completed teaching. |
| `question_links[]` | Optional exact question-evidence unit, question ID, PROPOSED direct/bridge role and optional operation/demand proposal. No learner observation or reviewed status. Links must match a pinned question ID. Absence is legitimate. |
| `native_mapping[]` | Existing pinned schema unit, its property name, handoff JSON pointer, and an explicit future authoring action. No unknown native fields or pretending a sidecar is a package. |
| `holds[]` | Stable issue ID, detail and affected boundary; preserve unresolved source/science/render/approval work. |
| `review` | R1 fixed values: semantic NOT_RUN, Core2 Owner approval PENDING, Core1A authoring NOT_STARTED, Core1B correspondence NOT_RUN. Promotion is outside R1. |
| `notes[]` | Scan/extraction limits, scope and author exposure; no embedded acceptance or promotion flags. |

## Construction step shape

Each step has `id`, `role`, `requirement`, `why_needed`, `unit_refs`, `claim_refs`, `warrant_unit_refs`, `depends_on`. Roles are INPUT, REPRESENT, CONNECT, TRANSFORM, VERIFY, BOUNDARY. References must resolve; a required step needs source evidence, a claim and an identified candidate warrant. A missing warrant means the record is incomplete: preserve the gap in the dossier instead of inventing a reference. `depends_on` must form a DAG. Existence of a warrant is not its qualification.

Each representation need has an id, `asset_ref` (nullable), `status` MISSING or DERIVED_UNREVIEWED, `correspondence` rows (`symbol`, `element`, `in_words`) and a `requirement`. A source figure is retained as source evidence, while its future teaching use/correspondence remains subject to review. R1 demonstrates derived SVG use only; other asset roles remain a documented future extension rather than coerced enums.

Question demand proposals, when present, use the pinned five factors and existing D1..D4 bands. No score is generated from a book subsection. The checker validates arithmetic and explicit factor keys, not cognitive truth or independent scoring.

## Checker result and limitations

`check_handoff.py FILE` is read-only and prints a JSON report. Exit 0 means local integrity PASS. Exit 1 means INVALID with findings. A structurally valid dossier reports `preparation=CANDIDATE`, `core1a_authoring=HOLD`, `semantic_review=NOT_RUN`, `native_package=NOT_EMITTED`. It never emits REVIEWED, QUALIFIED or learner-ready status. No external registry, authentication or promotion is implemented.

For binding to externally expected source identities, also pass `--trusted-pins PIN_FILE --trusted-pins-sha256 EXPECTED_SHA256`. The pin file is `{"schema":"source-pin-set/v1","sources":[...the exact source records...]}`. Obtain its expected digest from the separately trusted delivery receipt; do not read the expected hash from the handoff being checked. This rejects an attacker refreshing all local source/unit hashes against a different source. Without it the report explicitly says `SELF_DECLARED_ONLY`. Matching these external pins establishes expected local bytes, not official authenticity. A coerced or attacker-controlled expected digest defeats that trust assumption.

Unvalidated paraphrase meaning, intellectual completeness, scientific truth, scan transcription, diagram semantics and reviewer independence remain review obligations even when all hashes/references pass. Deliberately coherent but false prose can pass structural checks; the regression suite preserves that limitation instead of pretending text length establishes meaning.
