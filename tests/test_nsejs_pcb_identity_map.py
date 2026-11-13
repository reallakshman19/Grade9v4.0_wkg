"""Source-neutral canonical NSEJS PCB Core2 question-map regression/negative tests."""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nsejs_pcb_identity_map import load, validate, render, stage


def test_all_45_modules_267_question_occurrences_exactly_covered():
    doc = load()
    assert doc["module_count"] == len(doc["modules"]) == 45
    assert doc["candidate_question_count"] == len(doc["questions"]) == 267
    assert doc["distinct_claimed_external_ids"] == 263
    assert doc["subjects"] == {
        "PHYSICS": {"modules": 21, "questions": 95},
        "CHEMISTRY": {"modules": 13, "questions": 87},
        "BIOLOGY": {"modules": 11, "questions": 85},
    }
    assert len({x["question_uid"] for x in doc["questions"]}) == 267
    assert not any("math" in x["module_slug"] or
                   x["subject"] == "MATHEMATICS" for x in doc["questions"])
    assert all(len(q["content_revision_sha256"]) == 64 for q in doc["questions"])


def test_duplicate_labels_are_scoped_not_silently_deduplicated():
    rows = load()["questions"]
    aliases = Counter(x["claimed_external_question_id"] for x in rows)
    expected = {
        "NSEJS-2024-B-Q50", "CHEM-NSEJS-ATOM-01",
        "NSEJS-2024-C-Q55", "NSEJS-2024-P-Q46"
    }
    assert {name for name, count in aliases.items() if count > 1} == expected
    assert sum(x["external_id_collision"] == "CONFLICTING_RECORDS"
               for x in rows) == 8
    for alias in expected:
        records = [x for x in rows if x["claimed_external_question_id"] == alias]
        assert len({x["question_uid"] for x in records}) == 2
        assert len({x["content_revision_sha256"] for x in records}) == 2


def test_qrt_and_teaching_are_proposals_not_accepted_scientific_evidence():
    rows = load()["questions"]
    assert sum(x["proposed_crux_kind"] is not None and
               x["proposed_crux_kind"] != x["proposed_qrt_operation"]
               for x in rows) == 5
    assert sum(x["figure_byte_custody"] == "HOLD" for x in rows) == 13
    assert Counter(x["construction_fit"] for x in rows) == {
        "MISSING_CONSTRUCTION": 241, "RELATED_ONLY_UNVERIFIED": 26}
    assert sum(x["source_return_verified"] is True for x in rows) == 0
    assert all(x["verified_missing_reasoning_step"] is None and
               x["independent_qrt_review"] == "NOT_RUN" and
               x["source_custody"] == x["source_rights"] ==
               x["final_key_custody"] == x["academic_admission"] == "HOLD"
               for x in rows)


def test_no_original_stems_figures_answers_keys_or_approved_exam_tasks_published():
    data = load()
    assert data["source_originals_published"] == 0
    assert all(q["content_published"] is False for q in data["questions"])
    serialized = json.dumps(data)
    for field in ('"stem"', '"answer"', '"correct_option"', '"options"',
                  '"reasoning_route"', '"worked_solution"', '"figure_bytes"',
                  '"official_exam_key"'):
        assert field not in serialized


def test_browseable_source_neutral_page_has_all_questions(tmp_path):
    doc = load()
    html = render(doc)
    assert html.count("<details ") == 45
    assert html.count("<tr>") == 312  # 267 question rows + 45 table headers
    assert html.count("Related practice, NOT sufficient teaching") == 26
    assert "241 missing constructions" in html
    assert "Mathematics excluded" in html
    assert "SOURCE / RIGHTS / QRT / ACADEMIC HOLD" in html
    assert "<iframe" not in html.lower()
    receipt = stage(tmp_path)
    assert receipt == {"module_count": 45, "candidate_questions": 267,
                       "related_only": 26, "missing_construction": 241,
                       "exact_qualified": 0, "academic_admission": "HOLD"}
    assert (tmp_path / "nsejs/core2/question-map.html").read_text() == html
    assert json.loads((tmp_path / "nsejs/core2/question-map.v1.json").read_text()) == doc


@pytest.mark.parametrize("case", [
    "approve", "source_pass", "rights_pass", "independent_qrt",
    "publish_stem", "publish_answer", "alter_question_sha",
    "reuse_uid", "duplicate_not_flagged", "invent_fit",
    "claim_exact_source", "claim_verified_missing_reason",
    "add_math", "subject_swap", "module_count", "fake_new_source",
    "crux_kind_relabel", "year_spoof", "drop_row",
])
def test_fail_closed_on_unauthorized_promotions_and_tampering(case):
    doc = deepcopy(load())
    row = doc["questions"][0]
    if case == "approve":
        row["academic_admission"] = "PASS"
    elif case == "source_pass":
        row["source_custody"] = "PASS"
    elif case == "rights_pass":
        row["source_rights"] = "CLEARED"
    elif case == "independent_qrt":
        row["independent_qrt_review"] = "PASS"
    elif case == "publish_stem":
        row["stem"] = "Unverified exam content"
    elif case == "publish_answer":
        row["answer"] = "A"
    elif case == "alter_question_sha":
        row["content_revision_sha256"] = "0" * 64
    elif case == "reuse_uid":
        doc["questions"][1]["question_uid"] = row["question_uid"]
    elif case == "duplicate_not_flagged":
        next(r for r in doc["questions"] if
             r["external_id_collision"] == "CONFLICTING_RECORDS")[
             "external_id_collision"] = "NONE"
    elif case == "invent_fit":
        row["construction_fit"] = "FOCUSED_VERIFIED"
    elif case == "claim_exact_source":
        row["source_return_verified"] = True
    elif case == "claim_verified_missing_reason":
        row["verified_missing_reasoning_step"] = "Invented"
    elif case == "add_math":
        doc["modules"].append({"slug": "math-algebra-r1", "subject": "MATHEMATICS",
                               "question_count": 1, "source_bank_sha256": "a" * 64})
    elif case == "subject_swap":
        row["subject"] = "CHEMISTRY"
    elif case == "module_count":
        doc["module_count"] = 46
    elif case == "fake_new_source":
        doc["source_originals_published"] = 267
    elif case == "crux_kind_relabel":
        row["proposed_crux_kind"] = "SYNTHESIZE"
    elif case == "year_spoof":
        row["source_year_claim"] = 2024
    elif case == "drop_row":
        doc["questions"].pop()
    with pytest.raises(ValueError, match="PCB_CANONICAL_HOLD"):
        validate(doc)
