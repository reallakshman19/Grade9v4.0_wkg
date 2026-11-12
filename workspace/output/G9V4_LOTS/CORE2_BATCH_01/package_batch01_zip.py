import os
import json
import zipfile
import hashlib
import subprocess
from datetime import datetime, timezone

BATCH_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(BATCH_DIR, "CORE2_BATCH_01_PRIVATE_REVIEW.zip")

print(">>> Step 1: Running unit tests and capturing BATCH01_TEST.log...")
cmd_unit = ["py", "-3.14", os.path.join(BATCH_DIR, "test_batch01.py"), "-v"]
res_unit = subprocess.run(cmd_unit, capture_output=True, text=True, cwd=BATCH_DIR)
log_unit_path = os.path.join(BATCH_DIR, "BATCH01_TEST.log")
with open(log_unit_path, "w", encoding="utf-8") as f:
    f.write(res_unit.stdout + "\n" + res_unit.stderr)
print(f"Unit test exit code: {res_unit.returncode}")
assert res_unit.returncode == 0, f"Unit tests failed:\n{res_unit.stderr}"

print(">>> Step 2: Running Playwright browser audit and capturing BATCH01_PLAYWRIGHT_TEST.log...")
cmd_pw = ["node", os.path.join(BATCH_DIR, "verify_batch01_playwright.js")]
res_pw = subprocess.run(cmd_pw, capture_output=True, text=True, cwd=BATCH_DIR)
log_pw_path = os.path.join(BATCH_DIR, "BATCH01_PLAYWRIGHT_TEST.log")
with open(log_pw_path, "w", encoding="utf-8") as f:
    f.write(res_pw.stdout + "\n" + res_pw.stderr)
print(f"Playwright exit code: {res_pw.returncode}")
assert res_pw.returncode == 0, f"Playwright audit failed:\n{res_pw.stderr}"

# Files to manifest and package
files_to_pack = [
    "bank/core2_batch01_bank.json",
    "rendered/core2_batch01.html",
    "assets/fig_q01_atwood.svg",
    "assets/fig_q03_bead_semicircle.svg",
    "assets/fig_q04_projectile_energy.svg",
    "assets/fig_q05_atwood_work.svg",
    "assets/fig_q06_potential_curve.svg",
    "assets/fig_q09_bead_wire_spring.svg",
    "assets/fig_q10_incline_block.svg",
    "assets/fig_q12_vertical_circle.svg",
    "assets/fig_q15_spring_two_blocks.svg",
    "test_batch01.py",
    "verify_batch01_playwright.js",
    "BATCH01_TEST.log",
    "BATCH01_PLAYWRIGHT_TEST.log"
]

manifest_entries = []
for rel in files_to_pack:
    fpath = os.path.join(BATCH_DIR, rel.replace("/", os.sep))
    assert os.path.isfile(fpath), f"Missing file: {fpath}"
    data = open(fpath, "rb").read()
    manifest_entries.append({
        "path": rel,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest()
    })

manifest_data = {
    "batch_id": "BATCH-01",
    "title": "Grade9 v4.0 — Work, Power & Energy Core 2 Review Package (Batch 1: Q01-Q15)",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "PHYSICS_WPE_PILOT",
    "total_questions": 15,
    "included_lots": ["LOT-02", "LOT-03", "LOT-04"],
    "academic_admission": "NOT_ADMITTED",
    "disposition": "HOLD:ACADEMIC_ADMISSION",
    "governance_notice": "No academic approval inferred from software validation. Green CI means automatic tests passed; it never means student release is authorized.",
    "total_manifested_files": len(manifest_entries),
    "runtime_dependencies": {
        "python": ">=3.11 (tested on Python 3.14.0)",
        "node": ">=v18 (tested on Node v22.23.2)",
        "playwright": "playwright-core with chromium",
        "os": "Windows 11 (build 26100)",
        "shell": "PowerShell 5.1 / 7"
    },
    "files": manifest_entries
}

manifest_path = os.path.join(BATCH_DIR, "MANIFEST.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)
print(f"Authored MANIFEST.json ({len(manifest_entries)} payload entries).")

# Package into ZIP archive
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
    z.write(manifest_path, "MANIFEST.json")
    for rel in files_to_pack:
        fpath = os.path.join(BATCH_DIR, rel.replace("/", os.sep))
        z.write(fpath, rel)

zip_bytes = os.path.getsize(ZIP_PATH)
with open(ZIP_PATH, "rb") as f:
    zip_sha = hashlib.sha256(f.read()).hexdigest()

print(f"Created sealed ZIP: {ZIP_PATH}")
print(f"ZIP Bytes: {zip_bytes} | SHA-256: {zip_sha}")

# Author detached receipt to avoid circularity
receipt = {
    "schema_version": "grade9v4-batch-receipt-v1",
    "batch_id": "BATCH-01",
    "archive_filename": "CORE2_BATCH_01_PRIVATE_REVIEW.zip",
    "archive_bytes": zip_bytes,
    "archive_sha256": zip_sha,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "academic_admission": "NOT_ADMITTED",
    "disposition": "HOLD:ACADEMIC_ADMISSION",
    "total_questions": 15,
    "manifest_file_count": len(manifest_entries) + 1 # includes MANIFEST.json in ZIP
}

receipt_path = os.path.join(BATCH_DIR, "BATCH01_ARCHIVE_RECEIPT.json")
with open(receipt_path, "w", encoding="utf-8") as f:
    json.dump(receipt, f, indent=2, ensure_ascii=False)

print(f"Authored detached receipt at: {receipt_path}")
print(">>> BATCH 1 PACKAGING AND SELF-CHECK COMPLETE <<<")
