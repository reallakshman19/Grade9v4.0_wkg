"""Read-only mechanical checks for a candidate Core1A source handoff; no promotion."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath

FACTORS = ('concept_model_selection', 'representation_translation', 'reasoning_chain_length',
           'algebra_computational_load', 'trap_exception_sensitivity')
OPERATIONS = {'RETRIEVE', 'EXPLAIN', 'APPLY', 'MODEL', 'REPRESENT', 'SYNTHESIZE', 'JUSTIFY'}
ROLES = {'BOOK_TEXT', 'SOURCE_SCAN', 'DERIVED_FIGURE', 'CANONICAL_CANDIDATE',
         'NATIVE_CONTRACT', 'SYLLABUS', 'QUESTION_EVIDENCE'}
AUTHORITIES = {'OWNER_LOCAL_UNAUTHENTICATED', 'CANDIDATE_REFERENCE', 'LOCAL_CONTRACT'}


class Invalid(ValueError):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(detail)


def require(ok, code, detail):
    if not ok:
        raise Invalid(code, detail)


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'DUPLICATE_JSON_KEY', key)
        out[key] = value
    return out


def bad_constant(value):
    raise Invalid('NONFINITE_JSON', value)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'),
                      object_pairs_hook=unique_pairs, parse_constant=bad_constant)


def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'),
                     allow_nan=False).encode('utf-8')
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inside(root, relative):
    require(isinstance(relative, str) and bool(relative), 'UNSAFE_PATH', repr(relative))
    require('\\' not in relative and ':' not in relative and '\x00' not in relative,
            'UNSAFE_PATH', relative)
    path = Path(relative)
    require(not path.is_absolute() and not PureWindowsPath(relative).drive
            and all(p not in {'.', '..', ''} for p in relative.split('/')),
            'UNSAFE_PATH', relative)
    result = (root / path).resolve()
    require(result.is_relative_to(root.resolve()), 'UNSAFE_PATH', relative)
    return result


def pointer(value, ref):
    require(isinstance(ref, str) and (ref == '' or ref.startswith('/')),
            'BAD_POINTER', repr(ref))
    if not ref:
        return value
    for token in ref[1:].split('/'):
        for pos, char in enumerate(token):
            if char == '~':
                require(pos + 1 < len(token) and token[pos + 1] in '01', 'BAD_POINTER', ref)
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            require(token.isascii() and token.isdecimal() and
                    (token == '0' or not token.startswith('0')), 'BAD_POINTER', ref)
            require(int(token) < len(value), 'BAD_POINTER', ref)
            value = value[int(token)]
        else:
            require(isinstance(value, dict) and token in value, 'BAD_POINTER', ref)
            value = value[token]
    return value


def exact(obj, fields, label):
    require(isinstance(obj, dict) and set(obj) == set(fields.split()),
            'SHAPE', label + ': unexpected or missing fields')


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), 'EMPTY_TEXT', label)


def texts(value, label, nonempty=False):
    require(isinstance(value, list) and (bool(value) or not nonempty), 'SHAPE', label)
    for item in value:
        text(item, label)


def index(rows, label, nonempty=True):
    require(isinstance(rows, list) and (bool(rows) or not nonempty), 'SHAPE', label)
    result = {}
    for row in rows:
        require(isinstance(row, dict), 'SHAPE', label)
        ident = row.get('id')
        text(ident, label + '.id')
        require(ident not in result, 'DUPLICATE_ID', label + ':' + ident)
        result[ident] = row
    return result


def refs(values, target, label, nonempty=True):
    texts(values, label, nonempty)
    require(len(values) == len(set(values)), 'DUPLICATE_REF', label)
    for ref in values:
        require(ref in target, 'UNRESOLVED_REF', label + ':' + ref)


def _check(data, root, trusted_pins=None, trusted_pins_sha256=None):
    exact(data, 'schema id status purpose sources units claims binding construction question_links native_mapping holds review notes', 'root')
    require(data['schema'] == 'core1a-source-handoff/v1', 'SCHEMA', 'unsupported profile')
    require(data['status'] == 'CANDIDATE' and data['purpose'] == 'CORE1A_PREPARATION',
            'PROMOTION_FORBIDDEN', 'R1 is preparation only')
    text(data['id'], 'id')
    trust_binding = 'SELF_DECLARED_ONLY'
    if trusted_pins is not None or trusted_pins_sha256 is not None:
        require(trusted_pins is not None and isinstance(trusted_pins_sha256, str) and
                len(trusted_pins_sha256) == 64, 'TRUST_ANCHOR_REQUIRED', 'provide pin file and its externally expected SHA-256')
        require(file_sha(Path(trusted_pins)) == trusted_pins_sha256, 'TRUST_ANCHOR_MISMATCH', 'pin file differs from expected digest')
        pinset = load(trusted_pins)
        exact(pinset, 'schema sources', 'source pins')
        require(pinset['schema'] == 'source-pin-set/v1', 'TRUST_ANCHOR_REQUIRED', 'unsupported pin profile')
        pinned_sources = index(pinset['sources'], 'pinned sources')
        actual_sources = index(data['sources'], 'sources')
        require(digest(pinned_sources) == digest(actual_sources), 'SOURCE_PIN_MISMATCH', 'source identities differ from external pins')
        trust_binding = 'EXTERNAL_PIN_BYTES_MATCH'
    sources = index(data['sources'], 'sources')
    paths = {}
    for ident, source in sources.items():
        exact(source, 'id path sha256 role authority', ident)
        require(source['role'] in ROLES and source['authority'] in AUTHORITIES,
                'SOURCE_ROLE', ident)
        if source['role'] == 'CANONICAL_CANDIDATE':
            require(source['authority'] == 'CANDIDATE_REFERENCE', 'SOURCE_AUTHORITY', ident)
        if source['role'] == 'NATIVE_CONTRACT':
            require(source['authority'] == 'LOCAL_CONTRACT', 'SOURCE_AUTHORITY', ident)
        expected = source['sha256']
        require(isinstance(expected, str) and len(expected) == 64 and
                all(c in '0123456789abcdef' for c in expected), 'HASH_FORMAT', ident)
        path = inside(root, source['path'])
        require(path.is_file(), 'MISSING_ASSET', ident)
        require(file_sha(path) == expected, 'SOURCE_HASH_MISMATCH', ident)
        paths[ident] = path
    units = index(data['units'], 'units')
    for ident, unit in units.items():
        exact(unit, 'id source_ref kind locator content digest', ident)
        require(unit['source_ref'] in sources, 'UNRESOLVED_REF', ident)
        path = paths[unit['source_ref']]
        if unit['kind'] == 'LINES':
            exact(unit['locator'], 'start end', ident + '.locator')
            start, end = unit['locator']['start'], unit['locator']['end']
            lines = path.read_text(encoding='utf-8-sig').splitlines()
            require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                    'BAD_LOCATOR', ident)
            actual = '\n'.join(lines[start - 1:end])
        elif unit['kind'] == 'JSON_POINTER':
            exact(unit['locator'], 'pointer', ident + '.locator')
            actual = pointer(load(path), unit['locator']['pointer'])
        else:
            raise Invalid('UNSUPPORTED_EXTRACTION', ident)
        require(digest(actual) == digest(unit['content']), 'SOURCE_CORRESPONDENCE', ident)
        require(unit['digest'] == digest(unit['content']), 'UNIT_DIGEST', ident)
    claims = index(data['claims'], 'claims')
    for ident, claim in claims.items():
        exact(claim, 'id statement unit_refs conditions disputes qualification', ident)
        text(claim['statement'], ident)
        refs(claim['unit_refs'], units, ident)
        texts(claim['conditions'], ident + '.conditions', True)
        texts(claim['disputes'], ident + '.disputes')
        require(claim['qualification'] == 'UNREVIEWED', 'PROMOTION_FORBIDDEN', ident)
    binding = data['binding']
    exact(binding, 'spine_node spine_unit_ref microtopic_id capability_id library_unit_ref relation_unit_refs', 'binding')
    text(binding['spine_node'], 'spine_node')
    require(binding['spine_unit_ref'] in units, 'UNRESOLVED_REF', 'binding.spine_unit_ref')
    spine_unit = units[binding['spine_unit_ref']]
    require(sources[spine_unit['source_ref']]['role'] == 'SYLLABUS' and
            isinstance(spine_unit['content'], str) and
            binding['spine_node'] in [cell.strip() for cell in spine_unit['content'].split('|')],
            'SYLLABUS_BINDING', 'node must match a retained syllabus table row')
    require(binding['library_unit_ref'] in units, 'UNRESOLVED_REF', 'binding.library_unit_ref')
    lib_unit = units[binding['library_unit_ref']]
    require(sources[lib_unit['source_ref']]['role'] == 'CANONICAL_CANDIDATE',
            'LIBRARY_BINDING', 'binding must point to canonical candidate')
    micro = lib_unit['content']
    require(isinstance(micro, dict) and micro.get('id') == binding['microtopic_id'] and
            micro.get('primary_capability_ref') == binding['capability_id'],
            'LIBRARY_BINDING', 'microtopic or capability differs')
    refs(binding['relation_unit_refs'], units, 'binding.relations')
    for ref in binding['relation_unit_refs']:
        require(sources[units[ref]['source_ref']]['role'] == 'CANONICAL_CANDIDATE' and
                isinstance(units[ref]['content'], dict) and
                'conditions' in units[ref]['content'], 'WARRANT_BINDING', ref)
    c = data['construction']
    exact(c, 'inputs output obstacle decisive_move entry_assumptions conventions steps representation_needs worked_example_requirement boundary_requirements wrong_path_candidates check_requirements', 'construction')
    for field in ['inputs', 'entry_assumptions', 'conventions', 'boundary_requirements',
                  'wrong_path_candidates', 'check_requirements']:
        texts(c[field], 'construction.' + field, True)
    for field in ['output', 'obstacle', 'decisive_move', 'worked_example_requirement']:
        text(c[field], 'construction.' + field)
    steps = index(c['steps'], 'steps')
    for ident, step in steps.items():
        exact(step, 'id role requirement why_needed unit_refs claim_refs warrant_unit_refs depends_on', ident)
        require(step['role'] in {'INPUT','REPRESENT','CONNECT','TRANSFORM','VERIFY','BOUNDARY'}, 'STEP_ROLE', ident)
        text(step['requirement'], ident)
        text(step['why_needed'], ident + '.why_needed')
        refs(step['unit_refs'], units, ident + '.units')
        refs(step['claim_refs'], claims, ident + '.claims')
        refs(step['warrant_unit_refs'], units, ident + '.warrants')
        for ref in step['warrant_unit_refs']:
            require(sources[units[ref]['source_ref']]['role'] == 'CANONICAL_CANDIDATE',
                    'WARRANT_BINDING', ident + ':' + ref)
        refs(step['depends_on'], steps, ident + '.dependencies', False)
    visiting, visited = set(), set()
    def visit(ident):
        require(ident not in visiting, 'DEPENDENCY_CYCLE', ident)
        if ident in visited:
            return
        visiting.add(ident)
        for dep in steps[ident]['depends_on']:
            visit(dep)
        visiting.remove(ident)
        visited.add(ident)
    for ident in steps:
        visit(ident)
    for ident, rep in index(c['representation_needs'], 'representations').items():
        exact(rep, 'id asset_ref status correspondence requirement', ident)
        text(rep['requirement'], ident)
        require(rep['status'] in {'MISSING', 'DERIVED_UNREVIEWED'}, 'REPRESENTATION_STATUS', ident)
        if rep['asset_ref'] is None:
            require(rep['status'] == 'MISSING', 'REPRESENTATION_STATUS', ident)
        else:
            require(rep['asset_ref'] in sources and
                    sources[rep['asset_ref']]['role'] == 'DERIVED_FIGURE' and
                    rep['status'] == 'DERIVED_UNREVIEWED', 'FIGURE_ROLE', ident)
        require(isinstance(rep['correspondence'], list) and
                (bool(rep['correspondence']) or rep['asset_ref'] is None),
                'SHAPE', ident + '.correspondence')
        for row in rep['correspondence']:
            exact(row, 'symbol element in_words', ident + '.correspondence')
            for field in row:
                text(row[field], ident + '.' + field)
    for ident, link in index(data['question_links'], 'question_links', False).items():
        exact(link, 'id question_unit_ref question_id source_role operation demand status', ident)
        require(link['status'] == 'PROPOSED', 'PROMOTION_FORBIDDEN', ident)
        require(link['source_role'] in {'DIRECT_EXAM_EVIDENCE', 'PREREQUISITE_BRIDGE'}, 'SOURCE_ROLE', ident)
        require(link['question_unit_ref'] in units, 'UNRESOLVED_REF', ident)
        u = units[link['question_unit_ref']]
        require(sources[u['source_ref']]['role'] == 'QUESTION_EVIDENCE' and
                isinstance(u['content'], dict) and u['content'].get('id') == link['question_id'],
                'QUESTION_BINDING', ident)
        require(link['operation'] in OPERATIONS, 'OPERATION', ident)
        demand = link['demand']
        if demand is not None:
            exact(demand, 'factors score band evidence', ident + '.demand')
            require(isinstance(demand['factors'], dict) and set(demand['factors']) == set(FACTORS), 'DEMAND_FACTORS', ident)
            require(all(type(v) is int and 0 <= v <= 2 for v in demand['factors'].values()), 'DEMAND_FACTORS', ident)
            score = sum(demand['factors'].values())
            band = 'D1' if score <= 2 else 'D2' if score <= 5 else 'D3' if score <= 7 else 'D4'
            require(type(demand['score']) is int and demand['score'] == score and demand['band'] == band,
                    'DEMAND_ARITHMETIC', ident)
            require(isinstance(demand['evidence'], dict) and set(demand['evidence']) == set(FACTORS), 'DEMAND_EVIDENCE', ident)
            for evidence in demand['evidence'].values():
                text(evidence, ident + '.factor evidence')
    require(isinstance(data['native_mapping'], list) and bool(data['native_mapping']), 'SHAPE', 'native_mapping')
    for mapping in data['native_mapping']:
        exact(mapping, 'schema_unit_ref native_property handoff_pointer action', 'native_mapping')
        ref = mapping['schema_unit_ref']
        require(ref in units and sources[units[ref]['source_ref']]['role'] == 'NATIVE_CONTRACT',
                'NATIVE_MAPPING', str(ref))
        schema = units[ref]['content']
        require(isinstance(schema, dict) and mapping['native_property'] in schema.get('properties', {}),
                'NATIVE_MAPPING', str(mapping['native_property']))
        pointer(data, mapping['handoff_pointer'])
        require(mapping['action'] in {'AUTHOR_FROM_EVIDENCE', 'RESOLVE_EXISTING_REFS', 'AUTHOR_DISTINCT_EXAMPLE'},
                'NATIVE_MAPPING', 'not an authoring target')
    for ident, hold in index(data['holds'], 'holds').items():
        exact(hold, 'id detail affects', ident)
        text(hold['detail'], ident)
        texts(hold['affects'], ident + '.affects', True)
    require(data['review'] == {'semantic': 'NOT_RUN', 'core2_owner_approval': 'PENDING',
                              'core1a_authoring': 'NOT_STARTED', 'core1b_correspondence': 'NOT_RUN'},
            'PROMOTION_FORBIDDEN', 'R1 cannot accept review/approval claims')
    texts(data['notes'], 'notes', True)
    return {'integrity': 'PASS', 'trust_binding': trust_binding,
            'preparation': 'CANDIDATE', 'core1a_authoring': 'HOLD',
            'semantic_review': 'NOT_RUN', 'native_package': 'NOT_EMITTED',
            'sources_checked': len(sources), 'units_checked': len(units),
            'claims': len(claims), 'required_steps': len(steps),
            'question_links': len(data['question_links']), 'holds': data['holds'],
            'limitations': ['No scientific or pedagogical qualification',
                            'No authentication of sources or reviewers',
                            'No runtime/reveal/first-save validation',
                            'Paraphrase and diagram meaning require semantic review']}


def check(data, root, trusted_pins=None, trusted_pins_sha256=None):
    try:
        return _check(data, Path(root).resolve(), trusted_pins, trusted_pins_sha256)
    except Invalid as exc:
        return {'integrity': 'INVALID', 'findings': [{'code': exc.code, 'detail': exc.detail}],
                'core1a_authoring': 'HOLD', 'semantic_review': 'NOT_RUN'}
    except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, RecursionError) as exc:
        return {'integrity': 'INVALID', 'findings': [{'code': 'MALFORMED_OR_UNREADABLE', 'detail': str(exc)}],
                'core1a_authoring': 'HOLD', 'semantic_review': 'NOT_RUN'}


def check_file(path, trusted_pins=None, trusted_pins_sha256=None):
    path = Path(path)
    try:
        return check(load(path), path.parent, trusted_pins, trusted_pins_sha256)
    except (Invalid, OSError, ValueError) as exc:
        return {'integrity': 'INVALID', 'findings': [{'code': getattr(exc, 'code', 'UNREADABLE_JSON'),
                                                     'detail': str(exc)}], 'core1a_authoring': 'HOLD'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('handoff', type=Path)
    parser.add_argument('--trusted-pins', type=Path)
    parser.add_argument('--trusted-pins-sha256', help='Expected digest obtained through the trusted receipt, not read from the dossier')
    args = parser.parse_args()
    result = check_file(args.handoff, args.trusted_pins, args.trusted_pins_sha256)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['integrity'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
