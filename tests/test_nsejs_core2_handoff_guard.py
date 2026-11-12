"""Synthetic-only exact reader renderer & archive controls (no source exams)."""
from __future__ import annotations
import hashlib,json,subprocess,sys,zipfile
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from nsejs_core2_handoff_guard import (
    patch_reader,repair_zip,embedded,revisions,question_key,secure_zip,
    inspect_inventory,digest
)

FIXTURE=ROOT/'tests/fixtures/nsejs_core2_legacy_synthetic.html'

def fixture_zip(tmp:Path)->Path:
    original=FIXTURE.read_bytes()
    members={
        'preview/question-status.html':original,
        'modules/nsejs-alpha-r1/question-status.html':original,
        'README.md':b'SYNTHETIC PRIVATE TECHNICAL TEST, NO EXAM MATERIAL',
    }
    receipt={'files':[{'path':k,'size_bytes':len(v),'sha256':digest(v)}
                      for k,v in members.items() if k!='README.md'],
             'file_count':2,'status':'SYNTHETIC_HOLD'}
    members['HANDOFF_INVENTORY.json']=json.dumps(receipt).encode()
    path=tmp/'fixture.zip'
    with zipfile.ZipFile(path,'w') as z:
        for k,v in members.items():z.writestr(k,v)
    return path

def test_scoped_questions_and_missing_diagram_holds():
    html=FIXTURE.read_text()
    out,stats=patch_reader(html)
    assert stats['question_count']==2 and stats['scoped_count']==2
    assert stats['unscoped_count']==1 and stats['duplicate_ids']=={'SYN-DUP-ID':2}
    assert stats['missing_figures']==2
    assert embedded(html)[1]==embedded(out)[1]
    assert 'REQUIRED DIAGRAM UNAVAILABLE' in out
    assert 'G9PrivateCore2Store' in out
    assert 'Ambiguous' not in html or 'legacy' in out
    assert 'KEY AUTHORITY HOLD' in out
    assert 'NOT FOR PUBLICATION' in out
    assert out.count('g9-nsejs-private-core2-revisions')>=2

def test_source_specific_revision_changes_on_any_relevant_bytes():
    data=embedded(FIXTURE.read_text())[0]
    q=data['questions'][0]
    k=question_key(q)
    a=revisions(data)[k]
    alt=json.loads(json.dumps(data));alt['questions'][0]['options'][0]='New synthetic option'
    assert revisions(alt)[k]!=a
    alt=json.loads(json.dumps(data));alt['assets']={'synthetic-required-diagram.svg':'<svg></svg>'}
    assert revisions(alt)[k]!=a
    alt=json.loads(json.dumps(data));alt['questions'][0]['answer']='Changed'
    assert revisions(alt)[k]!=a
    assert k!=question_key(data['questions'][1])

def test_archive_repair_is_private_preserves_original_source_and_records_exact_diff(tmp_path):
    src=fixture_zip(tmp_path)
    out=tmp_path/'repaired.zip'
    receipt=repair_zip(src,out,digest(src.read_bytes()))
    assert receipt['academic_admission']=='HOLD'
    assert receipt['independent_qrt']=='NOT_RUN'
    assert receipt['source_key_verification']=='HOLD'
    assert receipt['status']=='PRIVATE_CANDIDATE_TECHNICAL_FIX_ACADEMIC_HOLD'
    assert receipt['publish'] is False
    with zipfile.ZipFile(src) as before,zipfile.ZipFile(out) as after:
        old=set(before.namelist());new=set(after.namelist())
        assert new-old=={'PRIVATE_REPAIR_RECEIPT.json'}
        for name in old:
            if name.endswith('question-status.html'):
                assert embedded(before.read(name).decode())[1]==embedded(after.read(name).decode())[1]
            else:
                assert before.read(name)==after.read(name)
        assert len([x for x in new if x.endswith('question-status.html')])==2
    with pytest.raises(ValueError,match='OUTPUT_ALREADY_EXISTS'):
        repair_zip(src,out,digest(src.read_bytes()))

def test_bad_sha_and_tampered_manifest_refused(tmp_path):
    src=fixture_zip(tmp_path)
    with pytest.raises(ValueError,match='UNTRUSTED_OR_CHANGED_HANDOFF_ZIP'):
        repair_zip(src,tmp_path/'out.zip','0'*64)
    with zipfile.ZipFile(src,'a') as z:z.writestr('unlisted-private-file.txt','unexpected')
    with pytest.raises(ValueError,match='UNLISTED_OR_MISSING_ORIGINAL_FILES'):
        repair_zip(src,tmp_path/'out.zip',digest(src.read_bytes()))

def test_duplicate_full_identity_unsupported_shape_and_js_injections_refused():
    data=embedded(FIXTURE.read_text())[0]
    bad=json.loads(json.dumps(data));bad['questions'][1]=bad['questions'][0].copy()
    src=FIXTURE.read_text();start=src.index('<script id="wpe-data" type="application/json">')
    old=embedded(src)[1]
    src=src.replace(old,json.dumps(bad),1)
    with pytest.raises(ValueError,match='DUPLICATED_SCOPED_QUESTION_IDENTITY'):
        patch_reader(src)
    with pytest.raises(ValueError,match='UNKNOWN_READER_RUNTIME'):
        patch_reader(FIXTURE.read_text().replace('  const attempts = new Map();',''))
    with pytest.raises(ValueError,match='EMBEDDED_BANK_MARKER_NOT_UNIQUE'):
        patch_reader(FIXTURE.read_text().replace('<script id="wpe-data"','<script id="broken-data"'))

def test_node_syntax_and_negative_no_original_exam_records(tmp_path):
    patched,_=patch_reader(FIXTURE.read_text())
    runtime=patched.rsplit('<script>',1)[1].split('</script>',1)[0]
    proc=subprocess.run(['node','--check'],input=runtime,capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    assert 'An ant is sitting' not in patched
    assert 'NSEJS-2024-P-Q' not in patched
    assert '<iframe' not in patched.lower()
