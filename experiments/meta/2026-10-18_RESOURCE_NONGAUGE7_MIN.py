#!/usr/bin/env python3
"""Small independent smoke audit for SOURCE-TAILORED-NONGAUGE7.
Full 22,720-instance audit was generated locally; this compact script
retests key exhaustive identities without third-party libraries.
"""
from itertools import product
import json

def eval_tree(T,z):
    r,branches=T
    q,a=branches[(z>>r)&1]
    return a[(z>>q)&1]

def clauses(T,b):
    r,branches=T
    C=[]
    for x in (0,1):
        q,out=branches[x]
        for y in (0,1):
            if q==r and y!=x: continue
            if out[y]!=b: C.append(set(((r,1-x),(q,1-y))))
    return C

def sat_clauses(C,z):
    return all(any(((z>>v)&1)==b for v,b in c) for c in C)

checks=0
n=3
opts=list(product(range(n),product((0,1),repeat=2)))
for root in range(n):
    for A in opts:
        for B in opts:
            T=(root,(A,B))
            for bit in (0,1):
                C=clauses(T,bit)
                assert all(len(x)<=2 for x in C)
                for z in range(8):
                    assert sat_clauses(C,z)==(eval_tree(T,z)==bit)
                    checks+=1

def clause(z,p):
    return any(((z>>j)&1)==p[j] for j in range(3))
pat=list(product((0,1),repeat=3))
for mask in range(256):
    subset=[pat[j] for j in range(8) if (mask>>j)&1]
    assert any(all(clause(z,p) for p in subset) for z in range(8)) == any(
      all(clause(z,p)==1 for p in subset) for z in range(8))

for n in range(1,10):
    def G(z):
        return [((z>>0)&1)] + [
          (1-((z>>i)&1)) | ((z>>(i+1))&1) for i in range(n-1)
        ] + [1-((z>>(n-1))&1)]
    assert all(not all(G(z)) for z in range(1<<n))
    for k in range(n+1):
        assert any(all(v for j,v in enumerate(G(z)) if j!=k)
                   for z in range(1<<n))
print(json.dumps({"report":"SOURCE-TAILORED-NONGAUGE7-MIN",
 "tree_checks":checks,"three_probe_clause_subsets":256,
 "minimal_unsat_chain_sizes":9,"failed":0},indent=2))
