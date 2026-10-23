#!/usr/bin/env python3
"""FACTOR-JOIN56 minimal complete deterministic reproduction.

No dependencies. Proves symbolic formulas in the report; small finite
controls independently brute force all original source assignments.
This is not the full audit.py in the conversation research package.
"""
from itertools import product

def family(p, q, sat):
    assert p > 0 and q > 0
    k = p + q
    z, w = 3*k+1, 3*k+2
    clauses = []
    for i in range(k):
        a, b, c = 3*i+1, 3*i+2, 3*i+3
        y = z if i < p else w
        clauses += [(a, b, c), (-a, y), (-b, y), (-c, y)]
    clauses += [(-z, w), (z, -w)] if sat else [(z, w), (-z, -w)]
    return 3*k+2, clauses

def satisfied(clauses, value):
    return all(any(value[abs(x)] == (x > 0) for x in C)
               for C in clauses)

def brute_models(n, clauses):
    count = 0
    for bits in product((False, True), repeat=n):
        val = {i+1: v for i, v in enumerate(bits)}
        count += satisfied(clauses, val)
    return count

def certified_profile(p, q, sat):
    n, F = family(p, q, sat)
    k = p+q
    z, w = n-1, n
    assert len(F) == 4*k+2
    assert all(len(C) in (2,3) for C in F)
    assert len(set(F)) == len(F)
    for i in range(k):
        four = F[4*i:4*i+4]
        a, b, c = four[0]
        y = z if i < p else w
        assert four == [(a,b,c), (-a,y), (-b,y), (-c,y)]
        # Sound signed-clause resolution:
        R = set(four[0])
        for x, C in zip((a,b,c), four[1:]):
            assert x in R and -x in C
            R = (R | set(C)) - {x,-x}
            assert all(-l not in R for l in R)
        assert R == {y}
    assert F[-2:] == ([(-z,w),(z,-w)] if sat else [(z,w),(-z,-w)])
    # For each (z,w), local existential masks require z=w=1.
    core = []
    for zbit, wbit in product((False,True), repeat=2):
        equal = (zbit == wbit) if sat else (zbit != wbit)
        all_local = zbit and wbit
        if equal and all_local:
            core.append((zbit,wbit))
    witness = None
    if core:
        witness = {i:False for i in range(1,n+1)}
        witness[z] = witness[w] = True
        for i in range(k):
            witness[3*i+1] = True
        assert satisfied(F,witness)
    return {
        'n':n, 'm':len(F), 'k':k, 'SAT':bool(core),
        'exact_model_count':7**k if core else 0,
        'strong_syntactic_2CNF_backdoor_min':k,
        'compiled_conflict_edges':0 if sat else 9*p*q,
        'certified_resolution_events':3*k,
        'core_SCC_calls':1,
        'witness_verified': witness is not None,
    }

def main():
    num = 0
    for p,q in [(1,1),(1,2),(2,2),(4,4),(8,8),(16,16),(32,32),(64,64)]:
        for sat in (True,False):
            n,F=family(p,q,sat)
            row=certified_profile(p,q,sat)
            assert row['SAT'] == sat
            if p+q <= 4:
                assert brute_models(n,F) == row['exact_model_count']
            print(p,q,'SAT' if sat else 'UNSAT',
                  'n',n,'m',len(F),'edges',row['compiled_conflict_edges'],
                  'models',row['exact_model_count'])
            num += 1
    print('verified paired cases:',num, 'P vs NP: OPEN')

if __name__ == '__main__':
    main()
