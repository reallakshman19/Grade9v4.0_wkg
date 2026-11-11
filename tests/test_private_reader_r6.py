"""Public-safe R6 synthetic controls. No owner handoff, exam content or figure bytes."""
from __future__ import annotations
import json
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from private_reader_r6 import canonical, sha, revise, question_key, transform, upgrade_site

SYNTHETIC = [
    {'topic':'ALPHA','id':'DUPLICATE-ID','source_id':'ONE','stem':'Synthetic energy problem A',
     'options':['Alpha choice','Beta choice'],'answer':'A', 'source_figures':[],
     'hints':[{'prompt':'Synthetic hint','text':'Synthetic advice'}]},
    {'topic':'BETA','id':'DUPLICATE-ID','source_id':'TWO','stem':'Synthetic energy problem B',
     'options':['First response','Second response'],'answer':'B','source_figures':[],
     'hints':[{'prompt':'Synthetic hint','text':'Synthetic advice'}]},
]

# This test reader is independently authored synthetic scaffolding. The labels,
# HTML and data are test-only; the actual private candidate is not included.
PAGE = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>R6 Synthetic</title></head>
<body><nav id="navlist"></nav><main id="question-root"></main>
<script id="wpe-data" type="application/json">__JSON__</script>
<script>
const data=JSON.parse(document.getElementById('wpe-data').textContent), qs=data.questions;
const nodes={list:document.getElementById('navlist'),root:document.getElementById('question-root')};
function questionKey(q){return [q.topic || 'UNSCOPED',q.source_id || '',q.id || ''].map(encodeURIComponent).join('::');}
const params=new URLSearchParams(window.location.search);
const requested = params.get('question');
  const chosen = qs.find(q => questionKey(q) === requested) ||
      qs.find(q => q.source_id === requested) ||
      qs.find(q => q.id === requested) || qs[0];
  let active = chosen ? questionKey(chosen) : '';

  const attempts = new Map();
