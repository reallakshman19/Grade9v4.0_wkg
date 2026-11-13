"""Source-first NSEJS recovery: honest Core1 missing-input receipts and paper-link practice.

This is NOT a source-authenticated question bank or an 18-module promotion.
Never copy source paper text, solutions, official PDF bytes, or workspace/sources
into a public package. The public release gate always stays ACADEMIC_HOLD.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

IAPT_HOSTS = {"iapt.org.in", "www.iapt.org.in", "mail.iapt.org.in"}
EXPECTED_YEARS = set(range(2020, 2025))
SUBJECTS = ("CHEMISTRY", "BIOLOGY")
ORIGIN = "IAPT_OFFICIAL_PAPER_LINK_ONLY_CONTENT_UNVERIFIED"
SCHEMA = "grade9-nsejs-source-linked-practice/v1"


def _sha(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _iapt_url(url: object) -> str:
    if not isinstance(url, str):
        raise ValueError("IAPT_URL_NOT_STRING")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname not in IAPT_HOSTS
        or not parsed.path.startswith("/") or parsed.username is not None
        or parsed.password is not None or parsed.port is not None
        or parsed.query or parsed.fragment):
        raise ValueError("NON_OFFICIAL_OR_UNSAFE_IAPT_URL")
    return url


def build_source_link_index(source: dict) -> dict:
    """Build only a paper/key URL index, never unverified question records."""
    if (not isinstance(source, dict) or
        source.get("schema") != "grade9-nsejs-official-source-locators/v1" or
        source.get("source_admission") != "HOLD" or
        source.get("copyright_and_redistribution") != "NOT_REVIEWED"):
        raise ValueError("UNQUALIFIED_OFFICIAL_LOCATOR_REGISTRY")
    rows = source.get("years")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_YEARS):
        raise ValueError("YEAR_CENSUS_NOT_PINNED")
    years = {}
    for entry in rows:
        year = entry.get("year")
        if (type(year) is not int or year not in EXPECTED_YEARS or
            year in years or entry.get("source_bytes_imported") is not False or
            entry.get("independently_authenticated") is not False):
            raise ValueError("UNQUALIFIED_OR_DUPLICATE_PAPER_SOURCE")
        paper = _iapt_url(entry.get("official_paper_url"))
        key = _iapt_url(entry.get("official_final_key_url"))
        archive = _iapt_url(entry.get("official_archive_url"))
        identity = {"year":year, "series":entry["exam_series"],
                    "paper_url":paper, "key_url":key, "archive_url":archive,
                    "paper_code":entry.get("paper_code")}
        row = {
            "year":year,
            "exam_series":entry["exam_series"],
            "source_origin":ORIGIN,
            "paper_url":paper,
            "key_url":key,
            "archive_url":archive,
            "source_revision_sha256":_sha(identity),
            "paper_evidence_status":entry.get("paper_link_status", "UNVERIFIED"),
            "key_evidence_status":entry.get("key_link_status", "UNVERIFIED"),
            "source_authentication":"HOLD",
            "academic_admission":"HOLD",
            "question_text_present":False,
            "official_answer_values_present":False,
            "attempt_eligibility":"LINK_ONLY_SOURCE_SCOPE_HOLD",
        }
        if year == 2024:
            if (entry.get("paper_code") != 51 or
                entry.get("part_A1_range") != [1, 48] or
                entry.get("part_A2_range") != [49, 60] or
                entry.get("part_A2_format") != "MULTIPLE_CORRECT" or
                entry.get("known_final_key_exception") !=
                {"question":20,"paper_code":51,"status":"DROP"}):
                raise ValueError("CODE51_2024_FORMAT_OR_DROP_NOT_VERIFIED")
            row["attempt_eligibility"] = "UNVERIFIED_LOCAL_NOTES_ONLY_CODE51"
            row["paper_code"] = 51
            row["supported_question_range"] = [1, 60]
            row["multi_answer_range"] = [49, 60]
            row["dropped_question_numbers"] = [20]
        years[year] = row
    if set(years) != EXPECTED_YEARS:
        raise ValueError("INCOMPLETE_OFFICIAL_SOURCE_INDEX")
    return {
        "schema":SCHEMA,
        "source_authority":ORIGIN,
        "source_registry_sha256":_sha(source),
        "academic_admission":"HOLD",
        "redistribution_rights":"HOLD",
        "student_claim":"UNVERIFIED_LOCAL_PAPER_NOTES_NOT_AN_EXAM_SCORE",
        "question_count_claimed":0,
        "actual_question_bodies":0,
        "subjects":list(SUBJECTS),
        "years":[years[y] for y in sorted(years,reverse=True)],
    }


def recovery_receipt(coverage: dict, builder_names: tuple[str,...]) -> dict:
    """Auditable per-construction missing-input map (without private question data)."""
    if (coverage.get("schema") != "grade9-nsejs-public-core1ab-coverage/v1" or
        coverage.get("tracked_constructions") != 26 or
        coverage.get("published_authored_preview_journeys") != 8 or
        coverage.get("not_published_constructions") != 18 or
        coverage.get("academic_admission") != "HOLD"):
        raise ValueError("CORE1_COVERAGE_NOT_PINNED")
    if len(set(builder_names)) != len(builder_names) or not builder_names:
        raise ValueError("REPRODUCIBLE_GENERATORS_NOT_DECLARED")
    rows = coverage["rows"]
    if len(rows) != 26 or len({r["construction_id"] for r in rows}) != 26:
        raise ValueError("CORE1_SOURCE_LEDGER_DUPLICATED")
    items=[]
    for row in rows:
        route=row.get("route")
        if row.get("academic_admission") != "HOLD" or row.get("original_exam_claim") is not False:
            raise ValueError("CORE1_ACADEMIC_SOURCE_PREMATURE_PROMOTION")
        public=bool(route)
        if public != (row.get("learner_status") == "AUTHORED_PREVIEW_UNVALIDATED"):
            raise ValueError("CORE1_ROUTE_STATUS_INCONSISTENT")
        if public and (not route.startswith("nsejs/") or not route.endswith("/index.html")):
            raise ValueError("CORE1_PUBLIC_ROUTE_INVALID")
        items.append({
            "construction_id":row["construction_id"],
            "subject":row["subject"],
            "historical_target":row["historical_target"],
            "source_matching":row["source_matching"],
            "academic_admission":"HOLD",
            "canonical_source_uid":None,
            "original_exam_claim":False,
            "technical_state":"EXISTING_AUTHORED_PREVIEW" if public else "MISSING_CHECKED_IN_REPRODUCIBLE_BUILD",
            "public_route":route if public else None,
            "needed_before_technical_preview":[] if public else [
                "CHECKED_IN_AUTHORING_OR_DETERMINISTIC_BUILDER",
                "PRIVATE_SOURCE_CUSTODY_ATTESTATION_WITHOUT_PUBLIC_SOURCE_COPY",
                "SOURCE_AND_QRT_IDENTITY_RECONCILIATION",
                "CORE1A_CORE1B_SCIENCE_AND_TRANSFER_EVIDENCE",
                "ORIGINAL_RENDERED_HTML_FIRST_ATTEMPT_GUARD",
                "REAL_HTTP_CHROMIUM_TABLET_RECEIPT",
                "OWNER_PUBLICATION_APPROVAL",
            ],
            "academically_qualified":False,
        })
    missing=[x for x in items if x["public_route"] is None]
    if len(missing)!=18:
        raise ValueError("CORE1_UNPUBLISHED_COUNT_CONFLICT")
    return {
        "schema":"grade9-nsejs-core1-recovery/v1",
        "release":"TECHNICAL_RECOVERY_ONLY_NOT_PUBLICATION_APPROVAL",
        "academic_admission":"HOLD",
        "builder_allowlist":list(builder_names),
        "tracked":26,"existing_technical_previews":8,"missing_reproducible_previews":18,
        "owner_reported_extra_construction_unidentified":1,
        "items":items,
    }


def render_core1_recovery(receipt: dict) -> str:
    if receipt.get("missing_reproducible_previews")!=18 or receipt.get("academic_admission")!="HOLD":
        raise ValueError("CORE1_RECOVERY_PUBLIC_DISPLAY_MUST_HOLD")
    cards=[]
    for item in receipt["items"]:
        if item["public_route"] is not None:
            continue
        name=html.escape(item["construction_id"].replace("-"," ").title())
        subject=html.escape(item["subject"])
        code=html.escape(item["construction_id"])
        cards.append(f'<li><h2>{name}</h2><p>{subject} · <code>{code}</code></p>'
                     '<p>No reproducible public authored module or authenticated source mapping is available. '
                     'Core1A/B teaching, independent transfer and browser evidence must be rebuilt and reviewed.</p>'
                     '<span class="hold">NOT PUBLISHED · source and academic HOLD</span></li>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>NSEJS · 18 Core1 recovery cases</title>'
            '<style>body{font:18px/1.6 system-ui,sans-serif;color:#153449;background:#f3f8fb;margin:0}'
            'main{max-width:1000px;margin:auto;padding:24px}ul{list-style:none;padding:0;display:grid;gap:14px}'
            'li{border:1px solid #bacfd8;border-radius:12px;padding:18px;background:white}'
            '.hold{font-weight:700;color:#765113}a{color:#145d79}'
            'a:focus-visible{outline:3px solid #a97627}</style></head><body><main>'
            '<a href="index.html">Back to NSEJS hub</a><h1>Core1A / Core1B · 18 recovery cases</h1>'
            '<p><strong>Engineering HOLD · not an approved teaching release.</strong> '
            'Eight distinct authored technical-preview journeys are already staged. '
            'These 18 remain absent from the checked-in reproducible builder set, '
            'and the historical 27th item lacks a test-backed construction identity. '
            'No source questions or examination figures are reproduced here.</p>'
            '<ul>'+"".join(cards)+'</ul>'
            '<p>For a new module, provide a deterministic builder, source custody, '
            'science and fresh-transfer evidence, protected attempt verification '
            'and owner approval. Passing tests never means academic approval.</p></main></body></html>')


def write_json(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
