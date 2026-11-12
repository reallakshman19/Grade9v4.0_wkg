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
from build_public_site_pages import PUBLIC_SHELL_FILES, write_shell

PAGES = (
    "preview/question-status.html",
    "modules/alpha/question-status.html",
    "modules/beta/question-status.html",
)

# The original four-question synthetic reader is retained under /preview;
# the site root is now the explicitly allowlisted school/NSEJS learning hub.


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
        write_shell(stage)
        files = sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())
        allowed = {*PUBLIC_SHELL_FILES, *PAGES}
        if set(files) != allowed:
            raise ValueError("PUBLIC_ALLOWLIST_MISMATCH")
        manifest = {"status":"PUBLIC_SAFE_SUBJECT_HUB_WITH_SYNTHETIC_READER",
                    "source_question_published":False,
                    "nsejs_academic_approval":"HOLD",
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
    print("PASS public subject home + NSEJS + four synthetic reader questions, files=" + str(len(result["files"])))


if __name__ == "__main__":
    main()