let filtered=[...qs];
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
function renderNav(){
 nodes.list.innerHTML=filtered.map(q=>'<button class="item" data-id="'+esc(questionKey(q))+'">'+esc(q.topic)+'</button>').join('');
 nodes.list.querySelectorAll('.item').forEach(btn=>{
  btn.addEventListener('click',()=>{
        active = btn.dataset.id;
        const url=new URL(window.location);
        url.searchParams.set('question',active);
        window.history.replaceState({},'',url);
        renderNav();renderQuestion();
  });
 });
}
function filters(){
    if (!filtered.some(q => questionKey(q) === active) && filtered.length > 0) {
      active = questionKey(filtered[0]);
    }
 renderNav();renderQuestion();
}
function solutionMarkup(q){return '<div class="solution">Synthetic solution</div>';}
function renderQuestion(){
 const q=qs.find(item=>questionKey(item)===active);
    if (!q) {
      nodes.root.innerHTML = '<p class="subtitle">No matching question found.</p>';
      return;
    }
    const st = attempts.get(questionKey(q)) || { selected: null, committed: false, revealed: false };
    nodes.root.innerHTML =
      '<h2>'+esc(q.stem)+'</h2>'+
      '<label><input type="radio" name="answer-option" value="A" '+(st.selected==='A'?'checked ':'')+(st.committed?'disabled':'')+'>A</label>'+
      '<label><input type="radio" name="answer-option" value="B" '+(st.selected==='B'?'checked ':'')+(st.committed?'disabled':'')+'>B</label>'+
      '<button id="commit-btn" type="button" '+(st.committed?'disabled':'')+'>Commit</button>'+
      '<span id="commit-note" class="live-note">' + (st.committed ? 'Attempt committed on this page only; reloading clears it.' : 'Select an option to enable commitment.') + '</span>' +
      '<button id="reveal-btn" type="button" '+(!st.committed || st.revealed?'disabled':'')+'>Reveal</button>'+
      '<div id="solution-container">'+(st.revealed?solutionMarkup(q):'')+'</div>'+
      '<details class="hint"><summary>Hint</summary><p>Synthetic hint</p></details>';
    const commitBtn=nodes.root.querySelector('#commit-btn');
    const revealBtn=nodes.root.querySelector('#reveal-btn');
    const commitNote=nodes.root.querySelector('#commit-note');
    const radioInputs=nodes.root.querySelectorAll('input[name="answer-option"]');
    radioInputs.forEach(radio=>radio.addEventListener('change',()=>{
      let cur = attempts.get(questionKey(q)) || { selected: null, committed: false, revealed: false };
      cur.selected=radio.value;
      attempts.set(questionKey(q), cur);
    }));
    commitBtn.addEventListener('click',()=>{
      const cur = attempts.get(questionKey(q));
      if (!cur || !cur.selected) {commitNote.textContent='Please choose an option';return;}
      cur.committed = true;
      attempts.set(questionKey(q), cur);
      commitBtn.disabled=true;
      revealBtn.disabled=false;
      radioInputs.forEach(r=>r.disabled=true);
      commitNote.textContent = 'Attempt committed. You may now reveal the worked solution.';
    });
    revealBtn.addEventListener('click',()=>{
      const cur = attempts.get(questionKey(q));
      if (!cur || !cur.committed) return;
      cur.revealed=true;
      attempts.set(questionKey(q), cur);
      nodes.root.querySelector('#solution-container').innerHTML=solutionMarkup(q);
      revealBtn.disabled=true;
    });
    const hintEls=[...nodes.root.querySelectorAll('.hint')];
    hintEls.forEach((el, idx)=>{
      el.addEventListener('toggle', () => {
        if (el.open && idx > 0 && !hintEls[idx - 1].open) {
          el.open = false;
        }
      });
    });
}
filters();
</script></body></html>'''


def fixture(tmp: Path):
    src=tmp/'private-synthetic';src.mkdir(parents=True)
    (src/'preview').mkdir()
    payload=canonical({'questions':SYNTHETIC,'assets':{}})
    (src/'preview/question-status.html').write_text(PAGE.replace('__JSON__',payload),encoding='utf-8')
    (src/'index.html').write_text('<!doctype html><title>Synthetic</title>',encoding='utf-8')
    (src/'.GRADE9_PRIVATE_REVIEW_ONLY').write_text('PRIVATE SYNTHETIC\n')
    report={'schema_version':'private-review.v1','purpose':'REVIEW_ONLY_NOT_FOR_PUBLICATION',
            'release_authority':'HOLD','academic_approval':'HOLD','record_count':2,
            'module_count':0,'figure_refs':0,'missing_figures':0,
            'source_question_digest':sha(canonical(SYNTHETIC).encode('utf-8')),
            'output_files':{x:sha((src/x).read_bytes()) for x in ('index.html','preview/question-status.html')}}
    (src/'PRIVATE_REVIEW_MANIFEST.json').write_text(canonical(report)+'\n')
    return src,tmp/'output'


def test_synthetic_revision_mutations():
    q=SYNTHETIC[0]
    a=revise(q,{})
    assert revise({**q,'answer':'B'}, {})!=a
    assert revise({**q,'options':['Changed',*q['options'][1:]]}, {})!=a
    assert revise({**q,'stem':q['stem']+' revised'}, {})!=a
    assert revise({**q,'source_figures':['new.svg']},{})!=a
    assert revise({**q,'source_figures':['new.svg']},{'new.svg':'<svg/>'})!=a
    assert question_key(SYNTHETIC[0])!=question_key(SYNTHETIC[1])


def test_synthetic_transform_source_preserved(tmp_path):
    src,out=fixture(tmp_path)
    old=json.loads((src/'PRIVATE_REVIEW_MANIFEST.json').read_text())
    after=upgrade_site(src,out)
    assert after['source_question_digest']==old['source_question_digest']
    assert after['runtime_profile']=='r6-revision-scoped-local-attempts'
    assert after['academic_approval']=='HOLD'
    page=(out/'preview/question-status.html').read_text()
    assert 'id="g9-r6-review-store"' in page
    data=json.loads(page.split('<script id="wpe-data" type="application/json">')[1].split('</script>')[0])
    assert data['questions']==SYNTHETIC
    assert len(data['review_revisions'])==2
    assert 'Ambiguous legacy question link' in page
    assert 'NOT SAVED' in page
    assert 'helpEvents' in page
    for rel,digest in after['output_files'].items():assert sha((out/rel).read_bytes())==digest


def test_reject_tampered_generated_source_and_unlisted_file(tmp_path):
    src,out=fixture(tmp_path)
    (src/'preview/question-status.html').write_text((src/'preview/question-status.html').read_text()+'tampered')
    with pytest.raises(ValueError,match='R6_INPUT_PIN_MISMATCH'):upgrade_site(src,out)
    assert not out.exists()
    src2,out2=fixture(tmp_path/'next')
    (src2/'unlisted.txt').write_text('not approved')
    with pytest.raises(ValueError,match='R6_UNACCOUNTED_OUTPUT_FILES'):upgrade_site(src2,out2)


def test_reject_symlink_and_public_authority_spoof(tmp_path):
    src,out=fixture(tmp_path)
    try:
        (src/'external').symlink_to(src/'index.html')
    except (OSError,NotImplementedError):
        pytest.skip('symlink not available')
    with pytest.raises(ValueError,match='R6_SYMLINK_REJECTED'):upgrade_site(src,out)
    (src/'external').unlink()
    manifest=src/'PRIVATE_REVIEW_MANIFEST.json'
    m=json.loads(manifest.read_text());m['release_authority']='APPROVED';manifest.write_text(canonical(m))
    with pytest.raises(ValueError,match='R6_RELEASE_AUTHORITY'):upgrade_site(src,out)


def test_refuse_reapply_to_its_own_generated_page(tmp_path):
    src,out=fixture(tmp_path);upgrade_site(src,out)
    with pytest.raises(ValueError,match='R6_MARKER_OR_DUPLICATE'):
        transform((out/'preview/question-status.html').read_text())
    with pytest.raises(ValueError,match='R6_UNSAFE_OUTPUT'):
        upgrade_site(src,out)