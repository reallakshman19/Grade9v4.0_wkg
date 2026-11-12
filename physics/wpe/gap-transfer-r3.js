/* Academic-only strengthening for merged F04–F08.
 * This is a declarative, source-independent second transfer for each original
 * Core1B lesson, NOT a new learner engine, gateway or Question Bank edit.
 * Each T2 uses the original six-stage state machine and its own immutable
 * local first response. Unreviewed written explanations are not auto-graded.
 */
(() => {
"use strict";
const model=(label,expected,choices,mistake)=>({
 id:"model",label,type:"select",choices:["Choose an idea",...choices,"I'm not sure yet"],
 expected,mistake,errorKind:"MODEL_CHOICE"
});
const assumption=(label,expected,choices,mistake)=>({
 id:"assumption",label,type:"select",choices:["Choose an idea",...choices,"I'm not sure yet"],
 expected,mistake,errorKind:"INVALID_ASSUMPTION"
});
const number=(id,label,expected,tol,mistake,errorKind="CALCULATION_OR_UNITS")=>({
 id,label,type:"number",expected,tol,mistake,errorKind
});
const why=(label)=>({id:"reason",label,type:"textarea"});
const changedWhy=(label)=>({id:"why",label,type:"textarea"});
window.WPE_R3_CONTENT={
F04:{
 academic:{
  decision:"What can the spring actually change? An INTERNAL spring changes separation; it cannot erase centre-of-mass momentum without outside impulse. Write velocities with signs, then split K = ½MV² + ½μ(u₁−u₂)².",
  observe:"Move the guided pair's common-drift slider. The two signed speeds and COM velocity change, while the relative speed and maximum stretch do not. At the relative turning point both blocks keep moving with the SAME COM velocity.",
  validity:"Measure which block is to the LEFT and which to the RIGHT; the sign of u₁−u₂ determines whether the spring is initially stretching or compressing. The original and first task use natural-length springs, with no outside horizontal work or friction. A preloaded spring adds initial potential energy.",
  limit:"With equal speeds, relative kinetic energy is zero even if both bodies race across the floor. As k→∞ for fixed relative energy, the displacement tends to zero. For the original one-moving-block test (m=0.25 kg each, k=2 N/m), the scientifically correct stretch is v/4; the inherited source CHECK suggesting v/(2√2) is inconsistent.",
  sourceBoundary:"The source's equal-and-opposite, zero-COM answer is conditional. It must not be generalized to one moving block, nonzero COM, external force or a prestrained spring."
 },
 originalAssumption:assumption("Which condition lets the INITIAL relative kinetic energy become spring energy?",
 "An initially relaxed spring with no external horizontal work",
 ["An initially relaxed spring with no external horizontal work",
  "Any common COM motion will stop at peak extension",
  "An outside brake removes an unknown amount of energy"],
 "For the original fresh problem the spring starts at natural length and the pair is horizontally isolated. Do not erase common drift."),
 transfer:{
  label:"Task B · Two ice skaters approaching (unfamiliar compression setting)",
  prediction:"Two skaters move toward one another and compress their shared spring. At peak compression, must they both stop, or only stop approaching each other? What motion remains?",
  challenge:"UNFAMILIAR SETTING. Two skaters on nearly frictionless ice wear a lightweight compressible spring bumper. Skater A is LEFT of B, mass 2 kg and velocity +3 m/s (right); B has mass 4 kg and velocity −1 m/s (left). Spring k=24 N/m, initially uncompressed. No one pushes on the ice during contact. Positive is RIGHT. Decide which energy compresses the bumper, then calculate signed COM velocity, relative energy and FIRST maximum compression.",
  fields:[
   model("Which kinetic-energy ledger can increase internal spring compression?",
    "Relative motion while COM drift persists",
    ["Relative motion while COM drift persists","Total kinetic energy because both skaters stop","Kinetic energy of skater A only"],
    "Only the relative speed vanishes at peak compression. Common COM drift cannot disappear without an external impulse."),
   assumption("What must hold while the skaters compress the bumper?",
    "No external horizontal work; spring initially relaxed",
    ["No external horizontal work; spring initially relaxed",
     "Friction removes an unknown fraction, but we may ignore it",
     "Both bodies are at rest in the ground frame at peak compression"],
    "State the horizontal-isolation and initial-strain assumptions before the relative-energy equation."),
   number("com","SIGNED common COM velocity at peak compression (m/s, right positive)",1/3,.016,
    "Use (2×(+3)+4×(−1))/6. If you obtain a negative sign, check which skater started left and the direction of B.","SIGN_OR_REFERENCE_FRAME"),
   number("relative","Initial kinetic energy available to compress the spring (J)",32/3,.12,
    "Compute μ=(2×4)/6=4/3 kg and relative speed 3−(−1)=4 m/s; Krel=½μw²."),
   number("compression","First maximum compression (m)",Math.sqrt(8/9),.016,
    "Set ½(24)x² equal to available relative energy, NOT total kinetic energy."),
   why("Explain which motion remains at peak compression, why the signs are chosen, and why your conservation law applies.")
  ],
  hints:[
   "Imagine filming BOTH skaters from a camera moving with their common centre of mass. Which motion still squeezes the spring?",
   "Signed velocities matter: A is moving right while B moves left. At peak compression both share one common velocity, not zero.",
   "Compute V=(m_Au_A+m_Bu_B)/(m_A+m_B), μ=m_Am_B/(m_A+m_B), Krel=½μ(u_A−u_B)², then ½kx²=Krel."
  ],
  worked:[
   ["COM drift and signed momentum","Total momentum is 2(+3)+4(−1)=+2 kg·m/s. Total mass 6 kg, so V=+1/3 m/s. The pair keeps drifting RIGHT at maximum compression."],
   ["Isolate the internal energy","Reduced mass μ=(2×4)/6=4/3 kg. Relative speed is +3−(−1)=+4 m/s; Krel=½(4/3)(16)=32/3≈10.667 J."],
   ["Check the full ledger","Total Kinitial=½(2)(3²)+½(4)(1²)=11 J. COM K=½(6)(1/3)²=1/3 J. The remaining 32/3 J is exactly the available relative energy."],
   ["Compression, not extension","½(24)x²=32/3 gives x=√(8/9)≈0.943 m. Skaters share velocity +1/3 m/s at the internal turning point; both do NOT stop."]
  ],
  boundary:"CHANGED CONDITION: the same skaters approach with identical velocities, but the spring bumper is ALREADY compressed by 0.20 m when the motion is specified. There is no loss. What additional initial spring energy must be included, and what is the FIRST maximum compression measured from natural length?",
  boundaryFields:[
   model("Which spring-energy ledger applies when there is initial compression?",
    "Initial relative kinetic energy PLUS preloaded spring energy",
    ["Initial relative kinetic energy PLUS preloaded spring energy",
     "Relative kinetic energy alone, because initial spring compression is irrelevant",
     "Total initial ground-frame kinetic energy only"],
    "A preloaded spring already stores ½kx₀². Include it in the relative-system energy budget."),
   number("preload","Initially stored spring energy (J)",.48,.012,
    "Initial compression 0.20 m stores ½(24)(0.20)² J."),
   number("compression","Maximum compression from natural length (m)",Math.sqrt(209)/15,.018,
    "Set ½kx_max²=Krel+½k(0.20)², and keep common COM energy out."),
   changedWhy("Explain why preloading changes the maximum compression but does not alter the conserved horizontal COM momentum.")
  ],
  boundaryCheck:"Initial relative KE=32/3 J, spring preload=½(24)(0.20²)=0.48 J. Thus ½(24)x_max²=32/3+0.48=836/75 J; x_max=√209/15≈0.9638 m. COM drift is still +1/3 m/s because an internal spring cannot change total horizontal momentum."
 }
},
F05:{
 academic:{
  decision:"Do we KNOW the whole spring's velocity field? One measured tip speed never determines the kinetic energy of a massive spring. The one-sixth rule needs an observed/assumed AFFINE field v(y)=v_tip y/L as well as uniform mass per length.",
  observe:"The slice slider changes N, not total mass. Each equally massive strip receives its OWN midpoint speed. Compare N=1,4,32; the midpoint sum approaches the continuum from below while total mass stays fixed.",
  validity:"The wall end is motionless; a stretched fraction s=y/L moves at s v_tip; mass density per instantaneous length is uniform. A moving support adds a nonzero base speed. A wave-shaped velocity field changes the integral even if both endpoint speeds remain the same.",
  limit:"At v_tip=0 the affine field has K=0. With a moving left endpoint u and right endpoint v, affine K=m(u²+uv+v²)/6; if u=v, the uniform-translation limit is ½mv², NOT mv²/6.",
  sourceBoundary:"The original source states a uniform wire and free-end uniform speed, but the linear INSTANTANEOUS velocity profile is a modeling assumption, not a rigorous consequence of tip speed alone. Elastic waves can violate it."
 },
 originalAssumption:assumption("Which observation is required before using the one-sixth factor?",
 "Fixed wall, uniform mass density and a linear local speed profile",
 ["Fixed wall, uniform mass density and a linear local speed profile",
  "Only the tip speed; interior speed distribution is irrelevant",
  "Any vibrating spring has exactly this speed profile"],
 "Both the fixed-end condition and the linear velocity profile are required; neither follows merely from one end moving."),
 transfer:{
  label:"Task B · Stretching safety cord with measured speed profile",
  prediction:"A long safety cord is being pulled at one end. Can its mass all be assigned the free-end speed? What would a point near the anchored end do?",
  challenge:"UNFAMILIAR SETTING. A uniform 3.0 kg elastic safety cord is clamped at a building on its left. At one instant a camera measures its axial speed to be v(s)=6s m/s, where s is fractional distance from the fixed end, 0≤s≤1. Calculate speed at s=¼, the continuum kinetic energy of the CORD, and the midpoint-slice estimate using N=6 equal-mass strips. Explain why measuring the spatial field—not only tip speed—licenses your result.",
  fields:[
   model("What must be integrated to find the cord's kinetic energy?",
    "Local kinetic energy of each mass slice at its measured speed",
    ["Local kinetic energy of each mass slice at its measured speed",
     "Entire cord at the 6 m/s tip speed",
     "Cord mass times the square of its average speed"],
    "The physical observable is a velocity field. Sum ½dm·v(s)², not ½m times the squared average speed."),
   assumption("What makes the simple integration in s valid?",
    "Uniform mass per instantaneous length; observed linear speed field",
    ["Uniform mass per instantaneous length; observed linear speed field",
     "An arbitrary standing wave still has linear internal speeds",
     "Only the two end velocities matter; internal profile need not be measured"],
    "Uniform mass determines dm=m ds, and a measured linear profile determines v(s)."),
   number("quarter","Cord speed at s=¼ (m/s)",1.5,.024,
    "Evaluate the measured field v(¼)=6×¼. Do not substitute the tip speed.","SPATIAL_REPRESENTATION"),
   number("energy","Continuum cord kinetic energy (J)",18,.15,
    "½m∫₀¹(6s)²ds = ½(3)(36)/3. Check the unit is joules."),
   number("slices","Midpoint 6-slice kinetic-energy estimate (J)",143/8,.16,
    "For six slices, each has mass 3/6 kg and midpoint speeds v_j=6(j+½)/6; square each speed, then sum."),
   why("Explain the meaning of s and how the slice sum approaches the integral without assuming every segment shares the tip speed.")
  ],
  hints:[
   "Visualize six equal-mass strips. The one against the wall is almost stationary; the free end is fastest.",
   "A slice at fractional location s has mass dm=m ds. For N slices use s_j=(j+½)/N rather than an endpoint velocity.",
   "Use K=½m∫₀¹[6s]²ds. For the six midpoint slices add ½(3/6)Σ[6(j+½)/6]²."
  ],
  worked:[
   ["Measured kinematics","s=y/L is distance fraction from fixed wall. At s=¼, v=6(¼)=1.5 m/s. The fixed end has 0; tip has 6 m/s."],
   ["Continuum energy","Uniform mass gives dm=3ds. K=½(3)∫₀¹(6s)²ds=54/3=18 J. This follows from the OBSERVED field, not merely the tip speed."],
   ["Finite midpoint slices","For N=6, 6 equal strips of mass 0.5 kg have midpoint speeds (j+½) m/s, j=0…5. K₆=½(0.5)Σ(j+½)²=(¼)(71.5)=17.875 J."],
   ["Interpret difference","The midpoint sum 17.875 J is slightly BELOW the true 18 J because s² is convex. Treating all 3 kg as moving at 6 m/s would yield 54 J, three times too high."]
  ],
  boundary:"CHANGED PHYSICAL MODEL: the cord has the SAME total mass 3 kg, fixed left end and tip speed 6 m/s, but a camera now measures v(s)=6s² instead of 6s (non-affine wave-like deformation). Find the new continuum kinetic energy and kinetic-equivalent tip mass. Why is the fixed-end one-sixth shortcut no longer justified?",
  boundaryFields:[
   model("How should the new wave-shaped speed field be treated?",
    "Integrate the newly measured square-of-speed profile",
    ["Integrate the newly measured square-of-speed profile",
     "Tip speed unchanged, so K must still be mv²/6",
     "All strips now move at tip speed"],
    "Equal endpoint speeds do not uniquely determine the internal speed field or total kinetic energy."),
   number("energy","New cord kinetic energy (J)",10.8,.14,
    "Use K=½(3)∫₀¹(6s²)²ds and ∫₀¹s⁴ds=1/5."),
   number("equivalent","Effective tip-speed mass (kg)",.6,.024,
    "Solve ½m_eff(6²)=K. The physical cord still weighs 3 kg."),
   changedWhy("Explain what the camera's nonlinear speed field disproves about using mv²/6 universally.")
  ],
  boundaryCheck:"v(s)=6s² gives mean-square speed 36∫s⁴ds=36/5. K=½(3)(36/5)=10.8 J. Relative to a 6 m/s tip, m_eff=2K/36=0.6 kg=m/5. The physical mass stays 3 kg. One-sixth is ONLY the linear-field result."
 }
},
F06:{
 academic:{
  decision:"For POWER, choose a time window first. In 1 s, new fluid crosses a fixed area: volume=A(v·n)Δt, mass=ρAvΔt. Every kilogram carries ½v² J/kg. Multiply kg/s by J/kg to produce W, then apply a fixed conversion fraction.",
  observe:"Move the wind-speed control. The drawn air column grows longer, mass flow increases linearly, and energy per kilogram increases quadratically. The electrical output grows cubically ONLY while ρ, A and η remain unchanged.",
  validity:"Steady uniform velocity normal to a fixed collection area; constant ρ, A, and η; only the incoming flow's kinetic energy is counted. Real extraction, pressure change, direction, blade pitch and performance curves can spoil this model.",
  limit:"With v→0 the kinetic power tends to zero. Halving cross-sectional area at fixed v halves the output. Doubling v gives eightfold only if A, ρ and efficiency remain fixed.",
  sourceBoundary:"Original v³ is a model prediction under the specified fixed fraction and wind interception; it does not certify actual turbine operation at cut-in, rated or shut-down speeds."
 },
 originalAssumption:assumption("Which conditions keep the v³ comparison valid?",
 "Constant density, swept area and efficiency; flow crosses the area",
 ["Constant density, swept area and efficiency; flow crosses the area",
  "Fixed air packet mass per second irrespective of speed",
  "Rotor area shrinks with increasing speed"],
 "One factor of v enters through rate of NEW mass, so compare equal areas, densities and conversion fractions."),
 transfer:{
  label:"Task B · Micro-hydroelectric current harvester",
  prediction:"A river generator sits in a steady water current. When the flow speeds up, what happens to the number of new kilograms crossing its opening each second?",
  challenge:"UNFAMILIAR SETTING. A micro-hydro device intercepts a steady water current perpendicular to a 0.25 m² intake. Density=1000 kg/m³, speed=2 m/s and it converts a constant 20% of the intercepted fluid's KINETIC energy flux into electrical power. There is no additional elevation or pressure head in this ideal model. Find intercepted mass rate, kinetic energy carried by each kilogram, and electrical output. Justify the physical power scaling, not merely the exponent.",
  fields:[
   model("Which product represents current kinetic power through the intake?",
    "Mass passing per second times kinetic energy per kilogram",
    ["Mass passing per second times kinetic energy per kilogram",
     "Kinetic energy of one fixed water packet irrespective of time",
     "Momentum flow ρAv² used directly as watts"],
    "Power is J/s, not joules of one packet and not force. ṁ in kg/s times ½v² in J/kg gives W."),
   assumption("What makes the simple intake formula physically applicable?",
    "Steady flow normal to fixed intake area; constant density and efficiency",
    ["Steady flow normal to fixed intake area; constant density and efficiency",
     "Water also descends an unknown vertical head that we ignore when computing TOTAL power",
     "Intake area changes with speed but its change is irrelevant"],
    "No unspecified pressure/head energy may silently enter a kinetic-only power estimate; use the normal velocity component."),
   number("flow","Intercepted water mass each second (kg/s)",500,4,
    "The moving 1-second column is 0.25×2 m³; multiply by 1000 kg/m³.","AREA_AND_RATE_REPRESENTATION"),
   number("specific","Kinetic energy per kilogram of current (J/kg)",2,.04,
    "Each kilogram brings ½(2²)=2 J/kg of kinetic energy; do not multiply density here."),
   number("power","Electrical output (W)",200,3,
    "Kinetic flux is 500 kg/s × 2 J/kg =1000 W; multiply by 0.20 to obtain output."),
   why("Explain why mass rate scales with v, specific energy with v² and when power cannot follow a v³ law.")
  ],
  hints:[
   "Draw the water column entering in exactly ONE second. Its length is speed × one second.",
   "Multiply rho by A by v to count kilograms each second; calculate ½v² J per kilogram separately.",
   "Use P_elec=ηṁ(½v²), and check the units kg/s × J/kg = W."
  ],
  worked:[
   ["Choose the mass boundary","In 1 s, volume=(0.25 m²)(2 m)=0.50 m³. At density 1000 kg/m³, ṁ=500 kg/s."],
   ["Calculate energy per unit mass","½v²=½(2²)=2 J/kg. This differs from mass rate; a water parcel with more speed carries more joules."],
   ["Convert to rate and useful output","Incoming kinetic power=500×2=1000 J/s. At constant η=0.20, electrical output=200 W."],
   ["Recover universal structure, not universal efficiency","P=½ηρAv³ under stated fixed A, ρ and η and a normal incoming flow. The fluid is WATER rather than WIND, but the kinetic-flux reasoning transfers."]
  ],
  boundary:"CHANGED ENVIRONMENT: speed becomes 3 m/s while physical intake area shrinks to 0.10 m². Density 1000 kg/m³ and η=20% remain fixed. Determine new electrical output and its RATIO to the original 200 W. Why is cubing the speed ratio alone wrong?",
  boundaryFields:[
   model("Which variables belong in the new comparison?",
    "New swept area AND new speed both alter kinetic flux",
    ["New swept area AND new speed both alter kinetic flux",
     "Only speed matters in a v³ rule even if intake area changes",
     "Mass arriving each second stays 500 kg/s"],
    "The cube relation is for constant area. Here use P_new/P_old=(A_new/A_old)(v_new/v_old)³."),
   number("power","New electrical output (W)",270,4,
    "Compute ½(0.20)(1000)(0.10)(3³)."),
   number("ratio","New output / old output",1.35,.025,
    "Apply BOTH factors: (0.10/0.25)×(3/2)³."),
   changedWhy("Explain how the reduction in intercepted area offsets the faster flow and why water pressure/head is excluded.")
  ],
  boundaryCheck:"New mass flow is 1000×0.10×3=300 kg/s, energy per kg=½(3²)=4.5 J/kg. Incoming kinetic flux=1350 W, so electrical output=0.20(1350)=270 W. Ratio=270/200=1.35, equivalently (0.10/0.25)(3/2)³=0.4×3.375=1.35."
 }
},
F07:{
 academic:{
  decision:"Define the event! 'Stops for an instant at the farthest angle' constrains ΔK=0, NOT acceleration=0. With CONSTANT horizontal F, use the horizontal displacement and gravitational height. 'Held at this angle' constrains TANGENTIAL net force=0. They are different experiments.",
  observe:"Move the target-angle slider. The visual distinguishes the two force outputs, both for the same bob angle. For small angles their ratio approaches 1/2; they do not become identical. The string's tension does no work along the circular path.",
  validity:"Zero friction, light inextensible string or smooth circular guide, fixed pivot/track, horizontal force constant during the turning-point model and a start/end at rest. For static holding, zero tangential acceleration. If force varies with angle, endpoint force cannot be multiplied by the full displacement.",
  limit:"As θ→0 (radians), F_turn≈Mgθ/2 but F_hold≈Mgθ. At θ→90°, the constant-work turning force tends to Mg while static holding force diverges; near 90°, the ideal string/static geometry needs careful feasibility checks.",
  sourceBoundary:"The original 'force required to displace until 45°' does NOT uniquely tell us whether a constant-force first turning point or an equilibrium hold is intended. Keep both 45° answers visible, do not certify a single universal key."
 },
 originalAssumption:assumption("What separates the two original fresh-model experiments?",
 "A: constant F, starts/ends at rest; B: instant static tangential balance",
 ["A: constant F, starts/ends at rest; B: instant static tangential balance",
  "A turning point automatically means zero acceleration",
  "The same force must hold the bob after a constant-force trip"],
 "The turning point has zero speed but generally nonzero tangential acceleration. Static hold needs zero acceleration."),
 transfer:{
  label:"Task B · Bead on a smooth circular track",
  prediction:"A bead can momentarily stop on a smooth hoop at a high point and then slide back. Does that mean forces on it are balanced at the instant of turning?",
  challenge:"UNFAMILIAR SETTING. A 0.50 kg bead travels on a smooth, rigid, vertical circular wire of radius 2.0 m. It starts at rest at the bottom. A CONSTANT rightward horizontal force carries it to its FIRST turning point at angle 30° from downward vertical. Separately, a rightward force can HOLD it statically at 30°. The track's normal reaction is perpendicular to motion and does no work; g=10. Choose the TWO appropriate models and calculate gravitational rise ΔU, constant turning-point force and static holding force. Explain why the forces differ.",
  fields:[
   model("Which pair of laws resolves these different experiments?",
    "Constant-force work for the turn; tangential balance for holding",
    ["Constant-force work for the turn; tangential balance for holding",
     "Tangential static balance in both cases because speed is zero at the turn",
     "One constant force must be the same for both experiments"],
    "Turning-point condition is zero FINAL velocity, not static equilibrium. Holding needs zero tangential acceleration."),
   assumption("What conditions allow the two clean calculations?",
    "Fixed smooth track; constant F in first trip; starts/ends at rest",
    ["Fixed smooth track; constant F in first trip; starts/ends at rest",
     "Track normal performs positive work while the bead moves",
     "The force changes with angle in the first trip, but endpoint force can be multiplied by total displacement"],
    "The track normal is perpendicular to motion, and the first trip needs a constant horizontal F."),
   number("rise","Gravitational potential-energy increase (J)",10-5*Math.sqrt(3),.04,
    "Vertical rise is R(1−cos30°); do not use horizontal Rsin30° for gravity.","GEOMETRY_AND_SIGN"),
   number("turn","CONSTANT horizontal force to reach the first 30° turn (N)",5*(2-Math.sqrt(3)),.04,
    "Use F·(Rsin30°)=MgR(1−cos30°), NOT instantaneous force balance."),
   number("hold","Horizontal force to HOLD bead at 30° (N)",5/Math.sqrt(3),.05,
    "Static tangent balance is Fcos30°=Mg sin30°; F=Mg tan30°."),
   why("Explain why the track normal does no work, why speed zero is not acceleration zero and which two distinct assumptions pick the formulas.")
  ],
  hints:[
   "Draw the bead's horizontal displacement and vertical height separately. A smooth circular track's normal force is perpendicular to the bead's velocity.",
   "For the FIRST turning point, the bead starts and ends at rest, so FΔx=MgΔh. That does NOT mean Fcosθ=Mg sinθ during the motion.",
   "For a held bead, resolve forces along the circle's tangent at θ=30°. Compare F_turn=Mg tan(θ/2) with F_hold=Mg tanθ."
  ],
  worked:[
   ["Geometry and track constraint","At 30°, horizontal displacement Δx=2sin30°=1 m. Height rise Δh=2(1−cos30°)=2−√3≈0.26795 m. The track normal does zero work."],
   ["Energy at first turn","ΔU=(0.5)(10)(2−√3)=10−5√3≈1.33975 J. Because ΔK=0 for start and first turn, Fturn(1m)=ΔU, so Fturn≈1.33975 N."],
   ["Equilibrium at 30° is a different case","Fhold cos30°=Mg sin30°, giving Fhold=5 tan30°=5/√3≈2.88675 N."],
   ["Physical difference","The constant-force turn is NOT held: the bead has nonzero tangential acceleration back toward the bottom at its endpoint. A continuously adjusted static holding force would have to vary with angle."]
  ],
  boundary:"CHANGED FORCE HISTORY. Instead of pushing with a constant F, an operator moves the SAME bead from 0 to 30° QUASI-STATICALLY, holding it near equilibrium at each intermediate angle with an angle-dependent horizontal force F(θ)=Mg tanθ. Find the INSTANTANEOUS horizontal force at 30° and the TOTAL horizontal work along the path. Is endpoint force times total Δx valid?",
  boundaryFields:[
   model("How do you compute work of the angle-dependent horizontal force?",
    "Integrate F(θ) times infinitesimal horizontal displacement dx",
    ["Integrate F(θ) times infinitesimal horizontal displacement dx",
     "Multiply the final 30° holding force by total horizontal displacement",
     "Use zero total work because the process is quasi-static"],
    "Quasi-static means negligible ΔK, not zero applied work. F varies, so integrate F(θ)dx."),
   number("endForce","Instantaneous horizontal force at 30° (N)",5/Math.sqrt(3),.05,
    "At each angle the required hold force is Mg tanθ, so use θ=30° for the endpoint only."),
   number("work","Operator's total horizontal work (J)",10-5*Math.sqrt(3),.04,
    "dx=R cosθ dθ. Thus ∫Fdx=∫Mg tanθ Rcosθ dθ=MgR(1−cos30°)."),
   changedWhy("Explain how a different force history can have the same endpoint height energy despite a different final instantaneous force.")
  ],
  boundaryCheck:"At 30°, instantaneous static force is 5tan30°=5/√3≈2.88675 N. During quasi-static motion F(θ)=5tanθ and dx=2cosθ dθ, so work W=∫₀³⁰°10sinθ dθ=10(1−cos30°)=10−5√3≈1.33975 J. Multiplying endpoint force by full 1 m gives ≈2.88675 J and is WRONG because the force was smaller earlier."
 }
},
F08:{
 academic:{
  decision:"First ask what energy the GIVEN friction claim refers to. '10% of wagon energy retained' is NOT the same as '10% of the 40,000 kg combined mass's energy stored'. The coached 1.6×10⁶ N/m uses the latter as an additional POSTULATE. A real two-body coupling needs separate masses, relative velocity and external braking work.",
  observe:"The guided retention slider changes only an ASSUMED whole-vehicle energy fraction and its conditional k; it does NOT animate the engine/wagon compression dynamics. Model B must instead use μ and relative velocity, which are different physical observables.",
  validity:"Whole-system fraction model only when explicitly stated as spring storage relative to entire initial KE. Two-body ideal model requires measured component masses/velocities, a relaxed massless spring and no external work. Braking forces can inject/remove RELATIVE energy even when total vehicle speed is known.",
  limit:"If both bodies have identical velocities and no external work, relative KE is zero, so a relaxed internal spring cannot compress. If initial relative speed→0 the ideal compression→0. With unknown external braking or damping, no unique compression or stiffness follows from total mass/speed.",
  sourceBoundary:"EX-N27's conditional k=1.6×10⁶ N/m is NOT a demonstrated unique engine/wagon mechanism. The phrase '90% of energy of wagon' cannot supply missing wagon mass, braking impulse, relative speed and residual COM energy."
 },
 originalAssumption:assumption("Which condition legitimizes the CURRENT fresh cart compression calculation?",
 "Both component masses and speeds known, no outside braking or internal damping",
 ["Both component masses and speeds known, no outside braking or internal damping",
  "Source coaching's 10% rule automatically applies to every coupling",
  "Only combined total mass is needed regardless of relative motion"],
 "Use an internal reduced-mass ledger only when the interaction is isolated and both component velocities are known."),
 transfer:{
  label:"Task B · Spacecraft docking through a compliant coupler",
  prediction:"Two spacecraft meet in space through a soft spring coupler. They continue drifting together after contact begins. Does the energy of their SHARED motion have to become spring compression?",
  challenge:"UNFAMILIAR SETTING. In deep space, a 200 kg spacecraft A approaches spacecraft B from the LEFT with velocity +4 m/s. B is to the RIGHT, mass 300 kg, initially stationary. An ideal massless spring coupler, stiffness k=9600 N/m, is initially relaxed. No thrusters fire and no damping acts during first compression. Positive is RIGHT. Find the common COM speed, initial RELATIVE kinetic energy and maximum coupler compression. Explain why the source's 10%-retention rule is irrelevant without that explicit assumption.",
  fields:[
   model("Which kinetic-energy model follows from this spacecraft scenario?",
    "Reduced-mass relative energy is available for the internal spring",
    ["Reduced-mass relative energy is available for the internal spring",
     "Ten percent of whole-system kinetic energy by the original wagon rule",
     "All of the ground-frame kinetic energy becomes spring energy"],
    "The ideal pair has no specified friction fraction; internal spring energy comes from relative velocity only."),
   assumption("What justifies conserving relative mechanical energy during compression?",
    "Both masses and velocities given; no thrusters or damping; spring relaxed",
    ["Both masses and velocities given; no thrusters or damping; spring relaxed",
     "Thrusters may supply unknown outside work but do not change relative motion",
     "The coupling has hidden dissipation equal to the original 90% claim"],
    "No external impulses or internal losses may be silently introduced into the ideal relative-energy model."),
   number("com","SIGNED COM velocity while coupling compresses (m/s)",1.6,.035,
    "Mass-weight velocities (200×(+4)+300×0)/500. It points right.","SIGN_OR_REFERENCE_FRAME"),
   number("relative","Initial relative kinetic energy available (J)",960,12,
    "Reduced mass is (200×300)/500=120 kg and relative speed is 4 m/s, so Krel=½(120)(4²)."),
   number("compression","First maximum spring compression (m)",Math.sqrt(.2),.014,
    "Set ½(9600)x² equal to 960 J; the common drift energy remains."),
   why("Explain which mass and speed observations justify your model, why both spacecraft still drift at peak compression, and why no unknown percentage was invented.")
  ],
  hints:[
   "A spacecraft pair can translate through space without closing its separation. What part of their motion changes the coupler length?",
   "Check signed momentum; a spring internal to the pair cannot erase it. At first maximum compression the relative velocity is zero, not COM velocity.",
   "Use μ=m_Am_B/(m_A+m_B), Krel=½μ(u_A−u_B)² and ½kx²=Krel. No percentage was specified."
  ],
  worked:[
   ["Centre of mass remains in motion","Total mass M=500 kg and momentum p=200×(+4)+300×0=+800 kg·m/s. Hence V_COM=+1.6 m/s."],
   ["Relative kinetic energy","Reduced mass μ=(200×300)/500=120 kg, relative speed=4 m/s. Krel=½(120)(4²)=960 J."],
   ["Full energy audit","Initial total kinetic energy=½(200)(4²)=1600 J. Shared COM kinetic energy is ½(500)(1.6²)=640 J. Exactly 960 J can enter the spring."],
   ["Compression under explicit ideal assumptions","½(9600)x²=960 J gives x=√0.2≈0.4472 m. Both spacecraft still move right at 1.6 m/s at first maximum compression."]
  ],
  boundary:"CHANGED FORCE MODEL: A docking thruster NOW fires on spacecraft A throughout compression, but the problem gives NO thrust history, impulse or work; all other initial information stays the same. Can you uniquely predict the first maximum compression from the previous relative-energy formula? Explain what additional measurement is required. Do not invent a new compression number.",
  boundaryFields:[
   model("Can the maximum compression still be determined uniquely?",
    "No: external thrust work/impulse during compression is unspecified",
    ["No: external thrust work/impulse during compression is unspecified",
     "Yes: exactly 0.4472 m because initial masses and speeds are unchanged",
     "Yes: it must be 10% of the original no-thruster compression"],
    "External thrust can change both COM momentum and the internal relative-energy ledger; its work/history is required."),
   assumption("Which missing information would be needed?",
    "Thrust force/impulse history or equivalent work plus relative motion",
    ["Thrust force/impulse history or equivalent work plus relative motion",
     "Only the original engine-wagon total mass",
     "No extra information is required for an external force"],
    "Thrust does not act equally on both bodies; the relative motion is no longer dynamically isolated."),
   changedWhy("Explain why adding an unspecified external thruster invalidates the unique relative-energy prediction and how you would reformulate the problem.")
  ],
  boundaryCheck:"With unknown thrust on A, dP_total/dt is no longer zero and the relative kinetic energy changes under external work. No unique maximum x can be computed from the given facts. Additional information on thrust force versus time/displacement (and its relative-motion work) or full motion measurements is required. The previous 0.4472 m is a CONDITIONAL no-thruster result, not valid automatically."
 }
}
};
})();
