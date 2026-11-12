from pathlib import Path
import hashlib,html,json,re,shutil,sys,unittest,copy
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
REPO=Path(r'C:\CodeC\Grade9v3.5')
sys.path.insert(0,str(REPO))
from Shared.tools import owner_bank,core2_v2
from jsonschema import Draft202012Validator

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bank=read(ROOT/'native/bank.json');side=read(ROOT/'review/questions.json');intake=read(ROOT/'native/intake.json');package=read(ROOT/'native/records.json')
for rel in ['css/modern-learner.css','css/tablet-12-7.css','js/display-controls.js','js/site-header.js']:
 dst=ROOT/rel;dst.parent.mkdir(exist_ok=True);shutil.copy2(REPO/'public'/rel,dst)

def errors(b=bank,s=side):
 result=owner_bank.check(b,intake=intake,complete=False)
 if len(b['questions'])!=8 or len({q['id'] for q in b['questions']})!=8:result.append('question denominator/uniqueness')
 idx={x['id']:x for x in s}
 for q in b['questions']:
  if q['id'] not in idx:result.append('missing sidecar');continue
  row=idx[q['id']]
  if digest(q)!=row['native_question_sha256']:result.append(q['id']+': native dependency changed')
  if sha(row['source']['source_answer'].encode())!=row['sl1']['source_answer_sha256']:result.append(q['id']+': source answer changed')
  if digest({'stem':q['stem'],'options':q['options'],'raw_question':row['source']['question']})!=row['sl1']['question_payload_sha256']:result.append(q['id']+': source question changed')
  if row['admission']!='NONE' or row['qrt']['exam_21_admission']:result.append('unsupported admission')
  if row['sl2']['learner_observation'] is not None:result.append('no original P1 exists')
  if row['sl2']['difficulty_proposal']!=q['difficulty']:result.append('difficulty mismatch')
 return result

