#!/usr/bin/env python3
"""LSPV-1/403 finite tests of source-retaining clocked preprocessors.
Not a verifier for native R_mix341. Deterministic, no third-party packages.
Usage: python3 lspv1_403_sat_preprocessor.py output.json
"""
import json, sys
from itertools import product

def canonical(n):
    return [[i] for i in range(1,n+1)]

def is_canonical(F):
    return isinstance(F,list) and len(F)>0 and all(c==[i] for i,c in enumerate(F,1))

def valid(F):
    return isinstance(F,list) and all(isinstance(c,list) and all(type(l)==int and l!=0 for l in c) for c in F)

def sat(F):
    assert valid(F)
    v=max((abs(l) for c in F for l in c),default=0)
    for a in product((False,True),repeat=v):
        if all(any(a[abs(l)-1] == (l>0) for l in c) for c in F):
            return True
    return False

def transform(F,halt_step):
    if not valid(F): return F
    if is_canonical(F) and halt_step is not None and halt_step<=len(F):
        z=len(F)+1
        return [c[:] for c in F]+[[z],[-z]]
    return [c[:] for c in F]

def xor3(v,charge):
    clauses=[]
    for bits in product((0,1),repeat=3):
        if sum(bits)%2 !=charge:
            clauses.append([(-x if bit else x) for x,bit in zip(v,bits)])
    return clauses

def k4(charge):
    E=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    F=[]
    for vertex in range(4):
        incident=[i+1 for i,(u,v) in enumerate(E) if u==vertex or v==vertex]
        F+=xor3(incident,charge[vertex])
    return F

checks=0
rows=[]
for h in [None]+list(range(1,12)):
    for n in range(1,10):
        F=canonical(n); G=transform(F,h)
        changed=h is not None and h<=n
        assert sat(F) and sat(G)==(not changed);checks+=2
        assert G[:n]==F and (len(G)==n+2)==changed;checks+=2
        assert is_canonical(F) and valid(G);checks+=2
        rows.append({'halt_step':h,'n':n,'trigger':changed,'sat_before':sat(F),'sat_after':sat(G),'retained_source':G[:n]==F,'output_clause_count':len(G)})
controls={
 'sat_units':[[1],[3]],
 'unsat_units':[[1],[-1]],
 'horn_sat':[[-1,2],[1]],
 'horn_unsat':[[1],[-1,2],[-2]],
 'twosat_sat':[[1,2],[-1,2]],
 'twosat_unsat':[[1,2],[1,-2],[-1,2],[-1,-2]],
 'tseitin_even':k4([0,0,0,0]),
 'tseitin_odd':k4([1,0,0,0]),
}
control_rows=[]
for name,F in controls.items():
    expected=sat(F)
    assert not is_canonical(F);checks+=1
    for h in [None,1,2,4,20]:
        G=transform(F,h)
        assert G==F and sat(G)==expected;checks+=2
    control_rows.append({'name':name,'sat':expected,'unchanged':True,'nclauses':len(F)})
for F in ['bad',42,[0],[[0]],[[1],['x']],[[True]],{'c':[[1]]}]:
    assert not valid(F) and transform(F,1)==F;checks+=2

# The symbolic theorem uses an arbitrary TM. This bounded test uses a finite
# explicit halting threshold and never purports to decide nonhalting.
raw={'id':'LSPV1_403_CLOCKED_SAT_PRESERVATION',
     'model':'Strict signed CNF clause arrays; finite halt-step controls',
     'rows':rows,'controls':control_rows,
     'malformed_rejections':7,'checks':checks,
     'theorem_verified_by_finite_test':False}
assert len(rows)==108 and checks>600
with open(sys.argv[1] if len(sys.argv)>1 else 'lspv1_403_raw.json','w') as f:json.dump(raw,f,indent=2,sort_keys=True)
print(json.dumps({'rows':len(rows),'controls':len(control_rows),'checks':checks}))
