"""Source-neutral PCB Core2 question-identity and reasoning-map generator.

Only source IDs, scoped occurrence UIDs, full-content SHA256 fingerprints,
author-proposed QRT/crux labels and explicit HOLD statuses are public.
NO exam stem, answer, figure, reasoning worked solution or custody proof.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path("nsejs/data/pcb-core2-identity-map.v1.json")
PIN = "f590bb80577143eb4a31c3fb8e58599ef722a624cdbde5774b88405f89f2ce51"
OPS = frozenset("RETRIEVE EXPLAIN APPLY MODEL REPRESENT SYNTHESIZE JUSTIFY".split())
SUBJECTS = {"PHYSICS": (21, 95), "CHEMISTRY": (13, 87), "BIOLOGY": (11, 85)}
PREVIEW = {
    "nsejs-optics-displacement-d3-r1", "nsejs-fluids-surface-energy-d3-r1",
    "nsejs-fluids-sound-r1", "chem-electronic-structure-d3-r1",
    "chem-phosphorus-oxyacids-d3-r1", "bio-immunology-defense-d3-r1",
    "bio-viral-genetics-d3-r1", "bio-genetics-coordination-r1",
}
ROOT_FIELDS = frozenset(
    "schema archive_sha256 mode source_custody redistribution_rights "
    "academic_admission independent_qrt_review source_originals_published "
    "module_count candidate_question_count distinct_claimed_external_ids "
    "subjects summary modules questions".split())
MODULE_FIELDS = frozenset("slug subject question_count source_bank_sha256".split())
QUESTION_FIELDS = frozenset(
    "question_uid module_slug subject ordinal claimed_external_question_id "
    "content_revision_sha256 source_year_claim proposed_qrt_operation "
    "proposed_crux_ref proposed_crux_kind independent_qrt_review "
    "verified_missing_reasoning_step figure_byte_custody source_custody "
    "final_key_custody source_rights academic_admission content_published "
    "construction_fit candidate_learning_route route_evidence "
    "source_return_verified external_id_collision".split())


def need(condition, code):
    if not condition:
        raise ValueError("PCB_CANONICAL_HOLD:" + code)


def is_sha(s):
    return isinstance(s, str) and re.fullmatch(r"[0-9a-f]{64}", s) is not None


def supplemental_slugs(root):
    result = set()
    for kind in ("chem", "physics"):
        doc = json.loads((root / (
            "nsejs/content/independent-core1-recovery-" + kind + ".v1.json"
        )).read_text("utf-8"))
        need(doc.get("academic_admission") == "HOLD" and
             doc.get("original_18_audit_equivalence") is False,
             "SUPPLEMENTAL_AUTHORITY_INVALID")
        for item in doc["items"]:
            need(item["slug"] not in result, "DUPLICATE_SUPPLEMENTAL_SLUG")
            result.add(item["slug"])
    need(len(result) == 18 and result.isdisjoint(PREVIEW),
         "SUPPLEMENTAL_LESSONS_18_DISJOINT_REQUIRED")
    return result


def validate(doc, *, root=ROOT):
    from nsejs_core2_public_catalog import REGISTER
    need(isinstance(doc, dict) and set(doc) == ROOT_FIELDS,
         "UNKNOWN_TOP_LEVEL_FIELD")
    # Independent owner-ZIP reconciliation fingerprint, over every metadata
    # field and row. No source stem/key is needed to enforce byte lineage.
    canonical = json.dumps(doc, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"), allow_nan=False)
    need(hashlib.sha256(canonical.encode("utf-8")).hexdigest() ==
         "752f7774ef3082bc6574678defb6b9a2ebcaff29624605144cac6a1507e8af82",
         "SOURCE_NEUTRAL_OWNER_ZIP_RECONCILIATION_FINGERPRINT")
    need(doc["schema"] == "grade9-pcb-core2-canonical-identity-map/v1" and
         doc["archive_sha256"] == PIN and
         doc["mode"] == "SOURCE_NEUTRAL_IDENTITY_AND_PROVISIONAL_REASONING_ONLY",
         "INVALID_SOURCE_OR_SCHEMA_PIN")
    need(doc["academic_admission"] == doc["source_custody"] ==
         doc["redistribution_rights"] == "HOLD" and
         doc["independent_qrt_review"] == "NOT_RUN" and
         doc["source_originals_published"] == 0, "ACADEMIC_PROMOTION_FORBIDDEN")
    need(doc["module_count"] == 45 and doc["candidate_question_count"] == 267 and
         doc["distinct_claimed_external_ids"] == 263, "COUNTS_INVALID")
    need(set(doc["subjects"]) == set(SUBJECTS), "MATHEMATICS_FORBIDDEN")
    for subj, (mods, questions) in SUBJECTS.items():
        need(doc["subjects"][subj] == {"modules": mods, "questions": questions},
             "SUBJECT_COUNTS_INVALID")
    expected = {slug: (subj, qty) for slug, subj, qty in REGISTER}
    module_rows = doc["modules"]
    question_rows = doc["questions"]
    need(isinstance(module_rows, list) and len(module_rows) == 45 and
         isinstance(question_rows, list) and len(question_rows) == 267,
         "45_MODULES_267_QUESTIONS_REQUIRED")
    found = {}
    for m in module_rows:
        need(isinstance(m, dict) and set(m) == MODULE_FIELDS, "MODULE_FIELDS_INVALID")
        slug = m["slug"]
        need(slug in expected and slug not in found and
             (m["subject"], m["question_count"]) == expected[slug] and
             is_sha(m["source_bank_sha256"]), "MODULE_NOT_IN_OWNER_REGISTER")
        found[slug] = m
    need(set(found) == set(expected), "MODULE_OMISSION")
    supplement = supplemental_slugs(root)
    by_mod = Counter()
    by_subj = Counter()
    fits = Counter()
    seen = set()
    aliases = defaultdict(list)
    crux_disagreements = 0
    figure_holds = 0
    for q in question_rows:
        need(isinstance(q, dict) and set(q) == QUESTION_FIELDS,
             "QUESTION_FIELDS_OR_EXAM_TEXT_LEAK")
        slug = q["module_slug"]
        need(slug in found and q["subject"] == found[slug]["subject"],
             "WRONG_SUBJECT_OR_MISSING_MODULE")
        index = q["ordinal"]
        need(type(index) is int and 1 <= index <= found[slug]["question_count"],
             "INVALID_MODULE_OCCURRENCE_INDEX")
        uid = f'g9:pcb:{q["subject"].lower()}:{slug}:{index:03d}'
        need(q["question_uid"] == uid and uid not in seen and
             is_sha(q["content_revision_sha256"]),
             "OCCURRENCE_ID_OR_DIGEST_INVALID")
        seen.add(uid)
        external = q["claimed_external_question_id"]
        need(isinstance(external, str) and
             re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]{1,120}", external) is not None,
             "EXTERNAL_ALIAS_INVALID")
        aliases[external].append(q)
        op = q["proposed_qrt_operation"]
        kind = q["proposed_crux_kind"]
        need(op in OPS and (kind in OPS or kind is None) and
             isinstance(q["proposed_crux_ref"], str) and
             0 < len(q["proposed_crux_ref"]) < 180,
             "PROVISIONAL_QRT_OR_CRUX_INVALID")
        crux_disagreements += bool(kind and kind != op)
        year = q["source_year_claim"]
        need(year is None or (type(year) is int and 2020 <= year <= 2024
                               and f"nsejs-{year}-" in slug),
             "EXAM_YEAR_MISASSIGNMENT")
        need(q["independent_qrt_review"] == "NOT_RUN" and
             q["verified_missing_reasoning_step"] is None and
             q["source_custody"] == q["final_key_custody"] ==
             q["source_rights"] == q["academic_admission"] == "HOLD" and
             q["content_published"] is False and
             q["source_return_verified"] is False and
             q["figure_byte_custody"] in ("HOLD", "NOT_ASSERTED"),
             "PER_QUESTION_AUTHORITY_FALSIFICATION")
        figure_holds += q["figure_byte_custody"] == "HOLD"
        if slug in PREVIEW:
            match = ("RELATED_ONLY_UNVERIFIED", "TOPIC_ONLY_AUTHORED_PREVIEW",
                     f'nsejs/{q["subject"].lower()}/core1/{slug}/index.html')
        elif slug in supplement:
            match = ("RELATED_ONLY_UNVERIFIED", "TOPIC_ONLY_SUPPLEMENTAL",
                     f'nsejs/{q["subject"].lower()}/core1/recovery/{slug}/index.html')
        else:
            match = ("MISSING_CONSTRUCTION", "NO_DIRECT_LESSON", None)
        need((q["construction_fit"], q["route_evidence"],
              q["candidate_learning_route"]) == match,
             "UNVERIFIED_ROUTE_FALSELY_MARKED_SUFFICIENT")
        by_mod[slug] += 1
        by_subj[q["subject"]] += 1
        fits[q["construction_fit"]] += 1
    need(all(by_mod[s] == m["question_count"] for s, m in found.items()),
         "MODULE_QUESTION_SET_INCOMPLETE")
    need(all(by_subj[s] == SUBJECTS[s][1] for s in SUBJECTS),
         "QUESTION_SUBJECT_COUNT_CHANGED")
    need(fits == Counter({"RELATED_ONLY_UNVERIFIED": 26,
                          "MISSING_CONSTRUCTION": 241}), "UNQUALIFIED_FIT_CHANGE")
    repeated = {k: g for k, g in aliases.items() if len(g) > 1}
    need(len(aliases) == 263 and len(repeated) == 4 and
         all(len(g) == 2 and
             len({r["content_revision_sha256"] for r in g}) == 2
             for g in repeated.values()), "EXTERNAL_ID_DUPLICATES_COLLAPSED")
    for group in aliases.values():
        flag = "CONFLICTING_RECORDS" if len(group) > 1 else "NONE"
        need(all(q["external_id_collision"] == flag for q in group),
             "EXTERNAL_DUPLICATE_FLAG_MISSING")
    need(crux_disagreements == 5 and figure_holds == 13,
         "UNRESOLVED_QRT_OR_FIGURE_RECONCILIATION_CHANGED")
    need(doc["summary"] == {
        "mapped_exact_qualified": 0, "topic_only_related": 26,
        "missing_construction": 241, "duplicate_external_ids": 4,
        "conflicting_qrt_crux_kind": 5, "missing_figure_custody": 13,
    }, "SUMMARY_OR_RELEASE_FALSE")


def load(*, root=ROOT):
    document = json.loads((root / DATA_PATH).read_text("utf-8"))
    validate(document, root=root)
    return document


def render(document, *, root=ROOT):
    validate(document, root=root)
    e = html.escape
    groups = []
    for subject in SUBJECTS:
        details = []
        for module in document["modules"]:
            if module["subject"] != subject:
                continue
            slug = module["slug"]
            items = [r for r in document["questions"] if r["module_slug"] == slug]
            trs = []
            for r in items:
                if r["construction_fit"] == "RELATED_ONLY_UNVERIFIED":
                    route = r["candidate_learning_route"].removeprefix("nsejs/")
                    practice = ('<a href="../' + e(route, quote=True) +
                                '">Related practice, NOT sufficient teaching</a>')
                else:
                    practice = "Missing construction"
                flags = []
                if r["external_id_collision"] == "CONFLICTING_RECORDS":
                    flags.append("Duplicated external ID")
                if r["proposed_crux_kind"] and r["proposed_crux_kind"] != r["proposed_qrt_operation"]:
                    flags.append("Proposed operation/crux conflict")
                if r["figure_byte_custody"] == "HOLD":
                    flags.append("Unverified figure")
                trs.append('<tr><th scope="row"><code>' + e(r["question_uid"]) +
                           '</code></th><td>' + e(r["claimed_external_question_id"]) +
                           '</td><td>' + e(r["proposed_qrt_operation"]) +
                           ' (provisional)</td><td>' + e(r["proposed_crux_ref"]) +
                           '</td><td>' + practice + '</td><td>' +
                           e("; ".join(flags) or "Source/QRT HOLD") + '</td></tr>')
            details.append('<details id="module-' + e(slug) + '"><summary>' +
                           e(slug.replace("-", " ")) + " · " + str(len(items)) +
                           ' candidate(s)</summary><div class="scroll"><table><thead>'
                           '<tr><th>Canonical question occurrence</th><th>External label</th>'
                           '<th>Proposed operation</th><th>Proposed crux</th>'
                           '<th>Learning construction</th><th>Unresolved evidence</th>'
                           '</tr></thead><tbody>' + "".join(trs) +
                           '</tbody></table></div></details>')
        groups.append('<section id="' + subject.lower() + '"><h2>' +
                      subject.title() + '</h2>' + "".join(details) + '</section>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>NSEJS Core2 · 267 question identity and reasoning map</title>'
            '<style>body{background:#eff6f8;color:#143746;font:16px/1.6 system-ui;margin:0}'
            'main{max-width:1240px;margin:auto;padding:25px}a{color:#075b7d}'
            'a:focus-visible,summary:focus-visible{outline:3px solid #b58b45;outline-offset:3px}'
            'nav{display:flex;flex-wrap:wrap;gap:16px}nav a{display:inline-flex;align-items:center;min-height:56px}'
            'section{background:white;border:1px solid #c9dce3;border-radius:12px;padding:18px;margin:20px 0}'
            'details{border-top:1px solid #d1e1e6}summary{cursor:pointer;padding:15px 8px;min-height:56px;font-weight:700}'
            '.scroll{overflow:auto}table{border-collapse:collapse;width:100%;min-width:870px}'
            'td,th{border-bottom:1px solid #dce7ea;padding:10px;text-align:left;vertical-align:top}'
            'th{background:#eef6f8}code{overflow-wrap:anywhere}.hold{padding:18px;border-left:5px solid #af812f;background:#fff7e5}'
            '@media(max-width:700px){main{padding:12px}section{padding:12px}}'
            '</style></head><body><main><nav><a href="index.html">Core2 inventory</a>'
            '<a href="../index.html">NSEJS hub</a><a href="../../architecture/index.html">Agent guidebook</a></nav>'
            '<h1>45 Core2 modules · 267 question identities and proposed reasoning moves</h1>'
            '<p class="hold"><strong>SOURCE / RIGHTS / QRT / ACADEMIC HOLD.</strong> '
            'This page provides a question-level <em>source-neutral inventory</em>, '
            'not an original exam-question reader. External labels are unverified aliases. '
            'The ZIP questions, answers, figures, original paper keys and solution text '
            'have NOT been published. All QRT labels and crux references are author proposals.</p>'
            '<p><strong>26 related-topic practice links · 241 missing constructions · '
            'zero independently qualified exact-question return routes.</strong> '
            'Four duplicate external labels, five provisional QRT/crux disagreements '
            'and thirteen unverified figure references remain under review.</p>' +
            "".join(groups) +
            '<p>Mathematics excluded. A working link never proves exact-task teaching sufficiency '
            'or authentic source admission.</p></main></body></html>')


def stage(out, *, root=ROOT):
    data = load(root=root)
    target = out / "nsejs/core2"
    target.mkdir(parents=True, exist_ok=True)
    (target / "question-map.html").write_text(render(data, root=root), "utf-8")
    (target / "question-map.v1.json").write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", "utf-8")
    return {"module_count": 45, "candidate_questions": 267,
            "related_only": 26, "missing_construction": 241,
            "exact_qualified": 0, "academic_admission": "HOLD"}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--stage", type=Path)
    args = ap.parse_args()
    if args.stage:
        print(json.dumps(stage(args.stage, root=args.root), sort_keys=True))
    else:
        print(json.dumps(load(root=args.root)["summary"], sort_keys=True))
