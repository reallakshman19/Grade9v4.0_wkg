"""Author checks against literal source bytes and the unchanged native validators."""
from pathlib import Path
from copy import deepcopy
import hashlib, json, sys, unittest
from native_adapter import adapt_fixture, digest, inspect_real_projection
ROOT=Path(__file__).resolve().parents[1]
REPO=Path(r'C:\CodeC\Grade9v3.5');sys.path.insert(0,str(REPO))
from Shared.tools import owner_bank, core2_v2, product_manifest, render_core
from jsonschema import Draft202012Validator
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
package=read(ROOT/'native/records.json');fixture=read(ROOT/'received-engineering/fixtures/synthetic_question.json')
binding=read(ROOT/'native/synthetic-binding.json');synthetic=read(ROOT/'native/synthetic-bank.json')
textbook=read(ROOT/'native/textbook-bank.json');manifest=read(ROOT/'native/manifest.json')
projection=read(ROOT/'received-private-r1/outputs/REAL_R1_SELECTION_PREFLIGHT.json')
schema=read(REPO/'Shared/library/package.schema.json')

class NativeIntegration(unittest.TestCase):
    def test_original_and_retained_bytes(self):
        for row in read(ROOT/'review/PRESERVATION_PINS.json'):
            for p in [Path(row['original']),ROOT/row['retained']]:
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'],str(p))
    def test_textbook_bank_is_byte_exact(self):
        self.assertEqual((ROOT/'native/textbook-bank.json').read_bytes(),(ROOT/'textbook-baseline/native/bank.json').read_bytes())
    def test_native_package_schema(self):Draft202012Validator(schema).validate(package)
    def test_native_question_schema_no_fixture_bypass(self):
        v=Draft202012Validator({'$ref':'#/$defs/question','$defs':schema['$defs']})
        for q in textbook['questions']+synthetic['questions']:v.validate(q)
    def test_native_bank_checks_with_actual_intakes(self):
        for name,bank in [('textbook',textbook),('synthetic',synthetic)]:
            self.assertEqual(owner_bank.check(bank,intake=read(ROOT/f'native/{name}-intake.json'),complete=False),[])
    def test_selected_nine_resolve_in_actual_renderer(self):
        ctx=render_core.context(ROOT/'native/manifest.json')
        self.assertEqual(len(product_manifest.validate_selection(ctx.manifest,ctx.packages,ctx.bank)['core2']),9)
    def test_wrong_record_authority_rejected(self):
        m=deepcopy(manifest);p=deepcopy(package);p['questions']=[deepcopy(synthetic['questions'][0])]
        m['selection']['core2']=[synthetic['questions'][0]['id']]
        with self.assertRaisesRegex(product_manifest.ProductSelectionError,'WRONG_AUTHORITY'):
            product_manifest.validate_selection(m,[p],textbook['questions'])
    def test_duplicate_selection_rejected(self):
        m=deepcopy(manifest);m['selection']['core2'].append(m['selection']['core2'][0])
        with self.assertRaisesRegex(product_manifest.ProductSelectionError,'DUPLICATE_ID'):
            product_manifest.validate_selection(m,[package],textbook['questions']+synthetic['questions'])
    def test_missing_selection_rejected(self):
        m=deepcopy(manifest);m['selection']['core2'].append('NO-SUCH-QUESTION')
        with self.assertRaisesRegex(product_manifest.ProductSelectionError,'UNRESOLVED'):
            product_manifest.validate_selection(m,[package],textbook['questions']+synthetic['questions'])
    def test_stem_mutation_rejected_against_intake(self):
        b=deepcopy(synthetic);b['questions'][0]['stem']+=' altered'
        self.assertTrue(any('stem' in x for x in owner_bank.check(b,intake=read(ROOT/'native/synthetic-intake.json'),complete=False)))
    def test_source_answer_change_invalidates_binding(self):
        f=deepcopy(fixture);f['answer']['summary']='A — Positive'
        with self.assertRaisesRegex(ValueError,'BINDING_STALE'):adapt_fixture(f,binding,package)
    def test_source_options_change_invalidates_binding(self):
        f=deepcopy(fixture);f['options'].reverse()
        with self.assertRaisesRegex(ValueError,'BINDING_STALE'):adapt_fixture(f,binding,package)
    def test_duplicate_option_ids_rejected(self):
        f=deepcopy(fixture);f['options'][1]['id']='A';b=deepcopy(binding);b['source_digest']=digest(f)
        with self.assertRaisesRegex(ValueError,'OPTION_ID_DUPLICATE'):adapt_fixture(f,b,package)
    def test_unsupported_figure_not_silently_dropped(self):
        f=deepcopy(fixture);f['figure_refs']=['unknown.png'];b=deepcopy(binding);b['source_digest']=digest(f)
        with self.assertRaisesRegex(ValueError,'FIGURE_MAPPING_UNSUPPORTED'):adapt_fixture(f,b,package)
    def test_real_exam_cannot_enter_synthetic_adapter(self):
        for r in projection['records']:
            with self.assertRaisesRegex(ValueError,'SYNTHETIC_SCOPE_REQUIRED'):adapt_fixture(r['question'],binding,package)
    def test_source_answer_route_preserved(self):
        q=synthetic['questions'][0]
        self.assertEqual(q['answer']['reasoning'],fixture['answer']['reasoning'])
        self.assertEqual([x['action'] for x in q['answer']['reasoning_route']],fixture['answer']['reasoning'])
        self.assertEqual(q['answer']['summary'],fixture['answer']['summary'])
    def test_option_identity_and_order(self):
        q=synthetic['questions'][0]
        self.assertEqual(q['options'],['Positive','Negative','Zero','Not enough information about the speed'])
    def test_unknown_option_label_mapping_rejected(self):
        f=deepcopy(fixture);f['options'][0]['id']='Z';b=deepcopy(binding);b['source_digest']=digest(f)
        with self.assertRaisesRegex(ValueError,'OPTION_LABEL_MAPPING_UNSUPPORTED'):adapt_fixture(f,b,package)
    def test_no_automatic_grader_projected(self):
        q=synthetic['questions'][0]
        self.assertNotIn('verification',q)
        html=(ROOT/'rendered/core2.html').read_text()
        self.assertNotIn('function grade(',html)
        self.assertEqual(q['origin'],'AUTHORED')
    def test_no_invented_official_identity(self):
        q=synthetic['questions'][0]
        self.assertFalse(set(owner_bank.OFFICIAL_ONLY).intersection(q['extensions'][owner_bank.CUSTODY_KEY]))
        self.assertFalse(q['extensions']['wpe:native_integration']['exam_admission'])
    def test_protected_move_leak_rejected_by_native_projection(self):
        q=deepcopy(synthetic['questions'][0]);plan=q['extensions'][core2_v2.SUPPORT_PLAN_KEY]
        plan['support_completions'][0]['completed_move_refs']=plan['protected_move_refs'][:]
        with self.assertRaisesRegex(core2_v2.Core2SupportProjectionError,'completing protected work'):core2_v2.project_support(q)
    def test_invalid_move_reference_rejected(self):
        q=deepcopy(synthetic['questions'][0]);q['extensions'][core2_v2.SUPPORT_PLAN_KEY]['protected_move_refs']=['MISSING']
        with self.assertRaisesRegex(core2_v2.Core2SupportProjectionError,'reasoning moves'):core2_v2.project_support(q)
    def test_supplied_method_prompts_retained_without_safe_claim(self):
        q=synthetic['questions'][0]
        self.assertEqual(q['extensions']['wpe:native_integration']['withheld_original_scaffolds'],fixture['scaffolds'])
        self.assertEqual(len(core2_v2.project_support(q)),2)
        self.assertTrue(all(r['provenance']==core2_v2.AUTHORED_CORE2_SUPPORT for r in core2_v2.project_support(q)))
    def test_relocation_changes_only_representation_asset_paths(self):
        p=deepcopy(package)
        p['representations']=[r for r in p['representations'] if r['id']!='REP-SYN-WPE-DIRECTIONS']
        p['title']=read(ROOT/'textbook-baseline/native/records.json')['title']
        rows=read(ROOT/'review/ASSET_RELOCATION.json');back={r['after']:r['before'] for r in rows}
        for r in p['representations']:r['rendered_asset_refs']=[back[a] for a in r.get('rendered_asset_refs',[])]
        self.assertEqual(p,read(ROOT/'textbook-baseline/native/records.json'))
    def test_all_fourteen_remain_held(self):
        readiness=read(ROOT/'review/EXAM_READINESS.json')
        self.assertEqual((readiness['conditional_leads'],readiness['vacancies'],readiness['admitted']),(14,7,0))
        for r in projection['records']:
            out=inspect_real_projection(r);self.assertEqual(out['state'],'HOLD');self.assertFalse(out['selected'])
        self.assertTrue(all(not i.startswith('EX-') and i!='WEP07-03' for i in manifest['selection']['core2']))
    def test_no_lesson_roles_or_outputs(self):
        self.assertEqual(manifest['output_roles'],['CORE2'])
        self.assertFalse((ROOT/'rendered/core1a.html').exists());self.assertFalse((ROOT/'rendered/core1b.html').exists())

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(NativeIntegration)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    (ROOT/'review/INTEGRATION_TESTS.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'pass':result.wasSuccessful(),
        'scope':'AUTHOR_TESTS; actual native schemas, validators, renderer context; no distinct QA or academic admission',
        'failed_details':[str(t)+': '+msg for t,msg in result.failures+result.errors]},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
