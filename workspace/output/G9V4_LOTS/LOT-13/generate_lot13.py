"""
Grade9 v4.0 — Lot 13 Generator (Questions 56–60)
Batch D, CP-3
Generates:
  - questions/56..60/QUESTION_AUDIT.json
  - source_only/56..60/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-13")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-13"}

# Lot 13 Physics & Calibration Data
LOT13_SPECS = {
    "AN-3": {
        "sequence": 56,
        "batch_sequence": 11,
        "method": "CENTRAL_FORCE_PATH_INDEPENDENCE_AND_CONSERVATIVE_THEORY",
        "predicted_option": "B: Both A and R are true but R is NOT the correct explanation of A",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Differentiating conservative central force fields from general non-conservative mechanical forces"},
                    "representation_translation": {"score": 1, "evidence": "Assertion-Reason logical schema mapping"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Verify truth of Assertion A, verify truth of Reason R, test causal explanatory dependency"},
                    "algebra_computational_load": {"score": 1, "evidence": "Qualitative theoretical analysis; zero algebraic calculation"},
                    "trap_exception_sensitivity": {"score": 2, "evidence": "Explanatory link fallacy: Reason stating true fact about non-conservative forces does not explain central force conservatism"}
                },
                "total": 8,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/2", "total": 8},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["EVALUATE"],
                "rationale": "Evaluating theoretical consistency of central force conservative fields and causal explanatory logic in mechanics",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option B unverified against official NTA master)",
            "HOLD:CENTRAL_FORCE_QUALIFICATION (Central force spherical symmetry assumption requires qualification)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.4 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Assertion A: Any standard central force F(r) = f(r) r^ is conservative, satisfying curl(F) = 0, so work done between any two points is independent of path. Assertion A is TRUE. Reason R: In mechanics, dissipative forces like friction or drag cannot be associated with a potential energy function. Reason R is TRUE. However, the non-existence of potential energy for dissipative forces does not explain why central forces are conservative and path-independent (path independence arises from radial curl-free symmetry). Thus R is not the correct explanation of A (Option B)."
    },
    "AN-5": {
        "sequence": 57,
        "batch_sequence": 12,
        "method": "ORTHOGONAL_FORCE_POWER_AND_KINETIC_ENERGY_INVARIANCE",
        "predicted_option": "A: its kinetic energy is constant",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "CBSE",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Power scalar product orthogonality condition P = F . v = 0 implying zero rate of change of kinetic energy"},
                    "representation_translation": {"score": 1, "evidence": "Multiple choice qualitative vector invariant deduction"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Orthogonal force does zero work => speed is constant => kinetic energy is strictly constant"},
                    "algebra_computational_load": {"score": 1, "evidence": "Zero algebraic computation; qualitative vector mechanics"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Confusing constant magnitude of acceleration with constant vector acceleration; velocity and acceleration rotate continuously"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "JUSTIFY",
                "secondary": ["MODEL"],
                "rationale": "Applying scalar work-energy theorem to perpendicular directional force constraints",
                "candidate_cell": "QRT-JUSTIFY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option A unverified against official CBSE master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "The instantaneous power delivered by the force is P = F . v. Given that F is always perpendicular to v, F . v = 0 at every instant. By the Work-Energy Theorem, dK/dt = P = 0, which implies that kinetic energy K is constant (Option A). Because the force has constant magnitude and is always perpendicular to velocity, the speed is constant while the direction of motion continuously changes (uniform circular motion in a plane). Thus velocity and acceleration vectors change direction continuously and are not constant."
    },
    "AN-6": {
        "sequence": 58,
        "batch_sequence": 13,
        "method": "CONSERVATIVE_FORCE_POTENTIAL_ENERGY_EXISTENCE_IDENTIFICATION",
        "predicted_option": "A: Frictional force",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "NOT_REQUIRED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Potential energy definition criterion: potential energy exists if and only if the force is conservative"},
                    "representation_translation": {"score": 1, "evidence": "Single-choice qualitative physical taxonomy"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Evaluate Coulomb, restoring, and gravity forces as conservative; identify friction as dissipative"},
                    "algebra_computational_load": {"score": 1, "evidence": "Zero computation"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Direct identification of non-conservative dissipative force"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "IDENTIFY",
                "secondary": ["JUSTIFY"],
                "rationale": "Identifying non-conservative dissipative forces incapable of potential energy representation",
                "candidate_cell": "QRT-IDENTIFY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option A unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Potential energy U is defined exclusively for conservative forces, such that F = -grad(U). Coulomb's electrostatic force, spring restoring force, and gravitational force are conservative forces with well-defined potential energies. Frictional force is non-conservative and dissipative (work done along a path is dissipated as thermal internal energy and cannot be recovered as mechanical potential energy). Therefore, frictional force cannot be expressed in terms of potential energy (Option A)."
    },
    "JEE-2026-04-04-S1-Q46": {
        "sequence": 59,
        "batch_sequence": 14,
        "method": "SUPERPOSED_FORCES_3D_VECTOR_WORK_DOT_PRODUCT",
        "predicted_option": "35",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Superposition of simultaneous 3D vector forces and directional unit vector displacement projection"},
                    "representation_translation": {"score": 1, "evidence": "Normalizing direction vector (3i^ - 4j^)/5 and scaling by distance 25 m to construct displacement vector"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Calculate resultant force F_net, calculate full displacement vector s, evaluate 3D dot product W = F_net . s"},
                    "algebra_computational_load": {"score": 1, "evidence": "Evaluating vector components: (5)(15) + (2)(-20) + (2)(0) = 75 - 40 = 35 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Remembering to normalize (3i^ - 4j^) by magnitude 5 before multiplying by 25 m"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["REPRESENT"],
                "rationale": "Applying 3D vector dot product work calculations with resultant force and directional displacement",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 35 unverified against official NTA master)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "1. Resultant force: F_net = F_1 + F_2 = (2 + 3)i^ + (3 - 1)j^ + (4 - 2)k^ = (5i^ + 2j^ + 2k^) N. 2. Unit displacement vector along direction (3i^ - 4j^): u^ = (3i^ - 4j^) / sqrt(3^2 + (-4)^2) = (3i^ - 4j^) / 5. 3. Total displacement vector: s = 25 * u^ = 25 * (3i^ - 4j^) / 5 = (15i^ - 20j^) m. 4. Work done by net force: W = F_net . s = (5)(15) + (2)(-20) + (2)(0) = 75 - 40 = 35 J."
    },
    "JEE-2026-04-06-S2-Q29": {
        "sequence": 60,
        "batch_sequence": 15,
        "method": "WORK_ENERGY_THEOREM_POSITION_DEPENDENT_VELOCITY",
        "predicted_option": "6911214180: 1250",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Work-energy theorem applied to 1D motion under position-dependent velocity function v(x) = 2x^2"},
                    "representation_translation": {"score": 1, "evidence": "Evaluating initial and final kinematic states at position boundaries x = 0 and x = 5 m"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Compute v(0) = 0, v(5) = 50 m/s, evaluate kinetic energy change W_net = 0.5 * m * (vf^2 - vi^2)"},
                    "algebra_computational_load": {"score": 1, "evidence": "Arithmetic evaluation: 0.5 * 1 * (50^2) = 0.5 * 2500 = 1250 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Evaluating work done by the body vs on the body phrasing ambiguity"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying work-energy theorem to non-linear position-dependent velocity profile",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option 6911214180 unverified against official NTA master)",
            "HOLD:WORK_BY_VS_ON_WORDING_AMBIGUITY (Work done by vs on the body wording requires clarification)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "1. At initial position x_i = 0 m: v_i = 2(0)^2 = 0 m/s, so K_i = 0 J. 2. At final position x_f = 5 m: v_f = 2(5)^2 = 50 m/s. 3. By Work-Energy Theorem: W_net = Delta K = 0.5 * m * (v_f^2 - v_i^2) = 0.5 * (1 kg) * (50^2 - 0) = 1250 J. (Alternative calculus route: F = m * v * dv/dx = 1 * (2x^2) * (4x) = 8x^3 N. W = int_0^5 8x^3 dx = [2x^4]_0^5 = 2(625) = 1250 J.) Matches option ID 6911214180."
    }
}

generated_audits = []
generated_source_only = []

for sid, spec in LOT13_SPECS.items():
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
        "stable_id": f"PHYS-WPE-LOT13-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-13",
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
            <span class="badge badge-lot">LOT-13</span><br>
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
    <title>Grade9 v4.0 — Lot 13 Private Review Dashboard (Questions 56–60)</title>
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
            <h1>Grade9 v4.0 — Lot 13 Private Review Dashboard</h1>
            <div class="header-meta">
                Batch D (CP-3) | Candidates Q56–Q60 | Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
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

print("Lot 13 Review Dashboard generated: review/index.html")
