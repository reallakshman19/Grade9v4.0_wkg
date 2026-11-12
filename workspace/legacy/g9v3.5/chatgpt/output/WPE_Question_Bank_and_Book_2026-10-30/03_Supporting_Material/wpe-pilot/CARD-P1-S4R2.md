[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S4R2 · move M4 · 28 Oct 2026
First line of your reply: METER: <context used>; basis

RECHECK of wep07-core1ab-4f30041d.json (independent checker): PASS_WITH_NOTE. Repairs 1, 2, 3, 6, 7 verified. Fix these last items and return a new file:
a. Repair 5 not done: S07 is unchanged. Write an explicit Grade 9 test for "turning point vs at rest" into S07.
b. Physics: CYCLE-COM predict asks if the midpoint 2 m gives the energy change and answers No, but a rigid 0.5 m shift gives -20 J whichever centre is used. Reword it to ask for the initial U or the centre height.
c. CYCLE-RESET repeats W-A2's numbers (2 kg, x=2, 3 m/s, -2x) and CYCLE-COM repeats W-A3's (1 kg at 1 m, 3 kg at 3 m). Change the numbers so 1B does not repeat a solved 1A example.
d. attempt.produces does not ask for rubric[0] (declare system, coordinate, domain): align them. Trim three pre-attempt hint phrases: "explain one reason E=U may fail to mean reversal", "do not invent a turning point", "after a controlled force change write a new ledger".
e. attempt.model_response: a cart starting at equilibrium has E=0, not 4 J; fix. Optional: give CYCLE-ROTATION a U or turn element.

RETURN: new file wep07-core1ab-<first 8 of sha256>.json, then:
TASK EVIDENCE · P1-WPE-G9v35 · S4R2
- file: <name>, sha256 <full>
- items a-e: <done / not done, one line each, with the JSON path>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
