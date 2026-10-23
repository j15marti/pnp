#!/usr/bin/env python3
"""SWAPQUARTET71 independent stdlib quickcheck.
Run: python research/agents/lspv-3/2026-10-24_0224_SWAPQUARTET71_quickcheck.py
The general proper-3CNF cube allows duplicate clauses after sign swaps;
do not silently treat those neighbors as strict unique-clause exact-(2,2).
"""
from itertools import product, combinations

def sat(formula, n):
    return any(all(any(((mask >> (abs(l)-1) & 1) == (l > 0))
                       for l in clause) for clause in formula)
               for mask in range(1 << n))

def conditioned(rest, n, x, val, disjunction):
    return any(((mask >> (x-1)) & 1) == val
               and any(((mask >> (abs(l)-1)) & 1) == (l > 0)
                       for l in disjunction)
               and all(any(((mask >> (abs(l)-1)) & 1) == (l > 0)
                           for l in clause) for clause in rest)
               for mask in range(1 << n))

def check():
    cube=[[(-i if sign else i) for i,sign in enumerate(bits,1)]
          for bits in product((0,1),repeat=3)]
    assert len(cube)==8 and not sat(cube,3)
    queries=0
    lower_bound=0
    sensitive_total=0
    for x in (1,2,3):
        positive=[j for j,c in enumerate(cube) if x in c]
        negative=[j for j,c in enumerate(cube) if -x in c]
        edges=set()
        for i in positive:
            for j in negative:
                rest=[c for t,c in enumerate(cube) if t not in (i,j)]
                A=[lit for lit in cube[i] if lit!=x]
                B=[lit for lit in cube[j] if lit!=-x]
                q1B=conditioned(rest,3,x,1,B)
                q0A=conditioned(rest,3,x,0,A)
                q1A=conditioned(rest,3,x,1,A)
                q0B=conditioned(rest,3,x,0,B)
                neighbor=[c[:] for c in cube]
                neighbor[i]=[-x if lit==x else lit for lit in cube[i]]
                neighbor[j]=[x if lit==-x else lit for lit in cube[j]]
                assert sat(cube,3)==(q1B or q0A)
                assert sat(neighbor,3)==(q1A or q0B)
                queries+=1
                if sat(neighbor,3)!=sat(cube,3):
                    edges.add((i,j))
        assert len(edges)==12
        sensitive_total+=len(edges)
        positions=[('P',i) for i in positive]+[('M',j) for j in negative]
        cover=None
        for size in range(len(positions)+1):
            if any(all(('P',i) in subset or ('M',j) in subset for i,j in edges)
                   for subset in map(set,combinations(positions,size))):
                cover=size;break
        assert cover==4
        lower_bound+=cover
    assert queries==48 and sensitive_total==36 and lower_bound==12
    print({'tested_swaps':queries,'opposite_label_swaps':sensitive_total,
           'exact_root_sign_read_bound':lower_bound,'failures':0})

if __name__=="__main__":
    check()
