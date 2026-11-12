# WPE-E05 · Inward force, stored energy and the speed needed for a circle

**Stage:** newly authored Core1A guide and Core1B reconstruction candidate; **not** an academic or Core2 admission.  
**Proposed source theme:** EX-M89. The consolidated reader labels it SYNTHESIZE/D3 and NOT_ADMITTED, with a coaching-predicted answer. This pack does not reuse its \(F\propto r^2\) force law, numerical coefficients or option choices. The source's correct exam/key correspondence and D-band remain unapproved.  
**Child's key decision:** separate **two operations**. The area under an **inward force magnitude versus radius** graph determines the *change in potential energy* between radii. The **force at the chosen radius** provides the centripetal force needed for that circular orbit. Add potential and kinetic energy only after doing both.

## Core1A — guided learning: a constant-magnitude inward force

Imagine a **1 kg** toy bead moving in a horizontal circular orbit around a central anchor. The anchor supplies an inward force of constant **3 N magnitude** wherever the bead is a positive distance \(r\) from it. Choose the reference \(U(0)=0\), and consider a circle of radius **2 m**. Assume the central force is conservative, and ignore other horizontal forces.

1. **Draw the arrows.** The bead's **velocity** is along the circle, tangent to the path. The **force** points toward the centre, perpendicular to that velocity. The inward radial component is \(F_r=-3\text{ N}\) when **positive r means outward**.
2. **Find potential energy by moving *radially* in your imagination.** From \(F_r=-dU/dr\), an inward 3 N force means \(dU/dr=+3\text{ N}\). Increasing distance from 0 to 2 m increases potential energy by the rectangular area under force-magnitude-versus-radius: \(U(2)-U(0)=(3\text{ N})(2\text{ m})=+6\text{ J}\). Thus \(U(2)=6\text{ J}\). A force pointing *inward* does **not** imply the potential energy itself must be negative.
3. **Find circular speed from inward force.** The inward-force requirement is \(mv^2/r=3\text{ N}\). With \(m=1\text{ kg}\) and \(r=2\text{ m}\), \(v^2=6\text{ m}^2/\text{s}^2\); \(v=\sqrt6\approx2.45\text{ m/s}\).
4. **Now combine energies.** Circular kinetic energy is \(K=\tfrac12mv^2=\tfrac12(1)(6)=3\text{ J}\). Total mechanical energy \(E=K+U=3+6=\mathbf{9\text{ J}}\).
5. **Check the important boundary.** During steady circular motion the bead stays at one radius, so the radial force does **zero work along the circle** (force perpendicular to velocity). The 6 J potential energy came from comparing different *radial positions*, **not** from imagining the bead continuously gaining energy as it circles.

**Child's two-question routine:** “How much does potential energy rise as r increases?” (find **area** under inward-force magnitude versus radius), then “How much inward force is needed at this radius?” (use **\(mv^2/r\)**). The two answers feed into \(E=K+U\), but the operations are different.

**A gentle contrast:** A signed force–radius graph would plot \(F_r=-3\text{ N}\), whose signed area equals *radial force work* \(W_r=-\Delta U\). A graph of the **positive inward-force magnitude** \(f(r)=3\text{ N}\), which we use here, has positive area equal to **\(\Delta U\)**. Label the vertical axis before using any area.

## Core1B — unseen challenge: a force graph that changes its rule

A **2 kg** toy spacecraft is held in a steady circular orbit around a central force source. For positive radial distance \(r\), the *magnitude* of the **conservative inward force** is described by this **new, piecewise force–radius graph**:

- **From 0 to 2 m:** the inward force magnitude is **4 N**, a horizontal line.
- **From 2 to 4 m:** the inward force magnitude grows **linearly** from **4 N at 2 m** to **8 N at 4 m** (so at 3 m it is **6 N**).
- Reference potential energy \(U(0)=0\). The force always points inward, so \(F_r=-f(r)\) when positive r points outward. The spacecraft is on the **3 m** circular orbit and has no radial motion.

Find the potential energy \(U(3\text{ m})\), required orbital speed, kinetic energy and total mechanical energy. Explain why you must **add two graph areas** before determining U, but use the **force value at 3 m** to determine circular speed. Do not treat the force magnitude graph as though its area were work done *during the circular orbit*.

### 01 Predict — before calculating
Is the spacecraft continuously gaining energy from the inward force as it travels around its circle? If the force magnitude grows with radius, should \(U(r)\) rise or fall as radius increases from the reference point?

