"""All examples are synthetic; no exam question or private handoff bytes."""
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from private_reader_integration import build, canonical_json, sha, OUTPUT_MARKER

SVG = '<svg xmlns="http://www.w3.org/2000/svg"><circle cx="5" cy="5" r="4"/></svg>'

# Synthetic browser runtime only. This fixture is NOT the private R2 reader.
HTML = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Synthetic test reader</title></head>
<body><header><h1>Synthetic source page</h1></header><nav id="navlist"></nav><main id="question-root"></main>
<script id="wpe-data" type="application/json">{}</script>
<script>
const data=JSON.parse(document.getElementById('wpe-data').textContent);
function questionKey(q){return [q.topic,q.source_id,q.id].map(encodeURIComponent).join('::');}
const nav=document.getElementById('navlist'),root=document.getElementById('question-root');
const attempts={};
function openQuestion(q){
 root.textContent='';
 const h=document.createElement('h2');h.textContent=q.stem;root.append(h);
 const missing=q.source_figures?.filter(f=>!data.assets?.[f])||[];
 if(missing.length){const p=document.createElement('p');p.dataset.figureHold='true';p.textContent='Required diagram unavailable';root.append(p);return;}
 for(const fig of q.source_figures||[]){const p=document.createElement('div');p.innerHTML=data.assets[fig];root.append(p);}
 const key=questionKey(q);
 const btn=document.createElement('button');btn.id='commit-btn';btn.textContent='Record local practice';btn.disabled=!!attempts[key];
 btn.onclick=()=>{attempts[key]=true;btn.disabled=true};root.append(btn);
}
for(const q of data.questions){
 const btn=document.createElement('button');btn.className='item';btn.dataset.id=questionKey(q);
 btn.textContent=questionKey(q);btn.onclick=()=>openQuestion(q);nav.append(btn);
}
openQuestion(data.questions[0]);
</script></body></html>'''


def fixture(tmp_path):
    root=tmp_path/'private';root.mkdir()
    aggregate=[];modules=[]
    for slug, topic, figure in [('alpha','OPTICS','drawn.svg'), ('beta','ELECTROSTATICS','missing.svg')]:
        items=[{'topic':topic,'source_id':'SAME','id':'Q1', 'stem':f'Synthetic {slug} one', 'source_figures':[figure]},
               {'topic':topic,'source_id':'SAME','id':'Q2', 'stem':f'Synthetic {slug} two', 'source_figures':[]}]
        aggregate.extend(items)
        data={'questions':[{k:v for k,v in q.items() if not (slug=='alpha' and k=='topic')} for q in items]}
        if slug=='alpha':data['assets']={'drawn.svg':SVG}
        path=f'modules/{slug}/question-status.html';target=root/path;target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(HTML.replace('{}',canonical_json(data),1),encoding='utf-8')
        modules.append({'slug':slug,'topic':topic,'path':path,'sha256':sha(target.read_bytes()),'count':2})
    agg_path=root/'preview/question-status.html';agg_path.parent.mkdir()
    agg_path.write_text(HTML.replace('{}',canonical_json({'questions':aggregate}),1),encoding='utf-8')
    manifest={'version':1,'review_only':True,
              'aggregate':{'path':'preview/question-status.html','sha256':sha(agg_path.read_bytes()),'count':4},
              'modules':modules,'expected_missing_figures':1}
    manifest_path=tmp_path/'private_manifest.json';manifest_path.write_text(canonical_json(manifest)+'\n')
    return root,manifest_path,tmp_path/'output'


def update_manifest_for_file(root,mpath,rel):
    data=json.loads(mpath.read_text())
    spec=next(x for x in [data['aggregate'], *data['modules']] if x['path']==rel)
    spec['sha256']=sha((root/rel).read_bytes())
    mpath.write_text(canonical_json(data)+'\n')


def test_non_destructive_deterministic_and_figure_recovery(tmp_path):
    root,mpath,out=fixture(tmp_path)
    before={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    first=build(root,out,mpath)
    assert first['record_count']==4 and first['missing_figures']==1
    assert first['figure_refs']==2 and first['module_count']==2
    assert (out/OUTPUT_MARKER).is_file()
    page=(out/'preview/question-status.html').read_text()
    assert 'drawn.svg' in page and '<circle' in page
    assert 'NOT FOR PUBLICATION' in (out/'index.html').read_text()
    first_bytes={str(p.relative_to(out)):sha(p.read_bytes()) for p in out.rglob('*') if p.is_file()}
    assert build(root,out,mpath)==first
    assert first_bytes=={str(p.relative_to(out)):sha(p.read_bytes()) for p in out.rglob('*') if p.is_file()}
    assert before=={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}


def test_pinned_input_mutation_fails_without_output(tmp_path):
    root,mpath,out=fixture(tmp_path)
    with (root/'preview/question-status.html').open('a') as f:f.write('CHANGED')
    with pytest.raises(ValueError,match='PINNED_INPUT_CHANGED'):build(root,out,mpath)
    assert not out.exists()


def test_mismatched_record_rejected_by_semantic_checker(tmp_path):
    root,mpath,out=fixture(tmp_path)
    p=root/'modules/beta/question-status.html'
    p.write_text(p.read_text().replace('Synthetic beta one','Incorrect candidate'),encoding='utf-8')
    update_manifest_for_file(root,mpath,'modules/beta/question-status.html')
    with pytest.raises(ValueError,match='SOURCE_TO_AGGREGATE_MISMATCH'):build(root,out,mpath)
    assert not out.exists()


def test_unsafe_svg_rejected_by_target_checker(tmp_path):
    root,mpath,out=fixture(tmp_path)
    p=root/'modules/alpha/question-status.html'
    p.write_text(p.read_text().replace('<circle cx=\\"5\\" cy=\\"5\\" r=\\"4\\"/>','<foreignObject/>'),encoding='utf-8')
    update_manifest_for_file(root,mpath,'modules/alpha/question-status.html')
    with pytest.raises(ValueError,match='UNSAFE_CANDIDATE_ASSET'):build(root,out,mpath)


def test_asset_collision_rejected(tmp_path):
    root,mpath,out=fixture(tmp_path)
    p=root/'preview/question-status.html'
    embedded=json.loads(p.read_text().split('type="application/json">')[1].split('</script>')[0])
    embedded['assets']={'drawn.svg':'<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>'}
    p.write_text(HTML.replace('{}',canonical_json(embedded),1))
    update_manifest_for_file(root,mpath,'preview/question-status.html')
    with pytest.raises(ValueError,match='ASSET_COLLISION'):build(root,out,mpath)


def test_required_figure_count_rejects_new_missing_media(tmp_path):
    root,mpath,out=fixture(tmp_path)
    m=json.loads(mpath.read_text());m['expected_missing_figures']=0;mpath.write_text(canonical_json(m)+'\n')
    with pytest.raises(ValueError,match='FIGURE_INVENTORY_CHANGED'):build(root,out,mpath)


def test_output_not_inside_input_and_not_unowned(tmp_path):
    root,mpath,out=fixture(tmp_path)
    with pytest.raises(ValueError,match='UNSAFE_OUTPUT_PATH'):build(root,root/'dist',mpath)
    out.mkdir();(out/'precious.txt').write_text('DO NOT DELETE')
    with pytest.raises(ValueError,match='OUTPUT_NOT_OWNED_BY_BUILDER'):build(root,out,mpath)
    assert (out/'precious.txt').read_text()=='DO NOT DELETE'


def test_bad_paths_rejected(tmp_path):
    root,mpath,out=fixture(tmp_path)
    m=json.loads(mpath.read_text());m['modules'][0]['path']='../outside.html';mpath.write_text(canonical_json(m)+'\n')
    with pytest.raises(ValueError,match='UNSAFE_INPUT_PATH'):build(root,out,mpath)


def test_public_release_fails_before_candidate_read(tmp_path):
    root,mpath,out=fixture(tmp_path)
    with pytest.raises(ValueError,match='PUBLIC_RELEASE_FORBIDDEN'):build(root,out,mpath,publish=True)
    assert not out.exists()


def test_synthetic_data_is_not_official_or_academic_evidence(tmp_path):
    root,mpath,out=fixture(tmp_path)
    result=build(root,out,mpath)
    assert result['academic_approval']=='HOLD'
    assert result['source_authenticity']=='UNKNOWN_SOURCE'
    assert result['release_authority']=='HOLD'
