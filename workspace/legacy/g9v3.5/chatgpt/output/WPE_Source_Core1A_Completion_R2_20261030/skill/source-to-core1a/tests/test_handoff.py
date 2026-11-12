"""Real-source mechanical controls; synthetic mutations are explicitly not exam evidence."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
import hashlib

SKILL = Path(__file__).resolve().parents[1]
ROOT = SKILL.parents[1]
spec = importlib.util.spec_from_file_location('checker', SKILL / 'scripts/check_handoff.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class HandoffTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '_checks'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='handoff-', dir=scratch)
        self.work = Path(self.temp.name).resolve()
        # Verify the absolute temporary deletion target before scheduling recursive cleanup.
        assert self.work.is_relative_to(scratch.resolve()) and self.work != scratch.resolve()
        self.addCleanup(self.temp.cleanup)
        shutil.copytree(SKILL / 'examples/wpe-work-direction', self.work, dirs_exist_ok=True)
        self.data = c.load(self.work / 'handoff.json')
        self.pins = self.work / 'source-pins.json'
        self.pin_sha = c.file_sha(self.pins)

    def check(self, trusted=True):
        return c.check(self.data, self.work, self.pins if trusted else None,
                       self.pin_sha if trusted else None)

    def invalid(self, code, trusted=True):
        result = self.check(trusted)
        self.assertEqual(result['integrity'], 'INVALID', result)
        self.assertEqual(result['findings'][0]['code'], code, result)

    def test_real_book_binding_passes_but_never_authorizes(self):
        r = self.check()
        self.assertEqual(r['integrity'], 'PASS', r)
        self.assertEqual(r['trust_binding'], 'EXTERNAL_PIN_BYTES_MATCH')
        self.assertEqual(r['core1a_authoring'], 'HOLD')
        self.assertEqual(r['native_package'], 'NOT_EMITTED')

    def test_untrusted_mode_is_explicit(self):
        self.assertEqual(self.check(False)['trust_binding'], 'SELF_DECLARED_ONLY')

    def test_optional_p1_and_question_join_are_not_required(self):
        self.assertEqual(self.data['question_links'], [])
        self.assertEqual(self.check()['integrity'], 'PASS')

    def test_changed_source_bytes(self):
        (self.work / 'sources/book.md').write_text('Substituted source', encoding='utf-8')
        self.invalid('SOURCE_HASH_MISMATCH')

    def test_substituted_excerpt_even_after_rehash(self):
        u = self.data['units'][0]
        u['content'] = 'A plausible but substituted paragraph.'
        u['digest'] = c.digest(u['content'])
        self.invalid('SOURCE_CORRESPONDENCE')

    def test_stale_unit_digest(self):
        self.data['units'][0]['digest'] = 'sha256:' + '0' * 64
        self.invalid('UNIT_DIGEST')

    def test_changed_locator(self):
        self.data['units'][0]['locator']['start'] += 1
        self.invalid('SOURCE_CORRESPONDENCE')

    def test_invalid_line_range(self):
        self.data['units'][0]['locator']['start'] = 0
        self.invalid('BAD_LOCATOR')

    def test_boolean_line_number(self):
        self.data['units'][0]['locator']['start'] = True
        self.invalid('BAD_LOCATOR')

    def test_json_pointer_substitution(self):
        u = next(u for u in self.data['units'] if u['id'] == 'U-MICRO')
        u['locator']['pointer'] = '/microtopics/1'
        self.invalid('SOURCE_CORRESPONDENCE')

    def test_bad_pointer_escape(self):
        u = next(u for u in self.data['units'] if u['id'] == 'U-MICRO')
        u['locator']['pointer'] = '/microtopics/~2'
        self.invalid('BAD_POINTER')

    def test_missing_asset(self):
        (self.work / 'sources/positive-work.svg').unlink()
        self.invalid('MISSING_ASSET')

    def test_duplicate_source_id(self):
        self.data['sources'].append(copy.deepcopy(self.data['sources'][0]))
        self.invalid('DUPLICATE_ID')

    def test_duplicate_unit_id(self):
        self.data['units'].append(copy.deepcopy(self.data['units'][0]))
        self.invalid('DUPLICATE_ID')

    def test_duplicate_claim_id(self):
        self.data['claims'].append(copy.deepcopy(self.data['claims'][0]))
        self.invalid('DUPLICATE_ID')

    def test_changed_capability(self):
        self.data['binding']['capability_id'] = 'CAP-UNSUPPORTED'
        self.invalid('LIBRARY_BINDING')

    def test_changed_microtopic(self):
        self.data['binding']['microtopic_id'] = 'MIC-UNSUPPORTED'
        self.invalid('LIBRARY_BINDING')

    def test_changed_syllabus_node(self):
        self.data['binding']['spine_node'] = 'WPE-N99'
        self.invalid('SYLLABUS_BINDING')

    def test_book_passage_is_not_canonical_warrant(self):
        self.data['construction']['steps'][0]['warrant_unit_refs'] = ['U-WORK']
        self.invalid('WARRANT_BINDING')

    def test_missing_warrant(self):
        self.data['construction']['steps'][0]['warrant_unit_refs'] = []
        self.invalid('SHAPE')

    def test_unresolved_claim(self):
        self.data['construction']['steps'][0]['claim_refs'] = ['NO-CLAIM']
        self.invalid('UNRESOLVED_REF')

    def test_dependency_cycle(self):
        self.data['construction']['steps'][0]['depends_on'] = ['REQ-CHECK']
        self.invalid('DEPENDENCY_CYCLE')

    def test_unresolved_dependency(self):
        self.data['construction']['steps'][0]['depends_on'] = ['NO-STEP']
        self.invalid('UNRESOLVED_REF')

    def test_native_field_invention(self):
        self.data['native_mapping'][0]['native_property'] = 'invented_core1a_panel'
        self.invalid('NATIVE_MAPPING')

    def test_native_pointer_missing(self):
        self.data['native_mapping'][0]['handoff_pointer'] = '/construction/absent'
        self.invalid('BAD_POINTER')

    def test_native_mapping_to_book(self):
        self.data['native_mapping'][0]['schema_unit_ref'] = 'U-WORK'
        self.invalid('NATIVE_MAPPING')

    def test_promoted_status_is_rejected(self):
        self.data['status'] = 'REVIEWED'
        self.invalid('PROMOTION_FORBIDDEN')

    def test_claim_qualification_enum_is_not_review(self):
        self.data['claims'][0]['qualification'] = 'VERIFIED'
        self.invalid('PROMOTION_FORBIDDEN')

    def test_owner_approval_enum_is_not_authority(self):
        self.data['review']['core2_owner_approval'] = 'APPROVED'
        self.invalid('PROMOTION_FORBIDDEN')

    def test_learner_observation_cannot_be_smuggled(self):
        self.data['learner_observation'] = {'independent': True}
        self.invalid('SHAPE')

    def test_book_badge_does_not_establish_exam_question(self):
        self.data['question_links'] = [dict(id='LINK-1', question_unit_ref='U-SOURCE-EXAMPLE', question_id='JEE-BOOK-BADGE',
            source_role='DIRECT_EXAM_EVIDENCE', operation='APPLY', demand=None, status='PROPOSED')]
        self.invalid('QUESTION_BINDING')

    def test_coherent_but_false_paraphrase_still_needs_semantic_review(self):
        self.data['claims'][0]['statement'] = 'A perpendicular force always does positive work.'
        r = self.check()
        self.assertEqual(r['integrity'], 'PASS')
        self.assertEqual(r['semantic_review'], 'NOT_RUN')
        self.assertEqual(r['core1a_authoring'], 'HOLD')

    def test_rehash_everything_cannot_change_externally_pinned_source(self):
        source = self.data['sources'][0]
        path = self.work / source['path']
        path.write_bytes(path.read_bytes() + b'\nA replaced edition.\n')
        source['sha256'] = c.file_sha(path)
        self.invalid('SOURCE_PIN_MISMATCH')

    def test_edited_pin_file_does_not_match_expected_receipt(self):
        pinset = c.load(self.pins)
        pinset['sources'][0]['sha256'] = '0' * 64
        self.pins.write_text(json.dumps(pinset), encoding='utf-8')
        self.invalid('TRUST_ANCHOR_MISMATCH')

    def test_pin_file_without_expected_digest_fails(self):
        r = c.check(self.data, self.work, self.pins, None)
        self.assertEqual(r['findings'][0]['code'], 'TRUST_ANCHOR_REQUIRED')

    def test_traversal_path(self):
        self.data['sources'][0]['path'] = '../outside.md'
        self.invalid('UNSAFE_PATH', False)

    def test_windows_absolute_path(self):
        self.data['sources'][0]['path'] = 'C:/outside.md'
        self.invalid('UNSAFE_PATH', False)

    def test_remote_path(self):
        self.data['sources'][0]['path'] = 'https://example.org/claim.md'
        self.invalid('UNSAFE_PATH', False)

    def test_duplicate_json_keys(self):
        p = self.work / 'invalid.json'
        p.write_text('{"schema":1,"schema":2}', encoding='utf-8')
        self.assertEqual(c.check_file(p)['findings'][0]['code'], 'DUPLICATE_JSON_KEY')

    def test_nonfinite_json(self):
        p = self.work / 'invalid.json'
        p.write_text('{"x":NaN}', encoding='utf-8')
        self.assertEqual(c.check_file(p)['findings'][0]['code'], 'NONFINITE_JSON')

    def test_invalid_json_does_not_crash(self):
        p = self.work / 'invalid.json'
        p.write_text('{bad', encoding='utf-8')
        self.assertEqual(c.check_file(p)['integrity'], 'INVALID')

    def synthetic_question(self):
        # This is a synthetic interface fixture, not a new exam record or admission.
        q = dict(id='SYNTHETIC-QUESTION-1', stem='Fixture only; not examination evidence.')
        path = self.work / 'sources/synthetic.json'
        path.write_text(json.dumps(q), encoding='utf-8')
        source = dict(id='SYNTHETIC', path='sources/synthetic.json', sha256=c.file_sha(path),
                      role='QUESTION_EVIDENCE', authority='OWNER_LOCAL_UNAUTHENTICATED')
        self.data['sources'].append(source)
        self.data['units'].append(dict(id='U-SYNTHETIC', source_ref='SYNTHETIC', kind='JSON_POINTER',
            locator=dict(pointer=''), content=q, digest=c.digest(q)))
        self.pins.write_text(json.dumps(dict(schema='source-pin-set/v1', sources=self.data['sources'])), encoding='utf-8')
        self.pin_sha = c.file_sha(self.pins)
        self.data['question_links'] = [dict(id='LINK-1', question_unit_ref='U-SYNTHETIC', question_id=q['id'],
            source_role='PREREQUISITE_BRIDGE', operation='APPLY', demand=None, status='PROPOSED')]

    def test_proposed_question_interface_remains_unqualified(self):
        self.synthetic_question()
        r = self.check()
        self.assertEqual(r['integrity'], 'PASS', r)
        self.assertEqual(r['question_links'], 1)
        self.assertEqual(r['core1a_authoring'], 'HOLD')

    def test_wrong_question_identity(self):
        self.synthetic_question()
        self.data['question_links'][0]['question_id'] = 'SOME-OTHER-QUESTION'
        self.invalid('QUESTION_BINDING')

    def test_question_demand_arithmetic_all_bands(self):
        self.synthetic_question()
        for scores, band in [([1,0,1,0,0],'D1'), ([1,1,1,1,1],'D2'), ([1,1,2,1,1],'D3'), ([2,2,2,1,1],'D4')]:
            with self.subTest(band=band):
                self.data['question_links'][0]['demand'] = dict(factors=dict(zip(c.FACTORS, scores)),
                    score=sum(scores), band=band, evidence={f:'Synthetic arithmetic fixture; not cognitive validation.' for f in c.FACTORS})
                self.assertEqual(self.check()['integrity'], 'PASS')

    def test_inflated_question_band(self):
        self.synthetic_question()
        self.data['question_links'][0]['demand'] = dict(factors={f:1 for f in c.FACTORS},
            score=5, band='D3', evidence={f:'Synthetic fixture.' for f in c.FACTORS})
        self.invalid('DEMAND_ARITHMETIC')

    def test_unknown_operation(self):
        self.synthetic_question()
        self.data['question_links'][0]['operation'] = 'PROOF_WITH_NO_QRT_OPERATION'
        self.invalid('OPERATION')

    def test_empty_existing_asset_correspondence(self):
        self.data['construction']['representation_needs'][0]['correspondence'] = []
        self.invalid('SHAPE')

    def test_explicit_missing_figure_can_be_prepared_but_not_promoted(self):
        rep = self.data['construction']['representation_needs'][0]
        rep['asset_ref'], rep['status'], rep['correspondence'] = None, 'MISSING', []
        r = self.check()
        self.assertEqual(r['integrity'], 'PASS')
        self.assertEqual(r['core1a_authoring'], 'HOLD')

    def test_html_dossier_escapes_source_interpretation(self):
        import sys
        sys.modules['check_handoff'] = c
        spec = importlib.util.spec_from_file_location('dossier', SKILL / 'scripts/render_handoff.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.data['claims'][0]['statement'] = '<script>UNTRUSTED()</script>'
        output = module.render(self.data, self.check())
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;script&gt;', output)

    def test_unsupported_extraction_does_not_fallback(self):
        self.data['units'][0]['kind'] = 'OCR_GUESSED'
        self.invalid('UNSUPPORTED_EXTRACTION')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(HandoffTests)
    names = [test.id().split('.')[-1] for test in suite]
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(dict(status='PASS' if result.wasSuccessful() else 'FAIL',
            tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
            cases=names, assessment='AUTHOR_MECHANICAL_CHECKS_ONLY', independent_review='NOT_RUN',
            semantic_control='Coherent false paraphrase can pass integrity; authoring remains HOLD.'), indent=2) + '\n', encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
