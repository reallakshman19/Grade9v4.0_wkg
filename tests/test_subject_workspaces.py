"""Shared subject preflight. Fixtures are synthetic contracts, NOT curricula."""
import json
from pathlib import Path

import pytest

from grade9qa.cli import main
from grade9qa.subject_workspaces import inspect_workspaces

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/three-subjects-candidate/manifest.json"
ROLES = ("CORE1", "CORE2", "CORE1A", "CORE1B", "CORE2A", "CORE2B")


@pytest.fixture
def manifest():
    return json.loads(EXAMPLE.read_text())


def contract():
    return {
        "learner_products": {role: {"production": "COMPILED"} for role in ROLES},
        "validator_catalogue": [
            {"id": "SYNTH-VALIDATOR", "status": "CANDIDATE",
             "result": {"comparison": "MATCHES_EXPECTED"},
             "does_not_prove": "Cannot establish scientific or academic validity."}
        ],
        "representation_kinds": [],
    }


def native(state="CONTRACT_ONLY", gates=0, packages=0, findings=None):
    return {
        "passed": True, "subjects_checked": 1,
        "subjects": [{"subject": "Physics", "state": state,
                      "gate_registries": gates, "library_packages": packages,
                      "findings": [] if findings is None else findings}],
    }


def make_root(tmp_path):
    root = tmp_path / "workspace"
    (root / "Shared/tools").mkdir(parents=True)
    (root / "Shared/tools/check_subjects.py").write_text("# synthetic marker, not native tool\n")
    (root / "Physics/adapter").mkdir(parents=True)
    (root / "Physics/adapter/CoreContracts.json").write_text(json.dumps(contract()))
    return root


def codes(report):
    return {item["code"] for item in report["diagnostics"]}


def inspect(manifest, root, report=None, bindings=None):
    return inspect_workspaces(manifest, root, {"PHYSICS":"Physics"} if bindings is None else bindings, report)


def test_real_core_contract_file_is_observed_but_untrusted(tmp_path, manifest):
    root = make_root(tmp_path)
    r = inspect(manifest, root)
    assert r["subjects"]["PHYSICS"]["six_core_contract"] == "SIX_DECLARED_UNTRUSTED"
    assert len(r["subjects"]["PHYSICS"]["contract_sha256"]) == 64
    assert r["academic_status"] == r["release_status"] == "HOLD"
    assert r["canonical_promotion"] == "NOT_PERFORMED"


def test_contract_only_native_discovery_is_hold(tmp_path, manifest):
    root = make_root(tmp_path)
    r = inspect(manifest, root, native())
    assert r["subjects"]["PHYSICS"]["native_discovery_status"] == "CONTRACT_ONLY"
    assert r["mechanical_status"] == "HOLD"
    assert "NATIVE_ACTIVE_SUBJECT_CONTRACT_ONLY" in codes(r)


def test_native_implemented_without_content_is_hollow(tmp_path, manifest):
    root = make_root(tmp_path)
    (root / "Physics/adapter/__init__.py").write_text("def load(): return object()\n")
    r = inspect(manifest, root, native(state="IMPLEMENTED"))
    assert "HOLLOW_IMPLEMENTED_SUBJECT" in codes(r)
    assert r["academic_status"] == "HOLD"


def test_native_implemented_but_missing_adapter_is_fail(tmp_path, manifest):
    root = make_root(tmp_path)
    r=inspect(manifest, root, native(state="IMPLEMENTED"))
    assert "NATIVE_IMPLEMENTED_WITHOUT_ADAPTER_FILE" in codes(r)
    assert r["mechanical_status"] == "FAIL"


def test_populated_synthetic_gates_and_library_still_hold(tmp_path, manifest):
    root = make_root(tmp_path)
    (root/"Physics/adapter/__init__.py").write_text("def load(): return object()\n")
    (root/"Physics/gates").mkdir(parents=True)
    (root/"Physics/gates/work.v1.json").write_text("{}")
    (root/"Physics/library").mkdir()
    (root/"Physics/library/part.json").write_text("{}")
    r=inspect(manifest, root, native(state="IMPLEMENTED",gates=1,packages=1))
    assert "SUBJECT_CONTENT_REQUIRES_NATIVE_REVIEW" in codes(r)
    assert r["mechanical_status"] == "HOLD"
    assert r["subjects"]["PHYSICS"]["library_package_files"] == 1


def test_native_count_contradicts_actual_files(tmp_path, manifest):
    root=make_root(tmp_path)
    (root/"Physics/adapter/__init__.py").write_text("def load(): return object()\n")
    r=inspect(manifest,root,native(state="IMPLEMENTED",gates=2,packages=4))
    assert "NATIVE_LOCAL_ARTIFACT_COUNT_DISAGREEMENT" in codes(r)
    assert r["mechanical_status"] == "FAIL"


