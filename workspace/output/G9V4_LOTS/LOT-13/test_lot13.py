"""
Test suite for Grade9 v4.0 — Lot 13 (Questions 56–60, Batch D, CP-3).
"""

import os
import json
import hashlib
import unittest

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_PATH = os.path.join(LOT_DIR, "ROSTER_PRIVATE.json")

EXPECTED_ROSTER_FILE_SHA = "dcc00afecf9c8688266d77672131148969a6dda39923510c141a3ca7c294662c"
EXPECTED_ROSTER_ITEMS_SHA = "dddb5121e835f34315e4600db5af327927c14b5ce3b5e06fc4c35329fe591b2d"
EXPECTED_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
EXPECTED_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"
EXPECTED_LOT13_SOURCES = ["AN-3", "AN-5", "AN-6", "JEE-2026-04-04-S1-Q46", "JEE-2026-04-06-S2-Q29"]

class TestLot13(unittest.TestCase):
    def test_01_roster_integrity(self):
        self.assertTrue(os.path.isfile(ROSTER_PATH))
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA)

        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(data["total_candidates"], 15)
        lot13_items = [r for r in data["roster"] if r["lot"] == "LOT-13"]
        self.assertEqual(len(lot13_items), 5)
        source_ids = [r["source_id"] for r in lot13_items]
        self.assertEqual(source_ids, EXPECTED_LOT13_SOURCES)

    def test_02_review_dashboard(self):
        review_html = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(review_html))
        with open(review_html, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("No academic approval inferred from software validation.", html)
        self.assertIn("HOLD_BASE_NOT_READY", html)
        for sid in EXPECTED_LOT13_SOURCES:
            self.assertIn(sid, html)

    def test_03_question_audit_records(self):
        for idx, expected_source in enumerate(EXPECTED_LOT13_SOURCES, 56):
            q_file = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_file))
            with open(q_file, encoding="utf-8") as f:
                rec = json.load(f)

            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-13")
            self.assertEqual(rec["batch"], "BATCH-D")
            self.assertEqual(rec["academic_admission"], "NOT_ADMITTED")
            self.assertEqual(rec["admission_gate"], "HOLD:ACADEMIC_ADMISSION")
            self.assertEqual(rec["core2_status"], "NOT_RUN")
            self.assertEqual(rec["solve_exposure"], "EXPOSED")

            # CBSE vs NTA authority check
            if expected_source == "AN-5":
                self.assertEqual(rec["key_issuing_authority"], "CBSE")
            else:
                self.assertEqual(rec["key_issuing_authority"], "NTA")

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
        for idx in range(56, 61):
            s_file = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_file))
            with open(s_file, encoding="utf-8") as f:
                rec = json.load(f)
            self.assertIn("confidentiality_notice", rec)
            for fk in forbidden_keys:
                self.assertNotIn(fk, rec)

    def test_05_candidate_solves(self):
        # AN-3 (Q56): Option B
        with open(os.path.join(LOT_DIR, "questions", "56", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q56 = json.load(f)
        self.assertTrue(q56["candidate_solve"]["predicted_option"].startswith("B:"))

        # AN-5 (Q57): Option A
        with open(os.path.join(LOT_DIR, "questions", "57", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q57 = json.load(f)
        self.assertTrue(q57["candidate_solve"]["predicted_option"].startswith("A:"))

        # AN-6 (Q58): Option A
        with open(os.path.join(LOT_DIR, "questions", "58", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q58 = json.load(f)
        self.assertTrue(q58["candidate_solve"]["predicted_option"].startswith("A:"))

        # JEE-2026-04-04-S1-Q46 (Q59): 35
        with open(os.path.join(LOT_DIR, "questions", "59", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q59 = json.load(f)
        self.assertEqual(q59["candidate_solve"]["predicted_option"], "35")

        # JEE-2026-04-06-S2-Q29 (Q60): 1250 / 6911214180
        with open(os.path.join(LOT_DIR, "questions", "60", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q60 = json.load(f)
        self.assertTrue("6911214180" in q60["candidate_solve"]["predicted_option"])
        self.assertTrue("1250" in q60["candidate_solve"]["predicted_option"])

if __name__ == "__main__":
    unittest.main()
