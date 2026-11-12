"""R2 exact-source preparation checks. No scientific or authoring promotion."""
from pathlib import Path
import argparse, json, re
from check_handoff import (Invalid, require, load, digest, file_sha, inside, pointer,
                           exact, text, texts, index, refs, ROLES, AUTHORITIES)

REVIEW = {'semantic':'NOT_RUN','core2_owner_approval':'PENDING',
          'core1a_authoring':'NOT_STARTED','core1b_correspondence':'NOT_RUN'}

def fingerprint(data):
    return digest({k:v for k,v in data.items() if k != 'dependency_digest'})

def evidence(data, root, pins=None, expected=None):
    sources=index(data['sources'],'sources')
    trust='SELF_DECLARED_ONLY'
    if pins is not None or expected is not None:
        require(pins is not None and isinstance(expected,str) and re.fullmatch('[0-9a-f]{64}',expected),
                'TRUST_ANCHOR_REQUIRED','pin file and separate expected SHA required')
        require(file_sha(pins)==expected,'TRUST_ANCHOR_MISMATCH','pin file changed')
        p=load(pins);exact(p,'schema sources','pins')
        require(p['schema']=='source-pin-set/v1','SCHEMA','pins')
        require(digest(index(p['sources'],'pins'))==digest(sources),'SOURCE_PIN_MISMATCH','source set differs')
        trust='EXTERNAL_PIN_BYTES_MATCH'
    paths={}
    for sid,s in sources.items():
        exact(s,'id path sha256 role authority',sid)
        require(s['role'] in (ROLES | {'REFERENCE_SOURCE'}) and s['authority'] in AUTHORITIES,'SOURCE_ROLE',sid)
        required={'CANONICAL_CANDIDATE':'CANDIDATE_REFERENCE','NATIVE_CONTRACT':'LOCAL_CONTRACT','REFERENCE_SOURCE':'CANDIDATE_REFERENCE'}
        require(s['role'] not in required or s['authority']==required[s['role']],'SOURCE_AUTHORITY',sid)
        require(isinstance(s['sha256'],str) and re.fullmatch('[0-9a-f]{64}',s['sha256']),'HASH_FORMAT',sid)
        path=inside(root,s['path']);require(path.is_file(),'MISSING_ASSET',sid)
        require(file_sha(path)==s['sha256'],'SOURCE_HASH_MISMATCH',sid);paths[sid]=path
    units=index(data['units'],'units')
    for uid,u in units.items():
        exact(u,'id source_ref kind locator content digest',uid)
        require(u['source_ref'] in sources,'UNRESOLVED_REF',uid)
        if u['kind']=='LINES':
            exact(u['locator'],'start end',uid)
            a,b=u['locator']['start'],u['locator']['end']; lines=paths[u['source_ref']].read_text(encoding='utf-8-sig').splitlines()
            require(type(a) is int and type(b) is int and 1<=a<=b<=len(lines),'BAD_LOCATOR',uid)
            value='\n'.join(lines[a-1:b])
        elif u['kind']=='JSON_POINTER':
            exact(u['locator'],'pointer',uid);value=pointer(load(paths[u['source_ref']]),u['locator']['pointer'])
        else:raise Invalid('UNSUPPORTED_EXTRACTION',uid)
        require(digest(value)==digest(u['content']),'SOURCE_CORRESPONDENCE',uid)
        require(u['digest']==digest(u['content']),'UNIT_DIGEST',uid)
    return sources,units,trust

def check_record(data,root,pins=None,expected=None):
    try:return _record(data,Path(root).resolve(),pins,expected)
    except Invalid as e:return {'integrity':'INVALID','findings':[{'code':e.code,'detail':e.detail}],'core1a_authoring':'HOLD'}
    except (OSError,ValueError,TypeError,KeyError,IndexError,AttributeError,RecursionError) as e:
        return {'integrity':'INVALID','findings':[{'code':'MALFORMED_OR_UNREADABLE','detail':str(e)}],'core1a_authoring':'HOLD'}

