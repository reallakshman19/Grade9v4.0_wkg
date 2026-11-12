#!/usr/bin/env python3
"""Reproducible public bootstrap + honest full-suite pytest classification.

Never fabricates private examination sources, suppresses tests or converts a
nonzero pytest run to a successful gate. The JSON report is diagnostic ONLY;
academic admission stays HOLD even if all public mechanical checks pass.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_GENERATORS = (
    "build_d3_batch2_modules.py",
    "build_d3_expansion_modules.py",
    "build_physics_fluids_core1.py",
    "build_bio_genetics_core1.py",
)
INPUT_MATCH = re.compile(r"(?:workspace[/\\](?:sources|output)[/\\][^\s'\"<>)]+)")


def bootstrap(root: Path = ROOT, runner=None) -> list[dict]:
    """Run only existing, checked-in public generators in deterministic order."""
    runner = runner or subprocess.run
    results = []
    for filename in PUBLIC_GENERATORS:
        script = root / filename
        if not script.is_file() or not script.resolve().is_relative_to(root.resolve()):
            raise RuntimeError("CHECKED_IN_GENERATOR_MISSING:" + filename)
        result = runner([sys.executable, filename], cwd=root, check=False,
                        capture_output=True, text=True)
        record = {"generator": filename, "exit_code": result.returncode}
        results.append(record)
        if result.returncode:
            raise RuntimeError("PUBLIC_BOOTSTRAP_FAILED:" + filename +
                               ":exit=" + str(result.returncode) +
                               ":" + (result.stderr or result.stdout)[-1000:])
    return results


def classify(message: str) -> dict:
    """Conservative diagnostic, not a waiver for any test outcome."""
    text = message.replace("\\", "/")
    inputs = sorted(set(m.group(0).rstrip(".,:;") for m in INPUT_MATCH.finditer(text)))
    private_inputs = [p for p in inputs if p.startswith("workspace/sources/")]
    output_inputs = [p for p in inputs if p.startswith("workspace/output/")]
    if private_inputs or "source-custody.json" in text and "No such file" in text:
        category = "PRIVATE_SOURCE_INPUT_UNAVAILABLE"
    elif output_inputs or "Missing module HTML:" in text or "Missing bank file:" in text:
        category = "GENERATED_OUTPUT_MISSING"
    elif "ModuleNotFoundError" in text or "ImportError" in text:
        category = "DEPENDENCY_OR_IMPORT_FAILURE"
    elif "AssertionError" in text or "assert " in text:
        category = "ASSERTION_DIFFERENCE_NEEDS_REVIEW"
    elif "TimeoutError" in text or "TimeoutExpired" in text:
        category = "EXECUTION_TIMEOUT"
    else:
        category = "IMPLEMENTATION_OR_UNKNOWN_FAILURE_NEEDS_REVIEW"
    return {"category": category, "referenced_inputs": inputs,
            "possible_stale_assertion": category == "ASSERTION_DIFFERENCE_NEEDS_REVIEW",
            "failure_is_waived": False}


def report_from_junit(path: Path, *, python_version: str | None = None) -> dict:
    if not path.is_file():
        raise RuntimeError("JUNIT_REPORT_MISSING")
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise RuntimeError("JUNIT_REPORT_CORRUPT") from exc
    nodes = tree.findall(".//testcase")
    if not nodes:
        raise RuntimeError("JUNIT_HAS_NO_TESTCASES")
    outcomes, counts = [], {"passed": 0, "failed": 0, "error": 0, "skipped": 0}
    for node in nodes:
        marker = next((n for n in ("failure", "error", "skipped")
                       if node.find(n) is not None), None)
        status = {"failure": "failed", "error": "error", "skipped": "skipped",
                  None: "passed"}[marker]
        counts[status] += 1
        if status != "passed":
            failure = node.find(marker)
            detail = ((failure.get("message") or "") + "\n" +
                      (failure.text or "")) if failure is not None else ""
            row = {"test": node.get("classname", "") + "::" + node.get("name", ""),
                   "status": status, "message": detail[:6000]}
            row.update(classify(detail) if marker != "skipped"
                       else {"category": "EXPLICIT_SKIP_PRESENT",
                             "referenced_inputs": [], "failure_is_waived": False})
            outcomes.append(row)
    return {"schema": "grade9-ci-failure-classification/v1",
            "python_version": python_version or sys.version.split()[0],
            "mechanical_test_counts": counts,
            "all_tests_executed": counts["skipped"] == 0,
            "academic_approval": "HOLD",
            "source_fidelity_waiver": False,
            "unresolved_tests": outcomes}


def run_suite(root: Path, output: Path, junit: Path, pytest_args: list[str],
              runner=None) -> int:
    runner = runner or subprocess.run
    output.parent.mkdir(parents=True, exist_ok=True)
    junit.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-m", "pytest", "-q", "--junitxml", str(junit)]
    command += pytest_args or ["tests"]
    result = runner(command, cwd=root, check=False)
    try:
        report = report_from_junit(junit)
    except RuntimeError as exc:
        report = {"schema": "grade9-ci-failure-classification/v1",
                  "academic_approval": "HOLD",
                  "source_fidelity_waiver": False,
                  "diagnostic_error": str(exc),
                  "unresolved_tests": []}
    report["pytest_exit_code"] = result.returncode
    report["command"] = command
    report["clean_checkout_claim"] = "REQUIRES_CI_RECEIPT"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    failures = report.get("mechanical_test_counts", {}).get("failed", 0)
    errors = report.get("mechanical_test_counts", {}).get("error", 0)
    skipped = report.get("mechanical_test_counts", {}).get("skipped", 0)
    if result.returncode != 0:
        return result.returncode
    # Avoid false green if a buggy runner returned success despite report problems.
    if report.get("diagnostic_error") or failures or errors or skipped:
        return 3
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap")
    run = sub.add_parser("run")
    run.add_argument("--json-out", type=Path, required=True)
    run.add_argument("--junit-out", type=Path, required=True)
    run.add_argument("pytest_args", nargs="*")
    args = ap.parse_args()
    if args.command == "bootstrap":
        for item in bootstrap():
            print("PUBLIC_GENERATOR_PASS", item["generator"])
        return 0
    return run_suite(ROOT, args.json_out, args.junit_out, args.pytest_args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as exc:
        print("REPRODUCIBILITY_GATE_FAILED:", exc, file=sys.stderr)
        sys.exit(2)
