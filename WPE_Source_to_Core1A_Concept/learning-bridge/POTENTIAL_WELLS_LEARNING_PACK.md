# WPE-E01 · Potential wells, turning points and reachable regions

**Stage:** new author-written Core1A/Core1B instructional candidate, not academic admission.  
**Proposed source themes:** WEP07-03 and EX-M109. The consolidated reader calls WEP07-03 APPLY/D2, while another source calls it SYNTHESIZE/D4; neither status is reconciled or approved here. The published source stems, answer keys and multi-select format are not reproduced.  
**Child's key decision:** a position is possible only if \(K=E-U(x)\geq0\). The *whole connected route* must be possible, and the lowest accessible potential gives the highest speed.

## Core1A — guided learning: one bowl-shaped well

Imagine a bead of mass **2 kg** sliding without friction along a smooth track whose potential energy is
\[
U(x)=1\ \mathrm{J}\left(\frac{x-2\ \mathrm{m}}{1\ \mathrm{m}}\right)^2.
\]
Its total energy is **4 J**. The expression is simply a bowl: lowest at \(x=2\text{ m}\).

1. **Make a small table before thinking about speed.** At \(x=0,1,2,3,4\text{ m}\), \(U=4,1,0,1,4\text{ J}\).
2. **Spend the energy budget.** \(K=E-U\): respectively \(K=0,3,4,3,0\text{ J}\). A negative value of \(K\) is impossible.
3. **Mark turning positions.** At \(x=0\) and \(x=4\text{ m}\), \(K=0\) and the bead may momentarily stop and reverse. Positions outside the interval require \(U>4\text{ J}\) and are inaccessible.
4. **Find maximum speed.** Speed is greatest where \(U\) is smallest, \(x=2\text{ m}\): \(v_{\max}=\sqrt{2K/m}=\sqrt{2(4)/2}=2\text{ m/s}\).
5. **Check a new energy value.** If total energy were only 1 J, solve \(U(x)\leq1\text{ J}\): the reachable interval shrinks to \(1\leq x\leq3\text{ m}\). **Energy level**, not the sketch's appearance, determines the boundaries.

**Child's rule:** find the shape → draw the horizontal total-energy line → shade only where the potential sits on or below the line → check whether those shaded parts connect. A stationary bead exactly at the bowl bottom is an equilibrium, not a bead racing at maximum speed.

## Core1B — fresh reconstruction: two valleys separated by a hill

A different 2 kg bead moves along the x-axis without friction. To keep the units clear, define \(q=x/(1\text{ m})\), a position number without units. Its potential energy is
\[
U(q)=(q^2-4)^2\ \mathrm{J}.
\]
The bead has **total energy 9 J**, starts at \(x=+2\text{ m}\) moving to the left, and can only move along the x-axis. Can it travel into the valley around \(-2\text{ m}\)? Find the allowed intervals of x, turning positions and highest possible speed. Explain why a low-energy destination might be separated from the bead by an inaccessible barrier.

### 01 Predict — before calculating
At \(q=-2,0,+2\), potential energies are \(0,16,0\text{ J}\). Two valleys look equally low. Is that enough to travel between them with only 9 J? Sketch a low valley–hill–valley picture.

### 02 Attempt — independent first model
Write \(K=9-(q^2-4)^2\), impose **\(K\geq0\)**, and solve for allowable positions. Mark the starting valley and route to the other one. Identify where speed is maximal. Record the original intervals, predicted path and reason before showing hints.

### 03 Reconstruct — compare the reasoning
Check the **connected interval** containing the start, not only whether the far valley itself has \(U\leq9\). Compare the energy line and turning points with the author-only reconstruction.

### 04 Diagnose
Watch for: concluding both valleys are reachable because their endpoints each have \(U=0\); treating \(K=0\) as forbidden rather than a turning point; treating \(U<0\) as the only way to be accessible; or maximizing speed where U is largest.

### 05 Repair
Re-draw the energy line at 9 J, shade the permitted intervals, circle the hilltop barrier, then revise the route decision and the maximum-speed calculation. Keep the original attempt and repair separately.

### 06 Boundary test
Raise total energy to **17 J**, with the same potential and mass. Is crossing the central hill now energetically possible? Calculate the **speed at \(x=0\)** and explain what changed.

## Author-only reference, not for learner-facing pre-attempt delivery

- \(K\geq0\iff(q^2-4)^2\leq9\iff|q^2-4|\leq3\iff1\leq q^2\leq7\).
- Permitted x intervals: \([-\sqrt7,-1]\text{ m}\) and \([1,\sqrt7]\text{ m}\). The start is in the **right** interval. At \(x=1\text{ m}\), the bead turns; it **cannot reach** the left valley across \(x=0\), where \(U=16\text{ J}>9\text{ J}\). The bead has enough energy for *either valley separately* but not for a connected route between them.
- The maximum accessible kinetic energy is 9 J at \(q=+2\) or \(q=-2\) (depending on which valley). For mass 2 kg, \(v_{\max}=\sqrt{2(9)/2}=3\text{ m/s}\).
- With **17 J**, \(U(0)=16\text{ J}\) and \(K(0)=1\text{ J}\), so \(v(0)=\sqrt{2(1)/2}=1\text{ m/s}\): the barrier can be crossed along the smooth one-dimensional trajectory.
- **Rubric:** dimensionally clear position variable, \(E-U\) test, two distinct allowed intervals, correct starting-component decision, two turning points for the right well, 3 m/s maximum speed, and 17 J boundary explanation. A correct speed without the connectivity inference is an incomplete reconstruction.

**Scientific conditions:** one-dimensional conservative motion with smooth potential and fixed E; no dissipation. The special borderline case **E = 16 J** at the central *unstable equilibrium* needs extra care: at exactly the hilltop energy, a trajectory may only approach it asymptotically, so we deliberately use **17 J** for the crossing boundary. Analytic inequalities and double wells are advanced extensions and must be scaffolded with a table and shaded regions.

**Separation check:** guided = one quadratic bowl with a single connected accessible region; fresh task = two-well quartic with disconnected regions and a changed-energy crossing test. Source WEP07-03's singular/rational potential and EX-M109's exact quartic coefficients are not reused.