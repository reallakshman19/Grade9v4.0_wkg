/* R5 C05 graph reasoning candidate signatures; NOT verified original exam plots.
 * Reuses merged gap-six-stage-engine.js, writes separate A/B attempt records,
 * leaves selected bank, source hashes, classifications, and all gateways alone.
 */
(() => {
"use strict";
const pick=(id,label,expected,wrong,mistake,kind="MODEL_CHOICE")=>({id,label,type:"select",choices:["Choose an idea",expected,...wrong,"I'm not sure yet"],expected,mistake,errorKind:kind});
const num=(id,label,expected,tol,mistake,kind="CALCULATION_OR_UNITS")=>({id,label,type:"number",expected,tol,mistake,errorKind:kind});
const reason=(label="Explain your physical law, axes, sign, units and the assumption that makes the operation valid")=>({id:"reason",label,type:"textarea"});
const why=(label="Explain the changed-condition model before reading its worked check")=>({id:"why",label,type:"textarea"});
const task=o=>({prediction:o.prediction,challenge:o.challenge,
 fields:[o.model,o.assumption,...o.numbers,reason(o.reason)],
 hints:o.hints,worked:o.worked,boundary:o.boundary,
 boundaryFields:[o.boundaryModel,...(o.boundaryNumbers||[]),why(o.boundaryWhy)],
 boundaryCheck:o.boundaryCheck});
const frame=(x,lo,hi,a,b)=>a+(x-lo)*(b-a)/(hi-lo);
const round=x=>Math.round(x*1000)/1000;

const G5U={
 source:"EX-M11",title:"A potential-energy curve is a force-sign and steepness map",short:"U(x) segments → signed force and |slope|",
 question:"Do the signs of potential-energy slopes change the RANKING of force magnitudes?",
 sourceCaution:"The available EX-M11 SVG is a smooth curve labeled stable/unstable, not a verified reproduction of the source's A–E four straight-segment plot. Its coaching slope coordinates (and option A) cannot be authenticated from this SVG. All R5 graphs here are deliberately NEW and explicitly labeled examples, never reconstructions of the original exam graph.",
 prerequisites:"For a 1D conservative force, F_x=−dU/dx; with U in J and x in m the slope has J/m=N. On a straight segment between two measured vertices the slope is ΔU/Δx; force has the opposite SIGN, while magnitude |F| uses ABSOLUTE slope. At a sharp corner a single derivative is undefined without a physical smoothing model.",
 core:"Choose axes before computing: U(x) graph means NEGATIVE SLOPE is force, whereas F(x) graph means SIGNED AREA is work. For piecewise-linear U, calculate every interior segment separately, convert units, then rank ABSOLUTE slopes. A horizontal U segment gives F=0, not the greatest force. An x axis in millimetres rather than metres changes conversion to newtons.",
 guide:"GUIDED EXAMPLE (not an original exam graph): a linear magnetic-trap potential has invented vertices (x m,U J) A(0,0), B(1,6), C(3,2), D(5,2), E(7,8). Its signed slopes are +6, −2, 0, +3 J/m. Thus forces are −6, +2, 0, −3 N and magnitude ranking AB>DE>BC>CD.",
 guideSteps:[
  ["Confirm which axes are displayed","Horizontal x (m), vertical potential U (J). The line SLOPE is J/m, not energy or work."],
  ["Read adjacent vertices; do not average across corners","AB ΔU/Δx=+6, BC=(2−6)/(3−1)=−2, CD=0, DE=(8−2)/(7−5)=+3 J/m."],
  ["Recover force DIRECTION","F=−dU/dx, so AB −6N, BC +2N, CD 0N, DE −3N. An increasing U pulls toward decreasing x."],
  ["Rank magnitude, not signed force","Take |F| for each interior segment: 6,2,0,3 N. Therefore AB>DE>BC>CD."],
  ["Ask where the rule is valid","At A/B/C/D/E corners the ideal piecewise graph has left/right slope disagreement; no unique instantaneous force at the corner is asserted."]
 ],
 wrong:"Wrong operator: using the signed slope itself as force, or ranking negative force values rather than absolute magnitudes; using area below U(x) would have units J·m, not N.",
 conditions:"1D position-dependent conservative field and an explicitly piecewise-linear potential; segment interiors have defined constant slopes. The provided guide graph is synthetic and uses SI x metres and U joules.",
 academic:{decision:"First check vertical U versus horizontal x. Negative slope gives SIGNED F; absolute slope gives force magnitude; never take area under U(x) as work.",
 observe:"Select a segment in the new guide's piecewise U(x) graph. The colored segment and its signed slope show that a large negative slope means large positive force, not weak force.",
 validity:"Conservative position field, known x and U units, interior of straight segments. At corners the derivative can be discontinuous or undefined.",
 limit:"A flat U interval gives zero force; a negative slope gives positive F; if the horizontal units shrink from m to 0.1m per tick, force magnitudes grow 10 times.",
 sourceBoundary:"Original EX-M11 author SVG and written step vertices disagree. No original exam force ranking or official answer is asserted from the available picture."},
 slider:{label:"Synthetic U(x): selected straight segment A–B, B–C, C–D, D–E",min:0,max:3,step:1,value:1},
 ...task({
  prediction:"If U rises with increasing x, which direction is the conservative force? Can the most negative signed force still have the LARGEST magnitude?",
  challenge:"TASK A · An ion trap has a NEW explicit piecewise potential (x in METRES, U in JOULES): A(0,0), B(2,10), C(5,4), D(7,4), E(8,7). On each open straight segment, rank |F| from greatest to least. Give signed F along BC and DE. These invented points are NOT the EX-M11 source graph.",
  model:pick("model","Which operation ranks force MAGNITUDES on U(x)?","Rank absolute values of each segment's negative slope",["Rank potential heights at the vertices","Take the signed area underneath U(x)"],"Conservative force is the negative derivative. Take |F| only after computing its sign."),
  assumption:pick("assumption","Where is each force value defined in this ideal graph?","Inside a linear segment, excluding unspecified sharp corners",["At every sharp corner a unique two-sided derivative is automatic","Force magnitudes depend only on vertical heights without Δx"],"Left and right slopes differ at corners; force there requires additional smoothness or a one-sided definition.","INVALID_ASSUMPTION"),
  numbers:[
   num("bc","SIGNED force on BC (N)",2,.08,"BC slope=(4−10)/(5−2)=−2 J/m, hence F=+2N.","SLOPE_SIGN"),
   num("de","SIGNED force on DE (N)",-3,.08,"DE slope=(7−4)/(8−7)=+3 J/m; force is −3N.","SLOPE_SIGN"),
  ],
  reason:"State the force magnitude rank AB>DE>BC>CD and why positive and negative force signs do not alone determine magnitude.",
  hints:["Label the axes: U in J, x in m. Compute ΔU/Δx for EACH open segment.","AB:+5, BC:−2, CD:0, DE:+3 J/m. F is the NEGATIVE slope, not the slope.","Take magnitudes 5,2,0,3 N for ranking: AB>DE>BC>CD."],
  worked:[
   ["Compute actual segment slopes","AB 10/2=+5, BC (4−10)/(5−2)=−2, CD 0, DE (7−4)/(8−7)=+3 J/m."],
   ["Invert signs to get forces","Signed F values are AB −5N; BC +2N; CD 0N; DE −3N."],
   ["Rank absolute values","Magnitudes are 5,2,0,3 N, so AB>DE>BC>CD. This is not a ranking of signed F or U."],
   ["Flag mathematical corners and units","Force is defined here on segment INTERIORS. At a sharp graph vertex the two-sided slope is not automatically defined."]
  ],
  boundary:"CHANGE THE HORIZONTAL SCALE: the same numbered A–E x tick values now denote units of 0.1 METRE per tick (U in J unchanged). What is signed F on DE in NEWTONS, and does the magnitude order change?",
  boundaryModel:pick("model","What happens to the slope when each x unit is 0.1m?", "Every force magnitude grows 10-fold; ordering stays the same",
       ["Forces unchanged because vertical energies unchanged","Only the graph's signed area changes"],"The physical Δx is 10 times smaller for each numeric tick step, so J/m slopes grow 10 times."),
  boundaryNumbers:[num("de","New signed F_DE (N)",-30,.5,"ΔU=3J across physical Δx=0.1m, so F=−30N.")],
  boundaryCheck:"DE has ΔU=+3 J and physical Δx=0.1m, so slope=+30J/m and F_DE=−30N. All slopes scale by 10, so |F| rank stays AB>DE>BC>CD. Reinterpreting axis units changes force, even when the plotted shape looks unchanged."
 }),
 transfer:task({
  label:"Task B · Optical microtrap graph measured in millijoules per millimetre",
  prediction:"Does an upward potential line always mean a force to the right? What unit does mJ/mm represent?",
  challenge:"UNFAMILIAR SETTING: optical-microtrap calibration records NEW vertices (x mm,U mJ): A(0,4), B(1,1), C(3,5), D(5,5). Each consecutive interval is straight. The bead experiences a 1D conservative force. Find signed F_AB, signed F_BC and rank their magnitudes against F_CD. Convert units carefully.",
  model:pick("model","Which graph rule and conversion are required?","F=−ΔU/Δx and 1 mJ/mm equals 1 N",["F=+ΔU/Δx and 1 mJ/mm is 0.001N","Area under U versus x is force"],"Both U and x units scale by 10⁻³, so mJ/mm = N; conservative force has a MINUS sign."),
  assumption:pick("assumption","Which graph observations are enough for each segment?","Straight measured intervals with conservative position force",["Any smooth-looking graph has constant slope everywhere","Potential energy can define dry friction force without limits"],"The segment-specific slope is meaningful for a conservative force on the stated interval.","INVALID_ASSUMPTION"),
  numbers:[
   num("ab","Signed force AB (N)",3,.07,"U decreases 3 mJ across +1 mm, slope −3mJ/mm, F=+3N.","AXIS_UNITS_AND_SIGN"),
   num("bc","Signed force BC (N)",-2,.07,"U increases 4mJ across 2mm; slope +2mJ/mm and F=−2N.","AXIS_UNITS_AND_SIGN"),
  ],
  reason:"Explain why AB force has magnitude 3N, BC 2N, CD 0, and why mJ/mm equals newtons.",
  hints:["Keep the factor 10⁻³ in BOTH potential and displacement; they cancel.","Find each straight segment's ΔU/Δx, then reverse its SIGN to obtain F.","AB slope −3, BC +2, CD zero mJ/mm. Thus F_AB +3N, F_BC −2N and magnitudes AB>BC>CD."],
  worked:[
   ["Inspect the graph's UNITS","U in millijoules and x in millimetres: 1mJ/mm=(10⁻³J)/(10⁻³m)=1N."],
   ["Calculate signed slopes","AB (1−4)/(1−0)=−3mJ/mm; BC (5−1)/(3−1)=+2mJ/mm; CD=(5−5)/(5−3)=0."],
   ["Obtain signed forces","F_AB=+3N, F_BC=−2N, F_CD=0N. Increasing U means force points LEFT."],
   ["Rank only magnitudes","|F_AB|=3>|F_BC|=2>|F_CD|=0N, irrespective of the opposite signs."]
  ],
  boundary:"REVERSE the coordinate definition x′=−x while describing the SAME physical microtrap force field. What is the signed F_AB with respect to x′, and does the physical force MAGNITUDE change?",
  boundaryModel:pick("model","What changes under reversal of the x coordinate?","Signed component reverses; physical magnitude stays unchanged",
    ["Both sign and magnitude reverse","Potential must change by a sign to remain conservative"],"Coordinate reversal flips the signed x-component but does not change the vector's length."),
  boundaryNumbers:[num("ab","Signed F_AB component in x′ (N)",-3,.07,"Originally F_x=+3N; under x′=−x, F_x′=−3N.")],
  boundaryCheck:"The same vector is +3N in the original +x direction, but in x′=−x coordinates its component is −3N. Magnitude remains 3N. Changing coordinates changes signs, not physical force size."
 })
};
const G5E={
 source:"EX-M61",title:"A potential-energy landscape filters allowed kinetic energy",short:"U(x) and total E → K(x), turning and forbidden regions",
 question:"Where can a particle with fixed total energy exist, move, stop or be unable to reach?",
 sourceCaution:"EX-M61's source-author SVG has a proposed E=8J line and potential plateaus, but exact ordinate values and source-equivalent figure are unverified. The coaching choice B is explicitly UNVERIFIED. This lesson uses a different invented graph; it DOES NOT certify an original 'incorrect statement' option.",
 prerequisites:"In 1D with time-independent conservative forces and no losses, total mechanical E=K+U is constant. Thus K(x)=E−U(x)≥0 at physically accessible positions, and v²=2(E−U)/m. If U>E, that part is classically forbidden. A local U≤E point may be disconnected from the current trajectory by an intervening U>E barrier.",
 core:"A potential graph gives kinetic energy from VERTICAL difference E−U at each position, not force from its height. Minimum U among points in the accessible region means maximum K and speed. If a plateau has U=E, K=0 throughout it; a particle cannot 'move slowly' across it without an additional force or energy. A turning point can occur where K=0, but not every K=0 point guarantees movement onward.",
 guide:"GUIDED NEW PROFILE: a 1kg cart in a conservative magnetic channel has synthetic points (x m,U J) (0,12),(1,12),(2,4),(3,16),(4,8) connected linearly. E=12J. At x=2 kinetic energy 8J and speed 4m/s; x=3 is forbidden (U=16>E). The high barrier prevents motion from x=2 to x=4 even though U(4)<E.",
 guideSteps:[
  ["Draw E as a horizontal level","Compare the graph's U(x) height with E=12J. Vertical gap down to U is K, not the graph's slope."],
  ["Calculate locally allowed K","At x2, U=4 so K=8J, v=√(2K/m)=4m/s. At x3, U=16 so K=−4J, physically forbidden."],
  ["Separate local allowance from connectivity","x4 has U=8, K=4J locally, but to reach it from x2 the particle would have to cross the U=16>E barrier."],
  ["Handle U=E exactly","On x0–1, U=E and K=0. A resting particle on a FLAT plateau has zero force and will not traverse the plateau spontaneously."],
  ["Check for source claims","No original potential-point heights are inferred from the unverified EX-M61 SVG. Model-specific x values and slopes are guide-only."]
 ],
 wrong:"Wrong: fastest motion where potential is greatest; K=E−U has the opposite relationship. Also wrong: every point with U<E can be reached from any starting point, despite barriers; K=0 is not a moving finite speed.",
 conditions:"Conservative 1D time-independent potential; specified fixed E, known m, no losses or hidden work; x paths constrained to the drawn continuous branch. If E changes or a motor acts, update the entire energy level.",
 academic:{decision:"For U(x) and a stated E, compare E with U and the whole connecting profile. Do not take an area under U(x) to find K.",
 observe:"Move the guide's horizontal E-level line: the allowed/forbidden status at x=2 and x=3 changes, while the U curve itself does not.",
 validity:"K=E−U applies to a fixed mechanical-energy ledger, with no friction, motor or explicit time dependence.",
 limit:"At U=E, speed=0; on a flat U=E plateau there is no tangential conservative force to initiate motion. If the energy lies below a barrier, a lower-U region beyond it can be locally allowed but inaccessible from a given side.",
 sourceBoundary:"Unverified figure and coaching option B remain HOLD; no invented original ordinate or motion region is certified."},
 slider:{label:"Synthetic U(x): total mechanical energy E (J)",min:6,max:18,step:1,value:12},
 ...task({
  prediction:"Is a location with U<E always reachable from a specific start? What happens where U=E or U>E?",
  challenge:"TASK A · A 2kg marble moves in a conservative ONE-DIMENSIONAL potential with synthetic connected vertices: A(x0,U3J), B(x1,U9J), C(x2,U12J), D(x3,U1J), all straight between. Total E=9J; it begins at A moving right. Find K at A and locally at D, determine if C is classically allowed and whether D is reachable without added energy.",
  model:pick("model","Which mathematical and physical tests are needed?","K=E−U for local allowance AND barrier connectivity from A",["Force is the area under U(x)","A low potential at D guarantees travel there irrespective of barriers"],"A point can be locally energy-allowed but disconnected from the starting motion by a higher U>E interval."),
  assumption:pick("assumption","What makes E a valid fixed reference?","No friction or extra work, fixed conservative U(x), continuous 1D path",["A motor provides unspecified energy but E remains 9J","Any negative K is physically permitted"],"Classical K must be nonnegative and conserved E only holds without hidden transfers.","INVALID_ASSUMPTION"),
  numbers:[num("ka","Kinetic energy at A (J)",6,.15,"E−U_A=9−3=6 J."),
           num("kd","LOCAL algebraic kinetic energy at D (J)",8,.15,"E−U_D=9−1=8J, but being locally allowed does not imply reachable.")],
  reason:"Explain that C is forbidden (U=12>E9) and D is inaccessible from A over the barrier despite its local 8J kinetic allowance.",
  hints:["Draw the horizontal E=9J line and mark U values above it.","At A K=9−3=6; at D local K=9−1=8; at C K would be −3J.","Trace the entire segment B→C→D: it rises above E. Motion from A cannot pass that barrier in classical energy-conserving mechanics."],
  worked:[
   ["Use energy as a vertical gap","At A K=9−3=6 J; D has a locally allowable K=9−1=8 J."],
   ["Detect forbidden region","At C, U=12J>E=9J, making K=−3J, impossible for an ordinary classical particle."],
   ["Check connectivity rather than isolated points","The straight-line profile crosses U=9 at B before rising to 12 at C; a bead moving from A cannot cross the forbidden B–C section."],
   ["State the two different conclusions","D is algebraically locally allowed, but the bead starting at A cannot reach D without added energy or another path."]
  ],
  boundary:"ADD 4J of external mechanical energy to the SAME marble before it reaches the barrier, so E becomes 13J and no further work/loss occurs. What is K at C? Can the marble cross C and reach D under the specified profile?",
  boundaryModel:pick("model","What does adding energy BEFORE the barrier change?","All points on the stated profile become energy-allowed when E=13J",["The previous forbidden interval remains forbidden regardless of E","K at C remains negative because its potential is large"],"Maximum U of the profile is 12J, below the new E=13J."),
  boundaryNumbers:[num("kc","New K at C (J)",1,.08,"K_C=13−12=+1J.")],
  boundaryCheck:"With E=13J, the full synthetic profile has U≤12J, so no part of this given segment is energy-forbidden. K_C=13−12=+1J, and D is reachable from A along the model path, unlike in the original 9J ledger."
 }),
 transfer:task({
  label:"Task B · Roller coaster gravitational-height map and an intervening hill",
  prediction:"If a roller coaster has enough total energy for a low valley beyond a hill, is it guaranteed to pass the hill?",
  challenge:"UNFAMILIAR SETTING: a 2kg carriage rolls without friction along a one-way vertical-profile track whose continuous height-versus-distance graph passes through (x m,h m): A(0,0.5), B(1,1.5), C(2,2.5), D(3,0.8), with straight connections. Take g10 and total mechanical E=40J with potential U=0 at h=0. Find K at B and locally at D. Can it move from A through C to D on this track?",
  model:pick("model","What representation gives energy and reachability?","Convert h(x) to U=mgh, then require E≥U along the ENTIRE path",["Take the area under h(x) to find kinetic energy","The final low point D alone proves it can cross the hill"],"Height is converted to gravitational U; an intervening U>E barrier blocks classical transit."),
  assumption:pick("assumption","Which track model permits using constant E?","Smooth stationary track, no braking/motor and constant g",["Unknown motor work throughout the hill","A moving guide adds unknown mechanical energy"],"The stated E applies only to the lossless fixed-track model.","INVALID_ASSUMPTION"),
  numbers:[num("kb","Kinetic energy at B (J)",10,.16,"U_B=2×10×1.5=30J; K=40−30=10J."),
           num("kd","LOCAL K at D (J)",24,.18,"U_D=2×10×0.8=16J; K=24J, though that does not prove arrival.")],
  reason:"Explain that at C, U=50J exceeds E=40J and the carriage cannot cross from A to D despite local K_D>0.",
  hints:["Vertical graph measures h (m), NOT energy. Multiply h by mg to obtain U.","E=40; at B U=30 K=10; at C U=50 > E; D has U=16 K=24 locally.","Passing through a hill with U>E would require negative K. A locally allowed valley beyond it does not provide a route."],
  worked:[
   ["Convert the axes to physical potential","U=mgh with m2, g10: at B U=30J; at C U=50J; at D U=16J."],
   ["Compute independent local values","K_B=40−30=10J and K_D(local)=40−16=24J."],
   ["Check the entire path","The hill at C requires 50J, but E is only 40J. The carriage turns before C and cannot reach D from A."],
   ["Name the missing inference","A force or speed at a separated endpoint does not prove that the path between endpoints is dynamically accessible."]
  ],
  boundary:"A MOTOR adds 15 J to the carriage's mechanical energy just after A and then switches OFF. E=55J for the remainder. What is K at the top of hill C, and can it cross now?",
  boundaryModel:pick("model","What changes after a stated finite motor work increment?","New constant E=55J exceeds the entire height barrier",["Motor energy never affects kinetic energy","The old E=40J remains conserved after a motor adds 15J"],"External motor work changes E, which is constant again only after the motor stops."),
  boundaryNumbers:[num("kc","Kinetic energy at C (J)",5,.11,"U_C=50J; K_C=55−50=5J.")],
  boundaryCheck:"After the +15J input, E=55J. The maximum profile potential is U_C=50J, so K_C=5J>0 and the carriage may pass C in the ideal no-loss model. Without the motor it was forbidden."
 })
};
const G5P={
 source:"EX-M69",title:"Constant POWER decides speed and displacement-time curvature",short:"Constant P → v(t), s(t) curvature, not a graph guess",
 question:"What does an s-versus-t curve look like when mechanical POWER is constant instead of FORCE?",
 sourceCaution:"EX-M69 has FOUR source options consisting only of missing [FIG-options-*] images, with no accessible authentic figures. None of A/B/C/D can be matched to a curve from the present evidence. The source steps implicitly assume a start from rest; finite nonzero constant power at exactly v=0 needs an idealized singular initial acceleration, so the t→0 solution is a limiting model, not a realistic finite-force launch.",
 prerequisites:"Power P=dK/dt = F·v. For a 1D constant-mass system driven by constant positive MECHANICAL power with no losses, K=½mv², so d(v²)/dt=2P/m. Therefore v(t)=√(u²+2Pt/m), and s(t)−s(0)=∫v(t)dt = [m/(3P)]{(u²+2Pt/m)^(3/2)−u³}, P>0. The slope ds/dt is speed, and the second derivative d²s/dt²=P/(mv)>0 for v>0.",
 core:"Starting formally from rest gives v∝√t and s∝t^(3/2), with increasing slope and decreasing positive curvature magnitude; NONZERO u instead gives s=[m/(3P)]{(u²+2Pt/m)^(3/2)−u³}, not a pure power law. Constant power differs from constant force (v∝t, s∝t² starting at rest); using an area under s(t) has no standard work meaning.",
 guide:"GUIDED (ideal post-start model, not the source graph): m=4kg, positive mechanical P=18W, u=0 at ideal t=0. For t>0, v=3√t m/s, s=2t^(3/2) metres; at t=4s, v=6m/s and s=16m. At the exact rest instant P=Fv would require unbounded F to keep P finite, so real drives start by a transition with finite force.",
 guideSteps:[
  ["Read the s–time axes","Displacement vertical (m), time horizontal (s). Slope is velocity (m/s); positive CURVATURE means increasing speed."],
  ["Start with a power ledger","P=d(½mv²)/dt, not P=constant force. Integrate over time: v²=u²+2Pt/m."],
  ["Derive a curve instead of picking its appearance","With ideal u0, m4, P18, v=3√t and s=∫3√t dt=2t^(3/2)."],
  ["Check concrete times and tangent slope","At t4, s=16m, v=6m/s. The curve increases and has positive curvature for t>0."],
  ["Mark the startup and figure limits","Finite positive power at exactly zero speed is an unphysical infinite-force limit. No missing EX-M69 option graph is recreated or selected."]
 ],
 wrong:"Wrong: constant power implies constant acceleration or a straight displacement-time line. Also wrong: claim a source option letter from unavailable figure images. Slope of s(t) is velocity; its area has units m·s, not kinetic-energy work.",
 conditions:"One-dimensional forward translation, constant positive MECHANICAL power transferred to kinetic energy, mass fixed, no losses or resistance, t>0 for formal rest start. With u>0 the initial acceleration stays finite; graph options absent remain unverified.",
 academic:{decision:"Derive d(v²)/dt from power before judging the DISPLACEMENT versus TIME curve; do not assume constant F.",
 observe:"Move time on an explicitly NEW s=2t^(3/2) graph. Its s grows faster than linearly, tangent slope v rises as √t, and acceleration falls for t>0.",
 validity:"Constant mechanical input P, fixed mass, no losses; actual startup from exactly zero speed needs a finite-force phase outside the ideal t>0 model.",
 limit:"At P→0 for nonzero u, s→ut and the s(t) graph becomes a straight line. For u=0 and t>0, s∝t^(3/2); at t=0 the ideal acceleration singularity must be disclosed.",
 sourceBoundary:"EX-M69 four option pictures are missing. No source option, curve identity, or official key is certified."},
 slider:{label:"Ideal guide: time t (seconds), P18W, m4kg, u0 limit",min:.25,max:4,step:.25,value:2},
 ...task({
  prediction:"Does constant motor power imply constant force? If an object already moves, must s(t) follow exactly t^(3/2)?",
  challenge:"TASK A · An automated towing winch supplies constant net MECHANICAL power P=50W to a 4kg frictionless cart already moving at u=5m/s at t0. Find its speed after 3s and displacement during those 3s. State whether the displacement-time curve is convex or linear, and why pure t^(3/2) is not exact here.",
  model:pick("model","Which dynamics law correctly determines displacement?", "Integrate v(t)=√(u²+2Pt/m) after a kinetic-energy rate equation",
    ["Use constant acceleration a=P/m","Use a straight line s(t)=ut because power is constant"],"Power is energy/time; F=P/v changes with speed, so acceleration is not constant."),
  assumption:pick("assumption","Which start and energy conditions are actually specified?", "Nonzero starting speed, fixed mass and all net power going into kinetic energy",
    ["Cart starts at rest with unbounded startup force assumed physically real","Unknown friction loss but all 50W still increases kinetic energy"],"The given nonzero u avoids the exact-rest singularity; losses would alter the net power.","INVALID_ASSUMPTION"),
  numbers:[num("speed","Speed at t=3s (m/s)",10,.12,"v²=25+(2×50/4)×3=100."),
           num("distance","Displacement over 3s (m)",70/3,.22,"∫_0³√(25+25t)dt = 2/(3×25)[1000−125]=70/3m.")],
  reason:"Explain that acceleration decreases with speed while s(t) has positive curvature, and why nonzero u changes the pure rest-start scaling.",
  hints:["Integrate P=d(½mv²)/dt to find v²=u²+(2P/m)t.","At t=3, v²=100, giving 10m/s. Displacement is the AREA under v(t), not under s(t).","Use ∫√(25+25t)dt = (2/(75))(25+25t)^(3/2) and evaluate 0..3."],
  worked:[
   ["Start with exact energy rate","2P/m=(2×50)/4=25 m²/s³, so v²(t)=25+25t and v(3)=√100=10m/s."],
   ["Integrate speed for distance","s(3)−s(0)=∫₀³√(25+25t)dt = [2(25+25t)^(3/2)/75]₀³."],
   ["Evaluate the endpoint powers","(100)^(3/2)=1000; (25)^(3/2)=125. Distance=(2/75)(875)=70/3≈23.333m."],
   ["Check curve type","Velocity rises and a=P/(mv)>0, so s(t) curves upward, but starting u=5 means it is not proportional only to t^(3/2)."]
  ],
  boundary:"AFTER t=3s the winch switches OFF and no resistive forces act for another 2 seconds. What ADDITIONAL distance is covered during the motor-OFF interval, and what graph shape applies?",
  boundaryModel:pick("model","What does zero net power and no force imply after shutdown?","Speed stays 10m/s; s(t) is linear during the extra 2s",
     ["It instantly stops when P becomes zero","It continues increasing as t^(3/2) with P off"],"With no net force or work, velocity is constant at the switch-off value."),
  boundaryNumbers:[num("distance","Extra motor-OFF displacement (m)",20,.18,"10m/s times 2s=20m.")],
  boundaryCheck:"At switch-off speed is 10m/s. With P_net=0 and no other tangential force, speed stays 10m/s. Extra distance over 2s is 20m; the new s(t) segment is straight."
 }),
 transfer:task({
  label:"Task B · Airport baggage trolley with constant useful power",
  prediction:"Why does a moving electric trolley speed up more slowly as it gets faster if its useful mechanical watts are fixed?",
  challenge:"UNFAMILIAR SETTING: a baggage trolley of mass 2kg rolls horizontally with negligible resistance. Its motor supplies useful constant MECHANICAL power 8W, starting speed 3m/s. Compute speed and distance after 2s. Show why force cannot be treated as constant.",
  model:pick("model","Which feature of a constant-power drive changes as speed rises?","F=P/v falls while v² grows linearly in time",
       ["F stays constant at P/m","Acceleration stays constant because mechanical power is constant"],"A fixed power source does decreasing force at higher v: F=P/v."),
  assumption:pick("assumption","Which output is included in the 8W value?", "Useful mechanical power after losses, with negligible resistance",
    ["8W is electrical input while motor efficiency is unknown","Unknown drag absorbs a variable part of 8W"],"Without an efficiency or loss model, electrical input watts cannot all be assigned to kinetic energy.","INVALID_ASSUMPTION"),
  numbers:[num("speed","Trolley speed at t=2s (m/s)",5,.08,"v²=9+(2×8/2)×2=25."),
           num("distance","Distance traveled in 2s (m)",49/6,.14,"∫₀²√(9+8t)dt = 2/(3×8)[125−27]=49/6m.")],
  reason:"Explain in words why useful constant watts raise kinetic energy linearly while acceleration decreases with speed.",
  hints:["Mechanical P=d(½mv²)/dt gives v²=9+8t.","After 2s, v²=25. For distance integrate speed √(9+8t), not its square.","s=(2/(3×8))[(9+8t)^(3/2)−27]; at t2 gives 49/6m."],
  worked:[
   ["Energy rate in seconds","2P/m=(2×8)/2=8, giving v²(t)=9+8t."],
   ["Speed at requested time","v²(2)=25 ⇒ v(2)=5m/s."],
   ["Integrate the velocity shape","s(2)=∫₀²√(9+8t)dt = 2/(24)(125−27)=98/12=49/6≈8.167m."],
   ["Inspect the physical driver","Since F=P/v, the motor force decreases as speed rises. Distance-time curvature is positive, but not quadratic as for constant acceleration."]
  ],
  boundary:"Motor input remains 8W ELECTRICAL, but the MECHANICAL efficiency drops to 50% throughout an independent 2s run at the same initial 3m/s; resistance is negligible. Find new final speed and displacement.",
  boundaryModel:pick("model","What energy rate now accelerates the trolley?", "Useful mechanical power is 4W, not the 8W electrical input",
     ["All electrical power remains 8W useful to kinetic energy","An unspecified motor efficiency does not affect kinetic-energy rate"],"Only ηP_electric is mechanical power when efficiency is specified."),
  boundaryNumbers:[num("speed","New speed after 2s (m/s)",Math.sqrt(17),.09,"v²=9+(2×4/2)×2=17."),
                   num("distance","New displacement (m)",(17*Math.sqrt(17)-27)/6,.14,"Integrate √(9+4t), result [2/(3×4)](17^(3/2)−27).")],
  boundaryCheck:"Useful power=0.5×8=4W. v²=9+4t, so v(2)=√17≈4.123m/s. Distance=(2/(3×4))[(17)^(3/2)−27]=(17√17−27)/6≈7.18m. Mechanical efficiency, not a guessed graph option, selects the curve."
 })
};
const G5V={
 source:"EX-M85",title:"Velocity–time endpoints determine NET work on the moving body",short:"v(t) → signed speed endpoints and ΔK",
 question:"Is the area under a velocity–time graph work, or displacement?",
 sourceCaution:"EX-M85's available fig_q30_vt_graph.svg is author-produced and unverified against the official exam diagram. Its labels display 50m/s at t0 and 40m/s at t2, consistent with a conditional −4500J coaching calculation for m10kg, but neither the source graph nor its key is authenticated. R5 uses entirely different fabricated velocities.",
 prerequisites:"Under the work–kinetic-energy theorem, W_NET=K_f−K_i=½m(v_f²−v_i²) for constant mass. On a v-versus-time graph, ordinate gives SIGNED velocity, area ∫vdt gives displacement (m), and slope dv/dt gives acceleration (m/s²). Neither the v–t area nor its slope is directly work (J).",
 core:"Read the two requested times from v(t); take their velocity ordinates, square them individually, subtract, multiply by ½m. Positive/negative velocity signs matter for DIRECTION of motion but kinetic energy uses v². A reversal can have zero net work if initial/final speed magnitudes match, even while displacement or forces are nonzero.",
 guide:"GUIDED NEW GRAPH: a 5kg shuttle has measured linear v(t)=6−4t m/s for 0≤t≤2s. It reverses direction at t=1.5s. Velocity changes from +6 to −2m/s; net work ½(5)(4−36)=−80J. Signed displacement ∫₀²(6−4t)dt=+4m, not −80J.",
 guideSteps:[
  ["Read axes and requested endpoints","Vertical is signed v(m/s), horizontal is t(s). At t0 v+6; t2 v−2."],
  ["Distinguish three different graph operations","Ordinate v gives a velocity. Slope gives acceleration. Signed area between v and t gives displacement; NOT work."],
  ["Compute kinetic energies separately","K_i=½5(6²)=90J, K_f=½5(−2)²=10J."],
  ["Find work by all forces","W_net=10−90=−80J. It can be negative even though the final velocity points left and the net displacement is right."],
  ["Check the distinct displacement","∫₀²(6−4t)dt=12−8=4m. Numeric 4m versus −80J rejects operator confusion."]
 ],
 wrong:"Wrong: area under v(t) equals mechanical work, or subtract signed velocities before squaring. Also wrong: final negative velocity means negative kinetic energy—kinetic energy is nonnegative.",
 conditions:"Constant mass, true signed v(t) on stated time interval, work requested is NET work of all forces, speed measured at each endpoint. A graph may be piecewise; use the requested endpoints, not a guessed constant slope.",
 academic:{decision:"First read the axes and times. v(t) area is DISPLACEMENT; kinetic-energy change across endpoints is NET WORK.",
 observe:"Move time along the new velocity curve: signed velocity crosses zero, displacement accumulates signed area, but kinetic energy remains nonnegative.",
 validity:"Mass fixed and W_net includes all forces. If only one agent's work is asked, subtract work by all OTHER agents.",
 limit:"Same initial and final speed magnitudes gives W_net=0 even if velocity reverses. Reversing direction does not make kinetic energy negative.",
 sourceBoundary:"M85 50→40m/s values are visible only in an author-produced SVG, not an officially authenticated graph. No original source key is admitted."},
 slider:{label:"Synthetic v(t)=6−4t: select t (seconds)",min:0,max:2,step:.25,value:1},
 ...task({
  prediction:"If a moving rover reverses velocity, can its NET work be negative even when its final direction is positive? Is ∫vdt work?",
  challenge:"TASK A · A 3kg delivery rover has a measured STRAIGHT-LINE velocity–time trace from v(0)=−4m/s to v(3s)=+2m/s, linear in between. Compute NET work from t0 to3 and signed displacement. Explain why these DIFFERENT outputs use different graph operations.",
  model:pick("model","Which two different operations apply to v(t)?","Net work uses Δ(½mv²); signed displacement uses ∫vdt",
        ["Area under v(t) is work measured in joules","Subtract velocity ordinates linearly to find kinetic energy"],"Area under v(t) has units metres, not joules; work is change in kinetic energy."),
  assumption:pick("assumption","Which interpretation of work is specified?","NET work of all forces on a constant-mass body",
        ["Only the motor force work is known from v(t)","Negative velocity means negative mass or kinetic energy"],"A velocity record gives total ΔK, not an individual force's contribution without others.","INVALID_ASSUMPTION"),
  numbers:[num("work","NET work from t0 to3 (J)",-18,.26,"½×3[(+2)²−(−4)²]=1.5(4−16)=−18J.","SQUARE_BEFORE_SUBTRACT"),
           num("displacement","SIGNED displacement (m)",-3,.08,"Trapezoid signed area under linear v(t): ((−4)+(+2))/2×3=−3m.","AREA_UNITS_AND_SIGN")],
  reason:"Explain why the rover can finish moving right yet have negative work and net displacement left.",
  hints:["Read v_i=−4 and v_f=+2; K is proportional to SQUARES, not signed velocity.","W_net=½m(v_f²−v_i²)=1.5(4−16)=−18J.","Signed displacement is the trapezoid ∫vdt=[(−4+2)/2]×3=−3m, not work."],
  worked:[
   ["Keep signed velocity but square for kinetic energy","v_i=−4, v_f=+2; K_i=½3×16=24J and K_f=½3×4=6J."],
   ["Compute NET work","W_net=K_f−K_i=6−24=−18J, despite the final positive direction."],
   ["Integrate v(t) for displacement","A linear velocity trace has signed trapezoid area [(−4+2)/2]×3=−3m."],
   ["Distinguish the operations and units","Velocity-time area is −3 METRES; kinetic-energy difference is −18 JOULES. Reversal does not equate them."]
  ],
  boundary:"CHANGE only the FINAL velocity to +4m/s over the same 3s linear trace, with v_i=−4m/s and mass3kg unchanged. Find NET work and signed displacement. Explain how motion occurred even if both outputs are zero.",
  boundaryModel:pick("model","What does equal initial/final speed magnitude imply?","Net work zero; signed displacement may also cancel for the specified symmetric linear trace",
    ["Net work must be positive because the velocity becomes positive","Kinetic energy must be negative at the initial negative velocity"],"Equal squared endpoint speeds imply ΔK=0; for this linear symmetric v(t), positive/negative signed areas cancel."),
  boundaryNumbers:[num("work","Changed NET work (J)",0,.1,"½3(4²−(−4)²)=0."),
                   num("displacement","Changed signed displacement (m)",0,.1,"[(-4+4)/2]×3=0.")],
  boundaryCheck:"For v_i=−4 and v_f=+4, K_i=K_f=24J, so W_net=0J. Linear signed v(t) has equal positive and negative areas, so displacement=0m, despite nonzero travel distance and nonzero intermediate acceleration."
 }),
 transfer:task({
  label:"Task B · Elevator cabin velocity sensor with reversal",
  prediction:"Can a cabin end the interval below its starting altitude yet have increased kinetic energy, and can net work be positive while gravity is always downward?",
  challenge:"UNFAMILIAR SETTING · An elevator cabin of mass 800kg has vertical velocity +2m/s (UP is positive) at t=0 and −1m/s at t=4s. Sensor v(t) is LINEAR across the interval. Find NET work on the cabin and SIGNED vertical displacement. Do not confuse net work with work by the motor alone.",
  model:pick("model","Which expression gives the cabin's NET work?","Difference in endpoint kinetic energies, not area under v(t)",
    ["Area under velocity-time gives joules","Work by motor alone equals the computed net work regardless of gravity"],"Without separate gravity and motor work records, only net work follows directly from v(t)."),
  assumption:pick("assumption","Which sign and system assumptions are in force?","Upward positive, constant mass; all-force NET work sought",
    ["The downward final velocity implies negative kinetic energy","Motor energy alone is determined from endpoint speed without gravity"],"Kinetic energy uses speed squared, while displacement keeps signed velocity.","INVALID_ASSUMPTION"),
  numbers:[num("work","NET work on cabin (J)",-1200,18,"½800[(−1)²−(+2)²]=400(1−4)=−1200J.","SQUARE_BEFORE_SUBTRACT"),
           num("displacement","SIGNED displacement (m)",2,.12,"Average of endpoints (2−1)/2=0.5m/s, times4s=+2m.","AREA_UNITS_AND_SIGN")],
  reason:"Explain why the signed displacement is upward even though final velocity is downward, and distinguish net work from individual motor/gravity work.",
  hints:["Read vertical v(t) ordinate at 0 and4; sign is not kinetic-energy sign.","K_i=½800×4=1600J; K_f=½800×1=400J; net work=−1200J.","Displacement uses signed v(t) trapezoid: (2−1)/2×4=+2m."],
  worked:[
   ["Read signed endpoint velocities","At t0 +2m/s (up); at t4 −1m/s (down). The linear trace must cross through zero."],
   ["Square speeds for kinetic energy","K_i=400×4=1600J; K_f=400×1=400J."],
   ["Use work–kinetic energy","W_net=400−1600=−1200J. Motor work by itself requires separate gravity and any other force work."],
   ["Recover signed vertical displacement","∫vdt=[(2−1)/2]×4=+2m: overall the cabin rose, even though it ends moving down."]
  ],
  boundary:"CHANGE only the final sensor velocity to −3m/s over 4s, same initial +2m/s and linear trace. What is new NET work and displacement? Why may the work sign change even though final motion points downward?",
  boundaryModel:pick("model","Which feature decides the sign of ΔK and net work?","Compare squared initial and final speed MAGNITUDES, not their directions",
     ["Downward velocity always implies negative work","Area under v(t) is net work after any reversal"],"Speed rises from magnitude2 to magnitude3, increasing kinetic energy even with negative final velocity."),
  boundaryNumbers:[num("work","Changed NET work (J)",2000,20,"½800(9−4)=2000J."),
                   num("displacement","Changed signed displacement (m)",-2,.15,"[(2−3)/2]×4=−2m.")],
  boundaryCheck:"K_i=1600J and K_f=½800×9=3600J, so W_net=+2000J. Signed displacement=[(2−3)/2]×4=−2m. Final downward direction does not determine work sign."
 })
};

const G5W={
 source:"AN-2",title:"Conservative work is the negative CHANGE in potential—not the negative line integral of force",short:"F(x) signed area ↔ W_c = −ΔU",
 question:"Which sign belongs to the work done BY the force and which belongs to the potential change?",
 sourceCaution:"AN-2 has no graph figure; it is a two-statement question. Its original wording gives W=−∫F·dr as 'work BY force', contradicting the conventional work definition W_by=+∫F·dr. The source's coaching choice C is a claim, not academically authenticated, and a path-independent conservative field is a precondition.",
 prerequisites:"Mechanical work BY force along a path is W_F=∫F·dr. If the force is conservative, ΔU=−W_F, so W_F=U_i−U_f. For a FORCE–DISPLACEMENT graph F_x(x), work is signed AREA ∫F_x dx (N·m=J). For a POTENTIAL–DISPLACEMENT graph U(x), the negative slope gives F_x, and the NEGATIVE endpoint difference gives conservative work.",
 core:"Do not insert a minus sign into the definition of WORK BY FORCE. The same physical process may have ΔU>0 and W_by<0. Path independence only holds for the conservative part; a dissipative force can add path-dependent work even when gravity's or spring's contribution is path-independent.",
 guide:"GUIDED: a Hooke spring exerts F_x=−4x N for x in metres, with U=2x² J. Moving a bead from x=1m to x=3m, W_by_spring=∫₁³−4x dx=−16J. Spring potential rises from 2J to18J (ΔU=+16J). Work BY spring is NEGATIVE and equals −ΔU.",
 guideSteps:[
  ["Label work actor and graph axes","F(x) is force (N) against displacement (m). Its signed AREA has joules. U(x) is energy (J), whose negative slope has newtons."],
  ["Use the correct definition","W_by=∫F_x dx, without a leading minus. With spring F=−4x over x1→3, the area is NEGATIVE."],
  ["Evaluate the force area","∫₁³−4x dx=−2(3²−1²)=−16J."],
  ["Compare endpoint potential","U=2x², so ΔU=2(9−1)=+16J. Only here is ΔU=−∫Fdx."],
  ["Check field/path conditions","Spring force is conservative; adding dry friction would make total work path dependent, not captured by one scalar spring U."]
 ],
 wrong:"Wrong: W_by=−∫F·dr (that is the conservative potential change, not work). Also wrong: use the positive magnitude of the F(x) area and discard its direction; work can be negative.",
 conditions:"Stationary conservative 1D field, signed x displacement, no loss in the spring potential ledger. If friction acts, keep its nonconservative work separate.",
 academic:{decision:"Read F(x) or U(x) axes; F(x) signed area equals work BY force, while ΔU=−W_c. A wrong extra minus flips the physics.",
 observe:"Move the endpoint on the new F=−4x graph: accumulated signed work changes while spring U increases; the two remain opposites for this conservative spring.",
 validity:"Single-valued time-independent potential for a conservative force; the integral follows the specified path and work actor.",
 limit:"Reversing endpoints reverses W_c and ΔU; a closed conservative loop has zero net work even if parts of the path contain nonzero force.",
 sourceBoundary:"AN-2 has no figure, but wording/key identity is still source-held. Work-by-force is defined with a PLUS integral; the potential change is its negative."},
 slider:{label:"Guide: final spring position x_f (m), start x_i=1m",min:0,max:3,step:.25,value:3},
 ...task({
  prediction:"Is work BY a conservative force equal to +∫F·dx or −∫F·dx? What happens to the sign when U increases?",
  challenge:"TASK A · A NEW 1D conservative electrostatic-style potential is U(x)=3x² joules with x in METRES. A charged test bead moves from x=−1m to x=+2m. Find work done BY the conservative force and the force component at x=+2m. Confirm work by integrating F(x)=−dU/dx rather than applying an extra minus.",
  model:pick("model","Which relationship gives work BY the conservative field?","W_by=U_i−U_f=+∫Fdx, where F=−dU/dx",["W_by=−∫Fdx always","Area under U(x) directly equals work"],"The negative of the force line integral is ΔU, not work done BY the force."),
  assumption:pick("assumption","What makes a scalar U(x) valid?","A 1D conservative position-dependent field with U given explicitly",["Unknown sliding friction is included inside U(x) as a conservative force","Force depends on path history and still has one position-only U"],"The supplied U belongs to the conservative field only; dissipative work needs a separate ledger.","INVALID_ASSUMPTION"),
  numbers:[num("work","Work BY field from −1m to +2m (J)",-9,.14,"U_i=3(1)=3J, U_f=3(4)=12J, so W=3−12=−9J.","NEGATIVE_WORK_SIGN"),
           num("force","Signed F_x at x=2m (N)",-12,.17,"F=−d(3x²)/dx=−6x; at x2 F=−12N.")],
  reason:"Explain why the force changes sign across x0 and how positive and negative signed areas produce the net −9J.",
  hints:["U_i=3J at x−1, U_f=12J at x+2. Work BY conservative field is U_i−U_f.","F(x)=−6x N; F positive for x negative, negative for x positive.","∫_{−1}^{2}−6x dx=−3(4−1)=−9J. Potential change is +9J."],
  worked:[
   ["Calculate endpoint potentials","U(−1)=3(−1)²=3J; U(+2)=3(2²)=12J."],
   ["Apply correct work sign","W_by=−ΔU=3−12=−9J, opposite to the positive ΔU=+9J."],
   ["Check local force and area","F=−6x N, so F(+2)=−12N. Integral ∫_{−1}^{+2}−6x dx=[−3x²]_{−1}^{2}=−9J."],
   ["Understand cancellation","Part of the path x<0 contributes positive work; x>0 contributes negative work. Signed area, not absolute area, gives net −9J."]
  ],
  boundary:"REVERSE the endpoints in an independent move (start x=+2m, finish x=−1m), same conservative U(x). What is work done BY the field, and why does its sign reverse?",
  boundaryModel:pick("model","What does path reversal do to conservative work?","It changes W_by from −9J to +9J while swapping U_i and U_f",
      ["The work remains −9J because the potential graph is identical","Work is always positive for a moving particle"],"A conservative line integral reverses sign when integration limits are interchanged."),
  boundaryNumbers:[num("work","Reversed work BY field (J)",9,.12,"U_i=12J at x2, U_f=3J at x−1; W=12−3=+9J.")],
  boundaryCheck:"Swapping endpoints gives W_by=U(2)−U(−1)=12−3=+9J. The same field does opposite signed work on the reversed path; the potential change becomes −9J."
 }),
 transfer:task({
  label:"Task B · Hiking trail gravity work and measured rolling resistance",
  prediction:"Does gravity do different total work on two routes that finish at the same mountain height, even if one path is longer?",
  challenge:"UNFAMILIAR SETTING: a 2kg parcel travels between two points on a mountain carriage track: start height3m, finish height7m, g=10. Two geometrically different paths link the SAME endpoints. With gravity as the only modeled working force, find conservative gravitational work and ΔU. Explain why path length is irrelevant to those two quantities.",
  model:pick("model","Which variable controls gravity's conservative work?","Vertical height difference only: W_g=−mg(h_f−h_i)",
    ["Total horizontal+vertical trail distance","Always positive work because the parcel moved"],"Conservative gravity work depends on vertical endpoints, not arbitrary path length."),
  assumption:pick("assumption","Which work is being requested?","Work BY gravity only in a uniform static gravitational field",
    ["TOTAL work including unspecified trail friction","Motor work despite no motor force being specified"],"The gravity contribution is separately identifiable; total work needs any other force ledger.","INVALID_ASSUMPTION"),
  numbers:[num("work","Work BY gravity (J)",-80,1,"−mgΔh=−2×10×4=−80J.","NEGATIVE_WORK_SIGN"),
           num("potential","Gravitational potential change ΔU (J)",80,1,"+mgΔh=+80J.")],
  reason:"Explain why two different routes between the same heights have equal gravity work, despite having different distances.",
  hints:["Gravity is vertical and conservative; only the height CHANGE enters its work.","Δh=7−3=+4m, m2, g10; ΔU=+80J.","W_by_gravity=−ΔU=−80J for both routes, irrespective of path shape."],
  worked:[
   ["Choose gravitational potential correctly","U=mgh; the parcel rises 4m, so ΔU=(2)(10)(4)=+80J."],
   ["Give work done BY gravity with sign","W_g=−mg(h_f−h_i)=−80J."],
   ["Check route independence","Every route with the same starting and finishing height has the same gravitational work (for uniform gravity)."],
   ["Separate possible other work","If a motor or tangential rolling resistance acts, its work must be added separately; gravity's own conservative contribution is still −80J."]
  ],
  boundary:"ADD a measured CONSTANT 5N tangential rolling resistance OPPOSING travel, and distinguish a 5m direct route from a 12m winding route between the SAME heights. What is TOTAL work by gravity PLUS resistance on each path? Does gravity's contribution change?",
  boundaryModel:pick("model","What changes when path-dependent resistance is added?","Gravity stays −80J; total work adds −5N times EACH path length",
     ["Gravity's work also grows with each path's length","Rolling resistance can be absorbed into one position-only gravitational U"],"Gravity is conservative; opposing resistance adds different negative work along different path lengths."),
  boundaryNumbers:[num("direct","Total work on 5m route (J)",-105,1,"−80−5×5=−105J."),
                   num("long","Total work on 12m route (J)",-140,1,"−80−5×12=−140J.")],
  boundaryCheck:"Gravity contributes −80J on BOTH paths. Measured resistance adds −25J along 5m and −60J along 12m. Total work =−105J or −140J. The full gravity+resistance work is path-dependent, so it is not simply −ΔU_gravity."
 })
};

const G5C={
 source:"AN-6",title:"Test whether a force has a position-only scalar potential",short:"Conservative field → closed-loop and path test",
 question:"Can the same start/end positions yield different work? If so, can one global U(position) explain that force?",
 sourceCaution:"AN-6 is a figure-free conceptual source; the standard friction/coulomb/restoring/gravity classification is conditional on ideal static fields and ordinary dry kinetic friction. Position dependence alone does not guarantee global conservativity in a multiply connected domain; a closed-loop zero-work condition is the robust criterion.",
 prerequisites:"For a static conservative force field with single-valued potential U(r), F=−∇U and ∮F·dr=0 around every allowed closed loop (equivalently path-independent work). A smooth curl-free field on a simply connected domain admits such a potential. Dry kinetic friction opposes motion and produces negative work proportional to travel length in a simple constant-resistance model; its work around a closed route is nonzero, so it has no single-valued position-only mechanical U.",
 core:"Use an ACTUAL TWO-PATH or CLOSED-LOOP test instead of labeling a force conservative from one negative work measurement. Gravitational/electrostatic fields (under static assumptions) and ideal elastic restoring forces have potentials; dry friction does not. A magnetic force may do zero work while being velocity-dependent, so 'zero work on one path' alone does not establish scalar potential.",
 guide:"GUIDED NEW FIELD on the x–y plane: F=(2y,0) newtons for x,y in metres, meaning F_x=2(N/m)·y. Traverse rectangle (0,0)→(2,0)→(2,1)→(0,1)→(0,0). Bottom/right/left work zero, upper edge x2→0 at y1 has F_x=+2N and Δx=−2m, giving closed-loop work −4J. Thus no single-valued U(x,y) for this field on the full rectangle.",
 guideSteps:[
  ["Ask if both endpoints or a complete loop are known","A conservative field returns zero work around ANY closed path. Check more than one route rather than one endpoint measurement."],
  ["Read the vector field's components","F=(2y,0) means F_x depends on y; F_y=0. Work uses F_x dx+F_y dy, not just the field's magnitude."],
  ["Integrate each rectangle edge","At y0 lower edge F_x0; along vertical edges dx0; upper edge at y1 has F_x=2N while x decreases2m, W=−4J."],
  ["Interpret the nonzero closed-loop integral","A single-valued potential would require ΔU=0 over a closed loop, hence ∮F·dr=0; our −4J disproves it."],
  ["Compare ordinary forces","Static gravity and ideal springs admit a U; kinetic friction on a reversible closed route dissipates energy instead of returning it."]
 ],
 wrong:"Wrong: every field that changes with position must have a scalar potential; or 'a zero-work segment' proves conservativity. A nonzero work integral around ONE closed loop is sufficient to refute a global position-only potential.",
 conditions:"Time-independent force and ordinary mechanical scalar U(r); work evaluated around physically allowed loops. For curl-free sufficiency assume a simply connected domain. Frictional resistance law explicitly depends on direction of motion and distance.",
 academic:{decision:"Ask whether work from A to B is path independent; a nonzero CLOSED-LOOP integral prevents a single-valued potential.",
 observe:"Change rectangle height on a new two-dimensional vector-field diagram. The upper horizontal edge acquires different force and nonzero loop work, while the lower edge remains zero.",
 validity:"Closed-loop test uses an explicitly defined static vector field and accessible paths. Local zero curl needs domain topology assumptions to imply global potential.",
 limit:"A zero-height degenerate loop has zero work even for a nonconservative field; checking ONLY that loop would prove nothing. A smooth conservative field has zero work for ALL closed loops.",
 sourceBoundary:"Original AN-6 source concepts are not a verified official key. Friction is nonconservative under the stated ordinary sliding model; static electric/gravity/ideal springs are the conservative comparison cases."},
 slider:{label:"Guide closed rectangle height h (m), width 2m; F=(2y,0)N",min:0,max:2,step:.25,value:1},
 ...task({
  prediction:"If a field does nonzero work around one closed route, can it still equal −∇U of one single-valued scalar U? Is one path with zero work enough to prove it conservative?",
  challenge:"TASK A · A small test robot feels a NEW planar static force F=(3y,0) N with y in metres (coefficient 3N/m). It follows closed CCW rectangle (0,0)→(2,0)→(2,1)→(0,1)→(0,0). Compute net work around the loop, and work along two open routes A=(0,0) to B=(2,1): route1 bottom then right, route2 up the left then along the TOP. Decide whether a single-valued scalar potential exists on the region.",
  model:pick("model","What proves that no global single-valued U exists?","Nonzero closed-loop work, equivalently two path-dependent A→B integrals",
      ["Force depends on y, so it must be conservative","Zero work along bottom edge alone proves potential exists"],"A force can depend on position yet be nonconservative; compare more than one path or a closed loop."),
  assumption:pick("assumption","Which mathematical field is supplied?", "A static 2D field F_x=3y N, F_y=0 on the full rectangle",
      ["Unknown friction force along each route instead of F=(3y,0)","Force is always tangent to the specific robot path"],"Work is ∫F_x dx+F_y dy for the stated field; vertical legs have zero field work.","INVALID_ASSUMPTION"),
  numbers:[num("loop","CCW closed-loop work (J)",-6,.15,"Top edge y1 has F_x3N, traversed x2→0: W=−6J.","CLOSED_LOOP_SIGN"),
           num("route2","A→B work by 'up LEFT then RIGHT across TOP' (J)",6,.15,"Along top y1, F_x=3N over Δx=+2m: +6J.")],
  reason:"State route1 work 0J, route2 +6J and closed loop −6J. Explain why a global scalar potential is impossible.",
  hints:["On a vertical edge dx=0, and F_y=0, so its work is zero.","Bottom y0 gives Fx0. Upper y1 gives Fx3N; direction on closed CCW top is LEFT so work −6J.","For A→B, bottom then up yields 0J; left up then top right yields +6J. Work depends on path."],
  worked:[
   ["Check actual field components","F_x=3y and F_y=0N. Work is F_x dx+F_y dy. Both vertical edges contribute zero."],
   ["Integrate the closed path","Bottom y0 yields0, right edge0, upper y1 moving x2→0 gives3×(−2)=−6J, left edge0."],
   ["Compare the two A→B open paths","Bottom→right gives0J; left→top gives(+3N)(+2m)=+6J."],
   ["Reject a position-only potential","Two distinct work values for the SAME A and B, or nonzero closed-loop work, prove no single-valued potential over this rectangle."]
  ],
  boundary:"REPLACE the original field with F=(0,−2y) N for the SAME rectangle, where y is in metres and coefficient 2N/m. Find CLOSED-LOOP work and the scalar potential U(x,y) up to an additive constant.",
  boundaryModel:pick("model","Which conservative model now fits the replacement field?","U=y² joules (plus constant), giving F_y=−dU/dy",
       ["A nonzero closed-loop integral is required for any potential","U=−y² because F_y is negative"],"If F_y=−2y, then ∂U/∂y=+2y, so U=y²."),
  boundaryNumbers:[num("loop","New closed-loop work (J)",0,.1,"For F_y=−2y, vertical ascending/descending integrals cancel, horizontal edges F_x0."),
                   num("potential","Value U at y=1m if U(0)=0 (J)",1,.1,"U(y)=y²; U(1)=1J.")],
  boundaryCheck:"The replacement F_y=−2y is conservative with U=y² J (using coefficient 1 J/m²), since −∂U/∂y=−2y. Its work around the closed rectangle is zero. With U(0)=0, U(1m)=1J."
 }),
 transfer:task({
  label:"Task B · Warehouse tug with dry rolling resistance on two routes",
  prediction:"A tug takes two routes between the same stations but the route lengths differ. Can one endpoint-only potential give BOTH friction-work totals?",
  challenge:"UNFAMILIAR SETTING · A warehouse robot experiences approximately CONSTANT 4N rolling RESISTANCE opposing its motion on a level floor. It moves from dock A to B via route1 length 3m or route2 length 5m (same endpoints). Compute work by resistance on both. Decide whether a position-only scalar potential U(x,y) can represent this rolling resistance over these routes.",
  model:pick("model","Which property decides if resistive work is a potential difference?", "Opposing friction work depends on path length, not solely endpoints",
      ["Same endpoints force same work for any force","Any constant-magnitude force is a conservative position field"],"Resistance reverses with motion direction and dissipates energy over the distance traveled."),
  assumption:pick("assumption","Which resistance law is explicitly given?", "Constant 4N opposite instantaneous travel along both routes",
      ["A fixed +x conservative force of 4N","No friction and a perfect lossless floor"],"The phrase 'opposes motion' defines a tangential, velocity-direction-dependent loss.","INVALID_ASSUMPTION"),
  numbers:[num("short","Resistance work on 3m route (J)",-12,.15,"−4N×3m=−12J.","PATH_AND_WORK_SIGN"),
           num("long","Resistance work on 5m route (J)",-20,.15,"−4N×5m=−20J.")],
  reason:"Explain why the differing work values with identical endpoints refute a single mechanical potential U(position) for dry resistance.",
  hints:["Work done by a force opposite motion is negative.","Use W=−f×path distance: the two lengths are 3m and5m.","−12J≠−20J for the SAME endpoints; a single position-only ΔU cannot equal both."],
  worked:[
   ["Resolve resistance direction","A 4N force against the tangent does negative work on every traveled segment."],
   ["Calculate two genuine paths","Route1 W=−4×3=−12J; route2 W=−4×5=−20J."],
   ["Apply the conservative criterion","A single-valued position potential would give one U(A)−U(B) for both routes. These resistive works differ."],
   ["Avoid overgeneralization","Mechanical energy lost to resistance becomes internal/thermal energy; that is not a reversible single-valued potential of the robot's position."]
  ],
  boundary:"REPLACE rolling resistance by a uniform static conservative force F_x=+3N to the right, F_y=0, acting as the robot moves between endpoints with horizontal displacement Δx=+2m on EITHER path. Find work on each path and a potential U(x) with U(0)=0.",
  boundaryModel:pick("model","What changes with the new fixed-direction force?", "Work is F_xΔx=+6J on both paths; U(x)=−3x",
     ["Work remains −12J or −20J because routes remain unequal","Work grows with length even for this conservative uniform field"],"A constant-direction position field has work determined by projected displacement, not total route length."),
  boundaryNumbers:[num("work","Work by uniform field on either path (J)",6,.12,"F_xΔx=3×2=6J."),
                   num("potential","U at x=2m, U(0)=0 (J)",-6,.12,"U(x)=−3x, so U(2)=−6J.")],
  boundaryCheck:"Uniform F=(3,0)N is conservative: U(x)=−3x J for x in metres and U(0)=0. Both routes A→B have Δx=+2m and W=+6J regardless of their different lengths."
 })
};
const G5X={
 source:"JEE-2026-04-06-S2-Q29",title:"A velocity–POSITION graph still gives work through ΔK",short:"v(x) endpoint speeds → work; v dv/dx → force",
 question:"Does the area under v(x) mean work? What changes when the horizontal axis is POSITION, not time?",
 sourceCaution:"This source provides an explicit formula v=2x² but no figure. Its coefficient has units m⁻¹s⁻¹ when x is in metres and v is m/s, and endpoint ΔK gives a FORMAL 1250J net-work result. However v(0)=0 under the autonomous smooth law dx/dt=2x² implies a particle placed exactly at x=0 does not spontaneously leave that equilibrium in finite time without an additional start/perturbation. The coaching answer is therefore a conditional endpoint calculation, not proof of a dynamically realizable launch.",
 prerequisites:"Given velocity as a function of POSITION v(x), read v_i=v(x_i) and v_f=v(x_f), then W_net=½m(v_f²−v_i²). The graph area ∫v(x)dx has units m²/s and is NEITHER displacement NOR work. If differentiable along a moving branch, acceleration a=dv/dt=v(dv/dx), so F_net(x)=mv(dv/dx); its signed area ∫Fdx is net work.",
 core:"Changing the x-axis of a graph from time to position changes what slope and area mean. v(t) area is displacement, but v(x) area is not. At v=0, the chain rule still gives a formal F; the ability to leave an exact equilibrium under an autonomous ODE must be separately checked. Use nonzero-start physically realizable models in new examples.",
 guide:"GUIDED NEW SENSOR GRAPH: a 2kg autonomous track robot has v(x)=1+x m/s for 1≤x≤3m, always moving to the right with v>0 (coefficient of x is 1s⁻¹). At x1 speed2 and x3 speed4m/s; W_net=½2(16−4)=12J. F(x)=mv dv/dx=2(1+x)N; integrating F from x1 to3 gives the SAME +12J.",
 guideSteps:[
  ["Read the independent variable precisely","Horizontal axis x(m), vertical signed v(m/s). This is v versus POSITION, not the more familiar v versus TIME."],
  ["Lookup the two endpoint speeds","At x1, v=2m/s; at x3, v=4m/s. The speeds are observed at different POSITIONS."],
  ["Apply work–kinetic energy","W_net=½m(v_f²−v_i²)=½2(16−4)=+12J. No area under v(x) is used."],
  ["Derive a force as a cross-check","For a moving differentiable path, a=v dv/dx and F=m v dv/dx=2(1+x)N. Its F–x AREA integrates to +12J."],
  ["Check existence and the zero-speed trap","The new guide has nonzero starting speed, avoiding the original zero-at-x0 autonomous equilibrium. Endpoint algebra does not by itself certify source launch dynamics."]
 ],
 wrong:"Wrong: take area under v(x) as work, or use dv/dx as acceleration (its units are 1/s). The correct acceleration is v dv/dx; a formal W_net result does not prove a particle departs a smooth autonomous equilibrium with v=0.",
 conditions:"Constant mass, differentiable prescribed v(x) on physically traversed moving branch, enough dynamical conditions for actual transit, work NET on body not an individual force. Coefficients carry units. New tasks begin with nonzero v.",
 academic:{decision:"Use endpoint speeds in ΔK for net work. For an independently known moving branch, force requires m v dv/dx, not m dv/dx alone.",
 observe:"Move along an invented v(x)=1+x plot. Velocity increases with POSITION; derived force and accumulated work change. The area under v(x) is not labeled work.",
 validity:"Position law must represent actual motion, not just formal endpoint values. At a smooth equilibrium with v(0)=0, prove startup rather than assuming it.",
 limit:"Equal speed magnitudes at endpoints give zero net work even if force did positive and negative work between them. In the original autonomous v=2x², x(0)=0 is a stationary solution not a finite-time launch.",
 sourceBoundary:"No official key authenticated. Source formal 1250J is conditional: exact zero-speed start under autonomous dx/dt=2x² needs extra physical initiation, and 'work done BY the body' is not automatically identical to work done ON it."},
 slider:{label:"New guide v(x)=1+x: position x(m)",min:1,max:3,step:.25,value:2},
 ...task({
  prediction:"Can a velocity-versus-position trace use its shaded area for net work the way a force-versus-position graph does?",
  challenge:"TASK A · A 4kg cleaning robot travels to the RIGHT on a horizontal track. Spatial-speed sensors measure an explicitly NEW law v(x)=2+0.5x m/s for 0≤x≤4m, with the coefficient 0.5 in s⁻¹; v(0)=2m/s. Find NET work on the robot over the interval and its instantaneous net force at x=4m using a=v dv/dx.",
  model:pick("model","Which equation gives net work from v(x)?","Use endpoint speeds in ΔK; derive F=m v dv/dx if needed",
      ["Integrate area directly below v(x) for work","Use m dv/dx as force without velocity factor"],"A position graph has different horizontal units than time; a=v dv/dx along a moving branch."),
  assumption:pick("assumption","What ensures the new speed law is a viable moving branch?","Nonzero v(0), constant mass and differentiable v(x) on the traveled segment",
      ["An exact zero-velocity equilibrium with no external launch","Undefined speed sign yet assume the x interval is traversed"],"The new motion starts with v0=2m/s; this avoids the source's exact v(0)=0 autonomous-start issue.","INVALID_ASSUMPTION"),
  numbers:[num("work","NET work x0→4 (J)",24,.28,"½4[(4)²−(2)²]=2(16−4)=24J.","ENDPOINT_SQUARED_SPEED"),
           num("force","Net F_x at x=4m (N)",8,.15,"a=v dv/dx=4×0.5=2 m/s²; F=4×2=8N.")],
  reason:"Explain why v(x)'s area is not work and how m v dv/dx produces an F(x) whose area agrees with ΔK.",
  hints:["Endpoint speeds: v_i=2, v_f=2+0.5(4)=4m/s.","W_net=½4(16−4)=24J. Area ∫v(x)dx has units m²/s, not J.","At x4 v4, dv/dx=0.5s⁻¹, a=v dv/dx=2m/s², so F=8N."],
  worked:[
   ["Read measured spatial endpoints","v(0)=2m/s, v(4)=4m/s; the horizontal axis is POSITION."],
   ["Compute net work from kinetic energy","K_i=½4(2²)=8J, K_f=½4(4²)=32J; net work +24J."],
   ["Derive force with the chain rule","dv/dx=0.5s⁻¹; at x4, a=v dv/dx=(4)(0.5)=2m/s² and F=4×2=8N."],
   ["Cross-check the actual force area","F(x)=4(2+0.5x)(0.5)=4+x N; ∫₀⁴(4+x)dx=16+8=24J. This is area under F(x), NOT v(x)."]
  ],
  boundary:"CHANGE to an independent REVERSE run from x=4m to x=0m with spatial velocity v(x)=−(2+0.5x)m/s, so the robot genuinely moves LEFT. What is NET work over this reverse run? Explain why the same positive F(x) can do NEGATIVE work on leftward displacement.",
  boundaryModel:pick("model","How is work determined on the negative-velocity reverse run?","Reverse endpoint speeds yield ΔK=−24J, while F_x remains positive",
      ["Speed sign alone makes kinetic energy negative","The reversed path must still have +24J because the graph looks the same"],"From x4 to x0 the speed magnitude drops 4→2, so kinetic energy decreases; force acts opposite displacement."),
  boundaryNumbers:[num("work","Net work for reverse x4→0 (J)",-24,.25,"½4[(-2)²−(-4)²]=2(4−16)=−24J.")],
  boundaryCheck:"In the stated REVERSE run, v(4)=−4 and v(0)=−2m/s. ΔK=½4[(−2)²−(−4)²]=−24J. F=m v(dv/dx)=4(2+0.5x)(0.5)=4+x N points right while dx<0, hence negative work."
 }),
 transfer:task({
  label:"Task B · Spatial radar speeds on an airport runway",
  prediction:"If a moving cart's speed is a square-root function of position, is its acceleration equal to the derivative dv/dx?",
  challenge:"UNFAMILIAR SETTING: spatial radar measures a 5kg ground-service vehicle moving RIGHT from x=0 to4m with v(x)=√(9+4x) m/s, where x is in metres and the constants have compatible SI units. Find net work from endpoints and the net FORWARD force using a=v dv/dx. The vehicle begins at nonzero 3m/s.",
  model:pick("model","Which expression correctly obtains acceleration from a spatial speed curve?", "a=v(dv/dx) and net work still equals endpoint ΔK",
    ["a=dv/dx because velocity is vertical axis","Area under v(x) gives mechanical work"],"Since x is not time, dv/dx has units 1/s, not m/s²; multiply by v."),
  assumption:pick("assumption","Which branch is physically traversed?", "Forward moving v>0 for every x from0 to4 with constant mass",
    ["v=0 at x0 and the cart departs without a launching force","Unknown reverse turns invalidate the given monotonic moving interval"],"A positive nonzero speed throughout makes the differentiable moving branch well defined.","INVALID_ASSUMPTION"),
  numbers:[num("work","NET work x0→4 (J)",40,.4,"v_i²=9, v_f²=25; W=½5(25−9)=40J."),
           num("force","Constant net forward force (N)",10,.18,"v dv/dx=(1/2)d(v²)/dx=½×4=2m/s²; F=5×2=10N.")],
  reason:"Explain why the velocity-position AREA is not work and why F(x) becomes a constant +10N under this spatial law.",
  hints:["Endpoint speed squared is directly visible: v²=9+4x.","W_net=½5[(9+16)−9]=40J.","a=v dv/dx=(1/2)d(v²)/dx=2m/s², F=5×2=10N; force work 10×4=40J."],
  worked:[
   ["Use spatial endpoints","v_i=√9=3m/s and v_f=√25=5m/s at x4."],
   ["Compute work from kinetic energy","W_net=½5(25−9)=2.5×16=40J."],
   ["Apply the chain rule","a=v dv/dx=½d(v²)/dx=½×4=2m/s², so F=m a=5×2=10N."],
   ["Cross-check F–x area","The net F is +10N constant through 4m, so ∫Fdx=+40J. The shaded area under v(x) has units m²/s and cannot replace it."]
  ],
  boundary:"CHANGE the measured spatial law to v(x)=√(9+4x−x²)m/s on 0≤x≤4, still moving forward with v>0 and same mass. What is NET work between x0 and4, even though net force is nonzero at intermediate positions?",
  boundaryModel:pick("model","What do equal squared endpoint speeds mean with varying force in between?","NET work zero; positive and negative force work cancel",
      ["No force acts at any position because work is zero","Work equals positive area under the speed-versus-position curve"],"Zero total ΔK does not mean local force or travel are zero."),
  boundaryNumbers:[num("work","Changed NET work x0→4 (J)",0,.1,"v²(0)=9 and v²(4)=9+16−16=9, so ΔK=0.")],
  boundaryCheck:"New v²(x)=9+4x−x² is positive over 0..4. Both endpoint speeds are 3m/s, so W_net=½5(9−9)=0J. But F(x)=(5/2)d(v²)/dx=10−5x N changes sign at x2; ∫₀⁴(10−5x)dx=40−40=0J. No area under v(x) was used."
 })
};

/* Distinct schematic figures grounded only in the expressly NEW guide data.
 * Never draw or reproduce an unauthenticated source figure. */
const signatures={G5U,G5E,G5P,G5V,G5W,G5C,G5X};
function drawModel(id,v,{host,readout,svg,svgText,svgLine}){
 const text=(x,y,msg)=>svg(host,"text",{x,y,fill:"#194b5e","font-size":13,"font-weight":"650"},msg);
 const line=(x1,y1,x2,y2,color="#447d94",weight=2)=>svgLine(host,x1,y1,x2,y2,color,weight);
 const x0=260,x1=595,yTop=42,yBot=223;
 const graph=(pts,minX,maxX,minY,maxY,labelX,labelY,selected=null)=>{
  const xx=x=>frame(x,minX,maxX,x0,x1),yy=y=>frame(y,minY,maxY,yBot,yTop);
  line(x0,yTop-6,x0,yBot+7,"#567985",2);
  line(x0-7,yBot,x1+12,yBot,"#567985",2);
  text(x1-60,247,labelX);text(x0-5,28,labelY);
  if(minY<0&&maxY>0){const zero=yy(0);line(x0,zero,x1,zero,"#a3bdc4",1);}
  if(pts?.length){
   svg(host,"polyline",{points:pts.map(p=>xx(p[0])+","+yy(p[1])).join(" "),fill:"none",stroke:"#207ea2","stroke-width":4});
   for(const [x,y] of pts)svg(host,"circle",{cx:xx(x),cy:yy(y),r:3.7,fill:"#18506a"});
   if(selected!=null&&selected>=0&&selected+1<pts.length){
    const a=pts[selected],b=pts[selected+1];
    line(xx(a[0]),yy(a[1]),xx(b[0]),yy(b[1]),"#db844e",6);
   }
  }
  return {xx,yy};
 };
 if(id==="G5U"){
  const pts=[[0,0],[1,6],[3,2],[5,2],[7,8]],i=Math.round(v),slopes=[6,-2,0,3],names=["AB","BC","CD","DE"];
  graph(pts,0,7,0,9,"x (m)","U (J)",i);
  text(22,53,"U(x), not F(x)");text(22,85,"Selected segment: "+names[i]);text(22,117,"Slope: "+slopes[i]+" J/m");text(22,150,"Force: "+(-slopes[i])+" N");
  readout.textContent="Synthetic graph: "+names[i]+" has signed slope "+slopes[i]+"J/m, hence F_x="+(-slopes[i])+"N and magnitude |F|="+Math.abs(slopes[i])+"N. Sharp corners are excluded.";
 }else if(id==="G5E"){
  const pts=[[0,12],[1,12],[2,4],[3,16],[4,8]],res=graph(pts,0,4,0,19,"x (m)","U (J)");
  const ey=res.yy(v);line(x0,ey,x1,ey,"#c57937",2);
  text(20,54,"Total energy E="+v+" J");text(20,89,"K(x2)="+(v-4)+" J");text(20,120,"K(x3)="+(v-16)+" J");
  readout.textContent="Synthetic conservative potential: at x=2, K=E−U="+(v-4)+"J; at x=3, K="+(v-16)+"J. A negative K is forbidden; an allowed point beyond a forbidden barrier is not automatically reachable.";
 }else if(id==="G5P"){
  const pts=Array.from({length:25},(_,i)=>{const t=i/6;return[t,2*t**1.5]});
  const res=graph(pts,0,4,0,17,"t (s)","s (m)");
  svg(host,"circle",{cx:res.xx(v),cy:res.yy(2*v**1.5),r:8,fill:"#d4884a"});
  text(20,52,"Constant mechanical P");text(20,85,"m=4kg, P=18W");text(20,118,"v(t)=3√t");
  readout.textContent="NEW ideal t>0 guide: t="+round(v)+"s, s=2t^(3/2)="+round(2*v**1.5)+"m, ds/dt=v="+round(3*Math.sqrt(v))+"m/s, acceleration="+round(1.5/Math.sqrt(v))+"m/s². Exact rest start at finite P needs a physical startup phase.";
 }else if(id==="G5V"){
  const pts=[[0,6],[2,-2]],res=graph(pts,0,2,-3,7,"t (s)","v (m/s)");
  svg(host,"circle",{cx:res.xx(v),cy:res.yy(6-4*v),r:8,fill:"#d4884a"});
  text(20,52,"Area ∫v dt = displacement");text(20,88,"Net work = ΔK");
  readout.textContent="NEW v(t)=6−4t: t="+round(v)+"s, v="+round(6-4*v)+"m/s, signed displacement from t0="+round(6*v-2*v*v)+"m, net work on 5kg="+round(2.5*((6-4*v)**2-36))+"J. A velocity's negative sign does not make its kinetic energy negative.";
 }else if(id==="G5W"){
  const pts=[[0,0],[3,-12]],res=graph(pts,0,3,-13,1,"x (m)","F_x (N)");
  svg(host,"circle",{cx:res.xx(v),cy:res.yy(-4*v),r:8,fill:"#d4884a"});
  text(20,52,"F(x) area = work BY force");text(20,86,"U(x)=2x² (J)");
  readout.textContent="NEW conservative spring: F_x("+round(v)+")="+round(-4*v)+"N, work from x=1m to x="+round(v)+"m is "+round(-2*(v*v-1))+"J; potential change is "+round(2*(v*v-1))+"J, its opposite. Signed area under F(x), not U(x), gives work.";
 }else if(id==="G5C"){
  const res=graph(null,0,2.5,0,2.5,"x (m)","y (m)");
  const xx=res.xx,yy=res.yy;
  const h=v;
  line(xx(0),yy(0),xx(2),yy(0),"#297c92",4);
  line(xx(2),yy(0),xx(2),yy(h),"#297c92",4);
  line(xx(2),yy(h),xx(0),yy(h),"#d38346",5);
  line(xx(0),yy(h),xx(0),yy(0),"#297c92",4);
  text(20,53,"F=(2y, 0)N");text(20,85,"Loop: bottom→right");text(20,108,"→top LEFT→bottom");
  readout.textContent="NEW 2D field: rectangle width=2m, height="+round(h)+"m; counterclockwise upper edge work = "+round(-4*h)+"J. All other edges do zero field work. Nonzero closed-loop work at h>0 refuses any global U(position).";
 }else if(id==="G5X"){
  const pts=[[1,2],[3,4]],res=graph(pts,1,3,1,5,"x (m)","v (m/s)");
  svg(host,"circle",{cx:res.xx(v),cy:res.yy(1+v),r:8,fill:"#d4884a"});
  text(20,54,"Horizontal axis is POSITION");text(20,87,"a=v·dv/dx");text(20,120,"F(x)=2(1+x)N");
  readout.textContent="NEW v(x)=1+x: x="+round(v)+"m, velocity="+round(1+v)+"m/s, net force for 2kg="+round(2*(1+v))+"N, accumulated W_net from x1="+round((1+v)**2-4)+"J. The area under v(x) is NOT work or displacement.";
 }
}
for(const [id,d] of Object.entries(signatures)){
 d.modelView=(val,ctx)=>drawModel(id,val,ctx);
 if(d.guideSteps.length!==5||d.worked.length!==4||!d.transfer||d.transfer.worked.length!==4||d.transfer.hints.length!==3)
  throw Error("Incomplete C05 R5 source-specific reasoning construction "+id);
 if(d.fields[0].id!=="model"||d.fields[1].id!=="assumption"||d.transfer.fields[0].id!=="model")
  throw Error("R5 independent graph model choice missing "+id);
}
if(typeof window.WPEGapJourneys!=="function")throw Error("Merged six-stage F-family engine is required");
window.WPEGapJourneys(signatures,{storagePrefix:"g9:wpe:c05-r5:v1:",coveragePath:"learning-coverage-r1.json"});
})();
