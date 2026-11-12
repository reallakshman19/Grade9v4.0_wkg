"""
Test suite for Grade9 v4.0 — Lot 12 (Questions 51–55, Batch D, CP-2).
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
EXPECTED_LOT12_SOURCES = ["EX-N38", "EX-N39", "EX-N42", "AN-1", "AN-2"]

class TestLot12(unittest.TestCase):
    def test_01_roster_integrity(self):
        self.assertTrue(os.path.isfile(ROSTER_PATH))
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA)

        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(data["total_candidates"], 15)
        lot12_items = [r for r in data["roster"] if r["lot"] == "LOT-12"]
        self.assertEqual(len(lot12_items), 5)
        source_ids = [r["source_id"] for r in lot12_items]
        self.assertEqual(source_ids, EXPECTED_LOT12_SOURCES)

    def test_02_review_dashboard(self):
        review_html = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(review_html))
        with open(review_html, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("No academic approval inferred from software validation.", html)
        self.assertIn("HOLD_BASE_NOT_READY", html)
        for sid in EXPECTED_LOT12_SOURCES:
            self.assertIn(sid, html)

    def test_03_question_audit_records(self):
        for idx, expected_source in enumerate(EXPECTED_LOT12_SOURCES, 51):
            q_file = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_file))
            with open(q_file, encoding="utf-8") as f:
                rec = json.load(f)

            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-12")
            self.assertEqual(rec["batch"], "BATCH-D")
            self.assertEqual(rec["academic_admission"], "NOT_ADMITTED")
            self.assertEqual(rec["admission_gate"], "HOLD:ACADEMIC_ADMISSION")
            self.assertEqual(rec["core2_status"], "NOT_RUN")
            self.assertEqual(rec["solve_exposure"], "EXPOSED")
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
        for idx in range(51, 56):
            s_file = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_file))
            with open(s_file, encoding="utf-8") as f:
                rec = json.load(f)
            self.assertIn("confidentiality_notice", rec)
            for fk in forbidden_keys:
                self.assertNotIn(fk, rec)

    def test_05_candidate_solves_and_trajectory(self):
        # EX-N38 (Q51): 18, TC-WPE-CONST-POWER-TRAJECTORY-01
        with open(os.path.join(LOT_DIR, "questions", "51", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q51 = json.load(f)
        self.assertEqual(q51["candidate_solve"]["predicted_option"], "18")
        self.assertEqual(q51["teaching_construction_family"]["construction_id"], "TC-WPE-CONST-POWER-TRAJECTORY-01")

        # EX-N39 (Q52): 346
        with open(os.path.join(LOT_DIR, "questions", "52", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q52 = json.load(f)
        self.assertEqual(q52["candidate_solve"]["predicted_option"], "346")

        # EX-N42 (Q53): 10
        with open(os.path.join(LOT_DIR, "questions", "53", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q53 = json.load(f)
        self.assertEqual(q53["candidate_solve"]["predicted_option"], "10")

        # AN-1 (Q54): D
        with open(os.path.join(LOT_DIR, "questions", "54", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q54 = json.load(f)
        self.assertTrue(q54["candidate_solve"]["predicted_option"].startswith("D:"))

        # AN-2 (Q55): C
        with open(os.path.join(LOT_DIR, "questions", "55", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q55 = json.load(f)
        self.assertTrue(q55["candidate_solve"]["predicted_option"].startswith("C:"))

if __name__ == "__main__":
    unittest.main()
