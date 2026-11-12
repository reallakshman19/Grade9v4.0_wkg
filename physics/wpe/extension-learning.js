/* WPE E01-E05: distinct authored extensions, not original exam questions.
 * Core1A follows the existing WPE extension learning packs. The fresh
 * reconstruction is revealed only after a locally saved first attempt.
 * Browser storage is practice convenience, not secure assessment.
 */
(() => {
  "use strict";
  const lessons = {
    E01: {
      title:"Potential wells: possible versus reachable",
      question:"Can two low valleys be separated by a hill you cannot cross?",
      prereq:"A moving object's total energy E is potential U plus kinetic K. Because K = ½mv², K cannot be negative. At K = 0 it can momentarily turn.",
      core:"A place is energetically allowed when U(x) ≤ E. A journey is possible only if EVERY intermediate place along a continuous route is allowed.",
      guide:"A 2 kg bead slides on a smooth one-dimensional track with U(x) = (x − 2)² joules when x is in metres. Total energy is 4 J. The bowl has its lowest point at x = 2 m.",
      steps:[
        ["Read the potential map","At x = 0, 1, 2, 3, 4 m, the potential energies are 4, 1, 0, 1, 4 J. Draw a horizontal E = 4 J line."],
        ["Make a kinetic-energy budget","Subtract each U from 4 J: K = 0, 3, 4, 3, 0 J. Anything with U greater than 4 J would demand negative K and is forbidden."],
        ["Locate the turning positions","At x = 0 and 4 m, K = 0, so the bead may momentarily stop and reverse. The entire interval from 0 to 4 m is connected and accessible."],
        ["Locate the greatest speed","Smallest U means largest K. At x = 2 m, K = 4 J and v = √(2K/m) = √(8/2) = 2 m/s."],
        ["Change one condition","At E = 1 J, the line meets the bowl at x = 1 and 3 m, so the allowed interval becomes [1, 3] m. Moving the energy line changes what is possible."]
      ],
      contrast:"An isolated low destination is not automatically reachable: if a higher hill lies between it and the start, compare the entire route with E. The lowest point also need not be where the bead starts.",
      misconception:"K = 0 is allowed at a turning position; K less than 0 is not. Speed is fastest at LOWEST potential, not at the highest hill. Exactly at a stable minimum with E = Umin, the bead can remain at rest.",
      assumptions:"One-dimensional conservative motion, no friction, fixed total E, and a smooth track. At a barrier top where E exactly equals a local maximum, crossing requires special dynamical care. The fresh crossing check uses E greater than the barrier.",
      challenge:"A different 2 kg bead moves on a frictionless x-axis. Put q = x/(1 m), so q is dimensionless. Its potential energy is U(q) = (q² − 4)² J. It has E = 9 J, starts at x = +2 m moving LEFT, and can only travel along this axis. Can it get into the valley near −2 m? Find the allowed x intervals, the turning positions in its starting valley and its maximum possible speed.",
      fields:[
        {id:"cross",label:"Can it reach the valley near −2 m from +2 m?",type:"select",options:["Choose a prediction","Yes","No","Not sure"]},
        {id:"intervals",label:"Allowed x intervals (m)",type:"text",hint:"Write both intervals; you may use √ and brackets."},
        {id:"turns",label:"Turning positions of the starting (right) region",type:"text"},
        {id:"maxSpeed",label:"Largest speed possible on its journey (m/s)",type:"number"},
        {id:"reason",label:"Why is or isn't the whole journey possible?",type:"textarea"}
      ],
      hints:[
        "Use the budget K = E − U. What sign must K have at any physically visited position?",
        "Make a short U table at x = +2, +1, 0, −1, −2 m before solving a long inequality.",
        "Shade the x-axis wherever the budget is possible. Starting at +2 m, trace a continuous path without jumping over any untested location."
      ],
      worked:[
        ["Check positions","K ≥ 0 requires (q² − 4)² ≤ 9. Take the square-root inequality: −3 ≤ q² − 4 ≤ 3, hence 1 ≤ q² ≤ 7."],
        ["Separate intervals","The allowed x values are [−√7, −1] m and [1, √7] m. These are TWO disconnected regions."],
        ["Follow the actual start","At +2 m the bead occupies the right-hand region. Moving left, it turns at +1 m. The hill at 0 has U = 16 J, which exceeds its 9 J budget. The left valley is low but NOT reachable from that start."],
        ["Calculate maximum speed","At +2 m, U = 0, so its maximum accessible K = 9 J. For 2 kg, v = √(2 × 9/2) = 3 m/s. The right-hand turning points are +1 and +√7 m."]
      ],
      checks:["I tested E − U ≥ 0, including K = 0.","I separated the two allowed regions.","I traced the connected region containing the actual start.","I found fastest motion at the lowest accessible U."],
      diagnoses:["I checked only the far destination.","I forgot to inspect the hill between the valleys.","I treated K = 0 as forbidden.","I maximized speed at maximum U.","I need to revise my algebra or units.","My model worked; I want to explain it more clearly."],
      diagnosisTips:["Check ALL intermediate positions, not just the endpoint.","Mark the central potential and the energy line on one graph.","A turning position can have zero speed for an instant.","Subtract U from E before using ½mv².","Rewrite −3 ≤ q²−4 ≤ 3 and restore metres from q.","State a connected route explicitly even when the numbers agree."],
      boundary:"Raise total energy to 17 J, keeping the same potential and bead. Is crossing x = 0 now energetically possible? What is its speed at x = 0? Explain the changed condition.",
      boundaryCheck:"At x = 0, U = 16 J. With E = 17 J, K = 1 J and v = √(2 × 1/2) = 1 m/s. The barrier is below E, so crossing is energetically possible. E = 16 J exactly is a special separatrix, not a guaranteed ordinary crossing.",
      visual:"well"
    },
    E02: {
      title:"Instantaneous power: force along motion",
      question:"Why can a moving object have zero power at an instant?",
      prereq:"One watt is one joule per second. Work depends on the component of force along displacement; power describes the rate at this instant, not an entire future journey.",
      core:"Instantaneous power is force along the CURRENT velocity: P = Fx vx + Fy vy. A perpendicular force gives zero power even if it causes acceleration.",
      guide:"A 2 kg trolley moves RIGHT at 3 m/s. A student pulls RIGHT with 6 N while resistance acts LEFT with 2 N. The floor is level.",
      steps:[
        ["Draw direction arrows","Choose right as positive: v = +3 m/s, Fpull = +6 N, Fresist = −2 N. Gravity and the normal are vertical, perpendicular to horizontal motion."],
        ["Calculate each rate","Pull power = (+6)(+3) = +18 W. Resistance power = (−2)(+3) = −6 W. Gravity and the normal each contribute 0 W."],
        ["Combine contributions","Net power = +12 W. The kinetic energy is increasing at 12 J per second AT THIS INSTANT."],
        ["Do not invent a future average","As the trolley accelerates, v can change. Thus P = Fv can change even if the forces stay the same. Average power over a period is total work ÷ elapsed time."],
        ["Reverse velocity, not forces","If the trolley momentarily moves LEFT at 3 m/s under the same force arrows, net power is (6 − 2)(−3) = −12 W."]
      ],
      contrast:"A moving body does not always gain kinetic energy. Force and velocity can be opposite (negative power) or perpendicular (zero power). Force magnitude multiplied by speed only works when aligned.",
      misconception:"Do not confuse +12 W now with +12 J gained in every later second. Net power can be zero while net force and acceleration are nonzero.",
      assumptions:"For the guide, horizontal forces at an instant, level motion, no vertical velocity; same applied force arrows in the reversal comparison. Two-dimensional force components in the fresh problem are an ADVANCED bridge: multiply corresponding horizontal arrows and add the signed contributions—no calculus required.",
      challenge:"A robot moves on a flat floor with instantaneous velocity 3 m/s RIGHT and 4 m/s FORWARD. Its motor pushes 6 N RIGHT. Resistance pushes 2 N LEFT and 1 N BACKWARD. Vertical forces are perpendicular to motion. Find the instant motor, resistance and net powers; tell whether kinetic energy is rising or falling, and explain why multiplying full force magnitude by speed is wrong.",
      fields:[
        {id:"motor",label:"Motor instantaneous power (W)",type:"number"},
        {id:"resist",label:"Resistance instantaneous power (W)",type:"number"},
        {id:"net",label:"Net instantaneous power (W)",type:"number"},
        {id:"trend",label:"Kinetic energy is...",type:"select",options:["Choose","Increasing now","Decreasing now","Unchanging now","Not sure"]},
        {id:"reason",label:"Show signed right/forward contributions, not just the final number",type:"textarea"}
      ],
      hints:[
        "Draw separate rightward and forward velocity arrows. Which force arrows have components in each direction?",
        "Make a two-column table: multiply each force's RIGHT component by 3, and FORWARD component by 4.",
        "Keep signs on resistance terms. Add the two component products for each force before adding the motor and resistance."
      ],
      worked:[
        ["Motor","Motor force = (+6, 0) N; velocity = (+3, +4) m/s. Motor power = 6×3 + 0×4 = +18 W."],
        ["Resistance","Resistance = (−2, −1) N, so resistance power = −2×3 −1×4 = −10 W."],
        ["Net instantaneous result","Net force = (+4, −1) N. Pnet = 4×3 − 1×4 = +8 W; kinetic energy is currently increasing at 8 J/s."],
        ["Why magnitudes fail","Speed magnitude is 5 m/s and net force magnitude is √17 N. Their product is NOT 8 W, because the vectors are not parallel. Only the force component along velocity transfers kinetic energy at that instant."]
      ],
      checks:["I resolved force and velocity along the same axes.","I kept resistance terms negative.","I used Pnet as an instantaneous energy-change rate.","I distinguished component products from magnitude products."],
      diagnoses:["I ignored the backward resistance.","I multiplied magnitudes instead of matching components.","I gave resistance the wrong sign.","I claimed current power is future average power.","I need to check arithmetic.","I can explain perpendicular-force zero power better."],
      diagnosisTips:["The 4 m/s forward velocity multiplies the backward resistance.","Separate each axis before adding; vectors are not all parallel.","A force opposite to its velocity component does negative power.","An instantaneous rate need not remain constant over time.","Recheck 6×3 and (−2×3−1×4).","Perpendicular forces can bend a path without changing speed at that instant."],
      boundary:"At a later instant the robot moves 1 m/s RIGHT and 4 m/s FORWARD, under the SAME forces. Find net instantaneous power. Is the robot moving? Can acceleration still be nonzero?",
      boundaryCheck:"Pnet = 4×1 −1×4 = 0 W. Speed is √(1² + 4²) = √17 m/s, not zero. Net force (+4, −1) N is nonzero and perpendicular to velocity, so acceleration exists but kinetic energy is instantaneously unchanged.",
      visual:"power"
    },
    E03: {
      title:"Spring contact → projectile flight",
      question:"Exactly when do you stop using the spring model?",
      prereq:"A spring stores ½kx², because its force falls as it relaxes. A launched object has separate horizontal and vertical motion once contact ends.",
      core:"Divide the event into phases. During contact, stored spring energy pays for friction and launch kinetic energy. After contact ends, use gravity for vertical flight time and unchanged horizontal speed for range.",
      guide:"Model A: a 1 kg puck is NOT attached to an ideal spring (k = 100 N/m) compressed 0.20 m. The horizontal surface is smooth. Model B: a DIFFERENT ball leaves a platform 1.25 m high, horizontally at 3 m/s. Use g = 10 m/s².",
      steps:[
        ["Contact has a clear end","The free puck is pushed only until the spring reaches natural length. Initially stored energy = ½×100×(0.20)² = 2 J."],
        ["Convert before separating","In the frictionless guide, at natural length ½×1×v² = 2 J, so puck speed = 2 m/s. The spring cannot pull it once contact ends."],
        ["Start a separate projectile model","The second ball begins FLIGHT horizontally. Vertical initial velocity is 0; gravity makes it fall 1.25 = ½×10×t², giving t = 0.50 s."],
        ["Use horizontal motion for range","With no air drag, vx stays 3 m/s. Its horizontal range is 3×0.50 = 1.50 m. Falling faster vertically does not reduce its horizontal velocity."],
        ["Join only when a real launcher needs both","First compute a dart's speed at release using its contact ledger; then transfer that speed into the flight equations. Never carry the spring push into free flight."]
      ],
      contrast:"The spring's initial force kx is not constant throughout release: its work is the triangular area ½kx². Flight time comes from height, not from dividing height by g.",
      misconception:"Do not carry contact friction or spring force into the air. The projectile is free only once it has left all supports, with the specified horizontal launch position.",
      assumptions:"Ideal Hookean spring, the object is NOT attached, release occurs at natural length, and no losses except any explicitly stated contact friction. Launch horizontal; constant g; no air drag. In real apparatus the geometry may differ; the contact boundary must be specified.",
      challenge:"A 0.50 kg dart is pushed by a spring with k = 125 N/m compressed 0.20 m. The dart is not attached. While the spring expands those 0.20 m, constant opposing friction = 2.5 N. At natural length it leaves a 1.25 m-high platform HORIZONTALLY. Use g = 10 m/s²; no air drag or friction in flight. Find spring energy, contact friction work, launch speed, fall time and horizontal range.",
      fields:[
        {id:"energy",label:"Initially stored spring energy (J)",type:"number"},
        {id:"friction",label:"Work of contact friction (J; include sign)",type:"number"},
        {id:"speed",label:"Horizontal launch speed (m/s)",type:"number"},
        {id:"time",label:"Flight time (s)",type:"number"},
        {id:"range",label:"Horizontal landing distance (m)",type:"number"},
        {id:"reason",label:"Where is the phase boundary, and which forces disappear?",type:"textarea"}
      ],
      hints:[
        "Mark two columns: while TOUCHING the spring, and after the dart LEAVES the platform.",
        "Compute the energy budget at natural length. For friction, work = opposing force × contact distance, with the correct sign.",
        "From horizontal launch, start with vertical fall h = ½gt². Then use horizontal speed times that duration."
      ],
      worked:[
        ["Contact energy","Stored energy = ½×125×0.20² = 2.50 J. Friction does −2.5×0.20 = −0.50 J, leaving 2.00 J of kinetic energy."],
        ["Launch speed","½×0.50×v² = 2.00, so vx = √8 ≈ 2.828 m/s. The spring and rubbing contact both end at launch."],
        ["Fall time","In the air, vertical drop is 1.25 = ½×10×t², so t = 0.50 s. Initial vertical speed is zero."],
        ["Range and force change","Range = vx t ≈ 2.828×0.50 = 1.414 m. Only gravity acts (ignoring air resistance); neither spring force nor contact friction continues during flight."]
      ],
      checks:["I marked contact and flight as different phases.","I used ½kx², not the initial force over the whole stroke.","I subtracted friction only during contact.","I used vertical motion for time and horizontal motion for range."],
      diagnoses:["I treated spring force as constant.","I forgot contact friction or its sign.","I carried spring/friction into flight.","I used t = h/g.","I mixed horizontal and vertical components.","I want to improve my units or rounding."],
      diagnosisTips:["The Hookean force decreases to zero as the spring relaxes.","The energy lost is force × CONTACT distance, opposing motion.","Once the dart leaves the launcher, contact forces cease.","For a horizontal launch, start with h = ½gt².","Gravity changes vertical velocity, not horizontal velocity here.","Check joules, seconds, m/s and metres at each stage."],
      boundary:"Keep the same launcher and platform, but make friction during contact ZERO. Find the new launch speed and range. Does the fall time change?",
      boundaryCheck:"Without friction, kinetic energy at launch = 2.50 J. vx = √(2×2.50/0.50) = √10 ≈ 3.162 m/s. The fall time stays 0.50 s; range increases to ≈ 1.581 m.",
      visual:"spring"
    },
    E04: {
      title:"Dissipative bouncing: energy is not speed",
      question:"How do tiny repeated rebounds add to a finite distance?",
      prereq:"Ignoring air drag, gravitational energy mgh becomes kinetic energy on the fall. Kinetic energy is proportional to speed SQUARED, not speed.",
      core:"If a bounce retains fraction r of the kinetic energy, the next rebound height is r times the previous height, while rebound speed is √r times the incoming speed. Count UP and DOWN each time.",
      guide:"Drop a 1 kg ball from rest at 2 m, using g = 10 m/s². Each ideal floor impact loses 75% of the incoming kinetic energy, so the retained fraction r = 0.25. Ignore air resistance.",
      steps:[
        ["First drop","It falls 2 m once and reaches the floor with K = mgh = 1×10×2 = 20 J."],
        ["First rebound","It keeps 25% of 20 J = 5 J, enough to rise h1 = 5/(1×10) = 0.5 m."],
        ["Apply the same retention each time","Next rebound heights are 0.25×0.5 = 0.125 m and 0.25×0.125 = 0.03125 m. Do not apply the 75% LOSS as a height ratio."],
        ["Compare energy and speed","With 25% energy retention, speed immediately after impact is √0.25 = 0.5 times incoming speed, not 0.25 times."],
        ["Count both directions","Distance = first 2 m drop + 2(0.5 + 0.125 + …). Optional advanced geometric sum: D = 2 + 2×0.5/(1−0.25) = 10/3 m ≈ 3.333 m."]
      ],
      contrast:"Half of the speed does not mean half of the kinetic energy: it means one-quarter of the energy. Similarly, half-energy rebounds have speed ratio √0.5.",
      misconception:"Never count only the upward legs. Use the initial drop ONCE and each complete rebound twice. A real ball ultimately stops; the infinite sequence is an ideal mathematical model.",
      assumptions:"Vertical rebounds on a level floor, fixed kinetic-energy loss fraction at impact, no energy loss during flights, no sideways motion. Geometric infinite series is an ADVANCED extension; first three heights and paired up/down distances are the prerequisite bridge.",
      challenge:"Release a ball from 2 m. On its FIRST impact it retains 75% of its pre-impact kinetic energy. On every LATER impact it retains 50%. Find the first three rebound heights, ideal total vertical distance and ratio of rebound speed to incoming speed on the FIRST impact. Explain when the rule switches.",
      fields:[
        {id:"h1",label:"First rebound height (m)",type:"number"},
        {id:"h2",label:"Second rebound height (m)",type:"number"},
        {id:"h3",label:"Third rebound height (m)",type:"number"},
        {id:"distance",label:"Total ideal vertical travel (m)",type:"number"},
        {id:"speedRatio",label:"First post/pre impact speed magnitude ratio",type:"number"},
        {id:"reason",label:"Explain the two retention rules and both-direction distance count",type:"textarea"}
      ],
      hints:[
        "Write a row for every impact: which energy-retention fraction applies to THIS row?",
        "After a rebound, the ball rises to the height corresponding to its remaining energy. Check whether a SPEED ratio must involve a square root.",
        "The first 2 m drop happens only once; every rebound contributes an upward and a downward journey. What repeats after the first impact?"
      ],
      worked:[
        ["Switch rules carefully","At first impact r0 = 0.75, so h1 = 0.75×2 = 1.5 m. Later r = 0.50, so h2 = 0.75 m and h3 = 0.375 m."],
        ["Sum the repeated rises","After the first special bounce, heights halve: 1.5 + 0.75 + 0.375 + … = 1.5/(1−0.5) = 3 m (optional infinite-series maths)."],
        ["Include all travel","The initial fall is 2 m. Rebounds go UP and DOWN, so D = 2 + 2×3 = 8 m, in the ideal model."],
        ["Check rebound speed","The first retained energy fraction is 0.75; speed ratio is √0.75 = √3/2 ≈ 0.866. It is not 0.75."]
      ],
      checks:["I switched from first-impact to later-impact fraction.","I related height to energy, speed to √energy.","I included first drop and both legs of rebounds.","I recognized the infinite series as an ideal extension."],
      diagnoses:["I kept 75% for every bounce.","I treated energy fraction as speed fraction.","I missed the initial drop.","I counted only upward travel.","I used the wrong first term or ratio.","I need to explain the ideal-model limit."],
      diagnosisTips:["Label impact 1 separately and impacts 2,3,… as a repeating rule.","Use K = ½mv² to transform an energy ratio into a speed ratio.","The released ball travels from 2 m to floor before any rebound.","Each bounce rise is followed by a fall of the same height.","Begin the repeating height sequence with h1 and ratio 0.5.","The total is a mathematical limit, not a claim that real balls bounce forever."],
      boundary:"Change the model: EVERY impact now retains 75% energy, including the first. From the same 2 m height, what is ideal total vertical travel, and why is it larger?",
      boundaryCheck:"Rebound heights form 1.5, 1.125, … m with ratio 0.75. Their sum is 1.5/(1−0.75) = 6 m; ideal travel D = 2 + 2×6 = 14 m. More retained energy means taller subsequent rebounds.",
      visual:"bounce"
    },
    E05: {
      title:"Radial force: graph area versus circular orbit",
      question:"Why can an inward force give positive potential energy?",
      prereq:"For a 1D conservative force, its work along radial displacement is −ΔU. On a circle, velocity is tangent while inward force is perpendicular. A circle needs inward acceleration v²/r.",
      core:"Two DIFFERENT operations: radial force-magnitude graph AREA gives increase in U with outward radius; the force HEIGHT at an orbit radius gives mv²/r. Only then add K + U.",
      guide:"A 1 kg bead has a conservative central force of constant magnitude 3 N pointing INWARD at positive radius r. Choose U(0) = 0 by continuous limit. Consider a steady circular orbit of radius 2 m; ignore drag.",
      steps:[
        ["Label force sign and velocity","Take outward radius positive. The signed radial force is Fr = −3 N; velocity around the circle is tangential and perpendicular to it."],
        ["Imagine moving radially outward","Against inward force, U rises by +3 N × 2 m = +6 J. This is area under the POSITIVE inward-magnitude graph, not work done while circling."],
        ["Use force at the chosen radius","For circular motion at r = 2 m, inward force = mv²/r = 3 N. So v² = 3×2/1 = 6 and v ≈ 2.45 m/s."],
        ["Combine energy only after both models","K = ½×1×6 = 3 J. The total mechanical energy of this 2 m orbit is E = U + K = 6 + 3 = 9 J."],
        ["Check the circle itself","Because force is perpendicular to tangential velocity, it does zero work along the orbit. The 6 J is a radial-position comparison, not energy added every lap."]
      ],
      contrast:"If the graph's vertical axis shows signed Fr = −3 N, its radial area is negative WORK and ΔU is the opposite sign. If it shows positive inward magnitude f = 3 N, area is POSITIVE ΔU. Read the axis.",
      misconception:"Potential energy is not automatically negative because force points inward. Use graph AREA for potential CHANGE, but graph HEIGHT at the orbit radius for circular force. Never use mv/r.",
      assumptions:"Conservative radial force for r > 0, inward magnitude f(r) ≥ 0, U(0) as a continuous reference limit. The inward direction is undefined exactly at r = 0; circular orbits considered only at r > 0. Elementary graph area and v²/r replace calculus as an explicit ADVANCED bridge. Different radius circles have different total E and are separate states.",
      challenge:"A 2 kg spacecraft is in an ideal circular orbit at r = 3 m. The conservative INWARD FORCE MAGNITUDE is 4 N from r = 0 to 2 m, then grows linearly from 4 N at r = 2 m to 8 N at r = 4 m (thus 6 N at 3 m). With U(0) = 0, find U(3), speed, K and total E. Distinguish the two graph operations and explain why the force does no work along the orbit.",
      fields:[
        {id:"potential",label:"U(3 m), using both graph areas (J)",type:"number"},
        {id:"localForce",label:"Force magnitude at r = 3 m (N)",type:"number"},
        {id:"speed",label:"Circular orbital speed (m/s)",type:"number"},
        {id:"kinetic",label:"Circular kinetic energy (J)",type:"number"},
        {id:"total",label:"Total energy of this circular orbit (J)",type:"number"},
        {id:"reason",label:"Explain area versus force height, and the zero work around a circle",type:"textarea"}
      ],
      hints:[
        "On an inward FORCE MAGNITUDE versus radius graph, compare U between radii by counting the area underneath.",
        "Start at the U(0) reference. Split radial area into 0–2 m and 2–3 m; the second section slopes.",
        "For orbit speed, ignore earlier areas and read the FORCE at 3 m. Sketch perpendicular inward force and tangential velocity before using mv²/r."
      ],
      worked:[
        ["Build potential from radial areas","First rectangle: 4×2 = 8 J. Next trapezoid from 2 to 3 m: ½(4+6)×1 = 5 J. Thus U(3) = 8 + 5 = 13 J."],
        ["Read local force independently","At 3 m, inward f(3) = 6 N. The circle condition is mv²/r = 6, so 2v²/3 = 6 and v = 3 m/s."],
        ["Compute orbit energies","K = ½×2×3² = 9 J. Total energy E(3) = U(3) + K = 13 + 9 = 22 J."],
        ["Explain no circular work","While the craft circles at constant radius, its force is inward but velocity tangential. F · v = 0. The area was an imagined RADIAL comparison, not energy continuously produced during each orbit."]
      ],
      checks:["I used both radial graph areas with correct sign.","I used the local force, not area, in mv²/r.","I found speed, K and E of the given circle.","I kept radial comparison separate from travel around the circle."],
      diagnoses:["I counted only the last area section.","I treated force height as potential energy.","I used a rectangle instead of a trapezoid.","I gave U a negative sign automatically.","I used mv/r instead of mv²/r.","I confused radial work with circular work."],
      diagnosisTips:["Begin from the reference U(0), not merely the nearest graph corner.","Force is in newtons; potential energy is an area in newton-metres.","For a sloped straight line, use average endpoint height × width.","On a positive inward-magnitude graph, outward U increases.","Inward acceleration for circular motion is v²/r.","Compare radial positions for ΔU; while circling, force is perpendicular to motion."],
      boundary:"Consider a DIFFERENT steady circle at r = 4 m, with the same force law and mass. Compute U(4), speed, K and total E(4). Why is this not the same spacecraft moving freely from the 3 m circle without extra energy?",
      boundaryCheck:"U(4) = 4×2 + ½(4+8)×2 = 8 + 12 = 20 J. Local force 8 N gives 2v²/4 = 8, so v = 4 m/s. K = ½×2×16 = 16 J and E(4) = 36 J. These are distinct circular-orbit states; the conservative force alone cannot change E from 22 to 36 J.",
      visual:"radial"
    }
  };
  const allIds = Object.keys(lessons);
  const stageNames = ["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
  const storagePrefix = "g9:wpe:extensions:v1:";
  const ns = "http://www.w3.org/2000/svg";
  const $ = (selector,scope=document) => scope.querySelector(selector);
  const node = (tag,cls,text) => {
    const element = document.createElement(tag);
    if(cls)element.className=cls;
    if(text!==undefined)element.textContent=text;
    return element;
  };
  const add = (parent,tag,cls,text) => {const e=node(tag,cls,text);parent.append(e);return e;};
  const svgNode = (parent,tag,attrs,text) => {
    const e=document.createElementNS(ns,tag);
    for(const [k,v] of Object.entries(attrs||{}))e.setAttribute(k,String(v));
    if(text!==undefined)e.textContent=text;
    parent.append(e);return e;
  };
  const key=id=>storagePrefix+id;
  const blank=id=>({schema:1,id,stage:0,prediction:"",predictionDraft:"",attemptDraft:{},first:null,hintsUsed:0,checks:[],diagnosis:null,repair:"",boundary:null});
  const states={};
  const persist=id=>{try{localStorage.setItem(key(id),JSON.stringify(states[id]));return true}catch(e){$("#save-notice").hidden=false;return false;}};
  for(const id of allIds){
    let s;
    try{s=JSON.parse(localStorage.getItem(key(id))||"null")}catch(_){}
    states[id]=(s && s.schema===1 && s.id===id && Number.isInteger(s.stage) && s.stage>=0 && s.stage<=5 && (s.stage<2 || (s.first && typeof s.first.reason==="string"))) ? s : blank(id);
  }
  let active="E01";
  let sourceLink=null;
  function button(parent,action,label,secondary=false){
    const e=add(parent,"button",secondary?"secondary":"primary",label);e.type="button";e.dataset.action=action;return e;
  }
  function list(parent,tag,items){
    const root=add(parent,tag);
    for(const item of items)add(root,"li",null,item);
    return root;
  }
  function paragraph(parent,text,cls){return add(parent,"p",cls||null,text);}
  function inputFor(parent,id,field,value){
    const wrap=add(parent,"div","field");
    const label=add(wrap,"label",null,field.label);
    const full=id+"-"+field.id;
    label.htmlFor=full;
    let e;
    if(field.type==="textarea"){e=add(wrap,"textarea");e.rows=4;}
    else if(field.type==="select"){
      e=add(wrap,"select");
      for(const choice of field.options){const opt=add(e,"option",null,choice);opt.value=choice;}
    }else{e=add(wrap,"input");e.type=field.type;e.inputMode=field.type==="number"?"decimal":"text";}
    e.id=full;e.dataset.field=field.id;e.value=value==null?"":value;
    if(field.hint)paragraph(wrap,field.hint,"field-tip");
    return e;
  }
  function stageSteps(host,state){
    const ol=add(host,"ol","step-list");
    stageNames.forEach((s,i)=>{
      const li=add(ol,"li",i===state.stage?"current":i<state.stage?"done":"pending",(i+1)+". "+s);
      if(i===state.stage)li.setAttribute("aria-current","step");
    });
  }
  function snapshot(host,s){
    const section=add(host,"section","snapshot");
    add(section,"h4",null,"Your first attempt (never overwritten by repair)");
    if(!s.first){paragraph(section,"No first attempt has been saved yet.");return}
    const dl=add(section,"dl");
    for(const [key,value] of Object.entries(s.first)){add(dl,"dt",null,key==="reason"?"Your explanation":key);add(dl,"dd",null,String(value));}
    paragraph(section,"Prediction: "+s.prediction);
  }
  function buildGuide(host,id,config){
    const guide=add(host,"section","guide");
    add(guide,"p","mini","CORE1A · Learn first");
    add(guide,"h2",null,"Build the physics idea");
    paragraph(guide,config.prereq,"prereq");
    paragraph(guide,config.core,"big-idea");
    paragraph(guide,config.guide);
    const chart=add(guide,"figure","visual");
    const svg=svgNode(chart,"svg",{viewBox:"0 0 640 290",role:"img","aria-label":id+" interactive physical model"});
    svg.id="guide-plot";
    add(chart,"figcaption",null,"Change the control. Watch what the model predicts, not just the numbers.");
    const controls=add(guide,"div","visual-controls");
    add(controls,"label",null,id==="E01"?"Total energy in the bowl (J)":id==="E02"?"Trolley velocity (m/s)":id==="E03"?"Contact friction (N)":id==="E04"?"Energy fraction retained": "Circular orbit radius (m)").htmlFor="guide-slider";
    const slider=add(controls,"input");slider.id="guide-slider";slider.type="range";
    const settings={E01:[0,6,1,4],E02:[-3,3,1,3],E03:[0,5,0.5,0],E04:[0.1,0.75,0.05,0.25],E05:[1,4,0.5,2]}[id];
    [slider.min,slider.max,slider.step,slider.value]=settings.map(String);
    const readout=add(controls,"output","model-readout");readout.htmlFor="guide-slider";
    slider.addEventListener("input",()=>drawVisual(id,Number(slider.value),svg,readout));
    drawVisual(id,Number(slider.value),svg,readout);
    const ol=add(guide,"ol","guide-steps");
    for(const [title,desc] of config.steps){
      const li=add(ol,"li");
      add(li,"strong",null,title+". ");
      li.append(document.createTextNode(desc));
    }
    const more=add(guide,"details","bridge");
    add(more,"summary",null,"Compare the common wrong model");
    paragraph(more,config.contrast);
    paragraph(more,config.misconception);
    const conditions=add(guide,"details","bridge");
    add(conditions,"summary",null,"Assumptions and advanced-maths bridge");
    paragraph(conditions,config.assumptions);
  }
  const nice=n=>Number(n.toFixed(3)).toString();
  function drawVisual(id,value,svg,out){
    svg.replaceChildren();
    const path=(d,color,width=3,dash)=>svgNode(svg,"path",{d,fill:"none",stroke:color,"stroke-width":width,...(dash?{"stroke-dasharray":dash}:{})});
    const textAt=(x,y,t,fill="#183e50",size=15)=>svgNode(svg,"text",{x,y,fill,"font-size":size,"font-weight":"600"},t);
    const line=(x1,y1,x2,y2,c="#7595a5",w=2)=>svgNode(svg,"line",{x1,y1,x2,y2,stroke:c,"stroke-width":w});
    svgNode(svg,"rect",{x:0,y:0,width:640,height:290,fill:"#f5fafc",rx:12});
    if(id==="E01"){
      const X=x=>55+x*132, Y=u=>240-u*28;
      line(55,240,595,240);line(55,240,55,30);
      for(let x=0;x<=4;x++)textAt(X(x)-5,264,x+"",null,13);
      for(let u=0;u<=6;u+=2)textAt(14,Y(u)+5,u+" J",null,12);
      let curve="";for(let i=0;i<=100;i++){const x=4*i/100;curve+=(i?" L":"M")+X(x).toFixed(1)+" "+Y((x-2)**2).toFixed(1);}
      path(curve,"#156c7d",4);
      line(55,Y(value),595,Y(value),"#ca7134",3);
      textAt(390,Math.max(27,Y(value)-12),"E = "+nice(value)+" J","#a95521");
      const r=Math.sqrt(value),a=Math.max(0,2-r),b=Math.min(4,2+r);
      svgNode(svg,"rect",{x:X(a),y:244,width:Math.max(0,X(b)-X(a)),height:8,fill:"#138578"});
      textAt(165,25,"U(x) = (x − 2)² J");
      out.textContent="Allowed positions on this 0–4 m view: "+nice(a)+" to "+nice(b)+" m. Turning points touch U = E; where U > E, K would be negative.";
    }else if(id==="E02"){
      line(70,195,560,195,"#8ba7af",4);
      svgNode(svg,"rect",{x:265,y:147,width:120,height:48,rx:8,fill:"#bde1e9",stroke:"#347a90"});
      textAt(285,177,"TROLLEY");
      line(330,138,470,138,"#158977",5);textAt(391,123,"pull +6 N","#147b70");
      line(320,213,205,213,"#ba683a",5);textAt(120,236,"resistance −2 N","#995c36");
      if(value!==0){const end=325+value*45;line(325,74,end,74,"#414d99",5);textAt(244,55,"v = "+value+" m/s","#414d99");}
      else textAt(195,72,"momentarily v = 0","#414d99");
      out.textContent="Power now: pull "+nice(6*value)+" W; resistance "+nice(-2*value)+" W; NET "+nice(4*value)+" W. Instantaneous—not an average.";
    }else if(id==="E03"){
      line(55,180,590,180,"#7b9ba9",3);
      const pts=[[72,140],[88,120],[104,160],[120,120],[136,160],[152,140]];
      svgNode(svg,"polyline",{points:pts.map(p=>p.join(",")).join(" "),fill:"none",stroke:"#bf8052","stroke-width":5});
      svgNode(svg,"rect",{x:185,y:132,width:46,height:46,rx:5,fill:"#8ed0d2",stroke:"#367783"});
      line(238,110,295,110,"#18897d",4);
      line(308,95,308,190,"#b56d4d",2);
      textAt(75,45,"SPRING CONTACT");textAt(375,45,"NO SPRING FORCE");
      textAt(235,218,"Natural length / separation boundary",null,14);
      const k=2-0.2*value,v=Math.sqrt(2*k);
      out.textContent="Guide puck: spring 2.00 J; friction work −"+nice(0.2*value)+" J; launch K "+nice(k)+" J; speed "+nice(v)+" m/s. Flight model B uses a different ball.";
    }else if(id==="E04"){
      line(32,252,612,252,"#688d9c",4);
      const peaks=[2,2*value,2*value**2,2*value**3];
      const heights=peaks.map(h=>h*88);
      for(let i=0;i<4;i++){
        const x=52+i*145;
        line(x,252,x,252-heights[i],"#a3c9cb",2);
        svgNode(svg,"circle",{cx:x,cy:252-heights[i],r:8,fill:i?"#278b7e":"#b8773f"});
        textAt(Math.max(2,x-24),Math.max(20,241-heights[i]),nice(peaks[i])+" m",null,12);
      }
      textAt(60,24,"Initial drop → rebound 1 → 2 → 3");
      out.textContent="r="+nice(value)+"; heights "+peaks.slice(1).map(nice).join(", ")+" m. Speed fraction √r="+nice(Math.sqrt(value))+". Ideal full travel "+nice(2+4*value/(1-value))+" m (advanced sum).";
    }else if(id==="E05"){
      // Left: force-magnitude area; right: orbit with radial/tangential arrows.
      line(48,224,310,224);line(48,224,48,45);
      svgNode(svg,"rect",{x:49,y:120,width:55*value,height:103,fill:"#b9e8d7",stroke:"#238e75","stroke-width":2});
      line(48,120,295,120,"#157c81",4);
      textAt(56,42,"Inward magnitude f = 3 N",null,14);
      textAt(58,255,"r outward → (m)",null,13);
      textAt(53,110,"3 N",null,12);
      const cx=465,cy=160,rad=44+value*14;
      svgNode(svg,"circle",{cx,cy,r:rad,fill:"none",stroke:"#92b4bf","stroke-width":2});
      svgNode(svg,"circle",{cx,cy,r:8,fill:"#536e7c"});
      svgNode(svg,"circle",{cx:cx+rad,cy,r:9,fill:"#1d8c80"});
      line(cx+rad-7,cy,cx+rad-45,cy,"#bc6d35",4);
      line(cx+rad,cy,cx+rad,cy-64,"#495fc0",4);
      textAt(365,25,"Orbit at r = "+nice(value)+" m",null,14);
      textAt(480,105,"v tangent", "#465cb1",12);
      textAt(392,194,"F inward","#a85d2c",12);
      out.textContent="Area gives U("+nice(value)+") = "+nice(3*value)+" J. Local force 3 N sets v = "+nice(Math.sqrt(3*value))+" m/s for 1 kg. Circular K = "+nice(1.5*value)+" J; force does zero work around the circle.";
    }
  }
  function renderStage(host,id,config){
    host.replaceChildren();
    const s=states[id];
    stageSteps(host,s);
    const stage=add(host,"section","stage-card");
    const heading=add(stage,"h3",null,(s.stage+1)+". "+stageNames[s.stage]);
    heading.tabIndex=-1;
    const controls=add(stage,"div","stage-actions");
    const notice=add(host,"p","status");notice.id="stage-status";notice.setAttribute("aria-live","polite");
    if(s.stage===0){
      paragraph(stage,"Make your own prediction before the calculation. 'Not sure yet' is allowed.");
      inputFor(stage,id,{id:"prediction",label:config.question,type:"textarea"},s.predictionDraft);
      button(controls,"save-prediction","Save prediction → Attempt");
    }
    if(s.stage===1){
      paragraph(stage,config.challenge,"challenge-prompt");
      paragraph(stage,"Show a model, not only numbers. Your original words and entries will be frozen when you choose 'Save first attempt'.","step-note");
      for(const field of config.fields)inputFor(stage,id,field,s.attemptDraft?.[field.id]);
      const hint=add(stage,"section","hints");
      add(hint,"h4",null,"Optional progressive help · no worked answer");
      const hintList=add(hint,"ol","hint-list");
      for(let i=0;i<Math.min(s.hintsUsed,config.hints.length);i++)add(hintList,"li",null,config.hints[i]);
      const hintButton=button(hint,"hint","Show next study cue ("+s.hintsUsed+"/"+config.hints.length+")",true);
      hintButton.disabled=s.hintsUsed>=config.hints.length;
      button(controls,"save-attempt","Save first attempt → Reconstruct");
    }
    if(s.stage===2){
      paragraph(stage,"Your first model has been saved. Compare it with the worked route; then check your steps.");
      snapshot(stage,s);
      const worked=add(stage,"section","worked");add(worked,"h4",null,"Worked reconstruction (now unlocked)");
      const ol=add(worked,"ol");for(const [heading,desc] of config.worked){const li=add(ol,"li");add(li,"strong",null,heading+". ");li.append(document.createTextNode(desc));}
      const checks=add(stage,"fieldset","self-check");
      add(checks,"legend",null,"Check what your reasoning included");
      config.checks.forEach((label,i)=>{
        const l=add(checks,"label");const c=add(l,"input");c.type="checkbox";c.value=String(i);c.dataset.check="true";c.checked=(s.checks||[]).includes(i);
        l.append(document.createTextNode(" "+label));
      });
      button(controls,"save-check","Compare → Diagnose");
    }
    if(s.stage===3){
      paragraph(stage,"Which idea will you fix first? A mistake is useful information.");
      const sel=add(stage,"select");sel.dataset.diagnosis="true";
      add(sel,"option",null,"Select a possible cause").value="";
      config.diagnoses.forEach((opt,i)=>{add(sel,"option",null,opt).value=String(i);});
      if(s.diagnosis)sel.value=String(s.diagnosis.index);
      inputFor(stage,id,{id:"why",label:"What clue tells you this was the first wrong step?",type:"textarea"},s.diagnosis?.why||"");
      button(controls,"save-diagnosis","Save diagnosis → Repair");
    }
    if(s.stage===4){
      paragraph(stage,"Use the clue, then rewrite your reasoning WITHOUT changing your original attempt.");
      const tip=add(stage,"p","diagnosis-tip",config.diagnosisTips[s.diagnosis?.index??0]);
      snapshot(stage,s);
      inputFor(stage,id,{id:"repair",label:"My repaired model and reason for the change",type:"textarea"},s.repair||"");
      button(controls,"save-repair","Save repair → Boundary test");
      const details=add(stage,"details","review-model");add(details,"summary",null,"Review previous worked model (optional)");
      for(const [head,desc] of config.worked)paragraph(details,head+": "+desc);
    }
    if(s.stage===5){
      paragraph(stage,"Change ONE condition and make a fresh prediction before opening its check:");
      paragraph(stage,config.boundary,"challenge-prompt");
      snapshot(stage,s);
      paragraph(stage,"My repair: "+s.repair,"repair-record");
      if(s.boundary===null){
        inputFor(stage,id,{id:"boundary",label:"My changed-condition prediction, working and explanation",type:"textarea"},"");
        button(controls,"save-boundary","Save boundary attempt → Open check");
      }else{
        paragraph(stage,"Your saved changed-condition attempt: "+s.boundary,"step-note");
        const check=add(stage,"section","worked");add(check,"h4",null,"Changed-condition check (now unlocked)");
        paragraph(check,config.boundaryCheck);
        const history=button(controls,"history","Review my first attempt and repair",true);
        history.setAttribute("aria-expanded","false");
        const done=add(stage,"p","done","Finished the six stages. Return to your original question and solve it using your own model.");
        if(sourceLink){const link=add(done,"a","return-original"," Return to "+sourceLink.id+" without revealing its answer");link.href=sourceLink.href;}
      }
    }
    const reset=button(controls,"reset","Start again (clears this lesson)",true);reset.classList.add("reset");
    stage.append(controls);
    heading.focus({preventScroll:true});
  }
  function readFields(host){
    const out={};host.querySelectorAll("[data-field]").forEach(e=>out[e.dataset.field]=e.value);return out;
  }
  function dispatch(host,id,config,event){
    const target=event.target.closest("button[data-action]");
    if(!target||!host.contains(target))return;
    const s=states[id],action=target.dataset.action;
    const warn=t=>$("#stage-status").textContent=t;
    if(action==="reset"){
      if(!window.confirm("Clear this lesson's prediction, first attempt, hints and repair?"))return;
      try{localStorage.removeItem(key(id))}catch(_){}
      states[id]=blank(id);render();return;
    }
    if(action==="hint"&&s.stage===1&&s.first===null){
      s.hintsUsed=Math.min(config.hints.length,s.hintsUsed+1);
      persist(id);renderStage(host,id,config);return;
    }
    if(action==="history"&&s.stage===5&&s.boundary!==null){
      const old=$(".history",host);
      if(old){old.remove();target.setAttribute("aria-expanded","false");return;}
      const history=add(host,"section","history");snapshot(history,s);
      paragraph(history,"Repaired model: "+s.repair);target.setAttribute("aria-expanded","true");return;
    }
    if(action==="save-prediction"&&s.stage===0){
      const v=$('[data-field="prediction"]',host).value.trim();
      if(!v){warn("Write a prediction, or 'Not sure yet', before continuing.");return;}
      s.prediction=v;s.predictionDraft="";s.stage=1;
    }else if(action==="save-attempt"&&s.stage===1&&s.first===null){
      const values=readFields(host);
      if(!values.reason?.trim()){warn("Write your reasoning (or 'Not sure yet') before seeing the worked reconstruction.");$('[data-field="reason"]',host).focus();return;}
      s.first={...values};s.attemptDraft={};s.stage=2;
    }else if(action==="save-check"&&s.stage===2){
      s.checks=[...host.querySelectorAll("[data-check]:checked")].map(e=>Number(e.value));s.stage=3;
    }else if(action==="save-diagnosis"&&s.stage===3){
      const val=$("[data-diagnosis]",host).value;
      if(val===""){warn("Choose one cause to investigate first.");return;}
      s.diagnosis={index:Number(val),why:$('[data-field="why"]',host).value.trim()};s.stage=4;
    }else if(action==="save-repair"&&s.stage===4){
      const val=$('[data-field="repair"]',host).value.trim();
      if(!val){warn("Explain what you repaired—or why you are still unsure.");return;}
      s.repair=val;s.stage=5;
    }else if(action==="save-boundary"&&s.stage===5&&s.boundary===null){
      const val=$('[data-field="boundary"]',host).value.trim();
      if(!val){warn("Attempt the changed condition before seeing its check.");return;}
      s.boundary=val;
    }else{return;}
    persist(id);render();
  }
  function updateProgress(){
    const completed=allIds.filter(id=>states[id].boundary!==null).length;
    $("#extension-progress").textContent=completed+" of 5 boundary challenges completed";
    $("#extension-meter").max=5;$("#extension-meter").value=completed;
    for(const id of allIds){const link=$('[data-lesson-link="'+id+'"]');if(link){link.classList.toggle("complete",states[id].boundary!==null);link.setAttribute("aria-current",id===active?"page":"false");}}
  }
  function render(){
    const hash=location.hash.slice(1).toUpperCase();
    if(allIds.includes(hash))active=hash;
    else if(!location.hash)active="E01";
    const config=lessons[active];
    $("#current-title").textContent=active+" · "+config.title;
    const host=$("#lesson-surface");host.replaceChildren();
    const article=add(host,"article","lesson");article.id=active;
    const header=add(article,"header","lesson-title");
    add(header,"p","mini","WPE "+active+" · Existing extension learning pack");
    add(header,"h2",null,config.title);
    paragraph(header,config.question);
    const pair=add(article,"div","learning-grid");
    buildGuide(pair,active,config);
    const challenge=add(pair,"section","challenge");
    add(challenge,"p","mini","CORE1B · A different challenge");
    add(challenge,"h2",null,"Predict → Attempt → Reconstruct");
    paragraph(challenge,"The challenge changes the setting. Think first, then use optional help. Your first model remains separate from any later repair.");
    const root=add(challenge,"div","stage-root");root.dataset.stageRoot=active;
    root.addEventListener("click",e=>dispatch(root,active,config,e));
    root.addEventListener("input",()=>{
      const s=states[active];
      if(s.stage===0)s.predictionDraft=$('[data-field="prediction"]',root)?.value||"";
      if(s.stage===1&&s.first===null)s.attemptDraft=readFields(root);
      if(s.stage===0 || s.stage===1)persist(active);
    });
    renderStage(root,active,config);
    const footer=add(article,"nav","lesson-footer");
    footer.setAttribute("aria-label","Learning navigation");
    const i=allIds.indexOf(active);
    const prev=add(footer,"a",null,i===0?"WPE chapter":"← Previous extension");prev.href=i===0?"index.html":"#"+allIds[i-1];
    const next=add(footer,"a",null,i===4?"Back to extensions start":"Next extension →");next.href="#"+allIds[(i+1)%5];
    if(sourceLink && sourceLink.lesson===active){const ret=add(footer,"a","return-original","Return to "+sourceLink.id+" without showing answer");ret.href=sourceLink.href;}
    updateProgress();
  }
  async function routeSource(){
    const sourceId=new URLSearchParams(location.search).get("question");
    if(!sourceId)return;
    const banner=$("#source-journey"),info=$("#source-message"),link=$("#source-return");
    if(!/^[A-Za-z0-9-]{2,64}$/.test(sourceId)){banner.hidden=false;info.textContent="Invalid source question identifier. No original question link was created.";return;}
    try{
      const [res,cov,bankRes]=await Promise.all([
        fetch("reasoning-paths.review.json",{cache:"no-store"}),
        fetch("learning-coverage-r1.json",{cache:"no-store"}),
        fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
      ]);
      if(!res.ok||!cov.ok||!bankRes.ok)throw Error("No source verification");
      const manifest=await res.json(),map=await cov.json(),bank=await bankRes.json();
      if(manifest.schema!=="wpe-reasoning-route-preview/v1"||manifest.policy!=="REVIEW_NAVIGATION_ONLY__NOT_CANONICAL_PREREQUISITE"||
         !Array.isArray(manifest.constructions)||map.schema!=="wpe-learner-coverage-r1/v1"||
         map.questions?.length!==74||bank.questions?.length!==74)throw Error("Invalid source inventory");
      const matched=map.questions.find(x=>x.source_id===sourceId);
      if(!matched||!bank.questions.some(x=>x.source_id===sourceId&&x.stem_sha256===matched.stem_sha256))throw Error("Unverified question ID");
      const proposed=manifest.constructions.some(row=>row.id==="WPE-"+active&&row.proposed_source_ids?.some(x=>x.id===sourceId&&x.reader_present));
      const primary=matched.primary_lesson===active&&matched.fit!=="MISSING_CONSTRUCTION";
      if(!primary&&!proposed)throw Error("Unmapped source/lesson pair");
      sourceLink={id:sourceId,lesson:active,href:"../../preview/question-status.html?question="+encodeURIComponent(sourceId)};
      banner.hidden=false;
      $("#source-title").textContent="Your original Question Bank entry: "+sourceId;
      info.textContent="Work through this different problem, then return to "+sourceId+" to make your own attempt. This is suggested practice, not an exam answer.";
      link.hidden=false;link.href=sourceLink.href;link.textContent="Return to "+sourceId+" without showing its answer";
      render();
    }catch(_){banner.hidden=false;info.textContent="This source ID is not mapped to the selected extension. No original question link is inferred.";link.hidden=true;}
  }
  allIds.forEach((id,i)=>{
    const nav=$("#extension-navigation");
    const a=add(nav,"a",null,(i+1)+". "+lessons[id].title);
    a.href="#"+id;a.dataset.lessonLink=id;
  });
  window.addEventListener("hashchange",()=>{sourceLink=null;$("#source-journey").hidden=true;render();routeSource();});
  render();
  routeSource();
})();
