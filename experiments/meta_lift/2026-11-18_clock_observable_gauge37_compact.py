#!/usr/bin/env python3
"""Independent compact CLOCKOBSERVABLEGAUGE37 finite witness check.
Full 53-model audit and raw data are in the local research bundle.
"""
import itertools
import json


def test(N, cap):
    h=(0,)*N
    def observation(f):
        q=0; trace=[]
        for i,b in enumerate(f):
            trace.append(str(i&1) if b and q<cap else '')
            q=min(cap,q+b)
        return (tuple(trace),q)
    rows=[]; mins={}
    for x in range(1<<N):
        f=tuple((x>>(N-i-1))&1 for i in range(N))
        o=observation(f)
        d=sum(f)
        if o not in mins or d<mins[o]:mins[o]=d
        rows.append((o,f))
    tests=0
    for o,f in rows:
        r=sum(w!='' for w in o[0])
        D=(r+1)*cap+r  # K=cap+1, e_phys=0, baseline h=0^N
        assert mins[o]<=D
        assert mins[o]<=cap
        tests+=2
    assert len(mins)==sum(__import__('math').comb(N,j) for j in range(cap+1))
    # Trace remembers first cap event positions, not merely the concatenated word.
    return dict(N=N,cap=cap,labels=len(mins),cases=len(rows),assertions=tests+1)


def controls():
    n=8
    def trace(f):
        q=0; t=[]
        for b in f:t.append(q);q^=b
        return tuple(t),q
    all_signatures={trace(f) for f in itertools.product((0,1),repeat=n)}
    assert len(all_signatures)==1<<n
    assert trace((1,0,1,0,1,0,1,0)) != trace((0,)*n)
    assert sum((1,0,1,0,1,0,1,0))>1
    return 3

if __name__=='__main__':
    reports=[test(8,1),test(8,2),test(16,1),test(16,2)]
    extra=controls()
    print(json.dumps({'revision':'CLOCKOBSERVABLEGAUGE37.compact.v1',
                      'status':'finite checks only; theorem is in separate report',
                      'models':reports,'assertions':sum(x['assertions'] for x in reports)+extra,
                      'failures':0},sort_keys=True))
