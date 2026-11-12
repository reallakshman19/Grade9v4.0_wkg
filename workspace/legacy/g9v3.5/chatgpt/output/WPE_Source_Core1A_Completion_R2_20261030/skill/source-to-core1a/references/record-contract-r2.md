# R2 records and integrity interfaces

Profiles: `core1a-source-handoff/v2` per node; `core1a-source-program/v1` for the real scope. These are derived sidecars, not native library/package or accepted schemas. R1 `core1a-source-handoff/v1` remains supported by its original checker. Strict UTF-8 JSON, no duplicate keys/nonfinite values, and exact allowed fields apply. Paths stay within their containing record/program folder, with no traversal, drive/URL paths or symlink escape.

## Node record

| Field | Contract |
|---|---|
| schema/id/title/status/purpose | v2; actual spine identity; CANDIDATE; CORE1A_PREPARATION |
| sources/units | Relative retained files, roles/authority, SHA-256; exact one-based inclusive line spans or RFC6901 pointers; canonical JSON unit digests |
| claims | Interpreted statement, exact unit refs, retained scan refs, conditions/disputes; UNREVIEWED |
| binding | Exact spine row and identity; actual candidate library microtopic/capability identities and provisional relationship; explicit unmatched canonical gaps |
| warrants | Claim refs, canonical candidate unit refs, separately typed reference-source review leads, reason/conditions; CANDIDATE or MISSING. MISSING has no fabricated unit and names the gap |
| construction | Inputs/output, obstacle/bridge, assumptions/conventions; step requirements with source/claim/warrant refs and DAG; representation requirements and source/derived roles; future distinct-example and boundary obligations |
| wrong_path_candidates | Hypothesis, claim refs, discriminating contrast, repair requirement; observation NONE |
| check_requirements | Claim refs, method, invariant, independence basis; DESIGN_ONLY |
| sl2_requirement_mapping | PENDING_REVIEWED_REQUIREMENT, null task identity, empty bindings and explicit missing input; R2 cannot manufacture a qualified join |
| native_mapping | Retained native schema definition, existing property, resolvable handoff pointer and prospective action |
| review_requests | Exactly one open request for each claim plus warrants, construction and SL2 mapping; each target carries its current canonical JSON digest |
| holds/review/notes | Open affected-boundary issues, fixed NOT_RUN/PENDING/NOT_STARTED gates and exposure/limits |
| dependency_digest | Digest of the whole record excluding this field; catches stale derived state, not coherent malicious replacement |

The current native mapping's capability target points to `/binding/canonical_matches`. That list may be empty where a genuine capability is missing; it describes a future resolution obligation rather than inventing a canonical primary identity. Native field existence is checked; semantic fit remains open.

## Program record

`scope` binds exact spine and book bytes. Actual spine rows supply the node denominator. `records` must match that node set exactly; every entry binds record SHA, separate pin-file SHA and prerequisite IDs. Record book/spine must be the same actual files as the scope. Prerequisites form a DAG; they remain proposed pedagogical bindings, not independently qualified prerequisites.

`line_dispositions` must cover every retained book line exactly once. Shared context and derived summaries may refer to multiple nodes; this is intake accounting, not a count of independent lessons. `scan_observations` must cover exactly the scans retained by records, without duplicates, pinning bytes and naming inspected region/observation/limits. The only supported observation state is AUTHOR_VIEWED_NOT_INDEPENDENT. A checker cannot prove an author actually looked; native tool evidence supplies that receipt.

`exclusions` names missing/out-of-scope material. `gates` preserve semantic NOT_RUN, Core2 Owner approval PENDING, Core1A authoring NOT_STARTED, Core1B correspondence NOT_RUN. A fake approved gate is invalid.

## Commands and readback

```text
python -B scripts/check_program.py PROGRAM --expected-sha256 EXPECTED_FROM_SEPARATE_RECEIPT
python -B scripts/render_program.py PROGRAM --expected-sha256 EXPECTED_FROM_SEPARATE_RECEIPT
```

Check returns exit0 for integrity PASS, otherwise exit1 with a structured finding. Trusted mode reports EXTERNAL_PROGRAM_BYTES_MATCH; otherwise SELF_DECLARED_PROGRAM_ONLY. Either mode retains science NOT_QUALIFIED, reviewed_SL2_joins0, native_lessons0, authoring HOLD. Rendering refuses an invalid program and writes only the linked HTML files beside their program/records; it does not rewrite source records or create course files.

To inspect a single node programmatically, `check_record(data, record_folder, pin_file, separate_expected_pin_sha)` is available. The public CLI remains the whole-program entry so coverage omissions are visible. Per-record PASS alone does not qualify a complete scope. No remote registry, reviewer authentication, semantic theorem checking, trusted promotion or native lesson emission is implemented.
