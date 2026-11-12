# Core-2 High-ROI Correction · Candidate / Independent-review required

Scope: Existing WPE Core-2 WBS 4.3, Grade9v4.0 Issue #1. Bounded Owner instruction (2 November 2026): repair EX-M6, TB-WPE-ILL-05, WEP07-03 and associated misleading hints, and fix exact-file manifest integrity. **No revamp, native Shared admission, publishing or learner-release approval.**

Parent main commit: `146e62364b10255949a76e34284f2922d13f60c2`.
Prior exact HTML blob: `ad3a3a4c9aacf710ab20fa5b04d5dd63b1a2eac2`.
Prior native review bank blob: `f6d7a873ee390747973842aab0c6765972aec7ce`.

## Changes and scientific justification

1. **EX-M6:** Paper reproduction [ALLEN, JEE Main Jan 23 2026 evening, page 3](https://www.allenoverseas.com/wp-content/themes/ALLENOverseas/lp-assets/2026/Physics/2301-Physics_Paper_With_Solution_Evening.pdf) places S 45 degrees from A on the lower semicircle; the coaching source lists answer A. The old reader instead used the full A-to-B arc and a purported constant horizontal velocity, not a valid circular-wire law. Parameterize angle phi from A=0 to B=pi, S=pi/4. From initial horizontal component v, speed at S is sqrt(2)v; energy gives speed_P(phi)^2=2v^2+2gR(sin phi-1/sqrt(2)). Accordingly tP=R integral_(pi/4)^pi [speed_P(phi)]^(-1) dphi, tQ=2R/v. Reachability requires v^2/(gR)>=1/sqrt(2). Direct numerical quadrature yields tP/tQ approx **1.00947** at v^2/(gR)=0.708 (reachable, contrary to A), versus **0.86445** at 1. The source-reported key is preserved as evidence but **not** taught as universally proved. Exact source/physical-intent reconciliation is still HOLD. Original author-created SVG remains unverified, no source redraw.
2. **TB-WPE-ILL-05:** Original stem omits initial speed. With arbitrary u, v_bottom=sqrt(u^2+2gl sin(theta)), and gravitational instantaneous power is mg sin(theta)*v_bottom. The source formula is the u=0 special case. Stem retained verbatim, missing condition made explicit.
3. **WEP07-03 / NSEP Q57:** [IAPT published 2025 solution](https://www.iapt.org.in/images/nse_2025/Answer_key/NSEP_-_2025_Solution_1_compressed.pdf) corroborates all four answer statements. The initial two pre-attempt hints previously disclosed E=0, a substitution and complete-square strategy. They now prompt reasoning without doing it for the student. Solution's erroneous final “isolate a,b” replaced by four-statement closure. **APPLY/D2 vs SYNTHESIZE/D4** QRT conflict still unreviewed, admission HOLD.

## Exact scope and closure

- Original stems, original options, figure source references, IDs, aliases, difficulty labels and question count **unchanged**.
- Only 3 question entries edited in the candidate native review bank and its matching embedded HTML; 71 other question entries preserved.
- The same three rows in audit_flags.csv updated; publication manifest rebuilt against exact new Git blobs; renderer/attempt/reveal JS, layout and assets untouched.
- Mechanical assertions live in `tests/test_wpe_core2_high_roi.py`; GitHub CI and actual browser test results must be separately observed. Independent scientific reviewer and Owner academic acceptance **NOT_RUN**.
- No academic approval inferred from software validation. Public page remains historical main until separate authorized review/merge.
