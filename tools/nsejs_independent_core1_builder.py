"""Build 18 distinct source-neutral Core1A/B repair journeys from checked-in text.

Never reconstruct missing private originals by guessing. Do not call these
historical B1–B7-audited modules, authenticated NSEJS questions or exam coverage.
The original 18 construction rows retain source/academic/publication HOLD.
"""
from __future__ import annotations
import hashlib
import html
import json
from pathlib import Path
import re

SOURCE_NAMES=("independent-core1-recovery-chem.v1.json",
              "independent-core1-recovery-physics.v1.json")
INPUT_ROOT=Path("nsejs/content")
SCHEMA="grade9-independent-core1-recovery-journeys/v1"
AUTHOR="ORIGINAL_AUTHORED_TRANSFER_NOT_SOURCE_EXAM"
STAGES=("predict","attempt","reconstruct","diagnose","repair","boundary")


def canonical(value: object)->str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,
                      separators=(",",":"),allow_nan=False)


def digest(value: object)->str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def validate_catalog(repository: Path,recovery: dict)->dict:
    if (recovery.get("missing_reproducible_previews")!=18 or
        recovery.get("academic_admission")!="HOLD" or
        len(recovery.get("items",[]))!=26):
        raise ValueError("CORE1_ORIGINAL_CENSUS_NOT_HELD")
    withheld={
        x["construction_id"]:x
        for x in recovery["items"] if x["public_route"] is None
    }
    if len(withheld)!=18:raise ValueError("MISSING_CONSTRUCTION_IDS_NOT_UNIQUE")
    items=[]
    for source in SOURCE_NAMES:
        p=repository/INPUT_ROOT/source
        raw=json.loads(p.read_text("utf-8"))
        if(raw.get("schema")!="grade9-independent-core1-remediation-source/v1"
           or raw.get("authority")!=AUTHOR
           or raw.get("academic_admission")!="HOLD"
           or raw.get("original_18_audit_equivalence") is not False):
            raise ValueError("RECOVERY_AUTHOR_CUSTODY_OR_SOURCE_INVALID:"+source)
        for row in raw["items"]:
            required=("slug","construction","subject","title","concept",
                      "predict","worked","challenge","steps","trap",
                      "repair","boundary","boundaryAnswer")
            if any(not row.get(k) for k in required):
                raise ValueError("AUTHORED_RECOVERY_FIELDS_MISSING")
            if not re.fullmatch(r"[a-z0-9-]+",row["slug"]):
                raise ValueError("INVALID_AUTHOR_RECOVERY_SLUG")
            if row["construction"] not in withheld:
                raise ValueError("NOT_ONE_OF_THE_18_ORIGINAL_HOLD_IDS")
            if row["subject"]!=withheld[row["construction"]]["subject"]:
                raise ValueError("ORIGINAL_SUBJECT_MISMATCH")
            if raw["subject"]!=row["subject"]:
                raise ValueError("AUTHOR_SUBJECT_FILE_MISMATCH")
            for field in ("concept","predict","worked","challenge","trap",
                          "repair","boundary","boundaryAnswer"):
                if not isinstance(row[field],str) or len(row[field].strip())<55:
                    raise ValueError("AUTHOR_REPAIR_CONTENT_UNDERDEVELOPED:"+row["slug"]+":"+field)
            if (not isinstance(row["steps"],list) or len(row["steps"])!=3
                or any(not isinstance(x,str) or len(x.strip())<40 for x in row["steps"])):
                raise ValueError("INDEPENDENT_REASONING_NOT_THREE_STEPS")
            if (row["challenge"].strip()==row["worked"].strip()
                or row["challenge"].strip()==row["boundary"].strip()):
                raise ValueError("TRANSFER_NOT_INDEPENDENT")
            record={
                **row,
                "uid":"g9:AUTHOR-RECOVERY:"+row["subject"]+":"+row["construction"],
                "source_origin":AUTHOR,
                "source_question_claim":False,
                "original_b1b7_audit_equivalence":False,
                "academic_admission":"HOLD",
                "public_mode":"SUPPLEMENTAL_TECHNICAL_ONLY",
                "stages":list(STAGES),
                "publication_route":f'nsejs/{row["subject"].lower()}/core1/recovery/{row["slug"]}/index.html',
            }
            record["revision_sha256"]=digest(record)
            items.append(record)
    if(len(items)!=18 or
       len({x["construction"] for x in items})!=18 or
       len({x["slug"] for x in items})!=18 or
       {x["construction"] for x in items}!=set(withheld)):
        raise ValueError("INDEPENDENT_AUTHORED_18_MISMATCH")
    return {
        "schema":SCHEMA,
        "author_authority":AUTHOR,
        "source_exam_admission":"HOLD",
        "academic_admission":"HOLD",
        "original_audited_module_count_recovered":0,
        "original_18_modules_still_on_hold":18,
        "supplemental_authored_skill_journeys":18,
        "historical_27th_unidentified":1,
        "status":"SOURCE_NEUTRAL_SUPPLEMENTAL_TECHNICAL_ONLY",
        "items":sorted(items,key=lambda x:x["construction"]),
    }


