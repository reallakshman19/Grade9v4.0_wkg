"""Build a private textbook Core2 candidate; never edit source or shared code."""
from pathlib import Path
import copy, hashlib, html, json, re, shutil, sys

ROOT=Path(__file__).resolve().parent
REPO=Path(r'C:\CodeC\Grade9v3.5')
SOURCE=Path(r'D:\CodeD\g9v3.5\chatgpt\output\WPE_Question_Bank_and_Book_2026-10-30\02_Book_and_Syllabus\01_Chapter_Extract\work_energy_power_extracted')
sys.path.insert(0,str(REPO))
from Shared.tools import owner_bank

def sha(b): return hashlib.sha256(b).hexdigest()
def digest(v): return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Existing exact source files only. The retained generator is not executed.
pins=[]
paths=[SOURCE/'work_energy_power.md',*sorted(SOURCE.glob('page_*.jpg')),*sorted((SOURCE/'images').glob('*.svg'))]
for src in paths:
 dst=ROOT/'sources'/src.relative_to(SOURCE);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 pins.append({'original':str(src),'retained':dst.relative_to(ROOT).as_posix(),'sha256':sha(src.read_bytes()),'bytes':src.stat().st_size})
canonical=REPO/'Physics/library/phy-work-energy-power.v1.json'
for src,name in [(canonical,'canonical-original.json'),(REPO/'Shared/library/package.schema.json','package.schema.json'),(REPO/'golden/units/G-CORE2-R2/core 2 template.zip','core2-template.zip'),(REPO/'Shared/vocabularies/learner-question-metadata.v1.json','learner-question-metadata.v1.json')]:
 dst=ROOT/'review'/name;shutil.copy2(src,dst);pins.append({'original':str(src),'retained':dst.relative_to(ROOT).as_posix(),'sha256':sha(src.read_bytes()),'bytes':src.stat().st_size})
for name in ['render_core.py','core2_v2.py','owner_bank.py','learner_metadata.py','product_manifest.py','product_coverage.py','web_blueprint_contract.py']:
 src=REPO/'Shared/tools'/name;shutil.copy2(src,ROOT/'review'/name);pins.append({'original':str(src),'retained':'review/'+name,'sha256':sha(src.read_bytes()),'bytes':src.stat().st_size})
for name in ['interactive-page-blueprints.v1.json']:
 src=REPO/'Shared/web'/name;shutil.copy2(src,ROOT/'review'/name);pins.append({'original':str(src),'retained':'review/'+name,'sha256':sha(src.read_bytes()),'bytes':src.stat().st_size})
save(ROOT/'review/SOURCE_PINS.json',pins)

text=(SOURCE/'work_energy_power.md').read_text(encoding='utf-8')
matches=list(re.finditer(r'^### Illustration (\d+).*$',text,re.M))
blocks={}
for i,m in enumerate(matches):
 end=matches[i+1].start() if i+1<len(matches) else len(text)
 # An illustration ends before the next numbered chapter section.
 nxt=re.search(r'^## (?:\d+\.|\d+\s)',text[m.end():end],re.M)
 if nxt:end=m.end()+nxt.start()
 raw=text[m.start():end].rstrip();raw=re.sub(r'\n---\s*$','',raw).rstrip()
 solution=re.search(r'^\*\*Solution[^\n]*\*\*[^\n]*\n',raw,re.M)
 assert solution
 question=raw[raw.index('**Problem**:')+len('**Problem**:'):solution.start()].strip()
 # Remove the trailing divider but keep exact original question content separately.
 working=raw[solution.start():].strip()
 # Contextual TIP is not part of the supplied answer for Illustration 2.
 working=working.split('> [!TIP]')[0].rstrip()
 blocks[int(m.group(1))]={'raw':raw,'question':question,'source_answer':working,'line_start':text[:m.start()].count('\n')+1,'line_end':text[:m.start()+len(raw)].count('\n')+1}
