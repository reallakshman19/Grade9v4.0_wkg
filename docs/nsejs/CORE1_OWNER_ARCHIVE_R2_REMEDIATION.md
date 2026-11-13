# Grade9 v4.0 — Owner Core1A/Core1B archive acceptance and publication gate (R2)

**Mode:** OWNER_ARCHIVE_RECEIVED · SCIENCE_REVIEW_REQUIRED · ORIGINAL_SOURCE_AND_ACADEMIC_HOLD.

Owner uploaded \`G9V4_ALL_CORE1_MODULES_COMPLETE_20261113.zip\`. Its SHA-256 is
\`e5d389e8da62fc8c219373691f42ed93233814284bd15cb64a5ab8b5a5ade40f\`.

## Reconciliation

The archive contains 27 module folders but 26 unique tested construction IDs
(16 Physics, 7 Chemistry, 3 Biology). \`chem-atomic-bonding-r1\` is an
identity duplicate of \`chem-atomic-structure-r1\`; the two Core1A/Core1B,
witness and HTML payloads are byte-identical. Their bank files differ.
The original \`MANIFEST.json\` incorrectly declares zero modules.

The uploaded original Core1A/Core1B producer-witness byte hashes match 27/27.
That is **not** independent validation of the science, source custody or learning
behavior. The uploaded archive contains **no** \`workspace/sources\` custody records.

The existing public-safe technical build publishes eight separately authored
Core1AB preview pages and **18 newly authored, source-neutral supplemental
skill-repair pages** (Draft PR #109). The 18 original source-bound historical
modules are **not published, academically admitted, or substituted with those
supplements**, even though candidate output files now exist privately.

The uploaded original HTML files do not demonstrate durable first-attempt
local-storage guarding; do not copy the original HTML into Pages or public Git.

## Four independent science/content blockers

| Original candidate | Finding | Required correction |
| --- | --- | --- |
| \`chem-chemical-substances-r1\` | Given oxide/product masses imply metal mass approximately 63.35 u; the stated zinc 65.4 u answer conflicts | Reconcile the masses and rewrite the entire calculation/rubric; get independent chemistry approval |
| \`nsejs-optics-lens-mirror-d3-r1\` | Stage 2 expects image at +30 cm; stage 3 calculates +60 cm | Freeze one coherent signed optical setup, recompute intermediate/final positions and magnification |
| \`nsejs-magnetism-r1\` | Exercise requires four diagrams not independently supplied in the exercise | Obtain authenticated rights-cleared figures or replace with an independent self-contained figure-free task |
| \`ioqjs-optics-conjugate-d3-r1\` | Asked answer is two object distances while accepted answers only list the focal length already given | Correct the answer specification and fully reconcile the source and sign/geometry model |

These defects are preserved as hard review gates; *do not silently modify*
the signed owner input outputs or producer witness hashes and call them original.

## Safe publication

\`tools/nsejs_owner_core1_publication_gate.py\` cross-checks the **source-neutral
metadata-only** receipt against the exact 18 missing construction IDs and
the independent technical supplement catalog. It forbids loss of the four
science holds and rejects any claim of independent original source approval.

The site displays an explicit owner archive receipt and continues to expose
the 18 separately authored technical skill-repair lessons with first-attempt
protection. No exam bank, original paper figure, archive ZIP, original A/B
construction or private source custody bytes are copied to Pages.

## Remaining gates to publish original source-bound modules

1. Original exam source, figures, right to redistribute, canonical occurrence
   UID and authoring lineage authenticated privately.
2. Four recorded science contradictions fixed in verified authoring inputs, and
   each original Core1A/B stage independently reviewed.
3. Rebuild original learner HTML from source-verified authoring with protected
   first attempts, reload persistence and independent boundary transfer.
4. Check real tablet portrait/landscape HTTP Chromium, accessibility,
   deterministic output digests, independent first-attempt receipts.
5. Restore all required private workspace sources and outputs and run the full
   unchanged repository QA on both supported Python versions.
6. Receive academic and Owner release approval before changing original
   construction publication status, merging or deploying production Pages.

**Mathematics is out of scope. No source or academic HOLD is downgraded.**
