"""Lossless-link candidate projection from R1 to the NEW engineering gate.

Never asserts source authenticity, reviewer independence, approved adapter, or
promotion. R1 proposals remain exposed; all unverified fields are null/held.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from core2_engine import canonical_digest,evaluate_selection

MAP={'single_correct_mcq':'SINGLE_CHOICE','multiple_correct_mcq':'MULTIPLE_CHOICE','numerical':'NUMERIC', 'numeric':'NUMERIC'}

def project(r):
    rawopts = r.get('options') or []
    opts=[]
    for i,o in enumerate(rawopts):
        if isinstance(o,dict):opts.append({'id':str(o.get('id',i+1)),'text':str(o.get('text',''))})
        else:
            m=re.match(r'^\s*([A-Za-z0-9]+)\s*[:.)-]\s*(.*)',str(o),re.S)
            opts.append({'id':m.group(1) if m else str(i+1),'text':m.group(2) if m else str(o)})
    tp=MAP.get((r.get('question_type') or '').lower(),'TEXT')
    alias=r.get('canonical_counting_id') or r['id']
    scores=(r.get('sl2_proposal') or {}).get('scores') or {}
    c=r.get('custody') or {}
    q={'id':alias,'original_identifier':r['id'],'origin':'EXAM_ORIGINAL',
       'stem':r.get('exact_stem',''),'options':opts,'subparts':[], 'conditions':[],
       'figure_refs':[x.get('url','UNBOUND') for x in c.get('unbound_figure_refs',[])],
       'hints':[],'scaffolds':[], 'answer':{},
       'extensions':{'wpe:response_type':tp,'wpe:r1_record_id':r['id'],'wpe:review_status':'EXPOSED_UNREVIEWED'}}
    return {'canonical_id':alias, 'duplicate_of':(r.get('sl1_proposal') or {}).get('duplicate_of'),
       'origin':'EXAM_ORIGINAL_UPSTREAM_UNVERIFIED','source_role':(r.get('placement') or {}).get('role'),
       'question':q,'source':{'original_r1_custody':c,'question_digest':canonical_digest({k:q.get(k) for k in ('stem','subparts','conditions','original_identifier')}),
       'options_digest':canonical_digest(opts),'figure_digests':[], 'required_figures_bound':False,
       'official_paper':None,'official_key':None, 'answer_versions':{'inherited_claim_digest':c.get('answer_digest'),'official_claim_digest':None,'reconciliation':'OPEN'}},
       'curriculum':{'semantic_cell_resolved':False,'capability_ref':None,'microtopic_ref':None},
       'assessment':{'factors':scores,'total':(r.get('sl2_proposal') or {}).get('total'),
        'band':(r.get('sl2_proposal') or {}).get('band'),'primary_operation':(r.get('sl2_proposal') or {}).get('operation'),
        'factor_evidence':{x.get('factor'):x.get('evidence') for x in (r.get('sl2_proposal') or {}).get('factor_evidence',[])},
        'decisive_move_evidence':(r.get('sl2_proposal') or {}).get('crux'),'competing_operations':[ (r.get('sl2_proposal') or {}).get('alternative') ],
        'source_stage':'AUTHOR_EXPOSED_HYPOTHESIS'},
       'governance':{'reviewer_exposure_disclosed':None,'qrt_adjudication':'HOLD'},
       'grading_policy':{},'prior_exposure':True,'r1_preserved_proposals':{'sl1':r.get('sl1_proposal'),'sl2':r.get('sl2_proposal')},
       'source_record_id':r['id']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--dispositions',required=True);p.add_argument('--selection',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    d=json.loads(Path(a.dispositions).read_text());s=json.loads(Path(a.selection).read_text())
    by_id={r['id']:r for r in d['records']}
    selected=[]
    for place in s['places']:
        if place.get('candidate_id'):
            selected.append(project(by_id[place['candidate_id']]))
    out={'schema':'wpe-core2-r1-bridge/v1','scope':'UNVERIFIED_PROPOSALS_ONLY','records':selected,
         'legacy_selection':s,'gate':evaluate_selection(selected)}
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('HOLD',len(selected),'prior exposures preserved')

if __name__=='__main__':main()
