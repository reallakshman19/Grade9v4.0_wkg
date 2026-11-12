/* WPE C01–C08 interactive student practice. Client-side only: NOT secured answers,
 * not authenticated learner evidence, not academic Core1A/B acceptance.
 * Source author packs: WPE-C01 through C08 (work, spring, power, rope, graphs, circular motion, conveyor flow and controlled-variable springs).
 */
(() => {
  "use strict";

  const stages = ["Predict", "Attempt", "Reconstruct", "Diagnose", "Repair", "Boundary test"];
  const signChoices = ["Positive (+)", "Negative (−)", "Zero (0)", "I'm not sure"];
  const lessons = {
    C01: {
      title: "Every force counts",
      version: 1,
      prediction: "Which forces help the scooter move up the ramp, which oppose it, and which do no work? Will it speed up?",
      hints: ["First choose the scooter as the system. Which way is its displacement while climbing?","Assign a work sign to each force before calculating. The normal force is perpendicular to the ramp, but gravity is not.","Add all signed work, then compare that total with the change in kinetic energy. Check whether the result permits motion from rest."],
      diagnosisFeedback: ["List motor, friction, gravity and normal force separately; choose the scooter as your system.","Use the uphill displacement as the reference direction. Friction opposes it; gravity also removes energy as height rises.","Only the sum of work by all forces equals ΔK. Rebuild your signed ledger before solving for speed.","The normal force is perpendicular to the surface displacement, so its work is zero.","Keep your force ledger; inspect signs, units and whether the final K is physically possible.","Start with a free-body sketch and label each force's angle to displacement."],
      fields: [
        {id:"system",type:"select",label:"What object are you following?",options:["The scooter", "Only the motor", "Only the friction", "I'm not sure"]},
        {id:"motor",type:"select",label:"Work done by the motor?",options:signChoices},
        {id:"friction",type:"select",label:"Work done by friction?",options:signChoices},
        {id:"gravity",type:"select",label:"Work done by gravity?",options:signChoices},
        {id:"normal",type:"select",label:"Work done by the normal force?",options:signChoices},
        {id:"netWork",type:"number",label:"Net work by all forces (J)",hint:"Use + or − for the total."},
        {id:"topSpeed",type:"number",label:"Speed at the top (m/s)",hint:"You can use a rounded number."},
        {id:"canReach",type:"select",label:"Will it reach the top?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain your force arrows, energy ledger and reasoning",hint:"You can write 'I'm not sure' and learn from the next step."}
      ],
      worked: [
        ["Pick the system", "Follow the 3 kg scooter moving 2 m uphill. Its normal force is perpendicular to the slope."],
        ["Make a four-force ledger", "Motor work = +15 × 2 = +30 J. Friction = −3 × 2 = −6 J. Gravity = −mgh = −3 × 10 × 0.5 = −15 J. Normal force = 0 J."],
        ["Add all the work", "Net work = +30 − 6 − 15 + 0 = +9 J. It is incorrect to set friction work alone equal to the change in kinetic energy."],
        ["Find the final speed", "It starts from rest, so initial kinetic energy is 0 J. Final kinetic energy = 9 J. Because ½ × 3 × v² = 9, v² = 6 and v ≈ 2.45 m/s. It reaches the top."]
      ],
      rubric: [
        "I followed the scooter as the system and identified all four forces.",
        "I matched each work sign to the scooter's uphill displacement.",
        "I included gravity and gave zero work to the perpendicular normal force.",
        "I used net work = change in kinetic energy to find speed."
      ],
      diagnoses: [
        "I left gravity out of my ledger.",
        "I gave friction or gravity the wrong sign.",
        "I used only friction work instead of total work.",
        "I gave the normal force nonzero work.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Write your corrected force ledger and final speed. Explain what you changed from your first try (or why no change was needed).",
      boundaryPrompt: "Now the scooter's motor pulls with only 10 N uphill. Everything else is unchanged and it starts from rest. Can it climb the whole ramp? Explain using the energy ledger or the forces—not just yes or no.",
      boundaryCheck: [
        "Motor work over a hypothetical full climb would be +10 × 2 = +20 J.",
        "Friction and gravity still require −6 J and −15 J, so net work over the full ramp would be −1 J.",
        "A scooter starting at rest has 0 J initial kinetic energy, and cannot finish with −1 J. It cannot climb the whole ramp without extra energy.",
        "Another check: downhill gravity component = mgh / 2 m = 7.5 N. Together with 3 N friction, resistance is 10.5 N, more than the motor's 10 N."
      ]
    },
    C02: {
      title: "When the spring stops pushing",
      version: 1,
      prediction: "At what point does the spring stop pushing? Will the cart's speed be the same at spring release and after the rough strip?",
      hints: ["Split the journey into spring contact and travel beyond the spring. What marks the moment an unattached spring stops pushing?","Calculate the stored elastic energy while compressed; use it to determine kinetic energy at release before adding any rough-strip losses.","On the rough strip, the spring no longer supplies work. Deduct frictional work from the release kinetic energy and check whether K stays nonnegative."],
      diagnosisFeedback: ["Mark the natural-length point as the end of contact for an unattached spring.","Use friction only where the track is rough; the initial spring contact phase is smooth.","Write the separate energy balances for the release and the end of the rough strip.","Check the elastic energy ½kx² and negative friction work before using K=½mv².","Keep the two-region model; verify the square and square-root arithmetic.","Sketch both regions with a clear boundary; list which forces act in each."],
      fields: [
        {id:"boundary",type:"select",label:"When does spring contact end?",options:["When the spring returns to natural length", "At the far end of the rough strip", "The spring keeps pushing forever", "I'm not sure"]},
        {id:"springEnergy",type:"number",label:"Initial spring energy (J)"},
        {id:"releaseSpeed",type:"number",label:"Speed right when contact ends (m/s)"},
        {id:"frictionWork",type:"number",label:"Work done by friction on the rough strip (J)",hint:"Use a negative sign if it removes energy."},
        {id:"finalSpeed",type:"number",label:"Speed at the end of the rough strip (m/s)"},
        {id:"canCross",type:"select",label:"Can the cart cross the 0.50 m strip?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain the two regions and the equations you chose",hint:"Name the contact phase and the rough-strip phase. 'I'm not sure' is okay."}
      ],
      worked: [
        ["Split the journey", "Region A: smooth contact as the spring goes from compressed to natural length. Region B: the 0.50 m rough strip after the cart is no longer touching the spring."],
        ["Energy at spring release", "Stored spring energy = ½ × 200 × 0.10² = 1.00 J. In smooth contact it becomes 1.00 J of kinetic energy. For the 2 kg cart: ½ × 2 × v² = 1, so release speed = 1.00 m/s."],
        ["Energy in the rough region", "The spring is no longer pushing. Friction work = −1 N × 0.50 m = −0.50 J, so final kinetic energy = 1.00 − 0.50 = 0.50 J."],
        ["Check the speed and route", "½ × 2 × v² = 0.50, giving v = √0.50 ≈ 0.707 m/s. The cart still has positive kinetic energy at the strip's end, so it crosses."]
      ],
      rubric: [
        "I marked where the unattached spring reaches natural length and stops pushing.",
        "I found spring energy and release speed using the smooth contact phase only.",
        "I included friction only on the separate rough strip.",
        "I carried release kinetic energy into the second region and found final speed."
      ],
      diagnoses: [
        "I kept adding spring force after contact ended.",
        "I added friction during the smooth spring-release section.",
        "I used the release speed again at the strip's far end.",
        "I mixed up spring energy, friction work or mass.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Redraw the contact boundary in words, then write a corrected two-region energy calculation and final speed. What changed?",
      boundaryPrompt: "Make the rough strip 1.00 m long instead of 0.50 m, keeping friction at 1 N. The cart starts from rest with the same spring. Does it reach the far end with a nonzero speed? Explain what happens there.",
      boundaryCheck: [
        "At spring release, the cart still has 1.00 J of kinetic energy.",
        "A 1.00 m strip with 1 N friction removes 1.00 J: friction work = −1.00 J.",
        "At the far end, kinetic energy would be exactly 0 J and speed 0 m/s. It reaches the endpoint and stops, but does not pass it with nonzero speed.",
        "A longer rough strip would require more energy than the cart has; without another push it cannot cross that longer strip."
      ]
    },
    C03: {
      title: "Energy added each second",
      version: 1,
      prediction: "With constant motor power, do we gain equal kinetic energy every second, equal speed every second, or both? Which graph will be straight?",
      hints: ["Identify what the source controls: a fixed rate of energy transfer, not a fixed force. What are the units of watts?","Write a K-versus-time table starting with the kinetic energy at t=0. Convert each K to speed only after that.","Read graph slopes: K–time slope is power; v–time slope is acceleration; displacement–time slope is speed. These slopes need not have the same shape."],
      diagnosisFeedback: ["Return to the units: watts are joules per second, not newtons or metres per second squared.","The trolley is already moving. Compute K₀ from its mass and starting speed before adding energy.","Use K=½mv² after each time row; equal energy increments do not mean equal speed increments.","Name both axes before describing a graph: energy, speed and displacement have different slopes.","Check the assumptions: net power is constant on a smooth track, but force P/v falls as speed grows.","Start with the distinction between power, work and kinetic energy. Compare units before equations."],
      fields: [
        {id:"powerMeaning",type:"select",label:"What does 18 W tell us?",options:["The motor adds 18 J every second", "The force is always 18 N", "The trolley gains 18 m/s every second", "I'm not sure"]},
        {id:"initialEnergy",type:"number",label:"Kinetic energy at the start (J)",hint:"Remember: the trolley is already moving at 2 m/s."},
        {id:"energyAt2",type:"number",label:"Total kinetic energy after 2 s (J)",hint:"Include the initial kinetic energy."},
        {id:"speedAt2",type:"number",label:"Speed after 2 s (m/s)",hint:"A rounded decimal is fine."},
        {id:"energyAt6",type:"number",label:"Total kinetic energy after 6 s (J)"},
        {id:"speedAt6",type:"number",label:"Speed after 6 s (m/s)"},
        {id:"energyGraph",type:"select",label:"Shape of kinetic energy against time?",options:["Straight rising line", "Curving line that flattens", "Horizontal line", "I'm not sure"]},
        {id:"speedGraph",type:"select",label:"Shape of speed against time?",options:["Straight rising line", "Rising curve that gradually flattens", "Horizontal line", "I'm not sure"]},
        {id:"distanceGraph",type:"select",label:"Shape of displacement against time?",options:["Straight rising line", "Rising curve that gets steeper", "Horizontal line", "I'm not sure"]},
        {id:"acceleration",type:"select",label:"Is acceleration constant?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Show your time → energy → speed table and explain the three graph shapes",hint:"It's okay to say 'I'm not sure' at any step."}
      ],
      worked: [
        ["Start with the trolley's own energy", "The 3 kg trolley starts at 2 m/s. K₀ = ½ × 3 × 2² = 6 J. Power is 18 W = 18 J of added kinetic energy each second, not 18 N."],
        ["Make a two-time energy table", "At 2 seconds, added energy = 18 × 2 = 36 J, total K = 6 + 36 = 42 J. At 6 seconds, added = 18 × 6 = 108 J, total K = 6 + 108 = 114 J."],
        ["Turn energy into speed", "Using K = ½mv²: at 2 s, v² = 2 × 42 / 3 = 28, so v ≈ 5.29 m/s. At 6 s, v² = 2 × 114 / 3 = 76, so v ≈ 8.72 m/s."],
        ["Choose the right graph shape", "K–time is a rising straight line (equal joules added each second). Speed–time rises but gradually flattens. Displacement–time rises and gets steeper because its slope is speed. You do not need to calculate exact distance."],
        ["Check acceleration", "It is not constant: at positive speed, the driving force F = P / v gets smaller as the trolley speeds up. Constant power does not mean constant force or equal speed gains each second."]
      ],
      rubric: [
        "I used 18 W as joules per second and included the trolley's starting energy.",
        "I built both time → added energy → total kinetic energy → speed rows.",
        "I used the correct axes to describe the three different graph shapes.",
        "I explained why constant power does not mean constant acceleration."
      ],
      diagnoses: [
        "I treated watts as newtons or as a fixed acceleration.",
        "I forgot the starting kinetic energy.",
        "I added the same speed each second instead of the same energy.",
        "I mixed up the speed, displacement and kinetic-energy graph shapes.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Correct the first wrong entry in your time–energy–speed table or your graph explanation. Give both speeds and say whether acceleration stays constant. What did you change?",
      boundaryPrompt: "The SAME 3 kg trolley still starts at 2 m/s, but the motor now supplies 9 W (half the original power). What is its speed after 2 seconds? Does that make its acceleration constant? Explain.",
      boundaryCheck: [
        "The trolley starts with K₀ = ½ × 3 × 2² = 6 J. The power is now 9 J/s.",
        "After 2 s it gains 9 × 2 = 18 J, so the total kinetic energy is 6 + 18 = 24 J.",
        "From ½ × 3 × v² = 24, we get v² = 16 and speed = 4 m/s.",
        "Acceleration is still not constant: the motor supplies constant power, so as speed grows its driving force F = P / v decreases. Power changed, not the kind of model."
      ]
    },
    C04: {
      title: "Only the hanging part",
      version: 1,
      prediction: "As you pull the rope upward from 4 m hanging to 2 m hanging, what happens to the hanging mass and the position of its middle? Will this take as much work as lifting all of it?",
      hints: ["Find the rope's mass per metre. Only the part below the edge contributes nonzero gravitational potential energy for the chosen zero.","Draw two separate hanging pieces. In each, both the hanging mass and its centre depth depend on the hanging length.","Find the potential energy in each picture relative to the platform, then subtract final minus initial for a very slow, frictionless lift."],
      diagnosisFeedback: ["Use mass per metre times hanging length, not the mass of the rope already on the table.","The hanging length changes, so hanging mass must be recalculated for the after-picture.","For a uniform hanging piece, its centre is halfway down that piece.","Use one fixed height-zero and calculate final potential energy minus initial potential energy.","Keep the two-picture model and recheck arithmetic and signs.","Make a before/after table with hanging length, mass, centre depth and U."],
      fields: [
        {id:"massPerMetre",type:"number",label:"Mass per metre of rope (kg/m)",hint:"Divide the whole rope mass by the whole rope length."},
        {id:"startMass",type:"number",label:"Mass hanging BEFORE the pull (kg)",hint:"Only 4 m out of 8 m hangs at the start."},
        {id:"startDepth",type:"number",label:"Depth of the hanging part's middle BEFORE (m below platform)"},
        {id:"startU",type:"number",label:"Gravitational potential energy BEFORE (J)",hint:"Choose platform height as zero. Below it is negative."},
        {id:"endMass",type:"number",label:"Mass hanging AFTER the pull (kg)",hint:"2 m still hangs. The hanging mass has changed."},
        {id:"endDepth",type:"number",label:"Depth of the hanging part's middle AFTER (m below platform)"},
        {id:"endU",type:"number",label:"Gravitational potential energy AFTER (J)"},
        {id:"helperWork",type:"number",label:"Positive work by the helper (J)",hint:"Take final potential energy minus initial potential energy."},
        {id:"modelChoice",type:"select",label:"Which mass model did you use?",options:["Only the hanging mass in each state", "The whole 4 kg rope in both states", "The mass hanging at the start for both states", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Describe the two hanging-length pictures and explain how you found the work",hint:"Describe the middle of each hanging piece. You may write 'I'm not sure'."}
      ],
      worked: [
        ["Start with mass per metre", "The 8 m rope has 4 kg of mass, so 4 ÷ 8 = 0.5 kg per metre. Only the hanging length contributes energy below platform height."],
        ["Draw the BEFORE state", "Initially 4 m hangs: hanging mass = 0.5 × 4 = 2 kg. Its middle is halfway down, at 2 m below the platform. With U = 0 on the platform, U_before = −2 × 10 × 2 = −40 J."],
        ["Draw the AFTER state", "Only 2 m remains hanging: mass = 0.5 × 2 = 1 kg; its middle is 1 m below the platform. U_after = −1 × 10 × 1 = −10 J."],
        ["Subtract final minus initial", "The helper pulls slowly on a smooth edge, so their positive work equals the rise in gravitational potential energy: (−10) − (−40) = +30 J."],
        ["Explain the key decision", "Both the hanging mass and its centre-of-mass depth shrink. Using the entire 4 kg rope or the starting hanging mass for the final state would model the wrong picture."]
      ],
      rubric: [
        "I found the mass per metre and used only the mass actually hanging in each state.",
        "I placed the middle of each uniform hanging piece halfway down.",
        "I calculated a separate potential energy before and after, using the platform as zero.",
        "I subtracted final minus initial and explained why the helper's work is positive."
      ],
      diagnoses: [
        "I treated the whole 4 kg rope as if it were hanging.",
        "I kept the hanging mass unchanged after pulling.",
        "I placed the middle at the bottom of the hanging piece.",
        "I mixed up the minus signs when subtracting potential energies.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Write a corrected BEFORE and AFTER table with hanging mass, middle depth and potential energy, then the helper's work. Explain which picture or subtraction you fixed.",
      boundaryPrompt: "Start with the SAME 8 m, 4 kg rope with 4 m hanging. Now pull it COMPLETELY onto the smooth platform (0 m hanging). How much work is needed, and why is this more than stopping with 2 m still hanging?",
      boundaryCheck: [
        "The starting hanging part is unchanged: 2 kg, with its middle 2 m below the platform, so U_before = −40 J.",
        "If the rope is fully on the platform, 0 m hangs: U_after = 0 J.",
        "The slow helper's work is U_after − U_before = 0 − (−40) = +40 J.",
        "That exceeds the +30 J partial-lift case because the helper lifts the remaining hanging 2 m section as well. The full rope does not rise by one identical height."
      ]
    },
    C05: {
      title: "Read the axes first",
      version: 1,
      prediction: "Which new graph card needs an area, and which two need a slope? What units should your answers use?",
      hints: ["Read each graph's vertical and horizontal axis labels, then ask what UNIT the question wants. Force × distance makes joules; distance ÷ time makes metres per second.","For the U–position graph, draw an arrow showing that potential rises to the right. A conservative force points opposite the direction of increasing potential. For card T, use only the requested 2–5 s interval."],
      diagnosisFeedback: ["Put the horizontal axis unit under the force graph. Multiply newtons by metres to get work; the line's slope has different units.","Find the change in U divided by change in position, then reverse its sign to get conservative force. The U–x area does not represent force.","Circle the requested 2–5 s interval, read its two displacement values and divide their difference by three seconds.","Start each card with 'vertical axis / horizontal axis / operation / resulting unit' before doing any number work.","Check your units and signs against the axes once more. If they match, keep the original reasoning and explain why.","Use one card at a time and start from its axis names. A small table is enough; you don't need all three answers at once."],
      fields: [
        {id:"graphR",type:"select",label:"Card R: How do you find work from force against position?",options:["Area between the line and x-axis", "Slope of the line", "Area under a potential–position line", "I'm not sure"]},
        {id:"workR",type:"number",label:"Card R: Work over 0–4 m (J)",hint:"The force rises from 0 N to 8 N. Think about a triangle."},
        {id:"graphS",type:"select",label:"Card S: How do you find the conservative force from U against x?",options:["Area under the graph", "Negative slope of the line", "Positive slope of the line", "I'm not sure"]},
        {id:"forceS",type:"number",label:"Card S: Conservative force (N)",hint:"Give a minus sign if the force points left."},
        {id:"graphT",type:"select",label:"Card T: How do you find velocity from displacement against time?",options:["Area below the curve", "Slope of the segment from 2–5 s", "Slope of the entire 0–5 s span", "I'm not sure"]},
        {id:"speedT",type:"number",label:"Card T: Velocity from 2–5 s (m/s)"},
        {id:"unitChoice",type:"select",label:"Which units belong to R, S and T, in that order?",options:["J, N, m/s", "N/m, J, m/s", "J, J, m", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain how the axes told you to use area or slope for all three cards",hint:"Use the pattern: axes → operation → quantity → units. 'I'm not sure' is okay."}
      ],
      worked: [
        ["R: read F against x", "The y-axis is force (N) and the x-axis is position (m). Work is the signed AREA under F–x. A triangle rising 0 to 8 N over 4 m has area ½ × 4 × 8 = +16 J. Its slope is NOT work."],
        ["S: read U against x", "Potential energy rises from 2 J at 0 m to 8 J at 2 m. The slope is (8 − 2) ÷ (2 − 0) = +3 J/m, and a conservative force is the NEGATIVE slope: F = −3 N. The area under U–x is not work."],
        ["T: read s against t", "Between 2 s and 5 s, displacement rises from 4 m to 16 m. The slope of THAT straight segment is (16 − 4) ÷ (5 − 2) = +4 m/s. The earlier 0–2 s part has a different slope and is not the interval asked."],
        ["Check the meaning of units", "Force × position → N·m = J of work; change in potential energy ÷ position → J/m = N of force, with a minus sign; change in displacement ÷ time → m/s of velocity."],
        ["What if the graph has a corner?", "Card T has a sharp join at 2 s. It has a well-defined slope from 2 to 5 s, but at the exact corner a single instantaneous slope is not defined. Always check which interval is requested."]
      ],
      rubric: [
        "I identified the horizontal and vertical axes and chose area, negative slope and slope, in that order.",
        "I used the triangular force–position AREA for +16 J of work instead of its line slope.",
        "I remembered the negative sign for the conservative force and got −3 N.",
        "I used only the 2–5 s segment and gave +4 m/s with the correct units."
      ],
      diagnoses: [
        "I used the slope of the force–position graph as work.",
        "I used the area of the potential–position graph or forgot the negative force sign.",
        "I measured the full 0–5 s interval instead of the 2–5 s segment.",
        "I mixed up units or did not look at the axes first.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "For each card, write its axes, the chosen operation and the physical answer with units. Circle in words the first wrong choice in your original explanation. What did you fix?",
      boundaryPrompt: "Imagine Card R is drawn with the SAME rising triangle from 0 to 8 N over 4 horizontal units, but the horizontal axis is now TIME (0–4 s), not position. What does the AREA under a force–time graph represent? Is it still work? Give the quantity and unit.",
      boundaryCheck: [
        "Read the altered axes FIRST: vertical F in newtons, horizontal t in seconds.",
        "The triangular area is still ½ × 4 × 8 = 16 numerically, but now its unit is N·s, not N·m.",
        "Area under FORCE–TIME is IMPULSE (change in momentum), so the result is +16 N·s for the shown positive force.",
        "It is NOT 16 J of work. A graph's meaning depends on its labeled axes, even when the shape looks identical."
      ]
    },
    C06: {
      title: "Stay on the circle?",
      version: 1,
      prediction: "The ball has enough energy to be at the top height in a calculation. Does that alone prove its string can stay taut? At the top, which way is inward and can a string push?",
      hints: ["Draw two arrows at the top of the circular path: one toward the centre and one in the direction of gravity. What direction would the tension in a taut string pull?","First use the height rise from bottom to top to estimate top speed from energy. THEN compare the inward force it needs with the weight that already points inward. A string cannot provide an outward push."],
      diagnosisFeedback: ["Separate the tests: reaching the top HEIGHT using energy is not the same as staying on the taut circular route.","At the top, the centre is below the ball. Redraw downward gravity and downward string tension before forming the radial-force equation.","A negative computed tension means the assumed taut-string model is invalid. A string cannot push; use this sign as a physical check.","Speed is tangent to the circle while inward acceleration has magnitude v²/r. Label their directions separately before calculating.","Recheck the 2r height difference, top-speed squared and force signs. Explain whether your initial model already did both tests.","Try two small calculations: 'energy allows this height?' and 'tension can pull inward?' The second decision is what the first cannot answer."],
      fields: [
        {id:"topInward",type:"select",label:"At the top of a vertical circle, which direction is toward its centre?",options:["Downward", "Upward", "Along its tangential velocity", "I'm not sure"]},
        {id:"heightRise",type:"number",label:"Height change from bottom to top (m)",hint:"The rise is twice the circle's 1 m radius."},
        {id:"candidateSpeedSquared",type:"number",label:"Candidate top speed squared, v² (m²/s²)",hint:"Use energy only for a hypothetical taut circle: v_top² = v_bottom² − 4gr."},
        {id:"candidateSpeed",type:"number",label:"Candidate top speed (m/s)"},
        {id:"energyPossible",type:"select",label:"Does energy alone allow a ball to be at the top height?",options:["Yes", "No", "I'm not sure"]},
        {id:"radialEquation",type:"select",label:"Which equation is valid at the top WHILE the string is taut?",options:["T + mg = mv²/r", "T − mg = mv²/r", "T = mg + mv²/r", "I'm not sure"]},
        {id:"topTension",type:"number",label:"Calculated top string tension (N)",hint:"A negative answer is a warning about the model."},
        {id:"staysTaut",type:"select",label:"Can this string remain taut all the way over the top?",options:["Yes", "No", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain the two checks—energy AND inward force—and what your tension sign means",hint:"Say what a real string can and cannot do. You may write 'I'm not sure'."}
      ],
      worked: [
        ["Check the height with energy", "The top is 2r = 2 × 1 = 2 m higher than the bottom. For a hypothetical taut circle, v_top² = v_bottom² − 4gr = 7² − 4 × 10 × 1 = 9. So candidate top speed = 3 m/s. Energy ALONE would allow that height."],
        ["Draw the top inward arrow", "At the very TOP, the centre of the circle is DOWNWARD. Both gravity mg and the taut-string tension T would point downward. The radial-force equation is T + mg = mv_top²/r."],
        ["Check the force the string would need", "For 1 kg, g = 10 and r = 1: needed inward force mv²/r = 1 × 9 ÷ 1 = 9 N, while gravity alone pulls inward with 10 N. Thus T = 9 − 10 = −1 N."],
        ["Interpret impossible negative tension", "A string can PULL but cannot PUSH. T = −1 N is not a real pulling tension. The imagined taut circular trajectory is impossible: the string goes slack BEFORE the top. After slackening, the bob is no longer constrained to the original circle."],
        ["State the difference between tests", "The correct conclusion is NOT 'the ball has too little energy to reach the height'. The energy test passes, but the radial-force (taut-string) test fails. Both are needed for a full taut circle."]
      ],
      rubric: [
        "I used the 2 m rise and calculated the candidate top speed squared from energy.",
        "I marked inward as downward at the top and wrote T + mg = mv²/r.",
        "I calculated −1 N and recognized it as an impossible pulling tension, not a normal negative force.",
        "I concluded the string slackens before the top; energy alone does not guarantee a taut circle."
      ],
      diagnoses: [
        "I assumed enough energy automatically means the ball stays on its circle.",
        "I drew the top inward direction or force signs incorrectly.",
        "I accepted negative tension as a real string pushing outward.",
        "I mixed up v²/r (inward acceleration) with tangential speed or acceleration.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Draw in words the top centre arrow and write BOTH the energy and radial-force checks. What must you correct about a negative tension and whether the string remains taut?",
      boundaryPrompt: "Keep the SAME 1 kg ball and 1 m light string, but start it at the bottom at 8 m/s instead of 7 m/s. Compute candidate top v² and the top tension. Could the string remain taut through the top now? Explain both checks.",
      boundaryCheck: [
        "For the hypothetical taut circle, v_top² = 8² − 4 × 10 × 1 = 64 − 40 = 24 m²/s². The energy test passes.",
        "At the top, inward is down and T + mg = mv²/r. Thus T = 1 × 24 / 1 − 1 × 10 = +14 N.",
        "The top tension is positive, so the string CAN remain taut at the top; under the ideal lossless conditions, the complete circular path is physically possible.",
        "For comparison, the ideal minimum bottom speed for a just-taut top is √(5gr) = √50 ≈ 7.07 m/s. Seven was slightly too low; eight is above it."
      ]

    },
    C07: {
      title: "Momentum arrives every second",
      version: 1,
      prediction: "The chips arrive already moving right. Does the belt need to speed them up? Will extra motor power all become the chips' kinetic energy, or might some become heat?",
      hints: ["Draw a one-second batch of arriving chips. Label their incoming horizontal speed and outgoing belt speed, and use kilograms EACH second rather than total chips accumulated.","Calculate the force from mass-per-second × speed change. Motor power uses BELT speed, while kinetic-energy change uses both squared speeds. What is left over during slipping?"],
      diagnosisFeedback: ["Use a control-volume picture: count new kilograms per second, not the entire stock already riding the conveyor.","Underline the 1 m/s incoming speed and the feed rule 'half the belt speed'. Recompute the horizontal velocity gain before force.","The motor keeps the belt moving, so its pickup force moves at BELT speed. Recalculate mechanical power at that speed.","Make a three-column energy ledger: motor input, chip kinetic-energy gain, and heat. Do not force the first two columns to match.","Check units in each line: kg/s × m/s makes N; N × m/s makes W. Then test whether the three power entries balance.","Start with two arrows, 'before' and 'after', and a small box labelled 'kg each second'. Keep each calculation separate."],
      fields: [
        {id:"model",type:"select",label:"Which object or flow are you following?",options:["Incoming kilograms of chips each second", "All chips ever collected on the belt", "Only the empty belt", "I'm not sure"]},
        {id:"flowRate",type:"number",label:"Mass of new chips per second (kg/s)",hint:"The feed rate equals half the numerical belt speed."},
        {id:"deltaVelocity",type:"number",label:"Horizontal velocity gain per kilogram (m/s)",hint:"Subtract incoming rightward speed from outgoing belt speed."},
        {id:"pickupForce",type:"number",label:"Force needed on new chips (N)",hint:"Flow rate multiplied by horizontal velocity gain."},
        {id:"motorPower",type:"number",label:"Extra motor power for pickup (W)",hint:"Force needed to hold belt speed × belt speed."},
        {id:"chipEnergy",type:"number",label:"Rate of chips' horizontal kinetic-energy gain (W)",hint:"½ × kilograms per second × (outgoing speed squared − incoming speed squared)."},
        {id:"heatRate",type:"number",label:"Rate of heat during speed matching (W)",hint:"Extra motor power minus chips' kinetic-energy-gain rate."},
        {id:"energyModel",type:"select",label:"Where does the extra motor power go?",options:["Part to chips' kinetic energy and part to frictional heating", "All to chips' kinetic energy", "All to gravity", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain your incoming → outgoing momentum picture and the three power rates",hint:"Start with kilograms each second, then explain why motor power is not equal to the chips' kinetic-energy gain. 'I'm not sure' is okay."}
      ],
      worked: [
        ["Read the feed rate and arrival speed", "The belt speed is 4 m/s, so the feeder delivers 4 ÷ 2 = 2 kg of chips EACH SECOND. Chips arrive already moving right at 1 m/s and leave at 4 m/s: Δv = 4 − 1 = +3 m/s."],
        ["Change momentum per second", "Horizontal force on the incoming stream is mass rate × Δv = 2 × (4 − 1) = +6 N. The chips push the belt backward with 6 N, so the motor must supply an extra 6 N forward to hold belt speed."],
        ["Find pickup-related motor power", "Motor power = extra forward force × belt speed = 6 N × 4 m/s = 24 W. Use belt speed, NOT incoming chip speed, for this motor power."],
        ["Compute kinetic-energy gain separately", "Each second, 2 kg of chips change speed from 1 to 4 m/s: gain rate = ½ × 2 × (4² − 1²) = 15 W. They did NOT start with zero horizontal kinetic energy."],
        ["Balance input, gain and heat", "Motor pickup power = 24 W; chips' kinetic-energy-gain rate = 15 W. The difference is 9 W of frictional heat in this idealized pickup. Check: ½ × 2 × (4 − 1)² = 9 W, so 24 = 15 + 9."]
      ],
      rubric: [
        "I used kilograms arriving EACH SECOND, not all the accumulated chips, and included the nonzero incoming rightward velocity.",
        "I used force = mass flow rate × (outgoing speed − incoming speed), giving +6 N.",
        "I used BELT speed to find 24 W of extra motor power and distinguished that from 15 W of chips' kinetic-energy gain.",
        "I balanced the 9 W heat rate and explained the speed-matching friction."
      ],
      diagnoses: [
        "I treated all chips already on the belt as the mass to accelerate.",
        "I forgot the incoming 1 m/s or ignored the given feed-rate rule.",
        "I used incoming speed rather than belt speed for motor power.",
        "I assumed all motor power becomes horizontal kinetic energy and forgot heat.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Redraw the incoming → outgoing chip speeds in words. Recalculate the flow rate, force and the separate 24 W motor, 15 W kinetic gain and 9 W heat entries. Explain the first difference from your original attempt.",
      boundaryPrompt: "The chips STILL arrive moving right at 1 m/s, and the feeder STILL delivers half the numerical belt speed in kg/s. But now the belt moves at 2 m/s instead of 4 m/s. Find the mass flow rate, pickup force, extra motor power, chips' kinetic-energy-gain rate and heat rate. Do all five merely halve? Why?",
      boundaryCheck: [
        "At 2 m/s, the flow rate is 2 ÷ 2 = 1 kg/s. The chips' horizontal speed gain is 2 − 1 = 1 m/s.",
        "Force on incoming chips = 1 × 1 = +1 N. Extra motor pickup power = 1 N × 2 m/s = 2 W.",
        "Chips' horizontal kinetic-energy-gain rate = ½ × 1 × (2² − 1²) = 1.5 W.",
        "Heat rate = 2 − 1.5 = 0.5 W. Check: ½ × 1 × (2 − 1)² = 0.5 W.",
        "The numbers do NOT all halve, because the mass flow, belt speed and incoming-to-outgoing velocity DIFFERENCE all change. Other motor losses remain outside this idealized model."
      ]
    },
    C08: {
      title: "What stays the same?",
      version: 1,
      prediction: "At equal compression, which pad looks stiffer from the 4 cm measurement? Will the stiffer pad store more energy under BOTH equal-extension and equal-final-force tests?",
      hints: ["First convert 4 centimetres to metres. Infer each k from the lab measurement using final force divided by compression; the two tests come AFTER this measurement.","Label Test X 'same compression' and Test Y 'same FINAL force'. For Y the softer spring compresses farther, so calculate each new x = F/k instead of reusing X's 5 cm."],
      diagnosisFeedback: ["Remember: 4 cm is 0.04 m and 5 cm is 0.05 m. Recalculate k in N/m before the energy comparisons.","Write 'same extension' over X and 'same final force' over Y. Each condition chooses a different comparison; stiffness alone does not choose the winner.","Test Y must use each spring's own compression under 12 N. Find x = F/k for Blue and Gold, then use elastic energy.","For a slowly increasing Hookean force, the area under the force–extension graph is a TRIANGLE: ½ × final force × extension.","Check that both tests use slow loading and final equilibrium conditions. Review the ordering without erasing the first try.","Start by writing what is held the SAME in each experiment; then calculate one spring at a time."],
      fields: [
        {id:"kBlue",type:"number",label:"Blue pad stiffness (N/m)",hint:"4 cm is 0.04 m. Use k = final force ÷ compression."},
        {id:"kGold",type:"number",label:"Gold pad stiffness (N/m)"},
        {id:"testXChoice",type:"select",label:"Test X: both compressed by 5 cm. Which stores more energy?",options:["Blue pad", "Gold pad", "Same energy", "I'm not sure"]},
        {id:"xBlue",type:"number",label:"Test X: Blue elastic energy (J)",hint:"Use ½ × k × 0.05²."},
        {id:"xGold",type:"number",label:"Test X: Gold elastic energy (J)"},
        {id:"testYChoice",type:"select",label:"Test Y: both reach 12 N FINAL force. Which stores more energy?",options:["Blue pad", "Gold pad", "Same energy", "I'm not sure"]},
        {id:"yBlueExtension",type:"number",label:"Test Y: Blue compression at final force (m)",hint:"New compression = 12 N ÷ stiffness."},
        {id:"yGoldExtension",type:"number",label:"Test Y: Gold compression at final force (m)"},
        {id:"yBlue",type:"number",label:"Test Y: Blue elastic energy (J)",hint:"At equal FINAL force use F² ÷ (2k), or ½ × final force × compression."},
        {id:"yGold",type:"number",label:"Test Y: Gold elastic energy (J)"},
        {id:"control",type:"select",label:"Why can the ranking reverse?",options:["Test X fixes compression; Test Y fixes FINAL force", "Both tests fix compression", "Both tests fix force throughout compression", "I'm not sure"]},
        {id:"reason",type:"textarea",label:"Explain how you inferred both stiffnesses and why the energy ranking switches",hint:"Use a small table: fixed extension versus fixed final force. You can write 'I'm not sure'."}
      ],
      worked: [
        ["Infer stiffness from the first measurements", "At a shared compression of 4 cm = 0.04 m, Blue needs 8 N so k_Blue = 8 ÷ 0.04 = 200 N/m. Gold needs 16 N so k_Gold = 16 ÷ 0.04 = 400 N/m. Gold is stiffer."],
        ["Test X fixes compression, not force", "Both pads are compressed 5 cm = 0.05 m. Blue stores ½ × 200 × 0.05² = 0.25 J. Gold stores ½ × 400 × 0.05² = 0.50 J. GOLD, the stiffer pad, stores more at fixed compression."],
        ["Test Y fixes FINAL force, not compression", "For the SAME final equilibrium force of 12 N: Blue compresses 12 ÷ 200 = 0.06 m; Gold compresses 12 ÷ 400 = 0.03 m. They do NOT have the same compression."],
        ["Compute stored energy at equal final force", "Elastic energy is F² ÷ (2k). Blue stores 12² ÷ (2 × 200) = 0.36 J; Gold stores 12² ÷ (2 × 400) = 0.18 J. BLUE, the softer pad, stores more at fixed FINAL force."],
        ["Explain the reversal and the loading triangle", "For fixed compression, U = ½kx² grows with k. For fixed final force, U = F²/(2k) falls with k. During slow loading the force rises from zero, so energy is ½ × final F × compression—not final F × compression."]
      ],
      rubric: [
        "I converted 4 cm to 0.04 m and inferred Blue 200 N/m and Gold 400 N/m.",
        "I labelled Test X as fixed 5 cm compression and calculated 0.25 J (Blue) and 0.50 J (Gold).",
        "I labelled Test Y as fixed FINAL 12 N force, found different final compressions, and calculated 0.36 J (Blue) and 0.18 J (Gold).",
        "I explained why the stiffer spring wins X but the softer wins Y, without treating final force as constant throughout slow loading."
      ],
      diagnoses: [
        "I used centimetres as metres when inferring stiffness.",
        "I assumed the stiffer pad always stores more energy.",
        "I treated Test Y as though both pads had equal compression.",
        "I multiplied final force × compression instead of the triangular loading area.",
        "My model was fine; I want to double-check the arithmetic.",
        "I'm not sure what went wrong yet."
      ],
      repairPrompt: "Circle in words what is fixed in X and Y. Make a corrected comparison table: each stiffness, both energies at 5 cm, then both energies at FINAL force 12 N and why the winner changes.",
      boundaryPrompt: "Repeat Test Y with the SAME ideal pads, but slowly increase the FINAL force to 24 N (double 12 N). How many times larger does each stored energy become? Calculate Blue and Gold energies, name which pad stores more, and explain why.",
      boundaryCheck: [
        "At a fixed stiffness, stored energy for a slowly increased FINAL force is F² ÷ (2k). Doubling F makes F² four times bigger.",
        "Blue at 24 N stores 24² ÷ (2 × 200) = 1.44 J, four times the former 0.36 J.",
        "Gold at 24 N stores 24² ÷ (2 × 400) = 0.72 J, four times the former 0.18 J.",
        "BLUE still stores more at the same FINAL force, because it is softer and compresses farther. This does not mean a suddenly applied constant 24 N force acts through the entire extension."
      ]

    }
  };

  function initState(lesson) {
    return {schema:1,lesson,stage:0,prediction:null,predictionDraft:"",draft:null,first:null,hintsUsed:0,reconstruction:null,diagnosis:null,repair:null,boundary:null};
  }
  function storageKey(lesson) { return "g9:wpe:d3d4:self-tutor:v1:"+lesson; }
  function load(lesson) {
    try {
      const value = JSON.parse(localStorage.getItem(storageKey(lesson)));
      if(value && value.schema===1 && value.lesson===lesson &&
         Number.isInteger(value.stage) && value.stage>=0 && value.stage<=5 &&
         (value.stage<2 || (value.first && typeof value.first.reason==="string")))
        return value;
    } catch (_) { /* Private mode and malformed storage are both supported. */ }
    return initState(lesson);
  }
  function persist(lesson, state) {
    try { localStorage.setItem(storageKey(lesson), JSON.stringify(state)); return true; }
    catch (_) { return false; }
  }
  function erase(lesson) { try { localStorage.removeItem(storageKey(lesson)); } catch (_) {} }
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if(className) node.className = className;
    if(text!==undefined) node.textContent = String(text);
    return node;
  }
  function addText(parent, tag, className, text) { const n=el(tag,className,text);parent.append(n);return n; }
  function addButton(parent, action, label, variant) {
    const button=el("button",variant||"primary",label);
    button.type="button"; button.dataset.action=action;parent.append(button);return button;
  }
  function stageHeader(root, state) {
    const ol=el("ol","step-list");
    ol.setAttribute("aria-label","Learning steps");
    stages.forEach((name,i)=>{
      const li=el("li",i===state.stage?"current":i<state.stage?"done":"upcoming",(i+1)+". "+name);
      if(i===state.stage)li.setAttribute("aria-current","step");
      ol.append(li);
    });
    root.append(ol);
  }
  function note(root, text, style) {addText(root,"p",style||"step-notice",text);}
  function actions(root) {return root.appendChild(el("div","stage-actions"));}
  function labelFor(root,control,name) {
    const label=el("label",null,name);label.htmlFor=control.id;root.append(label);return label;
  }
  function textArea(root,id,label,hint,defaultValue) {
    const control=el("textarea");
    control.id=id;control.dataset.input=id;control.rows=4;
    labelFor(root,control,label);
    if(hint) note(root,hint,"field-help");
    control.value=defaultValue||"";
    root.append(control);
    return control;
  }
  function select(root,id,label,options) {
    const control=el("select");control.id=id;control.dataset.input=id;
    labelFor(root,control,label);
    let opt=el("option",null,"Choose, or select 'I'm not sure'");
    opt.value="";control.append(opt);
    options.forEach(option=>{opt=el("option",null,option);opt.value=option;control.append(opt);});
    root.append(control);
  }
  function number(root,id,label,hint) {
    const control=el("input");control.type="number";control.step="any";control.inputMode="decimal";control.id=id;control.dataset.input=id;
    labelFor(root,control,label);
    if(hint)note(root,hint,"field-help");
    root.append(control);
  }
  function snapshot(root,state,config) {
    const box=el("section","snapshot");
    addText(box,"strong",null,"Your saved first try — unchanged");
    const dl=el("dl");
    addText(dl,"dt",null,"Prediction");
    addText(dl,"dd",null,state.prediction||"(No prediction written)");
    config.fields.forEach(field=>{
      addText(dl,"dt",null,field.label);
      addText(dl,"dd",null,(state.first && state.first[field.id]) || "(Not sure / blank)");
    });
    box.append(dl);root.append(box);
  }
  function workedList(root, rows, heading) {
    const box=el("section","worked");
    addText(box,"h5",null,heading);
    const list=el("ol");
    rows.forEach(row=>{
      const li=el("li");
      addText(li,"strong",null,row[0]+": ");
      li.append(document.createTextNode(row[1]));
      list.append(li);
    });
    box.append(list);root.append(box);
  }
  function rubricBlock(root,config,checkable,prior) {
    const box=el("section","rubric");
    addText(box,"h5",null,"Check your reasoning, not just the final number");
    const ul=el("ul");
    config.rubric.forEach((item,i)=>{
      const li=el("li");
      if(checkable) {
        const input=el("input");input.type="checkbox";input.value=String(i);input.dataset.rubric=String(i);
        if(prior && prior.includes(i))input.checked=true;
        const label=el("label");label.append(input,document.createTextNode(" "+item));li.append(label);
      } else li.textContent=item;
      ul.append(li);
    });
    box.append(ul);root.append(box);
  }
  function formValues(root) {
    const values={};
    root.querySelectorAll("[data-input]").forEach(field=>{values[field.dataset.input]=field.value.trim();});
    return values;
  }
  function render(lesson, focus) {
    const config=lessons[lesson], state=states[lesson];
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    root.replaceChildren();
    stageHeader(root,state);
    const card=el("section","stage-card");root.append(card);
    const stage=state.stage;
    const top=addText(card,"h4",null,(stage+1)+". "+stages[stage]);
    top.tabIndex=-1;
    if(stage===0) {
      note(card,"Make a prediction first. You don't need to be correct.", "stage-desc");
      textArea(card,"prediction-"+lesson,"What do you think will happen?",config.prediction,state.predictionDraft||state.prediction||"");
      addButton(actions(card),"save-prediction","Keep my prediction and try the problem");
    } else if(stage===1) {
      note(card,"Try the new problem independently. Work in any order and write how you decided. It's fine to say 'I'm not sure'.", "stage-desc");
      note(card,"Prediction saved: "+(state.prediction||"(not sure)"),"step-note");
      const form=el("div","attempt-fields");card.append(form);
      config.fields.forEach(field=>{
        const id=lesson+"-"+field.id;
        if(field.type==="select")select(form,id,field.label,field.options);
        if(field.type==="number")number(form,id,field.label,field.hint);
        if(field.type==="textarea")textArea(form,id,field.label,field.hint,"");
        const input=form.querySelector("#"+id);
        input.dataset.input=field.id;
        if(state.draft && typeof state.draft[field.id]==="string")input.value=state.draft[field.id];
      });
      note(card,"Your unfinished answers are saved on this browser as you type. You can come back to this skill later.","draft-note");
      const hints=config.hints||[];
      if(hints.length){
      const help=el("section","progressive-hints");help.dataset.hintPanel="true";
      addText(help,"strong",null,"Optional thinking hints — no worked answer");
      hints.slice(0,state.hintsUsed||0).forEach((hint,i)=>note(help,"Hint "+(i+1)+": "+hint,"hint-text"));
      card.append(help);
      const hintButton=addButton(actions(card),"next-hint","Show next hint ("+(state.hintsUsed||0)+"/"+hints.length+")","secondary");
      if((state.hintsUsed||0)>=hints.length)hintButton.disabled=true;
      }
      note(card,"Your answers will be frozen as your first attempt. A separate repair comes later.","stage-help");
      addButton(actions(card),"lock-attempt","Save my first attempt and reconstruct");
    } else if(stage===2) {
      note(card,"Now the worked steps are available. Compare them with your original model; we don't grade your writing.", "stage-desc");
      snapshot(card,state,config);
      workedList(card,config.worked,"Worked reconstruction");
      rubricBlock(card,config,true,state.reconstruction||[]);
      addButton(actions(card),"save-reconstruction","I compared the steps → Diagnose");
    } else if(stage===3) {
      note(card,"Find the first difference between your model and the worked steps, even if your number happened to match.", "stage-desc");
      snapshot(card,state,config);
      select(card,lesson+"-diagnosis","Which issue did you find first?",config.diagnoses);
      const field=card.querySelector("#"+lesson+"-diagnosis");field.dataset.input="diagnosis";
      textArea(card,lesson+"-diagnosisWhy","Why did you choose that issue?","If you got it right, explain what you double-checked.","");
      addButton(actions(card),"save-diagnosis","Keep my diagnosis → Repair");
    } else if(stage===4) {
      note(card,"Make a new version of the reasoning. Your original first attempt stays saved above.", "stage-desc");
      snapshot(card,state,config);
      const issueIndex=config.diagnoses.indexOf(state.diagnosis?.issue);
      if(issueIndex>=0 && config.diagnosisFeedback?.[issueIndex])note(card,"Try this repair: "+config.diagnosisFeedback[issueIndex],"diagnostic-tip");
      textArea(card,lesson+"-repair","My repaired calculation and explanation",config.repairPrompt,"");
      addButton(actions(card),"save-repair","Keep my repair → Boundary test");
    } else if(stage===5) {
      if(state.boundary===null) {
        note(card,"A small change to the physics can change the conclusion. Try this one yourself.", "stage-desc");
        addText(card,"p","reflection",config.boundaryPrompt);
        textArea(card,lesson+"-boundary","My answer to the changed-condition test","It's okay to say what you are unsure about.","");
        addButton(actions(card),"save-boundary","Save my boundary test and compare");
      } else {
        addText(card,"p","response-done","Boundary test completed. You've practised all six thinking stages!");
        const answer=el("section","snapshot");
        addText(answer,"strong",null,"Your boundary-test response");
        addText(answer,"p",null,state.boundary);
        card.append(answer);
        workedList(card,config.boundaryCheck.map((v,i)=>["Step "+(i+1),v]),"Compare the changed-condition reasoning");
        note(card,"These are self-check criteria, not a score. The stored first try and later repair are distinct.","stage-help");
        addButton(actions(card),"review-history","View original attempt and repair","secondary");
        if(sourceRoute && sourceRoute.lesson===lesson){
          const a=el("a","return-original","Return to "+sourceRoute.id+" and try the original question independently");
          a.href=sourceRoute.href;card.append(a);
        }
      }
    }
    // Once the first model is locked, the full reasoning stays available for
    // self-diagnosis and repair without exposing the boundary answer in advance.
    if(stage===3 || stage===4 || (stage===5 && state.boundary===null)){
      const ref=el("details","review-model");
      addText(ref,"summary",null,"Review the worked steps while thinking");
      workedList(ref,config.worked,"Worked model — open when you need it");
      card.append(ref);
    }
    const footer=actions(root);
    addButton(footer,"reset","Start this skill again (clears saved work)","danger");
    const msg=addText(root,"p","step-notice","");
    msg.setAttribute("aria-live","polite");msg.dataset.notice="true";
    if(!storageWorks)msg.textContent="This browser did not allow local saving. You can still work through this page, but your progress may disappear on reload.";
    if(focus)top.focus({preventScroll:true});
    updateProgress();
  }
  function updateProgress() {
    let count=0;
    Object.keys(lessons).forEach(lesson=>{ if(states[lesson].boundary!==null)count++; });
    const label=document.getElementById("overall-count");
    const meter=document.getElementById("overall-meter");
    if(label)label.textContent=count+" of "+Object.keys(lessons).length+" challenges completed";
    if(meter){meter.max=Object.keys(lessons).length;meter.value=count;}
  }
  function warn(root, text) {
    const notice=root.querySelector("[data-notice]");
    if(notice)notice.textContent=text;
  }
  function update(lesson, event) {
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    const action=event.target.closest("button[data-action]");
    if(!action || !root.contains(action))return;
    const kind=action.dataset.action;
    let state=states[lesson];
    if(kind==="next-hint" && state.stage===1 && !state.first){
      const used=Math.min(configHintCount(lesson),state.hintsUsed||0);
      if(used>=configHintCount(lesson))return;
      state.hintsUsed=used+1;
      const panel=root.querySelector("[data-hint-panel]");
      note(panel,"Hint "+state.hintsUsed+": "+lessons[lesson].hints[used],"hint-text");
      action.textContent="Show next hint ("+state.hintsUsed+"/"+configHintCount(lesson)+")";
      if(state.hintsUsed>=configHintCount(lesson))action.disabled=true;
      if(!persist(lesson,state))storageWorks=false;
      return;
    }
    if(kind==="reset") {
      if(!window.confirm("Clear this skill's saved prediction, first try and later repairs?"))return;
      erase(lesson);states[lesson]=initState(lesson);render(lesson,true);return;
    }
    if(kind==="review-history") {
      const old=root.querySelector(".history");
      if(old){old.remove();return;}
      const panel=el("section","history");
      snapshot(panel,state,lessons[lesson]);
      const repair=el("section","snapshot");
      addText(repair,"strong",null,"Your separate repair");
      addText(repair,"p",null,state.repair||"(no repair written)");
      panel.append(repair);
      action.parentNode.before(panel);return;
    }
    if(kind==="save-prediction" && state.stage===0) {
      const prediction=root.querySelector("textarea").value.trim();
      if(!prediction){warn(root,"Write a prediction or 'I'm not sure' so you can compare it later.");return;}
      state.prediction=prediction;state.stage=1;state.predictionDraft="";
    } else if(kind==="lock-attempt" && state.stage===1 && !state.first) {
      const values=formValues(root);
      if(!values.reason){
        warn(root,"Write a few words explaining your thinking—or 'I'm not sure'. Then you can see the worked steps.");
        root.querySelector('[data-input="reason"]').focus();
        return;
      }
      state.first=values;state.stage=2;state.draft=null;
    } else if(kind==="save-reconstruction" && state.stage===2) {
      state.reconstruction=[...root.querySelectorAll("[data-rubric]:checked")].map(x=>Number(x.value));
      state.stage=3;
    } else if(kind==="save-diagnosis" && state.stage===3) {
      const data=formValues(root);
      state.diagnosis={issue:data.diagnosis||"I'm not sure what went wrong yet.",why:data[lesson+"-diagnosisWhy"]||""};
      state.stage=4;
    } else if(kind==="save-repair" && state.stage===4) {
      const data=formValues(root);
      const repaired=data[lesson+"-repair"]||"";
      if(!repaired){warn(root,"Write what you changed—or that you are still unsure.");return;}
      state.repair=repaired;state.stage=5;
    } else if(kind==="save-boundary" && state.stage===5 && state.boundary===null) {
      const answer=root.querySelector("textarea").value.trim();
      if(!answer){warn(root,"Write your idea or 'I'm not sure' before opening the boundary check.");return;}
      state.boundary=answer;
    } else return;
    const saved=persist(lesson,state);
    if(!saved)storageWorks=false;
    render(lesson,true);
  }
  // Drafts live only in this browser. Committed first responses remain separate
  // and cannot be replaced by editing a later repair.
  function saveUnfinishedInput(lesson,event){
    const state=states[lesson];
    if(state.stage===0 && event.target.matches("textarea")){
      state.predictionDraft=event.target.value;
    }else if(state.stage===1 && !state.first && event.target.matches("[data-input]")){
      const root=document.querySelector('[data-stage-root="'+lesson+'"]');
      state.draft=formValues(root);
    }else return;
    if(!persist(lesson,state))storageWorks=false;
  }
  const configHintCount=lesson=>(lessons[lesson].hints||[]).length;
  let sourceRoute=null;
  async function bindSourceJourney(){
    const sourceId=new URLSearchParams(location.search).get("question");
    const lesson=location.hash.replace(/^#/,"");
    if(!sourceId||!/^[-A-Za-z0-9]{2,64}$/.test(sourceId)||!Object.prototype.hasOwnProperty.call(lessons,lesson))return;
    try{
      const [routing,coverage,original]=await Promise.all([
        fetch("reasoning-paths.review.json",{cache:"no-store"}),
        fetch("learning-coverage-r1.json",{cache:"no-store"}),
        fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
      ]);
      if(!routing.ok||!coverage.ok||!original.ok)return;
      const d=await routing.json(),map=await coverage.json(),bank=await original.json();
      if(d.schema!=="wpe-reasoning-route-preview/v1"||!Array.isArray(d.constructions)||
         map.schema!=="wpe-learner-coverage-r1/v1"||map.questions?.length!==74||bank.questions?.length!==74)return;
      const item=map.questions.find(q=>q.source_id===sourceId);
      if(!item||!bank.questions.some(q=>q.source_id===sourceId&&q.stem_sha256===item.stem_sha256))return;
      const suggested=d.constructions.some(r=>r.id==="WPE-"+lesson&&r.proposed_source_ids?.some(q=>q.id===sourceId&&q.reader_present));
      const primary=item.primary_lesson===lesson&&item.fit!=="MISSING_CONSTRUCTION";
      if(!primary&&!suggested||location.hash.replace(/^#/,"")!==lesson)return;
      const href="../../preview/question-status.html?question="+encodeURIComponent(sourceId);
      sourceRoute={id:sourceId,lesson,href};
      const banner=document.getElementById("source-journey");
      document.getElementById("source-journey-title").textContent="Your original question: "+sourceId;
      document.getElementById("source-journey-message").textContent=sourceId==="EX-M79"
        ?"This lesson investigates constant power as a comparison. The original gives a speed–distance relationship: decide its own physical model when you return."
        :"Learn the method through a different situation, try the challenge, then return to your original question.";
      const link=document.getElementById("source-journey-return");link.href=href;link.textContent="Return to "+sourceId+" without showing its answer";
      banner.hidden=false;
      const footer=document.querySelector("#"+lesson+" .unit-next");
      if(footer){const a=el("a","return-original","↩ Solve "+sourceId+" yourself");a.href=href;footer.append(a);}
      const state=states[lesson];
      if(state.boundary!==null)render(lesson,false);
    }catch(_){/* No invented return link if the source manifest is unavailable. */}
  }
  let storageWorks=true;
  const states={};
  // Read every topic state before the first render updates the shared counter.
  Object.keys(lessons).forEach(lesson=>{states[lesson]=load(lesson);});
  Object.keys(lessons).forEach(lesson=>{
    const root=document.querySelector('[data-stage-root="'+lesson+'"]');
    if(root){root.addEventListener("click",event=>update(lesson,event));root.addEventListener("input",event=>saveUnfinishedInput(lesson,event));root.addEventListener("change",event=>saveUnfinishedInput(lesson,event));render(lesson,false);}
  });
  window.addEventListener("hashchange",()=>{
    sourceRoute=null;
    document.getElementById("source-journey").hidden=true;
    document.querySelectorAll(".unit-next .return-original").forEach(link=>link.remove());
    bindSourceJourney();
  });
  bindSourceJourney();
})();