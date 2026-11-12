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
sys.path.insert(0, str(ROOT / "nsejs/contracts"))
from build_public_reader_preview import build_preview
from nsejs_core1ab_public_coverage import public_coverage, render_subject_index, render_official_sources
from source_learning_bridge import validate_bindings
from wpe_learner_contract import validate as validate_wpe_contract

PUBLIC_NSEJS = (
    "nsejs/index.html",
    "nsejs/physics/index.html",
    "nsejs/chemistry/index.html",
    "nsejs/biology/index.html",
    "nsejs/physics/question-bank.html",
    "nsejs/js/core2-physics-reader.js",
    "nsejs/js/core2-learning-route.js",
    "nsejs/data/physics-core2-candidates.v1.json",
    "nsejs/data/physics-core2-integrity.v1.json",
    "nsejs/data/physics-core2-source-evidence.v1.json",
    "nsejs/data/physics-authored-practice-r1.json",
    "nsejs/PUBLIC_PREVIEW_STATUS.json",
)
# Authored, source-bound Wave 2 Mechanics learner. This is ADDITIONAL to the
# eight existing generated Core1A/B previews, not a 9/26 coverage certificate.
MECHANICS_WPE_PUBLIC = (
    "nsejs/physics/learn-mechanics.html",
    "nsejs/css/wpe-touch-parity.css",
    "nsejs/js/wpe-contract-adapter.js",
    "nsejs/data/mechanics-wpe-teaching-pilot.v1.json",
    "nsejs/data/source-learning-bridge-tech-preview.v1.json",
)
MECHANICS_WPE_UID = "g9:PHYSICS:G9-AUTH-MECH-001"

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

def generated_lessons(stage: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="g9-authored-public-preview-") as td:
        temp = Path(td)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH","")
        for builder in GENERATORS:
            shutil.copyfile(ROOT / builder, temp / builder)
            subprocess.run([sys.executable, builder], cwd=temp, env=env,
                           check=True, capture_output=True, text=True, timeout=100)
        coverage = public_coverage(LESSONS, ROOT, temp / "workspace" / "output")
        put(stage, "nsejs/data/core1ab-coverage.v1.json",
            (json.dumps(coverage, indent=2, sort_keys=True) + "\n").encode("utf-8"))
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
                render_subject_index(subject, coverage).encode("utf-8"))
            add_learning_nav(stage,subject,modules)
    return coverage

def add_source_links(stage: Path) -> None:
    locators = ROOT / "docs" / "nsejs" / "official-iapt-source-locators-r1.json"
    put(stage, "nsejs/official-sources.html",
        render_official_sources(locators).encode("utf-8"))
    for subject in ("", "physics", "chemistry", "biology"):
        relative = f"nsejs/{subject}/index.html" if subject else "nsejs/index.html"
        page = stage / relative
        body = page.read_text(encoding="utf-8")
        if "</body>" not in body or 'id="official-iapt-links"' in body:
            raise ValueError("OFFICIAL_LINK_INSERTION_UNSAFE:"+relative)
        href = "../official-sources.html" if subject else "official-sources.html"
        block = ('<section id="official-iapt-links" style="max-width:1060px;margin:24px auto;'
                 'padding:20px;border:2px solid #b6c9d3;border-radius:12px;background:#fff">'
                 '<h2>Official IAPT source papers (external links only)</h2>'
                 '<p>Original papers stay on IAPT. These learning previews are not independently source-approved.</p>'
                 '<a style="display:inline-flex;align-items:center;min-height:56px;padding:12px 20px;'
                 'background:#125a79;color:white;border-radius:10px" href="'+href+'">'
                 'View official paper/key links</a></section>')
        page.write_text(body.replace("</body>", block + "\n</body>", 1), encoding="utf-8")

