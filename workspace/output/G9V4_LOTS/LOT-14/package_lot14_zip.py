import os
import json
import zipfile
import hashlib
from datetime import datetime, timezone

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(LOT_DIR, "LOT-14-PRIVATE-REVIEW.zip")

sibling_files = [
    "ROSTER_PRIVATE.json",
    "LOT14_TEST.log",
    "review/index.html",
    "questions/61/QUESTION_AUDIT.json",
    "questions/62/QUESTION_AUDIT.json",
    "questions/63/QUESTION_AUDIT.json",
    "questions/64/QUESTION_AUDIT.json",
    "questions/65/QUESTION_AUDIT.json",
    "source_only/61/SOURCE_ONLY.json",
    "source_only/62/SOURCE_ONLY.json",
    "source_only/63/SOURCE_ONLY.json",
    "source_only/64/SOURCE_ONLY.json",
    "source_only/65/SOURCE_ONLY.json",
    "test_lot14.py",
    "verify_lot14_viewport.js"
]

def build_manifest():
    manifest_entries = []
    for rel in sibling_files:
        fpath = os.path.join(LOT_DIR, rel.replace("/", os.sep))
        assert os.path.isfile(fpath), f"Missing required sibling file: {fpath}"
        with open(fpath, "rb") as f:
            data = f.read()
        manifest_entries.append({
            "path": rel,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()
        })

    manifest_data = {
        "batch_id": "BATCH-D",
        "lot_id": "LOT-14",
        "title": "Grade9 v4.0 — Lot 14 Self-Contained Review Package (Candidates 61-65)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "roster_sha256": "3d82e62b6cf0aacad158a7487d93be1d8fa3d1aac43173d798ce7f8f1e842ed0",
        "total_archive_members": 16,
        "manifested_sibling_files_count": len(manifest_entries),
        "runtime_dependencies": {
            "python": ">=3.11",
            "python_packages": ["pytest", "jsonschema"],
            "node": ">=v18",
            "playwright": "playwright-core with chromium",
            "os": "Windows 11",
            "shell": "PowerShell 5.1 / 7"
        },
        "files": manifest_entries
    }

    manifest_path = os.path.join(LOT_DIR, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Generated MANIFEST.json with {len(manifest_entries)} sibling entries.")
    return manifest_path

def create_zip():
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    build_manifest()

    all_to_zip = sibling_files + ["MANIFEST.json"]

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in all_to_zip:
            fpath = os.path.join(LOT_DIR, rel.replace("/", os.sep))
            zf.write(fpath, arcname=rel)

    size = os.path.getsize(ZIP_PATH)
    with open(ZIP_PATH, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    print(f"Created: {ZIP_PATH}")
    print(f"Size: {size} bytes | SHA-256: {sha}")

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
        print(f"Archive contains {len(names)} entries (expected 16):")
        for n in names:
            info = zf.getinfo(n)
            print(f"  {n} ({info.file_size} bytes)")
        assert len(names) == 16, f"Expected 16 files, got {len(names)}"

if __name__ == "__main__":
    create_zip()
