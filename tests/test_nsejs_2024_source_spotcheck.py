"""Bounded original-source negative controls for IAPT 2024 Code 51."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("nsejs_2024_source_spotcheck",
                                              ROOT / "tools/nsejs_2024_source_spotcheck.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def test_original_key_letters_can_match_while_question_source_is_substituted():
    result = audit.generate_and_audit()
    by_id = {x["candidate_id"]: x for x in result["cases"]}
    assert len(by_id) == 3
    q52 = by_id["BIO-NSEJS-2024-B-Q52"]
    assert q52["key_letters_matched"] is True
    assert q52["status"] == "SOURCE_CONFLICT_HOLD"
    assert "P0_Q52_OPTION_D_SUBSTITUTED_FOR_ORIGINAL" in q52["findings"]
    assert "P0_Q52_OPTION_B_SOURCE_WORDED_DIFFERENTLY" in q52["findings"]
    assert q52["academic_admission"] == "HOLD"


def test_bounded_lens_and_scandium_checks_do_not_authenticate_original_paper():
    result = audit.generate_and_audit()
    by_id = {x["candidate_id"]: x for x in result["cases"]}
    q57 = by_id["PHYS-NSEJS-2024-P-Q57"]
    assert q57["key_letters_matched"] is True
    assert q57["status"] == "BOUNDED_MATCH_ONLY_SOURCE_HOLD"
    assert "Q57_CANDIDATE_FIGURE_FIDELITY_NOT_VERIFIED" in q57["findings"]
    assert "Q57_ORIGINAL_SOURCE_FIGURE_NOT_STAGED" in q57["findings"]
    assert result["official_paper_raw_sha256_verified"] == (
        "b80e3bae4e64aaad11f43cc12f07ef17ae495b75e231122d440b0f81709379e8"
    )
    q56 = by_id["CHEM-NSEJS-2024-C-Q56"]
    assert q56["key_letters_matched"] is True
    assert q56["academic_admission"] == "HOLD"
    assert result["all_cases_source_admitted"] is False


def test_source_spotcheck_report_contains_no_original_question_text(tmp_path):
    path = tmp_path / "spotcheck.json"
    rc = audit.main(["--out", str(path)])
    assert rc == 0
    text = path.read_text(encoding="utf-8")
    assert "stem" not in text
    assert '"options"' not in text
    assert '"correct_option"' not in text
    assert '"key_letters_matched"' in text
    assert "SOURCE_CONFLICT_HOLD" in text
    assert audit.main(["--out", str(path), "--require-no-source-conflicts"]) == 5
