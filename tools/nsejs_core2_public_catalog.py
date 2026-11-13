"""Public-safe Core2 registry derived from Owner ZIP manifest, without exam text.

Only metadata is checked in. User-supplied archive bytes, original exam papers,
keys, stems, drawings and unapproved completed solutions are NOT published.
Maths is deliberately excluded. This is *not* a Core2 exam qualification.
"""
from __future__ import annotations
import hashlib
import html
import json
from pathlib import Path

SOURCE_ARCHIVE_SHA256 = "f590bb80577143eb4a31c3fb8e58599ef722a624cdbde5774b88405f89f2ce51"
SOURCE_STATUS = "SOURCE_CUSTODY_NOT_ESTABLISHED"
SCHEMA = "grade9-nsejs-core2-archive-metadata/v1"
# slug, subject, count: verified against exactly the 45 non-Mathematics
# per-module bank.json objects in Owner's independently SHA-checked ZIP.
REGISTER = (
("bio-environment-resources-r1","BIOLOGY",1),
("bio-genetics-coordination-r1","BIOLOGY",1),
("bio-immunology-defense-d3-r1","BIOLOGY",1),
("bio-life-processes-r1","BIOLOGY",1),
("bio-organisation-living-world-r1","BIOLOGY",1),
("bio-viral-genetics-d3-r1","BIOLOGY",1),
("chem-atomic-bonding-r1","CHEMISTRY",1),
("chem-atomic-structure-r1","CHEMISTRY",1),
("chem-chemical-substances-r1","CHEMISTRY",1),
("chem-electronic-structure-d3-r1","CHEMISTRY",1),
("chem-eudiometry-d3-r1","CHEMISTRY",1),
("chem-matter-mole-r1","CHEMISTRY",1),
("chem-phosphorus-oxyacids-d3-r1","CHEMISTRY",1),
("chem-redox-titration-d3-r1","CHEMISTRY",1),
("ioqjs-optics-conjugate-d3-r1","PHYSICS",1),
("nsejs-2020-biology-r1","BIOLOGY",8),
("nsejs-2020-chemistry-r1","CHEMISTRY",8),
("nsejs-2020-physics-r1","PHYSICS",8),
("nsejs-2021-biology-r1","BIOLOGY",11),
("nsejs-2021-chemistry-r1","CHEMISTRY",11),
("nsejs-2021-physics-r1","PHYSICS",11),
("nsejs-2022-biology-r1","BIOLOGY",20),
("nsejs-2022-chemistry-r1","CHEMISTRY",20),
("nsejs-2022-physics-r1","PHYSICS",20),
("nsejs-2023-biology-r1","BIOLOGY",20),
("nsejs-2023-chemistry-r1","CHEMISTRY",20),
("nsejs-2023-physics-r1","PHYSICS",20),
("nsejs-2024-biology-r1","BIOLOGY",20),
("nsejs-2024-chemistry-r1","CHEMISTRY",20),
("nsejs-2024-physics-r1","PHYSICS",20),
("nsejs-circuits-cube-d3-r1","PHYSICS",1),
("nsejs-circuits-ladder-d3-r1","PHYSICS",1),
("nsejs-circuits-r1","PHYSICS",1),
("nsejs-electrostatics-deflection-d3-r1","PHYSICS",1),
("nsejs-electrostatics-r1","PHYSICS",1),
("nsejs-fluids-sound-r1","PHYSICS",1),
("nsejs-fluids-surface-energy-d3-r1","PHYSICS",1),
("nsejs-magnetism-r1","PHYSICS",1),
("nsejs-magnetism-terminal-d3-r1","PHYSICS",1),
("nsejs-mechanics-r1","PHYSICS",1),
("nsejs-optics-displacement-d3-r1","PHYSICS",1),
("nsejs-optics-lens-mirror-d3-r1","PHYSICS",1),
("nsejs-optics-prism-d3-r1","PHYSICS",1),
("nsejs-optics-r1","PHYSICS",1),
("nsejs-optics-screw-lens-d3-r1","PHYSICS",1),
)
assert len(REGISTER) == 45
assert len({r[0] for r in REGISTER}) == 45
assert sum(row[2] for row in REGISTER) == 267
assert {(s,sum(n for _,ss,n in REGISTER if s==ss),sum(s==ss for _,ss,_ in REGISTER))
        for s in ("PHYSICS","CHEMISTRY","BIOLOGY")} == {
            ("PHYSICS",95,21),("CHEMISTRY",87,13),("BIOLOGY",85,11)}
