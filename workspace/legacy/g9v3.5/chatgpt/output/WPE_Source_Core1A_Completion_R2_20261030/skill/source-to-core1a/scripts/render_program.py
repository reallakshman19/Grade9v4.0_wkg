"""Render a private author-preparation catalogue and full linked dossiers; no lessons."""
from pathlib import Path
import argparse,html,json
from check_handoff import load,inside
from check_program import check_program
E=lambda v:html.escape(str(v),quote=True)
STYLE='''body{font:17px/1.6 system-ui,sans-serif;max-width:1120px;margin:auto;padding:28px;color:#1b3045;background:#f5f7fa}body{overflow-wrap:anywhere}code{overflow-wrap:anywhere;word-break:break-word}h1,h2,h3{line-height:1.2}h2{margin-top:2em}a{color:#145ba1}article,details,.panel{background:#fff;border:1px solid #d3dde6;border-radius:10px;padding:18px;margin:14px 0}.hold{border-left:6px solid #b77a11;background:#fff3d7;padding:18px}.flow{display:flex;flex-wrap:wrap;gap:8px}.flow span{background:#e5edf6;padding:8px 12px;border-radius:6px}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #ccd6df;padding:10px;overflow-wrap:anywhere}th:nth-child(2),th:nth-child(3){white-space:nowrap}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}img{max-width:100%;max-height:420px;object-fit:contain}.scroll{overflow:auto}.meta{font-size:14px;color:#4b6075}summary{cursor:pointer}@media print{body{background:white;padding:0}details{break-inside:avoid}.hold{background:white}}'''
def page(title,body):return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+'</title><style>'+STYLE+'</style></head><body>'+body+'</body></html>'
def listing(xs):return '<ul>'+''.join('<li>'+E(x)+'</li>' for x in xs)+'</ul>'
def linked(ids):return ', '.join('<a href="#'+E(x)+'">'+E(x)+'</a>' for x in ids) or 'None'
def record(d,result):
 b='<nav><a href="../index.html">All ten WPE nodes</a> · <a href="'+E(d['id'])+'.json">Exact JSON</a></nav><h1>'+E(d['id']+' · '+d['title'])+'</h1>'
 b+='<div class="hold"><strong>AUTHOR PREPARATION · CANDIDATE · LESSON AUTHORING HOLD</strong><br>Mechanical integrity '+E(result['integrity'])+'; source pins '+E(result['trust_binding'])+'. Science NOT_QUALIFIED. Reviewed SL2 join missing. No learner lesson or native package.</div>'
 c=d['construction'];b+='<h2>Required construction</h2><p>'+E(c['output'])+'</p><p><strong>Obstacle:</strong> '+E(c['obstacle'])+'</p><p><strong>Decisive move:</strong> '+E(c['decisive_move'])+'</p><h3>Inputs</h3>'+listing(c['inputs'])+'<h3>Prerequisites and conventions</h3>'+listing(c['entry_assumptions']+c['conventions'])
 b+='<h2>Source custody and original assets</h2><div class="scroll"><table><tr><th>ID / role</th><th>Retained file</th><th>Authority / digest</th></tr>'
 for s in d['sources']:b+='<tr><td>'+E(s['id']+' / '+s['role'])+'</td><td><a href="'+E(s['path'])+'">'+E(s['path'])+'</a></td><td>'+E(s['authority'])+'<br><code>'+E(s['sha256'])+'</code></td></tr>'
 b+='</table></div><h2>Concept claims, conditions and disputes</h2>'
 for x in d['claims']:
  b+='<article id="'+E(x['id'])+'"><h3>'+E(x['id'])+' · UNREVIEWED</h3><p>'+E(x['statement'])+'</p><p>Exact units: '+linked(x['unit_refs'])+'</p><p>Retained scan IDs: '+E(', '.join(x['source_scan_refs']))+'</p><h4>Conditions</h4>'+listing(x['conditions'])+'<h4>Disputes / qualification work</h4>'+listing(x['disputes'])+'</article>'
 b+='<h2>Canonical candidates and missing warrants</h2><p>Canonical matches are provisional relationships, never qualified science.</p>'+listing([m['microtopic_id']+' / '+m['capability_id']+' · '+m['relationship'] for m in d['binding']['canonical_matches']])+listing(d['binding']['canonical_gaps'])
 for w in d['warrants']:
  b+='<article id="'+E(w['id'])+'"><h3>'+E(w['id']+' · '+w['qualification'])+'</h3><p>'+E(w['needed_reason'])+'</p><p>Support: '+linked(w['unit_refs'])+'; reference leads (unqualified): '+linked(w['reference_unit_refs'])+'; claims: '+linked(w['claim_refs'])+'</p>'+listing(w['conditions'])+'<p><strong>Unresolved:</strong> '+E(w['gap'])+'</p></article>'
 b+='<h2>Construction requirements and dependencies</h2>'
 for s in c['steps']:
  b+='<article id="'+E(s['id'])+'"><h3>'+E(s['id']+' · '+s['role'])+'</h3><p>'+E(s['requirement'])+'</p><p><strong>Why:</strong> '+E(s['why_needed'])+'</p><p>Depends on '+linked(s['depends_on'])+'; source '+linked(s['unit_refs'])+'; claims '+linked(s['claim_refs'])+'; warrant requirements '+linked(s['warrant_refs'])+'</p></article>'
 b+='<h2>Representation and source-figure obligations</h2>'
 sources={s['id']:s for s in d['sources']}
 for r in c['representation_needs']:
  b+='<article><h3>'+E(r['status'])+'</h3><p>'+E(r['requirement'])+'</p>'
  if r['asset_ref']:b+='<img src="'+E(sources[r['asset_ref']]['path'])+'" alt="Retained derived source figure; correspondence unreviewed">'
  b+=listing([x['symbol']+' → '+x['element']+': '+x['in_words'] for x in r['correspondence']])+'</article>'
 b+='<h2>Boundaries and distinct-example obligation</h2>'+listing(c['boundary_requirements'])+'<p>'+E(c['worked_example_requirement'])+'</p><h2>Wrong-path hypotheses and repair requirements</h2>'
 for x in c['wrong_path_candidates']:
  b+='<article><p><strong>Hypothesis:</strong> '+E(x['hypothesis'])+'</p><p><strong>Contrast:</strong> '+E(x['diagnostic_contrast'])+'</p><p><strong>Required repair:</strong> '+E(x['repair_requirement'])+'</p><p>Learner observation: NONE.</p></article>'
 b+='<h2>Independent-check designs</h2>'
 for x in c['check_requirements']:
  b+='<article><p>'+E(x['method'])+'</p><p><strong>Expected invariant:</strong> '+E(x['expected_invariant'])+'</p><p>'+E(x['independence_basis'])+'</p><p>DESIGN_ONLY; no academic check or learner result claimed.</p></article>'
 b+='<h2>Reviewed SL2 requirement mapping</h2><div class="hold">'+E(d['sl2_requirement_mapping']['status'])+'<p>'+E(d['sl2_requirement_mapping']['missing_input'])+'</p></div><h2>Native Core1A field targets</h2><div class="scroll"><table><tr><th>Existing property</th><th>Preparation pointer</th><th>Future action</th></tr>'
 for m in d['native_mapping']:b+='<tr><td>'+E(m['native_property'])+'</td><td>'+E(m['handoff_pointer'])+'</td><td>'+E(m['action'])+'</td></tr>'
 b+='</table></div><h2>Version-bound review requests</h2>'
 for q in d['review_requests']:b+='<details><summary>'+E(q['id']+' · '+q['target_pointer'])+'</summary><p>'+E(q['question'])+'</p><code>'+E(q['target_digest'])+'</code>'+listing(q['required_evidence'])+'</details>'
 b+='<h2>Open issues</h2>'+listing([x['id']+': '+x['detail'] for x in d['holds']])+'<h2>Exact retained source units</h2>'
 for u in d['units']:
  content=u['content'] if isinstance(u['content'],str) else json.dumps(u['content'],indent=2,ensure_ascii=False)
  b+='<details id="'+E(u['id'])+'"><summary>'+E(u['id']+' / '+u['source_ref']+' / '+json.dumps(u['locator']))+'</summary><pre>'+E(content)+'</pre><code>'+E(u['digest'])+'</code></details>'
 b+='<h2>Exposure and limitations</h2>'+listing(d['notes'])+'<p class="meta">Dependency fingerprint '+E(d['dependency_digest'])+'</p>'
 return page(d['id']+' author preparation',b)
