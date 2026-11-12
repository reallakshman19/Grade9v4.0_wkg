"""Retain originals, map fixture explicitly, create relocatable native manifests."""
from pathlib import Path
import argparse, copy, hashlib, io, json, shutil, sys, zipfile
from native_adapter import adapt_fixture, digest, inspect_real_projection

ROOT = Path(__file__).resolve().parents[1]
BASELINE = Path(r'D:\CodeD\g9v3.5\chatgpt\output\WPE_Textbook_Core2_R1_20261030')
REPO = Path(r'C:\CodeC\Grade9v3.5')
DOWNLOADS = Path(r'C:\Users\reall\Downloads')
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def extract(z, out):
    if z.testzip(): raise ValueError('ZIP_CRC_FAILED')
    for n in z.namelist():
        dest = (out/n).resolve()
        if not dest.is_relative_to(out.resolve()): raise ValueError('ZIP_TRAVERSAL')
        if not n.endswith('/'):
            dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(z.read(n))

def retain():
    originals = ROOT/'originals'; originals.mkdir(exist_ok=True)
    pins = []
    for name, expected in [
        ('WPE_CORE2_R2_ENGINEERING_HANDOFF_PUBLIC_SAFE_20261030.zip','d2a24619b1def84bcc538615f6032a94f4161a5697067f60984280f1186a40e2'),
        ('WPE_CORE2_R2_OWNER_FULL_HANDOFF_20261030.zip','8609bcbdcb224abc37f7b72c50a15ecfb6abcacfbac5b585a40f164f900a6b1e')]:
        source = DOWNLOADS/name
        if sha(source) != expected: raise ValueError('HANDOFF_CHANGED:' + name)
        shutil.copy2(source, originals/name)
        pins.append({'original': str(source), 'retained': str((originals/name).relative_to(ROOT)), 'sha256': expected})
    extract(zipfile.ZipFile(originals/'WPE_CORE2_R2_ENGINEERING_HANDOFF_PUBLIC_SAFE_20261030.zip'), ROOT/'received-engineering')
    outer = zipfile.ZipFile(originals/'WPE_CORE2_R2_OWNER_FULL_HANDOFF_20261030.zip')
    raw = outer.read('original_immutable/WPE_CORE2_CODING_CANDIDATE_R1.zip')
    if hashlib.sha256(raw).hexdigest() != 'fca105392a2bcb579c9d382dc6d61afddb643af8b46d57d1fed2555a65f188a6': raise ValueError('R1_CHANGED')
    extract(zipfile.ZipFile(io.BytesIO(raw)), ROOT/'received-private-r1')
    for source in BASELINE.rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts:
            rel=source.relative_to(BASELINE); dst=ROOT/'textbook-baseline'/rel
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dst)
            pins.append({'original': str(source), 'retained': str(dst.relative_to(ROOT)), 'sha256': sha(source)})
    for rel in ['Shared/tools/render_core.py','Shared/tools/core2_v2.py','Shared/tools/owner_bank.py',
                'Shared/tools/product_manifest.py','Shared/tools/learner_metadata.py','Shared/tools/product_coverage.py',
                'Shared/tools/web_blueprint_contract.py','Shared/library/package.schema.json',
                'Shared/library/competitive-exam-bank.schema.json','Shared/web/interactive-page-blueprints.v1.json',
                'Physics/library/phy-work-energy-power.v1.json']:
        source=REPO/rel
        if not source.exists():
            if rel.endswith('competitive-exam-bank.schema.json'): continue
            raise FileNotFoundError(source)
        dst=ROOT/'dependencies'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dst)
        pins.append({'original':str(source),'retained':str(dst.relative_to(ROOT)),'sha256':sha(source)})
    save(ROOT/'review/PRESERVATION_PINS.json',pins)

