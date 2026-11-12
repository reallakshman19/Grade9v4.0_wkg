"""Offline *technical fixture* viewer. Not the governed Grade9V3 render_core.py.

Source answers are embedded in a static script for post-attempt UI rendering:
this is an interface lock, not a security boundary against source inspection.
Never use it for a protected learner deployment without a trusted answer service.
"""
from __future__ import annotations
import json
from html import escape
from pathlib import Path
from core2_engine import _source_question

STYLE = r'''
:root {font:16px/1.5 system-ui,Arial,sans-serif;color:#192535;background:#f5f7f9}
* {box-sizing:border-box} body{margin:0} main{max-width:1150px;margin:auto;padding:20px}
header{background:#11263e;color:white;padding:20px 28px;border-radius:14px;margin-bottom:16px}
h1{font-size:1.55rem;margin:3px 0} h2{font-size:1.15rem;margin-top:0}
.sub{color:#e1e8ee;font-size:.9rem} .layout{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(280px,1fr);gap:18px}
.panel{background:white;border:1px solid #dce2e9;border-radius:14px;padding:22px;margin-bottom:15px}
.kicker{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:#51677d;font-weight:700}
#stem{font-size:1.08rem;white-space:pre-wrap} .option{display:block;padding:9px 10px;border:1px solid #c9d5df;margin:8px 0;border-radius:9px}
.option:has(input:focus-visible){outline:3px solid #1c628f}button{font:inherit;padding:9px 14px;border-radius:9px;border:1px solid #54748f;background:#fff;cursor:pointer}
button.primary{background:#174b78;color:white;border-color:#174b78}button:disabled{opacity:.45;cursor:not-allowed}
button:focus-visible, input:focus-visible{outline:3px solid #f09c3e;outline-offset:2px}
small,.muted{color:#586c7d}.hint{padding:11px 13px;background:#f3f7fa;border-left:4px solid #366e95;border-radius:5px;margin:9px 0;white-space:pre-wrap}
#answer-panel[hidden],#solution[hidden],#next-hint[hidden]{display:none}#result{margin-top:10px;font-weight:650}
#figure-list{padding-left:18px} #answer-entry{width:100%;padding:10px;border:1px solid #9bafbf;border-radius:8px}
[role=status]{min-height:1.5em}.tag{display:inline-block;font-size:.7rem;background:#e6eef5;padding:2px 6px;border-radius:4px;margin-right:6px}
@media(max-width:760px){main{padding:10px}.layout{display:block}.panel{padding:16px}}
@media print {header{color:black;background:transparent;border-bottom:1px solid #aaa} button,.option input,#answer-panel,#solution,#result{display:none!important}main{max-width:100%}.panel{break-inside:avoid}}
'''
JS = r'''
'use strict';
const q = JSON.parse(document.getElementById('record-data').textContent);
const $ = id => document.getElementById(id);
const make = (tag, txt, cls) => {const node = document.createElement(tag); if(txt!==undefined) node.textContent=txt; if(cls) node.className=cls; return node};
const attempt = {committed:false, hintsSeen:0};
function init(){
  $('stem').textContent=q.stem;
  $('qid').textContent=q.original_identifier;
  $('type').textContent=q.extensions['wpe:response_type'];
  $('figures').hidden = !(q.figure_refs||[]).length;
  const fl=$('figure-list'); (q.figure_refs||[]).forEach(ref=>fl.appendChild(make('li',String(ref))));
  const cond=$('conditions');(q.conditions||[]).forEach(c=>cond.appendChild(make('li',c)));
  const kind=q.extensions['wpe:response_type'];
  const group=$('response-area');
  if(['SINGLE_CHOICE','MULTIPLE_CHOICE'].includes(kind)){
    q.options.forEach(opt=>{const label=make('label',undefined,'option');const el=make('input');el.type=kind==='SINGLE_CHOICE'?'radio':'checkbox';el.name='answer';el.value=opt.id;label.appendChild(el);label.appendChild(document.createTextNode(' '+opt.id+' — '+opt.text));group.appendChild(label)});
  }else {const inp=make('input');inp.id='answer-entry';inp.type='text';inp.autocomplete='off';inp.setAttribute('aria-label',kind==='NUMERIC'?'Your numeric answer':'Your written answer');group.appendChild(inp)}
  $('commit').addEventListener('click',commit);$('next-hint').addEventListener('click',hint);
  $('next-hint').hidden = !available.length;
  $('hint-count').textContent=available.length?`0 / ${available.length} hints opened`:'No pre-attempt hints available';
}
// Source hints and authored scaffolds are separate custody lanes.
const available = [...(q.hints||[]).filter(h=>typeof h==='object' && h.availability==='PRE_ATTEMPT_SAFE' && h.reveals!=='ANSWER').map(h=>({text:h.text,lane:'SOURCE HINT'})),
  ...(q.scaffolds||[]).filter(h=>h.availability==='PRE_ATTEMPT_SAFE' && h.reveals!=='ANSWER' && !h.completes_protected_move).map(h=>({text:h.text,lane:'AUTHORED SUPPORT'}))];
function hint(){if(attempt.hintsSeen>=available.length)return;
  const h=available[attempt.hintsSeen++];const p=make('div',undefined,'hint');p.appendChild(make('span',h.lane,'tag'));p.appendChild(make('span',h.text));$('hint-list').appendChild(p);
  $('hint-count').textContent=`${attempt.hintsSeen} / ${available.length} hints opened`;
  $('next-hint').disabled=attempt.hintsSeen===available.length;
}
function answerValue(){const kind=q.extensions['wpe:response_type'];
 if(['SINGLE_CHOICE','MULTIPLE_CHOICE'].includes(kind))return [...document.querySelectorAll('input[name=answer]:checked')].map(x=>x.value);
 return $('answer-entry').value.trim();}
function grade(v){const p=q.extensions['wpe:grading_policy'];
 if(p.type==='SINGLE_CHOICE' || p.type==='MULTIPLE_CHOICE'){
   const a=[...v].sort(),b=[...p.correct_ids].sort();return a.length===b.length && a.every((x,i)=>x===b[i])?'CORRECT':'INCORRECT';
 }
 if(p.type==='NUMERIC'){const n=Number(v);return v!==''&&Number.isFinite(n)&&Math.abs(n-p.exact_value)<=p.tolerance?'CORRECT':'INCORRECT';}
 return 'NEEDS_HUMAN_REVIEW';
}
function commit(){if(attempt.committed)return;const v=answerValue();if(Array.isArray(v)?!v.length:!v){$('result').textContent='Choose or enter an answer before committing.';return;}
 attempt.committed=true;document.querySelectorAll('#response-area input').forEach(x=>x.disabled=true);$('commit').disabled=true;
 const verdict=grade(v); $('result').textContent=verdict==='NEEDS_HUMAN_REVIEW'?'Attempt saved. Written responses require human assessment.':`Attempt recorded — ${verdict.toLowerCase()}.`;
 $('answer-panel').hidden=false;const solution=q.answer||{};
 $('answer-summary').textContent=solution.summary||'No solution summary supplied';
 const list=$('reasoning');(solution.reasoning||[]).forEach(move=>list.appendChild(make('li',typeof move==='string'?move:JSON.stringify(move))));
 $('check').textContent=solution.check||'';
 $('solution').hidden=false;$('solution').focus();
}
document.addEventListener('DOMContentLoaded',init);
'''


