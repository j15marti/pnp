#!/usr/bin/env python3
"""ARC212: bounded-degree grid monotone-2CNF residual audit and rank ledgers.

No third-party dependencies. All exhaustive regimes are explicitly bounded.
The asymptotic theorem is proved separately; this program is a finite control.
"""
from __future__ import annotations
import itertools
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

SEED = 2121028


def grid_edges(side):
    return tuple(sorted((i, j) for r in range(side) for c in range(side)
                        for i, j in [(r*side+c, r*side+c+1)] if c+1 < side)) + tuple(
                            sorted((i, j) for r in range(side) for c in range(side)
                            for i, j in [(r*side+c, (r+1)*side+c)] if r+1 < side))


def neighbors(n, edges):
    a = [set() for _ in range(n)]
    for u,v in edges:
        a[u].add(v);a[v].add(u)
    return a


def cross_edges(edges, left):
    return [(u,v) if u in left else (v,u) for u,v in edges if (u in left)!=(v in left)]


def full_induced_matching(n, edges, left):
    neigh=neighbors(n,edges)
    available=cross_edges(edges,left)
    picked=[]
    while available:
        u,v=available[0]
        picked.append((u,v))
        near={u,v}|neigh[u]|neigh[v]
        available=[(a,b) for a,b in available if a not in near and b not in near]
    chosen=[w for p in picked for w in p]
    assert len(chosen)==len(set(chosen))
    for i,(u,v) in enumerate(picked):
        assert v in neigh[u]
        for j,(a,b) in enumerate(picked):
            if i!=j:
                assert a not in neigh[u] and b not in neigh[u]
                assert a not in neigh[v] and b not in neigh[v]
    return picked


def partial_residual(n,edges,left,zeros):
    assert zeros <= left
    # Once a full clause in the prefix is false, the residual is constant false.
    for u,v in edges:
        if u in zeros and v in zeros:
            return ("FALSE",)
    right_right = tuple(sorted((u,v) for u,v in edges if u not in left and v not in left))
    units=tuple(sorted({v if u in zeros else u for u,v in edges
                        if (u in zeros and v not in left) or (v in zeros and u not in left)}))
    return (right_right,units)


def eval_residual(residual,truevars, right):
    if residual==("FALSE",):
        return False
    rr,units=residual
    return all(v in truevars for v in units) and all(u in truevars or v in truevars for u,v in rr)


def semantic_witnesses(n,edges,left,picked,verify_truth_table=False):
    assert all(u in left and v not in left for u,v in picked)
    q=len(picked)
    lhs=[u for u,v in picked]
    rhs=[v for u,v in picked]
    assert len(lhs)==len(set(lhs))
    signatures={}
    tested_flags=list(itertools.product((0,1),repeat=min(q,6)))
    tested_flags=[tuple(f)+(0,)*(q-len(f)) for f in tested_flags]
    tested_flags += [tuple(1 if j==i else 0 for j in range(q)) for i in range(q)]
    tested_flags=list(dict.fromkeys(tested_flags))
    for flags in tested_flags:
        zeros={u for u,bit in zip(lhs,flags) if bit}
        res=partial_residual(n,edges,left,zeros)
        assert res != ("FALSE",)
        sig=res[1]
        assert sig not in signatures, (n,left,picked,sig)
        signatures[sig]=flags
    # Each bit vector gives a distinct residual function, not merely a distinct encoding.
    # For any differing flags, one right matching vertex detects the difference.
    for f,g in itertools.combinations(signatures.values(),2):
        i=next(i for i in range(q) if f[i]!=g[i])
        zf={u for u,bit in zip(lhs,f) if bit}
        zg={u for u,bit in zip(lhs,g) if bit}
        rf=partial_residual(n,edges,left,zf)
        rg=partial_residual(n,edges,left,zg)
        truevars=set(range(n))-left-{rhs[i]}
        assert eval_residual(rf,truevars,set(range(n))-left) != eval_residual(rg,truevars,set(range(n))-left)
    # Additional independent exhaustive extensional check in the small regime.
    if verify_truth_table:
        right=sorted(set(range(n))-left)
        truth=[]
        for f in tested_flags:
            zeros={u for u,bit in zip(lhs,f) if bit}
            r=partial_residual(n,edges,left,zeros)
            signature=tuple(eval_residual(r,{v for v,b in zip(right,bs) if b},set(right))
                            for bs in itertools.product((0,1),repeat=len(right)))
            truth.append(signature)
        assert len(set(truth)) == len(tested_flags)
    return len(tested_flags)


