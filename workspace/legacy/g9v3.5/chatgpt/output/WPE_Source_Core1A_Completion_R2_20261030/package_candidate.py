from pathlib import Path,PurePosixPath
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
archive=R.parent/'WPE_SOURCE_CORE1A_COMPLETION_R2_CANDIDATE.zip'
payload={}
for p in R.rglob('*'):
 if p.is_file() and not any(x in ['_checks','__pycache__'] for x in p.relative_to(R).parts) and p.name!='DELIVERY_MANIFEST.json':
  payload[p.relative_to(R).as_posix()]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
manifest={'schema':'wpe-local-candidate-manifest/v1','files':payload,'privacy':'LOCAL_PRIVATE_SOURCE_BYTES; not authorized for public publication','status':'PREPARATION_CANDIDATE_NOT_QUALIFIED_LESSON'}
(R/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8',newline='\n')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(payload):z.write(R/rel,rel)
 z.write(R/'DELIVERY_MANIFEST.json','DELIVERY_MANIFEST.json')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(payload)|{'DELIVERY_MANIFEST.json'}
 for rel,entry in payload.items():
  assert not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts
  b=z.read(rel);assert len(b)==entry['bytes'] and sha(b)==entry['sha256'] and b==(R/rel).read_bytes(),rel
result={'archive':str(archive.resolve()),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'payloads':len(payload),'members':len(payload)+1,'CRC':'PASS','membership':'PASS','every_payload_hash_size_and_root_correspondence':'PASS'}
(R.parent/'WPE_SOURCE_CORE1A_R2_ARCHIVE_READBACK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(R.parent/'WPE_SOURCE_CORE1A_COMPLETION_R2_CANDIDATE.zip.sha256').write_text(result['sha256']+'  '+archive.name+'\n',encoding='ascii')
print(json.dumps(result,indent=2))
