#!/usr/bin/env python3
"""Independent permutation-bitset audit of exact 5/6-bit SAT certificates.
This does not use Hall matching or the predicted certificate structures to classify.
Each possible UNSAT completion is an eight-row permutation of masks 0..7.
"""
from collections import Counter
from itertools import combinations, permutations
from math import comb
from time import monotonic
import json

CASES = {
    'balanced_even': (0,0,3,3,5,5,6,6),
    'balanced_projection': (0,0,1,1,6,6,7,7),
    'balanced_extreme': (0,0,0,0,7,7,7,7),
    'unbalanced_prior': (1,2,3,4,5,6,7,7),
    'five_equal': (7,7,7,7,7,0,0,0),
    'six_equal': (7,7,7,7,7,7,0,0),
    'all_equal': (7,7,7,7,7,7,7,7),
    'unsat_permutation': (0,1,2,3,4,5,6,7),
}

def counts(a):
    m = Counter(a)
    duplicate = sum(comb(n,2) for n in m.values() if n >= 2)
    projected = 0
    for j,k in combinations(range(3),2):
        pr = Counter(((v>>j)&1, (v>>k)&1) for v in a)
        projected += sum(comb(n,3) for n in pr.values() if n>=3)
    supersets = 0
    five = 0
    for j in range(3):
        for bit in range(2):
            n = sum(((v>>j)&1)==bit for v in a)
            if n>=5:
                five += comb(n,5)
                supersets += comb(n,5)*(24-n)
            if n>=6:
                supersets += comb(n,6)
    return {'c5':five, 'duplicate_pair':duplicate,
            'triple_projection':projected, 'five_cert_extensions':supersets,
            'c6':duplicate+projected+supersets}

def source_query_completion_masks():
    # One bit in these big integers represents one of 8! complete UNSAT permutations.
    permits = [[0,0] for _ in range(24)]
    total = 0
    for idx, perm in enumerate(permutations(range(8))):
        flag = 1 << idx
        for row, mask in enumerate(perm):
            for j in range(3):
                permits[3*row+j][(mask>>j)&1] |= flag
        total += 1
    assert total == 40320
    return permits, (1<<total)-1

def audit(a, permits, all_perms):
    wanted = [permits[p][(a[p//3]>>(p%3))&1] for p in range(24)]
    got = {}
    sample = {}
    for k in (5,6):
        certs = 0
        for Q in combinations(range(24),k):
            good = all_perms
            for p in Q:
                good &= wanted[p]
                if not good:
                    break
            if not good:
                certs += 1
                if str(k) not in sample:
                    sample[str(k)] = list(Q)
        got[f'c{k}'] = certs
    expected = counts(a)
    assert got['c5'] == expected['c5'], (a, got, expected)
    assert got['c6'] == expected['c6'], (a, got, expected)
    return {'tuple':list(a),'expected':expected,'independent_permutation_c5':got['c5'],
            'independent_permutation_c6':got['c6'],'sample_certificates':sample}

def main():
    start = monotonic()
    permits, all_perms = source_query_completion_masks()
    result = {'version':'TMR2-ALL6-013','permutations':40320,
              'method':'independent permutation compatibility bitsets; no Hall/matcher oracle',
              'cases':{},'query_subsets_per_case':{'k5':comb(24,5),'k6':comb(24,6)}}
    for name, a in CASES.items():
        t=monotonic()
        result['cases'][name] = audit(a, permits, all_perms)
        result['cases'][name]['elapsed_seconds'] = round(monotonic()-t,3)
    result['total_query_subsets']=len(CASES)*(comb(24,5)+comb(24,6))
    result['total_failed_assertions'] = 0
    result['elapsed_seconds'] = round(monotonic()-start,3)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