def render_fixture(question: dict, *, technical_fixture: bool = False) -> str:
    if not technical_fixture:
        raise ValueError('UNREVIEWED_QUESTIONS_CANNOT_RENDER: governed renderer and academic gate required')
    errors = _source_question(question)
    if errors: raise ValueError('INVALID_QUESTION:'+','.join(errors))
    if not question.get('extensions',{}).get('wpe:synthetic_technical_fixture'):
        raise ValueError('SYNTHETIC_FIXTURE_FLAG_REQUIRED')
    if not question.get('extensions',{}).get('wpe:grading_policy'):
        raise ValueError('GRADING_POLICY_REQUIRED')
    payload=json.dumps(question,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WPE Core2 — synthetic engineering control</title><style>{STYLE}</style></head>
<body><main><header><div class="sub">CORE2 · INTERNAL ENGINEERING CONTROL — NOT AN EXAM ORIGINAL</div><h1>WPE · Attempt-first Challenge</h1><div class="sub">Unadmitted demo data · source/academic/Owner acceptance NOT RUN</div></header>
<div class="layout"><section><div class="panel"><p class="kicker">Question <span id="qid"></span> · <span id="type"></span></p><h2>Try before seeing the solution</h2><p id="stem"></p><ul id="conditions"></ul><div id="figures"><strong>Source figure references (custody only)</strong><ul id="figure-list"></ul></div><div id="response-area" aria-label="Your answer"></div><button id="commit" class="primary" type="button">Commit attempt</button><p id="result" role="status" aria-live="polite"></p></div>
<div class="panel" id="solution" hidden tabindex="-1"><p class="kicker">After attempt</p><h2>Explanation</h2><div id="answer-panel" hidden><p id="answer-summary"></p><ol id="reasoning"></ol><p id="check"></p></div></div></section>
<aside><div class="panel"><p class="kicker">Progressive support</p><h2>Hint ladder</h2><p class="muted">One hint at a time. Source hints and authored help remain labeled separately.</p><div id="hint-list" aria-live="polite"></div><p id="hint-count" role="status"></p><button id="next-hint" type="button">Reveal next hint</button></div>
<div class="panel"><p class="kicker">Quality status</p><p><strong>Technical fixture only.</strong> No certified source, independent Physics review, or learner release.</p></div></aside></div></main>
<script id="record-data" type="application/json">{payload}</script><script>{JS}</script></body></html>'''


def write_fixture(question: dict, target: str|Path) -> None:
    Path(target).write_text(render_fixture(question,technical_fixture=True),encoding='utf8')