def prepare():
    sys.path.insert(0,str(REPO))
    from Shared.tools import owner_bank
    base=ROOT/'textbook-baseline'
    package=read(base/'native/records.json')
    # Only relocate the existing representation assets. Canonical scientific fields stay identical.
    relocs=[]
    for rep in package['representations']:
        paths=[]
        for ref in rep.get('rendered_asset_refs',[]):
            src=Path(ref); local=base/src.relative_to(BASELINE)
            if not local.is_file(): raise ValueError('RETAINED_ASSET_MISSING:'+ref)
            paths.append(local.as_posix());relocs.append({'before':ref,'after':local.as_posix(),'sha256':sha(local)})
        rep['rendered_asset_refs']=paths
    package['title']='WPE · textbook and synthetic native integration — unreviewed'
    figure=ROOT/'assets/synthetic-directions.svg';figure.parent.mkdir(exist_ok=True)
    figure.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260" role="img" aria-labelledby="title desc"><title id="title">Stated force and displacement directions</title><desc id="desc">A trolley with an upward force arrow and a rightward displacement arrow. These are the directions already given in the synthetic question.</desc><rect x="115" y="150" width="110" height="45" rx="5" fill="#e3edf4" stroke="#254b65" stroke-width="3"/><circle cx="140" cy="207" r="10" fill="#254b65"/><circle cx="200" cy="207" r="10" fill="#254b65"/><path d="M170 145 V55 M160 68 L170 55 L180 68" fill="none" stroke="#167260" stroke-width="4"/><text x="195" y="90" font-family="sans-serif" font-size="20">stated force</text><path d="M220 175 H300 M286 165 L300 175 L286 185" fill="none" stroke="#254b65" stroke-width="4"/><text x="220" y="145" font-family="sans-serif" font-size="16">displacement</text></svg>''',encoding='utf-8')
    authored_rep=copy.deepcopy(package['representations'][0])
    authored_rep.update({'id':'REP-SYN-WPE-DIRECTIONS','kind':'AUTHORED_TECHNICAL_DIAGRAM','purpose':'Draw only the force and displacement directions stated in the supplied synthetic control.',
        'required_elements':['Vertical force arrow; horizontal displacement arrow; trolley.'],
        'read_order':['Compare the arrows with the directions already stated in the stem.'],
        'instance_constraints':['Technical control only; no examination source figure claim.'],
        'accessibility':['Descriptive SVG title and description.'],'rendered_asset_refs':[figure.as_posix()],
        'extensions':{'wpe:asset_provenance':'AUTHOR_ENGINEERING_CONTROL; not a source question figure','wpe:independent_visual_review':'NOT_RUN'}})
    package['representations'].append(authored_rep)
    save(ROOT/'native/records.json',package);save(ROOT/'review/ASSET_RELOCATION.json',relocs)
    fixture=read(ROOT/'received-engineering/fixtures/synthetic_question.json')
    qid=fixture['id']; mid=[qid+'-M'+str(i+1) for i in range(3)]
    factors=dict(zip(('concept_model_selection','representation_translation','reasoning_chain_length','algebra_computational_load','trap_exception_sensitivity'),(1,1,0,0,1)))
    binding={'id':qid,'source_digest':digest(fixture),'capability_ref':'CAP-WEP-WORK-DIRECTION','family_ref':'FAM-PHY-WEP-PRACTICE','representation_ref':'REP-SYN-WPE-DIRECTIONS',
        'reasoning_route':[{'id':mid[i],'kind':kind,'action':sentence,'why_valid':why,'inputs':[inp],'output':out,'source_ref':'SYNTHETIC-ENGINEERING-HANDOFF'}
            for i,(sentence,kind,why,inp,out) in enumerate(zip(fixture['answer']['reasoning'],['CONNECT','REPRESENT','VERIFY'],
                ['The supplied fixture explicitly assumes a constant force.','The fixture states perpendicular directions.','The force has no component in the displacement direction.'],
                ['The stated constant force and displacement.','Vertical force and horizontal displacement.','The perpendicular directions.'],
                ['Use the scalar product.','The force component along displacement is zero.','Zero work by this force.']))],
        'crux_move_ref':mid[1],
        'difficulty':{'band':'D2','score':3,'components':factors,'basis':'Author-only technical fixture proposal; no D3/D4 coverage or academic admission.',
            'component_evidence':dict(zip(factors,['Choose constant-force work.','Compare the stated directions.','No chained calculation.','No numerical calculation.','Distinguish one force from all forces.']))},
        'safe_orientation':[
            {'prompt':'What quantity does the question ask you to find?','text':'Keep your response about the work of the stated force.', 'learner_stage':'KEY_CONCEPT','support_kind':'CONNECT','reveals':'CONCEPT','supports_move_ref':mid[0]},
            {'prompt':'Which givens are stated explicitly?','text':'Reread the two stated directions before choosing an option.','learner_stage':'REPRESENTATION','support_kind':'REPRESENT','reveals':'CONCEPT','supports_move_ref':mid[1]}]}
    save(ROOT/'native/synthetic-binding.json',binding)
    q=adapt_fixture(fixture,binding,package)
    intake={'inputs':{'questions':[{'id':qid,'text':fixture['stem']}]}}
    intake['intake_digest']='sha256:'+digest(intake['inputs'])
    bank={'schema_version':owner_bank.SCHEMA_VERSION,'bank_id':'wpe-synthetic-native-r1','intake_digest':intake['intake_digest'],'questions':[q]}
    save(ROOT/'native/synthetic-intake.json',intake);save(ROOT/'native/synthetic-bank.json',bank)
    # Keep all eight textbook questions and their native bank bytes unchanged.
    shutil.copy2(base/'native/bank.json',ROOT/'native/textbook-bank.json')
    shutil.copy2(base/'native/intake.json',ROOT/'native/textbook-intake.json')
    all_ids=[row['id'] for row in read(ROOT/'native/textbook-bank.json')['questions']]+[qid]
    m={'schema':'product-manifest/v1','product_id':'WPE-CORE2-NATIVE-INTEGRATION-R1','subject':'Physics',
       'title':'WPE · private native integration draft', 'home_href':'../index.html','question_bank_href':'../review.html',
       'package_refs':[(ROOT/'native/records.json').as_posix()],
       'bank_refs':[(ROOT/'native/textbook-bank.json').as_posix(),(ROOT/'native/synthetic-bank.json').as_posix()],
       'output_roles':['CORE2'],'selection':{'microtopics':[],'core2':all_ids,'core2a':[],'core2b':[]}}
    save(ROOT/'native/manifest.json',m)
    sm=copy.deepcopy(m);sm['product_id']='WPE-SYNTHETIC-NATIVE-CONTROL-R1';sm['bank_refs']=[(ROOT/'native/synthetic-bank.json').as_posix()];sm['selection']['core2']=[qid]
    save(ROOT/'native/synthetic-manifest.json',sm)
    pre=read(ROOT/'received-private-r1/outputs/REAL_R1_SELECTION_PREFLIGHT.json')
    from core2_engine import evaluate_selection
    gate=evaluate_selection(pre['records'])
    save(ROOT/'review/EXAM_READINESS.json',{'status':'HOLD','target':21,'conditional_leads':len(pre['records']),
        'vacancies':7,'admitted':0,'engineering_metadata_gate':gate,
        'native_readiness':[inspect_real_projection(r) for r in pre['records']],
        'legacy_selection':pre['legacy_selection'],'review':'AUTHOR_TECHNICAL_ONLY; distinct academic/QA NOT_RUN'})
    for rel in ['css/modern-learner.css','css/tablet-12-7.css','js/display-controls.js','js/site-header.js']:
        dst=ROOT/rel;dst.parent.mkdir(exist_ok=True);shutil.copy2(REPO/'public'/rel,dst)
    print('Prepared 8 unchanged textbook bank questions + 1 explicit synthetic native control; 14 examination records held.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--retain',action='store_true');a=ap.parse_args()
    if a.retain: retain()
    sys.path.insert(0,str(ROOT/'received-engineering/src'))
    prepare()