def _record(d,root,pins,expected):
    exact(d,'schema id title status purpose sources units claims binding warrants construction sl2_requirement_mapping native_mapping review_requests holds review notes dependency_digest','record')
    require(d['schema']=='core1a-source-handoff/v2','SCHEMA','record')
    require(d['status']=='CANDIDATE' and d['purpose']=='CORE1A_PREPARATION','PROMOTION_FORBIDDEN','preparation only')
    text(d['id'],'id');text(d['title'],'title')
    ss,uu,trust=evidence(d,root,pins,expected)
    claims=index(d['claims'],'claims')
    for cid,c in claims.items():
        exact(c,'id statement unit_refs source_scan_refs conditions disputes qualification',cid)
        refs(c['source_scan_refs'],ss,cid,False)
        require(all(ss[x]['role']=='SOURCE_SCAN' for x in c['source_scan_refs']),'FIGURE_ROLE',cid)
        text(c['statement'],cid);refs(c['unit_refs'],uu,cid)
        texts(c['conditions'],cid,True);texts(c['disputes'],cid)
        require(c['qualification']=='UNREVIEWED','PROMOTION_FORBIDDEN',cid)
    b=d['binding'];exact(b,'spine_node spine_unit_ref canonical_matches canonical_gaps','binding')
    require(b['spine_node']==d['id'] and b['spine_unit_ref'] in uu,'SYLLABUS_BINDING','node identity')
    su=uu[b['spine_unit_ref']]
    require(ss[su['source_ref']]['role']=='SYLLABUS' and isinstance(su['content'],str) and
            b['spine_node'] in [x.strip() for x in su['content'].split('|')],'SYLLABUS_BINDING','exact table row required')
    texts(b['canonical_gaps'],'canonical gaps')
    require(isinstance(b['canonical_matches'],list),'SHAPE','canonical matches')
    for m in b['canonical_matches']:
        exact(m,'unit_ref microtopic_id capability_id relationship semantic_status','canonical match')
        require(m['unit_ref'] in uu,'UNRESOLVED_REF','canonical match')
        u=uu[m['unit_ref']];v=u['content']
        require(ss[u['source_ref']]['role']=='CANONICAL_CANDIDATE' and isinstance(v,dict) and
                v.get('id')==m['microtopic_id'] and v.get('primary_capability_ref')==m['capability_id'],
                'LIBRARY_BINDING','exact candidate capability identity')
        require(m['relationship'] in ['DIRECT_CANDIDATE','PREREQUISITE_BRIDGE','SCOPE_NEARBY'] and
                m['semantic_status']=='UNREVIEWED','PROMOTION_FORBIDDEN','canonical semantic match')
    require(b['canonical_matches'] or b['canonical_gaps'],'UNACCOUNTED_GAP','canonical coverage')
    warrants=index(d['warrants'],'warrants')
    for wid,w in warrants.items():
        exact(w,'id claim_refs unit_refs reference_unit_refs needed_reason conditions qualification gap',wid)
        refs(w['claim_refs'],claims,wid);text(w['needed_reason'],wid);texts(w['conditions'],wid,True)
        refs(w['unit_refs'],uu,wid,False)
        refs(w['reference_unit_refs'],uu,wid,False)
        require(all(ss[uu[x]['source_ref']]['role']=='REFERENCE_SOURCE' for x in w['reference_unit_refs']),'REFERENCE_ROLE',wid)
        require(w['qualification'] in ['CANDIDATE','MISSING'],'PROMOTION_FORBIDDEN',wid)
        if w['qualification']=='MISSING':
            require(not w['unit_refs'],'WARRANT_BINDING','missing warrant must not fake a bound unit');text(w['gap'],wid)
        else:
            require(bool(w['unit_refs']),'WARRANT_BINDING',wid)
            for ref in w['unit_refs']:
                require(ss[uu[ref]['source_ref']]['role']=='CANONICAL_CANDIDATE','WARRANT_BINDING',wid)
    c=d['construction']
    exact(c,'inputs output obstacle decisive_move entry_assumptions conventions steps representation_needs worked_example_requirement boundary_requirements wrong_path_candidates check_requirements','construction')
    for f in ['inputs','entry_assumptions','conventions','boundary_requirements']:texts(c[f],f,True)
    for f in ['output','obstacle','decisive_move','worked_example_requirement']:text(c[f],f)
    steps=index(c['steps'],'steps')
    for sid,s in steps.items():
        exact(s,'id role requirement why_needed unit_refs claim_refs warrant_refs depends_on',sid)
        require(s['role'] in ['INPUT','REPRESENT','CONNECT','TRANSFORM','VERIFY','BOUNDARY'],'STEP_ROLE',sid)
        text(s['requirement'],sid);text(s['why_needed'],sid)
        refs(s['unit_refs'],uu,sid);refs(s['claim_refs'],claims,sid);refs(s['warrant_refs'],warrants,sid)
        refs(s['depends_on'],steps,sid,False)
    anchor_ids=[*uu,*claims,*warrants,*steps]
    require(len(anchor_ids)==len(set(anchor_ids)),'AMBIGUOUS_ANCHOR','rendered evidence IDs must not collide')
    active,done=set(),set()
    def visit(s):
        require(s not in active,'DEPENDENCY_CYCLE',s)
        if s in done:return
        active.add(s)
        for dep in steps[s]['depends_on']:visit(dep)
        active.remove(s);done.add(s)
    for sid in steps:visit(sid)
    used_claims={x for s in steps.values() for x in s['claim_refs']}
    require(set(claims)<=used_claims,'ORPHAN_CLAIM','claims absent from construction')
    for rid,r in index(c['representation_needs'],'representations').items():
        exact(r,'id asset_ref status source_scan_refs correspondence requirement',rid)
        text(r['requirement'],rid);refs(r['source_scan_refs'],ss,rid,False)
        require(all(ss[x]['role']=='SOURCE_SCAN' for x in r['source_scan_refs']),'FIGURE_ROLE',rid)
        if r['asset_ref'] is None:require(r['status']=='MISSING','REPRESENTATION_STATUS',rid)
        else:
            require(r['asset_ref'] in ss,'UNRESOLVED_REF',rid)
            role=ss[r['asset_ref']]['role']
            require((role=='DERIVED_FIGURE' and r['status']=='DERIVED_UNREVIEWED') or
                    (role=='SOURCE_SCAN' and r['status']=='SOURCE_UNREVIEWED'),'FIGURE_ROLE',rid)
        require(isinstance(r['correspondence'],list),'SHAPE',rid)
        if r['asset_ref']:require(bool(r['correspondence']),'REPRESENTATION_CORRESPONDENCE',rid)
        for row in r['correspondence']:
            exact(row,'symbol element in_words',rid)
            for v in row.values():text(v,rid)
    for rid,r in index(c['wrong_path_candidates'],'repair designs').items():
        exact(r,'id hypothesis claim_refs diagnostic_contrast repair_requirement observation',rid)
        refs(r['claim_refs'],claims,rid)
        for f in ['hypothesis','diagnostic_contrast','repair_requirement']:text(r[f],rid)
        require(r['observation']=='NONE','FABRICATED_OBSERVATION',rid)
    for cid,x in index(c['check_requirements'],'check designs').items():
        exact(x,'id claim_refs method expected_invariant independence_basis status',cid)
        refs(x['claim_refs'],claims,cid)
        for f in ['method','expected_invariant','independence_basis']:text(x[f],cid)
        require(x['status']=='DESIGN_ONLY','PROMOTION_FORBIDDEN',cid)
    q=d['sl2_requirement_mapping'];exact(q,'status task_identity requirement_bindings missing_input','SL2 join')
    require(q['status']=='PENDING_REVIEWED_REQUIREMENT' and q['task_identity'] is None and
            q['requirement_bindings']==[],'UNSUPPORTED_REVIEW_JOIN','R2 does not consume trusted adjudication')
    text(q['missing_input'],'missing SL2 input')
    require(isinstance(d['native_mapping'],list) and bool(d['native_mapping']),'NATIVE_MAPPING','empty mapping')
    for m in d['native_mapping']:
        exact(m,'schema_unit_ref native_property handoff_pointer action','native mapping')
        require(m['schema_unit_ref'] in uu,'NATIVE_MAPPING','schema unit')
        u=uu[m['schema_unit_ref']]
        require(ss[u['source_ref']]['role']=='NATIVE_CONTRACT' and
                m['native_property'] in u['content'].get('properties',{}),'NATIVE_MAPPING','native property')
        pointer(d,m['handoff_pointer'])
        require(m['action'] in ['AUTHOR_FROM_EVIDENCE','RESOLVE_EXISTING_REFS','AUTHOR_DISTINCT_EXAMPLE'],
                'NATIVE_MAPPING','action')
    requests=index(d['review_requests'],'review requests')
    targets=[r.get('target_pointer') for r in requests.values()]
    required_targets={'/claims/'+str(i) for i in range(len(d['claims']))}|{'/warrants','/construction','/sl2_requirement_mapping'}
    require(len(targets)==len(set(targets)) and set(targets)==required_targets,'REVIEW_COVERAGE','every consequential target needs one version-bound request')
    for rid,r in requests.items():
        exact(r,'id target_pointer target_digest question required_evidence status',rid)
        target=pointer(d,r['target_pointer'])
        require(r['target_digest']==digest(target),'STALE_REVIEW_REQUEST',rid)
        text(r['question'],rid);texts(r['required_evidence'],rid,True)
        require(r['status']=='OPEN','PROMOTION_FORBIDDEN',rid)
    for hid,h in index(d['holds'],'holds').items():
        exact(h,'id detail affects',hid);text(h['detail'],hid);texts(h['affects'],hid,True)
    require(d['review']==REVIEW,'PROMOTION_FORBIDDEN','review/Owner flags cannot unlock construction')
    texts(d['notes'],'notes',True)
    require(d['dependency_digest']==fingerprint(d),'STALE_DEPENDENCY','record changed')
    return {'integrity':'PASS','trust_binding':trust,'preparation':'CANDIDATE','core1a_authoring':'HOLD',
            'semantic_review':'NOT_RUN','native_package':'NOT_EMITTED','claims':len(claims),'units':len(uu),
            'construction_roles':len(steps),'candidate_warrants':sum(w['qualification']=='CANDIDATE' for w in warrants.values()),
            'missing_warrants':sum(w['qualification']=='MISSING' for w in warrants.values()),'reviewed_SL2_joins':0}

