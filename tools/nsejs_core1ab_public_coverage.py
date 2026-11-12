"""Build a SOURCE-NEUTRAL NSEJS Core1A/Core1B coverage index for public Pages.

The authoritative input is the checked-in test-backed construction census,
NOT a guessed count, copied private workspace, or a claimed authentic exam.
Eight authored HTML journeys are published; other constructions are visibly
NOT_READY rather than represented by broken links. All academic gates HOLD.
"""
from __future__ import annotations

from collections import Counter
import html
import json
from pathlib import Path
from urllib.parse import urlparse

from agent_b_core1ab_reconcile import census, ROOT

EXPECTED_REVIEWED = 26
OWNER_REPORTED = 27
PUBLIC_SUBJECTS = ("physics", "chemistry", "biology")


def public_coverage(public_lessons: dict[str, tuple[str, ...]], root: Path = ROOT,
                    generated_output: Path | None = None) -> dict:
    """Reconcile real test-backed IDs and public authored page production."""
    if set(public_lessons) != set(PUBLIC_SUBJECTS):
        raise ValueError("All three subjects required")
    published_slugs = [s for slugs in public_lessons.values() for s in slugs]
    if len(published_slugs) != len(set(published_slugs)):
        raise ValueError("Duplicate lesson route")
    # Census uses ONLY question IDs, candidate UID metadata and test paths.
    # Source materials are intentionally not needed or exported here.
    report = census(repo_root=root, generated_root=Path("/__no_private_sources__"))
    rows = report["constructions"]
    if len(rows) != EXPECTED_REVIEWED or len(published_slugs) != 8:
        raise ValueError("PUBLIC_COVERAGE_COUNT_CHANGED_REVIEW_REQUIRED")
    status = []
    published = set()
    for item in rows:
        subject = item["subject"].lower()
        slug = item["expected_module"]
        is_published = bool(slug and slug in public_lessons[subject])
        if is_published:
            if slug in published:
                raise ValueError("Same generated lesson assigned twice")
            published.add(slug)
            if generated_output is not None:
                page = generated_output / slug / "learning_journey.html"
                if not page.is_file() or 'data-role="save-firstAttempt"' not in page.read_text("utf-8"):
                    raise ValueError("MISSING_PROTECTED_LEARNING_JOURNEY:"+slug)
        identity = item["match"]
        source_hold = "KNOWN_SOURCE_SUBSTITUTION" if item["target_question_id"] == "BIO-NSEJS-2024-B-Q52" else identity
        status.append({
            "construction_id": item["construction_id"],
            "subject": subject.upper(),
            "historical_target": item["target_question_id"],
            "source_matching": source_hold,
            "canonical_source_uid_admitted": None,
            "academic_admission": "HOLD",
            "original_exam_claim": False,
            "learner_status": "AUTHORED_PREVIEW_UNVALIDATED" if is_published else "NOT_PUBLISHED",
            "route": f"nsejs/{subject}/core1/{slug}/index.html" if is_published else None,
            "engineering_note": "Browser-protected authored practice; not original-source approval" if is_published
                                else "Original private workspace authoring/build inputs unavailable; not a verified learner page",
        })
    if published != set(published_slugs):
        raise ValueError("Public lesson missing from tracked test construction IDs: "+repr(
            sorted(set(published_slugs)-published)
        ))
    breakdown = {subject: {
        "tracked": sum(x["subject"] == subject.upper() for x in status),
        "published": sum(x["subject"] == subject.upper() and x["route"] is not None for x in status)
    } for subject in PUBLIC_SUBJECTS}
    if sum(x["tracked"] for x in breakdown.values()) != EXPECTED_REVIEWED:
        raise ValueError("Inconsistent tracked census")
    if sum(x["published"] for x in breakdown.values()) != 8:
        raise ValueError("Inconsistent published count")
    return {
        "schema": "grade9-nsejs-public-core1ab-coverage/v1",
        "scope": "TEST_BACKED_CONSTRUCTIONS_NOT_FULL_SYLLABUS",
        "tracked_constructions": EXPECTED_REVIEWED,
        "owner_historical_reported_constructions": OWNER_REPORTED,
        "unidentified_historical_count": OWNER_REPORTED-EXPECTED_REVIEWED,
        "published_authored_preview_journeys": 8,
        "not_published_constructions": EXPECTED_REVIEWED-8,
        "academic_admission": "HOLD",
        "source_authenticity": "NOT_INDEPENDENTLY_VERIFIED",
        "subject_breakdown": breakdown,
        "rows": sorted(status, key=lambda x: (x["subject"], x["construction_id"])),
    }


def _safe(s: object) -> str:
    return html.escape(str(s), quote=True)


