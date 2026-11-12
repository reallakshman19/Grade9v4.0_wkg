#!/usr/bin/env python3
"""Deterministic public Physics candidate snapshot builder.

The public legacy preview is migration input, not authenticated exam authority.
No private owner sources/papers are ingested or published. Source identifier and
question content are conserved; official locator corrections are metadata only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
from nsejs_core2_audit import source_questions,validate

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"preview/question-status.html"
OUTPUT=ROOT/"nsejs/data/physics-core2-candidates.v1.json"
SCHEMA="grade9-nsejs-physics-core2-candidate-corpus/v1"

def git_blob_sha(content:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()

def compile_corpus(source_bytes:bytes,corrections:dict)->dict:
    qs=source_questions(source_bytes.decode("utf-8"))
    assert len(qs)==50,"Unexpected source-corpus cardinality"
    problems=validate(qs)
    if problems:
        raise ValueError("Structural source problems: "+", ".join(problems))
    if set(corrections).difference({q["source_id"] for q in qs}):
        raise ValueError("Official locator correction references unknown source")
    return {
        "schema_version":SCHEMA,
        "source_path":"preview/question-status.html",
        "source_git_blob_sha":git_blob_sha(source_bytes),
        "source_authority":"LEGACY_PUBLIC_CANDIDATE_SNAPSHOT_NOT_ACADEMICALLY_ADMITTED",
        "source_claims_status":"HOLD",
        "qrt_adjudication":"HOLD",
        "known_paper_locator_corrections":corrections,
        "questions":qs,
    }

def generated_bytes(corpus:dict)->bytes:
    return (json.dumps(corpus,ensure_ascii=False,indent=2)+"\n").encode("utf-8")

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=SOURCE)
    p.add_argument("--out",type=Path,default=OUTPUT)
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    try:
        candidate=json.loads(args.out.read_text(encoding="utf-8"))
        if candidate.get("schema_version")!=SCHEMA:
            raise ValueError("Unsupported candidate corpus schema")
        expected=compile_corpus(args.source.read_bytes(),candidate.get("known_paper_locator_corrections",{}))
        built=generated_bytes(expected)
        if args.check:
            if expected!=candidate:
                print("CANDIDATE_CORPUS_DRIFT: source snapshot and committed JSON differ",file=sys.stderr)
                return 2
            if generated_bytes(expected)!=generated_bytes(compile_corpus(args.source.read_bytes(),candidate["known_paper_locator_corrections"])):
                print("NONDETERMINISTIC_BUILD",file=sys.stderr)
                return 3
            print("PASS: deterministic 50-record public candidate corpus, no source promotion")
            return 0
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_bytes(built)
        print("WROTE",args.out,len(built),"bytes; origin remains UNVERIFIED")
        return 0
    except (ValueError,KeyError,OSError,UnicodeError) as error:
        print("CANDIDATE_CORPUS_BUILD_FAIL:"+str(error),file=sys.stderr)
        return 2

if __name__=="__main__":raise SystemExit(main())
