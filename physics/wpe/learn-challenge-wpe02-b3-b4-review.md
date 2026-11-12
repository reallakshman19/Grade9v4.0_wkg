# WPE-02 · Core1A B3 / Core1B B4 sufficiency review

**Date:** 2026-11-02 · **Reviewer posture:** author-exposed analytical review, *not* independent QRT, blind academic subject sign-off or Owner approval.  
**Scope:** the five existing candidate Learn → Challenge pairs, referenced by `learn-challenge-source-map.json`.  
**Decision:** **HOLD** for native academic promotion. B3 and B4 are noncompensatory, and no student reconstruction evidence has been collected.

## Criteria and overall result

- **B3 — Teaching sufficiency:** Does Core1A *work through* the decisive cognitive operation and physical conditions, rather than merely state a rule?
- **B4 — Fresh reconstruction:** Is Core1B a genuinely new, appropriately supported task; and is there evidence a learner can solve it independently without copying the guided route?
- The guidebook distinguishes **constructed design**, **actual learner evidence**, **independent academic qualification**, and **Owner release**. Technical UI tests do not prove B3 or B4.

| Construction | B3 review | B4 design assessment | Academic B4 evidence |
| --- | --- | --- | --- |
| work-sign | HOLD — coverage gap | Weak transfer | HOLD — no independent learner evidence |
| momentum-energy | HOLD — coverage gap | Weak transfer | HOLD — no independent learner evidence |
| energy-motion | HOLD — coverage gap | Promising transfer design | HOLD — no independent learner evidence |
| potential-force | HOLD — coverage gap | Promising transfer design | HOLD — no independent learner evidence |
| momentum-fragments | HOLD — coverage gap | Promising transfer design | HOLD — no independent learner evidence |

## Question-by-question analytical findings

### 1. work-sign · source Q1, Q3, Q7

**B3 — HOLD.** The sole guided calculation gives negative friction work (−30 J). Positive/zero cases and the net-work versus one-force distinction appear only as general prose, not demonstrated decisions. Q7's source force/distance ambiguity is still unresolved.

**B4 — HOLD.** The robot challenge repeats an opposed-force calculation twice and adds the values; it is not merely a numerical clone, but the decisive sign rule is repeated without meaningful new force-model selection.

**Science/key check (editorial only):** A. −6×4−4×2=−32 J

**Candidate remediation:** Add distinct guided force–displacement decisions for +, − and zero work and demonstrate net work without copying the reserved robot task. For B4: Review replacement with a changed condition where the learner chooses which force reverses, distinguish fixed-direction and resistive forces, and justify each sign; preserve a genuinely unseen stem.

### 2. momentum-energy · source Q2, Q4, Q8

**B3 — HOLD.** The worked case is one numerical K=p²/(2m) substitution. Equal-p mass comparison, equal-K mass comparison, momentum doubling and the K–p parabola are stated in a note, not worked or graphically reasoned.

**B4 — HOLD.** The equal-p 1 kg/4 kg comparison is a near-direct application of a rule explicitly displayed directly above the challenge; the new ratio calculation is not sufficient evidence of independent model selection.

**Science/key check (editorial only):** A. K_A=64/2=32 J, K_B=64/8=8 J, ratio 4:1

**Candidate remediation:** Construct two or three non-reserved guided comparison/graph moves, with conditions; retain the separate original Q2/Q4/Q8 source references. For B4: Propose a fresh data/graph interpretation requiring the student to determine whether mass or momentum is held fixed, then justify which relationship applies.

### 3. energy-motion · source Q5, Q6, Q9

**B3 — HOLD.** The guided step evaluates K and v at one point, then states reachability and turning-point rules. It does not demonstrate a guided whole-path decision. Source Q5's distinction between uniform change with time and nonlinear change with height remains a note, not an assessed construction.

**B4 — HOLD.** Testing reachability across an intervening energy barrier is a meaningful operation change from a one-point energy calculation. The initial task omitted g; it now explicitly states 10 m/s². No independent learner reconstruction has been observed.

**Science/key check (editorial only):** B. At ridge U=(1 kg)(10 m/s²)(6 m)=60 J > E=50 J; inaccessible

**Candidate remediation:** Create a different guided path/turning-point sequence before the reserved ridge challenge; handle Q5 as an explicit additional construction or narrow the mapping. For B4: Preserve the distinct ridge task and first-response record; get independent review that the taught path reasoning is sufficient without leaking the exact barrier decision.

