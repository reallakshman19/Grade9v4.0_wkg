[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S4R3 · move M5 · 28 Oct 2026
First line of your reply: METER: <context used>; basis

RECHECK of wep07-core1ab-8761d7da.json (independent checker): PASS_WITH_NOTE. Items a-e all verified, no regressions. Two last fixes, nothing else changes:
1. core1b.concept_cycles[id=CYCLE-COM].attempt.rejected[1] contradicts itself: it calls the midpoint "wrong for dU=-70 J" and then says dU is unchanged. Rewrite: the midpoint gives the right dU under a rigid shift but the wrong absolute initial U (280 J vs 340 J).
2. Neutralise three mild pre-attempt hints in attempt.produces: CYCLE-COM (names the midpoint comparison), CYCLE-ROTATION (says the old inertia is invalid), CYCLE-RESET ("force-free track"). Ask for the quantity, do not point to the trap.

SAVE: save the new file to the Owner's Google Drive folder <DRIVE_FOLDER> (and also offer it as a download here).

RETURN: new file wep07-core1ab-<first 8 of sha256>.json, then:
TASK EVIDENCE · P1-WPE-G9v35 · S4R3
- file: <name>, sha256 <full>, Drive: saved yes/no
- fixes 1-2: <done / not done, with the JSON path>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
