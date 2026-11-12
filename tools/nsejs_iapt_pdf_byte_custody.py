#!/usr/bin/env python3
"""Fetch exact IAPT PDF bytes inside an ephemeral CI job; emit digests only.

Never write, upload or publish the original PDFs or extracted question text.
Only host-allowlisted IAPT TLS URLs; redirects outside IAPT fail closed.
The receipt is byte custody evidence, NOT licensing or academic approval.
"""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import ssl
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

ALLOWED_HOSTS = frozenset(("iapt.org.in", "www.iapt.org.in", "mail.iapt.org.in"))
URLS = {
    "NSEJS_2024_CODE51_PAPER": (
        "https://iapt.org.in/wp-content/uploads/NSEJS-2024_Set_51.pdf",
        "https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf",
        "https://mail.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf",
    ),
    "NSEJS_2024_FINAL_KEY": (
        "https://iapt.org.in/wp-content/uploads/NSEJS_-_2024_Final_Answer_Key.pdf",
        "https://www.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf",
        "https://mail.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf",
    ),
}
ARCHIVE_URLS = {
    "IOQJS_2020_21_CODE51_PAPER": (
        "https://iapt.org.in/images/nse_2020/IOQJS%20PART%20I%202020-21.pdf",
        "https://www.iapt.org.in/images/nse_2020/IOQJS%20PART%20I%202020-21.pdf",
    ),
    "IOQJS_2020_21_FINAL_KEY": (
        "https://iapt.org.in/wp-content/uploads/Final-Answer-key-IOQJS-2020-21Part-I.pdf",
        "https://www.iapt.org.in/images/nse_2020/final-answer-keys-ioqjs-part-I.pdf",
    ),
    "IOQJS_2021_22_CODE51_PAPER": (
        "https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i.pdf",
        "https://www.iapt.org.in/images/nse_2021/ioqjs_2021_22_part_i.pdf",
    ),
    "IOQJS_2021_22_FINAL_KEY": (
        "https://iapt.org.in/wp-content/uploads/ioqjs_2021_22_part_i_answer_key.pdf",
        "https://www.iapt.org.in/images/nse_2021/ioqjs_2021_22_part_i_answer_key.pdf",
    ),
    "NSEJS_2022_23_CODE51_PAPER": (
        "https://iapt.org.in/wp-content/uploads/nsejs_2022_23_part_i.pdf",
        "https://www.iapt.org.in/images/nse_2022/nsejs_2022_23_part_i.pdf",
    ),
    "NSEJS_2022_23_FINAL_KEY": (
        "https://iapt.org.in/wp-content/uploads/nsejs-2022-final-answer-key.pdf",
    ),
    "NSEJS_2023_24_CODE51_PAPER": (
        "https://iapt.org.in/wp-content/uploads/NSEJS_2023_Set_51.pdf",
        "https://www.iapt.org.in/images/nse_2023/NSEJS_2023_Set_51.pdf",
    ),
    "NSEJS_2023_24_KEY_AS_LINKED_BY_IAPT": (
        "https://iapt.org.in/wp-content/uploads/NSEJS_2023_TENTATIVE_ANSWER_KEY.pdf",
    ),
}
# 2023 key URL carries a TENTATIVE filename despite prior official page's
# FINAL label. Its publication/revision authority must be verified separately.

MAX_BYTES = 25 * 1024 * 1024
MIN_BYTES = 512


def allowlisted_url(url: str) -> bool:
    p = urlparse(url)
    return (p.scheme == "https" and p.hostname in ALLOWED_HOSTS
            and p.port in (None, 443) and not p.username and not p.password
            and p.path.lower().endswith(".pdf") and not p.fragment)


def safe_http_error(exc: Exception) -> str:
    """No URL query data, tokens or response bodies in public output."""
    if isinstance(exc, HTTPError):
        return "HTTP_" + str(exc.code)
    if isinstance(exc, URLError):
        return "URL_TRANSPORT_ERROR_" + type(exc.reason).__name__
    if isinstance(exc, TimeoutError):
        return "TIMEOUT"
    return type(exc).__name__.upper()[:50]


