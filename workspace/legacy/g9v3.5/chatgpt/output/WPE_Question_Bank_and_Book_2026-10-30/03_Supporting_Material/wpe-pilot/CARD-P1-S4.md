[OTM · Oracle] TO P1-WPE-G9v35 · G9v3.5 · CARD S4 · move M2 · 27 Oct 2026
First line of your reply: METER: <your context used, as a percentage or token count>; basis (last time the line came back as the template)

S3 RESULT (independent checker, read the IAPT papers and keys)
- WEP07-01 2024 Q4 PASS; WEP07-02 2024 Q32 PASS; WEP07-03 2025 Q57 PASS_WITH_NOTE (key from the solution PDF only); WEP07-04 2024 Q59 PASS_WITH_NOTE (needs rotation; only b, c test WEP-07); WEP07-05 2019 Q19 PASS_WITH_NOTE (needs SHM, weak fit).
- Oracle decision: the slice is WEP07-01, -02, -03 (core) and -04 (extension, "needs rotation"). WEP07-05 leaves WEP-07.
- Core2 will be crops of the official IAPT pages, made locally. You do not write Core2.

TASK S4 (W4): ONE Core1A/1B pair for key idea WEP-07, built for this slice
- Read Shared/roles/CORE1A.md, CORE1B.md and CORE-AUTHORITY-CONTRACT.md (public repo reallakshman19/Grade9v3.5) and follow them exactly.
- Core1A and Core1B share ONE inferential jump: the crux the four questions have in common. Name that jump in one sentence first, then show how each of the 4 questions uses it (1-2 lines each, no full solutions, no question text).
- Grade 9 reader: no calculus. Where -03 needs the minimum of U, use completing the square. Mark the rotation step in -04 as "beyond Grade 9, given".
- Keep your hint ladders and reasoning routes from S2; fix any that the S3 notes affect (-03 key source, -04 parts b and c only).
- Give the pair as one downloadable file, wep07-core1ab-<first 8 chars of its sha256>.json (or .md if the role files ask for markdown).

RETURN: end with this plain-text block, no question text:
TASK EVIDENCE · P1-WPE-G9v35 · S4
- inferential jump: <one sentence>
- files: <name>, sha256 <full>
- role rules followed: <file: yes/no, each>
- changes to S2 labels: <list or none>
- not done / unsure: <list>
SELF-CHECK: what could be wrong that this check would not catch: <list>