assert set(blocks)=={1,2,3,4,5,6,11,12}

# Interpretive metadata is author-proposed. Each route is source-derived packaging,
# not a claim that this exact prose or additional check was printed in the book.
spec={
1:dict(title='Constant-force work in three dimensions',cap='WORK-DIRECTION',nodes=['WPE-N01'],operation='APPLY',scores=[1,1,1,1,1],pages=[2],answer='W = -24 J.',crux=0,
 evidence=['Choose constant-force dot product from the stated force and two positions.','Translate endpoint positions into displacement.','Use displacement before evaluating work.','Evaluate three signed products and their sum.','Reversing displacement reverses the work sign.'],
 moves=[('REPRESENT','Subtract initial position from final position.','Displacement is the change of position, not the final position itself.','The two supplied position vectors','s = (4, -8, 8) m.'),('CONNECT','Take the dot product of force and displacement.','The force is constant and the question asks its work.','F = (2, 3, -1) N and s','W = 2(4) + 3(-8) - 1(8).'),('TRANSFORM','Evaluate the signed sum.','Each Cartesian term is a force component times the matching displacement component.','The three signed products','W = -24 J.')],
 support=[('Which two positions define the displacement?','Use the final and initial positions in their stated order.'),('Which components need to be paired?','Keep Cartesian component pairs and their signs together.')],
 check='Author check: reversing the path gives +24 J for the same constant force; the unit is N m = J.',trap='Using the final position instead of the displacement.',issues=['Printed and extracted wording are not verbatim identical; this reader preserves the supplied extraction.']),
2:dict(title='Tension, gravity and net work',cap='NET-WORK-SIGN',nodes=['WPE-N01','WPE-N03'],operation='APPLY',scores=[1,1,2,1,1],pages=[2,3],answer='T = 59 N; tension work = 147.5 J; gravity work = -122.5 J; net work = 25 J.',crux=0,
 evidence=['Find tension from the upward acceleration before calculating its work.','Translate upward and downward forces into signed work.','Coordinate force balance, two individual works and their net.','Routine multiplication and signed addition.','Confusing individual work with net work changes the result.'],
 moves=[('CONNECT','Use T - mg = ma to determine tension.','The block accelerates upward under tension and gravity.','m = 5 kg, g = 9.8 m/s², a = 2 m/s²','T = 5(9.8 + 2) = 59 N.'),('TRANSFORM','Calculate work separately for tension and gravity.','Their forces have opposite directions relative to upward displacement.','s = 2.5 m','W_T = 147.5 J and W_g = -122.5 J.'),('VERIFY','Add the individual works and compare with net-force work.','Work is additive for the forces acting on this particle model.','W_T and W_g','W_net = 25 J = ma s.')],
 support=[('Which force does the first part ask about?','Distinguish tension from the net force before calculating work.'),('How do the two force directions compare with the motion?','Track each force separately relative to the same upward displacement.')],
 check='Author check: ma s = 5 × 2 × 2.5 = 25 J, agreeing with the signed work sum.',trap='Taking tension equal to weight despite the stated acceleration.',postfig='fig_03_fbd_string_raising.svg',issues=['The scan puts g = 9.8 in the solution rather than the printed stem; the extraction includes it as a given.','Derived FBD includes T - mg = ma, so it is solution-only.']),
3:dict(title='Position-dependent force',cap='WORK-DIRECTION',nodes=['WPE-N02'],operation='APPLY',scores=[1,1,1,1,0],pages=[3,4],answer='W = 21 J.',crux=0,
 evidence=['Identify variable-force work rather than one constant-force substitution.','Translate F(x) into a bounded work integral or equivalent area.','Integrate before substituting the bounds.','Routine linear-polynomial integration and evaluation.','No extra hidden domain exception is required.'],
 moves=[('CONNECT','Write work as the integral of the stated force over x.','The force and displacement are along the x direction and force varies with x.','F(x) = 10 + 0.50x N, x from 0 to 2 m','W = integral from 0 to 2 of (10 + 0.50x) dx.'),('TRANSFORM','Evaluate the definite integral.','An antiderivative is 10x + 0.25x².','The stated bounds','W = 20 + 1 = 21 J.')],
 support=[('Does the force stay constant?','Compare its expression at the beginning and end of the interval.'),('What does work accumulate over the stated displacement?','Use the whole interval rather than only an endpoint force.')],
 check='Author check: the linear force rises from 10 N to 11 N; trapezoid area is 10.5 N × 2 m = 21 J.',trap='Multiplying only the final force by the whole displacement.',issues=['The canonical work-direction capability is a prerequisite bridge, not a qualified variable-force warrant.']),
4:dict(title='Work on a rough incline',cap='WORK-DIRECTION',nodes=['WPE-N01','WPE-N09'],operation='APPLY',scores=[1,1,1,1,1],pages=[4,5],answer='Gravity work = 70.56 J; friction work = -18.816 J; normal work = 0 J.',crux=0,
 evidence=['Apply work separately to gravity, friction and the normal.','Resolve the vertical force relative to motion down the incline.','Obtain the normal before kinetic friction and its work.','Routine multi-operation numerical evaluation.','Signs and the normal being perpendicular matter.'],
 moves=[('REPRESENT','Identify the angle each force makes with the displacement.','The plane is fixed and the block moves down it.','Inclination 37° and sliding direction','Gravity has a downhill component; friction is uphill; normal is perpendicular.'),('CONNECT','Use R = mg cos(37°) and f = μR.','There is no acceleration perpendicular to the fixed straight plane in this model.','m = 4 kg, μ = 0.2, cos(37°) = 0.8','R = 31.36 N and f = 6.272 N.'),('TRANSFORM','Compute the three signed works.','Use the same 3 m displacement for all forces and their respective directions.','sin(37°) = 0.6 and s = 3 m','W_g = 70.56 J; W_f = -18.816 J; W_N = 0 J.')],
 support=[('Which force directions are fixed by the incline?','Distinguish normal and tangential directions.'),('Which force determines the sliding-friction magnitude?','Use the contact normal, with the stated coefficient.')],
 check='Author check: net work is 51.744 J; normal work vanishes by perpendicularity, not because normal force is zero.',trap='Using the full weight as the friction-determining normal force.',prefig='fig_06_incline_block.svg',postfig='fig_07_incline_fbd.svg',issues=['Stationary-plane kinetic-friction model only; no universal claim that friction work is always negative.','The extraction supplies trigonometric approximations from the printed working.','Derived FBD includes final work relations and is solution-only.']),
5:dict(title='Gravitational power at the bottom of an incline',cap='POWER-RATES',nodes=['WPE-N10','WPE-N08'],operation='APPLY',scores=[1,1,2,1,1],pages=[5],answer='Source result, conditional on release from rest: P = mg sin(θ) sqrt(2gl sin(θ)).',crux=0,
 evidence=['Combine bottom speed with power of the named gravitational force.','Translate the incline geometry into h = l sin(θ).','Coordinate energy or kinematics with a force-velocity projection.','Routine symbolic substitution and simplification.','Force attribution matters; the missing initial speed is a source defect, not a demand bonus.'],
 moves=[('DECIDE','State that the source solution assumes release from rest.','The supplied stem does not specify initial speed, so its displayed result is conditional.','Fixed smooth incline and source working','Under that additional assumption, v_bottom = sqrt(2gl sin(θ)).'),('CONNECT','Project gravity onto velocity along the incline.','Power of gravity is F_g dot v, not weight magnitude times speed without a projection.','v_bottom along the incline','P = mg v_bottom sin(θ).'),('TRANSFORM','Insert the conditional bottom speed.','This follows only under the initial-rest interpretation used by the source.','The preceding two relations','P = mg sin(θ) sqrt(2gl sin(θ)).')],
 support=[('What information about the motion is explicitly supplied?','Check whether the initial state is determined before using the source result.'),('Whose power is requested?','Keep gravitational power distinct from an unnamed applied force.')],
 check='Author check: for nonzero initial speed u, the same smooth-plane model instead uses v_bottom² = u² + 2gl sin(θ); the printed result is the u = 0 case.',trap='Treating the conditional zero-initial-speed answer as uniquely determined by the original stem.',issues=['UNDERDETERMINED_STEM: initial speed is absent; displayed source answer assumes release from rest.']),
6:dict(title='Net power during nonuniform circular motion',cap='POWER-RATES',nodes=['WPE-N10','WPE-N04'],operation='APPLY',scores=[1,1,2,1,1],pages=[5],answer='Source choice (B): P = m k² r² t.',crux=0,
 evidence=['Net power must include the speed-changing force, not only the radial component.','Convert centripetal acceleration into speed using a_c = v²/r.','Find speed, differentiate it, and combine tangential force with velocity.','Routine time differentiation and product.','Zero radial power does not mean zero net power.'],
 moves=[('REPRESENT','Use a_c = v²/r to infer the speed law.','The radius is constant. For the source convention k ≥ 0 and t ≥ 0, speed is krt.','a_c = k²rt²','v² = k²r²t².'),('CONNECT','Separate radial and tangential contributions to power.','The radial contribution is perpendicular to velocity; changing speed still has a tangential contribution.','v = krt for the source convention','a_t = kr and P = F_t v.'),('TRANSFORM','Evaluate tangential power.','F_t = ma_t in the particle model.','F_t = mkr and v = krt','P = m k² r² t, option (B).')],
 support=[('Does centripetal acceleration describe all of the acceleration?','Consider whether the speed changes as time changes.'),('Which force component is perpendicular to velocity?','Distinguish that component from the one changing the speed.')],
 check='Author check: K = (1/2)m k²r²t²; dK/dt = m k²r²t, agreeing with the source choice.',trap='Selecting zero because the centripetal contribution alone has zero power.',issues=['The source convention uses nonnegative elapsed time; speed is a magnitude.']),
11:dict(title='A uniform chain slipping off a table',cap='MECH-ENERGY-CONDITION',nodes=['WPE-N06','WPE-N08'],operation='MODEL',scores=[2,2,2,1,1],pages=[9],answer='Source result, conditional on zero initial kinetic energy and its ideal chain model: K_final = (4/9)mgl.',crux=0,
 evidence=['Choose a distributed-energy model rather than placing the whole mass at one arbitrary height.','Construct initial and final mass-height distributions with a consistent zero.','Coordinate density, two potential-energy integrals and energy balance.','Routine quadratic integration; not scored high merely for calculus.','Initial kinetic energy and ideal contact assumptions affect the final result.'],
 moves=[('REPRESENT','Set table height as zero and use uniform linear mass density m/l.','Different parts of the chain have different heights.','Initial hanging length l/3 and full length l','dm = (m/l) dx and dU = -(m/l)g x dx.'),('TRANSFORM','Evaluate the initial and final potential energies.','Use hanging-depth bounds 0 to l/3 initially and 0 to l finally.','The uniform-density model','U_initial = -mgl/18; U_final = -mgl/2.'),('CONNECT','Apply the energy balance with the source initial-rest assumption.','The printed solution explicitly takes initial kinetic energy as zero; the ideal contact model admits no dissipative work.','The two potential energies and K_initial = 0','K_final = U_initial - U_final = (4/9)mgl.')],
 support=[('Is the whole chain at one height?','Track the distribution of mass above and below the chosen reference level.'),('What initial kinetic energy is actually specified?','Compare the problem statement with the assumption used in the supplied working.')],
 check='Author check: using the hanging segment centre of mass gives U_initial = -(m/3)g(l/6), and U_final = -mg(l/2), the same change.',trap='Putting all initial mass at the centre of the hanging part.',postfig='fig_09_overhanging_chain.svg',issues=['Initial rest appears in the printed solution, not in the supplied extracted stem.','Flexible-chain contact/edge idealization and lossless energy transfer require distinct review.','The derived SVG prints the final answer and is solution-only; a safe original-figure projection is pending.']),
12:dict(title='A block pushed by a compressed spring',cap='MECH-ENERGY-CONDITION',nodes=['WPE-N02','WPE-N06','WPE-N08'],operation='MODEL',scores=[2,1,2,2,2],pages=[9],answer='Extracted conditional model: v(x) = sqrt((k/m)[L₀²/4 - (L₀-x)²]) for L₀/2 ≤ x ≤ L₀; v(x) = (L₀/2)sqrt(k/m) after detachment.',crux=1,
 evidence=['Select a unilateral contact model: pushed against the spring does not mean permanently attached.','Translate wall distance into spring compression while contact lasts.','Coordinate initial energy, contact phase and subsequent free motion.','Construct and bound a piecewise symbolic expression.','Detachment at natural length changes the governing expression.'],
 moves=[('CONNECT','Determine initial elastic energy from compression L₀/2.','The extraction specifies release from rest and a light spring in the ideal frictionless model.','Initial compression L₀/2','E_initial = kL₀²/8.'),('DECIDE','Separate contact motion from motion after loss of contact.','A block merely pushed against the spring is not pulled back once it separates.','Wall distance x and natural length L₀','Contact range L₀/2 ≤ x ≤ L₀; thereafter no spring force on the detached block.'),('TRANSFORM','Solve the energy relation during contact and preserve speed after detachment.','While contact lasts, compression is L₀-x; afterward the horizontal net force vanishes in this model.','(1/2)mv² + (1/2)k(L₀-x)² = kL₀²/8','The piecewise velocity expression in the extracted answer.')],
 support=[('What does the text say about how block and spring are connected?','Distinguish being pushed against a spring from being permanently attached.'),('Does one interaction law apply over the whole trajectory?','Locate the point where contact can end without changing the original givens.')],
 check='Author check: the expression gives v = 0 at x = L₀/2 and joins continuously to (L₀/2)sqrt(k/m) at x = L₀. The formula is not extended into x < L₀/2.',trap='Continuing a restoring spring force after the unconnected block has detached.',prefig='fig_10_spring_block_wall.svg',issues=['The printed solution is qualitative; the extraction adds the piecewise algebra and explicit initial-rest wording.','The printed assertion of no external forces must be read as no external energy transfer in this ideal model; gravity and table normal exist.'])
}

