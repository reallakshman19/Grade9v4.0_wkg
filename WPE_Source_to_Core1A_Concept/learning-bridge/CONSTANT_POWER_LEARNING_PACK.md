# WPE-C03 · Constant power changes speed — not constant acceleration

**Stage:** original, author-written instructional candidate. Not accepted native Core1A or Core1B.  
**Proposed source themes:** EX-M62, EX-M79, EX-M69. These are theme links, not approved QRT task-level joins; the EX-M62 operation/band claims conflict in the inherited records.  
**Child's key decision:** **constant power** means equal energy delivered each second; it does **not** mean equal force or equal gain in speed each second.

## Core1A — guided learning, not the reserved challenge

**A motor helps a toy sled already in motion.** A 2 kg toy sled moves at 2 m/s on a level, frictionless track. A motor delivers a steady *mechanical power* of 12 W for 4 seconds. Ignore other horizontal work. How does its speed change?

1. **Read the unit.** \(12\text{ W}=12\text{ J/s}\), so the motor adds 12 J of kinetic energy **each second**. Do not confuse watts with newtons.
2. **Start with the sled's energy.** \(K_0=\tfrac12mv_0^2=\tfrac12(2)(2^2)=4\text{ J}\).
3. **Build an energy ledger:** \(K(t)=K_0+Pt=4+12t\) joules. At \(t=1\text{ s}\), \(K=16\text{ J}\). At \(t=4\text{ s}\), \(K=52\text{ J}\).
4. **Convert energy into speed.** For this 2 kg sled, \(K=v^2\) numerically in joules, so \(v(1)=4\text{ m/s}\) and \(v(4)=\sqrt{52}\approx7.21\text{ m/s}\). The speed did **not** grow by the same number of m/s each second.
5. **Pick the graphs.** The *kinetic energy–time* plot is straight because the increase is 12 J/s. The *speed–time* plot rises but gradually flattens (its slope gets smaller), since \(v(t)=\sqrt{4+12t}\). The *displacement–time* plot becomes steeper as the sled speeds up; its slope is speed. Distance is the area under a speed–time curve, **not** the area under an energy–time curve.

**A child-friendly graph check:** The motor adds 36 J between \(t=1\text{ s}\) and \(t=4\text{ s}\). That is constant energy gain per second, even though the speed rises from 4 to about 7.21 m/s rather than increasing by 12 m/s.

**Why force is not constant:** Where the sled is moving forward at speed \(v>0\), \(P=Fv\) for a forward driving force, so \(F=P/v\). As speed increases, the force for the same power becomes smaller.

### Optional mathematics extension — only if the child's syllabus supports it

For an **idealized** cart starting from rest with constant *net* power \(P\) and no losses, \(K=Pt\) gives
\[
\frac12 mv^2=Pt,\qquad v(t)=\sqrt{\frac{2P}{m}}\,t^{1/2}.
\]
Distance is accumulated speed, \(s(t)=\int_0^t v(\tau)\,d\tau\), so
\[
s(t)=\frac23\sqrt{\frac{2P}{m}}\,t^{3/2}.
\]
**Do not memorize \(t^{3/2}\) as a universal rule:** it only follows from these exact assumptions. A real finite-force motor cannot supply exactly constant nonzero power at **zero** speed; the idealization has \(F=P/v\to\infty\) as \(v\to0^+\). For Grade 9 learners who have not studied integration, use the energy table, the speed–time curve and area-under-the-curve idea; keep this derivation teacher/advanced-only.

## Core1B — unseen challenge (different mass, start speed and power)

**A powered classroom trolley.** A 3 kg trolley already rolls right at 2 m/s when a motor starts delivering a steady **18 W of mechanical power**. It travels on a smooth level track with negligible resistive work. What are its speeds after **2 seconds** and **6 seconds**? Sketch the *shape* of its kinetic energy–time, speed–time and displacement–time graphs. Explain whether the acceleration stays constant.

### 01 Predict — before calculating
Will the trolley gain an equal **speed** each second, or equal **kinetic energy** each second? Which of the three plots should be straight? Make a guess before choosing formulas.

### 02 Attempt — independently construct the model
Write \(K_0\); form a **time → supplied energy → total kinetic energy → speed** table for 2 s and 6 s; sketch all three graph shapes and explain the choice of axes. Do not begin from \(s=\tfrac12at^2\) without first checking that acceleration is constant. Record the child's first table and explanation before hints or answers.

### 03 Reconstruct — after committing the response
Ask the learner to compare the initial energy, the energy added each second and the shape of \(v(t)\) with the author reference. Why is the motor force smaller once speed is higher?

### 04 Diagnose
Look for: **watts mistaken for newtons**, \(v=v_0+at\) with an invented constant \(a\), taking \(18t\) as the **total** energy instead of the **added** energy, or treating area under the \(K\)–\(t\) graph as displacement.

### 05 Repair
Have the child correct the **first incorrect row or graph axis**, then recompute and describe what changed. Keep the revised reasoning distinct from the first attempt.

### 06 Boundary test
The same trolley and initial speed now receive **9 W** instead of 18 W. What is its speed after 2 seconds? Does the constant-acceleration conclusion suddenly become valid? Explain.

## Author-only reference, not for learner-facing pre-attempt delivery

- \(K_0=\tfrac12(3)(2^2)=6\text{ J}\).
- At \(t=2\text{ s}\), \(K=6+18(2)=42\text{ J}\); \(v=\sqrt{2(42)/3}=\sqrt{28}\approx5.29\text{ m/s}\).
- At \(t=6\text{ s}\), \(K=6+18(6)=114\text{ J}\); \(v=\sqrt{76}\approx8.72\text{ m/s}\). The speed increase over 4 s is **not** four times the increase over the first 2 s.
- \(K(t)=6+18t\) is a straight rising line, \(v(t)=\sqrt{4+12t}\) rises with decreasing slope, and displacement increases with an increasing slope because \(ds/dt=v\). A qualitative sketch suffices; computing exact displacement requires more advanced mathematics.
- Force \(F=18/v\) falls as speed rises (when velocity and force are aligned), hence acceleration \(a=F/3\) falls: **not constant acceleration**.
- Boundary: \(K(2)=6+9(2)=24\text{ J}\), \(v=\sqrt{2(24)/3}=\sqrt{16}=4\text{ m/s}\). Constant *power*, not constant acceleration, still describes the motor.
- **Rubric:** identifies fixed mechanical power, includes initial kinetic energy, constructs two correct time–energy–speed transitions, distinguishes three graph operations, rejects constant acceleration with a reason, and handles the changed-power check. Do not grade the child solely on numerical answers.

**Scientific conditions:** motor power here means power *actually transferred to translational kinetic energy* (not electrical input), mass constant, no friction or drag, already nonzero initial speed. The zero-speed idealization is separately labeled as an optional mathematical limit.

**Separation check:** guide = 2 kg sled at 12 W with worked times 1 s and 4 s; independent = 3 kg trolley at 18 W with times 2 s and 6 s plus three graph decisions and a changed-power test. Neither reproduces the source-question stems or options.