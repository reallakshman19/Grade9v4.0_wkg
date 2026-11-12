from pathlib import Path
import json,sys,hashlib,csv
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
R=Path(__file__).resolve().parent;S=R/'skill/source-to-core1a';P=S/'examples/wpe-source-program'
sys.path.insert(0,str(S/'scripts'))
from render_program import page,E,listing,render
from check_program import check_program
from check_handoff import file_sha,load
expected=load(R/'review/EXTERNAL_PIN_RECEIPT.json')['sha256'];result=render(P/'program.json',expected)
(R/'review/PROGRAM_CHECK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
cov=load(R/'review/COVERAGE.json');receipts=load(R/'review/SOURCE_RECEIPT.json')
program=load(P/'program.json');records=[load(P/x['path']) for x in program['records']]
stats={'nodes':len(records),'claims':sum(len(d['claims']) for d in records),'exact_units':sum(len(d['units']) for d in records),'construction_requirements':sum(len(d['construction']['steps']) for d in records),'review_requests':sum(len(d['review_requests']) for d in records),'native_mapping_rows':sum(len(d['native_mapping']) for d in records),'wrong_path_designs':sum(len(d['construction']['wrong_path_candidates']) for d in records),'independent_check_designs':sum(len(d['construction']['check_requirements']) for d in records),'missing_warrant_groups':sum(w['qualification']=='MISSING' for d in records for w in d['warrants']),'candidate_warrant_groups':sum(w['qualification']=='CANDIDATE' for d in records for w in d['warrants']),'retained_original_files':len(receipts),'source_lines_accounted':486,'source_scans_author_viewed':9,'qualified_warrants':0,'reviewed_SL2_joins':0,'native_lessons':0}
(R/'review/COUNTS.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
table='\n'.join('| '+x['node']+' | '+x['title']+' | '+x['canonical_match']+' | '+('Explicit gap' if x['missing_warrant'] else 'Candidate only')+' |' for x in cov)
report=f'''# WPE Source → Core1A completion R2 — preparation result

**Scoped outcome:** the local candidate skill/protocol and preparation workflow now account for all ten frozen WPE syllabus nodes. This completes the approved candidate-preparation scope, not science qualification, reviewed task alignment or learner lessons. Original R1 and source inputs are preserved. No installation or remote update occurred.

## Owner request and authority

Owner asked to complete the source→concept/prerequisite→qualified-warrant→construction→condition/boundary→wrong-route repair→independent-check→reviewed-SL2 requirement flow, then explicitly assigned Coder for WPE-SOURCE-CORE1A-COMPLETION-R2 and approved a single-agent local routine,60minutes/60inspection-verification calls. Session otherwise remains Oracle(standalone), thread01a188e5-af7a-7881-b414-b465ca99680f. Scientific qualification/reviewed SL2 must have genuine evidence; unresolved parts stay explicit. No Core1A lesson, agent, installation, remote write or D3.1 resume is permitted here.

## What was completed

The skill is v0.2.0-candidate. Retained v1 record/checker/example remain compatible. New typed v2 node records and a program scope checker cover honest partial source bindings. Source→claim→candidate/missing warrant→construction role→native property→version-bound review request is mechanically traversable. MISSING is a first-class warrant state and has no fake canonical reference. Source scans, generated figures and a proposed reference ontology have distinct roles. Reviewed SL2 remains explicitly pending; the schema cannot forge a reviewed task, independent outcome or Owner approval.

All ten actual spine identities and all486 retained chapter lines have an intake disposition. There are{stats['claims']} claims,{stats['exact_units']} exact units,{stats['construction_requirements']} requirement rows,{stats['review_requests']} review requests,{stats['native_mapping_rows']} native property mappings,ten repair designs andten independent-check designs. These are author obligations, not completed teaching or observed learner performance. The numbers arise from this WPE case, not universal minimums for every skill use.

Twenty-seven originals are retained: all25 files from the supplied Book/Syllabus folder, plus canonical library and native package schema. The original SVG-generation script is retained but never executed. The full chapter remains with all relative SVG image assets. All nine supplied page scans were visually inspected as author evidence, with per-page region and limitations. This is not pixel-exact OCR, diagram equivalence, publisher authenticity or independent scientific acceptance.

## Coverage and actual source gaps

| Node | Preparation subject | Canonical relationship | Warrant frontier |
|---|---|---|---|
{table}

Nine candidate warrant groups are bound provisionally; seven missing-warrant groups remain. Zero warrants are independently qualified. Some groups support prerequisites only. No borrowed microtopic is promoted to cover an absent primary capability. Especially, variable-force integration/spring laws, momentum development, path-independence derivations, spring potential, force–potential slope, chain/contact/turning models and friction contact laws need actual qualification or additional canonical work. Even nodes without an explicit missing group retain unreviewed scientific scope.

The reference ontology is retained with exact atomic-competency pointers as **REFERENCE_SOURCE**, not CANONICAL_CANDIDATE. It contains proposed force-gradient material, so N07's gap is an explicit chapter derivation and qualified canonical binding, not absence from every supplied file. Its self-described canonical_rules/source_authority labels do not confer authority. Its zero-second-derivative stability classification and broad force/work claims need review. Recall-topic notes include inherited band/exam proposals; these are retained context, never adjudicated SL2 or authentic examination evidence.

## Printed material versus extraction

1. Page7's printed substitution line reads W_c=Delta U; the extraction uses a minus sign. This discrepancy is retained for review; neither bytes nor a source label resolves Physics.
2. Page6 ends near a concepts heading. The retained image does not expose a general force–potential slope derivation; the extraction adds explicit spring formulas. The missing section8 is not reconstructed.
3. Page9's printed chain solution states initial kinetic energy zero, while the extracted problem stem omits initial rest and its solution assumes it. Preserve the actual assumption.
4. Page9's spring solution is largely qualitative. The extraction expands it into a piecewise algebraic solution. That algebra is derived transcription, not a verbatim printed passage or a newly authored Core1A lesson.
5. Page8 includes an overbroad claim about curved paths requiring changes of both force magnitude and direction; the extract omits it. Omission and correction need traceable treatment.
6. Printed and extracted blanket friction claims remain disputed. A fixed-plane sliding example cannot establish a universal sign or static-friction work rule across bodies/frames/contacts.
7. The power incline speed expression needs the actual initial-state assumptions. Average versus instantaneous, individual-force versus net power stay distinct.
8. Generated SVGs and extracted summary/authenticity/WCAG claims are derived artifacts/claims. They are not original scanned figures or accepted accessibility/source certification.

Collisions, absent illustration numbers7–10 and missing section8 remain excluded/missing source scope. Existing eight book illustrations stay source examples; no official examination identity or Core2 admission follows from coaching badges. No authored replacement questions fill the21-original target.

## Native authoring and review boundaries

Targets are actual retained native properties: entry assumptions, inferential jump, teaching path, step why_valid, representation correspondence, worked anchor and capability reference. No native records/package/manifest/course render are emitted. For an absent capability the target points to a pending match list, never an invented ID. The native source-interpretation acquisition and authoring request/packet must be real when later authorized.

Each review request pins the exact current target object. Missing/duplicate review targets and changed target digests fail integrity. The program's externally expected digest binds all record and pin-file identities. Without that external anchor, whole-program replacement remains self-declared even if its internal pin files agree. Matching expected bytes does not authenticate sources or a reviewer.

The reviewed-SL2 consumer boundary remains unimplemented because no genuine reviewed requirement was supplied. Later integration must consume the actual current task/source/dependency identity, operation/demand, source role, reviewer authority/exposure and native disposition. R2 deliberately rejects fake reviewed enums instead of providing a misleading promotion command. Scientific review, binder sufficiency and actual native runtime are separate work.

## Verification and surviving wrong cases

See review/REGRESSION_RESULTS.json for the actually executed final suite, and review/PROGRAM_CHECK.json for the exact externally pinned program check. The suite preserves50 R1 tests and adds60 R2 tests at this version, including true gap acceptance, coherent source substitution, key/pointer/path/reference errors, missing or duplicate scope, cycles, stale target digests, fictional observations, fake approved states and reference material masquerading as canonical science. HTML interpretation/source markup is escaped.

A coherent false Physics claim with consistently refreshed internal hashes can still PASS mechanical integrity. Both versions explicitly preserve that test: semantic review remains NOT_RUN and authoring HOLD. No independent reviewer or forward-testing agent is launched. Original tests rerun from a relocated copy establish portability only, not independent academic endorsement.

Static link/anchor, source-preservation and ZIP checks have separate receipts. Browser observations, if performed, are narrowly recorded in review/BROWSER_CHECK.json; do not infer scientific/course correctness from a screenshot or DOM. Frozen original candidate ZIPs/skills are never edited. The delivery receipt outside the ZIP closes actual time/call counts and final archive identity.

## Continuation and original project gates

Latest received Core2 remains14 conditional leads/seven gaps/zero independent admissions; its original13/eight freeze is unchanged. R2 changes source preparation, not Core2. Completed Core2 Owner approval precedes Core1A lesson construction; Core1A approval precedes Core1B. D3.1 remains PAUSED. The published Page/Common snapshot still records the earlier one-dossier preparation state; this local-only routine does not update those shared records.

Next useful consumer is a genuinely appointed scientific/source reviewer and QRT/binding owner for one exact construction brief, with missing material and prior author exposure disclosed. No assignment or scope is created by this report. Owner reviews this R2 output first. Any subsequent source, canonical, adapter, reviewed-task or lesson work needs its actual authority and new resource bound after closure.
'''
(R/'COMPLETION_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
body='<h1>WPE source preparation · R2</h1><div class="hold"><strong>Candidate preparation complete across10 scope nodes</strong><br>Science and reviewed SL2 remain open; zero native lessons. D3.1 paused.</div><p><a href="skill/source-to-core1a/examples/wpe-source-program/index.html">Open all ten detailed dossiers</a></p><p><a href="COMPLETION_REPORT.md">Completion report</a> · <a href="skill/source-to-core1a/SKILL.md">Skill</a> · <a href="skill/source-to-core1a/references/protocol-r2.md">Protocol</a> · <a href="review/PROGRAM_CHECK.json">Program checks</a> · <a href="coverage.csv">Coverage CSV</a></p><table><tr><th>Measure</th><th>Actual result</th></tr>'+''.join('<tr><td>'+E(k.replace('_',' '))+'</td><td>'+E(v)+'</td></tr>' for k,v in stats.items())+'</table><h2>Completion boundary</h2><p>Source coverage means every node and retained line is accounted for. It does not certify all concepts, warrants, teaching or examination evidence. Open the detailed dossiers to inspect exact passages, conditions, gaps, repair/check designs and review requests.</p>'
(R/'index.html').write_text(page('WPE Source → Core1A R2',body),encoding='utf-8',newline='\n')
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.scripts=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='script':self.scripts+=1
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
files=[R/'index.html',P/'index.html',*sorted((P/'handoffs').glob('*.html'))]
parsed={}
for f in files:
 x=Parse();x.feed(f.read_text(encoding='utf-8'));parsed[f.resolve()]=x
fail=[];checked=0
for f,x in parsed.items():
 if x.scripts:fail.append(str(f)+' script element')
 for raw in x.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:fail.append(str(f)+' unexpected remote link '+raw);continue
  dest=(f.parent/unquote(u.path)).resolve() if u.path else f
  if not dest.is_relative_to(R.resolve()) or not dest.is_file():fail.append(str(f)+' missing/outside '+raw);continue
  if u.fragment:
   target=parsed.get(dest)
   if target is None:
    target=Parse();target.feed(dest.read_text(encoding='utf-8'));parsed[dest]=target
   if unquote(u.fragment) not in target.ids:fail.append(str(f)+' missing anchor '+raw)
  checked+=1
pres=[]
for old in load(R/'review/R1_PRESERVATION_BASELINE.json'):
 p=Path(old['path']);pres.append({'path':old['path'],'unchanged':p.is_file() and file_sha(p)==old['sha256']})
for x in receipts:
 p=Path(x['original_path']);copy=R/x['candidate_path']
 pres.append({'path':str(p),'unchanged':file_sha(p)==x['sha256'],'copy_matches':file_sha(copy)==x['sha256']})
validation={'source_nodes':10,'source_lines':486,'HTML_files':len(files),'local_links_and_fragments_checked':checked,'findings':fail,'static_HTML':'PASS' if not fail else 'FAIL','original_R1_and_sources':'PASS' if all(x['unchanged'] and x.get('copy_matches',True) for x in pres) else 'FAIL','science':'NOT_QUALIFIED','independent_review':'NOT_RUN'}
(R/'review/PRESERVATION.json').write_text(json.dumps(pres,indent=2),encoding='utf-8');(R/'review/STATIC_VALIDATION.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2));assert not fail and validation['original_R1_and_sources']=='PASS'
