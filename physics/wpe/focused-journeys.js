/* WPE focused reasoning constructions F01–F03.
 * The existing Physics Blueprint / six-stage Core1A→Core1B method is reused.
 * Author-created problems only. No original exam keys or QRT promotions.
 * Public page source is inspectable: this is NOT secure assessment.
 */
(() => {
  "use strict";
  const stages=["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
  const scenarios={
    F01:{
      source:"EX-M97",title:"The force doing work is not always the net force",short:"Launch power: applied versus net",
      sourceCaution:"The source's coaching key treats net-force power as muscular power. An idealized applied-force × centre-of-mass-speed rate also differs from net-force power. For a real jumper, ground contact can be stationary: F_ground × v_COM is a centre-of-mass pseudo-work rate, not directly measured muscular power. Additional body-motion assumptions would be needed to infer that. This lesson compares the rates without certifying the original key.",
      question:"Which force should multiply the speed to give power delivered by a lifting agent?",
      prerequisites:"Before starting: work is force along displacement; power is work per unit time at that instant. Energy changes through work of ALL forces. Weight mg acts downward even while something accelerates upward.",
      core:"Choose a force owner before calculating: P_lifter = T v, but dK/dt = (T − mg)v. The difference mgv is the rate of increase of gravitational potential energy. At release, the applied force ceases; gravity alone governs flight.",
      guide:"Guided anchor: a 2 kg demonstration carriage starts at rest in a vertical guide. A cable pulls upward with constant 30 N over 1.0 m, then disconnects. Gravity is 10 m/s², with negligible friction.",
      guideSteps:[
        ["Draw both forces","The cable pulls up 30 N, weight pulls down 20 N. Their NET is 10 N upward, but the cable is still delivering a 30 N pull."],
        ["Apply work–energy while attached","Net work = (30 − 20)×1 = 10 J. Starting from rest, ½(2)v² = 10, so the release speed is √10 ≈ 3.162 m/s."],
        ["Separate two powers","At the instant just BEFORE disconnection: cable power = 30√10 ≈ 94.9 W; net kinetic-energy rate = 10√10 ≈ 31.6 W. Weight removes energy at −20√10 W."],
        ["Locate the maximum in this phase","With constant positive acceleration, the speed increases from 0 to √10. Cable power T v therefore peaks just before release, not at the initial stationary instant."],
        ["Now change physical phase","Once the cable disconnects, upward motion continues but the cable power becomes ZERO. The carriage rises another v²/(2g) = 0.50 m while gravity slows it to rest."]
      ],
      wrong:"Multiplying (T − mg) by v gives the rate at which kinetic energy changes, not the mechanical power supplied by a specified cable. The two values agree only when weight does no work (for instance, horizontal motion with vertical weight).",
      conditions:"Vertical motion; constant applied upward cable force during contact, no friction or drag; carriage begins at rest. The cable and carriage move at the same speed at the attachment point. The instant of disconnection is taken from the attached side; after disconnection cable power is zero.",
      challenge:"FRESH task: a 3 kg rescue lift leaves rest on a vertical rail. A motorized cable pulls upward with a CONSTANT 54 N through 0.80 m; then the cable detaches. Take g = 10 m/s² and neglect losses. Find net force and acceleration while attached, release speed, maximum cable power just before release, the instantaneous net power at that moment, and the additional height after release. Distinguish motor power from kinetic-energy gain rate.",
      prediction:"As the carriage speeds up, does cable power peak at the beginning or just before release? Is the net-force power the same as cable power? Explain your initial expectation.",
      fields:[
        {id:"model",label:"Which force defines mechanical power supplied by the cable?",type:"select",choices:["Choose an idea","Upward cable force T","Net force T − mg","Weight mg","I'm not sure yet"],expected:"Upward cable force T",mistake:"Power of the cable uses the cable's own upward force; net power is a different quantity."},
        {id:"netForce",label:"Net upward force while attached (N)",type:"number",expected:24,tol:.05,mistake:"Subtract weight 3×10 from the applied 54 N."},
        {id:"acceleration",label:"Upward acceleration while attached (m/s²)",type:"number",expected:8,tol:.03,mistake:"Divide the net upward force by mass, not the cable force."},
        {id:"speed",label:"Speed just before release (m/s)",type:"number",expected:Math.sqrt(12.8),tol:.04,mistake:"The net work during 0.80 m equals the change in kinetic energy."},
        {id:"cablePower",label:"Maximum cable power just before release (W)",type:"number",expected:54*Math.sqrt(12.8),tol:1,mistake:"Use applied 54 N times the release speed, NOT net 24 N times speed."},
        {id:"netPower",label:"Net instantaneous rate of change of K (W)",type:"number",expected:24*Math.sqrt(12.8),tol:1,mistake:"Net kinetic-energy power uses the 24 N resultant instead."},
        {id:"flightHeight",label:"Additional height after release (m)",type:"number",expected:.64,tol:.02,mistake:"Once detached, use kinetic energy converting to mgh; no cable acts."},
        {id:"reason",label:"Show your force arrows, phase boundary and why the two powers differ",type:"textarea"}
      ],
      hints:[
        "Pause at the word 'supplied'. Which agent is supplying power? Draw its force separately from gravity.",
        "Before release, write a net-work ledger with TWO forces. A net kinetic-energy rate and the cable's delivered power have different owners.",
        "After release, do not use the cable. What energy remains at launch and where can it go?"
      ],
      worked:[
        ["During attachment","Weight = 30 N down. Net upward force = 54 − 30 = 24 N, giving acceleration a = 24/3 = 8 m/s²."],
        ["Release speed","Net work = 24×0.80 = 19.2 J = ½(3)v². Thus v² = 12.8 and v ≈ 3.578 m/s."],
        ["Two distinct powers","Cable power rises with v and just before detachment is 54√12.8 ≈ 193.2 W. Kinetic-energy rate then is 24√12.8 ≈ 85.9 W. Their 107.3 W difference is mgv, the instantaneous gravitational-energy increase."],
        ["After detachment","Cable power becomes 0. Gravity alone decelerates the carriage; additional rise h = v²/(2g) = 12.8/20 = 0.64 m. No power is added by the cable in flight."]
      ],
      boundary:"CHANGE ONLY THE CABLE FORCE to 42 N, still 3 kg, 0.80 m, and initially stationary. Find the new release speed and maximum cable power. Which original formula changes, and does the extra rise increase or decrease?",
      boundaryFields:[
        {id:"speed",label:"New release speed (m/s)",type:"number",expected:Math.sqrt(6.4),tol:.04,mistake:"New net force is 42−30=12 N."},
        {id:"power",label:"New maximum cable power (W)",type:"number",expected:42*Math.sqrt(6.4),tol:.9,mistake:"Cable power still multiplies its own force, 42 N, by release speed."},
        {id:"height",label:"New extra rise (m)",type:"number",expected:.32,tol:.02,mistake:"After release, v²/(2g) with the NEW speed."},
        {id:"why",label:"Explain which phase changed and why",type:"textarea"}
      ],
      boundaryCheck:"New net force 12 N, a = 4 m/s² and v² = 2×4×0.80 = 6.4. Release speed ≈ 2.530 m/s. Maximum cable power = 42×2.530 ≈ 106.3 W; net power at release = 12×2.530 ≈ 30.4 W. Extra rise = 6.4/(2×10) = 0.32 m. Less upward cable force reduces both launch speed and subsequent climb.",
      visual:"lift",slider:{label:"Guided cable force (N)",min:20,max:60,step:2,value:30}
    },
    F02:{
      source:"EX-N39",title:"A rough incline uses two energy ledgers",short:"Go up, stop, return: two losses",
      question:"Why must you count friction once while climbing and AGAIN while returning?",
      prerequisites:"An object moving uphill loses kinetic energy to rising gravitational potential and to friction. When it slides back, gravity gives kinetic energy but friction still removes it. Kinetic friction opposes the direction of motion each time.",
      core:"Same distance, opposite direction: uphill K₀ = mgd sinθ + μmgd cosθ. Downhill K_return = mgd sinθ − μmgd cosθ. Eliminating d gives K_return/K₀ = (sinθ − μcosθ)/(sinθ + μcosθ).",
      guide:"Guided anchor: a 1 kg puck slides up a 45° rough ramp with initial kinetic energy 16 J. Its kinetic friction coefficient is 1/3, and g=10 m/s². It stops and slips back. The surface has the same μ on each leg.",
      guideSteps:[
        ["Choose two directions","During ascent, both gravity's down-slope component and friction oppose the uphill velocity. On descent, gravity helps but friction opposes downhill motion."],
        ["Find the uphill energy split","At 45°, sinθ=cosθ. Write μcosθ = (1/3)sinθ. Of 16 J, gravity gains 12 J as U, and friction dissipates 4 J before the top."],
        ["Rebuild the downhill budget","The 12 J height energy is released on the way down, but friction again removes 4 J. Return kinetic energy is only 8 J, not the original 16 J."],
        ["Compare speeds, not just energies","K is proportional to v² for fixed mass. So v_return/v_initial = √(8/16) = 1/√2 ≈ 0.707."],
        ["Check limits","For μ=0 and a fully smooth round trip, the speed magnitude returns unchanged. If μ approaches tanθ, downhill acceleration approaches zero; do not assert a spontaneous return from rest at the limiting case."]
      ],
      wrong:"The upward gravity loss is regained on descent, but friction is NEVER regained. The round trip loses twice the friction work magnitude; the return speed ratio is the square root of the kinetic-energy ratio.",
      conditions:"Straight fixed incline, same constant kinetic μ in each direction, no air drag, no other work. For a downhill return starting from rest, gravitational down-slope force must exceed kinetic friction: μ < tanθ, and static friction must permit the start (otherwise static μ_s must be specified). 'Return kinetic energy' refers to the same starting height.",
      challenge:"FRESH task: a 2 kg lab slider starts up a fixed rough ramp at 37°. Take sin37°=3/5 and cos37°=4/5, g=10 m/s². At the base its initial kinetic energy is 18 J. It stops, then slides back to the SAME base with 2 J of kinetic energy. Friction is kinetic and constant in magnitude both ways; assume static friction permits the return. Determine μ, the distance to the turning point, and the ratio of return to initial speed. Explain which energies cancel and which are lost twice.",
      prediction:"Could the slider regain all its starting kinetic energy simply because it returns to the same height? Where is energy irreversibly lost?",
      fields:[
        {id:"model",label:"What is the correct work ledger for one full round trip?",type:"select",choices:["Choose an idea","Gravity cancels, friction loses energy on both legs","Gravity and friction each cancel","Only uphill friction counts","I'm not sure yet"],expected:"Gravity cancels, friction loses energy on both legs",mistake:"Gravity's net work over a closed vertical route is zero, while friction remains negative on both legs."},
        {id:"mu",label:"Coefficient of kinetic friction μ",type:"number",expected:.6,tol:.015,mistake:"Use both upward and downward ledgers, or eliminate the turning distance by dividing them."},
        {id:"distance",label:"Distance along incline to the turning point (m)",type:"number",expected:5/6,tol:.03,mistake:"Uphill 18 J is spent on mgd sinθ AND μmgd cosθ."},
        {id:"ratio",label:"Return speed / initial speed",type:"number",expected:1/3,tol:.015,mistake:"The kinetic-energy ratio is 2/18, but speed follows its square root."},
        {id:"reason",label:"Describe how gravity and friction act on each leg and check that downhill motion is possible",type:"textarea"}
      ],
      hints:[
        "The slider starts and finishes at the same height. Which force's TOTAL round-trip work must therefore be zero?",
        "Make one equation for initial kinetic energy spent uphill and a different one for kinetic energy acquired downhill. Friction opposes each velocity.",
        "Use the two measured kinetic energies to eliminate the unknown turning distance BEFORE solving for the friction coefficient."
      ],
      worked:[
        ["Make two distinct ledgers","Uphill: 18 = mgd(sin37° + μcos37°). Downhill: 2 = mgd(sin37° − μcos37°). The +/− signs change for gravity, not for friction as a loss."],
        ["Eliminate the distance","Divide: 2/18 = (0.6−0.8μ)/(0.6+0.8μ). Thus (1/9)(0.6+0.8μ) = 0.6−0.8μ, giving μ = 0.6."],
        ["Recover distance and speed ratio","Uphill: 18 = (2×10)d(0.6 + 0.6×0.8) = 21.6d, hence d = 5/6 ≈ 0.833 m. The speed ratio is √(2/18) = 1/3."],
        ["Check physical return","μ = 0.6 is less than tan37° = 0.75, so gravity's down-slope component exceeds kinetic friction. With static release assumed, descending motion is possible. Energy lost to friction on each leg is μmgd cosθ = 8 J; 18 − 2×8 = 2 J."]
      ],
      boundary:"CHANGE THE RAMP to 45° (sin=cos), keeping μ=0.6, initial K=18 J and the same material. The turning distance changes. What is return-speed/initial-speed, and what is return kinetic energy?",
      boundaryFields:[
        {id:"ratio",label:"New return speed / initial speed",type:"number",expected:.5,tol:.015,mistake:"Use (sinθ−μcosθ)/(sinθ+μcosθ) for the energy ratio; take its square root."},
        {id:"energy",label:"New kinetic energy back at the base (J)",type:"number",expected:4.5,tol:.12,mistake:"At 45°, the energy fraction is (1−μ)/(1+μ), applied to 18 J."},
        {id:"why",label:"Explain why return speed changes even though μ stays the same",type:"textarea"}
      ],
      boundaryCheck:"At 45°, Kreturn/Kinitial = (1−0.6)/(1+0.6) = 0.25. Thus speed ratio = √0.25 = 0.5 and return kinetic energy = 18×0.25 = 4.5 J. Compared with 37°, the steeper ramp gives gravity a larger share relative to friction over the climb and return.",
      visual:"incline",slider:{label:"Guided kinetic friction μ",min:0,max:.8,step:"any",value:1/3}
    },
    F03:{
      source:"WEP07-01",title:"When an applied force reverses, the equilibrium moves",short:"Spring switch: new equilibrium, new turning point",
      question:"Why can a spring travel far beyond its former natural position after a sudden force switch?",
      prerequisites:"A Hookean spring pulls toward its natural position: Fspring = −kx for signed extension x. A constant applied force shifts the force-balance equilibrium to x_eq = Fapplied/k. At a turning point, instantaneous speed is zero.",
      core:"A sudden change of constant applied force changes the effective potential Ueff(x) = ½kx² − Fnew x. Position and velocity stay continuous through a non-impulsive switch, but the new equilibrium is DIFFERENT. Starting from rest, the two turning points lie symmetrically about x_eq, so x_other = 2x_eq − x_initial.",
      guide:"Guided anchor: a 100 N/m spring pushes a frictionless slider on a horizontal line. The slider starts at x = −0.10 m (compression), held motionless by an OLD leftward force of 10 N. Suddenly the applied force becomes +20 N RIGHT and remains constant. x=0 is natural length.",
      guideSteps:[
        ["Keep a signed coordinate","Rightward extension is positive x. The initial position −0.10 m has spring force +10 N, exactly balanced by the original leftward hold −10 N."],
        ["Switch the force, not the position","Immediately after the change, the slider is still at x = −0.10 m with v = 0. The NEW applied force is +20 N; old equilibrium is no longer relevant."],
        ["Find new equilibrium","Under +20 N, balance requires k x_eq = +20 N, so x_eq = +0.20 m. A mass released from rest oscillates symmetrically about this new centre."],
        ["Find the other turning point","Initial turning position −0.10 m lies 0.30 m LEFT of the new centre. The opposite turning position is 0.30 m RIGHT of centre: x_other=+0.50 m."],
        ["Check with energy and force direction","Ueff(x) = ½×100x²−20x. It has equal values at x=−0.10 and +0.50 m. At +0.50 m the mass momentarily stops; the spring force then points back left."]
      ],
      wrong:"Do not keep balancing the OLD applied force after it changes, and do not conserve the OLD total potential expression across the switch. Instead record x and v at the instant and conserve energy under the NEW constant force thereafter.",
      conditions:"Horizontal Hookean spring; ideal slider with no damping; attached spring and no impact; applied force changes direction instantaneously but has no impulsive displacement, so x and v remain continuous. External force is then constant. The new equilibrium can be beyond the spring's natural length.",
      challenge:"FRESH task: a frictionless slider is attached to a horizontal spring of k=80 N/m. It is initially held still at x=+0.05 m (extension), with RIGHT positive. Suddenly the original rightward 4 N holding force is reversed and TRIPLED to a constant 12 N LEFT. Find the new equilibrium x_eq, the OTHER turning point (maximum compression), and the effective-potential energy at the initial position after the switch. Explain why you cannot use the old equilibrium to find the extreme.",
      prediction:"Does the slider instantly jump to its new force-balance position when the force switches? Which way will it initially accelerate?",
      fields:[
        {id:"model",label:"What must stay continuous during an instantaneous force switch without impulse?",type:"select",choices:["Choose an idea","Position and velocity","Old equilibrium position","Old potential-energy formula","I'm not sure yet"],expected:"Position and velocity",mistake:"A force switch changes acceleration, but not x and v instantaneously without an impulse."},
        {id:"force",label:"New applied force Fnew with right-positive sign (N)",type:"number",expected:-12,tol:.05,mistake:"The new force points LEFT and has triple the old 4 N magnitude."},
        {id:"eq",label:"New equilibrium x_eq (m; signed)",type:"number",expected:-.15,tol:.004,mistake:"Force balance after switching: −kx + Fnew = 0."},
        {id:"turn",label:"Other turning position x_other (m; signed)",type:"number",expected:-.35,tol:.007,mistake:"Both turning points are equally far from the NEW equilibrium."},
        {id:"energy",label:"New effective potential Ueff at the initial x=+0.05 m (J)",type:"number",expected:.7,tol:.018,mistake:"Use ½kx² − Fnew x; Fnew is −12 N."},
        {id:"reason",label:"Explain the force switch, new equilibrium and turning point",type:"textarea"}
      ],
      hints:[
        "Choose RIGHT as positive. What is the sign of the newly applied force? Does the slider's location change during the switch?",
        "Set NEW spring force + NEW applied force to zero to locate the NEW equilibrium. Compare it with the initial held position.",
        "A frictionless spring moving under a constant force has two turning points symmetric about its equilibrium. Use the unchanged initial x and v=0 as one endpoint."
      ],
      worked:[
        ["Switch force correctly","Initially x=+0.05 m, and the holding force is +4 N. After the non-impulsive switch Fnew = −12 N, but x stays +0.05 m and v stays zero."],
        ["Locate the new equilibrium","Force balance −80x_eq −12 = 0 gives x_eq = −0.15 m, a compressed position."],
        ["Find far turning point","The initial point is 0.20 m RIGHT of new equilibrium. The other extremum is 0.20 m LEFT: x_other = −0.15−0.20 = −0.35 m. It is a compression, not an extension."],
        ["Check new energy","Ueff(x)=½(80)x²−(−12)x=40x²+12x J (x in metres). At initial x=+0.05: Ueff=0.10+0.60=0.70 J. At x=−0.35: Ueff=4.90−4.20=0.70 J, with K=0 at both endpoints."]
      ],
      boundary:"CHANGE THE NEW FORCE to ZERO immediately after the original held position x=+0.05 m (same spring). What is the new equilibrium and the opposite extreme? Compare maximum compression with the −12 N case.",
      boundaryFields:[
        {id:"eq",label:"New force-free equilibrium x_eq (m)",type:"number",expected:0,tol:.001,mistake:"With no external pull, an ideal spring balances at natural length."},
        {id:"turn",label:"Other turning point x_other (m)",type:"number",expected:-.05,tol:.004,mistake:"From rest at +0.05 m, free oscillation about x_eq=0 reaches −0.05 m."},
        {id:"why",label:"Explain why the swing is now smaller",type:"textarea"}
      ],
      boundaryCheck:"With Fnew=0, x_eq=0 and Ueff=½kx². Starting from rest at +0.05 m, the equal-energy opposite turn is x_other=−0.05 m. Its maximum compression is only 5 cm, compared with 35 cm under the continuous leftward 12 N force.",
      visual:"spring",slider:{label:"Guided new rightward force divided by original 10 N",min:0,max:3,step:.25,value:2}
    }
  };
  const ids=Object.keys(scenarios);
  const prefix="g9:wpe:focused:v1:";
  // The first variant retains its existing key; transfer is separate.
  const requestedVariant=()=>new URLSearchParams(location.search).get("variant")==="transfer"?"transfer":"first";
  const stateKey=(id,variant=requestedVariant())=>variant==="transfer"?id+":transfer":id;
  const chosenScenario=id=>requestedVariant()==="transfer"?{...scenarios[id],...window.WPE_F_TRANSFER?.[id]}:scenarios[id];
  const doc=document,svgNS="http://www.w3.org/2000/svg";
  const $=(selector,root=doc)=>root.querySelector(selector);
  const el=(tag,text,className)=>{
    const n=doc.createElement(tag);
    if(text!=null)n.textContent=text;
    if(className)n.className=className;
    return n;
  };
  const add=(parent,tag,text,className)=>{const n=el(tag,text,className);parent.append(n);return n;};
  const svg=(parent,tag,attrs,text)=>{
    const e=doc.createElementNS(svgNS,tag);
    Object.entries(attrs||{}).forEach(([k,v])=>e.setAttribute(k,String(v)));
    if(text!=null)e.textContent=text;
    parent.append(e);return e;
  };
  const svgText=(parent,x,y,t)=>svg(parent,"text",{x,y,fill:"#244e61","font-size":"15","font-weight":"700"},t);
  const svgLine=(parent,x1,y1,x2,y2,color="#719ba8",weight=3)=>svg(parent,"line",{x1,y1,x2,y2,stroke:color,"stroke-width":weight});
  const nice=n=>Number(n.toFixed(3)).toString();
  function blank(id){return {schema:1,id,stage:0,prediction:"",predictionDraft:"",draft:{},first:null,hints:[],checks:[],diagnosis:null,repair:"",boundary:null,helpHistory:[],exposure:"UNASSISTED_UNTIL_FIRST_ATTEMPT"};}
  const states={};
  let storageWorks=true;
  for(const id of ids)for(const variant of ["first","transfer"]){
    const key=stateKey(id,variant);let saved=null;
    try{saved=JSON.parse(localStorage.getItem(prefix+key)||"null");}catch(_){}
    states[key]=(saved&&saved.schema===1&&saved.id===key&&Number.isInteger(saved.stage)&&saved.stage>=0&&saved.stage<=5&&(saved.stage<2||(saved.first&&saved.first.answers&&typeof saved.first.answers.reason==="string")))?saved:blank(key);
  }
  function persist(id){const key=stateKey(id);try{localStorage.setItem(prefix+key,JSON.stringify(states[key]));return true;}catch(_){storageWorks=false;$("#save-notice").hidden=false;return false;}}
  let active="F01", sourceLink=null;
  function input(parent,id,field,value){
    const group=add(parent,"div",null,"field");
    const label=add(group,"label",field.label);
    const name=id+"-"+field.id;label.htmlFor=name;
    let e;
    if(field.type==="textarea"){e=add(group,"textarea");e.rows=4;}
    else if(field.type==="select"){
      e=add(group,"select");
      for(const c of field.choices)add(e,"option",c).value=c;
    }else{e=add(group,"input");e.type=field.type;e.inputMode="decimal";e.step="any";}
    e.id=name;e.dataset.field=field.id;if(field.type==="text")e.inputMode="text";e.value=value??(field.type==="select"?field.choices[0]:"");
    return e;
  }
  function action(parent,key,label,secondary=false){
    const b=add(parent,"button",label,secondary?"secondary":"primary");b.type="button";b.dataset.action=key;return b;
  }
  function paragraph(parent,text,cls){return add(parent,"p",text,cls);}
  function drawModel(id,val,host,readout){
    host.replaceChildren();
    svg(host,"rect",{x:0,y:0,width:640,height:265,rx:12,fill:"#f4f9fc"});
    if(id==="F01"){
      const m=2,g=10,F=val,net=F-m*g;
      svgLine(host,92,220,545,220,"#7e9fae",4);
      svg(host,"rect",{x:268,y:111,width:100,height:68,rx:8,fill:"#bce0e8",stroke:"#316f85","stroke-width":3});
      svgText(host,281,148,"2 kg load");svgLine(host,316,111,316,53,"#167b6c",5);
      svgText(host,338,63,"Cable +"+nice(F)+" N");
      svgLine(host,316,180,316,240,"#ac623a",5);svgText(host,339,239,"Weight −20 N");
      svgText(host,46,30,"Upward force model · cable vs net");
      const v=net>0?Math.sqrt(2*net*1/m):0;
      readout.textContent=net>0
        ?"Net force "+nice(net)+" N; release speed "+nice(v)+" m/s; cable power at release "+nice(F*v)+" W; net kinetic-energy rate "+nice(net*v)+" W."
        :"Applied force does not exceed the 20 N weight. From rest, this model does not launch upward. There is no positive takeoff-speed prediction.";
    }else if(id==="F02"){
      const mu=val,s=Math.SQRT1_2,K0=16,up=K0/(1+mu),loss=K0-up,down=up-loss;
      svgLine(host,105,215,505,75,"#648f9e",5);
      svg(host,"rect",{x:270,y:128,width:65,height:40,rx:7,fill:"#a6ddd7",stroke:"#2a897f","stroke-width":2,transform:"rotate(-19 302 150)"});
      svgLine(host,252,120,212,76,"#1b8174",4);svgText(host,85,49,"Climb: gravity + friction cost energy");
      svgLine(host,366,176,410,222,"#ba6b40",4);svgText(host,347,252,"Return: friction still costs energy");
      svgText(host,466,44,"45° ramp");
      readout.textContent="For μ="+nice(mu)+", initial K 16 J → height energy "+nice(up)+" J and uphill friction loss "+nice(loss)+" J; returning K "+nice(down)+" J. Return speed fraction "+nice(Math.sqrt(down/K0))+".";
    }else{
      const a=.10,eq=val*a,initial=-a,other=2*eq-initial;
      svgLine(host,50,197,595,197,"#7fa0ad",3);
      const X=x=>320+x*420;
      for(const x of [-.2,0,.2,.4,.6]){svgLine(host,X(x),193,X(x),205);svgText(host,X(x)-12,228,nice(x));}
      svg(host,"circle",{cx:X(initial),cy:170,r:11,fill:"#c88647"});
      svg(host,"circle",{cx:X(eq),cy:170,r:11,fill:"#238779"});
      svg(host,"circle",{cx:X(other),cy:170,r:11,fill:"#536ebe"});
      svgText(host,44,31,"Signed extension x (metres) →");
      svgText(host,67,63,"Orange = start; green = new equilibrium; blue = other turn");
      readout.textContent="New rightward force = "+nice(val*10)+" N; x_eq="+nice(eq)+" m. Initial x=−0.10 m; opposite turning position x="+nice(other)+" m. A force switch does not teleport the slider.";
    }
  }
  function buildGuide(host,id,data){
    const guide=add(host,"section",null,"guide");
    paragraph(guide,"CORE1A · Understand the physics first","mini");
    add(guide,"h2","Why the model works");
    paragraph(guide,data.prerequisites,"prereq");
    paragraph(guide,data.core,"big-idea");
    paragraph(guide,data.guide);
    const figure=add(guide,"figure",null,"visual");
    const scene=svg(figure,"svg",{viewBox:"0 0 640 265",role:"img","aria-label":id+" interactive physics model"});
    const cap=add(figure,"figcaption","Move the control to check how a condition changes the physical model.");
    const ctr=add(guide,"div",null,"visual-controls");
    const label=add(ctr,"label",data.slider.label);label.htmlFor="guide-slider";
    const range=add(ctr,"input");range.id="guide-slider";range.type="range";
    range.min=data.slider.min;range.max=data.slider.max;range.step=data.slider.step;range.value=data.slider.value;
    const output=add(ctr,"output",null,"model-readout");output.htmlFor="guide-slider";
    const redraw=()=>{drawModel(id,Number(range.value),scene,output);cap.textContent="Interactive model · "+data.slider.label+". This is the guided anchor, not the fresh challenge answer.";};
    range.addEventListener("input",redraw);redraw();
    const ol=add(guide,"ol",null,"guide-steps");
    for(const [name,description] of data.guideSteps){
      const li=add(ol,"li");add(li,"strong",name+". ");
      li.append(doc.createTextNode(description));
    }
    const contrast=add(guide,"details",null,"bridge");
    add(contrast,"summary","Compare a tempting wrong approach");
    paragraph(contrast,data.wrong);
    const cond=add(guide,"details",null,"bridge");
    add(cond,"summary","Validity conditions and prerequisite bridge");
    paragraph(cond,data.conditions);
  }
  const numeric=(raw)=>raw==null||String(raw).trim()===""?NaN:Number(raw);
  function feedback(field,value){
    if(field.type==="textarea"||field.type==="text")return {status:"ungraded",text:"Your explanation or symbolic expression is saved, not automatically graded."};
    if(value==null||String(value).trim()===""||field.type==="select"&&value==="Choose an idea")
      return {status:"missing",text:"No model decision or value entered yet. "+field.mistake};
    const good=field.type==="select"?value===field.expected:Number.isFinite(numeric(value))&&Math.abs(numeric(value)-field.expected)<=field.tol;
    return good?{status:"matches",text:"Your entry matches this authored model. Check that your explanation also justifies it."}
      :{status:"review",text:"Review this step: "+field.mistake};
  }
  function drawAssessment(host,fields,answer){
    const summary=add(host,"section",null,"assessment");
    add(summary,"h4","Feedback based on YOUR saved entries");
    paragraph(summary,"These checks compare selected models and numerical entries only. They do not grade explanations or prove mastery.");
    const list=add(summary,"ul");
    let firstIssue=null;
    for(const field of fields.filter(f=>f.type!=="textarea")){
      const result=feedback(field,answer[field.id]);
      if(!firstIssue&&result.status!=="matches"&&result.status!=="ungraded")firstIssue={field:field.id,why:result.text};
      const li=add(list,"li");
      add(li,"strong",field.label+": ");
      li.append(doc.createTextNode(result.text));
      li.className=result.status;
    }
    return firstIssue;
  }
  function snapshot(host,s){
    const box=add(host,"section",null,"snapshot");
    add(box,"h4","Your preserved first attempt");
    if(!s.first){paragraph(box,"No first attempt saved.");return;}
    const dl=add(box,"dl");
    for(const [key,value] of Object.entries(s.first.answers)){
      add(dl,"dt",key==="reason"?"Your original explanation":key);
      add(dl,"dd",String(value));
    }
    paragraph(box,"Original prediction: "+s.prediction);
    paragraph(box,"Study cues viewed before first attempt: "+s.first.hintsUsed+". This browser record is practice history, not secure evidence.");
  }
  function stepHeader(host,s){
    const ol=add(host,"ol",null,"step-list");
    stages.forEach((label,i)=>{
      const li=add(ol,"li",(i+1)+". "+label,i===s.stage?"current":i<s.stage?"done":"pending");
      if(i===s.stage)li.setAttribute("aria-current","step");
    });
  }
  function showStage(host,id,d,focus){
    host.replaceChildren();
    const s=states[stateKey(id)];
    stepHeader(host,s);
    const box=add(host,"section",null,"stage-card");
    const title=add(box,"h3",(s.stage+1)+". "+stages[s.stage]);title.tabIndex=-1;
    const acts=add(box,"div",null,"stage-actions");
    if(s.stage===0){
      paragraph(box,"Predict BEFORE seeing the fresh reconstruction. You can write 'I'm not sure' and learn from that.");
      input(box,id,{id:"prediction",label:d.prediction,type:"textarea"},s.predictionDraft);
      action(acts,"prediction","Save prediction → Attempt");
    }else if(s.stage===1){
      paragraph(box,d.challenge,"challenge-prompt");
      paragraph(box,"Decide the physical model and record WHY before the worked solution. You may leave a number blank if unsure; write an explanation.","step-note");
      d.fields.forEach(f=>input(box,id,f,s.draft?.[f.id]));
      const h=add(box,"section",null,"hints");
      add(h,"h4","Optional progressive study cues");
      const ol=add(h,"ol",null,"hint-list");
      s.hints.forEach(i=>add(ol,"li",d.hints[i]));
      const next=action(h,"hint","Show next cue ("+s.hints.length+"/"+d.hints.length+")",true);
      next.disabled=s.hints.length>=d.hints.length;
      action(acts,"attempt","Save first attempt → Reconstruct");
    }else if(s.stage===2){
      paragraph(box,"Your first model is frozen separately. Compare its steps, not only its answer, with this reconstruction.");
      snapshot(box,s);
      drawAssessment(box,d.fields,s.first.answers);
      const worked=add(box,"section",null,"worked");add(worked,"h4","Worked reconstruction · unlocked after the attempt");
      const ol=add(worked,"ol");
      for(const [name,description] of d.worked){const li=add(ol,"li");add(li,"strong",name+". ");li.append(doc.createTextNode(description));}
      const checks=add(box,"fieldset",null,"self-check");add(checks,"legend","Which model steps did you explain?");
      ["I chose the appropriate force/energy owner.","I identified where the physical conditions change.","I justified the signs and equations.","I checked the numerical result and its units."].forEach((label,i)=>{
        const row=add(checks,"label");const c=add(row,"input");c.type="checkbox";c.value=i;c.dataset.check="true";c.checked=s.checks.includes(i);
        row.append(doc.createTextNode(" "+label));
      });
      action(acts,"reconstruct","Compare → Diagnose");
    }else if(s.stage===3){
      paragraph(box,"Start with the FIRST place your model diverged. The suggestion below uses your numerical entries, but only you can judge your written reasoning.");
      const assessment=add(box,"div");
      const issue=drawAssessment(assessment,d.fields,s.first.answers);
      const suggested=issue?issue.field:"explanation";
      paragraph(box,issue?"Possible first divergence: "+suggested+". "+issue.why:"Your numerical entries match the authored model; explain why each equation is valid, not only the arithmetic.","diagnosis-tip");
      if(Array.isArray(d.diagnoses)){
         const alternatives=add(box,"details",null,"bridge");
         add(alternatives,"summary","Common mistaken models and repair hints (optional)");
         const examples=add(alternatives,"ol");
         d.diagnoses.forEach((mistake,i)=>{const li=add(examples,"li");paragraph(li,mistake);paragraph(li,d.diagnosisTips?.[i]||"Check your assumptions.");});
       }
       const group=add(box,"div",null,"field");const label=add(group,"label","Where will you examine your reasoning first?");label.htmlFor="diagnosis-select";
      const select=add(group,"select");select.id="diagnosis-select";select.dataset.diagnosis="true";
      add(select,"option","Choose a step").value="";
      d.fields.filter(f=>f.type!=="textarea").forEach(f=>add(select,"option",f.label).value=f.id);
      add(select,"option","My written model / assumptions").value="explanation";
      if(s.diagnosis)select.value=s.diagnosis.field;
      input(box,id,{id:"why",label:"What caused the mismatch?",type:"textarea"},s.diagnosis?.why||"");
      action(acts,"diagnose","Save diagnosis → Repair");
    }else if(s.stage===4){
      paragraph(box,"Repair the cause, not just the final number. Keep your first attempt intact.");
      snapshot(box,s);
      const f=d.fields.find(f=>f.id===s.diagnosis?.field);
      paragraph(box,f?f.mistake:"Check conditions, system boundaries and the first unsupported inference.","diagnosis-tip");
      input(box,id,{id:"repair",label:"My corrected reasoning and why I changed it",type:"textarea"},s.repair);
      action(acts,"repair","Save repair → Boundary test");
      const review=add(box,"details",null,"review-model");add(review,"summary","Review the worked model again (optional)");
      d.worked.forEach(([h,description])=>paragraph(review,h+": "+description));
    }else if(s.stage===5){
      paragraph(box,"Make a fresh decision under a changed physical condition. Do not open its solution until you attempt it.");
      paragraph(box,d.boundary,"challenge-prompt");
      snapshot(box,s);
      paragraph(box,"Your revised model: "+s.repair,"repair-record");
      if(s.boundary===null){
        d.boundaryFields.forEach(f=>input(box,id,f,undefined));
        action(acts,"boundary","Commit boundary attempt → Check");
      }else{
        paragraph(box,"Your saved changed-condition explanation: "+(s.boundary.why||""),"step-note");
        drawAssessment(box,d.boundaryFields,s.boundary);
        const worked=add(box,"section",null,"worked");add(worked,"h4","Changed-condition reconstruction");paragraph(worked,d.boundaryCheck);
        action(acts,"history","Review my original attempt and repair",true);
        paragraph(box,"You finished this fresh problem. You can return to the original question immediately; the next challenge is optional.","done");
         if(requestedVariant()==="first"&&window.WPE_F_TRANSFER?.[id]){
           const another=add(box,"a","Try another challenge · optional transfer","transfer-challenge-link");
           const next=new URL(location.href);next.searchParams.set("variant","transfer");next.hash=id;another.href=next.pathname+next.search+next.hash;
         }else if(requestedVariant()==="transfer"){
           const initial=add(box,"a","Resume my first challenge","transfer-challenge-link");
           const prev=new URL(location.href);prev.searchParams.delete("variant");prev.hash=id;initial.href=prev.pathname+prev.search+prev.hash;
         }
        if(sourceLink?.lesson===id){
          const a=add(box,"a","Return to "+sourceLink.source+" without showing its answer","return-original");
          a.href=sourceLink.href;
        }
      }
    }
    action(acts,"reset","Restart this journey (clears saved work)",true).classList.add("reset");
    box.append(acts);
    const note=add(box,"p","","status");note.setAttribute("aria-live","polite");note.dataset.notice="true";
    if(focus)title.focus({preventScroll:true});
  }
  function readValues(host){const vals={};host.querySelectorAll("[data-field]").forEach(n=>{vals[n.dataset.field]=n.value;});return vals;}
  function dispatch(host,id,data,event){
    const btn=event.target.closest("button[data-action]");
    if(!btn||!host.contains(btn))return;
    const s=states[stateKey(id)],key=btn.dataset.action;
    const warn=message=>{const n=$("[data-notice]",host);if(n)n.textContent=message;};
    if(key==="reset"){
      if(!window.confirm("Clear this lesson's saved prediction, first attempt, hints, diagnosis and repair?"))return;
      try{localStorage.removeItem(prefix+stateKey(id))}catch(_){}
      states[stateKey(id)]=blank(stateKey(id));render();return;
    }
    if(key==="hint"&&s.stage===1&&s.first===null&&s.hints.length<data.hints.length){
      const idx=s.hints.length;s.hints.push(idx);
      s.helpHistory.push({kind:"HINT_"+(idx+1),at:new Date().toISOString()});
      s.exposure="HELPED_BEFORE_FIRST_ATTEMPT";
      // Do NOT render a new field set: hints must not destroy unsaved work.
      const list=$(".hint-list",host);add(list,"li",data.hints[idx]);
      btn.textContent="Show next cue ("+s.hints.length+"/"+data.hints.length+")";
      btn.disabled=s.hints.length===data.hints.length;
      s.draft=readValues(host);
      persist(id);return;
    }
    if(key==="history"&&s.stage===5&&s.boundary!==null){
      const old=$(".history",host);if(old){old.remove();return;}
      const history=add(host,"section",null,"history");snapshot(history,s);
      paragraph(history,"Your separate repair: "+s.repair);return;
    }
    if(key==="prediction"&&s.stage===0){
      const value=$('[data-field="prediction"]',host).value.trim();
      if(!value){warn("Record your prediction—or that you are unsure—before continuing.");return;}
      s.prediction=value;s.predictionDraft="";s.stage=1;
    }else if(key==="attempt"&&s.stage===1&&s.first===null){
      const values=readValues(host);
      if(!values.reason?.trim()){warn("Explain your model (or write 'I'm not sure') before revealing the worked method.");return;}
      if(!values.model||values.model==="Choose an idea"){warn("Choose an initial model, or select 'I'm not sure yet'.");return;}
      s.first={answers:{...values},hintsUsed:s.hints.length,helpHistory:s.helpHistory.slice(),capturedAt:new Date().toISOString()};
      s.draft={};s.stage=2;
    }else if(key==="reconstruct"&&s.stage===2){
      s.checks=[...host.querySelectorAll("[data-check]:checked")].map(x=>Number(x.value));s.stage=3;
    }else if(key==="diagnose"&&s.stage===3){
      const chosen=$("[data-diagnosis]",host).value;
      if(!chosen){warn("Choose the first step to examine.");return;}
      const why=$('[data-field="why"]',host).value.trim();
      if(!why){warn("Explain what caused that difference—even if still unsure.");return;}
      s.diagnosis={field:chosen,why};s.stage=4;
    }else if(key==="repair"&&s.stage===4){
      const value=$('[data-field="repair"]',host).value.trim();
      if(!value){warn("Write how your model changed, or why you remain unsure.");return;}
      s.repair=value;s.stage=5;
    }else if(key==="boundary"&&s.stage===5&&s.boundary===null){
      const values=readValues(host);
      if(!values.why?.trim()){warn("Explain your changed-condition decision before seeing its check.");return;}
      s.boundary={...values,capturedAt:new Date().toISOString()};
    }else{return;}
    persist(id);render(true);
  }
  function updateProgress(){
    const count=ids.flatMap(id=>[id,id+":transfer"]).filter(key=>states[key].boundary!==null).length;
    $("#progress-label").textContent=count+" of 6 first and optional boundary challenges completed";
    $("#progress-meter").max=6;$("#progress-meter").value=count;
    for(const id of ids){
      const a=$('[data-journey="'+id+'"]');
      a.classList.toggle("complete",states[stateKey(id)].boundary!==null);
      a.setAttribute("aria-current",id===active?"page":"false");
    }
  }
  function render(focus=false){
    const requested=location.hash.slice(1).toUpperCase();
    active=ids.includes(requested)?requested:"F01";
    const d=chosenScenario(active),root=$("#journey-root");root.replaceChildren();
     if(requestedVariant()==="transfer"&&!window.WPE_F_TRANSFER?.[active]){root.textContent="The second challenge is unavailable; open the first challenge instead.";return;}
    $("#current-title").textContent=active+" · "+scenarios[active].short+(requestedVariant()==="transfer"?" · Try another challenge":"");
    const article=add(root,"article",null,"lesson");
    article.id=active;
    const header=add(article,"header",null,"lesson-title");
    paragraph(header,"LEARN THE IDEA · Physical model · not an exam key","mini");
    add(header,"h2",scenarios[active].title);paragraph(header,scenarios[active].question);
     if(requestedVariant()==="transfer")paragraph(header,"The teaching below remains the original F lesson. Now choose a model for a second, unfamiliar transfer task.","step-note");
    const grid=add(article,"div",null,"learning-grid");
    buildGuide(grid,active,d);
    const challenge=add(grid,"section",null,"challenge");
    paragraph(challenge,requestedVariant()==="transfer"?"TRY ANOTHER CHALLENGE · Optional transfer":"TRY IT YOURSELF · First fresh challenge","mini");
    add(challenge,"h2","Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary test");
     if(requestedVariant()==="transfer")paragraph(challenge,"A different scenario from PR #55, kept separate from your first saved answer; do not consult the reconstruction before committing your own model.","step-note");
    paragraph(challenge,"Original thinking is saved before the worked answer. Study hints are optional; the boundary is a different condition.");
    const host=add(challenge,"div",null,"stage-root");host.dataset.stageRoot=active;
    host.addEventListener("click",e=>dispatch(host,active,d,e));
    host.addEventListener("input",()=>{
      const s=states[stateKey(active)];
      if(s.stage===0)s.predictionDraft=$('[data-field="prediction"]',host)?.value||"";
      else if(s.stage===1&&s.first===null)s.draft=readValues(host);
      else return;
      persist(active);
    });
    host.addEventListener("change",()=>{
      const s=states[stateKey(active)];if(s.stage===1&&s.first===null){s.draft=readValues(host);persist(active);}
    });
    showStage(host,active,d,focus);
    const footer=add(article,"nav",null,"lesson-footer");footer.setAttribute("aria-label","Other focused journeys");
    const n=ids.indexOf(active);
    const prev=add(footer,"a",n?"← Previous new journey":"Learn → Challenge tile");prev.href=n?"#"+ids[n-1]:"learn-challenge.html";
    const next=add(footer,"a",n<2?"Next new journey →":"All 74 question learning routes");next.href=n<2?"#"+ids[n+1]:"learn-challenge.html#question-routes";
    if(sourceLink?.lesson===active){
      const a=add(footer,"a","Return to "+sourceLink.source,"return-original");a.href=sourceLink.href;
    }
    const caveat=add(article,"details",null,"bridge");
    add(caveat,"summary","Source-question science caution");
    paragraph(caveat,d.sourceCaution||"This is authored practice, not approval of an original examination key.");
    updateProgress();
  }
  async function bindSource(){
    const source=new URLSearchParams(location.search).get("question");
    const box=$("#source-journey"),returnLink=$("#source-return");
    sourceLink=null;returnLink.hidden=true;
    if(!source){box.hidden=true;return;}
    box.hidden=false;$("#source-title").textContent="Your Question Bank route";
    if(!/^[A-Za-z0-9-]{2,64}$/.test(source)){$("#source-message").textContent="Invalid question identifier. No source return inferred.";return;}
    try{
      const [r,q]=await Promise.all([
        fetch("learning-coverage-r1.json",{cache:"no-store"}),
        fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
      ]);
      if(!r.ok||!q.ok)throw Error("route data unavailable");
      const map=await r.json(),bank=await q.json();
      if(map.schema!=="wpe-learner-coverage-r1/v1"||!Array.isArray(map.questions)||bank.questions?.length!==74)throw Error("source inventory changed");
      const found=map.questions.find(x=>x.source_id===source);
      if(!found||!bank.questions.some(x=>x.source_id===source&&x.stem_sha256===found.stem_sha256)||found.primary_lesson!==active||found.fit==="MISSING_CONSTRUCTION")
        throw Error("source does not map to this lesson");
      sourceLink={source,lesson:active,href:"../../preview/question-status.html?question="+encodeURIComponent(source)};
      $("#source-title").textContent="Your original question: "+source;
      $("#source-message").textContent=(found.fit==="RELATED_BRIDGE"?"RELATED PRACTICE ONLY: this lesson is not complete teaching for the original question. ":found.fit==="TARGETED_PRACTICE"?"Close practice match: check the original assumptions. ":"Focused practice with a different model. ")+"Return to "+source+" to make your own original attempt. No lesson confirms the source coaching key.";
      returnLink.hidden=false;returnLink.href=sourceLink.href;returnLink.textContent="Return to "+source+" without showing its answer";
      render(false);
    }catch(_){$("#source-message").textContent="This question has no verified route to the selected focused journey. No original-question return link is invented.";returnLink.hidden=true;}
  }
  for(const id of ids){
    const a=add($("#journey-navigation"),"a",id+" · "+scenarios[id].short);
    a.href="#"+id;a.dataset.journey=id;
  }
  window.addEventListener("hashchange",()=>{sourceLink=null;render();bindSource();});
  render();bindSource();
})();
