from pathlib import Path
import sys,json,shutil,subprocess,concurrent.futures
R=Path(__file__).resolve().parent;S=R/'skill/source-to-core1a'
work=R/'_checks/relocated';assert work.resolve().is_relative_to(R.resolve()) and work.resolve()!=R.resolve()
target=work/'skill/source-to-core1a';target.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(S,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
def suite(skill,dest):
 code="""import unittest,io,json,sys,time
from pathlib import Path
s=Path(sys.argv[1]);out=Path(sys.argv[2]);stream=io.StringIO();t=time.monotonic()
r=unittest.TextTestRunner(stream=stream,verbosity=1).run(unittest.defaultTestLoader.discover(str(s/'tests')))
d={'tests_run':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'successful':r.wasSuccessful(),'elapsed_seconds':round(time.monotonic()-t,2),'output':stream.getvalue(),'scope':'Author-side mechanical regression; not independent scientific review'}
out.write_text(json.dumps(d,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in d.items() if k!='output'}));raise SystemExit(not r.wasSuccessful())
"""
 p=subprocess.run([sys.executable,'-B','-c',code,str(skill.resolve()),str(dest.resolve())],capture_output=True,text=True,timeout=180)
 return {'exit_code':p.returncode,'output':p.stdout+p.stderr}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 jobs=[ex.submit(suite,S,R/'review/REGRESSION_RESULTS.json'),ex.submit(suite,target,R/'review/PORTABLE_REGRESSION_RESULTS.json')]
 results=[x.result() for x in jobs]
for result in results:print(json.dumps(result))
assert all(x['exit_code']==0 for x in results)
guard="""from pathlib import Path
import sys,json
orig=Path(sys.argv[1]).resolve();skill=Path(sys.argv[2]).resolve();expected=sys.argv[3]
sys.path.insert(0,str(skill/'scripts'))
from check_program import check_program
from unittest.mock import patch
old=Path.open;reads=[]
blocked=[orig,Path('C:/CodeC/Grade9v3.5').resolve(),Path('D:/CodeD/g9v3.5/chatgpt/output/WPE_Question_Bank_and_Book_2026-10-30').resolve()]
def guarded(self,*a,**kw):
 p=self.resolve()
 if any(p.is_relative_to(x) for x in blocked):raise PermissionError('Original source access denied')
 reads.append(str(p));return old(self,*a,**kw)
with patch.object(Path,'open',guarded):
 try:(orig/'SKILL.md').read_text();raise AssertionError('Guard did not deny original')
 except PermissionError:pass
 result=check_program(skill/'examples/wpe-source-program/program.json',expected)
assert result['integrity']=='PASS',result
print(json.dumps({'integrity':'PASS','guard_probe':'ORIGINAL_ACCESS_DENIED','original_reads_during_check':0,'relocated_read_operations':len(reads),'scope_binding':result['scope_binding'],'nodes':result['nodes_accounted'],'science':'NOT_QUALIFIED'}))
"""
expected=json.loads((R/'review/EXTERNAL_PIN_RECEIPT.json').read_text())['sha256']
p=subprocess.run([sys.executable,'-B','-c',guard,str(S.resolve()),str(target.resolve()),expected],capture_output=True,text=True,timeout=60)
print(p.stdout+p.stderr);assert p.returncode==0
(R/'review/PORTABILITY.json').write_text(p.stdout,encoding='utf-8')
# Final code-byte correspondence, not an assertion based on a copied label.
import hashlib
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
codefiles=[p for p in S.rglob('*.py') if '__pycache__' not in p.parts]
equal=[{'path':str(p.relative_to(S)),'sha256':sha(p),'relocated_matches':sha(p)==sha(target/p.relative_to(S))} for p in codefiles]
assert all(x['relocated_matches'] for x in equal)
(R/'review/PORTABLE_CODE_IDENTITIES.json').write_text(json.dumps(equal,indent=2),encoding='utf-8')
browser={'tool':'Installed cached Playwright CLI, Chrome headless, loopback127.0.0.1 only','performed':['Root entry→ten-node catalogue native click','Catalogue→N07 gap dossier native click','N07 desktop1280: missing warrant and pending reviewed SL2 visible; no horizontal overflow','N09 source-derived figure loaded1/1','N09 mobile390: initial overflow reproduced, fixed in renderer CSS, final documentWidth390 equals viewport390','Screenshots catalogue and N07 desktop / N09 mobile inspected'], 'not_run':['Actual learner lesson/Core2 runtime or scientific review','All ten dossiers individually exercised in browser','Catalogue mobile DOM count/overflow measurement: CLI selector quoting error; no PASS inferred'], 'known_console':['Missing favicon404; not a missing source figure or script exception'], 'cleanup':'Both task browser sessions closed; both verified port8773 server processes stopped','static_link_checks':528,'semantic_acceptance':'NONE'}
(R/'review/BROWSER_CHECK.json').write_text(json.dumps(browser,indent=2),encoding='utf-8')
source_rows=json.loads((R/'review/SOURCE_RECEIPT.json').read_text())
inputroot=Path('D:/CodeD/g9v3.5/chatgpt/output/WPE_Question_Bank_and_Book_2026-10-30/02_Book_and_Syllabus').resolve()
expected_files={str(p.resolve()) for p in inputroot.rglob('*') if p.is_file()}
captured={str(Path(x['original_path']).resolve()) for x in source_rows if Path(x['original_path']).resolve().is_relative_to(inputroot)}
assert expected_files==captured,(expected_files-captured,captured-expected_files)
(R/'review/INPUT_COVERAGE.json').write_text(json.dumps({'input_files':len(expected_files),'retained_input_files':len(captured),'missing':[],'extra_context_files':2,'original_generator':'RETAINED_NOT_EXECUTED','reference_ontology':'REFERENCE_SOURCE_NOT_CANONICAL'},indent=2),encoding='utf-8')
print(json.dumps({'suite_results':'PASS','relocation':'PASS','final_code_files_matched':len(equal),'input_files_retained':len(captured)}))