assert not any("math" in slug or subject=="MATHEMATICS" for slug,subject,_ in REGISTER)


def registry() -> dict:
    rows=[{"slug":slug, "subject":subject,
           "unverified_candidate_question_count":number,
           "student_question_route":None,
           "source_custody":SOURCE_STATUS,
           "academic_admission":"HOLD",
           "original_exam_authenticity":"NOT_ESTABLISHED",
           "public_question_text":False}
          for slug,subject,number in REGISTER]
    return {"schema":SCHEMA,"status":"METADATA_CATALOG_ONLY",
            "academic_admission":"HOLD","redistribution_rights":"HOLD",
            "source_archive_sha256":SOURCE_ARCHIVE_SHA256,
            "module_count":45,"candidate_question_count":267,
            "subjects":{"PHYSICS":{"modules":21,"candidates":95},
                        "CHEMISTRY":{"modules":13,"candidates":87},
                        "BIOLOGY":{"modules":11,"candidates":85}},
            "original_exam_question_bodies_published":0,
            "independently_admitted_original_exam_questions":0,
            "source_custody_records_imported":0,
            "public_student_modules_from_uploaded_zip":0,
            "items":rows}


def validate(data: dict)->None:
    actual=registry()
    if data != actual:
        raise ValueError("UNAPPROVED_CORE2_METADATA_OR_PUBLICATION_PROMOTION")
    if (data["academic_admission"]!="HOLD" or
        data["redistribution_rights"]!="HOLD" or
        any(row["student_question_route"] is not None or
            row["public_question_text"] is not False for row in data["items"])):
        raise ValueError("CORE2_CUSTODY_PUBLICATION_BLOCKED")


def render(data: dict) -> str:
    validate(data)
    sections=[]
    for sub in ("PHYSICS","CHEMISTRY","BIOLOGY"):
        items=[r for r in data["items"] if r["subject"]==sub]
        rows="".join(
           '<tr><th scope="row">'+html.escape(x["slug"].replace("-"," "))+'</th>'
           '<td>'+str(x["unverified_candidate_question_count"])+'</td>'
           '<td><strong>Source and academic HOLD</strong><span class="small">'
           ' · No question text or approved learner route</span></td></tr>'
           for x in items)
        link=('<a href="../physics/question-bank.html">Physics authored question practice</a>'
              if sub=="PHYSICS" else
              f'<a href="../{sub.lower()}/question-bank.html">'
              'IAPT official-paper-linked practice notebook (original paper external)</a>')
        sections.append(
            '<section class="card" id="'+sub.lower()+'"><h2>'+sub.title()+'</h2>'
            '<p>'+str(len(items))+' uploaded module records · '
            +str(sum(r["unverified_candidate_question_count"] for r in items))+
            ' unreviewed candidate questions, <strong>none source-admitted from ZIP.</strong></p>'
            '<p>'+link+'</p>'
            '<div class="scroll"><table><thead><tr><th scope="col">Module</th>'
            '<th scope="col">Candidates</th><th scope="col">Public status</th></tr>'
            '</thead><tbody>'+rows+'</tbody></table></div></section>')
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Core2 — Physics, Chemistry, Biology · Grade9 v4.0</title>'
        '<style>body{font:17px/1.6 system-ui,sans-serif;margin:0;background:#eef5f8;'
        'color:#143449}main{max-width:1240px;margin:auto;padding:26px}'
        'a{color:#075878;text-underline-offset:3px}'
        'a:focus-visible{outline:3px solid #b97920;outline-offset:3px}'
        '.card{background:white;border:1px solid #c1d0d9;'
        'border-radius:15px;padding:20px;margin:20px 0}'
        '.hold{border-left:6px solid #b17a24;background:#fff5d9;padding:18px}'
        'nav{display:flex;gap:16px;flex-wrap:wrap}'
        'nav a{display:inline-flex;min-height:56px;align-items:center}'
        'h1{font-size:clamp(1.6rem,3vw,2.4rem)}'
        '.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%}'
        'th,td{padding:10px;text-align:left;border-bottom:1px solid #d4e1e7}'
        'th{font-weight:700}.small{color:#455d69;font-size:.85rem}'
        '@media(max-width:700px){main{padding:14px}th,td{padding:8px}}'
        '</style></head><body><main>'
        '<nav aria-label="Subject navigation"><a href="../index.html">NSEJS hub</a>'
        '<a href="../physics/index.html">Physics</a>'
        '<a href="../chemistry/index.html">Chemistry</a>'
        '<a href="../biology/index.html">Biology</a></nav>'
        '<h1>Core2 · candidate coverage and source-safe practice</h1>'
        '<p class="hold"><strong>Technical inventory · UNVALIDATED · SOURCE/ACADEMIC HOLD.</strong> '
        'The Owner archive contains 45 Physics/Chemistry/Biology module records '
        'and 267 candidate questions. This page publishes only checked '
        'metadata, not their exam question stems, diagrams, keys or solutions. '
        'None of the 267 questions is source-qualified or academically admitted. '
        'Use the links below for independently identified <em>authored</em> '
        'practice or external original IAPT paper notebooks; no exam endorsement '
        'or completeness is claimed.</p>'
        '<p><a href="question-map.html">Browse all 267 question occurrence IDs, '
        'provisional reasoning operations and missing learning constructions</a></p>'
        +''.join(sections)+
        '<p>No Mathematics records included. No academic approval inferred from '
        'software validation.</p></main></body></html>')