class IAPTOnlyRedirect(HTTPRedirectHandler):
    """Reject redirects before issuing a request outside the official domain."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowlisted_url(newurl):
            raise ValueError("REDIRECT_LEFT_IAPT_ALLOWLIST")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_official_bytes(url: str, timeout: int = 18) -> tuple[bytes, str]:
    if not allowlisted_url(url):
        raise ValueError("SOURCE_URL_NOT_IAPT_ALLOWLISTED")
    req = Request(url, headers={
        "User-Agent": "Grade9-NSEJS-SourceCustody/1.0 academic-review (no redistribution)",
        "Accept": "application/pdf",
        "Cache-Control": "no-cache",
    })
    opener = build_opener(IAPTOnlyRedirect(), HTTPSHandler(context=ssl.create_default_context()))
    with opener.open(req, timeout=timeout) as response:
        actual = response.geturl()
        if not allowlisted_url(actual):
            raise ValueError("REDIRECT_LEFT_IAPT_ALLOWLIST")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("SOURCE_PDF_TOO_LARGE")
        if len(body) < MIN_BYTES or not body.startswith(b"%PDF-"):
            raise ValueError("NOT_REAL_PDF_BYTES")
        return body, actual


def inspect_pdf_bytes(data: bytes) -> dict:
    from pypdf import PdfReader
    reader = PdfReader(BytesIO(data), strict=False)
    pages = len(reader.pages)
    if pages < 1:
        raise ValueError("PDF_PAGE_COUNT_INVALID")
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "pdf_pages": pages,
        "pdf_encrypted": reader.is_encrypted,
    }


def inspect_one(name: str, candidates: tuple[str, ...], timeout: int = 18) -> dict:
    attempts: list[dict] = []
    for url in candidates:
        if not allowlisted_url(url):
            attempts.append({"url": url, "error_code": "NON_IAPT_URL_BLOCKED"})
            continue
        try:
            content, final_url = read_official_bytes(url, timeout=timeout)
            stats = inspect_pdf_bytes(content)
            return {
                "document": name,
                "fetch_status": "RAW_PDF_BYTES_FETCHED_HASHED",
                "official_archive_source": "IAPT",
                "requested_url": url,
                "final_url": final_url,
                **stats,
                "content_text_exported": False,
                "original_pdf_exported": False,
                "rights_to_redistribute": "NOT_VERIFIED",
                "figure_fidelity": "NOT_VERIFIED",
                "independent_academic_admission": "HOLD",
                "attempts": attempts,
            }
        except Exception as exc:
            attempts.append({"url": url, "error_code": safe_http_error(exc)})
    return {
        "document": name, "fetch_status": "RAW_SOURCE_NOT_RECEIVED",
        "sha256": None, "size_bytes": None, "pdf_pages": None,
        "rights_to_redistribute": "NOT_VERIFIED",
        "figure_fidelity": "NOT_VERIFIED",
        "independent_academic_admission": "HOLD",
        "content_text_exported": False, "original_pdf_exported": False,
        "attempts": attempts,
    }


def build_receipt(timeout: int = 18, include_archives: bool = False) -> dict:
    sources = {**URLS, **ARCHIVE_URLS} if include_archives else URLS
    rows = [inspect_one(n, urls, timeout=timeout) for n, urls in sources.items()]
    count = sum(x["fetch_status"] == "RAW_PDF_BYTES_FETCHED_HASHED" for x in rows)
    return {
        "schema": "grade9-nsejs-iapt-source-raw-byte-custody/v1",
        "retrieval_method": "IAPT_HTTPS_ALLOWLIST_WITH_TLS_VERIFICATION",
        "source_pdf_content_embedded": False,
        "source_pdf_files_saved": False,
        "raw_pdf_documents_received": count,
        "expected_documents": len(rows),
        "archive_years_attempted": include_archives,
        "source_rights": "NOT_VERIFIED",
        "independent_source_fidelity": "NOT_VERIFIED",
        "academic_admission": "HOLD",
        "qrt_adjudication": "HOLD",
        "original_figure_comparison": "NOT_VERIFIED",
        "documents": rows,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--timeout", type=int, default=18)
    ap.add_argument("--include-archive-years", action="store_true",
                    help="Also attempt official 2020–2023 IOQJS/NSEJS papers and keys")
    ap.add_argument("--require-both", action="store_true",
                    help="Exit 7 unless both actual official PDFs were fetched+hashed")
    args = ap.parse_args(argv)
    if not 1 <= args.timeout <= 60:
        ap.error("timeout outside [1,60]")
    report = build_receipt(timeout=args.timeout, include_archives=args.include_archive_years)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("IAPT_PDF_SOURCE_CUSTODY:", report["raw_pdf_documents_received"],
          "/", report["expected_documents"], "actual official PDF byte receipts",
          "| rights=NOT_VERIFIED | admission=HOLD")
    for doc in report["documents"]:
        print(doc["document"], doc["fetch_status"],
              doc.get("sha256") or "SHA256_NOT_RECEIVED",
              doc.get("size_bytes") or "SIZE_NOT_RECEIVED",
              "pages", doc.get("pdf_pages") or "NOT_RECEIVED")
    code51 = {x["document"]: x["fetch_status"] for x in report["documents"]
              if x["document"] in URLS}
    if args.require_both and not (
        len(code51) == 2
        and all(x == "RAW_PDF_BYTES_FETCHED_HASHED" for x in code51.values())
    ):
        return 7
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
