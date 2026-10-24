#!/usr/bin/env python3
"""DENSE-BOUNDARY128: full finite DPLL controls, standard library only.
Primary full audit in companion local reproducibility package; this is a compact independent replication.
"""
from itertools import combinations, product
from random import Random
from collections import Counter
import json, sys

def dpll(cs, pins=()):
    cs = [tuple(c) for c in cs] + [(v,) for v in pins]
    def run(C):
        if any(not c for c in C): return False
        if not C: return True
        while True:
            u = next((c[0] for c in C if len(c)==1), None)
            if u is None: break
            C = [tuple(x for x in c if x != -u) for c in C if u not in c]
            if any(not c for c in C): return False
            if not C: return True
        v = abs(min(C, key=len)[0])
        for p in (v,-v):
            nxt = [tuple(x for x in c if x != -p) for c in C if p not in c]
            if run(nxt): return True
        return False
    return run(cs)

def source_brute(F,n):
    for a in range(1<<n):
        if all(any(((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in F):
            return True
    return False

def guarded(F,n,d):
    assert d>=1 and all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    m=len(F); cur=n+1; g=cur; out=[]
    for p,q,r in F:
        cur+=1; a=cur
        out.extend(((-g,p,a),(-a,q,r)))
    z=[]
    for _ in range(d):
        cur+=1; z.append(cur)
    def pad(u,v):
        nonlocal cur
        cur+=1; e=cur
        out.extend(((u,v,e),(u,v,-e)))
    if d==1:
        pad(-g,z[0]); pad(g,-z[0])
    else:
        h=z[0]
        for i in range(1,d):
            if i==d-1: nxt=g
            else:
                cur+=1; nxt=cur
            pad(-h,nxt); pad(-z[i],nxt)
            out.append((h,z[i],-nxt))
            h=nxt
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in out)
    assert len(out)==2*m+(4 if d==1 else 5*(d-1))
    assert cur==n+m+(4 if d==1 else 4*d-3)
    return out,tuple(z)

def main():
    rng=Random(202610242024)
    signs=list(product((1,-1),repeat=3))
    all3=[tuple((i+1)*s[i] for i in range(3)) for s in signs]
    sources=[]
    for mask in range(1,256):
        sources.append((3,[all3[i] for i in range(8) if mask>>i&1]))
    xa=[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]
    xb=[(-1,2,3),(-1,-2,-3),(1,2,-3),(1,-2,3)]
    sources.extend([(3,xa),(3,xa+xb)])
    all4=[tuple(v*s for v,s in zip(vs,sg)) for vs in combinations(range(1,5),3) for sg in product((-1,1),repeat=3)]
    for k in range(60):
        sources.append((4,[all4[i] for i in rng.sample(range(len(all4)),3+k%22)]))
    C=Counter()
    for n,F in sources:
        sat=source_brute(F,n)
        assert dpll(F)==sat
        C['source_sat' if sat else 'source_unsat']+=1
        for d in (1,2,3,4):
            G,z=guarded(F,n,d)
            assert dpll(G)
            assert all(any(x<0 for x in c) for c in G)
            C['generated']+=1
            for bits in range(1<<d):
                pins=[z[i] if bits>>i&1 else -z[i] for i in range(d)]
                ans=dpll(G,pins)
                assert ans==(sat or bits==0)
                C['pinned_queries']+=1
                C['yes' if ans else 'no']+=1
    return dict(C)

if __name__=='__main__':
    res=main()
    print(json.dumps(res,sort_keys=True,indent=2))
