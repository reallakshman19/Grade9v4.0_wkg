import json
from grade9qa.cli import main
from grade9qa.validate import inspect
from grade9qa.io import confined_path
from grade9qa.errors import InputError
from grade9qa.sha256 import file_sha256
import pytest

def modify(root, file, fn):
    p = root / file
    data = json.loads(p.read_text())
    fn(data)
    p.write_text(json.dumps(data))

def error_codes(root):
    return [entry.code for entry in inspect(root / "bundle.json")[2]]

def test_bridge_stays_hold(candidate,tmp_path):
    output = tmp_path/"bridge.json"
    assert main(["bridge","--bundle",str(candidate/"bundle.json"),"--out",str(output)]) == 0
    d=json.loads(output.read_text())
    assert d["bridge_results"][0]["result"]=="HOLD"

def test_report_stable_except_time(candidate,tmp_path):
    a=tmp_path/"a.json"; b=tmp_path/"b.json"
    args=["--bundle",str(candidate/"bundle.json"),"--out"]
    assert main(["validate",*args,str(a)])==0
    assert main(["validate",*args,str(b)])==0
    d1=json.loads(a.read_text()); d2=json.loads(b.read_text())
    d1.pop("generated_at"); d2.pop("generated_at")
    assert d1==d2

def test_multiple_pages_one_construction(candidate,tmp_path):
    def add_page(rows):
        clone=dict(rows[0]); clone["id"]="LESSON-A02"; rows.append(clone)
    modify(candidate,"lessons.json",add_page)
    modify(candidate,"constructions.json",lambda rows:rows[0]["lesson_ids"].append("LESSON-A02"))
    out=tmp_path/"out.json"
    assert main(["validate","--bundle",str(candidate/"bundle.json"),"--out",str(out)])==0
    assert json.loads(out.read_text())["coverage"]["candidate_constructions"]==1

def test_extra_schema_field_rejected(candidate):
    modify(candidate,"warrants.json",lambda rows:rows[0].update(unknown="cannot infer approval"))
    assert "SCHEMA_ERROR" in error_codes(candidate)

def test_missing_collection(candidate):
    (candidate/"warrants.json").unlink()
    assert "INPUT_ERROR" in error_codes(candidate)

def test_bad_collection_type(candidate):
    (candidate/"warrants.json").write_text("{}")
    assert "SCHEMA_ERROR" in error_codes(candidate)

def test_symlink_cannot_escape(candidate,tmp_path):
    external=tmp_path/"outside.json"; external.write_text("[]")
    (candidate/"external.json").symlink_to(external)
    modify(candidate,"bundle.json",lambda d:d["files"].update(sources="external.json"))
    assert "INPUT_ERROR" in error_codes(candidate)

def test_direct_path_traversal_rejected(candidate):
    with pytest.raises(InputError):
        confined_path(candidate,"../outside.json")

def test_sha256_matches_fixture(candidate):
    assert file_sha256(candidate/"synthetic-note.txt") == "abec801212bbf56f4449022053d5edc4f7ca4a1528050e7316034b458da08de4"

def test_not_qualified_despite_valid_hash(candidate,tmp_path):
    out=tmp_path/"out.json"
    assert main(["qualify","--bundle",str(candidate/"bundle.json"),"--out",str(out)])==3
    assert json.loads(out.read_text())["qualification_status"]=="HOLD"
