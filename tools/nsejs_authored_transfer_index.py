"""Derive safe authored (NOT official-exam) Chemistry/Biology Core1B transfer practice.

Read only the existing deterministic, checked-in Core1B authoring output.
Do not copy the original target bank, QRT nomination or source figures to public.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

SUBJECTS=("chemistry","biology")
SCHEMA="grade9-nsejs-authored-core1b-practice/v1"
ORIGIN="GRADE9_ORIGINAL_CORE1B_TRANSFER_NOT_OFFICIAL_NSEJS"
SUFFIX={"chemistry":"CHEMISTRY","biology":"BIOLOGY"}


def sha(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value,sort_keys=True,separators=(",",":"),
        ensure_ascii=False).encode("utf-8")).hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"\s+"," ",re.sub(r"[^\w\s]"," ",text)).strip().casefold()


def derive_authored_transfer_index(generated: Path,
                                  lessons: dict[str,tuple[str,...]]) -> dict:
    if set(SUBJECTS)-set(lessons):
        raise ValueError("CORE1B_SUBJECTS_MISSING")
    rows=[]
    for subject in SUBJECTS:
        slugs=lessons[subject]
        for slug in slugs:
            path=generated/slug
            b=json.loads((path/"core1b_reconstruction.json").read_text("utf-8"))
            bank=json.loads((path/"bank.json").read_text("utf-8"))
            original=(bank.get("questions") or [])
            if (len(original)!=1 or not isinstance(original[0].get("stem"),str)
                or b.get("academic_status")!="HOLD:ACADEMIC_ADMISSION"):
                raise ValueError("CORE1B_AUTHOR_CUSTODY_NOT_VALID:"+slug)
            stages=b.get("stages") or {}
            attempt=stages.get("stage_2_attempt") or {}
            reconstruct=stages.get("stage_3_reconstruct") or {}
            boundary=stages.get("stage_6_boundary_test") or {}
            prompt=attempt.get("prompt")
            fresh_id=b.get("fresh_context_ref")
            if (not isinstance(prompt,str) or len(prompt)<55 or
                not isinstance(fresh_id,str) or len(fresh_id)<10 or
                fresh_id.upper().find("AUTHENTIC-EXAM")>=0 or
                fresh_id==b.get("target_question_id") or
                normalized(prompt)==normalized(original[0]["stem"]) or
                not isinstance(boundary.get("prompt"),str) or
                not isinstance(boundary.get("answer"),str) or
                len(boundary["prompt"])<25 or len(boundary["answer"])<25):
                raise ValueError("CORE1B_FRESH_TRANSFER_UNQUALIFIED:"+slug)
            raw_steps=reconstruct.get("route") or []
            if not isinstance(raw_steps,list) or len(raw_steps)<2:
                raise ValueError("CORE1B_RECONSTRUCTION_NOT_AUTHORED:"+slug)
            steps=[]
            for step in raw_steps:
                if not isinstance(step,dict):
                    raise ValueError("CORE1B_RECONSTRUCTION_UNREADABLE:"+slug)
                answer=step.get("step_answer")
                if not isinstance(answer,str) or len(answer)<8:
                    raise ValueError("CORE1B_RECONSTRUCTION_ANSWER_MISSING:"+slug)
                steps.append({"ask":str(step.get("ask") or ""), "answer":answer})
            if not isinstance(b.get("progressive_hints",[]),list):
                raise ValueError("CORE1B_HINTS_INVALID:"+slug)
            exercise={
                "uid":"g9:NSEJS:AUTHORED_CORE1B:"+SUFFIX[subject]+":"+slug,
                "subject":SUFFIX[subject],
                "lesson_slug":slug,
                "original_exam_question":False,
                "source_origin":ORIGIN,
                "academic_admission":"HOLD",
                "independent_science_review":"HOLD",
                "fresh_task_ref":fresh_id,
                "prompt":prompt,
                "boundary_question":boundary["prompt"],
                "boundary_author_response":boundary["answer"],
                "reconstruction":steps,
                "lesson_route":f"nsejs/{subject}/core1/{slug}/index.html",
            }
            exercise["revision_sha256"]=sha(exercise)
            rows.append(exercise)
    if len(rows)!=5 or len({x["uid"] for x in rows})!=5:
        raise ValueError("AUTHORED_CORE1B_CENSUS_INVALID")
    return {
        "schema":SCHEMA,
        "source_origin":ORIGIN,
        "academic_admission":"HOLD",
        "source_exam_authenticated":False,
        "official_exam_questions_published":0,
        "copy_of_original_exam_stem":False,
        "source_rights_review":"HOLD",
        "authored_transfer_count":5,
        "items":rows,
    }
