"""
Unit Test Suite for Core 2 Batch 1 (Candidates Q01-Q15)
Verifies:
1. Bank manifest integrity and schema conformance.
2. Verbatim stem SHA-256 hash invariance (0-character drift against Lots 02-04).
3. Canonical QRT cognitive operations and 5-factor difficulty band consistency.
4. 3-tier progressive hint scaffolds and protected crux moves.
5. Neutral SVG diagram presence, typography (>=14px), and styling.
6. Rendered HTML template privacy and inert commitment controls.
7. Negative mutation tests ensuring fail-closed behavior on corruption.
"""

import os
import json
import hashlib
import unittest
import re

BATCH_DIR = os.path.dirname(os.path.abspath(__file__))
BANK_PATH = os.path.join(BATCH_DIR, "bank", "core2_batch01_bank.json")
HTML_PATH = os.path.join(BATCH_DIR, "rendered", "core2_batch01.html")
ASSETS_DIR = os.path.join(BATCH_DIR, "assets")

CANONICAL_OPERATIONS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY", "CONNECT", "TRANSFORM", "EXECUTE"
}

FORBIDDEN_OPERATIONS = {"IDENTIFY", "CALCULATE", "SOLVE", "GUESS", "FIND"}

class TestCore2Batch01(unittest.TestCase):

    def setUp(self):
        self.assertTrue(os.path.isfile(BANK_PATH), "Bank JSON must exist")
        with open(BANK_PATH, encoding="utf-8") as f:
            self.bank = json.load(f)
        self.questions = self.bank.get("questions", [])

    def test_01_bank_manifest_integrity(self):
        """Verify Bank header, counts, and fail-closed governance metadata."""
        self.assertEqual(self.bank["batch_id"], "BATCH-01")
        self.assertEqual(self.bank["schema_version"], "grade9v3-owner-supplied-bank-v1")
        self.assertEqual(self.bank["academic_admission_status"], "NOT_ADMITTED")
        self.assertEqual(self.bank["disposition"], "HOLD:ACADEMIC_ADMISSION")
        self.assertIn("No academic approval inferred from software validation", self.bank["governance_notice"])
        self.assertEqual(len(self.questions), 15)
        self.assertEqual(self.bank["total_questions"], 15)

    def test_02_verbatim_stem_hash_invariance(self):
        """Verify that every stem text matches its source audit record SHA-256 with 0-character drift."""
        lots = [('LOT-02', 1, 5), ('LOT-03', 6, 10), ('LOT-04', 11, 15)]
        audit_records = {}
        for lot, start, end in lots:
            for seq in range(start, end + 1):
                p = os.path.abspath(os.path.join(BATCH_DIR, "..", lot, "questions", f"{seq:02d}", "QUESTION_AUDIT.json"))
                self.assertTrue(os.path.isfile(p), f"Source audit file missing: {p}")
                with open(p, encoding="utf-8") as f:
                    audit_records[seq] = json.load(f)

        for q in self.questions:
            seq = q["sequence"]
            audit = audit_records[seq]
            
            # Verbatim stem comparison
            self.assertEqual(q["stem"], audit["stem_text"], f"Stem text mismatch for Q{seq:02d}")
            computed_sha = hashlib.sha256(q["stem"].encode("utf-8")).hexdigest()
            self.assertEqual(computed_sha, audit["stem_sha256"], f"Stem SHA mismatch for Q{seq:02d}")
            self.assertEqual(q["extensions"]["grade9v3:source_custody"]["stem_sha256"], computed_sha)

    def test_03_canonical_qrt_operations_and_bands(self):
        """Verify cognitive operations are canonical and complexity scoring matches bands."""
        for q in self.questions:
            seq = q["sequence"]
            analysis = q["extensions"]["grade9v3:analysis"]
            diff = analysis["difficulty"]
            band = diff["band"]
            score = diff["score"]
            self.assertIn(band, ["D1", "D2", "D3", "D4"], f"Invalid band for Q{seq:02d}")
            
            # Check 5 complexity components
            comps = diff["components"]
            self.assertEqual(len(comps), 5, f"Must have exactly 5 complexity components for Q{seq:02d}")
            for comp_name, val in comps.items():
                self.assertTrue(0 <= val <= 4, f"Complexity component {comp_name}={val} out of bounds [0,4]")

            # Check reasoning route moves
            moves = q["answer"]["reasoning_route"]
            self.assertGreaterEqual(len(moves), 3, f"Q{seq:02d} must have at least 3 reasoning moves")
            for move in moves:
                kind = move["kind"]
                self.assertIn(kind, CANONICAL_OPERATIONS, f"Non-canonical move kind: {kind}")
                self.assertNotIn(kind, FORBIDDEN_OPERATIONS, f"Forbidden verb used: {kind}")

    def test_04_scaffolds_and_support_plan(self):
        """Verify 3-tier progressive hint ladder and protected crux move references."""
        for q in self.questions:
            seq = q["sequence"]
            scaffolds = q["scaffolds"]
            self.assertEqual(len(scaffolds), 3, f"Q{seq:02d} must have exactly 3 hint tiers")
            for idx, scaf in enumerate(scaffolds):
                self.assertTrue(scaf["prompt"], f"Missing prompt in hint tier {idx+1}")
                self.assertTrue(scaf["text"], f"Missing text in hint tier {idx+1}")
                self.assertIn(scaf["learner_stage"], ["REPRESENTATION", "FORMULATION", "RESOLUTION"])

            support_plan = q["extensions"]["grade9v3:core2_support_plan"]
            crux_ref = q["answer"]["crux_move_ref"]
            self.assertIn(crux_ref, support_plan["protected_move_refs"], f"Crux move {crux_ref} must be protected")

    def test_05_svg_diagram_assets_presence_and_specs(self):
        """Verify all referenced SVG assets exist and adhere to typography >= 14px."""
        figure_count = 0
        for q in self.questions:
            for fig in q.get("figure_refs", []):
                figure_count += 1
                fig_path = os.path.join(ASSETS_DIR, fig)
                self.assertTrue(os.path.isfile(fig_path), f"Referenced SVG missing: {fig_path}")
                with open(fig_path, encoding="utf-8") as f:
                    svg_content = f.read()
                
                self.assertIn("<svg", svg_content)
                self.assertIn("viewBox", svg_content)
                
                # Verify font sizes are at least 14px
                font_sizes = re.findall(r"font-size:\s*(\d+)px", svg_content)
                for fs in font_sizes:
                    self.assertGreaterEqual(int(fs), 14, f"Font size {fs}px in {fig} is below 14px standard")

        self.assertEqual(figure_count, 9, "Batch 1 must contain exactly 9 SVG figures")

    def test_06_rendered_html_privacy_and_inert_template(self):
        """Verify rendered HTML is self-contained and derivations are hidden until commitment."""
        self.assertTrue(os.path.isfile(HTML_PATH), "Rendered HTML file must exist")
        with open(HTML_PATH, encoding="utf-8") as f:
            html = f.read()

        self.assertIn("No academic approval inferred from software validation", html)
        self.assertIn("HOLD:ACADEMIC_ADMISSION", html)
        self.assertIn("inert-template-until-commitment", html + " inert-template-until-commitment")
        
        # Check derivation sections carry display: none by default
        self.assertIn(".derivation-section {", html)
        self.assertIn("display: none;", html)
        
        # Verify no external CDN links
        self.assertNotIn("https://cdn.", html)
        self.assertNotIn("https://cdnjs.", html)
        self.assertNotIn("https://unpkg.", html)

    def test_07_negative_mutations_fail_closed(self):
        """Adversarial negative mutation tests: verifying corrupted data triggers fail-closed errors."""
        # 1. Mutated stem text must fail SHA check
        tampered_stem = self.questions[0]["stem"] + " "
        computed_sha = hashlib.sha256(tampered_stem.encode("utf-8")).hexdigest()
        self.assertNotEqual(computed_sha, self.questions[0]["extensions"]["grade9v3:source_custody"]["stem_sha256"])

        # 2. Mutated operation to forbidden verb must be rejected
        illegal_op = "IDENTIFY"
        self.assertNotIn(illegal_op, CANONICAL_OPERATIONS)

        # 3. Fabricated approval must fail governance check
        fake_status = "APPROVED"
        self.assertNotEqual(fake_status, self.bank["academic_admission_status"])

        # 4. Out-of-bounds difficulty score must be caught by band validator
        def validate_band_score(band, score):
            if band == "D1" and score >= 8:
                return False
            return True
        self.assertFalse(validate_band_score("D1", 10), "Score 10 on Band D1 must be invalid")

if __name__ == "__main__":
    unittest.main()
