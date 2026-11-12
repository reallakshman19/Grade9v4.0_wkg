"""
Grade9 v4.0 — Lot 09 Generator (Questions 36–40)
Batch C, CP-2
Generates:
  - questions/36..40/QUESTION_AUDIT.json
  - source_only/36..40/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-09")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-09"}

LOT09_SPECS = {
    "EX-M98": {
        "sequence": 36,
        "batch_sequence": 6,
        "method": "SERIES_SPRINGS_FORCE_EQUALITY",
        "predicted_option": "A: (4)/(3)",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Series spring coupling: identical restoring force F transmitted across both springs"},
                    "representation_translation": {"score": 1, "evidence": "Formulating stored energy as E = F^2 / (2k) instead of displacement"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Evaluating inverse ratio of spring constants EA/EB = kB/kA"},
                    "algebra_computational_load": {"score": 0, "evidence": "Direct fraction reduction 400/300 = 4/3"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Avoiding trap of assuming equal compression (which would give 3/4)"}
                },
                "total": 4,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/0/1", "total": 4},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["RETRIEVE"],
                "rationale": "Applying series spring force transmission law to energy ratio",
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
        "derivation": "In series, compression force F is identical for both springs. Stored energy E = F^2 / (2k). Ratio E_A / E_B = (F^2 / (2*kA)) / (F^2 / (2*kB)) = kB / kA = 400 / 300 = 4/3."
    },
    "EX-M101": {
        "sequence": 37,
        "batch_sequence": 7,
        "method": "WORK_INEQUALITY_COMPARISON",
        "predicted_option": "A: Statement 1 is false, Statement 2 is true",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Contrasting constant-force vs constant-displacement spring energy regimes"},
                    "representation_translation": {"score": 1, "evidence": "Translating verbal statements into mathematical inequalities"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Deduce k1 < k2 from constant force condition, then evaluate constant displacement condition"},
                    "algebra_computational_load": {"score": 0, "evidence": "Qualitative inequality comparison"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Inversion of inequality when moving from F^2/(2k) to (1/2)kx^2"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/2/0/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["APPLY"],
                "rationale": "Evaluating logical validity and explanation relationship of dual physics statements",
                "candidate_cell": "QRT-JUSTIFY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:JUSTIFY_REQUIRES_ADJUDICATION (QRT review required for Statement 1/2 justification rubric)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Same force F: W = F^2/(2k). W1 > W2 => F^2/(2k1) > F^2/(2k2) => k1 < k2. Statement 2 is TRUE. Same extension x: W = (1/2)kx^2. Since k1 < k2, W1 < W2. Statement 1 claims W1 > W2, which is FALSE. Therefore Statement 1 is false, Statement 2 is true."
    },
    "EX-M105": {
        "sequence": 38,
        "batch_sequence": 8,
        "method": "WORK_ENERGY_SPRING_WITH_FRICTION",
        "predicted_option": "B: 5.5𝑐𝑚",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Work-energy theorem combining dissipative friction work and spring elastic potential energy"},
                    "representation_translation": {"score": 1, "evidence": "Formulating quadratic energy balance: KE_initial = f_k * x + (1/2) * k * x^2"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Set up energy equation and solve quadratic for physical compression distance"},
                    "algebra_computational_load": {"score": 1, "evidence": "Solving quadratic equation with large spring constant 10000 N/m"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Not neglecting friction work over spring compression distance x"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying work-energy balance to combined spring-friction system",
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
        "derivation": "Initial KE = (1/2)*m*v^2 = 0.5 * 2 * 16 = 16 J. Energy balance: 16 = f_k * x + (1/2)*k*x^2 = 15*x + 5000*x^2 => 5000*x^2 + 15*x - 16 = 0. Using quadratic formula: x = (-15 + sqrt(225 + 320000)) / 10000 = (-15 + 565.88) / 10000 = 0.05509 m = 5.5 cm."
    },
    "EX-M106": {
        "sequence": 39,
        "batch_sequence": 9,
        "method": "CONSTANT_HORIZONTAL_FORCE_PENDULUM",
        "predicted_option": "D: 𝑀𝑔(√(2)−1)",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Work-energy theorem for constant force displacement vs quasi-static equilibrium"},
                    "representation_translation": {"score": 1, "evidence": "Geometry of pendulum displacement: horizontal = L*sin(45), vertical = L*(1-cos(45))"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Equating work done by constant horizontal force to gravitational potential gain at momentary rest"},
                    "algebra_computational_load": {"score": 1, "evidence": "Radical factoring: (sqrt(2)-1)/sqrt(2) * sqrt(2) = sqrt(2)-1"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing essential model ambiguity between constant force vs quasi-static force"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "rationale": "Formulating work-energy model for constant horizontal force pulling pendulum to momentary rest",
                "candidate_cell": "QRT-MODEL-D3",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "version": "0.2.0",
            "sha256": "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9",
            "blueprint_cell_ref": "D3.4",
            "topic_tag": "WPE-02-POTENTIAL",
            "status": "PINNED_CELL_UNQUALIFIED"
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "sha256": "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b",
            "status": "CELL_UNQUALIFIED_ADAPTER_GAP",
            "note": "WPE adapter defines cell D3.1 only. Target cell D3.4 requires adapter cell expansion; flagged as SPEC_GAP."
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Coaching key unverified against official NTA master)",
            "HOLD:MODEL_AMBIGUITY (Constant force work-energy gives Mg(sqrt(2)-1) whereas quasi-static equilibrium gives Mg)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Horizontal displacement of mass: delta_x = L*sin(45) = L/sqrt(2). Vertical rise: delta_y = L*(1 - cos(45)) = L*(1 - 1/sqrt(2)). By work-energy theorem, W_net = W_F - Delta U = 0 (comes to rest at 45 deg) => F * (L/sqrt(2)) = M*g*L*(1 - 1/sqrt(2)) = M*g*L*((sqrt(2)-1)/sqrt(2)). Multiplying by sqrt(2)/L: F = M*g*(sqrt(2) - 1)."
    },
    "EX-M109": {
        "sequence": 40,
        "batch_sequence": 10,
        "method": "POTENTIAL_ENERGY_MINIMA_AND_MAX_SPEED",
        "predicted_option": "A: (3)/(√(2))",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Connecting maximum kinetic energy to potential energy minima via mechanical energy conservation"},
                    "representation_translation": {"score": 1, "evidence": "Finding potential energy minimum using calculus first and second derivatives"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Differentiate V(x) to locate minima at x=+-1, evaluate V_min=-1/4 J, subtract from total energy E=2 J to get KE_max=9/4 J, and solve for speed"},
                    "algebra_computational_load": {"score": 1, "evidence": "Negative sign subtraction: 2 - (-1/4) = 9/4 J, and radical reduction: sqrt(9/2) = 3/sqrt(2)"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Avoiding false minimum at x=0 (which is an unstable local maximum with V=0)"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying calculus extrema to 1D potential energy well and conservation of energy",
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
            "topic_tag": "WPE-02-POTENTIAL",
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
        "derivation": "Potential energy V(x) = x^4/4 - x^2/2. Critical points: dV/dx = x^3 - x = x(x^2 - 1) = 0 => x = 0, +-1. At x = +-1: V''(+-1) = 3(1) - 1 = 2 > 0 (minima). Minimum potential energy: V_min = 1/4 - 1/2 = -1/4 J = -0.25 J. Conservation of energy: E = KE_max + V_min => 2 = KE_max - 0.25 => KE_max = 2.25 J = 9/4 J. Speed: (1/2)*m*v_max^2 = 9/4 => (1/2)*(1)*v_max^2 = 9/4 => v_max^2 = 9/2 => v_max = 3 / sqrt(2) m/s."
    }
}

(LOT_DIR / "questions").mkdir(exist_ok=True)
(LOT_DIR / "source_only").mkdir(exist_ok=True)
(LOT_DIR / "review").mkdir(exist_ok=True)

generated_audits = []

for sid, spec in LOT09_SPECS.items():
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
        "stable_id": f"PHYS-WPE-LOT09-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-09",
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
            <span class="badge badge-lot">LOT-09</span><br>
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
    <title>Grade9 v4.0 — Lot 09 Private Review Dashboard (Questions 36–40)</title>
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
            <h1>Grade9 v4.0 — Lot 09 Candidate Review (Batch C, Questions 36–40)</h1>
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
