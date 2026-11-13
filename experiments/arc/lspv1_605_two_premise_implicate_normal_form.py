#!/usr/bin/env python3
"""Exhaustive verifier for the two-premise CNF implicate normal form.
Independent semantic valuations versus syntactic source/RES+weakening closure.
"""
from itertools import product
import json
import hashlib

def clauses(n):
    out=[]
    for v in product((-1,0,1),repeat=n):
        out.append(frozenset((i+1)*(1 if s==1 else -1) for i,s in enumerate(v) if s))
    return out

def satisfied(clause,assign):
    return any(((assign>>(abs(l)-1))&1)==(1 if l>0 else 0) for l in clause)

def predicted(A,B,C):
    if A<=C or B<=C:
        return True
    for pivot in A:
        if -pivot not in B:
            continue
        resolvent=(A-{pivot})|(B-{-pivot})
        if not any(-x in resolvent for x in resolvent) and resolvent<=C:
            return True
    return False

def semantic(A,B,C,n):
    return all((not satisfied(A,s)) or (not satisfied(B,s)) or satisfied(C,s) for s in range(1<<n))

def run(n):
    cs=clauses(n); cases=0; pos=0; paths={'source_A':0,'source_B':0,'resolvent':0}; checksum=hashlib.sha256()
    for A in cs:
        for B in cs:
            for C in cs:
                p=predicted(A,B,C)
                a=semantic(A,B,C,n)
                cases+=1
                if a: pos+=1
                if p!=a:
                    raise AssertionError(dict(n=n,A=sorted(A),B=sorted(B),C=sorted(C),semantic=a,normal_form=p))
                if a:
                    if A<=C: paths['source_A']+=1
                    elif B<=C: paths['source_B']+=1
                    else: paths['resolvent']+=1
                checksum.update(b'1' if a else b'0')
    return {'n':n,'normalized_clauses':len(cs),'triple_cases':cases,'entailed':pos,'not_entailed':cases-pos,'witness_type':paths,'bits_sha256':checksum.hexdigest(),'errors':0}

def hostile():
    cases = [
        ("opposite_units", [1], [-1], [], True),
        ("resolution_to_unit", [1,2], [-1,2], [2], True),
        ("resolution_and_weakening", [1,2], [-1,3], [2,3,4], True),
        ("no_empty_from_unrelated_units", [1], [2], [], False),
        ("no_empty_from_sat_pair", [1,2], [-1,-2], [], False),
        ("not_a_stronger_resolvent", [1,2], [-1,3], [2], False),
        ("one_source_with_weakening", [1], [2], [1,2,3], True),
    ]
    rows=[]
    for name,A,B,C,expected in cases:
        A,B,C=map(frozenset,(A,B,C))
        q=predicted(A,B,C)
        t=semantic(A,B,C,4)
        if t != expected or q!=expected:
            raise AssertionError({"name":name,"expected":expected,"observed":[q,t]})
        rows.append({"name":name,"entailed":t,"expected":expected})
    F=[frozenset([1]),frozenset([-1,2]),frozenset([-2])]
    assert all(not semantic(F[i],F[j],frozenset(),2) for i in range(3) for j in range(i+1,3))
    assert all(not (satisfied(F[0],x) and satisfied(F[1],x) and satisfied(F[2],x)) for x in range(4))
    rows.append({"name":"three_clause_global_unsat_vs_pairwise_sat","entailed_globally":True,"entailed_by_any_pair":False})
    return rows

if __name__=='__main__':
    a=[run(1),run(2),run(3),run(4)]
    print(json.dumps({'result':'PASS','tests':a,'hostile_controls':hostile(),'statement':'F={A,B} |= C iff A subset C, B subset C, or a non-tautological resolvent subset C','scope':'non-tautological normalized clauses over 1..4 vars, empty clause included; not historical native R_mix341'},indent=2))
