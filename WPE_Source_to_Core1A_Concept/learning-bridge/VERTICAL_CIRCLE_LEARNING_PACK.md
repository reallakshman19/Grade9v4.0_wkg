# WPE-C06 · Vertical circles: enough energy AND enough inward force

**Stage:** original, author-written instructional candidate; not accepted native Core1A or Core1B.  
**Proposed source themes:** EX-M39, EX-N31, EX-M18, EX-M6. These are candidate construction links, **not** independent QRT findings.  
**Child's key decision:** energy determines the *possible speed*, but the string or track must also be able to provide the **required inward (radial) force**. Passing the energy check alone may not keep the object on a circular path.

## Core1A — guided learning, not the reserved challenge

**A toy bob whirls on a string.** A 0.5 kg ball moves in a vertical circle at the end of a light **taut string** of length \(r=2\text{ m}\). At the very top, its speed is \(6\text{ m/s}\). Take \(g=10\text{ m/s}^2\), ignore air resistance and friction at the pivot. What is its tension at the top, and what speed would it have at the bottom if the string stays taut?

1. **Point toward the circle's centre.** At the **top**, the centre is **downward**. Gravity \(mg\) and string tension \(T\) both point inward (downward). Radial acceleration is \(a_r=v^2/r\), so \(T+mg=mv_{\mathrm{top}}^2/r\).
2. **Calculate top tension.** \(mg=(0.5)(10)=5\text{ N}\), and \(mv^2/r=(0.5)(36)/2=9\text{ N}\). Thus \(T_{\mathrm{top}}=9-5=+4\text{ N}\): the string can pull inward and stay taut.
3. **Use energy for the speed change.** The top is \(2r=4\text{ m}\) above the bottom. A 0.5 kg ball gains \(mg(2r)=0.5(10)(4)=20\text{ J}\) of potential energy when moving bottom → top. Hence moving top → bottom it gains 20 J of kinetic energy.
4. **Find the bottom speed.** \(v_{\mathrm{bottom}}^2=v_{\mathrm{top}}^2+4gr=36+80=116\), so \(v_{\mathrm{bottom}}=\sqrt{116}\approx10.77\text{ m/s}\).
5. **Check force directions at the bottom.** Inward is now **upward**. The string tension pulls up, gravity acts down, so \(T-mg=mv_{\mathrm{bottom}}^2/r\). Here \(T_{\mathrm{bottom}}=0.5(116/2)+5=34\text{ N}\).
6. **A crucial sign test:** a string can **pull** but cannot **push**. If a calculation gives \(T<0\), do not treat it as a physical negative-tension string: the assumed taut circular path has become invalid. For a bob at the top, maintaining taut contact requires \(mv_{\mathrm{top}}^2/r\ge mg\), or \(v_{\mathrm{top}}^2\ge gr\).

**Radial versus tangential acceleration:** \(v^2/r\) points toward the centre and changes the direction of motion. Gravity can also change the *speed* through its tangential component at other positions. At the exact top and bottom, gravity is radial and its tangential component is zero. Do not add radial and tangential accelerations as if they point in the same direction.

**Picture to draw:** circle, centre dot, top bob and bottom bob; at each position draw a bold arrow **toward the centre** before choosing the signs for weight and tension.

## Core1B — unseen challenge (energy seems sufficient, but contact fails)

**Will the toy loop stay taut?** A **1 kg** bob is attached to a light string of length **1 m**. At the bottom of its vertical circle it has speed **7 m/s**, moving tangentially toward the rising side of the circle. The pivot is fixed; the string is initially taut. Use \(g=10\text{ m/s}^2\) and neglect air resistance. 

Can this bob complete the **full circular path with the string remaining taut all the way to the top**? Check *both* energy and the inward-force condition, and explain precisely what a negative computed tension means.

### 01 Predict — before calculating
Would having enough mechanical energy to reach the top automatically guarantee a taut circle? At the top, which way is inward, and can the string push?

