#!/usr/bin/env python3
"""LSPV-1/486: exhaustive affine-cell control, g=1..3.
Enumerate every RREF binary linear subspace and every affine coset.
Independent of historical R_mix341 verifier and any SAT oracle.
"""
from itertools import combinations, product
from collections import Counter
import json, time

def and_gate(x, i):
    return ((x >> (2*i)) & 1) & ((x >> (2*i+1)) & 1)

def rref_bases(n, d):
    for piv in combinations(range(n), d):
        ps = set(piv)
        free = [(i, j) for i in range(d)
                for j in range(piv[i]+1,n) if j not in ps]
        for vals in product((0,1), repeat=len(free)):
            rows = [1 << j for j in piv]
            for (i,j),v in zip(free, vals):
                if v: rows[i] ^= 1 << j
            yield rows, piv

def affine_on_cell(origin, rows, g):
    for i in range(g):
        c = and_gate(origin,i)
        ds = [and_gate(origin^b,i)^c for b in rows]
        for t in range(1<<len(rows)):
            x=origin; predicted=c
            for j,b in enumerate(rows):
                if (t>>j)&1: x^=b; predicted^=ds[j]
            if and_gate(x,i) != predicted: return False
    return True

def check(g):
    n=2*g; totals=Counter(); valid=Counter(); maxdim=-1
    for d in range(n+1):
        for rows,piv in rref_bases(n,d):
            pivot_mask=sum(1<<i for i in piv)
            for origin in range(1<<n):
                if origin & pivot_mask: continue
                totals[d]+=1
                if affine_on_cell(origin,rows,g):
                    valid[d]+=1; maxdim=max(d,maxdim)
                    assert d<=g, (g,d,rows,origin)
    assert maxdim==g
    return {'g':g,'n':n,'all_cosets_by_dimension':dict(totals),
            'valid_cosets_by_dimension':dict(valid),
            'total_cosets':sum(totals.values()),
            'valid_cosets':sum(valid.values()),
            'maximum_valid_dimension':maxdim,
            'full_cube_cover_lower_bound':1<<g,
            'matching_coordinate_partition_cells':1<<g,
            'passed':True}

if __name__=='__main__':
    t=time.perf_counter()
    result={'experiment':'LSPV-1/486 affine-coset exhaustive control',
      'status':'COMPUTATIONAL',
      'results':[check(g) for g in (1,2,3)],
      'elapsed_seconds':round(time.perf_counter()-t,6),
      'scope':'all affine cosets of GF(2)^(2g) for g<=3',
      'not_a_native_R_mix341_checker':True}
    print(json.dumps(result,sort_keys=True,indent=2))
