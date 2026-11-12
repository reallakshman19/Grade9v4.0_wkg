/* C06 R4 candidate constructions. Reuses unmodified six-stage F-family
 * practice renderer and C06's energy + radial-feasibility foundation.
 * Does not edit or promote any of the original 74 source questions.
 */
(() => {
"use strict";
const pick=(id,label,expected,wrong,mistake,kind="MODEL_CHOICE")=>({id,label,type:"select",
 choices:["Choose an idea",expected,...wrong,"I'm not sure yet"],expected,mistake,errorKind:kind});
const num=(id,label,expected,tol,mistake,kind="CALCULATION_OR_UNITS")=>({id,label,type:"number",expected,tol,mistake,errorKind:kind});
const reason=(label="Explain the model choice, physical conditions and why the tempting shortcut fails")=>({id:"reason",label,type:"textarea"});
const why=(label="Explain your changed-condition model choice before checking the answer")=>({id:"why",label,type:"textarea"});
const task=(o)=>({
 prediction:o.prediction,challenge:o.challenge,
 fields:[o.model,o.assumption,...o.numbers,reason(o.reason)],
 hints:o.hints,worked:o.worked,boundary:o.boundary,
 boundaryFields:[o.boundaryModel,...(o.boundaryNumbers||[]),why(o.boundaryWhy)],
 boundaryCheck:o.boundaryCheck
});
const springMath={
  chord:"The distance from the BOTTOM anchor to a bead at angle θ measured FROM THE TOP is d(θ)=2R cos(θ/2), for 0≤θ≤180°. Height above the bottom is y(θ)=R(1+cosθ). The angle of a bead when d=R is θ=120°, not 60° measured from top.",
  energy:"For a smooth CAPTIVE guide, ½mv_f²=mg[y_i−y_f]+½k[(d_i−ℓ₀)²−(d_f−ℓ₀)²] if the bead starts at rest. Both spring and gravity have potential energy; the track's ideal normal does no work.",
  caution:"The supplied author-produced EX-M18 SVG has a TOP spring anchor and a noncircular contour although the proposed written solution assumes a BOTTOM anchor on a circular hoop. It is NOT verified as the original source figure. A bead constrained by a two-sided/captive guide can follow the arc, but an ordinary one-sided wall requires a separate N≥0 contact feasibility check. This lesson assumes a captive guide, not unverified unilateral contact."
};
const C6S={
 source:"EX-M18",title:"A spring changes length while a bead moves around a hoop",short:"Hoop + spring · geometry before energy",
 question:"How much gravitational height and elastic extension change on a circular guide—and what contact model keeps the bead on that path?",
 sourceCaution:springMath.caution,
 prerequisites:"Recall ½kx² for a Hooke spring, mgy for height, and the fact that an ideal track reaction is perpendicular to displacement. A string or one-sided contact can fail if its normal/tension would need to be negative; a CAPTIVE ring/groove instead enforces the path in both radial directions.",
 core:springMath.chord+" "+springMath.energy+" The contact feasibility of a one-sided wall is NOT proved by an energy calculation.",
 guide:"GUIDED, NOT THE SOURCE: a 2 kg bead on a smooth captive circular rail of R=1 m carries a spring to a peg at the bottom (k=10 N/m, natural length ℓ₀=R). Released from rest at the SIDE (θ=90° from top), it reaches d=R at θ=120°. Take g=10 m/s².",
 guideSteps:[
  ["Draw two distinct line segments","The bead-to-centre distance is fixed R; the spring is a CHORD to the bottom anchor. They are not the same distance. The chord length is 2R cos(θ/2)."],
  ["Find the target angle","At d=R, 2cos(θ/2)=1, giving θ=120° from TOP. This is 60° from DOWNWARD vertical; mixing reference axes gives a wrong height."],
  ["Read the gravitational drop","At the side y_i=R; at θ=120°, y_f=R(1−½)=R/2. The drop is R/2=0.5 m, so gravity releases 10 J."],
  ["Write BOTH spring endpoint energies","Initial spring extension=(√2−1)R, final extension=0. Spring release=½(10)(√2−1)²≈0.858 J."],
  ["Check speed and the contact premise","½(2)v²=10+0.858 gives v≈3.295 m/s. A captive guide can enforce the arc; a unilateral hoop wall would additionally require its reaction to remain physically admissible."],
 ],
 wrong:"Wrong: identify spring length with R throughout because the bead moves on a radius-R circle; the spring is an off-centre CHORD. Another wrong model uses N≥0 as if it automatically follows from energy; capture versus one-sided contact must be declared.",
 conditions:"Smooth rigid CAPTIVE circular rail, fixed bottom peg, light linear spring, point bead, known resting length, ideal normal perpendicular to motion, zero initial speed. θ measured clockwise from the top; y measured up from bottom. For one-sided walls, compute radial contact N(θ) and refuse the constrained path whenever N would go negative.",
 academic:{decision:"First reconstruct the anchor and circle; then choose spring+gravity conservation. Separately decide if the guide is captive or unilateral.",
 observe:"Move the angle: the bead-to-bottom chord changes even though the bead-to-centre radius does not. The diagram draws BOTH segments and shows spring extension and height.",
 validity:"This is a stated bottom-anchor CAPTIVE R4 example, not authentication of the original author schematic. If only a one-sided wall is given, energy is merely conditional on remaining in contact.",
 limit:"At k→0 the speed depends solely on height drop. At g→0 only spring release remains; if an endpoint has MORE spring energy than the start, the assumed starting-from-rest trajectory may be inaccessible.",
 sourceBoundary:springMath.caution},
 slider:{label:"Bead angle θ from TOP (degrees): chord and height",min:0,max:180,step:5,value:90},
 ...task({
  prediction:"If a spring is anchored at the bottom of a circular rail, does the bead-to-centre R equal its spring length? Would a captive rail need the same N≥0 condition as a one-sided wall?",
  challenge:"TASK A · A 1 kg bead rides a smooth CAPTIVE vertical circular rail of radius 2 m, with a light k=8 N/m spring connected to a bottom peg and natural length ℓ₀=R. Starting from REST at θ=60° from TOP, it travels to the position where spring length first becomes R. Take g=10. Find the target θ, starting spring energy and bead speed there. Identify the contact assumption.",
  model:pick("model","Which mathematical system must be used?","Spring-chord geometry plus gravity and spring energy, on a captive rail",["Spring length stays R at every point","Only radial force, with no potential-energy change"],"Distance to centre stays R but spring-to-bottom distance varies with angle."),
  assumption:pick("assumption","What does the example assume about contact?","A captive frictionless rail enforces the arc in either radial direction",["Any unilateral wall keeps contact regardless of N","The spring force has no radial component"],"A one-sided wall cannot push/pull in both radial directions; its contact needs a separate check.","INVALID_ASSUMPTION"),
  numbers:[
   num("target","Target angle from TOP (degrees)",120,1,"Set 2R cos(θ/2)=R. θ=120° from top, 60° from bottom.","GEOMETRY_AND_REFERENCE"),
   num("spring","Initial spring energy (J)",16*(Math.sqrt(3)-1)**2,.14,"At θ=60°, d=√3R and extension=(√3−1)R. Apply ½kx²."),
   num("speed","Final bead speed (m/s)",Math.sqrt(2*(20+16*(Math.sqrt(3)-1)**2)),.07,"Gravity releases mgR=20 J; initial spring release adds 16(√3−1)² J. Use ½mv²."),
  ],
  reason:"Explain why the spring length is a chord, why gravity does work, and what contact a captive rail permits.",
  hints:["Mark the top angle, centre, BOTTOM spring peg and bead. The spring is not a radius.","Chord to bottom is d=2R cos(θ/2), and y=R(1+cosθ). Find initial/final spring extensions.","Use ½mv_f²=mg(y_i−y_f)+½k(x_i²−x_f²). Do not assume an unverified wall contact condition."],
  worked:[
   ["Determine the actual chord","At θ_i=60°, d_i=2Rcos30°=√3R. At d_f=R, cos(θ_f/2)=½, so θ_f=120° from TOP."],
   ["Separate height from spring","y_i=1.5R and y_f=0.5R, so Δh=R=2 m. Gravity supplies mgΔh=20 J."],
   ["Compute spring release","With ℓ₀=R and k=8, initial extension x_i=(√3−1)×2 m. U_s,i=½(8)[2(√3−1)]²=16(√3−1)²≈8.574 J; final extension zero."],
   ["Find conditional speed and contact meaning","½(1)v²=20+8.574 yields v≈7.560 m/s. This speed assumes the bead remains on a CAPTIVE track. An ordinary one-sided hoop must separately pass the radial N≥0 check."]
  ],
  boundary:"CHANGE SPRING REST LENGTH only to ℓ₀=1.5R while retaining k=8, m=1, R=2 and the SAME θ_i=60°, θ_f=120° positions. Spring initially slightly extended and finally compressed. What is the NEW final speed? Explain why comparing only initial extension is wrong.",
  boundaryModel:pick("model","How must the changed spring rest length enter the energy ledger?","Include elastic potential at both start and finish, even in compression",["Set final spring energy to zero despite changed ℓ₀","Use only gravitational work because the spring crosses equilibrium"],"New natural length makes final spring length R a COMPRESSED spring, so its final energy is nonzero."),
  boundaryNumbers:[num("speed","Changed final speed (m/s)",Math.sqrt(2*(20+16*(Math.sqrt(3)-1.5)**2-4)),.08,"U_i=16(√3−1.5)² J and U_f=4 J. Set ½v²=20+U_i−U_f.")],
  boundaryCheck:"With ℓ₀=3 m, d_i=2√3 m and d_f=2 m: U_i=16(√3−1.5)²≈0.8616 J, U_f=½8(−1m)²=4 J. v²=2(20+U_i−4), hence v≈5.807 m/s. A spring stores energy in compression as well as extension."
 }),
 transfer:task({
  label:"Task B · Circular horizontal robot rail with off-centre elastic tether",
  prediction:"At the exactly opposite point, the spring initially pulls radially. Can a robot starting at rest move away by itself? After a tiny perturbation, could it accelerate without a height change?",
  challenge:"UNFAMILIAR SETTING: a 2 kg robot rolls on a smooth captive HORIZONTAL circular track of radius 1 m. It is tethered by a k=20 N/m elastic cord to a peg at the RIGHTMOST point of the circle; natural length is √2 m. At the LEFTMOST point the robot is initially at rest in an UNSTABLE equilibrium: the spring force is radial and cannot initiate tangential movement. A vanishingly small tangential perturbation starts it moving toward the TOPMOST point (a quarter-turn around the centre). Calculate the LIMITING released spring energy and speed as perturbation size and energy tend to zero. The peg stays fixed. Do not invent gravitational work.",
  model:pick("model","Which energy ledger applies on the horizontal rail?","Only elastic energy changes; gravitational height is constant",["Gravity supplies mgR between leftmost and topmost points","Tether length remains one radius R"],"On a horizontal plane all points have equal gravitational height; the peg-to-robot chord changes."),
  assumption:pick("assumption","Which contact/force assumptions are given?","A captive smooth horizontal rail, fixed peg and massless elastic tether",["A one-sided rail and arbitrary external motor work","Tether has fixed length regardless of attachment geometry"],"With the fixed anchor and no motor/friction work AFTER an infinitesimal initiating perturbation, compute the limiting spring-energy release. At the exactly opposite point at exact rest, tangential force is zero and no motion starts.","INVALID_ASSUMPTION"),
  numbers:[
   num("spring","Elastic energy released (J)",10*(2-Math.sqrt(2))**2,.06,"Initial tether length 2R, final √2R at perpendicular circle points. Subtract both elastic energies.","GEOMETRY_AND_REFERENCE"),
   num("speed","Speed at the topmost point of horizontal track (m/s)",Math.sqrt(10*(2-Math.sqrt(2))**2),.04,"½(2)v² equals released spring energy; height is unchanged.")
  ],
  reason:"Explain why the curved path is compatible with zero gravitational work, and why the tether chord—not circle radius—controls energy.",
  hints:["Draw the fixed peg on the rightmost circumference point and measure straight-line CHORD distances to robot locations.","From the opposite point the tether length is 2R; from the top point it is √2R and equals its natural length.","Use ΔK=−ΔU_s after the vanishing perturbation; gravitational potential does NOT change on a horizontal circle. This is a limit of perturbed motion."],
  worked:[
   ["Reconstruct the horizontal geometry","From the right peg to left robot the distance is 2R=2 m. Right peg to top robot is the hypotenuse √2R=√2 m. At EXACT rest at the opposite point the spring exerts no tangential force, so departure requires an arbitrarily small initiating perturbation."],
   ["Compare spring endpoints","With ℓ₀=√2m, initial extension is 2−√2 m and final extension 0. Initial elastic energy ½20(2−√2)²=10(2−√2)²≈3.431 J."],
   ["Exclude unsupported energy","A horizontal circle changes no gravitational height. The captive guide's perpendicular normal does no work, and no motor/damping is specified."],
   ["Solve speed","In the limit of vanishing perturbation energy, ½(2)v²→3.431 J, so v→√3.431≈1.852 m/s. This is a limiting perturbed trajectory, NOT spontaneous motion from exact rest at an unstable equilibrium. A one-sided contact rail would require an additional feasibility check."]
  ],
  boundary:"ROTATE the same robot rail into a VERTICAL plane, with the left point level with the centre and the top point 1 m HIGHER. Use the same vanishing-perturbation initial-energy limit and the same spring. Can it reach the upper point without additional work? Give the energy deficit in joules instead of inventing an upper-point speed.",
  boundaryModel:pick("model","Can the spring release overcome the new gravitational rise?","No: spring release is less than the required gravitational energy",["Yes: horizontal result has the same speed","Yes: every captive guide supplies kinetic energy"],"The guide controls direction but cannot supply work if smooth and stationary."),
  boundaryNumbers:[num("deficit","Minimum additional energy needed (J)",20-10*(2-Math.sqrt(2))**2,.07,"Gravity needs mgR=20 J but spring releases ≈3.431 J.")],
  boundaryCheck:"In the vanishing-perturbation limit, vertical lift from leftmost to top is R=1 m, requiring mgR=(2)(10)(1)=20 J. Elastic release supplies only 10(2−√2)²≈3.431 J. Deficit≈16.569 J, so the upper point is not reachable from rest without outside work. Do NOT write a square root of negative kinetic energy."
 })
};

const C6A={
 source:"EX-M39",title:"One circular path, two perpendicular acceleration components",short:"Radial and tangential acceleration",
 question:"At the turning point, does zero speed mean zero acceleration? At the bottom, is the acceleration tangent or inward?",
 sourceCaution:"The source's original equality at one pendulum angle combines TWO accelerations evaluated at different points. It does not say that v²/L is the TOTAL acceleration everywhere. Source identity and exact official diagram remain unverified.",
 prerequisites:"The acceleration of a constrained particle has radial magnitude a_r=v²/R toward the centre and tangential component a_t=dv/dt. Only the radial part vanishes when instantaneous speed is zero. Gravity has a tangential component g sinθ on a smooth vertical path.",
 core:"For a pendulum released from rest at θ₀ from vertical, at the extreme point a_r=0 and |a_t|=g sinθ₀. At the bottom a_t=0 and a_r=v_b²/L=2g(1−cosθ₀) from energy. Away from these special points the magnitude is √(a_r²+a_t²), not their ordinary sum.",
 guide:"GUIDED: a 2 m pendulum is released from θ₀=60° and g=10. The initial turning-point speed is zero but |a_t|=10 sin60°≈8.660 m/s². At bottom its radial acceleration is 2g(1−cos60°)=10 m/s².",
 guideSteps:[
  ["Draw velocity and the centre arrow","The tangent to the circle is perpendicular to the radius. A bob can momentarily stop with nonzero tangential acceleration."],
  ["At the initial extreme","v=0 ⇒ a_r=v²/L=0. Tension has no tangential component, so |a_t|=g sin60°≈8.660 m/s²."],
  ["Find bottom speed from potential","Drop Δh=L(1−cosθ₀). Conservation gives v_b²=2gL(1−cosθ₀)."],
  ["Find bottom acceleration components","At bottom gravity and tension are radial, so a_t=0; a_r=v_b²/L=2g(1−cos60°)=10 m/s²."],
  ["Guard the generalization","At an intermediate angle both components can be nonzero. Compute total |a| as perpendicular-vector magnitude, not a_r alone."]
 ],
 wrong:"Wrong: at extreme v=0 hence 'acceleration must be zero'. The gravitational tangential component is nonzero and starts the swing. Another wrong model treats v²/L as total acceleration at every point or adds perpendicular components as scalars.",
 conditions:"Light inextensible string or captive smooth circular track, stationary support, no drag, angle from downward vertical, gravity vertically downward, initial extreme released from rest. Tangential g sinθ uses the smooth no-other-tangential-force condition.",
 academic:{decision:"Resolve velocity, radial acceleration and tangential acceleration into DIFFERENT directions before comparing magnitudes.",
 observe:"Angle slider changes tangential g sinθ and the energy-derived bottom radial 2g(1−cosθ) differently; the extreme has zero radial speed but not zero total acceleration.",
 validity:"The original equality is an extreme-versus-bottom comparison for an ideal pendulum. Away from those points both components contribute.",
 limit:"θ₀→0 makes both accelerations→0 (trivial no-swing root). A shorter string at the same release angle changes bottom speed, but the bottom radial acceleration remains 2g(1−cosθ₀).",
 sourceBoundary:"Author-proposed θ=2 arctan(½) belongs to the ideal frictionless nonzero swing; the zero-angle root is a degenerate limit, not the same physical motion."},
 slider:{label:"Release angle θ₀ (degrees) comparing extreme and bottom",min:0,max:85,step:5,value:60},
 ...task({
  prediction:"Can the extreme position have zero speed and nonzero acceleration? Will the bottom acceleration be inward or tangential?",
  challenge:"TASK A: a frictionless 1.6 m pendulum is RELEASED FROM REST at θ₀=45° from downward vertical in g=10. Find its total acceleration MAGNITUDE at the release extreme and at the lowest point, then decide WHICH is larger. Explain the different directions and why L cancels in the bottom result.",
  model:pick("model","How do you calculate each magnitude?","Extreme tangential g sinθ; bottom radial 2g(1−cosθ)",["Both accelerations are v²/L","Both accelerations vanish at the turning point"],"At release v=0 so radial is zero but tangential gravity is nonzero. Bottom tangential gravity is zero."),
  assumption:pick("assumption","Which idealized situation permits this comparison?","Smooth ideal pendulum released from rest at the stated angle",["An additional tangential motor force of unknown magnitude","Air drag removes unknown mechanical energy"],"The bottom speed comes from lossless gravitational energy only.","INVALID_ASSUMPTION"),
  numbers:[
   num("extreme","Magnitude at release extreme (m/s²)",10/Math.sqrt(2),.09,"a_r=0, |a_t|=g sin45°.","VECTOR_COMPONENT"),
   num("bottom","Magnitude at bottom (m/s²)",20*(1-1/Math.sqrt(2)),.1,"v_b²/L=2g(1−cos45°), not g sin45°."),
  ],
  reason:"Explain how two perpendicular acceleration types exchange roles between release and lowest point; state which magnitude is larger.",
  hints:["At the extreme instantaneous v=0 so a_r=0, but gravity still pulls along the tangent.","At the bottom gravity has no tangential component. Find v_b from height loss.","Use a_ext=g sinθ₀ and a_bottom=2g(1−cosθ₀); compare numerically."],
  worked:[
   ["Identify the directions","Extreme speed zero ⇒ a_r=0; tangential acceleration has magnitude g sinθ₀. At bottom tangential acceleration 0; velocity is horizontal and acceleration points up toward pivot."],
   ["Compute extreme","a_ext=10 sin45°=10/√2≈7.071 m/s²."],
   ["Use height change","v_b²=2gL(1−cos45°). Radial bottom a_b=v_b²/L=20(1−1/√2)≈5.858 m/s²."],
   ["Compare the correct quantities","Extreme total acceleration is larger (7.071>5.858). The string length cancels only in this energy-derived bottom radial expression."]
  ],
  boundary:"SHORTEN the string to 0.8 m without changing release angle, g or initial rest condition. Does the bottom RADIAL acceleration change? Compute it and explain how v_b can change while v_b²/L remains the same.",
  boundaryModel:pick("model","What happens to bottom radial acceleration as L halves?","It stays 2g(1−cosθ₀) because speed squared scales with L",["It doubles as 1/L without changing v²","It halves because the string is shorter"],"Energy makes v_b²∝L, so the ratio v_b²/L stays the same."),
  boundaryNumbers:[num("bottom","New bottom radial acceleration (m/s²)",20*(1-1/Math.sqrt(2)),.1,"Use g and release angle, not the previous speed with new radius.")],
  boundaryCheck:"New v_b²=2(10)(0.8)(1−cos45°), half the former speed squared, while a_b=v_b²/0.8=20(1−1/√2)≈5.858 m/s², unchanged. An isolated 1/L formula that freezes v² is the wrong changed-condition model."
 }),
 transfer:task({
  label:"Task B · Camera measuring a roller on a vertical circular guide",
  prediction:"When a roller moves midway up a vertical curved guide, can its acceleration have inward AND tangential parts at the same instant?",
  challenge:"UNFAMILIAR SETTING: a roller is confined to a smooth vertical circular guide of radius 2 m. A camera measures speed 4 m/s at θ=30° from downward vertical, where the only tangential force is gravity (g=10). Find radial inward acceleration, tangential acceleration MAGNITUDE, and total acceleration MAGNITUDE. Decide whether v²/R alone describes the full vector.",
  model:pick("model","Which quantity is the total acceleration magnitude?","Square-root of squared radial and tangential components",["Radial acceleration v²/R alone","Arithmetic sum v²/R+g sinθ"],"The radial and tangent directions are perpendicular, not collinear."),
  assumption:pick("assumption","Which physical observation supplies tangential acceleration?","Smooth stationary vertical rail with gravity as the only tangential force",["Unknown tangential motor pushing the roller","Friction along the rail of unknown sign"],"An additional tangent force changes a_t and makes the given data insufficient.","INVALID_ASSUMPTION"),
  numbers:[
   num("radial","Inward radial component magnitude (m/s²)",8,.08,"a_r=v²/R=16/2."),
   num("tangent","Tangential component magnitude (m/s²)",5,.08,"|a_t|=g sin30°; direction is DOWNHILL along the tangent.","VECTOR_COMPONENT"),
   num("total","TOTAL acceleration magnitude (m/s²)",Math.sqrt(89),.12,"Combine PERPENDICULAR components: √(8²+5²), not their sum."),
  ],
  reason:"Explain radial versus tangent directions and why their components may both be present.",
  hints:["Draw the inward radius arrow and tangent arrow as perpendicular.","Use speed for inward acceleration v²/R; use gravity's tangent projection g sinθ for the other.","Pythagoras applies to radial/tangent components of the acceleration VECTOR."],
  worked:[
   ["Measure inward acceleration","a_r=v²/R=4²/2=8 m/s², always toward the centre."],
   ["Resolve gravity along the tangent","At θ=30°, the smooth rail provides no tangent force, so |a_t|=10sin30°=5 m/s², directed down the guide."],
   ["Combine as perpendicular vectors","The acceleration magnitude is √(8²+5²)=√89≈9.434 m/s²."],
   ["Reject v²/R as total","Centripetal acceleration is only the RADIAL component; it equals total acceleration only when the tangent component is zero."]
  ],
  boundary:"REDUCE the rail radius from 2 m to 1 m while the camera still measures speed 4 m/s at θ=30°. Keep the tangent-force assumption. What are new radial and TOTAL acceleration magnitudes?",
  boundaryModel:pick("model","What changes when curvature increases at unchanged speed/angle?","Radial v²/R doubles; gravitational tangent projection stays the same",["Both components double because R halves","Tangential acceleration disappears when radius changes"],"Gravity's projection depends on angle, not curvature radius."),
  boundaryNumbers:[num("radial","New inward radial acceleration (m/s²)",16,.1,"16/1=16 m/s²."),
                  num("total","New total acceleration magnitude (m/s²)",Math.sqrt(281),.2,"√(16²+5²)=√281 m/s².")],
  boundaryCheck:"At R=1 m, a_r=16 m/s²; |a_t|=5 m/s² unchanged because θ and g are unchanged. Total magnitude √(256+25)=√281≈16.763 m/s². Gravity's tangential projection does not scale with 1/R."
 })
};

const C6H={
 source:"EX-N31",title:"A smooth exterior dome stops pushing before the bead stops moving",short:"Exterior hemisphere · N = 0 boundary",
 question:"When does a sliding block leave a convex surface, and why is N=0 a force boundary, not a zero-speed condition?",
 sourceCaution:"The EX-N31 2R/3 height result is the limit of a bead given an infinitesimal downhill displacement/perturbation from rest at the TOP of a stationary smooth EXTERIOR hemisphere, with initial energy tending to crown-rest energy and no supplementary constraints. At exact unperturbed rest at the crown, no tangential force can initiate sliding. A rigid captive groove or a different start changes the result. The exact original figure has not been verified.",
 prerequisites:"An exterior smooth hemisphere can PUSH outward along its surface normal N≥0 but cannot pull inward to keep a bead attached. Inward is toward the sphere centre. Gravity supplies inward mg cosθ; outward normal subtracts: mg cosθ−N=mv²/R while touching.",
 core:"In the infinitesimally perturbed rest-at-crown LIMIT, v²=2gR(1−cosθ). Thus N=mg cosθ−m v²/R=m g(3cosθ−2). At N=0, cosθ=2/3 and height above the equator h=Rcosθ=2R/3. For initial downhill speed u at crown, cosθ_det=(u²+2gR)/(3gR), IF contact exists initially.",
 guide:"GUIDED: a 0.5 kg puck is infinitesimally nudged downhill from the exact stationary crown of a smooth EXTERIOR sphere, R=5 m, g=10. Take the limit of vanishing displacement and initial kinetic energy. Exact unperturbed rest would remain at the unstable equilibrium. In the sliding limit, it detaches when cosθ=2/3: h=10/3≈3.333 m above the equatorial plane. The puck then flies freely rather than continuing on the sphere.",
 guideSteps:[
  ["Separate the physical forces","Inward points toward sphere centre. The normal pushes OUTWARD and gravity has an inward component mg cosθ. An exterior wall cannot provide N<0."],
  ["Compute speed while still touching","After a vanishing downhill perturbation (exact crown rest alone would not move), conservation gives the limiting v²=2gR(1−cosθ). The normal force does no work while contact exists."],
  ["Apply the inward radial balance","mg cosθ−N=mv²/R; substitute speed to obtain N=mg(3cosθ−2)."],
  ["Find the boundary","N first reaches 0 at cosθ=2/3, so h=Rcosθ=5×2/3=10/3 m. Speed is NONZERO there."],
  ["Stop using the constrained model after release","Beyond N=0, the puck follows projectile motion. Extrapolating v²/R and a fictitious negative N past release is invalid."]
 ],
 wrong:"Wrong: put N plus mg cosθ both inward, which reverses the exterior-contact sign. Also wrong: say detachment occurs when speed becomes zero, or apply a captive track's two-sided force to a smooth dome.",
 conditions:"Exterior convex stationary smooth sphere, small point particle, no drag or adhesion, initial speed clearly specified, normal only outward and N≥0. θ measured from TOP outward radial line. Formula is conditional on contact up to the found boundary.",
 academic:{decision:"Use TWO independent statements while touching: energy to find speed, inward force balance to test N≥0. Once the normal would turn negative, stop the constrained trajectory.",
 observe:"Slide along the crown angle; read N/(mg)=3cosθ−2, which falls to zero while v² is already positive. After release the sphere no longer steers the puck.",
 validity:"Sphere exterior contact differs from a captive wire; at the crown an initial tangential speed u must satisfy u²≤gR or contact is impossible immediately.",
 limit:"u²=gR makes initial N=0 and release at the top; u²>gR requires N<0 at the initial crown, so it cannot start in surface contact. In the vanishing-perturbation crown-rest LIMIT, detachment h=2R/3. Exact crown rest without a disturbance has no initiated descent.",
 sourceBoundary:"The 2R/3 source result is a perturbation LIMIT of an ideally smooth EXTERIOR sphere; exact crown rest is stationary until disturbed. An author-drawn source figure is unverified and must not be promoted."},
 slider:{label:"Position θ from crown on exterior sphere (degrees)",min:0,max:85,step:5,value:35},
 ...task({
  prediction:"Could a bead leave a convex dome with POSITIVE speed? What happens first: its speed vanishes or normal contact reaches zero?",
  challenge:"TASK A: a 2 kg puck is placed at the TOP of a smooth EXTERIOR hemisphere of R=4 m and given a tangential downhill speed u=√20 m/s. Take g=10. Find its initial normal force and height above the sphere equator when N FIRST becomes zero. Explain why the familiar 2R/3 factor cannot be blindly reused.",
  model:pick("model","What equations describe contact until release?","Energy with initial speed, and exterior radial mg cosθ−N=mv²/R",["N+mg cosθ=mv²/R for an outside sphere","Detachment occurs only at speed zero"],"The exterior surface normal is OUTWARD; initial kinetic energy changes the detachment angle."),
  assumption:pick("assumption","Which surface constraint is physically used?","One-sided smooth exterior normal N≥0, no adhesion",["Captive wire can pull bead inward","Normal is fixed and never drops to zero"],"A smooth outside sphere cannot supply inward adhesive force.","INVALID_ASSUMPTION"),
  numbers:[
   num("initialN","Initial normal reaction (N)",10,.16,"N_top=m(g−u²/R)=2(10−20/4)=10 N.","RADIAL_SIGN"),
   num("height","First-release height above equatorial plane (m)",10/3,.05,"cosθ=(u²+2gR)/(3gR)=100/120=5/6; h=4×5/6."),
  ],
  reason:"Explain why initial speed shifts release upward and why no normal can become negative.",
  hints:["Start with energy v²=u²+2gR(1−cosθ).","For exterior contact write mg cosθ−N=mv²/R, with N≥0.","At release N=0. Solve 3gR cosθ=u²+2gR, then h=Rcosθ."],
  worked:[
   ["Establish contact at crown","At top N=m(g−u²/R)=2(10−20/4)=10 N>0; contact is initially feasible."],
   ["Include launch speed in energy","While on dome, v²=20+2(10)(4)(1−cosθ)."],
   ["Apply N=0 when exterior pushing ends","mg cosθ=mv²/R ⇒ 3gRcosθ=u²+2gR ⇒ cosθ=(20+80)/120=5/6."],
   ["Translate angle to height","h=Rcosθ=4×5/6=10/3≈3.333 m. The puck departs with nonzero speed; the post-detachment path is NOT circular."]
  ],
  boundary:"INCREASE initial speed to u=√(gR)=√40 m/s at the crown, with other data unchanged. What is the initial normal, and where does the puck first lose contact?",
  boundaryModel:pick("model","What happens at u²=gR on the exterior crown?","N=0 immediately at the top; no later on-sphere arc can be assumed",["The puck must slide down until h=2R/3","The normal becomes an inward pulling force"],"At the crown N=m(g−u²/R)=0 already."),
  boundaryNumbers:[num("normal","Normal force at initial crown (N)",0,.05,"m(g−gR/R)=0."),
                   num("height","Release height above equator (m)",4,.05,"Detachment is at the top, h=R.")],
  boundaryCheck:"At u²=gR=40, N_top=m(g−u²/R)=0, so first loss of contact is at the crown itself, height R=4 m. A larger u would need negative normal immediately and could not begin by following the smooth exterior sphere."
 }),
 transfer:task({
  label:"Task B · Marble released partway down a smooth convex playground dome",
  prediction:"If a marble is placed on the SIDE of an exterior dome rather than the crown, is the classic 2R/3 release height still universal?",
  challenge:"UNFAMILIAR SETTING: a marble starts from REST on the OUTSIDE of a smooth convex playground dome of R=3 m at θ₀=60° from the crown (not at the crown). It slides downward with g=10, no adhesion. Where does its normal first vanish, measured as HEIGHT above the equator? Is the crown-release formula still valid?",
  model:pick("model","What is the energy reference for release?","Use initial height Rcosθ₀; then exterior N=0 at a later angle",["Always use crown height R as start","Treat the playground dome as a captive track"],"Changing the release point changes available gravitational energy."),
  assumption:pick("assumption","What does a smooth convex surface guarantee?","Normal can only push outward while N≥0, not pull inward",["Adhesion holds the marble to any angle","A negative normal is acceptable without a tether"],"The surface loses contact when the needed normal reaches zero.","INVALID_ASSUMPTION"),
  numbers:[
   num("cos","Cosine of detachment angle from crown",1/3,.02,"From rest at θ₀=60°, v²=2gR(cosθ₀−cosθ). At N=0 solve 3cosθ=2cosθ₀.","RADIAL_SIGN"),
   num("height","Detachment height above equator (m)",1,.05,"h=Rcosθ=3×1/3."),
  ],
  reason:"Explain why the starting θ₀ enters energy but N=0 still defines contact loss.",
  hints:["Choose the actual initial vertical height Rcos60°, not R.","Use v²=2gR(cosθ₀−cosθ) and mg cosθ−N=mv²/R while in contact.","At N=0, 3cosθ=2cosθ₀=1; h=Rcosθ."],
  worked:[
   ["Reconstruct initial conditions","The marble starts with v=0 at θ₀=60°, height h₀=3cos60°=1.5 m above equator, not at 3m."],
   ["Use energy from that height","v²=2gR(cosθ₀−cosθ), where cosθ₀=½."],
   ["Find contact boundary","At N=0, gRcosθ=v²=2gR(½−cosθ), so 3cosθ=1 and cosθ=1/3."],
   ["Compute height","h=3×1/3=1 m. The crown-release answer 2R/3 would be 2 m and is WRONG for this different start."]
  ],
  boundary:"MOVE the rest starting angle to θ₀=30° from the crown, leaving the same R and no initial speed. What is the new release height? Why did the release condition change without changing the normal's SIGN constraint?",
  boundaryModel:pick("model","What controls changed release height?","Energy now starts from Rcos30°; N=0 remains the contact boundary",["Detachment stays at 1m independent of start","Contact must be lost only when speed reaches zero"],"Starting gravitational potential changes, while exterior N≥0 remains the same condition."),
  boundaryNumbers:[num("height","New detachment height (m)",Math.sqrt(3),.05,"cosθ_det=2cos30°/3=√3/3, so h=3×√3/3=√3.")],
  boundaryCheck:"For θ₀=30°, cosθ₀=√3/2. Detachment at cosθ=2cosθ₀/3=√3/3, giving h=3(√3/3)=√3≈1.732 m. The one-sided contact rule is unchanged; gravitational starting energy changed."
 })
};

const C6T={
 source:"EX-M36",title:"A string must stay taut at the top—not merely reach that height",short:"Vertical loop · minimum taut speed",
 question:"What extra condition decides whether a mass can finish a full vertical circle while attached to a STRING?",
 sourceCaution:"The source's 5:1 kinetic-energy ratio assumes a LIGHT INEXTENSIBLE STRING kept taut over the top at limiting T_top=0, with no losses. A rigid captive guide can push outward and needs a different admissibility test; reaching a top point is not always completing a moving loop.",
 prerequisites:"A point mass attached to a light string of length L rises 2L from bottom to top. Energy on a hypothetical taut path gives v_top²=u_bottom²−4gL. At top the centre is downward, so T+mg=mv_top²/L. Since a string cannot push, T≥0.",
 core:"Minimum top speed for a TAUT string satisfies v_top²≥gL, so u_bottom²≥5gL. The limiting top is T_top=0, v_top²=gL and ratio K_bottom/K_top=5 if energy is conserved. A captive rigid rail can supply a radial force of either sign and does not obey string-only T≥0.",
 guide:"GUIDED: 1 kg stone on a 1.5 m light string starts at bottom at 9 m/s, g=10. Hypothetical top v²=81−60=21 m²/s² and T_top=1(21/1.5−10)=4 N; it stays taut. Critical bottom speed is √(5gL)=√75≈8.660 m/s.",
 guideSteps:[
  ["Do not confuse height with complete motion","Energy determines whether kinetic energy can remain after climbing 2L. It does NOT determine whether a string can provide the needed inward force."],
  ["At top draw the inward arrow","At top inward points DOWN; both weight and a taut string tension point DOWN. Write T+mg=mv²/L."],
  ["Check a concrete climb","For L=1.5, g10, bottom u9, v_top²=9²−4(10)(1.5)=21. The top still has positive speed."],
  ["Calculate the tension's sign","T_top=m(v_top²/L−g)=1(21/1.5−10)=+4 N; the string can pull inward."],
  ["Locate the just-taut boundary","Set T_top=0 ⇒ v_top²=gL and u_bottom²=5gL. Below this bottom threshold a hypothetical taut trajectory becomes physically impossible before the apex."]
 ],
 wrong:"Wrong: equate u² to 4gL and claim the string completes the loop if energy can just reach the top. That ignores the required inward acceleration; a negative calculated tension means the STRING model has failed, not that it pushes outward.",
 conditions:"Ideal massless inextensible STRING, point mass, no external work or friction, stationary pivot, gravity constant; top at height 2L. Rigid captive rails and rods can exert both signs of radial force and require their own model. The boundary T_top=0 is a limiting taut-string case.",
 academic:{decision:"Make TWO checks: bottom-to-top energy and a nonnegative top tension. Then distinguish string, rod and captive rail.",
 observe:"Change bottom launch speed: the speed-squared remaining at top changes, and required top tension changes sign at u=√(5gL). Negative tension is a model-refusal signal.",
 validity:"The critical 5gL threshold is for a full ideal taut STRING path. For a captive rail with both-sided reaction, negative 'string tension' may be replaced by a physical outward guide force.",
 limit:"At u²=4gL, top speed would be zero but top STRING tension would be −mg; energy reachability alone is not enough. At u²=5gL, T_top=0 and v_top=√gL>0. Mass cancels in threshold speed.",
 sourceBoundary:"The source's 5:1 ratio is conditional on the string exactly taut at top with T_top=0 and no losses; a captive guide does not impose the same limit."},
 slider:{label:"Bottom launch speed u (m/s), string length 1.5m",min:0,max:13,step:.5,value:9},
 ...task({
  prediction:"If a ball has enough energy to REACH the top of a circle, must a string necessarily remain taut? What sign of top tension would disprove it?",
  challenge:"TASK A: a 2 kg ball tied to a light 2 m STRING moves vertically with g=10. At the lowest point it is launched at 11 m/s. Find hypothetical top speed squared and REAL top tension if the string remains taut; compare launch speed with the limiting √(5gL). Explain whether the model is feasible.",
  model:pick("model","What tests justify a full taut-string loop?","Energy plus nonnegative string tension at the top",["Energy reachability alone","String tension may be negative because the string can push"],"The inward top radial equation must pass T≥0 after the energy check."),
  assumption:pick("assumption","What radial force does the string permit?","Only inward pulling tension, T≥0",["A string can also push radially outward","A massive rod and string impose identical force conditions"],"A massless flexible string does not exert a compressive outward force.","INVALID_ASSUMPTION"),
  numbers:[
   num("v2","Top speed squared (m²/s²)",41,.5,"u²−4gL=121−80=41."),
   num("tension","Top string tension (N)",21,.35,"T=m(v²/L−g)=2(41/2−10)=21N.","RADIAL_SIGN"),
  ],
  reason:"Explain the inward direction, energy calculation, sign rule and how the minimum u²≥5gL differs from merely reaching the top.",
  hints:["Climb is 2L; energy gives v_top²=u²−4gL.","At top inward points down, so T+mg=mv²/L.","Check T=m(v_top²/L−g) is NONNEGATIVE, and compare u² with 5gL."],
  worked:[
   ["Energy for a hypothetical circle","v_top²=11²−4(10)(2)=41 m²/s², so top speed √41≈6.403 m/s."],
   ["Check top inward force","T+mg=mv²/L; T=2(41/2−10)=+21 N, a feasible pulling tension."],
   ["Find critical launch speed","The just-taut threshold u²≥5gL=100, so u≥10 m/s. Actual launch 11 m/s exceeds threshold."],
   ["Interpret what was proved","The string can remain taut through the top under the stated ideal conditions. This requires BOTH energy and radial feasibility."]
  ],
  boundary:"REDUCE bottom speed to √90 m/s with the same string and gravity. Energy would leave v_top²=10, but what top tension would the hypothetical circular path require? Does it remain taut?",
  boundaryModel:pick("model","What do you conclude from a NEGATIVE computed string tension?","The taut-path assumption fails; the string slackens before the top",["A negative tension is an acceptable pulling force","Positive top kinetic energy always proves a taut loop"],"A string cannot push outward to enforce the hypothetical path."),
  boundaryNumbers:[num("tension","Hypothetical top string tension (N)",-10,.25,"T=2(10/2−10)=−10N; flag invalid model, not a real force.")],
  boundaryCheck:"At u²=90, hypothetical top speed²=90−80=10. T_top=2(10/2−10)=−10 N, which a string cannot provide. It slackens before reaching the apex; energy alone permits the height but not a taut circular path."
 }),
 transfer:task({
  label:"Task B · Steel roller inside a rigid captive vertical loop",
  prediction:"Can a captive rigid groove push outward when a flexible string would go slack? Should both devices have the same minimum bottom speed?",
  challenge:"UNFAMILIAR SETTING: a 1 kg roller enters a smooth, rigid, mechanically CAPTIVE vertical circular groove of radius 2 m with bottom speed u=√90 m/s (g=10). At the top the groove can exert inward OR outward radial reaction. Calculate top speed squared and the required TOP track force magnitude and DIRECTION. Would the same initial motion work for an ideal STRING?",
  model:pick("model","What model distinguishes captive track from string?","A captive groove can exert either radial force sign; a string cannot push",["Use the string T≥0 condition for both devices","Energy alone decides the direction of top track force"],"A captive constraint can supply an outward/upward force, while a string can only pull inward."),
  assumption:pick("assumption","What is true about this track's contact?","Mechanically captive, smooth guide can push on both radial sides",["Only a unilateral inside-wall normal is available","The track supplies gravitational energy as the roller rises"],"The groove is two-sided and stationary; its reaction does no tangential work.","INVALID_ASSUMPTION"),
  numbers:[
   num("v2","Top speed squared (m²/s²)",10,.2,"u²−4gR=90−80=10."),
   num("force","Required UPWARD/outward track force magnitude at top (N)",5,.15,"Gravity contributes 10N inward; required inward mv²/R=5N, so groove supplies 5N outward.","RADIAL_SIGN"),
  ],
  reason:"Explain why a rigid captive groove can remain feasible even when the equivalent string requires negative tension.",
  hints:["Energy from bottom to top needs height gain 2R, regardless of which smooth guide enforces the path.","At top inward is DOWN. Required inward force is mv_top²/R=5N while gravity pulls down 10N.","The groove must push UP 5N. A flexible string cannot do that; track and string have different admissible force signs."],
  worked:[
   ["Use energy on the constrained path","v_top²=u²−4gR=90−80=10 m²/s²; top speed √10 m/s is positive."],
   ["Resolve the net radial force","At top inward DOWN, required net inward mv²/R=1×10/2=5 N. Gravity supplies 10 N downward."],
   ["Find outward guide reaction","The captive groove must push UPWARD 5 N to reduce inward net force to 5 N. Two-sided mechanical capture permits this."],
   ["Reject the string substitution","An ideal string would demand T=5−10=−5 N, impossible. Its path would go slack before apex despite positive kinetic energy."]
  ],
  boundary:"REPLACE the captive groove with a light flexible STRING of the same length and unchanged bottom launch speed u=√90 m/s. Can it follow a complete taut circle? State what sign of top tension its hypothetical path requires.",
  boundaryModel:pick("model","What changes when the rigid captive rail becomes a string?","String cannot provide required outward top force; taut circular path fails",["Identical energy guarantees identical contact feasibility","String can pull or push in both directions"],"The changed constraint changes which radial force sign is physically allowed."),
  boundaryNumbers:[num("tension","Hypothetical top tension (N)",-5,.1,"T=m(v²/R−g)=5−10=−5 N (impossible).")],
  boundaryCheck:"Same energy yields v_top²=10, but the STRING model at top demands T=mv²/R−mg=5−10=−5 N. Strings cannot push; before the top the trajectory stops being a taut circular path. The captive groove can provide the +5 N outward normal that the string cannot."
 })
};

const C6W={
 source:"EX-N11",title:"Work around a rough circular path belongs to the full path ledger",short:"Rough circular guide · work and loss",
 question:"Can we determine the TOTAL work of a rough tube from endpoints without knowing its friction force at every point? When is a local friction law necessary?",
 sourceCaution:"The original EX-N11 asks the NET work done by its tube, not a coefficient of friction. With initial top speed and final rest at bottom, W_tube=ΔK−W_g even if five revolutions/oscillations occurred. The path details matter for deriving a local friction law or individual lap losses; the author figure is not verified.",
 prerequisites:"Work–energy theorem: ΔK=W_g+W_normal+W_friction+W_other. An ideal constraint normal to instantaneous motion does ZERO work; a fixed rough tube's total work is from tangential friction/contact interactions. Gravity is conservative: W_g=mg(y_i−y_f). Friction can be position-dependent, W_f=−∫ f_t(s)ds, NOT simply −μmg times an arbitrary path.",
 core:"For a rough stationary circular tube, if only total work by tube is asked and endpoints are known: W_tube=(K_f−K_i)−mg(y_i−y_f). A count of loops does NOT alter gravitational work between the same heights. If given f_t(s) along a traveled distance, integrate its nonconservative work; without a force law you cannot infer a unique friction coefficient from a single work number.",
 guide:"GUIDED: a 2 kg block in a rough vertical closed circular channel (R=0.5 m) starts at top at 6 m/s and ends at rest at bottom after some path. g=10. Initial K=36 J; gravity adds 20 J across 1 m drop; tube must do −56 J total regardless of how many rotations were made.",
 guideSteps:[
  ["Choose the question's requested quantity","TOTAL work by the tube is one number. A local friction-versus-position force law is a different, stronger question."],
  ["Use only observable endpoints for ΔK","K_i=½(2)(6²)=36 J; final K_f=0, so ΔK=−36 J."],
  ["Count only net height change for gravity","Top to bottom height drop is 2R=1 m. Gravity work +mg(1m)=+20 J, not +20 J per lap."],
  ["Solve total tube work","ΔK=W_g+W_tube, giving −36=+20+W_tube ⇒ W_tube=−56 J."],
  ["Know what cannot be inferred","No specified μ, local wall normal, speed history or friction law. 'Five laps' does NOT prove constant per-lap friction or let us infer μ uniquely."]
 ],
 wrong:"Wrong: multiply gravitational work by five revolutions, or assume tube work −μmg·distance when normal reaction depends on radial speed and position. Another wrong path sets friction to 0 because normal work vanishes: the tube can do NONZERO tangential friction work.",
 conditions:"Fixed rough closed channel, block's endpoints and speeds known, gravity uniform, normal perpendicular to travel, any other external work excluded. For local friction force integrate actual tangential magnitude over actual arclength; the number of turns alone does not specify that force.",
 academic:{decision:"Decide whether the task asks total work by the tube (endpoint ledger) or needs local work distribution (requires force law). Do not invent μ from laps.",
 observe:"Visual slider represents extra completed laps while initial/final HEIGHTS stay fixed; gravity endpoint work does NOT accumulate per lap. Frictional loss can depend on path and dynamics.",
 validity:"Rigid stationary guide normal work zero; tube friction generally nonconservative. If a motor or moving guide performs extra work, include it separately.",
 limit:"Same initial/final heights ⇒ W_g=0 regardless of winding count. For a horizontal circle with known friction f_t(s), W_f=−∫f_t(s)ds. Without f_t(s), per-lap friction force cannot be deduced.",
 sourceBoundary:"Source total W_tube=−245 J follows from its conditional start/end states and no other work. The five-oscillation wording does NOT authenticate any friction coefficient or a constant-work-per-lap law."},
 slider:{label:"Number of complete detours with same start/end heights",min:0,max:8,step:1,value:5},
 ...task({
  prediction:"If a moving puck loops several times but ends at the same final height, does gravity do extra work for every loop? What information determines the tube's total work?",
  challenge:"TASK A: a 0.5 kg capsule slides inside a ROUGH vertical circular tube of R=1 m, initially at TOP at 10 m/s and eventually at BOTTOM at 2 m/s. Gravity g=10; no motor acts. Find ΔK, work by gravity, and TOTAL work by the tube. Explain why the number of intermediate complete laps is unnecessary for this total.",
  model:pick("model","Which operation gives total tube work?","W_tube = ΔK − mg(y_i−y_f), regardless of detours",["Multiply gravity work by lap count","Tube has zero work because normal reaction is perpendicular"],"Friction is included in tube work; gravity depends on endpoint heights, not loop count."),
  assumption:pick("assumption","What is assumed about other energy transfers?","Stationary tube, normal work zero and no external motor work",["Unknown motor adds energy but tube work unchanged","Gravity can be multiplied by arbitrary lap count"],"A motor would require its own work term; no such work is supplied.","INVALID_ASSUMPTION"),
  numbers:[
   num("delta","Change in kinetic energy ΔK (J)",-24,.3,"½(0.5)(2²−10²)=−24 J.","SIGN_AND_ENERGY"),
   num("grav","Work by gravity (J)",10,.15,"Drop is 2R=2 m, so mg·2R=10 J."),
   num("tube","TOTAL work done by tube (J)",-34,.4,"W_tube=−24−10=−34 J."),
  ],
  reason:"Explain why gravity's work depends on height only, while rough-tube loss may depend on path, yet can still be recovered as a TOTAL.",
  hints:["Use ΔK=½m(v_f²−v_i²), with its sign.","Gravity work for TOP to BOTTOM is +mg(2R), independent of detours.","Solve ΔK=W_g+W_tube. Do not invent a μ or force distribution."],
  worked:[
   ["Kinetic change","ΔK=½(0.5)(4−100)=−24 J."],
   ["Gravity's endpoint work","Height falls by 2R=2 m, so W_g=(0.5)(10)(2)=+10 J, not multiplied by loops."],
   ["Tube's total work","W_tube=ΔK−W_g=−24−10=−34 J. Ideal normal contributes zero; rough-contact tangential work accounts for loss."],
   ["Interpret what is NOT known","A detailed f_t(s), μ or per-lap loss cannot be recovered without force/normal and motion information. TOTAL work is fully determined by specified endpoints."]
  ],
  boundary:"KEEP initial speed 10 m/s and m=0.5 kg, but the capsule eventually stops at its original TOP height rather than the bottom. Gravity's net work is now zero. What is tube TOTAL work? State why no lap count appears.",
  boundaryModel:pick("model","What is gravity's work between equal start/end heights?","Zero regardless of how many turns were made",["Positive mg2R for every lap","Negative because the tube is rough"],"Gravity is conservative even when the tube is rough."),
  boundaryNumbers:[num("tube","New total work by tube (J)",-25,.3,"K_i=25 J, final K=0, and ΔU_grav=0, so W_tube=−25J.")],
  boundaryCheck:"At equal starting and ending heights, gravity's work is zero despite any laps. Initial K=½0.5·100=25 J, final zero. Therefore total tube work=−25 J. The work distribution along laps is still unknown."
 }),
 transfer:task({
  label:"Task B · Horizontal circular laboratory groove with measured drag law",
  prediction:"Can a circular guide do negative work even if its perpendicular normal does none? What if tangential friction grows with distance traveled?",
  challenge:"UNFAMILIAR SETTING: a 1 kg puck travels in a stationary smooth-WALL but tangentially RESISTIVE HORIZONTAL circular lab groove (radius 3 m). Starting at 8 m/s it travels 4 m of arc. A sensor measures tangential resistance f_t(s)=2+s NEWTONS, where s is distance traveled in METRES from the start, 0≤s≤4. No other tangential force acts. Find friction work and speed after 4 m. Decide whether to multiply a single friction value by the distance or integrate.",
  model:pick("model","How should distance-varying resistance be treated?","Integrate negative tangential work −∫₀⁴(2+s)ds",["Assume uniform 2N drag over all 4m","Use normal centripetal force times the 4m arc length"],"The recorded tangential resistance changes with s; radial normal force does no work."),
  assumption:pick("assumption","Which physical forces do work along the horizontal groove?","Only measured tangential resistance; normal perpendicular; gravity vertical",["Radial reaction does work along the circular tangent","Gravity contributes a vertical height drop around a horizontal circle"],"Along horizontal motion, both gravity and radial constraint reaction are perpendicular to displacement.","INVALID_ASSUMPTION"),
  numbers:[
   num("work","Friction work over 4m (J)",-16,.2,"W_f=−[2×4+4²/2]=−16J.","INTEGRAL_AND_SIGN"),
   num("speed","Final puck speed (m/s)",Math.sqrt(32),.08,"K_i=½(1)8²=32J; K_f=16J ⇒ v_f=√32 m/s."),
  ],
  reason:"Explain why the drag must be integrated and why radial normal force and gravity do zero work.",
  hints:["The force acts opposite motion, so work is negative. Is its magnitude constant along the arc?","Integrate ∫₀⁴(2+s)ds=2s+s²/2 evaluated at endpoints.","Use ½m(v_f²−v_i²)=W_f. Do not mistake radial centripetal force for tangential drag."],
  worked:[
   ["Choose the arc coordinate","Tangential resistance is f_t(s)=2+s N along 0≤s≤4 m. Work W_f=−∫₀⁴ f_t(s)ds."],
   ["Integrate the varying resistance","W_f=−[2s+s²/2]₀⁴=−(8+8)=−16 J."],
   ["Identify other work","The path is horizontal; gravity is vertical, and the stationary groove normal is radial. Both are perpendicular to displacement and contribute zero work."],
   ["Recover kinetic energy","Initial K=½(1)(8²)=32 J. Final K=32−16=16 J, giving v_f=√(2×16)=√32≈5.657 m/s."]
  ],
  boundary:"REPLACE the varying drag with CONSTANT 3 N opposite motion along the same 4m segment. Compute new total drag work and final speed. Explain why the old integral is no longer the relevant force model.",
  boundaryModel:pick("model","What work model applies when measured drag is constant?","W=−f·s with f=3N for the entire 4m",["Reuse previous −16J because circular path is unchanged","Apply normal force multiplied by arc length"],"Constant drag means a different work integral: −3×4, not the previous varying-law result."),
  boundaryNumbers:[num("work","New drag work (J)",-12,.18,"−3N×4m=−12J."),
                   num("speed","New final speed (m/s)",Math.sqrt(40),.08,"K_f=32−12=20J; v²=40.")],
  boundaryCheck:"With constant f_t=3N, W_f=−3×4=−12 J and K_f=32−12=20 J. Hence v_f=√(2×20)=√40≈6.325 m/s. The old −16J belonged to a different measured force-versus-distance law."
 })
};

const scenarios={C6S,C6A,C6H,C6T,C6W};
const NS="http://www.w3.org/2000/svg";
const nice=n=>Number.isFinite(n)?Math.round(n*1000)/1000:"undefined";
function diagram(id,value,{host,readout,svg,svgLine}){
  const tx=(x,y,s)=>svg(host,"text",{x,y,fill:"#23566a","font-size":14,"font-weight":"600"},s);
  const r=100,cx=318,cy=136;
  svg(host,"circle",{cx,cy,r,fill:"none",stroke:"#5b96a4","stroke-width":4});
  const a=value*Math.PI/180;
  if(id==="C6S"){
    const x=cx+r*Math.sin(a),y=cy-r*Math.cos(a);
    svg(host,"circle",{cx:x,cy:y,r:11,fill:"#e59b74"});
    svg(host,"circle",{cx,cy:cy+r,r:6,fill:"#3f667c"});
    svgLine(host,cx,cy,x,y,"#a7a7bc",2);
    svgLine(host,cx,cy+r,x,y,"#d88942",4);
    const d=2*Math.cos(a/2),h=1+Math.cos(a);
    tx(23,52,"R is always bead-to-CENTRE");
    tx(22,81,"Bottom peg is spring anchor");
    tx(24,113,"θ from TOP: "+nice(value)+"°");
    readout.textContent="R=1: bead-to-centre radius stays 1m; spring chord="+nice(d)+"m; height from bottom="+nice(h)+"m; with rest length 1m the spring extension is "+nice(d-1)+"m. Captive guide is an assumption.";
  }else if(id==="C6A"){
    const x=cx+r*Math.sin(a),y=cy+r*Math.cos(a);
    svgLine(host,cx,cy,x,y,"#1f7186",3);
    svg(host,"circle",{cx:x,cy:y,r:10,fill:"#d49e62"});
    svgLine(host,x,y,x+38,y,"#d09a48",3);
    tx(26,51,"Tangent and radius differ");
    tx(25,81,"Release θ from BOTTOM");
    tx(25,111,"θ="+nice(value)+"°");
    const ext=10*Math.sin(a),bottom=20*(1-Math.cos(a));
    readout.textContent="At release extreme: radial a=0, tangential |a|="+nice(ext)+" m/s². At lowest point after release: tangential a=0, radial a="+nice(bottom)+" m/s². Neither is a universal total-acceleration formula.";
  }else if(id==="C6H"){
    const x=cx+r*Math.sin(a),y=cy-r*Math.cos(a);
    svg(host,"circle",{cx:x,cy:y,r:10,fill:"#dd9273"});
    svgLine(host,cx,cy,x,y,"#55738a",2);
    svgLine(host,x,y,x+Math.sin(a)*32,y-Math.cos(a)*32,"#bf7f40",4);
    tx(22,51,"Exterior dome: normal OUTWARD");
    tx(22,81,"Gravity inward component mg cosθ");
    const ratio=3*Math.cos(a)-2,det=Math.acos(2/3)*180/Math.PI;
    readout.textContent="Perturbed crown-rest LIMIT: N/(mg)="+nice(ratio)+" at θ="+value+"°. It reaches zero at θ≈"+nice(det)+"°, where height=2R/3. For N<0 the assumed exterior contact is impossible (bead leaves).";
  }else if(id==="C6T"){
    const x=cx,y=cy-r;
    svg(host,"circle",{cx:x,cy:y,r:11,fill:"#c68c64"});
    svgLine(host,cx,cy,x,y,"#3a7489",3);
    tx(22,52,"Taut STRING at top: T>=0");
    tx(22,82,"v_top²=u_bottom²−4gL");
    const L=1.5,g=10,v2=value**2-4*g*L,T=v2/L-g;
    readout.textContent="Bottom u="+nice(value)+" m/s: hypothetical v_top²="+nice(v2)+" m²/s²; required top tension for 1kg="+nice(T)+"N. Negative value means the STRING CANNOT stay taut (not a real compressive tension).";
  }else{
    svg(host,"circle",{cx,cy,r:r-10,fill:"none",stroke:"#8f9f9e","stroke-width":6,opacity:.4});
    svg(host,"circle",{cx:cx,cy:cy-r,r:10,fill:"#bb8c53"});
    tx(22,51,"Vertical circle: gravity is endpoint work");
    tx(22,81,"Tube friction is path-dependent");
    tx(22,111,"Extra completed laps: "+value);
    readout.textContent="For the guided block start TOP and finish BOTTOM, gravitational work remains +20 J even after "+value+" complete detours. Total tube work=−56 J from endpoints. The local friction per lap cannot be inferred without its law.";
  }
}
for(const [id,d] of Object.entries(scenarios)){
 d.modelView=(v,ctx)=>diagram(id,v,ctx);
 if(!d.transfer?.fields||d.fields.length<4||d.transfer.fields.length<4||!d.academic)throw Error("C06 construction incomplete "+id);
}
/* First A and B attempt keys are scoped under g9:wpe:c06-r4:v1; merged F04–F08
   practice data is intentionally untouched. */
if(typeof window.WPEGapJourneys!=="function")throw Error("Existing six-stage student renderer is required");
window.WPEGapJourneys(scenarios,{storagePrefix:"g9:wpe:c06-r4:v1:",coveragePath:"learning-coverage-r1.json"});
})();