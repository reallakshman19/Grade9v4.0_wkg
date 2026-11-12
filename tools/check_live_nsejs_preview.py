#!/usr/bin/env python3
"""Verify exact GitHub Pages bytes for an authorized NSEJS technical preview."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def download(url:str)->bytes:
    request=Request(url,headers={"User-Agent":"Grade9-NSEJS-Pages-exact-byte-check","Cache-Control":"no-cache"})
    with urlopen(request,timeout=20) as r:
        if r.status!=200:
            raise ValueError("HTTP_STATUS_"+str(r.status)+":"+url)
        return r.read()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--url",required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    args=ap.parse_args()
    expected=json.loads(args.manifest.read_text(encoding="utf-8"))
    if expected.get("status")!="GRADE9_NSEJS_UNVALIDATED_TECHNICAL_PREVIEW" or expected.get("academic_approval")!="HOLD":
        raise ValueError("DEPLOY_MANIFEST_ADMISSION_OR_SCOPE_INVALID")
    if expected.get("core1ab_authored_lesson_pages")!=8 or expected.get("school_wpe_preserved") is not True:
        raise ValueError("PREVIEW_COMPLETENESS_FALSE")
    base=args.url.rstrip("/")+"/"
    manifest_bytes=args.manifest.read_bytes()
    last=None
    for attempt in range(18):
        try:
            if download(urljoin(base,"PUBLIC_PREVIEW_MANIFEST.json"))!=manifest_bytes:
                raise ValueError("PAGES_REVISION_MISMATCH")
            for path,digest in expected["files"].items():
                if hashlib.sha256(download(urljoin(base,path))).hexdigest()!=digest:
                    raise ValueError("PAGES_FILE_HASH_MISMATCH:"+path)
            print("PASS exact live GitHub Pages preview:",base,len(expected["files"]),"hash-matched static assets; academic HOLD")
            return 0
        except Exception as exc:
            last=exc
            if attempt<17:time.sleep(3)
    raise ValueError("LIVE_PAGES_VALIDATION_FAILED:"+str(last))

if __name__=="__main__":
    raise SystemExit(main())
