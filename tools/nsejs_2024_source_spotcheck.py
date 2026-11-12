#!/usr/bin/env python3
"""Read-only 2024 Code-51 source spot check; NOT an original-exam importer.

Checks a few short publicly observed conceptual anchors and answer-format facts
against generated AUTHORED candidates. Never exports stems, options or figures.
A matching answer key is never considered proof of verbatim source identity.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BUILDER = "build_d3_batch2_modules.py"


def check_bank(root: Path) -> dict:
    """Read generated candidate modules; only emit bounded status codes."""
    cases = []
    for module, question_id in (
        ("bio-immunology-defense-d3-r1", "BIO-NSEJS-2024-B-Q52"),
        ("nsejs-optics-displacement-d3-r1", "PHYS-NSEJS-2024-P-Q57"),
        ("chem-electronic-structure-d3-r1", "CHEM-NSEJS-2024-C-Q56"),
    ):
        path = root / module / "bank.json"
        if not path.is_file():
            cases.append({"candidate_id": question_id,
                          "status": "NOT_RECEIVED", "findings": ["CANDIDATE_BANK_NOT_RECEIVED"]})
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            candidates = [q for q in raw["questions"] if isinstance(q, dict) and q.get("id") == question_id]
        except (OSError, ValueError, TypeError, KeyError):
            candidates = []
        if len(candidates) != 1:
            cases.append({"candidate_id": question_id, "status": "HOLD",
                          "findings": ["CANDIDATE_ID_NOT_UNIQUE_OR_INVALID"]})
            continue
        q = candidates[0]
        opts = {str(o.get("id", "")).upper(): str(o.get("text", ""))
                for o in q.get("options", []) if isinstance(o, dict)}
        findings = []
        if sorted(opts) != ["A", "B", "C", "D"]:
            findings.append("OPTIONS_NOT_A_THROUGH_D")
        submitted = set(str(q.get("correct_option", "")).replace(" ", "").split(","))
        expected = {
            "BIO-NSEJS-2024-B-Q52": {"A", "C", "D"},
            "PHYS-NSEJS-2024-P-Q57": {"A", "B", "C", "D"},
            "CHEM-NSEJS-2024-C-Q56": {"A", "B", "C"},
        }[question_id]
        if submitted != expected:
            findings.append("IAPT_CODE_51_ANSWER_LETTERS_DIFFER")
        if question_id.endswith("B-Q52"):
            if (q.get("original_exam_question") is not False or
                q.get("source_claim_status") != "KNOWN_NON_VERBATIM_AUTHORED_ADAPTATION" or
                q.get("exam_source_admission") != "HOLD_P0_Q52_OPTIONS_SUBSTITUTED"):
                findings.append("P0_SOURCE_CONTRADICTION_NOT_QUARANTINED")
            original_d = opts.get("D", "").lower()
            original_b = opts.get("B", "").lower()
            if not ("igm" in original_d and "igd" in original_d
                    and ("b cell" in original_d or "b-cell" in original_d)):
                findings.append("P0_Q52_OPTION_D_SUBSTITUTED_FOR_ORIGINAL")
            if not ("eosinophil" in original_b and "polymorphonuclear" in original_b):
                findings.append("P0_Q52_OPTION_B_SOURCE_WORDED_DIFFERENTLY")
        elif question_id.endswith("P-Q57"):
            stem = str(q.get("stem", "")).lower()
            if "75 cm" not in stem or "12 cm" not in stem:
                findings.append("Q57_ORIGINAL_NUMERIC_ANCHORS_DIFFER")
            # Numeric anchors alone do not authenticate the original figure.
            # The official paper PDF was hashed in CI, but its optical
            # diagram has not been reproduced as an authenticated source figure.
            if not q.get("source_figures"):
                findings.append("Q57_ORIGINAL_SOURCE_FIGURE_NOT_STAGED")
            findings.append("Q57_CANDIDATE_FIGURE_FIDELITY_NOT_VERIFIED")
        else:
            findings.append("Q56_ORIGINAL_STEM_OPTIONS_NOT_FULLY_ATTESTED")
        if findings and any(x.startswith(("P0_", "OPTIONS_NOT_", "IAPT_", "Q57_ORIGINAL_NUMERIC"))
                            for x in findings):
            status = "SOURCE_CONFLICT_HOLD"
        else:
            status = "BOUNDED_MATCH_ONLY_SOURCE_HOLD"
        cases.append({"candidate_id": question_id, "status": status,
                      "findings": sorted(set(findings)),
                      "key_letters_matched": submitted == expected,
                      "academic_admission": "HOLD"})
    custody_manifest = ROOT / "docs/nsejs/official-2024-code51-raw-byte-custody-r1.json"
    official_hash = None
    if custody_manifest.is_file():
        try:
            meta = json.loads(custody_manifest.read_text(encoding="utf-8"))
            paper = next(d for d in meta.get("documents", [])
                         if d.get("id") == "IAPT_NSEJS_2024_PAPER_CODE51")
            if paper.get("raw_byte_retrieval_status") == "VERIFIED_BY_EXACT_HEAD_CI":
                official_hash = paper.get("sha256")
        except (OSError, ValueError, StopIteration):
            pass
    return {
        "schema": "grade9-nsejs-2024-code51-spotcheck/v1",
        "official_paper_code": 51,
        "official_paper_raw_sha256_verified": official_hash,
        "evidence_note": "IAPT 2024 Code-51 paper & final key visually/textually inspected; raw PDF bytes not imported",
        "code51_q20": "DROP",
        "code51_a2_format": "MULTIPLE_CORRECT",
        "all_cases_source_admitted": False,
        "source_rights": "NOT_REVIEWED",
        "cases": cases,
    }


def generate_and_audit(repo: Path = ROOT) -> dict:
    with tempfile.TemporaryDirectory(prefix="nsejs_2024_source_check_") as temp:
        root = Path(temp)
        env = dict(os.environ)
        env["PYTHONPATH"] = str(repo) + os.pathsep + env.get("PYTHONPATH", "")
        builder_copy = root / BUILDER
        shutil.copyfile(repo / BUILDER, builder_copy)
        p = subprocess.run([sys.executable, str(builder_copy)], cwd=root,
                           env=env, capture_output=True, text=True, timeout=90)
        if p.returncode != 0:
            return {"schema": "grade9-nsejs-2024-code51-spotcheck/v1",
                    "status": "BUILDER_FAILED_HOLD", "cases": [], "academic_admission": "HOLD",
                    "build_exit_code": p.returncode}
        return check_bank(root / "workspace" / "output")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--require-no-source-conflicts", action="store_true",
                   help="Exit 5 on a known conflict; does not grant academic PASS even if none")
    args = p.parse_args(argv)
    result = generate_and_audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    conflicts = [x for x in result["cases"] if x["status"] == "SOURCE_CONFLICT_HOLD"]
    print(f"NSEJS_CODE51_SOURCE_HOLD: {len(conflicts)} bounded source conflicts; "
          f"{len(result['cases'])} candidate items checked; report={args.out}")
    if args.require_no_source_conflicts and (conflicts or not result["cases"]):
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