component_names=['concept_model_selection','representation_translation','reasoning_chain_length','algebra_computational_load','trap_exception_sensitivity']
intake={'schema':'wpe-textbook-intake/v1','inputs':{'questions':[]},'source_role':'OWNER_SUPPLIED_TEXTBOOK_EXTRACT','official_exam_status':'UNVERIFIED'}
for n,b in blocks.items():
 stem=b['question']
 stem=re.sub(r'!\[[^\]]*\]\([^)]*\)','',stem)
 stem=re.sub(r'<div.*?</div>','',stem,flags=re.S).strip()
 options=[]
 if n==6:
  first=stem.index('(A)');opts=stem[first:];stem=stem[:first].rstrip()
  options=[m.group(0).strip() for m in re.finditer(r'\([A-D]\).*?(?=\n\([A-D]\)|\Z)',opts,re.S)]
 intake['inputs']['questions'].append({'id':f'TB-WPE-ILL-{n:02}','label':f'Illustration {n}','text':stem})
 b['native_stem']=stem;b['options']=options
intake['intake_digest']='sha256:'+digest(intake['inputs'])
bank=owner_bank.new(intake,'wpe-textbook-r1')
bank['title']='WPE textbook illustrations — private Core2 review candidate'
bank['extensions']={'source_role':'OWNER_SUPPLIED_TEXTBOOK_EXTRACT','academic_status':'UNREVIEWED','classification_status':'AUTHOR_PROPOSED','official_exam_status':'UNVERIFIED'}
package=json.loads(canonical.read_text(encoding='utf-8-sig'))
package['package_id']='WPE-TEXTBOOK-CORE2-R1-CONTEXT';package['title']='Work, Energy and Power — textbook Core2 candidate';package['status']='CANDIDATE'
# This context copy does not claim newly qualified canonical content.
package['extensions']['wpe:textbook_context']={'canonical_sha256':sha(canonical.read_bytes()),'canonical_status':'CANDIDATE','purpose':'Native rendering context only; no Core1A lesson emitted.'}
package['questions']=[]
package['representations']=[]
package['resources']=[{'id':'TB-WPE-EXTRACT','version':'0.1.0','status':'CANDIDATE','source_refs':[],'evidence_refs':[],'extensions':{'wpe:provenance':'OWNER_SUPPLIED_TEXTBOOK_EXTRACT','wpe:printed_identity':'NOT_ESTABLISHED'},'title':'Supplied Work, Energy and Power chapter extract','origin':'LOCAL','locator':(ROOT/'sources/work_energy_power.md').as_posix(),'edition':'Unidentified supplied book; exact saved bytes retained','section':'Illustrations 1–6, 11–12','last_checked':'2026-10-30','access_status':'SECTION_INSPECTED','rights_status':'Owner-supplied private review; no public redistribution in this routine','snapshot_ref':None,'snapshot_digest':None,'role':['QUESTION_BANK'],'supports_claims':[],'entry_capabilities':[],'depth':['ADVANCED'],'selection_reason':'Existing textbook questions explicitly selected by Owner for Core2 preparation.','fallback':[]}]
for n,s in spec.items():
 for key in ['prefig','postfig']:
  if key not in s:continue
  fname=s[key];rid='REP-TB-'+fname.removesuffix('.svg').upper().replace('_','-')
  if any(r['id']==rid for r in package['representations']):continue
  package['representations'].append({'id':rid,'version':'0.1.0','status':'CANDIDATE','source_refs':[],'evidence_refs':[],'extensions':{'wpe:asset_provenance':'EXISTING_EXTRACT_GENERATED_REDRAW','wpe:independent_visual_review':'NOT_RUN'},'kind':'SOURCE_DERIVED_REDRAW','purpose':'Supplied extract diagram; generated redraw rather than original printed artwork.','required_elements':[],'relation_refs':[],'read_order':[],'instance_constraints':[],'accessibility':['Retain the supplied SVG accessible text.'],'misleading_alternatives':[],'rendered_asset_refs':[(ROOT/'sources/images'/fname).as_posix()],'scene_instances':[]})
  s[key+'_ref']=rid

