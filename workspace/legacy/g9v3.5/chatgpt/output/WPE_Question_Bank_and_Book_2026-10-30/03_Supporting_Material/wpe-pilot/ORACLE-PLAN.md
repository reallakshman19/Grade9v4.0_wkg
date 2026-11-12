# G9v3.5 WPE pilot: Oracle plan (OTM as Oracle)

Owner, 27 Oct 2026 22:30: "you are the oracle, see latest skill, plan your activity, including built in browser chatgpt agent via task evidence and github datachatgpt" (CL #1 6450379061).
Status: PLAN ONLY. The G9v3.5 HOLD is in force; nothing runs until the Owner says "lift hold".

## Who does what (skill v7.18 §2, §5, §13.1, §17.10)

| Role | Who | Never |
|---|---|---|
| Oracle | OTM: WBS, cards, challenge every return, integration challenge | write learner content; give the independent verdict; accept |
| Producer | ChatGPT chat in the built-in browser, new chat `P1-WPE-G9v35` | approve itself |
| Independent check | fresh Sonnet checker given only the bundle (no IR on G9v3.5 now) | see the producer's chat |
| Compile (W5 page) | OTM-BUILT beside B2 (`who: OTM · context held, B2 route`) | change B2 |
| Acceptance | Owner | — |

O5 and 6ae0484d are on standby. PR #310's 10 JEE candidates stay as a candidate input.

## Channels
- **In:** one zip in Drive Handoffs/g9v35 (lesson 12a; `G9-WPE-pilot-inputs.zip` is built, sha e604a616…). The chat opens it with the Google Drive plugin. Its first reply lists the files it could read.
- **GitHub data:** the chat reads `Shared/` (roles, vocabularies) through its GitHub connector, read only.
- **TASK EVIDENCE:** a ChatGPT chat cannot post to GitHub. Each reply ends with a plain-text TASK EVIDENCE + SELF-CHECK block. A Sonnet reader copies it word for word to the producer's evidence thread on CoordinatorLandingpage, as `[AGENT · P1-WPE-G9v35] (relayed by OTM)`. The onboarding test post is the first relay that reads back.
- **Out:** the Owner downloads the files; I find them by name and sha256.
- **Sends:** guarded sends only (SEND_INTENT, then SENT_TO_CHAT). Sonnet reads the chat about every 10 minutes.

## Steps (the slice first, then scale)

| # | Step | Who | Done when |
|---|---|---|---|
| S0 | Pick the slice: one key idea and 3–5 D3/D4 items from the REFERENCE bank (13 D3/D4 items), each with a band reason and a source | Oracle (OTM). A fresh checker fixes the targets and the falsifier. | The slice card is posted on #311 |
| S1 | Onboard the producer: new chat, Drive plugin, zip, evidence test post | OTM (guarded send) | The file list is returned and the relay reads back |
| S2 | W1 + W2: full originals (stem, options, figure, official key) and Smart Labelling 1 (demand, 5 factors, band, key step, prerequisites, hint ladder, route) | Producer | TASK EVIDENCE is relayed |
| S3 | Challenge: originals checked word for word against the source, bands re-derived | Oracle, then a fresh checker | PASS, or repair cards |
| S4 | W3 Core2 per item and W4 one Core1A/1B pair for the key idea | Producer | TASK EVIDENCE is relayed |
| S5 | W5 compile: one page, built the way B2 was built | OTM-BUILT | The page opens locally and its sha is recorded |
| S6 | Non-author spot-check (personal-use bar: CHECKED), then the Owner validates | Fresh checker, then the Owner | The Owner says ok |
| S7 | Scale to all 13 D3/D4 items: same chat or a new one, reusing the Library brief | Producer | Per S2–S6 |

## Dispositions
- **#311** (C1 return): the input to S0.
- **#313** (academic review): replaced for the slice by the S3 fresh check. Its reviewer stays UNKNOWN.
- **#312** (Math): parked, outside the WPE pilot.
- **PR #309 / #310:** stay drafts and are not merged. #310 is a candidate source pool.
- **O5's implementer brief:** not issued.

## Open for the Owner
1. "lift hold": starts S0 and S1.
2. Core1A/1B: one pair per key idea (my pick), or one pair per question.
