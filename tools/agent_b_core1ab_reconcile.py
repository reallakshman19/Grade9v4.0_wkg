"""Agent B source-neutral per-construction census, B1–B7 ledger and custody gap report.

Do not infer canonical identity from displayed exam numbers. This does not adjudicate
subject science, source authenticity or academic release. No original stems are emitted.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOOKUP = ROOT / "docs" / "agent-b-physics-uid-lookup-r1.json"
BUILDERS = (
    "build_d3_batch2_modules.py",
    "build_d3_expansion_modules.py",
    "build_physics_fluids_core1.py",
    "build_bio_genetics_core1.py",
)
CONSTRUCTION_TEST_GLOB = "test_*core1*.py"
OWNER_SCOPE_COUNT = 27
ID_PATTERN = re.compile(r"""(?P<key>construction_id|target_question_id)\s*['"]\]\s*==\s*['"](?P<value>[^'"]+)['"]""")
RE_PATH = re.compile(r"""workspace/output/([a-z0-9-]+)""")
RE_PARTS = re.compile(r"""['"]workspace['"]\s*/\s*['"]output['"]\s*/\s*['"]([a-z0-9-]+)['"]""")


def subject_of(construction_id: str) -> str:
    if construction_id.startswith("PHYS-"):
        return "PHYSICS"
    if construction_id.startswith("CHEM-"):
        return "CHEMISTRY"
    if construction_id.startswith("BIO-"):
        return "BIOLOGY"
    return "UNKNOWN"


def extract_construction(test_path: Path) -> dict | None:
    source = test_path.read_text(encoding="utf-8")
    matches: dict[str, str] = {}
    for m in ID_PATTERN.finditer(source):
        if m.group("key") in matches and matches[m.group("key")] != m.group("value"):
            raise ValueError(f"Conflicting {m.group('key')} declarations in {test_path.name}")
        matches[m.group("key")] = m.group("value")
    if not {"construction_id", "target_question_id"} <= matches.keys():
        return None
    a = RE_PATH.search(source) or RE_PARTS.search(source)
    return {
        "test": test_path.name,
        "construction_id": matches["construction_id"],
        "target_question_id": matches["target_question_id"],
        "subject": subject_of(matches["construction_id"]),
        "expected_module": a.group(1) if a else None,
    }


def load_lookup(path: Path = LOOKUP) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["records"]
    if len(rows) != 50 or len({x["source_id"] for x in rows}) != 50:
        raise ValueError("Agent A pinned 50-item interface is missing or malformed")
    if any(x.get("qrt_adjudication") != "HOLD" or x.get("academic_release") != "NOT_ADMITTED" for x in rows):
        raise ValueError("Invalid source authority state: do not silently admit a source or QRT nomination")
    return data


def match_uid(construction: dict, lookup: dict) -> dict:
    """Display-number matches propose review candidates only, never authenticated bindings."""
    subject, target = construction["subject"], construction["target_question_id"]
    if subject != "PHYSICS":
        return {"match": "OUTSIDE_PHYSICS_LOOKUP", "uid": None, "candidates": [], "binding_status": "HOLD"}
    rows = lookup["records"]
    exact = [x for x in rows if x["source_id"] == target]
    if len(exact) == 1:
        return {"match": "EXACT_SOURCE_OCCURRENCE_ID", "uid": exact[0]["question_uid"],
                "candidates": [exact[0]["question_uid"]], "binding_status": "HOLD"}
    same_label = [x for x in rows if x["displayed_id"] == target]
    candidates = sorted(x["question_uid"] for x in same_label)
    if len(candidates) == 1:
        return {"match": "DISPLAYED_ALIAS_ONLY", "uid": None, "candidates": candidates,
                "binding_status": "HOLD"}
    if len(candidates) > 1:
        return {"match": "AMBIGUOUS_DISPLAYED_ALIAS", "uid": None, "candidates": candidates,
                "binding_status": "HOLD"}
    return {"match": "UNMAPPED", "uid": None, "candidates": [], "binding_status": "HOLD"}


def _load_candidate(module_dir: Path, construct: dict) -> dict:
    """Use only candidate JSON. Never copy original bank stems into an audit report."""
    if not module_dir.is_dir():
        return {"artifact": "NOT_RECEIVED", "B3": "HOLD", "B4": "HOLD", "B5": "NOT_RUN", "B6": "HOLD",
                "findings": ["NO_GENERATED_CANDIDATE"]}
    paths = {name: module_dir / (name + ".json")
             for name in ("core1a_construction", "core1b_reconstruction", "witness")}
    if any(not p.is_file() for p in paths.values()):
        return {"artifact": "INCOMPLETE", "B3": "HOLD", "B4": "HOLD", "B5": "NOT_RUN", "B6": "HOLD",
                "findings": ["CANDIDATE_FILE_MISSING"]}
    try:
        a, b, w = [json.loads(paths[name].read_text(encoding="utf-8")) for name in paths]
    except (ValueError, OSError):
        return {"artifact": "UNREADABLE", "B3": "FAIL", "B4": "FAIL", "B5": "NOT_RUN", "B6": "HOLD",
                "findings": ["INVALID_CANDIDATE_BYTES"]}
    findings = []
    if a.get("construction_id") != construct["construction_id"] or b.get("construction_id") != construct["construction_id"]:
        findings.append("CONSTRUCTION_ID_MISMATCH")
    if a.get("target_question_id") != construct["target_question_id"] or b.get("target_question_id") != construct["target_question_id"]:
        findings.append("TARGET_ID_MISMATCH")
    if a.get("academic_status") != "HOLD:ACADEMIC_ADMISSION" or b.get("academic_status") != "HOLD:ACADEMIC_ADMISSION":
        findings.append("ACADEMIC_ADMISSION_UNSUPPORTED")
    required_a = ("teaching_path", "worked_conceptual_anchor", "misconceptions", "exit_task")
    b3 = "STRUCTURE_PRESENT_REVIEW_REQUIRED" if all(a.get(k) for k in required_a) else "HOLD"
    if b3 == "HOLD":
        findings.append("B3_TEACHING_SPANS_INCOMPLETE")
    stages = b.get("stages", {})
    required_b = ("stage_2_attempt", "stage_3_reconstruct", "stage_4_diagnose",
                  "stage_5_repair", "stage_6_boundary_test")
    b6 = "STRUCTURE_PRESENT_REVIEW_REQUIRED" if all(stages.get(k) for k in required_b) else "HOLD"
    if b6 == "HOLD":
        findings.append("B6_DIAGNOSIS_OR_TRANSFER_MISSING")
    w_c1b = w.get("core1b", {})
    if w.get("review_receipts"):
        findings.append("REVIEW_RECEIPTS_REQUIRE_INDEPENDENT_AUTHENTICATION")
    if w_c1b.get("attempt_events"):
        findings.append("PRODUCER_EVENTS_NOT_BROWSER_VERIFIED")
    if not b.get("fresh_context_ref", "").startswith(("AB-PRACTICE-", "PHYS-NSEJS-")):
        findings.append("UNPROVEN_FRESH_CONTEXT_ID")
    prompt = str(stages.get("stage_2_attempt", {}).get("prompt", ""))
    if not prompt.strip():
        findings.append("B4_FRESH_PROMPT_MISSING")
    html_page = module_dir / "learning_journey.html"
    if html_page.is_file():
        page = html_page.read_text(encoding="utf-8")
        if 'id="content-core1b"' in page and "Stage 3" in page and "data-agent-b-core1b" not in page:
            findings.append("B5_CORE1B_ANSWER_VISIBILITY_REVIEW_REQUIRED")
        if "<iframe" in page.lower():
            findings.append("B5_IFRAME_UNSUPPORTED")
        b5 = "GENERATED_PAGE_REVIEW_REQUIRED"
    else:
        findings.append("B5_RUNTIME_NOT_RECEIVED")
        b5 = "NOT_RUN"
    if "TARGET_ID_MISMATCH" in findings or "CONSTRUCTION_ID_MISMATCH" in findings:
        b3 = b6 = "FAIL"
    return {"artifact": "GENERATED", "B3": b3, "B4": "REVIEW_REQUIRED" if prompt.strip() else "HOLD",
            "B5": b5, "B6": b6, "findings": sorted(set(findings))}


def generate_in_temp(repo_root: Path, out: Path) -> list[dict]:
    """Only permitted public authoring scripts. Never fabricate missing source custody."""
    events = []
    env = dict(os.environ)
    env["PYTHONPATH"] = str(repo_root) + os.pathsep + env.get("PYTHONPATH", "")
    for name in BUILDERS:
        source = repo_root / name
        if not source.is_file():
            events.append({"builder": name, "status": "NOT_RECEIVED"})
            continue
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        try:
            proc = subprocess.run([sys.executable, str(dest)], cwd=out, env=env,
                                  capture_output=True, text=True, timeout=60)
            status = "EXECUTED" if proc.returncode == 0 else "BUILD_FAILED_HOLD"
            events.append({"builder": name, "status": status, "returncode": proc.returncode})
        except (subprocess.TimeoutExpired, OSError):
            events.append({"builder": name, "status": "BUILD_NOT_RUN_HOLD"})
    return events


def census(repo_root: Path = ROOT, lookup_path: Path = LOOKUP,
           generated_root: Path | None = None) -> dict:
    lookup = load_lookup(lookup_path)
    tests = sorted((repo_root / "tests").glob(CONSTRUCTION_TEST_GLOB))
    inventory = [x for p in tests if (x := extract_construction(p)) is not None]
    by_id = [x["construction_id"] for x in inventory]
    if len(by_id) != len(set(by_id)):
        raise ValueError("Duplicate Core1A/1B construction ID in repository tests")
    if generated_root is None:
        generated_root = repo_root / "workspace/output"
    rows = []
    for item in inventory:
        binding = match_uid(item, lookup)
        module_name = item.get("expected_module")
        evidence = _load_candidate(generated_root / module_name, item) if module_name else {
            "artifact": "MODULE_PATH_NOT_DECLARED", "B3": "HOLD", "B4": "HOLD",
            "B5": "NOT_RUN", "B6": "HOLD", "findings": ["NO_MODULE_DIRECTORY"]}
        item = {**item, **binding, **evidence,
                "B1": "HOLD", "B2": "HOLD", "B7": "HOLD",
                "academic_status": "HOLD",
                "science_review": "NOT_INDEPENDENTLY_QUALIFIED"}
        if item["match"] == "AMBIGUOUS_DISPLAYED_ALIAS":
            item["findings"].append("DISPLAYED_ID_COLLISION")
        if item["match"] == "UNMAPPED":
            item["findings"].append("NO_AGENT_A_SOURCE_OCCURRENCE")
        rows.append(item)
    mapped = {}
    for row in rows:
        mapped[row["match"]] = mapped.get(row["match"], 0) + 1
    return {
        "schema": "grade9-agent-b-core1ab-reconciliation/v1",
        "agent_a_interface_commit": lookup["source_head"],
        "agent_a_index_blob_sha": lookup["source_blob_sha"],
        "candidate_owner": "Agent B: Core1A and Core1B only",
        "source_authority": "Agent A; no Agent B registry mutation",
        "owner_reported_count": OWNER_SCOPE_COUNT,
        "test_backed_construction_count": len(rows),
        "count_discrepancy": OWNER_SCOPE_COUNT-len(rows),
        "count_discrepancy_status": "HOLD" if len(rows) != OWNER_SCOPE_COUNT else "NONE",
        "mapping_counts": dict(sorted(mapped.items())),
        "academic_admission": "HOLD",
        "release": "NOT_ADMITTED",
        "note": "Display matches are provisional and never bind canonical source identity. Missing workspace files remain NOT_RECEIVED.",
        "constructions": rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--lookup", type=Path, default=LOOKUP)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--generate", action="store_true",
                    help="Run only four public root-level builders in temporary isolated workspace")
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.generate:
        with tempfile.TemporaryDirectory(prefix="agent_b_census_") as folder:
            output = Path(folder)
            generator_events = generate_in_temp(args.root, output)
            report = census(args.root, args.lookup, output/"workspace"/"output")
    else:
        generator_events = []
        report = census(args.root, args.lookup)
    report["generator_events"] = generator_events
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(f"Agent B {report['test_backed_construction_count']}/{report['owner_reported_count']} "
          f"census; {report['mapping_counts']}; academic=HOLD; report={args.out}")
    for event in generator_events:
        print("builder:", event["builder"], event["status"])
    # A successful census command is a receipt for reconciliation only, never academic PASS.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