sidecars=[]
for q,(n,b) in zip(bank['questions'],blocks.items()):
 s=spec[n];qid=f'TB-WPE-ILL-{n:02}';q['id']=qid;q['original_identifier']=f'Textbook extract · Illustration {n} · candidate, independently unreviewed'
 scores=dict(zip(component_names,s['scores']));score=sum(s['scores']);band='D1' if score<=2 else 'D2' if score<=5 else 'D3' if score<=7 else 'D4'
 diff={'band':band,'score':score,'components':scores,'basis':'Author proposal for the exact supplied extract before support; independent adjudication pending. '+s['title'],'component_evidence':dict(zip(component_names,s['evidence']))}
 moves=[]
 for i,(kind,action,why,inputs,output) in enumerate(s['moves']):
  move={'id':f'{qid}-M{i+1}','kind':kind,'action':action,'why_valid':why,'inputs':[inputs],'output':output,'source_ref':f'TB-WPE-EXTRACT#illustration-{n}'}
  moves.append(move)
 scaffolds=[]
 for i,(prompt,body) in enumerate(s['support']):
  scaffolds.append({'prompt':prompt,'text':body,'learner_stage':'REPRESENTATION' if i==0 else 'FIRST_MOVE','support_kind':'REPRESENT' if i==0 else 'CONNECT','reveals':'METHOD','supports_move_ref':moves[min(i,len(moves)-1)]['id']})
 q.update({'version':'0.1.0','status':'CANDIDATE','source_refs':['TB-WPE-EXTRACT'],'evidence_refs':[],'origin':'ORIGINAL','origin_ref':'TB-WPE-EXTRACT','subparts':[],'options':b['options'],'conditions':['Private textbook candidate. Source wording is the supplied extraction; equivalence to the printed page is not certified.','JEE labels printed in the book have not been authenticated against an examination paper.','Classification and source-derived working are author proposals; no independent admission or grading is claimed.'], 'figure_refs':[s['prefig_ref']] if s.get('prefig_ref') else [],'primary_capability_ref':'CAP-WEP-'+s['cap'],'secondary_capability_refs':[],'family_ref':'FAM-PHY-WEP-PRACTICE','adaptation':None,'exposure':[],'hints':[],'scaffolds':scaffolds,'response':{'type':'single_choice' if n==6 else 'free_response'},'learner_question_type':'single_correct_mcq' if n==6 else 'constructed_response','difficulty':diff,
 'answer':{'kind':'MODEL_RESPONSE','summary':s['answer'],'reasoning':[m['action']+' '+m['output'] for m in moves],'reasoning_route':moves,'crux_move_ref':moves[s['crux']]['id'],'check':s['check'],'acceptable_alternatives':[],'subpart_answers':[],'verification_status':'DISPUTED' if n in [5,11,12] else 'CHECKED_BY_AUTHOR'}})
 # Surface source limitations without silently amending the problem's givens.
 q['conditions'] += ['Source review: '+x for x in s['issues']]
 ext=q['extensions'];ext['grade9v3:analysis'].update({'topic':'Work, Energy and Power','exam_source_badge':f'Supplied textbook extract · Illustration {n}','learner_question_type':q['learner_question_type'],'difficulty':diff,'common_wrong_route':s['trap'],'stable_crux_move':moves[s['crux']]['action']})
 ext['wpe:textbook_source']={'role':'OWNER_SUPPLIED_TEXTBOOK_EXTRACT','printed_exam_label':'JEE Advanced' if n in [2,5,12] else 'JEE Main','exam_identity':'UNAUTHENTICATED_SOURCE_LABEL','extract_sha256':sha(text.encode()),'line_start':b['line_start'],'line_end':b['line_end'],'scan_pages':s['pages'],'printed_wording_equivalence':'UNREVIEWED','source_answer_sha256':sha(b['source_answer'].encode()),'source_question_sha256':sha(b['question'].encode()),'support_provenance':'AUTHOR_SOURCE_DERIVED','solution_provenance':'AUTHOR_STRUCTURED_FROM_EXTRACT_NOT_VERBATIM_PRINT'}
 ext['grade9v3:core2_support_plan']={'protected_move_refs':[moves[s['crux']]['id']],'support_completions':[{'support_ref':f'scaffolds[{i}]','completed_move_refs':[],'availability':'PRE_ATTEMPT_SAFE'} for i in range(len(scaffolds))]}
 if s.get('postfig_ref'):q['representation_roles']={'bound_ref':s['postfig_ref']}
 # Exact math literals are typeset by the governed renderer, not a remote CDN.
 ext['grade9v3:math_spans']=[]
 for target,value in [('stem',q['stem']),*[(f'option:{i}',v) for i,v in enumerate(q['options'])]]:
  seen=set()
  for m in re.finditer(r'\$([^$]+)\$',value):
   if m.group(0) in seen:continue
   seen.add(m.group(0));ext['grade9v3:math_spans'].append({'target':target,'literal':m.group(0),'tex':m.group(1),'display':False})
 side={'profile':'wpe-textbook-core2-review/v1','id':qid,'illustration':n,'title':s['title'],'source':b,'scan_pages':s['pages'],'sl1':{'question_role':'OWNER_SUPPLIED_TEXTBOOK_EXTRACT','source_document_identity':'EXACT_SAVED_EXTRACT','printed_equivalence':'PENDING','exam_identity':'UNVERIFIED','official_key':'NOT_ESTABLISHED','question_payload_sha256':digest({'stem':q['stem'],'options':q['options'],'raw_question':b['question']}),'source_answer_sha256':sha(b['source_answer'].encode()),'assets':[s[k] for k in ['prefig','postfig'] if k in s],'first_try':'CANDIDATE_WITH_SOURCE_WARNINGS' if n not in [5,11,12] else 'CONDITIONAL_SOURCE_DEFECT'},'sl2':{'mode':'QUESTION','operation_proposal':s['operation'],'difficulty_proposal':diff,'decisive_move':moves[s['crux']]['action'],'input_roles':[m['inputs'] for m in moves],'output_role':s['answer'],'competing_operation':'APPLY' if s['operation']=='MODEL' else 'MODEL','competition_reason':'An explicit distributed/contact representation is decisive.' if s['operation']=='MODEL' else 'The governing model is familiar and its execution is the principal demand.','review':'AUTHOR_PROPOSED_NOT_INDEPENDENT','learner_observation':None},'qrt':{'placement':'PROVISIONAL','source_role':'TEXTBOOK_QUESTION','exam_21_admission':False,'reviewed_construction_join':'PENDING','syllabus_nodes':s['nodes']},'issues':s['issues'],'admission':'NONE','native_question_sha256':digest(q)}
 sidecars.append(side)

