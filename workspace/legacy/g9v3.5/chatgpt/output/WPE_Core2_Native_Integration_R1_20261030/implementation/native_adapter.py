"""Explicit technical-fixture adapter; never grants examination admission.

The received custom dialect and native question are separate records. This
adapter supports ONLY a source-hash-bound authored fixture. Real examination
projections are inspected and held, never repaired with fabricated answers.
"""
from copy import deepcopy
import hashlib
import json

FACTORS = ('concept_model_selection', 'representation_translation',
           'reasoning_chain_length', 'algebra_computational_load',
           'trap_exception_sensitivity')

def digest(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode()).hexdigest()

def adapt_fixture(source, binding, package):
    if (source.get('origin') != 'AUTHORED_TECHNICAL_FIXTURE' or
        source.get('extensions', {}).get('wpe:synthetic_technical_fixture') is not True):
        raise ValueError('SYNTHETIC_SCOPE_REQUIRED: real records require a distinct authorized source/review integration')
    if binding.get('source_digest') != digest(source) or binding.get('id') != source.get('id'):
        raise ValueError('FIXTURE_BINDING_STALE')
    if source.get('figure_refs'):
        raise ValueError('FIGURE_MAPPING_UNSUPPORTED: do not substitute a text-only fixture')
    if source.get('extensions', {}).get('wpe:response_type') != 'SINGLE_CHOICE':
        raise ValueError('RESPONSE_MAPPING_UNSUPPORTED')
    opts = source.get('options', [])
    if not opts or any(not isinstance(o, dict) or not o.get('id') or not o.get('text') for o in opts):
        raise ValueError('OPTION_MAPPING_INCOMPLETE')
    if len({o['id'] for o in opts}) != len(opts):
        raise ValueError('OPTION_ID_DUPLICATE')
    if [o['id'] for o in opts] != [chr(65+i) for i in range(len(opts))]:
        raise ValueError('OPTION_LABEL_MAPPING_UNSUPPORTED')
    for key, collection in [('capability_ref', 'capabilities'), ('family_ref', 'question_families')]:
        if binding.get(key) not in {row['id'] for row in package[collection]}:
            raise ValueError('UNRESOLVED_' + key.upper())
    rep=binding.get('representation_ref')
    if rep not in {r['id'] for r in package['representations']}:
        raise ValueError('UNRESOLVED_AUTHORED_REPRESENTATION')
    a = source.get('answer', {})
    if not a.get('summary') or not a.get('reasoning') or not a.get('check'):
        raise ValueError('SOURCE_ANSWER_INCOMPLETE')
    route = binding['reasoning_route']
    if [m['action'] for m in route] != a['reasoning']:
        raise ValueError('REASONING_NOT_SOURCE_BOUND')
    factors = binding['difficulty']['components']
    if set(factors) != set(FACTORS) or any(type(v) is not int or not 0 <= v <= 2 for v in factors.values()):
        raise ValueError('DIFFICULTY_FACTORS_INVALID')
    total = sum(factors.values())
    band = 'D1' if total <= 2 else 'D2' if total <= 5 else 'D3' if total <= 7 else 'D4'
    if binding['difficulty']['score'] != total or binding['difficulty']['band'] != band:
        raise ValueError('DIFFICULTY_MISMATCH')
    q = {
        'id': source['id'], 'version': '0.1.0', 'status': 'CANDIDATE',
        'origin': 'AUTHORED', 'origin_ref': 'SYNTHETIC-ENGINEERING-HANDOFF',
        'original_identifier': 'SYNTHETIC CONTROL ONLY · no examination admission',
        'stem': source['stem'], 'subparts': deepcopy(source.get('subparts', [])),
        'options': [o['text'] for o in opts],
        'conditions': deepcopy(source['conditions']) + ['Synthetic engineering control; independently unreviewed.'],
        'figure_refs': [rep], 'source_refs': [], 'evidence_refs': [],
        'primary_capability_ref': binding['capability_ref'],
        'secondary_capability_refs': [], 'family_ref': binding['family_ref'],
        'adaptation': None, 'exposure': [], 'hints': [],
        'scaffolds': deepcopy(binding['safe_orientation']),
        'response': {'type': 'single_choice'}, 'learner_question_type': 'single_correct_mcq',
        'difficulty': deepcopy(binding['difficulty']),
        'answer': {'kind': 'MODEL_RESPONSE', 'summary': a['summary'],
                   'reasoning': deepcopy(a['reasoning']), 'check': a['check'],
                   'reasoning_route': deepcopy(route), 'crux_move_ref': binding['crux_move_ref'],
                   'acceptable_alternatives': [], 'subpart_answers': [], 'verification_status': 'NOT_RUN'},
        'extensions': {
            'grade9v3:source_custody': {'authority_class': 'OWNER_SUPPLIED_RAW_INPUT',
                'intake_ref': source['id'], 'wording_custody': 'VERBATIM',
                'text_sha256': 'sha256:' + hashlib.sha256(source['stem'].encode()).hexdigest()},
            'grade9v3:analysis': {'learner_question_type': 'single_correct_mcq',
                'difficulty': deepcopy(binding['difficulty']), 'topic': 'Work, Energy and Power',
                'exam_source_badge': 'Synthetic engineering control · not an examination',
                'common_wrong_route': 'Confusing a force magnitude with its work along a displacement.',
                'stable_crux_move': route[1]['action'], 'expected_time_seconds': 0},
            'grade9v3:core2_support_plan': {'protected_move_refs': [binding['crux_move_ref']],
                'support_completions': [{'support_ref': 'scaffolds[' + str(i) + ']',
                    'completed_move_refs': [], 'availability': 'PRE_ATTEMPT_SAFE'}
                    for i in range(len(binding['safe_orientation']))]},
            'wpe:native_integration': {'profile': 'SYNTHETIC_ONLY', 'source_digest': digest(source),
                'binding_digest': digest(binding), 'exam_admission': False,
                'option_identity': [{'source_id': o['id'], 'native_index': i, 'text': o['text']}
                                    for i, o in enumerate(opts)],
                'withheld_original_scaffolds': deepcopy(source.get('scaffolds', [])),
                'support_disposition': 'Original method prompts retained here, not asserted safe; two explicit orientation prompts project.',
                'grading_policy': 'NATIVE_SELF_CHECK_ONLY; received automatic grader is not projected'}
        }
    }
    return q

def inspect_real_projection(record):
    """Deterministic readiness report. No metadata-only path can confer admission."""
    q = record.get('question') or {}
    reasons = ['ACADEMIC_ADMISSION_NOT_ESTABLISHED', 'NATIVE_EXAM_CONVERSION_NOT_AUTHORIZED_BY_THIS_FIXTURE_PROFILE']
    if not str(q.get('stem') or '').strip(): reasons.append('STEM_MISSING')
    if not (q.get('answer') or {}).get('reasoning_route'): reasons.append('NATIVE_ANSWER_ROUTE_MISSING')
    if not (q.get('answer') or {}).get('summary'): reasons.append('NATIVE_ANSWER_SUMMARY_MISSING')
    if q.get('figure_refs') and not record.get('source', {}).get('required_figures_bound'):
        reasons.append('REQUIRED_FIGURES_UNBOUND')
    return {'id': record.get('canonical_id'), 'state': 'HOLD', 'selected': False,
            'admitted': False, 'native_mapping_reasons': reasons, 'source_record_digest': digest(record)}
