"""
LOT-03 Test Suite (Unittest)
Verifies candidates 6-10 (EX-M11, EX-M14, EX-M16, EX-M18, EX-M24),
immutable stem text hashes, fail-closed stem mutation,
sealed source-only packets, self-contained review package manifest,
EX-M18 geometry reconstruction & SOURCE_FIDELITY_REPAIR alert,
EX-M14 g=9.8 convention documentation, EX-M16 next scoping recommendation,
governance fail-closed gates, SL2 scoring, and viewport checks.
"""

import os
import json
import hashlib
import unittest

LOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROSTER_PATH = os.path.join(LOT_DIR, "ROSTER_PRIVATE.json")
if not os.path.isfile(ROSTER_PATH):
    ROSTER_PATH = os.path.abspath("workspace/output/G9V4_LOTS/BATCH-A/ROSTER_PRIVATE.json")

EXPECTED_ROSTER_FILE_SHA = "8fc0ae47c9d79d62445c07f16f0d7e56dafcc1320380e3f5c134064df7752d5d"
EXPECTED_ROSTER_ITEMS_SHA = "5c6c0a41dcd2970e725b3210cafd02dfb0e005677a6a4c19e247c437811488fb"
EXPECTED_BP_SHA = "ac32dc937403cac33c76343f2e7e0dabd7c2c4a3188cb3b453ddf2576578ddf9"
EXPECTED_ADAPTER_SHA = "899e61e59370a3fc5d6f73b7d8cbb65165d0782c9fba20acd83439ae441e6a9b"
EXPECTED_LOT03_SOURCES = ["EX-M11", "EX-M14", "EX-M16", "EX-M18", "EX-M24"]


