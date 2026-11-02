#!/usr/bin/env python3
"""LSPV-2 329 concise independent source and cut verification, stdlib only.
Full polynomial lower-bound circulation producer and no-import verifier are in run archive.
"""
import itertools,json,collections
POS=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9))
F=POS+tuple(tuple(-x for x in c) for c in POS)
assert len(F)==12 and len({tuple(sorted(c)) for c in F})==12
assert all(sum(x in c for c in F)==sum(-x in c for c in F)==2 for x in range(1,10))

def models(p):
    free=[i for i in range(1,10) if i not in p]
    count=0
    for tail in itertools.product((0,1),repeat=len(free)):
        x=dict(p);x.update(zip(free,tail))
        if all(any(x[abs(z)]==int(z>0) for z in c) for c in F):count+=1
    return count

def locally_falsified(p):
    return any(all(abs(z) in p and p[abs(z)]!=int(z>0) for z in c) for c in F)

def arc_bounds(p):
    E=[]
    for j,c in enumerate(POS,1):
        t=sum(p.get(e,-1)==1 for e in c)
        r=sum(e not in p for e in c)
        lo=max(0,1-t);hi=min(r,2-t)
        if lo>hi:return None
        E.append(('source',f'c{j}',lo,hi) if j<=3 else (f'c{j}','sink',lo,hi))
    for x in range(1,10):
        if x not in p:E.append((f'c{1+(x-1)//3}',f'c{4+(x-1)%3}',0,1))
    E.append(('sink','source',0,9))
    return E

def check_cut(p,S):
    E=arc_bounds(p);assert E is not None
    S=set(S)
    L=sum(lo for u,v,lo,hi in E if u not in S and v in S)
    U=sum(hi for u,v,lo,hi in E if u in S and v not in S)
    assert L>U
    return L,U

pU={3:0,6:0,7:1,8:1};pS={**pU,3:1}
assert not locally_falsified(pU)
assert models(pU)==0 and models(pS)==5
assert check_cut(pU,('source','sink','c1','c2','c4','c5'))==(1,0)
w=(0,0,1,1,0,0,1,1,0)
assert all(any(w[abs(z)-1]==int(z>0) for z in c) for c in F)
assert all(w[i-1]==v for i,v in pS.items())
count=collections.Counter()
for cube in itertools.product((-1,0,1),repeat=9):
    p={i+1:v for i,v in enumerate(cube) if v!=-1}
    n=models(p)
    count['SAT' if n else 'UNSAT_LOCAL' if locally_falsified(p) else 'UNSAT_NONLOCAL']+=1
assert count=={'SAT':12001,'UNSAT_LOCAL':6926,'UNSAT_NONLOCAL':756}
print(json.dumps({'checked_cubes':3**9,'labels':dict(count),'nonlocal_original_cut':[1,0],
  'same_original_opposite_models':[0,5], 'P_vs_NP':'OPEN'},sort_keys=True))
