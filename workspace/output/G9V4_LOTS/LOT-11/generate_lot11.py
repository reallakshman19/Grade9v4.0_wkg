"""
Grade9 v4.0 — Lot 11 Generator (Questions 46–50)
Batch D, CP-1
Generates:
  - questions/46..50/QUESTION_AUDIT.json
  - source_only/46..50/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-11")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-11"}

# Lot 11 Physics & Calibration Data
LOT11_SPECS = {
    "EX-N21": {
        "sequence": 46,
        "batch_sequence": 1,
        "method": "POSITION_DEPENDENT_FORCE_WORK_INTEGRAL",
        "predicted_option": "2",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT_FIGURE_PENDING",
        "figure_status": "REQUIRED_UNRESOLVED",
        "figure_reference": "FIG-stem-1",
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Work integral with position-dependent directional force F = 2N at angle theta = kx"},
                    "representation_translation": {"score": 2, "evidence": "Parameterizing horizontal force component Fx = F*cos(kx) and integrating along x"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Formulate W = int_0^x 2*cos(kx')dx', evaluate definite integral to (2/k)*sin(kx), equate to (n/k)*sin(theta)"},
                    "algebra_computational_load": {"score": 1, "evidence": "Direct calculus evaluation of cosine integral yielding coefficient n = 2"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Normal force and vertical component do no work on smooth horizontal plane"}
                },
                "total": 8,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/2/2/1/1", "total": 8},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "rationale": "Constructing dynamic work integral model with coupled variable angle force on frictionless plane",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 2 unverified against official NTA master)",
            "HOLD:FIGURE_CUSTODY_UNRESOLVED (Question figure [FIG-stem-1] custody unverified)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Work done by variable force: W = int_0^x F_x dx' = int_0^x 2*cos(kx') dx' = (2/k)*sin(kx) = (2/k)*sin(theta). By Work-Energy Theorem, Delta K = E = W = (2/k)*sin(theta). Comparing with E = (n/k)*sin(theta) yields n = 2."
    },
    "EX-N27": {
        "sequence": 47,
        "batch_sequence": 2,
        "method": "WORK_ENERGY_DISSIPATIVE_SPRING_BALANCE",
        "predicted_option": "16",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Energy conservation balancing dissipative fractional friction loss (90%) and spring elastic potential (10%)"},
                    "representation_translation": {"score": 1, "evidence": "Converting velocity 72 km/h -> 20 m/s and relating wagon kinetic energy to shock absorber compression"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Compute initial KE (8 MJ), determine stored spring energy (800 kJ), solve for spring constant k"},
                    "algebra_computational_load": {"score": 1, "evidence": "Arithmetic division: (800000 * 2) / 1.0^2 = 1.6 * 10^6 N/m = 16 * 10^5 N/m"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Initial length of shock absorber 1.5 m is an extraneous distractor; only compression 1.0 m enters energy"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying work-energy partition theorem with fractional dissipative losses to spring deceleration",
                "candidate_cell": "QRT-APPLY-D3",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 16 unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Speed v = 72 km/h = 20 m/s. Initial KE = 0.5 * 40,000 * 20^2 = 8,000,000 J. Friction loss = 90% * 8,000,000 = 7,200,000 J. Remaining energy absorbed by spring: U_spring = 800,000 J. 0.5 * k * x^2 = 800,000 J with x = 1.0 m => k = 1,600,000 N/m = 16 * 10^5 N/m. Spring constant prefactor is 16."
    },
    "EX-N30": {
        "sequence": 48,
        "batch_sequence": 3,
        "method": "CONTINUOUS_CHAIN_POTENTIAL_ENERGY_CONSERVATION",
        "predicted_option": "40",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Continuous gravitational potential energy modeling via center of mass elevation shift for hanging chain"},
                    "representation_translation": {"score": 1, "evidence": "Translating 2 m on table to 1 m overhang out of total 3 m length, with linear mass density 1 kg/m"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Compute initial PE with 1m hanging (CM at -0.5m), final PE with 3m hanging (CM at -1.5m), equate PE loss to KE"},
                    "algebra_computational_load": {"score": 1, "evidence": "Direct arithmetic: Ui = -1*10*0.5 = -5 J, Uf = -3*10*1.5 = -45 J, Kf = 40 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Using CM elevation at half-length rather than full length; avoiding confusion between lying vs hanging length"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["APPLY"],
                "rationale": "Modeling variable potential energy of flexible continuum mass slipping off smooth horizontal table",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 40 unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Total length L = 3 m, mass M = 3 kg => linear density lambda = 1 kg/m. Smooth table reference U = 0 at surface. Initial state: 1 m hanging (mass 1 kg), CM at y = -0.5 m => U_i = -1 * 10 * 0.5 = -5 J. Final state: 3 m hanging (mass 3 kg), CM at y = -1.5 m => U_f = -3 * 10 * 1.5 = -45 J. Mechanical energy conserved: K_i + U_i = K_f + U_f => 0 - 5 = K_f - 45 => K_f = 40 J."
    },
    "EX-N31": {
        "sequence": 49,
        "batch_sequence": 4,
        "method": "HEMISPHERE_NORMAL_CONTACT_LOSS_ENERGY_CONSERVATION",
        "predicted_option": "2",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT_FIGURE_PENDING",
        "figure_status": "REQUIRED_UNRESOLVED",
        "figure_reference": "FIG-stem-1",
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Coupling mechanical energy conservation with radial dynamic contact loss condition N = 0 on spherical surface"},
                    "representation_translation": {"score": 1, "evidence": "Expressing normal component of gravity and centripetal acceleration in terms of vertical height h: cos(theta) = h/R"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Formulate speed v^2 = 2g(R - h), set radial equilibrium mg*cos(theta) - m*v^2/R = 0, solve for detachment height h = 2R/3"},
                    "algebra_computational_load": {"score": 1, "evidence": "Direct substitution h = (2/3)*3 = 2 m"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Height h defined from base plane vs fallen distance R - h from zenith"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "MODEL",
                "secondary": ["JUSTIFY"],
                "rationale": "Modeling dynamic detachment threshold on curved frictionless boundary under gravity",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 2 unverified against official NTA master)",
            "HOLD:FIGURE_CUSTODY_UNRESOLVED (Question figure [FIG-stem-1] custody unverified)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Let theta be angle from vertical. Height h = R*cos(theta). By energy conservation, 0.5*m*v^2 = mg*(R - h) => v^2 = 2g(R - h). Radial equation: mg*cos(theta) - N = m*v^2/R. At detachment point, N = 0 => mg*(h/R) = m*(2g(R - h))/R => h = 2(R - h) => 3h = 2R => h = 2R/3. Given R = 3 m => h = 2 m."
    },
    "EX-N34": {
        "sequence": 50,
        "batch_sequence": 5,
        "method": "SPRING_ENERGY_HORIZONTAL_PROJECTILE_KINEMATICS",
        "predicted_option": "1",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT_FIGURE_PENDING",
        "figure_status": "REQUIRED_UNRESOLVED",
        "figure_reference": "FIG-stem-1",
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Sequential two-phase model: elastic potential energy to horizontal kinetic energy, followed by 2D ballistic free fall"},
                    "representation_translation": {"score": 1, "evidence": "Unit conversions (100 g -> 0.1 kg) and horizontal projection trajectory range formula"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Determine muzzle speed from spring decompression, compute flight time from vertical drop H = 2 m, evaluate horizontal range d = v*t"},
                    "algebra_computational_load": {"score": 1, "evidence": "Calculations with square roots: v = 0.05*sqrt(1000) = 0.5*sqrt(10), t = sqrt(4/10) = 2/sqrt(10), d = 0.5*sqrt(10)*2/sqrt(10) = 1 m"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Neglecting gravitational potential energy inside horizontal barrel"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying spring decompression energy conservation coupled with ballistic horizontal range kinematics",
                "candidate_cell": "QRT-APPLY-D3",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 1 unverified against official NTA master)",
            "HOLD:FIGURE_CUSTODY_UNRESOLVED (Question figure [FIG-stem-1] custody unverified)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Spring constant k = 100 N/m, mass m = 0.1 kg, compression x = 0.05 m. Launch velocity: 0.5*k*x^2 = 0.5*m*v^2 => v = x*sqrt(k/m) = 0.05*sqrt(100/0.1) = 0.05*sqrt(1000) = 0.5*sqrt(10) m/s. Vertical fall from height H = 2 m: t = sqrt(2H/g) = sqrt(4/10) = 2/sqrt(10) s. Horizontal range: d = v*t = (0.5*sqrt(10)) * (2/sqrt(10)) = 1.0 m."
    }
}

generated_audits = []
generated_source_only = []

for sid, spec in LOT11_SPECS.items():
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
        "stable_id": f"PHYS-WPE-LOT11-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-11",
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
            <span class="badge badge-lot">LOT-11</span><br>
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
    <title>Grade9 v4.0 — Lot 11 Private Review Dashboard (Questions 46–50)</title>
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
            <h1>Grade9 v4.0 — Lot 11 Private Review Dashboard</h1>
            <div class="header-meta">
                Batch D (CP-1) | Candidates Q46–Q50 | Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
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

print("Lot 11 Review Dashboard generated: review/index.html")
