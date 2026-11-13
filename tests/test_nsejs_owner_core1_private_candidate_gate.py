"""Public-only negative controls for private Core1 archive gate.

No original paper, answer or private module is supplied or copied here.
"""
from __future__ import annotations

from decimal import Decimal
import hashlib
import json
import zipfile

import pytest

from tools.audit_nsejs_owner_core1_private_zip import check, check_single_core2_bank_link, verify_core2_bank_linkage


def test_zinc_negative_control_and_corrected_mass():
    oxide = Decimal("2.035")
    def atom_mass(product):
        return (oxide * 78 - product * 16) / (product - oxide)
    # Old accepted number was inconsistent with asserted Zn 65.4 u.
    assert abs(atom_mass(Decimal("3.625")) - Decimal("65.4")) > 1
    assert atom_mass(Decimal("3.585")) == Decimal("65.4")
    acid_moles = oxide / (Decimal("65.4") + 16)
    assert acid_moles == Decimal("0.025")
    assert acid_moles / Decimal("0.50") * 1000 == Decimal("50")


def test_mirror_reflection_coordinates_and_bad_scale():
    f = 10
    obj = 15
    mirror = 20
    v1 = f * obj / (obj - f)
    assert v1 == 30
    assert 2 * mirror - v1 == 10
    assert v1 / (-obj) == -2
    # A scaled f=20, u=30 case is a DIFFERENT authored task.
    assert (20 * 30 / (30 - 20)) == 60


def test_conjugate_answer_is_object_pair_not_supplied_focal_length():
    u1, u2, f = 18, 6, 9
    assert u1 + u2 == 24
    assert u1 * u2 == f * (u1 + u2) / 2
    assert abs((1/u1 + 1/u2) - 2/f) < 1e-12
    assert 9 not in (u1, u2)


def test_private_zip_gate_refuses_absent_archive(tmp_path):
    with pytest.raises(ValueError, match="CANDIDATE_ARCHIVE_MISSING"):
        check(tmp_path / "missing.zip")


def test_private_zip_gate_refuses_invalid_inventory(tmp_path):
    candidate = tmp_path / "invalid-inventory.zip"
    with zipfile.ZipFile(candidate, "w") as archive:
        archive.writestr("MANIFEST.json", json.dumps({"total_modules": 26}))
    with pytest.raises(ValueError, match="CANDIDATE_INVENTORY_CHANGED"):
        check(candidate)


def test_private_zip_gate_refuses_wrong_hash_before_inspection(tmp_path):
    candidate = tmp_path / "invalid-sha.zip"
    with zipfile.ZipFile(candidate, "w") as archive:
        archive.writestr("MANIFEST.json", "{}")
    with pytest.raises(ValueError, match="CANDIDATE_ARCHIVE_SHA_MISMATCH"):
        check(candidate, candidate_sha="0"*64)


def _synthetic_core2_bank_link():
    """Synthetic bytes only, no original exam text/answers or private data."""
    slug = "nsejs-optics-r1"
    sample = {"questions": [{"id": "SYNTHETIC-P-Q01",
                             "stem": "Invented check fixture only"}]}
    raw = json.dumps(sample, separators=(",", ":")).encode("utf-8")
    revision = json.dumps(sample["questions"][0], sort_keys=True,
                          ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    module = {"slug": slug, "subject": "PHYSICS",
              "source_bank_sha256": hashlib.sha256(raw).hexdigest()}
    row = {"module_slug": slug, "subject": "PHYSICS",
           "ordinal": 1, "claimed_external_question_id": "SYNTHETIC-P-Q01",
           "question_uid": "g9:pcb:physics:nsejs-optics-r1:001",
           "content_revision_sha256": hashlib.sha256(revision).hexdigest(),
           "academic_admission": "HOLD", "source_custody": "HOLD",
           "independent_qrt_review": "NOT_RUN", "source_return_verified": False,
           "content_published": False,
           "construction_fit": "RELATED_ONLY_UNVERIFIED",
           "candidate_learning_route": "nsejs/physics/core1/nsejs-optics-r1/index.html"}
    return slug, raw, module, row


def test_synthetic_private_core2_full_revision_linkage():
    slug, raw, module, row = _synthetic_core2_bank_link()
    check_single_core2_bank_link(slug, raw, module, row)


def test_core2_private_linkage_refuses_inconsistent_bank_byte_hash():
    slug, raw, module, row = _synthetic_core2_bank_link()
    corrupted = raw.replace(b"Invented", b"Altered!")
    with pytest.raises(ValueError, match="CORE2_BANK_SHA256_MISMATCH"):
        check_single_core2_bank_link(slug, corrupted, module, row)


def test_core2_private_linkage_refuses_modified_question_with_updated_bank_hash():
    slug, raw, module, row = _synthetic_core2_bank_link()
    corrupted = raw.replace(b"Invented", b"Altered!")
    module["source_bank_sha256"] = hashlib.sha256(corrupted).hexdigest()
    with pytest.raises(ValueError, match="CORE2_FULL_REVISION_SHA256_MISMATCH"):
        check_single_core2_bank_link(slug, corrupted, module, row)


def test_core2_private_linkage_refuses_question_uid_or_label_substitution():
    slug, raw, module, row = _synthetic_core2_bank_link()
    row["question_uid"] = "g9:pcb:physics:some-other-identity:001"
    with pytest.raises(ValueError, match="CORE2_CANONICAL_OCCURRENCE_MISMATCH"):
        check_single_core2_bank_link(slug, raw, module, row)
    row["question_uid"] = "g9:pcb:physics:nsejs-optics-r1:001"
    row["claimed_external_question_id"] = "SYNTHETIC-OTHER-QUESTION"
    with pytest.raises(ValueError, match="CORE2_EXTERNAL_ID_MISMATCH"):
        check_single_core2_bank_link(slug, raw, module, row)


def test_core2_private_linkage_refuses_fake_approval_or_false_teaching():
    slug, raw, module, row = _synthetic_core2_bank_link()
    row["academic_admission"] = "PASS"
    with pytest.raises(ValueError, match="CORE2_SOURCE_OR_ACADEMIC_PROMOTION"):
        check_single_core2_bank_link(slug, raw, module, row)
    row["academic_admission"] = "HOLD"
    row["construction_fit"] = "EXACT_MATCH_QUALIFIED"
    with pytest.raises(ValueError, match="CORE2_RELATED_ROUTE_PROMOTED_OR_MISSING"):
        check_single_core2_bank_link(slug, raw, module, row)


def test_core2_linkage_requires_full_27_private_banks(tmp_path):
    with pytest.raises(ValueError, match="CORE1_BANK_LINKAGE_27_REQUIRED"):
        verify_core2_bank_linkage({"synthetic": b"{}"}, repository_root=tmp_path)
