"""Private NSEJS Core2 handoff audit gate: source-neutral, fail-closed.

Does not publish, change, or import source exam materials. It inspects a
recipient-pinned private handoff ZIP and emits a local metadata-only report.
No QRT, official source, figure/key, or academic approval is inferred from
a successful structural check. All five-factor assessments remain unreviewed.
"""
from __future__ import annotations
import argparse, hashlib, json, stat, zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

MARKER='<script id="wpe-data" type="application/json">'
REQUIRED_QRT_FACTORS={
    'concept_model_selection','representation_translation',
    'reasoning_chain_length','algebra_computational_load',
    'trap_exception_sensitivity'
}
APPROVAL='HOLD'

def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()

def safe_member_name(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name and not name.startswith('/') and ':' not in name
                and '\\' not in name and '..' not in p.parts and
                all(part not in ('','.','..') for part in name.split('/')))

def read_handoff(path:Path,expected_sha256:str)->dict[str,bytes]:
    raw=path.read_bytes()
    if sha(raw)!=expected_sha256:
        raise ValueError('PINNED_SOURCE_ZIP_MISMATCH')
    with zipfile.ZipFile(path) as archive:
        entries={}
        total=0
        for item in archive.infolist():
            if item.is_dir():
                continue
            if not safe_member_name(item.filename) or item.filename in entries:
                raise ValueError('UNSAFE_OR_DUPLICATE_ARCHIVE_MEMBER')
            if stat.S_IFMT(item.external_attr>>16)==stat.S_IFLNK:
                raise ValueError('ARCHIVE_SYMLINK_REFUSED')
            total+=item.file_size
            if item.file_size>12_000_000 or total>45_000_000:
                raise ValueError('UNBOUNDED_ARCHIVE_REFUSED')
            entries[item.filename]=archive.read(item)
    if 'HANDOFF_INVENTORY.json' not in entries:
        raise ValueError('HANDOFF_INVENTORY_MISSING')
    manifest=json.loads(entries['HANDOFF_INVENTORY.json'])
    original=manifest.get('files')
    if not isinstance(original,list) or not original:
        raise ValueError('HANDOFF_INVENTORY_UNSUPPORTED')
    expected=set()
    for item in original:
        name=item['path']
        if not safe_member_name(name) or name in expected:
            raise ValueError('HANDOFF_MEMBER_ID_DUPLICATE')
        expected.add(name)
        if name not in entries or len(entries[name])!=item['size_bytes'] or sha(entries[name])!=item['sha256']:
            raise ValueError('HANDOFF_MEMBER_HASH_MISMATCH:'+name)
    # Some original handoffs exclude the README and self-inventory by design.
    if set(entries)-{'HANDOFF_INVENTORY.json','README.md'}!=expected:
        raise ValueError('UNLISTED_OR_MISSING_HANDOFF_MEMBER')
    return entries

def embedded_bank(html:bytes)->dict:
    source=html.decode('utf-8')
    if source.count(MARKER)!=1:raise ValueError('EMBEDDED_SOURCE_MARKER_MISSING')
    start=source.index(MARKER)+len(MARKER)
    end=source.find('</script>',start)
    if end<0:raise ValueError('EMBEDDED_SOURCE_END_MISSING')
    data=json.loads(source[start:end])
    if not isinstance(data.get('questions'),list):
        raise ValueError('QUESTIONS_NOT_ARRAY')
    return data

def scoped_id(q:dict)->str:
    """Never identify an attempt by bare q.id: it may repeat across subjects."""
    parts=[q.get('topic'),q.get('source_id'),q.get('id')]
    if not all(isinstance(p,str) and p.strip() for p in parts):
        raise ValueError('QUESTION_SCOPED_ID_INCOMPLETE')
    return '::'.join(parts)

