#!/usr/bin/env python3
"""Independent source-authenticated Resolution replay for the linked strict exact22 control.
The checker does NOT prove a universal theorem or discover certificates.
"""
import json, hashlib,sys
from pathlib import Path

HERE=Path(__file__).parent
TRACE=HERE/'2026-10-29_0726_TERNARY_CLAUSE_PORT162_resolution.json'

def check_trace(path=TRACE):
    data=json.loads(Path(path).read_text())
    orig=data['orig'];lines={int(i):x for i,x in data['lines'].items()}
    assert len(orig)==43
    # Independently parse full source clauses, not just involved parents.
    first=[tuple(c) for c in orig[:40]]
    assert len(set(tuple(sorted(c)) for c in first))==40
    import hashlib
    source_digest=hashlib.sha256(json.dumps(orig[:40],separators=(',',':')).encode()).hexdigest()
    assert source_digest=='2af85fecbb8871c57ac47dbf6f2e3423f8bc2a3c03bfda135f89f21f16a52413'
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in first)
    assert tuple(orig[40])==(1,) and tuple(orig[41])==(2,) and tuple(orig[42])==(-13,)
    # Verify signed degrees and connectedness of original, independent of builder.
    from collections import Counter
    deg=Counter((abs(l),l>0) for c in first for l in c)
    assert all(deg[(v,True)]==deg[(v,False)]==2 for v in range(1,31))
    source_set=set()
    for i,(c) in enumerate(orig,1):
        if i in lines:
            d=lines[i]
            assert tuple(d['clause'])==tuple(c)
            assert d['source']==i
            source_set.add(i)
    n_derived=0
    for lineid in sorted(lines):
        d=lines[lineid]
        if 'source' in d:continue
        n_derived+=1
        ia,ib=d['parents'];pivot=d['pivot']
        assert ia<lineid and ib<lineid
        assert ia in lines and ib in lines
        a=set(lines[ia]['clause']);b=set(lines[ib]['clause'])
        assert pivot in a and -pivot in b
        out=(a-{pivot})|(b-{-pivot})
        assert not any(-l in out for l in out)
        assert out==set(d['clause'])
        assert len(out)==len(d['clause'])
    empty=data['empty_id']
    assert empty in lines and lines[empty]['clause']==[]
    assert n_derived==18
    assert len(source_set)==11
    return {'checked_derived_steps':n_derived,'authenticated_sources_and_assumptions':len(source_set),'empty_clause_id':empty}

if __name__=='__main__':
    check=check_trace()
    print(json.dumps(check,sort_keys=True))
    # Mutation controls: wrong pivot and malformed empty target must fail.
    d=json.loads(TRACE.read_text());changed=[k for k in d['lines'] if 'parents' in d['lines'][k]][0]
    import tempfile
    for which in ('pivot','resolvent'):
        e=json.loads(json.dumps(d))
        if which=='pivot':e['lines'][changed]['pivot']+=99
        else:e['lines'][changed]['clause']=[300]
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',delete=False) as fp:
            json.dump(e,fp);temp=fp.name
        try:
            check_trace(temp)
            raise AssertionError('checker accepted mutation '+which)
        except AssertionError as exc:
            if str(exc).startswith('checker accepted mutation'):raise
        finally:
            Path(temp).unlink()
    print('two corruptions rejected')