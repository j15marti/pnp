#!/usr/bin/env python3
"""Apply the exact ARC-0005 additive inserts only to explicitly checked blobs.

This script performs no network calls and makes no Git commit. Fetch/read the
current root files first. On concurrent edits, review the new sources and pass
their freshly verified blob SHAs. Default operation only prints a dry run.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import signal

DEFAULTS = {
    'main4.tex': '39e04a41c0015de39cd717d886d38c7ec15e97df',
    'main5.tex': '86eae3305853dec082bb7bbd277c9c887d612d03',
}

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def plan(root: Path, insert_root: Path, expected: dict[str,str]) -> list[dict]:
    changes=[]
    for name in ('main4.tex','main5.tex'):
        old=(root/name).read_bytes()
        insert=(insert_root/name.replace('.tex','.insert.tex')).read_bytes()
        if blob(old) != expected[name]:
            raise ValueError(f'{name}: stale SHA; refetch and review, do not overwrite')
        marker=insert.splitlines()[0]
        if marker in old:
            raise ValueError(f'{name}: ARC-0005 already present; inspect before retry')
        anchor=b'\\bibliographystyle{plain}'
        if old.count(anchor)!=1:
            raise ValueError(f'{name}: expected one bibliography anchor')
        new=old.replace(anchor,insert+b'\n'+anchor,1)
        assert new.replace(insert+b'\n',b'',1)==old
        changes.append({'path':name,'base_blob_sha':blob(old),'new_blob_sha':blob(new),'sha256':hashlib.sha256(new).hexdigest(),'body':new})
    return changes

def main() -> None:
    signal.alarm(25)
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path.cwd())
    ap.add_argument('--main4-sha',default=DEFAULTS['main4.tex'])
    ap.add_argument('--main5-sha',default=DEFAULTS['main5.tex'])
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    edits=plan(args.root,Path(__file__).resolve().parent,
               {'main4.tex':args.main4_sha,'main5.tex':args.main5_sha})
    if args.apply:
        # Both sources were validated before either replacement is attempted.
        for item in edits:
            path=args.root/item['path']
            if blob(path.read_bytes())!=item['base_blob_sha']:
                raise ValueError('file changed after validation; stop and inspect')
            tmp=path.with_suffix(path.suffix+'.ARC-0005.tmp')
            tmp.write_bytes(item['body']);tmp.replace(path)
            assert blob(path.read_bytes())==item['new_blob_sha']
    print(json.dumps({'state':'APPLIED_LOCALLY' if args.apply else 'DRY_RUN',
                      'changes':[{k:v for k,v in e.items() if k!='body'} for e in edits]},indent=2))
    signal.alarm(0)

if __name__=='__main__':
    main()
