# WPE-E02 · Instantaneous power: force in the direction of motion

**Stage:** original author-written teaching and fresh-task draft, not native academic admission.  
**Proposed source themes:** TB-WPE-ILL-05 and TB-WPE-ILL-06. The consolidated reader explicitly flags **TB-WPE-ILL-05 as under-specified because the initial speed is missing**; this pack does not quietly assume it was released from rest or promote an official answer.  
**Child's key decision:** power at one instant is the **rate work is happening at that instant**, controlled by the part of the force along the current velocity, not simply total force magnitude or speed.

## Core1A — guided learning: a trolley being pulled

A 2 kg trolley is already moving horizontally **right at 3 m/s**. A student pulls with a horizontal **6 N rightward** force, and a resistive force of **2 N leftward** also acts at that moment.

1. **Think direction before multiplying.** The pull and motion point the same way: \(P_{\mathrm{pull}}=6\times3=+18\text{ W}\). Resistance and motion point in opposite directions: \(P_{\mathrm{resist}}=-2\times3=-6\text{ W}\).
2. **Add power contributions:** net horizontal force is \(+4\text{ N}\), so \(P_{\mathrm{net}}=(6-2)(3)=+12\text{ W}\). The trolley's *kinetic energy is increasing at 12 J per second at this moment*.
3. **Keep instant and interval apart.** \(12\text{ W}\) is an **instantaneous** rate, not a claim that exactly 12 J is added in every future second. The trolley may speed up, so the power could change as velocity changes.
4. **Check perpendicular forces.** The normal support and gravity are vertical while the motion is horizontal. Their instantaneous powers are zero: the forces are perpendicular to velocity.
5. **Read a changed situation.** If the trolley were momentarily moving **left** at 3 m/s under the *same applied forces*, the signs would reverse and \(P_{\mathrm{net}}=-12\text{ W}\); kinetic energy would momentarily decrease.

**Simple rule:** \(P=\mathbf F\cdot\mathbf v\). For a one-dimensional horizontal force, put in a **sign** for direction. One watt is one joule per second. For an incline, the **component of gravity along the instantaneous direction of motion** contributes \(mg\sin\theta\,v\) in magnitude; the sign changes between uphill and downhill travel.

**Source-custody reminder for teachers:** a problem asking for bottom power on an incline without stating initial speed cannot determine one numerical value from the height alone. This is a source ambiguity, not a missing learner assumption we may silently insert.

## Core1B — fresh reconstruction: two forces and diagonal motion

A small robot travels across a horizontal floor. At one instant its velocity has components **3 m/s right** and **4 m/s forward**. A motor exerts a **6 N rightward** force; resistance exerts **2 N leftward** and **1 N backward**. Ignore other horizontal forces and treat gravity/support as perpendicular to the floor.

Find the **instantaneous motor power**, the **instantaneous resistive power**, the **net power** and whether the robot's kinetic energy is increasing or decreasing at that instant. Explain why simply multiplying the **magnitudes** of the total force and speed gives the wrong net power.

### 01 Predict — before calculating
Does the backward component of resistance matter even though the motor pushes right? Could the robot be moving and still have **zero instantaneous net power**?

### 02 Attempt — independently choose aligned force components
Draw a right/forward arrow for the velocity. For each force, calculate the contributions from its rightward and forward components:
\[
P=F_xv_x+F_yv_y.
\]
Calculate three powers and the sign of \(dK/dt\). Write the **units** and retain the first model, not just the number.

### 03 Reconstruct — after commitment
Use the author model to compare each force component's signed contribution and the total. Explain why \(P_{\mathrm{net}}=\mathbf F_{\mathrm{net}}\cdot\mathbf v\) does not automatically equal \(|\mathbf F_{\mathrm{net}}|\,|\mathbf v|\).

### 04 Diagnose
Look for: ignoring backward resistance, treating every force as positive because speed is positive, adding the component **magnitudes** rather than signed products, or claiming current net power determines all later energy gain.

### 05 Repair
Correct the first mistaken force arrow or component product; show how this changes net power and the *instantaneous* kinetic-energy trend. Save the repaired reasoning separately.

### 06 Boundary test
At another instant the robot's velocity components are **1 m/s right** and **4 m/s forward**, with the **same forces**. Recompute net power. Is it moving? Can its acceleration still be nonzero if the instantaneous rate of kinetic-energy change is zero?

## Author-only reference, not for learner-facing pre-attempt delivery

- Motor \(\mathbf F_m=(6,0)\text{ N}\), resistance \(\mathbf F_r=(-2,-1)\text{ N}\), and velocity \(\mathbf v=(3,4)\text{ m/s}\). Net force \(\mathbf F=(4,-1)\text{ N}\).
- Motor instantaneous power \(P_m=6(3)+0(4)=+18\text{ W}\); resistance \(P_r=-2(3)-1(4)=-10\text{ W}\); **net** \(P=+8\text{ W}\). Kinetic energy is increasing at **8 J/s at that instant**.
- Robot speed is 5 m/s, while \(|\mathbf F_{\mathrm{net}}|=\sqrt{17}\text{ N}\); the product \(5\sqrt{17}\text{ W}\) is **not** 8 W because force and velocity do not point in the same direction.
- Changed instant \(\mathbf v=(1,4)\text{ m/s}\): \(P_{\mathrm{net}}=4(1)-1(4)=0\text{ W}\). The robot is still moving at \(\sqrt{17}\text{ m/s}\), and its force/acceleration is nonzero; the net force is instantaneously **perpendicular** to velocity, so kinetic energy is momentarily neither rising nor falling.
- **Rubric:** distinguishes force and velocity directions, computes three signed powers, explains instantaneous \(dK/dt\), does not confuse work over time with current power, and handles moving-but-zero-power boundary.

**Scientific conditions:** instantaneous force components in a horizontal plane, orthogonal right/forward axes, ordinary nonrelativistic motion, no vertical work at that instant. Two-dimensional component dot products are an **advanced scaffolding step**; offer arrow diagrams and component tables to learners who have not studied vector notation.

**Separation check:** guide = one-dimensional trolley, two opposing forces; fresh task = independently choose right/forward components for diagonal motion, then assess a perpendicular-net-force boundary. Neither repeats the original incline nor circular-motion source stems.