class Checks(unittest.TestCase):
 def test_actual_dependency_and_native_intake(self):self.assertEqual(errors(),[])
 def test_exact_eight_identities(self):self.assertEqual({x['illustration'] for x in side},{1,2,3,4,5,6,11,12})
 def test_original_and_retained_bytes(self):
  for row in read(ROOT/'review/SOURCE_PINS.json'):
   self.assertEqual(sha(Path(row['original']).read_bytes()),row['sha256']);self.assertEqual(sha((ROOT/row['retained']).read_bytes()),row['sha256'])
 def test_question_and_package_schema(self):
  schema=read(ROOT/'review/package.schema.json');Draft202012Validator(schema).validate(package)
  v=Draft202012Validator({'$ref':'#/$defs/question','$defs':schema['$defs']})
  for q in bank['questions']:v.validate(q)
 def test_stem_mutation_rejected(self):
  b=copy.deepcopy(bank);b['questions'][0]['stem']+=' changed';self.assertTrue(errors(b))
 def test_option_mutation_rejected(self):
  b=copy.deepcopy(bank);b['questions'][5]['options'][1]='Changed';self.assertTrue(errors(b))
 def test_key_mutation_rejected(self):
  b=copy.deepcopy(bank);b['questions'][5]['answer']['summary']='Choice D';self.assertTrue(errors(b))
 def test_source_working_mutation_rejected(self):
  s=copy.deepcopy(side);s[0]['source']['source_answer']+=' altered';self.assertTrue(errors(s=s))
 def test_duplicate_identity_rejected(self):
  b=copy.deepcopy(bank);b['questions'][1]['id']=b['questions'][0]['id'];self.assertTrue(errors(b))
 def test_invented_exam_field_rejected(self):
  b=copy.deepcopy(bank);b['questions'][0]['extensions']['grade9v3:source_custody']['year']=2020;self.assertTrue(errors(b))
 def test_fake_admission_rejected(self):
  s=copy.deepcopy(side);s[0]['admission']='ADMITTED';self.assertTrue(errors(s=s))
 def test_fabricated_p1_rejected(self):
  s=copy.deepcopy(side);s[0]['sl2']['learner_observation']={'answer':'-24 J'};self.assertTrue(errors(s=s))
 def test_support_lane_and_crux_references(self):
  for q in bank['questions']:
   self.assertEqual(q['hints'],[]);self.assertEqual(len(core2_v2.project_solution(q['answer'])),len(q['answer']['reasoning_route']))
   rows=core2_v2.project_support(q);self.assertEqual(len(rows),2)
   self.assertTrue(all(x['provenance']==core2_v2.AUTHORED_CORE2_SUPPORT for x in rows))
 def test_demand_sum_and_band(self):
  for q in bank['questions']:
   d=q['difficulty'];n=sum(d['components'].values());self.assertEqual(n,d['score']);self.assertEqual(d['band'],'D1' if n<=2 else 'D2' if n<=5 else 'D3' if n<=7 else 'D4')
 def test_numeric_work_checks(self):
  self.assertEqual(2*4+3*(-8)-8,-24);self.assertEqual(Fraction(105,10)*2,21)
  self.assertEqual(5*(Fraction(98,10)+2)*Fraction(25,10),Fraction(295,2))
  self.assertEqual(4*Fraction(98,10)*3*Fraction(6,10),Fraction(7056,100))
  self.assertEqual(-Fraction(2,10)*4*Fraction(98,10)*Fraction(8,10)*3,-Fraction(18816,1000))
 def test_chain_distribution_check(self):self.assertEqual(Fraction(1,2)-Fraction(1,18),Fraction(4,9))
 def test_spring_endpoint_check(self):
  self.assertEqual(Fraction(1,4)-(1-Fraction(1,2))**2,0);self.assertEqual(Fraction(1,4)-(1-1)**2,Fraction(1,4))
 def test_conditional_stems_not_silently_fixed(self):
  for i in [4,6]:self.assertNotIn('from rest',bank['questions'][i]['stem'])
  self.assertTrue(any('initial speed is absent' in x for x in side[4]['issues']))
 def test_pre_attempt_answer_figures_absent(self):
  for i in [1,3,6]:
   q=bank['questions'][i];self.assertNotIn(q.get('representation_roles',{}).get('bound_ref'),q['figure_refs'])
  self.assertIn('4/9 mgl',(ROOT/'sources/images/fig_09_overhanging_chain.svg').read_text())
 def test_no_core1a_lesson_output(self):self.assertFalse((ROOT/'rendered/core1a.html').exists())

suite=unittest.defaultTestLoader.loadTestsFromTestCase(Checks)
res=unittest.TextTestRunner(verbosity=1).run(suite)
save(ROOT/'review/REGRESSION_RESULTS.json',{'tests':res.testsRun,'failures':len(res.failures),'errors':len(res.errors),'success':res.wasSuccessful(),'type':'AUTHOR_MECHANICAL_AND_LIMITED_ARITHMETIC_CHECKS','independent_review':'NOT_RUN','limitations':'Arithmetic checks do not qualify all science or authenticate printed/examination custody.'})
if not res.wasSuccessful():raise SystemExit(1)

