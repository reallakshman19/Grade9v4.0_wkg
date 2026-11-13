"""Adversarial QA root-cause tests; diagnostics never waive the full suite."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_failure_triage import _safe_reference, analyze, format_markdown


def receipt():
    return {
        "schema": "grade9-ci-failure-classification/v1",
        "academic_approval": "HOLD",
        "source_fidelity_waiver": False,
        "pytest_exit_code": 1,
        "mechanical_test_counts": {"passed": 997, "failed": 2, "error": 2, "skipped": 0},
        "unresolved_tests": [
            {"test":"tests.test_bio_environment_resources::test_source_custody",
             "status":"error", "category":"PRIVATE_SOURCE_INPUT_UNAVAILABLE",
             "referenced_inputs":["workspace/sources/bio/BIO-NSEJS-ENV-01/source-custody.json"]},
            {"test":"tests.test_bio_environment_resources::test_bank",
             "status":"error", "category":"GENERATED_OUTPUT_MISSING",
             "referenced_inputs":["workspace/output/bio-environment-resources-r1/bank.json"]},
            {"test":"tests.test_bio_environment_resources::test_qrt",
             "status":"failed", "category":"ASSERTION_DIFFERENCE_NEEDS_REVIEW",
             "referenced_inputs":[]},
            {"test":"tests.test_math_algebra::test_preview_math_count",
             "status":"failed", "category":"ASSERTION_DIFFERENCE_NEEDS_REVIEW",
             "referenced_inputs":[]},
        ]
    }


def test_group_missing_private_and_generated_output_without_false_green(tmp_path):
    r = analyze(receipt(), root=tmp_path)
    assert r["full_qa"] == "FAIL_CLOSED"
    assert r["ready_to_merge_as_full_qa_pass"] is False
    assert r["academic_approval"] == "HOLD"
    assert r["waivers"] is False
    assert r["source_missing_files_observed"] == 1
    assert r["output_missing_files_observed"] == 1
    assert r["observed_missing_file_count"] == 2
    assert r["modules_with_prerequisite_failures"] == 1
    assert r["mechanical_test_counts"] == receipt()["mechanical_test_counts"]
    assert len(r["module_ledger"]) == 2
    assert len(r["unresolved_outside_observed_dependency_modules"]) == 1
    assert "test_preview_math_count" in r["unresolved_outside_observed_dependency_modules"][0]["test"]
    in_scope = [m for m in r["module_ledger"] if "bio_environment" in m["module"]][0]
    assert in_scope["failed"] == 1 and in_scope["error"] == 2
    assert in_scope["additional_unresolved_tests_need_retest"][0]["test"].endswith("test_qrt")
    assert "does not" in r["note"] or "not a complete inventory" in r["note"]


def test_existing_files_do_not_infer_test_success_or_academic_release(tmp_path):
    p = tmp_path / "workspace/sources/bio/BIO-NSEJS-ENV-01/source-custody.json"
    p.parent.mkdir(parents=True)
    p.write_text('{"unverified":true}', encoding="utf-8")
    q = tmp_path / "workspace/output/bio-environment-resources-r1/bank.json"
    q.parent.mkdir(parents=True)
    q.write_text('{"unverified":true}', encoding="utf-8")
    r = analyze(receipt(), root=tmp_path)
    assert r["observed_missing_file_count"] == 0
    assert len(r["referenced_files_that_now_exist"]) == 2
    assert r["full_qa"] == "FAIL_CLOSED"
    assert r["ready_to_merge_as_full_qa_pass"] is False


@pytest.mark.parametrize("bad", [
    "../../workspace/sources/abc",
    "workspace/../../secret/fixture.txt",
    "workspace/sources/../output/forged.json",
    "workspace/sources/",
    "workspace/output/.",
    "workspace/output/a//bank.json",
    "not-workspace/output/a/b",
    "/tmp/workspace/sources/bio/a",
    None,
    5,
])
def test_reject_unsafe_dependency_paths(bad):
    assert _safe_reference(bad) is None


def test_windows_separators_are_normalized_but_not_traversal():
    assert _safe_reference(r"workspace\sources\bio\A\source-custody.json") == (
        "workspace/sources/bio/A/source-custody.json")
    assert _safe_reference(r"workspace\output\..\outside.txt") is None


def test_true_pytest_pass_still_only_mechanical_and_never_academic(tmp_path):
    r = receipt()
    r["pytest_exit_code"] = 0
    r["unresolved_tests"] = []
    r["mechanical_test_counts"] = {"passed":997, "failed":0, "error":0, "skipped":0}
    report = analyze(r, root=tmp_path)
    assert report["full_qa"] == "MECHANICAL_PASS_ONLY"
    assert report["ready_to_merge_as_full_qa_pass"] is True
    assert report["academic_approval"] == "HOLD"


def test_corrupt_count_report_is_fail_closed(tmp_path):
    r = receipt()
    r["unresolved_tests"].pop()
    a = analyze(r, root=tmp_path)
    assert a["full_qa"] == "HOLD_REPORT_COUNT_MISMATCH"
    assert a["ready_to_merge_as_full_qa_pass"] is False


@pytest.mark.parametrize("bad", [
    {},
    {"mechanical_test_counts": {"passed":0, "failed":0, "error":0, "skipped":0}},
    {"mechanical_test_counts": {"passed": 4, "failed": -1,"error":0,"skipped":0},
     "unresolved_tests":[]},
])
def test_missing_invalid_or_negative_count_report_fails_closed(tmp_path,bad):
    assert analyze(bad, root=tmp_path)["full_qa"] == "HOLD_REPORT_MISSING_OR_INVALID"


def test_explicit_skip_never_creates_mechanical_pass(tmp_path):
    r = receipt()
    r["mechanical_test_counts"]={"passed":1,"failed":0,"error":0,"skipped":1}
    r["unresolved_tests"]=[{"test":"tests.fake::test_skip","status":"skipped",
                            "category":"EXPLICIT_SKIP_PRESENT","referenced_inputs":[]}]
    r["pytest_exit_code"]=0
    out=analyze(r, root=tmp_path)
    assert out["full_qa"]=="FAIL_CLOSED"
    assert out["mechanical_test_counts"]["skipped"]==1
    assert out["academic_approval"]=="HOLD"


def test_diagnostic_markdown_names_both_observed_dependencies(tmp_path):
    report=analyze(receipt(),root=tmp_path)
    text=format_markdown(report)
    assert "FULL" not in text or "Full repository" in text
    assert "FAIL_CLOSED" in text
    assert "workspace/sources/bio" in text
    assert "workspace/output/bio" in text
    assert "NOT a successful full-suite test" in text
    assert "independently" in text.lower() or "independent" in text.lower()


def test_cli_diagnostic_success_never_equals_strict_qa_success(tmp_path):
    inp=tmp_path/"full-receipt.json"
    inp.write_text(json.dumps(receipt()),encoding="utf-8")
    root=ROOT/"tools/qa_failure_triage.py"
    args=[sys.executable,str(root),"--json-in",str(inp),
          "--json-out",str(tmp_path/"triage.json"),
          "--markdown-out",str(tmp_path/"triage.md"),
          "--root",str(tmp_path)]
    diag=subprocess.run(args,capture_output=True,text=True,check=False)
    assert diag.returncode==0
    assert "FAIL_CLOSED" in diag.stdout
    assert json.loads((tmp_path/"triage.json").read_text())["full_qa"]=="FAIL_CLOSED"
    strict=subprocess.run(args+["--strict"],capture_output=True,text=True,check=False)
    assert strict.returncode==3


def test_unreadable_cli_receipt_is_explicit_hold(tmp_path):
    args=[sys.executable,str(ROOT/"tools/qa_failure_triage.py"),
          "--json-in",str(tmp_path/"missing.json"),
          "--json-out",str(tmp_path/"triage.json"),
          "--markdown-out",str(tmp_path/"triage.md"),
          "--root",str(tmp_path),"--strict"]
    proc=subprocess.run(args,capture_output=True,text=True,check=False)
    assert proc.returncode==3
    assert json.loads((tmp_path/"triage.json").read_text())["full_qa"] == (
        "HOLD_REPORT_MISSING_OR_INVALID")
