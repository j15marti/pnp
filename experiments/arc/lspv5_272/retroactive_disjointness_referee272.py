#!/usr/bin/env python3
"""Decision-only red team for retroactive contexts on canonical G_(2t).

The proved lower bound is only for the declared promised pin-bit query model.
It is linear and has a matching exact algorithm; it is not SAT hardness.
"""
from __future__ import annotations

import argparse
import collections
import functools
import itertools
import json
from pathlib import Path

F9 = (
    (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9),
)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)

PINS={"A":{5:1},"B":{5:1,4:0,6:0},"Q":{1:0,5:0,6:0},"Z":{}}
EXPECTED={
    "A":((0,0),(23,36)),
    "B":((0,0),(0,3)),
    "Q":((0,13),(0,0)),
    "Z":((34,47),(23,36)),
}

def sat(formula, assignment):
    return all(any(assignment[abs(x)] == int(x > 0) for x in c) for c in formula)

def grammar(formula,n=None):
    try:
        if not formula:return False
        n=n or max(abs(x) for c in formula for x in c)
        if n%3 or 3*len(formula)!=4*n:return False
        seen=set();occ=collections.Counter()
        for c in formula:
            if len(c)!=3 or len({abs(x) for x in c})!=3:return False
            if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
            key=tuple(sorted(c))
            if key in seen:return False
            seen.add(key);occ.update(c)
        return all(occ[v]==occ[-v]==2 for v in range(1,n+1))
    except Exception:return False

def build(blocks):
    out=[]
    for i in range(blocks):
        off=9*i; nxt=9*((i+1)%blocks)+5
        for j,c in enumerate(F9):
            cc=[]
            for x in c:
                v=abs(x)+off
                if j==0 and x==5:v=nxt
                cc.append(v if x>0 else -v)
            out.append(tuple(cc))
    return tuple(out)

def local_matrix(pins):
    ans=[[0,0],[0,0]]
    for left,right in itertools.product((0,1),repeat=2):
        if 5 in pins and pins[5]!=left:continue
        free=[v for v in range(1,10) if v!=5 and v not in pins]
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(pins);a.update(zip(free,bits));a[5]=left
            ok=True
            for j,c in enumerate(F9):
                if not any((right if j==0 and x==5 else a[abs(x)])==int(x>0) for x in c):
                    ok=False;break
            ans[left][right]+=ok
    return tuple(map(tuple,ans))

def mm(A,B):
    return tuple(tuple(sum(A[i][h]*B[h][j] for h in (0,1)) for j in (0,1)) for i in (0,1))

def direct_count(formula,pins):
    n=max(abs(x) for c in formula for x in c)
    free=[v for v in range(1,n+1) if v not in pins]
    count=0;first=None;leaves=[]
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits))
        false=[j for j,c in enumerate(formula) if not any(a[abs(x)]==int(x>0) for x in c)]
        if not false:
            count+=1
            if first is None:first=[a[v] for v in range(1,n+1)]
        else:leaves.append(false[0])
    return count,first,leaves

def block_pins(beta,sigma):
    pins={}
    for i,(b,s) in enumerate(zip(beta,sigma)):
        odd=18*i;even=odd+9
        for v,x in PINS["B" if b else "A"].items():pins[odd+v]=x
        for v,x in PINS["Q" if s else "Z"].items():pins[even+v]=x
    return pins

def disj(bits):
    t=len(bits)//2
    return int(all(not(bits[2*i] and bits[2*i+1]) for i in range(t)))

def exact_depth(t):
    """Brute-force optimal deterministic decision-tree depth for DISJ_t."""
    n=2*t
    @functools.lru_cache(None)
    def solve(state):
        vals=[]
        unknown=[i for i,x in enumerate(state) if x<0]
        for fill in itertools.product((0,1),repeat=len(unknown)):
            z=list(state)
            for i,b in zip(unknown,fill):z[i]=b
            vals.append(disj(z))
            if len(set(vals))==2:break
        if len(set(vals))<=1:return 0
        best=n+1
        for i in unknown:
            worst=0
            for b in (0,1):
                z=list(state);z[i]=b
                worst=max(worst,solve(tuple(z)))
            best=min(best,1+worst)
        return best
    return solve((-1,)*n),solve.cache_info().currsize

def adversary_force(t,order):
    """Answer first query in each pair 1 and its mate 0."""
    seen=[0]*t;ans={}
    for q in order:
        i=q//2
        ans[q]=1 if seen[i]==0 else 0
        seen[i]+=1
        # Until both bits of every pair are read, label is not forced.
        if any(x<2 for x in seen):
            assert any(x<2 for x in seen)
    assert len(ans)==2*t and disj([ans[i] for i in range(2*t)])==1
    return ans

