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
