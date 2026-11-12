"""Fail-closed PRIVATE 50-record Core2 handoff hardening, no academic promotion.

Processes a recipient-pinned owner-provided ZIP locally. Never commit/publish
private output. Does not change original embedded question records, source papers,
figures, solution data, claimed keys, difficulty or QRT labels. Repairs only the
reader runtime and supplies an independent status/custody receipt.
"""
from __future__ import annotations
import argparse, hashlib, json, re, stat, zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

MARKER='<script id="wpe-data" type="application/json">'
ENGINE_START="  const qs = data.questions;"
READER_END='</script>'
QRT_FACTORS=('concept_model_selection','representation_translation','reasoning_chain_length',
             'algebra_computational_load','trap_exception_sensitivity')

def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def question_key(q):
    return '::'.join(str(q.get(k) or 'UNSPECIFIED') for k in ('topic','source_id','id'))

def secure_zip(z):
    seen=set();entries={}
    for info in z.infolist():
        name=info.filename
        if info.is_dir():continue
        pp=PurePosixPath(name)
        if name in seen or name.startswith('/') or '..' in pp.parts or '\\' in name or ':' in name or not name:
            raise ValueError('UNSAFE_OR_DUPLICATE_ARCHIVE_MEMBER:'+name)
        if stat.S_IFMT(info.external_attr>>16)==stat.S_IFLNK:raise ValueError('SYMLINK_IN_ARCHIVE:'+name)
        if info.file_size>12_000_000 or sum(i.file_size for i in z.infolist())>45_000_000:
            raise ValueError('UNBOUNDED_ARCHIVE')
        seen.add(name);entries[name]=z.read(info)
    return entries

def inspect_inventory(entries):
    manifest=json.loads(entries['HANDOFF_INVENTORY.json'])
    for item in manifest['files']:
        path=item['path']
        if path not in entries or len(entries[path])!=item['size_bytes'] or digest(entries[path])!=item['sha256']:
            raise ValueError('ORIGINAL_HANDOFF_CUSTODY_HASH_MISMATCH:'+path)
    if set(entries)-{'HANDOFF_INVENTORY.json','README.md'}!=set(item['path'] for item in manifest['files']):
        raise ValueError('UNLISTED_OR_MISSING_ORIGINAL_FILES')
    return manifest

def embedded(page):
    if page.count(MARKER)!=1:raise ValueError('EMBEDDED_BANK_MARKER_NOT_UNIQUE')
    start=page.index(MARKER)+len(MARKER);end=page.find(READER_END,start)
    if end<0:raise ValueError('EMBEDDED_BANK_END_MISSING')
    data=json.loads(page[start:end]);return data,page[start:end]

# The revision is computed from the entire source record and actual original figure
# bytes (or null for a missing figure). It does not trust only the stem hash.
def revisions(data):
    qs=data['questions'];assets=data.get('assets') or {}
    out={}
    for q in qs:
        k=question_key(q)
        if k in out:raise ValueError('DUPLICATED_SCOPED_QUESTION_IDENTITY:'+k)
        refs={name:digest(assets[name].encode('utf-8')) if isinstance(assets.get(name),str) else None
              for name in q.get('source_figures',[])}
        out[k]=digest(canonical({'question':q,'figures':refs}).encode('utf-8'))
    return out

def replace_exact(s,old,new,minimum=1):
    count=s.count(old)
    if count!=minimum:raise ValueError('READER_TEMPLATE_ANCHOR_MISMATCH:'+old[:90]+':'+str(count))
    return s.replace(old,new)

