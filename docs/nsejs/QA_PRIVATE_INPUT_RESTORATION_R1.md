# Grade9 v4.0 — Full Python QA restoration protocol (R1)

**Status:** SOURCE_INPUTS_MISSING · FAIL_CLOSED. This is an engineering handoff, **not** a software, academic or source-authenticity release certificate.

## Verified clean-checkout QA finding (2026-11-12)

The unfiltered repository suite was run on Python 3.11 and 3.12 and still failed with **26 failures and 424 errors**. A diagnostic receipt observed at least **30 distinct missing source-file paths** under `workspace/sources` and **187 distinct missing generated-output paths** under `workspace/output`. The paths come from failed tests and are a **lower bound, not a complete source corpus inventory**. At least one failure (mathematics Question Status preview expecting ten polynomial questions on a WPE-focused page) requires separate product-scope reconciliation.

The **public-source-neutral** lane is separately tested and may be green; that is **not full repository QA**. Both private-input and output-dependent tests remain in the unfiltered suite; nothing is skipped, excluded or declared an expected failure.

## Authorized source recovery (Owner action)

1. Identify each source that the private test modules require, including an independently checkable source-custody record, authorized original source files, and any expected generation scripts. Verify ownership/usage rights; do **not** commit private exam papers or source records to public Git.
2. Generate `workspace/output` with the approved source-bound pipeline wherever possible. Do not create fake custody receipts, fake answer keys or empty files to satisfy path checks.
3. If restoring an **independently verified private backup**, place its files in a private ZIP using repository-relative paths under `workspace/sources/` and `workspace/output/`. Create a separate JSON manifest:

```json
{
  "schema": "grade9-private-qa-input-bundle/v1",
  "academic_approval": "HOLD",
  "files": {
    "workspace/sources/<subject>/<item>/source-custody.json": "<actual SHA-256>",
    "workspace/output/<module>/bank.json": "<actual SHA-256>"
  }
}
```

The above entries are **placeholders**. Replace them with the real verified files and hashes. Obtain both the manifest SHA-256 and the archive SHA-256 independently from the Owner.

4. Run the checksum-pinned tool **outside any public CI storage or checked-in commit** (the first command performs no write):

```sh
python tools/qa_verified_input_restore.py \
  --bundle /private/qa-inputs.zip \
  --manifest /private/qa-inputs.json \
  --expected-bundle-sha256 <OWNER_VERIFIED_ZIP_SHA256> \
  --expected-manifest-sha256 <OWNER_VERIFIED_MANIFEST_SHA256>
```

To restore verified workspace bytes only after checking the receipt, add `--restore`. The tool rejects path traversal, symlinks, out-of-scope files, unexpected members, conflicting existing bytes, digest mismatches, and manifests claiming academic approval. It does not itself verify academic fidelity or correctness of the upstream sources.

5. Run the **entire unchanged** strict suite and the dependency receipt on **both** Python versions:

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

The return codes must all be zero to qualify **technical full-suite QA**. Even then, original NSEJS source fidelity, QRT, independent scientific correctness, live Pages deployment and observed student mastery require distinct approval.

## Release guards

- Do not change or weaken existing content tests merely because source data is absent.
- Do not suppress test collection, use blanket skip/xfail or overwrite source files with synthetic fixtures.
- Preserve the full CI run's nonzero result until actual authorized evidence exists and all assertions pass.
- Do not upload private original papers to the public GitHub Actions artifact, HTML preview or Git history.
- Any existing public-only pass is a **subset** result and cannot be renamed “full repository QA PASS.”

**Open release prerequisite:** locate and independently verify the private source/output dataset, then repair remaining genuine assertions and rerun the exact merged revision.
