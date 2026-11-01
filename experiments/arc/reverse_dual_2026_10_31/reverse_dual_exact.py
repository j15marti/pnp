#!/usr/bin/env python3
"""Finite dual reverse-cofactor and boundary-mask verifier for canonical Y6.
Only offline exhaustive diagnostics; not an efficient universal SAT solver.
"""
from itertools import product
from collections import Counter
import json

F=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
N=6

def valid(F,n):
    if n%3 or 3*len(F)!=4*n: return False
    counts=Counter()
    seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if any(abs(x)<1 or abs(x)>n for x in c): return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        key=tuple(sorted(c))
        if key in seen: return False
        seen.add(key)
        counts.update(c)
    return all(counts[x]==2 and counts[-x]==2 for x in range(1,n+1))

def ctrue(c,a):
    return any(a[abs(x)-1]==int(x>0) for x in c)

def completions(F,p):
    free=[i for i,b in enumerate(p) if b==-1]
    for b in product((0,1),repeat=len(free)):
        a=list(p)
        for i,v in zip(free,b): a[i]=v
        if all(ctrue(c,a) for c in F): yield tuple(a)

def residual(F,p):
    r={}
    for j,c in enumerate(F,1):
        if any(p[abs(x)-1]==int(x>0) for x in c): continue
        r[j]=tuple(x for x in c if p[abs(x)-1]==-1)
    return r

def profile(clauses,boundary,interior):
    answers={}
    for bits in product((0,1),repeat=len(boundary)):
        shared=dict(zip(boundary,bits))
        ok=False
        for free in product((0,1),repeat=len(interior)):
            a={**shared,**dict(zip(interior,free))}
            if all(any(a[abs(x)]==int(x>0) for x in c) for c in clauses):
                ok=True
                break
        answers[''.join(map(str,bits))]=ok
    return answers

def interface_case(F,p,left_ids,right_ids,B,XL,XR):
    r=residual(F,p)
    assert set(r)==set(left_ids)|set(right_ids)
    assert not set(XL).intersection(XR)
    left=[r[j] for j in left_ids]; right=[r[j] for j in right_ids]
    assert all(set(map(abs,c))<=set(B)|set(XL) for c in left)
    assert all(set(map(abs,c))<=set(B)|set(XR) for c in right)
    L=profile(left,B,XL); R=profile(right,B,XR)
    overlap=sorted(b for b in L if L[b] and R[b])
    witnesses=sum(1 for _ in completions(F,p))
    assert bool(overlap)==bool(witnesses)
    cover={b:('L' if not L[b] else 'R') for b in L if b not in overlap}
    assert len(cover)+len(overlap)==2**len(B)
    return {"partial":list(p),"boundary":B,
        "left_original_clause_ids":left_ids,"right_original_clause_ids":right_ids,
        "left_sat_mask":sorted(b for b in L if L[b]),
        "right_sat_mask":sorted(b for b in R if R[b]),
        "intersection":overlap,"refutation_cover":cover,
        "complete_witness_count":witnesses}

def main():
    assert valid(F,N)
    states={p:bool(next(completions(F,p),None))
            for p in product((-1,0,1),repeat=N)}
    assert len(states)==729
    edges=0
    for p,y in states.items():
        for i,v in enumerate(p):
            if v!=-1: continue
            p0=p[:i]+(0,)+p[i+1:]
            p1=p[:i]+(1,)+p[i+1:]
            assert y==(states[p0] or states[p1])
            assert (not y)==((not states[p0]) and (not states[p1]))
            edges+=1
    assert edges==1458
    counter=Counter('SAT' if x else 'UNSAT' for x in states.values())
    assert counter['SAT']==529 and counter['UNSAT']==200
    u=interface_case(F,(-1,0,1,0,0,-1),[2],[3,6],[1],[],[6])
    s=interface_case(F,(-1,0,1,0,1,-1),[3],[6],[6],[],[1])
    assert u["left_sat_mask"]==["1"] and u["right_sat_mask"]==["0"]
    assert not u["intersection"] and u["refutation_cover"]=={"0":"L","1":"R"}
    assert s["intersection"]==["1"]
    # Both global extreme complete assignments fail while Y6 has 20 witnesses.
    assert not all(ctrue(c,(0,)*N) for c in F)
    assert not all(ctrue(c,(1,)*N) for c in F)
    assert sum(1 for _ in completions(F,(-1,)*N))==20
    # A disjoint canonical SAT copy with x7=0 gives 20*10 models,
    # illustrating the polynomial SAT-to-nonempty-residual mapping.
    F2=F+tuple(tuple((1 if x>0 else -1)*(abs(x)+6) for x in c) for c in F)
    assert valid(F2,12)
    gadget=tuple(0 if i==6 else -1 for i in range(12))
    assert sum(1 for _ in completions(F2,gadget))==200
    out={"status":"PASS","canonical_source":"Y6","states":len(states),
         "sat_states":counter["SAT"],"unsat_states":counter["UNSAT"],
         "reverse_cofactor_variable_checks":edges,"source_witnesses":20,
         "both_global_endpoints_fail":True,
         "unsat_boundary_case":u,"sat_boundary_case":s,
         "disjoint_gadget_fixed_variable_models":200,
         "scope":"finite offline audit; no polynomial all-target guarantee"}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=="__main__": main()
