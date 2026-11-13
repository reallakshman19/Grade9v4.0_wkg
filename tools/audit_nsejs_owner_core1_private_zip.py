#!/usr/bin/env python3
"""Audit a PRIVATE Owner Core1 candidate ZIP without publishing private content.

The receipt proves byte integrity and specific candidate invariants only.
It cannot approve exam-source custody, rights, scientific review, QRT or B1-B7.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zipfile

EXPECTED_ALIAS = {
    "chem-atomic-structure-r1",
    "chem-atomic-bonding-r1",
}
SUBJECTS = {"PHYSICS": 16, "CHEMISTRY": 7, "BIOLOGY": 3}


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def read_json(archive: zipfile.ZipFile, name: str) -> dict:
    value = json.loads(archive.read(name))
    require(isinstance(value, dict), "INVALID_JSON_OBJECT:" + name)
    return value



def check_single_core2_bank_link(slug: str, bank_bytes: bytes,
                                 module: dict, question: dict) -> None:
    """Compare one private Core1 bank to PR115's public digest-only metadata.

    A matching digest is *lineage*, never source authenticity or QRT approval.
    """
    require(module.get("slug") == slug and
            question.get("module_slug") == slug,
            "CORE2_MODULE_IDENTITY_MISMATCH:" + slug)
    require(sha(bank_bytes) == module.get("source_bank_sha256"),
            "CORE2_BANK_SHA256_MISMATCH:" + slug)
    bank = json.loads(bank_bytes)
    rows = bank.get("questions")
    require(isinstance(rows, list) and len(rows) == 1,
            "CORE2_SOURCE_BANK_NOT_SINGLE_QUESTION:" + slug)
    source_question = rows[0]
    require(isinstance(source_question, dict) and
            source_question.get("id") == question.get("claimed_external_question_id"),
            "CORE2_EXTERNAL_ID_MISMATCH:" + slug)
    full_revision = json.dumps(source_question, sort_keys=True,
                               ensure_ascii=False, separators=(",", ":"),
                               allow_nan=False).encode("utf-8")
    require(sha(full_revision) == question.get("content_revision_sha256"),
            "CORE2_FULL_REVISION_SHA256_MISMATCH:" + slug)
    subject = module.get("subject")
    require(subject in SUBJECTS and
            question.get("subject") == subject and
            question.get("ordinal") == 1 and
            question.get("question_uid") ==
            f"g9:pcb:{subject.lower()}:{slug}:001",
            "CORE2_CANONICAL_OCCURRENCE_MISMATCH:" + slug)
    require(question.get("academic_admission") == "HOLD" and
            question.get("source_custody") == "HOLD" and
            question.get("independent_qrt_review") == "NOT_RUN" and
            question.get("source_return_verified") is False and
            question.get("content_published") is False,
            "CORE2_SOURCE_OR_ACADEMIC_PROMOTION:" + slug)
    # Two private bank files bind one historical Chemistry construction ID;
    # they are different Core2 questions, NOT interchangeable source UIDs.
    if slug == "chem-atomic-bonding-r1":
        require(question.get("construction_fit") == "MISSING_CONSTRUCTION" and
                question.get("candidate_learning_route") is None,
                "CHEMISTRY_ALIAS_FALSELY_QUALIFIED")
    else:
        require(question.get("construction_fit") == "RELATED_ONLY_UNVERIFIED" and
                question.get("candidate_learning_route") is not None,
                "CORE2_RELATED_ROUTE_PROMOTED_OR_MISSING:" + slug)


def verify_core2_bank_linkage(private_banks: dict[str, bytes], *,
                             repository_root: Path) -> dict:
    """Join 27 private Core1 banks to PR115 45/267 canonical metadata by SHA.

    The complete public registry is itself validated through PR115's strict
    fingerprint validator; no private stem, answer or figure is returned.
    """
    from tools.nsejs_pcb_identity_map import load as load_core2
    require(len(private_banks) == 27, "CORE1_BANK_LINKAGE_27_REQUIRED")
    public = load_core2(root=repository_root)
    modules = {item["slug"]: item for item in public["modules"]}
    questions = {item["module_slug"]: item for item in public["questions"]
                 if item["module_slug"] in private_banks}
    require(len(questions) == 27 and
            set(private_banks) == set(questions) and
            set(private_banks).issubset(modules),
            "CORE1_CORE2_SOURCE_OCCURRENCE_JOIN_INCOMPLETE")
    for slug, bank_bytes in private_banks.items():
        check_single_core2_bank_link(slug, bank_bytes, modules[slug],
                                     questions[slug])
    aliases = ["chem-atomic-bonding-r1", "chem-atomic-structure-r1"]
    a, b = [questions[s] for s in aliases]
    require(a["claimed_external_question_id"] ==
            b["claimed_external_question_id"] and
            a["question_uid"] != b["question_uid"] and
            a["content_revision_sha256"] != b["content_revision_sha256"] and
            a["external_id_collision"] == b["external_id_collision"] ==
            "CONFLICTING_RECORDS",
            "CORE1_CHEMISTRY_ALIAS_COLLISION_UNRESOLVED")
    require(sum(item["construction_fit"] == "RELATED_ONLY_UNVERIFIED"
                for item in questions.values()) == 26 and
            sum(item["construction_fit"] == "MISSING_CONSTRUCTION"
                for item in questions.values()) == 1,
            "CORE1_CORE2_LEARNING_FIT_COUNTS_UNEXPECTED")
    return {
        "status": "BYTE_AND_REVISION_MATCH_ACADEMIC_HOLD",
        "core1_private_bank_shas_matched": 27,
        "core1_private_question_revisions_matched": 27,
        "core1_source_question_uid_count": 27,
        "unique_core1_constructions": 26,
        "related_topic_only": 26,
        "missing_construction": 1,
        "remaining_core2_occurrences_without_proven_exact_routes": 267,
        "missing_figure_custody_core2": public["summary"]["missing_figure_custody"],
        "producer_qrt_conflicts_core2": public["summary"]["conflicting_qrt_crux_kind"],
        "source_custody": "HOLD",
        "independent_qrt": "NOT_RUN",
        "academic_admission": "HOLD",
    }


def check(candidate_path: Path, original_path: Path | None = None,
          candidate_sha: str | None = None, original_sha: str | None = None,
          core2_repository_root: Path | None = None) -> dict:
    require(candidate_path.is_file(), "CANDIDATE_ARCHIVE_MISSING")
    digest = sha(candidate_path.read_bytes())
    if candidate_sha:
        require(digest == candidate_sha, "CANDIDATE_ARCHIVE_SHA_MISMATCH")

    with zipfile.ZipFile(candidate_path) as candidate:
        require(candidate.testzip() is None, "CORRUPT_CANDIDATE_ARCHIVE")
        files = {name for name in candidate.namelist() if not name.endswith("/")}
        folders = sorted({
            name.split("/")[1] for name in files
            if name.startswith("modules/") and name.count("/") >= 2
        })
        require(len(files) == 165 and len(folders) == 27, "CANDIDATE_INVENTORY_CHANGED")
        mapping: dict[str, list[str]] = defaultdict(list)
        by_subject = Counter()
        for folder in folders:
            root = "modules/" + folder + "/"
            needed = ("bank.json", "core1a_construction.json",
                      "core1b_reconstruction.json", "learning_journey.html",
                      "witness.json")
            require(all(root + name in files for name in needed),
                    "REQUIRED_MEMBER_MISSING:" + folder)
            core_a = candidate.read(root + "core1a_construction.json")
            core_b = candidate.read(root + "core1b_reconstruction.json")
            a, b = json.loads(core_a), json.loads(core_b)
            witness = read_json(candidate, root + "witness.json")
            require(a.get("status") == "CANDIDATE" and
                    b.get("status") == "CANDIDATE" and
                    witness.get("status") == "CANDIDATE",
                    "CANDIDATE_STATUS_NOT_EXPLICIT:" + folder)
            require(a.get("academic_status", "").startswith("HOLD") and
                    (b.get("academic_status", "").startswith("HOLD") or
                     b.get("academic_status") == "UNREVIEWED_CANDIDATE"),
                    "ACADEMIC_STATUS_PROMOTED:" + folder)
            require(witness["core1a"]["content_sha256"] == "sha256:" + sha(core_a) and
                    witness["core1b"]["task_sha256"] == "sha256:" + sha(core_b),
                    "WITNESS_HASH_MISMATCH:" + folder)
            require(not witness.get("review_receipts"),
                    "INDEPENDENT_REVIEW_CLAIM_UNAUTHORIZED:" + folder)
            cid = a.get("construction_id")
            require(cid and b.get("construction_id") == cid,
                    "CONSTRUCTION_ID_MISMATCH:" + folder)
            mapping[cid].append(folder)
            prefix = folder.split("-", 1)[0]
            subject = ("PHYSICS" if prefix in ("nsejs", "ioqjs") else
                       "CHEMISTRY" if prefix == "chem" else
                       "BIOLOGY" if prefix == "bio" else "UNKNOWN")
            require(subject != "UNKNOWN", "UNEXPECTED_SUBJECT:" + folder)
            by_subject[subject] += 1

        require(len(mapping) == 26, "UNIQUE_CONSTRUCTION_COUNT_MISMATCH")
        aliases = {cid: value for cid, value in mapping.items() if len(value) > 1}
        require(len(aliases) == 1 and
                set(next(iter(aliases.values()))) == EXPECTED_ALIAS,
                "CHEMISTRY_ALIAS_INCONSISTENT")
        require(by_subject == Counter({"PHYSICS": 16, "CHEMISTRY": 8, "BIOLOGY": 3}),
                "SUBJECT_FOLDER_CENSUS_MISMATCH")
        manifest = read_json(candidate, "MANIFEST.json")
        require(manifest.get("total_modules") == 26 and
                manifest.get("archive_folder_count") == 27 and
                manifest.get("breakdown_by_subject") == {
                    "Physics": 16, "Chemistry": 7, "Biology": 3},
                "MANIFEST_COUNTS_INCONSISTENT")
        require(manifest.get("source_authentication") == "HOLD" and
                manifest.get("independent_science_review") == "NOT_RUN" and
                manifest.get("academic_status") == "HOLD",
                "MANIFEST_ACADEMIC_PROMOTION")

        chem = read_json(candidate,
                         "modules/chem-chemical-substances-r1/core1b_reconstruction.json")
        c2 = chem["stages"]["stage_2_attempt"]
        require("3.585" in c2["prompt"] and "3.625" not in c2["prompt"] and
                "65.4" in c2["produces"] and
                abs((2.035 * 78 - 3.585 * 16)/(3.585 - 2.035) - 65.4) < 1e-9,
                "ZINC_STOICHIOMETRY_NOT_CORRECTED")

        mirror = read_json(candidate,
                          "modules/nsejs-optics-lens-mirror-d3-r1/core1b_reconstruction.json")
        stage2, stage3 = mirror["stages"]["stage_2_attempt"], mirror["stages"]["stage_3_reconstruct"]
        answers = " ".join(stage2["accepted"])
        route = " ".join(x["step_answer"] for x in stage3["route"])
        require("10 cm" in answers and "30 cm" in route and "10 cm" in route and
                "60 cm" not in route and "40 cm" not in route,
                "LENS_MIRROR_GEOMETRY_NOT_CORRECTED")

        lens = read_json(candidate,
                        "modules/ioqjs-optics-conjugate-d3-r1/core1b_reconstruction.json")
        task = lens["stages"]["stage_2_attempt"]
        accepted = " | ".join(task["accepted"])
        require("18" in accepted and "6" in accepted and
                "9 cm" not in accepted and
                "strictly greater than 2f" in lens["stages"]["stage_6_boundary_test"]["answer"],
                "CONJUGATE_OBJECT_DISTANCES_NOT_CORRECTED")

        magnet = candidate.read(
            "modules/nsejs-magnetism-r1/learning_journey.html").decode("utf-8")
        magnetic_witness = read_json(candidate,
                                    "modules/nsejs-magnetism-r1/witness.json")
        require("NOT the authenticated original" in magnet and
                "Flawed Key" not in magnet and "[Valid:" not in magnet and
                "[Invalid:" not in magnet and
                magnetic_witness["source_and_physics"].get(
                    "original_figure_custody") == "HOLD_LOCATED_OFFICIAL_C51_Q44_NO_BYTE_HASH_OR_RIGHTS" and
                magnetic_witness["source_and_physics"].get(
                    "paper_code_crosswalk", {}).get("official_code51_question") == 44 and
                magnetic_witness["source_and_physics"].get(
                    "paper_code_crosswalk", {}).get("official_code54_question") == 28 and
                magnetic_witness["source_and_physics"].get(
                    "paper_code_crosswalk", {}).get("source_paper_bytes_sha256") is None,
                "MAGNETISM_SOURCE_FIGURE_HOLD_MISSING")

        # Static presence audit only: a page with six headings is not a
        # six-stage protected learner. Do not turn these counts into PASS.
        storage_tokens = ("localstorage", "sessionstorage", "indexeddb")
        original_html_with_storage_api = sum(
            any(token in candidate.read("modules/" + folder + "/learning_journey.html")
                .decode("utf-8").lower() for token in storage_tokens)
            for folder in folders
        )

        private_banks = {
            slug: candidate.read("modules/" + slug + "/bank.json")
            for slug in folders
        }
        core2_linkage = (
            verify_core2_bank_linkage(private_banks,
                                     repository_root=core2_repository_root)
            if core2_repository_root is not None
            else {"status": "NOT_RUN_NO_PUBLIC_CORE2_INDEX"}
        )

        if original_path:
            require(original_path.is_file(), "ORIGINAL_ARCHIVE_MISSING")
            original_digest = sha(original_path.read_bytes())
            if original_sha:
                require(original_digest == original_sha,
                        "ORIGINAL_ARCHIVE_SHA_MISMATCH")
            with zipfile.ZipFile(original_path) as original:
                require(original.testzip() is None, "ORIGINAL_ARCHIVE_CORRUPT")
                for folder in folders:
                    bank = "modules/" + folder + "/bank.json"
                    require(candidate.read(bank) == original.read(bank),
                            "ORIGINAL_SOURCE_BANK_MUTATED:" + folder)
        else:
            original_digest = None

        return {
            "status": "CANDIDATE_INVARIANTS_PASS_SOURCE_HOLD",
            "candidate_sha256": digest,
            "original_sha256": original_digest,
            "archive_members": len(files),
            "folders": 27,
            "unique_construction_ids": 26,
            "unique_subject_counts": SUBJECTS,
            "chemistry_alias_count": 1,
            "core1a_witness_hashes": 27,
            "core1b_witness_hashes": 27,
            "source_bank_bytes_compared": 27 if original_path else 0,
            "pr115_core2_private_source_lineage": core2_linkage,
            "specific_science_fixes_checked": 3,
            "private_original_html_storage_api_present": original_html_with_storage_api,
            "private_original_html_first_attempt_persistence": "HOLD_NOT_PROVEN",
            "private_original_html_browser_tests": "NOT_RUN_BY_THIS_TOOL",
            "original_magnetism_figure": "HOLD_RAW_BYTE_HASH_AND_RIGHTS",
            "independent_review": "NOT_RUN",
            "academic_admission": "HOLD",
            "full_python_qa": "NOT_RUN_BY_THIS_TOOL",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--original", type=Path)
    parser.add_argument("--candidate-sha256")
    parser.add_argument("--original-sha256")
    parser.add_argument("--core2-repository-root", type=Path,
                        help="Opt in to PR115 strict 45/267 metadata lineage join")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    try:
        receipt = check(args.candidate, args.original, args.candidate_sha256,
                        args.original_sha256, args.core2_repository_root)
    except (ValueError, KeyError, IndexError, TypeError, OSError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}))
        return 1
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
