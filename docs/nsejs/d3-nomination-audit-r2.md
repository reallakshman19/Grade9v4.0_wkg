# Grade9 NSEJS Physics QRT — Eight D3 Nomination Review R2

**Evidence boundary:** Based on PR #80 public candidate source and common Physics five-factor rubric ranges in `src/grade9qa/qrt_binding.py`. A band-score consistency check is not an independent academic QRT adjudication.

| Source occurrence | Topic | Producer operation | Nominated band | Five-factor score | Score-based band | Finding |
|---|---|---|---|---:|---|---|
| `NSEJS-22-OPT-01` | OPTICS | SYNTHESIZE | D3 | 6 | D3 | Numerically consistent; academic HOLD |
| `NSEJS-22-OPT-02` | OPTICS | SYNTHESIZE | D3 | 6 | D3 | Numerically consistent; academic HOLD |
| `IOQJS-21-OPT-01` | OPTICS | SYNTHESIZE | D3 | 7 | D3 | Numerically consistent; academic HOLD |
| `NSEJS-19-OPT-02` | OPTICS | SYNTHESIZE | D3 | 2 | D1 | RUBRIC_BAND_MISMATCH · HOLD |
| `NSEJS-FND-ELEC-04` | ELECTROSTATICS | MODEL | D3 | 5 | D2 | RUBRIC_BAND_MISMATCH · HOLD |
| `NSEJS-FND-CIRC-01` | CURRENT_ELECTRICITY | MODEL | D3 | 5 | D2 | RUBRIC_BAND_MISMATCH · HOLD |
| `NSEJS-FND-CIRC-02` | CURRENT_ELECTRICITY | SYNTHESIZE | D3 | 5 | D2 | RUBRIC_BAND_MISMATCH · HOLD |
| `NSEJS-18-MAG-01` | MAGNETISM_AND_EMI | SYNTHESIZE | D3 | 6 | D3 | Numerically consistent; academic HOLD |

**Four material contradictions:** `NSEJS-19-OPT-02` is nominated D3 but score 2 (D1 range). `NSEJS-FND-ELEC-04`, `NSEJS-FND-CIRC-01`, `NSEJS-FND-CIRC-02` are nominated D3 but score 5 (D2 range). Do not silently rewrite scores or relabel question demand; require independent five-factor evidence and protected learner-task review.

**Remaining four:** Numeric D3 range is consistent, but this alone does not establish D3 cognitive qualification. Operation direction, source authenticity, scientific model validity, Core1A/B correspondence, original figure dependency and independent review remain unverified.

**D4:** No candidate scores 8–10 and no D4 nomination is in the observed 50. The common draft Physics Blueprint requests D3/D4 coverage across seven operations, but is `DRAFT_OWNER_REVIEW`; it is not a verified syllabus denominator or admission receipt. All fourteen generic Blueprint cells need Owner/academic scope and topic adapter evidence, not fabricated D4 labels.

**Source evidence:** Five official paper locators and keys were compared against IAPT Paper Code 51, as documented separately; the other 45 examination source claims are NOT independently verified. QRT outcome for all 50 is HOLD.

**Negative control:** `python tools/nsejs_core2_audit.py --strict-qrt` is expected to exit nonzero until this genuine inconsistency is resolved with authoritative evidence. Public candidate preview may remain available with explicit HOLD; a strict academic release must not pass.

**No academic approval inferred from software validation.**
