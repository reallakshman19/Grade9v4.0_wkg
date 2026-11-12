"""Build the W5 WEP-07 study page (Core2 -> Core1A -> Core1B) beside B2.

OTM-BUILT. Usage: python -I build_w5.py <pair.json> <core2_dir> <out_dir>
B2 (standalone/study/nlm-core1ab) is not read or changed.
"""
import base64, hashlib, html, json, os, sys

pair_path, core2_dir, out_dir = sys.argv[1:4]
raw = open(pair_path, 'rb').read()
pair_sha = hashlib.sha256(raw).hexdigest()
d = json.loads(raw.decode('utf-8'))

# Core2 items: id, label, official key (hidden until the learner records an answer), extension note.
CORE2 = [
    ('WEP07-01', 'NSEP 2024 (Set 61) · Q4', 'd', 'single', ''),
    ('WEP07-02', 'NSEP 2024 (Set 61) · Q32', 'a', 'single', ''),
    ('WEP07-03', 'NSEP 2025 (Set 611) · Q57', 'a, b, c, d', 'multi', 'Key from the IAPT published solution.'),
    ('WEP07-04', 'NSEP 2024 (Set 61) · Q59', 'b, c', 'multi',
     'Extension: needs rotation (beyond Grade 9, given). Only parts (b) and (c) test WEP-07; (c) uses the horizontal release of (b).'),
]

e = html.escape


def get(path):
    cur = d
    for part in path.split('.'):
        cur = cur[part]
    return cur


def label(k):
    return e(str(k).replace('_', ' '))


def render(v, depth=0):
    """Generic readable rendering of strings, lists and dicts."""
    if isinstance(v, str):
        return '<p>%s</p>' % e(v) if depth == 0 else e(v)
    if isinstance(v, (int, float, bool)) or v is None:
        return e(json.dumps(v))
    if isinstance(v, list):
        if not v:
            return '<em>none</em>'
        return '<ul>%s</ul>' % ''.join('<li>%s</li>' % render(x, depth + 1) for x in v)
    rows = ''.join('<dt>%s</dt><dd>%s</dd>' % (label(k), render(x, depth + 1)) for k, x in v.items())
    return '<dl>%s</dl>' % rows


def details(summary, body, open_=False):
    return '<details%s><summary>%s</summary>%s</details>' % (' open' if open_ else '', summary, body)


# ---- Core2
core2_html = []
for cid, lab, key, kind, note in CORE2:
    png = [f for f in os.listdir(core2_dir) if f.startswith(cid) and f.endswith('.png')][0]
    b64 = base64.b64encode(open(os.path.join(core2_dir, png), 'rb').read()).decode()
    ext = '<span class="tag ext">Extension</span>' if cid == 'WEP07-04' else '<span class="tag">Core</span>'
    hint = 'one letter' if kind == 'single' else 'all correct letters, e.g. a, c'
    core2_html.append(f'''
<article class="card" id="{cid}">
  <header><h3>{e(cid)} · {e(lab)}</h3>{ext}</header>
  <img class="crop" alt="Original question {e(cid)}, official IAPT paper page crop" src="data:image/png;base64,{b64}">
  {'<p class="note">' + e(note) + '</p>' if note else ''}
  <div class="attempt" data-gate="{cid}">
    <label>Your answer ({hint})<input type="text" data-save="{cid}-ans" autocomplete="off"></label>
    <button type="button" data-record="{cid}">Record my answer</button>
    <div class="reveal" hidden><p><strong>Official key:</strong> {e(key)}</p>
    <p class="muted">Check your reasoning in the Core 1A tab, then try Core 1B.</p></div>
  </div>
</article>''')

# ---- Core1A (everything is a completed worked teaching sequence)
a = d['core1a']
a_parts = ['<h2>%s</h2>' % e(a['title']), '<p class="jump"><strong>The one idea all four questions share:</strong> %s</p>' % e(d['shared_inferential_jump'])]
names = {'bucket.conventions': 'Conventions', 'microtopic.entry_assumptions': 'What we assume',
         'microtopic.inferential_jump': 'The key step', 'representation': 'Pictures and scenes',
         'microtopic.teaching_path': 'Teaching path', 'core1a.questions': 'Worked examples',
         'microtopic.misconceptions': 'Common mistakes', 'relation.checks': 'Checks on the energy relation',
         'microtopic.exit_task': 'Exit task', 'proposed_extension_candidate': 'Extension: rotation (beyond Grade 9)',
         'authority': None}
