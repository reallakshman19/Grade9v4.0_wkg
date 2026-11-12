"""Real retained WPE positives and synthetic mutations; none are exam evidence."""
from pathlib import Path
import sys,copy,json,tempfile,shutil,unittest
S=Path(__file__).resolve().parents[1];sys.path.insert(0,str(S/'scripts'))
import check_program as c
from check_handoff import load,file_sha,digest,Invalid
P=S/'examples/wpe-source-program'

class RecordChecks(unittest.TestCase):
 def setUp(self):
  self.d=load(P/'handoffs/WPE-N01.json');self.root=P/'handoffs'
 def result(self,d=None):return c.check_record(d or self.d,self.root)
 def bad(self,code):
  r=self.result();self.assertEqual(r['integrity'],'INVALID',r);self.assertEqual(r['findings'][0]['code'],code,r)
 def test_real_all_ten_records_pass_with_hold(self):
  for ref in load(P/'program.json')['records']:
   r=c.check_record(load(P/ref['path']),(P/ref['path']).parent,P/ref['pins_path'],ref['pins_sha256'])
   self.assertEqual(r['integrity'],'PASS',r);self.assertEqual(r['core1a_authoring'],'HOLD');self.assertEqual(r['reviewed_SL2_joins'],0)
 def test_no_reviewed_question_or_optional_p1_required(self):self.assertEqual(self.result()['integrity'],'PASS')
 def test_missing_general_slope_is_honest_valid_gap(self):
  r=self.result(load(P/'handoffs/WPE-N07.json'));self.assertEqual(r['integrity'],'PASS',r);self.assertEqual(r['candidate_warrants'],0);self.assertEqual(r['missing_warrants'],1)
 def test_refreshing_source_excerpt_digest_cannot_substitute(self):
  self.d['units'][0]['content']='A plausible replacement.';self.d['units'][0]['digest']=digest(self.d['units'][0]['content']);self.bad('SOURCE_CORRESPONDENCE')
 def test_json_pointer_type_and_value_are_bound(self):
  u=next(x for x in self.d['units'] if x['id']=='U-MICRO');u['locator']['pointer']='/microtopics/1';self.bad('SOURCE_CORRESPONDENCE')
 def test_boolean_line_bound_is_rejected(self):self.d['units'][0]['locator']['start']=True;self.bad('BAD_LOCATOR')
 def test_duplicate_source_id(self):self.d['sources'].append(copy.deepcopy(self.d['sources'][0]));self.bad('DUPLICATE_ID')
 def test_duplicate_claim_id(self):self.d['claims'].append(copy.deepcopy(self.d['claims'][0]));self.bad('DUPLICATE_ID')
 def test_traversal(self):self.d['sources'][0]['path']='../book.md';self.bad('UNSAFE_PATH')
 def test_absolute_windows_path(self):self.d['sources'][0]['path']='C:/book.md';self.bad('UNSAFE_PATH')
 def test_forged_verified_source(self):self.d['sources'][0]['authority']='VERIFIED';self.bad('SOURCE_ROLE')
 def test_forged_qualified_claim(self):self.d['claims'][0]['qualification']='QUALIFIED';self.bad('PROMOTION_FORBIDDEN')
 def test_forged_qualified_warrant(self):self.d['warrants'][0]['qualification']='QUALIFIED';self.bad('PROMOTION_FORBIDDEN')
 def test_missing_warrant_cannot_point_at_convenient_unit(self):
  self.d['warrants'][0]['qualification']='MISSING';self.bad('WARRANT_BINDING')
 def test_book_is_not_canonical_warrant(self):self.d['warrants'][0]['unit_refs']=['U-BOOK-1'];self.bad('WARRANT_BINDING')
 def test_wrong_capability_foreign_key(self):self.d['binding']['canonical_matches'][0]['capability_id']='CAP-WRONG';self.bad('LIBRARY_BINDING')
 def test_wrong_spine_node(self):self.d['binding']['spine_node']='WPE-N02';self.bad('SYLLABUS_BINDING')
 def test_fake_canonical_review(self):self.d['binding']['canonical_matches'][0]['semantic_status']='REVIEWED';self.bad('PROMOTION_FORBIDDEN')
 def test_cycle(self):self.d['construction']['steps'][0]['depends_on']=['REQ-BOUNDARY'];self.bad('DEPENDENCY_CYCLE')
 def test_unit_and_claim_ids_cannot_make_ambiguous_html_anchor(self):
  self.d['units'][0]['id']='C1'
  for claim in self.d['claims']:claim['unit_refs']=['C1' if x=='U-BOOK-1' else x for x in claim['unit_refs']]
  for step in self.d['construction']['steps']:step['unit_refs']=['C1' if x=='U-BOOK-1' else x for x in step['unit_refs']]
  self.bad('AMBIGUOUS_ANCHOR')
 def test_orphan_claim(self):
  for x in self.d['construction']['steps']:x['claim_refs']=[r for r in x['claim_refs'] if r!='C3'] or ['C1']
  self.bad('ORPHAN_CLAIM')
 def test_fake_scan_role(self):self.d['claims'][0]['source_scan_refs']=['BOOK'];self.bad('FIGURE_ROLE')
 def test_fake_figure_role(self):self.d['construction']['representation_needs'][0]['asset_ref']='BOOK';self.bad('FIGURE_ROLE')
 def test_empty_figure_correspondence(self):self.d['construction']['representation_needs'][0]['correspondence']=[];self.bad('REPRESENTATION_CORRESPONDENCE')
 def test_fake_learner_observation(self):self.d['construction']['wrong_path_candidates'][0]['observation']='OBSERVED';self.bad('FABRICATED_OBSERVATION')
 def test_executed_check_not_forged(self):self.d['construction']['check_requirements'][0]['status']='PASS';self.bad('PROMOTION_FORBIDDEN')
 def test_reviewed_sl2_enum_not_consumed(self):self.d['sl2_requirement_mapping']['status']='REVIEWED';self.bad('UNSUPPORTED_REVIEW_JOIN')
 def test_named_but_unbound_question_not_consumed(self):self.d['sl2_requirement_mapping']['task_identity']='M101';self.bad('UNSUPPORTED_REVIEW_JOIN')
 def test_nonexistent_native_property(self):self.d['native_mapping'][0]['native_property']='invented';self.bad('NATIVE_MAPPING')
 def test_stale_review_target_even_with_new_record_fingerprint(self):
  self.d['construction']['output']='Changed construction';self.d['dependency_digest']=c.fingerprint(self.d);self.bad('STALE_REVIEW_REQUEST')
 def test_missing_review_request(self):self.d['review_requests'].pop();self.bad('REVIEW_COVERAGE')
 def test_duplicate_review_target(self):self.d['review_requests'][1]['target_pointer']=self.d['review_requests'][0]['target_pointer'];self.bad('REVIEW_COVERAGE')
 def test_forged_review_request_done(self):self.d['review_requests'][0]['status']='CLOSED';self.bad('PROMOTION_FORBIDDEN')
 def test_owner_gate_cannot_be_data_only(self):self.d['review']['core2_owner_approval']='APPROVED';self.bad('PROMOTION_FORBIDDEN')
 def test_stale_fingerprint(self):self.d['notes'].append('Changed dependency');self.bad('STALE_DEPENDENCY')
 def test_coherent_false_claim_is_still_semantically_unqualified(self):
  # Explicit surviving wrong case, not proof of a semantic detector.
  self.d['claims'][0]['statement']='A force perpendicular to displacement always transfers positive work.'
  for q in self.d['review_requests']:q['target_digest']=digest(c.pointer(self.d,q['target_pointer']))
  self.d['dependency_digest']=c.fingerprint(self.d)
  r=self.result();self.assertEqual(r['integrity'],'PASS',r);self.assertEqual(r['semantic_review'],'NOT_RUN');self.assertEqual(r['core1a_authoring'],'HOLD')
 def test_reference_cannot_be_canonical_warrant(self):
  self.d['warrants'][0]['unit_refs']=['U-REFERENCE-WEP-01'];self.bad('WARRANT_BINDING')
 def test_book_cannot_be_reference_lead(self):
  self.d['warrants'][0]['reference_unit_refs']=['U-BOOK-1'];self.bad('REFERENCE_ROLE')
 def test_original_scan_is_valid_evidence_but_not_reviewed(self):
  r=self.d['construction']['representation_needs'][0];r['asset_ref']='SCAN-1';r['status']='SOURCE_UNREVIEWED'
  for q in self.d['review_requests']:q['target_digest']=digest(c.pointer(self.d,q['target_pointer']))
  self.d['dependency_digest']=c.fingerprint(self.d)
  self.assertEqual(self.result()['integrity'],'PASS')
 def test_html_escapes_interpretation_and_source_markup(self):
  from render_program import record
  self.d['claims'][0]['statement']='<script>alert(1)</script>'
  for q in self.d['review_requests']:q['target_digest']=digest(c.pointer(self.d,q['target_pointer']))
  self.d['dependency_digest']=c.fingerprint(self.d)
  h=record(self.d,self.result());self.assertNotIn('<script>',h);self.assertIn('&lt;script&gt;',h)
 def test_unexpected_fields_rejected(self):self.d['learner_result']='independent';self.bad('SHAPE')