def su_modes(formula):
    n=max(abs(x) for c in formula for x in c);checks=0
    for A,B in itertools.combinations(formula,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        want=(not opp,not same,not same,not opp);got=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A);AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B);BU=all(a[abs(x)]!=int(x>0) for x in B)
            got=[p or q for p,q in zip(got,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(got)==want;checks+=4
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert grammar(F9,9) and grammar(Y6,6) and grammar(F15,15)
    mats={k:local_matrix(v) for k,v in PINS.items()}
    assert mats==EXPECTED
    theta={(b,s):(mm(EXPECTED[b],EXPECTED[s])[0][0]+mm(EXPECTED[b],EXPECTED[s])[1][1]) for b in "AB" for s in ("Z","Q")}
    assert theta=={("A","Z"):2377,("A","Q"):299,("B","Z"):108,("B","Q"):0}

    g2=build(2);assert grammar(g2,18)
    g2_counts={}
    cert={}
    for b,s in ((0,0),(1,0),(0,1),(1,1)):
        c,w,l=direct_count(g2,block_pins((b,),(s,)))
        g2_counts[f"{b}{s}"]=c
        if (b,s)==(0,1):cert["AQ_witness"]=w
        if (b,s)==(1,1):cert["BQ_leaf_count"]=len(l);cert["BQ_leaf_histogram"]=dict(collections.Counter(l))
    assert g2_counts=={"00":2377,"10":108,"01":299,"11":0}

    # Verify factorization on every joint context through t=3.
    exhaustive=[]
    for t in range(1,4):
        F=build(2*t);assert grammar(F,18*t)
        for beta in itertools.product((0,1),repeat=t):
            for sigma in itertools.product((0,1),repeat=t):
                pred=1
                for b,s in zip(beta,sigma):pred*=theta[("B" if b else "A","Q" if s else "Z")]
                if t<=1:
                    got=direct_count(F,block_pins(beta,sigma))[0]
                    assert got==pred
                assert (pred>0)==bool(disj(tuple(x for pair in zip(beta,sigma) for x in pair)))
        exhaustive.append({"t":t,"contexts":4**t,"direct_original_enumeration":t<=1})

    depths=[]
    for t in range(1,6):
        d,states=exact_depth(t);assert d==2*t
        depths.append({"t":t,"optimal_exact_depth":d,"partial_states":states})
        for order in (list(range(2*t)),list(reversed(range(2*t)))):
            adversary_force(t,order)

    controls={
        "Y6_models":direct_count(Y6,{})[0],"F9_models":direct_count(F9,{})[0],
        "F9_SU_pair_modes":su_modes(F9),
        "F15_SAT_models":direct_count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0))))[0],
        "F15_UNSAT_models":direct_count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))[0],
    }
    assert controls=={"Y6_models":20,"F9_models":70,"F9_SU_pair_modes":264,"F15_SAT_models":2,"F15_UNSAT_models":0}
    malformed=[(),((1,1,2),),((1,-2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed);controls["malformed_rejected"]=len(malformed)

    out={
      "run":"RETROACTIVE_DISJOINTNESS_REFEREE272","timestamp_PST":"2026-11-01 12:48",
      "status":"PROVED/EXACT restricted decision-query theorem plus COMPUTATIONAL controls",
      "P_vs_NP":"OPEN",
      "theorem":{
        "quantifiers":"for every t>=1, on the promised 2t independent A/B and Z/Q indicator bits of the same canonical G_(2t) original",
        "function":"SAT iff DISJ_t(beta,sigma)=AND_i NOT(beta_i AND sigma_i)",
        "deterministic_exact_query_complexity":"exactly 2t",
        "lower_bound":"adversary answers the first queried bit of every pair 1 and its mate 0; every pair must be completed before the accepting label is forced",
        "upper_bound":"query both promised indicator bits in every pair and reject on 11",
        "scope":"promised pin-slot bit-query model; not arbitrary-machine time and not untouched-original language hardness"
      },
      "three_regimes":{"current_beta_only_queries":0,"fixed_all_Q_queries": "t", "joint_beta_sigma_queries":"2t"},
      "matrices":{k:[list(r) for r in v] for k,v in mats.items()},"theta":{b+s:v for (b,s),v in theta.items()},
      "G2_counts":g2_counts,"G2_certificates":cert,"exhaustive_controls":exhaustive,"optimal_depth_checks":depths,"controls":controls,
      "charged_algorithm":"promise authentication + 2t indicator reads + O(t) pair tests + O(log t) index/live counter bits; source grammar and pin-location discovery remain separately charged",
      "charged_recurrence":"W(z)=C_grammar/source/index/head + sum_attempted C_discover/select/switch/failed + C_query/pair/proof/cache/replay + sum_children(C_output/access/guest+W(child)); peak is simultaneous live state",
      "wrappers":{"DELAY":"charged despite zero logical data change","COPY_RECOMP":"charged","logical_XOR":"offline only"},
      "limitations":["2^t continuation classes do not imply exponential work","2t bit queries do not imply linear writable space with indexed rereads","no all-input quotient acquisition theorem","no arbitrary-A ARC","no numerical same-machine FLMV transfer"]
    }
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","depths":depths,"G2_counts":g2_counts,"controls":controls,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__":main()
