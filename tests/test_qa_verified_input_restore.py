"""Private QA evidence restore controls — synthetic test bytes only.

No original examination content is bundled or committed by these tests.
"""
from __future__ import annotations

from copy import deepcopy
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
from qa_verified_input_restore import (
    PrivateInputError, safe_path, validate_bundle, restore, file_sha
)

SOURCE = "workspace/sources/chem/SYNTHETIC-Q-01/source-custody.json"
OUTPUT = "workspace/output/synthetic-chem-r1/bank.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package(tmp_path: Path, *, payloads: dict[str, bytes] | None = None,
            manifest_changes: dict | None = None) -> tuple[Path, Path, Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    payloads = payloads or {SOURCE:b'{"synthetic":true}', OUTPUT:b'{"synthetic_bank":true}'}
    manifest = {"schema":"grade9-private-qa-input-bundle/v1",
                "academic_approval":"HOLD",
                "files":{p:sha(data) for p,data in payloads.items()}}
    if manifest_changes:
        manifest.update(manifest_changes)
    m = tmp_path / "private-manifest.json"
    m.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    archive = tmp_path / "private-inputs.zip"
    with ZipFile(archive, "w") as z:
        for name, data in payloads.items():
            z.writestr(name,data)
    return repo, archive, m, file_sha(archive), file_sha(m)


def validate(args):
    root,bundle,manifest,bundle_sha,manifest_sha=args
    return validate_bundle(bundle,manifest,bundle_sha,manifest_sha,root)


def test_checksum_pinned_restore_is_opt_in_and_does_not_approve_science(tmp_path):
    args=package(tmp_path)
    result=validate(args)
    assert result["count"]==2
    assert result["academic_approval"]=="HOLD"
    assert not (args[0]/SOURCE).exists()
    assert not (args[0]/OUTPUT).exists()
    outcome=restore(result)
    assert outcome["academic_approval"]=="HOLD"
    assert outcome["full_python_qa"]=="NOT_YET_RUN"
    assert (args[0]/SOURCE).read_bytes()==b'{"synthetic":true}'
    assert (args[0]/OUTPUT).read_bytes()==b'{"synthetic_bank":true}'
    assert restore(validate(args))["files"]==2


@pytest.mark.parametrize("which",["bundle","manifest"])
def test_altered_bundle_or_manifest_pin_blocks_before_writing(tmp_path,which):
    args=list(package(tmp_path))
    args[3 if which=="bundle" else 4]="0"*64
    with pytest.raises(PrivateInputError,match="SHA256_MISMATCH"):
        validate(args)
    assert not (args[0]/SOURCE).exists()


@pytest.mark.parametrize("invalid", [
    "workspace/sources/../admin/secrets.json",
    "workspace/output/../../outside.json",
    "workspace/sources/bad\\path/file.json",
    "workspace/sources/a/unsafe.py",
    "/absolute/workspace/sources/a.json",
    "workspace/sources/x//source-custody.json",
    "workspace/sources/x/file.json/../../a.json",
])
def test_archive_never_writes_executable_traversal_or_absolute_paths(invalid):
    with pytest.raises(PrivateInputError,match="UNSAFE_PRIVATE_BUNDLE_PATH"):
        safe_path(invalid)


def test_archive_path_traversal_fails_even_when_manifest_pinned(tmp_path):
    args=package(tmp_path,payloads={
        SOURCE:b'{"synthetic":true}',"workspace/output/../../escape.json":b"bad"
    })
    with pytest.raises(PrivateInputError,match="UNSAFE_PRIVATE_BUNDLE_PATH"):
        validate(args)
    assert not (tmp_path/"escape.json").exists()


def test_archive_extra_file_rejected_before_any_write(tmp_path):
    args=package(tmp_path)
    archive=args[1]
    with ZipFile(archive,"a") as z:
        z.writestr("workspace/output/unpinned/bank.json",b"bad")
    updated=(args[0],archive,args[2],file_sha(archive),args[4])
    with pytest.raises(PrivateInputError,match="PRIVATE_ARCHIVE_CONTENTS_NOT_MANIFEST_PINNED"):
        validate(updated)
    assert not (args[0]/SOURCE).exists()


def test_owner_manifest_cannot_claim_academic_pass(tmp_path):
    args=package(tmp_path,manifest_changes={"academic_approval":"PASS"})
    with pytest.raises(PrivateInputError,match="PRIVATE_MANIFEST_ADMISSION_OR_SCHEMA_INVALID"):
        validate(args)


def test_bundle_requires_actual_source_records_not_output_only(tmp_path):
    args=package(tmp_path,payloads={OUTPUT:b'{"synthetic":true}'})
    with pytest.raises(PrivateInputError,match="NO_PRIVATE_SOURCE_CUSTODY_IN_BUNDLE"):
        validate(args)


def test_file_content_must_match_manifest_not_merely_archive_hash(tmp_path):
    args=package(tmp_path)
    record=json.loads(args[2].read_text())
    record["files"][SOURCE]="a"*64
    args[2].write_text(json.dumps(record,sort_keys=True))
    updated=(args[0],args[1],args[2],args[3],file_sha(args[2]))
    with pytest.raises(PrivateInputError,match="PRIVATE_FILE_SHA256_MISMATCH"):
        validate(updated)


def test_existing_private_source_is_never_overwritten_with_different_bytes(tmp_path):
    args=package(tmp_path)
    target=args[0]/SOURCE
    target.parent.mkdir(parents=True)
    target.write_bytes(b"unrelated evidence")
    with pytest.raises(PrivateInputError,match="EXISTING_WORKSPACE_BYTES_CONFLICT"):
        validate(args)
    assert target.read_bytes()==b"unrelated evidence"


def test_existing_workspace_symlink_escape_is_forbidden(tmp_path):
    args=package(tmp_path)
    outer=tmp_path/"elsewhere"
    outer.mkdir()
    ws=args[0]/"workspace"
    ws.symlink_to(outer,target_is_directory=True)
    with pytest.raises(PrivateInputError,match="WORKSPACE_SYMLINK_FORBIDDEN"):
        validate(args)
    assert not list(outer.iterdir())


def test_zip_member_symlinks_are_forbidden(tmp_path):
    args=package(tmp_path)
    archive=args[1]
    archive.unlink()
    with ZipFile(archive,"w") as z:
        link=ZipInfo(SOURCE)
        link.create_system=3
        link.external_attr=(stat.S_IFLNK | 0o777) << 16
        z.writestr(link,b"../../escape")
        z.writestr(OUTPUT,b'{"synthetic_bank":true}')
    record={"schema":"grade9-private-qa-input-bundle/v1","academic_approval":"HOLD",
            "files":{SOURCE:sha(b"../../escape"),OUTPUT:sha(b'{"synthetic_bank":true}')}}
    args[2].write_text(json.dumps(record))
    updated=(args[0],archive,args[2],file_sha(archive),file_sha(args[2]))
    with pytest.raises(PrivateInputError,match="PRIVATE_ARCHIVE_SYMLINK_FORBIDDEN"):
        validate(updated)


def test_unpinned_cli_is_strict_nonzero(tmp_path):
    args=package(tmp_path)
    cmd=[sys.executable,str(ROOT/"tools/qa_verified_input_restore.py"),
         "--bundle",str(args[1]),"--manifest",str(args[2]),
         "--expected-bundle-sha256","0"*64,
         "--expected-manifest-sha256",args[4],
         "--root",str(args[0]),"--restore"]
    result=subprocess.run(cmd,capture_output=True,text=True,check=False)
    assert result.returncode==2
    assert not (args[0]/SOURCE).exists()


def test_verified_cli_dry_run_does_not_write(tmp_path):
    args=package(tmp_path)
    cmd=[sys.executable,str(ROOT/"tools/qa_verified_input_restore.py"),
         "--bundle",str(args[1]),"--manifest",str(args[2]),
         "--expected-bundle-sha256",args[3],
         "--expected-manifest-sha256",args[4],
         "--root",str(args[0])]
    result=subprocess.run(cmd,capture_output=True,text=True,check=False)
    assert result.returncode==0
    receipt=json.loads(result.stdout)
    assert receipt["status"]=="PINNED_PRIVATE_BUNDLE_VERIFIED_NO_WRITE"
    assert receipt["academic_approval"]=="HOLD"
    assert not (args[0]/SOURCE).exists()
