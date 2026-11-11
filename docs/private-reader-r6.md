# R6 — Private reader scoped links and local practice

**Mode:** contributor SELF_REVIEW; public-safe tooling, synthetic CI only. This branch contains no original owner question payload, exam figure, or generated private review page. No academic approval inferred from software validation.

## Technical fix

On a recipient-verified R5 private review site, `tools/private_reader_r6.py` generates a new, separately pinned review-only directory. Original source HTML files remain unchanged; canonical question/answer JSON is byte-for-byte semantically identical. It rejects stale hashes, symlinks, unlisted output paths, attempted overwrite, invalid release claims and unexpected reader source patterns.

The generated reader uses subject/topic + source occurrence + question ID for navigation. If a legacy unscoped alias matches two records, it displays an explicit selection list instead of selecting the first. An exact fully scoped link still resolves automatically; an unknown link is not silently replaced by the first question.

The generated browser-local practice state is keyed to a SHA-256 revision covering all question fields, the answer/key and actual available figure byte digests (with missing figures explicitly represented). It preserves a committed first response and help/reveal events when browser storage permits; it reports `NOT SAVED` if storage fails. Local browser data is **not a secure exam attempt or independent evidence**. Content changes produce a different revision and do not silently reuse a stale first attempt.

Required unavailable diagrams stay blocked. Original examinations, scientific validity, QRT qualification, academic release, and published Pages remain HOLD.

## Execution — authorized private local machine only

```bash
python tools/private_reader_r6.py --site /private/verified/R5_review_site --out /private/R6_review_site
```

The R5 private input must have `.GRADE9_PRIVATE_REVIEW_ONLY` and `PRIVATE_REVIEW_MANIFEST.json` with pinned HTML files. R6 writes a new manifest with all emitted hashes and `runtime_profile: r6-revision-scoped-local-attempts`. Never commit or publish that output.

## Public-safe CI

```bash
python -m pytest -q tests/test_private_reader_r6.py
python -m playwright install chromium
python tools/check_private_reader_r6_http.py
```

The browser workflow exercises synthetic questions over real HTTP at 1280×800, 1472×920 and 800×1280. Smartphone HTTP is not required. Synthetic results do not prove private-candidate HTTP acceptance. Any private browser administrator block is recorded as NOT_RUN rather than bypassed.

## Review and release status

This is stacked atop Draft PR #74, whose base is the verified public baseline. It does **not** reconstruct the original producer branch. Separate exact-head independent review is needed before merge. Missing official papers/figures, original keys, Core1A/Core1B and QRT receipts cannot be automatically generated or approved.