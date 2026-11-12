import os
import json
import zipfile
import hashlib
from datetime import datetime, timezone

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(LOT_DIR, "LOT-07-PRIVATE-REVIEW.zip")

sibling_files = [
    "ROSTER_PRIVATE.json",
    "LOT07_TEST.log",
    "review/index.html",
    "questions/26/QUESTION_AUDIT.json",
    "questions/27/QUESTION_AUDIT.json",
    "questions/28/QUESTION_AUDIT.json",
    "questions/29/QUESTION_AUDIT.json",
    "questions/30/QUESTION_AUDIT.json",
    "source_only/26/SOURCE_ONLY.json",
    "source_only/27/SOURCE_ONLY.json",
    "source_only/28/SOURCE_ONLY.json",
    "source_only/29/SOURCE_ONLY.json",
    "source_only/30/SOURCE_ONLY.json",
    "test_lot07.py",
    "verify_lot07_viewport.js"
]

def build_manifest():
    manifest_entries = []
    for rel in sibling_files:
        fpath = os.path.join(LOT_DIR, rel.replace("/", os.sep))
        assert os.path.isfile(fpath), f"Missing required sibling file: {fpath}"
        data = open(fpath, "rb").read()
        manifest_entries.append({
            "path": rel,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()
        })

    manifest_data = {
        "batch_id": "BATCH-B",
        "lot_id": "LOT-07",
        "title": "Grade9 v4.0 — Lot 07 Self-Contained Review Package (Candidates 26-30)",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "roster_sha256": "df05237bc3a7e8a0df0a0e395f6d2e85ad0750eaba4cf110d26e52b59162a3c6",
        "total_archive_members": 16,
        "manifested_sibling_files_count": len(manifest_entries),
        "runtime_dependencies": {
            "python": ">=3.11 (tested on Python 3.14.0)",
            "python_packages": ["pytest", "jsonschema"],
            "node": ">=v18 (tested on Node v22.23.2)",
            "playwright": "playwright-core with chromium (local or C:/Users/reall/AppData/Local/Temp/pw-1.52.0/node_modules/playwright-core)",
            "os": "Windows 11 (build 26100)",
            "shell": "PowerShell 5.1 / 7"
        },
        "files": manifest_entries
    }

    manifest_path = os.path.join(LOT_DIR, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Generated MANIFEST.json with {len(manifest_entries)} sibling entries.")
    return manifest_path, manifest_data

def package_zip():
    manifest_path, manifest_data = build_manifest()

    all_files_to_pack = [("MANIFEST.json", manifest_path)]
    for rel in sibling_files:
        fpath = os.path.join(LOT_DIR, rel.replace("/", os.sep))
        all_files_to_pack.append((rel, fpath))

    assert len(all_files_to_pack) == 16, f"Expected exactly 16 files, got {len(all_files_to_pack)}"

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, fpath in all_files_to_pack:
            zf.write(fpath, arcname=arcname)

    zip_bytes = open(ZIP_PATH, "rb").read()
    zip_sha = hashlib.sha256(zip_bytes).hexdigest()
    print(f"Created: {ZIP_PATH}")
    print(f"Size: {len(zip_bytes)} bytes | SHA-256: {zip_sha}")

    # Integrity verification
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        namelist = zf.namelist()
        print(f"Archive contains {len(namelist)} entries (expected 16):")
        assert len(namelist) == 16, f"Archive member count mismatch: {len(namelist)}"
        for name in namelist:
            info = zf.getinfo(name)
            print(f"  {info.filename} ({info.file_size} bytes)")

    return zip_sha, len(zip_bytes)

if __name__ == "__main__":
    package_zip()
