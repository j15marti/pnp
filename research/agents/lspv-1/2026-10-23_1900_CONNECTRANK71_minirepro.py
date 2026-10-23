#!/usr/bin/env python3
"""CONNECTRANK71 independent finite verification; Python standard library."""
from itertools import product
from collections import Counter

def source(g):
    C=[]
    for i in range(g):
        x,y,z,zn=i+1,g+i+1,2*g+i+1,2*g+(i+1)%g+1
        C.extend(((x,-y,z),(x,-y,-z),(-x,y,zn),(-x,y,-zn)))
    return C

def holds(clauses, bits):
    return all(any(bits[abs(v)-1] == (v>0) for v in c) for c in clauses)

def rank(rows):
    basis={}
    for v in rows:
        while v:
            h=v.bit_length()-1
            if h in basis: v^=basis[h]
            else: basis[h]=v;break
    return len(basis)

for g in range(1,6):
    clauses=source(g)
    counts=Counter((abs(v),v>0) for c in clauses for v in c)
    assert len(clauses)==4*g
    assert all(counts[(i,p)]==2 for i in range(1,3*g+1) for p in (False,True))
    assert all(len({abs(v) for v in c})==3 for c in clauses)
    count=0
    for bits in product((False,True),repeat=3*g):
        expected=all(bits[i]==bits[g+i] for i in range(g))
        assert holds(clauses,bits)==expected
        count+=expected
    assert count==2**(2*g)
    rows=[]
    for x in product((False,True),repeat=g):
        row=0
        for index,(y,z) in enumerate(product(product((False,True),repeat=g),repeat=2)):
            if x==y: row|=1<<index
        rows.append(row)
    assert rank(rows)==2**g
    print('g=%d n=%d m=%d models=%d GF2_rank=%d'%(g,3*g,4*g,count,2**g))
print('PASS')
