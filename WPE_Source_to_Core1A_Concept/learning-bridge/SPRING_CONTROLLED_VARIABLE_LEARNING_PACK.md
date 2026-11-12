# WPE-C08 · Which spring stores more? First ask what stays fixed

**Stage:** original author-written instructional candidate; not native Core1A/Core1B admission.  
**Proposed source theme:** EX-M101. Its selected pilot classification and consolidated reader classification disagree; do not treat this pack as an accepted version of the original two-statement exam item. The source stem and its answer choices are **not** copied here.  
**Child's key decision:** a stiffer spring stores more energy at a **fixed extension**, but less at a **fixed final applied force**. The child must identify the variable held constant before deciding.

## Core1A — guided learning, not the reserved challenge

**Two toy springs in a workshop.** Spring A is soft (\(k_A=100\text{ N/m}\)); spring B is stiffer (\(k_B=200\text{ N/m}\)). The springs are ideal, obey Hooke's law \(F=kx\), and are stretched slowly from their natural lengths so they finish at rest. Compare how much elastic energy each stores in **two different** experiments.

1. **Start with what the spring stores.** When its extension is \(x\), \(U_s=\tfrac12kx^2\). This is the **area under a force–extension graph** from zero to \(x\): force rises from 0 to \(kx\), so the triangle has area \(\tfrac12(kx)x\). Do not just multiply the final force by the entire extension.
2. **Experiment A — keep extension fixed.** Stretch each spring slowly by the **same \(x=0.10\text{ m}\)**. A stores \(\tfrac12(100)(0.10)^2=0.50\text{ J}\); B stores \(\tfrac12(200)(0.10)^2=1.00\text{ J}\). The **stiffer B stores more**, because \(x\) is held fixed.
3. **Experiment B — keep the final applied force fixed.** Slowly increase the applied force on each spring from zero until it reaches the **same final \(F=10\text{ N}\)**. Their extensions differ: \(x_A=F/k_A=0.10\text{ m}\) while \(x_B=F/k_B=0.05\text{ m}\). The energies are \(0.50\text{ J}\) in A and \(0.25\text{ J}\) in B. The **softer A stores more**, because it stretches farther under the same final force.
4. **Explain the reversal.** With \(x\) fixed, use \(U_s=\tfrac12kx^2\), which grows with \(k\). With **final \(F\) fixed**, substitute \(x=F/k\): \(U_s=\tfrac{F^2}{2k}\), which becomes smaller when \(k\) becomes larger.
5. **Say the question aloud before calculating:** “Are we making both springs move the *same distance*, or giving them the *same final force*?” The answer can reverse even though neither spring changes.

**Draw this picture:** two starting springs with no extension, then **two possible experiment labels**. Under “equal extension” put matching length marks; under “equal final force” put matching force arrows but *different* extension lengths.

**Important force-language condition:** “same force” here means the **same final, slowly applied force at equilibrium**, starting from zero. If someone suddenly applies a constant 10 N force to a moving spring, it may overshoot and oscillate; its stored energy is not calculated by assuming the same quasistatic process. A compressed spring follows the same energy equations when extension magnitude is replaced by compression magnitude.

## Core1B — unseen challenge (infer stiffness from observations)

**Mystery spring pads.** Two colored spring pads are ideal and behave linearly while being compressed slowly. A lab table shows the force needed to hold each at the **same compression of 4 cm**:

| Spring pad | Force measured at 4 cm compression |
|---|---:|
| Blue | 8 N |
| Gold | 16 N |

Now the class tries two **different tests** with each pad.

- **Test X:** Compress **both pads by exactly 5 cm**, then hold them at rest.
- **Test Y:** Starting uncompressed, slowly increase the pushing force on **each** pad until the final measured force reaches **12 N**, then hold them at rest.

Which pad stores more energy in Test X? Which stores more in Test Y? **Calculate both energies in each test, then explain why the ranking reverses.** You are *not* directly given the two stiffnesses; find them from the original measurements.

