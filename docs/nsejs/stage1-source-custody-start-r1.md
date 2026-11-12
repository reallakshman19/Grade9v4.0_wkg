# NSEJS completion — Stage 1 source-custody intake and runnable preflight

Task: G9V4-NSEJS-CORE2-SOURCE-CUSTODY-PREFLIGHT-R1
Mode: OWNER-STARTED · CONTRIBUTOR · READ-ONLY INPUT AUDIT · FAIL_CLOSED
Baseline: main e3fc01ae822b937846db03043a1f0731a29da3f4 (12 Nov 2026)

## Evidence position

The deployed NSEJS site is an **unvalidated technical preview**. Its Physics Core2 reader contains 50 source-claimed candidate records and one separately authored practice record, none academically admitted. Chemistry and Biology Core2 public source-backed banks are unavailable. Eight Core1A/Core1B authored practice journeys are generated and routed to Pages. The 26-construction Agent B ledger has 18 other test-backed constructions without reproducible public learner pages; the reported 27th construction is not yet identified.

The 15 source-dependent year/subject tests for 2020–2024 declare **79 expected items per subject (237 total)** but do **not** prove original examination coverage. Never add the Physics 50 candidate records to 237 as independent items. The repository does not provide the private workspace source/custody directories or required generated Core2 bank/report bundles for those 15 test groups.

Latest pre-start main CI:
- Public Pages build/deployment succeeded at e3fc01ae822b937846db03043a1f0731a29da3f4.
- Python QA failed: 756 passed, 31 failed and 464 errors on Python 3.11. Absent private source/output fixtures and outdated assumptions about preview/question-status.html are distinct defects. No test is waived here.
- The 12.7-inch touchscreen is the public learner UI target, not phone viewport qualification.

## Implemented Stage 1 (new branch)

A new source-neutral CLI, tools/nsejs_source_custody_preflight.py:
- Reads the owner-reported year/subject test-expectation CSV and rejects missing/duplicated 2020–2024 subject/year rows.
- Checks the exact five required generated files per group, source-root presence, record count, unique safe IDs and per-question source_item.json/source-custody.json structure **when approved inputs exist**.
- Produces a JSON and Markdown metadata-only receipt. No questions, options, answers, keys, figures, private ZIP files or original examination text are exported.
- Never trusts custody_mode=EMBEDDED_VERBATIM or comparison_status=ORIGINAL_EXACT as *independent* source authentication.
- Offers a --require-files mode (exit 3 when inputs incomplete) and an independent --academic-gate mode (exit 4 for academic HOLD); the ordinary reporting mode completes successfully and honestly records missing inputs.
- Has synthetic negative tests for missing inputs, duplicate IDs, cross-subject IDs, unsafe IDs, and false proof by self-declared ORIGINAL_EXACT.

GitHub Actions publishes metadata-only custody receipts as an artifact while confirming strict and academic HOLD exit codes. The workflow's technical green status **does not** mean that question banks or source rights were recovered.

## Custody handoff — Agent A / owner

Use a private, access-controlled intake, never unverified public Git:

1. Identify the authorized original examination paper(s), answer keys and any essential figures by year, code, page and item number. Record SHA-256 from actual bytes, origin, version and rights.
2. Reconcile the source occurrence ID against the historic displayed ID, preserving conflicting aliases rather than overwriting them.
3. Provide per-item source_item and source-custody materials plus independently checked stem/options/key/figure fidelity. Their declarations are a starting point, not proof.
4. Run the existing deterministic source-preserving Core2 builders against approved inputs, producing the expected bank, intake, two Smart Label reports and HTML for each selected year/subject group.
5. Run the new preflight. Only when structural files are actually present can --require-files return zero; source/academic/QRT status remains HOLD until independent acceptance.
6. Update the canonical question UID, content revision, QRT operation and five-factor evidence through Agent A's source-controlled interface. Agent B then links Core1A teaching and Core1B fresh inference to accepted cognitive roles.

### Prioritization

- P0: Recover authentic Chemistry and Biology 2024 source/year bundles and their required figures; their public Core2 banks are presently unavailable.
- P0: Fix known Physics official-ID contradictions, absent figures, 48 producer-vs-observed stem hash discrepancies, and four nominated D3 score/band contradictions **without silently altering the source**.
- P1: Reconcile all 15 source-year test groups, including source rights and independent QRT, then construct verified public-safe exports.
- P1: Complete Agent B's remaining 18 test-backed Core1A/B journeys, address the 26-versus-27 discrepancy, and bind required Core2 operations to explicit teaching/transfer evidence.
- P1: Review and correct obsolete legacy preview-card test assumptions separately from missing private source fixtures; preserve test coverage and do not make CI green by skipping expected examinations.

## Acceptance

Stage 1 ACCEPTED only for a truthful, reproducible custody inventory and adversarial tests. Source intake, the full 237 author-test claims, Chemistry/Biology banks, original Physics fidelity, academic acceptance, overall QA and the remaining learner journeys all remain HOLD or NOT_RECEIVED.

No merge, no Pages deployment, no new original-source data publication and no academic approval inferred from software validation.


## Stage 1B — official PDF raw-byte custody achieved (12 November 2026)

The original Stage 1 note described PDF byte hashes as NOT_RECEIVED at that time. Subsequent exact-head GitHub Actions retrieved and hashed actual PDF bytes from IAPT HTTPS in ephemeral runner memory. No original PDF bytes were committed or uploaded as artifacts.

- All ten named 2020–2024 official paper/key PDFs now have SHA-256, byte size and page count. The older 2020 image-host PDF path returned HTTP 404, but the original IAPT uploads PDF (36 pages) was retrieved and hashed; its exact individual paper-code page span still requires review.
- Verified 2024 Code 51 paper: SHA-256 b80e3bae4e64aaad11f43cc12f07ef17ae495b75e231122d440b0f81709379e8; 1,189,141 bytes; 14 pages.
- Verified 2024 final key: SHA-256 6d56f6f4e7f3c6b7a0b7b6146c0e7e9386c035fc5988c5523fe6551fc9374926; 453,386 bytes; one page.
- Full ten-file digest ledger: docs/nsejs/official-2020-2024-raw-byte-custody-r1.json.
- Machine receipt: https://github.com/reallakshman19/Grade9v4.0/actions/runs/43230608507.
- Code 51 Q52's original-option substitution remains a P0 source defect (Issue #86). The authentic Q57 source drawing is not yet staged or independently matched.
- Source registry, exact figure/stem/key comparisons, academic correctness, QRT qualification, publication permissions and release acceptance all remain HOLD. Ten raw PDF SHA receipts are not ten approved native Core2 banks.

### Safe-publication boundary

Continue linking directly to original IAPT-hosted PDFs and publishing separately authored learning constructions. Do not embed or mirror whole original papers into a public source bank without verified rights, source/figure fidelity and independent academic acceptance. The fifteen legacy subject-year bank/input groups still lack reproducible production artifacts, independently of the ten PDF hash receipts.