save(ROOT/'native/intake.json',intake);save(ROOT/'native/bank.json',bank);save(ROOT/'native/records.json',package)
for rep in package['representations']:
 rep['required_elements']=['The exact retained SVG geometry and labels; generated redraw status remains explicit.']
 rep['read_order']=['Read the stated geometry and labelled physical quantities.']
 rep['instance_constraints']=['Bound only to the illustration whose source includes this retained redraw.']
save(ROOT/'native/records.json',package)
manifest={'schema':'product-manifest/v1','product_id':'WPE-TEXTBOOK-CORE2-R1','subject':'Physics','home_href':'../index.html','question_bank_href':'../review.html','package_refs':[(ROOT/'native/records.json').as_posix()],'bank_refs':[(ROOT/'native/bank.json').as_posix()],'output_roles':['CORE2'],'selection':{'microtopics':[],'core2':[q['id'] for q in bank['questions']],'core2a':[],'core2b':[]},'coverage':{'omitted':{},'sources':[{'source':'Supplied chapter extract, Illustrations 1–6 and 11–12','kind':'TEXTBOOK','questions':8,'ingested':8,'status':'INGESTED','reason':'All eight exact supplied illustrations retained; no claim about missing illustrations or examination identity.'}]}}
save(ROOT/'native/manifest.json',manifest);save(ROOT/'review/questions.json',sidecars)
schema=json.loads((REPO/'Shared/library/package.schema.json').read_text(encoding='utf-8-sig'))
from jsonschema import Draft202012Validator
v=Draft202012Validator(schema)
errs=[]
for q in bank['questions']:
 for e in v.evolve(schema=schema['$defs']['question']).iter_errors(q):errs.append(q['id']+': '+e.message)
errors=owner_bank.check(bank,intake=intake,complete=False)
save(ROOT/'review/NATIVE_INPUT_CHECK.json',{'question_errors':errs,'owner_bank_errors':errors,'question_count':len(bank['questions']),'semantic_review':'NOT_RUN'})
if errs or errors:raise ValueError((errs+errors)[:8])
print('Built eight source-bound native questions and review sidecars. No academic admission.')