def render_subject_index(subject: str, coverage: dict) -> str:
    if subject not in PUBLIC_SUBJECTS:
        raise ValueError("Unsupported subject")
    rows = [r for r in coverage["rows"] if r["subject"] == subject.upper()]
    if not rows:
        raise ValueError("Missing subject census")
    sections = []
    for row in rows:
        name = _safe(row["construction_id"].replace("-", " ").title())
        is_ready = row["route"] is not None
        if is_ready:
            slug = row["route"].split("/")[-2]
            action = f'<a class="lesson-link" href="{_safe(slug)}/index.html">Open authored lesson</a>'
            state = "Authored preview available · Unvalidated"
        else:
            action = '<span class="not-ready">Not published · no learner link</span>'
            state = "Not yet reproducibly generated"
        flag = (" · Source contradiction HOLD" if row["source_matching"] == "KNOWN_SOURCE_SUBSTITUTION"
                else " · Source / QRT HOLD")
        sections.append(
            '<li class="lesson-card">'
            f'<h2>{name}</h2><p>{_safe(state+flag)}</p>'
            f'<p class="minor">Construction: <code>{_safe(row["construction_id"])}</code>'
            f' · Historical target: <code>{_safe(row["historical_target"])}</code></p>'
            f'{action}</li>'
        )
    total = len(rows)
    available = sum(x["route"] is not None for x in rows)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>NSEJS {_safe(subject.title())} · Core1A/Core1B coverage</title>'
            '<style>'
            '*{box-sizing:border-box}body{font:18px/1.65 system-ui,sans-serif;background:#f4f8fb;'
            'color:#142c40;margin:0}main{max-width:1060px;margin:auto;padding:clamp(18px,3vw,36px)}'
            'h1{font-size:2rem;line-height:1.25}h2{font-size:1.18rem;margin:.2rem 0}'
            '.hold{padding:18px;border-left:5px solid #ab780d;background:#fff5d5}'
            'ul{list-style:none;margin:22px 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}'
            '.lesson-card{border:1px solid #b5c5d3;background:white;border-radius:12px;padding:22px}'
            '.lesson-link{display:inline-flex;align-items:center;min-height:56px;padding:12px 20px;border-radius:10px;'
            'background:#145877;color:white;font-weight:650;text-decoration:none;touch-action:manipulation}'
            'a:focus-visible{outline:3px solid #1971c2;outline-offset:3px}'
            '.not-ready{display:inline-block;color:#5d4a30;background:#f1e9dc;padding:10px;border-radius:9px}'
            '.minor{font-size:.88rem;overflow-wrap:anywhere;color:#364b5e}'
            '@media (orientation:portrait) and (min-width:800px){ul{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '</style></head><body><main>'
            f'<a href="../index.html">Back to {_safe(subject.title())} subjects</a>'
            f'<h1>Core1A + Core1B learning coverage · {_safe(subject.title())}</h1>'
            f'<p class="hold"><strong>Technical preview · UNVALIDATED · Academic HOLD.</strong> '
            f'{available} of {total} test-backed constructions have executable authored journeys. '
            'Others are listed as NOT PUBLISHED, not fake lessons. These are not authenticated original examination questions.'
            '</p><ul>'+"".join(sections)+
            '</ul><p>Source UIDs, figures, QRT and B1–B7 academic acceptance remain independent gates. '
            'No academic approval inferred from software validation.</p></main></body></html>')


def render_official_sources(locator_path: Path) -> str:
    """Link to IAPT's own files without mirroring the original question paper."""
    manifest = json.loads(locator_path.read_text(encoding="utf-8"))
    years = manifest.get("years", [])
    if len(years) != 5:
        raise ValueError("IAPT source locator list incomplete")
    cards = []
    for row in sorted(years, key=lambda r: r["year"], reverse=True):
        urls = []
        for label, field in (("IAPT official archive", "official_archive_url"),
                             ("Official paper (IAPT)", "official_paper_url"),
                             ("Official key (IAPT)", "official_final_key_url")):
            url = row.get(field)
            if not url:
                continue
            p = urlparse(url)
            if p.scheme != "https" or p.hostname not in ("iapt.org.in", "www.iapt.org.in", "mail.iapt.org.in"):
                raise ValueError("UNVERIFIED_OFFICIAL_SOURCE_HOST")
            urls.append(f'<a href="{_safe(url)}" rel="noopener noreferrer" target="_blank">{_safe(label)}</a>')
        cards.append(f'<li><h2>{_safe(row["year"])} · {_safe(row["exam_series"])}</h2>'
                     '<p>Official locator only; source-fidelity and reproduction rights not approved.</p>'
                     '<div class="links">'+"".join(urls)+'</div></li>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>NSEJS · Official IAPT source links</title><style>'
            '*{box-sizing:border-box}body{margin:0;background:#f4f8fb;color:#133047;font:18px/1.6 system-ui,sans-serif}'
            'main{max-width:1060px;margin:auto;padding:28px}li{list-style:none;background:white;border:1px solid #c0d0dc;'
            'border-radius:12px;padding:22px;margin:14px 0}.links{display:flex;flex-wrap:wrap;gap:12px}'
            '.links a{display:inline-flex;align-items:center;min-height:56px;padding:12px 18px;background:#155c79;'
            'color:white;text-decoration:none;border-radius:10px;touch-action:manipulation}'
            'a:focus-visible{outline:3px solid #1971c2;outline-offset:3px}'
            '.hold{background:#fff5d5;border-left:5px solid #ac7517;padding:16px}'
            '</style></head><body><main><a href="index.html">Back to NSEJS</a>'
            '<h1>Official IAPT source links (external)</h1><p class="hold"><strong>Link only.</strong> '
            'These files remain on the official publisher website; no original paper, key or figure is mirrored here. '
            'Source authentication, rights to reproduce, full question fidelity, and academic admission remain on HOLD.</p>'
            '<ul>'+"".join(cards)+'</ul><p>2020–21 and 2021–22 use IOQJS Part I nomenclature. '
            'The original 2024 Code 51 key drops Q20 and treats Q49–60 as multiple-answer questions.</p>'
            '</main></body></html>')
