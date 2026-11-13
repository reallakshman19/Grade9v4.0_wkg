#!/usr/bin/env python3
"""Private owner-ZIP -> public-safe identity-map byte reproducibility verifier.

Never extracts the ZIP or publishes exam question text/answers. Requires a
separately supplied private ZIP, checks the complete owner-pinned archive and
manifest, then compares each full question's SHA256 with the metadata-only
tracked map. This is NOT proof that papers/keys are official or rights cleared.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
from zipfile import ZipFile, BadZipFile

from nsejs_pcb_identity_map import load, PIN


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def category(slug):
    if slug.startswith("bio-") or "-biology-" in slug:
        return "BIOLOGY"
    if slug.startswith("chem-") or "-chemistry-" in slug:
        return "CHEMISTRY"
    if slug.startswith("math-"):
        return "MATHEMATICS"
    return "PHYSICS"


def verify(archive: Path, *, root: Path):
    if not archive.is_file() or digest(archive.read_bytes()) != PIN:
        raise ValueError("OWNER_ZIP_SHA256_MISMATCH")
    public = load(root=root)
    by_uid = {r["question_uid"]: r for r in public["questions"]}
    by_mod = {m["slug"]: m for m in public["modules"]}
    seen = set()
    year_rows = 0
    with ZipFile(archive) as zipped:
        infos = zipped.infolist()
        names = [i.filename for i in infos]
        if (len(infos) != 210 or len(set(names)) != len(names) or
                sum(i.file_size for i in infos) > 15_000_000 or
                any(not i.filename or i.filename.startswith("/") or
                    "\\" in i.filename or ".." in i.filename.split("/") or
                    stat.S_ISLNK(i.external_attr >> 16) for i in infos)):
            raise ValueError("PRIVATE_ARCHIVE_INVALID_OR_UNSAFE")
        manifest = json.loads(zipped.read("MANIFEST.json"))
        if len(manifest) != 208 or len({x["archive_path"] for x in manifest}) != 208:
            raise ValueError("OWNER_MANIFEST_INVALID")
        for entry in manifest:
            p = entry["archive_path"]
            value = zipped.read(p)
            if digest(value) != entry["sha256"] or len(value) != entry["bytes"]:
                raise ValueError("OWNER_MANIFEST_MEMBER_HASH_INVALID:" + p)
        if set(names) - {e["archive_path"] for e in manifest} - {"MANIFEST.json", "README.md"}:
            raise ValueError("OWNER_MANIFEST_UNLISTED_MEMBER")
        banks = sorted(p for p in names
                       if re.fullmatch(r"individual_banks/[^/]+/bank.json", p))
        if len(banks) != 47:
            raise ValueError("OWNER_ARCHIVE_47_BANKS_EXPECTED")
        for path in banks:
            slug = path.split("/")[1]
            if category(slug) == "MATHEMATICS":
                continue
            module = by_mod.get(slug)
            raw = zipped.read(path)
            if not module or digest(raw) != module["source_bank_sha256"] or (
                    module["subject"] != category(slug)):
                raise ValueError("BANK_BYTES_OR_MODULE_SUBJECT_MISMATCH:" + slug)
            bank = json.loads(raw)
            if len(bank["questions"]) != module["question_count"]:
                raise ValueError("BANK_QUESTION_COUNT_MISMATCH:" + slug)
            for i, question in enumerate(bank["questions"], 1):
                uid = f'g9:pcb:{module["subject"].lower()}:{slug}:{i:03d}'
                row = by_uid.get(uid)
                if (not row or uid in seen or
                        question["id"] != row["claimed_external_question_id"] or
                        digest(canonical(question)) != row["content_revision_sha256"]):
                    raise ValueError("EXACT_QUESTION_BYTES_OR_ALIAS_MISMATCH:" + uid)
                seen.add(uid)
                year_rows += row["source_year_claim"] is not None
    if len(seen) != 267 or seen != set(by_uid):
        raise ValueError("267_QUESTION_OCCURRENCES_NOT_EXHAUSTIVE")
    return {
        "status": "PRIVATE_OWNER_BYTES_MATCH_CANONICAL_METADATA",
        "archive_sha256": PIN,
        "verified_owner_manifest_members": 208,
        "pcb_bank_count": 45,
        "pcb_question_occurrences": len(seen),
        "module_year_claimed_question_rows": year_rows,
        "original_exam_admission": "HOLD",
        "rights": "HOLD",
        "independent_qrt": "NOT_RUN",
        "source_figures_and_keys_verified": False,
        "question_text_placed_in_public_repo": False,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", required=True, type=Path)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    try:
        result = verify(args.zip, root=args.root)
        if args.report:
            args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, OSError, BadZipFile, KeyError, json.JSONDecodeError) as exc:
        print("PCB_OWNER_SOURCE_REPLAY_HOLD:", exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
