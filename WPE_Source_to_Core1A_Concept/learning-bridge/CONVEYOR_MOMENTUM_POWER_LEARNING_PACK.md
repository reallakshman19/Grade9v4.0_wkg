# WPE-C07 · A conveyor belt: momentum arrives every second

**Stage:** original author-written instructional candidate, not admitted native Core1A or Core1B.  
**Proposed source theme:** EX-M16 (its consolidated reader record is a MODEL/D3 *candidate*, not an independent admission). The original's speed-dependent feed-rate relationship is **not reproduced** in this guided problem or fresh challenge.  
**Child's key decision:** model the **stream of incoming material**, not a fixed lump. The belt must continuously change arriving material's horizontal momentum. The power needed to keep the belt moving is **not always the same** as the increase in the material's kinetic energy.

## Core1A — guided learning, not the reserved challenge

**Sand hopping onto a toy conveyor.** A conveyor belt moves to the right at a steady **2 m/s**. Each second, **1 kg** of sand drops onto it with **zero horizontal speed**. The belt grips the sand, speeds it up horizontally and carries it away at 2 m/s. Assume a steady flow, neglect other conveyor loads and focus on **horizontal** energy and forces.

1. **Draw the motion of a little batch.** In 1 s, 1 kg arrives with horizontal momentum **0**; it leaves with \((1)(+2)=+2\text{ kg·m/s}\). The sand needs a rightward push.
2. **Think per second, not total mass collected.** Momentum transferred to sand in one second is \(+2\text{ kg·m/s}\). Average horizontal force on incoming sand is \(F=\dot m(v-u)=(1\text{ kg/s})(2-0)\text{ m/s}=2\text{ N}\). This steady-flow model is about the *incoming kilograms each second*, not the entire load already on the belt.
3. **Find what the motor must do.** Sand pushes backward on the belt with 2 N, so the motor must add 2 N of forward force to maintain its speed. The belt moves 2 m each second: **motor power** needed for this pickup is \(P=Fv=2\times2=4\text{ W}\).
4. **Check where the energy goes.** Each second the newly arriving 1 kg gains \(K=\tfrac12(1)(2^2)-0=2\text{ J}\), i.e. the *rate* of horizontal kinetic-energy gain is **2 W**. Why did the motor supply **4 W**? During frictional pickup, the belt slips relative to initially slower sand. The remaining **2 W becomes heat** in the idealized inelastic pickup.
5. **Check the boundary.** If the incoming sand already moved horizontally at **2 m/s** to the right, the belt would have no horizontal momentum to add. This *pickup-only* force and power would be zero (other motor losses could still exist).

**Mini energy ledger (per second):**

| Motor supplies | Sand's horizontal kinetic energy increases | Heat during speed matching |
|---:|---:|---:|
| \(4\text{ J}\) | \(2\text{ J}\) | \(2\text{ J}\) |

**What the letters mean:** \(u\) = incoming *horizontal* velocity, \(v\) = belt and outgoing speed, \(\dot m\) = kilograms joining the belt **per second**. For incoming sand slower than the belt, with both velocities rightward and the belt maintained at constant speed,
\[
F=\dot m(v-u),\qquad P_{\mathrm{pickup}}=Fv=\dot m(v-u)v.
\]
Incoming material's kinetic-energy gain per second is \(\tfrac12\dot m(v^2-u^2)\); the difference \(\tfrac12\dot m(v-u)^2\) appears as heat in this idealized frictional speed-matching model. These are **different** energy quantities, not competing formulas for the same thing.

### A gentle variable-flow extension (not an exam-question replica)

A feeder might drop **more kilograms per second** when the belt speeds up. For example, in a *separate invented feeder* the rate is \(\dot m=0.5v\) kg/s when the numerical value of \(v\) is measured in m/s. Sand again arrives with zero horizontal speed. At \(v=2\), \(\dot m=1\text{ kg/s}\) and \(P=4\text{ W}\). At \(v=4\), \(\dot m=2\text{ kg/s}\) and \(P=(2)(4)(4)=32\text{ W}\). **Do not assume** the mass rate stays constant when the question gives a rate–speed rule. The rate formula and the velocity change must both be used. This linear-in-\(v\) feeder is an illustrative invention, not the source question's rate law.

## Core1B — fresh challenge (moving arrivals and a speed-dependent feed rate)

**Wood chips joining a moving school conveyor.** A belt carries chips to the right at **4 m/s**. A chute delivers chips at an **incoming horizontal speed of 1 m/s to the right**. The flow rate is set by the belt speed: in kg/s it equals **half the numerical speed in m/s**, so \(\dot m= v/2\) kg/s. The chips leave moving with the belt. Friction transfers horizontal momentum while each chip matches the belt speed; assume steady flow and ignore unrelated motor losses and vertical-energy changes.

