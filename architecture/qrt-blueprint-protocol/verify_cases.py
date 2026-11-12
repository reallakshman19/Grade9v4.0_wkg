#!/usr/bin/env python3
"""Read-only QRT × Physics Blueprint training/golden fixture validator.

Validates the SHAPE of proposed records, consistent operation/band routing,
fact-checks selected documentary statuses, and verifies HOLD negative controls.
It never assigns an academic reviewer, validates a sealed blind receipt, grants
Owner approval, changes native SL1/SL2 data, or qualifies a tile.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OPERATIONS = ("RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY")
FACTORS = (
    "concept_model_selection", "representation_translation", "reasoning_chain_length",
    "algebra_computational_load", "trap_exception_sensitivity",
)
BAND_RANGE = {"D1": (0, 2), "D2": (3, 5), "D3": (6, 7), "D4": (8, 10)}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(kind: str, obj: dict) -> None:
    schema = read(HERE / "schemas" / f"{kind}.schema.json")
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(obj))
    if errors:
        first = sorted(errors, key=lambda e: list(map(str, e.path)))[0]
        raise ValueError(f"{kind} schema: {'.'.join(map(str, first.path))}: {first.message}")


def expected_cell(operation: str | None, band: str | None) -> str | None:
    if operation not in OPERATIONS or band not in ("D3", "D4"):
        return None
    return f"{band}.{OPERATIONS.index(operation)+1}"


def evaluate(record: dict) -> dict:
    """Fail-closed recommendation on documentary data, NEVER academic admission."""
    validate_schema("question-route", record)
    holds = []
    source, proposed, qrt = record["source"], record["sl2"], record["qrt"]
    blueprint, adapter, learning, admission = (
        record["blueprint"], record["adapter"], record["learning"], record["admission"]
    )

    if source["custody"] != "AUTHENTICATED" or source["independent_original_receipt"] is None:
        holds.append("SOURCE_NOT_AUTHENTICATED")
    if source["figure"] in ("UNQUALIFIED", "PENDING"):
        holds.append("FIGURE_PENDING")
    if source["key"] not in ("VERIFIED",):
        holds.append("KEY_PENDING")

    if qrt["status"] == "CONTESTED":
        holds.append("QRT_CONTESTED")
    elif qrt["status"] != "ADJUDICATED":
        holds.append("QRT_NOT_ADJUDICATED")
    if qrt["status"] == "NOT_RUN" and any(qrt[k] is not None for k in ("operation", "band", "total", "factors")):
        holds.append("QRT_UNRUN_WITH_FABRICATED_RESULT")

    if qrt["factors"] is not None:
        if sum(qrt["factors"][key]["score"] for key in FACTORS) != qrt["total"]:
            holds.append("QRT_SCORE_SUM_MISMATCH")
        if qrt["band"] in BAND_RANGE and qrt["total"] is not None:
            lo, hi = BAND_RANGE[qrt["band"]]
            if not lo <= qrt["total"] <= hi:
                holds.append("QRT_SCORE_BAND_MISMATCH")
    elif qrt["total"] is not None:
        holds.append("QRT_SCORE_FACTORS_MISSING")
    if (qrt["operation"] is not None and qrt["band"] is not None
            and (qrt["operation"] != proposed["operation"] or qrt["band"] != proposed["band"])):
        holds.append("DEMAND_DISAGREEMENT")

    # Do not turn B07's recorded first pass into final adjudication.
    supported_qrt = (
        qrt["status"] == "ADJUDICATED"
        and qrt["reviewer_receipt"] is not None
        and qrt["sealed_first_pass_digest"] is not None
        and qrt["exposure"] == "SEALED_SOURCE_ONLY"
        and qrt["factors"] is not None
        and "QRT_SCORE_SUM_MISMATCH" not in holds
        and "QRT_SCORE_BAND_MISMATCH" not in holds
    )
    if not supported_qrt:
        holds.append("NO_QRT_ADMISSION")

    # A reviewed lower-band first pass must not fill the D3/D4 grid.
    reviewed_lower = qrt["status"] in ("FIRST_PASS_RECORDED", "ADJUDICATED") and qrt["band"] in ("D1", "D2")
    if reviewed_lower:
        holds.append("D1_D2_BLUEPRINT_SPEC_PENDING")
        recommended = None
    elif supported_qrt:
        recommended = expected_cell(qrt["operation"], qrt["band"])
    else:
        # Candidate routing from SL2 is educational planning only, not selection.
        recommended = expected_cell(proposed["operation"], proposed["band"])

    supplied = blueprint["candidate_cell"]
    if supplied != recommended:
        holds.append("CELL_OPERATION_MISMATCH")
    if recommended and (recommended not in read(ROOT / blueprint["path"])["cells"]):
        holds.append("BLUEPRINT_CELL_MISSING")
    if blueprint["status"] != "APPROVED" or blueprint["approved_binding_receipt"] is None:
        holds.append("BLUEPRINT_DRAFT")
    if (adapter["status"] != "APPROVED_SELECTED" or adapter["selected_exact_path"] is None
            or adapter["selected_git_blob_sha"] is None or adapter["owner_receipt"] is None):
        holds.append("ADAPTER_UNSELECTED")

    if learning["status"] == "UNMAPPED":
        holds.append("LEARNING_UNMAPPED")
    if learning["status"] == "AUTHOR_PACK_ONLY":
        holds.append("AUTHOR_PACK_NOT_INTERACTIVE")
    if learning["semantic_join"] != "INDEPENDENTLY_REVIEWED" or learning["b1_b7_receipt"] is None:
        holds.append("LEARNING_NOT_QUALIFIED")

    # Structural presence of receipts is not a trusted independent signature.
    # This read-only engine cannot grant APPROVED even when all strings exist.
    if admission["status"] == "ADMITTED" or learning["status"] == "QUALIFIED_TILE":
        holds.append("NO_TRUSTED_RECEIPTS")
    if admission["owner_receipt"] is None or admission["native_core2_receipt"] is None:
        holds.append("ADMISSION_RECEIPTS_MISSING")
    return {
        "question_id": record["question_id"],
        "candidate_cell": recommended,
        "candidate_only": True,
        "holds": sorted(set(holds)),
        "release": "HOLD",
        "verified_independently": False,
    }


def verify_documentary_sources(bundle: dict) -> None:
    """Check golden examples have not invented or drifted from repo evidence."""
    pins = read(HERE / "source-pins.json")
    if pins["schema"] != "g9v4-qrt-blueprint-source-pins/v1":
        raise ValueError("Unexpected source-pin manifest schema.")
    if pins["authority"] != "AUTHOR_EXPOSED_ENGINEERING_REFERENCE_ONLY__NOT_OWNER_APPROVAL":
        raise ValueError("Source-pin record claims unearned academic authority.")
    for name, item in pins["sources"].items():
        filepath = ROOT / item["path"]
        if not filepath.is_file():
            raise ValueError(f"{name}: pinned source missing at {filepath}")
        content = filepath.read_bytes()
        git_blob_sha = hashlib.sha1(
            b"blob " + str(len(content)).encode("ascii") + b"\0" + content
        ).hexdigest()
        if git_blob_sha != item["git_blob_sha"]:
            raise ValueError(f"{name}: Git blob changed; re-audit before updating pin.")
    blueprint = read(ROOT / "templates/physics-blueprint/physics-blueprint.D3-D4.json")
    if blueprint["version"] != "0.2.0" or blueprint["status"] != "DRAFT_OWNER_REVIEW":
        raise ValueError("Pinned Blueprint status/version drift; audit and update references, never silently promote.")
    if len(blueprint["cells"]) != 14 or blueprint["column_order"] != list(OPERATIONS):
        raise ValueError("14-cell Blueprint or operation order changed.")
    bank = read(ROOT / "workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json")
    reader = {row["source_id"]: row for row in bank["questions"]}
    b07 = read(ROOT / "preview/batches/b07-qrt-evidence.json")
    reviewed = {row["source_id"]: row for row in b07["tasks"]}
    pilot = read(ROOT / "WPE_Source_to_Core1A_Concept/evidence/RECEIVED_selection_21_places.json")
    pilot_by_id = {row.get("candidate_id"): row for row in pilot["places"] if row.get("candidate_id")}
    for case in bundle["cases"]:
        route = case["route"]
        qid = route["question_id"]
        if not route["fixture_not_evidence"]:
            raise ValueError("Training case must carry fixture_not_evidence=true")
        if qid not in reader or reader[qid]["review_state"] != "NOT_ADMITTED":
            raise ValueError(f"{qid}: missing/unexpected question-bank source state")
        if route["qrt"]["status"] == "FIRST_PASS_RECORDED":
            source = reviewed[qid]["current_demand_assessment"]
            if (source["operation"] != route["qrt"]["operation"]
                    or source["band"] != route["qrt"]["band"]
                    or source["total"] != route["qrt"]["total"]):
                raise ValueError(f"{qid}: first-pass result drift")
            actual = [route["qrt"]["factors"][f]["score"] for f in FACTORS]
            if actual != source["factors"]:
                raise ValueError(f"{qid}: first-pass numeric factor drift")
        if qid == "WEP07-03":
            candidate = pilot_by_id[qid]
            if candidate["band"] != route["sl2"]["band"] or candidate["operation"] != route["sl2"]["operation"]:
                raise ValueError("WEP07-03 pilot label drift")
        else:
            if reader[qid]["op"] != route["sl2"]["operation"] or reader[qid]["band"] != route["sl2"]["band"]:
                raise ValueError(f"{qid}: consolidated reader proposal drift")
    if len(bank["questions"]) != 74:
        raise ValueError("Question reader count drift; inventory needs a new audit.")


def apply_mutation(route: dict, path: str, value):
    obj = route
    keys = path.split(".")
    for name in keys[:-1]:
        obj = obj[name]
    obj[keys[-1]] = value


def run() -> dict:
    bundle = read(HERE / "fixtures/golden-cases.json")
    if bundle["schema"] != "g9v4-qrt-blueprint-golden-cases/v1":
        raise ValueError("Unexpected fixture catalogue schema")
    verify_documentary_sources(bundle)
    cases = {case["id"]: case for case in bundle["cases"]}
    results = []
    for case in cases.values():
        route = case["route"]
        actual = evaluate(route)
        wanted = case["expect"]
        if (actual["candidate_cell"] != wanted["candidate_cell"] or actual["release"] != wanted["release"]):
            raise AssertionError((case["id"], actual, wanted))
        for condition in wanted["contains"]:
            if condition not in actual["holds"]:
                raise AssertionError(f"{case['id']} missing hold {condition}: {actual['holds']}")
        results.append({"case": case["id"], "pass": True, "candidate_cell": actual["candidate_cell"],
                        "release": actual["release"]})
    negative = []
    for bad in bundle["negative_controls"]:
        route = deepcopy(cases[bad["based_on"]]["route"])
        apply_mutation(route, bad["mutation"]["path"], bad["mutation"]["value"])
        actual = evaluate(route)
        if bad["expected_reason"] not in actual["holds"] or actual["release"] != "HOLD":
            raise AssertionError(f"{bad['id']} failed to reject {bad['expected_reason']}")
        negative.append({"case": bad["id"], "pass": True, "reason": bad["expected_reason"]})
    return {"status": "PASS", "scope": "STRUCTURAL_AND_DOCUMENTARY_ONLY_NO_APPROVAL",
            "positive_cases": results, "negative_controls": negative}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
