"""Owner-private Core2 archive restore tests using SYNTHETIC content only."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
from zipfile import ZipFile, ZipInfo

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_core2_bank_archive import (
    OutputRecoveryHold, sha_file, preflight_destinations, restore,
    verify_bank_archive,
)

BANK = "individual_banks/synthetic-physics-r1/bank.json"
QUESTIONS = "individual_banks/synthetic-physics-r1/questions.json"


def archive_at(tmp_path, payloads=None, included_extra=None):
    payloads = payloads or {BANK: b'{"questions":[]}', QUESTIONS:b"[]"}
    archive = tmp_path / "owner-output.zip"
    manifest = [{"archive_path":name, "bytes":len(value),
                 "sha256":hashlib.sha256(value).hexdigest()}
                for name,value in payloads.items()]
    with ZipFile(archive,"w") as z:
        for name,value in payloads.items():
            z.writestr(name,value)
        z.writestr("MANIFEST.json",json.dumps(manifest))
        z.writestr("README.md","Unvalidated synthetic preview")
        if included_extra:
            z.writestr("unlisted-unknown.txt",b"unlisted")
    return archive, sha_file(archive)


def test_byte_exact_verified_no_write_default(tmp_path):
    archive,pin=archive_at(tmp_path)
    out=verify_bank_archive(archive,pin)
    assert len(out)==2
    assert all(k.startswith("workspace/output/") for k in out)
    root=tmp_path/"checkout"
    root.mkdir()
    assert preflight_destinations(root,out)==(2,0)
    assert not (root/"workspace").exists()
    result=restore(root,out)
    assert result=={"written":2,"already_matching":0}
    assert preflight_destinations(root,out)==(0,2)
    assert restore(root,out)=={"written":0,"already_matching":2}


def test_bad_pin_and_tampered_bytes_fail_closed(tmp_path):
    archive,pin=archive_at(tmp_path)
    with pytest.raises(OutputRecoveryHold,match="ARCHIVE_SHA256_MISMATCH"):
        verify_bank_archive(archive,"0"*64)
    with pytest.raises(OutputRecoveryHold,match="OWNER_ARCHIVE_SHA256_PIN_REQUIRED"):
        verify_bank_archive(archive,"unpinned")
    with ZipFile(archive,"a") as z:
        z.writestr("surprise.txt","extra")
    with pytest.raises(OutputRecoveryHold,match="BUNDLE_UNLISTED_FILES"):
        verify_bank_archive(archive,sha_file(archive))


@pytest.mark.parametrize("bad",[
    "individual_banks/../synthetic-physics-r1/bank.json",
    "individual_banks/synthetic-physics-r1/../../other.json",
    "individual_banks/synthetic-physics-r1/payload.py",
    "individual_banks/synthetic-physics-r1/deep/fake.json",
    "individual_banks//bank.json",
    "workspace/sources/biology/forged.json",
])
def test_non_allowlisted_source_or_path_rejected(tmp_path,bad):
    archive,pin=archive_at(tmp_path,payloads={BANK:b"ok",bad:b"unsafe"})
    with pytest.raises(OutputRecoveryHold):
        verify_bank_archive(archive,pin)


def test_changed_manifests_not_trusted_even_if_archive_sha_is_pinned(tmp_path):
    archive,pin=archive_at(tmp_path)
    with ZipFile(archive,"a") as z:
        z.writestr("unexpected-extra.txt","unknown")
    with pytest.raises(OutputRecoveryHold,match="BUNDLE_UNLISTED_FILES"):
        verify_bank_archive(archive,sha_file(archive))


def test_unlisted_extra_file_fails_before_restore(tmp_path):
    archive,pin=archive_at(tmp_path,included_extra=True)
    with pytest.raises(OutputRecoveryHold,match="BUNDLE_UNLISTED_FILES"):
        verify_bank_archive(archive,pin)


def test_restoration_never_overwrites_existing_custody_or_bank(tmp_path):
    archive,pin=archive_at(tmp_path)
    data=verify_bank_archive(archive,pin)
    root=tmp_path/"checkout"
    target=root/"workspace/output/synthetic-physics-r1/bank.json"
    target.parent.mkdir(parents=True)
    target.write_text("existing scientific work",encoding="utf-8")
    with pytest.raises(OutputRecoveryHold,match="TARGET_BYTE_CONFLICT"):
        restore(root,data)
    assert target.read_text()=="existing scientific work"
    assert not (root/"workspace/output/synthetic-physics-r1/questions.json").exists()


def test_restoration_refuses_symlink_to_outside_checkout(tmp_path):
    archive,pin=archive_at(tmp_path)
    data=verify_bank_archive(archive,pin)
    root=tmp_path/"checkout"
    root.mkdir()
    external=tmp_path/"external"
    external.mkdir()
    (root/"workspace").symlink_to(external,target_is_directory=True)
    with pytest.raises(OutputRecoveryHold,match="TARGET_SYMLINK_FORBIDDEN"):
        preflight_destinations(root,data)
    assert not list(external.iterdir())


def test_owner_zip_symlink_member_rejected(tmp_path):
    archive,pin=archive_at(tmp_path)
    archive.unlink()
    with ZipFile(archive,"w") as z:
        zi=ZipInfo(BANK)
        zi.create_system=3
        zi.external_attr=(stat.S_IFLNK | 0o777) << 16
        z.writestr(zi,"/tmp/outside")
        z.writestr("MANIFEST.json",json.dumps([
            {"archive_path":BANK,"bytes":len("/tmp/outside"),
             "sha256":hashlib.sha256(b"/tmp/outside").hexdigest()}]))
    with pytest.raises(OutputRecoveryHold,match="BUNDLE_SYMLINK_FORBIDDEN"):
        verify_bank_archive(archive,sha_file(archive))


def test_cli_default_is_dry_run_and_science_hold(tmp_path):
    archive,pin=archive_at(tmp_path)
    root=tmp_path/"checkout";root.mkdir()
    cmd=[sys.executable,str(ROOT/"tools/qa_core2_bank_archive.py"),
         "--archive",str(archive),"--expected-sha256",pin,
         "--root",str(root)]
    result=subprocess.run(cmd,capture_output=True,text=True,check=False)
    assert result.returncode==0,result.stderr
    report=json.loads(result.stdout)
    assert report["status"]=="DRY_RUN_NO_FILES_WRITTEN"
    assert report["candidate_output_files"]==2
    assert report["academic_approval"]=="HOLD"
    assert report["source_custody"]=="NOT_PROVIDED"
    assert report["full_python_qa"]=="NOT_RUN"
    assert not (root/"workspace").exists()


def test_cli_apply_opt_in_still_maintains_qa_hold(tmp_path):
    archive,pin=archive_at(tmp_path)
    root=tmp_path/"checkout";root.mkdir()
    cmd=[sys.executable,str(ROOT/"tools/qa_core2_bank_archive.py"),
         "--archive",str(archive),"--expected-sha256",pin,
         "--root",str(root),"--apply"]
    result=subprocess.run(cmd,capture_output=True,text=True,check=False)
    assert result.returncode==0,result.stderr
    report=json.loads(result.stdout)
    assert report["status"]=="PRIVATE_OUTPUT_ONLY_RESTORE_COMPLETE"
    assert report["source_custody"]=="NOT_PROVIDED"
    assert report["written"]==2
    assert (root/"workspace/output/synthetic-physics-r1/bank.json").exists()
