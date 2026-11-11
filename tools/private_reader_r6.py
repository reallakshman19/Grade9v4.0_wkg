"""Private Grade9 technical reader R6: deterministic scoped links and local practice.

Works on verified private R5 review sites. Does NOT approve questions, supply missing
figures, or authorize publishing. Input tree remains unmodified. Re-pins only the
resulting private review artifact. The JS store is *not* a secure assessment backend.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

MARKER = '<script id="wpe-data" type="application/json">'
END = '</script>'
RUNTIME = r'''<script id="g9-r6-review-store">
window.G9ReviewStore = (() => {
  const prefix = 'g9:private:practice:v3:';
  function storageKey(scope, revision) {
    return prefix + encodeURIComponent(scope) + ':' + revision;
  }
  function fresh() { return {selected: null, committed: false, revealed: false,
    firstAttempt: null, helpEvents: [], storageStatus: 'UNSAVED'}; }
  function read(scope, revision) {
    const result = fresh();
    try {
      const data = JSON.parse(localStorage.getItem(storageKey(scope, revision)) || 'null');
      if (data && data.version === 3 && data.scope === scope &&
          data.revision === revision && Array.isArray(data.helpEvents) &&
          typeof data.committed === 'boolean' && typeof data.revealed === 'boolean' &&
          (!data.committed || (data.firstAttempt && typeof data.firstAttempt === 'object'))) {
        return {...result, selected: data.selected || null, committed: data.committed,
          revealed: data.revealed && data.committed, firstAttempt: data.firstAttempt || null,
          helpEvents: data.helpEvents.filter(n => Number.isInteger(n) && n >= 0),
          storageStatus: 'SAVED_LOCAL'};
      }
    } catch (_) { /* disabled storage must never become a fake success */ }
    return result;
  }
  function write(scope, revision, state) {
    const data = {version: 3, scope, revision, selected: state.selected || null,
      committed: !!state.committed, revealed: !!state.revealed,
      firstAttempt: state.firstAttempt || null,
      helpEvents: Array.isArray(state.helpEvents) ? state.helpEvents : []};
    try {
      localStorage.setItem(storageKey(scope, revision), JSON.stringify(data));
      state.storageStatus = 'SAVED_LOCAL';
      return true;
    } catch (_) {
      state.storageStatus = 'UNSAVED';
      return false;
    }
  }
  return {read, write};
})();
</script>
'''


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def identity(q):
    return [str(q.get('topic') or 'UNSCOPED'), str(q.get('source_id') or ''), str(q.get('id') or '')]


def uri_component(s):
    from urllib.parse import quote
    return quote(s, safe="~()*!.'-")


def question_key(q):
    return '::'.join(uri_component(part) for part in identity(q))


def revise(q, assets):
    # Provenance/source identity, options, answer, conditions and actual figure bytes.
    # Missing required media are explicit null digests, never fabricated data.
    figure_digests = {name: sha(assets[name].encode('utf-8')) if name in assets else None
                      for name in q.get('source_figures', [])}
    return sha(canonical({'question':q, 'figure_byte_digests':figure_digests}).encode('utf-8'))


def replace_once(source, original, replacement):
    count=source.count(original)
    if count != 1: raise ValueError('R6_EXPECTED_RUNTIME_ANCHOR_MISMATCH:'+str(count))
    return source.replace(original,replacement,1)


def patch_reader(js_html: str) -> str:
    old = '''  const chosen = qs.find(q => questionKey(q) === requested) ||
      qs.find(q => q.source_id === requested) ||
      qs.find(q => q.id === requested) || qs[0];
  let active = chosen ? questionKey(chosen) : '';

  const attempts = new Map();'''
    new = '''  // Scoped links are authoritative. A repeated legacy alias must be resolved
  // by an explicit learner choice rather than silently opening the first match.
  const exact = requested ? qs.find(q => questionKey(q) === requested) : null;
  const legacyMatches = requested && !exact ?
    qs.filter(q => q.source_id === requested || q.id === requested) : [];
  const chosen = exact || (legacyMatches.length === 1 ? legacyMatches[0] :
    (!requested ? qs[0] : null));
  let active = chosen ? questionKey(chosen) : '';
  let unresolvedLink = Boolean(requested && !chosen);

  const attempts = new Map();
  function getAttempt(q) {
    const key = questionKey(q);
    if (!attempts.has(key)) {
      attempts.set(key, G9ReviewStore.read(key, data.review_revisions[key]));
    }
    return attempts.get(key);
  }
  function putAttempt(q, state) {
    const key = questionKey(q);
    G9ReviewStore.write(key, data.review_revisions[key], state);
    attempts.set(key, state);
    return state.storageStatus === 'SAVED_LOCAL';
  }'''
    js_html=replace_once(js_html,old,new)
    js_html=replace_once(js_html,'''    if (!filtered.some(q => questionKey(q) === active) && filtered.length > 0) {''',
                              '''    if (!unresolvedLink && !filtered.some(q => questionKey(q) === active) && filtered.length > 0) {''')
    # A bounded, text-escaped disambiguation view; no answer/attempt shown.
    old = '''    if (!q) {
      nodes.root.innerHTML = '<p class="subtitle">No matching question found.</p>';
      return;
    }'''
    new = '''    if (!q) {
      const candidates = legacyMatches.filter(item =>
        filtered.some(candidate => questionKey(candidate) === questionKey(item)));
      nodes.root.innerHTML = '<section class="stage" role="status"><h2>' +
        (candidates.length > 1 ? 'Ambiguous legacy question link' : 'Question link not resolved') +
        '</h2><p>A legacy identifier is not globally unique. Select the intended topic; ' +
        'no answer or attempt was automatically opened.</p>' +
        candidates.map(item => '<button type="button" class="btn choose-legacy" data-id="' +
          esc(questionKey(item)) + '">' + esc(item.topic) + ' · ' + esc(item.source_id) +
          ' · ' + esc(item.id) + '</button>').join('') + '</section>';
      nodes.root.querySelectorAll('.choose-legacy').forEach(button =>
        button.addEventListener('click', () => {
          active = button.dataset.id;
          unresolvedLink = false;
          const url = new URL(window.location);
          url.searchParams.set('question', active);
          window.history.replaceState({}, '', url);
          renderNav(); renderQuestion();
        }));
      return;
    }'''
    js_html=replace_once(js_html,old,new)
    js_html=replace_once(js_html,'''        active = btn.dataset.id;
        const url''',
                              '''        active = btn.dataset.id;
        unresolvedLink = false;
        const url''')
    js_html=replace_once(js_html,'''    const st = attempts.get(questionKey(q)) || { selected: null, committed: false, revealed: false };''',
                              '''    const st = getAttempt(q);''')
    js_html=replace_once(js_html,'''      let cur = attempts.get(questionKey(q)) || { selected: null, committed: false, revealed: false };''',
                              '''      let cur = getAttempt(q);''')
    getter = '      const cur = attempts.get(questionKey(q));'
    if js_html.count(getter) != 2:
        raise ValueError('R6_ATTEMPT_GET_ANCHOR_COUNT')
    js_html = js_html.replace(getter, '      const cur = getAttempt(q);')
    if js_html.count('attempts.set(questionKey(q), cur);')!=3:
        raise ValueError('R6_ATTEMPT_SAVE_ANCHOR_COUNT')
    js_html=js_html.replace('attempts.set(questionKey(q), cur);','putAttempt(q, cur);')
    js_html=replace_once(js_html,'''      cur.committed = true;
      putAttempt(q, cur);''',
                              '''      if (cur.committed) return; // preserve the first committed response
      cur.committed = true;
      cur.firstAttempt = {selected: cur.selected, at: new Date().toISOString(),
        assisted: !!(cur.helpEvents && cur.helpEvents.length)};
      putAttempt(q, cur);''')
    js_html=replace_once(js_html,'''      commitNote.textContent = 'Attempt committed. You may now reveal the worked solution.';''',
                              '''      commitNote.textContent = cur.storageStatus === 'SAVED_LOCAL' ?
        'First attempt saved in this browser for this question revision (ungraded, not certified).' +
          (cur.firstAttempt.assisted ? ' ASSISTED: a hint was opened before commitment.' :
            ' No hint opened before commitment (browser-local observation only).') :
        'Attempt committed on this page, but browser storage failed: NOT SAVED; reload loses progress.';''')
    js_html=replace_once(js_html,'''      '<span id="commit-note" class="live-note">' + (st.committed ? 'Attempt committed on this page only; reloading clears it.' : 'Select an option to enable commitment.') + '</span>' +''',
                              '''      '<span id="commit-note" class="live-note">' + (st.committed ?
        (st.storageStatus === 'SAVED_LOCAL' ? 'First attempt restored from local browser storage (ungraded).' +
          (st.firstAttempt && st.firstAttempt.assisted ? ' ASSISTED by previously opened hint.' : '') :
          'First attempt exists on this page only; storage failed.') : 'Select an option to enable commitment.') + '</span>' +''')
    old='''      el.addEventListener('toggle', () => {
        if (el.open && idx > 0 && !hintEls[idx - 1].open) {
          el.open = false;
        }
      });'''
    new='''      el.addEventListener('toggle', () => {
        if (el.open && idx > 0 && !hintEls[idx - 1].open) {
          el.open = false;
          return;
        }
        if (el.open) {
          const cur = getAttempt(q);
          cur.helpEvents = Array.isArray(cur.helpEvents) ? cur.helpEvents : [];
          if (!cur.helpEvents.includes(idx)) {
            cur.helpEvents.push(idx);
            putAttempt(q, cur);
          }
        }
      });'''
    js_html=replace_once(js_html,old,new)
    # Question changes via filters should not keep unresolved legacy ID pending.
    # Main script reads review_revisions injected in the JSON, not a separate file.
    return js_html


def transform(html_text: str) -> str:
    if html_text.count(MARKER) != 1 or 'id="g9-r6-review-store"' in html_text:
        raise ValueError('R6_MARKER_OR_DUPLICATE')
    start=html_text.index(MARKER)+len(MARKER)
    end=html_text.index(END,start)
    data=json.loads(html_text[start:end]);qs=data['questions']
    assets=data.get('assets') or {}
    revisions={question_key(q):revise(q,assets) for q in qs}
    if len(revisions)!=len(qs):raise ValueError('R6_SCOPED_ID_COLLISION')
    data['review_revisions']=revisions
    payload=canonical(data)
    if '</script' in payload.lower() or '<!--' in payload:raise ValueError('R6_UNSAFE_EMBEDDED_DATA')
    original_questions=canonical(qs)
    out=html_text[:start]+payload+html_text[end:]
    # Patch only expected candidate runtime; fail closed instead of quietly doing nothing.
    out=patch_reader(out)
    if out.count('</head>')!=1:raise ValueError('R6_HEAD_INVALID')
    out=out.replace('</head>',RUNTIME+'</head>',1)
    # Provenance: no modifications to original source questions and answer bytes.
    if canonical(json.loads(out.split(MARKER,1)[1].split(END,1)[0])['questions'])!=original_questions:
        raise ValueError('R6_SOURCE_QUESTION_MUTATED')
    return out


def upgrade_site(source:Path,output:Path):
    source=source.resolve(strict=True)
    output=output.absolute()
    if output.resolve().is_relative_to(source) or output.resolve() == source or output.exists():
        raise ValueError('R6_UNSAFE_OUTPUT')
    receipt=json.loads((source/'PRIVATE_REVIEW_MANIFEST.json').read_text())
    if receipt.get('release_authority')!='HOLD' or receipt.get('academic_approval')!='HOLD':
        raise ValueError('R6_RELEASE_AUTHORITY')
    files=receipt['output_files']
    if not isinstance(files,dict) or not files or not all(isinstance(p,str) and p for p in files):
        raise ValueError('R6_OUTPUT_FILE_LIST_INVALID')
    # The generated review artifact must be a closed, file-pinned tree. Never
    # follow symlinks, copy hidden unaccounted assets, or allow path traversal.
    allowed=set(files)|{'PRIVATE_REVIEW_MANIFEST.json','.GRADE9_PRIVATE_REVIEW_ONLY'}
    actual_files=set()
    for item in source.rglob('*'):
        if item.is_symlink():raise ValueError('R6_SYMLINK_REJECTED')
        if item.is_file():actual_files.add(item.relative_to(source).as_posix())
    if actual_files!=allowed:
        raise ValueError('R6_UNACCOUNTED_OUTPUT_FILES')
    for name in files:
        path=Path(name)
        if (path.is_absolute() or not name.endswith('.html') or
            any(part in ('.','..','') for part in name.split('/')) or
            '\\' in name or ':' in name or '\x00' in name):
            raise ValueError('R6_UNSAFE_OUTPUT_REFERENCE')
    actual={p:sha((source/p).read_bytes()) for p in files}
    if actual!=files:raise ValueError('R6_INPUT_PIN_MISMATCH')
    data=json.loads((source/'preview/question-status.html').read_text('utf-8').split(MARKER,1)[1].split(END,1)[0])
    if sha(canonical(data['questions']).encode('utf-8'))!=receipt.get('source_question_digest'):
        raise ValueError('R6_SOURCE_QUESTION_DIGEST_MISMATCH')
    orig_digest=receipt['source_question_digest']
    with tempfile.TemporaryDirectory(prefix='g9-r6-') as temp:
        stage=Path(temp)/'site'
        shutil.copytree(source,stage,symlinks=True)
        for path in files:
            if path.endswith('/question-status.html'):
                target=stage/path
                target.write_text(transform(target.read_text('utf-8')),encoding='utf-8')
        for path in files: files[path]=sha((stage/path).read_bytes())
        receipt['runtime_profile']='r6-revision-scoped-local-attempts'
        receipt['source_question_digest']=orig_digest
        receipt['release_authority']='HOLD'
        receipt['academic_approval']='HOLD'
        (stage/'PRIVATE_REVIEW_MANIFEST.json').write_text(canonical(receipt)+'\n',encoding='utf-8')
        if not (stage/'.GRADE9_PRIVATE_REVIEW_ONLY').is_file():raise ValueError('R6_PRIVATE_MARKER_MISSING')
        output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(stage,output)
    return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--site',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    result=upgrade_site(args.site,args.out)
    print('PASS private R6',result['record_count'],result['runtime_profile'])