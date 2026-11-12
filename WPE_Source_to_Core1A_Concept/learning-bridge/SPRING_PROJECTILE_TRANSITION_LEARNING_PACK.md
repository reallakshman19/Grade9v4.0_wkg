# WPE-E03 · Spring launch to flight: know when the model changes

**Stage:** original authored Core1A/Core1B proposal; no academic admission.  
**Proposed source theme:** EX-N34. Its consolidated reader refers to an original figure that has **not been independently qualified** for this task; this pack uses new scenarios and does not claim to reproduce the source diagram or its answer.  
**Child's key decision:** use an **energy budget while the spring touches the object**, then switch to **projectile motion after launch**. Gravity determines flight time; horizontal speed determines horizontal distance.

## Core1A — guided learning: two separate models before combining them

**Model A — a puck leaving a spring on a level surface.** A 1 kg toy puck touches, but is **not attached to**, a spring compressed by 0.20 m with stiffness 100 N/m. The spring and puck rest on a smooth horizontal track.

1. **Contact phase:** stored energy \(U_s=\tfrac12kx^2=\tfrac12(100)(0.20)^2=2\text{ J}\).
2. **At the natural length:** the spring cannot pull the puck once contact ends. With no energy loss, \(K=\tfrac12mv^2=2\text{ J}\), giving launch speed \(v=2\text{ m/s}\).
3. **After contact:** do **not** keep adding spring work; on a smooth level track the horizontal speed stays 2 m/s.

**Model B — a different ball already launched horizontally.** Independently, a ball leaves a platform **1.25 m high** at **3 m/s horizontally**, with no spring involved. Take \(g=10\text{ m/s}^2\).

4. **Downward flight:** initial vertical speed is zero. \(h=\tfrac12gt^2\), so \(1.25=5t^2\) and \(t=0.50\text{ s}\).
5. **Horizontal flight:** ignore air resistance, so \(v_x=3\text{ m/s}\) throughout. Range \(d=v_xt=3(0.50)=1.50\text{ m}\).

**Two-model reminder:** spring energy finds horizontal speed *while contact exists*; height and gravity find **flight time after leaving the edge**. The ball does not continue feeling spring force in midair. A graph with time horizontally and vertical displacement downward is curved; horizontal position vs time is straight.

## Core1B — fresh reconstruction: contact friction then a flight

A 0.50 kg foam dart rests on a **horizontal** spring launcher at the edge of a platform. Its spring constant is **125 N/m** and it is compressed **0.20 m**. The dart is **not attached** to the spring. While contact lasts over the 0.20 m release, a constant friction force of **2.5 N** acts against motion. After the spring reaches its natural length, the dart immediately leaves the platform **horizontally** from a height of **1.25 m**. Ignore air resistance and any further contact forces in flight; use \(g=10\text{ m/s}^2\).

Find the spring's starting energy, energy lost to friction **during contact**, horizontal launch speed, time of flight and horizontal landing distance. Explain why **the spring force and contact friction cannot appear in the in-flight horizontal equation**.

### 01 Predict — before calculating
Will all the stored spring energy become motion? Does gravity stop the dart moving horizontally? Identify where the **spring phase ends** and the **flight phase begins**.

### 02 Attempt — independently model both regions
Draw a boundary at the spring's natural length. Build a contact ledger: **stored spring energy → friction work → launch kinetic energy**. Then use separate vertical and horizontal flight equations. Save the first diagram, equations and landing estimate before hints.

### 03 Reconstruct — after committing the first response
Compare your energy ledger and projectile equations against the author reference. Explain why using the original compression force as a **constant** force throughout 0.20 m would overestimate spring work.

### 04 Diagnose
Check for: applying \(\tfrac12kx^2\) without subtracting friction; carrying spring force or friction into flight; using flight time \(t=h/g\); confusing vertical acceleration with horizontal acceleration; or treating the spring as attached.

### 05 Repair
Correct the **first wrong phase boundary or ledger entry**, then recompute the launch speed and range. Preserve the original attempt and revised model separately.

### 06 Boundary test
Keep the same setup but make the spring-contact region **frictionless**. Recalculate launch speed and landing distance. Which of the two flight quantities—horizontal speed or time to fall—changes?

## Author-only reference, not for learner-facing pre-attempt delivery

- Spring energy \(U_s=\tfrac12(125)(0.20)^2=2.50\text{ J}\).
- Friction work during contact \(W_f=-(2.5)(0.20)=-0.50\text{ J}\), so launch kinetic energy \(K=2.00\text{ J}\).
- Launch speed \(v_x=\sqrt{2K/m}=\sqrt{4/0.5}=\sqrt8\approx2.828\text{ m/s}\).
- Fall time from 1.25 m, with zero initial vertical speed: \(t=\sqrt{2h/g}=\sqrt{0.25}=0.50\text{ s}\).
- Landing distance \(d=v_xt=\sqrt8(0.5)=\sqrt2\approx1.414\text{ m}\).
- **Boundary without friction:** \(K=2.50\text{ J}\), launch speed \(v_x=\sqrt{2(2.5)/0.5}=\sqrt{10}\approx3.162\text{ m/s}\); fall time is **still 0.50 s**; range becomes \(\sqrt{10}/2\approx1.581\text{ m}\).
- **Rubric:** explicit contact/flight boundary, correct \(\tfrac12kx^2\) and friction loss only in contact, correct launch energy and speed, correct vertical flight time, independent horizontal range, and correct changed-friction prediction. A bare landing distance without both phases is incomplete reconstruction.

**Scientific conditions:** ideal Hookean horizontal spring, dart and spring not attached; friction acts *only* during the 0.20 m contact movement; spring natural length coincides with the platform edge; dart leaves horizontally; negligible air drag, no vertical launch component, fixed gravitational acceleration, no other energy losses. In a real launcher, barrel details may change the contact/exit geometry; here every region is deliberately specified.

**Separation check:** guide teaches a smooth spring–puck release and a *separate* horizontal launch with no spring. Fresh task requires the child to **join those two representations**, include friction only within spring contact and explain the change of model. It does not reuse the source figure or published stem.