def lesson_html(row: dict)->str:
    sub=html.escape(row["subject"].title())
    title=html.escape(row["title"])
    slug=html.escape(row["slug"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{sub} · {title} · Independent Core1 repair · Grade9</title>
<style>
[hidden]{{display:none!important}}
body{{background:#f3f8fa;color:#19394e;margin:0;font:18px/1.6 system-ui,sans-serif}}
header,main,footer{{max-width:1060px;margin:auto;padding:19px 24px}}
header{{display:flex;gap:15px;flex-wrap:wrap}}
h1{{font-size:clamp(1.6rem,3vw,2.3rem);line-height:1.3}}
h2{{font-size:1.2rem}}
a{{color:#135b80}}
a:focus-visible,button:focus-visible,textarea:focus-visible{{outline:4px solid #b57b1f;outline-offset:3px}}
.hold{{background:#fff3db;border:2px solid #c9aa6e;border-radius:12px;padding:15px}}
.stage{{border:2px solid #adc5d0;background:white;border-radius:12px;margin:18px 0;padding:18px 22px}}
button{{font:inherit;background:#165b7b;color:white;border:0;border-radius:10px;min-height:56px;padding:13px 21px;font-weight:740;margin:8px 10px 8px 0}}
button:disabled{{background:#7e919c;cursor:not-allowed}}
textarea{{width:100%;min-height:140px;padding:13px;border:2px solid #90acb8;border-radius:10px;font:inherit}}
#recovery-status{{border-left:4px solid #ad813b;background:#fff7e5;padding:13px 17px}}
ol{{padding-left:25px}}
#solution-body{{background:#e9f7f1;border:1px solid #96beb1;border-radius:10px;padding:18px;margin:12px 0}}
@media(max-width:650px){{header,main,footer{{padding:12px}}.stage{{padding:14px}}}}
</style><script defer src="../../../../js/core1-independent-recovery.js"></script>
</head><body data-recovery-slug="{slug}">
<header><a href="../../index.html">Core1 lessons</a>
<a href="../../../../core1-recovery.html">18 original HOLD cases</a>
<a href="../../../../index.html">NSEJS hub</a></header>
<main><h1>{title}</h1>
<p class="hold"><strong>Independent Grade9-authored supplementary teaching · NOT a recovered original examination module.</strong>
The corresponding historical Core1 construction is still withheld. No original paper stem, figure or
private authored output is copied. Source custody, B1–B7, science and academic admission remain HOLD.</p>
<section id="recovery-lesson" aria-label="Six-stage independent Core1A/Core1B skill journey">
<p id="recovery-status" role="status">Verifying the authored lesson revision…</p></section>
</main><footer>No academic approval inferred from software validation.</footer></body></html>'''