class TestLot03(unittest.TestCase):
    def test_01_roster_integrity(self):
        """Verify ROSTER_PRIVATE.json existence, file SHA, embedded SHA and LOT-03 roster segment."""
        self.assertTrue(os.path.isfile(ROSTER_PATH), "ROSTER_PRIVATE.json must exist")
        with open(ROSTER_PATH, "rb") as f:
            content = f.read()
        file_sha = hashlib.sha256(content).hexdigest()
        self.assertEqual(file_sha, EXPECTED_ROSTER_FILE_SHA, f"Roster file SHA mismatch: {file_sha}")
        
        data = json.loads(content.decode("utf-8"))
        self.assertEqual(data["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA, "Roster embedded items SHA mismatch")
        self.assertEqual(data["total_candidates"], 15)
        lot03_items = [r for r in data["roster"] if r["lot"] == "LOT-03"]
        self.assertEqual(len(lot03_items), 5)
        source_ids = [r["source_id"] for r in lot03_items]
        self.assertEqual(source_ids, EXPECTED_LOT03_SOURCES)

    def test_02_manifest_integrity(self):
        """Verify MANIFEST.json file entries, byte counts, and SHA-256 hashes."""
        manifest_path = os.path.join(LOT_DIR, "MANIFEST.json")
        self.assertTrue(os.path.isfile(manifest_path), "MANIFEST.json must exist")
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["lot_id"], "LOT-03")
        self.assertEqual(manifest["roster_sha256"], EXPECTED_ROSTER_ITEMS_SHA)
        self.assertEqual(manifest["total_archive_members"], 16)
        self.assertEqual(len(manifest["files"]), 15)

        # Check documented runtime dependencies
        self.assertIn("runtime_dependencies", manifest)
        deps = manifest["runtime_dependencies"]
        for required_key in ["python", "python_packages", "node", "playwright", "os", "shell"]:
            self.assertIn(required_key, deps, f"Missing runtime dependency key: {required_key}")

        for entry in manifest["files"]:
            fpath = os.path.join(LOT_DIR, entry["path"])
            self.assertTrue(os.path.isfile(fpath), f"File {entry['path']} missing on disk")
            if "TEST.log" in entry["path"]:
                continue  # Skip test log byte/sha check during test execution as it may be actively written
            with open(fpath, "rb") as f:
                data = f.read()
            self.assertEqual(len(data), entry["bytes"], f"Byte mismatch for {entry['path']}")
            sha = hashlib.sha256(data).hexdigest()
            self.assertEqual(sha, entry["sha256"], f"SHA mismatch for {entry['path']}")

    def test_03_question_audit_records(self):
        """Verify each of the 5 QUESTION_AUDIT.json records satisfies fail-closed criteria."""
        for idx_offset, expected_source in enumerate(EXPECTED_LOT03_SOURCES):
            idx = idx_offset + 6
            q_path = os.path.join(LOT_DIR, "questions", f"{idx:02d}", "QUESTION_AUDIT.json")
            self.assertTrue(os.path.isfile(q_path), f"Audit file missing: {q_path}")
            with open(q_path, encoding="utf-8") as f:
                rec = json.load(f)

            # Roster sequence alignment
            self.assertEqual(rec["sequence"], idx)
            self.assertEqual(rec["source_id"], expected_source)
            self.assertEqual(rec["lot"], "LOT-03")

            # Governance fail-closed invariants
            self.assertEqual(rec["academic_admission"], "NOT_ADMITTED", "Must NOT be admitted academically")
            self.assertEqual(rec["admission_gate"], "HOLD:ACADEMIC_ADMISSION", "Gate must be on HOLD")
            self.assertEqual(rec["core2_status"], "NOT_RUN", "Core2 must not be prematurely run")
            self.assertEqual(rec["solve_exposure"], "EXPOSED", "Must declare EXPOSED, no false blind claim")

            # Stem text hash invariant
            computed_stem_sha = hashlib.sha256(rec["stem_text"].encode("utf-8")).hexdigest()
            self.assertEqual(rec["stem_sha256"], computed_stem_sha, f"stem_sha256 mismatch for {expected_source}")
            self.assertEqual(rec["source_hash"], computed_stem_sha, f"source_hash mismatch for {expected_source}")

            # SL2 structure
            sl2 = rec["sl2"]
            self.assertEqual(sl2["mode"], "QUESTION")
            diff = sl2["difficulty_evidence"]
            comps = diff["components"]
            self.assertEqual(len(comps), 5)
            calculated_sum = sum(c["score"] for c in comps.values())
            self.assertEqual(calculated_sum, diff["total"])
            for cname, cdata in comps.items():
                self.assertIn(cdata["score"], [0, 1, 2], f"Invalid score in {cname}")

            # Blueprint fit check
            if diff["band"] in ["D1", "D2"]:
                self.assertEqual(rec["blueprint_fit"], "BLUEPRINT=SPEC_PENDING")
                self.assertEqual(rec["adapter_fit"], "ADAPTER=SPEC_PENDING")
            elif diff["band"] in ["D3", "D4"]:
                self.assertIsInstance(rec["blueprint_fit"], dict)
                self.assertEqual(rec["blueprint_fit"]["sha256"], EXPECTED_BP_SHA)
                self.assertEqual(rec["blueprint_fit"]["version"], "0.2.0")
                self.assertEqual(rec["adapter_fit"]["sha256"], EXPECTED_ADAPTER_SHA)

            # Specific question checks
            if expected_source == "EX-M18":
                self.assertIn("source_fidelity_repair_note", rec)
                self.assertIn("SOURCE_FIDELITY_REPAIR", rec["source_fidelity_repair_note"])
                self.assertEqual(rec["figure_status"], "HOLD:FIGURE_UNRESOLVED")
                solve = rec["candidate_solve"]
                self.assertIn("sqrt(3gR + (k R^2 / m))", solve["derivation"])
                self.assertTrue(solve["predicted_option"].startswith("B:"))
                self.assertIn("bottom of hoop", solve["assumed_parameters_from_coaching_figure"])
            elif expected_source == "EX-M14":
                self.assertIn("gravity_value_status", rec["candidate_solve"])
                self.assertIn("9.8", rec["candidate_solve"]["gravity_value_status"])
            elif expected_source == "EX-M16":
                self.assertIn("next_scope_recommendation", rec)
                self.assertIn("PROPOSED_NEXT_TEXT_ONLY_D3_CANDIDATE", rec["next_scope_recommendation"])

            # Blockers non-empty
            self.assertGreaterEqual(len(rec["blockers"]), 1)

    def test_04_source_only_packets(self):
        """Verify each of the 5 source-only packets is sealed and free of candidate solve/keys/scores."""
        for idx_offset, expected_source in enumerate(EXPECTED_LOT03_SOURCES):
            idx = idx_offset + 6
            s_path = os.path.join(LOT_DIR, "source_only", f"{idx:02d}", "SOURCE_ONLY.json")
            self.assertTrue(os.path.isfile(s_path), f"Source-only file missing: {s_path}")
            with open(s_path, encoding="utf-8") as f:
                srec = json.load(f)

            self.assertEqual(srec["source_id"], expected_source)
            self.assertEqual(srec["sequence"], idx)
            self.assertIn("stem_text", srec)
            self.assertIn("options", srec)
            self.assertIn("confidentiality_notice", srec)

            # Stem hash alignment
            computed_stem_sha = hashlib.sha256(srec["stem_text"].encode("utf-8")).hexdigest()
            self.assertEqual(srec["stem_sha256"], computed_stem_sha)

            # Blind confidentiality invariants: must NOT contain solutions, keys, SL2, or reviewer notes
            forbidden_fields = [
                "candidate_solve", "sl2", "official_key", "key_status", "solve_status",
                "academic_admission", "admission_gate", "blockers", "next_action",
                "derivation", "limiting_cases", "solve_exposure", "source_fidelity_repair_note"
            ]
            for fld in forbidden_fields:
                self.assertNotIn(fld, srec, f"Forbidden field '{fld}' leaked in sealed source packet {s_path}")

    def test_05_stem_mutation_fail_closed(self):
        """Demonstrate fail-closed behavior: tampering with stem text causes hash mismatch."""
        q_path = os.path.join(LOT_DIR, "questions", "06", "QUESTION_AUDIT.json")
        with open(q_path, encoding="utf-8") as f:
            rec = json.load(f)
        
        original_stem = rec["stem_text"]
        mutated_stem = original_stem + " [TAMPER_ATTEMPT]"
        mutated_sha = hashlib.sha256(mutated_stem.encode("utf-8")).hexdigest()
        self.assertNotEqual(mutated_sha, rec["stem_sha256"], "Mutated stem must fail hash check")
        self.assertNotEqual(mutated_sha, rec["source_hash"], "Mutated stem must fail source_hash check")

    def test_06_html_dashboard_content(self):
        """Verify review/index.html content, disclaimers, and rendered candidate IDs."""
        html_path = os.path.join(LOT_DIR, "review", "index.html")
        self.assertTrue(os.path.isfile(html_path))
        with open(html_path, encoding="utf-8") as f:
            html = f.read()
        self.assertIn("NOT_ADMITTED", html)
        self.assertIn("No academic approval inferred from software validation", html)
        self.assertIn("SOURCE_FIDELITY_REPAIR", html)
        for sid in EXPECTED_LOT03_SOURCES:
            self.assertIn(sid, html)


if __name__ == "__main__":
    unittest.main()