# Runtime is not a secure exam store: browser-local persistence is tamperable.
# It is nevertheless fail-closed under unavailable/stale storage and revision changes.
STORE=r'''<script id="g9-nsejs-private-core2-store">
window.G9PrivateCore2Store=(()=>{
  const prefix='g9:nsejs:core2:private:v1:';
  const enc=s=>encodeURIComponent(String(s));
  function key(identity,revision){return prefix+enc(identity)+':'+revision;}
  function fresh(){return {selected:null,committed:false,revealed:false,firstAttempt:null,helpEvents:[],saved:false};}
  function read(identity,revision){
    try{
      const raw=localStorage.getItem(key(identity,revision));
      const obj=JSON.parse(raw||'null');
      if(obj&&obj.version===1&&obj.identity===identity&&obj.revision===revision&&
          Array.isArray(obj.helpEvents)&&typeof obj.committed==='boolean'&&
          typeof obj.revealed==='boolean'&&(!obj.revealed||obj.committed)&&
          (!obj.committed||(obj.firstAttempt&&typeof obj.firstAttempt.answer==='string'&&
              obj.firstAttempt.answer.length>0&&obj.selected===obj.firstAttempt.answer))){
        return {...fresh(),selected:obj.selected||null,committed:obj.committed,
          revealed:obj.revealed,firstAttempt:obj.firstAttempt||null,
          helpEvents:obj.helpEvents,saved:true,_raw:raw};
      }
    }catch(_){}
    return {...fresh(),_raw:null};
  }
  function write(identity,revision,state){
    const payload={version:1,identity,revision,selected:state.selected||null,
      committed:!!state.committed,revealed:!!state.revealed,
      firstAttempt:state.firstAttempt||null,
      helpEvents:Array.isArray(state.helpEvents)?state.helpEvents:[]};
    if(payload.revealed&&!payload.committed)return false;
    if(payload.committed&&(!payload.firstAttempt||!payload.firstAttempt.answer))return false;
    try{
      const k=key(identity,revision),now=localStorage.getItem(k);
      if(now!==(state._raw||null))return false; // stale second-tab form
      const raw=JSON.stringify(payload);
      localStorage.setItem(k,raw);
      if(localStorage.getItem(k)!==raw)return false;
      state._raw=raw;state.saved=true;return true;
    }catch(_){state.saved=false;return false;}
  }
  return {read,write};
})();
</script>
'''

