"""Source-pinned WPE QRT × Blueprint coverage register.

These tests reconcile *author-exposed review metadata*, not independent QRT,
original-paper authenticity, native Core1A/Core1B acceptance or child mastery.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "architecture" / "qrt-blueprint-protocol"
REGISTER = DIR / "wpe-coverage-register.json"
BLUEPRINT = ROOT / "templates/physics-blueprint/physics-blueprint.D3-D4.json"
OPS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def inputs():
    d = load(REGISTER)
    src = {name: load(ROOT / item["path"]) for name, item in d["pins"].items()}
    return d, src


def test_74_records_and_exact_source_git_blob_pins():
    report, source = inputs()
    assert report["schema"] == "g9v4-wpe-qrt-blueprint-coverage-register/v1"
    assert report["status"] == "AUTHOR_EXPOSED_COVERAGE_REGISTER__NO_ACADEMIC_ADMISSION"
    assert set(report["pins"]) == {
        "bank", "routes", "pilot", "qrt_b07", "source_b08", "corrective_b09",
        "practice", "blueprint"
    }
    for name, pin in report["pins"].items():
        content = (ROOT / pin["path"]).read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert pin["git_blob_sha"] == digest, name
    assert report["operations"] == list(OPS) == source["blueprint"]["column_order"]
    assert source["blueprint"]["version"] == "0.2.0"
    assert source["blueprint"]["status"] == "DRAFT_OWNER_REVIEW"
    assert len(source["blueprint"]["cells"]) == 14
    question_ids = [q["source_id"] for q in report["questions"]]
    assert question_ids == [q["source_id"] for q in source["bank"]["questions"]]
    assert len(question_ids) == len(set(question_ids)) == 74
    assert report["summary"]["total_questions"] == 74
    assert report["summary"]["admitted"] == 0


def test_every_question_source_and_proposed_band_are_unmodified():
    report, source = inputs()
    keyed = {x["source_id"]: x for x in source["bank"]["questions"]}
    for row in report["questions"]:
        source_row = keyed[row["source_id"]]
        assert row["display_id"] == source_row["id"]
        assert row["category"] == source_row["category"]
        assert row["reader_proposal"]["operation"] == source_row["op"]
        assert row["reader_proposal"]["band"] == source_row["band"]
        assert row["reader_proposal"]["review_state"] == source_row["review_state"] == "NOT_ADMITTED"
        assert row["source_evidence"]["stem_sha256"] == source_row["stem_sha256"]
        assert row["source_evidence"]["source_figure_count"] == len(source_row["source_figures"])
        assert row["source_evidence"]["official_key_state"] == source_row["key_state"]
        assert row["source_evidence"]["source_flag_count"] == len(source_row["flags"])
        assert row["source_evidence"]["original_figure_verified"] is False
        assert row["source_evidence"]["source_custody"] == "NOT_AUTHENTICATED_BY_THIS_REGISTER"
        assert row["admission"] == "NOT_ADMITTED"
        assert row["qrt_evidence"]["independent_final_adjudication"] is False
        assert row["learning"]["exact_inference_independently_verified"] is False
        assert row["learning"]["semantic_join"] == "PROPOSED_UNQUALIFIED"
        assert row["blueprint_route"]["approved_cell"] is None
        assert row["blueprint_route"]["adapter_status"] == "UNSELECTED"
        assert row["blueprint_route"]["blueprint_status"] == "DRAFT_OWNER_REVIEW"
    assert Counter(q["reader_proposal"]["band"] for q in report["questions"]) == Counter({
        "D1": 5, "D2": 47, "D3": 17, "D4": 5
    })
    assert report["summary"]["reader_d3d4"] == 22


def test_qrt_first_pass_and_source_gate_overlay_not_invented():
    report, src = inputs()
    indexed = {x["source_id"]: x for x in report["questions"]}
    b07 = {x["source_id"]: x for x in src["qrt_b07"]["tasks"]}
    assert len(b07) == 5
    assert report["summary"]["b07_reviewed_d2_ids"] == ["EX-M62", "EX-M73", "EX-M101", "WEP07-03"]
    assert report["summary"]["b07_contested_ids"] == ["EX-M79"]
    for qid, row in indexed.items():
        qrt = row["qrt_evidence"]
        if qid not in b07:
            assert qrt["status"] == "NOT_RUN_IN_B07"
            assert qrt["reviewed_band"] is None and qrt["reviewed_operation"] is None
            assert qrt["score_total"] is None and qrt["factors"] is None
            continue
        item = b07[qid]
        assert qrt["status"] == item["review_status"]
        assert qrt["reported_role"] == item["source_role"]
        assert qrt["qrt_final_admission"] == item["qrt_final_admission"] == "NOT_GRANTED"
        assessment = item["current_demand_assessment"]
        if assessment:
            assert qrt["reviewed_operation"] == assessment["operation"]
            assert qrt["reviewed_band"] == assessment["band"] == "D2"
            assert qrt["score_total"] == assessment["total"] == sum(qrt["factors"])
            assert qrt["factors"] == assessment["factors"]
            assert row["blueprint_route"]["candidate_cell"] is None
        else:
            assert qrt["score_total"] is None and qrt["reviewed_band"] is None
    b08 = {x["id"]: x for x in src["source_b08"]["cases"]}
    b09 = {x["id"]: x for x in src["corrective_b09"]["cases"]}
    assert len(b08) == len(b09) == 5
    for qid, x in indexed.items():
        assert x["source_evidence"]["b08_custody"] == (
            b08[qid]["source_custody"] if qid in b08 else None)
        assert x["source_evidence"]["b08_figure_gate"] == (
            b08[qid]["figure"]["status"] if qid in b08 else None)
        assert x["source_evidence"]["b09_corrective_gate"] == (
            b09[qid]["source_gate"] if qid in b09 else None)


def test_learning_routes_and_nine_d3_d4_gaps_are_exact():
    report, src = inputs()
    routes = defaultdict(list)
    for item in src["routes"]["constructions"]:
        for link in item["proposed_source_ids"]:
            routes[link["id"]].append(item["id"])
    by_id = {x["source_id"]: x for x in report["questions"]}
    for qid, row in by_id.items():
        actual = row["learning"]
        expected = routes.get(qid, [])
        assert actual["related_construction_ids"] == expected
        interactive = [x for x in expected if x.startswith("WPE-C")]
        authored = [x for x in expected if x.startswith("WPE-E")]
        assert actual["interactive_ids"] == interactive
        assert actual["author_pack_ids"] == authored
        mode = "INTERACTIVE_RELATED_PRACTICE" if interactive else (
            "AUTHOR_PACK_ONLY" if authored else "UNMAPPED")
        assert actual["status"] == mode
        assert row["next_actions"]["source"] and row["next_actions"]["qrt"]
        assert row["next_actions"]["learning"]
    high = [x for x in report["questions"] if x["reader_proposal"]["band"] in ("D3", "D4")]
    assert len(high) == 22
    assert Counter(x["learning"]["status"] for x in high) == Counter({
        "INTERACTIVE_RELATED_PRACTICE": 13, "AUTHOR_PACK_ONLY": 6, "UNMAPPED": 3
    })
    assert set(report["summary"]["reader_d3d4_unmapped_ids"]) == {
        "EX-M97", "EX-N39", "WEP07-01"
    }
    assert set(report["summary"]["reader_d3d4_author_only_ids"]) == {
        "EX-M82", "EX-M89", "EX-M109", "EX-N34",
        "TB-WPE-ILL-05", "TB-WPE-ILL-06"
    }
    assert Counter(x["learning"]["status"] for x in report["questions"]) == Counter({
        "INTERACTIVE_RELATED_PRACTICE": 18, "AUTHOR_PACK_ONLY": 7, "UNMAPPED": 49
    })
    assert all(row["learning"]["semantic_join"] == "PROPOSED_UNQUALIFIED" for row in high)


def test_14_candidate_blueprint_cells_are_never_academic_approvals():
    report, src = inputs()
    bp = src["blueprint"]
    assert len(bp["cells"]) == 14
    for row in report["questions"]:
        band, op = row["reader_proposal"]["band"], row["reader_proposal"]["operation"]
        reviewed = row["qrt_evidence"]["reviewed_band"]
        expected = f"{band}.{OPS.index(op) + 1}" if (
            band in ("D3", "D4") and op in OPS and reviewed not in ("D1", "D2")
        ) else None
        assert row["blueprint_route"]["candidate_cell"] == expected, row["source_id"]
        if expected:
            assert expected in bp["cells"]
            assert row["blueprint_route"]["basis"] == "READER_PROPOSAL_ONLY"
        assert row["blueprint_route"]["approved_cell"] is None
    assert report["blueprint"]["adapter_status"] == "UNSELECTED"
    assert report["blueprint"]["native_qrt_admissions"] == 0
    assert report["release_policy"]["d31"] == "PAUSED"


def test_21_place_pilot_is_separate_even_when_reader_absent():
    report, src = inputs()
    pilot = src["pilot"]["places"]
    out = report["pilot_places"]
    assert len(out) == len(pilot) == 21
    by_id = {x["source_id"]: x for x in report["questions"]}
    for expected, actual in zip(pilot, out):
        assert actual["place_id"] == expected["place_id"]
        assert actual["candidate_id"] == expected["candidate_id"]
        assert actual["pilot_band"] == expected["band"]
        assert actual["pilot_status"] == expected["status"]
        assert actual["qrt_final_admitted"] is False
        q = by_id.get(expected["candidate_id"])
        if expected["candidate_id"] is None:
            comparison = "VACANT"
        elif q is None:
            comparison = "ABSENT_FROM_CURRENT_READER"
        else:
            comparison = "AGREE" if (q["reader_proposal"]["operation"],
                                    q["reader_proposal"]["band"]) == (
                                    expected["operation"], expected["band"]) else "CONFLICT"
            assert expected["place_id"] in q["pilot_overlay"]["places"]
        assert actual["comparison"] == comparison
    assert report["summary"]["pilot_places"] == 21
    assert report["summary"]["pilot_pending"] == 14
    assert report["summary"]["pilot_vacant"] == 7
    assert report["summary"]["pilot_agree"] == 3
    assert report["summary"]["pilot_conflict"] == 8
    assert report["summary"]["pilot_absent"] == 3
    assert {x["candidate_id"] for x in out if x["comparison"] == "ABSENT_FROM_CURRENT_READER"} == {
        "EX-M81", "EX-M44", "EX-M60"
    }
    assert all(not x["qrt_final_admitted"] for x in out)



def test_machine_schema_requires_full_fields_and_no_fabricated_approvals():
    report = load(REGISTER)
    schema = load(DIR / "schemas" / "coverage-register.schema.json")
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(report))
    assert not errors, [str(e) for e in errors[:4]]
    assert schema["properties"]["questions"]["items"]["properties"]["admission"] == {
        "const": "NOT_ADMITTED"
    }
    assert schema["properties"]["pilot_places"]["items"]["properties"]["qrt_final_admitted"] == {
        "const": False
    }
    assert all(not row["qrt_evidence"]["independent_final_adjudication"]
               for row in report["questions"])
    assert all(not x["qrt_final_admitted"] for x in report["pilot_places"])


def test_priority_dashboard_links_and_accessible_dynamic_filters():
    home = (ROOT / "architecture/index.html").read_text(encoding="utf-8")
    protocol = (DIR / "index.html").read_text(encoding="utf-8")
    runbook = (DIR / "RUNBOOK.md").read_text(encoding="utf-8")
    page = (DIR / "wpe-coverage.html").read_text(encoding="utf-8")
    assert 'href="qrt-blueprint-protocol/wpe-coverage.html"' in home
    assert 'href="wpe-coverage.html"' in protocol
    assert "[search the 74-question WPE QRT" in runbook
    assert '<main class="cov" id="main">' in page
    assert 'id="question-rows"' in page and 'id="pilot-rows"' in page
    assert 'id="filter"' in page and 'id="search"' in page
    assert 'id="learning"' in page and 'aria-live="polite"' in page
    assert 'fetch("wpe-coverage-register.json"' in page
    assert "textContent" in page and "replaceChildren" in page
    assert "innerHTML" not in page
    assert "all academic admissions" not in page.lower() or "NOT_ADMITTED" in page
    assert "no automatic qrt admission" in page.lower()