def render(path,expected=None):
 path=Path(path).resolve();p=load(path);result=check_program(path,expected)
 if result['integrity']!='PASS':raise ValueError(json.dumps(result))
 root=path.parent;rows=[]
 outputs=[root/'index.html',*[inside(root,x['path']).with_suffix('.html') for x in p['records']]]
 if any(x.is_symlink() or not x.resolve().is_relative_to(root) for x in outputs):
  raise ValueError('Output must stay in the program folder without symlink targets')
 for ref in p['records']:
  fp=inside(root,ref['path']);d=load(fp);out=fp.with_suffix('.html');out.write_text(record(d,result['records'][d['id']]),encoding='utf-8',newline='\n')
  rows.append('<tr><td><a href="'+E(str(out.relative_to(root)).replace('\\','/'))+'">'+E(d['id']+' · '+d['title'])+'</a></td><td>'+str(len(d['claims']))+'</td><td>'+str(len(d['units']))+'</td><td>'+str(sum(w['qualification']=='MISSING' for w in d['warrants']))+'</td><td>UNQUALIFIED / SL2 pending</td></tr>')
 b='<h1>WPE · Source → Core1A preparation</h1><p>Ten-node author catalogue · R2 candidate</p><div class="hold"><strong>10/10 syllabus nodes accounted for; 0 qualified lessons</strong><br>30 interpreted claims · '+str(sum(len(load(inside(root,x['path']))['units']) for x in p['records']))+' exact units · nine source scans author-viewed. Source gaps and unqualified warrants remain explicit. Completed Core2 approval is still required before Core1A lesson construction; Core1A approval precedes Core1B. D3.1 PAUSED.</div>'
 b+='<p><a href="program.json">Program JSON</a> · <a href="../../references/protocol-r2.md">R2 protocol</a> · <a href="../../references/record-contract-r2.md">Record contract</a></p><div class="flow">'+''.join('<span>'+E(x)+'</span>' for x in ['Exact passages / scans','Claims / prerequisites','Candidate or missing warrants','Construction requirements','Conditions / boundaries','Wrong-path / repair designs','Independent-check designs','Reviewed SL2 join: pending'])+'</div>'
 b+='<p>Mechanical scope check '+E(result['scope_binding'])+'. This is an authoring input, not a learner course, exam bank or scientific approval.</p><div class="scroll"><table><tr><th>Open detailed dossier</th><th>Claims</th><th>Units</th><th>Missing warrant groups</th><th>Qualification</th></tr>'+''.join(rows)+'</table></div><h2>Printed scans versus extraction</h2>'
 for o in p['scan_observations']:b+='<article><a href="'+E(o['source_path'])+'">'+E(Path(o['source_path']).name)+'</a><p><strong>'+E(o['region'])+'</strong></p><p>'+E(o['observation'])+'</p><p>'+E(o['limits'])+'</p></article>'
 b+='<h2>Excluded or missing source scope</h2>'+listing(p['exclusions'])+'<h2>Complete source-line accounting</h2><p>All486 retained lines have an intake disposition. Accounting is not scientific coverage or completed teaching.</p><table><tr><th>Lines</th><th>Role</th><th>Nodes</th><th>Reason</th></tr>'
 for seg in p['line_dispositions']:b+='<tr><td>'+E(str(seg['start'])+'–'+str(seg['end']))+'</td><td>'+E(seg['disposition'])+'</td><td>'+E(', '.join(seg['node_refs']))+'</td><td>'+E(seg['reason'])+'</td></tr>'
 b+='</table>';(root/'index.html').write_text(page('WPE source preparation R2',b),encoding='utf-8',newline='\n');return result
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('program',type=Path);ap.add_argument('--expected-sha256');a=ap.parse_args();print(json.dumps(render(a.program,a.expected_sha256),indent=2))