def patch_reader(page: str)->tuple[str,dict]:
    data,source_json=embedded(page)
    page=page.replace("\r\n","\n")
    qs=data.get('questions')
    if not isinstance(qs,list) or not qs:raise ValueError('QUESTION_LIST_MISSING')
    revs=revisions(data)
    if page.count(ENGINE_START)!=1 or page.count('  const attempts = new Map();')!=1:
        raise ValueError('UNKNOWN_READER_RUNTIME')
    # Only add extra configuration adjacent to running script. Keep original embedded
    # bank JSON byte-for-byte, even if claims are unverified and remain HOLD.
    config='<script id="g9-nsejs-private-core2-revisions" type="application/json">'+canonical(revs)+'</script>\n'
    page=page.replace("<script>\n(()=>{\n  'use strict';\n  const data = JSON.parse(document.getElementById('wpe-data').textContent);",
          STORE+config+"<script>\n(()=>{\n  'use strict';\n  const data = JSON.parse(document.getElementById('wpe-data').textContent);",1)
    if 'g9-nsejs-private-core2-revisions' not in page:raise ValueError('SCRIPT_ENTRY_NOT_PATCHED')
    page=replace_exact(page,ENGINE_START,ENGINE_START+'''
  const reviewRevisions=JSON.parse(document.getElementById('g9-nsejs-private-core2-revisions').textContent);
  const questionKey=q=>[q.topic||'UNSPECIFIED',q.source_id||'UNSPECIFIED',q.id||'UNSPECIFIED'].join('::');
  const attemptKey=q=>questionKey(q);
  const legacyQuestion=new URLSearchParams(window.location.search).get('question');
  const exactChoice=qs.find(q=>questionKey(q)===legacyQuestion);
  const possibleLegacy=legacyQuestion&&!exactChoice?qs.filter(q=>q.id===legacyQuestion||q.source_id===legacyQuestion):[];
  let ambiguousQuestion=Boolean(legacyQuestion&&!exactChoice&&possibleLegacy.length!==1);
  function getAttempt(q){
    const k=attemptKey(q);
    if(!attempts.has(k)) attempts.set(k,G9PrivateCore2Store.read(k,reviewRevisions[k]));
    return attempts.get(k);
  }
  function saveAttempt(q,state){
    const k=attemptKey(q);
    if(!G9PrivateCore2Store.write(k,reviewRevisions[k],state))return false;
    attempts.set(k,state);return true;
  }
''')
    old="""  let active = params.get('question') || qs[0].id;
  if (!qs.some(q => q.id === active)) active = qs[0].id;"""
    new="""  let active = exactChoice?questionKey(exactChoice):
    (possibleLegacy.length===1?questionKey(possibleLegacy[0]):(!legacyQuestion?questionKey(qs[0]):''));"""
    page=replace_exact(page,old,new)
    page=replace_exact(page,"  const attempts = new Map();","  const attempts = new Map();")
    # The code above uses attempts (let/const declared later) only when invoked
    # by render after initialization, never during initial declaration.
    page=page.replace('q.id === active','questionKey(q) === active')
    page=page.replace('esc(q.id)', 'esc(questionKey(q))')
    page=page.replace('item.id === active','questionKey(item) === active')
    page=page.replace('active = filtered[0].id','active = questionKey(filtered[0])')
    page=page.replace('active = filtered[idx - 1].id','active = questionKey(filtered[idx - 1])')
    page=page.replace('active = filtered[idx + 1].id','active = questionKey(filtered[idx + 1])')
    page=page.replace("' data-id=\"' + esc(q.id) + '\"'","' data-id=\"' + esc(questionKey(q)) + '\"'")
    page=page.replace('if (!filtered.some(q => questionKey(q) === active) && filtered.length > 0)',
                      'if (!ambiguousQuestion && !filtered.some(q => questionKey(q) === active) && filtered.length > 0)')
    page=replace_exact(page,"        active = btn.dataset.id;","        active = btn.dataset.id;\n        ambiguousQuestion=false;")
    page=replace_exact(page,"    if (!q) {\n      nodes.root.innerHTML = '<p class=\"subtitle\">No matching question found.</p>';\n      return;\n    }", """    if (!q) {
      const candidates=possibleLegacy.filter(item=>filtered.some(x=>questionKey(x)===questionKey(item)));
      nodes.root.innerHTML='<section class="stage" role="status"><h2>Unresolved or repeated legacy question identifier</h2>'+
        '<p>Select an explicit subject-specific record. No answer is auto-selected.</p>'+
        candidates.map(item=>'<button type="button" class="btn disambiguate" data-id="'+esc(questionKey(item))+'">'+
          esc(item.topic)+' · '+esc(item.source_id)+' · '+esc(item.id)+'</button>').join('')+'</section>';
      nodes.root.querySelectorAll('.disambiguate').forEach(button=>button.addEventListener('click',()=>{
        active=button.dataset.id;ambiguousQuestion=false;
        const url=new URL(window.location);url.searchParams.set('question',active);
        window.history.replaceState({},'',url);renderNav();renderQuestion();
      }));
      return;
    }""")
    page=replace_exact(page,'const st = attempts.get(q.id) || { selected: null, committed: false, revealed: false };','const st = getAttempt(q);')
    page=replace_exact(page,'const svg = data.assets[figName];',"const svg = data.assets && Object.hasOwn(data.assets,figName) ? data.assets[figName] : null;")
    page=replace_exact(page,"      }\n    }\n\n    // Options", """      } else {
        media='<div class="alert" role="alert"><strong>REQUIRED DIAGRAM UNAVAILABLE · HOLD</strong>'+
          '<p>The diagram is not present in this verified handoff. Do not infer the answer from text alone.</p></div>';
      }
    }

    // Options""")
    page=page.replace('attempts.get(q.id) || { selected: null, committed: false, revealed: false }','getAttempt(q)')
    page=page.replace('attempts.get(q.id)','getAttempt(q)')
    page=page.replace('attempts.set(q.id, cur)','attempts.set(attemptKey(q), cur)')
    page=page.replace('attempts.set(q.id,cur)','attempts.set(attemptKey(q),cur)')
    page=page.replace("'Attempt committed in this browser session.'", "'First attempt saved locally; not a secure examination record.'")
    page=page.replace("'<span class=\"chip\">' + esc(q.key_state) + '</span>'", "'<span class=\"chip hold\">KEY AUTHORITY HOLD · source reports ' + esc(q.key_state) + '</span>'")
    page=page.replace("'Official examination key on file. Academic qualification remains candidate unadmitted.'", "'Source/key authority not independently verified. Private author/coaching reconstruction only.'")
    page=page.replace(' · Verbatim source preserved.',' · Source data unchanged; original authenticity not independently verified.')
    # Source-level primary original attempts should have no H1-H3 reveal before
    # a frozen unassisted response. Hints after attempt retain exposure history.
    page=replace_exact(page,"        hintMarkup(q) +", "        (st.committed ? hintMarkup(q) : '<p class=\"subtitle\">Hints unlock after a saved first attempt so the original response remains independent.</p>') +")
    marker="""    commitBtn.addEventListener('click', () => {
      const cur = getAttempt(q);
      if (!cur || !cur.selected) {
        commitNote.textContent = 'Please choose an option before committing.';
        return;
      }
      cur.committed = true;
      attempts.set(attemptKey(q), cur);
      commitBtn.disabled = true;
      revealBtn.disabled = false;
      radioInputs.forEach(r => r.disabled = true);
      commitNote.textContent = 'Attempt committed. You may now reveal the worked solution.';
      revealBtn.scrollIntoView({ behavior: 'auto', block: 'nearest' });
    });"""
    new_commit="""    commitBtn.addEventListener('click', () => {
      const cur=getAttempt(q);
      if(!cur || !cur.selected || cur.committed){commitNote.textContent='Choose an option first.';return;}
      const candidate={...cur,committed:true,revealed:false,
        firstAttempt:{answer:cur.selected,savedAt:new Date().toISOString(),helpBeforeAttempt:cur.helpEvents.length}};
      if(!saveAttempt(q,candidate)){
        commitNote.textContent='SAVE FAILED or stale tab. No attempt committed; refresh and retry.';
        return;
      }
      renderQuestion();
    });"""
    page=replace_exact(page,marker,new_commit)
    marker_reveal="""    revealBtn.addEventListener('click', () => {
      const cur = getAttempt(q);
      if (!cur || !cur.committed) return;
      cur.revealed = true;
      attempts.set(attemptKey(q), cur);
      revealBtn.disabled = true;
      nodes.root.querySelector('#reveal-note').textContent = 'Solution unlocked.';
      nodes.root.querySelector('#solution-container').innerHTML = solutionMarkup(q);
    });"""
    replacement="""    revealBtn.addEventListener('click',()=>{
      const cur=getAttempt(q);
      if(!cur.committed || !cur.firstAttempt)return;
      if(!saveAttempt(q,{...cur,revealed:true})){
        nodes.root.querySelector('#reveal-note').textContent='Local save failed; solution stays protected.';return;
      }
      renderQuestion();
    });"""
    page=replace_exact(page,marker_reveal,replacement)
    # Help events are recorded against the exact original attempt separately.
    page=replace_exact(page,"""        if (el.open && idx > 0 && !hintEls[idx - 1].open) {
          el.open = false;
        }""", """        if(el.open && idx>0 && !hintEls[idx-1].open){el.open=false;return;}
        if(el.open){
          const state=getAttempt(q);
          const candidate={...state,helpEvents:[...state.helpEvents,idx]};
          if(!saveAttempt(q,candidate))el.open=false;
        }""")
    # On a different-tab change, drop stale cached record, refresh view.
    page=replace_exact(page,'  // Initialize\n  filters();',"""  window.addEventListener('storage',event=>{
    if(event.key&&event.key.startsWith('g9:nsejs:core2:private:v1:')){
      attempts.clear();renderQuestion();
    }
  });
  // Initialize
  filters();""")
    # Presentation labels must not overclaim the original-source evidence.
    before,after=page.split(MARKER,1)
    before=before.replace('All questions shown are authentic examination items with official keys verified.',
      'Original question identity, diagrams and answer-key authority are NOT independently verified; all records remain candidates.')
    before=before.replace('Authentic National Standard Examination',
      'Unverified candidate transcription of National Standard Examination')
    if '<body>' not in before:raise ValueError('PRIVATE_REVIEW_BODY_MISSING')
    before=before.replace('<body>', '<body><aside role="status" style="padding:10px 16px;background:#ffefcd;color:#5d3110;font:700 14px system-ui">PRIVATE REVIEW ONLY · SOURCE AND KEY AUTHORITY HOLD · NOT FOR PUBLICATION · NOT ACADEMICALLY ADMITTED</aside>',1)
    page=before+MARKER+after
    current_json=embedded(page)[1]
    page=page.replace(current_json,source_json,1)
    return page, {'question_count':len(qs),'scoped_count':len(revs),'unscoped_count':len(set(q.get('id') for q in qs)),
                  'duplicate_ids':dict((k,v) for k,v in Counter(q.get('id') for q in qs).items() if v>1),
                  'missing_figures':sum(1 for q in qs for name in q.get('source_figures',[]) if name not in (data.get('assets') or {})),
                  'source_json_digest':digest(source_json.encode('utf-8'))}