### 02 Attempt — independently choose two models
Draw a top and bottom picture. Use the bottom kinetic energy and rise of \(2r\) to calculate the **circular-path candidate** \(v_{\mathrm{top}}^2\). Then write the separate top radial equation \(T+mg=mv_{\mathrm{top}}^2/r\). Decide whether the tension is physically possible. Save the student's explanation before hints or answers.

### 03 Reconstruct — after commitment
Compare the **energy result** and the **tension result** to the author-only reference. The child must say *why the first check is not enough*, rather than just give “yes” or “no.”

### 04 Diagnose
Watch for: (a) declaring success just because \(v_{\mathrm{top}}^2>0\), (b) using \(T-mg\) at the top instead of \(T+mg\), (c) accepting \(T=-1\text{ N}\) as an ordinary pulling tension, or (d) applying \(v^2/r\) tangentially.

### 05 Repair
Ask the child to draw the **top inward arrow** and re-evaluate which forces can point inward. If tension becomes negative in the assumed circular model, replace the conclusion with **“the string goes slack before the top; this circular-path model no longer applies.”** Preserve the initial model separately.

### 06 Boundary test
Keep everything the same but change the **bottom speed to 8 m/s**. Recalculate \(v_{\mathrm{top}}^2\) and \(T_{\mathrm{top}}\). Could the string then remain taut at the top? Optionally derive the smallest idealized bottom speed that just reaches \(T_{\mathrm{top}}=0\).

## Author-only reference, not for learner-facing pre-attempt delivery

- From energy for the **hypothetical taut circle**, \(v_{\mathrm{top}}^2=v_{\mathrm{bottom}}^2-4gr=49-40=9\text{ m}^2/\text{s}^2\). So energy **alone** would allow the top location at \(v=3\text{ m/s}\).
- Inward at the **top** is downward. \(T+mg=mv_{\mathrm{top}}^2/r\), so \(T=(1)(9)/1-(1)(10)=-1\text{ N}\). A string **cannot push**: the attempted taut circular solution is physically impossible. The bob becomes slack **before** the top, after which it follows motion not constrained to the original circle.
- To keep a string taut through the top, \(T_{\mathrm{top}}\ge0\Rightarrow v_{\mathrm{top}}^2\ge gr=10\). Combining with the bottom-to-top energy rise gives \(v_{\mathrm{bottom}}^2\ge 5gr=50\), so the ideal minimum bottom speed is \(\sqrt{50}\approx7.07\text{ m/s}\). The given 7 m/s is slightly too small.
- **Boundary \(v_{\mathrm{bottom}}=8\text{ m/s}\):** \(v_{\mathrm{top}}^2=64-40=24\), \(T_{\mathrm{top}}=24-10=+14\text{ N}\). The string can remain taut at the top (and along the ideal lossless circular path).
- **Rubric:** distinguishes energy from radial-force test, chooses inward direction at top, computes \(v_{\mathrm{top}}^2=9\), identifies \(T=-1\text{ N}\) as an impossible *taut-string* outcome, states slack-path interpretation, and verifies the 8 m/s boundary. An answer of “not enough energy” is **not** an acceptable explanation: energy is enough to reach that height, but tension is not physically admissible.

**Scientific conditions:** light inextensible string, fixed pivot and constant \(r\) only **while taut**; no drag/dissipation; ideal nonrelativistic motion; at the bottom, the bob's velocity is horizontal and tangent to the circle, directed so it moves upward along the following arc. The energy calculation of a hypothetical top position must **not** be mistaken for a valid future trajectory once the string becomes slack. A rigid rail or rod can supply different constraint forces, so string-specific \(T\ge0\) is not universal.

**Separation check:** guided = *given top speed* for a 0.5 kg bob on 2 m string, calculate actual top tension and bottom speed; independent = *given bottom speed* for 1 kg bob on 1 m string and decide whether the taut constraint is physically possible. Neither the source question nor its original geometry is copied.