/* WPE R2 five source-specific constructions, all using the existing
 * six-stage Core1A/Core1B student engine and visual conventions.
 * F04 + F08 share one TWO-BODY MODEL FOUNDATION, but different fresh
 * decisions: reversible relative energy versus source-conditioned loss.
 * No original exam stems, coaching keys or QRT labels are modified.
 */
(() => {
"use strict";
const twoBody={
  prerequisites:"Two bodies can move together overall AND change separation. Write total mass M=m₁+m₂, centre-of-mass velocity V=(m₁u₁+m₂u₂)/M, relative speed w=u₁−u₂, and reduced mass μ=m₁m₂/M. With no external impulse or work, Ktotal = ½MV² + ½μw². Only the second part changes when their separation changes through an ideal internal spring.",
  reason:"At maximum compression or elongation their relative speed is momentarily zero, but their common centre-of-mass motion may remain. Equating ALL kinetic energy to spring energy would incorrectly erase that shared drift. An external brake, a dissipative damper or a mechanical support changes the ledger and needs explicit data."
};
const scenarios={
F04:{
  source:"EX-M50",title:"Two moving blocks: shared travel versus stretch",short:"Two blocks · spring energy",
  sourceCaution:"The original equal-and-opposite setup has zero total momentum, so its x=v/2 result is a special case. Its inherited limiting-case CHECK for only one block moving incorrectly claims v/(2√2); with two 0.25 kg blocks and k=2 N/m, the correct relative-energy result is v/4. Do not copy that check. This fresh challenge keeps COM motion nonzero.",
  question:"Why does an internal spring absorb relative kinetic energy rather than the energy of two blocks travelling together?",
  prerequisites:twoBody.prerequisites,
  core:twoBody.reason,
  guide:"GUIDED ANCHOR: two frictionless blocks, masses 1 kg and 3 kg, start with a spring at natural length. Block 1 is to the RIGHT of block 2; at an instant block 1 moves right at +2 m/s and block 2 moves left at −2 m/s. k=8 N/m. They are separating, and the spring is attached to both.",
  guideSteps:[
    ["Distinguish two speeds","Their centre-of-mass velocity is V=(1×2+3×(−2))/4=−1 m/s. Their relative speed is w=2−(−2)=4 m/s. Translating the pair does not by itself stretch the spring."],
    ["Decompose kinetic energy","Total K=½(1)(2²)+½(3)(2²)=8 J. Common-motion energy is ½(4)(1²)=2 J. Internal relative energy is therefore 6 J."],
    ["Check with reduced mass","μ=(1×3)/(1+3)=0.75 kg. Then Krelative=½μw²=½(0.75)(16)=6 J, agreeing with subtraction."],
    ["Find maximum elongation","At the far turn w=0 and both blocks share V=−1 m/s. With no losses, ½(8)x²=6 J, so x=√1.5≈1.225 m."],
    ["Test the 'same drift' case","If we add +5 m/s to BOTH initial speeds, the new pair has +7 and +3 m/s: w is still 4. The centre of mass moves faster, but maximum stretch is unchanged because only w determines Krelative."]
  ],
  wrong:"Wrong path: set ½kx² equal to ½m₁u₁²+½m₂u₂² without checking V. That is correct only when the centre of mass is initially stationary. At maximum extension the blocks generally still move together.",
  conditions:"1D horizontal spring, initially unstretched and attached at both ends; no friction or external horizontal impulse; Hooke's law; neglect spring mass. Positive velocity points right. First maximum elongation is the instant w=0.",
  challenge:"FRESH MODEL CHOICE: on a frictionless line two attached blocks have m₁=1 kg (RIGHT-hand block) and m₂=3 kg (LEFT-hand block). The spring (k=6 N/m) is initially at natural length. At that instant u₁=+4 m/s and u₂=−2 m/s, so they begin separating. Determine centre-of-mass velocity, reduced mass, relative kinetic energy, and first maximum spring elongation. Explain why total kinetic energy is NOT wholly stored in the spring.",
  prediction:"Can the entire initial kinetic energy turn into spring potential when the pair's total momentum is not zero? What will still be moving at maximum extension?",
  fields:[
    {id:"model",label:"Choose the energy model for internal spring elongation",type:"select",choices:["Choose an idea","Relative kinetic energy ½μ(u₁−u₂)²","Total kinetic energy of both blocks","Only the lighter block's kinetic energy","I'm not sure yet"],expected:"Relative kinetic energy ½μ(u₁−u₂)²",mistake:"The common centre-of-mass kinetic energy survives at maximum extension. Use relative velocity and reduced mass."},
    {id:"com",label:"Centre-of-mass speed V with right-positive sign (m/s)",type:"number",expected:-.5,tol:.018,mistake:"Mass-weight the signed velocities: (1×4 + 3×(−2))/4."},
    {id:"mu",label:"Reduced mass μ (kg)",type:"number",expected:.75,tol:.012,mistake:"Compute m₁m₂/(m₁+m₂)."},
    {id:"relative",label:"Relative kinetic energy available to the spring (J)",type:"number",expected:13.5,tol:.1,mistake:"Use w=4−(−2)=6 m/s, not the COM speed; Krel=½μw²."},
    {id:"extension",label:"First maximum spring elongation (m)",type:"number",expected:Math.sqrt(4.5),tol:.04,mistake:"Set ½kx²=Krelative. Do not include ½MV²."},
    {id:"reason",label:"Draw the motion of both blocks at maximum elongation and explain what energy remains",type:"textarea"}
  ],
  hints:[
    "Pause at the word 'internal'. What changes the blocks' separation: the whole pair moving or the difference in their velocities?",
    "Choose the COM frame, then identify which kinetic-energy part remains even at a relative turning point.",
    "With m₁ and m₂ unequal, compute reduced mass. Use only their relative kinetic energy for spring stretch."
  ],
  worked:[
    ["What stays moving","V=(1×4 + 3×(−2))/(1+3)=−0.5 m/s. At maximum elongation both blocks move LEFT together at −0.5 m/s, so translational kinetic energy remains ½(4)(.5²)=0.5 J."],
    ["Internal mass and speed","μ=(1×3)/(4)=0.75 kg and w=4−(−2)=6 m/s. Thus Krel=½(.75)(36)=13.5 J."],
    ["Check full energy","Initial total kinetic energy is ½(1)(16)+½(3)(4)=14 J, correctly splitting into 0.5 J COM + 13.5 J relative."],
    ["Use spring's share only","½(6)x²=13.5 J gives x=√4.5≈2.121 m. The far turn means relative speed 0, NOT each speed 0."]
  ],
  boundary:"CHANGE ONLY THE SECOND BLOCK'S MASS from 3 kg to 1 kg, keeping u₁=+4 m/s, u₂=−2 m/s, k=6 N/m and no external work. Rechoose the internal-energy model and find the new reduced mass, spring elongation and COM speed. Does the shared drift stay the same?",
  boundaryFields:[
    {id:"mu",label:"New reduced mass (kg)",type:"number",expected:.5,tol:.012,mistake:"With two equal 1 kg blocks, μ=(1×1)/(1+1)."},
    {id:"extension",label:"New maximum elongation (m)",type:"number",expected:Math.sqrt(3),tol:.04,mistake:"The relative speed remains 6 m/s; the reduced mass changed, so the spring energy changed."},
    {id:"com",label:"New COM velocity (m/s, signed)",type:"number",expected:1,tol:.025,mistake:"Mass-weight the two velocities with the NEW masses."},
    {id:"why",label:"What changed in the internal energy while relative speed stayed fixed?",type:"textarea"}
  ],
  boundaryCheck:"New μ=0.5 kg, w=6 m/s and Krel=½(.5)(36)=9 J. Hence x=√(2×9/6)=√3≈1.732 m. New COM velocity=(4−2)/2=+1 m/s, different from the original −0.5. Lower reduced mass makes the relative energy, and hence the maximum extension, smaller.",
  slider:{label:"Add the SAME rightward drift (m/s) to both guided blocks",min:-5,max:5,step:1,value:0},
  visual:"twoBody"
},
F05:{
  source:"EX-M92",title:"A heavy spring has many different speeds",short:"Massive spring · slice then integrate",
  sourceCaution:"The familiar K=mv²/6 follows from a LINEAR instantaneous velocity profile (uniform fractional stretch). A finite-mass spring can transmit elastic waves, so specifying only its end speed does not establish that profile in arbitrary fast motion.",
  question:"If one end of the spring is fixed, should every tiny piece be given the free end's full speed?",
  prerequisites:"Mass is spread continuously along the spring. Kinetic energy belongs to EVERY mass piece at its own speed: dK=½v(y)²dm. A fixed point has speed zero. An affine/uniform stretch has speed increasing linearly with distance from the fixed end.",
  core:"Visual first: cut the spring into N equal mass slices, estimate each slice's speed at its midpoint and add ½(m/N)vᵢ². In uniform extension, v(y)=(y/L)v_end and dm=(m/L)dy. The sum tends to K=½mv_end²∫₀¹s²ds=mv_end²/6.",
  guide:"GUIDED ANCHOR: a uniform 1.2 kg spring extends affinely while its wall end remains fixed and its tip moves at 3 m/s. Divide it into 4 equal mass slices and use each midpoint speed before doing an integral.",
  guideSteps:[
    ["Make a real picture of changing motion","The fixed end has speed 0. At fractions y/L=¼,½,¾,1 the local speeds are .75,1.5,2.25,3 m/s respectively. The further from the wall, the greater the speed."],
    ["Discretize before integrating","With four equal 0.3 kg slices, midpoint speeds are 0.375,1.125,1.875,2.625 m/s. Add the four values ½(0.3)vᵢ²; this gives 1.771875 J."],
    ["Look for convergence","As N grows, the midpoint-slice sum approaches 1.8 J. A point-mass shortcut ½mv_end²=5.4 J is three times too large."],
    ["Explain the continuous limit","Write dK=½(m/L)dy×(v_end y/L)². Integrating y from 0 to L gives (½)(m v_end²)(1/3)=mv_end²/6=1.8 J."],
    ["Translate to effective mass","The same energy is ½(m/3)v_end². This 'm/3' is an equivalent kinetic-energy mass for THIS profile, not a claim that two-thirds of the spring's matter disappears."]
  ],
  wrong:"Wrong path: assign tip speed to every coil or choose average speed v/2, then square it. K depends on the average of v(y)², NOT the square of average v(y). If uniform elongation is not justified, the one-sixth result is not forced.",
  conditions:"Uniform mass per instantaneous length, one end fixed and the other moving at v_end, uniform-affine axial stretch so v(y)=v_end y/L at one instant; ignore sideways vibration and wave-mode deformation. This is an explicit model condition, not a general consequence of the tip moving uniformly.",
  challenge:"FRESH EXPLANATION: an ideal uniformly stretching spring has total mass 2.4 kg and length L. Its left end is fixed and its right end moves right at 4 m/s. Under a linear velocity profile, find the speed at ¾L, the continuum total kinetic energy, the equivalent kinetic-energy mass referred to tip speed, and the factor by which ½mv_tip² overestimates it. Explain why the slice sum tends to a one-third mean-square-speed factor.",
  prediction:"Would dividing the spring into many smaller pieces make the total kinetic energy approach the energy of a point mass moving at 4 m/s, half that, or less? Why?",
  fields:[
    {id:"model",label:"What profile is justified by the stated uniform stretching model?",type:"select",choices:["Choose an idea","Velocity rises linearly from 0 at the fixed end","Every coil moves at the tip speed","Every coil moves at half the tip speed","I'm not sure yet"],expected:"Velocity rises linearly from 0 at the fixed end",mistake:"The fixed end cannot move; under affine extension each fraction y/L has speed (y/L)v_tip."},
    {id:"speed",label:"Speed at ¾L (m/s)",type:"number",expected:3,tol:.04,mistake:"Use v(y)=v_tip(y/L)."},
    {id:"energy",label:"Continuum spring kinetic energy (J)",type:"number",expected:6.4,tol:.08,mistake:"Integrate the local mass kinetic energy; the result is mv_tip²/6."},
    {id:"effective",label:"Equivalent mass at tip speed (kg)",type:"number",expected:.8,tol:.018,mistake:"Set ½m_eff v_tip²=mv_tip²/6."},
    {id:"factor",label:"Point-mass shortcut / true spring K ratio",type:"number",expected:3,tol:.04,mistake:"Compare ½mv² with (1/6)mv²."},
    {id:"reason",label:"Explain the slice velocities and why the square must be averaged before multiplying by mass",type:"textarea"}
  ],
  hints:[
    "Draw the wall and free end. Ask whether a piece near the wall can have the same speed as the free tip.",
    "Imagine four equal-mass slices and assign each the local midpoint speed. Does energy depend on v or on v²?",
    "Turn the slice sum into an integral in s=y/L, using dK=½v(s)²dm. Do not replace the distribution by average velocity before squaring."
  ],
  worked:[
    ["Local speed and assumption","Under affine stretch, v(y)=4(y/L) m/s, so at y=¾L, v=3 m/s. The endpoint speed alone would not determine this without the stated profile."],
    ["Integrate the distributed mass","dm=(2.4/L)dy, so K=½(2.4)(4²)∫₀¹s²ds=(½)(2.4)(16)/3=6.4 J."],
    ["Equivalent kinetic mass","½m_eff(4²)=6.4 gives m_eff=0.8 kg=m/3. The spring remains physically 2.4 kg."],
    ["Challenge the tempting shortcut","Treating every piece as moving at 4 m/s yields K_wrong=½(2.4)(16)=19.2 J, exactly 3× the affine-stretch result."]
  ],
  boundary:"CHANGE THE BOUNDARY CONDITION: the left end now moves right at 1 m/s while the right end moves right at 4 m/s. Assume a linear velocity variation between the ends, not the old fixed-end profile. Find the spring's kinetic energy for m=2.4 kg, and the midpoint speed. Why is mv_tip²/6 no longer appropriate?",
  boundaryFields:[
    {id:"energy",label:"New distributed spring kinetic energy (J)",type:"number",expected:8.4,tol:.1,mistake:"Now v(s)=1+3s; integrate ½m[1+3s]² over s from 0 to 1."},
    {id:"mid",label:"Speed at the halfway point (m/s)",type:"number",expected:2.5,tol:.04,mistake:"Average the TWO endpoint velocities at the spatial midpoint."},
    {id:"why",label:"What changed physically, and why can you not reuse the fixed-wall factor?",type:"textarea"}
  ],
  boundaryCheck:"v(s)=1+3s m/s. Its mean squared speed is ∫₀¹(1+3s)²ds=∫(1+6s+9s²)ds=1+3+3=7 (m/s)². Therefore K=½(2.4)(7)=8.4 J. At the midpoint v=.5(1+4)=2.5 m/s. General affine two-end formula K=m(u²+uv+v²)/6; it reduces to mv²/6 ONLY if u=0.",
  slider:{label:"Number of equal midpoint slices in the guided spring",min:1,max:32,step:1,value:4},
  visual:"slices"
},
F06:{
  source:"EX-M96",title:"Wind power combines energy per mass and mass per second",short:"Wind generator · why v cubed",
  sourceCaution:"The cubic law assumes fixed air density, rotor area and electrical conversion fraction under the compared conditions. Real turbine efficiencies, control limits and winds vary; the ideal scaling is not universal at all speeds.",
  question:"Why does doubling wind speed intercept twice the air EACH second while each kilogram carries four times the kinetic energy?",
  prerequisites:"Power is energy PER UNIT TIME. A wind stream transports volume A×v every second through a fixed area A. Multiplying by air density gives mass flow rate ṁ=ρAv. One kilogram of wind moving at speed v carries kinetic energy ½v² joules per kilogram.",
  core:"Use TWO rates with distinct owners: intercepted mass flow rate ṁ=ρAv (proportional to v), and kinetic energy per unit intercepted mass ε=½v². Their product is wind power P_wind=½ρAv³. A fixed electrical fraction η gives P_elec=½ηρAv³. Compare this mass-through-area reasoning with C07's incoming material flow; conveyor momentum rate is a different law.",
  guide:"GUIDED ANCHOR: wind density 1.2 kg/m³, a turbine's effective swept area 5 m², speed 10 m/s and a CONSTANT electrical conversion fraction 40%. Determine how much air passes per second before asking how much kinetic energy it carries.",
  guideSteps:[
    ["Draw the moving air column","One second of wind brings a column length v×1s=10 m through area 5 m²: intercepted volume 50 m³ per second."],
    ["Convert volume flow to mass flow","ṁ=ρAv=(1.2)(5)(10)=60 kg/s. This is a rate of NEW mass arriving, not 60 kg moving inside a closed box."],
    ["Find energy per kilogram","Each kilogram of wind at 10 m/s carries ½(10²)=50 J/kg of translational kinetic energy."],
    ["Multiply the two rates","P_wind=(60 kg/s)(50 J/kg)=3000 J/s=3000 W. At η=0.40, electrical power is 1200 W."],
    ["Change speed as a model test","Doubling speed to 20 m/s, with ρ,A,η unchanged, doubles ṁ AND multiplies energy per kg by four: total output becomes eight times 1200 W."]
  ],
  wrong:"Wrong path: use only ½mv² and hold 'm' constant while computing POWER through a turbine. At higher wind speed, MORE air passes the rotor each second. Also do not import C07's momentum flux as if it were wind kinetic-energy flux; same idea of mass arrival, different physical quantity.",
  conditions:"Steady uniform air flow; fixed positive density ρ, fixed turbine swept area A and fixed conversion fraction η over the compared cases; v is the component through the rotor. Wind kinetic-energy flux is a model estimate, not a universal realistic generator performance curve.",
  challenge:"FRESH WIND MODEL: air density 1.25 kg/m³ passes uniformly through a rotor swept area of 8 m² at 6 m/s. A generator converts a constant 30% of intercepted wind kinetic power to electrical power. Find the mass intercepted each second, kinetic energy passing the rotor each second, electrical power in watts, and the exponent of v in the ideal output relation. Explain the two factors of v that combine.",
  prediction:"If only wind speed doubles, with density, area and conversion fixed, why is the electrical output not merely four times as large?",
  fields:[
    {id:"model",label:"Which combined physical model gives the ideal electrical output?",type:"select",choices:["Choose an idea","ṁ∝v multiplied by energy per kg∝v²","A fixed packet of mass with energy∝v² only","Mass flow grows as v²; energy per kg stays fixed","I'm not sure yet"],expected:"ṁ∝v multiplied by energy per kg∝v²",mistake:"The moving wind column is longer each second at higher v; each kilogram also carries v² energy."},
    {id:"flow",label:"Air mass flow rate through the rotor (kg/s)",type:"number",expected:60,tol:.5,mistake:"ṁ=ρAv=1.25×8×6."},
    {id:"wind",label:"Wind kinetic-energy flux (W)",type:"number",expected:1080,tol:8,mistake:"Multiply ½v² J/kg by ṁ kg/s, before electrical efficiency."},
    {id:"output",label:"Electrical power output (W)",type:"number",expected:324,tol:3,mistake:"Apply the 0.30 fraction to wind power, not to speed."},
    {id:"exponent",label:"Speed exponent in the ideal P∝vⁿ relation (n)",type:"number",expected:3,tol:.01,mistake:"One factor from mass flow plus two factors from energy per kilogram."},
    {id:"reason",label:"Explain the moving air volume per second and the kinetic energy each kilogram transports",type:"textarea"}
  ],
  hints:[
    "First ask: how much NEW air crosses a fixed area in one second? Draw a column whose length changes with wind speed.",
    "How do density and volume-per-second produce kilograms per second? Keep units kg/s distinct from J/kg.",
    "Combine ṁ in kg/s with ½v² in J/kg. Only after that multiply by the fixed conversion fraction."
  ],
  worked:[
    ["Count mass each second","ṁ=(1.25 kg/m³)(8 m²)(6 m/s)=60 kg/s."],
    ["Count joules per kilogram","ε=½(6 m/s)²=18 J/kg, so P_wind=(60)(18)=1080 J/s=1080 W."],
    ["Convert into electrical output","η=0.30 gives P_elec=0.30(1080)=324 W."],
    ["Recover cubic speed","P_elec=½ηρAv³; ρ,A,η fixed means v¹ from ṁ and v² from per-mass K, giving v³, not v²."]
  ],
  boundary:"CHANGE TWO CONDITIONS at once: wind speed rises from 6 to 9 m/s but the available swept area HALVES from 8 to 4 m². Keep ρ=1.25 and η=0.30 fixed. What is the new electrical power and the ratio to the original 324 W? Explain why just cubing the speed ratio would be incomplete.",
  boundaryFields:[
    {id:"output",label:"New electrical power (W)",type:"number",expected:546.75,tol:4,mistake:"Use ½ηρA v³ with the NEW area and NEW wind speed."},
    {id:"ratio",label:"New output / original output",type:"number",expected:1.6875,tol:.02,mistake:"Area ratio 4/8 multiplies the cubic speed ratio (9/6)³."},
    {id:"why",label:"Explain which factors changed and why this is not a pure doubling-wind comparison",type:"textarea"}
  ],
  boundaryCheck:"Pnew=½(0.30)(1.25)(4)(9³)=546.75 W. Relative output=(4/8)(9/6)³=½×3.375=1.6875. Speed increased, but swept area decreased: do not apply the cubic speed factor alone.",
  slider:{label:"Guided wind speed (m/s) with fixed density, area and conversion",min:0,max:25,step:1,value:10},
  visual:"wind"
},
F07:{
  source:"EX-M106",title:"A pendulum's turning-point force is not its holding force",short:"Pendulum · work versus balance",
  sourceCaution:"The source asks for a horizontal force 'required to displace it until' 45°. The coaching result Mg(√2−1) assumes a CONSTANT force applied from rest that leaves the bob momentarily at rest at 45°. A static hold at 45° instead needs Mg. Without specifying the force history or final speed, the bare words are ambiguous.",
  question:"Does 'move it up to an angle' describe work done during motion, or a force that balances the bob at that angle?",
  prerequisites:"A pendulum of length L moves on a circle. A horizontal push does work FΔx, where Δx=Lsinθ. Raising the mass by Δh=L(1−cosθ) gains MgΔh gravitational energy. For equilibrium at one angle, the tangential components of forces balance. An impulse and time-varying push are different models.",
  core:"Two honest questions: CONSTANT F from rest to a turning point with no losses needs F Lsinθ = MgL(1−cosθ), so F=Mg tan(θ/2). A STATIC hold at θ requires F cosθ=Mg sinθ, so F=Mg tanθ. At 45°, these are Mg(√2−1) and Mg respectively.",
  guide:"GUIDED ANCHOR: a 1 kg bob on a 1 m light string, g=10 m/s², starts at the vertical lowest point. Consider 45°. Compare (A) constant rightward force applied from rest until first turning point and (B) a force holding it motionless after carefully positioning it.",
  guideSteps:[
    ["Sketch the geometry","At θ=45°, horizontal travel x=Lsin45°=0.707 m; vertical rise h=L(1−cos45°)≈0.293 m. Weight does negative work −Mgh."],
    ["Ask what motion is specified","Case A: the bob is released from rest under a CONSTANT rightward force and is instantaneously at rest at the far turn. It may have been moving during the journey."],
    ["Use work only for case A","Work F×0.707 equals gained gravitational energy (1)(10)(0.293)=2.929 J. Thus F≈4.142 N=Mg(√2−1)."],
    ["Ask for a different situation","Case B: held quietly at 45° means zero tangential acceleration at that instant. Resolve along tangent: F cos45°=Mg sin45°, so F=Mg=10 N."],
    ["Watch the limit","For small θ, constant-turning-point F≈Mgθ/2, whereas static hold F≈Mgθ. No universal 'horizontal force to reach 45°' exists without specifying motion/history."]
  ],
  wrong:"Wrong path: quietly substitute F=Mg tanθ into the work equation for a constant-force trip. The static equation asks for zero acceleration at ONE point, while a turning point asks only for instantaneously zero speed. The bob generally has nonzero tangential acceleration at a turning point.",
  conditions:"Ideal inextensible string of fixed length; point mass and gravity, no friction/air drag; force horizontal and (for case A) constant throughout displacement; starts at rest at bottom and ends at first turning point with K=0. For case B, the bob is held motionless at specified angle. If force varies over the path, work requires its actual history.",
  challenge:"FRESH COMPARISON: a 2 kg bob hangs on a light 1.2 m string in g=10 m/s². At 60° from vertical, compare two independently stated situations. (A) A constant horizontal rightward force takes the bob from rest at the bottom to a first turning point at 60°, with no energy losses. (B) A rightward horizontal force holds the bob STATICALLY at 60°. Find the rise in gravitational energy, the required constant A force and the holding B force. Explain why they differ even though the endpoint angle is identical.",
  prediction:"Should the constant-force trip ending at a turning point require the same force as holding the bob statically at 60°? What condition distinguishes these?",
  fields:[
    {id:"model",label:"What distinguishes the two 60° situations?",type:"select",choices:["Choose an idea","Turning-point work ledger versus static tangential balance","Both require static tangential balance","Both require work per unit time only","I'm not sure yet"],expected:"Turning-point work ledger versus static tangential balance",mistake:"Zero speed at a turning point does not imply zero tangential acceleration or static force balance."},
    {id:"rise",label:"Gravitational energy gained (J)",type:"number",expected:12,tol:.1,mistake:"Use ΔU=MgL(1−cos60°), not MgLsin60°."},
    {id:"constant",label:"Case A constant rightward force (N)",type:"number",expected:20/Math.sqrt(3),tol:.16,mistake:"Set F Lsin60°=ΔU; F=Mg tan(60°/2)."},
    {id:"static",label:"Case B static holding force (N)",type:"number",expected:20*Math.sqrt(3),tol:.35,mistake:"Resolve forces tangent to the arc: F cos60°=Mg sin60°."},
    {id:"reason",label:"Explain why zero final velocity in A does not mean force equilibrium, and name the missing source condition",type:"textarea"}
  ],
  hints:[
    "Draw the final bob position. Which displacement does a HORIZONTAL force use for WORK, and which displacement describes gravitational HEIGHT?",
    "Turning point means the bob's speed is zero at one instant; does it say its tangential acceleration is zero? Static holding imposes a DIFFERENT condition.",
    "For case A equate constant horizontal work with height energy. For case B resolve horizontal pull and weight along the tangent."
  ],
  worked:[
    ["Geometry and potential","L=1.2 m and θ=60°. Δh=1.2(1−½)=0.60 m; Δx=1.2sin60°≈1.039 m. So ΔU=(2)(10)(.60)=12 J."],
    ["Constant-force trip","Case A: F_A Δx = ΔU; F_A=12/(1.2sin60°)=20 tan30°≈11.547 N. The bob can momentarily stop at 60° yet accelerate back toward the bottom."],
    ["Static hold","Case B: tangential force balance F_B cos60°=Mg sin60°, so F_B=Mg tan60°=20√3≈34.641 N."],
    ["Compare and state ambiguity","The ratio is three for 60°. If the source wording only says 'force required to displace' and does not specify constant-force turning point or static hold, there is no unique force law from that phrase alone."]
  ],
  boundary:"CHANGE ONLY THE TARGET ANGLE from 60° to 30°, with M=2 kg, g=10 m/s² and an ideal string. Calculate the constant horizontal force required to end at the first turning point AND the force to hold the bob statically there. How do the two equations differ as angle tends to zero?",
  boundaryFields:[
    {id:"constant",label:"Constant-force turning-point force at 30° (N)",type:"number",expected:20*Math.tan(Math.PI/12),tol:.12,mistake:"Use F=Mg tan(θ/2) with θ=30°."},
    {id:"static",label:"Static holding force at 30° (N)",type:"number",expected:20*Math.tan(Math.PI/6),tol:.17,mistake:"Use F=Mg tanθ, not the energy equation."},
    {id:"why",label:"Explain why both approach zero but at different small-angle rates",type:"textarea"}
  ],
  boundaryCheck:"At 30°, F_turning=20 tan15°≈5.359 N. Static hold F_hold=20 tan30°≈11.547 N. For small θ in radians, tan(θ/2)≈θ/2 whereas tanθ≈θ, so the constant-force turning-point result is about half the static holding force. The limit preserves the physical distinction.",
  slider:{label:"Guided final angle (degrees)",min:5,max:80,step:5,value:45},
  visual:"pendulum"
},
F08:{
  source:"EX-N27",title:"A shock absorber needs an energy budget AND a motion model",short:"Shock absorber · who retains energy?",
  sourceCaution:"The source states a 40,000 kg total mass and that 90% of the wagon's energy is lost. The coached 16×10⁵ N/m can be obtained by ASSUMING that 10% of WHOLE-SYSTEM initial kinetic energy is stored at 1 m compression. This is not uniquely a two-body engine–wagon prediction: wagon mass, initial relative velocity, braking forces, damping and remaining COM energy are unspecified.",
  question:"When is a percentage of the whole vehicle's energy a usable spring budget, and when must we model two distinct moving masses?",
  prerequisites:twoBody.prerequisites,
  core:twoBody.reason+" An additional ASSUMED whole-system energy budget may instead say 'a stated fraction f of ½Mv² goes into ½kx²'. That is a separate, conditional bookkeeping model. It does NOT automatically follow from the reduced-mass dynamics of a moving engine and wagon.",
  guide:"TWO EXPLICITLY DIFFERENT GUIDED MODELS. Model A assumes a single 1000 kg vehicle initially at 10 m/s. It loses 90% of its initial kinetic energy and stores exactly the remaining 10% in a spring at compression 0.50 m. Model B is an ideal two-body spring coupling between an engine of 1000 kg moving at +8 m/s and a stationary 3000 kg wagon, with k=150,000 N/m and no external losses.",
  guideSteps:[
    ["A. State a full-system assumption","Initial vehicle kinetic energy is ½(1000)(10²)=50,000 J. Under the explicit ASSUMPTION that only 10% reaches the spring, the stored energy is 5000 J, not the full 50,000 J."],
    ["A. Derive stiffness conditionally","½k(0.50²)=5000 J, so k=40,000 N/m. This is a correct consequence of the ASSUMED budget; the original physical system need not satisfy it without additional dynamics."],
    ["B. Separate common and relative motion","For 1000 kg at +8 and 3000 kg at 0, COM velocity is (1000×8)/4000=2 m/s. Reduced mass μ=(1000×3000)/4000=750 kg; relative speed is 8 m/s."],
    ["B. Calculate actual internal energy","Relative kinetic energy is ½(750)(8²)=24,000 J. The initial total is 32,000 J, split into 8000 J COM motion and 24,000 J relative motion."],
    ["B. Find compression from relative motion","With a lossless spring k=150,000 N/m, ½kx²=24,000 J gives x=√0.32≈0.566 m. This depends on BOTH masses and their relative speed, not on an arbitrary 10% of whole-system energy."]
  ],
  wrong:"Wrong path: assume a wagon moving with its engine at the same speed can compress an internal spring from that shared forward kinetic energy alone. With zero relative speed, the ideal pair cannot change its coupling compression unless an external force or brake changes their relative motion. Another wrong path is treating a stated energy-retention fraction as a unique two-body braking solution when component masses are missing.",
  conditions:"Model A: f=10% whole initial KE reaches spring at maximum compression; residual translational/thermal energy is handled by the postulated budget. Model B: 1D horizontal bodies joined by a massless linear spring, initially relaxed, no external impulse, friction or damping; genuine compression uses relative mass μ and relative initial speed. A real braking engine–wagon pair may violate either idealization.",
  challenge:"FRESH MODEL CHOICE: two frictionless industrial carts are connected by an ideal spring, initially uncompressed. Cart A is LEFT of cart B, moving RIGHT toward B, with mass 600 kg and speed +6 m/s; cart B has mass 900 kg and speed 0. The spring stiffness is 54,000 N/m. No brakes, damping or outside horizontal forces act. Find the COM speed, reduced mass, relative kinetic energy available for compression and FIRST maximum compression. Explain why using 10% of whole-system kinetic energy would be unjustified here.",
  prediction:"If cart B were moving at +6 m/s along with A, would their common 6 m/s motion alone compress the internal spring? Why or why not?",
  fields:[
    {id:"model",label:"Which source of spring energy is justified by the FRESH cart data?",type:"select",choices:["Choose an idea","Relative kinetic energy of the two carts","Automatically 10% of their total kinetic energy","All of the initial total kinetic energy","I'm not sure yet"],expected:"Relative kinetic energy of the two carts",mistake:"The fresh setup supplies both masses and velocities, and explicitly has no dissipation. Use the relative motion, not a source-only 10% assumption."},
    {id:"com",label:"Centre-of-mass speed (m/s, signed)",type:"number",expected:2.4,tol:.04,mistake:"Mass-weight 600×6+900×0, then divide by 1500."},
    {id:"mu",label:"Reduced mass (kg)",type:"number",expected:360,tol:4,mistake:"μ=(600×900)/(600+900)."},
    {id:"relative",label:"Relative kinetic energy available for compression (J)",type:"number",expected:6480,tol:70,mistake:"The relative speed is 6 m/s: Krel=½μw²."},
    {id:"compression",label:"Maximum spring compression (m)",type:"number",expected:Math.sqrt(.24),tol:.014,mistake:"At relative stopping point, ½(54000)x²=6480 J."},
    {id:"reason",label:"Compare this two-body model with a separately ASSUMED 10% whole-system energy budget",type:"textarea"}
  ],
  hints:[
    "Decide whether the new cart problem gave you a dissipation percentage. If none is given and both bodies can drift, what energy is available internally?",
    "Calculate COM speed and relative speed separately. At peak compression do both carts have to stop, or just approach the same speed?",
    "Use μ=m₁m₂/(m₁+m₂), then ½μ(u₁−u₂)²=½kx². Keep COM energy outside the spring ledger."
  ],
  worked:[
    ["Find COM motion","V=(600×6+900×0)/1500=+2.4 m/s. Total Kinitial=½(600)(6²)=10,800 J. COM energy is ½(1500)(2.4²)=4320 J."],
    ["Calculate internal share","μ=(600×900)/1500=360 kg; relative speed w=6 m/s. Krel=½(360)(6²)=6480 J, agreeing with 10,800−4320."],
    ["Solve compression","½(54,000)x²=6480, so x=√(12960/54000)=√0.24≈0.4899 m."],
    ["Explain the OTHER model","A whole-system '10% retained' hypothesis would instead give 1080 J, not 6480 J, and a different compression. No such percentage was supplied for these ideal carts. An engine–wagon problem requires masses/braking history to determine the actual relative budget."]
  ],
  boundary:"CHANGE THE IDEALIZATION: suppose a damper in the cart coupling removes exactly 25% of the AVAILABLE RELATIVE kinetic energy during compression, while the system's COM motion remains unchanged. Same masses, speeds and k. How much energy now reaches the spring, and what is the new maximum compression? Why is 25% of total 10,800 J the wrong loss?",
  boundaryFields:[
    {id:"energy",label:"Relative energy stored in spring after damping (J)",type:"number",expected:4860,tol:60,mistake:"Keep 75% of RELATIVE initial energy 6480 J, not 75% of total kinetic energy."},
    {id:"compression",label:"New maximum compression (m)",type:"number",expected:Math.sqrt(.18),tol:.014,mistake:"Now ½kx²=4860; x shrinks by √.75 compared with the undamped case."},
    {id:"why",label:"Explain the energy owner, unchanged COM motion and why a whole-system percent is different",type:"textarea"}
  ],
  boundaryCheck:"Damper dissipates 0.25×6480=1620 J of relative energy; spring receives 0.75×6480=4860 J. With k=54,000 N/m, x=√(9720/54000)=√0.18≈0.4243 m. The common-motion 4320 J remains unaffected under the stated internal-damping assumption. Applying 25% to 10,800 J would confuse two different energy ledgers.",
  slider:{label:"Fraction (%) of the ASSUMED whole-system energy retained by spring",min:0,max:100,step:5,value:10},
  visual:"shock"
}
};
function modelSvg(id,val,{host,readout,svg,svgLine,svgText,nice}){
  const text=(x,y,value,size=14)=>svg(host,"text",{x,y,fill:"#23566a","font-size":size,"font-weight":"650"},value);
  if(id==="F04"||id==="F08"){
    svgLine(host,30,213,605,213,"#809aa6",4);
    svg(host,"rect",{x:82,y:137,width:100,height:56,rx:9,fill:"#bbdedc",stroke:"#2b7584","stroke-width":2});
    svg(host,"rect",{x:458,y:137,width:112,height:56,rx:9,fill:"#bed5f5",stroke:"#5474a0","stroke-width":2});
    const zig=[];for(let i=0;i<=16;i++){const x=182+i*(276/16),y=i===0||i===16?165:165+(i%2?15:-15);zig.push((i?"L":"M")+x+" "+y);}
    svg(host,"path",{d:zig.join(" "),fill:"none",stroke:"#b77b38","stroke-width":4});
    text(100,166,id==="F04"?"Body B":"Body A");text(470,166,id==="F04"?"Body A":"Body B");text(245,115,"Internal spring");
    if(id==="F04"){
      const shift=val,u1=2+shift,u2=-2+shift,V=-1+shift;
      text(55,65,"u₂="+nice(u2)+" m/s");text(450,65,"u₁="+nice(u1)+" m/s");
      svgLine(host,150,88,100,88,"#1a856d",4);svgLine(host,420,88,470,88,"#9c6644",4);
      readout.textContent="Shift both speeds by "+nice(shift)+" m/s. Relative speed stays "+nice(u1-u2)+" m/s, relative energy stays 6 J and maximum stretch stays √1.5 ≈ 1.225 m; COM velocity changes to "+nice(V)+" m/s.";
    }else{
      const f=val/100,E=f*50000,k=f===0?0:2*E/(.5**2);
      text(37,51,"Model A: ASSUMED energy budget");text(340,51,"Model B: relative compression");
      readout.textContent="Whole-system hypothetical: retained "+nice(val)+"% of 50,000 J = "+nice(E)+" J in spring at 0.50 m; conditional k="+nice(k)+" N/m. This does NOT determine the true two-body coupling. Model B needs both masses and relative speed.";
    }
  }else if(id==="F05"){
    const N=Math.max(1,Math.round(val)),m=1.2,v=3,ratio=(4*N*N-1)/(12*N*N),K=.5*m*v*v*ratio;
    const left=66,right=580,y=153,w=(right-left)/N;
    svgLine(host,64,72,64,224,"#6b8795",10);text(38,49,"Fixed: v=0");
    for(let i=0;i<N;i++){
      const relative=(i+.5)/N,speed=relative*v;
      svg(host,"rect",{x:left+i*w,y:y-20*relative,width:Math.max(.8,w-1),height:35+20*relative,fill:i%2?"#8bc7b9":"#bbdedb",stroke:"#568f93","stroke-width":.6});
      if(N<=8)text(left+i*w+3,y-31*relative-15,nice(speed));
    }
    text(420,52,"Free tip: v=3 m/s");
    readout.textContent=N+" equal midpoint slices: K_N="+nice(K)+" J, approaching continuum mv²/6=1.8 J. The point-mass shortcut would give 5.4 J. Slice speeds increase along the spring.";
  }else if(id==="F06"){
    const v=val,rho=1.2,A=5,eta=.4,flow=rho*A*v,wind=.5*flow*v*v;
    for(let i=0;i<9;i++){
      const x=40+i*45,offset=v*2;
      svgLine(host,x+offset,85+i%2*15,x+offset+32,85+i%2*15,"#5b9ab5",3);
    }
    svgLine(host,475,35,475,226,"#537f8f",5);
    svg(host,"ellipse",{cx:475,cy:136,rx:25,ry:91,fill:"#c8e7ef",stroke:"#2c7c93","stroke-width":3});
    svg(host,"circle",{cx:475,cy:136,r:11,fill:"#215f76"});
    text(29,40,"Moving air: length in 1 s = v metres");
    text(507,89,"Swept area A");
    readout.textContent="At v="+nice(v)+" m/s, ρ=1.2 and area=5: mass flow="+nice(flow)+" kg/s; energy per kg="+nice(.5*v*v)+" J/kg; wind power="+nice(wind)+" W; electrical output at fixed 40%="+nice(eta*wind)+" W.";
  }else if(id==="F07"){
    const t=val*Math.PI/180,Mg=10,turn=Mg*Math.tan(t/2),hold=Mg*Math.tan(t);
    svgLine(host,320,46,320,221,"#acc3cb",2);
    const x=320+145*Math.sin(t),y=50+145*Math.cos(t);
    svgLine(host,320,50,x,y,"#2d7c87",4);
    svg(host,"circle",{cx:x,cy:y,r:22,fill:"#d6b77d",stroke:"#936a37","stroke-width":2});
    svg(host,"circle",{cx:320,cy:50,r:8,fill:"#315c76"});
    text(343,57,"Pivot");
    text(24,60,"Angle "+nice(val)+"°");
    text(24,91,"Constant-force far turn");
    text(24,116,"versus");
    text(24,143,"Static equilibrium");
    readout.textContent="Angle "+nice(val)+"°: work-ledger constant force from rest to turning point = "+nice(turn)+" N; force to hold the bob statically at that angle = "+nice(hold)+" N. A turning point is not equilibrium.";
  }
}
/* R3 retains original Task A and adds Task B as separate committed practice,
 * without changing source questions, shared C/E/F components or PR #61 routes. */
const academic=window.WPE_R3_CONTENT;
if(!academic||Object.keys(academic).sort().join(",")!=="F04,F05,F06,F07,F08")
 throw Error("R3 transfer science definitions unavailable");
for(const [id,d] of Object.entries(scenarios)){
 const r3=academic[id];
 if(!r3?.academic||!r3.transfer||r3.transfer.fields?.[0]?.id!=="model")
   throw Error("R3 source-specific construction incomplete: "+id);
 d.academic=r3.academic;
 d.transfer=r3.transfer;
 d.fields.splice(1,0,r3.originalAssumption);
 for(const f of d.fields){
  if(!f.errorKind&&f.type==="select")f.errorKind="MODEL_CHOICE";
  if(!f.errorKind&&f.type==="number")f.errorKind=/^(com|speed|mid)$/.test(f.id)?"SIGN_OR_REPRESENTATION":"CALCULATION_OR_UNITS";
 }
 d.modelView=(val,help)=>modelSvg(id,val,help);
}
if(typeof window.WPEGapJourneys!=="function")throw Error("Existing six-stage student engine was not loaded");
window.WPEGapJourneys(scenarios,{storagePrefix:"g9:wpe:gaps:v2:",coveragePath:"learning-coverage-r1.json"});
})();
