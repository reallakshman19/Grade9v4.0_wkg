# WPE-E04 · Repeated bounces: energy lost is not speed lost

**Stage:** original author-written teaching and reconstruction pack, not native academic admission.  
**Proposed source theme:** EX-M82, a candidate in the consolidated reader; its original task and coaching answer are not copied.  
**Child's key decision:** the fraction of **kinetic energy retained** after an impact becomes the same fraction of the *next rebound height*, because \(mgh\) converts to kinetic energy before impact. Speed scales with the **square root** of that fraction. Add both upward **and** downward distances after every rebound.

## Core1A — guided learning: equal loss each bounce

A 1 kg rubber ball is released from rest at height **2 m** above a level floor. Use \(g=10\text{ m/s}^2\). On **every** impact with the floor, the ball loses **75% of its kinetic energy** and retains **25%**. Assume vertical bounces with no air resistance.

1. **First drop:** the ball travels **2 m down** and reaches the floor with \(K=mgh=(1)(10)(2)=20\text{ J}\).
2. **First rebound:** after the impact it keeps \(25\%\) of 20 J = **5 J**, so it climbs to \(h_1=5/(mg)=0.5\text{ m}\).
3. **Second and third rebounds:** after another impact, it keeps \(25\%\) of the energy again, so \(h_2=0.25(0.5)=0.125\text{ m}\) and \(h_3=0.03125\text{ m}\). Height decreases by a factor of **0.25** each impact, **not** a factor of 0.5.
4. **Count distance carefully:** the first 2 m drop happens once. Every complete rebound adds an **upward height and the matching downward height**:
   \[
   D=2+2(0.5+0.125+0.03125+\cdots)\text{ m}.
   \]
5. **Optional infinite-sum extension:** the heights form a geometric series with ratio \(r=0.25\). Their sum is \(0.5/(1-0.25)=2/3\text{ m}\), so \(D=2+2(2/3)=10/3\text{ m}\approx3.333\text{ m}\).

**Child's rule:** keep the **energy** fraction for rebound height, but use its **square root** for rebound speed. If 25% of kinetic energy remains, the upward speed just after impact is 50% of the downward speed just before impact. This follows because \(K=\tfrac12mv^2\).

**Important limit:** this is an ideal model of many tiny rebounds. Real balls eventually stop for reasons not included here; infinite geometric sums may be teacher-supported enrichment if they are outside the student's syllabus.

## Core1B — fresh reconstruction: only the first impact is different

A small ball is released from rest **2 m above the floor**, with negligible air resistance and vertical rebounds.

- At the **first** floor impact it retains **75%** of the kinetic energy it had just before impact.
- At **every later** impact it retains only **50%** of its pre-impact kinetic energy.

Calculate its **first three rebound heights**, and find the **total vertical distance** in the ideal model after all rebounds have become arbitrarily small. Explain why using 75% as the fraction for **every** bounce is wrong. Also state the ratio of upward speed to just-before-impact downward speed for the **first** bounce.

### 01 Predict — before calculating
Will the ball rebound to the original 2 m height? Is the post-impact speed fraction the same as the post-impact **energy** fraction? Does the 75% rule apply to the second impact?

### 02 Attempt — choose the changing bounce rule
Draw the original drop once. Make a rebound table with columns **bounce number → energy fraction used → rebound height → up-and-down travel**. Explicitly switch from **0.75** to **0.50 after the first impact**. Work out the first three rebounds and the total series. Preserve the original table and explanation before any hints.

### 03 Reconstruct — after commitment
Compare the child's first impact and the **later repeat rule** separately. Ask: which rebound height is the first term in the continuing half-height sequence? Why must it be counted **twice** in total travel?

### 04 Diagnose
Look for: using 0.75 on all impacts, subtracting rather than multiplying fractional energy, taking 75% energy as 75% speed, forgetting the initial drop, counting only ascent and no descents, or using a geometric sum with the wrong first term.

### 05 Repair
Correct the first wrong **retention-factor** row, rebuild the height sequence and explain the two-direction distance count; save the amended table separately from the first response.

### 06 Boundary test
Suppose instead **every** impact retains 75% kinetic energy. Starting from the same 2 m drop, what would the ideal total vertical distance be? Explain why it is larger than your original answer.

## Author-only reference, not for learner-facing pre-attempt delivery

- First impact: starting energy \(mgh\); **first rebound height** \(h_1=(0.75)(2)=1.5\text{ m}\).
- Later impacts: \(h_2=(0.50)(1.5)=0.75\text{ m}\); \(h_3=(0.50)(0.75)=0.375\text{ m}\). The later heights continue to halve.
- Sum of *all* rebound heights \(=1.5+0.75+0.375+\cdots=1.5/(1-0.5)=3\text{ m}\).
- Total travel \(D=2+2(3)=\mathbf{8\text{ m}}\).
- First rebound **speed** ratio \(v_{\mathrm{after}}/|v_{\mathrm{before}}|=\sqrt{0.75}=\sqrt3/2\approx0.866\), not 0.75.
- **Boundary, all impacts retain 75% energy:** rebound heights start at 1.5 m and repeat with factor 0.75, so sum \(=1.5/(1-0.75)=6\text{ m}\) and \(D=2+2(6)=\mathbf{14\text{ m}}\).
- **Rubric:** models the first impact separately, switches to the correct subsequent retention fraction, gives three correct heights, includes initial drop and both legs of every bounce, gives 8 m total, distinguishes energy fraction from speed fraction, and handles the all-75% boundary. A correct distance without the phase-switch explanation is incomplete.

**Scientific conditions:** vertical floor collisions, loss fractions refer specifically to **kinetic energy immediately before/after each impact**, gravitational potential energy fully converts to/from kinetic energy during flights, no air drag, constant \(g\), no sideways motion; the ideal infinite-series calculation treats progressively smaller bounces without time-resolution limits.

**Separation check:** guide = one unchanged 25% retention fraction at **every** impact from a 2 m height; fresh task = a first-impact 75% retention followed by **a different 50% repeat rule**, requiring the learner to choose the appropriate first term and ratio before finding total travel. The original source wording and exact numerical scenario are not duplicated.