### 4. potential-force · source Q10

**B3 — HOLD.** Core1A solves one differentiable algebraic linear potential and includes a prose finite-slope example. It has no guided two-interval reconstruction of force from a plotted potential, nor a worked nondifferentiable-corner boundary.

**B4 — HOLD.** The student must calculate two interval slopes and apply the negative-gradient sign, which is a genuine representation/segmentation change. The answer options do not test the corner, even though the old mapping claimed it did; mapping now corrected.

**Science/key check (editorial only):** A. Slopes +4 and −3 J/m imply forces −4 and +3 N on the two open intervals; at x=2 derivative undefined

**Candidate remediation:** Teach a contrasting graph-slope example and differentiability boundary without reproducing the reserved piecewise values or shapes. For B4: Keep the open-interval claim precise. If corner interpretation is an intended target, assess it with a separate genuinely fresh prompt after sufficient teaching.

### 5. momentum-fragments · source Q11

**B3 — HOLD.** The example relies on a rest-start system with zero initial momentum. A prose transfer note says to compute nonzero initial momentum if moving, but does not guide such a model decision. The calculation of energy change for moving-parent fragmentation is also not guided.

**B4 — HOLD.** Unlike the guided rest case, the challenge requires conservation with nonzero initial momentum plus an independent kinetic-energy comparison; physics answer is consistent, but no student reconstruction or approved scope evidence is present.

**Science/key check (editorial only):** A. p_initial=8; p_small=5, v_heavy=(8−5)/1.5=2 m/s; K_initial=16 J, K_final=28 J, change +12 J

**Candidate remediation:** Teach a guided nonzero-initial-momentum conservation setup using a different context and values, plus explicit energy-source accounting; retain the reserved moving-parent task. For B4: Obtain WPE scope authorization and independent B3/B4 review; use first-attempt reasoning evidence rather than answer-option agreement.

## Immediate scientific/editorial correction

The **Energy and Motion** Core1B ridge problem previously relied on the adjacent Core1A problem to supply gravitational acceleration. Its independent stem now explicitly says **“Take g = 10 m/s²”**; the source map mirrors that correction. With this condition, its answer remains B. This is an editorial repair, not academic acceptance.

The **Potential Energy and Force** mapping previously claimed the challenge assessed an undefined force at the sharp corner. The current answer options only test open intervals, so the mapping now describes that narrower operation honestly. The worked check may explain the corner, but it does not turn an unasked condition into assessment evidence.

## Cross-cutting evidence limitations

- Source Q1–Q11 form an unverified scan; source claims, publisher, rights and answer-key custody are not qualified
- Source maps describe themes rather than accepted task-level QRT operations; Q7/Q9/Q10/Q11 flags remain
- Core1A and Core1B appear simultaneously side-by-side (desktop); students can consult worked steps while answering, and the answer key is available in downloaded JS
- Locking with a choice and eight characters cannot show that reasoning is correct; localStorage and reset are learner-controlled; no independent attempt witness
- No protected learner-response dataset, independent reasoning rubrics or observed changed-condition transfer is present
- The optional two hints and worked check are provided after the local lock but are not validated independent learning evidence
- Original Q12 is truncated and excluded

## Acceptance path and next scoped authoring proposal

1. Subject expert and Owner resolve source/Blueprint/adapter and Core2 dependencies for the exact task scope. No fabricated QRT difficulty or signed decision is permitted.
2. Repair **B3** by creating *different* guided examples for the missing decisive operations (contrasts, graph use, whole-path energy, piecewise force, nonzero momentum), preserving challenge confidentiality.
3. Re-review **B4 design** using an operation-level task-to-teaching matrix; the two weak-transfer tasks need a specific new model-selection or condition-change decision, not simply additional arithmetic.
4. Obtain protected, independently assessed reasoning evidence from students or a properly scoped validation protocol; checkbox answers alone cannot prove reconstruction. Use a secure record if formal assessment is intended.
5. Conduct an independent academic review and Owner approval before any native Core1A/Core1B promotion.

**No status changes:** `native_core1a=NOT_ACCEPTED`, `native_core1b=NOT_ACCEPTED`, `qrt=NOT_RUN`, `blueprint_adapter=UNSELECTED`, `owner=PENDING`.

The companion machine-readable file is `learn-challenge-wpe02-b3-b4-review.json`. Earlier WPE-01 was a technical remediation, not an academic acceptance.
