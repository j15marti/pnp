#!/usr/bin/env python3
"""M22-OVERLAP-BARRIER143: exact six-variable census and seeded independent
uniform signed-degree-two 3-uniform hypergraph samples. Stdlib only.
No SAT runtime lower bound or physical FLMV resource trace is claimed.
Usage: python 2026-10-24_1439_M22_OVERLAP143_minirepro.py
"""
import argparse
import collections
import itertools
import json
import math
import random

SEED=202610241445

def hypergraphs_six():
    triples=list(itertools.combinations(range(1,7),3))
    return [tuple(t) for t in itertools.combinations(triples,4)
            if all(sum(v in edge for edge in t)==2 for v in range(1,7))]

def sat(p,q,k):
    for assignment in itertools.product((0,1),repeat=k):
        if (all(any(assignment[x-1] for x in t) for t in p) and
            all(any(not assignment[x-1] for x in t) for t in q)):
            return True
    return False

def uniform_degree_two(k,rng):
    assert k>=6 and k%3==0
    stubs=list(range(1,k+1))*2
    tries=0
    while True:
        tries+=1
        rng.shuffle(stubs)
        edges=tuple(tuple(sorted(stubs[j:j+3])) for j in range(0,2*k,3))
        if len(set(edges))==len(edges) and all(len(set(e))==3 for e in edges):
            return frozenset(edges),tries

def theory(k):
    h=2*k//3
    delta=2/3-math.log(2,3)
    e=8*k/(3*(k-1)*(k-2))
    return dict(expected_overlap=e,max_q=h,
                bound_not_max_q=min(1,e),
                bound_branch_better=min(1,e/(delta*k)))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--samples",type=int,default=400)
    parser.add_argument("--sizes",default="12,18,30,60,120")
    args=parser.parse_args()
    H=hypergraphs_six()
    assert len(H)==75
    freq=collections.Counter()
    labels=collections.Counter()
    for p in H:
        for q in H:
            defect=4-len(set(p)&set(q))
            freq[defect]+=1
            is_sat=sat(p,q,6)
            labels["SAT" if is_sat else "UNSAT"]+=1
            assert is_sat
    assert freq=={0:75,2:1260,3:1680,4:2610}
    P={(1,2,3),(1,4,5),(2,4,6),(3,5,6)}
    Q={(1,2,4),(1,3,6),(2,3,5),(4,5,6)}
    assert P in [set(a) for a in H] and Q in [set(a) for a in H]
    models=sum(all(any(b[x-1] for x in t) for t in P) and
               all(any(not b[x-1] for x in t) for t in Q)
               for b in itertools.product((0,1),repeat=6))
    assert models==20
    rng=random.Random(SEED)
    results=[]
    for k in [int(v) for v in args.sizes.split(",")]:
        hist=collections.Counter()
        total_trials=0
        for _ in range(args.samples):
            p,a=uniform_degree_two(k,rng)
            q,b=uniform_degree_two(k,rng)
            total_trials+=a+b
            hist[len(p&q)]+=1
        better=sum(z for h,z in hist.items() if 3**(2*k//3-h)<2**k)
        results.append(dict(k=k,pairs=args.samples,
                            overlap_hist=dict(sorted(hist.items())),
                            mean_overlap=sum(h*z for h,z in hist.items())/args.samples,
                            max_q_fraction=hist[0]/args.samples,
                            factor_branch_better_fraction=better/args.samples,
                            configuration_trials=total_trials,
                            theory=theory(k)))
    out=dict(id="M22-OVERLAP-BARRIER143",seed=SEED,
             exact_six=dict(systems=len(H),pairs=75*75,
                            q_hist=dict(sorted(freq.items())),
                            labels=dict(labels),Y_models=models,
                            in_target_pairs=5550,mean_overlap=0.8),
             random=results,
             status="COMPUTATIONAL controls; exact probability theorem proved separately; P-vs-NP and ARC OPEN")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
