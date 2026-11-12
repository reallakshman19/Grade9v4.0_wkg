"""Private Owner review entry, current concept addendum and exact integration map."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
e=html.escape
style='''body{font:17px/1.6 system-ui;color:#203344;background:#f4f6f9;margin:0}main{max-width:1120px;margin:auto;padding:24px}a{color:#075c9c}nav{display:flex;flex-wrap:wrap;gap:18px}.note,section{background:white;border:1px solid #cad5df;border-radius:12px;padding:20px;margin:20px 0}.hold{border-left:6px solid #af7900;background:#fff4d9}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px}.metric{font-size:30px;font-weight:700}table{border-collapse:collapse;width:100%}td,th{padding:10px;text-align:left;border-bottom:1px solid #ccd5dd;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f8;padding:14px}input,select{font:inherit;padding:8px;max-width:100%;box-sizing:border-box}summary{cursor:pointer}section[hidden]{display:none}.tablewrap{overflow:auto}code{overflow-wrap:anywhere}@media(max-width:600px){main{padding:12px}td,th{padding:6px;font-size:14px}}'''
def page(title,body,js=''):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><style>'+style+'</style><main><nav><a href="index.html">Overview</a><a href="rendered/core2.html">Native Core2 reader</a><a href="review.html">Source review</a><a href="concept.html">Concept and limits</a></nav><h1>'+e(title)+'</h1>'+body+'</main><script>'+js+'</script></html>'

r=read(ROOT/'review/EXAM_READINESS.json');pre=read(ROOT/'received-private-r1/outputs/REAL_R1_SELECTION_PREFLIGHT.json')
book=read(ROOT/'textbook-baseline/review/questions.json');ops=['RETRIEVE','EXPLAIN','APPLY','MODEL','REPRESENT','SYNTHESIZE','JUSTIFY']
matrix='<div class="tablewrap"><table id="matrix"><tr><th>Operation</th><th>D3 proposals / admitted</th><th>D4 proposals / admitted</th><th>Vacancies across D3/D4</th></tr>'
for op in ops:
    matrix+='<tr><th>'+op+'</th>'
    for band in ['D3','D4']:
        ids=[x['canonical_id'] for x in pre['records'] if x['assessment']['primary_operation']==op and x['assessment']['band']==band]
        matrix+='<td data-cell="'+op+'-'+band+'"><a href="review.html?category=examination&amp;operation='+op+'&amp;band='+band+'">'+str(len(ids))+' pending / 0 admitted</a>'+'<br>'+e(', '.join(ids))+'</td>'
    matrix+='<td>'+str(r['legacy_selection']['operation_coverage'][op]['vacant'])+'</td></tr>'
matrix+='</table></div>'
body='''<p class="note hold"><strong>Private engineering candidate — product acceptance pending.</strong> The learner reader contains eight textbook illustrations and one synthetic control. It contains zero admitted examination originals. No Core1A/Core1B lessons are delivered.</p>
<div class="cards"><section><div class="metric">8</div>Preserved textbook questions</section><section><div class="metric">1</div>Synthetic native control</section><section><div class="metric">14 / 7 / 0</div>Examination leads / gaps / admissions</section></div>
<section><h2>Review the integration</h2><ol><li><a href="rendered/core2.html">Open the combined nine-record native reader</a>: commit an answer, request support and reveal working.</li><li><a href="synthetic-rendered/core2.html">Open the strict native synthetic control</a>: zero reference-depth gaps; engineering evidence only.</li><li><a href="textbook-baseline/rendered/core2.html">Compare the original eight-question draft</a>: preserved unchanged, including its open findings.</li><li><a href="review.html">Inspect the examination holds and textbook source notes</a>.</li></ol><p>The native interface records commitment and supports self-check. It does not grade correctness or establish independent P1 evidence. Static HTML contains recoverable answer bytes.</p></section>
<section><h2>Examination QRT matrix: 14 cells, target 21 originals</h2><p>Three distinct originals per operation across both bands. Counts below are inherited proposals. Vacancies belong to an operation across D3/D4 and are shown once.</p>'''+matrix+'</section>'
body+='<section><h2>Validation and open work</h2><ul><li><a href="review/INTEGRATION_TESTS.json">26 current author integration tests</a>; the 33 received engineering unit tests were also rerun successfully.</li><li><a href="review/BROWSER_CHECKS.json">60 author browser checks</a>: 1280/390 widths, typed/MCQ/keyboard commitments, support, solution gating, state restoration and exact negative controls.</li><li><a href="review/BUILD_CONTROLS.json">Actual strict rejection, missing-identity rejection and relocated-input rebuild</a>.</li><li><a href="rendered/render-receipt.json">Combined native receipt</a>: ten inherited reference-depth findings remain; <a href="synthetic-rendered/render-receipt.json">synthetic strict receipt</a>: zero depth gaps.</li></ul><p>Incomplete subject portal routes, a historical NLM concept route and absent PDF outputs remain visible native-shell integration findings. Distinct academic and technical review are NOT_RUN. Source/answer/figure custody and exact operation/demand still block all fourteen examination leads.</p><p>Core2 → Owner approval → Core1A → Owner approval → Core1B. D3.1 remains paused.</p></section>'
(ROOT/'index.html').write_text(page('WPE Core2 · native integration review',body),encoding='utf-8')

cards=[]
gate={x['id']:x for x in r['engineering_metadata_gate']['items']}
native={x['id']:x for x in r['native_readiness']}
for x in pre['records']:
    q=x['question'];a=x['assessment'];ident=x['canonical_id'];op=a['primary_operation'];band=a['band']
    detail='<p><strong>HOLD · unadmitted examination lead.</strong> '+e(op+' / '+band+' author proposal')+'</p><p>'+e(q.get('stem') or '[Stem missing in received projection]')+'</p><ol type="A">'+''.join('<li>'+e(o['text'])+'</li>' for o in q.get('options',[]))+'</ol>'
    detail+='<p>Upstream paper claim: '+e(str(x.get('source',{}).get('original_r1_custody',{}).get('paper') or 'UNKNOWN'))+' · unauthenticated here.</p>'
    detail+='<details><summary>Exact blockers, inherited cognitive proposal and dependency</summary><pre>'+e(json.dumps({'native':native[ident],'metadata_gate':gate[ident],'author_proposal':a},ensure_ascii=False,indent=2))+'</pre></details>'
    cards.append('<section class="record" id="'+e(ident)+'" data-category="examination" data-operation="'+op+'" data-band="'+band+'"><h2>'+e(ident)+'</h2>'+detail+'</section>')
for x in book:
    cards.append('<section class="record" id="'+x['id']+'" data-category="textbook" data-operation="'+x['sl2']['operation_proposal']+'" data-band="'+x['sl2']['difficulty_proposal']['band']+'"><h2>'+e(x['id']+' · '+x['title'])+'</h2><p>Preserved textbook question; independently unreviewed. Separate from the examination denominator.</p><a href="rendered/core2.html#'+x['id']+'">Native question</a> · <a href="textbook-baseline/review.html#'+x['id']+'">Retained source/solution review</a><ul>'+''.join('<li>'+e(t)+'</li>' for t in x['issues'])+'</ul></section>')
cards.append('<section class="record" id="SYN-WPE-DIRECTION-CONTROL-01" data-category="synthetic" data-operation="" data-band="D2"><h2>Synthetic native control</h2><p>Author engineering fixture only; no examination coverage.</p><a href="synthetic-rendered/core2.html">Open strict native control</a> · <a href="native/synthetic-binding.json">Exact authored binding</a></section>')
filters='<label>Source category <select id="category"><option value="">All categories</option><option value="examination">Examination leads</option><option value="textbook">Textbook questions</option><option value="synthetic">Synthetic control</option></select></label> <label>Operation <select id="operation"><option value="">All operations</option>'+''.join('<option>'+op+'</option>' for op in ops)+'</select></label> <label>Band <select id="band"><option value="">All bands</option>'+''.join('<option>'+b+'</option>' for b in ['D2','D3','D4'])+'</select></label> <label>Search <input id="search" type="search"></label><p id="count" aria-live="polite"></p>'
js="""const fields=['category','operation','band','search'];const rows=[...document.querySelectorAll('.record')];const params=new URLSearchParams(location.search);fields.forEach(k=>{document.getElementById(k).value=params.get(k)||'';document.getElementById(k).addEventListener('input',filter)});function filter(){const v=Object.fromEntries(fields.map(k=>[k,document.getElementById(k).value]));rows.forEach(r=>r.hidden=!!((v.category&&r.dataset.category!==v.category)||(v.operation&&r.dataset.operation!==v.operation)||(v.band&&r.dataset.band!==v.band)||(v.search&&!r.textContent.toLowerCase().includes(v.search.toLowerCase()))));document.getElementById('count').textContent=rows.filter(r=>!r.hidden).length+' of '+rows.length+' records shown. No academic admission is implied.'}filter();"""
(ROOT/'review.html').write_text(page('WPE · private source and hold catalogue','<p class="note hold">Owner/author view: source-bearing questions and exposed reasoning. This catalogue is not a learner examination or an admission decision.</p>'+filters+''.join(cards),js),encoding='utf-8')

mapping=[
 ['Custom origin AUTHORED_TECHNICAL_FIXTURE','Native origin AUTHORED; synthetic label and no-admission extension','Real EXAM_ORIGINAL remains held; no official-exam fields invented.'],
 ['Option objects with source IDs','Native option text strings; A… labels supplied by native renderer; reversible source ID/index map','Non-A… order/unknown labels are rejected rather than silently renamed.'],
 ['Answer kind SINGLE_CHOICE and grading policy','Native MODEL_RESPONSE, supplied prose and explicit typed route','No automatic grading code or academic verification claim is imported.'],
 ['Three supplied method scaffolds declared safe upstream','Retained unchanged in the mapping sidecar; two explicit authored orientation prompts project','Original prompts are not silently certified safe; independent semantic review remains open.'],
 ['Original textbook owner bank','Byte-identical bank and intake copied; all eight selected','Printed/extract correspondence and source assumptions remain open.'],
 ['Derived textbook package','Existing scientific fields preserved; title changed; asset paths relocated; one synthetic representation appended','Original canonical library and source package remain untouched.'],
 ['Handoff cloned manifest','New absolute candidate package/bank refs; only CORE2 outputs; exact nine IDs','Relocation verified with C: runtime; no standalone native toolchain claim.'],
 ['Fourteen examination projections','Rerun unchanged metadata gate + explicit native readiness report; searchable source catalogue','None selected, mapped into a fake complete bank, or counted as admitted.']]
save(ROOT/'review/NATIVE_MAPPING.json',{'mapping':mapping,'profile':'SYNTHETIC_NATIVE_INTEGRATION_ONLY; textbook reuse','academic_admissions':0})
concept='''# WPE Core2 native integration R1 — concept and acceptance addendum

This candidate continues the completed eight-question textbook draft and the received examination engineering proposal. It does not replace either original or introduce Core1A lessons. The native integration is locally demonstrated; the 21-original examination product remains PARTIAL.

## Two source routes, one native reader contract

Existing textbook questions may feed Core2. Explanatory book passages and syllabus feed Core1A preparation. An examination claim requires independently bound paper, question/figure and key evidence plus distinct academic adjudication; a printed examination label in a book is insufficient. Duplicate occurrences must eventually reconcile to one original counting identity.

The native reader implements commitment → requested support → protected answer/working → self-check. Its static source contains answer bytes; its local storage is a UI convenience, not an original independently saved P1 record. The standalone handoff grader was not grafted into this reader.

## Exact delivered scope

Eight textbook bank records and their original baseline files are preserved byte-for-byte. The combined reader selects these eight plus one clearly synthetic engineering control. The synthetic-only strict build has zero reference-depth gaps. The combined draft retains the textbook baseline's ten missing-representation/overflow findings. The new synthetic diagram shows only directions already supplied in its stem; it is authored engineering support, not a source examination figure.

The adapter supports only the pinned authored synthetic dialect, SINGLE_CHOICE with A… option order, supplied answer prose, explicit route/support/representation bindings and existing canonical capability/family references. Unknown figure mapping, unsupported response/option label mappings, stale source bindings and invalid native references fail rather than being silently normalized. Native owner-bank checks and actual package/question schemas run in addition to the adapter; no fixture-directory schema bypass is used.

All fourteen examination records still have empty native answer summaries/routes in the received projection; one has no stem and three carry unbound figure references. Their source/key, approved-adapter, semantic-cell and distinct review dependencies remain open. This integration intentionally does not manufacture those missing academic fields. The regenerated metadata gate and native readiness report agree on HOLD. Counts remain fourteen conditional leads, seven vacancies, zero admissions against twenty-one distinct originals, three per operation across D3/D4, fourteen cells.

## What the checks establish

The 33 received unit tests were rerun successfully and remain structural prototype checks. The 26 new author integration tests use the unchanged native schemas/validators and literal preserved source bytes. Actual renderer controls reject a strict combined build atomically and reject an unresolved selection even under draft mode. Relocated input construction succeeds with original candidate and textbook source reads denied, but still requires the declared C: native runtime. This is not a portable independent runtime distribution.

Browser checks cover both viewport widths, support body reveal, blank refusal, mouse and keyboard typed/MCQ commitments, protected solution opening, assisted-state/response restoration, page overflow and exact wrong/correct standalone-viewer controls. The original browser assertion searched 'correct' inside 'incorrect'; the replacement oracle compares full result strings and demonstrates a wrong answer failing the positive verdict. This is author evidence, not distinct QA or academic qualification.

## Preserved limits and next consumer

Native-shell links to unavailable subject portals, the inherited NLM concept route and absent PDFs remain open. No placeholder course pages or false PDF were added. Original source assumptions, printed/extract differences, missing source figures and Physics qualifications remain visible. The two registered repository golden fixtures remain candidates, not newly Owner-blessed fixtures; this synthetic strict control does not confer such blessing.

A distinct technical reviewer should verify current bytes, schema authority, native flow and negative controls. A distinct academic reviewer must inspect exact examination source/question/key/figures and independently determine the primary operation and five-factor demand using the pinned Physics blueprint and explicitly selected compatible WPE adapter. Only an evidenced admission can fill a quota. The source-to-Core1A ten-node dossier remains preparation with zero qualified warrants/reviewed SL2 joins/native lessons.

Core2 → Owner approval → Core1A lesson construction → Owner approval → Core1B remains the product gate. An engineering preview is not that approval. D3.1 remains paused. No remote write, installation, new agent or release is performed.
'''
(ROOT/'CONCEPT_NOTE.md').write_text(concept,encoding='utf-8')
table='<table><tr><th>Received field</th><th>Native mapping</th><th>Limit</th></tr>'+''.join('<tr>'+''.join('<td>'+e(c)+'</td>' for c in row)+'</tr>' for row in mapping)+'</table>'
(ROOT/'concept.html').write_text(page('WPE · integration concept and contracts','<pre>'+e(concept)+'</pre>'+table),encoding='utf-8')
(ROOT/'README.md').write_text('''# WPE-CORE2-NATIVE-INTEGRATION-R1

PRIVATE / SOURCE-BEARING / AUTHOR ENGINEERING CANDIDATE. Start with index.html. Open rendered/core2.html for 8 textbooks + 1 synthetic control; synthetic-rendered/core2.html is the strict control. The original textbook reader is retained under textbook-baseline/. No examination admission or independent QA is claimed.

## Rebuild in this Windows environment

Python with jsonschema and the pinned C:/CodeC/Grade9v3.5 runtime is required. No installation is included. Set PYTHONDONTWRITEBYTECODE=1 or use -B. From implementation/:

    python -B prepare_candidate.py
    python -B C:/CodeC/Grade9v3.5/Shared/tools/render_core.py build --manifest ../native/manifest.json --out ../rendered --draft --reference
    python -B C:/CodeC/Grade9v3.5/Shared/tools/render_core.py build --manifest ../native/synthetic-manifest.json --out ../synthetic-rendered --reference
    python -B test_integration.py
    python -B verify_builds.py

Run prepare_candidate.py without --retain for an already retained candidate. --retain reacquires the hash-checked original archives/baseline and is intended only for a new candidate. prepare_candidate.py rewrites candidate manifests and synthetic bindings intentionally; do not run it over a reviewed freeze without recording new hashes.

Browser protocol: serve this candidate only on loopback; use an isolated Playwright CLI Chrome session and implementation/browser_checks.js. It expects http://127.0.0.1:8785, saves screenshots to this original candidate path, and returns JSON. Adapt root/screenshot paths explicitly when moving the harness. It does not publish or contact chat agents. Stop the server and close only this task browser after checks.

## Distinct QA handoff

Read CONCEPT_NOTE.md, review/NATIVE_MAPPING.json, PRESERVATION_PINS.json, INTEGRATION_TESTS.json, BUILD_CONTROLS.json, BROWSER_CHECKS.json and both native render receipts. Replay the explicit failures. Check the eight-question bank byte identity; the only pre-existing package-field changes are title and representation asset paths, plus one appended synthetic representation. Confirm no real EX-* question enters the native selection.

The received 33-test engine is preserved under received-engineering/. Its synthetic fake witnesses prove structure only. Do not convert metadata eligibility into admission. Received original browser_test.py has a documented substring-oracle defect and Linux-specific browser path; current browser_checks.js supplies the corrected exact predicate and actual URL/keyboard checks. Do not claim the unchanged original browser script was rerun.

14 examination leads / 7 vacancies / 0 admissions. Owner review of engineering scope does not approve the complete Core2 product or waive Core1A/Core1B gates. D3.1 paused. Original worktree custody/cleanliness is not asserted; all product edits are confined to this separate local candidate.
''',encoding='utf-8')
print('Created private Owner entry, 14-cell matrix, 23-record review catalogue, concept note and exact native mapping.')
