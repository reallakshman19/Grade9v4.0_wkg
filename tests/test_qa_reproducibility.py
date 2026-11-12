"""Diagnostics cannot convert missing academic sources or pytest failures to PASS."""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import json
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_reproducibility import (PUBLIC_GENERATORS, bootstrap, classify,
                                report_from_junit, run_suite)


@pytest.mark.parametrize("message,expected", [
    ("FileNotFoundError: workspace/sources/physics/A/source-custody.json",
     "PRIVATE_SOURCE_INPUT_UNAVAILABLE"),
    ("AssertionError: Missing module HTML: workspace/output/optics/core1a.html",
     "GENERATED_OUTPUT_MISSING"),
    ("ModuleNotFoundError: No module named 'science'",
     "DEPENDENCY_OR_IMPORT_FAILURE"),
    ("AssertionError: assert 0 == 10", "ASSERTION_DIFFERENCE_NEEDS_REVIEW"),
    ("TimeoutExpired('Chromium')", "EXECUTION_TIMEOUT"),
    ("unexpected result", "IMPLEMENTATION_OR_UNKNOWN_FAILURE_NEEDS_REVIEW"),
])
def test_distinct_failure_categories_are_never_waived(message, expected):
    result = classify(message)
    assert result["category"] == expected
    assert result["failure_is_waived"] is False


def make_junit(path: Path, extra: str = "") -> None:
    path.write_text(
        '<testsuite><testcase classname="t" name="ok"/>'
        '<testcase classname="t" name="missing">'
        '<error message="FileNotFoundError: workspace/sources/exam/paper.pdf">'
        'Missing workspace/sources/exam/paper.pdf</error></testcase>' + extra +
        '</testsuite>', encoding="utf-8")


def test_junit_receipt_exposes_both_pass_and_missing_private_source(tmp_path):
    p = tmp_path / "junit.xml"
    make_junit(p)
    data = report_from_junit(p, python_version="3.11.0")
    assert data["mechanical_test_counts"] == {
        "passed": 1, "failed": 0, "error": 1, "skipped": 0}
    assert data["academic_approval"] == "HOLD"
    assert data["unresolved_tests"][0]["category"] == "PRIVATE_SOURCE_INPUT_UNAVAILABLE"
    assert data["unresolved_tests"][0]["failure_is_waived"] is False


def test_full_suite_failure_remains_nonzero_even_if_report_generated(tmp_path):
    p = tmp_path / "junit.xml"
    make_junit(p)
    def runner(command, **_):
        return SimpleNamespace(returncode=1)
    out = tmp_path / "report.json"
    assert run_suite(tmp_path, out, p, ["tests"], runner=runner) == 1
    report = json.loads(out.read_text("utf-8"))
    assert report["pytest_exit_code"] == 1
    assert report["unresolved_tests"]
    assert report["source_fidelity_waiver"] is False


def test_buggy_green_runner_cannot_hide_junit_errors(tmp_path):
    p = tmp_path / "junit.xml"
    make_junit(p)
    assert run_suite(tmp_path, tmp_path / "report.json", p, [],
                     runner=lambda *_a, **_k: SimpleNamespace(returncode=0)) == 3


def test_missing_or_invalid_junit_remains_nonzero(tmp_path):
    out = tmp_path / "report.json"
    assert run_suite(tmp_path, out, tmp_path / "missing.xml", [],
                     runner=lambda *_a, **_k: SimpleNamespace(returncode=0)) == 3
    assert json.loads(out.read_text("utf-8"))["diagnostic_error"] == "JUNIT_REPORT_MISSING"


def test_skips_cannot_create_false_green(tmp_path):
    p = tmp_path / "junit.xml"
    p.write_text('<testsuite><testcase classname="t" name="hidden"><skipped/></testcase></testsuite>',
                 encoding="utf-8")
    assert run_suite(tmp_path, tmp_path / "out.json", p, [],
                     runner=lambda *_a, **_k: SimpleNamespace(returncode=0)) == 3


def test_bootstrap_only_runs_four_checked_in_generators(tmp_path):
    calls = []
    for name in PUBLIC_GENERATORS:
        (tmp_path / name).write_text("# checked in test fixture\n", encoding="utf-8")
    def runner(argv, **kwargs):
        calls.append(argv[-1])
        return SimpleNamespace(returncode=0, stdout="", stderr="")
    result = bootstrap(tmp_path, runner=runner)
    assert calls == list(PUBLIC_GENERATORS)
    assert len(result) == 4


def test_bootstrap_rejects_missing_public_generator(tmp_path):
    with pytest.raises(RuntimeError, match="CHECKED_IN_GENERATOR_MISSING"):
        bootstrap(tmp_path, runner=lambda *_a, **_k: SimpleNamespace(returncode=0))


def test_bootstrap_stops_at_failed_generator(tmp_path):
    for name in PUBLIC_GENERATORS:
        (tmp_path / name).write_text("# synthetic only\n", encoding="utf-8")
    def fails(argv, **kwargs):
        return SimpleNamespace(returncode=4, stdout="", stderr="no source")
    with pytest.raises(RuntimeError, match="PUBLIC_BOOTSTRAP_FAILED"):
        bootstrap(tmp_path, runner=fails)
