#!/usr/bin/env python3
"""LSPV-1/626: full-sign guard family and polarity/advice audit (stdlib only).
Execute: python experiments/arc/lspv1_626_guard_cover_correct_path_audit.py
For evidence set an optional first CLI argument to an output JSON path.
"""
import itertools
import json
import random
import sys
from fractions import Fraction as Q

def clause(s, r):
    return tuple(-(i+1) if (s >> i)&1 else (i+1) for i in range(r))

def holds(c, a):
    return any(((a >> (abs(l)-1)) & 1) == int(l>0) for l in c)

def sat(F, a):
    return all(holds(c, a) for c in F)

def mask(c, r):
    assert len(c)==r and set(map(abs,c))==set(range(1,r+1))
    return sum(1 << (abs(l)-1) for l in c if l<0)

def missing_by_xor(F, r):
    out=0
    for s in range(1<<r): out^=s
    for c in F: out^=mask(c,r)
    return out

def audit_exhaustive(r):
    R=1<<r
    maps=1<<R
    deletions=0
    constant=0
    for f in range(maps):
        B=[[],[]]
        for s in range(R): B[(f>>s)&1].append(clause(s,r))
        F=B[0]+B[1]
        assert all(not sat(F,z) for z in range(R))
        for z in range(R):
            assert [j for j in range(2) if not sat(B[j],z)] == [(f>>z)&1]
            G=[clause(s,r) for s in range(R) if s!=z]
            assert missing_by_xor(G,r)==z
            assert sum(sat(G,x) for x in range(R))==1
            assert sat(G,z)
            deletions+=1
        if f==0 or f==maps-1:constant+=1
    return {'r':r,'selector_maps':maps,'checked_critical_deletions':deletions,
            'maps_with_global_fixed_bad_block':constant,
            'maps_without_global_fixed_bad_block':maps-constant}

def audit_sampled(r, samples):
    R=1<<r
    rng=random.Random(20261118+r)
    tested=0
    for _ in range(samples):
        f=rng.getrandbits(R)
        B=[[],[]]
        for s in range(R):B[(f>>s)&1].append(clause(s,r))
        for z in range(R):
            assert [j for j in range(2) if not sat(B[j],z)]==[(f>>z)&1]
            G=[clause(s,r) for s in range(R) if s!=z]
            assert missing_by_xor(G,r)==z
            assert sum(sat(G,x) for x in range(R))==1
            tested+=1
    return {'r':r,'maps_sampled':samples,'checked_deletions':tested,'seed':20261118+r}

def t5_count(E,n):
    return sum(all((a[v]-a[u])%5 in (1,3) for u,v in E)
               for a in itertools.product(range(5),repeat=n))

def co_flmv(c,k):
    g=Q(1)
    for _ in range(k):g=c*c*g/(1+c*g)
    return min((1/g-c)/k,c**(-2*k))

def main():
    c=Q(133,100)
    co=max(((co_flmv(c,k),k) for k in range(1,81)))
    out={
        'status':'PROVED symbolic, COMPUTATIONAL check; unrestricted P/NP OPEN',
        'exhaustive':[audit_exhaustive(r) for r in (1,2,3)],
        'sampled':[audit_sampled(4,512)],
        'T5_counts':{'arc':t5_count([(0,1)],2),
                     'digon':t5_count([(0,1),(1,0)],2),
                     'directed_triangle':t5_count([(0,1),(1,2),(2,0)],3)},
        'source_layout':{'rows_exponent':'.195','blocks_exponent':'.65',
             'child_length_exponent':'.35','calls_exponent':'.845',
             'materialization_exponent':'1.195',
             'max_seed_time_exponent_for_1_33':str((Q(133,100)-Q(845,1000))/Q(35,100)),
             'max_seed_space_exponent_for_half':str(Q(1,2)/Q(35,100))},
        'FLMV_conondeterministic_c133':{'optimal_k_checked':co[1],
                                         'd_exact':str(co[0]),'d_approx':float(co[0])}
    }
    assert out['T5_counts']=={'arc':10,'digon':0,'directed_triangle':15}
    assert out['source_layout']['max_seed_time_exponent_for_1_33']=='97/70'
    result=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as f:f.write(result)
    print(result,end='')

if __name__=='__main__':main()