def sample_splits(side,seed,limit=24):
    n=side*side
    rng=random.Random(seed+side)
    sets=[]
    for order in [list(range(n)),[r*side+c for c in range(side) for r in range(side)],
                  [r*side+(c if r%2==0 else side-1-c) for r in range(side) for c in range(side)]]:
        sets.append(frozenset(order[:n//2]))
    for _ in range(limit):
        order=list(range(n));rng.shuffle(order)
        sets.append(frozenset(order[:n//2]))
    return sorted(set(sets),key=lambda x:tuple(sorted(x)))


def audit_side(side):
    n=side*side
    assert side%2==0
    ed=grid_edges(side)
    assert len(ed)==2*side*(side-1)
    deg=Counter(v for e in ed for v in e)
    assert max(deg.values())<=4
    minimum_cross=None
    balanced_cuts=0
    if side<=4:
        iterator=itertools.combinations(range(n),n//2)
        total_expected=math.comb(n,n//2)
    else:
        iterator=sample_splits(side,SEED)
        total_expected=None
    for verts in iterator:
        left=set(verts)
        crossing=len(cross_edges(ed,left))
        minimum_cross=crossing if minimum_cross is None else min(minimum_cross,crossing)
        assert crossing>=side//2
        balanced_cuts+=1
    if total_expected is not None:
        assert balanced_cuts==total_expected
    samples=sample_splits(side,SEED)
    sample_data=[]
    for sample in samples:
        left=set(sample)
        picked=full_induced_matching(n,ed,left)
        cross=len(cross_edges(ed,left))
        assert len(picked)*32>=cross
        # Separate extensional check for tiny 4x4 cases, on 6 sampled cuts.
        full_sem=side<=4 and len(sample_data)<6
        cnt=semantic_witnesses(n,ed,left,picked,full_sem)
        sample_data.append({"cross":cross,"induced_matching":len(picked),"tested_distinct_residuals":cnt,"theoretical_residual_lower":2**len(picked),"full_truth_table_checked":full_sem})
    # An all-one SAT model is independent of the encoded graph and its width.
    sat_witness={i for i in range(n)}
    assert all(u in sat_witness or v in sat_witness for u,v in ed)
    return {"L":side,"variables":n,"clauses":len(ed),"balanced_cuts_tested":balanced_cuts,
            "minimum_crossing_edges":minimum_cross,"sample_cuts":len(sample_data),
            "min_sampled_induced_matching":min(d["induced_matching"] for d in sample_data),
            "max_sampled_induced_matching":max(d["induced_matching"] for d in sample_data),
            "full_extensional_checks":sum(d["full_truth_table_checked"] for d in sample_data),
            "monotone_2sat_all_one_witness":True,"sample_details":sample_data[:6]}


def rank_controls():
    data=[]
    for n in [4,8,12,16,20]:
        rank=1<<n
        assert rank.bit_length()<=n+1
        assert rank>n**2 if n>=8 else True
        data.append({"input_bits":n,"rank_value":rank,"rank_bit_length":rank.bit_length(),"single_step_decrement_iterations":rank,
                     "polynomial_value_example":n*n,"poly_value_iterations_ceiling":n*n})
    return data


def main():
    sides=(2,4,6,8,12)
    results=[audit_side(s) for s in sides]
    report={"run_id":"ARC212_GRID_RESIDUAL_RANK","seed":SEED,"sampling":"exact all balanced cuts L<=4, deterministic 27 random/structured cuts for larger sizes", 
            "mathematical_claim":"grid F_G monotone 2CNF requires >=2^(L/64) residual functions at a balanced cut for every order; graph supports easy all-one witness",
            "proof_status":"restricted exact mathematical argument separately supplied; finite assertions computational",
            "grid":results,"rank_counterexample":rank_controls(),"assumptions_and_caveats":[
                "Full 2^n SAT graph assignment decision not hard; all ones satisfies F_G.",
                "Residual lower bound concerns fixed-order exact Boolean function/OBDD evaluation, not SAT decision.",
                "Monotone 2CNF grid is not the strict signed exact-(2,2)-3CNF source language.",
                "Only polynomial VALUE rank bounds iterations; bit length alone does not.",
                "No comparison of Turing-machine and indexed-RAM numerical lower-bound exponents is made."]}
    p=Path(__file__).with_name('2026-10-28_2100_ARC212_grid_semantic_rank_raw.json')
    p.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"status":"PASS","sides":sides,"balanced_cut_checks":sum(x['balanced_cuts_tested'] for x in results),
                      "sampled_interface_checks":sum(x['sample_cuts'] for x in results),
                      "exhaustive_residual_truth_table_checks":sum(x['full_extensional_checks'] for x in results),
                      "rank_checks":len(report['rank_counterexample']),"raw":str(p)},sort_keys=True))

if __name__=="__main__":
    main()