[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S5R · move M9 · 28 Oct 2026
First line of your reply: METER: <context used>; basis

CHECK of wep01-core1ab-9e95dde5.json (independent checker): FAIL, text repairs only. Every number, sign and angle recomputes correctly. Fix these and return a new file; nothing else changes.
BLOCKING
1. microtopic.exit_task: the prompt says three forces and "no other forces", but the answer adds gravity as a fourth. Make the prompt and the answer agree.
2. core1b.concept_cycles ANGLE, ZERO, OWNERSHIP, FRAME: predict.defensible_answer must answer the prompt (now e.g. "Choose the board.", "Target: bag.", or a restatement).
3. Oracle decision: Grade 9 uses the ground frame only. Mark frame-dependence of work (W01-A5, CYCLE-FRAME, MIS06, SCN05) as "beyond Grade 9, given", or replace CYCLE-FRAME with a ground-frame cycle. Remove any non-inertial-frame content (scope.excluded lists it).
MODERATE
4. Predict prompts must not name the trap ("travelled distance", "drive-force alone"), and attempt.produces must ask for the result, not spell out the recipe; the learner rebuilds the jump.
5. Visible conventions C1 and C3 give away CYCLE-OWNERSHIP before the attempt: defer them or neutralise them.
6. Add one Core1B cycle (or boundary test) that elicits the s = 0 case taught in A4 and MIS07.
MINOR
7. Declare "rigid body" as a general convention. 8. CYCLE-ANGLE: change the 60° angled-pull structure, and SCN04's 9 N, 5 m, +45 J, so 1B does not mirror A1. 9. S04: construct the cos θ projection (component along the displacement) rather than assert it. 10. Make the OWNERSHIP and FRAME boundary tests a reasoning task, not a recall yes/no.

SAVE: save the file to the Owner's Google Drive folder <DRIVE_FOLDER> (and also offer it as a download here).

RETURN: new file wep01-core1ab-<first 8 of sha256>.json, then:
TASK EVIDENCE · P1-WPE-G9v35 · S5R
- file: <name>, sha256 <full>, Drive: saved yes/no
- items 1-10: <done / not done, with the JSON path>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
