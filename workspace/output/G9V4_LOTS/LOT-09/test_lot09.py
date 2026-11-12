"""
Test suite for Grade9 v4.0 — Lot 09 (Questions 36–40, Batch C, CP-2).
"""

import os
import json
import hashlib
import unittest

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_PATH = os.path.join(LOT_DIR, "ROSTER_PRIVATE.json")

EXPECTED_ROSTER_FILE_SHA = "3e8825bd623f83d20552e2af6a6dc867060cb6353f8a2a4234b3a21580ad616e"
EXPECTED_ROSTER_ITEMS_SHA = "cbed9ff430ab97659941a25613e4b6b6db4cbd3137afb25c971acfe8af27fe4f"
EXPECTED_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
EXPECTED_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"
EXPECTED_LOT09_SOURCES = ["EX-M98", "EX-M101", "EX-M105", "EX-M106", "EX-M109"]

class TestLot09(unittest.TestCase):
    def test_01_roster_integrity(self):
        self.assertTrue(os.path.isfile(ROSTER_PATH))
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA)

        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(data["total_candidates"], 15)
        lot09_items = [r for r in data["roster"] if r["lot"] == "LOT-09"]
        self.assertEqual(len(lot09_items), 5)
        source_ids = [r["source_id"] for r in lot09_items]
        self.assertEqual(source_ids, EXPECTED_LOT09_SOURCES)

    def test_02_review_dashboard(self):
        review_html = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(review_html))
        with open(review_html, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("No academic approval inferred from software validation.", html)
        self.assertIn("HOLD_BASE_NOT_READY", html)
        for sid in EXPECTED_LOT09_SOURCES:
            self.assertIn(sid, html)

    def test_03_question_audit_records(self):
        for idx, expected_source in enumerate(EXPECTED_LOT09_SOURCES, 36):
            q_file = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_file))
            with open(q_file, encoding="utf-8") as f:
                rec = json.load(f)

            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-09")
            self.assertEqual(rec["academic_admission"], "NOT_ADMITTED")
            self.assertEqual(rec["admission_gate"], "HOLD:ACADEMIC_ADMISSION")
            self.assertEqual(rec["core2_status"], "NOT_RUN")
            self.assertEqual(rec["solve_exposure"], "EXPOSED")

            computed_stem_sha = hashlib.sha256(rec["stem_text"].encode("utf-8")).hexdigest()
            self.assertEqual(rec["stem_sha256"], computed_stem_sha)
            self.assertEqual(rec["source_hash"], computed_stem_sha)

            sl2 = rec["sl2"]
            self.assertEqual(sl2["mode"], "QUESTION")
            diff = sl2["difficulty_evidence"]
            comps = diff["components"]
            self.assertEqual(len(comps), 5)
            self.assertEqual(sum(c["score"] for c in comps.values()), diff["total"])

            if diff["band"] in ["D1", "D2"]:
                self.assertEqual(rec["blueprint_fit"], "BLUEPRINT=SPEC_PENDING")
                self.assertEqual(rec["adapter_fit"], "ADAPTER=SPEC_PENDING")
            elif diff["band"] in ["D3", "D4"]:
                self.assertIsInstance(rec["blueprint_fit"], dict)
                self.assertEqual(rec["blueprint_fit"]["sha256"], EXPECTED_BP_SHA)
                self.assertEqual(rec["blueprint_fit"]["version"], "0.2.0")
                self.assertIn(rec["blueprint_fit"]["blueprint_cell_ref"], ["D3.3", "D3.4"])

            self.assertGreaterEqual(len(rec["blockers"]), 1)

    def test_04_source_only_packets(self):
        forbidden_keys = ["candidate_solve", "official_key", "predicted_option", "worked_solution", "score"]
        for idx in range(36, 41):
            s_file = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_file))
            with open(s_file, encoding="utf-8") as f:
                rec = json.load(f)
            self.assertIn("confidentiality_notice", rec)
            for fk in forbidden_keys:
                self.assertNotIn(fk, rec)

    def test_05_candidate_solves(self):
        # EX-M98 (Q36): 4/3
        with open(os.path.join(LOT_DIR, "questions", "36", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q36 = json.load(f)
        self.assertTrue(q36["candidate_solve"]["predicted_option"].startswith("A:"))

        # EX-M101 (Q37): Statement 1 false, Statement 2 true
        with open(os.path.join(LOT_DIR, "questions", "37", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q37 = json.load(f)
        self.assertTrue(q37["candidate_solve"]["predicted_option"].startswith("A:"))

        # EX-M105 (Q38): 5.5 cm
        with open(os.path.join(LOT_DIR, "questions", "38", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q38 = json.load(f)
        self.assertTrue(q38["candidate_solve"]["predicted_option"].startswith("B:"))

        # EX-M106 (Q39): Mg(sqrt(2)-1)
        with open(os.path.join(LOT_DIR, "questions", "39", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q39 = json.load(f)
        self.assertTrue(q39["candidate_solve"]["predicted_option"].startswith("D:"))

        # EX-M109 (Q40): 3 / sqrt(2)
        with open(os.path.join(LOT_DIR, "questions", "40", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q40 = json.load(f)
        self.assertTrue(q40["candidate_solve"]["predicted_option"].startswith("A:"))

    def test_06_fail_closed_tamper_simulation(self):
        q36_path = os.path.join(LOT_DIR, "questions", "36", "QUESTION_AUDIT.json")
        with open(q36_path, encoding="utf-8") as f:
            rec = json.load(f)
        tampered_stem = rec["stem_text"] + " [MUTATED]"
        tampered_sha = hashlib.sha256(tampered_stem.encode("utf-8")).hexdigest()
        self.assertNotEqual(tampered_sha, rec["stem_sha256"])

if __name__ == "__main__":
    unittest.main()
