import copy, json, sys, unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from core2_engine import (FACTORS,OPS,canonical_digest,evaluate_record,evaluate_selection,fingerprint,make_derived_package)
from learner_render import render_fixture

FIX=json.load(open(BASE/'fixtures/synthetic_question.json'))

def mock_approved(n=0,op='APPLY'):
    # TEST-ONLY bogus official witnesses and review refs prove only structural gates.
    q=copy.deepcopy(FIX);q['id']=f'TEST-ID-{n}';q['origin']='EXAM_ORIGINAL';q['original_identifier']=f'TEST-{n}';
    q['extensions'].pop('wpe:synthetic_technical_fixture',None)
    paper={'artifact_ref':'SYN-PAPER','artifact_sha256':'a'*64,'locator':'p1/Q1','source_authority':'SYNTHETIC TEST','witness_ref':'SYN-PAPER-W','upstream_status':'AUTHENTICATED'}
    key={'artifact_ref':'SYN-KEY','artifact_sha256':'b'*64,'locator':'p3/row1','source_authority':'SYNTHETIC TEST','witness_ref':'SYN-KEY-W','upstream_status':'AUTHENTICATED'}
    r={'canonical_id':q['id'],'origin':'EXAM_ORIGINAL_AUTHENTICATED','source_role':'DIRECT_EXAM','question':q,
    'source':{'question_digest':canonical_digest({k:q.get(k) for k in ('stem','subparts','conditions','original_identifier')}),'options_digest':canonical_digest(q['options']),'figure_digests':[],'official_paper':paper,'official_key':key,'required_figures_bound':True,'custody_mode':'EMBEDDED_VERBATIM','rights_status':'AUTHORIZED_TO_EMBED','rights_authorization_ref':'SYNTHETIC_RIGHTS','answer_versions':{'inherited_claim_digest':'c'*64,'official_claim_digest':'d'*64,'reconciliation':'AGREED_VERSIONED','reconciliation_ref':'SYN-RECON'}},
    'curriculum':{'rubric_sha256':'e'*64,'blueprint_sha256':'f'*64,'adapter_sha256':'0'*64,'adapter_owner_approved':True,'adapter_owner_approval_ref':'SYN-OWNER','semantic_cell_resolved':True,'cell_ref':f'{op}-D3','capability_ref':'CAP-TEST','microtopic_ref':'MIC-TEST'},
    'assessment':{'factors':dict(zip(FACTORS,(2,1,1,1,1))),'total':6,'band':'D3','primary_operation':op,'factor_evidence':{f:f+' supported by specific test-only example' for f in FACTORS},'independent_solution_ref':'SYN-SOL','decisive_move_evidence':'TEST ONLY choose a physical law','competing_operations':[]},
    'governance':{'owner_execution_authorization_ref':'SYN-EXEC','reviewer_appointment_ref':'SYN-REVIEW-APP','reviewer_identity':'SYN-REVIEWER','author_identity':'SYN-AUTHOR','reviewer_exposure_disclosed':True,'reviewer_first_pass_ref':'SYN-SEALED','reviewer_attestation_ref':'SYN-ATT','qrt_adjudication':'ADMITTED','qrt_adjudication_ref':'SYN-QRT','primary_counting_operation':op},
    'grading_policy':q['extensions']['wpe:grading_policy']}
    r['assessment']['subject_sha256']=fingerprint(r)
    return r


