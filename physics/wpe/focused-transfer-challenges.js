/* PR #55 read-only donor: E06→F01 transfer, E07→F02 transfer, E08→F03 transfer.
 * Only authored challenge definitions are reused; existing F01–F03 guides,
 * diagrams, source coverage, native URLs and progress renderer remain authoritative.
 * No learner mastery, source answer-key approval or secure assessment is implied.
 */
window.WPE_F_TRANSFER=Object.freeze({
  "F01": {
    "donor": "PR #55 · E06",
    "title": "Ground push power versus net acceleration",
    "prediction": "Why isn't the power supplied by an upward push the same as net acceleration power? Predict which physical model will be necessary and what might change at the phase boundary.",
    "challenge": "A different 4 kg toy starts from rest. A CONSTANT upward force pushes it for 0.50 m before it separates. It then rises ANOTHER 0.80 m in free flight. Take g=10 m/s². Find its take-off speed, kinetic gain, gravity work during contact, applied push force, and the MAXIMUM instantaneous mechanical power of that applied force during contact. Assume the ideal applied force acts at a moving launcher contact point with the toy; this is not a claim about power of human muscles.",
    "fields": [
      {
        "id": "takeoffSpeed",
        "label": "Take-off speed (m/s)",
        "type": "number",
        "expected": 4,
        "tol": 0.03,
        "mistake": "Use the separate extra 0.80 m free-flight rise, not the 0.50 m contact distance."
      },
      {
        "id": "contactGain",
        "label": "Kinetic-energy gain during push (J)",
        "type": "number",
        "expected": 32,
        "tol": 0.2,
        "mistake": "Takeoff speed follows free flight; contact kinetic gain is ½mv²."
      },
      {
        "id": "contactGravity",
        "label": "Gravity's work during push (J)",
        "type": "number",
        "expected": -20,
        "tol": 0.15,
        "mistake": "Weight acts DOWN during the whole 0.50 m push; its work is negative."
      },
      {
        "id": "appliedForce",
        "label": "Upward applied contact force (N)",
        "type": "number",
        "expected": 104,
        "tol": 0.4,
        "mistake": "Applied work must pay for both 32 J kinetic gain and 20 J gravity increase, over 0.50 m."
      },
      {
        "id": "netForce",
        "label": "Net accelerating force during contact (N)",
        "type": "number",
        "expected": 64,
        "tol": 0.4,
        "mistake": "Subtract 40 N weight from the applied push; this is not the same as the applied force."
      },
      {
        "id": "appliedPower",
        "label": "MAXIMUM applied mechanical power (W)",
        "type": "number",
        "expected": 416,
        "tol": 1.5,
        "mistake": "Use 104 N applied force × 4 m/s. Net force × speed measures the kinetic-energy rate."
      },
      {
        "id": "model",
        "label": "Which force must be multiplied by speed for supplied push power?",
        "type": "select",
        "choices": [
          "Choose an idea",
          "Applied upward contact force",
          "Net accelerating force only",
          "Weight only",
          "Not sure yet"
        ],
        "expected": "Applied upward contact force",
        "tol": 0,
        "mistake": "Power delivered by the ideal moving applied force uses that force, not net force."
      },
      {
        "id": "reason",
        "label": "Explain the TWO phases and why applied and net power differ",
        "type": "textarea",
        "mistake": "Explain this physical model in your own words before comparing the worked reasoning."
      }
    ],
    "hints": [
      "Use the flight rise AFTER take-off to find speed at the contact boundary, not the push displacement.",
      "During contact, the applied push pays for kinetic gain AND gravity's negative work. Keep the contact and free-flight distances separate.",
      "The power question asks for the rate of work done by the applied upward force, not solely net acceleration; speed is highest at take-off."
    ],
    "worked": [
      [
        "Free flight determines take-off speed",
        "Extra rise 0.80 m requires v²=2gh=16 m²/s², hence v=4 m/s at separation."
      ],
      [
        "Contact energy includes rising against gravity",
        "K increases by ½(4)(4²)=32 J. Weight does −(4)(10)(0.50)=−20 J during contact, so applied work must supply 32+20=52 J."
      ],
      [
        "Find applied rather than only net force",
        "F_applied=52/0.50=104 N. Weight is 40 N down, so F_net=104−40=64 N."
      ],
      [
        "Compute power for the CORRECT force",
        "Maximum applied power at take-off is F_applied v=104×4=416 W. F_net v=64×4=256 W is the kinetic-energy rate, not total mechanical power of the push."
      ],
      [
        "Check contact and free-flight phases",
        "52 J applied energy during contact becomes 32 J kinetic plus 20 J gravitational potential. After separation, the toy rises under gravity alone."
      ]
    ],
    "checks": [
      "I used the extra 0.80 m flight height to infer take-off speed 4 m/s.",
      "I included the 20 J gravitational energy rise during the 0.50 m ground push.",
      "I calculated applied F=104 N separately from net F=64 N.",
      "I found applied push power 416 W rather than net kinetic-energy rate 256 W."
    ],
    "diagnoses": [
      "I used the 0.80 m free-flight height as contact distance.",
      "I forgot the gravitational work while the toy was still being pushed.",
      "I treated net F×v as the power delivered by the applied force.",
      "I continued the applied push into free flight.",
      "The phase model was correct but I want to check arithmetic.",
      "I'm still unsure which force provides the energy."
    ],
    "diagnosisTips": [
      "Mark the contact boundary at 0.50 m and the separate later rise of 0.80 m.",
      "Gravity acts throughout both phases, including during the push; add contact mgs to the kinetic gain.",
      "Net F explains dK/dt; applied F explains work rate delivered by the contact push.",
      "Only gravity acts during flight; no extra contact work is supplied after separation.",
      "Recheck work units (N·m=J), power units (N·m/s=W) and the energy balance.",
      "Start with two labelled boxes, CONTACT and FLIGHT, and one force arrow for each agent."
    ],
    "boundary": "The same 4 kg toy still starts from rest and is pushed upward for 0.50 m, but its later FREE flight rise is only 0.45 m. Find new take-off speed, contact applied force and maximum applied mechanical power; distinguish net power.",
    "boundaryCheck": "Later rise 0.45 m implies v²=9 and take-off v=3 m/s. Contact kinetic gain is 18 J; contact gravity rise needs 20 J. Applied work=38 J, applied force=76 N, MAXIMUM applied power=76×3=228 W. Net force=(76−40)=36 N and its kinetic-energy rate at take-off is 108 W. The 0.45 m is not the push distance.",
    "boundaryFields": [
      {
        "id": "speed",
        "label": "New take-off speed (m/s)",
        "type": "number",
        "expected": 3,
        "tol": 0.04,
        "mistake": "Use the 0.45 m EXTRA rise after contact."
      },
      {
        "id": "force",
        "label": "New applied force (N)",
        "type": "number",
        "expected": 76,
        "tol": 0.4,
        "mistake": "Applied contact work is kinetic gain 18 J plus 20 J gravitational gain."
      },
      {
        "id": "power",
        "label": "New maximum mechanical applied power (W)",
        "type": "number",
        "expected": 228,
        "tol": 1,
        "mistake": "Use 76 N × 3 m/s."
      },
      {
        "id": "netPower",
        "label": "New net kinetic-energy rate at take-off (W)",
        "type": "number",
        "expected": 108,
        "tol": 1,
        "mistake": "Use (76−40)×3, not applied power."
      },
      {
        "id": "why",
        "label": "Explain the changed condition and model",
        "type": "textarea"
      }
    ]
  },
  "F02": {
    "donor": "PR #55 · E07",
    "title": "Two incline journeys, two friction losses",
    "prediction": "Why does a block lose energy to friction on BOTH the ascent and the descent? Predict which physical model will be necessary and what might change at the phase boundary.",
    "challenge": "A new block is launched uphill on a rough incline of 45°. Its kinetic friction coefficient μ is constant. After stopping it returns to its original launch position at speed (2/3) of the initial speed v₀. Assume it DOES slide back and sin45°=cos45°. Determine μ from two properly signed motion phases and explain why mass and v₀ cancel.",
    "fields": [
      {
        "id": "model",
        "label": "Which model describes the full uphill and downhill trip?",
        "type": "select",
        "choices": [
          "Choose an idea",
          "Uphill gravity + friction; downhill gravity − friction",
          "Gravity and friction both cancel",
          "Only the ascent loses friction energy",
          "I'm not sure yet"
        ],
        "expected": "Uphill gravity + friction; downhill gravity − friction",
        "mistake": "Ascent spends kinetic energy on gravity AND friction; on descent gravity gives kinetic energy while friction removes it."
      },
      {
        "id": "frictionUp",
        "label": "On ascent, friction points...",
        "type": "select",
        "choices": [
          "Choose an idea",
          "Down the slope",
          "Up the slope",
          "Sideways",
          "Not sure"
        ],
        "expected": "Down the slope",
        "tol": 0,
        "mistake": "Friction always opposes travel; uphill travel means downhill friction."
      },
      {
        "id": "frictionDown",
        "label": "On descent, friction points...",
        "type": "select",
        "choices": [
          "Choose an idea",
          "Down the slope",
          "Up the slope",
          "Sideways",
          "Not sure"
        ],
        "expected": "Up the slope",
        "tol": 0,
        "mistake": "On return the slider moves downhill, so friction points uphill."
      },
      {
        "id": "upFactor",
        "label": "Uphill retarding factor in units of g·sin45°",
        "type": "text",
        "mistake": "On ascent the stopping factor is (1 + μ) times g sin45°."
      },
      {
        "id": "downFactor",
        "label": "Downhill accelerating factor in units of g·sin45°",
        "type": "text",
        "mistake": "On descent the acceleration factor is (1 − μ) times g sin45°."
      },
      {
        "id": "returnRatioSquared",
        "label": "(v_return / v₀)²",
        "type": "number",
        "expected": 0.4444444444444444,
        "tol": 0.008,
        "mistake": "Square the 2/3 speed ratio before using energy or acceleration."
      },
      {
        "id": "mu",
        "label": "Coefficient of kinetic friction μ",
        "type": "number",
        "expected": 0.38461538461538464,
        "tol": 0.008,
        "mistake": "At 45°, (1−μ)/(1+μ) = (2/3)² = 4/9, so μ = 5/13."
      },
      {
        "id": "reason",
        "label": "Explain why friction costs energy on both legs and use the SAME distance",
        "type": "textarea",
        "mistake": "Explain this physical model in your own words before comparing the worked reasoning."
      }
    ],
    "hints": [
      "Draw a separate friction arrow for UP and DOWN travel, both opposite the motion.",
      "Write the uphill stopping distance as v₀²/[2g(sin45°+μcos45°)]. The SAME distance is used on descent.",
      "Relate the RETURN SPEED SQUARED to the ratio of downhill and uphill acceleration. With 45°, sine and cosine are equal."
    ],
    "worked": [
      [
        "Two phase-specific along-slope force models",
        "On ascent, stopping acceleration magnitude is g(sin45°+μcos45°); on descent, forward acceleration is g(sin45°−μcos45°). Gravity direction stays downhill; friction reverses."
      ],
      [
        "Use one shared stopping distance",
        "d=v₀²/[2g(sinθ+μcosθ)] and v_return²=2gd(sinθ−μcosθ). Thus r²=(sinθ−μcosθ)/(sinθ+μcosθ)."
      ],
      [
        "Cancel the equal sine and cosine",
        "At 45°, r²=(1−μ)/(1+μ). The observed r=2/3 gives r²=4/9."
      ],
      [
        "Solve and check physical bound",
        "4(1+μ)=9(1−μ), giving 13μ=5 and μ=5/13≈0.384615. It is nonnegative and less than tan45°=1, so the block slides back."
      ],
      [
        "Reconcile energy losses",
        "The block returns to the same height, so gravity work over the full path is zero. Friction removes energy during ascent and descent and makes return speed smaller than v₀."
      ]
    ],
    "checks": [
      "I gave friction opposite movement separately on the uphill and downhill legs.",
      "I used the SAME stopping distance with two differently signed accelerations.",
      "I squared the 2/3 speed ratio to get 4/9, then solved μ=5/13.",
      "I checked the resulting μ is positive and low enough for descent to occur."
    ],
    "diagnoses": [
      "I drew friction down the ramp on both legs.",
      "I forgot to square the speed ratio.",
      "I used a different stopping distance for descent.",
      "I treated gravity as losing net energy on a completed round trip.",
      "My arrows were correct; I need to check the algebra.",
      "I'm not sure why two phases share the same distance."
    ],
    "diagnosisTips": [
      "Friction always points opposite the current motion, so its direction must flip.",
      "Energy is proportional to speed squared; square 2/3 before calculating μ.",
      "The block stops at the same point and returns to the same base, so each leg spans the same d.",
      "Gravity loses and regains equal potential energy on this closed vertical route; friction dissipates energy twice.",
      "Simplify (4/9)(1+μ)=1−μ without changing the original force signs.",
      "Draw a start, turning point and return arrow, then write which forces oppose each direction."
    ],
    "boundary": "On the SAME 45° incline, a new trial returns to its starting position at speed (3/4)v₀. What μ is implied, and why is it less than in the original trial?",
    "boundaryCheck": "For the 45° incline, r²=(1−μ)/(1+μ). With r=3/4, r²=9/16, so 9(1+μ)=16(1−μ). Thus 25μ=7 and μ=7/25=0.28, smaller than 5/13. Less friction means less round-trip energy loss. Gravity still cancels over the full return.",
    "boundaryFields": [
      {
        "id": "ratioSquared",
        "label": "New squared return-speed ratio",
        "type": "number",
        "expected": 0.5625,
        "tol": 0.009,
        "mistake": "Square 3/4 before solving friction."
      },
      {
        "id": "mu",
        "label": "New coefficient μ",
        "type": "number",
        "expected": 0.28,
        "tol": 0.008,
        "mistake": "Solve (1−μ)/(1+μ)=9/16."
      },
      {
        "id": "why",
        "label": "Explain the changed condition and model",
        "type": "textarea"
      }
    ]
  },
  "F03": {
    "donor": "PR #55 · E08",
    "title": "New spring-force equilibrium, new turning point",
    "prediction": "Where does the spring stop after the external force suddenly changes? Predict which physical model will be necessary and what might change at the phase boundary.",
    "challenge": "A different spring with k=50 N/m holds its block at rest compressed at x_i=−0.20 m under an old force −10 N. At time zero the applied force is replaced suddenly by constant +15 N and it is released from rest. Use x positive RIGHT from natural length. Find new equilibrium, initial post-switch effective energy, far positive turning point and an energy check.",
    "fields": [
      {
        "id": "initialX",
        "label": "Initial signed spring position (m)",
        "type": "number",
        "expected": -0.2,
        "tol": 0.004,
        "mistake": "A compressed spring position left of natural length is signed −0.20 m."
      },
      {
        "id": "newEquilibrium",
        "label": "New equilibrium position (m)",
        "type": "number",
        "expected": 0.3,
        "tol": 0.004,
        "mistake": "Use NEW +15 N in k x_eq=F_new, never the original −10 N."
      },
      {
        "id": "initialEnergy",
        "label": "Effective energy at initial rest position (J)",
        "type": "number",
        "expected": 4,
        "tol": 0.06,
        "mistake": "Use ½kx²−F_new x at the original position after switching."
      },
      {
        "id": "turning",
        "label": "Other far positive turning position (m)",
        "type": "number",
        "expected": 0.8,
        "tol": 0.008,
        "mistake": "Turning points are symmetric about NEW +0.30 m equilibrium, not x=0."
      },
      {
        "id": "turningEnergy",
        "label": "Effective potential at far turning point (J)",
        "type": "number",
        "expected": 4,
        "tol": 0.06,
        "mistake": "Compute post-switch U_eff at +0.80 m; it must equal the initial 4 J."
      },
      {
        "id": "model",
        "label": "Which energy is conserved after the force switch?",
        "type": "select",
        "choices": [
          "Choose an idea",
          "Spring elastic energy only",
          "K + spring energy − F_new·x",
          "K + spring energy − F_old·x",
          "Not sure yet"
        ],
        "expected": "K + spring energy − F_new·x",
        "tol": 0,
        "mistake": "Spring-only energy omits work done by the new persistent force."
      },
      {
        "id": "reason",
        "label": "Explain why the new equilibrium sets the turning-point symmetry",
        "type": "textarea",
        "mistake": "Explain this physical model in your own words before comparing the worked reasoning."
      }
    ],
    "hints": [
      "Initial compression is NEGATIVE x. Put the old equilibrium and new applied force on one signed axis.",
      "Once switched to constant +15 N, use x_eq=F_new/k; do not keep the old applied force in the motion equation.",
      "For post-switch turning points K=0 and U_eff is equal. Complete the square or use symmetry about the NEW equilibrium."
    ],
    "worked": [
      [
        "Check initial holding state",
        "At x_i=−0.20 m with k=50 N/m, spring force is −kx_i=+10 N, balanced by the old external −10 N. At the moment of switching the block is at rest."
      ],
      [
        "Change to the NEW equilibrium",
        "New applied force is +15 N. Therefore kx_eq=+15 and x_eq=+0.30 m."
      ],
      [
        "Calculate post-switch effective energy",
        "U_eff=½(50)x²−15x J. At x_i=−0.20 m: U_eff=1+3=4 J; initial K=0."
      ],
      [
        "Use symmetry or solve the turning-point quadratic",
        "The other turning point is x_other=2x_eq−x_i=0.60−(−0.20)=+0.80 m. Substitution gives U_eff(0.80)=16−12=4 J, matching the starting value."
      ],
      [
        "Explain why the spring-only model fails",
        "The new external constant force moves the block and does work. Only K+½kx²−15x is conserved after the switch; spring energy alone changes."
      ]
    ],
    "checks": [
      "I identified the initial compressed position x_i=−0.20 m and the old holding force correctly.",
      "I used the NEW +15 N force to calculate equilibrium x_eq=+0.30 m.",
      "I conserved post-switch K+U_eff and found the far turning point x=+0.80 m.",
      "I checked equal effective energies 4 J at both turning points and explained why spring energy alone is insufficient."
    ],
    "diagnoses": [
      "I treated the compressed starting position as +0.20 m.",
      "I conserved spring energy alone and ignored the new force's work.",
      "I kept the old applied holding force in the new effective potential.",
      "I reflected about natural length x=0 instead of new equilibrium.",
      "My effective potential was right but I made an arithmetic error.",
      "I'm not sure how changing the force moves equilibrium."
    ],
    "diagnosisTips": [
      "With x positive rightward, compression to the left is negative; the spring force has the opposite sign.",
      "The new constant force supplies work; include −F_new x in the potential energy.",
      "Only the force actually applied after t=0 belongs in the post-switch effective potential.",
      "Turn points of a quadratic with constant forcing are symmetric about F_new/k, not natural length.",
      "Recompute U_eff at both turning positions and compare the same energy value.",
      "Start with two snapshots: old held equilibrium and new switched force, then redraw the axis."
    ],
    "boundary": "Keep k=50 N/m and initial rest position x_i=−0.20 m, but change the switched constant force to +5 N. Find the NEW equilibrium and the OTHER turning point; verify effective potential at both.",
    "boundaryCheck": "With +5 N after switch, new equilibrium is x_eq=5/50=+0.10 m and the far turning point is x=2(0.10)−(−0.20)=+0.40 m. Initial effective energy is ½(50)(0.20²)−5(−0.20)=1+1=2 J. At x=+0.40 m, U_eff=½(50)(0.40²)−5(0.40)=4−2=2 J. The new force changes the equilibrium and turning point; old holding force does not enter post-switch energy.",
    "boundaryFields": [
      {
        "id": "eq",
        "label": "New equilibrium (m)",
        "type": "number",
        "expected": 0.1,
        "tol": 0.004,
        "mistake": "Use NEW +5 N divided by k=50."
      },
      {
        "id": "turn",
        "label": "New far turning position (m)",
        "type": "number",
        "expected": 0.4,
        "tol": 0.007,
        "mistake": "Reflect −0.20 m around new +0.10 m equilibrium."
      },
      {
        "id": "energy",
        "label": "New effective energy at both turns (J)",
        "type": "number",
        "expected": 2,
        "tol": 0.05,
        "mistake": "Use ½kx²−5x and compare both endpoints."
      },
      {
        "id": "why",
        "label": "Explain the changed condition and model",
        "type": "textarea"
      }
    ]
  }
});