def check_program(path,expected=None):
    try:return _program(Path(path).resolve(),expected)
    except Invalid as e:return {'integrity':'INVALID','findings':[{'code':e.code,'detail':e.detail}]}
    except (OSError,ValueError,TypeError,KeyError,IndexError,AttributeError) as e:
        return {'integrity':'INVALID','findings':[{'code':'MALFORMED_OR_UNREADABLE','detail':str(e)}]}

def _program(path,expected):
    p=load(path);root=path.parent
    exact(p,'schema id status scope records line_dispositions scan_observations exclusions gates','program')
    require(p['schema']=='core1a-source-program/v1' and p['status']=='CANDIDATE','SCHEMA','program')
    if expected:require(file_sha(path)==expected,'PROGRAM_PIN_MISMATCH','program differs from external expected digest')
    s=p['scope'];exact(s,'spine_path spine_sha256 book_path book_sha256','scope')
    spine=inside(root,s['spine_path']);book=inside(root,s['book_path'])
    require(file_sha(spine)==s['spine_sha256'] and file_sha(book)==s['book_sha256'],'SCOPE_SOURCE_MISMATCH','scope bytes changed')
    nodes=re.findall(r'^\|\s*(WPE-N\d+)\s*\|',spine.read_text(encoding='utf-8-sig'),re.M)
    require(nodes and len(set(nodes))==len(nodes),'SYLLABUS_BINDING','duplicate or absent source nodes')
    records=index(p['records'],'records');require(set(records)==set(nodes),'COVERAGE_MISMATCH','record set must equal exact spine nodes')
    results={};scan_paths=set()
    for nid,r in records.items():
        exact(r,'id path sha256 pins_path pins_sha256 prerequisites','record reference')
        fp=inside(root,r['path']);pp=inside(root,r['pins_path'])
        require(file_sha(fp)==r['sha256'],'RECORD_HASH_MISMATCH',nid)
        d=load(fp);require(d['id']==nid,'RECORD_ID_MISMATCH',nid)
        result=check_record(d,fp.parent,pp,r['pins_sha256'])
        require(result['integrity']=='PASS','RECORD_INVALID',nid+': '+json.dumps(result))
        by_role={role:[x for x in d['sources'] if x['role']==role] for role in ['BOOK_TEXT','SYLLABUS']}
        for role,scope_file in [('BOOK_TEXT',book),('SYLLABUS',spine)]:
            require(len(by_role[role])==1 and inside(fp.parent,by_role[role][0]['path'])==scope_file,'RECORD_SCOPE_MISMATCH',nid)
        scan_paths.update(str(inside(fp.parent,x['path'])) for x in d['sources'] if x['role']=='SOURCE_SCAN')
        refs(r['prerequisites'],records,nid,False);results[nid]=result
    visiting,done=set(),set()
    def visit(n):
        require(n not in visiting,'PROGRAM_DEPENDENCY_CYCLE',n)
        if n in done:return
        visiting.add(n)
        for dep in records[n]['prerequisites']:visit(dep)
        visiting.remove(n);done.add(n)
    for n in nodes:visit(n)
    lines=book.read_text(encoding='utf-8-sig').splitlines(); seen=set()
    for seg in p['line_dispositions']:
        exact(seg,'start end disposition node_refs reason','line disposition')
        a,b=seg['start'],seg['end']
        require(type(a) is int and type(b) is int and 1<=a<=b<=len(lines),'BAD_LOCATOR','line coverage')
        require(not seen.intersection(range(a,b+1)),'DUPLICATE_LINE_DISPOSITION','overlapping source accounting')
        seen.update(range(a,b+1));refs(seg['node_refs'],records,'line nodes',False);text(seg['reason'],'line reason')
        require(seg['disposition'] in ['SOURCE_SECTION','SHARED_CONTEXT','EXTRACTION_METADATA','DERIVED_SUMMARY'],'SOURCE_ROLE','line disposition')
    require(seen==set(range(1,len(lines)+1)),'UNACCOUNTED_SOURCE_LINES','every line needs a disposition, not necessarily a teaching claim')
    observed_paths=[]
    for o in p['scan_observations']:
        exact(o,'source_path sha256 region observation limits status','scan observation')
        require(file_sha(inside(root,o['source_path']))==o['sha256'],'SOURCE_HASH_MISMATCH','scan')
        for f in ['region','observation','limits']:text(o[f],'scan '+f)
        require(o['status']=='AUTHOR_VIEWED_NOT_INDEPENDENT','PROMOTION_FORBIDDEN','scan')
        observed_paths.append(str(inside(root,o['source_path'])))
    require(len(observed_paths)==len(set(observed_paths)) and set(observed_paths)==scan_paths,'SCAN_COVERAGE','all and only retained record scans need observations')
    texts(p['exclusions'],'exclusions',True)
    require(p['gates']==REVIEW,'PROMOTION_FORBIDDEN','program gates')
    return {'integrity':'PASS','scope_binding':'EXTERNAL_PROGRAM_BYTES_MATCH' if expected else 'SELF_DECLARED_PROGRAM_ONLY',
            'nodes_accounted':len(nodes),'source_lines_accounted':len(seen),'records':results,'science':'NOT_QUALIFIED',
            'reviewed_SL2_joins':0,'native_lessons':0,'authoring':'HOLD'}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('program',type=Path);ap.add_argument('--expected-sha256')
    a=ap.parse_args();r=check_program(a.program,a.expected_sha256);print(json.dumps(r,indent=2))
    return 0 if r['integrity']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
