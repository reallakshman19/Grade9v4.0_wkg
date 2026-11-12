"""
Grade9 v4.0 — Lot 14 Generator (Questions 61–65)
Batch D / Final Five Provisional In-Scope WPE Identities
Generates:
  - questions/61..65/QUESTION_AUDIT.json
  - source_only/61..65/SOURCE_ONLY.json
  - review/index.html
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

LOT_DIR = Path("D:/CodeD/grade9v4/workspace/output/G9V4_LOTS/LOT-14")
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
roster_items = {r["source_id"]: r for r in roster_data["roster"] if r["lot"] == "LOT-14"}

# Allowed native cognitive operations
ALLOWED_OPERATIONS = {"RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}

# Lot 14 Physics & Calibration Data
LOT14_SPECS = {
    "JEE-2026-04-06-S1-Q28": {
        "sequence": 61,
        "lot_sequence": 1,
        "method": "WORK_ENERGY_THEOREM_DISSIPATIVE_RESISTANCE",
        "predicted_option": "6952787592: - 9.98",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "official_key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Work-energy theorem with conservative gravity and unknown dissipative drag force W_g + W_res = Delta K"},
                    "representation_translation": {"score": 1, "evidence": "Unit conversions: mass 1 g -> 10^-3 kg, height 1 km -> 1000 m"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Compute W_g = 10 J, compute Kf = 0.0125 J, isolate W_res = Kf - W_g"},
                    "algebra_computational_load": {"score": 1, "evidence": "Arithmetic subtraction: 0.0125 - 10.0 = -9.9875 J"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Distinguishing negative resistive work from positive gravity work; nearest option rounding"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Enforced strict D2 band mapping for score sum 5 (3-5 = D2)"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying work-energy balance to particle terminal descent with resistive dissipation",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option 6952787592 unverified against official NTA master)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:NEAREST_OPTION_VS_ROUNDING (Rounding of -9.9875 to -9.98 requires review)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Mass m = 1 g = 10^-3 kg, fall distance h = 1 km = 1000 m, initial speed vi = 0, final speed vf = 5 m/s. Work done by gravity: W_g = m*g*h = (10^-3)(10)(1000) = +10.0 J. Final kinetic energy: K_f = 0.5 * (10^-3) * (5^2) = 0.0125 J. By Work-Energy Theorem, W_g + W_res = Delta K = 0.0125 J => W_res = 0.0125 - 10.0 = -9.9875 J ~= -9.98 J. Matches option ID 6952787592."
    },
    "JEE-2026-04-02-S2-Q31": {
        "sequence": 62,
        "lot_sequence": 2,
        "method": "UNIVERSAL_GRAVITATION_MECHANICAL_ENERGY_CONSERVATION",
        "predicted_option": "691121616: 11.2 km/s; 6.27 x 10^7 J",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "official_key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "Conservation of mechanical energy in non-uniform 1/r gravitational potential field from infinity to Earth surface"},
                    "representation_translation": {"score": 1, "evidence": "Relating surface potential GMm/R to surface gravity acceleration parameter g*R"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Determine potential difference U(infty) - U(R) = mgR, equate to kinetic energy k, solve for impact speed v"},
                    "algebra_computational_load": {"score": 1, "evidence": "Numerical calculation: k = 1 * 9.8 * 6.4e6 = 6.272e7 J, v = sqrt(2*9.8*6.4e6) = 11.2 km/s"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Prerequisite boundary: non-uniform inverse-square gravitation required rather than uniform mgh"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying energy conservation to escape/infall potential in central gravitational field",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Option 691121616 unverified against official NTA master)",
            "HOLD:NONUNIFORM_GRAVITY_PREREQUISITE (Inverse square gravitation prerequisite requires qualification in WPE)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Conservation of energy between r = infty and r = R (Earth radius): E_initial = 0 + 0 = 0. E_final = K_f - GMm/R = 0 => K_f = GMm/R = m*g*R = (1 kg)(9.8 m/s^2)(6.4 x 10^6 m) = 6.272 x 10^7 J ~= 6.27 x 10^7 J. Impact speed: 0.5 * m * v^2 = K_f => v = sqrt(2*g*R) = sqrt(2 * 9.8 * 6.4 x 10^6) = sqrt(1.2544 x 10^8) = 11.2 x 10^3 m/s = 11.2 km/s. Matches option 691121616."
    },
    "JEE-2026-04-04-S1-Q49": {
        "sequence": 63,
        "lot_sequence": 3,
        "method": "TIME_DEPENDENT_VECTOR_FORCE_INTEGRATION_AND_POWER",
        "predicted_option": "200",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "VERIFIED_TEXT",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": None,
        "key_issuing_authority": "NTA",
        "official_key_status": "HOLD:OFFICIAL_KEY_UNRESOLVED",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 2, "evidence": "2D vector calculus kinematics from time-varying force followed by instantaneous power dot product P = F . v"},
                    "representation_translation": {"score": 1, "evidence": "Interpreting 2D Cartesian polynomial components in vector unit notation"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Integrate a(t) = F(t)/m to obtain v(t), evaluate both F and v at t = 2 s, compute vector dot product"},
                    "algebra_computational_load": {"score": 1, "evidence": "Polynomial integration and evaluation: P = (4)(2) + (24)(8) = 8 + 192 = 200 W"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Prerequisite calculus: time-varying acceleration invalidates standard constant-acceleration kinematic formulas"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "INITIAL_CALIBRATION", "scores": "2/1/2/1/1", "total": 7},
                "differences": "Initial native factor audit"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying vector calculus kinematic integration and dot product power definition",
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
            "HOLD:OFFICIAL_KEY_UNRESOLVED (Numerical answer 200 unverified against official NTA master)",
            "HOLD:CALCULUS_PREREQUISITE_UNQUALIFIED (Time-dependent vector calculus integration requires qualification)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.3 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Mass m = 2 kg. F(t) = 2t i^ + 6t^2 j^ N. Acceleration a(t) = F(t)/m = t i^ + 3t^2 j^ m/s^2. Since body begins to move from rest, v(0) = 0. Velocity v(t) = int_0^t a(t') dt' = (t^2 / 2) i^ + t^3 j^ m/s. At t = 2 s: F(2) = 2(2) i^ + 6(4) j^ = 4 i^ + 24 j^ N. v(2) = (4/2) i^ + (8) j^ = 2 i^ + 8 j^ m/s. Instantaneous power: P = F(2) . v(2) = (4)(2) + (24)(8) = 8 + 192 = 200 W."
    },
    "WEP07-02": {
        "sequence": 64,
        "lot_sequence": 4,
        "method": "UNIFORM_CHAIN_OVERHANG_POTENTIAL_ENERGY_CONSERVATION",
        "predicted_option": "a: v = sqrt(g(L - y0^2/L))",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "UNBOUND_ORIGINAL_PENDING_WITNESS",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": "SAVED_ITEM_CROP:WEP07-02_NSEP2024-61_Q32.png",
        "key_issuing_authority": "IAPT",
        "official_key_status": "HOLD:OFFICIAL_KEY_NOT_RETAINED",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Recognizing a constant-mass flexible chain as an energy-conserving system despite varying hanging fraction"},
                    "representation_translation": {"score": 2, "evidence": "Translating changing dangling length into gravitational potential energy of uniform segment at center-of-mass depth y/2"},
                    "reasoning_chain_length": {"score": 2, "evidence": "Formulate U_initial and U_final, calculate energy difference, equate to whole-chain kinetic energy"},
                    "algebra_computational_load": {"score": 1, "evidence": "Simplify lambda*g*(L^2 - y0^2)/2 against kinetic energy lambda*L*v^2/2"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Recognizing entire chain of mass lambda*L moves with speed v as it leaves table"}
                },
                "total": 7,
                "band": "D3",
                "prior_proposal": {"source": "AUDITED_PRIOR_RECORD", "scores": "1/2/2/1/1", "total": 7},
                "differences": "Preserved audited five-factor score 7, mapped to D3.6 (SYNTHESIZE)"
            },
            "demand_proposal": {
                "primary": "SYNTHESIZE",
                "secondary": ["MODEL"],
                "rationale": "Coordinating distributed gravitational potential energy states with full-continuum kinetic energy",
                "candidate_cell": "QRT-SYNTHESIZE-D3",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": {
            "blueprint_id": "PHYS-QRT-BLUEPRINT",
            "version": "0.2.0",
            "sha256": "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9",
            "blueprint_cell_ref": "D3.6",
            "topic_tag": "WPE-02-POTENTIAL",
            "status": "PINNED_CELL_UNQUALIFIED"
        },
        "adapter_fit": {
            "adapter_id": "PHYS-TOPIC-WPE",
            "sha256": "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b",
            "status": "CELL_UNQUALIFIED_ADAPTER_GAP",
            "note": "WPE adapter defines cell D3.1 only. Target cell D3.6 requires adapter cell expansion; flagged as SPEC_GAP."
        },
        "blockers": [
            "HOLD:EXACT_TEXT_EXTRACTION_NOT_COMPLETED (Registry lacks bound stem text; pending independent witness)",
            "HOLD:OFFICIAL_KEY_NOT_RETAINED (Official key not bound/retained in local registry)",
            "HOLD:ADAPTER_CELL_GAP (WPE adapter lacks D3.6 cell authority)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Take tabletop edge as U = 0. Dangling segment of length y0 has mass lambda*y0 with center of mass at -y0/2, so U_i = -0.5 * lambda * g * y0^2. When entire chain leaves edge, hanging mass is lambda*L with center of mass at -L/2, so U_f = -0.5 * lambda * g * L^2. Kinetic energy of entire chain: K_f = 0.5 * (lambda * L) * v^2. By conservation of energy: 0.5 * lambda * L * v^2 = 0.5 * lambda * g * (L^2 - y0^2) => L * v^2 = g * (L^2 - y0^2) => v = sqrt(g * (L - y0^2 / L)). Matches option a."
    },
    "WEP07-03": {
        "sequence": 65,
        "lot_sequence": 5,
        "method": "POTENTIAL_WELL_TURNING_POINT_AND_VELOCITY_EXTREMUM",
        "predicted_option": "a, b, c, d (All four statements verified)",
        "solve_status": "CANDIDATE_DERIVED",
        "source_custody": "UNBOUND_ORIGINAL_PENDING_WITNESS",
        "figure_status": "REQUIRED_RETAINED",
        "figure_reference": "PDF_PAGE:15_Q57:NSEP_-_2025_Set_611.pdf",
        "key_issuing_authority": "IAPT",
        "official_key_status": "VERIFIED_IAPT_KEY_RECEIPT",
        "sl2": {
            "mode": "QUESTION",
            "difficulty_evidence": {
                "components": {
                    "concept_model_selection": {"score": 1, "evidence": "Applying mechanical energy conservation E = K + U = 0 to 1D non-linear potential well"},
                    "representation_translation": {"score": 1, "evidence": "Substituting beta = alpha/x0 and writing potential in terms of dimensionless ratio z = x0/x"},
                    "reasoning_chain_length": {"score": 1, "evidence": "Execute energy conservation to extract v(x) and complete the square for velocity extremum"},
                    "algebra_computational_load": {"score": 1, "evidence": "Algebraic completing of the square: z - z^2 = 1/4 - (z - 1/2)^2"},
                    "trap_exception_sensitivity": {"score": 1, "evidence": "Verifying turning point constraint x >= x0 where 0 < z <= 1 coexists with E = 0"}
                },
                "total": 5,
                "band": "D2",
                "prior_proposal": {"source": "ADJUDICATED_RECONCILIATION", "scores": "1/1/1/1/1", "total": 5},
                "differences": "Preserved previously adjudicated APPLY/D2 decision per B2 CP-4 checkpoint instructions"
            },
            "demand_proposal": {
                "primary": "APPLY",
                "secondary": ["MODEL"],
                "rationale": "Applying energy conservation and quadratic extremum formulas to 1D potential function",
                "candidate_cell": "QRT-APPLY-D2",
                "status": "PROPOSED"
            },
            "status": "UNREVIEWED"
        },
        "blueprint_fit": "BLUEPRINT=SPEC_PENDING",
        "adapter_fit": "ADAPTER=SPEC_PENDING",
        "blockers": [
            "HOLD:EXACT_TEXT_EXTRACTION_NOT_COMPLETED (Registry lacks bound stem text; pending independent witness)",
            "HOLD:SPEC_PENDING (No qualified D1/D2 common blueprint or topic adapter)",
            "HOLD:PAPER_CODE_61_VS_611_RECONCILIATION (Paper code 61 vs 611 reconciliation requires review)",
            "HOLD:ACADEMIC_ADMISSION (No human reviewer approval receipt)"
        ],
        "derivation": "Potential U(x) = alpha/x^2 - beta/x with alpha, beta > 0. Released from rest at x0 = alpha/beta => beta = alpha/x0. Substitute beta: U(x) = (alpha/x0^2)[(x0/x)^2 - x0/x]. At release point x = x0: U(x0) = 0 and K(x0) = 0, so conserved total energy E = 0. Statement (d) holds. Statement (a) holds. Speed: 0.5 * m * v^2 = -U(x) => v(x) = [(2*alpha/(m*x0^2)) * (x0/x - (x0/x)^2)]^(1/2). Statement (b) holds. Complete square for maximum speed: z - z^2 = 1/4 - (z - 1/2)^2, maximum is 1/4 at z = 1/2 (x = 2*x0) => v_max = sqrt(alpha / (2*m*x0^2)). Statement (c) holds. Official key (a, b, c, d) verified by IAPT final key receipt."
    }
}

generated_audits = []
generated_source_only = []

for sid, spec in LOT14_SPECS.items():
    seq = spec["sequence"]
    ros = roster_items[sid]
    reg = reg_by_id.get(sid, {})

    q_dir = LOT_DIR / "questions" / f"{seq:02d}"
    s_dir = LOT_DIR / "source_only" / f"{seq:02d}"
    q_dir.mkdir(parents=True, exist_ok=True)
    s_dir.mkdir(parents=True, exist_ok=True)

    stem_raw = reg.get("stem")
    if stem_raw:
        stem_text = stem_raw
        stem_sha = hashlib.sha256(stem_text.encode("utf-8")).hexdigest()
        source_hash = stem_sha
        source_digest = f"sha256:{stem_sha}"
        stem_status = "VERIFIED_BOUND_TEXT"
    else:
        stem_text = None
        stem_sha = None
        source_hash = None
        source_digest = None
        stem_status = "SOURCE_INCOMPLETE_UNBOUND_REGISTRY_STEM"

    options_raw = reg.get("options")
    if isinstance(options_raw, dict):
        options = [f"{k}: {v}" for k, v in options_raw.items()]
    elif isinstance(options_raw, list):
        options = options_raw
    else:
        options = None

    # Validate Blueprint cell correspondence against 7 canonical operations
    op = spec["sl2"]["demand_proposal"]["primary"]
    assert op in ALLOWED_OPERATIONS, f"Invalid operation: {op}"

    bp_fit = spec["blueprint_fit"]
    if isinstance(bp_fit, dict):
        cell_ref = bp_fit["blueprint_cell_ref"]
        # Operation mapping verification: D3.3 = APPLY, D3.4 = MODEL, D3.6 = SYNTHESIZE, etc.
        expected_op_col_map = {
            "RETRIEVE": "1", "EXPLAIN": "2", "APPLY": "3", "MODEL": "4",
            "REPRESENT": "5", "SYNTHESIZE": "6", "JUSTIFY": "7"
        }
        band = spec["sl2"]["difficulty_evidence"]["band"]
        expected_cell_ref = f"{band}.{expected_op_col_map[op]}"
        assert cell_ref == expected_cell_ref, f"Blueprint cell mismatch! {cell_ref} != {expected_cell_ref} for operation {op}"

    # 1. Full Question Audit Record
    audit_rec = {
        "sequence": seq,
        "lot_sequence": spec["lot_sequence"],
        "task_identity": ros["task_identity"],
        "stable_id": f"PHYS-WPE-LOT14-Q{seq:02d}",
        "source_id": sid,
        "lot": "LOT-14",
        "paper": ros["paper"],
        "source_type": "EXAM_PAPER_TRANSCRIBED" if stem_raw else "UNBOUND_NSEP_DESCRIPTOR",
        "source_custody": spec["source_custody"],
        "stem_binding": ros["stem_binding"],
        "stem_text": stem_text,
        "stem_sha256": stem_sha,
        "source_hash": source_hash,
        "source_record_digest": source_digest,
        "duplicate_parent": None,
        "scope": "PRIMARY_IN_SCOPE_WPE",
        "key_status": spec["official_key_status"],
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
        "lot_sequence": spec["lot_sequence"],
        "paper": ros["paper"],
        "stem_status": stem_status,
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

    stem_disp = (q['stem_text'][:130] + '...') if q['stem_text'] else "<span class='text-muted'>[STEM UNBOUND IN REGISTRY] Pending independent witness</span>"

    rows_html.append(f"""
    <tr>
        <td class="col-seq">
            <strong>#{q['sequence']}</strong><br>
            <span class="badge badge-lot">LOT-14</span><br>
            <small class="mono">{q['task_identity']}</small><br>
            <small>Lot #{q['lot_sequence']}</small>
        </td>
        <td class="col-source">
            <strong>{q['source_id']}</strong><br>
            <small class="text-muted">{q['paper']}</small><br>
            <span class="badge badge-source">{q['source_custody']}</span>
            <span class="badge badge-fig">{q['figure_status']}</span><br>
            <small>Auth: <strong>{q['key_issuing_authority']}</strong></small>
        </td>
        <td class="col-stem">
            <div class="stem-preview">{stem_disp}</div>
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
    <title>Grade9 v4.0 — Lot 14 Private Review Dashboard (Questions 61–65)</title>
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
            <h1>Grade9 v4.0 — Lot 14 Private Review Dashboard</h1>
            <div class="header-meta">
                Final Five Provisional In-Scope Candidates (Q61–Q65) | Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}<br>
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
            Grade9 v4.0 Academic Platform &bull; Private Review Artifact &bull; Confidential &bull; Lot 14 Concluded
        </footer>
    </div>
</body>
</html>
"""

review_dir = LOT_DIR / "review"
review_dir.mkdir(parents=True, exist_ok=True)
with open(review_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Lot 14 Review Dashboard generated: review/index.html")
