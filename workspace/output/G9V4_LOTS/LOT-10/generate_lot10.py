"""
Grade9 v4.0 — Lot 10 Generator (Questions 41–45)
Batch C, CP-3
Generates:
  - questions/41..45/QUESTION_AUDIT.json
  - source_only/41..45/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-10")
ROOT = Path("D:/CodeD/grade9v4")

REGISTRY_PATH = ROOT / "workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data/registry.json"
LEDGER_PATH = ROOT / "workspace/output/G9V4_LOTS/LOT-00/source-index-private.json"
ROSTER_PATH = LOT_DIR / "ROSTER_PRIVATE.json"

with open(REGISTRY_PATH, encoding="utf-8") as f:
    registry = json.load(f)
reg_by_id = {r["id"]: r for r in registry["records"]}

with open(LEDGER_PATH, encoding="utf-8") as f:
    ledger = json.load(f)
ledger_by_id = {r["id"]: r for r in ledger["records"]}

with open(ROSTER_PATH, encoding="utf-8") as f:
    roster_data = json.load(f)
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-10"}

LOT10_SPECS = {
    "EX-M111": {
        "sequence": 41,
        "batch_sequence": 11,
        "method": "WORK_ENERGY_PARTITIONED_INCLINE",
        "predicted_option": "D: 2tan𝜙",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Work-energy theorem over partitioned smooth and rough incline segments"},
                    "representation_translation": {"score": 1, "evidence": "Relating gravitational potential loss to normal friction dissipation"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Equating gravitational work over full length L to friction work over lower half L/2"},
                    "algebra_computational_load": {"score": 0, "evidence": "Simple trigonometric quotient sin(phi)/cos(phi) = tan(phi)"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Factoring half length L/2 for friction vs full length L for gravity"}
                },
                "total": 4,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/0/1", "total": 4},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying work-energy balance across segmented incline with variable friction",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Body starts and ends at rest => Net work W_net = 0. Work by gravity: W_g = m*g*L*sin(phi). Work by friction over lower half: W_f = -mu * m*g*cos(phi) * (L/2). Equating: m*g*L*sin(phi) = mu * m*g*cos(phi) * (L/2) => sin(phi) = (mu/2)*cos(phi) => mu = 2*tan(phi)."
    },
    "EX-M120": {
        "sequence": 42,
        "batch_sequence": 12,
        "method": "CONSTANT_POWER_DISTANCE_SCALING",
        "predicted_option": "B: 𝑡^(3/2)",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Constant power kinematic scaling: Pt = (1/2)mv^2 => v ~ t^(1/2)"},
                    "representation_translation": {"score": 1, "evidence": "Integrating proportional speed with respect to time to find distance scaling"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Two-step proportionality: power -> speed -> distance"},
                    "algebra_computational_load": {"score": 0, "evidence": "Power law integration: 1/2 + 1 = 3/2"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Distinguishing constant power displacement (t^(3/2)) from constant acceleration (t^2)"}
                },
                "total": 4,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/0/1", "total": 4},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["RETRIEVE"],
                "rationale": "Applying work-energy power scaling to 1D straight-line kinematics",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Constant power P delivered: W = P*t = (1/2)*m*v^2 => v = sqrt(2*P*t/m) proportional to t^(1/2). Distance x = int v dt proportional to int t^(1/2) dt proportional to t^(3/2)."
    },
    "EX-N8": {
        "sequence": 43,
        "batch_sequence": 13,
        "method": "INCLINE_DYNAMICS_AND_INSTANTANEOUS_POWER",
        "predicted_option": "300",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Newton's second law on incline to find pulling force, then instantaneous power P = F*v"},
                    "representation_translation": {"score": 1, "evidence": "Resolving gravity along 30 degree incline and kinematics v = a*t"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Find pulling force F = 30 N, speed at t=10s v = 10 m/s, evaluate power product"},
                    "algebra_computational_load": {"score": 1, "evidence": "Arithmetic multiplication: 30 * 10 = 300 W"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Not confusing effective acceleration with pulling force alone"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying dynamics and kinematics to calculate instantaneous power delivery",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Incline angle 30 deg, acceleration a = 1 m/s^2. Equation of motion along incline: F_pull - m*g*sin(30) = m*a => F_pull = 5*10*0.5 + 5*1 = 25 + 5 = 30 N. At t = 10s: velocity v = a*t = 1 * 10 = 10 m/s. Instantaneous power P = F_pull * v = 30 * 10 = 300 W."
    },
    "EX-N11": {
        "sequence": 44,
        "batch_sequence": 14,
        "method": "WORK_ENERGY_CIRCULAR_TUBE_FRICTION",
        "predicted_option": "-245",
        "solve_status": "HOLD:FIGURE_UNRESOLVED",
        "source_custody": "PARTIAL (Remote figure [FIG-stem-1] unresolved)",
        "figure_status": "REQUIRED_UNRESOLVED",
        "figure_reference": "[FIG-stem-1]",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Work-energy theorem on vertical circular constraint with friction dissipation"},
                    "representation_translation": {"score": 1, "evidence": "Translating vertical displacement between top and bottom of circle (2R)"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Evaluate Delta KE, gravity work, and deduce constraint work"},
                    "algebra_computational_load": {"score": 1, "evidence": "Squaring 22^2 = 484 and subtraction: -242 - 3 = -245"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Tracking negative sign of dissipative friction work and unresolved figure geometry"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["REPRESENT"],
                "rationale": "Application of work-energy theorem to dissipative circular tube motion",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:FIGURE_UNRESOLVED (Remote figure [FIG-stem-1] missing from local custody)",
            "HOLD:SIGNED_WORK_VS_KEY_DISPUTE (Sign convention dispute between friction work -245J vs magnitude)",
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Initial speed v0 = 22 m/s at top. Comes to rest at bottom region. Delta KE = 0 - (1/2)*m*v0^2 = -0.5 * 1 * 484 = -242 J. Work by gravity: drop h = 2*R = 2*0.15 = 0.3 m => W_g = m*g*h = 1 * 10 * 0.3 = 3 J. Work-energy theorem: W_net = W_g + W_tube = Delta KE => 3 + W_tube = -242 => W_tube = -245 J. Held on figure custody."
    },
    "EX-N19": {
        "sequence": 45,
        "batch_sequence": 15,
        "method": "CONSTANT_POWER_DISPLACEMENT_INTEGRATION",
        "predicted_option": "4",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Connecting constant power to differential kinematics: (1/2)mv^2 = Pt => v = sqrt(2Pt/m)"},
                    "representation_translation": {"score": 1, "evidence": "Integrating v(t) = sqrt(P)*t^(1/2) with respect to time to obtain displacement formula"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Integrate to find x(t), evaluate at t=4s, equate to target expression (1/3)alpha^2 sqrt(P) to extract alpha"},
                    "algebra_computational_load": {"score": 1, "evidence": "Evaluating fractional exponent 4^(3/2) = 8 and solving alpha^2 = 16 => alpha = 4"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Matching target expression prefactors carefully"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying calculus integration to constant power velocity function",
                "candidate_cell": "QRT-APPLY-D3",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "version": "0.2.0",
            "sha256": "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9",
            "blueprint_cell_ref": "D3.3",
            "topic_tag": "WPE-03-POWER",
            "status": "PINNED_CELL_UNQUALIFIED"
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "sha256": "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b",
            "status": "CELL_UNQUALIFIED_ADAPTER_GAP",
            "note": "WPE adapter defines cell D3.1 only. Target cell D3.3 requires adapter cell expansion; flagged as SPEC_GAP."
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Mass m = 2 kg. (1/2)*m*v^2 = P*t => (1/2)*(2)*v^2 = P*t => v = sqrt(P)*t^(1/2). Displacement x(t) = int_0^t sqrt(P)*t'^(1/2) dt' = (2/3)*sqrt(P)*t^(3/2). At t = 4s: t^(3/2) = 4^(3/2) = 8 => x(4) = (2/3)*sqrt(P)*8 = (16/3)*sqrt(P) = (1/3)*(16)*sqrt(P). Comparing with (1/3)*alpha^2*sqrt(P): alpha^2 = 16 => alpha = 4."
    }
}

(LOT_DIR / "questions").mkdir(exist_ok=True)
(LOT_DIR / "source_only").mkdir(exist_ok=True)
(LOT_DIR / "review").mkdir(exist_ok=True)

generated_audits = []

for sid, spec in LOT10_SPECS.items():
    seq = spec["sequence"]
    reg = reg_by_id[sid]
    led = ledger_by_id[sid]
    ros = roster_items[sid]

    stem_text = reg["stem"]
    stem_sha = hashlib.sha256(stem_text.encode("utf-8")).hexdigest()
    assert stem_sha == led["stem_sha256"], f"Stem SHA mismatch for {sid}"

    options = reg.get("options", [])

    q_dir = LOT_DIR / "questions" / f"{seq:02d}"
    s_dir = LOT_DIR / "source_only" / f"{seq:02d}"
    q_dir.mkdir(parents=True, exist_ok=True)
    s_dir.mkdir(parents=True, exist_ok=True)

    audit_rec = {
        "sequence": seq,
        "batch_sequence": spec["batch_sequence"],
        "task_identity": ros["task_identity"],
        "stable_id": f"PHYS-WPE-LOT10-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-10",
        "batch": "BATCH-C",
        "paper": ros["paper"],
        "source_type": "EXAM_PAPER_TRANSCRIBED",
        "source_custody": spec["source_custody"],
        "stem_text": stem_text,
        "stem_sha256": stem_sha,
        "source_hash": stem_sha,
        "source_record_digest": f"sha256:{stem_sha}",
        "duplicate_parent": None,
        "scope": "PRIMARY_IN_SCOPE_WPE",
        "key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "figure_status": spec["figure_status"],
        "figure_reference": spec["figure_reference"],
        "options": options,
        "solve_exposure": "EXPOSED",
        "solve_status": spec["solve_status"],
        "candidate_solve": {
            "method": spec["method"],
            "predicted_option": spec["predicted_option"],
            "derivation": spec["derivation"]
        },
        "sl2": spec["sl2"],
        "blueprint_fit": spec["blueprint_fit"],
        "adapter_fit": spec["adapter_fit"],
        "core2_status": "NOT_RUN",
        "owner_admission": "PENDING_INDEPENDENT_REVIEW",
        "b2_blind_status": "PENDING_BLIND_SOLVE",
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION",
        "blockers": spec["blockers"],
        "next_action": "B2 independent source-only solve + official NTA master key reconciliation"
    }

    # Add shared teaching construction family for EX-M120 and EX-N19
    if sid in ["EX-M120", "EX-N19"]:
        audit_rec["teaching_construction_family"] = {
            "construction_id": "TC-WPE-CONST-POWER-TRAJECTORY-01",
            "shared_candidates": ["EX-M62", "EX-M64", "EX-M65", "EX-M120", "EX-N19"],
            "note": "Shares the ideal constant-power kinematic trajectory construction family with EX-M62, EX-M64, EX-M65."
        }

    q_file = q_dir / "QUESTION_AUDIT.json"
    with open(q_file, "w", encoding="utf-8") as f:
        json.dump(audit_rec, f, indent=2, ensure_ascii=False)
    generated_audits.append(audit_rec)

    source_only_rec = {
        "source_id": sid,
        "task_identity": ros["task_identity"],
        "sequence": seq,
        "batch_sequence": spec["batch_sequence"],
        "paper": ros["paper"],
        "stem_text": stem_text,
        "stem_sha256": stem_sha,
        "options": options,
        "figure_reference": spec["figure_reference"],
        "confidentiality_notice": "Source custody blind packet. Academic solve, answer key, and scoring omitted. Private review only."
    }

    s_file = s_dir / "SOURCE_ONLY.json"
    with open(s_file, "w", encoding="utf-8") as f:
        json.dump(source_only_rec, f, indent=2, ensure_ascii=False)

    print(f"Generated Q{seq:02d} ({sid}): Audit & Source-Only sealed.")

# Generate review/index.html
rows_html = []
for q in generated_audits:
    bp_disp = q["blueprint_fit"]
    if isinstance(bp_disp, dict):
        bp_cell = f"<strong>{bp_disp['blueprint_id']}</strong><br><small>{bp_disp['blueprint_cell_ref']} ({bp_disp['topic_tag']})</small>"
    else:
        bp_cell = f"<span class='badge badge-hold'>{bp_disp}</span>"

    rows_html.append(f"""
    <tr>
        <td class="col-seq">
            <strong>#{q['sequence']}</strong><br>
            <span class="badge badge-lot">LOT-10</span><br>
            <small class="mono">{q['task_identity']}</small><br>
            <small>Batch #{q['batch_sequence']}</small>
        </td>
        <td class="col-source">
            <strong>{q['source_id']}</strong><br>
            <small class="text-muted">{q['paper']}</small><br>
            <span class="badge badge-source">{q['source_custody']}</span>
            <span class="badge badge-fig">{q['figure_status']}</span>
        </td>
        <td class="col-stem">
            <div class="stem-preview">{q['stem_text'][:140]}...</div>
            <div class="solve-summary">
                <strong>Method:</strong> <code>{q['candidate_solve']['method']}</code><br>
                <strong>Predicted Option:</strong> {q['candidate_solve']['predicted_option']}
            </div>
        </td>
        <td class="col-cog">
            <strong>{q['sl2']['demand_proposal']['primary']}</strong> ({q['sl2']['difficulty_evidence']['band']})<br>
            <small>Score: {q['sl2']['difficulty_evidence']['total']}/10</small><br>
            <span class="badge badge-prop">{q['sl2']['demand_proposal']['status']}</span>
        </td>
        <td class="col-bp">{bp_cell}</td>
        <td class="col-gates">
            <span class="badge badge-admission">{q['academic_admission']}</span>
            <ul class="blocker-list">
                {"".join(f"<li>{b}</li>" for b in q['blockers'])}
            </ul>
        </td>
    </tr>
    """)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade9 v4.0 — Lot 10 Private Review Dashboard (Questions 41–45)</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --surface: #ffffff;
            --border: #e2e8f0;
            --text: #0f172a;
            --text-muted: #64748b;
            --primary: #2563eb;
            --warning: #d97706;
            --warning-bg: #fffbeb;
            --danger: #b91c1c;
            --danger-bg: #fef2f2;
            --info: #0891b2;
            --info-bg: #ecfeff;
            --badge-bg: #f1f5f9;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.5;
            padding: 16px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}

        h1 {{ font-size: 20px; font-weight: 700; margin-bottom: 6px; }}
        .header-meta {{ font-size: 13px; color: var(--text-muted); }}

        .table-wrap {{
            overflow-x: auto;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}

        th {{
            background: #f1f5f9;
            padding: 10px 12px;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }}

        .col-seq {{ width: 100px; }}
        .col-source {{ width: 180px; }}
        .col-stem {{ width: 340px; }}
        .col-cog {{ width: 140px; }}
        .col-bp {{ width: 180px; }}
        .col-gates {{ width: 260px; }}

        .badge {{
            display: inline-block;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: 600;
            border-radius: 4px;
            margin-top: 4px;
        }}

        .badge-lot {{ background: #e0e7ff; color: #3730a3; }}
        .badge-source {{ background: #dcfce7; color: #166534; }}
        .badge-fig {{ background: #fef9c3; color: #854d0e; }}
        .badge-prop {{ background: #f3e8ff; color: #6b21a8; }}
        .badge-hold {{ background: var(--warning-bg); color: var(--warning); border: 1px solid #fde68a; }}
        .badge-admission {{ background: var(--danger-bg); color: var(--danger); font-weight: 700; }}

        .stem-preview {{
            font-size: 12px;
            color: #334155;
            margin-bottom: 6px;
        }}

        .solve-summary {{
            font-size: 11px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 6px;
            border-radius: 4px;
        }}

        .blocker-list {{
            list-style: disc;
            padding-left: 16px;
            font-size: 11px;
            color: var(--danger);
        }}

        footer {{
            margin-top: 24px;
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Grade9 v4.0 — Lot 10 Candidate Review (Batch C, Questions 41–45)</h1>
            <div class="header-meta">
                Status: <strong>PROCEEDING_CANDIDATE_TRIAGE_ONLY</strong> | Admissions: <strong>0/5 ADMITTED</strong> | PR Status: <strong>HOLD_BASE_NOT_READY</strong><br>
                Governance Rule: Fail-closed on missing official keys and unverified figures. Zero public leakages.
            </div>
        </header>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Sequence</th>
                        <th>Source Identity</th>
                        <th>Transcribed Stem & Solve Model</th>
                        <th>Cognitive (SL2)</th>
                        <th>Blueprint Fit</th>
                        <th>Admission & Blockers</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows_html)}
                </tbody>
            </table>
        </div>

        <footer>
            <div>Grade9 v4.0 Local Workspace | Physics WPE Topic Adapter (Pilot)</div>
            <div>No academic approval inferred from software validation.</div>
        </footer>
    </div>
</body>
</html>
"""

review_html_path = LOT_DIR / "review" / "index.html"
with open(review_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\nCreated Review Dashboard: {review_html_path}")
