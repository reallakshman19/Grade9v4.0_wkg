"""Freeze this private candidate and verify every packaged payload against bytes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Final generated documentary views use the observed final evidence counts.
subprocess.run([sys.executable,'-B',str(ROOT/'implementation/finish_delivery.py')],check=True)
checks=read(ROOT/'review/INTEGRATION_TESTS.json');browser=read(ROOT/'review/BROWSER_CHECKS.json');controls=read(ROOT/'review/BUILD_CONTROLS.json')
if not checks['pass'] or browser['passed']!=browser['total'] or not controls['pass']:raise ValueError('CHECKS_NOT_PASSING')
pins=read(ROOT/'review/PRESERVATION_PINS.json')
for row in pins:
    if sha(Path(row['original']))!=row['sha256'] or sha(ROOT/row['retained'])!=row['sha256']:raise ValueError('ORIGINAL_OR_RETAINED_CHANGED:'+row['original'])
save(ROOT/'review/UPSTREAM_UNIT_RERUN.json',{'command':'python -B -m unittest discover -s tests -p test_engine.py -v',
    'cwd':'received-engineering','tests':33,'failures':0,'errors':0,'observed_exit_code':0,
    'evidence':'Executed in this approved routine; terminal output lists all 33 tests. Original source/tests unchanged.',
    'scope':'Structural prototype tests with synthetic fake review/source witnesses; not native or academic acceptance.'})
save(ROOT/'review/CLEANUP.json',{'browser_session':'wpe-native-r1','browser':'CLOSED (CLI readback)',
    'loopback_server_pid':30804,'port':8785,'server':'STOPPED (exact task command-line verified before stopping)',
    'agents_launched':0,'remote_writes':0,'d31':'PAUSED'})

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
cache={};missing=[];broken_fragments=[];total=0
def parsed(path):
    if path not in cache:
        obj=Links();obj.feed(path.read_text(encoding='utf-8'));cache[path]=obj
    return cache[path]
for rel in ['index.html','review.html','concept.html','rendered/index.html','rendered/core2.html','synthetic-rendered/index.html','synthetic-rendered/core2.html']:
    p=ROOT/rel
    for href in parsed(p).links:
        u=urlsplit(href)
        if u.scheme or href.startswith('//'):continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        total+=1
        if not target.exists():missing.append({'page':rel,'href':href});continue
        if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in parsed(target).ids:
            broken_fragments.append({'page':rel,'href':href})
save(ROOT/'review/LOCAL_LINKS.json',{'checked_occurrences':total,'missing_files':missing,'missing_fragments':broken_fragments,
    'scope':'Current seven Owner/native entry pages; retained historical baseline not reauthored. Native missing portals/PDF remain open.',
    'owner_entry_broken_links':[x for x in missing+broken_fragments if x['page'] in ['index.html','review.html','concept.html']]})
if any(x['page'] in ['index.html','review.html','concept.html'] for x in missing+broken_fragments):raise ValueError('OWNER_ENTRY_LINK_BROKEN')

context=ROOT/'context';context.mkdir(exist_ok=True)
for name in ['WPE_QUESTION_TO_CORE2_END_TO_END_PLAN_20261030.md','WPE_QUESTION_TO_CORE2_INPUT_REGISTER_20261030.json','WPE_ORACLE_PLAN_CONSOLIDATED_CHECKPOINT_20261030.md']:
    shutil.copy2(ROOT.parent/name,context/name)

save(ROOT/'review/CHANGE_RECORD.json',{'task':'WPE-CORE2-NATIVE-INTEGRATION-R1','scope':'Separate private candidate only',
    'changes':['Explicit source-bound synthetic native adapter and authored bindings','Native manifest selects 8 preserved textbook questions plus 1 synthetic control',
               'Native package changes only title and existing asset paths, with 1 appended synthetic representation','New strict synthetic-only native manifest',
               '14 received examination records retained and held; regenerated metadata/native readiness reports','Private entry/matrix/filter catalogue, mapping, controls and continuity'],
    'unchanged':['Original textbook bank/intake and complete retained baseline','Both original handoff archives','Canonical library and native schema/renderer/tool files','Original skill files and Physics blueprints/adapters'],
    'test_counts':{'upstream_unit_rerun':33,'current_author_integration':checks['tests'],'browser_assertions':browser['total'],'actual_build_controls':len(controls['results'])},
    'acceptance':{'academic':'NOT_RUN','distinct_technical_qa':'NOT_RUN','owner_product':'NOT_REQUESTED_BY_THIS_RECEIPT','real_exam_admissions':0},
    'open_reference_gaps':10,'link_findings_file':'LOCAL_LINKS.json'})

(ROOT/'review/FAILURES_AND_LIMITS.md').write_text('''# Retained failed attempts and scope limits

- Initial new-test setup assumed the canonical package had a question. It has questions=[]; the wrong-authority test now constructs that explicit negative condition and passes against the unchanged native selection validator. Product data was not altered to satisfy the test.
- Sandboxed Chrome failed its crashpad launch. An approved outside-sandbox isolated Chrome session ran actual loopback URL navigation. Initial sandbox server was unreachable from that session; the task-specific hidden loopback server was launched outside the sandbox and later stopped.
- Initial relocation probe failed at sandbox temporary-directory permissions. The corrected probe used a checked workspace path, denied reads from the primary candidate and original textbook during build, and passed. A nonessential sandbox process query also lacked CIM permission; cleanup used the authorized host context and exact task command line.
- Source-ID option labels initially appeared twice because the native renderer supplies A/B/C/D labels. Native option strings now preserve text only with a reversible ID/index sidecar; unsupported source label sequences fail explicitly. The synthetic horizontal arrow was shortened after visual inspection to avoid clipping in the native projection. Final native builds/tests/screenshots were refreshed.
- The received engine/standalone browser are retained unchanged. Original browser_test.py was not rerun; its Linux executable path and substring assertion are unsuitable here. The current CLI harness uses exact wrong/correct result strings and demonstrates the false positive of the old substring test.
- The strict synthetic build has zero depth gaps but is not an Owner-blessed golden or independent Physics verdict. The combined draft retains ten textbook reference-depth findings; missing native portal/PDF/concept links are enumerated in LOCAL_LINKS.json. There is no security boundary against viewing static answer bytes.
- Relocated input rebuilding still uses the pinned C: native runtime. The private ZIP is a data/code/evidence handoff, not a standalone installed native runtime or public release.
- Academic review, authentic paper/key/figure custody, compatible approved WPE-adapter resolution, 21-question coverage, distinct technical QA, complete-Core2 Owner approval and later Core1A/Core1B construction remain open. No original P1 attempt is invented; local browser state is not learner research evidence.
''',encoding='utf-8')
continuity='''# WPE native Core2 integration R1 continuity

Restore Oracle (standalone), actual chat 01a188e5-af7a-7881-b414-b465ca99680f. Owner explicitly assigned Coder for WPE-CORE2-NATIVE-INTEGRATION-R1, one local single-agent routine up to60minutes/60calls. This is author engineering work, not independent QA. No remote write, installation, new agent, academic admission, Core1A lesson or D3.1 resume occurred. The external final delivery receipt records actual closure bounds; do not reuse remaining capacity after closure.

Start index.html → rendered/core2.html: eight preserved textbook bank questions and one clearly synthetic control, ten inherited textbook depth findings. synthetic-rendered/core2.html is the strict native one-question control with zero depth gaps. textbook-baseline/ retains the original complete candidate unchanged. Native bank and intake bytes are preserved. Only existing package title/asset paths change; one authored synthetic representation is appended. Canonical library/native code/schemas/original archives remain unchanged.

Read CONCEPT_NOTE.md, README.md, review/CHANGE_RECORD.json, NATIVE_MAPPING.json, PRESERVATION_PINS.json, INTEGRATION_TESTS.json, BUILD_CONTROLS.json, BROWSER_CHECKS.json, LOCAL_LINKS.json and FAILURES_AND_LIMITS.md. Source-bound adapter supports synthetic SINGLE_CHOICE with explicit A… option mapping only. Unknown features fail; this does not supply a generic trusted real-exam adapter. Required independent semantic/scientific review remains open.

Observed 33 received unit tests,26 new author integration tests,60 browser assertions and3 actual build controls passed. Browser desktop/phone checks cover commitment, safe requested support, protected solution, keyboard/typed/MCQ responses, assisted-state restoration, catalogue/matrix filters and exact negative grading controls on the separate received standalone viewer. Native reader remains self-check only. The final diagrams were visually inspected. Actual strict combined build refuses without overwriting the sentinel; draft rejects unresolved IDs. Relocation with original candidate/book reads denied passes, but C: native runtime is still required.

Examination proposal remains14 conditional leads/7vacancies/0admissions against21 originals,3peroperation acrossD3/D4 (14matrixcells). No real lead selected. Received native answers are empty; one stem and three figure bindings remain missing. Metadata eligibility cannot confer source authenticity, appointment, academic adjudication or admission. M101 and cut-spring MAIN remain different task identities. QRT blueprint and adapter documentary context retained under context/; no approved unified adapter has been selected here.

Core1A remains ten-node source preparation, no new lessons. Completed Core2 → Owner approval → Core1A lesson construction → Owner approval → Core1B; this engineering preview does not waive those gates. D3.1 PAUSED. Next consumer is a genuinely distinct technical reviewer, then the Owner's scoped engineering review; academic source/admission work is separate. No agents were appointed or messaged. Browser wpe-native-r1 closed; exact task loopback server stopped. Original worktree cleanliness/custody is not asserted. Private archive includes source-bearing Owner handoffs; do not publish it.
'''
(ROOT/'CONTINUITY.md').write_text(continuity,encoding='utf-8')

exclude={'server.stdout.log','server.stderr.log','server.pid'}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in exclude and p.name!='FILE_SHA256_MANIFEST.json')
seal={'schema':'wpe-private-candidate-sha256/v1','privacy':'OWNER_PRIVATE_SOURCE_BEARING',
      'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
save(ROOT/'FILE_SHA256_MANIFEST.json',seal)
archive=ROOT.parent/'WPE_CORE2_NATIVE_INTEGRATION_R1_PRIVATE_CANDIDATE_20261030.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[ROOT/'FILE_SHA256_MANIFEST.json']:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    if z.testzip():raise ValueError('ZIP_CRC_FAILED')
    if set(z.namelist())!={x['path'] for x in seal['files']}|{'FILE_SHA256_MANIFEST.json'}:raise ValueError('ZIP_MEMBER_SET_MISMATCH')
    for row in seal['files']:
        b=z.read(row['path'])
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('ZIP_PAYLOAD_MISMATCH:'+row['path'])
save(ROOT.parent/'WPE_CORE2_NATIVE_INTEGRATION_R1_PACKAGE_RECEIPT_20261030.json',{
    'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'payloads':len(files),
    'crc':'PASS','complete_manifest':'PASS','member_hashes_and_sizes':'PASS',
    'privacy':'OWNER_PRIVATE_SOURCE_BEARING','frozen_utc':datetime.now(timezone.utc).isoformat(),
    'preservation_pins_checked':len(pins),'native_selected':9,'textbook':8,'synthetic':1,'admitted_examinations':0,
    'tests':{'received_units':33,'author_integration':checks['tests'],'browser':browser['total'],'build_controls':len(controls['results'])},
    'reference_depth_gaps':{'combined':10,'synthetic':0},'unresolved_native_link_occurrences':len(missing)+len(broken_fragments),
    'owner_entry_link_errors':0,'distinct_qa':'NOT_RUN','academic_review':'NOT_RUN','owner_product_approval':'PENDING'})
print('PRIVATE ZIP VERIFIED',archive.stat().st_size,'bytes;',len(files),'payloads;',sha(archive))
print('Preservation pins',len(pins),'; current links checked',total,'; native link findings',len(missing)+len(broken_fragments))
