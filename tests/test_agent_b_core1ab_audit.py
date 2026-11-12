"""Source-neutral mutation checks for the Agent B fail-closed audit."""
import hashlib
import importlib.util
import json
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "tools" / "agent_b_core1ab_audit.py"
spec = importlib.util.spec_from_file_location("agent_b_core1ab_audit", MODULE)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def candidate(tmp_path, *, exact_copy=False, exam_context=False, leak=False, static_route=False):
    root = tmp_path / "synthetic"
    root.mkdir()
    source = "A synthetic convex lens has a screen distance of 96 cm and focal length 18 cm."
    prompt = source if exact_copy else "Find a focal length from an independently measured 48 cm displacement at a 96 cm screen separation."
    (root / "bank.json").write_text(json.dumps({"questions":[{"id":"SYN-Q1","stem":source}]}))
    (root / "core1a_construction.json").write_text(json.dumps({
        "construction_id":"SYN-C1","target_question_id":"SYN-Q1",
        "academic_status":"HOLD:ACADEMIC_ADMISSION",
        "worked_conceptual_anchor":{"problem":"Distinct synthetic teaching anchor"},
        "misconceptions":[{"wrong_idea":"Assuming there is always one lens position"}]}))
    b = {"construction_id":"SYN-C1","target_question_id":"SYN-Q1",
         "academic_status":"HOLD:ACADEMIC_ADMISSION",
         "fresh_context_ref":"SYN-Q1-AUTHENTIC-EXAM" if exam_context else "SYN-TRANSFER-02",
         "protected_fresh_inference_W":"Infer the focal length from measured displacement",
         "stages":{"stage_2_attempt":{"prompt":prompt,"produces":"f = 18.0 cm"},
                   "stage_4_diagnose":{"question":"Why?"},"stage_5_repair":{"action":"Revise"},
                   "stage_6_boundary_test":{"prompt":"Changed geometry"}},
         "progressive_hints":[{"text":"Define variables"}, {"text":"Use reciprocal roots"},
                              {"text":"The value is 18.0" if leak else "What does the separation determine?"}]}
    raw = json.dumps(b).encode()
    (root / "core1b_reconstruction.json").write_bytes(raw)
    (root / "witness.json").write_text(json.dumps({"core1b":{"task_sha256":"sha256:"+hashlib.sha256(raw).hexdigest()},"review_receipts":[]}))
    if static_route:
        (root / "learning_journey.html").write_text('<div id="content-core1b"><p>Stage 3: Reconstruct</p><p>The answer is revealed.</p></div><div class="footer"></div>')
    return root


def codes(result):
    return {f["code"] for f in result["findings"]}


def test_source_identical_challenge_rejected(tmp_path):
    assert "VERBATIM_SOURCE_REUSE" in codes(audit.audit_module(candidate(tmp_path, exact_copy=True)))


def test_false_fresh_exam_reference_rejected(tmp_path):
    assert "SOURCE_AS_FRESH_CONTEXT" in codes(audit.audit_module(candidate(tmp_path, exam_context=True)))


def test_hint_revealing_numeric_W_rejected(tmp_path):
    assert "H3_NUMERICAL_W_LEAK" in codes(audit.audit_module(candidate(tmp_path, leak=True)))


def test_reconstruction_without_separate_commit_rejected(tmp_path):
    assert "CORE1B_RECONSTRUCTION_UNGATED" in codes(audit.audit_module(candidate(tmp_path, static_route=True)))


def test_no_automatic_approval_on_structurally_sufficient_candidate(tmp_path):
    result = audit.audit_module(candidate(tmp_path))
    assert result["status"] == "HOLD"
    assert "INDEPENDENT_EVIDENCE_PENDING" in codes(result)


def test_empty_generated_tree_is_hold_not_pass(tmp_path):
    outcome = audit.audit_tree(tmp_path)
    assert outcome["status"] == "HOLD" and outcome["count"] if "count" in outcome else outcome["status"] == "HOLD"
