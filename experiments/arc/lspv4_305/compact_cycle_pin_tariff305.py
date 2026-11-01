#!/usr/bin/env python3
"""LSPV-4 305 compact self-contained witness for the pinned-cycle theorem.
Full independent verifier and per-occurrence source raw in ZIP archive.
"""
import itertools, json
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
def valid(F):
    n=max(abs(x) for C in F for x in C)
    return len(F)*3==4*n and len(set(tuple(sorted(C)) for C in F))==len(F) and all(len(C)==3 and len({abs(x) for x in C})==3 and len({x>0 for x in C})==1 for C in F) and all(sum(x==v for C in F for x in C)==2 and sum(x==-v for C in F for x in C)==2 for v in range(1,n+1))
def model_count(F,p):
    free=[i for i in range(1,max(abs(x) for C in F for x in C)+1) if i not in p]
    total=0
    for values in itertools.product((False,True),repeat=len(free)):
        a=dict(p);a.update(zip(free,values))
        total+=all(any(a[abs(x)]==(x>0) for x in C) for C in F)
    return total
def binary_edges(F,p):
    out=[]
    for j,C in enumerate(F):
        if any(abs(x) in p and p[abs(x)]==(x>0) for x in C):continue
        free=[abs(x) for x in C if abs(x) not in p]
        if len(free)==2:out.append((j,*free))
    return out
def triangles(E):
    out=[]
    for a,b,c in itertools.combinations(E,3):
        V={v for e in (a,b,c) for v in e[1:]}
        P={tuple(sorted(e[1:])) for e in (a,b,c)}
        if len(V)==3 and len(P)==3:out.append(tuple(sorted((a[0],b[0],c[0]))))
    return sorted(set(out))
def run(F):
    assert valid(F)
    n=max(abs(x) for C in F for x in C)
    totals={'states':0,'max_binary':0,'max_nu':0,'failures':0}
    for bits in itertools.product((None,False,True),repeat=n):
        p={i+1:x for i,x in enumerate(bits) if x is not None}
        E=binary_edges(F,p);used=set();nu=0
        for C in triangles(E):
            if used.isdisjoint(C):used.update(C);nu+=1
        totals['states']+=1
        totals['max_binary']=max(totals['max_binary'],len(E));totals['max_nu']=max(totals['max_nu'],nu)
        if len(E)>2*len(p) or 3*nu>2*len(p):totals['failures']+=1
    return totals
assert valid(F9) and valid(Y6)
satp={5:False,6:True,7:False,8:False,9:True}
unsatp={8:False,3:False,7:False,6:False,1:True,5:True}
assert model_count(F9,{})==70 and model_count(Y6,{})==20
assert model_count(F9,satp)==3 and model_count(F9,unsatp)==0
result={'run':'305','F9':run(F9),'Y6':run(Y6),'same_F9_SAT_extensions':3,'same_F9_UNSAT_extensions':0,'root_F9_delta':6,'root_Y6_delta':4}
assert result['F9']['failures']==result['Y6']['failures']==0
print(json.dumps(result,sort_keys=True,indent=2))