# Topic grouping is by uploaded module filename, not by verified question content.
# The five 2020–2024 bank modules per subject remain in the unclassified
# historical-year group. Do not imply year-batch questions match topic cards.
TOPIC_FILE_GROUPS = {
    "physics": (
        ("optics", (
            "ioqjs-optics-conjugate-d3-r1", "nsejs-optics-displacement-d3-r1",
            "nsejs-optics-lens-mirror-d3-r1", "nsejs-optics-prism-d3-r1",
            "nsejs-optics-r1", "nsejs-optics-screw-lens-d3-r1")),
        ("mechanics", ("nsejs-mechanics-r1",)),
        ("circuits", (
            "nsejs-circuits-r1", "nsejs-circuits-cube-d3-r1",
            "nsejs-circuits-ladder-d3-r1")),
        ("electrostatics", (
            "nsejs-electrostatics-r1", "nsejs-electrostatics-deflection-d3-r1")),
        ("magnetism", (
            "nsejs-magnetism-r1", "nsejs-magnetism-terminal-d3-r1")),
        ("fluids", (
            "nsejs-fluids-sound-r1", "nsejs-fluids-surface-energy-d3-r1")),
    ),
    "chemistry": (
        ("matter", ("chem-matter-mole-r1",)),
        ("reactions", ("chem-chemical-substances-r1",)),
        ("atomic", (
            "chem-atomic-bonding-r1", "chem-atomic-structure-r1",
            "chem-electronic-structure-d3-r1")),
        ("acids", ("chem-phosphorus-oxyacids-d3-r1",)),
        ("redox", ("chem-redox-titration-d3-r1",)),
        ("eudiometry", ("chem-eudiometry-d3-r1",)),
    ),
    "biology": (
        ("cell", (
            "bio-organisation-living-world-r1", "bio-viral-genetics-d3-r1")),
        ("life", (
            "bio-life-processes-r1", "bio-immunology-defense-d3-r1")),
        ("coordination", ("bio-genetics-coordination-r1",)),
        ("heredity", ()),
        ("ecology", ("bio-environment-resources-r1",)),
    ),
}