for blk in a['ordered_blocks']:
    if 'show' in blk:
        a_parts.append('<p>%s</p>' % e(blk['show']))
        continue
    ref = blk.get('ref')
    title = names.get(ref, ref)
    if title is None:
        continue  # authority goes to the Owner view
    if ref == 'core1a.questions':
        qs = []
        for q in a['questions']:
            ans = q['answer']
            steps = ''.join('<li>%s</li>' % e(s) for s in ans.get('reasoning', []))
            qs.append(details('<strong>%s</strong> · %s' % (e(q['id']), e(q['title'])),
                              '<p>%s</p><ol>%s</ol><p><strong>Summary:</strong> %s</p>%s' % (
                                  e(q['setup']), steps, e(str(ans.get('summary', ''))),
                                  details('Rubric and check', render({k: ans[k] for k in ('rubric', 'check') if k in ans})))))
        a_parts.append('<h3>%s</h3>%s' % (title, ''.join(qs)))
    elif ref == 'microtopic.exit_task':
        x = get(ref)
        a_parts.append('<h3>%s</h3><p>%s</p>%s' % (title, e(x['prompt']), details('Show the answer', render(x['answer']))))
    else:
        a_parts.append(details('<strong>%s</strong>' % e(title), render(get(ref)), open_=(ref == 'microtopic.inferential_jump')))

# ---- Core1B (attempt first; only listed fields before the attempt)
b = d['core1b']
conv = {c['id']: c for c in d['bucket']['conventions']}


def conv_list(ids_key):
    out = []
    for cid in b.get(ids_key, []):
        c = conv.get(cid) or next((v for k, v in conv.items() if k.endswith(cid)), None)
        if c:
            out.append('<li>%s</li>' % render({k: v for k, v in c.items() if k != 'id'}, 1))
    return '<ul>%s</ul>' % ''.join(out)


me = d['microtopic']['elicitation']
b_parts = ['<p>%s</p>' % e(b['ordered_blocks'][0]['text']),
           details('<strong>Conventions you may use</strong>', conv_list('visible_convention_refs'), True)]


def cycle(cid, title, predict_prompt, produces, after):
    return f'''
<article class="card cycle" id="{e(cid)}">
  <header><h3>{e(title)}</h3></header>
  <p><strong>Predict:</strong> {e(predict_prompt)}</p>
  <p><strong>Attempt:</strong> {e(produces)}</p>
  <div class="attempt" data-gate="{e(cid)}">
    <label>Your prediction and working<textarea rows="6" data-save="{e(cid)}-work"></textarea></label>
    <button type="button" data-record="{e(cid)}">Record my attempt</button>
    <div class="reveal" hidden>{after}</div>
  </div>
</article>'''


main_after = render({'defensible answer to the prediction': me['predict'].get('defensible_answer'),
                     'model response': me['attempt'].get('model_response'),
                     'rubric': me['attempt'].get('rubric'),
                     'accepted': me['attempt'].get('accepted'),
                     'rejected': me['attempt'].get('rejected')}) + details('Reconstruct', render(me['reconstruct'])) \
    + details('Boundary test', render(me['boundary_test']))
b_parts.append(cycle('B-MAIN', 'Main cycle', me['predict']['prompt'], me['attempt']['produces'], main_after))
for c in b['concept_cycles']:
    after = render({'defensible answer to the prediction': c['predict'].get('defensible_answer'),
                    'model response': c['attempt'].get('model_response'),
                    'rubric': c['attempt'].get('rubric'),
                    'accepted': c['attempt'].get('accepted'),
                    'rejected': c['attempt'].get('rejected')}) + details('Reconstruct', render(c['reconstruct'])) \
        + details('Boundary test', render(c['boundary_test']))
    t = c['id'].replace('CYCLE-', '').replace('-', ' ').title()
    if 'ROTATION' in c['id']:
        t += ' · extension, beyond Grade 9'
    b_parts.append(cycle(c['id'], t, c['predict']['prompt'], c['attempt']['produces'], after))
b_parts.append('<div class="after-all" hidden>%s%s%s</div>' % (
    details('<strong>More conventions</strong>', conv_list('deferred_convention_refs')),
    details('<strong>Common mistakes and repairs</strong>', render(d['microtopic']['misconceptions'])),
    details('<strong>Representation check</strong>', render(d['representation']))))

# ---- Owner view
crop_rows = ''.join('<li>%s</li>' % e(l) for l in open(os.path.join(core2_dir, 'MANIFEST.md'), encoding='utf-8').read().splitlines())
owner = render({'pair file': os.path.basename(pair_path), 'pair sha256': pair_sha, 'writer status': d.get('writer_status'),
                'authority': d.get('authority'), 'scope': d.get('scope'),
                'not done or unsure': d.get('not_done_or_unsure'), 'self check': d.get('self_check_what_could_be_wrong'),
                'stretch flags': d.get('prerequisite_stretch_flags')}) + '<h4>Core2 manifest</h4><ul>%s</ul>' % crop_rows

page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shell.html'), encoding='utf-8').read()
page = (page.replace('{{CORE2}}', ''.join(core2_html)).replace('{{CORE1A}}', ''.join(a_parts))
        .replace('{{CORE1B}}', ''.join(b_parts)).replace('{{OWNER}}', owner)
        .replace('{{PAIR}}', e(os.path.basename(pair_path))))
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, 'index.html')
open(out, 'w', encoding='utf-8', newline='\n').write(page)
print(out, len(page.encode('utf-8')), hashlib.sha256(page.encode('utf-8')).hexdigest())
