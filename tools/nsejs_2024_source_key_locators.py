"""IAPT 2024 Code-51 source identity & official final-key LINKED record index.

These are exam *locators*, not reproduced questions. Transcribed answer letters
and paper-level subject ranges require independent item-by-item verification.
Do not infer 2020-23 codes, redistribute original stems, or claim academic/QRT
admission from this record map. All question text and figures stay on IAPT.
"""
from __future__ import annotations
import hashlib
import json

SCHEMA="grade9-nsejs-code51-publisher-key-locators/v1"
OFFICIAL_PAPER="https://www.iapt.org.in/images/nse_2024/NSEJS-2024_Set_51.pdf"
OFFICIAL_KEY="https://www.iapt.org.in/images/nse_2024/NSEJS_-_2024_Final_Answer_Key.pdf"
# Source: IAPT 2024 official Code 51 FINAL key, publicly linked in source
# registry. Exact source-PDF bytes and rights are not included in the build.
# Academic reviewer must independently authenticate every subject assignment.
KEY={
 1:"D",2:"C",3:"B",4:"C",5:"A",6:"C",7:"D",8:"A",
 9:"A",10:"C",11:"C",12:"A",13:"D",14:"A",15:"C",16:"B",
 17:"C",18:"D",19:"D",20:"DROP",21:"B",22:"A",23:"A",24:"C",
 25:"D",26:"C",27:"A",28:"C",29:"C",30:"A",31:"B",32:"B",
 49:"ABD",50:"CD",51:"BC",52:"ACD",
 53:"ABC",54:"CD",55:"AD",56:"ABC",
}
SUBJECT_NUMBERS={
 "BIOLOGY":tuple(range(1,17))+(49,50,51,52),
 "CHEMISTRY":tuple(range(17,33))+(53,54,55,56),
}
ID_BASIS="EXISTING_2024_SUBJECT_TEST_CENSUS_PROVISIONAL_NOT_INDEPENDENTLY_ADMITTED"

def digest(value: object)->str:
    return hashlib.sha256(json.dumps(value,sort_keys=True,
         separators=(",",":"),ensure_ascii=False).encode("utf-8")).hexdigest()

def official_locator_bank(registry: dict) -> dict:
    if registry.get("schema")!="grade9-nsejs-source-linked-practice/v1" or (
        registry.get("academic_admission")!="HOLD" or
        registry.get("redistribution_rights")!="HOLD" or
        registry.get("actual_question_bodies")!=0):
        raise ValueError("IAPT_SOURCE_LINK_REGISTRY_NOT_HELD")
    matches=[x for x in registry["years"] if x["year"]==2024]
    if (len(matches)!=1 or matches[0].get("paper_code")!=51 or
        matches[0].get("paper_url")!=OFFICIAL_PAPER or
        matches[0].get("key_url")!=OFFICIAL_KEY or
        matches[0].get("source_authentication")!="HOLD" or
        matches[0].get("dropped_question_numbers")!=[20] or
        matches[0].get("multi_answer_range")!=[49,60]):
        raise ValueError("IAPT_FINAL_KEY_PROVENANCE_CONFLICT")
    if (len(KEY)!=40 or set(KEY)!=set(SUBJECT_NUMBERS["BIOLOGY"])|set(SUBJECT_NUMBERS["CHEMISTRY"]) or
        len(set(SUBJECT_NUMBERS["BIOLOGY"])&set(SUBJECT_NUMBERS["CHEMISTRY"]))!=0):
        raise ValueError("SUBJECT_OCCURRENCE_CENSUS_NOT_UNIQUE")
    records=[]
    for sub,numbers in SUBJECT_NUMBERS.items():
        if len(numbers)!=20:raise ValueError("SUBJECT_CENSUS_NOT_TWENTY")
        for num in numbers:
            part="A2" if num>=49 else "A1"
            key=KEY[num]
            if num==20 and key!="DROP":raise ValueError("DROPPED_2024_Q20_KEY_MUST_NOT_BE_INFERRED")
            if num!=20 and (not key or len(set(key))!=len(key) or
                             any(c not in "ABCD" for c in key) or
                             (part=="A1" and len(key)!=1)):
                raise ValueError("MALFORMED_OFFICIAL_FINAL_KEY")
            uid=f"g9:NSEJS:2024:51:{sub}:Q{num:02d}"
            info={
                "uid":uid,"subject":sub,"year":2024,"paper_code":51,
                "question_number":num,"part":part,
                "publisher_key":list(key) if key!="DROP" else None,
                "publisher_key_status":"DROP" if key=="DROP" else "IAPT_TRANSCRIBED_PROVISIONAL",
                "source_locator":OFFICIAL_PAPER,
                "publisher_final_key_url":OFFICIAL_KEY,
                "subject_identity_basis":ID_BASIS,
                "source_question_text":None,"source_figures":[],
                "source_custody":"HOLD","academic_admission":"HOLD",
                "usage":"READ_EXTERNAL_PAPER_AND_COMMIT_BEFORE_LOCAL_KEY_COMPARISON",
            }
            info["revision_sha256"]=digest(info)
            records.append(info)
    result={
        "schema":SCHEMA,
        "paper_url":OFFICIAL_PAPER,"final_key_url":OFFICIAL_KEY,
        "registry_sha256":digest(registry),
        "origin":"IAPT_2024_CODE51_PAPER_AND_FINAL_KEY_PUBLIC_LOCATORS",
        "source_text_copied":False,
        "questions_present_as_original_text":0,
        "total_locator_records":40,
        "subject_locator_counts":{"BIOLOGY":20,"CHEMISTRY":20},
        "key_transcription_status":"PROVISIONAL_UNTIL_SECOND_REVIEW",
        "academic_admission":"HOLD","redistribution_review":"HOLD",
        "subject_mapping_basis":ID_BASIS,
        "items":records,
    }
    return result