def expose_zip_coverage_in_subject_cards(page: str, subject: str, catalog: dict) -> str:
    """Expose the newly published 267-ID map *inside* existing topic tiles.

    Does not alter the older 50+1 Physics reader, Chemistry/Biology paper
    notebooks, core1 statuses, or original source admission.
    """
    import re
    sb = subject.upper()
    module_by_slug = {r["slug"]: r for r in catalog["items"]}
    scoped = {slug for slug, row in module_by_slug.items() if row["subject"] == sb}
    grouped = TOPIC_FILE_GROUPS[subject]
    topic_slugs = [slug for _, slugs in grouped for slug in slugs]
    year_slugs = {slug for slug in scoped
                  if re.fullmatch(r"nsejs-202[0-4]-" + subject + r"-r1", slug)}
    if (len(topic_slugs) != len(set(topic_slugs)) or
            set(topic_slugs) & year_slugs or
            set(topic_slugs) | year_slugs != scoped or len(year_slugs) != 5 or
            sum(module_by_slug[x]["unverified_candidate_question_count"]
                for x in year_slugs) != 79):
        raise ValueError("CORE2_TOPIC_BANK_FILENAME_CENSUS_MISMATCH")

    # The synthetic unit-test subject fixture has no topic cards.
    if 'class="topics-grid-12-7"' not in page:
        return page
    cards = list(re.finditer(
        r'<article class="topic-card-tab">[\s\S]*?</article>', page))
    if len(cards) != len(grouped):
        raise ValueError("CORE2_TOPIC_CARD_STRUCTURE_CHANGED")

    replacements = []
    for index, match in enumerate(cards):
        card = match.group(0)
        topic, slugs = grouped[index]
        if (card.count('<span class="core-name">Question Bank</span>') != 1
                or card.count('class="topic-desc"') != 1
                or 'data-core2-zip-topic=' in card):
            raise ValueError("CORE2_TOPIC_CARD_ANCHOR_CHANGED")
        count = sum(module_by_slug[x]["unverified_candidate_question_count"]
                    for x in slugs)
        if count != len(slugs):
            raise ValueError("CORE2_TOPICAL_MODULE_EXPECTED_ONE_CANDIDATE_EACH")
        module_links = "".join(
            '<li><a href="../core2/question-map.html#module-' +
            html.escape(slug, quote=True) + '">' +
            html.escape(slug.replace("-", " ")) + '</a></li>'
            for slug in slugs)
        if slugs:
            detail = (
                '<details style="margin-top:7px"><summary style="cursor:pointer;'
                'min-height:56px;display:flex;align-items:center;color:#075c83;'
                'font-weight:750">Show ' + str(len(slugs)) +
                ' ZIP module ID(s)</summary><ul style="margin:6px 0 0 17px;'
                'padding:0;line-height:1.7">' + module_links + '</ul></details>'
            )
        else:
            detail = (
                '<p style="margin:7px 0 0">No standalone topic bank in ZIP. '
                '<a href="../core2/question-map.html#' + subject +
                '">Browse historical-year subject records</a>.</p>'
            )
        callout = (
            '<section class="core2-zip-topic-preview" data-core2-zip-topic="' +
            topic + '" aria-label="New source-held Core2 ZIP module inventory" '
            'style="margin:12px 0;padding:12px 14px;border:1px solid #a0c3d4;'
            'border-left:5px solid #12698d;border-radius:10px;'
            'background:#edf7fb;color:#123a52">'
            '<strong>NEW · Uploaded ZIP Core2: ' + str(len(slugs)) +
            ' topic module(s), ' + str(count) +
            ' unvalidated question ID(s)</strong>'
            '<p style="font-size:.9rem;margin:5px 0">Source-held ID inventory '
            'only; the full exam questions and answer keys are not published. '
            'This is separate from the existing candidate-bank button.</p>' +
            detail + '</section>'
        )
        card2 = card.replace(
            '<div class="cores-sub-deck">',
            callout + '\n        <div class="cores-sub-deck">', 1)
        if card2 == card:
            raise ValueError("CORE2_SUBDECK_ANCHOR_NOT_FOUND")
        replacements.append((match.start(), match.end(), card2))

    for start, end, val in reversed(replacements):
        page = page[:start] + val + page[end:]

    totals = catalog["subjects"][sb]
    topical = len(topic_slugs)
    year_rows = sum(module_by_slug[x]["unverified_candidate_question_count"]
                    for x in year_slugs)
    if totals["modules"] != topical + 5 or totals["candidates"] != topical + year_rows:
        raise ValueError("CORE2_SUBJECT_SUMMARY_INCONSISTENT")
    overview = (
        '<section id="pcb-core2-zip-now-visible" '
        'aria-label="New uploaded ZIP Core2 question identity coverage" '
        'style="margin:20px 0;padding:23px;border:2px solid #087198;'
        'border-radius:15px;background:#e7f5fb;color:#14384a">'
        '<h2 style="margin:0 0 7px">NEW · Uploaded Core2 ZIP coverage</h2>'
        '<p><strong>' + str(totals["modules"]) + ' ' + subject.title() +
        ' modules · ' + str(totals["candidates"]) +
        ' question IDs indexed</strong> (' + str(topical) +
        ' standalone topic modules + 5 historical-year banks containing ' +
        str(year_rows) + ' candidate IDs).</p>'
        '<p><strong>Metadata only · Source/rights/academic HOLD.</strong> '
        'These are <em>not</em> the existing topic-button question records. '
        'No full ZIP stems, figures, keys or solutions are published.</p>'
        '<a href="../core2/question-map.html#' + subject +
        '" style="min-height:56px;display:inline-flex;align-items:center;'
        'font-weight:800;background:#115a79;color:white;border-radius:9px;'
        'padding:12px 20px;text-decoration:none">'
        'Browse all ' + str(totals["candidates"]) +
        ' source-held question IDs</a></section>'
    )
    opening = '<div class="topics-grid-12-7">'
    if page.count(opening) != 1:
        raise ValueError("CORE2_TOPIC_GRID_AMBIGUOUS")
    return page.replace(opening, overview + '\n    ' + opening, 1)


