"""Render an author dossier, never a Core1A learner lesson. No scripts or unescaped source markup."""
from pathlib import Path
import argparse
import html
import json
from check_handoff import check_file, load


def esc(value):
    return html.escape(str(value), quote=True)


def render(data, result):
    c = data['construction']
    def listing(values):
        return '<ul>' + ''.join('<li>' + esc(v) + '</li>' for v in values) + '</ul>'
    sources = ''.join('<tr><td>' + esc(s['id']) + '</td><td>' + esc(s['role']) +
        '</td><td><a href="' + esc(s['path']) + '">' + esc(s['path']) + '</a></td><td>' +
        esc(s['authority']) + '</td></tr>' for s in data['sources'])
    claims = ''.join('<article><h3>' + esc(c['id']) + ' · UNREVIEWED</h3><p>' + esc(c['statement']) +
        '</p><p>Evidence: ' + ', '.join('<a href="#' + esc(u) + '">' + esc(u) + '</a>' for u in c['unit_refs']) +
        '</p><p>Conditions: ' + esc('; '.join(c['conditions'])) + '</p><p>Open: ' + esc('; '.join(c['disputes'])) + '</p></article>' for c in data['claims'])
    steps = ''.join('<article><h3>' + esc(s['id']) + ' · ' + esc(s['role']) + '</h3><p>' + esc(s['requirement']) +
        '</p><p>Why needed: ' + esc(s['why_needed']) + '</p><p>Depends on: ' + esc(', '.join(s['depends_on']) or 'none') +
        '</p><p>Candidate warrants: ' + esc(', '.join(s['warrant_unit_refs'])) + '</p></article>' for s in data['construction']['steps'])
    units = ''.join('<details id="' + esc(u['id']) + '"><summary>' + esc(u['id']) + ' · ' + esc(u['source_ref']) +
        ' · ' + esc(json.dumps(u['locator'])) + '</summary><pre>' + esc(u['content'] if isinstance(u['content'], str)
        else json.dumps(u['content'], indent=2, ensure_ascii=False)) + '</pre></details>' for u in data['units'])
    holds = ''.join('<li><strong>' + esc(h['id']) + '</strong>: ' + esc(h['detail']) + '</li>' for h in data['holds'])
    mapping = ''.join('<tr><td>' + esc(m['native_property']) + '</td><td>' + esc(m['handoff_pointer']) +
        '</td><td>' + esc(m['action']) + '</td></tr>' for m in data['native_mapping'])
    reps = ''.join('<article><h3>' + esc(r['id']) + ' · ' + esc(r['status']) + '</h3><p>' + esc(r['requirement']) +
        '</p><p>Retained asset: ' + esc(r['asset_ref'] or 'MISSING') + '</p>' + listing([
            v['symbol'] + ' → ' + v['element'] + ': ' + v['in_words'] for v in r['correspondence']]) + '</article>'
        for r in c['representation_needs'])
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + \
        '<title>Core1A source handoff · author dossier</title><style>body{font:17px/1.55 system-ui,sans-serif;max-width:1050px;margin:auto;padding:24px;color:#203047;background:#f7f8fb}h1,h2,h3{line-height:1.2}article,details{background:white;border:1px solid #d5dce5;border-radius:8px;padding:16px;margin:12px 0}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #cbd3df;text-align:left;padding:10px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}.scroll{overflow:auto}.status{border-left:6px solid #a96200;background:#fff4da;padding:16px}a{color:#174ca0}summary{cursor:pointer}</style>' + \
        '<h1>Core1A source handoff</h1><p>WPE work-direction · author preparation dossier</p>' + \
        '<div class="status"><strong>CANDIDATE · Core1A authoring HOLD</strong><br>Mechanical integrity: ' + esc(result['integrity']) + \
        '. Source pin check: ' + esc(result.get('trust_binding', 'NOT_CHECKED')) + \
        '. Semantic review NOT_RUN. No learner lesson, native package or approval is produced.</div>' + \
        '<h2>What the future teacher must construct</h2><p>' + esc(data['construction']['output']) + '</p><p>' + \
        esc(data['construction']['obstacle']) + '</p><p><strong>Decisive bridge requirement:</strong> ' + esc(c['decisive_move']) + \
        '</p><h3>Inputs</h3>' + listing(c['inputs']) + '<h3>Entry assumptions</h3>' + listing(c['entry_assumptions']) + \
        '<h3>Conventions</h3>' + listing(c['conventions']) + '<h2>Source and authority</h2><div class="scroll"><table><tr><th>ID</th><th>Role</th><th>Evidence</th><th>Authority</th></tr>' + \
        sources + '</table></div><h2>Interpreted claims</h2>' + claims + '<h2>Required construction roles</h2>' + steps + \
        '<h2>Representation obligations</h2>' + reps + '<h2>Boundaries</h2>' + listing(c['boundary_requirements']) + \
        '<h2>Wrong-route hypotheses</h2>' + listing(c['wrong_path_candidates']) + '<h2>Independent-check requirements</h2>' + listing(c['check_requirements']) + \
        '<h2>Worked-example obligation</h2><p>' + esc(data['construction']['worked_example_requirement']) + \
        '</p><h2>Question requirement join</h2><p>' + esc('No reviewed Core2 task is joined.' if not data['question_links'] else 'PROPOSED only; no QRT qualification.') + \
        '</p><h2>Native authoring targets</h2><div class="scroll"><table><tr><th>Existing property</th><th>Handoff pointer</th><th>Future action</th></tr>' + mapping + \
        '</table></div><h2>Open issues</h2><ul>' + holds + '</ul><h2>Exact retained source units</h2>' + units + \
        '<h2>Inspection limits</h2><ul>' + ''.join('<li>' + esc(n) + '</li>' for n in data['notes']) + '</ul></html>'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('handoff', type=Path)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--trusted-pins', type=Path)
    p.add_argument('--trusted-pins-sha256')
    args = p.parse_args()
    result = check_file(args.handoff, args.trusted_pins, args.trusted_pins_sha256)
    if result['integrity'] != 'PASS':
        raise SystemExit(json.dumps(result))
    if not args.out.resolve().is_relative_to(args.handoff.resolve().parent):
        raise SystemExit('Output must stay inside the handoff example folder')
    args.out.write_text(render(load(args.handoff), result), encoding='utf-8')
    print(str(args.out))


if __name__ == '__main__':
    main()