### 01 Predict — before calculating
Which is stiffer according to the 4 cm measurements? Would that pad store more energy in **both** tests, or does the answer depend on what is kept the same?

### 02 Attempt — independently reconstruct both models
Draw a small two-row comparison with “**fixed extension**” and “**fixed final force**” headers. Convert centimetres to metres, infer each spring constant from the first table, and compute two energies in Test X and two in Test Y. Explain *why you chose a different starting expression for the two tests*. Preserve the first table and explanation before any hint or answer.

### 03 Reconstruct — after commitment
Compare the child's stiffness inference and the two controlled-variable models with the author reference. Ask: in Test Y, why must the **softer** pad stretch farther when both reach the same final pushing force?

### 04 Diagnose
Look for: treating 4 cm as 4 m, using \(F\times x\) rather than the spring's triangular loading work, assuming the **stiffer** pad always stores more energy, keeping \(x=5\text{ cm}\) fixed during the **equal-force** test, or using \(U=\tfrac12 kx^2\) with a *final force* but no calculation of the resulting \(x=F/k\).

### 05 Repair
Have the child **circle what is fixed in each experiment**, find the first incorrect inference, recompute only that comparison, and write a sentence explaining the reversal. The repaired response must be recorded separately from the original.

### 06 Boundary test
Repeat **Test Y** but slowly increase the final applied force to **24 N**, twice its earlier value, while both spring constants remain the same. By what factor does stored energy increase for **each** pad? Which pad still stores more, and why?

## Author-only reference, not for learner-facing pre-attempt delivery

- From the measurements at \(x=4\text{ cm}=0.04\text{ m}\): \(k_{\mathrm{blue}}=8/0.04=200\text{ N/m}\), \(k_{\mathrm{gold}}=16/0.04=400\text{ N/m}\). Gold is twice as stiff.
- **Test X, equal extension \(x=0.05\text{ m}\):** \(U_{\mathrm{blue}}=\tfrac12(200)(0.05)^2=0.25\text{ J}\); \(U_{\mathrm{gold}}=\tfrac12(400)(0.05)^2=0.50\text{ J}\). The stiffer **Gold** stores more.
- **Test Y, same final applied force \(F=12\text{ N}\):** \(x_{\mathrm{blue}}=12/200=0.06\text{ m}\), \(x_{\mathrm{gold}}=12/400=0.03\text{ m}\). Therefore \(U_{\mathrm{blue}}=F^2/(2k)=144/(400)=0.36\text{ J}\), \(U_{\mathrm{gold}}=144/(800)=0.18\text{ J}\). The softer **Blue** stores more.
- **Boundary:** doubling final force to \(24\text{ N}\) quadruples energy at each fixed \(k\). Blue stores \(24^2/(2\times200)=1.44\text{ J}\), Gold stores \(24^2/(2\times400)=0.72\text{ J}\). Blue remains higher for *equal final force*.
- **Rubric:** reads that Test X controls extension while Test Y controls final force, finds 200/400 N/m from the data, handles cm→m, computes four correct energies, gives the controlled-variable explanation for reversed ordering, rejects the \(F\times x\) overcount, and successfully handles the doubled-force boundary. The final ranking alone is insufficient to show reconstruction.

**Scientific conditions:** small elastic Hookean deformations within range; no hysteresis, friction or losses; identical reference of zero stored energy when unstressed; controlled loading slow enough to be quasistatic and leave pads at rest. The measured force is **final equilibrium force**, not a constant applied force throughout deformation.

**Separation check:** guide = two **given** stiffnesses (100/200 N/m), direct worked equal-extension and equal-final-force calculations; independent = **measured force/compression data** from which the learner must infer stiffnesses (200/400 N/m) and then decide which variable is controlled in two new experiments. This different representation and two-layer decision avoid simply copying an exam question or the guide's numbers.