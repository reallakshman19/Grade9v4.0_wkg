# WPE Core1A → Core1B transfer readiness R3 — academic physics audit

**Scope:** F04–F08 only, latest main including merged PRs #57/#62. The five original selected-bank questions, options, stems, keys, source digests and the proposed QRT/Physics Blueprint classifications are NOT edited. PR #61 owns unified entry/return, optional #55 donor content and shared C/E/F navigation; this PR does not take over that work.

**Status:** AUTHOR-CHECKED / AUTOMATION-CHECKED as recorded by tests; **independent academic reviewer = HOLD**; **real learner mastery = NOT_RUN**. No software passing result is an academic approval. The teaching content is original explanatory work, not authentication of a coaching key.

## B1–B7: reusable academic rubric

| Gate | What must be demonstrated, not merely asserted |
| --- | --- |
| **B1 · Source-specific target** | The exact Question Bank concept and primary student decision are named, with no accidental source-key promotion |
| **B2 · Construction signature** | State system, signs, interacting parts, state changes, constraints, conserved quantities and valid equations |
| **B3 · Core1A sufficiency** | Guided anchor differs from source, diagram/control has a meaningful observable, misleading alternative is diagnosed, and model validity and limits are explicit |
| **B4 · Core1B fresh inference** | Task A and an unrelated-setting Task B require different model choice and physical assumptions before numerical substitution |
| **B5 · Attempt integrity** | Separate local first-attempt record for A and B, before worked solutions; progressive cues labeled as assistance; not secure grading |
| **B6 · Diagnosis and transfer** | Feedback distinguishes model, assumption, sign/representation and arithmetic errors; the learner repairs and reasons under a changed physical condition |
| **B7 · Provenance and caution** | Original source wording/coaching claim identified as a CLAIM, derivation independently checked, textbook principles cited, unresolved source ambiguities retained |

## Audit and strengthening decisions, journey by journey

### F04 · EX-M50 — two moving blocks connected by a spring

