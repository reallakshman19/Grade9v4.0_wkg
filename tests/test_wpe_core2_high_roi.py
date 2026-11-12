"""Regression checks for bounded WPE Core-2 high-ROI scientific/hint correction."""
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "workspace/output/WPE_Core2_Consolidated_20261102"
BANK = OUTPUT / "native-candidate/selected_bank.review.json"
PAGE = ROOT / "preview/question-status.html"
MANIFEST = OUTPUT / "MANIFEST.review.json"

def payload():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    html = PAGE.read_text(encoding="utf-8")
    match = re.search(r'<script id="wpe-data" type="application/json">(.*?)</script>', html, re.DOTALL)
    assert match, "Reader's embedded JSON missing"
    embedded = json.loads(match.group(1))
    return bank, embedded, html

def entry(records, source_id):
    hits = [q for q in records if q["source_id"] == source_id]
    assert len(hits) == 1, source_id
    return hits[0]

def test_all_question_data_matches_native_candidate():
    bank, page, html = payload()
    assert bank["academic_admission"] == "NOT_ADMITTED"
    assert len(bank["questions"]) == len(page["questions"]) == 74
    assert bank["questions"] == page["questions"]
    assert len({q["id"] for q in bank["questions"]}) == 74
    assert "if(!s?.committed)return" in html
    assert "function showSolution(q)" in html

def test_changed_source_stems_are_untouched():
    bank, _, _ = payload()
    ids = {
        "EX-M6": "7d9e6e00a473b5219d71fa3889281e129945bb5c19d9f53407d7ca7fe570e1b6",
        "TB-WPE-ILL-05": "826dfe7a0d485ccb73b58e73d3a8f88c535e84961ac9c281e8ff0971658e51fd",
        "WEP07-03": "f2c82329078c24516058311cf0d166b937b1c983a9c273732d3ef0ab8e842c0c",
    }
    for source, expected in ids.items():
        q = entry(bank["questions"], source)
        assert q["stem_sha256"] == expected
        assert hashlib.sha256(q["stem"].encode("utf-8")).hexdigest() == expected

def test_ex_m6_must_not_claim_universal_key():
    bank, _, _ = payload()
    q = entry(bank["questions"], "EX-M6")
    assert q["review_state"] == "NOT_ADMITTED"
    assert q["key_state"].startswith("HOLD:")
    assert "NOT a verified universal" in q["answer"]
    assert "0.708" in q["check"]
    assert "horizontal velocity component" in " ".join(q["steps"]).lower()

def test_nsep_multiple_correct_and_no_decisive_pre_attempt_hint():
    bank, _, _ = payload()
    q = entry(bank["questions"], "WEP07-03")
    assert q["question_type"] == "multi_correct_mcq"
    assert len(q["options"]) == 4
    assert q["review_state"] == "NOT_ADMITTED"
    assert len(q["hints"]) == 3
    hints = " ".join(h["text"].lower() for h in q["hints"])
    for prohibited in ["e = 0", "z = x0/x", "complete the square", "crux move"]:
        assert prohibited not in hints
    assert "(d)" in q["steps"][-1]

def test_textbook_incline_preserves_condition():
    bank, _, _ = payload()
    q = entry(bank["questions"], "TB-WPE-ILL-05")
    assert q["review_state"] == "NOT_ADMITTED"
    assert "initial speed is unspecified" in q["answer"]
    assert "u=0" in q["answer"]
    assert "sqrt(u^2 + 2gl sin(theta))" in q["answer"]
    assert q["question_type"] == "constructed_response"

def _time_ratio(lam, n=6000):
    """Simpson quadrature for R=g=1, lambda=v^2/(gR)."""
    a, b = math.pi / 4, math.pi
    h = (b - a) / n
    def inv_speed(phi):
        return 1 / math.sqrt(2 * lam + 2 * (math.sin(phi) - 1 / math.sqrt(2)))
    integral = h / 3 * (inv_speed(a) + inv_speed(b) + sum(
        (4 if i % 2 else 2) * inv_speed(a + i * h) for i in range(1, n)
    ))
    return integral / (2 / math.sqrt(lam))

def test_ex_m6_coaching_time_order_has_reachable_counterexample():
    # Both values exceed the B-reachability bound lambda >= 1/sqrt(2).
    assert 0.708 > 1 / math.sqrt(2)
    assert _time_ratio(0.708) > 1.005
    assert _time_ratio(1.0) < 0.87

def test_manifest_pins_real_git_blob_sha():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for target in (PAGE, BANK, OUTPUT / "review/audit_flags.csv", OUTPUT / "review/HIGH_ROI_CORRECTION_20261102.md"):
        rel = target.relative_to(ROOT).as_posix()
        matching = [a for a in manifest["artifacts"] if a["path"] == rel]
        assert len(matching) == 1, rel
        content = target.read_bytes()
        obj = b"blob " + str(len(content)).encode() + bytes([0]) + content
        assert hashlib.sha1(obj).hexdigest() == matching[0]["sha"], rel
