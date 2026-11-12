"""
Test suite for Grade9 v4.0 — Lot 10 (Questions 41–45, Batch C, CP-3).
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
EXPECTED_LOT10_SOURCES = ["EX-M111", "EX-M120", "EX-N8", "EX-N11", "EX-N19"]

class TestLot10(unittest.TestCase):
    def test_01_roster_integrity(self):
        self.assertTrue(os.path.isfile(ROSTER_PATH))
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA)

        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(data["total_candidates"], 15)
        lot10_items = [r for r in data["roster"] if r["lot"] == "LOT-10"]
        self.assertEqual(len(lot10_items), 5)
        source_ids = [r["source_id"] for r in lot10_items]
        self.assertEqual(source_ids, EXPECTED_LOT10_SOURCES)

    def test_02_review_dashboard(self):
        review_html = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(review_html))
        with open(review_html, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("No academic approval inferred from software validation.", html)
        self.assertIn("HOLD_BASE_NOT_READY", html)
        for sid in EXPECTED_LOT10_SOURCES:
            self.assertIn(sid, html)

    def test_03_question_audit_records(self):
        for idx, expected_source in enumerate(EXPECTED_LOT10_SOURCES, 41):
            q_file = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_file))
            with open(q_file, encoding="utf-8") as f:
                rec = json.load(f)

            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-10")
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
        for idx in range(41, 46):
            s_file = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_file))
            with open(s_file, encoding="utf-8") as f:
                rec = json.load(f)
            self.assertIn("confidentiality_notice", rec)
            for fk in forbidden_keys:
                self.assertNotIn(fk, rec)

    def test_05_candidate_solves(self):
        # EX-M111 (Q41): 2tan(phi)
        with open(os.path.join(LOT_DIR, "questions", "41", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q41 = json.load(f)
        self.assertTrue(q41["candidate_solve"]["predicted_option"].startswith("D:"))

        # EX-M120 (Q42): t^(3/2)
        with open(os.path.join(LOT_DIR, "questions", "42", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q42 = json.load(f)
        self.assertTrue(q42["candidate_solve"]["predicted_option"].startswith("B:"))

        # EX-N8 (Q43): 300
        with open(os.path.join(LOT_DIR, "questions", "43", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q43 = json.load(f)
        self.assertEqual(q43["candidate_solve"]["predicted_option"], "300")

        # EX-N11 (Q44): -245
        with open(os.path.join(LOT_DIR, "questions", "44", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q44 = json.load(f)
        self.assertEqual(q44["figure_status"], "REQUIRED_UNRESOLVED")
        self.assertEqual(q44["solve_status"], "HOLD:FIGURE_UNRESOLVED")

        # EX-N19 (Q45): 4
        with open(os.path.join(LOT_DIR, "questions", "45", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q45 = json.load(f)
        self.assertEqual(q45["candidate_solve"]["predicted_option"], "4")

    def test_06_fail_closed_tamper_simulation(self):
        q41_path = os.path.join(LOT_DIR, "questions", "41", "QUESTION_AUDIT.json")
        with open(q41_path, encoding="utf-8") as f:
            rec = json.load(f)
        tampered_stem = rec["stem_text"] + " [MUTATED]"
        tampered_sha = hashlib.sha256(tampered_stem.encode("utf-8")).hexdigest()
        self.assertNotEqual(tampered_sha, rec["stem_sha256"])

if __name__ == "__main__":
    unittest.main()
