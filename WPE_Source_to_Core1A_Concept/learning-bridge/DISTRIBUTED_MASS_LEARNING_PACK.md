# WPE-C04 · A hanging chain: which mass actually rises?

**Stage:** original author-written instructional candidate; not admitted native Core1A/Core1B.  
**Proposed source themes:** EX-M73, WEP07-02, TB-WPE-ILL-11. The source-task operation/demand claims are unresolved; the reader disagrees with the pilot placement of EX-M73.  
**Child's key decision:** when only **part** of a uniform chain hangs over a table, it is that hanging part whose mass and centre of mass must be represented. The hanging mass **changes** as it is pulled in.

## Core1A — guided learning, not the reserved challenge

**A soft chain on a table.** A uniform 4 m chain has mass 2 kg. Half of its length, 2 m, hangs vertically over a smooth table edge; the other half rests on the table. A helper pulls it **very slowly** until the whole chain lies on the tabletop. The table is smooth, and \(g=10\text{ m/s}^2\). How much work must the helper do against gravity?

1. **Draw only the hanging piece.** The whole chain weighs 2 kg, but only **2 of its 4 metres** are below the table. Its mass per metre is \(\lambda=M/L=2/4=0.5\text{ kg/m}\).
2. **Find the mass being lifted.** Hanging length \(x=2\text{ m}\) has mass \(\lambda x=1\text{ kg}\), not 2 kg.
3. **Find its middle.** The hanging piece is uniform, so its centre of mass is halfway down: **1 m below the tabletop**.
4. **Compare gravitational energies.** Take the table as potential energy zero. Initially the hanging part contributes \(U_i=-(1)(10)(1)=-10\text{ J}\); the chain lying on the table contributes zero. At the end, everything is on the table, \(U_f=0\). The helper must provide \(W_{\mathrm{helper}}=U_f-U_i=+10\text{ J}\), since it is pulled slowly without friction or change in kinetic energy.
5. **Check the boundary.** If no chain hung down, there would be no lifting work. If **all** the 4 m chain hung down, the whole 2 kg mass would begin with its middle 2 m below the table, so lifting it all would require \(2\times10\times2=40\text{ J}\).

**Helpful picture to draw:** a horizontal line for the table; mark the 2 m hanging portion as a vertical strip; put a dot **halfway down that strip**. The dot moves upward as the hanging strip becomes shorter.

**Optional general pattern:** for uniform chain mass per length \(\lambda\), hanging length \(x\), and zero height at the tabletop,
\[
U(x)=-(\lambda x)g\left(\frac{x}{2}\right)=-\frac12\lambda g x^2.
\]
This is **not** a magic chain formula to memorize. The two factors of \(x\) arise because *both the hanging mass and its centre-of-mass depth change*. You can reconstruct the result with a drawing and arithmetic.

## Core1B — unseen challenge (a different stopping point)

**Pull a rescue rope only part of the way up.** An 8 m uniform rope has mass 4 kg. Initially **4 m hang below** a smooth platform edge. A child slowly pulls it upward until **2 m remain hanging**. Neglect friction, any change in kinetic energy and any stretch. Use \(g=10\text{ m/s}^2\). How much positive work must the child do?

### 01 Predict — before calculating
Will the child do as much work as pulling the whole rope completely onto the platform? Which parts of the rope actually change height?

### 02 Attempt — construct the changing-mass model
Draw **two** hanging-length pictures (4 m before, 2 m after). For **each** picture, identify the hanging mass and the depth of its centre of mass. Compute its potential energy relative to the tabletop, then subtract final minus initial. Explain why using the mass of the entire 4 kg rope for both drawings is wrong. Save the first drawings and explanation before any hints.

### 03 Reconstruct — after commitment
Compare the child's *two hanging states* to the author model. Ask: How did the changing hanging mass affect the calculation? Why is the result positive even though the initial and final potential energies are both negative?

### 04 Diagnose
Likely errors: (a) raising all 4 kg through 2 m, (b) holding the hanging mass constant even after pulling, (c) treating the hanging piece's centre of mass as being at its **bottom**, or (d) subtracting energies in the wrong order.

### 05 Repair
Have the student redraw the state where the first mass/centre mistake appears, correct only that state's energy, and then recompute \(\Delta U\). Preserve the original attempt separately.

### 06 Boundary test
From the **same initial 4 m hanging position**, what work would be needed to pull the rope **completely** onto the platform (0 m hanging)? Why must it exceed the answer for stopping with 2 m still hanging?

## Author-only reference, not for learner-facing pre-attempt delivery

- Rope mass per metre: \(\lambda=4/8=0.5\text{ kg/m}\).
- At 4 m hanging: mass \(=2\text{ kg}\), centre of mass \(=2\text{ m}\) below tabletop; \(U_i=-(2)(10)(2)=-40\text{ J}\).
- At 2 m hanging: mass \(=1\text{ kg}\), centre \(=1\text{ m}\) below tabletop; \(U_f=-(1)(10)(1)=-10\text{ J}\).
- Helper's positive work: \(W_{\mathrm{helper}}=U_f-U_i=-10-(-40)=+30\text{ J}\).
- Equivalent check from \(U(x)=-\lambda g x^2/2\): \(U(4)=-40\), \(U(2)=-10\), same \(+30\text{ J}\). The 2 m of rope still hanging must **not** be treated as though all its mass had already reached the platform.
- Boundary: if final hanging length is 0 m, \(U_f=0\), so total work from the original starting state is \(40\text{ J}\), larger than 30 J.
- **Rubric:** represents both states, correct mass per length, correct changing hanging masses, correct half-length centre positions, correct signed \(\Delta U\), and sensible boundary comparison. An isolated answer of “30 J” is not a demonstrated construction.

**Scientific conditions:** uniform flexible rope, no stretch, smooth edge and platform, vertical hanging section, quasistatic pulling so \(\Delta K\approx0\), no dissipation. The helper's work equals the gravitational potential-energy increase only under these conditions.

**Separation check:** guided = 4 m/2 kg chain, halfway hanging, pulled **fully** onto tabletop; independent = 8 m/4 kg rope, pulled from 4 m hanging to **2 m still hanging**, requiring two nonzero energy states. No original examination wording or figures are copied.