def test_missing_native_report_is_explicit(tmp_path, manifest):
    root=make_root(tmp_path)
    assert "NATIVE_SUBJECT_RUN_NOT_SUPPLIED" in codes(inspect(manifest,root))


def test_missing_contract_keeps_hold(tmp_path, manifest):
    root=make_root(tmp_path)
    (root/"Physics/adapter/CoreContracts.json").unlink()
    r=inspect(manifest,root,native())
    assert "CORE_CONTRACT_FILE_MISSING" in codes(r)


def test_native_subject_without_local_contract_is_fail(tmp_path, manifest):
    root=make_root(tmp_path)
    (root/"Physics/adapter/CoreContracts.json").unlink()
    r=inspect(manifest,root,native())
    assert "NATIVE_SUBJECT_WITHOUT_LOCAL_CONTRACT" in codes(r)
    assert r["mechanical_status"] == "FAIL"


def test_six_roles_enforced(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    data=json.loads(p.read_text())
    del data["learner_products"]["CORE2B"]
    p.write_text(json.dumps(data))
    r=inspect(manifest,root)
    assert "SIX_CORE_ROLE_CONTRACT_MISMATCH" in codes(r)
    assert r["mechanical_status"] == "FAIL"


def test_forged_core_compiled_claim_without_code_is_not_approved(tmp_path, manifest):
    root=make_root(tmp_path)
    r=inspect(manifest,root,native())
    assert r["release_status"]=="HOLD"
    assert r["subjects"]["PHYSICS"]["adapter_file_present"] is False


def test_product_without_status_fails(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    obj=json.loads(p.read_text())
    obj["learner_products"]["CORE1"].pop("production")
    p.write_text(json.dumps(obj))
    assert "CORE_PRODUCT_PRODUCTION_UNKNOWN" in codes(inspect(manifest,root))


def test_noncompiled_product_requires_reason(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    obj=json.loads(p.read_text())
    obj["learner_products"]["CORE1"]["production"]="NOT_COMPILED"
    p.write_text(json.dumps(obj))
    assert "CORE_PRODUCT_MISSING_REASON" in codes(inspect(manifest,root))


def test_validator_does_not_prove_must_be_declared(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    obj=json.loads(p.read_text())
    obj["validator_catalogue"][0]["does_not_prove"]=""
    p.write_text(json.dumps(obj))
    assert "NATIVE_VALIDATOR_LIMIT_MISSING" in codes(inspect(manifest,root))


def test_native_contract_rejects_duplicate_json_keys(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    p.write_text('{"learner_products":{}, "learner_products":{}}')
    assert "CORE_CONTRACT_INVALID_JSON" in codes(inspect(manifest,root))


def test_native_contract_rejects_nonfinite_json(tmp_path, manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    p.write_text('{"learner_products":NaN}')
    assert "CORE_CONTRACT_INVALID_JSON" in codes(inspect(manifest,root))


def test_subject_binding_parent_escape_rejected(tmp_path, manifest):
    root=make_root(tmp_path)
    r=inspect(manifest,root,bindings={"PHYSICS":"../Other"})
    assert "UNSAFE_SUBJECT_DIR" in codes(r)


def test_subject_binding_cross_subject_collision(tmp_path, manifest):
    root=make_root(tmp_path)
    r=inspect(manifest,root,bindings={"PHYSICS":"Physics","MATHEMATICS":"physics"})
    assert "COLLIDING_SUBJECT_DIRECTORIES" in codes(r)


def test_unknown_subject_binding_is_not_accepted(tmp_path, manifest):
    root=make_root(tmp_path)
    assert "UNKNOWN_BINDING_SUBJECT" in codes(inspect(manifest,root,bindings={"BIOLOGY":"Biology"}))


def test_missing_workspace_root_holds(tmp_path, manifest):
    r=inspect(manifest,tmp_path/"absent")
    assert "SUBJECT_REPOSITORY_MISSING" in codes(r)
    assert r["mechanical_status"]=="HOLD"


def test_missing_shared_checker_is_evidence_gap(tmp_path, manifest):
    root=make_root(tmp_path)
    (root/"Shared/tools/check_subjects.py").unlink()
    assert "ORIGINAL_SHARED_CHECKER_NOT_IN_ROOT" in codes(inspect(manifest,root))


def test_symlink_escape_on_subject_contract_is_fail(tmp_path, manifest):
    root=make_root(tmp_path)
    outside=tmp_path/"external.json"
    outside.write_text(json.dumps(contract()))
    c=root/"Physics/adapter/CoreContracts.json"
    c.unlink()
    c.symlink_to(outside)
    assert "CONTRACT_PATH_ESCAPE" in codes(inspect(manifest,root))


def test_planned_subject_binding_does_not_make_math_approved(tmp_path, manifest):
    root=make_root(tmp_path)
    r=inspect(manifest,root,bindings={"PHYSICS":"Physics","MATHEMATICS":"Mathematics"})
    assert "PLANNED_SUBJECT_WORKSPACE_PREMATURE" in codes(r)
    assert r["subjects"]["MATHEMATICS"]["academic_status"] == "HOLD"


def test_native_findings_cannot_be_hidden(tmp_path, manifest):
    root=make_root(tmp_path)
    r=inspect(manifest,root,native(findings=["CONTRACT_FAILURE"]))
    assert r["mechanical_status"] == "FAIL"
    assert "NATIVE_NATIVE_SUBJECT_FINDINGS_PRESENT" in codes(r)


def test_native_forged_release_flag_cannot_change_result(tmp_path, manifest):
    root=make_root(tmp_path)
    claim=native()
    claim["release_allowed"]=True
    result=inspect(manifest,root,claim)
    assert result["release_status"]=="HOLD"
    assert "release_allowed" not in json.dumps(result)


def test_no_private_curriculum_data_echoed(tmp_path, manifest):
    root=make_root(tmp_path)
    c=root/"Physics/adapter/CoreContracts.json"
    data=json.loads(c.read_text())
    data["private_original_exam_stem"]="NOT_FOR_PUBLICATION"
    c.write_text(json.dumps(data))
    assert "NOT_FOR_PUBLICATION" not in json.dumps(inspect(manifest,root))


def test_report_deterministic(tmp_path,manifest):
    root=make_root(tmp_path)
    assert inspect(manifest,root,native()) == inspect(manifest,root,native())


def test_cli_candidate_output_is_hold(tmp_path,manifest):
    root=make_root(tmp_path)
    m=tmp_path/"m.json";m.write_text(json.dumps(manifest))
    b=tmp_path/"bindings.json";b.write_text('{"PHYSICS":"Physics"}')
    nr=tmp_path/"native.json";nr.write_text(json.dumps(native()))
    o=tmp_path/"out.json"
    assert main(["subject-workspace-audit","--manifest",str(m),"--root",str(root),
                 "--bindings",str(b),"--native-report",str(nr),"--out",str(o)])==3
    assert json.loads(o.read_text())["academic_status"]=="HOLD"


def test_cli_rejects_overwriting_native_workspace(tmp_path,manifest):
    root=make_root(tmp_path)
    m=tmp_path/"m.json";m.write_text(json.dumps(manifest))
    b=tmp_path/"bindings.json";b.write_text('{"PHYSICS":"Physics"}')
    out=root/"README.md"
    assert main(["subject-workspace-audit","--manifest",str(m),"--root",str(root),
                 "--bindings",str(b),"--out",str(out)])==2
    assert not out.exists()


def test_cli_rejects_overwriting_native_report(tmp_path,manifest):
    root=make_root(tmp_path)
    m=tmp_path/"m.json";m.write_text(json.dumps(manifest))
    b=tmp_path/"bindings.json";b.write_text('{"PHYSICS":"Physics"}')
    nr=tmp_path/"native.json";nr.write_text(json.dumps(native()))
    original=nr.read_bytes()
    assert main(["subject-workspace-audit","--manifest",str(m),"--root",str(root),
                 "--bindings",str(b),"--native-report",str(nr),"--out",str(nr)])==2
    assert nr.read_bytes()==original


def test_empty_noncompiled_reason_rejected(tmp_path,manifest):
    root=make_root(tmp_path)
    p=root/"Physics/adapter/CoreContracts.json"
    content=json.loads(p.read_text())
    content["learner_products"]["CORE1"]["production"]="NOT_COMPILED"
    content["learner_products"]["CORE1"]["reason"]="  "
    p.write_text(json.dumps(content))
    assert "CORE_PRODUCT_MISSING_REASON" in codes(inspect(manifest,root))


def test_unmapped_native_subject_directory_requires_explicit_binding(tmp_path,manifest):
    root=make_root(tmp_path)
    shared=native()
    shared["subjects_checked"]=2
    shared["subjects"].append({"subject":"Mathematics","state":"CONTRACT_ONLY",
                              "gate_registries":0,"library_packages":0,"findings":[]})
    r=inspect(manifest,root,shared)
    assert "NATIVE_UNBOUND_SUBJECT_DIRECTORY" in codes(r)
    assert r["academic_status"]=="HOLD"