def repair_zip(src:Path,out:Path,expected:str):
    if out.exists():raise ValueError('OUTPUT_ALREADY_EXISTS')
    raw=src.read_bytes()
    if digest(raw)!=expected:raise ValueError('UNTRUSTED_OR_CHANGED_HANDOFF_ZIP')
    with zipfile.ZipFile(src) as zin:entries=secure_zip(zin)
    old_inventory=inspect_inventory(entries)
    original={name:digest(data) for name,data in entries.items()}
    previews=sorted(x for x in entries if x.endswith('question-status.html'))
    if not previews:raise ValueError('NO_READERS_TO_REPAIR')
    results={}
    for path in previews:
        old=entries[path].decode('utf-8')
        new,stats=patch_reader(old)
        # Exact original question JSON embedded unchanged.
        assert embedded(old)[1]==embedded(new)[1]
        entries[path]=new.encode('utf-8');results[path]=stats
    # Original member bytes remain untouched except review HTML; original
    # inventory retained as a SOURCE receipt, not misrepresented as current hashes.
    receipt={'status':'PRIVATE_CANDIDATE_TECHNICAL_FIX_ACADEMIC_HOLD','publish':False,
             'input_sha256':expected,'source_file_count':old_inventory['file_count'],
             'original_file_sha256':original,'result_file_sha256':{k:digest(v) for k,v in entries.items()},
             'reader_audit':results,'independent_qrt':'NOT_RUN',
             'source_key_verification':'HOLD','academic_admission':'HOLD',
             'prior_inventory_note':'HANDOFF_INVENTORY.json remains the original handoff receipt, not an updated output manifest',
             'correction_scope':'viewer only; original source/question datasets are byte-identical'}
    entries['PRIVATE_REPAIR_RECEIPT.json']=(canonical(receipt)+'\n').encode('utf-8')
    with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as zout:
        for path in sorted(entries):zout.writestr(path,entries[path])
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--expected-sha256',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    r=repair_zip(a.input,a.output,a.expected_sha256)
    print(json.dumps({'status':r['status'],'reader_audit':r['reader_audit']},indent=2))
if __name__=='__main__':main()
