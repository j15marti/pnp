#!/usr/bin/env python3
"""Meta-solver exact-one rational nullity and modular-blind UNSAT control.
python3 2026-11-23_1037_modular_blind_reproducer.py
Pure Python 3, deterministic, no external packages.
"""
from fractions import Fraction
from itertools import combinations, product
from random import Random
import json

BLIND=((0,1,2),(0,1,3),(0,2,3),(0,4,5),(1,2,4))
FANO=((1,4,6),(2,3,6),(0,3,4),(2,4,5),(0,1,2),(1,3,5),(0,5,6))

def sat_models(edges,n):
    return [mask for mask in range(1<<n) if all(
        sum((mask>>v)&1 for v in e)==1 for e in edges)]

def rref(edges,n,p=None):
    A=[]
    for e in edges:
        row=[0]*n+[1]
        for v in e:row[v]+=1
        A.append([Fraction(x) for x in row] if p is None else [x%p for x in row])
    pivots=[];updates=0
    for col in range(n):
        j=len(pivots)
        row=next((i for i in range(j,len(A)) if A[i][col]),None)
        if row is None:continue
        A[j],A[row]=A[row],A[j]
        pivot=A[j][col]
        inv=1/pivot if p is None else pow(pivot,-1,p)
        A[j]=[x*inv if p is None else x*inv%p for x in A[j]]
        for i in range(len(A)):
            if i==j or not A[i][col]:continue
            fac=A[i][col]
            A[i]=[(x-fac*y if p is None else (x-fac*y)%p)
                  for x,y in zip(A[i],A[j])]
            updates+=n+1
        pivots.append(col)
    inconsistent=any(not any(row[:-1]) and row[-1] for row in A)
    return A,pivots,inconsistent,updates

def rational_boolean_solver(edges,n):
    A,pivots,bad,updates=rref(edges,n)
    free=[j for j in range(n) if j not in pivots]
    if bad:return dict(status='UNSAT',rank=len(pivots),k=len(free),
                       patterns=0,updates=updates)
    for count,bits in enumerate(product((0,1),repeat=len(free)),1):
        x=[None]*n
        for j,b in zip(free,bits):x[j]=Fraction(b)
        for row,j in zip(A,pivots):
            x[j]=row[-1]-sum(row[k]*x[k] for k in free)
        if all(v in (0,1) for v in x) and all(sum(x[j] for j in e)==1 for e in edges):
            return dict(status='SAT',rank=len(pivots),k=len(free),
                        patterns=count,updates=updates)
    return dict(status='UNSAT',rank=len(pivots),k=len(free),
                patterns=1<<len(free),updates=updates)

def copied_system_stats(edges):
    by_orig={};rows=[];binary=[];n=0
    for e in edges:
        vv=[]
        for orig in e:
            n+=1;vv.append(n);by_orig.setdefault(orig,[]).append(n)
        rows.append(vv)
        binary.extend([(-a,-b) for a,b in combinations(vv,2)])
    for copies in by_orig.values():
        for v in copies[1:]:
            binary.extend([(copies[0],-v),(-copies[0],v)])
    # XOR rows disjoint, each has a local odd-parity witness.
    # Binary clauses are separately SAT on the all-zero witness.
    # Pairwise equivalence clauses identify copies and justify quotient.
    return dict(copies=n,xor_rows=len(rows),binary_clauses=len(binary),
                quotient_variables=len(by_orig))

def audit(edges,n):
    oracle=bool(sat_models(edges,n))
    exact=rational_boolean_solver(edges,n)
    assert (exact['status']=='SAT')==oracle
    fields={str(p):not rref(edges,n,p)[2] for p in (2,3,5,7,11,13,17,19,23)}
    # Every Boolean solution satisfies all modular linear relaxations.
    if oracle:assert all(fields.values())
    return dict(oracle='SAT' if oracle else 'UNSAT',rational=exact,
                fields=fields,copied=copied_system_stats(edges))

def main():
    integer_witness=(-1,1,1,1,-1,3)
    assert all(sum(integer_witness[v] for v in e)==1 for e in BLIND)
    families={}
    for name,edges,n in [('blind',BLIND,6),('fano',FANO,7)]:
        root=audit(edges,n)
        assert root['oracle']=='UNSAT'
        neighbor_counts=[len(sat_models(edges[:i]+edges[i+1:],n))
                         for i in range(len(edges))]
        assert all(neighbor_counts)
        families[name]=dict(root=root,deletion_neighbor_counts=neighbor_counts)
    assert all(families['blind']['root']['fields'].values())
    assert not families['fano']['root']['fields']['3']
    rng=Random(20261123);random_tests=0;random_unsat=0
    for n in range(4,9):
        pool=list(combinations(range(n),3))
        for _ in range(20):
            E=tuple(rng.sample(pool,rng.randrange(1,min(len(pool),n+7)+1)))
            result=audit(E,n)
            random_tests+=1
            random_unsat+=result['oracle']=='UNSAT'
    print(json.dumps(dict(status='PASS',families=families,
                          integer_witness=integer_witness,
                          random_tests=random_tests,
                          random_unsat=random_unsat),indent=2))

if __name__=='__main__':main()
