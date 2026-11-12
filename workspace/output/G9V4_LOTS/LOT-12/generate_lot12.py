"""
Grade9 v4.0 — Lot 12 Generator (Questions 51–55)
Batch D, CP-2
Generates:
  - questions/51..55/QUESTION_AUDIT.json
  - source_only/51..55/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-12")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-12"}

# Lot 12 Physics & Calibration Data
LOT12_SPECS = {
    "EX-N38": {
        "sequence": 51,
        "batch_sequence": 6,
        "method": "CONSTANT_POWER_DISPLACEMENT_INTEGRATION",
        "predicted_option": "18",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Connecting constant engine power to kinetic energy and integrating non-linear velocity profile"},
                    "representation_translation": {"score": 1, "evidence": "Integrating v(t) = sqrt(2Pt/m) over time to derive straight-line displacement"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Find v(t) from Pt = 0.5*m*v^2, evaluate definite integral x(t) = int_0^9 v(t')dt', compute x(9)"},
                    "algebra_computational_load": {"score": 1, "evidence": "Evaluating fractional power 9^(3/2) = 27 and multiplying (2/3)*27 = 18 m"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing acceleration is non-constant; standard kinematic equations v=u+at cannot be used"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying calculus integration to constant power velocity function under rectilinear motion",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 18 unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Mass m = 2 kg, constant power P = 1 J/s. From work-energy theorem, P*t = 0.5*m*v^2 => (1)*t = 0.5*(2)*v^2 => v(t) = t^(1/2). Displacement x = int_0^t v(t') dt' = int_0^9 t'^(1/2) dt' = (2/3)*[t^(3/2)]_0^9 = (2/3)*(27) = 18 m.",
        "teaching_construction_family": {
            "construction_id": "TC-WPE-CONST-POWER-TRAJECTORY-01",
            "shared_candidates": ["EX-M43", "EX-M62", "EX-M64", "EX-M65", "EX-M120", "EX-N19"],
            "note": "Shares the ideal constant-power kinematic trajectory construction family with EX-M43, EX-M62, EX-M64, EX-M65, EX-M120, EX-N19."
        }
    },
    "EX-N39": {
        "sequence": 52,
        "batch_sequence": 7,
        "method": "INCLINE_ROUND_TRIP_WORK_ENERGY_FRICTION_DISSIPATION",
        "predicted_option": "346",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Round-trip inclined plane work-energy balance under non-conservative friction dissipation"},
                    "representation_translation": {"score": 1, "evidence": "Translating ascent/descent kinematics to total path length 2d and velocity deficit (v0/2)"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Relate ascent deceleration to distance d, equate two-way friction loss to net kinetic deficit 3/8 mv0^2, solve for mu"},
                    "algebra_computational_load": {"score": 2, "evidence": "Trigonometric simplification yielding mu = sqrt(3)/5 and integer scaling I = 1000 * 0.3464 = 346"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing friction does negative work in both ascent and descent directions"}
                },
                "total": 8,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/2/1", "total": 8},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "rationale": "Modeling coupled dissipative ascent/descent on inclined plane using work-energy theorem",
                "candidate_cell": "QRT-MODEL-D3",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "version": "0.2.0",
            "sha256": "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9",
            "blueprint_cell_ref": "D3.3",
            "topic_tag": "WPE-01-WORK",
            "status": "PINNED_CELL_UNQUALIFIED"
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "sha256": "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b",
            "status": "CELL_UNQUALIFIED_ADAPTER_GAP",
            "note": "WPE adapter defines cell D3.1 only. Target cell D3.3 requires adapter cell expansion; flagged as SPEC_GAP."
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 346 unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Ascent retardation a_up = g*(sin 30 + mu*cos 30). Distance to stop: d = v0^2 / (2*a_up). Round-trip net work done is solely due to friction: W_f = -2 * mu * m * g * cos 30 * d. Change in KE: Delta K = 0.5*m*(v0/2)^2 - 0.5*m*v0^2 = -(3/8)*m*v0^2. Equating: 2 * mu * m * g * cos 30 * [v0^2 / (2*g*(sin 30 + mu*cos 30))] = (3/8)*m*v0^2 => mu*cos 30 / (sin 30 + mu*cos 30) = 3/8 => 8*mu*cos 30 = 3*sin 30 + 3*mu*cos 30 => 5*mu*cos 30 = 3*sin 30 => mu = (3/5)*tan 30 = sqrt(3)/5 = 1.73205/5 = 0.34641. Since mu = I/1000, nearest integer to I is 346."
    },
    "EX-N42": {
        "sequence": 53,
        "batch_sequence": 8,
        "method": "MECHANICAL_ENERGY_CONSERVATION_TRAJECTORY_EXTREMA",
        "predicted_option": "10",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT_FIGURE_PENDING",
        "figure_status": "REQUIRED_UNRESOLVED",
        "figure_reference": "FIG-stem-1",
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Conservation of total mechanical energy in conservative gravitational field"},
                    "representation_translation": {"score": 1, "evidence": "Reading elevation coordinates hA = 2 m and hP = 1 m from schematic track and projectile description"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Direct energy conservation: KE_P = E_initial - PE_P = mg(hA - hP)"},
                    "algebra_computational_load": {"score": 1, "evidence": "Direct arithmetic: 1 * 10 * (2 - 1) = 10 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing intermediate track profile AOC and launch projectile angle are superfluous"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["REPRESENT"],
                "rationale": "Applying mechanical energy conservation across elevation points",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 10 unverified against official NTA master)",
            "HOLD:FIGURE_CUSTODY_UNRESOLVED (Question figure [FIG-stem-1] custody unverified)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Mass m = 1 kg, g = 10 m/s^2. Since track is frictionless and air resistance is absent, mechanical energy is conserved throughout. E_total = K_A + U_A = 0 + m*g*h_A = 1 * 10 * 2 = 20 J. At apex point P (height h_P = 1 m): U_P = m*g*h_P = 1 * 10 * 1 = 10 J. Kinetic energy at P: K_P = E_total - U_P = 20 - 10 = 10 J."
    },
    "AN-1": {
        "sequence": 54,
        "batch_sequence": 9,
        "method": "WORK_SIGN_CONVENTIONS_FORCE_DISPLACEMENT_EVALUATION",
        "predicted_option": "D: B and E only",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Sign determination of work done W = F . d across multiple dynamic force vectors"},
                    "representation_translation": {"score": 1, "evidence": "Multi-statement qualitative verbal analysis"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Evaluate 5 individual physical assertions against dot product sign conventions"},
                    "algebra_computational_load": {"score": 1, "evidence": "Zero algebraic computation; qualitative sign auditing"},
                    "trap_exception_sensitivity": {"score": 2, "evidence": "Trap in statement D: confusing net work = 0 for uniform velocity with work done by applied force alone; trap in statement A: work done by man vs gravity"}
                },
                "total": 8,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/2", "total": 8},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["EVALUATE"],
                "rationale": "Evaluating correctness of work sign assertions across diverse physical mechanical interactions",
                "candidate_cell": "QRT-JUSTIFY-D3",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "version": "0.2.0",
            "sha256": "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9",
            "blueprint_cell_ref": "D3.3",
            "topic_tag": "WPE-01-WORK",
            "status": "PINNED_CELL_UNQUALIFIED"
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "sha256": "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b",
            "status": "CELL_UNQUALIFIED_ADAPTER_GAP",
            "note": "WPE adapter defines cell D3.1 only. Target cell D3.3 requires adapter cell expansion; flagged as SPEC_GAP."
        },
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option D unverified against official NTA master)",
            "HOLD:FORCE_FRAME_CONTACT_QUALIFICATIONS (Force frame contact qualifications require review)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "A. Force by man on rope/bucket is upward, displacement upward => W > 0 (False). B. Gravitational force downward, displacement upward => W < 0 (True). C. Friction opposes downward slide along plane => W < 0 (False). D. Applied force is in direction of motion => W_applied > 0, even though net work W_net = 0 (False). E. Air resistance opposes instantaneous velocity of pendulum => W < 0 (True). Thus only B and E are correct (Option D)."
    },
    "AN-2": {
        "sequence": 55,
        "batch_sequence": 10,
        "method": "CONSERVATIVE_FORCE_LINE_INTEGRAL_AND_PATH_INDEPENDENCE_EVALUATION",
        "predicted_option": "C: Both Statement I and Statement II are false",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Rigorous definition of work done by force field W = +int F.dr vs potential energy change Delta U = -int F.dr"},
                    "representation_translation": {"score": 1, "evidence": "Dual statement logical verification"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Audit integral sign convention in Statement I; audit path independence axiom of conservative force in Statement II"},
                    "algebra_computational_load": {"score": 1, "evidence": "Checking sign convention on line integral definition"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Sign error confusion between work done by force (+W) and potential energy change (-W = Delta U)"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["EVALUATE"],
                "rationale": "Evaluating theoretical consistency of line integral signs and conservative force path-independence theorems",
                "candidate_cell": "QRT-JUSTIFY-D3",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option C unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Statement I: Work done BY the force is defined as W = +int_(r1)^(r2) F.dr. The negative integral -int F.dr represents Delta U (change in potential energy), not work done by force. Statement I is FALSE. Statement II: For any conservative force field, the work done is independent of the path taken between r1 and r2. Statement II claims it changes with the path, which is directly contradictory to the definition of a conservative force. Statement II is FALSE. Therefore, both Statement I and Statement II are false (Option C)."
    }
}

generated_audits = []
generated_source_only = []

for sid, spec in LOT12_SPECS.items():
    seq = spec["sequence"]
    ros = roster_items[sid]
    reg = reg_by_id[sid]

    q_dir = LOT_DIR / "questions" / f"{seq:02d}"
    s_dir = LOT_DIR / "source_only" / f"{seq:02d}"
    q_dir.mkdir(parents=True, exist_ok=True)
    s_dir.mkdir(parents=True, exist_ok=True)

    stem_text = reg["stem"]
    stem_sha = hashlib.sha256(stem_text.encode("utf-8")).hexdigest()
    options = reg.get("options", [])
    if isinstance(options, dict):
        options = [f"{k}: {v}" for k, v in options.items()]

    # 1. Full Question Audit Record
    audit_rec = {
        "sequence": seq,
        "batch_sequence": spec["batch_sequence"],
        "task_identity": ros["task_identity"],
        "stable_id": f"PHYS-WPE-LOT12-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-12",
        "batch": "BATCH-D",
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
        "key_issuing_authority": spec["key_issuing_authority"],
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
        "next_action": f"B2 independent source-only solve + official {spec['key_issuing_authority']} master key reconciliation"
    }

    if "teaching_construction_family" in spec:
        audit_rec["teaching_construction_family"] = spec["teaching_construction_family"]

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
            <span class="badge badge-lot">LOT-12</span><br>
            <small class="mono">{q['task_identity']}</small><br>
            <small>Batch #{q['batch_sequence']}</small>
        </td>
        <td class="col-source">
            <strong>{q['source_id']}</strong><br>
            <small class="text-muted">{q['paper']}</small><br>
            <span class="badge badge-source">{q['source_custody']}</span>
            <span class="badge badge-fig">{q['figure_status']}</span><br>
            <small>Auth: <strong>{q['key_issuing_authority']}</strong></small>
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
    <title>Grade9 v4.0 — Lot 12 Private Review Dashboard (Questions 51–55)</title>
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
        .col-cog {{ width: 130px; }}
        .col-bp {{ width: 170px; }}
        .col-gates {{ width: 260px; }}

        .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
        .text-muted {{ color: var(--text-muted); }}

        .badge {{
            display: inline-block;
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
            margin-top: 4px;
        }}

        .badge-lot {{ background: #ede9fe; color: #6d28d9; }}
        .badge-source {{ background: #e0f2fe; color: #0369a1; }}
        .badge-fig {{ background: #fef3c7; color: #92400e; }}
        .badge-prop {{ background: #dcfce7; color: #15803d; }}
        .badge-hold {{ background: #fef2f2; color: #b91c1c; font-family: monospace; }}
        .badge-admission {{ background: #fef2f2; color: #991b1b; font-weight: 700; border: 1px solid #f87171; }}

        .stem-preview {{
            font-size: 12px;
            color: var(--text);
            margin-bottom: 8px;
            max-height: 60px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .solve-summary {{
            font-size: 12px;
            background: #f8fafc;
            padding: 6px 8px;
            border-radius: 4px;
            border: 1px solid #e2e8f0;
        }}

        .blocker-list {{
            list-style: none;
            margin-top: 6px;
        }}

        .blocker-list li {{
            font-size: 11px;
            color: var(--danger);
            margin-bottom: 2px;
            padding-left: 12px;
            position: relative;
        }}

        .blocker-list li::before {{
            content: "•";
            position: absolute;
            left: 2px;
            color: var(--danger);
        }}

        footer {{
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
        }}

        .pr-banner {{
            margin-top: 15px;
            padding: 10px 14px;
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 6px;
            font-size: 12px;
            color: #92400e;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Grade9 v4.0 — Lot 12 Private Review Dashboard</h1>
            <div class="header-meta">
                Batch D (CP-2) | Candidates Q51–Q55 | Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
                <strong>Academic Notice:</strong> No academic approval inferred from software validation.
            </div>
            <div class="pr-banner">
                <strong>PR Gate Status:</strong> <code>PR: HOLD_BASE_NOT_READY</code> — Retained in local private storage until stable base designated by owner.
            </div>
        </header>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Sequence</th>
                        <th>Source Custody</th>
                        <th>Stem & Candidate Solve</th>
                        <th>Cognitive Demand</th>
                        <th>Blueprint Fit</th>
                        <th>Gates & Blockers</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows_html)}
                </tbody>
            </table>
        </div>

        <footer>
            Grade9 v4.0 Academic Platform &bull; Private Review Artifact &bull; Confidential
        </footer>
    </div>
</body>
</html>
"""

review_dir = LOT_DIR / "review"
review_dir.mkdir(parents=True, exist_ok=True)
with open(review_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Lot 12 Review Dashboard generated: review/index.html")
