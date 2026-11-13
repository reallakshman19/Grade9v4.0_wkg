#!/usr/bin/env python3
"""Fail-closed authored-question-to-lesson binding. No academic approval."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9-]{2,80}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class BindingError(ValueError):
    """Unsafe, stale or ambiguous question-to-lesson binding."""


def revision_payload(question: dict) -> dict:
    """Mirror nsejs/js/core2-physics-reader.js revisionPayload order and fields."""
    return {
        "uid": "g9:PHYSICS:" + question["source_id"],
        "source_id": question["source_id"],
        "original_id": question["id"],
        "stem": question["stem"],
        "options": question["options"],
        "answer": question["answer"],
        "question_type": question["question_type"],
        "figures": question.get("source_figures") or [],
        "figure_note": question.get("figure_note") or "",
        "reasoning": question.get("steps") or [],
        "boundary": question.get("check") or "",
    }


def content_revision(question: dict) -> str:
    """SHA256 of UTF-8 JSON.stringify-equivalent canonical reader payload."""
    try:
        canonical = json.dumps(revision_payload(question), ensure_ascii=False,
                               separators=(",", ":"))
    except (KeyError, TypeError, ValueError) as exc:
        raise BindingError("SOURCE_REVISION_INPUT_MALFORMED") from exc
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_bindings(mapping: dict, collection: dict) -> list[dict]:
    if mapping.get("schema") != "grade9-nsejs-source-learning-bridge/v1":
        raise BindingError("INVALID_BRIDGE_SCHEMA")
    if mapping.get("source_revision_algorithm") != "core2-physics-reader-revisionPayload-sha256/v1":
        raise BindingError("INCOMPATIBLE_CONTENT_REVISION_ALGORITHM")
    if mapping.get("route_status") != "UNBUILT_TECHNICAL_PILOT":
        raise BindingError("UNVERIFIED_PILOT_ROUTE_STATUS")
    if mapping.get("academic_admission") != "HOLD":
        raise BindingError("ACADEMIC_ADMISSION_MUST_REMAIN_HOLD")
    if collection.get("schema_version") != "nsejs-authored-practice/v1":
        raise BindingError("UNSUPPORTED_SOURCE_COLLECTION")
    if collection.get("source_claim") != "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM":
        raise BindingError("UNAUTHORIZED_SOURCE_ORIGIN")
    if collection.get("academic_release") != "HOLD":
        raise BindingError("SOURCE_ACADEMIC_HOLD_MISSING")
    questions, routes = collection.get("questions"), mapping.get("routes")
    if not isinstance(questions, list) or not isinstance(routes, list) or not routes:
        raise BindingError("MISSING_SOURCE_OR_ROUTES")
    by_id = {}
    for question in questions:
        if not isinstance(question, dict) or not isinstance(question.get("source_id"), str):
            raise BindingError("MALFORMED_SOURCE_ENTRY")
        key = question["source_id"]
        if key in by_id:
            raise BindingError("DUPLICATE_SOURCE_ID:" + key)
        by_id[key] = question
    seen_uid, seen_lesson, seen_tasks = set(), set(), set()
    for row in routes:
        if not isinstance(row, dict):
            raise BindingError("MALFORMED_ROUTE")
        source_id, uid = row.get("source_id"), row.get("question_uid")
        if not isinstance(source_id, str) or source_id not in by_id:
            raise BindingError("UNKNOWN_SOURCE_ID")
        if uid != "g9:PHYSICS:" + source_id or uid in seen_uid:
            raise BindingError("DUPLICATE_OR_MISMATCHED_QUESTION_UID")
        seen_uid.add(uid)
        q = by_id[source_id]
        if (q.get("id") != source_id or q.get("topic") != "MECHANICS" or
            q.get("category") != "AUTHORED_PRACTICE" or
            q.get("origin") != "GRADE9_ORIGINAL_AUTHORING_NOT_EXAM" or
            q.get("qrt_adjudication") != "HOLD" or
            q.get("science_review") != "HOLD" or
            q.get("review_state") != "NOT_ADMITTED"):
            raise BindingError("SOURCE_PROVENANCE_OR_TOPIC_INVALID")
        if row.get("source_collection") != "nsejs/data/physics-authored-practice-r1.json":
            raise BindingError("SOURCE_COLLECTION_MISMATCH")
        if row.get("origin") != "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM":
            raise BindingError("FALSE_EXAM_PROVENANCE")
        if row.get("subject") != "PHYSICS" or row.get("topic") != q["topic"]:
            raise BindingError("SUBJECT_OR_TOPIC_MISMATCH")
        revision = row.get("content_revision_sha256")
        if not isinstance(revision, str) or not HEX64.fullmatch(revision):
            raise BindingError("SOURCE_REVISION_NOT_SHA256")
        if revision != content_revision(q):
            raise BindingError("STALE_SOURCE_REVISION:" + source_id)
        lesson = row.get("lesson_id")
        if not isinstance(lesson, str) or not SAFE_ID.fullmatch(lesson) or lesson in seen_lesson:
            raise BindingError("DUPLICATE_OR_INVALID_LESSON_ID")
        seen_lesson.add(lesson)
        if row.get("lesson_status") != "PENDING_WAVE2" or row.get("lesson_revision") != "UNBUILT":
            raise BindingError("UNVERIFIED_LESSON_MUST_NOT_BE_PUBLISHED")
        if row.get("reasoning_operation") != q.get("op") or not row.get("prerequisite"):
            raise BindingError("REASONING_OR_PREREQUISITE_MISMATCH")
        ids = [row.get("task_a_id"), row.get("task_b_id"), row.get("transfer_id")]
        if any(not isinstance(v, str) or not SAFE_ID.fullmatch(v) for v in ids):
            raise BindingError("INVALID_TASK_ID")
        if (len(set(ids)) != 3 or seen_tasks.intersection(ids) or lesson in ids
            or seen_lesson.intersection(ids)):
            raise BindingError("SHARED_ATTEMPT_OR_TRANSFER_ID")
        seen_tasks.update(ids)
        ret = row.get("source_return")
        if not isinstance(ret, dict) or ret.get("question_uid") != uid or ret.get("content_revision_sha256") != revision:
            raise BindingError("SOURCE_RETURN_REVISION_MISMATCH")
        if ret.get("topic") != "mechanics" or ret.get("page") != "nsejs/physics/question-bank.html":
            raise BindingError("UNSUPPORTED_SOURCE_RETURN")
    return routes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping", type=Path, default=ROOT / "nsejs/data/source-learning-bridge-pilot.v1.json")
    ap.add_argument("--collection", type=Path, default=ROOT / "nsejs/data/physics-authored-practice-r1.json")
    args = ap.parse_args()
    try:
        routes = validate_bindings(json.loads(args.mapping.read_text("utf-8")),
                                   json.loads(args.collection.read_text("utf-8")))
    except (OSError, json.JSONDecodeError, BindingError) as exc:
        print("HOLD source-learning binding:", exc)
        return 2
    print("PASS source-learning contract:", len(routes),
          "authored route(s); academic HOLD; lesson unbuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