def all21(): return [mock_approved(i,OPS[i//3]) for i in range(21)]

class Admission(unittest.TestCase):
    def valid(self):
        r=mock_approved();self.assertEqual(evaluate_record(r)['state'],'BUILD_ELIGIBLE_METADATA_ONLY');return r
    def block(self, mutate, expected):
        r=self.valid();mutate(r);out=evaluate_record(r);self.assertIn(expected,out['reasons'])
    def test_01_synthetic_metadata_example_only(self):self.valid()
    def test_02_empty_not_admitted(self):self.assertIn('SELECTION_NOT_21',evaluate_selection([])['errors'])
    def test_03_no_official_paper(self):self.block(lambda r:r['source'].pop('official_paper'), 'OFFICIAL_PAPER_CUSTODY_OPEN')
    def test_04_no_key(self):self.block(lambda r:r['source'].pop('official_key'),'OFFICIAL_KEY_CUSTODY_OPEN')
    def test_05_same_witness(self):self.block(lambda r:r['source']['official_key'].update(witness_ref='SYN-PAPER-W'),'PAPER_KEY_WITNESSES_NOT_DISTINCT')
    def test_06_figure_missing(self):self.block(lambda r:r['question']['figure_refs'].append('MISSING.png'),'FIGURE_DIGESTS_INCOMPLETE')
    def test_07_key_reconciliation(self):self.block(lambda r:r['source']['answer_versions'].update(reconciliation='DISPUTED'),'ANSWER_RECONCILIATION_OPEN')
    def test_08_inherited_answer(self):self.block(lambda r:r['source']['answer_versions'].pop('inherited_claim_digest'),'INHERITED_ANSWER_MISSING')
    def test_09_adapter_authority(self):self.block(lambda r:r['curriculum'].update(adapter_owner_approved=False),'ADAPTER_AUTHORITY_OPEN')
    def test_10_blueprint_drift(self):self.block(lambda r:r['curriculum'].update(blueprint_sha256='1'*64),'ASSESSMENT_SUBJECT_STALE')
    def test_11_stem_drift(self):self.block(lambda r:r['question'].update(stem='altered stem'),'SOURCE_TEXT_DIGEST_MISMATCH')
    def test_12_option_drift(self):self.block(lambda r:r['question']['options'][0].update(text='changed'),'SOURCE_OPTION_DIGEST_MISMATCH')
    def test_13_d2_not_counted(self):self.block(lambda r:r['assessment']['factors'].update(concept_model_selection=1,reasoning_chain_length=0),'NOT_D3_D4')
    def test_14_reviewer_same_author(self):self.block(lambda r:r['governance'].update(reviewer_identity='SYN-AUTHOR'),'REVIEWER_INDEPENDENCE_OPEN')
    def test_15_exposure_undisclosed(self):self.block(lambda r:r['governance'].update(reviewer_exposure_disclosed=False),'REVIEWER_EXPOSURE_UNDISCLOSED')
    def test_16_qrt_missing(self):self.block(lambda r:r['governance'].update(qrt_adjudication='HOLD'),'QRT_ADMISSION_OPEN')
    def test_17_alias_not_primary(self):self.block(lambda r:r.update(duplicate_of='ORIGINAL'),'DUPLICATE_ALIAS_NOT_PRIMARY')
    def test_18_mismatched_response(self):self.block(lambda r:r['grading_policy'].update(type='NUMERIC'),'GRADING_TYPE_MISMATCH')
    def test_19_wrong_option(self):self.block(lambda r:r['grading_policy'].update(correct_ids=['Z']),'ANSWER_OPTION_ID_INVALID')
    def test_20_protected_scaffold(self):self.block(lambda r:r['question']['scaffolds'][0].update(completes_protected_move=True),'PROTECTED_CRUX_LEAK_0')
    def test_rights_fail_closed(self):self.block(lambda r:r['source'].update(rights_status='UNKNOWN'),'SOURCE_REPRODUCTION_RIGHTS_OPEN')
    def test_external_reference_not_silently_embedded(self):self.block(lambda r:r['source'].update(custody_mode='EXTERNAL_REFERENCE'),'EXTERNAL_REFERENCE_CUSTODY_NOT_IMPLEMENTED')
    def test_missing_original_figure_bytes(self):
        r=mock_approved();r['question']['figure_refs']=['original.png'];r['source']['figure_digests']=['a'*64]
        r['source']['question_digest']=canonical_digest({k:r['question'].get(k) for k in ('stem','subparts','conditions','original_identifier')});r['assessment']['subject_sha256']=fingerprint(r)
        from core2_engine import verify_assets
        with self.assertRaisesRegex(ValueError,'ORIGINAL_ASSET_ROOT_MISSING'): verify_assets([r])
    def test_21_quota(self):self.assertEqual(evaluate_selection(all21())['state'],'BUILD_ELIGIBLE_METADATA_ONLY')
    def test_22_duplicate_counted(self):
        rr=all21();rr[-1]['canonical_id']=rr[0]['canonical_id'];self.assertIn('DUPLICATE_PRIMARY_COUNT',evaluate_selection(rr)['errors'])
    def test_23_wrong_operation_quota(self):
        rr=all21();rr[-1]['assessment']['primary_operation']='APPLY';self.assertIn('OPERATION_QUOTA:APPLY',evaluate_selection(rr)['errors'])
    def test_24_no_owner_release_needed_to_build(self):self.assertNotIn('owner_core2_acceptance',mock_approved()['governance'])
    def test_25_package_preserves_library(self):
        rr=all21();library={'subject':'Physics','questions':[],'capabilities':[{'id':'CAP-TEST'}],'microtopics':[{'id':'MIC-TEST'}],'status':'CANDIDATE'}
        manifest={'schema':'product-manifest/v1','selection':{'core2':[],'core2a':[],'core2b':[]}}
        original=copy.deepcopy(library)
        pkg=make_derived_package(rr,library,manifest,{'target_package':'candidate-bank.json','resource':{},'resources':[]})
        self.assertEqual(library,original);self.assertEqual(len(pkg['bank.json']['questions']),21)
        self.assertEqual(pkg['records.json'],library)
        self.assertEqual(pkg['manifest.json']['selection']['core2a'],[])
        self.assertTrue(all(x['status']=='CANDIDATE' for x in pkg['bank.json']['questions']))
    def test_26_native_manifest_nonempty_fails(self):
        with self.assertRaisesRegex(ValueError,'WPE_NATIVE_MANIFEST_NOT_EMPTY_STOP'):
            make_derived_package(all21(),{'subject':'Physics','questions':[],'capabilities':[{'id':'CAP-TEST'}],'microtopics':[{'id':'MIC-TEST'}]}, {'schema':'product-manifest/v1','selection':{'core2':['EXISTING']}}, {'target_package':'bank.json'})
    def test_27_cannot_package_real_candidates(self):
        with self.assertRaisesRegex(ValueError,'CANNOT_BUILD'):
            make_derived_package([],{}, {},{})
    def test_28_render_requires_synthetic_flag(self):
        with self.assertRaisesRegex(ValueError,'SYNTHETIC_FIXTURE_FLAG_REQUIRED'):
            q=copy.deepcopy(FIX);q['extensions'].pop('wpe:synthetic_technical_fixture');render_fixture(q,technical_fixture=True)
    def test_29_render_production_refused(self):
        with self.assertRaisesRegex(ValueError,'UNREVIEWED_QUESTIONS_CANNOT_RENDER'):
            render_fixture(FIX)
    def test_30_fixture_escapes_html(self):
        q=copy.deepcopy(FIX);q['stem']='<img src=x onerror=alert(1)>'
        out=render_fixture(q,technical_fixture=True)
        self.assertNotIn('<img src=x',out)
        self.assertIn('\\u003cimg',out)

if __name__=='__main__':unittest.main()
