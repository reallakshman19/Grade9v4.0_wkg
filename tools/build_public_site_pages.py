"""Public-safe student homepage and NSEJS navigation for GitHub Pages.

This is a display-only, curated site shell; no private source questions, real
exam images, bank content, student data, or approved NSEJS curriculum is copied.
The existing synthetic 4-question reader is staged separately by its builder.
The repo's historical engineering/reader workspaces stay untouched.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
PUBLISHED_PREVIEW_PAGES=(
 "preview/index.html",
 "preview/physics-wpe.html",
 "preview/practice.html",
 "preview/progress.html",
 "preview/alpha-board.html",
)
PUBLISHED_PREVIEW_ASSETS=("preview/assets/app.css","preview/assets/app.js")
HUB_PAGES=(
 "index.html",
 "physics/index.html",
 "mathematics/index.html",
 "chemistry/index.html",
 "architecture/index.html",
 "physics/wpe/index.html",
 "nsejs/index.html",
 "nsejs/physics/index.html",
 "nsejs/chemistry/index.html",
 "nsejs/biology/index.html",
)
HUB_ASSETS=("site.css",)
PUBLIC_SHELL_FILES=tuple(sorted((*HUB_PAGES,*HUB_ASSETS,*PUBLISHED_PREVIEW_PAGES,*PUBLISHED_PREVIEW_ASSETS)))
# Strictly no /workspace, /reference, /tests, /tools or exam-original bank.
assert len(PUBLIC_SHELL_FILES)==len(set(PUBLIC_SHELL_FILES)) and all(
 not path.startswith(("workspace/","reference/","tests/","tools/")) for path in PUBLIC_SHELL_FILES
)

NAV=(
 ("Physics","physics/index.html"),
 ("Mathematics","mathematics/index.html"),
 ("Chemistry","chemistry/index.html"),
 ("NSEJS","nsejs/index.html"),
 ("Architecture","architecture/index.html"),
)
def prefix(path: str)->str:
 return "../"*(len(Path(path).parts)-1)

def link(path: str,target: str)->str:
 return prefix(path)+target

def a(path: str,destination: str,label: str)->str:
 return '<a href="'+escape(link(path,destination),quote=True)+'">'+escape(label)+'</a>'

def card(path: str,number: str,icon: str,title: str,description: str,destination: str,
         action: str,hold: bool=False)->str:
 return ('<article class="card'+(' hold' if hold else '')+'">'
         '<div class="tile-icon" aria-hidden="true">'+icon+'</div>'
         '<small>'+escape(number)+'</small><h2>'+escape(title)+'</h2><p>'+escape(description)+'</p>'
         +a(path,destination,action)+'</article>')

def layout(path: str,section: str,title: str,intro: str,body: str,active: str="")->str:
 tabs=''.join('<a href="'+escape(link(path,url),quote=True)+'"'
               +(' aria-current="page"' if active==url.split("/")[0] else '')+'>'+escape(label)+'</a>'
               for label,url in NAV)
 return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
  '<meta name="viewport" content="width=device-width,initial-scale=1">'
  '<meta name="theme-color" content="#102f43">'
  '<meta name="description" content="Grade9 subject learning and NSEJS Junior Science preparation status.">'
  f'<title>{escape(title)} · Grade9 v4.0</title>'
  f'<link rel="stylesheet" href="{escape(link(path,"site.css"),quote=True)}">'
  '</head><body><header class="mast"><div class="container top">'
  f'<a class="logo" href="{escape(link(path,"index.html"),quote=True)}"><i>G9</i>Grade9 v4.0</a>'
  '<nav class="tabs" aria-label="School subjects and NSEJS entrance preparation">'+tabs+'</nav>'
  '</div><div class="container hero"><div class="kicker">'+escape(section)+'</div>'
  f'<h1>{escape(title)}</h1><p>{escape(intro)}</p></div></header>'
  f'<main class="container main">{body}</main>'
  '<footer class="footer"><div class="container"><span>Grade9 v4.0 · Public learning preview'
  ' · Academic approval not inferred</span>'
  f'<a href="{escape(link(path,"index.html"),quote=True)}">Home</a></div></footer>'
  '</body></html>\n')

def status(head: str,note: str)->str:
 return '<div class="status warn"><strong>'+escape(head)+'</strong><p>'+escape(note)+'</p></div>'

def render(path: str)->str:
 if path=="index.html":
  body=(status("School learning and NSEJS are separate learning tracks",
    "Physics WPE is a learning preview; no independently admitted examination questions or complete NSEJS course are claimed.")
   +'<h2 class="section-title">Choose your learning track</h2>'
   +'<div class="cards two">'
   +card(path,"SCHOOL SUBJECTS","📚","Learn by subject",
         "Open Physics, Mathematics or Chemistry without being redirected into an exam-only technical reader.",
         "physics/index.html","Explore school Physics")
   +card(path,"JUNIOR SCIENCE · NSEJS","🎯","NSEJS subject-wise preparation",
         "A separate route for Physics, Chemistry and Biology. Physics Foundation is a candidate; the other sciences await reviewed content.",
         "nsejs/index.html","Open NSEJS subjects")+'</div>'
   +'<h2 class="section-title">School subject directories</h2><div class="cards">'
   +card(path,"PHYSICS · ACTIVE PILOT","⚛️","Physics","Work, Power & Energy has an independent public learning demonstration.", "physics/index.html","Open Physics")
   +card(path,"MATHEMATICS · PLANNED","📐","Mathematics","School mathematics subject directory; no qualified topic is claimed yet.", "mathematics/index.html","Open Mathematics",True)
   +card(path,"CHEMISTRY · PLANNED","🧪","Chemistry","School chemistry subject directory; content is under review.", "chemistry/index.html","Open Chemistry",True)
   +'</div><div class="panel"><h2>Where is the reader demo?</h2>'
   '<p>The four-question synthetic reader still exists as a technical example, but is no longer the entire website homepage.</p>'
   f'<div class="linklist">{a(path,"preview/physics-wpe.html","Public WPE foundation example")}'
   f'{a(path,"preview/practice.html","Try synthetic spring practice")}'
   f'{a(path,"preview/question-status.html","Four-question synthetic technical reader")}'
   f'{a(path,"architecture/index.html","How Grade9 verifies content")}</div></div>')
  return layout(path,"Grade9 · Learn · Practise · Explore","Choose your subject or NSEJS track",
   "School subjects and Junior Science preparation have their own clear routes. Start with a subject, not a technical reader.",
   body)
 if path=="physics/index.html":
  body=(status("Physics pilot · academic release on HOLD",
   "The WPE public example is a teaching demonstration, not a certified examination curriculum.")
   +'<div class="cards two">'
   +card(path,"SCHOOL PHYSICS","⚡","Work, Power & Energy",
    "Try a public, source-independent foundational example, or view the synthetic practice reader.",
    "physics/wpe/index.html","Open WPE foundation")
   +card(path,"JUNIOR SCIENCE","🎯","NSEJS Physics Foundation",
    "See the separate NSEJS Physics study route; do not treat WPE alone as full NSEJS Physics coverage.",
    "nsejs/physics/index.html","Open NSEJS Physics")+'</div>')
  return layout(path,"School / Physics","Physics chapters",
    "Learn forces, motion and energy in the school-subject track.",body,"physics")
 if path=="mathematics/index.html":
  body=(status("School Mathematics · content qualification pending",
   "No academically admitted Mathematics topic, Blueprint or lesson is claimed.")
   +'<div class="panel"><h2>Mathematics will stay a school subject</h2>'
   '<p>This does not become a fourth NSEJS examination science. Mathematics supports scientific problem solving but is not a separately named NSEJS subject in the 2026 IAPT syllabus.</p>'
   f'<div class="linklist">{a(path,"index.html","Back to subject selection")}</div></div>')
  return layout(path,"School / Mathematics","Mathematics",
   "Mathematics learning remains in its own school-subject directory.",body,"mathematics")
 if path=="chemistry/index.html":
  body=(status("School Chemistry · content qualification pending",
   "Chemistry Blueprints and lessons are not yet independently admitted.")
   +'<div class="cards two">'
   +card(path,"SCHOOL CHEMISTRY","🧪","Chemistry topics",
    "This directory is reserved for reviewed school Chemistry topics; no exam content is invented here.",
    "index.html","Chemistry overview",True)
   +card(path,"NSEJS SCIENCE","🎯","NSEJS Chemistry",
    "A separate Junior Science preparation route with its own future admission decisions.",
    "nsejs/chemistry/index.html","Open NSEJS Chemistry",True)+'</div>')
  return layout(path,"School / Chemistry","Chemistry",
   "School Chemistry remains separate from exam preparation.",body,"chemistry")
 if path=="architecture/index.html":
  body=('<div class="panel"><h2>Content review is not the same as deployment</h2>'
   '<p>Source custody, model correctness, learning sufficiency, independent attempts, independent academic review and release authority are distinct checks. Passing UI tests does not certify an exam answer or a course.</p>'
   '<p>The full technical records and Architecture Guidebook remain in the public repository without being copied into this student-facing Pages package.</p>'
   '<div class="linklist"><a href="https://github.com/reallakshman19/Grade9v4.0/tree/main/architecture">Read the Architecture documents on GitHub</a>'
   f'{a(path,"index.html","Return to student homepage")}</div></div>')
  return layout(path,"About Grade9","Architecture and quality checks",
    "A short guide to what our technical and academic evidence actually means.",body,"architecture")
 if path=="physics/wpe/index.html":
  body=(status("WPE Foundation · synthetic public practice",
   "This page contains no authenticated examination bank, official figure or approved NSEJS Physics course.")
   +'<div class="cards two">'
   +card(path,"EXPLAIN · NEW EXAMPLE","💡","Understand energy",
    "An original spring-energy example with explicit assumptions and a separate worked check.",
    "preview/physics-wpe.html","Open the concept demonstration")
   +card(path,"PRACTISE · SYNTHETIC","✏️","Attempt a spring problem",
    "Try an original practice question; local attempts are not secure examination grading.",
    "preview/practice.html","Try the practice")+'</div>'
   +'<div class="panel"><h2>What about the original Question Bank?</h2>'
   '<p>The source-bound WPE Question Bank and reviewer-only readers are not included in this public-safe Pages package. A synthetic reader is provided for technical validation only.</p>'
   f'<div class="linklist">{a(path,"preview/question-status.html","Open synthetic technical reader")}'
   f'{a(path,"nsejs/physics/index.html","NSEJS Physics track")}</div></div>')
  return layout(path,"School Physics / WPE","Work, Power & Energy",
   "Explore the safe public example without confusing a technical reader with a complete course.",body,"physics")
 if path=="nsejs/index.html":
  body=(status("NSEJS is a preparation track — not an admitted course",
   "The official Junior Science examination covers Physics, Chemistry and Biology. Only a Physics WPE Foundation candidate is currently demonstrable here.")
   +'<h2 class="section-title">Choose a Junior Science subject</h2><div class="cards">'
   +card(path,"NSEJS · PHYSICS","⚛️","Physics Foundation",
    "Start with energy and work reasoning, then progress after independent source and curriculum review.",
    "nsejs/physics/index.html","Explore Physics Foundation")
   +card(path,"NSEJS · CHEMISTRY · HOLD","🧪","Chemistry",
    "Subject route prepared; no approved Chemistry lessons, test bank or coverage yet.",
    "nsejs/chemistry/index.html","View Chemistry status",True)
   +card(path,"NSEJS · BIOLOGY · HOLD","🌱","Biology",
    "A subject status page only; no Biology workspace, source corpus or lessons are invented.",
    "nsejs/biology/index.html","View Biology status",True)+'</div>'
   +'<div class="panel"><h2>Keep school classes separate</h2>'
   '<p>NSEJS is a science exam-preparation pathway; the existing Grade9 Physics, Mathematics and Chemistry school tabs remain independently accessible.</p>'
   f'<div class="linklist">{a(path,"index.html","School subject homepage")}'
   '<a href="https://iapt.org.in/">Official examination organizer (IAPT)</a></div></div>')
  return layout(path,"Exam preparation / NSEJS","NSEJS · Subject-wise Junior Science",
    "Physics · Chemistry · Biology. Learn the right model, justify it, and try unfamiliar questions only where teaching is qualified.",body,"nsejs")
 if path=="nsejs/physics/index.html":
  body=(status("NSEJS Physics Foundation · candidate only",
    "Physics WPE examples exist as public practice; syllabus-wide coverage, official question keys, independent academic review and exam admission are still on HOLD.")
    +'<div class="cards two">'
    +card(path,"PHYSICS · FOUNDATION","⚡","Work, Power & Energy",
      "Use a source-independent spring and conservation demonstration as one entry point; it is not a complete NSEJS lesson sequence.",
      "preview/physics-wpe.html","Open Physics Foundation example")
    +card(path,"PHYSICS · PRACTICE","✏️","Try a fresh practice",
      "A small public-safety demonstration, not the authentic exam question bank.",
      "preview/practice.html","Try the spring example")+'</div>'
    +'<div class="panel"><h2>Other NSEJS Physics topics</h2>'
    '<p>Motion, graphs, forces, fluids, sound, optics and electricity require their own source checks, teaching and fresh transfer tasks before being marked available. Do not infer their readiness from WPE.</p>'
    f'<div class="linklist">{a(path,"nsejs/index.html","All NSEJS subjects")}</div></div>')
  return layout(path,"NSEJS / Physics","Physics Foundation",
    "Learn the model before attempting a fresh application. Subject admission status is not implied.",body,"nsejs")
 if path in ("nsejs/chemistry/index.html","nsejs/biology/index.html"):
  chemistry=path.startswith("nsejs/chemistry/")
  subject="Chemistry" if chemistry else "Biology"
  body=(status(f"NSEJS {subject} · no admitted lessons",
    "Subject entry is a navigation placeholder only: no verified source bank, teaching construction or assessment is publicly available.")
    +'<div class="panel"><h2>What needs to happen first?</h2>'
    '<p>Source and figure custody, subject-specific Blueprint, physical/chemical/biological reasoning audit, guided construction, fresh transfer tasks, independent academic validation and an Owner release decision.</p>'
    f'<div class="linklist">{a(path,"nsejs/index.html","All NSEJS subjects")}'
    f'{a(path,"index.html","School subject homepage")}</div></div>')
  return layout(path,f"NSEJS / {subject}",f"NSEJS {subject} · Planned",
      "The subject exists in the exam outline but this app does not claim a completed workspace.",body,"nsejs")
 raise ValueError("UNAPPROVED_PUBLIC_PAGE:"+path)

# The legacy public lesson pages contain no original examination source payload.
# Replace only unsupported/unpublished LINKS in the rendered copies. The input
# source repository files remain byte-identical.
_LEGACY_LINK_TARGETS={
 '../physics/wpe/learn-challenge.html':'../physics/wpe/index.html',
 '../physics/wpe/question-bank.html':'question-status.html',
 'batches/reader.html':'question-status.html',
}
_PREVIEW_NAV_STYLE='''<style id="public-safe-nav-style">
.public-safe-nav{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;padding:12px max(20px,calc((100% - 1120px)/2));background:#10384f;color:#fff;font:700 14px system-ui,sans-serif}
.public-safe-nav a{color:#e0f7fb;padding:7px 10px;border-radius:7px;text-decoration:none}
.public-safe-nav a:hover,.public-safe-nav a:focus-visible{background:#26687b;outline-offset:2px}
</style>'''
_PREVIEW_NAV='''<nav class="public-safe-nav" aria-label="Grade9 subject and NSEJS navigation">
<a href="../index.html">Grade9 Home</a><a href="../physics/index.html">Physics</a>
<a href="../mathematics/index.html">Mathematics</a><a href="../chemistry/index.html">Chemistry</a>
<a href="../nsejs/index.html">NSEJS</a><a href="../architecture/index.html">Architecture</a>
</nav>'''

def preview_html(path: str)->str:
 if path not in PUBLISHED_PREVIEW_PAGES:
  raise ValueError("PREVIEW_PAGE_NOT_ALLOWED")
 txt=(ROOT/path).read_text(encoding="utf-8")
 txt=txt.replace('<script data-grade9-nav defer src="../site-nav.js"></script>','')
 for old,new in _LEGACY_LINK_TARGETS.items():
  txt=txt.replace('href="'+old+'"','href="'+new+'"')
 # Only display new content, never claim that the synthetic reader is a real QBank.
 txt=txt.replace('Question Bank · Review','Synthetic reader · review only')
 txt=txt.replace('Question Bank','Synthetic technical reader')
 txt=txt.replace('Cumulative WPE reader','Synthetic technical reader')
 txt=txt.replace('Technical examples','Synthetic technical examples')
 txt=txt.replace('Five-skill guided path','Public WPE overview')
 txt=txt.replace('Five guided skills','Public WPE overview')
 txt=txt.replace('Five-skill guided','Public WPE overview')
 txt=txt.replace('Original learning preview','Public learning preview')
 if "</head>" not in txt or "<body>" not in txt:
  raise ValueError("PUBLIC_LEGACY_PREVIEW_TEMPLATE_CHANGED:"+path)
 txt=txt.replace("</head>",_PREVIEW_NAV_STYLE+"</head>",1)
 txt=txt.replace("<body>","<body>"+_PREVIEW_NAV,1)
 return txt

def write_shell(stage: Path)->None:
 for path in HUB_PAGES:
  dst=stage/path;dst.parent.mkdir(parents=True,exist_ok=True)
  dst.write_text(render(path),encoding="utf-8")
 for path in PUBLISHED_PREVIEW_PAGES:
  dst=stage/path;dst.parent.mkdir(parents=True,exist_ok=True)
  dst.write_text(preview_html(path),encoding="utf-8")
 for path in (*PUBLISHED_PREVIEW_ASSETS,*HUB_ASSETS):
  dst=stage/path;dst.parent.mkdir(parents=True,exist_ok=True)
  dst.write_bytes((ROOT/path).read_bytes())
