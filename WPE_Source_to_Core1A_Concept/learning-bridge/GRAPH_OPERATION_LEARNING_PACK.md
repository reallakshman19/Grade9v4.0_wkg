# WPE-C05 · Read the axes first: area or slope?

**Stage:** original author-written instructional candidate, not native Core1A/Core1B admission.  
**Proposed source themes:** EX-M56, EX-M61, EX-M69. The exact original graph assets for these selected pilot themes are **not verified** by this construction; the lesson uses new descriptions, never a substituted “original” figure.  
**Child's key decision:** the **units on the graph axes** tell you whether a region's area means work or a line's slope means force or velocity. An identical-looking line can describe different physics.

## Core1A — guided learning, not the reserved challenge

**Three small graphs from a science notebook.** Every graph is specified in words so the learner can draw it without an unavailable image. x- and y-axis labels are essential.

1. **Graph A — force against position.** Vertical axis: horizontal force \(F_x\) in newtons. Horizontal axis: position \(x\) in metres. The line is horizontal at \(+3\text{ N}\) from \(x=0\) to \(x=2\text{ m}\). **Area** between line and axis is a rectangle: \(W=(3\text{ N})(2\text{ m})=+6\text{ J}\). A force *below* the axis over forward displacement would give negative work.
2. **Graph B — potential energy against position.** Vertical: potential energy \(U\) in joules. Horizontal: \(x\) in metres. A straight line runs from \((0\text{ m},9\text{ J})\) to \((2\text{ m},3\text{ J})\). **Slope** \(=(3-9)/(2-0)=-3\text{ J/m}\). The conservative force is \(F_x=-dU/dx=+3\text{ N}\). The **area under this graph is not work**.
3. **Graph C — displacement against time.** Vertical: displacement \(s\) in metres. Horizontal: time \(t\) in seconds. A straight line runs from \((0\text{ s},0\text{ m})\) to \((3\text{ s},6\text{ m})\). **Slope** \(=\Delta s/\Delta t=6/3=2\text{ m/s}\), the velocity. Area under \(s\)–\(t\) is **not** travelled distance.
4. **Check with units.** Area \(F\times x\) has \(\text{N}\cdot\text{m}=\text{J}\); slope \(U/x\) has \(\text{J/m}=\text{N}\); slope \(s/t\) has \(\text{m/s}\). Each output unit tells you what kind of answer is possible.
5. **Say the decision before calculating.** “These axes show __ versus __, so I must use __, because the answer should be measured in __.”

**Mini choice (not the reserved task):** A line sloping upwards on a displacement–time graph shows **positive velocity**; it does not, by itself, give the force or work. A sloping upwards *potential-energy* line has a conservative force **in the negative x-direction**.

## Core1B — unseen challenge (three different graph decisions)

**The robot-lab graph cards.** A student finds three *new* graphs. Each line joins the listed points as a straight section, with units labeled:

- **Card R (force–position):** y-axis \(F_x\) (N), x-axis \(x\) (m). Force rises **linearly** from \((x=0\text{ m},F_x=0\text{ N})\) to \((x=4\text{ m},F_x=8\text{ N})\). The robot moves in the positive x-direction. Find the **work** by this force over 0–4 m.
- **Card S (potential–position):** y-axis \(U\) (J), x-axis \(x\) (m). Potential rises linearly from \((0\text{ m},2\text{ J})\) to \((2\text{ m},8\text{ J})\). Find the **conservative force component** within this interval.
- **Card T (displacement–time):** y-axis \(s\) (m), x-axis \(t\) (s). The line runs in two *straight* segments through \((0\text{ s},0\text{ m})\), \((2\text{ s},4\text{ m})\), \((5\text{ s},16\text{ m})\). What is the **velocity between 2 s and 5 s**?

The important challenge is not merely arithmetic: **choose the correct graph operation for each card and explain why the other operation would be wrong**.

### 01 Predict — before calculating
Which card requires *area*, and which two require *slope*? Label each answer with its physical unit before inserting numbers.

### 02 Attempt — choose the model independently
Sketch three tiny labeled graphs or reconstruct their coordinates. On each card write **axes → operation → quantity → units** and compute all three. Explain why the middle card uses a **negative** slope and why the first card's triangular area is not calculated like a rectangle. Save the first explanation before hints.

### 03 Reconstruct — after commitment
Compare each chosen operation and dimension with the answer rubric. Explain why the Card R triangle's area means work, the Card S slope means force and the Card T slope means velocity.

### 04 Diagnose
Look for: using the slope of the force–position graph as work, taking the area under potential–position as work, missing the minus sign in \(F_x=-dU/dx\), averaging Card T's speed across **the whole 0–5 s** rather than the requested 2–5 s, or omitting units.

### 05 Repair
Ask the child to **circle the axis labels** on the first wrong card, rewrite that card's *operation* and only then recompute. Keep the corrected answer separate from the original.

### 06 Boundary test
Card R now has the same triangular shape and numbers but the horizontal axis is **time in seconds**, not position. What does the **area** under an \(F_x\)–\(t\) graph represent? Is it still work? State the new unit.

## Author-only reference, not for learner-facing pre-attempt delivery

- **R:** triangular area \(W=\tfrac12(4\text{ m})(8\text{ N})=+16\text{ J}\). Slope \(8/4=2\text{ N/m}\) is **not** the requested work.
- **S:** \(dU/dx=(8-2)/2=+3\text{ J/m}\), so \(F_x=-3\text{ N}\). The graph's positive potential values do not imply positive force.
- **T:** second segment slope \(v=(16-4)/(5-2)=12/3=4\text{ m/s}\). The 0–2 s segment has \(2\text{ m/s}\) but is not the requested interval. At the ideal corner \(t=2\text{ s}\), instantaneous slope is not uniquely defined; the prompt deliberately asks on the **open** 2–5 s segment.
- **Boundary:** force–**time** triangular area \(=\tfrac12(4\text{ s})(8\text{ N})=16\text{ N}\cdot\text{s}\), which is *impulse* \(\Delta p\), **not work**. Changing an axis changes the physical operation even if a drawing looks identical.
- **Rubric:** labels all axes and units; chooses area/slope/slope for defensible reasons; computes +16 J, −3 N and +4 m/s; correctly explains why \(F\)–\(t\) area is impulse; can identify one wrong method and repair it.

**Scientific conditions:** Card R uses force component along signed one-dimensional displacement, Card S a one-dimensional differentiable conservative potential on the interval, and Card T straight segments with defined constant velocities away from corners. No unseen original graph is being asserted or reconstructed.

**Separation check:** guided = three simpler horizontal/falling/straight line graphs with direct quantity prompts; independent = rising **triangular force area**, rising potential with negative force and **piecewise** displacement–time segment. The decisive learner choice is which operation each axis pair warrants.