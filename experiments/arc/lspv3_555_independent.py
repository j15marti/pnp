#!/usr/bin/env python3
"""Independent Python controls for distinct FREE-CASE, NOT R_mix341."""
from itertools import product, combinations
import json

def full3():
    return [tuple((-(i+1) if a[i] else i+1) for i in range(3)) for a in product((0,1),repeat=3)]

def tseitin4():
    edges=list(combinations(range(4),2))
    cnf=[]
    for v in range(4):
        incident=[i for i,(a,b) in enumerate(edges) if v in (a,b)]
        for values in product((0,1),repeat=3):
            if (sum(values)%2)!=(1 if v==0 else 0):
                cnf.append(tuple((-(e+1) if values[j] else e+1) for j,e in enumerate(incident)))
    return cnf

def satisfied_clause(clause,a):
    return any((a[abs(l)-1]==1)==(l>0) for l in clause)

def numbers_of_models(cnf,n):
    return sum(all(satisfied_clause(c,a) for c in cnf) for a in product((0,1),repeat=n))

def validate_free(cnf,n):
    leaves=0
    for a in product((0,1),repeat=n):
        falsified=[i for i,c in enumerate(cnf) if not satisfied_clause(c,a)]
        if not falsified: return False, leaves
        assert 0<=falsified[0]<len(cnf)
        leaves+=1
    return True,leaves

F=full3();G=tseitin4();S=F[1:]
assert len(F)==8 and len(G)==16
assert (numbers_of_models(F,3),numbers_of_models(G,6),numbers_of_models(S,3))==(0,0,1)
assert validate_free(F,3)==(True,8)
assert validate_free(G,6)==(True,64)
assert validate_free(S,3)[0] is False
for n in range(1,7):
    full=[tuple((-(i+1) if a[i] else i+1) for i in range(n)) for a in product((0,1),repeat=n)]
    assert len(full)==2**n and numbers_of_models(full,n)==0
    for d in range(n):
        for partial in product((0,1),repeat=d):
            assert not any(all(abs(l)<=d and not satisfied_clause((l,),partial) for l in c) for c in full)
    for a in product((0,1),repeat=n):
        assert sum(not satisfied_clause(c,a) for c in full)==1
print(json.dumps({'run':'LSPV-3/555','independentPython':True,'strict3Models':0,
    'strict3LeafClosures':8,'oddK4Models':0,'oddK4LeafClosures':64,
    'fullWidthFamiliesTested':6,'satControlModels':1,'satControlAccepted':False,
    'calculus':'counterfactual no paid operations','pVsNP':'OPEN'},indent=2))
