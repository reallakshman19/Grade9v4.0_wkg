[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S4R · move M3 · 28 Oct 2026
First line of your reply: METER: <context used>; basis

S4 CHECK (independent checker, file wep07-core1ab-def19622.json): PASS_WITH_NOTE. Physics and routes are correct (Q1 d, Q2 a, Q3 a-d, Q4 b,c); no stems or options leaked; one shared jump. Repair these, in this order, and return a new file:
1. Attempt-first: remove bucket.conventions C4 ("reject E<U") and C6 ("E=U gives K=0") from core1b.pre_attempt_visible; they give the jump away before the attempt.
2. Core1B parity: give reset, centre-of-mass, completing-the-square and rotation each a real predict / attempt / rubric item (now one-line route asks only). Make coverage_keys match the content.
3. The jump: widen its first clause so Q1 (effective potential), Q2 (centre-of-mass U, no turning point) and Q4 (choosing the piece/system) sit inside it. Keep it ONE jump.
4. Rubric criterion 6 asks for things the attempt never asks; align them. Strengthen the weak boundary test.
5. Add a Grade 9 test for "turning point vs at rest"; state the missing assumptions: Q4(c) break at the vertical after horizontal release; Q1 static equilibrium before reversal, ideal spring, constant force; drop "cart held at equilibrium" wording (non-conservative hold).
6. Replace worked anchors that mirror slice questions (W-A3 = Q2 key step, W-A2 = Q1 structure, core1b route[7] = Q3 solution shape) with non-isomorphic ones; add one unbounded (no second turning point) example.
7. Fix source_ref bindings (S01, S02, S09, S10), complete entry_assumptions, add scenes beyond U = x^2, and mark the rod-break/fracture text in S10, SCN03, MIS05, route[5] as extension (beyond Grade 9). Flag the z = x0/x substitution and kx^2/2, -Fx potentials as stretches.
Keep answer-bearing fields (letters, option formulas) marked hidden-from-learner.

RETURN: new file wep07-core1ab-<first 8 of sha256>.json, then:
TASK EVIDENCE · P1-WPE-G9v35 · S4R
- file: <name>, sha256 <full>
- repairs 1-7: <done / partial / not done, one line each>
- jump (new wording): <one sentence>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
