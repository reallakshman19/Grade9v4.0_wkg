#!/usr/bin/env python3
"""Publish a bounded, clearly UNVALIDATED NSEJS technical preview on GitHub Pages.

Preserves existing school/WPE public routes and synthetic practice. Includes
only already-public candidate records and generated AUTHORED Core1A/B HTML.
Never copies workspace/sources, private original-paper PDFs, or review archives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_public_reader_preview import build_preview

PUBLIC_NSEJS = (
    "nsejs/index.html",
    "nsejs/physics/index.html",
    "nsejs/chemistry/index.html",
    "nsejs/biology/index.html",
    "nsejs/physics/question-bank.html",
    "nsejs/js/core2-physics-reader.js",
    "nsejs/data/physics-core2-candidates.v1.json",
    "nsejs/data/physics-core2-integrity.v1.json",
    "nsejs/data/physics-core2-source-evidence.v1.json",
    "nsejs/data/physics-authored-practice-r1.json",
    "nsejs/PUBLIC_PREVIEW_STATUS.json",
)
PUBLIC_SCHOOL_DIRS = (
    "physics/wpe", "architecture", "css", "js",
)
PUBLIC_SCHOOL_FILES = (
    "index.html", "physics/index.html",
    "mathematics/index.html", "chemistry/index.html", "site.css",
    "site-nav.js",
)
GENERATORS = (
    "build_d3_batch2_modules.py",
    "build_d3_expansion_modules.py",
    "build_physics_fluids_core1.py",
    "build_bio_genetics_core1.py",
)
LESSONS = {
    "physics": (
        "nsejs-optics-displacement-d3-r1",
        "nsejs-fluids-surface-energy-d3-r1",
        "nsejs-fluids-sound-r1",
    ),
    "chemistry": (
        "chem-electronic-structure-d3-r1",
        "chem-phosphorus-oxyacids-d3-r1",
    ),
    "biology": (
        "bio-immunology-defense-d3-r1",
        "bio-viral-genetics-d3-r1",
        "bio-genetics-coordination-r1",
    ),
}
assert sum(map(len, LESSONS.values())) == 8

def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()

def put(root: Path, relative: str, payload: bytes) -> None:
    dest = root / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(payload)

def add_learning_nav(stage: Path, subject: str, slugs: tuple[str, ...]) -> None:
    path = stage / "nsejs" / subject / "index.html"
    body = path.read_text(encoding="utf-8")
    if "</body>" not in body:
        raise ValueError("SUBJECT_HTML_NOT_CLOSED:"+subject)
    if 'id="agent-b-authored-preview"' in body:
        raise ValueError("DUPLICATE_LEARNING_PREVIEW_LINK")
    link = '<section id="agent-b-authored-preview" class="tablet-container" aria-labelledby="agent-b-preview-heading" style="max-width:1000px;margin:28px auto;padding:24px;border:2px solid #b88e49;border-radius:15px;background:#fffaf0;color:#14364a"><h2 id="agent-b-preview-heading">Core1A / Core1B authored technical preview</h2><p>Learning modules are UNVALIDATED, academically on HOLD and are not official NSEJS questions. Independently verified source/academic approval is not claimed.</p><a href="core1/index.html" style="display:inline-block;min-height:56px;box-sizing:border-box;padding:15px 20px;border-radius:12px;background:#0b5977;color:#fff;font-weight:700;text-decoration:none">Open '+str(len(slugs))+' authored learning modules</a></section>'
    path.write_text(body.replace("</body>",link+"\n</body>",1),encoding="utf-8")

def lesson_index(subject: str, slugs: tuple[str, ...]) -> str:
    cards="\n".join(
        '<li><a href="'+slug+'/index.html" style="display:block;min-height:56px;box-sizing:border-box;padding:18px;border:1px solid #9bb6c5;border-radius:12px;background:#fff;margin-bottom:12px;text-decoration:none;color:#13415a">'+slug.replace("-"," ").title()+'</a></li>'
        for slug in slugs
    )
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NSEJS '+subject.title()+' · Authored Core1A / Core1B preview</title><style>body{font:18px/1.55 system-ui,sans-serif;background:#f4f8fb;color:#133047;margin:0}main{max-width:1000px;margin:auto;padding:28px}a{color:#0c577c}h1{font-size:1.8rem}ul{padding:0;list-style:none}.hold{border-left:5px solid #ac7517;background:#fff7df;padding:16px}a:focus-visible{outline:3px solid #bb7f1b}</style></head><body><main><a href="../index.html">Back to NSEJS '+subject.title()+'</a><h1>Core1A + Core1B authored learning modules</h1><p class="hold"><strong>Technical preview · UNVALIDATED · Academic HOLD.</strong> Authored teaching/transfer content, not official examination endorsement. B1–B7 and independent source-custody acceptance remain separate.</p><ul>'+cards+'</ul><p>No academic approval inferred from software validation.</p></main></body></html>')

def generated_lessons(stage: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="g9-authored-public-preview-") as td:
        temp = Path(td)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH","")
        for builder in GENERATORS:
            shutil.copyfile(ROOT / builder, temp / builder)
            subprocess.run([sys.executable, builder], cwd=temp, env=env,
                           check=True, capture_output=True, text=True, timeout=100)
        for subject, modules in LESSONS.items():
            for slug in modules:
                src = temp / "workspace" / "output" / slug / "learning_journey.html"
                if not src.is_file():
                    raise ValueError("MISSING_AUTHORED_LEARNING_HTML:"+slug)
                html = src.read_text(encoding="utf-8")
                if ("No academic approval inferred" not in html or
                    "agent-b-127-tablet-touch" not in html or
                    'data-role="save-firstAttempt"' not in html):
                    raise ValueError("AUTHOR_LESSON_HOLD_OR_ATTEMPT_CONTRACT_MISSING:"+slug)
                put(stage, f"nsejs/{subject}/core1/{slug}/index.html", html.encode("utf-8"))
            put(stage, f"nsejs/{subject}/core1/index.html",
                lesson_index(subject, modules).encode("utf-8"))
            add_learning_nav(stage,subject,modules)

def build(out: Path) -> dict:
    out=out.resolve()
    if out.exists() or out == ROOT or out.is_relative_to(ROOT/"workspace"):
        raise ValueError("STAGE_LOCATION_NOT_NEW")
    # Underlying synthetic fixture remains available at /preview.
    build_preview(out)
    for relative in PUBLIC_SCHOOL_DIRS:
        src=ROOT/relative
        if not src.is_dir():
            raise ValueError("MISSING_SCHOOL_ROUTE:"+relative)
        shutil.copytree(src,out/relative,dirs_exist_ok=True)
    for relative in PUBLIC_SCHOOL_FILES:
        src=ROOT/relative
        if not src.is_file():
            raise ValueError("MISSING_SCHOOL_ROUTE:"+relative)
        put(out,relative,src.read_bytes())
    for relative in PUBLIC_NSEJS:
        src=ROOT/relative
        if not src.is_file():
            raise ValueError("MISSING_NSEJS_PREVIEW_ASSET:"+relative)
        put(out,relative,src.read_bytes())
    generated_lessons(out)
    (out/".nojekyll").write_text("",encoding="utf-8")
    file_list=sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    if any(p.startswith(("workspace/","sources/","tests/","tools/")) or
           p.endswith((".pdf",".zip",".xlsx")) or
           "legacy-physics-candidate-source" in p for p in file_list):
        raise ValueError("PRIVATE_SOURCE_OR_ARCHIVE_IN_PUBLIC_PACKAGE")
    manifest={
        "status":"GRADE9_NSEJS_UNVALIDATED_TECHNICAL_PREVIEW",
        "academic_approval":"HOLD",
        "source_rights_review":"HOLD",
        "source_question_published":True,
        "candidate_50_record_published":True,
        "official_source_figures_published":False,
        "core1ab_authored_lesson_pages":8,
        "school_wpe_preserved":True,
        "existing_synthetic_reader_preserved":True,
        "files":{name:sha((out/name).read_bytes()) for name in file_list if name!="PUBLIC_PREVIEW_MANIFEST.json"}
    }
    (out/"PUBLIC_PREVIEW_MANIFEST.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    args=ap.parse_args()
    result=build(args.out)
    print("PASS: public NSEJS technical preview with 8 authored Core1AB pages, 50 source-claimed + 1 authored Core2, %d staged files" % len(result["files"]))

if __name__=="__main__":main()
