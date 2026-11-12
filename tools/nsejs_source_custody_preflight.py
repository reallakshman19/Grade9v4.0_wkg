#!/usr/bin/env python3
"""Strict, source-neutral NSEJS custody inventory. Never generates exam questions.

The CSV contains author TEST EXPECTATIONS, not independently admitted exam counts.
Never promote a claimed ORIGINAL_EXACT status to academic approval.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs/nsejs/subject-year-source-availability-r1.csv")
SOURCE_FILES = ("source_item.json", "source-custody.json")
OUTPUT_FILES = ("bank.json", "intake.json", "sl1_check_report.json",
                "sl2_check_report.json", "core2_module.html")
YEARS = range(2020, 2025)
SUBJECTS = ("PHYSICS", "CHEMISTRY", "BIOLOGY")
SUBJECT_CODES = {"PHYSICS": "P", "CHEMISTRY": "C", "BIOLOGY": "B"}
SAFE_ID = re.compile(r"^NSEJS-\d{4}-[PCB]-Q\d{2}$")
REQUIRED_FIELDS = ("year", "subject", "author_test_declared_count",
                   "bank_expected_path", "source_root_expected")
OFFICIAL_LOCATORS = Path("docs/nsejs/official-iapt-source-locators-r1.json")


def load_manifest(root: Path = ROOT, manifest: Path = MANIFEST) -> list[dict]:
    with (root / manifest).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not set(REQUIRED_FIELDS).issubset(reader.fieldnames or []):
            raise ValueError("Manifest columns missing")
        rows = list(reader)
    keys = [(row["year"], row["subject"]) for row in rows]
    expected = {(str(year), subject) for year in YEARS for subject in SUBJECTS}
    if len(rows) != 15 or set(keys) != expected or len(set(keys)) != 15:
        raise ValueError("Expected 15 unique 2020-2024 subject-year rows")
    for row in rows:
        year, subject = row["year"], row["subject"]
        if not row["author_test_declared_count"].isdigit():
            raise ValueError("Non-numeric author test count")
        expected_bank = f"workspace/output/nsejs-{year}-{subject.lower()}-r1/bank.json"
        source_root = {"PHYSICS": "workspace/sources/nsejs",
                       "CHEMISTRY": "workspace/sources/chem",
                       "BIOLOGY": "workspace/sources/bio"}[subject]
        if row["bank_expected_path"] != expected_bank or row["source_root_expected"] != source_root:
            raise ValueError("Unexpected bank/source path "+year+"/"+subject)
    return sorted(rows, key=lambda r: (int(r["year"]), r["subject"]))


def json_object(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, ValueError):
        return None


def inspect_row(root: Path, row: dict) -> dict:
    """Only path/structural metadata, never original stems/answers/figures."""
    bank_path = Path(row["bank_expected_path"])
    bank_dir = root / bank_path.parent
    source_root = root / row["source_root_expected"]
    declared = int(row["author_test_declared_count"])
    missing_outputs = [name for name in OUTPUT_FILES if not (bank_dir / name).is_file()]
    flags = ["GENERATED_OUTPUT_NOT_RECEIVED"] if missing_outputs else []
    bank = json_object(bank_dir / "bank.json") if "bank.json" not in missing_outputs else None
    ids, missing_sources, invalid_sources = [], [], []
    if "bank.json" not in missing_outputs and bank is None:
        flags.append("BANK_JSON_INVALID")
    questions = bank.get("questions") if bank is not None else None
    if bank is not None and not isinstance(questions, list):
        flags.append("BANK_QUESTIONS_NOT_LIST")
    if isinstance(questions, list):
        for item in questions:
            qid = item.get("id") if isinstance(item, dict) else None
            if not isinstance(qid, str) or not SAFE_ID.fullmatch(qid):
                flags.append("BANK_QUESTION_ID_INVALID")
                continue
            if qid[:10] != f"NSEJS-{row['year']}" or qid[11:12] != SUBJECT_CODES[row["subject"]]:
                flags.append("BANK_YEAR_SUBJECT_MISMATCH")
            ids.append(qid)
        if len(ids) != len(set(ids)):
            flags.append("BANK_DUPLICATE_QUESTION_ID")
        if len(questions) != declared:
            flags.append("BANK_COUNT_DISAGREES_WITH_AUTHOR_TEST")
        for qid in sorted(set(ids)):
            source_dir = source_root / qid
            missing = [name for name in SOURCE_FILES if not (source_dir / name).is_file()]
            if missing:
                missing_sources.append({"source_id": qid, "missing_files": missing})
                continue
            item = json_object(source_dir / "source_item.json")
            custody = json_object(source_dir / "source-custody.json")
            if item is None or custody is None:
                invalid_sources.append(qid)
            elif item.get("source_item_locator") != qid or custody.get("source_item_locator") != qid:
                invalid_sources.append(qid)
                flags.append("CUSTODY_SOURCE_ID_CONFLICT")
            elif custody.get("comparison_status") == "ORIGINAL_EXACT":
                flags.append("ORIGINAL_EXACT_DECLARATION_NOT_INDEPENDENT_PROOF")
    if missing_sources:
        flags.append("SOURCE_CUSTODY_NOT_RECEIVED")
    if invalid_sources:
        flags.append("SOURCE_CUSTODY_INVALID")
    if not source_root.is_dir():
        flags.append("SOURCE_ROOT_NOT_RECEIVED")
    blockers = {"BANK_JSON_INVALID", "BANK_QUESTIONS_NOT_LIST", "BANK_QUESTION_ID_INVALID",
                "BANK_YEAR_SUBJECT_MISMATCH", "BANK_DUPLICATE_QUESTION_ID",
                "BANK_COUNT_DISAGREES_WITH_AUTHOR_TEST", "CUSTODY_SOURCE_ID_CONFLICT"}
    structurally_complete = (
        not missing_outputs and isinstance(questions, list) and len(questions) == declared
        and len(ids) == declared and not missing_sources and not invalid_sources
        and not blockers.intersection(flags)
    )
    return {
        "year": int(row["year"]), "subject": row["subject"],
        "author_test_expected_items": declared,
        "bank_path": bank_path.as_posix(),
        "source_root": Path(row["source_root_expected"]).as_posix(),
        "bank_records_found": len(questions) if isinstance(questions, list) else None,
        "missing_output_files": missing_outputs,
        "missing_source_files": missing_sources,
        "invalid_source_ids": invalid_sources,
        "status": "STRUCTURE_PRESENT_NOT_ACADEMICALLY_VERIFIED" if structurally_complete else "INPUT_CUSTODY_HOLD",
        "flags": sorted(set(flags)),
        "academic_admission": "HOLD",
        "source_authenticity": "NOT_INDEPENDENTLY_VERIFIED",
        "qrt_adjudication": "HOLD",
    }


def load_official_locators(root: Path = ROOT, path: Path = OFFICIAL_LOCATORS) -> dict:
    """Read only publicly named IAPT PDF locators, never their source text.

    A URL linked from an official archive is provenance, not a downloaded
    source-custody artifact, licensed redistribution or QRT approval.
    """
    source = json_object(root / path)
    if not source or source.get("schema") != "grade9-nsejs-official-source-locators/v1":
        raise ValueError("Missing or malformed IAPT locator manifest")
    years = source.get("years")
    if not isinstance(years, list) or len(years) != 5:
        raise ValueError("Exactly five historical exam-year locator rows required")
    seen = set()
    for item in years:
        if not isinstance(item, dict) or not isinstance(item.get("year"), int):
            raise ValueError("Invalid IAPT locator row")
        year = item["year"]
        if year in seen or year not in YEARS:
            raise ValueError("Duplicate or unexpected IAPT year")
        seen.add(year)
        if item.get("source_bytes_imported") is not False or item.get("independently_authenticated") is not False:
            raise ValueError("Cannot claim official source bytes or authentication in metadata-only intake")
        for field in ("official_archive_url", "official_paper_url", "official_final_key_url"):
            url = item.get(field)
            if url is None and field == "official_paper_url" and year == 2020:
                continue
            if not isinstance(url, str) or not re.fullmatch(
                r"https://(?:www\.)?iapt\.org\.in/[A-Za-z0-9_./%-]+", url
            ):
                raise ValueError("Non-IAPT source URL or missing locator: "+field)
        if year in (2020, 2021) and not str(item.get("exam_series", "")).startswith("IOQJS_"):
            raise ValueError("2020/21 and 2021/22 must retain IOQJS Part I source identity")
    final = next(x for x in years if x["year"] == 2024)
    if (final.get("paper_code") != 51 or final.get("part_A1_range") != [1, 48]
            or final.get("part_A2_range") != [49, 60]
            or final.get("part_A2_format") != "MULTIPLE_CORRECT"
            or final.get("known_final_key_exception") != {
                "question": 20, "paper_code": 51, "status": "DROP"
            }):
        raise ValueError("IAPT 2024 paper-code 51 answer-format/drop facts must be preserved")
    return source


def audit(root: Path = ROOT, manifest: Path = MANIFEST) -> dict:
    official = load_official_locators(root)
    official_by_year = {x["year"]: x for x in official["years"]}
    records = [inspect_row(root, row) for row in load_manifest(root, manifest)]
    for row in records:
        year = official_by_year[row["year"]]
        row["official_exam_series"] = year["exam_series"]
        row["official_archive_url"] = year["official_archive_url"]
        row["official_paper_locator"] = year["official_paper_url"]
        row["official_final_key_locator"] = year["official_final_key_url"]
        row["official_locator_status"] = (
            "PAPER_AND_KEY_URLS_LOCATED_NOT_IMPORTED" if year["official_paper_url"]
            else "OFFICIAL_KEY_ONLY_PAPER_NOT_LOCATED"
        )
        if row["year"] in (2020, 2021):
            row["flags"].append("IOQJS_PART_I_SOURCE_IDENTITY_REVIEW_REQUIRED")
        if row["year"] == 2024:
            row["flags"].append("IAPT_CODE_51_QUESTION_20_DROPPED")
            row["flags"].append("IAPT_CODE_51_QUESTIONS_49_60_MULTI_CORRECT")
        row["flags"] = sorted(set(row["flags"]))
    subjects = Counter(x["subject"] for x in records)
    if any(subjects.get(subject) != 5 for subject in SUBJECTS):
        raise ValueError("Expected five year rows per subject")
    totals = {subject: sum(x["author_test_expected_items"] for x in records
                            if x["subject"] == subject) for subject in SUBJECTS}
    return {
        "schema": "grade9-nsejs-source-custody-preflight/v1",
        "scope": "AUTHOR_TEST_EXPECTATIONS_NOT_OFFICIAL_EXAM_COVERAGE",
        "official_archive_years_located": len(official_by_year),
        "official_paper_url_years_located": sum(bool(x["official_paper_url"]) for x in official["years"]),
        "official_final_key_url_years_located": sum(bool(x["official_final_key_url"]) for x in official["years"]),
        "official_lc2024_key_exception": "NSEJS-2024 CODE 51 Q20 DROP",
        "locators_are_source_custody": False,
        "subject_year_rows": len(records),
        "author_test_expected_by_subject": totals,
        "author_test_expected_total": sum(totals.values()),
        "missing_or_invalid_subject_year_bundles": sum(x["status"] == "INPUT_CUSTODY_HOLD" for x in records),
        "academic_admission": "HOLD", "source_rights": "NOT_REVIEWED",
        "qrt_adjudication": "HOLD",
        "public_physics_50": "SEPARATE_UNRECONCILED_CANDIDATE_CORPUS",
        "rows": records,
    }


def markdown(report: dict) -> str:
    lines = [
        "# NSEJS source-custody preflight",
        "",
        "**Academic admission: HOLD.** The reported counts are author test expectations, not official exam totals.",
        "A self-declared ORIGINAL_EXACT field never proves independent source authentication.",
        f"Official IAPT archive pages located for {report['official_archive_years_located']}/5 years; "
        f"paper URLs located for {report['official_paper_url_years_located']}/5.",
        "These are links, not recovered authorized source bytes or native source-custody records.",
        "2020-21/2021-22 are IOQJS Part I source series; do not relabel them as conventional NSEJS.",
        "Official 2024 Paper Code 51: Q20 is DROP; Q49-60 are multiple-correct.",

        "",
        f"Test-declared total: {report['author_test_expected_total']} across 15 subject-year groups.",
        f"Missing/incomplete groups: {report['missing_or_invalid_subject_year_bundles']}.",
        "The separate public Physics 50-item candidate corpus must not be counted again.",
        "",
        "| Year | Subject | Test-declared | Bank records | Status | Missing outputs |",
        "|---|---|---:|---:|---|---:|",
    ]
    for row in report["rows"]:
        got = row["bank_records_found"]
        lines.append(f"| {row['year']} | {row['subject']} | {row['author_test_expected_items']} | "
                     f"{'NOT_RECEIVED' if got is None else got} | {row['status']} | "
                     f"{len(row['missing_output_files'])} |")
    lines += [
        "", "## Needed before production Core2 qualification",
        "1. Approved original paper, key, figure and individual source custody bytes, held privately.",
        "2. Authenticated generation for all required banks, intake, reports and source-preserving HTML.",
        "3. Independent exact-source, figure, answer, QRT and rights review.",
        "4. Separate canonical UID and Core1A/Core1B learning-route reconciliation.",
        "", "No original text, answer key or figure content is exported in this receipt."
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    parser.add_argument("--require-files", action="store_true",
                        help="Exit 3 when one or more source/output groups are missing")
    parser.add_argument("--academic-gate", action="store_true",
                        help="Exit 4 until independently accepted source/QRT/rights evidence is available")
    args = parser.parse_args(argv)
    report = audit(args.root, args.manifest)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(markdown(report), encoding="utf-8")
    print(f"SOURCE_CUSTODY_HOLD: {report['missing_or_invalid_subject_year_bundles']}/15 "
          f"subject-year groups missing/incomplete; "
          f"{report['author_test_expected_total']} author-test claims (not authenticated originals)")
    if args.academic_gate:
        return 4
    return 3 if args.require_files and report["missing_or_invalid_subject_year_bundles"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
