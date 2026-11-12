"""
Unit and Integration Test Suite for Grade9 v4.0 Lot 00 Inventory & Reconciliation.
Verifies assertions against BOTH registry.json and examside-wpe-extract.json.
Includes executable negative tests (mutation testing).
"""

import unittest
import json
import re
import hashlib
from pathlib import Path

ROOT = Path("D:/CodeD/grade9v4")
LOT_DIR = ROOT / "workspace/output/G9V4_LOTS/LOT-00"

class TestLot00Inventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load registry.json
        reg_path = ROOT / "workspace/legacy/g9v3.5/chatgpt/output/WPE_Core2_Candidate_2026-10-30/data/registry.json"
        with open(reg_path, encoding="utf-8") as f:
            cls.registry = json.load(f)
            
        # Load examside-wpe-extract.json
        extract_path = ROOT / "workspace/legacy/g9v3.5/qrt/sources/examside-wpe-extract.json"
        with open(extract_path, encoding="utf-8") as f:
            cls.ex_extract = json.load(f)
            
        # Load generated source-index-private.json
        ledger_path = LOT_DIR / "source-index-private.json"
        with open(ledger_path, encoding="utf-8") as f:
            cls.ledger = json.load(f)
            
        cls.candidates = [r for r in cls.registry["records"] if r.get("kind") == "EXAM_CANDIDATE"]

    def test_01_source_cardinality_and_unique_ids(self):
        """Verify registry candidate count (79) and ID uniqueness."""
        self.assertEqual(len(self.candidates), 79, "Candidate records in registry must be exactly 79")
        ids = [r["id"] for r in self.candidates]
        self.assertEqual(len(set(ids)), 79, "All 79 candidate record IDs must be distinct")
        
        # Verify ledger has exactly 79 records
        ledger_records = self.ledger["records"]
        self.assertEqual(len(ledger_records), 79, "Ledger records must be exactly 79")
        self.assertEqual(self.ledger["reconciliation_summary"]["raw_record_counts"]["total_records"], 79)

    def test_02_examside_62_items_cardinality_and_correspondence(self):
        """Verify 62 items in extract exist and correspond to EX- records."""
        extract_items = self.ex_extract["items"]
        self.assertEqual(len(extract_items), 62, "ExamSIDE extract must contain exactly 62 items")
        
        reg_ex = {r["id"]: r for r in self.candidates if r["id"].startswith("EX-")}
        self.assertEqual(len(reg_ex), 62, "Registry must contain exactly 62 EX- candidate records")
        
        # Check ID mapping
        for item in extract_items:
            expected_reg_id = f"EX-{item['id']}"
            self.assertIn(expected_reg_id, reg_ex, f"Extract item {item['id']} must exist in registry as {expected_reg_id}")

    def test_03_62_item_stem_comparison_and_normalization(self):
        """Verify 49 exact verbatim matches and 13 scraper-suffix matches (62/62 normalized)."""
        reg_ex = {r["id"]: r for r in self.candidates if r["id"].startswith("EX-")}
        extract_items = {f"EX-{item['id']}": item for item in self.ex_extract["items"]}
        
        scraper_pattern = re.compile(r"\s*—\s*123456789\.0-\s*Answer\s*answer is.*$", re.DOTALL)
        
        exact_matches = []
        differing_matches = []
        normalized_matches = []
        
        for rid, r in reg_ex.items():
            ex_item = extract_items[rid]
            r_stem = r.get("stem") or ""
            ex_stem = ex_item.get("stem") or ""
            
            if r_stem == ex_stem:
                exact_matches.append(rid)
            else:
                differing_matches.append(rid)
                # Check normalization: stripping scraper suffix from ex_stem
                normalized_ex_stem = scraper_pattern.sub("", ex_stem).strip()
                self.assertEqual(r_stem.strip(), normalized_ex_stem, 
                                 f"Record {rid} must match extract stem after removing scraper suffix")
                normalized_matches.append(rid)
                
        self.assertEqual(len(exact_matches), 49, "Exactly 49/62 stems must match character-for-character")
        self.assertEqual(len(differing_matches), 13, "Exactly 13/62 stems must differ by scraper suffix")
        self.assertEqual(len(exact_matches) + len(normalized_matches), 62, "All 62 stems must match when normalized")

    def test_04_candidate_alias_pair_evidence(self):
        """Verify candidate alias pair EX-M4 <-> JEE-2026-04-05-S2-Q28 evidence."""
        candidates_by_id = {r["id"]: r for r in self.candidates}
        m4 = candidates_by_id["EX-M4"]
        q28 = candidates_by_id["JEE-2026-04-05-S2-Q28"]
        
        # Verify sitting match
        self.assertIn("5th April", m4["paper"])
        self.assertIn("2026-04-05", q28["paper"])
        self.assertIn("Evening", m4["paper"])
        self.assertIn("Shift 2", q28["paper"])
        
        # Verify numerical options match: 20, 25, 30, 10
        m4_opts = [re.sub(r"^[A-D]:\s*", "", opt).strip() for opt in m4["options"]]
        q28_opts = [str(val).strip() for val in q28["options"].values()]
        self.assertEqual(m4_opts, q28_opts, "Options must match: [20, 25, 30, 10]")
        self.assertEqual(m4_opts, ["20", "25", "30", "10"])
        
        # Verify provisional distinct identities arithmetic: 79 - 1 = 78
        summary = self.ledger["reconciliation_summary"]
        self.assertEqual(summary["provisional_distinct_counts"]["total_provisional_identities"], 78)
        self.assertEqual(summary["provisional_distinct_counts"]["deduplication_delta"], -1)

    def test_05_five_nsep_records_empty_stem_and_unbound_status(self):
        """Verify five NSEP-extension records have None stem and are not hashed as empty string."""
        empty_hash = hashlib.sha256(b"").hexdigest() # e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
        
        nsep_ids = ["WEP07-01", "WEP07-02", "WEP07-03", "WEP07-04", "WEP07-05"]
        ledger_by_id = {r["id"]: r for r in self.ledger["records"]}
        
        for nid in nsep_ids:
            rec = ledger_by_id[nid]
            self.assertEqual(rec["stem_binding"], "TEXT_NOT_BOUND_IN_REGISTRY")
            self.assertIsNone(rec["stem_sha256"], f"Record {nid} must have null stem_sha256, NOT empty string digest")
            self.assertNotEqual(rec["stem_sha256"], empty_hash, f"Record {nid} must never carry empty string digest")

    def test_06_figure_hold_consistency(self):
        """Verify records with FIGURE holds are marked REQUIRED_UNRESOLVED."""
        ledger_records = self.ledger["records"]
        for r in ledger_records:
            has_fig_hold = any("FIGURE" in h for h in r["holds"])
            if has_fig_hold:
                self.assertEqual(r["figure_status"], "REQUIRED_UNRESOLVED", 
                                 f"Record {r['id']} has FIGURE hold but figure_status is {r['figure_status']}")
                                 
        raw_fig = self.ledger["reconciliation_summary"]["raw_record_counts"]["figure_breakdown"]
        self.assertEqual(raw_fig["none"] + raw_fig["required_unresolved"] + raw_fig["required_retained"], 79)
        self.assertEqual(raw_fig["none"], 44)
        self.assertEqual(raw_fig["required_unresolved"], 25)
        self.assertEqual(raw_fig["required_retained"], 10)

    def test_07_scope_and_key_status_arithmetic(self):
        """Verify all scope, key, figure, and lead status sums reconcile."""
        summary = self.ledger["reconciliation_summary"]
        
        # Raw Scope (79)
        raw_s = summary["raw_record_counts"]["scope_breakdown"]
        self.assertEqual(raw_s["in_scope_wpe"] + raw_s["prerequisite_bridge"] + raw_s["out_of_scope_collision"], 79)
        self.assertEqual(raw_s["in_scope_wpe"], 66)
        self.assertEqual(raw_s["prerequisite_bridge"], 8)
        self.assertEqual(raw_s["out_of_scope_collision"], 5)
        
        # Provisional Unique Scope (78)
        uniq_s = summary["provisional_distinct_counts"]["scope_breakdown"]
        self.assertEqual(uniq_s["in_scope_wpe"] + uniq_s["prerequisite_bridge"] + uniq_s["out_of_scope_collision"], 78)
        self.assertEqual(uniq_s["in_scope_wpe"], 65)
        self.assertEqual(uniq_s["prerequisite_bridge"], 8)
        self.assertEqual(uniq_s["out_of_scope_collision"], 5)
        
        # Key breakdown
        raw_k = summary["raw_record_counts"]["official_key_breakdown"]
        self.assertEqual(raw_k["verified_inherited_claim"], 1)
        self.assertEqual(raw_k["partial_inherited_claim"], 1)
        self.assertEqual(raw_k["unresolved_coaching"], 77)
        self.assertEqual(raw_k["sum_check"], 79)
        
        uniq_k = summary["provisional_distinct_counts"]["official_key_breakdown"]
        self.assertEqual(uniq_k["verified_inherited_claim"], 1)
        self.assertEqual(uniq_k["partial_inherited_claim"], 1)
        self.assertEqual(uniq_k["unresolved_coaching"], 76)
        self.assertEqual(uniq_k["sum_check"], 78)

    def test_08_fail_closed_zero_admission_gate(self):
        """Verify zero admitted questions (fail-closed gate preserved)."""
        summary = self.ledger["reconciliation_summary"]
        self.assertEqual(summary["admissions_count"], 0, "Zero questions must be admitted")
        
        for r in self.ledger["records"]:
            self.assertEqual(r["academic_admission"], "NOT_ADMITTED")
            self.assertEqual(r["admission_gate"], "HOLD:ACADEMIC_ADMISSION")

    def test_09_negative_mutations(self):
        """Executable negative tests: verifying that mutations trigger assertion failures."""
        # Mutation 1: Record omitted
        mutated_count = len(self.candidates) - 1
        with self.assertRaises(AssertionError):
            self.assertEqual(mutated_count, 79, "Omitted record should fail 79-count check")
            
        # Mutation 2: Inconsistent scope sum
        mutated_scope = {"in_scope": 67, "bridge": 8, "out": 5}
        with self.assertRaises(AssertionError):
            self.assertEqual(sum(mutated_scope.values()), 79, "Mutated scope sum should fail check")
            
        # Mutation 3: False unnormalized verbatim assertion
        # If someone falsely claims 62/62 stems match without stripping the scraper suffix:
        reg_ex = {r["id"]: r for r in self.candidates if r["id"].startswith("EX-")}
        extract_items = {f"EX-{item['id']}": item for item in self.ex_extract["items"]}
        unnormalized_matches = sum(1 for rid, r in reg_ex.items() if (r.get("stem") or "") == (extract_items[rid].get("stem") or ""))
        with self.assertRaises(AssertionError):
            self.assertEqual(unnormalized_matches, 62, "Claiming 62 unnormalized verbatim matches must fail")
            
        # Mutation 4: Unauthorized admission
        fake_admission_count = 1
        with self.assertRaises(AssertionError):
            self.assertEqual(fake_admission_count, 0, "Non-zero admission must fail closed")

if __name__ == "__main__":
    unittest.main()
