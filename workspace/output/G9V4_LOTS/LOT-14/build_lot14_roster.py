"""
Grade9 v4.0 — Lot 14 Roster Freezing Script.
Selects the final 5 in-scope WPE candidates (Q61–Q65) from Lot 00 ledger:
  - JEE-2026-04-06-S1-Q28 (Q61)
  - JEE-2026-04-02-S2-Q31 (Q62)
  - JEE-2026-04-04-S1-Q49 (Q63)
  - WEP07-02 (Q64)
  - WEP07-03 (Q65)
Asserts no overlap with Lots 02–13 (Batches A, B, C, D) or Lot 01 bridge (EX-M39).
Saves to workspace/output/G9V4_LOTS/LOT-14/ROSTER_PRIVATE.json.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("D:/CodeD/grade9v4")
LOT_DIR = ROOT / "workspace/output/G9V4_LOTS/LOT-14"
LOT_DIR.mkdir(parents=True, exist_ok=True)
ROSTER_PATH = LOT_DIR / "ROSTER_PRIVATE.json"

LEDGER_PATH = ROOT / "workspace/output/G9V4_LOTS/LOT-00/source-index-private.json"
REGISTRY_PATH = ROOT / "workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data/registry.json"

with open(LEDGER_PATH, encoding="utf-8") as f:
    ledger = json.load(f)

with open(REGISTRY_PATH, encoding="utf-8") as f:
    registry = json.load(f)

reg_by_id = {r["id"]: r for r in registry["records"]}
ledger_by_id = {r["id"]: r for r in ledger["records"]}

# Gather all previous candidate IDs across Batch A, B, C, D and Lot 01
prior_ids = set()
prior_ids.add("EX-M39") # Lot 01 bridge

for batch in ["BATCH-A", "BATCH-B", "BATCH-C", "BATCH-D"]:
    batch_roster_path = ROOT / f"workspace/output/G9V4_LOTS/{batch}/ROSTER_PRIVATE.json"
    with open(batch_roster_path, encoding="utf-8") as f:
        bdata = json.load(f)
    for r in bdata["roster"]:
        prior_ids.add(r["source_id"])

assert len(prior_ids) == 61, f"Expected 61 prior IDs (15*4 + 1), found {len(prior_ids)}"

target_ids = [
    "JEE-2026-04-06-S1-Q28",
    "JEE-2026-04-02-S2-Q31",
    "JEE-2026-04-04-S1-Q49",
    "WEP07-02",
    "WEP07-03"
]

# Assert no overlap
for sid in target_ids:
    assert sid not in prior_ids, f"Overlap detected: {sid} is already in prior batches!"
    assert sid in ledger_by_id, f"Candidate {sid} missing from Lot 00 ledger!"

roster_records = []
for idx_0based, sid in enumerate(target_ids):
    cum_seq = 61 + idx_0based
    lot_seq = 1 + idx_0based
    lrec = ledger_by_id[sid]
    reg_rec = reg_by_id.get(sid, {})

    stem_raw = reg_rec.get("stem")
    if stem_raw:
        stem_sha = hashlib.sha256(stem_raw.encode("utf-8")).hexdigest()
        stem_prev = stem_raw[:120].replace("\n", " ")
    else:
        stem_sha = None
        stem_prev = "[UNBOUND_REGISTRY_STEM] Exact question text not bound in registry.json; pending external witness."

    roster_records.append({
        "sequence": cum_seq,
        "lot_sequence": lot_seq,
        "lot": "LOT-14",
        "source_id": sid,
        "registry_index": lrec["index"],
        "task_identity": lrec["exact_task_identity"],
        "paper": lrec["paper"],
        "origin": lrec["origin"],
        "scope": lrec["scope"],
        "figure_status": lrec["figure_status"],
        "stem_binding": lrec.get("stem_binding", "BOUND_IN_REGISTRY" if stem_raw else "TEXT_NOT_BOUND_IN_REGISTRY"),
        "stem_sha256": stem_sha,
        "stem_preview": stem_prev,
        "academic_admission": "NOT_ADMITTED",
        "admission_gate": "HOLD:ACADEMIC_ADMISSION"
    })

canonical_roster_json = json.dumps(roster_records, sort_keys=True, ensure_ascii=False)
roster_items_sha = hashlib.sha256(canonical_roster_json.encode("utf-8")).hexdigest()

roster_doc = {
    "lot_id": "LOT-14",
    "title": "Grade9 v4.0 — Lot 14 Frozen Roster (Final Five WPE In-Scope Candidates Q61–Q65)",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "roster_sha256": roster_items_sha,
    "total_candidates": len(roster_records),
    "sequence_range": [61, 65],
    "lot_sequence_range": [1, 5],
    "provenance_policy": "FAIL_CLOSED_NO_AUTOMATIC_ADMISSION",
    "academic_admission": "NOT_ADMITTED",
    "roster": roster_records
}

with open(ROSTER_PATH, "w", encoding="utf-8") as f:
    json.dump(roster_doc, f, indent=2, ensure_ascii=False)

file_bytes = ROSTER_PATH.read_bytes()
file_sha = hashlib.sha256(file_bytes).hexdigest()

print("LOT 14 ROSTER FROZEN (PASS):")
print(f"  Path: {ROSTER_PATH}")
print(f"  File Size: {len(file_bytes)} bytes")
print(f"  File SHA-256: {file_sha}")
print(f"  Embedded Items SHA-256: {roster_items_sha}")
for rec in roster_records:
    print(f"    Q{rec['sequence']:02d} (Lot #{rec['lot_sequence']:02d}): {rec['source_id']} | {rec['paper']} | stem_sha={rec['stem_sha256']}")
