"""Source-preserving *private review* reader integration. Not a public publisher.

Run this against independently received, locally pinned candidate input files.
The builder never edits its sources or claims academic/source authenticity. It may
produce private review HTML containing input question material, so do NOT commit
or deploy output. Its public tests use only synthetic questions.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

ROOT_MARKER = '<script id="wpe-data" type="application/json">'
END_MARKER = '</script>'
HOLD_MARKER = 'Required diagram unavailable'
MANIFEST_NAME = 'PRIVATE_REVIEW_MANIFEST.json'
OUTPUT_MARKER = '.GRADE9_PRIVATE_REVIEW_ONLY'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: object) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def relative_path(root: Path, value: str) -> Path:
    """Reject traversal, symlink hops, rooted URLs, and Windows path tricks."""
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise ValueError('UNSAFE_INPUT_PATH')
    pp = PurePosixPath(value)
    if pp.is_absolute() or any(x in ('', '.', '..') for x in value.split('/')) or ':' in value:
        raise ValueError('UNSAFE_INPUT_PATH')
    dest = root.joinpath(*pp.parts)
    if not dest.resolve().is_relative_to(root) or any(x.is_symlink() for x in [dest, *dest.parents] if x != root.parent):
        raise ValueError('UNSAFE_INPUT_PATH')
    if not dest.is_file():
        raise ValueError('MISSING_INPUT_FILE')
    return dest


def identity(question: dict) -> tuple[str, str, str]:
    return (str(question.get('topic', '')), str(question.get('source_id', '')), str(question.get('id', '')))


def read_reader(path: Path, expected: str) -> tuple[str, dict]:
    raw = path.read_bytes()
    if sha(raw) != expected:
        raise ValueError('PINNED_INPUT_CHANGED')
    source = raw.decode('utf-8')
    if source.count(ROOT_MARKER) != 1:
        raise ValueError('EMBEDDED_DATA_MARKER_NOT_UNIQUE')
    st = source.index(ROOT_MARKER) + len(ROOT_MARKER)
    en = source.find(END_MARKER, st)
    if en < 0:
        raise ValueError('MISSING_DATA_END')
    data = json.loads(source[st:en])
    if not isinstance(data, dict) or not isinstance(data.get('questions'), list):
        raise ValueError('QUESTION_LIST_MISSING')
    if 'function questionKey(q)' not in source or HOLD_MARKER not in source:
        raise ValueError('READER_MISSING_SCOPED_ID_OR_FIGURE_HOLD')
    if 'data.assets[figName]' in source:
        raise ValueError('UNGUARDED_ASSET_LOOKUP')
    return source, data


def safe_svg(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        root = ET.fromstring(value)
    except ET.ParseError:
        return False
    allowed = {'svg', 'g', 'path', 'line', 'circle', 'rect', 'text',
               'tspan', 'polyline', 'polygon', 'ellipse', 'defs', 'marker'}
    if root.tag.rsplit('}', 1)[-1] != 'svg':
        return False
    for element in root.iter():
        if element.tag.rsplit('}', 1)[-1] not in allowed:
            return False
        for key, val in element.attrib.items():
            name = key.rsplit('}', 1)[-1].lower()
            if name.startswith('on') or name in {'href', 'src', 'style', 'formaction'}:
                return False
            if 'javascript:' in val.lower() or 'url(' in val.lower():
                return False
    return True


def embed(template: str, data: dict) -> str:
    st = template.index(ROOT_MARKER) + len(ROOT_MARKER)
    en = template.index(END_MARKER, st)
    payload = canonical_json(data)
    if '</script' in payload.lower() or '<!--' in payload:
        raise ValueError('UNSAFE_EMBEDDED_DATA')
    out = template[:st] + payload + template[en:]
    safe_header = (
        '<header><h1>Private technical review · Source-unverified candidate reader</h1>'
        '<p>Original exam identity, figures, answer keys and scientific correctness '
        'have not been independently qualified.</p>'
        '<p>HOLD · NOT FOR PUBLICATION · NO ACADEMIC APPROVAL</p></header>'
    )
    out, n = re.subn(r'(?s)<header\b[^>]*>.*?</header>', lambda _: safe_header, out, count=1)
    if n != 1:
        raise ValueError('HEADER_MISSING')
    # Older candidate pages have a second, non-header original-exam claim.
    # Replace only presentation copy; never alter the embedded question data.
    out = re.sub(
        r'(?is)<p\s+class=["\']subtitle["\'][^>]*>.*?</p>',
        lambda _: '<p class="subtitle">Candidate records — original exam status unverified</p>',
        out, count=1
    )
    if re.search(r'\b\d+\s+authentic\s+(?:items|questions)\b', out, re.I):
        raise ValueError('UNVERIFIED_ORIGINAL_CLAIM_REMAINS')
    return out


def hub(entries: list[tuple[str, str, int]], missing: int) -> str:
    rows = ''.join(
        f'<li><a href="{html.escape(url, quote=True)}">{html.escape(name)}</a> '
        f'({count} candidate records)</li>' for name, url, count in entries
    )
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>Private reader review</title></head><body><main>"
            "<h1>Private technical reader review — HOLD</h1>"
            "<p>Source authenticity, scientific review and QRT approval are not established. "
            "NOT FOR PUBLICATION.</p>"
            f"<p>Unavailable required diagram references: {missing}.</p><ul>{rows}</ul>"
            "</main></body></html>\n")


def load_manifest(root: Path, path: Path) -> tuple[dict, list[dict]]:
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if manifest.get('version') != 1 or manifest.get('review_only') is not True:
        raise ValueError('INVALID_PRIVATE_MANIFEST')
    aggregate = manifest.get('aggregate')
    modules = manifest.get('modules')
    if not isinstance(aggregate, dict) or not isinstance(modules, list) or not modules:
        raise ValueError('INVALID_PRIVATE_MANIFEST')
    seen_paths, seen_topics, seen_slugs = set(), set(), set()
    for item in [aggregate, *modules]:
        if not isinstance(item, dict) or set(item) - {'path', 'sha256', 'topic', 'slug', 'count'}:
            raise ValueError('INVALID_PRIVATE_MANIFEST')
        digest = item.get('sha256')
        if not isinstance(digest, str) or re.fullmatch(r'[a-f0-9]{64}', digest) is None:
            raise ValueError('INVALID_PRIVATE_MANIFEST')
        path_value = item.get('path')
        if path_value in seen_paths:
            raise ValueError('DUPLICATE_INPUT_PATH')
        seen_paths.add(path_value)
        if not isinstance(path_value, str) or not path_value.endswith('.html'):
            raise ValueError('INVALID_PRIVATE_MANIFEST')
        relative_path(root, path_value)
    for mod in modules:
        slug, topic = mod.get('slug'), mod.get('topic')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-z][a-z0-9-]{1,62}', slug):
            raise ValueError('INVALID_MODULE_SLUG')
        if not isinstance(topic, str) or not re.fullmatch(r'[A-Z][A-Z0-9_]{1,62}', topic):
            raise ValueError('INVALID_TOPIC_ID')
        if slug in seen_slugs or topic in seen_topics:
            raise ValueError('DUPLICATE_MODULE_SCOPE')
        seen_slugs.add(slug);seen_topics.add(topic)
        if not isinstance(mod.get('count'), int) or mod['count'] < 1:
            raise ValueError('INVALID_MODULE_COUNT')
    if not isinstance(aggregate.get('count'), int) or aggregate['count'] < 1:
        raise ValueError('INVALID_AGGREGATE_COUNT')
    if sum(m['count'] for m in modules) != aggregate['count']:
        raise ValueError('INCONSISTENT_MANIFEST_COUNTS')
    expected_missing = manifest.get('expected_missing_figures')
    if not isinstance(expected_missing, int) or expected_missing < 0:
        raise ValueError('INVALID_MISSING_FIGURE_EXPECTATION')
    return manifest, modules


def tree_digest(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): sha(p.read_bytes()) for p in root.rglob('*')
            if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts
            and '.pytest_cache' not in p.parts}


def build(root: Path, out: Path, manifest_path: Path, publish: bool = False) -> dict:
    if publish:
        raise ValueError('PUBLIC_RELEASE_FORBIDDEN')
    root, out = root.resolve(), out.absolute()
    if not root.is_dir() or out.is_symlink() or out.resolve().is_relative_to(root) or out.resolve() == root.parent:
        raise ValueError('UNSAFE_OUTPUT_PATH')
    if out.exists() and (not out.is_dir() or not (out / OUTPUT_MARKER).is_file()):
        raise ValueError('OUTPUT_NOT_OWNED_BY_BUILDER')
    pins, modules = load_manifest(root, manifest_path)
    before = tree_digest(root)
    agg_spec = pins['aggregate']
    template, data = read_reader(relative_path(root, agg_spec['path']), agg_spec['sha256'])
    questions = data['questions']
    agg_map = {identity(q): q for q in questions}
    if len(questions) != agg_spec['count'] or len(agg_map) != len(questions):
        raise ValueError('AGGREGATE_CENSUS_OR_DUPLICATE_IDENTITY')
    assets: dict[str, str] = {}
    outputs: dict[str, bytes] = {}
    expected_keys: set[tuple[str, str, str]] = set()
    entries = [('Combined reader', 'preview/question-status.html', len(questions))]
    for item in modules:
        slug, topic = item['slug'], item['topic']
        page_html, module_data = read_reader(relative_path(root, item['path']), item['sha256'])
        module_q = module_data['questions']
        if len(module_q) != item['count']:
            raise ValueError('MODULE_CENSUS_MISMATCH')
        for q in module_q:
            normalized = {**q, 'topic': topic}
            key = identity(normalized)
            if key in expected_keys or key not in agg_map or normalized != agg_map[key]:
                raise ValueError('SOURCE_TO_AGGREGATE_MISMATCH')
            expected_keys.add(key)
        module_assets = module_data.get('assets', {})
        if not isinstance(module_assets, dict):
            raise ValueError('MODULE_ASSET_MAP_INVALID')
        for key, value in module_assets.items():
            if not isinstance(key, str) or not safe_svg(value):
                raise ValueError('UNSAFE_CANDIDATE_ASSET')
            if key in assets and value != assets[key]:
                raise ValueError('ASSET_COLLISION')
            assets[key] = value
        out_path = f'modules/{slug}/question-status.html'
        outputs[out_path] = embed(page_html, {**module_data, 'questions':
                                   [{**q, 'topic': topic} for q in module_q]}).encode('utf-8')
        entries.append((slug, out_path, item['count']))
    if expected_keys != set(agg_map):
        raise ValueError('AGGREGATE_UNCOVERED_RECORDS')
    aggregate_assets = data.get('assets', {})
    if not isinstance(aggregate_assets, dict):
        raise ValueError('AGGREGATE_ASSET_MAP_INVALID')
    for key, value in aggregate_assets.items():
        if not isinstance(key, str) or not safe_svg(value):
            raise ValueError('UNSAFE_CANDIDATE_ASSET')
        if key in assets and assets[key] != value:
            raise ValueError('ASSET_COLLISION')
        assets[key] = value
    for q in questions:
        if not isinstance(q.get('source_figures', []), list):
            raise ValueError('FIGURE_REFERENCE_INVALID')
    figures = [(identity(q), asset, asset in assets)
               for q in questions for asset in q.get('source_figures', [])]
    missing = sum(not available for _, _, available in figures)
    if missing != pins['expected_missing_figures']:
        raise ValueError('FIGURE_INVENTORY_CHANGED')
    outputs['preview/question-status.html'] = embed(template, {**data, 'assets': assets}).encode('utf-8')
    outputs['index.html'] = hub(entries, missing).encode('utf-8')
    receipt = {
        'schema_version': 'private-review.v1', 'release_authority': 'HOLD',
        'purpose': 'REVIEW_ONLY_NOT_FOR_PUBLICATION',
        'source_authenticity': 'UNKNOWN_SOURCE',
        'academic_approval': 'HOLD',
        'record_count': len(questions), 'module_count': len(modules),
        'figure_refs': len(figures), 'missing_figures': missing,
        'source_question_digest': sha(canonical_json(questions).encode('utf-8')),
        'input_manifest_digest': sha(manifest_path.read_bytes()),
        'output_files': {key: sha(value) for key, value in sorted(outputs.items())}
    }
    outputs[MANIFEST_NAME] = (canonical_json(receipt) + '\n').encode('utf-8')
    outputs[OUTPUT_MARKER] = b'PRIVATE REVIEW ONLY - NEVER DEPLOY\n'
    if tree_digest(root) != before:
        raise RuntimeError('SOURCE_TREE_MUTATED_DURING_READ')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='g9-private-', dir=out.parent) as tmp:
        staged = Path(tmp) / 'site'
        staged.mkdir()
        for key, value in outputs.items():
            dest = staged / key
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(value)
        if out.exists():
            shutil.rmtree(out)
        shutil.move(str(staged), str(out))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--publish', action='store_true', help='always prohibited')
    a = parser.parse_args()
    receipt = build(a.root, a.out, a.manifest, a.publish)
    print('PASS private review only records=%d figures missing=%d' %
          (receipt['record_count'], receipt['missing_figures']))


if __name__ == '__main__':
    main()