esc=html.escape
style='body{font:17px/1.55 system-ui;color:#182a36;background:#f5f7fa;margin:0}main{max-width:1100px;margin:auto;padding:24px}a{color:#075cad}section,.card{background:white;border:1px solid #ccd7df;border-radius:10px;padding:20px;margin:20px 0}.hold{background:#fff3d9;padding:16px;border-left:5px solid #b87400}table{border-collapse:collapse;width:100%}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f8;padding:15px}summary{cursor:pointer;font-weight:650}svg,img{max-width:100%;height:auto}nav a{display:inline-block;padding:8px}code{overflow-wrap:anywhere}@media(max-width:600px){main{padding:12px}table{font-size:14px}td,th{padding:6px}}'
def page(title,body):return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><style>'+style+'</style><main><nav><a href="index.html">Overview</a><a href="rendered/core2.html">Core2 reader</a><a href="review.html">Source and label review</a><a href="concept.html">Revised concept</a></nav><h1>'+esc(title)+'</h1>'+body+'</main></html>'
gaps=read(ROOT/'rendered/render-receipt.json')['gaps']
rows=''.join('<tr><td><a href="rendered/core2.html#'+s['id']+'">Illustration '+str(s['illustration'])+'</a></td><td>'+esc(s['title'])+'</td><td>'+s['sl2']['operation_proposal']+' · '+s['sl2']['difficulty_proposal']['band']+'</td><td><a href="review.html#'+s['id']+'">'+str(len(s['issues']))+' source notes</a></td></tr>' for s in side)
body='<p class="hold"><strong>Private review candidate: eight textbook questions, zero independent admissions.</strong> Uses the actual governed Core2 renderer. This is a draft learner flow for Owner review, not a completed accepted course or an authenticated examination bank.</p><p>The supplied textbook now feeds both Core2 questions and Core1A preparation. These eight illustrations do not change the separate 21-question examination target. Core1A lessons are not authored; D3.1 remains paused.</p><p><a href="rendered/core2.html">Open the eight-question Core2 reader →</a></p><table><tr><th>Question</th><th>Topic</th><th>Author proposal</th><th>Evidence</th></tr>'+rows+'</table><section><h2>What you can review</h2><p>Exact extracted stem and options; typed commitment; two requested support prompts per question; staged structured working; source limitations; and source-answer evidence in the separate author view. Commitment neither grades the answer nor supplies independent P1 evidence.</p><h2>Open native build findings</h2><p>'+str(len(gaps))+' reference-depth findings remain. Missing pre-attempt representations and inherited SVG label overflow are recorded; no bypass or blueprint weakening was used.</p><ul>'+''.join('<li>'+esc(g['record']+': '+g['detail'])+'</li>' for g in gaps)+'</ul><p><a href="review/REGRESSION_RESULTS.json">Mechanical check results</a> · <a href="rendered/render-receipt.json">Native draft receipt</a> · <a href="CONCEPT_NOTE.md">Concept note Markdown</a></p></section>'
(ROOT/'index.html').write_text(page('WPE textbook → Core2: eight-question review',body),encoding='utf-8')
sections=[]
for s in side:
 scans=' '.join('<a href="sources/page_'+str(p).zfill(2)+'.jpg">Scan '+str(p)+'</a>' for p in s['scan_pages'])
 sections.append('<section id="'+s['id']+'"><h2>Illustration '+str(s['illustration'])+' — '+esc(s['title'])+'</h2><p><a href="rendered/core2.html#'+s['id']+'">Try in native reader</a> · '+scans+'</p><p class="hold">AUTHOR EVIDENCE VIEW: contains source answers. Printed exam labels are unverified. Extract-to-print equivalence remains pending; source wording and working below are exact saved extraction.</p><ul>'+''.join('<li>'+esc(x)+'</li>' for x in s['issues'])+'</ul><details><summary>Exact extracted question</summary><pre>'+esc(s['source']['question'])+'</pre></details><details><summary>Exact extracted source working — contains answer</summary><pre>'+esc(s['source']['source_answer'])+'</pre></details><h3>SL1-style custody</h3><pre>'+esc(json.dumps(s['sl1'],ensure_ascii=False,indent=2))+'</pre><h3>SL2 proposal and QRT join</h3><pre>'+esc(json.dumps({'SL2':s['sl2'],'QRT':s['qrt']},ensure_ascii=False,indent=2))+'</pre></section>')
(ROOT/'review.html').write_text(page('Textbook source and labelling review','<p>These are supplementary review sidecars, not independently reviewed native SL1/SL2 admissions. Source answers are deliberately confined to this author view and protected learner solutions.</p>'+''.join(sections)),encoding='utf-8')
(ROOT/'concept.html').write_text(page('Revised source routes','<pre>'+esc((ROOT/'CONCEPT_NOTE.md').read_text())+'</pre>'),encoding='utf-8')
seal={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [ROOT/'native/bank.json',ROOT/'native/records.json',ROOT/'native/intake.json',ROOT/'native/manifest.json',ROOT/'review/questions.json']}
save(ROOT/'review/DEPENDENCY_SEAL.json',{'files':seal,'trust':'LOCAL_AUTHOR_RECEIPT_ONLY','science':'UNREVIEWED'})
print('Rendered overview, evidence and revised concept; 20 checks complete.')