def publish(stage: Path) -> dict:
    data=registry()
    validate(data)
    root=stage/"nsejs"
    dest=root/"core2"
    dest.mkdir(parents=True,exist_ok=True)
    (dest/"index.html").write_text(render(data),encoding="utf-8")
    (dest/"inventory.v1.json").write_text(
        json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    # Source-neutral question-level identities, not original exams or native Core2.
    from nsejs_pcb_identity_map import stage as stage_pcb_question_map
    stage_pcb_question_map(stage)
    for subject in ("physics","chemistry","biology"):
        path=root/subject/"index.html"
        page=path.read_text("utf-8")
        if ("core2-archive-register" in page or
            page.count('<main class="tablet-container">') != 1):
            raise ValueError("CORE2_REGISTER_DUPLICATE_OR_SUBJECT_HTML_INVALID")
        link=(
            '<section id="core2-archive-register" '
            'style="position:relative;isolation:isolate;z-index:1;max-width:1050px;'
            'margin:22px auto;padding:22px;border:2px solid #93aebc;'
            'border-radius:13px;background:#f3fafc;color:#15384b">'
            '<h2>Core2 question coverage · source-safe register</h2>'
            '<p><strong>UNVALIDATED · Source and academic HOLD.</strong> '
            'The recovered Owner archive supplies a metadata inventory only; '
            'unapproved original exam question bodies are not published.</p>'
            '<a href="../core2/index.html#'+subject+'" '
            'style="position:relative;z-index:3;display:inline-flex;'
            'min-height:56px;align-items:center;pointer-events:auto;'
            'padding:10px 20px;border-radius:9px;background:#135c79;'
            'color:#fff;text-decoration:none;font-weight:700">'
            'Browse '+subject.title()+' Core2 candidate coverage</a></section>'
        )
        # Put the link at the *start* of the subject's main content, not at
        # the bottom after a very tall topic grid. This prevents off-screen
        # touch hit-testing/scroll restoration from obscuring the link.
        path.write_text(
            expose_zip_coverage_in_subject_cards(
                page.replace('<main class="tablet-container">',
                             '<main class="tablet-container">\n'+link,1),
                subject, data),
            encoding="utf-8")
    return {"status":data["status"],"module_count":data["module_count"],
            "candidate_question_count":data["candidate_question_count"],
            "original_exam_question_bodies_published":0,
            "academic_admission":"HOLD","redistribution_rights":"HOLD"}
