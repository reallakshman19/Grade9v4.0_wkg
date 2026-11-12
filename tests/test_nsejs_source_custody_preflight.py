"""Adversarial tests for source-neutral NSEJS custody inventory.

Synthetic text below is test fixture data, never real exam content.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("nsejs_source_custody_preflight",
                                              ROOT / "tools/nsejs_source_custody_preflight.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def candidate_row(count=1):
    return {
        "year": "2024", "subject": "PHYSICS",
        "author_test_declared_count": str(count),
        "bank_expected_path": "workspace/output/nsejs-2024-physics-r1/bank.json",
        "source_root_expected": "workspace/sources/nsejs",
    }


def build_synthetic(tmp_path, items):
    bank_dir = tmp_path / "workspace/output/nsejs-2024-physics-r1"
    bank_dir.mkdir(parents=True, exist_ok=True)
    for name in audit.OUTPUT_FILES:
        (bank_dir / name).write_text("{}", encoding="utf-8")
    (bank_dir / "bank.json").write_text(json.dumps({"questions": items}), encoding="utf-8")
    source_root = tmp_path / "workspace/sources/nsejs"
    source_root.mkdir(parents=True, exist_ok=True)
    for q in items:
        qid = q["id"]
        if not audit.SAFE_ID.fullmatch(qid):
            continue
        path = source_root / qid
        path.mkdir(exist_ok=True)
        (path / "source_item.json").write_text(json.dumps({"source_item_locator": qid}), encoding="utf-8")
        (path / "source-custody.json").write_text(json.dumps({
            "source_item_locator": qid,
            "comparison_status": "ORIGINAL_EXACT",
            "custody_mode": "EMBEDDED_VERBATIM",
        }), encoding="utf-8")


def test_main_manifest_is_15_author_claim_groups_not_official_coverage():
    rows = audit.load_manifest()
    assert len(rows) == 15
    assert sum(int(r["author_test_declared_count"]) for r in rows) == 237
    assert {r["subject"] for r in rows} == {"PHYSICS", "CHEMISTRY", "BIOLOGY"}


def test_missing_clean_checkout_files_fail_closed(tmp_path):
    data = audit.inspect_row(tmp_path, candidate_row())
    assert data["status"] == "INPUT_CUSTODY_HOLD"
    assert len(data["missing_output_files"]) == len(audit.OUTPUT_FILES)
    assert "SOURCE_ROOT_NOT_RECEIVED" in data["flags"]
    assert data["academic_admission"] == "HOLD"


def test_self_declared_exact_source_never_becomes_verified(tmp_path):
    build_synthetic(tmp_path, [{"id":"NSEJS-2024-P-Q01","stem":"PRIVATE EXAM-LOOKALIKE DATA"}])
    data = audit.inspect_row(tmp_path, candidate_row())
    assert data["status"] == "STRUCTURE_PRESENT_NOT_ACADEMICALLY_VERIFIED"
    assert data["source_authenticity"] == "NOT_INDEPENDENTLY_VERIFIED"
    assert "ORIGINAL_EXACT_DECLARATION_NOT_INDEPENDENT_PROOF" in data["flags"]
    assert "PRIVATE" not in json.dumps(data)


def test_bank_missing_source_item_is_hold(tmp_path):
    build_synthetic(tmp_path, [{"id":"NSEJS-2024-P-Q01"}])
    (tmp_path / "workspace/sources/nsejs/NSEJS-2024-P-Q01/source_item.json").unlink()
    data = audit.inspect_row(tmp_path, candidate_row())
    assert data["status"] == "INPUT_CUSTODY_HOLD"
    assert data["missing_source_files"][0]["source_id"] == "NSEJS-2024-P-Q01"


def test_path_traversal_and_cross_subject_id_rejected(tmp_path):
    build_synthetic(tmp_path, [{"id":"../private"}])
    data = audit.inspect_row(tmp_path, candidate_row())
    assert "BANK_QUESTION_ID_INVALID" in data["flags"]
    assert data["status"] == "INPUT_CUSTODY_HOLD"
    build_synthetic(tmp_path, [{"id":"NSEJS-2024-C-Q01"}])
    data = audit.inspect_row(tmp_path, candidate_row())
    assert "BANK_YEAR_SUBJECT_MISMATCH" in data["flags"]


def test_duplicate_question_ids_do_not_count_as_complete(tmp_path):
    build_synthetic(tmp_path, [{"id":"NSEJS-2024-P-Q01"}, {"id":"NSEJS-2024-P-Q01"}])
    data = audit.inspect_row(tmp_path, candidate_row(count=2))
    assert "BANK_DUPLICATE_QUESTION_ID" in data["flags"]
    assert data["status"] == "INPUT_CUSTODY_HOLD"


def test_author_counts_not_relabelled_academic_admission():
    result = audit.audit()
    assert result["author_test_expected_by_subject"] == {
        "PHYSICS": 79, "CHEMISTRY": 79, "BIOLOGY": 79,
    }
    assert result["subject_year_rows"] == 15
    assert result["academic_admission"] == result["qrt_adjudication"] == "HOLD"
    assert "SEPARATE_UNRECONCILED" in result["public_physics_50"]


def test_cli_strict_missing_returns_three_and_academic_gate_four(tmp_path):
    # Use the real metadata manifest, but a synthetic empty private-input root.
    dest = tmp_path / "docs/nsejs"
    dest.mkdir(parents=True)
    (dest / "subject-year-source-availability-r1.csv").write_bytes(
        (ROOT / audit.MANIFEST).read_bytes()
    )
    (dest / "official-iapt-source-locators-r1.json").write_bytes(
        (ROOT / audit.OFFICIAL_LOCATORS).read_bytes()
    )
    path = tmp_path / "receipt.json"
    status = audit.main(["--root", str(tmp_path), "--json-out", str(path), "--require-files"])
    assert status == 3 and path.is_file()
    result = json.loads(path.read_text(encoding="utf-8"))
    assert result["missing_or_invalid_subject_year_bundles"] == 15
    assert audit.main(["--root", str(tmp_path), "--academic-gate"]) == 4



def test_official_year_series_and_source_links_are_recorded_not_imported():
    data = audit.load_official_locators()
    years = {row["year"]: row for row in data["years"]}
    assert len(years) == 5
    assert years[2020]["exam_series"] == "IOQJS_2020_21_PART_I"
    assert years[2021]["exam_series"] == "IOQJS_2021_22_PART_I"
    assert years[2020]["official_paper_url"] is None
    assert all(not row["source_bytes_imported"] for row in years.values())
    assert all(not row["independently_authenticated"] for row in years.values())


def test_iapt_2024_paper_code_51_drop_and_multiple_correct_preserved():
    years = {row["year"]: row for row in audit.load_official_locators()["years"]}
    paper = years[2024]
    assert paper["paper_code"] == 51
    assert paper["known_final_key_exception"] == {
        "question": 20, "paper_code": 51, "status": "DROP"
    }
    assert paper["part_A2_range"] == [49, 60]
    assert paper["part_A2_format"] == "MULTIPLE_CORRECT"


def test_untrusted_source_locator_metadata_fails_validation(tmp_path):
    source = audit.load_official_locators()
    p = tmp_path / audit.OFFICIAL_LOCATORS
    p.parent.mkdir(parents=True)
    broken = json.loads(json.dumps(source))
    broken["years"][0]["official_archive_url"] = "https://attacker.example/source.pdf"
    p.write_text(json.dumps(broken), encoding="utf-8")
    with pytest.raises(ValueError, match="Non-IAPT"):
        audit.load_official_locators(tmp_path)
    broken["years"][0] = source["years"][0]
    broken["years"][4]["known_final_key_exception"] = {"question": 20, "paper_code": 51, "status": "A"}
    p.write_text(json.dumps(broken), encoding="utf-8")
    with pytest.raises(ValueError, match="Code 51"):
        audit.load_official_locators(tmp_path)


def test_located_official_urls_do_not_clear_missing_native_custody():
    report = audit.audit()
    assert report["official_archive_years_located"] == 5
    assert report["official_paper_url_years_located"] == 4
    assert report["official_final_key_url_years_located"] == 5
    assert report["locators_are_source_custody"] is False
    assert report["missing_or_invalid_subject_year_bundles"] == 15
    assert report["academic_admission"] == "HOLD"
    for row in report["rows"]:
        assert row["official_archive_url"].startswith("https://iapt.org.in/")
        assert row["official_locator_status"].endswith("_NOT_IMPORTED") or row["official_locator_status"].endswith("_NOT_LOCATED")
        if row["year"] == 2024:
            assert "IAPT_CODE_51_QUESTION_20_DROPPED" in row["flags"]
            assert "IAPT_CODE_51_QUESTIONS_49_60_MULTI_CORRECT" in row["flags"]
