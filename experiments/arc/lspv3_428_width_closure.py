#!/usr/bin/env python3
"""Exact strict ordinary-Resolution width-closure lower bound checker on published K4/K3,3 odd Tseitin 3-CNFs. This does not check mixed Rmix341.
Run: python lspv3_428_width_closure.py
"""
import itertools
from collections import defaultdict,deque

def mk(h):
    edges=([(i,j) for i in range(4) for j in range(i+1,4)] if h==4 else [(i,j) for i in range(3) for j in range(3,6)])
    inc=[[] for _ in range(h)]
    for i,(u,v) in enumerate(edges,1):inc[u].append(i);inc[v].append(i)
    out=[]
    for u,row in enumerate(inc):
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2==(u==0):continue
            out.append(frozenset((-z if b else z) for z,b in zip(row,a)))
    return out
def restrict(C,lit):
    return [frozenset(v for v in c if v!=-lit) for c in C if lit not in c]
def close(C,w):
    found=set(c for c in C if len(c)<=w);q=deque(found);pos=defaultdict(set);neg=defaultdict(set);attempts=0
    for c in found:
        for v in c:(pos if v>0 else neg)[abs(v)].add(c)
    while q:
        c=q.popleft()
        if not c:return True,len(found),attempts
        for v in c:
            for d in tuple((neg if v>0 else pos)[abs(v)]):
                a,b=(c,d) if v>0 else (d,c)
                attempts+=1
                r=(a-{abs(v)})|(b-{-abs(v)})
                if len(r)>w or any(-z in r for z in r) or r in found:continue
                r=frozenset(r);found.add(r);q.append(r)
                for z in r:(pos if z>0 else neg)[abs(z)].add(r)
    return False,len(found),attempts
if __name__=='__main__':
    expected={(4,3,0):16,(4,2,1):4,(4,2,-1):4,(6,4,0):384,(6,3,1):68,(6,3,-1):68}
    for (h,w,lit),count in expected.items():
        C=mk(h)
        if lit:C=restrict(C,lit)
        out=close(C,w)
        print(h,w,lit,out)
        assert out[0] is False and out[1]==count
    print('All six independently closed lower-width conditions VERIFIED')
