#!/usr/bin/env python3
"""Independent finite and FLMV checks for LSPV-4 ARC-EXPONENT-SELECTOR263.
Reads immutable producer raw JSON, independently enumerates original clauses
and all four S/U clause-pair modes. No nonstdlib dependencies.
"""
import itertools, json, sys
from fractions import Fraction as Q

def sat(cnf, a):
    return all(any(a[abs(l)-1] == (l > 0) for l in clause) for clause in cnf)

def tcount(clause, a):
    return sum(a[abs(l)-1] == (l > 0) for l in clause)

def exact_modes(c, d):
    out = {}
    variables = sorted({abs(l) for l in c+d})
    for p, q in itertools.product(('S','U'), repeat=2):
        out[p+q] = False
        for bits in itertools.product((False,True), repeat=len(variables)):
            a = dict(zip(variables,bits))
            tc=sum(a[abs(l)] == (l>0) for l in c)
            td=sum(a[abs(l)] == (l>0) for l in d)
            if tc == (len(c) if p=='S' else 0) and td == (len(d) if q=='S' else 0):
                out[p+q] = True
                break
    return out

def curve(c):
    f=Q(1); best=(-1,None)
    for k in range(1,200):
        f=c*f/(1+f)
        d=min((1/f-c)/k,c**(-k))
        if d > best[0]: best=(d,k)
        if k>=3 and c**(-k-1) < best[0]: return best
    raise ValueError("No certified infinite-tail cutoff")

def test(raw):
    assert curve(Q(6,5)) == (Q(23,45),2)
    assert curve(Q(241,200)) == (Q(11642479,23232400),2)
    checks=0
    for obj in raw['formulae']:
        F=obj['clauses']; n=obj['n']; models=0
        for bits in itertools.product((False,True),repeat=n):
            ts=[tcount(c,bits) for c in F]
            b=tuple(not v for v in bits)
            for j,c in enumerate(F):
                assert ts[j]+tcount(c,b)==3
                checks+=1
            models+=int(all(v>0 for v in ts))
        assert models == obj['models']
        checks+=1
        for p in obj['pair_compatibility']:
            i,j=p['clause_indices']
            assert p['modes']==exact_modes(F[i-1],F[j-1])
            checks+=4
        d=obj['baseline_dpll']
        assert d['sat'] == (models>0)
        if d['witness'] is not None:
            assert sat(F,tuple(bool(b) for b in d['witness']))
        checks+=1
        for c in obj['targets']:
            for o in c['occurrences']:
                assert o['S'] == o['invert_U'] and o['U'] == o['invert_S']
                checks+=1
    halts=[(x['n'],x['halted']) for x in raw['profiles'] if x['name']=='HALT_40']
    assert (32,False) in halts and (64,True) in halts
    assert all(not x['halted'] for x in raw['profiles'] if x['name']=='LOOP')
    return {'checks':checks,'flmv':'passed, including certified tail','all_original_labels':'passed','source_paired':'passed','late_wrapper':'passed'}

if __name__ == '__main__':
    with open(sys.argv[1],encoding='utf-8') as f: data=json.load(f)
    print(json.dumps(test(data),indent=2))
