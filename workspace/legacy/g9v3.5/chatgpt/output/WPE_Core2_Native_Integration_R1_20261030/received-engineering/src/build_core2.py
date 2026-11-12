"""CLI: fail-closed real WPE package compiler and synthetic UI generation.

Only source-verified/adjudicated admissions can enter real package. This CLI
cannot authenticate uploaded review claims; human verifier signs them outside.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from core2_engine import evaluate_selection, make_derived_package
from learner_render import write_fixture


def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='mode',required=True)
    g=sub.add_parser('gate');g.add_argument('--admissions',required=True);g.add_argument('--out',required=True)
    b=sub.add_parser('package');b.add_argument('--admissions',required=True);b.add_argument('--library',required=True);b.add_argument('--manifest',required=True);b.add_argument('--bank-meta',required=True);b.add_argument('--outdir',required=True);b.add_argument('--assets-root')
    v=sub.add_parser('fixture');v.add_argument('--question',required=True);v.add_argument('--out',required=True)
    a=ap.parse_args()
    if a.mode=='fixture':
        write_fixture(load(a.question),a.out);print('TECHNICAL_FIXTURE_ONLY',a.out);return 0
    admissions=load(a.admissions);records=admissions['records'] if isinstance(admissions,dict) else admissions
    if a.mode=='gate':
        result=evaluate_selection(records);dump(a.out,result);print(result['state']);return 0 if result['state']=='BUILD_ELIGIBLE_METADATA_ONLY' else 2
    pkg=make_derived_package(records,load(a.library),load(a.manifest),load(a.bank_meta),assets_root=a.assets_root)
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    for name in ('manifest.json','bank.json','records.json','validation'):
        fn=name if name.endswith('.json') else name+'.json';dump(out/fn,pkg[name])
    digests={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.json')}
    dump(out/'BUILD_HASHES.json',{'schema':'wpe-core2-build-digests/v1','status':'CANDIDATE_NOT_RELEASED','sha256':digests})
    print('BUILD_ELIGIBLE_METADATA_ONLY / OWNER_RELEASE_NOT_RUN');return 0

if __name__=='__main__':raise SystemExit(main())
