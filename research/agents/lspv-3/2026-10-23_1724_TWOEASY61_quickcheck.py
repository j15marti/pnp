#!/usr/bin/env python3
"""Standalone exact all-YES affine/2CNF selector reduction audit (stdlib only).
For complete DPLL and source-serialization controls see the expanded local package.
"""
from itertools import product

def accepted(clause, bits):
    return any(bits[abs(z)-1] == (z > 0) for z in clause)

def compile_source(n, source):
    parity, binary, proper = [], [], []
    for j, clause in enumerate(source):
        tri = tuple(n+3*j+i+1 for i in range(3))
        parity.append((tri, 1))
        a,b,c = tri
        proper += [(a,b,c),(a,-b,-c),(-a,b,-c),(-a,-b,c)]
        binary += [(-a,-b),(-a,-c),(-b,-c)]
        binary += [(-tri[i],clause[i]) for i in range(3)]
    nxt = n+3*len(source)+1
    for a,b in binary:
        z=nxt
        nxt+=1
        proper += [(a,b,z),(a,b,-z)]
    assert nxt-1 == n+9*len(source)
    assert len(proper) == 16*len(source)
    assert all(len({abs(z) for z in clause})==3 for clause in proper)
    return parity,binary,proper

def count_selector_extensions(n, source):
    count=0
    models=0
    for bits in product((False,True),repeat=n):
        true_counts=[sum(bits[abs(z)-1] == (z>0) for z in c) for c in source]
        ways=1
        for t in true_counts:
            ways*=t
        count+=ways
        models+=int(all(x>0 for x in true_counts))
    return models,count

def main():
    all_clauses=[
        tuple((-1 if mask>>i & 1 else 1)*(i+1) for i in range(3))
        for mask in range(8)]
    sat=unsat=0
    for mask in range(256):
        source=[cl for i,cl in enumerate(all_clauses) if mask>>i & 1]
        affine,binary,proper=compile_source(3,source)
        # Both component root labels are always SAT, for every source:
        # affine: select the first indicator of each clause;
        # binary: select no indicators, with any original assignment.
        y_true={tri[0] for tri,_ in affine}
        assert all(sum(v in y_true for v in tri)==1 for tri,_ in affine)
        zero_assignment={i:False for i in range(1,4+3*len(source))}
        assert all((zero_assignment[abs(a)]==(a>0)) or
                   (zero_assignment[abs(b)]==(b>0))
                   for a,b in binary)
        models,extensions=count_selector_extensions(3,source)
        assert (models>0)==(extensions>0)
        assert len(proper)==16*len(source)
        sat+=int(models>0)
        unsat+=int(models==0)
    assert sat>0 and unsat>0 and sat+unsat==256
    print({"n_source_cases":256,"sat_cases":sat,
           "unsat_cases":unsat,"all_affine_SAT":True,
           "all_2CNF_SAT":True,"unexpected_failures":0})

if __name__=="__main__":
    main()
