"""
Grade9 v4.0 — Lot 07 Generator (Batch B, Questions 26–30)
Generates:
  - 5x QUESTION_AUDIT.json (questions/26..30)
  - 5x SOURCE_ONLY.json (source_only/26..30)
  - review/index.html (Responsive Dashboard)
"""

import os
import json
import hashlib
from datetime import datetime, timezone

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_PATH = os.path.join(LOT_DIR, "ROSTER_PRIVATE.json")

with open(ROSTER_PATH, encoding="utf-8") as f:
    roster_bundle = json.load(f)

lot07_items = [r for r in roster_bundle["roster"] if r["lot"] == "LOT-07"]
assert len(lot07_items) == 5, f"Expected 5 items in Lot 07, got {len(lot07_items)}"

PHYS_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
PHYS_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"

lot07_data = [
    {
        "sequence": 26,
        "batch_sequence": 11,
        "source_id": "EX-M78",
        "task_identity": "Q-ID-29",
        "paper": "JEE Main 2019 (Online) 9th January Morning Slot",
        "stem_text": "A block of mass m, lying on a smooth horizontal surface, is attached to a spring (of negligible mass) of spring constant k. The other end of the spring is fixed, as shown in the figure. The block is initially at rest in its equilibrium position. If now the block is pulled with a constant force F, the maximum speed of the block is : [FIG-stem-1]",
        "options": [
            "A: (2𝐹)/(√(𝑚𝑘))",
            "B: (𝐹)/(𝜋√(𝑚𝑘))",
            "C: (𝜋𝐹)/(√(𝑚𝑘))",
            "D: (𝐹)/(√(𝑚𝑘))"
        ],
        "figure_reference": "[FIG-stem-1] Horizontal spring-block setup unverified against master",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "source_custody": "PARTIAL (spring-block diagram unresolved)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "SPRING_BLOCK_WORK_ENERGY_MAX_SPEED",
            "derivation": "Maximum speed occurs at the equilibrium position where net force is zero: F_net = F - k*x = 0 => x_0 = F/k. By Work-Energy Theorem from rest (x=0, v=0) to equilibrium position (x_0, v_max): W_net = W_force + W_spring = Delta KE => F*x_0 - 1/2 k x_0^2 = 1/2 m v_max^2. Substituting x_0 = F/k: F*(F/k) - 1/2 k*(F/k)^2 = F^2/k - F^2/(2k) = F^2/(2k) = 1/2 m v_max^2 => v_max^2 = F^2 / (mk) => v_max = F / sqrt(mk). Matches Option D.",
            "predicted_option": "D: (𝐹)/(√(𝑚𝑘))",
            "limiting_cases": "If k -> infinity, v_max -> 0. If m -> infinity, v_max -> 0. Simple harmonic motion verification: equilibrium shift x_0 = F/k, amplitude A = F/k, angular frequency omega = sqrt(k/m), maximum speed v_max = omega * A = sqrt(k/m) * (F/k) = F / sqrt(mk)."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "CALCULATE_MAX_SPEED_UNDER_CONSTANT_FORCE",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Equilibrium condition and quadratic substitution"},
                    "physics_concepts": {"score": 1, "rationale": "Work-Energy Theorem with spring potential and constant force"},
                    "cognitive_depth": {"score": 1, "rationale": "Identifying that maximum speed occurs at zero acceleration"},
                    "representation_load": {"score": 0, "rationale": "Diagram confirms standard horizontal spring layout"},
                    "structural_complexity": {"score": 1, "rationale": "Coupled force equilibrium and energy balance"}
                },
                "total": 4
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (diagram needed to verify spring anchoring and axis orientation)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Verify official NTA diagram and key for 09-01-2019 Morning Slot."
    },
    {
        "sequence": 27,
        "batch_sequence": 12,
        "source_id": "EX-M79",
        "task_identity": "Q-ID-30",
        "paper": "JEE Main 2018 (Online) 16th April Morning Slot",
        "stem_text": "A body of mass m starts moving from rest along x-axis so that its velocity varies as 𝜐=𝑎√(𝑠) where a is a constant and s is the distance covered by the body. The total work done by all the forces acting on the body in the first t seconds after the start of the motion is :",
        "options": [
            "A: (1)/(8) m a4 t2",
            "B: 8 m a4 t2",
            "C: 4 m a4 t2",
            "D: (1)/(4) m a4 t2"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained mathematical question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "WORK_ENERGY_THEOREM_VELOCITY_DISTANCE_RELATION",
            "derivation": "Velocity definition: v = ds/dt = a * s^(1/2). Separating variables: s^(-1/2) ds = a dt. Integrating from s=0 at t=0: 2 * s^(1/2) = a * t => s^(1/2) = (a * t) / 2 => s(t) = (a^2 * t^2) / 4. Velocity as a function of time: v(t) = ds/dt = (a^2 * t) / 2. By Work-Energy Theorem: Total work done W = Delta KE = 1/2 m v(t)^2 - 0 = 1/2 m [ (a^2 * t) / 2 ]^2 = 1/2 m [ (a^4 * t^2) / 4 ] = (1/8) m a^4 t^2. Matches Option A.",
            "predicted_option": "A: (1)/(8) m a4 t2",
            "limiting_cases": "If a=0, W=0. If t=0, W=0. Dimensional verification: [a] = m^(1/2) s^(-1). [m a^4 t^2] = kg * (m^2 s^(-4)) * s^2 = kg m^2 s^(-2) = Joules. Factor 1/8 matches uniquely."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "DERIVE_WORK_FROM_DISTANCE_VELOCITY_RELATION",
            "difficulty_evidence": {
                "band": "D3",
                "components": {
                    "math_steps": {"score": 2, "rationale": "Separation of variables integration and kinetic energy computation"},
                    "physics_concepts": {"score": 1, "rationale": "Work-Energy Theorem W = Delta KE and kinematic definitions"},
                    "cognitive_depth": {"score": 2, "rationale": "Transforming distance-dependent velocity to time-dependent kinetic energy"},
                    "representation_load": {"score": 0, "rationale": "Pure algebraic and symbolic formulation"},
                    "structural_complexity": {"score": 1, "rationale": "Non-linear differential relation"}
                },
                "total": 6
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "cell": "WPE-01-WORK-VARIABLE-D3",
            "version": "0.2.0",
            "sha256": PHYS_BP_SHA
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "version": "0.1.0",
            "sha256": PHYS_ADAPTER_SHA
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:INDEPENDENT_REVIEW_PENDING (requires unexposed blind physics review before admission)"
        ],
        "next_action": "Verify official NTA key and submit for independent blind review."
    },
    {
        "sequence": 28,
        "batch_sequence": 13,
        "source_id": "EX-M82",
        "task_identity": "Q-ID-32",
        "paper": "JEE Main 2017 (Online) 8th April Morning Slot",
        "stem_text": "An object is dropped from a height h from the ground. Every time it hits the ground it loses 50% of its kinetic energy. The total distance covered as t → ∞ is :",
        "options": [
            "A: 3h",
            "B: ∞",
            "C: (5)/(3) h",
            "D: (8)/(3) h"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained mathematical question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "INELASTIC_BOUNCE_INFINITE_SERIES",
            "derivation": "Initial drop from height h: distance d0 = h, kinetic energy before 1st impact KE0 = mgh. At 1st bounce, it loses 50% KE, retaining KE1 = 0.5 mgh. Rebound height h1 = KE1 / (mg) = h/2. Up-and-down distance for 1st bounce is 2*h1 = 2*(h/2) = h. At 2nd bounce, retains KE2 = 0.5 KE1 = 0.25 mgh, rebound height h2 = h/4, contributing 2*h2 = h/2. For each subsequent bounce k >= 1, rebound height is h_k = h / 2^k, contributing distance 2*h_k = 2h / 2^k = h / 2^(k-1). Total distance covered: D = d0 + sum_{k=1}^infinity 2*h_k = h + [ h + h/2 + h/4 + ... ] = h + h / (1 - 1/2) = h + 2h = 3h. Matches Option A.",
            "predicted_option": "A: 3h",
            "limiting_cases": "If 0% KE lost (elastic bounce), D = infinity (Option B). If 100% lost (inelastic stick), D = h. With restitution coefficient e where e^2 = 0.5: D = h * (1 + e^2) / (1 - e^2) = h * (1 + 0.5) / (1 - 0.5) = h * 1.5 / 0.5 = 3h."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "SUM_INFINITE_BOUNCE_SERIES",
            "difficulty_evidence": {
                "band": "D3",
                "components": {
                    "math_steps": {"score": 2, "rationale": "Infinite geometric series summation"},
                    "physics_concepts": {"score": 1, "rationale": "Inelastic collision and gravitational potential energy"},
                    "cognitive_depth": {"score": 2, "rationale": "Distinguishing asymmetric initial drop from symmetric rebound paths"},
                    "representation_load": {"score": 0, "rationale": "Pure textual and algebraic formulation"},
                    "structural_complexity": {"score": 1, "rationale": "Infinite limit integration/summation"}
                },
                "total": 6
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "cell": "WPE-02-ENERGY-CONSERVATION-D3",
            "version": "0.2.0",
            "sha256": PHYS_BP_SHA
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "version": "0.1.0",
            "sha256": PHYS_ADAPTER_SHA
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:INDEPENDENT_REVIEW_PENDING (requires unexposed blind physics review before admission)"
        ],
        "next_action": "Verify official NTA key and submit for independent blind review."
    },
    {
        "sequence": 29,
        "batch_sequence": 14,
        "source_id": "EX-M84",
        "task_identity": "Q-ID-33",
        "paper": "JEE Main 2016 (Online) 10th April Morning Slot",
        "stem_text": "A particle of mass M is moving in a circle of fixed radius R in such a way that its centripetal acceleration at time t is given by n2 R t2 where n is a constant. The power delivered to the particle by the force acting on it, is :",
        "options": [
            "A: M n2 R2 t",
            "B: M n R2 t",
            "C: M n R2 t2",
            "D: (1)/(2) M n2 R2 t2"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained mathematical question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "CIRCULAR_DYNAMICS_TANGENTIAL_POWER",
            "derivation": "Centripetal acceleration a_c = v^2 / R = n^2 R t^2 => v^2 = n^2 R^2 t^2 => v(t) = n R t. Tangential acceleration a_t = dv/dt = n R. Centripetal force is perpendicular to velocity and does zero work (zero power). Tangential force F_t = M a_t = M (n R). Power delivered P = F_t * v = (M n R) * (n R t) = M n^2 R^2 t. Alternatively: KE = 1/2 M v^2 = 1/2 M (n^2 R^2 t^2) => Power P = d(KE)/dt = 1/2 M n^2 R^2 (2t) = M n^2 R^2 t. Matches Option A.",
            "predicted_option": "A: M n2 R2 t",
            "limiting_cases": "If n=0 or t=0, P=0. Dimensional analysis: [M n^2 R^2 t] = kg * (s^-2) * (m^2) * s = kg m^2 s^-3 = Watt. Option A is the unique exact result."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "CALCULATE_CIRCULAR_TANGENTIAL_POWER",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Differentiation of kinetic energy with respect to time"},
                    "physics_concepts": {"score": 1, "rationale": "Work done by centripetal vs tangential forces in circular motion"},
                    "cognitive_depth": {"score": 1, "rationale": "Recognizing that power equals rate of change of kinetic energy"},
                    "representation_load": {"score": 0, "rationale": "Pure algebraic and text description"},
                    "structural_complexity": {"score": 1, "rationale": "Circular kinematics coupled with dynamic power"}
                },
                "total": 4
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Verify official NTA key and submit for independent blind review."
    },
    {
        "sequence": 30,
        "batch_sequence": 15,
        "source_id": "EX-M85",
        "task_identity": "Q-ID-34",
        "paper": "JEE Main 2016 (Online) 10th April Morning Slot",
        "stem_text": "Velocity-time graph for a body of mass 10 kg is shown in figure. Work-done on the body in first two seconds of the motion is : [FIG-stem-1]",
        "options": [
            "A: 12000 J",
            "B: − 12000 J",
            "C: − 4500 J",
            "D: − 9300 J"
        ],
        "figure_reference": "[FIG-stem-1] Velocity-time graph unverified against authentic master",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "source_custody": "PARTIAL (v-t graph unresolved)",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "WORK_ENERGY_THEOREM_VT_GRAPH",
            "derivation": "Work done equals change in kinetic energy: W = Delta KE = 1/2 m (v_2^2 - v_0^2). Coaching solution reports v_0 = 50 m/s and v_2 = 40 m/s, yielding W = 1/2 * 10 * (40^2 - 50^2) = 5 * (1600 - 2500) = -4500 J (Option C). However, the initial velocity and acceleration slope cannot be independently verified without the authentic diagram asset.",
            "predicted_option": "HOLD:FIGURE_UNRESOLVED",
            "limiting_cases": "Cannot confirm slope or velocity values without original figure."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "CALCULATE_WORK_FROM_VT_GRAPH",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Evaluating kinetic energy difference"},
                    "physics_concepts": {"score": 1, "rationale": "Work-Energy Theorem from kinematic graph"},
                    "cognitive_depth": {"score": 1, "rationale": "Reading speed at t=2 from linear deceleration graph"},
                    "representation_load": {"score": 1, "rationale": "Graph reading required"},
                    "structural_complexity": {"score": 0, "rationale": "Direct kinematic reading"}
                },
                "total": 4
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (v-t graph unverified against authentic master)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Obtain authentic NTA question paper for 10-04-2016 Morning Slot to extract v-t diagram."
    }
]