Find (a) kilograms delivered per second, (b) average horizontal force needed to speed up the incoming chips, (c) extra motor power needed to keep the belt at 4 m/s, and (d) the rate of horizontal kinetic-energy gain of the chips. Explain **why (c) and (d) are not equal**.

### 01 Predict — before calculating
Does the motor need to supply power if chips already travel a little to the right? Should the incoming speed be treated as **zero**? Will all motor power become horizontal kinetic energy?

### 02 Attempt — choose and construct the momentum-flow model
Draw a small **before → after** arrow diagram showing rightward \(u=1\) and \(v=4\text{ m/s}\). Start from **mass per second** and **momentum gained per kilogram**. Calculate force, \(P=Fv\), and the separate kinetic-energy gain per second. Give each answer a unit and describe where any difference goes. Keep the initial reasoning before hints and solutions.

### 03 Reconstruct — after commitment
Compare the mass-flow model, **velocity difference \(v-u\)**, power and energy ledger with the reference. Ask: why would using the sand's final momentum *without subtracting its initial momentum* exaggerate the required force?

### 04 Diagnose
Look for: using total accumulated conveyor mass, forgetting incoming horizontal speed, interpreting \(\dot m=v/2\) as \(\dot m=1/2\) independent of speed, setting motor power equal to kinetic-energy increase, or forgetting that belt speed (not incoming speed) multiplies the reaction force in \(P=Fv\).

### 05 Repair
The child draws their own two-arrow control-volume picture, identifies the **first incorrect flow or velocity-change term**, corrects the calculation and explains how the energy ledger balances. Store the repair separately from the original attempt.

### 06 Boundary test
The **same feeder rule and incoming speed of 1 m/s** are kept, but belt speed is now **2 m/s**. Recalculate flow rate, pickup force, motor power, kinetic-energy-gain rate and heat rate. Should they all halve simply because belt speed halves? Explain.

## Author-only reference, not for learner-facing pre-attempt delivery

- At \(v=4\text{ m/s}\), \(\dot m=4/2=2\text{ kg/s}\). Incoming \(u=1\text{ m/s}\), outgoing \(v=4\text{ m/s}\); change in horizontal velocity \(=+3\text{ m/s}\).
- Force required on chips: \(F=\dot m(v-u)=2(4-1)=+6\text{ N}\); reaction on belt is \(-6\text{ N}\). To maintain belt speed, extra motor force is +6 N and **motor power** \(P=Fv=6(4)=24\text{ W}\).
- Chips' horizontal kinetic-energy-gain rate is \(\dot K=\tfrac12\dot m(v^2-u^2)=\tfrac12(2)(16-1)=15\text{ W}\). The other \(24-15=9\text{ W}\) becomes heat in the modeled speed-matching interaction; independently \(\tfrac12\dot m(v-u)^2=\tfrac12(2)(3^2)=9\text{ W}\).
- Boundary: if \(v=2\text{ m/s}\), the feeder supplies \(\dot m=1\text{ kg/s}\), \(\Delta v=+1\text{ m/s}\), \(F=+1\text{ N}\), \(P=2\text{ W}\), \(\dot K=\tfrac12(1)(4-1)=1.5\text{ W}\), and heat rate \(=0.5\text{ W}\). No single “everything halves” rule works because speed, feed rate and speed difference each change.
- **Rubric:** correctly identifies incoming *horizontal* momentum, uses rate per second, substitutes a speed-dependent \(\dot m\), computes force and reaction signs, distinguishes 24 W motor input from 15 W kinetic-energy-gain rate, balances 9 W heat, and re-models the boundary case. A numerically correct answer without the flow picture and energy explanation is incomplete.

**Scientific conditions:** ideal steady one-dimensional mass pickup; arriving chips and outgoing chips have explicitly given rightward horizontal speeds, horizontal acceleration arises from slipping friction, and the belt speed remains constant via a motor. We consider **pickup-related incremental motor power** and horizontal kinetic-energy changes only; lifting/drop, startup transients, bearing loss and electrical inefficiency are outside this model. If arriving material is faster than the belt, signs and energy-flow interpretation need re-analysis rather than blindly reusing the positive-slip heat discussion.

**Separation check:** guide = sand initially with zero horizontal speed, fixed 1 kg/s feed and a simple 2 m/s belt, then a separate invented linear feeder contrast; Core1B = *already-moving* incoming wood chips and a new belt-speed-dependent \(v/2\) rate with an explicit kinetic-energy/heat comparison and altered-speed boundary. The original exam task and its rate law are not reproduced.