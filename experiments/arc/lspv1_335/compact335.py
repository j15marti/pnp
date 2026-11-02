#!/usr/bin/env python3
"""Independent standard-library finite reproducer for LSPV-1 335.
Only unit-cost binary-resolution DAG size is optimized; not general SAT runtime."""
from collections import deque
from itertools import combinations, product
import json

CS=((1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2))
U=CS+((),)
INDEX={c:i for i,c in enumerate(U)}
def truth(l,a):
    v=a[abs(l)-1]
    return v if l>0 else not v
def models(f,n):
    return [a for a in product((False,True),repeat=n)
            if all(any(truth(l,a) for l in c) for c in f)]
def res(a,b):
    for p in a:
        if -p not in b: continue
        q=set(a)|set(b)
        q.discard(p);q.discard(-p)
        if any(-x in q for x in q): continue
        yield tuple(sorted(q,key=lambda x:(abs(x),-x)))
PAIRS={}
for i,a in enumerate(U):
    for j,b in enumerate(U):
        if j<=i:continue
        for c in res(a,b):
            PAIRS.setdefault(INDEX[c],[]).append((i,j))
def optimum(mask):
    q=deque([(mask,0)]);seen={mask}
    while q:
        bits,d=q.popleft()
        if bits&256:return d
        for k,parents in PAIRS.items():
            if bits&(1<<k):continue
            if not any((bits&(1<<i)) and (bits&(1<<j)) for i,j in parents):continue
            nxt=bits|(1<<k)
            if nxt not in seen:
                seen.add(nxt);q.append((nxt,d+1))
    raise AssertionError("Resolution must refute every UNSAT CNF")
UNSAT={};MU={}
for mask in range(256):
    src=tuple(c for i,c in enumerate(CS) if mask&(1<<i))
    if models(src,2):continue
    w=optimum(mask);UNSAT[mask]=(src,w)
    if all(models(src[:i]+src[i+1:],2) for i in range(len(src))):
        MU[mask]=(src,w)
assert (len(UNSAT),len(MU))==(161,11)
count=0
for mask,(src,w) in UNSAT.items():
    assert any((cm&mask)==cm and cw>=w for cm,(cf,cw) in MU.items())
    for i in range(8):
        if not mask&(1<<i):
            assert optimum(mask|(1<<i))<=w
            count+=1
assert count==532
mx={}
for m in range(2,9):
    a=max(w for _,(f,w) in UNSAT.items() if len(f)<=m)
    b=max(w for _,(f,w) in MU.items() if len(f)<=m)
    assert a==b;mx[m]=a
assert list(mx.values())==[1,2,3,3,3,3,3]
EDGES=list(combinations(range(4),2))
def k4(charge):
    f=[]
    for v,b in enumerate(charge):
        inc=[i for i,e in enumerate(EDGES) if v in e]
        for pattern in product((0,1),repeat=3):
            if sum(pattern)%2==b:continue
            f.append(tuple((i+1 if p==0 else -(i+1)) for i,p in zip(inc,pattern)))
    return tuple(f)
odd=k4((1,0,0,0));even=k4((0,0,0,0))
assert len(odd)==len(even)==16
assert (len(models(odd,6)),len(models(even,6)))==(0,8)
assert all(models(odd[:i]+odd[i+1:],6) for i in range(16))
sensitive=0
for i,c in enumerate(odd):
    for j,p in enumerate(c):
        new=list(odd);new[i]=c[:j]+(-p,)+c[j+1:]
        assert models(new,6);sensitive+=1
assert sensitive==48
for src,expected in ((odd,False),(even,True)):
    guard=tuple((-7,)+c for c in src)
    assert bool(models(guard,7))
    assert bool([a for a in models(guard,7) if a[6]])==expected
def valid(f,n):
    return isinstance(n,int) and n>=0 and isinstance(f,(list,tuple)) and all(
        isinstance(c,(list,tuple)) and all(isinstance(l,int) and
        not isinstance(l,bool) and l!=0 and abs(l)<=n for l in c) for c in f)
bad=[([[0]],1),([[2]],1),([[True]],1),("oops",1),([["x"]],1),([[1]],-1)]
assert all(not valid(f,n) for f,n in bad)
assert valid([[],[1,-1],[1],[1]],1)
print(json.dumps({"status":"PASS","all_formulas":256,"unsat":len(UNSAT),
"MU":len(MU),"source_extensions":count,"core_tests":len(UNSAT),
"worst_case_W_m_le":mx,"K4_odd_models":0,"K4_even_models":8,
"K4_sign_sensitive":sensitive,"malformed_rejected":len(bad)},sort_keys=True))