# Write QUESTION_AUDIT.json and SOURCE_ONLY.json for LOT-07
for item in lot07_data:
    seq = item["sequence"]
    sid = item["source_id"]

    q_dir = os.path.join(LOT_DIR, "questions", f"{seq:02d}")
    os.makedirs(q_dir, exist_ok=True)

    stem = item["stem_text"]
    stem_sha = hashlib.sha256(stem.encode("utf-8")).hexdigest()

    audit_record = {
        "sequence": seq,
        "batch_sequence": item["batch_sequence"],
        "task_identity": item["task_identity"],
        "stable_id": f"G9V4-PHYS-WPE-{sid}",
        "source_id": sid,
        "lot": "LOT-07",
        "batch": "BATCH-B",
        "paper": item["paper"],
        "source_type": "JEE_MAIN_PAST_EXAM_QUESTION",
        "source_custody": item["source_custody"],
        "stem_text": stem,
        "stem_sha256": stem_sha,
        "source_hash": stem_sha,
        "source_record_digest": stem_sha,
        "duplicate_parent": None,
        "scope": "IN_SCOPE_WPE_ONLY",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": item["figure_status"],
        "figure_reference": item["figure_reference"],
        "options": item["options"],
        "solve_exposure": "EXPOSED",
        "solve_status": item["solve_status"],
        "candidate_solve": item["candidate_solve"],
        "sl2": item["sl2"],
        "blueprint_fit": item["blueprint_fit"],
        "adapter_fit": item["adapter_fit"],
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_CP4_GATE",
        "b2_blind_status": "UNREVIEWED",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": item["blockers"],
        "next_action": item["next_action"]
    }

    with open(os.path.join(q_dir, "QUESTION_AUDIT.json"), "w", encoding="utf-8") as f:
        json.dump(audit_record, f, indent=2)

    # Source-only sealed packet
    s_dir = os.path.join(LOT_DIR, "source_only", f"{seq:02d}")
    os.makedirs(s_dir, exist_ok=True)

    source_only_record = {
        "source_id": sid,
        "task_identity": item["task_identity"],
        "sequence": seq,
        "batch_sequence": item["batch_sequence"],
        "paper": item["paper"],
        "stem_text": stem,
        "stem_sha256": stem_sha,
        "options": item["options"],
        "figure_reference": item["figure_reference"],
        "confidentiality_notice": "SEALED SOURCE-ONLY PACKET FOR BLIND INDEPENDENT REVIEW. Contains NO answers, keys, explanations, candidate solutions, SL2 factor scores, or prior review commentary."
    }

    with open(os.path.join(s_dir, "SOURCE_ONLY.json"), "w", encoding="utf-8") as f:
        json.dump(source_only_record, f, indent=2)