### 02 Attempt — model both operations independently
Draw a force-magnitude–radius graph with a horizontal 4 N section and an increasing straight-line section. Calculate the **rectangle from 0–2 m** and the **trapezoid from 2–3 m**, adding them to obtain \(U(3)\). Then sketch an inward force arrow and a **tangential velocity** arrow at the 3 m orbit; use \(mv^2/r=f(3)\) to determine the speed. Finally compute \(K\) and \(E=U+K\), giving units and justifying each step. Preserve the first reasoning attempt before hints or the author-only key.

### 03 Reconstruct — after commitment
Compare **the two separate area pieces**, the local inward-force value and the circular-force equation with the reference. Explain which part represents stored potential energy and why the orbit's radial force does no work while the radius stays fixed.

### 04 Diagnose
Look for: using only the area from 2–3 m and forgetting the 0–2 m reference history; mistaking the force graph's **local height** for potential energy; calculating a rectangular 2–3 m area instead of a trapezoid; assigning negative U merely because the force points inward; or setting \(mv/r\) instead of \(mv^2/r\).

### 05 Repair
Correct the first wrong graph segment or force arrow, then reconstruct \(U\), \(v\), \(K\) and \(E\). The corrected calculation and why it changed should be kept separate from the original attempt.

### 06 Boundary test
Consider a **different steady circular orbit at 4 m**, with the **same force law and spacecraft mass**. Recompute \(U(4)\), \(v(4)\), \(K(4)\) and total \(E(4)\). Is \(E(4)\) the same as at 3 m? Why should this **not** be described as the same spacecraft freely spiralling from one steady orbit to another while total energy stays fixed?

## Author-only reference, not for learner-facing pre-attempt delivery

- For positive r, \(F_r=-f(r)=-dU/dr\), so \(dU/dr=f(r)\). With \(U(0)=0\), \(U(r)=\text{area under the positive inward-force magnitude graph from 0 to }r\). This is **potential energy difference**, not work done around a circle.
- From 0 to 2 m: rectangle \(A_1=(4\text{ N})(2\text{ m})=8\text{ J}\). From 2 to 3 m: trapezoid \(A_2=\tfrac12(4+6)\text{ N}\,(1\text{ m})=5\text{ J}\). Therefore **\(U(3)=8+5=13\text{ J}\)**.
- Local inward force at 3 m is 6 N; \(mv^2/r=6\) implies \(v^2=6(3)/2=9\text{ m}^2/\text{s}^2\), so **\(v=3\text{ m/s}\)**.
- Kinetic energy \(K=\tfrac12(2)(3^2)=9\text{ J}\); **total mechanical energy \(E=U+K=13+9=22\text{ J}\)**.
- Boundary at 4 m: the new 2–4 m trapezoid has area \(\tfrac12(4+8)(2)=12\text{ J}\); with the first rectangle, **\(U(4)=20\text{ J}\)**. Local inward force is 8 N; \(v^2=8(4)/2=16\), so **\(v(4)=4\text{ m/s}\)**, **\(K(4)=16\text{ J}\)** and **\(E(4)=36\text{ J}\)**.
- Different circular radii are **distinct orbit states** with different total energies. A conservative central force does no work on a body moving at constant radius; it does not spontaneously transfer that body between circular radii. A separate process would be needed to change the orbit energy.
- **Rubric:** correctly distinguishes positive inward-force magnitude from signed radial force, includes both force–radius area pieces, obtains \(U(3)=13\text{ J}\), uses the *local* 6 N for \(mv^2/r\), finds \(v=3\text{ m/s}\), \(K=9\text{ J}\), \(E=22\text{ J}\), explicitly states no work during circular travel, and gives the separate 4 m orbit state. A final “22 J” without the two-model explanation is not independent reconstruction evidence.

**Scientific conditions:** radial conservative central force for \(r>0\), positive r outward, force magnitude nonnegative and directed inward, positive reference U(0)=0 defined as the continuous limit from \(r>0\); at the exact central point \(r=0\) a fixed inward direction is undefined, so the force law is used only at **positive** r. Orbit motion is ideal, at a steady fixed radius and under the specified central force; no drag or propulsion. The force graph joins continuously at r=2 m. “Area under graph” uses **radial distance**, not an orbit's travelled arc length. The boundary task refers to a *different* orbit, not a continuous lossless transition between orbits.

**Separation check:** guided = a constant inward-force magnitude of 3 N, 1 kg bead at 2 m, rectangular area; fresh task = a **piecewise force–radius graph**, 2 kg spacecraft at 3 m requiring rectangle + trapezoid, followed by a separately energized 4 m orbit. This does not reproduce EX-M89's quadratic radial force or the coaching-predicted multiple-choice response.