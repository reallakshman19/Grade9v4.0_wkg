"""Finalize documentation and a private, exact-byte review archive."""
from pathlib import Path
import datetime,hashlib,html,json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

browser={'tool':'Installed Playwright CLI / Chrome; loopback only','initial_launch':'Sandbox Chrome crash-handler failure; approved outside-sandbox route used. Initial sandbox preview unavailable from browser; hidden outside-sandbox preview then used.','before_commit':{'questions':8,'live_solution_moves':0,'inert_templates':32,'chain_answer_visible':False,'document_width':1280,'viewport':1280},'exercised':['Illustration 1 typed answer and commitment','Illustration 1 solution opened and final work visible','Illustration 1 first guided prompt requested; later Reveal support body intentionally remained closed','Illustration 6 option B selected and committed; three solution moves materialized','Illustration 11 remained uncommitted with no solution moves and no visible 4/9 answer','Mobile width390 fits390 document; desktop1280 fits1280','Screenshots desktop and mobile visually inspected'],'known_tool_event':'One stale solution ref after commitment was rejected; a fresh snapshot supplied the current ref and the later click succeeded.','not_run':['All eight solutions and every hint reveal individually exercised','Independent P1 collection or academic review','Full source-to-print and original-figure equivalence','Native portal and PDF integration'],'console':['favicon404 only during exercised paths'],'cleanup':read(ROOT/'review/CLEANUP.json'),'independent_acceptance':'NONE'}
save(ROOT/'review/BROWSER_CHECK.json',browser)
results=read(ROOT/'review/REGRESSION_RESULTS.json');native=read(ROOT/'rendered/render-receipt.json');links=read(ROOT/'review/STATIC_LINKS.json')
side=read(ROOT/'review/questions.json');bank=read(ROOT/'native/bank.json')
extract_hash=sha((ROOT/'sources/work_energy_power.md').read_bytes())
hash_claims=[q['extensions']['wpe:textbook_source']['extract_sha256'] for q in bank['questions']]
save(ROOT/'review/EXTRACT_HASH_READBACK.json',{'retained_byte_sha256':extract_hash,'all_record_extract_hashes_match':all(h==extract_hash for h in hash_claims)})
if not all(h==extract_hash for h in hash_claims):raise ValueError('Extract byte hash differs from record claim')
report='''# WPE textbook Core2 R1 — delivery and review

Status: PARTIAL / PRIVATE OWNER REVIEW CANDIDATE. Eight supplied textbook illustrations are prepared in the actual native Core2 reader. Zero independent admissions; no completed Core1A lesson. The examination-bank proposal of 14 conditional leads/seven gaps remains separate and unchanged.

## Concept correction delivered first

The textbook supplies both explanatory passages for Core1A preparation and existing questions for Core2. This corrects the earlier overly rigid bank/non-bank split. CONCEPT_NOTE.md and concept.html are the current local revision. The frozen historical Source-to-Core1A report and all earlier ZIPs are preserved, not overwritten. No shared Page/Common record was changed.

## Exact output

index.html: Owner overview and eight-question links. rendered/core2.html: governed draft learner reader. review.html: author-only evidence and SL1/SL2-style proposals. native/: actual intake, owner-supplied bank, package context and product manifest. review/questions.json: eight supplementary source/cognitive/QRT dossiers. sources/: exact retained extract, nine scans and ten supplied generated SVGs.

The reader preserves the supplied extracted stem and original MCQ choices; equivalence to printed wording is not asserted. The book's JEE badges are unauthenticated source labels. Source working, including Solution (B), is separately retained in the author view. Structured route prose, support and additional checks are author-derived and explicitly distinct from printed source text. These sidecars have not passed an appointed independent Smart Labelling review. No learner attempt has become EVIDENCE-mode P1.

Each question has two requested support prompts. Native support defaults permit requested pre-commit orientation; requests do not complete the declared protected move. Such exposure prevents an independent-first-attempt claim. A native owner-bank check rejects the attempted AFTER_ATTEMPT configuration because its support-count logic counts only pre-attempt support. No shared validator was changed or bypassed. This candidate uses the supported requested-orientation lane and records no independent learner evidence.

## Verification and limits

Twenty author-side tests pass: exact eight identities, original/retained bytes, native question/package schemas, intake correspondence, dependency changes to stem/options/answer/working, duplicates, invented exam identity, fake admission/P1, support/crux references, five-factor sums, limited arithmetic/endpoint checks and protected answer-figure placement. This does not qualify all Physics or establish source authenticity.

Actual unmodified renderer build: PAGES, --draft --reference, output role CORE2 only. Eight question records selected; two native pages written. Ten reference-depth gaps remain: missing pre-attempt representations and inherited SVG label overflow. The diagram carrying the chain answer, string force-balance FBD and incline answer FBD are confined to protected solutions. Retained redraws are not certified original figures. Review the exact render-receipt.json rather than treating a successful draft build as academic completion.

Browser: eight questions, zero live solution moves before commitment, untouched chain answer absent; typed and MCQ commitments tested; first working and first support prompt exercised. Mobile390 and desktop1280 widths fit. The first support reveal body and every later support rung were not individually exercised. One stale-ref interaction was retried with a fresh snapshot. Three screenshots were inspected. Only favicon404 occurred on the exercised routes. Task browser closed and preview servers absent.

Static navigation: 79 links inspected; 11 missing-link occurrences remain in the native shell (subject portals, inherited topic registry route and unproduced PDF). These are actual draft integration defects, not successful navigation. Core2 reader content, overview, source review and local CSS/JS are present. Do not follow the unrelated inherited NLM topic route as evidence of WPE construction. The current standalone ZIP is for viewing the private draft. Native rebuild uses the original read-only C:\\CodeC toolchain and absolute pinned input paths; portable native rebuild has not been established.

## Source defects carried forward

5: missing initial speed; displayed result conditional on release from rest. 11: initial zero kinetic energy supplied by printed solution, not the extracted stem; chain contact/edge assumptions unqualified. 12: extraction adds detailed piecewise algebra and explicit rest beyond the printed qualitative working. Canonical variable-force/spring/contact warrants and reviewed task joins remain pending. No text was silently repaired into a different question.

Owner may review source fidelity, reader experience and candidate classifications now. Independent semantic review, original-figure fidelity, native reference-depth defects and shell/PDF integration remain before academic acceptance. Owner approval is still required before Core1A lesson construction; Core1B follows Core1A approval. D3.1 remains PAUSED.
'''
(ROOT/'DELIVERY_REPORT.md').write_text(report,encoding='utf-8')
note=(ROOT/'CONCEPT_NOTE.md').read_text(encoding='utf-8')
note+='\n## Delivered textbook candidate\n\nEight native Core2 question records and a governed draft reader now exist. Twenty author checks pass. Native render retains ten reference-depth findings; static shell navigation retains eleven missing-link occurrences. Eight source/cognitive/QRT sidecars are proposals, not reviewed native Smart Labelling admissions. Browser checks cover typed and MCQ commitments, first working, first support prompt, protected untouched chain and desktop/mobile width. All eight have zero independent admissions. See DELIVERY_REPORT.md and review/BROWSER_CHECK.json. Native source code and input originals remain unchanged.\n'
(ROOT/'CONCEPT_NOTE.md').write_text(note,encoding='utf-8')
concept=ROOT/'concept.html';s=concept.read_text(encoding='utf-8');a=s.index('<pre>');b=s.index('</pre>',a);concept.write_text(s[:a]+'<pre>'+html.escape(note)+s[b:],encoding='utf-8')
overview=ROOT/'index.html';s=overview.read_text(encoding='utf-8');s=s.replace('</main>','<section class="hold"><h2>Draft integration limits</h2><p>Eleven native shell links are unavailable locally: subject portals, an inherited unrelated topic route and PDF. Do not treat them as completed navigation. Source and semantic review remain pending.</p><p><a href="DELIVERY_REPORT.md">Full delivery report</a> · <a href="review/BROWSER_CHECK.json">Browser evidence and limitations</a></p></section></main>');overview.write_text(s,encoding='utf-8')
continuity='''# WPE textbook Core2 R1 continuity

Thread01a188e5-af7a-7881-b414-b465ca99680f. Restore Oracle (standalone); do not repeat role selection. Task WPE-TEXTBOOK-CORE2-R1 was the bounded continuation approved by Owner's “update you concept note and then proceed” after the explicit Coder/45-minute/45-call proposal. AUTHORITY.json retains interpretation and scope. External WPE_TEXTBOOK_CORE2_R1_DELIVERY_RECEIPT.json closes this pre-delivery snapshot. No reuse of closed capacity.

Concept note corrected first: textbook questions also supply Core2. New local CONCEPT_NOTE.md/concept.html supersede the rigid source split; frozen older notes/ZIPs remain historical. Eight illustrations1–6,11–12 source-bound into native owner-supplied bank plus actual package/manifest and unmodified governed Core2 renderer. Native draft has10 reference-depth gaps, local shell11 missing-link occurrences. Twenty author checks pass; browser typed/MCQ commitments and protection/width exercised, not every hint or solution. No independent review/admission or P1. Source diagrams that leak work/answer are solution-only. Book JEE labels unauthenticated; extraction not certified verbatim print. Questions5,11,12 conditional/disputed. Source-to-Core1A R2 still ten-node preparation, zero qualified warrants/reviewed joins/native lessons.

Entry index.html; learner draft rendered/core2.html; author evidence review.html; full DELVERY details DELIVERY_REPORT.md; native inputs native/; pin/validation/browser reports review/. Local rendered viewing assets retained, but portable native rebuild NOT_ESTABLISHED: original pinned C:\\CodeC toolchain and absolute native paths required. Do not claim accepted Core2 or complete template fidelity from a draft render. Governing textbook/exam denominator remains separate; original examination return14 conditional/seven gaps/zero admissions unchanged.

All sources/shared tools/original skills preserved. No remote writes, installation, new agents, lessons or D3.1 resume. Preview browser/server closed; cleanup receipt saved. Owner reviews exact candidate next. Distinct semantic review, source/figure fidelity and native/shell defects remain. Completed-Core2 Owner approval still precedes Core1A construction; Core1A approval precedes Core1B. D3.1 remains PAUSED. Current stable pointer updated locally only.
'''
(ROOT/'CONTINUITY.md').write_text(continuity,encoding='utf-8')
payloads=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name!='DELIVERY_MANIFEST.json' and '__pycache__' not in p.parts:
  payloads.append({'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save(ROOT/'DELIVERY_MANIFEST.json',{'schema':'private-review-archive/v1','task':'WPE-TEXTBOOK-CORE2-R1','payloads':payloads,'academic_acceptance':'NONE'})
archive=OUT/'WPE_TEXTBOOK_CORE2_R1_CANDIDATE.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for row in payloads:z.write(ROOT/row['path'],row['path'])
 z.write(ROOT/'DELIVERY_MANIFEST.json','DELIVERY_MANIFEST.json')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert set(z.namelist())=={x['path'] for x in payloads}|{'DELIVERY_MANIFEST.json'}
 for row in payloads:
  raw=z.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and raw==(ROOT/row['path']).read_bytes()
identity={'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'payloads':len(payloads),'members':len(payloads)+1,'CRC':'PASS','membership':'PASS','every_payload_hash_size_and_root_correspondence':'PASS'}
(archive.with_suffix('.zip.sha256')).write_text(identity['sha256']+'  '+archive.name+'\n')
save(OUT/'WPE_TEXTBOOK_CORE2_R1_ARCHIVE_READBACK.json',identity)
print(json.dumps(identity,indent=2))