print("Generated 5 question audits and 5 sealed source-only packets for LOT-07.")

# Generate review/index.html
review_dir = os.path.join(LOT_DIR, "review")
os.makedirs(review_dir, exist_ok=True)

rows_html = []
for item in lot07_data:
    bp_disp = item["blueprint_fit"]
    if isinstance(bp_disp, dict):
        bp_cell = f"<strong>{bp_disp['blueprint_id']}</strong><br><small>{bp_disp['cell']}</small>"
    else:
        bp_cell = f"<span class='badge badge-hold'>{bp_disp}</span>"

    rows_html.append(f"""
    <tr>
        <td class="col-seq"><strong>#{item['sequence']}</strong><br><small class="mono">{item['task_identity']}</small><br><small>Batch Seq: #{item['batch_sequence']}</small></td>
        <td class="col-source">
            <strong>{item['source_id']}</strong><br>
            <small class="text-muted">{item['paper']}</small><br>
            <span class="badge badge-source">{item['source_custody']}</span>
            <span class="badge badge-fig">{item['figure_status']}</span>
        </td>
        <td class="col-stem">
            <div class="stem-preview">{item['stem_text'][:160]}...</div>
            <details class="candidate-details">
                <summary>View Candidate Solve & Working</summary>
                <div class="solve-box">
                    <p><strong>Predicted Option:</strong> {item['candidate_solve']['predicted_option']}</p>
                    <p><strong>Method:</strong> <code>{item['candidate_solve']['method']}</code></p>
                    <p><strong>Derivation:</strong> {item['candidate_solve']['derivation']}</p>
                    <p><strong>Limiting Cases:</strong> {item['candidate_solve']['limiting_cases']}</p>
                </div>
            </details>
        </td>
        <td class="col-cog">
            <strong>{item['sl2']['decisive_operation']}</strong> ({item['sl2']['difficulty_evidence']['band']})<br>
            <small>Score: {item['sl2']['difficulty_evidence']['total']}/10</small><br>
            <span class="badge badge-prop">{item['sl2']['demand_proposal']['status']}</span>
        </td>
        <td class="col-bp">{bp_cell}</td>
        <td class="col-gates">
            <span class="badge badge-admission">NOT_ADMITTED</span>
            <ul class="blocker-list">
                {"".join(f"<li>{b}</li>" for b in item['blockers'])}
            </ul>
        </td>
    </tr>
    """)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade9 v4.0 — LOT-07 Source & Candidate Solve Audit (Questions 26–30)</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --text: #0f172a;
            --text-muted: #64748b;
            --primary: #2563eb;
            --danger: #b91c1c;
            --warning: #d97706;
            --success: #15803d;
            --neutral-bg: #f1f5f9;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 16px;
            font-size: 14px;
            min-width: 0;
            overflow-x: hidden;
        }}
        .container {{
            max-width: 1365px;
            margin: 0 auto;
            background: var(--surface);
            border-radius: 8px;
            border: 1px solid var(--border);
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            min-width: 0;
        }}
        header {{
            border-bottom: 2px solid var(--border);
            padding-bottom: 16px;
            margin-bottom: 20px;
        }}
        h1 {{ font-size: 22px; font-weight: 700; color: var(--text); margin-bottom: 6px; word-break: break-word; }}
        .header-meta {{
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .notice-banner {{
            background: #fffbeb;
            border-left: 4px solid var(--warning);
            padding: 14px 18px;
            margin-bottom: 24px;
            border-radius: 0 4px 4px 0;
            font-size: 13px;
            color: #92400e;
        }}
        .table-wrapper {{
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 24px;
            -webkit-overflow-scrolling: touch;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            min-width: 900px;
        }}
        th, td {{
            padding: 12px 14px;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }}
        th {{
            background: #f8fafc;
            font-weight: 600;
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
        }}
        .col-seq {{ width: 110px; }}
        .col-source {{ width: 220px; word-break: break-word; }}
        .col-stem {{ min-width: 260px; word-break: break-word; }}
        .col-cog {{ width: 140px; }}
        .col-bp {{ width: 140px; word-break: break-word; }}
        .col-gates {{ width: 260px; word-break: break-word; }}

        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            margin: 2px 0;
            word-break: break-all;
        }}
        .badge-admission {{ background: #fef2f2; color: var(--danger); border: 1px solid #fecaca; }}
        .badge-hold {{ background: #fff7ed; color: var(--warning); border: 1px solid #fed7aa; }}
        .badge-source {{ background: #eff6ff; color: var(--primary); }}
        .badge-fig {{ background: #f1f5f9; color: var(--text-muted); }}
        .badge-prop {{ background: #f3e8ff; color: #7e22ce; }}

        .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        .text-muted {{ color: var(--text-muted); }}
        .stem-preview {{ font-size: 13px; margin-bottom: 8px; color: #334155; }}
        .candidate-details {{
            margin-top: 6px;
            font-size: 12px;
        }}
        .candidate-details summary {{
            cursor: pointer;
            color: var(--primary);
            font-weight: 600;
        }}
        .solve-box {{
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 10px;
            margin-top: 6px;
        }}
        .solve-box p {{ margin-bottom: 6px; }}
        .solve-box p:last-child {{ margin-bottom: 0; }}
        .blocker-list {{
            margin-top: 4px;
            padding-left: 16px;
            font-size: 11px;
            color: var(--danger);
        }}
        .blocker-list li {{ margin-bottom: 2px; }}
        footer {{
            border-top: 1px solid var(--border);
            padding-top: 16px;
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}
        @media (max-width: 600px) {{
            body {{ padding: 8px; }}
            .container {{ padding: 12px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Grade9 v4.0 — LOT-07 Source & Candidate Solve Audit (Questions 26–30)</h1>
            <div class="header-meta">
                <span><strong>Batch:</strong> BATCH-B (CP-3)</span>
                <span><strong>Lot:</strong> LOT-07 (Roster Positions 11–15)</span>
                <span><strong>Scope:</strong> Physics / WPE</span>
                <span><strong>Admissions:</strong> 0 / 5 (Strict Fail-Closed)</span>
            </div>
        </header>

        <div class="notice-banner">
            <strong>Mandatory Governance Boundary:</strong> ZERO academic approvals inferred from software validation. All 5 candidate questions remain in state <code>NOT_ADMITTED</code>. No Core2 learner cards have been constructed. Official NTA master answer keys and authentic figure assets remain on HOLD awaiting independent review.
        </div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th class="col-seq">Seq / Task ID</th>
                        <th class="col-source">Source & Custody</th>
                        <th class="col-stem">Question Stem & Candidate Solve</th>
                        <th class="col-cog">SL2 Proposal</th>
                        <th class="col-bp">Blueprint / Adapter</th>
                        <th class="col-gates">Academic Gate & Blockers</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows_html)}
                </tbody>
            </table>
        </div>

        <footer>
            <div>Produced by Local Coding Agent | Low-Discretion Autonomous Mode</div>
            <div>No academic approval inferred from software validation.</div>
        </footer>
    </div>
</body>
</html>
"""

html_path = os.path.join(review_dir, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated LOT-07 review dashboard: {html_path}")