def audit(entries:dict[str,bytes])->dict:
    files=sorted(name for name in entries if name.endswith('question-status.html'))
    if not files:raise ValueError('NO_CORE2_READER')
    paths={name.rsplit('/',1)[0] for name in files if name.startswith('modules/')}
    blocks={}
    for path in files:
        data=embedded_bank(entries[path])
        questions=data['questions']
        if not questions:raise ValueError('EMPTY_READER:'+path)
        qualified=[scoped_id(q) for q in questions]
        if len(qualified)!=len(set(qualified)):
            raise ValueError('REPEATED_FULL_QUESTION_IDENTITY:'+path)
        bare=[q['id'] for q in questions]
        missing_media=[{'question':scoped_id(q),'name':name}
                       for q in questions for name in q.get('source_figures',[])
                       if not isinstance((data.get('assets') or {}).get(name),str)]
        blocks[path]={
            'count':len(questions),
            'full_identity_count':len(set(qualified)),
            'bare_id_count':len(set(bare)),
            'repeated_bare_ids':dict((k,v) for k,v in Counter(bare).items() if v>1),
            'missing_required_figure_count':len(missing_media),
            # No stems, full questions, private figure bytes or answers in reports.
            'missing_figures':[{'question_sha256':sha(item['question'].encode()),
                                'figure_name_sha256':sha(item['name'].encode())}
                               for item in missing_media],
            'source_key_claims':dict(Counter(str(q.get('key_state','UNSPECIFIED')) for q in questions)),
            'unadmitted':sum(1 for q in questions if q.get('review_state')=='NOT_ADMITTED'),
        }
    packets=[x for x in entries if x.endswith('/source-custody.json') and x.startswith('sources/')]
    factor_errors=[]
    for name in sorted(x for x in entries if x.endswith('/bank.json') and x.startswith('modules/')):
        bank=json.loads(entries[name])
        for q in bank.get('questions',[]):
            diff=q.get('difficulty')
            if diff is None:
                factor_errors.append({'module':name,'reason':'DIFFICULTY_MISSING_OR_OUTSIDE_STANDARD_LOCATION'})
                continue
            if set(diff.get('components',{}))!=REQUIRED_QRT_FACTORS:
                factor_errors.append({'module':name,'reason':'FIVE_CANONICAL_FACTOR_KEYS_MISMATCH'})
                continue
            if not all(type(v) is int and 0<=v<=2 for v in diff['components'].values()):
                factor_errors.append({'module':name,'reason':'FACTOR_SCORE_RANGE_INVALID'})
            elif sum(diff['components'].values())!=diff.get('score'):
                factor_errors.append({'module':name,'reason':'FACTOR_TOTAL_MISMATCH'})
    for name in sorted(x for x in entries if x.endswith('sl2_check_report.json')):
        gate=json.loads(entries[name]).get('gate_summary',{})
        if any(gate.get(k)=='PASS' for k in ('qrt','construction','release')):
            factor_errors.append({'module':name,'reason':'UNATTESTED_GATE_CANNOT_PROVE_ACADEMIC_APPROVAL'})
    aggregate=blocks.get('preview/question-status.html')
    return {
        'schema':'nsejs-core2-private-audit/v1',
        'mode':'READ_ONLY_SOURCE_NEUTRAL_AUTHOR_EXPOSED',
        'source_material_published':False,
        'academic_admission':APPROVAL,
        'independent_qrt_status':'NOT_RUN',
        'official_figures_and_keys':'UNVERIFIED',
        'core1a_core1b_B1_B7':'UNQUALIFIED',
        'exact_aggregate_count':aggregate['count'] if aggregate else None,
        'module_count':len(paths),
        'source_custody_packet_count':len(packets),
        'reader_checks':blocks,
        'source_contract_issues':factor_errors,
        'gate':'HOLD' if (factor_errors or not packets or
             any(b['missing_required_figure_count'] or b['repeated_bare_ids']
                 for b in blocks.values())) else 'HOLD',
        'notes':[
            'Source/official-key claims in the input remain unverified irrespective of byte hashes.',
            'D1/D2 needs an approved Blueprint; the existing D3/D4 draft is not approval.',
            'One nonempty Core1B response plus six visible stages is not B1–B7 qualification.',
            'Run a separately dispatched source-only independent QRT reviewer after original paper custody.',
        ]
    }

def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-zip',type=Path,required=True)
    parser.add_argument('--expected-sha256',required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    if args.report.exists():raise ValueError('REFUSE_OVERWRITE_REPORT')
    report=audit(read_handoff(args.private_zip,args.expected_sha256))
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('CUSTODY_AUDIT_COMPLETE · independent_qrt=NOT_RUN · academic=HOLD')
if __name__=='__main__':main()
