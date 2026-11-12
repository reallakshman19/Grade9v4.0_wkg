"""Synthetic-only controls for private NSEJS Core2 50-source audit.

Original exam stems, options and diagrams are NEVER included in CI fixtures.
"""
from __future__ import annotations
import hashlib,io,json,sys,zipfile
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from nsejs_core2_private_audit import (sha,read_handoff,scoped_id,embedded_bank,audit)

def sample(question_id='SHARED-Q',source='SYN-ONE',topic='ALPHA',figure='absent.svg'):
    return {'id':question_id,'source_id':source,'topic':topic,
            'stem':'Synthetic object changes speed on a straight line',
            'options':['Symbol A','Symbol B'],'answer':'A',
            'source_figures':[figure] if figure else [],'key_state':'UNVERIFIED',
            'review_state':'NOT_ADMITTED','band':'D2','op':'APPLY'}

def html(data):
    return ('<!doctype html><html><body><script id="wpe-data" type="application/json">'+
            json.dumps(data,sort_keys=True)+'</script></body></html>').encode('utf-8')

def bank():
    return {'questions':[{'id':'SYN-A','difficulty':{'band':'D2','score':4,
        'components':{'concept_model_selection':1,'representation_translation':1,
        'reasoning_chain_length':1,'algebra_computational_load':1,
        'trap_exception_sensitivity':0}}}]}

def fixture(tmp,invalid=False):
    files={
        'preview/question-status.html':html({'questions':[sample(),sample(topic='BETA',source='SYN-TWO')]}),
        'modules/nsejs-alpha-r1/question-status.html':html({'questions':[sample()]}),
        'modules/nsejs-beta-r1/question-status.html':html({'questions':[sample(topic='BETA',source='SYN-TWO')]}),
        'modules/nsejs-alpha-r1/bank.json':json.dumps(bank()).encode(),
        'modules/nsejs-beta-r1/bank.json':json.dumps(bank()).encode(),
        'sources/nsejs/SYN-A/source-custody.json':b'{"status":"CANDIDATE"}',
        'README.md':b'SYNTHETIC FIXTURE NOT AN EXAM',
    }
    if invalid:
        b=bank()
        b['questions'][0]['difficulty']['components']={'noncanonical':4}
        files['modules/nsejs-beta-r1/bank.json']=json.dumps(b).encode()
    receipt={'files':[{'path':p,'size_bytes':len(raw),'sha256':sha(raw)}
                      for p,raw in files.items() if p!='README.md']}
    files['HANDOFF_INVENTORY.json']=json.dumps(receipt).encode()
    out=tmp/'fixture.zip'
    with zipfile.ZipFile(out,'w') as zipf:
        for p,raw in files.items():zipf.writestr(p,raw)
    return out

def test_synthetic_scoped_identity_keeps_two_repeated_bare_ids_separate():
    a=sample()
    b=sample(topic='BETA',source='SYN-TWO')
    assert a['id']==b['id']
    assert scoped_id(a)!=scoped_id(b)

def test_synthetic_figure_missing_and_key_claims_do_not_become_approvals(tmp_path):
    path=fixture(tmp_path)
    files=read_handoff(path,sha(path.read_bytes()))
    out=audit(files)
    assert out['gate']=='HOLD'
    assert out['academic_admission']=='HOLD'
    assert out['independent_qrt_status']=='NOT_RUN'
    assert out['module_count']==2
    assert out['exact_aggregate_count']==2
    assert out['reader_checks']['preview/question-status.html']['bare_id_count']==1
    assert out['reader_checks']['preview/question-status.html']['full_identity_count']==2
    assert out['reader_checks']['preview/question-status.html']['repeated_bare_ids']=={'SHARED-Q':2}
    assert out['reader_checks']['preview/question-status.html']['missing_required_figure_count']==2
    assert out['source_custody_packet_count']==1
    assert 'Synthetic object' not in json.dumps(out)
    assert not out['source_material_published']

def test_reject_changed_archive_bytes_and_changed_included_member(tmp_path):
    path=fixture(tmp_path)
    expected=sha(path.read_bytes())
    assert read_handoff(path,expected)
    with zipfile.ZipFile(path,'a') as zipf:zipf.writestr('unexpected.txt','tamper')
    with pytest.raises(ValueError,match='PINNED_SOURCE_ZIP_MISMATCH'):
        read_handoff(path,expected)
    with pytest.raises(ValueError,match='UNLISTED_OR_MISSING_HANDOFF_MEMBER'):
        read_handoff(path,sha(path.read_bytes()))

def test_reject_unsafe_names_symlinks_and_duplicate_scoped_source(tmp_path):
    path=fixture(tmp_path)
    with zipfile.ZipFile(path,'a') as zipf:zipf.writestr('../wrong','x')
    with pytest.raises(ValueError,match='UNSAFE_OR_DUPLICATE_ARCHIVE_MEMBER'):
        read_handoff(path,sha(path.read_bytes()))
    bad=html({'questions':[sample(),sample()]})
    with pytest.raises(ValueError,match='REPEATED_FULL_QUESTION_IDENTITY'):
        audit({'preview/question-status.html':bad})

def test_canonical_qrt_contract_is_checked_but_not_approved(tmp_path):
    path=fixture(tmp_path,invalid=True)
    report=audit(read_handoff(path,sha(path.read_bytes())))
    assert any(x['reason']=='FIVE_CANONICAL_FACTOR_KEYS_MISMATCH'
               for x in report['source_contract_issues'])
    assert report['gate']=='HOLD'
    assert report['core1a_core1b_B1_B7']=='UNQUALIFIED'

def test_reject_incomplete_id_and_not_a_real_qrt_review():
    with pytest.raises(ValueError,match='QUESTION_SCOPED_ID_INCOMPLETE'):
        scoped_id({'id':'SYN','topic':'ALPHA'})
    assert not hasattr(sys.modules['nsejs_core2_private_audit'],'approve_qrts')

def test_synthetic_source_embedded_bank_can_be_retrieved_without_evaluating_js():
    data={'questions':[sample()]}
    assert embedded_bank(html(data))==data
    with pytest.raises(ValueError,match='EMBEDDED_SOURCE_MARKER_MISSING'):
        embedded_bank(b'<html><body>Unknown</body></html>')
