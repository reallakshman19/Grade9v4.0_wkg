"""Build an explicitly allowlisted, synthetic-only Grade9 technical preview.

Never copies private candidate source, Figures, source scans, or review outputs
into the public site. Publication is NOT academic approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))
from private_reader_integration import build, ROOT_MARKER, END_MARKER
from test_private_reader_integration import fixture

PAGES = (
    "preview/question-status.html",
    "modules/alpha/question-status.html",
    "modules/beta/question-status.html",
)

HUB = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Grade9 | Synthetic reader technical preview</title>
<style>
:root{font-family:system-ui,sans-serif;color-scheme:light}
body{margin:0;background:#f1f7fa;color:#143344}
main{max-width:1000px;margin:0 auto;padding:clamp(22px,4vw,54px)}
header{padding:22px 0;border-bottom:2px solid #bedce1}
h1{line-height:1.15;font-size:clamp(30px,3.2vw,44px)}
.alert{background:#fff7df;border:1px solid #edc773;border-radius:12px;padding:16px 18px}
.links{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:15px;margin:24px 0}
.links a{display:block;text-decoration:none;color:#113e50;background:#fff;padding:21px;
border-radius:12px;border:1px solid #c4dce1;box-shadow:0 2px 8px #122c3b14}
.links a:focus-visible{outline:3px solid #b35d00}
small{color:#46606c;display:block;margin-top:7px}
</style></head><body><main>
<header><p>GRADE9 V4.0 · TECHNICAL PREVIEW</p>
<h1>Synthetic question reader</h1>
<p>Public-safe interaction test · Optimized for 12.7-inch screens</p></header>
<p class="alert"><strong>Not an exam or academic release.</strong>
All four questions are synthetic software fixtures, not original examination
questions. One deliberately missing diagram is withheld. No Physics, QRT,
or learner assessment approval is claimed.</p>
<div class="links">
<a href="preview/question-status.html"><strong>Combined synthetic reader</strong>
<small>Four synthetic questions, two topics, duplicate legacy IDs</small></a>
<a href="modules/alpha/question-status.html"><strong>Topic Alpha</strong>
<small>Two synthetic questions, including one test SVG</small></a>
<a href="modules/beta/question-status.html"><strong>Topic Beta</strong>
<small>Two synthetic questions; missing-figure HOLD demonstration</small></a></div>
<p>Technical source: <a href="https://github.com/reallakshman19/Grade9v4.0">
Grade9 v4.0 on GitHub</a>.</p>
</main></body></html>
"""


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def build_preview(out: Path) -> dict:
    out = out.absolute()
    if out.exists() or out.is_symlink() or out == ROOT or out.is_relative_to(ROOT / "workspace"):
        raise ValueError("OUTPUT_MUST_BE_NEW")
    with tempfile.TemporaryDirectory(prefix="g9-public-synthetic-") as temp:
        scratch = Path(temp)
        root, pins, built = fixture(scratch)
        source_receipt = build(root, built, pins)
        if source_receipt["record_count"] != 4 or source_receipt["module_count"] != 2 or source_receipt["missing_figures"] != 1:
            raise ValueError("SYNTHETIC_FIXTURE_CHANGED")
        if source_receipt["academic_approval"] != "HOLD" or source_receipt["release_authority"] != "HOLD":
            raise ValueError("ACADEMIC_GATE_CHANGED")
        stage = scratch / "site"
        stage.mkdir()
        for path in PAGES:
            raw = (built / path).read_bytes()
            text = raw.decode("utf-8")
            if text.count(ROOT_MARKER) != 1:
                raise ValueError("SYNTHETIC_DATA_MISSING")
            data = json.loads(text.split(ROOT_MARKER, 1)[1].split(END_MARKER, 1)[0])
            if not data["questions"] or any(not str(q.get("stem", "")).startswith("Synthetic ") for q in data["questions"]):
                raise ValueError("NON_SYNTHETIC_QUESTION_BLOCKED")
            if "g9-reader-12p7-layout" not in text or "NOT FOR PUBLICATION" not in text:
                raise ValueError("PREVIEW_CONTRACT_MISSING")
            dst = stage / path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
        (stage / "index.html").write_text(HUB, encoding="utf-8")
        (stage / ".nojekyll").write_bytes(b"")
        files = sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())
        allowed = {".nojekyll", "index.html", *PAGES}
        if set(files) != allowed:
            raise ValueError("PUBLIC_ALLOWLIST_MISMATCH")
        manifest = {"status":"SYNTHETIC_TECHNICAL_ONLY",
                    "academic_approval":"HOLD",
                    "candidate_50_record_published":False,
                    "files":{f:digest((stage / f).read_bytes()) for f in files}}
        (stage / "PUBLIC_PREVIEW_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(stage, out)
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    result = build_preview(args.out)
    print("PASS synthetic public preview: 4 questions, files=" + str(len(result["files"])))


if __name__ == "__main__":
    main()
