# E1 handoff — Core2 integration, bounded proposed next task

**Status: PREPARED / NOT_DISPATCHED / NOT_TRANSFERRED.** Candidate author: Oracle standalone (contributor and self-tester). Recipient: E1 builder/engineering integrator — NOT YET ASSIGNED. Governing WBS: **G9v3.5 published R5 → 4.2 → 4.2.1**. This is not an additional project WBS.

**Why:** Current WPE R1 is a source assessment catalogue, while Grade9v3.5 `products/physics/phy-work-energy-power.manifest.json` has `selection.core2=[]`. Build a source-bound, template-compliant Core2 path without promoting proposals.

**Exact local candidate:** `WPE_CORE2_CODING_CANDIDATE_R1.zip` with SHA-256 in root receipt. Input original archive SHA-256 `f9f5cf75652f20483d44e837c564fe4635e55aa75dd6007d988c297e82ef82c4`. Existing R1 original records and native SL1/SL2 overlays remain untouched. Current Grade9v3.5 main `8a02a8eb23ea37a7d8acb74d1bc193dd17657e5b`.

**One implementation slice:** Inspect and reconcile our `core2_engine.py` against `Shared/roles/CORE2.md`, `Shared/tools/core2_v2.py`, `Shared/tools/render_core.py`, the native package schema and the pinned registry; implement one *synthetic* end-to-end canonical build/renderer/quality pass as a technical control, with a negative case (official paper missing or D2 substitution) failing. Do not author or adapt WPE exam questions to fill coverage. Only after a real independently admitted WPE original exists may a second distinct WPE golden be attempted. If project requires a narrower 4.2.1 tile, use the verified WBS and keep this cross-cutting engine as an integration dependency rather than silently replacing the tile.

**Expected return:** PR/diff against exact main, declared candidate byte manifest, tests and failures, reproduced negative case, actual native renderer and browser evidence, source–schema incompatibilities, and next actor. Attach via authorized Common `relay/AGENT_WORK` or approved private Drive; receiver independently verifies bytes. An in-chat sandbox link is LOCAL_ONLY, not completed transfer.

**STOP IF:** WBS/mode authority conflicts, adapter unapproved, source/key/figure unverified, missing governing renderer, or attempt to mark an author-exposed proposal as academic admission. Do not modify review enum, freeze baseline, registry source bytes, release settings or Progress Page controls in this engineering task. Do not claim a synthetic answer lock protects secrets from page-source inspection.

**Review:** Distinct independent technical reviewer after E1 return. Independent Physics admission stays a separate academic task, currently prepared at Grade9v3.5 #313 and unassigned.
