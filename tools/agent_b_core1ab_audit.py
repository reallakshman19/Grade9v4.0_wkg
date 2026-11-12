"""Source-neutral Agent B Core1A/Core1B adversarial audit; never academic approval.

This tool does not edit Agent A's question banks, QRT records or shared runtime.
It deliberately treats structural checks as insufficient for B3/B4/B6 qualification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def _numbers(value: str) -> set[str]:
    return set(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", value))


def _add(findings: list[dict], gate: str, code: str, state: str, reason: str) -> None:
    findings.append({"gate": gate, "code": code, "state": state, "reason": reason})


def audit_module(folder: Path) -> dict:
    """Check candidate evidence only; return bounded FAIL/HOLD findings."""
    findings: list[dict] = []
    data = {}
    for name in ("bank", "core1a_construction", "core1b_reconstruction", "witness"):
        p = folder / (name + ".json")
        if not p.is_file():
            _add(findings, "B7", "NOT_RECEIVED_" + name.upper(), "HOLD", "Candidate file absent.")
            continue
        try:
            data[name] = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError, OSError) as exc:
            _add(findings, "B7", "UNREADABLE_" + name.upper(), "FAIL", type(exc).__name__)

    a = data.get("core1a_construction")
    b = data.get("core1b_reconstruction")
    w = data.get("witness")
    bank = data.get("bank")
    if isinstance(a, dict) and isinstance(b, dict):
        if a.get("construction_id") != b.get("construction_id"):
            _add(findings, "B2", "CONSTRUCTION_ID_MISMATCH", "FAIL", "Core1A and Core1B construction identities differ.")
        if a.get("target_question_id") != b.get("target_question_id"):
            _add(findings, "B2", "SOURCE_UID_MISMATCH", "FAIL", "Core1A and Core1B source UIDs differ.")
        if a.get("academic_status") != "HOLD:ACADEMIC_ADMISSION" or b.get("academic_status") != "HOLD:ACADEMIC_ADMISSION":
            _add(findings, "B7", "ACADEMIC_STATUS_NOT_HELD", "FAIL", "Candidate must not assert academic admission.")
        if not a.get("worked_conceptual_anchor") or not a.get("misconceptions"):
            _add(findings, "B3", "TEACHING_EVIDENCE_INCOMPLETE", "HOLD", "Teaching anchor or misconception repair absent.")
        stages = b.get("stages") or {}
        attempt = stages.get("stage_2_attempt") or {}
        prompt = str(attempt.get("prompt", ""))
        source_id = str(b.get("target_question_id", ""))
        context = str(b.get("fresh_context_ref", ""))
        if not prompt.strip():
            _add(findings, "B4", "FRESH_CHALLENGE_MISSING", "FAIL", "No separate Core1B attempt prompt.")
        if "AUTHENTIC-EXAM" in context.upper() or (context and context == source_id):
            _add(findings, "B4", "SOURCE_AS_FRESH_CONTEXT", "FAIL", "Fresh challenge points to the source examination, not a separate practice identity.")
        if isinstance(bank, dict):
            questions = [q for q in bank.get("questions", []) if isinstance(q, dict) and q.get("id") == source_id]
            if len(questions) != 1:
                _add(findings, "B7", "SOURCE_UID_NOT_UNIQUE", "HOLD", "Cannot bind exactly one source question.")
            else:
                original = str(questions[0].get("stem", ""))
                if original.strip() and prompt.strip() and re.sub(r"\W+", "", original).casefold() == re.sub(r"\W+", "", prompt).casefold():
                    _add(findings, "B4", "VERBATIM_SOURCE_REUSE", "FAIL", "Core1B repeats the source question verbatim.")
                elif len(_numbers(original) & _numbers(prompt) - {"0", "1", "2"}) >= 2:
                    _add(findings, "B4", "SOURCE_PARAMETERS_REUSED", "HOLD", "Source and Core1B share quantitative inputs; human semantic freshness review required.")
        hints = b.get("progressive_hints") or []
        if hints and isinstance(hints[-1], dict):
            h3 = str(hints[-1].get("text", ""))
            result = str(attempt.get("produces", ""))
            values = {v for v in _numbers(result) if "." in v and v not in {"0.0", "1.0"}}
            if any(v in _numbers(h3) for v in values):
                _add(findings, "B4", "H3_NUMERICAL_W_LEAK", "FAIL", "Final-step answer token appears in precommit H3.")
        if not stages.get("stage_4_diagnose") or not stages.get("stage_5_repair") or not stages.get("stage_6_boundary_test"):
            _add(findings, "B6", "DIAGNOSIS_TRANSFER_INCOMPLETE", "HOLD", "Diagnosis, repair or changed-condition transfer missing.")

    journey = folder / "learning_journey.html"
    if not journey.is_file():
        _add(findings, "B5", "RUNTIME_NOT_RECEIVED", "HOLD", "Generated learner journey absent from Git.")
    else:
        page = journey.read_text(encoding="utf-8")
        if 'id="content-core1b"' in page:
            panel = page.split('id="content-core1b"', 1)[1].split('<div class="footer"', 1)[0]
            has_answer = "Stage 3:" in panel or "Stage 3</" in panel
            has_separate_commit = bool(re.search(r"(commit|save)\w*(Core1B|Reconstruction|BAnswer)", page))
            if has_answer and not has_separate_commit:
                _add(findings, "B5", "CORE1B_RECONSTRUCTION_UNGATED", "FAIL",
                     "Stage 3 is static in the Core1B tab, with no Core1B-specific commitment function.")
        if "<iframe" in page.lower():
            _add(findings, "B5", "IFRAME_ROUTE", "FAIL", "Core1B journey uses iframe.")

    if isinstance(w, dict):
        if w.get("review_receipts"):
            _add(findings, "B7", "RECEIPTS_REQUIRE_INDEPENDENT_VERIFICATION", "HOLD", "Untrusted receipts cannot grant academic approval.")
        core1b_receipt = w.get("core1b") or {}
        task_hash = core1b_receipt.get("task_sha256")
        candidate = folder / "core1b_reconstruction.json"
        if task_hash and candidate.is_file():
            digest = "sha256:" + hashlib.sha256(candidate.read_bytes()).hexdigest()
            if task_hash != digest:
                _add(findings, "B2", "CORE1B_HASH_MISMATCH", "FAIL", "Witness binding is stale.")

    for gate in ("B1", "B3", "B4", "B5", "B6", "B7"):
        if not any(f["gate"] == gate for f in findings):
            _add(findings, gate, "INDEPENDENT_EVIDENCE_PENDING", "HOLD",
                 "Presence of fields or a green test is not independent qualification.")
    overall = "FAIL" if any(x["state"] == "FAIL" for x in findings) else "HOLD"
    return {"module": folder.name, "status": overall, "findings": findings}


def audit_tree(root: Path) -> dict:
    modules = sorted({p.parent for p in root.rglob("core1b_reconstruction.json")})
    if not modules:
        return {"status": "HOLD", "modules": [], "reason": "NOT_RECEIVED: no generated Core1B candidate modules"}
    results = [audit_module(p) for p in modules]
    return {"status": "FAIL" if any(x["status"] == "FAIL" for x in results) else "HOLD",
            "modules": results, "count": len(results)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True, help="Private generated candidate tree; read-only")
    p.add_argument("--out", type=Path, help="Optional result JSON; never contains source stems")
    args = p.parse_args()
    outcome = audit_tree(args.root)
    serialized = json.dumps(outcome, sort_keys=True, indent=2)
    if args.out:
        args.out.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 2 if outcome["status"] == "FAIL" else 3  # Never an academic PASS.


if __name__ == "__main__":
    raise SystemExit(main())