class ProgramChecks(unittest.TestCase):
 def setUp(self):
  scratch=S.parents[1]/'_checks';scratch.mkdir(exist_ok=True)
  self.temp=tempfile.TemporaryDirectory(prefix='program-',dir=scratch)
  self.root=Path(self.temp.name).resolve();assert self.root.is_relative_to(scratch.resolve()) and self.root!=scratch.resolve()
  self.addCleanup(self.temp.cleanup);shutil.copytree(P,self.root,dirs_exist_ok=True)
  self.path=self.root/'program.json';self.d=load(self.path)
 def result(self,expected=None):
  self.path.write_text(json.dumps(self.d,ensure_ascii=False),encoding='utf-8')
  return c.check_program(self.path,expected)
 def bad(self,code):
  r=self.result();self.assertEqual(r['integrity'],'INVALID',r);self.assertEqual(r['findings'][0]['code'],code,r)
 def test_complete_source_denominator(self):
  r=self.result();self.assertEqual(r['integrity'],'PASS',r);self.assertEqual(r['nodes_accounted'],10);self.assertEqual(r['source_lines_accounted'],486)
 def test_external_program_digest(self):
  self.path.write_text(json.dumps(self.d,ensure_ascii=False),encoding='utf-8');expected=file_sha(self.path)
  r=self.result(expected);self.assertEqual(r['scope_binding'],'EXTERNAL_PROGRAM_BYTES_MATCH',r)
 def test_stale_external_program_digest(self):
  r=self.result('0'*64);self.assertEqual(r['findings'][0]['code'],'PROGRAM_PIN_MISMATCH')
 def test_missing_node(self):self.d['records'].pop();self.bad('COVERAGE_MISMATCH')
 def test_duplicate_node(self):self.d['records'].append(copy.deepcopy(self.d['records'][0]));self.bad('DUPLICATE_ID')
 def test_stale_record_bytes(self):
  p=self.root/self.d['records'][0]['path'];p.write_text('{}');self.bad('RECORD_HASH_MISMATCH')
 def test_changed_source_bytes(self):
  (self.root/'handoffs/sources/book.md').write_text('Substitution');self.bad('SCOPE_SOURCE_MISMATCH')
 def test_false_refreshed_source_identity_against_separate_pin(self):
  ref=self.d['records'][0];p=self.root/ref['path'];d=load(p);d['sources'][0]['sha256']='0'*64
  p.write_text(json.dumps(d));ref['sha256']=file_sha(p);self.bad('RECORD_INVALID')
 def test_record_id_not_filename(self):
  ref=self.d['records'][0];p=self.root/ref['path'];d=load(p);d['id']='WPE-N02';p.write_text(json.dumps(d));ref['sha256']=file_sha(p);self.bad('RECORD_ID_MISMATCH')
 def test_program_prerequisite_cycle(self):self.d['records'][0]['prerequisites']=['WPE-N10'];self.bad('PROGRAM_DEPENDENCY_CYCLE')
 def test_missing_source_lines(self):self.d['line_dispositions'].pop();self.bad('UNACCOUNTED_SOURCE_LINES')
 def test_overlap_source_lines(self):self.d['line_dispositions'][1]['start']=10;self.bad('DUPLICATE_LINE_DISPOSITION')
 def test_unknown_disposition_node(self):self.d['line_dispositions'][0]['node_refs']=['WPE-N99'];self.bad('UNRESOLVED_REF')
 def test_missing_scan_observation(self):self.d['scan_observations'].pop();self.bad('SCAN_COVERAGE')
 def test_duplicate_scan_observation(self):self.d['scan_observations'].append(copy.deepcopy(self.d['scan_observations'][0]));self.bad('SCAN_COVERAGE')
 def test_fake_independent_scan_acceptance(self):self.d['scan_observations'][0]['status']='INDEPENDENTLY_VERIFIED';self.bad('PROMOTION_FORBIDDEN')
 def test_path_escape(self):self.d['records'][0]['path']='../external.json';self.bad('UNSAFE_PATH')
 def test_global_fake_owner_approval(self):self.d['gates']['core2_owner_approval']='APPROVED';self.bad('PROMOTION_FORBIDDEN')
 def test_strict_json_duplicates_and_nonfinite(self):
  for raw in ['{"a":1,"a":2}','{"a":NaN}']:
   self.path.write_text(raw)
   self.assertEqual(c.check_program(self.path)['integrity'],'INVALID')

if __name__=='__main__':unittest.main()
