[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S6R · move M10 · 28 Oct 2026
First line of your reply: METER: <context used>; basis

CHECK of wep02-core1ab-a74b883f.json (independent checker): FAIL, text repairs only. Every number, sign and area recomputes correctly. The visible conventions C1–C3 are clean. Fix these and return a new file; nothing else changes.
BLOCKING (the pre-attempt text gives away the trap or the recipe)
1. CYCLE-SPRING-ENDPOINTS: produces must ask for the outcome ("the work done by the spring and by the pull for this stretch, with justification and units"), not list the steps or say "compare initial/final spring energy". The predict must not name the "whole stored energy" trap; use a neutral question ("How should the work for the stretch from x1 to x2 be found?").
2. CYCLE-COMPRESS-THROUGH-ZERO: remove "split the path at x=0, calculate the two signed triangular works". Ask for the total spring work with units, and what can be said about the external work. Neutralise the predict ("always restores toward x=0").
3. CYCLE-CROSS: remove "break the graph into regions" and "whether force=0 at x=3 requires the puck to stop". The predict must not state the sign trap ("sum of two positive magnitudes"). Ask for the work from x=1 to x=5 and what the zero force at x=3 tells you.
MODERATE
4. CYCLE-GRAPH produces: ask for the work and a justification, not the step list or the endpoint hint.
5. microtopic.elicitation.attempt: give one concrete graph or a checkable numeric target; the rubric should test an outcome, not the presence of parts.
6. CYCLE-REVERSE and CYCLE-NEGATIVE: soften the predicts ("must have the same sign", "negative at both endpoints") and drop "check the total over the two legs".
7. Numbers: Core1B must not mirror Core1A. Change CROSS's net +2 J (same as A2), REVERSE's 2→8 N over 3 m (MIS01), the GRAPH structure 0→5 m (A1), and the exit task's x1 = 0.10 m (A4).
8. Oracle decision: ONE jump. "The signed area under the force–position graph generalises F × s; the ideal spring is the straight-line case." Move the by/against-a-spring comparison (and its slow, frictionless assumptions) into conventions.
9. core1b.extension_marker says "NONE" while proposed_extension_candidate says CANDIDATE. Make them agree, per CORE-AUTHORITY-CONTRACT.
MINOR
10. S07: construct ½kx² as the triangle (base x, height kx) inside the step. 11. SCN02-CROSS: "piecewise-straight", not "a line". 12. relation.model_assumptions: "area-based work", not "integral-by-area". 13. NEGATIVE and SPRING boundary tests: use a limiting case (e.g. x1 = 0 gives ½kx2²), not a trivial zero. 14. SPRING predict: say "slowly, no friction" before mentioning the balancing pull.

SAVE: save the file to the Owner's Google Drive folder <DRIVE_FOLDER> (and also offer it as a download here).

RETURN: new file wep02-core1ab-<first 8 of sha256>.json, then:
TASK EVIDENCE · P1-WPE-G9v35 · S6R
- file: <name>, sha256 <full>, Drive: saved yes/no
- items 1-14: <done / not done, with the JSON path>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
