#!/usr/bin/env python3
"""Diagnose a STRICT full-repository pytest receipt without waiving any tests.

A clean public checkout cannot regenerate original exam/source-custody records
from unrelated authored modules. This reporter groups the root prerequisites
behind the missing workspace files, but never changes pytest's exit code or
claims that an unresolved test passed. It reads only path metadata, not the
contents of private examination sources.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

PREREQUISITES = frozenset({
    "PRIVATE_SOURCE_INPUT_UNAVAILABLE",
    "GENERATED_OUTPUT_MISSING",
})
COUNT_KEYS = ("passed", "failed", "error", "skipped")


def _safe_reference(value: object) -> str | None:
    """Return only a workspace-relative, non-traversing dependency path."""
    if not isinstance(value, str):
        return None
    path = value.strip().replace("\\", "/").rstrip(".,:;")
    parts = path.split("/")
    if (len(parts) < 3 or parts[0] != "workspace"
        or parts[1] not in {"sources", "output"}
        or any(part in {"", ".", ".."} for part in parts)
        or "\x00" in path):
        return None
    return path


def analyze(report: dict, *, root: Path) -> dict:
    """Emit actionable prerequisite clusters while preserving the true FAIL.

    A failure from the same test module as a missing private source may be
    downstream, but is NOT classified as fixed; it needs a fresh full rerun.
    """
    counts = report.get("mechanical_test_counts")
    unresolved = report.get("unresolved_tests")
    usable = (isinstance(counts, dict) and
              all(type(counts.get(key)) is int and counts[key] >= 0
                  for key in COUNT_KEYS) and
              isinstance(unresolved, list))
    if not usable:
        return {"schema": "grade9-python-qa-prerequisites/v1",
                "full_qa": "HOLD_REPORT_MISSING_OR_INVALID",
                "academic_approval": "HOLD", "waivers": False,
                "diagnostic_error": report.get("diagnostic_error", "INCOMPLETE_QA_REPORT"),
                "ready_to_merge_as_full_qa_pass": False}
    if len(unresolved) != sum(counts[key] for key in ("failed", "error", "skipped")):
        return {"schema": "grade9-python-qa-prerequisites/v1",
                "full_qa": "HOLD_REPORT_COUNT_MISMATCH",
                "academic_approval": "HOLD", "waivers": False,
                "diagnostic_error": "JUNIT_CASE_COUNTS_DO_NOT_MATCH_UNRESOLVED",
                "ready_to_merge_as_full_qa_pass": False,
                "mechanical_test_counts": counts}
    modules: dict[str, dict] = {}
    inputs: dict[str, dict] = {}
    for row in unresolved:
        if not isinstance(row, dict):
            continue
        name = row.get("test", "")
        module = name.split("::")[0] if isinstance(name, str) else "UNRECOGNIZED_TEST"
        record = modules.setdefault(module, {
            "module": module, "failed": 0, "error": 0, "skipped": 0,
            "source_dependencies": set(), "output_dependencies": set(),
            "other_unresolved_tests": [],
        })
        status = row.get("status")
        if status in ("failed", "error", "skipped"):
            record[status] += 1
        category = row.get("category")
        refs = row.get("referenced_inputs", [])
        if not isinstance(refs, list):
            refs = []
        found = []
        for raw in refs:
            p = _safe_reference(raw)
            if p is None:
                continue
            found.append(p)
            kind = "PRIVATE_SOURCE" if p.startswith("workspace/sources/") else "GENERATED_OUTPUT"
            if p not in inputs:
                local = root / p
                inputs[p] = {"path": p, "kind": kind, "present": local.is_file(),
                             "required_by": set()}
            inputs[p]["required_by"].add(module)
            record["source_dependencies" if kind == "PRIVATE_SOURCE"
                   else "output_dependencies"].add(p)
        # This flag is conservative: an assertion may be a genuine regression,
        # even when a different test in the module also lacks private files.
        if category not in PREREQUISITES or not found:
            record["other_unresolved_tests"].append({
                "test": name, "category": category or "UNCLASSIFIED",
                "status": status,
            })
    # Only files that a failing/erroring test *actually referenced* are
    # recorded. Never imply this is the complete private dataset inventory.
    broken = sorted(inputs.values(), key=lambda x: x["path"])
    missing = [{**row, "required_by": sorted(row["required_by"])}
               for row in broken if not row["present"]]
    present = [{**row, "required_by": sorted(row["required_by"])}
               for row in broken if row["present"]]
    ordered = []
    dependent_modules = 0
    independent = []
    for name, record in sorted(modules.items()):
        dependency_bound = bool(record["source_dependencies"] or
                                record["output_dependencies"])
        if dependency_bound:
            dependent_modules += 1
        else:
            independent.extend(record["other_unresolved_tests"])
        ordered.append({
            "module": name, "failed": record["failed"],
            "error": record["error"], "skipped": record["skipped"],
            "prerequisite_status":
                "SOURCE_OR_OUTPUT_RESTORE_REQUIRED" if dependency_bound
                else "UNCLASSIFIED_REQUIRES_INVESTIGATION",
            "referenced_sources": sorted(record["source_dependencies"]),
            "referenced_outputs": sorted(record["output_dependencies"]),
            "additional_unresolved_tests_need_retest": record["other_unresolved_tests"],
        })
    fully_passed = (not any(counts[k] for k in ("failed", "error", "skipped"))
                    and report.get("pytest_exit_code") == 0
                    and not report.get("diagnostic_error"))
    return {
        "schema": "grade9-python-qa-prerequisites/v1",
        "full_qa": "MECHANICAL_PASS_ONLY" if fully_passed else "FAIL_CLOSED",
        "academic_approval": "HOLD", "waivers": False,
        "ready_to_merge_as_full_qa_pass": fully_passed,
        "pytest_exit_code": report.get("pytest_exit_code"),
        "mechanical_test_counts": counts,
        "source_missing_files_observed": sum(x["kind"] == "PRIVATE_SOURCE" for x in missing),
        "output_missing_files_observed": sum(x["kind"] == "GENERATED_OUTPUT" for x in missing),
        "observed_missing_file_count": len(missing),
        "note": ("Observed missing paths are lower-bound evidence from failed tests, "
                 "not a complete inventory or a substitute for authentic custody."),
        "missing_references": missing,
        "referenced_files_that_now_exist": present,
        "modules_with_prerequisite_failures": dependent_modules,
        "module_ledger": ordered,
        "unresolved_outside_observed_dependency_modules": independent,
        "next_actions": [
            "Recover authorized private workspace/sources with source-custody evidence; do not fabricate or commit private exam material.",
            "Regenerate workspace/output using the real source-bound builders; do not substitute unrelated public authored fixtures.",
            "Rerun the entire unfiltered Python 3.11 and 3.12 suite before claiming QA success.",
            "Independently investigate residual assertions and academic QRT HOLDs; software PASS does not constitute source or science approval.",
        ],
    }


def format_markdown(analysis: dict) -> str:
    counts = analysis.get("mechanical_test_counts", {})
    lines = [
        "# Full repository Python QA — source dependency receipt",
        "",
        "**Full QA:** " + analysis["full_qa"],
        "**Academic approval:** HOLD (separate from all software tests)",
        "**Waivers/skips introduced:** NONE",
        "",
        "Counts: " + " · ".join(
            f"{key}: {counts.get(key, 'unknown')}" for key in COUNT_KEYS),
        f"Distinct missing source paths OBSERVED: {analysis.get('source_missing_files_observed', 'unknown')}",
        f"Distinct missing generated-output paths OBSERVED: {analysis.get('output_missing_files_observed', 'unknown')}",
        f"Modules with observed missing inputs: {analysis.get('modules_with_prerequisite_failures', 'unknown')}",
        "",
        "This is a dependency diagnostic, NOT a successful full-suite test.",
        "Observed paths are a lower bound; re-run after authorized restoration.",
        "",
        "## Missing workspace paths actually observed",
    ]
    for row in analysis.get("missing_references", []):
        lines.append(f"- `{row['path']}` — {row['kind']} "
                     f"(seen in {len(row['required_by'])} test module(s))")
    lines.extend(["", "## Unresolved tests outside observed dependency modules"])
    for row in analysis.get("unresolved_outside_observed_dependency_modules", []):
        lines.append(f"- {row['test']}: {row['category']}")
    lines.extend(["", "## Remediation without false QA green"])
    for i, item in enumerate(analysis.get("next_actions", []), 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-in", type=Path, required=True)
    ap.add_argument("--json-out", type=Path, required=True)
    ap.add_argument("--markdown-out", type=Path, required=True)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--strict", action="store_true",
                    help="Exit nonzero unless the FULL unfiltered suite passed.")
    args = ap.parse_args()
    try:
        source = json.loads(args.json_in.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        source = {"diagnostic_error": "UNREADABLE_FULL_QA_RECEIPT:" + str(exc)}
    result = analyze(source, root=args.root.resolve())
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_out.write_text(format_markdown(result), encoding="utf-8")
    print("QA_DEPENDENCY_DIAGNOSTIC:", result["full_qa"],
          "source_missing:", result.get("source_missing_files_observed", "?"),
          "output_missing:", result.get("output_missing_files_observed", "?"),
          "academic:HOLD")
    if args.strict and not result["ready_to_merge_as_full_qa_pass"]:
        return 3
    return 0  # Diagnostic completed; NEVER call this QA PASS.


if __name__ == "__main__":
    sys.exit(main())