- **B1 target:** The spring responds to change in separation, not unchanging overall drift. Zero total momentum in the original equal/opposite 0.25 kg setup is a special case.
- **B2 construction:** Isolated 1D two-body system; signed velocities; reduced mass μ=m₁m₂/(m₁+m₂); V=(m₁u₁+m₂u₂)/(m₁+m₂); energy decomposition K=½MV²+½μ(u₁−u₂)². For initially relaxed, ideal spring, ½kx²=K_relative at its relative turning point. Extension or compression depends on ordering/sign.
- **B3 Core1A:** Existing guided 1/3 kg unequal-mass anchor, drift slider and full K decomposition retained. New observable test, explicit preload caveat and equal-speed / rigid-spring limits. **Source defect:** the inherited original check says only one 0.25 kg body moving yields x=v/(2√2), but the same source masses and k=2 N/m independently give **x=v/4**. Lesson warns; source key and record remain unchanged.
- **B4 Core1B:** A = 1/3 kg blocks with nonzero COM and maximum elongation (existing). **B = two approaching skaters, 2/4 kg, signed +3/−1 m/s, k=24 N/m, maximum compression, nonzero COM.** The task requires choosing relative versus total energy; it is not a renumbered spring-elongation question.
- **B5:** A keeps the original `F04` local practice key; B uses `F04-T2`. Stage-one first responses and hint exposure never copy between keys.
- **B6:** Wrong model (both stop), invalid external-work assumption, wrong velocity sign and wrong conversion to spring energy have distinct cues. B's changed case adds a **pre-compression of 0.20 m**; learner must include old spring potential without losing COM momentum.
- **B7:** Relative-motion decomposition follows [Physics LibreTexts/OpenStax-derived mechanics](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_%28OpenStax%29/Book%3A_University_Physics_I_-_Mechanics_Sound_Oscillations_and_Waves_%28OpenStax%29/01%3A_Units_and_Measurement/13%3A_Kinetic_Energy/13.02%3A_Convertible_and_Translational_Kinetic_Energy) and [OpenStax centre of mass](https://openstax.org/books/university-physics-volume-1/pages/9-6-center-of-mass). **HOLD:** independent reviewer should confirm sign convention, the original limiting-check discrepancy, and meaning of maximum extension.

### F05 · EX-M92 — finite-mass spring's distributed kinetic energy

- **B1 target:** Never infer K=mv²/6 merely from the free-end speed; derive it from a **linear instantaneous velocity profile**.
- **B2 construction:** Mass per present length m/L, fixed end v(0)=0, affine field v(y)=v_tip y/L. For a local mass dm=(m/L)dy, K=½∫v(y)²dm=mv_tip²/6. An N-slice midpoint sum converges to this value. If both ends have speeds u,v in an affine field, K=m(u²+uv+v²)/6.
- **B3 Core1A:** Preserves graphical midpoint strips and convergence 1→32, 1.2 kg/3 m/s anchor and "square first, then average" explanation. Adds explicit wall/profile/wave-model limits. The source only supplies a moving free end and uniform wire: a linear interior profile is an assumption, not a consequence of one endpoint observation.
- **B4:** A = 2.4 kg spring, 4 m/s and moving-left-end boundary (existing). **B = clamped 3 kg rescue/safety cord with camera-measured v(s)=6s, derive K and six-strip midpoint estimate.** Changed case **v(s)=6s² with same endpoint speed** forces re-integration, not one-sixth substitution.
- **B5:** Separate `F05` and `F05-T2` attempt/hint/repair records.
- **B6:** Wrong uniform-speed model, unobserved affine-field assumption, incorrect spatial fraction and average-before-square arithmetic each receive explicit correction. The original mass is not replaced physically by its effective m/3 kinetic mass.
- **B7:** The [spring effective-mass textbook problem](https://www.pearson.com/channels/physics/textbook-solutions/giancoli-5th-edition-9780137488179/ch-07-work-and-energy/we-usually-neglect-the-mass-of-a-spring-if-it-is-small-compared-to-the-mass-atta) explicitly conditions its m/3 kinetic-energy equivalent on v(x)∝x; this is a profile model, not an all-springs theorem. **HOLD:** independently check whether the original source intends affine deformation/quasi-static extension, and the change under wave motion.

### F06 · EX-M96 — wind-generator kinetic-energy flux

- **B1:** Explain WHY power scales as speed cubed under fixed density, area and efficiency, instead of memorizing an exponent.
- **B2:** Stationary collection area A, uniform incoming normal velocity v and density ρ; in Δt, swept volume AvΔt, mass ρAvΔt, kinetic energy per mass ½v². Hence power=η·(ρAv)(½v²)=½ηρAv³.
- **B3:** Existing wind-column illustration, 1-second volume flow and worked 10 m/s example retained. New note requires observer to inspect BOTH mass rate and joules/kg. C07 conveyor lesson shares the flow boundary idea but uses a different momentum-flux law; R3 does not edit C07.
- **B4:** A = fresh 1.25 kg/m³ rotor problem, speed/area boundary (existing). **B = water kinetic-current harvester**, ρ=1000, area 0.25 m², speed 2 m/s, 20% electrical fraction; no pressure/elevation head. Boundary changes BOTH velocity (3 m/s) and area (0.10 m²).
- **B5:** Independent `F06` and `F06-T2` first responses.
- **B6:** Direct targeted feedback for fixed-packet mistake, confusing momentum and energy rates, missing normal-area representation and forgetting the efficiency. Power units checked as kg/s × J/kg = W.
- **B7:** [U.S. DOE Small Wind Guidebook (kinetic power, rotor area, density, and v³)](https://www.energy.gov/cmei/systems/windexchange/small-wind-guidebook) and [OpenStax kinetic energy](https://openstax.org/books/university-physics-volume-1/pages/7-2-kinetic-energy); the v³ law only covers the specified constant-fraction kinetic flux, not a real turbine's full power curve. **HOLD:** applicability to actual devices with changing η, area, pressure and head.

### F07 · EX-M106 — horizontal force applied to a pendulum

- **B1:** Explicitly distinguish two distinct interpretations of ambiguous "force required to displace until 45°" wording.
- **B2:** For a fixed-length pendulum or frictionless circular path, Δx=Lsinθ, Δh=L(1−cosθ). With a **constant horizontal force** from rest to first turning point at rest, F_turnΔx=MgΔh and F_turn=Mg tan(θ/2). Holding at static equilibrium requires F_hold cosθ=Mg sinθ, hence F_hold=Mg tanθ.
- **B3:** Existing 1 kg guided 45° comparison and angle slider retained. New checkpoint explicitly says turning speed zero does NOT imply tangential acceleration zero. At small θ, turning force≈Mgθ/2, static force≈Mgθ. At 45°: Mg(√2−1) versus Mg, both conditional.
- **B4:** A = 2 kg pendulum, 60° turning versus holding, new 30° boundary (existing). **B = 0.50 kg bead constrained to a 2 m smooth rigid circular wire**, 30° turning and holding. Boundary changes the force HISTORY to F(θ)=Mg tanθ quasi-static, requiring integration instead of F_endpoint·Δx.
- **B5:** Independent `F07` and `F07-T2` first responses.
- **B6:** Different feedback for confusing zero speed with equilibrium, using Lsinθ for vertical height, assuming normal reaction does work, or incorrectly using final holding force to compute the total work under a varying force.
- **B7:** Derived from work–kinetic-energy theorem and tangential force balance; not determined by source wording alone. **HOLD:** source-key authority and whether the exam explicitly requires constant-force first-turn interpretation.

### F08 · EX-N27 — engine/wagon shock absorber

- **B1:** Contrast (i) a POSTULATED whole-system energy-retention fraction with (ii) an actual coupled two-body relative-energy model.
- **B2:** Conditional coached budget: if 10% of TOTAL ½(40,000)(20²)=8×10⁶ J becomes spring energy at 1 m, then ½k(1²)=8×10⁵ J, giving k=1.6×10⁶ N/m. This does **not** follow uniquely from "90% of the wagon's energy lost" unless missing details are supplied. For an isolated actual pair, spring energy initially available is ½μ(u_A−u_B)², not the whole COM kinetic energy.
- **B3:** Retains two separately worked anchors (1000 kg 10% assumed budget; 1000/3000 kg ideal two-body), makes the visual retention slider's POSTULATE label explicit and gives the identical-speeds zero-relative-energy limit.
- **B4:** A = 600/900 kg cart coupling with no brakes, 25%-of-relative-energy damper boundary (existing). **B = 200/300 kg spacecraft docking with an ideal coupler**: choose reduced-mass relative energy and predict compression. Boundary introduces an **unspecified active thruster**; a new numerical compression becomes genuinely underdetermined, not guessable from the old value.
- **B5:** Separate `F08` and `F08-T2` committed first answers and optional hints.
- **B6:** Distinct feedback for unjustified 10% carry-over, missing thruster/damper information, wrong COM motion and total-versus-relative energy. Under-determination is an acceptable scientific answer to the boundary task.
- **B7:** [OpenStax mechanics—centre of mass](https://openstax.org/books/university-physics-volume-1/pages/9-6-center-of-mass) and [relative convertible energy](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_%28OpenStax%29/Book%3A_University_Physics_I_-_Mechanics_Sound_Oscillations_and_Waves_%28OpenStax%29/01%3A_Units_and_Measurement/13%3A_Kinetic_Energy/13.02%3A_Convertible_and_Translational_Kinetic_Energy). **HOLD:** missing individual masses/braking history prevent authentication of a unique original mechanism. The coaching key is not silently promoted.

## Testable teaching artifacts and academic boundary

- **Task A** remains R2's original fresh problem for each F04–F08; its own new assumption-choice check is inserted before arithmetic.
- **Task B** (R3) is a separate unfamiliar setting, not a copy of A with new numbers, retaining its own first prediction, model selection, assumption, numerical entries, three optional hints, frozen first response, visible diagnosis, written repair and model-changing boundary check.
- The **same pre-existing six-stage renderer** is reused on F04–F08 only, with A preserved under its old local-storage key and B under an `-T2` suffix. No common C/E/F engine, gateway, Question Bank, source custody, PR #55 donor or PR #61 integration file is edited.
- Numerically matching answers never automatically grade written explanations as correct; the learner must justify the physical model. Neither practice-history storage nor browser checks constitute secure examination records.
- **Independent academic acceptance: HOLD. Real learner observation: NOT_RUN. Source-key authority: NOT_REVIEWED.** The short observation protocol is in `docs/wpe-r3-real-learner-observation-protocol.md`.
