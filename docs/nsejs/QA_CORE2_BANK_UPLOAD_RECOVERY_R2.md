# Grade9 v4.0 — Owner Core2 QA Bank Recovery (2026-11-13)

**Task:** `G9V4-CORE2-QA-BANK-RESTORE-R2`

**Scope:** PRIVATE_WORKSPACE_OUTPUT_RECOVERY_ONLY · SOURCE_FIRST · FAIL_CLOSED

## Actual owner ZIP

Archive filename: `G9V4_ALL_CORE2_QA_BANKS_20261113.zip`

SHA-256: `f590bb80577143eb4a31c3fb8e58599ef722a624cdbde5774b88405f89f2ce51`

The archive contains 210 non-directory members. All 208 manifest-listed members were independently SHA-256 verified; the remaining README is informational and not included in the manifest. Its 47 standard module directories contain 197 restorable Core2 output files. Six separate `G9V4_LOTS` bank exports are deliberately excluded from restoration because they are tracked in a different repository area and should not be overwritten.

The archive contains **no original `workspace/sources/**/source-custody.json` records** and no SL1/SL2, Core1A/Core1B construction, reconstruction, witness or learning-journey proof. Its own audit states `academic_admission = 0 / 237 ADMITTED`; the global listing has 335 candidate question records, not 335 independently approved exam questions.

## Exact dependency comparison

Compared against the separately obtained SHA-backed CI artifact from the final Wave 3/QA integration job:

| QA prerequisite | Observed missing | Exact output paths recoverable from uploaded ZIP | Remaining missing |
|---|---:|---:|---:|
| `workspace/output/**` | 187 | 68 | 119 |
| `workspace/sources/**` | 30 | 0 | 30 |

The 68 matching outputs are 41 `bank.json`, 16 `core2_module.html`, and 11 `questions.json` files. The missing 119 outputs include 31 SL1 reports, 16 SL2 reports, and 72 Core1 construction/reconstruction/learning-journey/witness artifacts.

Separate content issue identified by an independent QRT structural check: `CHEM-NSEJS-REACT-02` has `op=JUSTIFY` and `crux_move_ref=...-M2`, while `tests/test_chem_chemical_substances.py` expects JUSTIFY → M3. This needs evidence-based academic resolution, not a guessed source edit.

## Exact safe restore procedure

1. Retain the ZIP **outside public Git**. In a private checkout of the repository, independently verify the archive SHA shown above.
2. Run the dry-run preflight (it does not extract or write):

```sh
python tools/qa_core2_bank_archive.py \
  --archive /private/G9V4_ALL_CORE2_QA_BANKS_20261113.zip \
  --expected-sha256 f590bb80577143eb4a31c3fb8e58599ef722a624cdbde5774b88405f89f2ce51 \
  --root /private/Grade9v4.0
```

3. Only after checking the report and destination, repeat with `--apply`. Existing conflicting bytes and symlinked target paths are refused. No source custody is invented and no tracked LOT output is overwritten.
4. Restore the **separate authentic custody and SL1/SL2 + Core1** evidence, using the governing `QA_PRIVATE_INPUT_RESTORATION_R1.md` and any independently signed source review receipts. Do not fabricate them from question-bank contents.
5. Run the entire original unfiltered QA on Python 3.11 and 3.12:

```sh
python tools/qa_reproducibility.py bootstrap
python tools/qa_reproducibility.py run \
  --json-out qa-artifacts/failures.json \
  --junit-out qa-artifacts/junit.xml
python tools/qa_failure_triage.py \
  --json-in qa-artifacts/failures.json \
  --json-out qa-artifacts/root-causes.json \
  --markdown-out qa-artifacts/root-causes.md --strict
```

The source-neutral CI lane passing remains independent of the full suite. Neither importer execution, checksum verification nor partial test recovery constitutes original NSEJS source fidelity, scientific accuracy, academic release, student mastery or permission to deploy to GitHub Pages.

**Next source gate:** obtain an original custody-linked workspace package (not just banks) covering the 30 observed missing source records, SL1/SL2 artifacts and 18 protected Core1 module builds; resolve QRT and Mathematics preview differences from real academic evidence, then rerun strict full QA without skips or xfails.
