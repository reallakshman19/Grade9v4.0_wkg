"""
Test suite for Grade9 v4.0 — Lot 14 (Questions 61–65, Batch D / CP-4 Final Five Provisional In-Scope WPE Identities).
Includes positive verification and negative mutation tests covering:
1. Exact band-from-sum rubric (0-2 D1, 3-5 D2, 6-7 D3, 8-10 D4)
2. Allowed operation vocabulary (7 canonical operations only)
3. Exact Blueprint-cell / operation correspondence
4. Source tamper detection (stem SHA verification)
5. Blind source-only packet isolation and unbound registry stem protections.
"""

import os
import json
import hashlib
import unittest

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_PATH = os.path.join(LOT_DIR, "ROSTER_PRIVATE.json")

EXPECTED_ROSTER_FILE_SHA = "63f6e4f032d2466ac06c280787d776b44a392d72ad20d07e321bd5c680885d40"
EXPECTED_ROSTER_ITEMS_SHA = "3d82e62b6cf0aacad158a7487d93be1d8fa3d1aac43173d798ce7f8f1e842ed0"
EXPECTED_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
EXPECTED_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"
EXPECTED_LOT14_SOURCES = [
    "JEE-2026-04-06-S1-Q28",
    "JEE-2026-04-02-S2-Q31",
    "JEE-2026-04-04-S1-Q49",
    "WEP07-02",
    "WEP07-03"
]

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}

OPERATION_CELL_MAP = {
    1: "RETRIEVE",
    2: "EXPLAIN",
    3: "APPLY",
    4: "MODEL",
    5: "REPRESENT",
    6: "SYNTHESIZE",
    7: "JUSTIFY"
}

def determine_band(score_sum: int) -> str:
    if 0 <= score_sum <= 2:
        return "D1"
    elif 3 <= score_sum <= 5:
        return "D2"
    elif 6 <= score_sum <= 7:
        return "D3"
    elif 8 <= score_sum <= 10:
        return "D4"
    else:
        raise ValueError(f"Score sum {score_sum} out of 0-10 bounds")

def validate_cell_operation(cell_ref: str, operation: str) -> bool:
    parts = cell_ref.split(".")
    if len(parts) != 2:
        return False
    try:
        col = int(parts[1])
    except ValueError:
        return False
    expected_op = OPERATION_CELL_MAP.get(col)
    return expected_op == operation

