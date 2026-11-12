# WPE Core2 — coding candidate R1 (Oracle standalone, self-assessed)

**Status:** LOCAL_ENGINEERING_CANDIDATE / NOT_TRANSFERRED / NOT_CORE2_ADMITTED / NOT_OWNER_ACCEPTED.
**Governing published WBS:** G9v3.5 R5 (2026-10-29), WBS `4.2` and first instance `4.2.1`. No parallel WBS was created. This candidate is the *cross-cutting Core2 engineering admission/product mechanism*, not a claim that the six physics-idea tiles or the 21 original questions are finished.

## What is coded

- `src/core2_engine.py`: distinct source/key witnesses, digest/identity, provenance/rights, figures, versioned answer claims, SL2 0–2 anchors and D3/D4, disclosure of reviewer exposure, QRT counting home, curriculum pins and manifest admission preflight. No enum or source override.
- `src/r1_bridge.py`: reads original R1 dispositions and selection (unmodified), projects each pending record into the new proposed gate, preserves exposed proposals and aliases, leaves all missing authority unresolved.
- `src/build_core2.py`: `gate`, `package`, `fixture` commands. Package compilation derives `bank.json` and `manifest.json` with 21 unique qualifying selection homes; leaves native library `records.json` unchanged. Requires nonempty official evidence and named review receipts. Never confers academic approval.
- `src/learner_render.py`: **separate synthetic technical control only** (not the governed `Shared/tools/render_core.py`), attempt-first, typed answer, one-at-a-time labeled scaffold hints, delayed visual answer reveal, keyboard/touch layout, no pre-attempt solution in visible DOM. The solution is present in local JavaScript and is **not cryptographically protected**; production must use the governed renderer and appropriate answer-service policy.
- `fixtures/synthetic_question.json`: explicitly invented stress case tied to WPE idea `direction decides effect`; it is **not an examination original and earns no coverage**.
- `outputs/REAL_R1_SELECTION_PREFLIGHT.json`: all 14 leads blocked, seven source matrix vacancies, no question promoted.

## Reproduce tests

```
PYTHONPATH=src python -m unittest discover -s tests -v
python tests/browser_test.py
PYTHONPATH=src python src/build_core2.py fixture --question fixtures/synthetic_question.json --out outputs/SYNTHETIC_CORE2_GOLDEN.html
PYTHONPATH=src python src/build_core2.py gate --admissions outputs/REAL_R1_SELECTION_PREFLIGHT.json --out outputs/REAL14_GATE_RECEIPT.json
```

`gate` intentionally exits **2** on real current R1 HOLD. Browser tests run in Chromium with `set_content` because this environment blocks `file://` and `127.0.0.1` navigation. No live HTTP deployment test is claimed.

## Source basis

- Original frozen source ZIP `WPE_CORE2_21_REVIEW_CANDIDATE_20261030.zip`: SHA-256 `f9f5cf75652f20483d44e837c564fe4635e55aa75dd6007d988c297e82ef82c4` independently rechecked this turn.
- R1 dispositions SHA-256 `796d1a7b579182abb9cbb15e7aef8ee0c65f5028cf278b2ac65ffc87418c3dfd`.
- R1 selection SHA-256 `4eed0a28a32a3e64f018a4506102781417e57bad7d586b3f6d239a0d9a036a97`.
- Current Grade9v3.5 main pinned at `8a02a8eb23ea37a7d8acb74d1bc193dd17657e5b`; examined `Shared/roles/CORE2.md`, `Shared/tools/core2_v2.py`, `Shared/tools/blueprint_spec.py`, `Physics/candidates/phy-work-energy-power.v1.json`, `products/physics/phy-work-energy-power.manifest.json`, `Physics/units/phy-work-energy-power/UNIT.md`.
- User-supplied template `core 2 template(1).zip`, current canonical WPE R1/R2 supplied documents; synthetic fixture is not derived from exam text.

## Not done and why

1. **No real 21-question product:** zero independently admitted exam originals; 14 pending and 7 vacancies in R1. Academic acceptance is external and remains NOT_RUN.
2. **No authoritative WPE topic-adapter selection:** multiple versions; approved semantics and pin absent. Proposed gate enforces approval references but cannot verify the signer's authority itself.
3. **No native governed renderer tests:** actual current Grade9v3.5 checkout and dependencies not present in this container; GitHub connector read source only. `render_core`, strict quality gate, generated PDF and native browser workflow are NOT_RUN.
4. **No public upload, agent dispatch, relay transfer, or Progress Page sync:** current G9v3.5 page still marks `mode=otm`; no `oracle-cycles/g9v35/CURRENT.json` is on Common main. Owner selected Oracle standalone in this chat, but control handover is not enforced.
5. **Native SL1/SL2 digest semantics remain unchanged.** Derived build fingerprint is new, version-bound and explicitly not a substitute for native digests.

## Next connected delivery

Review/integrate `src/core2_engine.py` against exact Grade9v3.5 master schema and existing `Shared/tools/core2_v2.py` + `Shared/tools/render_core.py`; replace synthetic renderer with native golden fixture only once one WPE question is independently admitted and the topic-adapter/rights states are resolved. The second delivery is a separate independent technical QA pass for the exact integrated candidate; no automatic adoption on author self-tests.
