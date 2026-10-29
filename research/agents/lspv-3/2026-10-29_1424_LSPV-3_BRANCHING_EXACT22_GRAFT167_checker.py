#!/usr/bin/env python3
"""Independent exact-source Resolution checker for GRAFT167 JSON.
Usage: python checker.py [proof.json]
No trust in the generator's original clause IDs or derived clauses.
"""
import json, pathlib, sys

def main(path):
    obj=json.loads(pathlib.Path(path).read_text())
    source=obj['clauses']; rows=obj['proof']; db={}
    assert len(rows)>=len(source)
    for index,row in enumerate(rows,1):
        assert row['id']==index
        c=tuple(row['clause']);assert len(c)==len(set(c))
        assert not any(-v in c for v in c)
        if index<=len(source):
            assert row.get('source')==index
            assert sorted(c)==sorted(source[index-1])
        else:
            a,b=row['parents'];pivot=row['pivot']
            assert 1<=a<index and 1<=b<index
            ca,cb=db[a],db[b]
            assert pivot in ca and -pivot in cb
            resolved=(set(ca)-{pivot})|(set(cb)-{-pivot})
            assert not any(-v in resolved for v in resolved)
            assert set(c)==resolved
        db[index]=c
    assert db[len(rows)]==tuple()
    print(json.dumps({'checked_sources':len(source),'derived':len(rows)-len(source),
                      'final_empty_clause_id':len(rows),'valid':True}))

if __name__=='__main__':
    here=pathlib.Path(__file__).parent
    main(sys.argv[1] if len(sys.argv)>1 else
         here/'2026-10-29_1424_BRANCHING_EXACT22_GRAFT167_example_proof.json')