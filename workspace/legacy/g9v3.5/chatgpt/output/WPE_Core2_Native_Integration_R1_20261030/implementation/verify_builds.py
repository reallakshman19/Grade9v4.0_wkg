"""Actual fail-closed CLI and relocated-input build checks, using pinned native tools."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1];REPO=Path(r'C:\CodeC\Grade9v3.5')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
native=REPO/'Shared/tools/render_core.py';results=[]
out=ROOT/'review/negative-strict';out.mkdir(exist_ok=True)
(out/'core2.html').write_text('DO NOT OVERWRITE',encoding='utf-8')
r=subprocess.run([sys.executable,'-B',str(native),'build','--manifest',str(ROOT/'native/manifest.json'),'--out',str(out),'--reference'],capture_output=True,text=True)
results.append({'case':'strict combined draft is rejected atomically','pass':r.returncode==2 and (out/'core2.html').read_text()=='DO NOT OVERWRITE','exit':r.returncode,'stderr':r.stderr})
wrong=read(ROOT/'native/synthetic-manifest.json');wrong['selection']['core2']=['MISSING-QUESTION']
save(ROOT/'review/negative-unresolved-manifest.json',wrong)
r=subprocess.run([sys.executable,'-B',str(native),'build','--manifest',str(ROOT/'review/negative-unresolved-manifest.json'),'--out',str(ROOT/'review/negative-unresolved-output'),'--draft','--reference'],capture_output=True,text=True)
results.append({'case':'draft cannot bypass missing selected identity','pass':r.returncode==1 and 'UNRESOLVED' in r.stderr and not (ROOT/'review/negative-unresolved-output').exists(),'exit':r.returncode,'stderr':r.stderr})
# Relocate candidate inputs. C: remains the declared native runtime; original
# textbook source and primary candidate reads are explicitly denied after import.
sys.path.insert(0,str(REPO))
from Shared.tools import render_core
with tempfile.TemporaryDirectory(prefix='wpe-native-r1-relocation-',dir=ROOT.parent) as td:
    target=Path(td)
    if not target.resolve().is_relative_to(Path(r'D:\CodeD\g9v3.5').resolve()):
        raise ValueError('RELOCATION_TARGET_OUTSIDE_WORKSPACE')
    for name in ['native','assets','textbook-baseline/sources']:
        shutil.copytree(ROOT/name,target/name)
    for f in (target/'native').glob('*.json'):
        # Only known native path strings are relocated. Scientific fields remain unchanged.
        raw=f.read_text(encoding='utf-8');f.write_text(raw.replace(ROOT.as_posix(),target.as_posix()),encoding='utf-8')
    denied=[];read_paths=[];original_book=ROOT.parent/'WPE_Textbook_Core2_R1_20261030'
    def guard(event,args):
        if event!='open' or not isinstance(args[0],str):return
        p=Path(args[0]).resolve()
        if p.is_relative_to(ROOT.resolve()) or p.is_relative_to(original_book.resolve()):
            denied.append(str(p));raise PermissionError('ORIGINAL_CANDIDATE_OR_BOOK_READ_DENIED:'+str(p))
        read_paths.append(str(p))
    active={'on':True}
    def audit(event,args):
        if active['on']:guard(event,args)
    sys.addaudithook(audit)
    try:
        pages,gaps,digest,advisories,waived=render_core.build_report(target/'native/manifest.json',held_to='REFERENCE')
        relocated={'case':'relocated inputs rebuild without primary candidate or original textbook reads',
            'pass':len(pages)==2 and len(gaps)==10 and not denied,'pages':list(pages),'depth_gaps':len(gaps),'denied_reads':denied,'observed_file_opens':len(read_paths),
            'runtime':'C:/CodeC/Grade9v3.5 native runtime still required; not a standalone toolchain distribution'}
    finally:active['on']=False
    results.append(relocated)
save(ROOT/'review/BUILD_CONTROLS.json',{'results':results,'pass':all(x['pass'] for x in results),'scope':'AUTHOR_NATIVE_BUILD_CONTROLS'})
for x in results:print(x['case'], 'PASS' if x['pass'] else 'FAIL')
raise SystemExit(0 if all(x['pass'] for x in results) else 1)
