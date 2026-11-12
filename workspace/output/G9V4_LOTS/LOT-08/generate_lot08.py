"""
Grade9 v4.0 — Lot 08 Generator (Questions 31–35)
Batch C, CP-1
Generates:
  - questions/31..35/QUESTION_AUDIT.json
  - source_only/31..35/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-08")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-08"}

# Lot 08 Physics & Calibration Data
LOT08_SPECS = {
    "EX-M89": {
        "sequence": 31,
        "batch_sequence": 1,
        "method": "CENTRAL_FORCE_ENERGY_INTEGRATION",
        "predicted_option": "D: (5)/(6) 𝛼 r3",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Connecting centripetal dynamic force balance to kinetic energy and integrating radial force for potential energy"},
                    "representation_translation": {"score": 1, "evidence": "Translating central force law statement into definite radial integral with U(0)=0 datum"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Two-stage derivation: circular orbit speed -> KE = (1/2)alpha*r^3, radial integral -> PE = (1/3)alpha*r^3, then summing"},
                    "algebra_computational_load": {"score": 1, "evidence": "Fractional addition 1/2 + 1/3 = 5/6"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Distinguishing between inverse square gravity vs r^2 central power law"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "rationale": "Constructing dynamic central force model and energy integral under non-standard power law",
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
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Central force F = alpha*r^2 = m*v^2 / r => m*v^2 = alpha*r^3 => KE = (1/2)*alpha*r^3. Potential energy: dU = -F_radial dr = alpha*r^2 dr => U(r) = int_0^r alpha*r'^2 dr' = (1/3)*alpha*r^3. Total mechanical energy E = KE + U = (1/2)*alpha*r^3 + (1/3)*alpha*r^3 = (5/6)*alpha*r^3."
    },
    "EX-M90": {
        "sequence": 32,
        "batch_sequence": 2,
        "method": "SPRING_ENERGY_ELASTIC_COLLISION",
        "predicted_option": "B: 0.6 J",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Conservation of mechanical energy for spring-mass system combined with elastic collision velocity transfer"},
                    "representation_translation": {"score": 1, "evidence": "Translating position x/2 into 1/4 fraction of initial elastic potential energy"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Two-step reasoning: evaluate kinetic energy from post-collision speed (0.45 J), then scale by 4/3 factor"},
                    "algebra_computational_load": {"score": 1, "evidence": "Arithmetic multiplication: E0 = (4/3) * 0.45 = 0.6 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing that approaching half distance leaves 1/4 (not 1/2) energy in the spring"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Standard application of spring potential energy and head-on elastic collision kinetic transfer",
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
        "derivation": "At collision x/2, mass 0.1 kg stops and identical mass moves with 3 m/s => KE = (1/2)*m*v^2 = 0.5 * 0.1 * 9 = 0.45 J. Potential energy remaining in spring at x/2 is U(x/2) = (1/2)*k*(x/2)^2 = (1/4)*E_total. Energy conserved: E_total - (1/4)*E_total = KE => (3/4)*E_total = 0.45 J => E_total = 0.45 * (4/3) = 0.6 J."
    },
    "EX-M92": {
        "sequence": 33,
        "batch_sequence": 3,
        "method": "CONTINUOUS_SPRING_MASS_INTEGRATION",
        "predicted_option": "D: (1)/(6) m 𝑣 2",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Continuous mass integration under linear affine velocity profile v(y) = v*(y/l)"},
                    "representation_translation": {"score": 1, "evidence": "Setting up 1D continuum integral for kinetic energy over spring length"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Formulate differential mass element dm = (m/l)dy, express local speed, evaluate polynomial integral"},
                    "algebra_computational_load": {"score": 1, "evidence": "Definite integration of y^2 yielding l^3/3 and resulting 1/6 prefactor"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Avoiding trap of treating spring as point mass (1/2 mv^2) or average speed (1/8 mv^2)"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying continuum kinetic energy integration to distributed mass spring",
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
        "derivation": "Element at distance y from fixed end has speed v(y) = v*(y/l). Element mass dm = (m/l)dy. Total kinetic energy KE = int_0^l (1/2)*dm*(v(y))^2 = (1/2)*(m/l)*(v^2/l^2) * int_0^l y^2 dy = (1/2)*(m*v^2 / l^3) * (l^3 / 3) = (1/6)*m*v^2."
    },
    "EX-M96": {
        "sequence": 34,
        "batch_sequence": 4,
        "method": "FLUID_POWER_VELOCITY_SCALING",
        "predicted_option": "D: 𝑣^(3)",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Mass flow rate scaling dm/dt proportional to v, kinetic energy proportional to v^2"},
                    "representation_translation": {"score": 1, "evidence": "Combining mass flux and kinetic energy into power rate equation"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Single proportionality chain dm/dt ~ v => P ~ (dm/dt)*v^2 ~ v^3"},
                    "algebra_computational_load": {"score": 0, "evidence": "Direct exponent addition: 1 + 2 = 3"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Avoiding quadratic distractor v^2 (which assumes constant mass rather than fluid flux)"}
                },
                "total": 4,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/0/1", "total": 4},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying mass-flux kinetic energy scaling to windmill power generation",
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
        "derivation": "Mass of air intercepted per second: dm/dt = rho * A * v. Kinetic energy per unit time of this intercepted air: P_wind = (1/2)*(dm/dt)*v^2 = (1/2)*rho*A*v^3. Since electrical power output is a fixed fraction of wind power, P_elec proportional to v^3."
    },
    "EX-M97": {
        "sequence": 35,
        "batch_sequence": 5,
        "method": "VERTICAL_LEAP_DYNAMICS_AND_POWER",
        "predicted_option": "B: 6.26×10^(3) Watts at take off",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Connecting crouching vertical acceleration phase to ballistic free flight rise and power definition"},
                    "representation_translation": {"score": 1, "evidence": "Separating crouching push phase (0.5 m) from airborne rise (1.0 m)"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Find takeoff velocity from ballistic rise, compute accelerating force during push, evaluate P = F*v at takeoff"},
                    "algebra_computational_load": {"score": 1, "evidence": "Square root and multiplication: 1400 * sqrt(20) = 6261 W"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Noting coaching key dispute between net accelerating force F_net = 1400 N vs ground normal force N = 2100 N"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Application of kinematics and instantaneous mechanical power to vertical biomechanical jump",
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
            "HOLD:KEY_DISPUTE (Coaching key evaluates net accelerating force F_net=1400N rather than ground contact force F_ground=2100N)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Free flight rise h = 1.0 m => v_takeoff = sqrt(2*g*h) = sqrt(2 * 10 * 1) = sqrt(20) = 4.472 m/s. During crouching push s = 0.5 m from rest: v^2 = 2*a*s => 20 = 2*a*0.5 => a = 20 m/s^2. Net accelerating force F_net = m*a = 70 * 20 = 1400 N. Instantaneous power delivered to acceleration at takeoff: P = F_net * v_takeoff = 1400 * 4.472 = 6261 W = 6.26 * 10^3 W at takeoff."
    }
}

# Generate directories
(LOT_DIR / "questions").mkdir(exist_ok=True)
(LOT_DIR / "source_only").mkdir(exist_ok=True)
(LOT_DIR / "review").mkdir(exist_ok=True)

generated_audits = []
generated_source_only = []

for sid, spec in LOT08_SPECS.items():
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

    # 1. Full Audit Record
    audit_rec = {
        "sequence": seq,
        "batch_sequence": spec["batch_sequence"],
        "task_identity": ros["task_identity"],
        "stable_id": f"PHYS-WPE-LOT08-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-08",
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

    # 2. Sealed Source-Only Record (zero solves, keys, or scores)
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
    generated_source_only.append(source_only_rec)

    print(f"Generated Q{seq:02d} ({sid}): Audit & Source-Only sealed.")

# 3. Generate review/index.html
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
            <span class="badge badge-lot">LOT-08</span><br>
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
    <title>Grade9 v4.0 — Lot 08 Private Review Dashboard (Questions 31–35)</title>
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
            <h1>Grade9 v4.0 — Lot 08 Candidate Review (Batch C, Questions 31–35)</h1>
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