def validate_mechanics_wpe_public_pilot(original: dict, preview: dict,
                                        lesson: dict, collection: dict) -> dict:
    """Independent positive authorization for a technical-only, authored pilot.

    The original UNBUILT mapping is NEVER promoted or modified. The separate
    technical-preview mapping may unlock a lesson only after complete question
    revision, QRT HOLD, owner/task IDs, and its exact lesson revision match.
    """
    [source_row] = validate_bindings(original, collection)
    if (original.get("route_status") != "UNBUILT_TECHNICAL_PILOT" or
        source_row.get("lesson_status") != "PENDING_WAVE2" or
        source_row.get("lesson_revision") != "UNBUILT"):
        raise ValueError("SOURCE_FIRST_UNBUILT_CUSTODY_NOT_PRESERVED")
    rows = preview.get("routes")
    if (not isinstance(rows, list) or len(rows) != 1 or
        preview.get("schema") != original["schema"] or
        preview.get("academic_admission") != "HOLD" or
        preview.get("route_status") != "TECHNICAL_PREVIEW" or
        preview.get("preview_authority") != "AUTHORED_TECHNICAL_ONLY_NOT_ACADEMIC_ADMISSION"):
        raise ValueError("WPE_PREVIEW_MANIFEST_NOT_QUALIFIED")
    [candidate] = rows
    critical = ("question_uid", "source_id", "content_revision_sha256",
                "source_collection", "origin", "subject", "topic", "lesson_id",
                "task_a_id", "task_b_id", "transfer_id", "source_return")
    if any(candidate.get(key) != source_row.get(key) for key in critical):
        raise ValueError("WPE_SOURCE_LEARNING_BRIDGE_NOT_EXACT")
    if (candidate.get("lesson_status") != "READY_FOR_TECHNICAL_PREVIEW" or
        candidate.get("lesson_revision") != lesson.get("lesson", {}).get("revision") or
        candidate.get("academic_admission") != "HOLD" or
        candidate.get("original_source_status") != "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"):
        raise ValueError("WPE_LESSON_READINESS_OR_SOURCE_CLAIM_INVALID")
    result = validate_wpe_contract(lesson, preview)
    if (result["source_uid"] != MECHANICS_WPE_UID or
        result["academic_admission"] != "HOLD" or
        lesson.get("source_return",{}).get("route_status") != "TECHNICAL_PREVIEW"):
        raise ValueError("WPE_SOURCE_AUTHORIZATION_FAILED")
    return {"published":True, "source_uid":MECHANICS_WPE_UID,
            "source_revision_sha256":result["source_revision"],
            "lesson_revision":candidate["lesson_revision"],
            "lesson_id":candidate["lesson_id"], "academic_approval":"HOLD",
            "source_authenticity":"AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM",
            "status":"AUTHORED_TECHNICAL_PREVIEW_ONLY"}


def publish_mechanics_wpe_pilot(stage: Path) -> dict:
    def read(path: str) -> dict:
        return json.loads((ROOT/path).read_text(encoding="utf-8"))
    original = read("nsejs/data/source-learning-bridge-pilot.v1.json")
    preview = read("nsejs/data/source-learning-bridge-tech-preview.v1.json")
    lesson = read("nsejs/data/mechanics-wpe-teaching-pilot.v1.json")
    source = read("nsejs/data/physics-authored-practice-r1.json")
    qualified = validate_mechanics_wpe_public_pilot(original,preview,lesson,source)
    for path in MECHANICS_WPE_PUBLIC:
        content=(ROOT/path).read_bytes()
        if path.endswith((".html",".js")) and b"<iframe" in content.lower():
            raise ValueError("NO_IFRAMES_ALLOWED_IN_NSEJS_WPE_PILOT")
        put(stage,path,content)
    # Only the single correctly bound authored Mechanics question is
    # discoverable. All other Core2 records remain candidate-only.
    subject_page=stage/"nsejs/physics/index.html"
    page=subject_page.read_text(encoding="utf-8")
    if 'id="nsejs-wpe-mechanics-parity"' in page or "</body>" not in page:
        raise ValueError("DUPLICATE_OR_INVALID_WPE_HUB_INSERTION")
    href=("learn-mechanics.html?source_uid=" +
          qualified["source_uid"] +
          "&source_revision=" + qualified["source_revision_sha256"])
    block=(
        '<section id="nsejs-wpe-mechanics-parity" class="tablet-container" '
        'aria-labelledby="nsejs-mechanics-heading" '
        'style="margin:24px auto;padding:22px;border:2px solid #6c9fad;'
        'border-radius:15px;background:#f0f9fc;color:#173749">'
        '<h2 id="nsejs-mechanics-heading">Mechanics Core1A → Core1B · '
        'six-stage authored technical preview</h2>'
        '<p><strong>UNVALIDATED · Academic HOLD.</strong> '
        'A single source-bound authored Grade9 Physics practice example, '
        'not an original NSEJS exam question or academically admitted source. '
        'Use the interactive collision model and independent Task A/B.</p>'
        '<a href="'+href+'" style="display:inline-flex;align-items:center;'
        'min-height:56px;padding:14px 22px;border-radius:12px;'
        'background:#145c76;color:#fff;font-weight:750;text-decoration:none">'
        'Open authored Mechanics six-stage learner</a>'
        '</section>'
    )
    subject_page.write_text(page.replace("</body>",block+"\n</body>",1),
                            encoding="utf-8")
    return qualified


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
    coverage = generated_lessons(out)
    mechanics_wpe = publish_mechanics_wpe_pilot(out)
    add_source_links(out)
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
        "core1ab_authored_lesson_pages": coverage["published_authored_preview_journeys"],
        "core1ab_test_backed_constructions": coverage["tracked_constructions"],
        "core1ab_unpublished_constructions": coverage["not_published_constructions"],
        "additional_authored_mechanics_wpe_parity_preview": mechanics_wpe,
        "official_sources_link_only": True,
        "school_wpe_preserved":True,
        "existing_synthetic_reader_preserved":True,
        "files":{name:sha((out/name).read_bytes()) for name in file_list if name not in ("PUBLIC_PREVIEW_MANIFEST.json",".nojekyll")}
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
