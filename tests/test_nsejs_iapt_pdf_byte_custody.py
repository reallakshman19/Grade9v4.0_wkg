"""Adversarial official PDF-byte custody controls; no examination content."""
import hashlib
import importlib.util
import json
from pathlib import Path
from urllib.error import HTTPError

import pytest
from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "nsejs_iapt_pdf_byte_custody", ROOT / "tools/nsejs_iapt_pdf_byte_custody.py")
custody = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(custody)


def fake_pdf() -> bytes:
    from io import BytesIO
    buff = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(buff)
    return buff.getvalue()


@pytest.mark.parametrize("url", [
    "http://iapt.org.in/wp-content/uploads/file.pdf",
    "https://external.example/file.pdf",
    "https://iapt.org.in.evil.example/file.pdf",
    "https://iapt.org.in/wp-content/uploads/file.html",
    "https://u:pass@iapt.org.in/foo.pdf",
    "https://iapt.org.in/foo.pdf#hidden",
])
def test_reject_wrong_scheme_domain_extension_credentials_and_fragment(url):
    assert not custody.allowlisted_url(url)


def test_allow_only_official_pdf_urls():
    assert custody.allowlisted_url(
        "https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf")
    assert custody.allowlisted_url(
        "https://mail.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf")


def test_actual_pdf_sha256_uses_bytes_not_text_or_declared_manifest():
    raw = fake_pdf()
    facts = custody.inspect_pdf_bytes(raw)
    assert raw.startswith(b"%PDF-")
    assert facts["sha256"] == hashlib.sha256(raw).hexdigest()
    assert facts["size_bytes"] == len(raw)
    assert facts["pdf_pages"] == 1
    assert facts["pdf_encrypted"] is False


def test_redirect_to_non_iapt_fails_before_request():
    handler = custody.IAPTOnlyRedirect()
    from urllib.request import Request
    import io
    with pytest.raises(ValueError, match="REDIRECT_LEFT_IAPT"):
        handler.redirect_request(Request("https://iapt.org.in/paper.pdf"),
                                 io.BytesIO(), 302, "Redirect",
                                 {"Location": "https://other.example/pdf.pdf"},
                                 "https://other.example/pdf.pdf")


def test_source_retrieval_writes_digest_only_and_does_not_misclassify_rights(monkeypatch):
    raw = fake_pdf()
    def retrieve(url, timeout):
        assert custody.allowlisted_url(url)
        return raw, url
    monkeypatch.setattr(custody, "read_official_bytes", retrieve)
    result = custody.build_receipt(timeout=2)
    assert result["raw_pdf_documents_received"] == 2
    assert result["academic_admission"] == "HOLD"
    assert result["source_rights"] == "NOT_VERIFIED"
    assert result["source_pdf_content_embedded"] is False
    assert all(x["sha256"] == hashlib.sha256(raw).hexdigest()
               for x in result["documents"])
    output = json.dumps(result)
    assert "%PDF" not in output and "Contents" not in output
    assert '"rights_to_redistribute": "NOT_VERIFIED"' in output


def test_network_failure_preserves_unverified_sha(monkeypatch):
    def retrieve(url, timeout):
        raise HTTPError(url, 403, "Forbidden", {}, None)
    monkeypatch.setattr(custody, "read_official_bytes", retrieve)
    result = custody.build_receipt(timeout=1)
    assert result["raw_pdf_documents_received"] == 0
    assert result["academic_admission"] == "HOLD"
    assert all(x["sha256"] is None for x in result["documents"])
    assert all(x["fetch_status"] == "RAW_SOURCE_NOT_RECEIVED" for x in result["documents"])
    assert all(row["error_code"] == "HTTP_403" for doc in result["documents"]
               for row in doc["attempts"])


def test_invalid_pdf_produces_no_fake_hash(monkeypatch):
    monkeypatch.setattr(custody, "read_official_bytes",
                        lambda url, timeout: (b"<html>not pdf</html>", url))
    result = custody.build_receipt(timeout=1)
    assert result["raw_pdf_documents_received"] == 0
    assert all(x["sha256"] is None for x in result["documents"])