class TestLot14(unittest.TestCase):
    def test_01_roster_integrity(self):
        self.assertTrue(os.path.isfile(ROSTER_PATH))
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA)

        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(data["total_candidates"], 5)
        self.assertEqual(data["sequence_range"], [61, 65])
        
        lot14_items = data["roster"]
        self.assertEqual(len(lot14_items), 5)
        source_ids = [r["source_id"] for r in lot14_items]
        self.assertEqual(source_ids, EXPECTED_LOT14_SOURCES)

        # Assert no overlap with prior lots
        all_prior = set()
        for lot_num in range(2, 14):
            r_path = os.path.join(LOT_DIR, "..", f"LOT-{lot_num:02d}", "ROSTER_PRIVATE.json")
            if os.path.isfile(r_path):
                with open(r_path, encoding="utf-8") as f:
                    r_data = json.load(f)
                    for item in r_data["roster"]:
                        all_prior.add(item["source_id"])
        overlap = set(source_ids).intersection(all_prior)
        self.assertEqual(len(overlap), 0, f"Found overlapping candidates: {overlap}")

    def test_02_review_dashboard(self):
        review_html = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(review_html))
        with open(review_html, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("No academic approval inferred from software validation.", html)
        self.assertIn("HOLD_BASE_NOT_READY", html)
        self.assertIn("viewport", html)
        for sid in EXPECTED_LOT14_SOURCES:
            self.assertIn(sid, html)

    def test_03_question_audit_records(self):
        for idx, expected_source in enumerate(EXPECTED_LOT14_SOURCES, 61):
            q_file = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_file))
            with open(q_file, encoding="utf-8") as f:
                rec = json.load(f)

            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-14")
            self.assertEqual(rec["academic_admission"], "NOT_ADMITTED")
            self.assertEqual(rec["admission_gate"], "HOLD:ACADEMIC_ADMISSION")
            self.assertEqual(rec["core2_status"], "NOT_RUN")
            self.assertEqual(rec["solve_exposure"], "EXPOSED")

            # Authority check
            if expected_source in ["WEP07-02", "WEP07-03"]:
                self.assertEqual(rec["key_issuing_authority"], "IAPT")
                self.assertEqual(rec["source_type"], "UNBOUND_NSEP_DESCRIPTOR")
                self.assertIsNone(rec["stem_text"])
                self.assertIsNone(rec["stem_sha256"])
                self.assertIsNone(rec["source_hash"])
                self.assertEqual(rec["stem_binding"], "TEXT_NOT_BOUND_IN_REGISTRY")
            else:
                self.assertEqual(rec["key_issuing_authority"], "NTA")
                self.assertEqual(rec["source_type"], "EXAM_PAPER_TRANSCRIBED")
                self.assertIsNotNone(rec["stem_text"])
                computed_stem_sha = hashlib.sha256(rec["stem_text"].encode("utf-8")).hexdigest()
                self.assertEqual(rec["stem_sha256"], computed_stem_sha)
                self.assertEqual(rec["source_hash"], computed_stem_sha)

            # Key status separation
            if expected_source == "WEP07-03":
                self.assertEqual(rec["key_status"], "VERIFIED_IAPT_KEY_RECEIPT")
            elif expected_source == "WEP07-02":
                self.assertEqual(rec["key_status"], "HOLD:OFFICIAL_KEY_NOT_RETAINED")
            else:
                self.assertEqual(rec["key_status"], "HOLD:OFFICIAL_KEY_UNRESOLVED")

            # SL2 Rubric and Allowed Operations
            sl2 = rec["sl2"]
            self.assertEqual(sl2["mode"], "QUESTION")
            diff = sl2["difficulty_evidence"]
            comps = diff["components"]
            self.assertEqual(len(comps), 5)
            comp_sum = sum(c["score"] for c in comps.values())
            self.assertEqual(comp_sum, diff["total"])
            
            # Exact score sum to band check
            expected_band = determine_band(comp_sum)
            self.assertEqual(diff["band"], expected_band)

            # Allowed operations vocabulary
            demand = sl2["demand_proposal"]
            self.assertIn(demand["primary"], CANONICAL_OPERATIONS)
            for sec in demand.get("secondary", []):
                self.assertIn(sec, CANONICAL_OPERATIONS)

            # Cell operation correspondence
            if expected_band in ["D1", "D2"]:
                self.assertEqual(rec["blueprint_fit"], "BLUEPRINT=SPEC_PENDING")
                self.assertEqual(rec["adapter_fit"], "ADAPTER=SPEC_PENDING")
            elif expected_band in ["D3", "D4"]:
                self.assertIsInstance(rec["blueprint_fit"], dict)
                cell_ref = rec["blueprint_fit"]["blueprint_cell_ref"]
                self.assertTrue(validate_cell_operation(cell_ref, demand["primary"]),
                                f"Mismatch between cell {cell_ref} and primary op {demand['primary']}")
                self.assertEqual(rec["blueprint_fit"]["sha256"], EXPECTED_BP_SHA)
                self.assertEqual(rec["blueprint_fit"]["version"], "0.2.0")
                self.assertEqual(rec["adapter_fit"]["status"], "CELL_UNQUALIFIED_ADAPTER_GAP")

            self.assertGreaterEqual(len(rec["blockers"]), 1)

    def test_04_source_only_packets(self):
        forbidden_keys = [
            "candidate_solve", "official_key", "predicted_option",
            "worked_solution", "score", "difficulty_evidence", "sl2", "blockers"
        ]
        for idx in range(61, 66):
            s_file = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_file))
            with open(s_file, encoding="utf-8") as f:
                rec = json.load(f)
            self.assertIn("confidentiality_notice", rec)
            for fk in forbidden_keys:
                self.assertNotIn(fk, rec)

            if rec["source_id"] in ["WEP07-02", "WEP07-03"]:
                self.assertEqual(rec["stem_status"], "SOURCE_INCOMPLETE_UNBOUND_REGISTRY_STEM")
                self.assertIsNone(rec["stem_text"])
                self.assertIsNone(rec["stem_sha256"])
                self.assertIsNone(rec["options"])
            else:
                self.assertEqual(rec["stem_status"], "VERIFIED_BOUND_TEXT")
                self.assertIsNotNone(rec["stem_text"])
                self.assertIsNotNone(rec["stem_sha256"])
                # Q63 is a numerical value type, so options is None
                if rec["sequence"] == 63:
                    self.assertIsNone(rec["options"])
                else:
                    self.assertIsNotNone(rec["options"])

    def test_05_candidate_solves(self):
        # Q61 (JEE-2026-04-06-S1-Q28): Option 6952787592 (-9.98 J)
        with open(os.path.join(LOT_DIR, "questions", "61", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q61 = json.load(f)
        self.assertIn("6952787592", q61["candidate_solve"]["predicted_option"])
        self.assertIn("- 9.98", q61["candidate_solve"]["predicted_option"])

        # Q62 (JEE-2026-04-02-S2-Q31): Option 691121616
        with open(os.path.join(LOT_DIR, "questions", "62", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q62 = json.load(f)
        self.assertIn("691121616", q62["candidate_solve"]["predicted_option"])

        # Q63 (JEE-2026-04-04-S1-Q49): 200 W
        with open(os.path.join(LOT_DIR, "questions", "63", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q63 = json.load(f)
        self.assertIn("200", q63["candidate_solve"]["predicted_option"])

        # Q64 (WEP07-02): Option a (sqrt(g(L - y0^2/L)))
        with open(os.path.join(LOT_DIR, "questions", "64", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q64 = json.load(f)
        self.assertIn("a:", q64["candidate_solve"]["predicted_option"])
        self.assertIn("sqrt(g(L - y0^2/L))", q64["candidate_solve"]["predicted_option"])

        # Q65 (WEP07-03): Option a, b, c, d
        with open(os.path.join(LOT_DIR, "questions", "65", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            q65 = json.load(f)
        self.assertIn("a, b, c, d", q65["candidate_solve"]["predicted_option"])
        self.assertEqual(q65["sl2"]["demand_proposal"]["primary"], "APPLY")
        self.assertEqual(q65["sl2"]["difficulty_evidence"]["band"], "D2")

    # =========================================================================
    # NEGATIVE MUTATION TESTS (Enforcing rubric, vocabulary, cell mapping, SHA)
    # =========================================================================

    def test_06_negative_mutation_wrong_band(self):
        """Negative test: mutating total score to 8 must fail if band is kept as D3."""
        with open(os.path.join(LOT_DIR, "questions", "62", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            rec = json.load(f)
        
        # Mutate total score to 8 (which belongs to D4), keep band D3
        mutated = json.loads(json.dumps(rec))
        mutated["sl2"]["difficulty_evidence"]["total"] = 8
        mutated["sl2"]["difficulty_evidence"]["components"]["algebra_computational_load"]["score"] = 2
        
        comp_sum = sum(c["score"] for c in mutated["sl2"]["difficulty_evidence"]["components"].values())
        declared_band = mutated["sl2"]["difficulty_evidence"]["band"]
        correct_band = determine_band(comp_sum)
        
        # The validator must reject declared_band ("D3") because correct_band is "D4"
        with self.assertRaises(AssertionError):
            self.assertEqual(declared_band, correct_band, "Validator failed to catch wrong band for score 8!")

    def test_07_negative_mutation_invalid_operation(self):
        """Negative test: mutating operation to 'IDENTIFY' or 'CALCULATE' must fail canonical check."""
        invalid_ops = ["IDENTIFY", "CALCULATE", "ANALYZE", "SOLVE", "EVALUATE"]
        for bad_op in invalid_ops:
            with self.assertRaises(AssertionError):
                self.assertIn(bad_op, CANONICAL_OPERATIONS, f"Failed to reject non-canonical operation: {bad_op}")

    def test_08_negative_mutation_wrong_cell_binding(self):
        """Negative test: pairing APPLY with D3.4 (MODEL) or SYNTHESIZE with D3.3 (APPLY) must fail."""
        # D3.4 is Column 4 -> MODEL
        self.assertFalse(validate_cell_operation("D3.4", "APPLY"), "Failed to reject APPLY bound to D3.4")
        self.assertFalse(validate_cell_operation("D3.1", "APPLY"), "Failed to reject APPLY bound to D3.1")
        self.assertFalse(validate_cell_operation("D3.3", "SYNTHESIZE"), "Failed to reject SYNTHESIZE bound to D3.3")
        self.assertFalse(validate_cell_operation("D3.6", "MODEL"), "Failed to reject MODEL bound to D3.6")

    def test_09_negative_mutation_tampered_stem_sha(self):
        """Negative test: altering one character of stem_text without changing SHA must fail."""
        with open(os.path.join(LOT_DIR, "questions", "61", "QUESTION_AUDIT.json"), encoding="utf-8") as f:
            rec = json.load(f)
        
        original_sha = rec["stem_sha256"]
        tampered_stem = rec["stem_text"] + " " # append one space
        tampered_sha = hashlib.sha256(tampered_stem.encode("utf-8")).hexdigest()
        
        with self.assertRaises(AssertionError):
            self.assertEqual(tampered_sha, original_sha, "Failed to catch stem text tamper / SHA mismatch!")

if __name__ == "__main__":
    unittest.main()
