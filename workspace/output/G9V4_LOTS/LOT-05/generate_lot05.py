"""
Grade9 v4.0 — Lot 05 Generator (Batch B, Questions 16–20)
Generates:
  - 5x QUESTION_AUDIT.json (questions/16..20)
  - 5x SOURCE_ONLY.json (source_only/16..20)
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

lot05_items = [r for r in roster_bundle["roster"] if r["lot"] == "LOT-05"]
assert len(lot05_items) == 5, f"Expected 5 items in Lot 05, got {len(lot05_items)}"

# Verified Blueprint pin from docs/agent-entry/CURRENT_PATHS.json
PHYS_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
PHYS_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"

lot05_data = [
    {
        "sequence": 16,
        "batch_sequence": 1,
        "source_id": "EX-M56",
        "task_identity": "Q-ID-18",
        "paper": "JEE Main 2022 (Online) 26th June Evening Shift",
        "stem_text": "Arrange the four graphs in descending order of total work done; where W1, W2, W3 and W4 are the work done corresponding to figure a, b, c and d respectively. [FIG-stem-1] [FIG-stem-2] [FIG-stem-3] [FIG-stem-4]",
        "options": [
            "A: W3 > W2 > W1 > W4",
            "B: W3 > W2 > W4 > W1",
            "C: W2 > W3 > W4 > W1",
            "D: W2 > W3 > W1 > W4"
        ],
        "figure_reference": "[FIG-stem-1..4] 4 remote figure graphs unverified against authentic master",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "source_custody": "PARTIAL (4 remote figure placeholders unresolved)",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "WORK_FROM_FORCE_DISPLACEMENT_GRAPHS",
            "derivation": "Work done equals the area under each F(x) vs x curve. According to coaching note: Wa = 0, Wb > 0, Wc > Wb > 0, Wd < 0, giving W3 > W2 > W1 > W4. However, numerical coordinates and axis scales are unverified in absence of original figures.",
            "predicted_option": "A: W3 > W2 > W1 > W4",
            "limiting_cases": "Missing graph curves prevent independent mathematical area integration."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "COMPARE_WORK_ACROSS_GRAPHS",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Area under 4 linear segments"},
                    "physics_concepts": {"score": 1, "rationale": "Work as integral of F dx"},
                    "cognitive_depth": {"score": 1, "rationale": "Ordering 4 distinct values"},
                    "representation_load": {"score": 1, "rationale": "Interpreting 4 graphical sub-figures"},
                    "structural_complexity": {"score": 0, "rationale": "Direct parallel comparison"}
                },
                "total": 4
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (4 remote sub-figures unverified against authentic exam master)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Source verified original NTA exam paper PDF to retrieve the four figures."
    },
    {
        "sequence": 17,
        "batch_sequence": 2,
        "source_id": "EX-M61",
        "task_identity": "Q-ID-20",
        "paper": "JEE Main 2021 (Online) 27th July Evening Shift",
        "stem_text": "Given below is the plot of a potential energy function U(x) for a system, in which a particle is in one dimensional motion, while a conservative force F(x) acts on it. Suppose that Emech = 8 J, the incorrect statement for this system is : [FIG-stem-1] [ where K.E. = kinetic energy ]",
        "options": [
            "A: at x > x4 K.E. is constant throughout the region.",
            "B: at x < x1, K.E. is smallest and the particle is moving at the slowest speed.",
            "C: at x = x2, K.E. is greatest and the particle is moving at the fastest speed.",
            "D: at x = x3, K.E. = 4 J."
        ],
        "figure_reference": "[FIG-stem-1] U(x) vs x graph unverified against authentic master",
        "figure_status": "HOLD:FIGURE_UNRESOLVED",
        "source_custody": "PARTIAL (remote U(x) curve unresolved)",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "candidate_solve": {
            "method": "POTENTIAL_ENERGY_CURVE_ANALYSIS",
            "derivation": "Conservation of mechanical energy: E_mech = K(x) + U(x) = 8 J. At any point, K(x) = 8 - U(x). Coaching note asserts: at x < x1, U = 8 J => K = 0 J (particle at rest, speed is zero), contradicting Option B's assertion of 'moving at slowest speed'. Requires diagram to confirm potential plateau values at x1, x2, x3, x4.",
            "predicted_option": "B: at x < x1, K.E. is smallest and the particle is moving at the slowest speed.",
            "limiting_cases": "Without authentic U(x) plot, potential values at specific points cannot be independently checked."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "EVALUATE_POTENTIAL_ENERGY_CURVE",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Simple subtraction K = E - U"},
                    "physics_concepts": {"score": 1, "rationale": "Potential well and mechanical energy conservation"},
                    "cognitive_depth": {"score": 1, "rationale": "Identifying the false physical statement"},
                    "representation_load": {"score": 1, "rationale": "Reading potential values from graph"},
                    "structural_complexity": {"score": 1, "rationale": "Multi-region evaluation"}
                },
                "total": 5
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (potential energy graph U(x) unverified against official master)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (coaching key unverified against NTA official master)",
            "HOLD:SPEC_PENDING_D2 (no common D1/D2 teaching blueprint qualified)"
        ],
        "next_action": "Retrieve original NTA paper diagram for 27-07-2021 Evening Shift."
    },
    {
        "sequence": 18,
        "batch_sequence": 3,
        "source_id": "EX-M62",
        "task_identity": "Q-ID-21",
        "paper": "JEE Main 2021 (Online) 27th July Evening Shift",
        "stem_text": "An automobile of mass 'm' accelerates starting from origin and initially at rest, while the engine supplies constant power P. The position is given as a function of time by :",
        "options": [
            "A: ((9𝑃)/(8𝑚))^((1)/(2))𝑡^((3)/(2))",
            "B: ((8𝑃)/(9𝑚))^((1)/(2))𝑡^((2)/(3))",
            "C: ((9𝑚)/(8𝑃))^((1)/(2))𝑡^((3)/(2))",
            "D: ((8𝑃)/(9𝑚))^((1)/(2))𝑡^((3)/(2))"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained mathematical question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "CONSTANT_POWER_KINEMATIC_INTEGRATION",
            "derivation": "Power definition: P = F * v = (m * dv/dt) * v. Separating variables: P dt = m v dv. Integrating from rest (v=0 at t=0): P t = 1/2 m v^2 => v(t) = sqrt(2Pt/m) = (2P/m)^(1/2) * t^(1/2). Since v = dx/dt and starting from origin (x=0 at t=0): x(t) = integral_0^t (2P/m)^(1/2) * tau^(1/2) dtau = (2P/m)^(1/2) * (2/3) * t^(3/2) = sqrt( (4/9) * (2P/m) ) * t^(3/2) = (8P / (9m))^(1/2) * t^(3/2). This corresponds exactly to Option D.",
            "predicted_option": "D: ((8𝑃)/(9𝑚))^((1)/(2))𝑡^((3)/(2))",
            "limiting_cases": "If P=0, x=0. If m -> infinity, x -> 0. As t -> 0, x -> 0. Dimensional analysis: [P/m] = (kg m^2 s^-3) / kg = m^2 s^-3. [(P/m)^(1/2) * t^(3/2)] = (m s^(-3/2)) * s^(3/2) = m (meters). Options A, C, D have correct dimensions; option B has incorrect time exponent 2/3. Constant power requires exponent 3/2 with coefficient sqrt(8/9)."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "DERIVE_POSITION_FROM_CONSTANT_POWER",
            "difficulty_evidence": {
                "band": "D3",
                "components": {
                    "math_steps": {"score": 2, "rationale": "Two-stage differential equation integration (t -> v -> x)"},
                    "physics_concepts": {"score": 1, "rationale": "Instantaneous power P = Fv and Work-Energy Theorem"},
                    "cognitive_depth": {"score": 2, "rationale": "Algebraic derivation of time-dependent trajectory under non-constant force"},
                    "representation_load": {"score": 0, "rationale": "Pure symbolic algebraic formulation"},
                    "structural_complexity": {"score": 1, "rationale": "Coupled kinematic and dynamic variables"}
                },
                "total": 6
            },
            "demand_proposal": {"status": "PROPOSED"}
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "cell": "WPE-03-POWER-D3-CALC",
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
        "next_action": "Selected as PRIME CANDIDATE for private Core2 authoring prototype. Verify official NTA key and submit for independent blind solve."
    },
    {
        "sequence": 19,
        "batch_sequence": 4,
        "source_id": "EX-M64",
        "task_identity": "Q-ID-22",
        "paper": "JEE Main 2021 (Online) 20th July Evening Shift",
        "stem_text": "A body at rest is moved along a horizontal straight line by a machine delivering a constant power. The distance moved by the body in time 't' is proportional to :",
        "options": [
            "A: 𝑡^((3)/(2))",
            "B: 𝑡^((1)/(2))",
            "C: 𝑡^((1)/(4))",
            "D: 𝑡^((3)/(4))"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained scaling relation question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "CONSTANT_POWER_SCALING_RELATION",
            "derivation": "By Work-Energy Theorem: Total work done W = P * t. Assuming initial rest: 1/2 m v^2 = P * t => v^2 proportional to t => v proportional to t^(1/2). Distance x = integral v dt proportional to integral t^(1/2) dt proportional to t^(3/2). Matches Option A.",
            "predicted_option": "A: 𝑡^((3)/(2))",
            "limiting_cases": "If constant force F acted, v proportional to t and x proportional to t^2. Under constant power P, force F = P/v decreases as speed increases, so distance grows as t^(3/2) (between linear and quadratic)."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "ANALYZE_POWER_SCALING",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Single proportional integration"},
                    "physics_concepts": {"score": 1, "rationale": "Work done under constant power W = Pt"},
                    "cognitive_depth": {"score": 1, "rationale": "Proportional scaling deduction"},
                    "representation_load": {"score": 0, "rationale": "Pure text description"},
                    "structural_complexity": {"score": 1, "rationale": "Power to kinematics mapping"}
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
        "sequence": 20,
        "batch_sequence": 5,
        "source_id": "EX-M65",
        "task_identity": "Q-ID-23",
        "paper": "JEE Main 2021 (Online) 18th March Morning Shift",
        "stem_text": "A constant power delivering machine has towed a box, which was initially at rest, along a horizontal straight line. The distance moved by the box in time 't' is proportional to :-",
        "options": [
            "A: t2/3",
            "B: t3/2",
            "C: t",
            "D: t1/2"
        ],
        "figure_reference": "NONE (pure text question)",
        "figure_status": "NOT_REQUIRED",
        "source_custody": "VERIFIED_TEXT_ONLY (Self-contained scaling relation question)",
        "solve_status": "CANDIDATE_DERIVED",
        "candidate_solve": {
            "method": "CONSTANT_POWER_SCALING_RELATION",
            "derivation": "Constant power P = m v (dv/dt). Integrating from rest: P t = 1/2 m v^2 => v proportional to t^(1/2). Distance x = integral v dt proportional to t^(3/2). Matches Option B (t3/2).",
            "predicted_option": "B: t3/2",
            "limiting_cases": "Consistent with EX-M64 and EX-M62. Demonstrates robust cross-sitting invariance of the constant-power scaling law x ~ t^(3/2)."
        },
        "sl2": {
            "mode": "QUESTION",
            "decisive_operation": "ANALYZE_POWER_SCALING",
            "difficulty_evidence": {
                "band": "D2",
                "components": {
                    "math_steps": {"score": 1, "rationale": "Single proportional integration"},
                    "physics_concepts": {"score": 1, "rationale": "Work done under constant power W = Pt"},
                    "cognitive_depth": {"score": 1, "rationale": "Proportional scaling deduction"},
                    "representation_load": {"score": 0, "rationale": "Pure text description"},
                    "structural_complexity": {"score": 1, "rationale": "Power to kinematics mapping"}
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
    }
]

# Generate QUESTION_AUDIT.json and SOURCE_ONLY.json for each item
for item in lot05_data:
    seq = item["sequence"]
    sid = item["source_id"]
    
    # Audit record
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
        "lot": "LOT-05",
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

print("Generated 5 question audits and 5 sealed source-only packets for LOT-05.")

# Generate review/index.html
review_dir = os.path.join(LOT_DIR, "review")
os.makedirs(review_dir, exist_ok=True)

rows_html = []
for item in lot05_data:
    bp_disp = item["blueprint_fit"]
    if isinstance(bp_disp, dict):
        bp_cell = f"<strong>{bp_disp['blueprint_id']}</strong><br><small>{bp_disp['cell']}</small>"
    else:
        bp_cell = f"<span class='badge badge-hold'>{bp_disp}</span>"

    proto_badge = ""
    if item["source_id"] == "EX-M62":
        proto_badge = "<div class='proto-badge'>SELECTED FOR CORE2 PROTOTYPE</div>"

    rows_html.append(f"""
    <tr>
        <td class="col-seq"><strong>#{item['sequence']}</strong><br><small class="mono">{item['task_identity']}</small><br><small>Batch Seq: #{item['batch_sequence']}</small></td>
        <td class="col-source">
            <strong>{item['source_id']}</strong><br>
            <small class="text-muted">{item['paper']}</small><br>
            <span class="badge badge-source">{item['source_custody']}</span>
            <span class="badge badge-fig">{item['figure_status']}</span>
            {proto_badge}
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
    <title>Grade9 v4.0 — LOT-05 Source & Candidate Solve Audit (Questions 16–20)</title>
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

        .proto-badge {{
            background: #dbeafe;
            color: #1e40af;
            border: 1px solid #93c5fd;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 6px;
            border-radius: 4px;
            margin-top: 4px;
            display: inline-block;
        }}

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
            <h1>Grade9 v4.0 — LOT-05 Source & Candidate Solve Audit (Questions 16–20)</h1>
            <div class="header-meta">
                <span><strong>Batch:</strong> BATCH-B (CP-1)</span>
                <span><strong>Lot:</strong> LOT-05 (Roster Positions 1–5)</span>
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

print(f"Generated LOT-05 review dashboard: {html_path}")
