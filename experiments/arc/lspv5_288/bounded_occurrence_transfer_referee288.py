#!/usr/bin/env python3
"""REFEREE288: paid generic 4-occurrence SAT transfer firewall.

The published Peng--Xiao algorithm is adopted as a black-box theorem.  This
program independently verifies that the canonical target grammar is a subset
of its d=4 input class and replays the mandatory finite SAT/circuit controls.
It does not implement or re-prove the Peng--Xiao branching algorithm.
"""
from __future__ import annotations
import argparse, collections, functools, hashlib, itertools, json, math
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
     (7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),
     (7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def canonical(F,n):
    if not F or n%3 or 3*len(F)!=4*n:return False
    if len({tuple(sorted(c)) for c in F})!=len(F):return False
    q=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if any(type(x) is not int or not x or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def ass(n,z):return {i:(z>>(i-1))&1 for i in range(1,n+1)}
def count(F,n,p=None):
    p={} if p is None else dict(p);free=[v for v in range(1,n+1) if v not in p];q=0
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));q+=sat(F,a)
    return q

def occurrence_profile(F,n):
    pos=[0]*(n+1);neg=[0]*(n+1)
    for c in F:
        for x in c:(pos if x>0 else neg)[abs(x)]+=1
    return {"positive":pos[1:],"negative":neg[1:],
            "total":[pos[v]+neg[v] for v in range(1,n+1)],
            "maximum_total":max(pos[v]+neg[v] for v in range(1,n+1)),
            "literal_records":sum(map(len,F))}

def compile_private(F,n):
    gates=[];outs=[];depth={v:0 for v in range(1,n+1)}
    def add(op,x,y):
        z=n+len(gates)+1;gates.append((z,op,x,y));depth[z]=1+max(depth[abs(x)],depth[abs(y)]);return z
    for c in F:outs.append(add("OR",add("OR",c[0],c[1]),c[2]))
    while len(outs)>1:outs=[add("AND",outs[i],outs[i+1]) if i+1<len(outs) else outs[i] for i in range(0,len(outs),2)]
    return gates,outs[0],depth[outs[0]]

def eval_circuit(gates,root,a):
    b=dict(a)
    for z,op,x,y in gates:
        X=b[abs(x)] if x>0 else 1-b[abs(x)];Y=b[abs(y)] if y>0 else 1-b[abs(y)]
        b[z]=int((X or Y) if op=="OR" else (X and Y))
    return bool(b[root])

def obdd_extrema(F,n):
    tab=tuple(int(sat(F,ass(n,z))) for z in range(1<<n));cost={}
    for S in range(1<<n):
        pre=[i for i in range(n) if S>>i&1]
        for v in range(n):
            if S>>v&1:continue
            rest=[i for i in range(n) if not(S>>i&1) and i!=v];pairs=set()
            for pa in range(1<<len(pre)):
                base=sum(((pa>>k)&1)<<i for k,i in enumerate(pre));lo=hi=0
                for rb in range(1<<len(rest)):
                    z=base+sum(((rb>>k)&1)<<i for k,i in enumerate(rest));lo|=tab[z]<<rb;hi|=tab[z|1<<v]<<rb
                if lo!=hi:pairs.add((lo,hi))
            cost[S,v]=len(pairs)
    full=(1<<n)-1
    @functools.lru_cache(None)
    def best(S):return 0 if S==full else min(cost[S,v]+best(S|1<<v) for v in range(n) if not(S>>v&1))
    @functools.lru_cache(None)
    def worst(S):return 0 if S==full else max(cost[S,v]+worst(S|1<<v) for v in range(n) if not(S>>v&1))
    S=natural=0
    for v in range(n):natural+=cost[S,v];S|=1<<v
    return {"best":best(0),"natural":natural,"worst":worst(0)}

def su_modes(F,n):
    q=0
    for i,j in itertools.combinations(range(len(F)),2):
        for A,B in itertools.product((0,1),repeat=2):
            req={};good=True
            for c,mode in ((F[i],A),(F[j],B)):
                for x in c:
                    val=int(x>0) if mode else int(x<0)
                    if abs(x) in req and req[abs(x)]!=val:good=False
                    req[abs(x)]=val
            brute=False
            for z in range(1<<n):
                a=ass(n,z)
                def hit(c,mode):
                    t=[a[abs(x)]==int(x>0) for x in c]
                    return all(t) if mode else not any(t)
                if hit(F[i],A) and hit(F[j],B):brute=True;break
            assert brute==good;q+=1
    return q

def malformed_count():
    bad=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    return sum(not canonical(F,max([abs(x) for c in F for x in c],default=3)) for F in bad)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    fixtures={"Y6_20":(Y6,6),"Z6_18":(Z6,6),"F9":(F9,9),"F15":(F15,15)}
    fixture_data={}
    for name,(F,n) in fixtures.items():
        assert canonical(F,n);prof=occurrence_profile(F,n);assert prof["maximum_total"]==4
        g,r,d=compile_private(F,n);models=0
        for z in range(1<<n):
            a=ass(n,z);v=eval_circuit(g,r,a);assert v==sat(F,a);models+=v
        fixture_data[name]={"n":n,"m":len(F),"models":models,"occurrences":prof,
                            "private_forward":{"gates":len(g),"depth":d,"truth_rows":1<<n}}
    assert [fixture_data[k]["models"] for k in fixtures]==[20,18,70,1032]
    common={3:0,5:1,6:0,7:0,8:0};p0={**common,1:0};p1={**common,1:1}
    c0,c1=count(F9,9,p0),count(F9,9,p1);assert (c0,c1)==(2,0)
    free=[2,4,9];cover=[]
    for bits in itertools.product((0,1),repeat=3):
        a=dict(p1);a.update(zip(free,bits));false=[i for i,c in enumerate(F9) if not any(a[abs(x)]==int(x>0) for x in c)]
        assert false;cover.append({"free_bits":bits,"false_source_clause_ids":false})
    obdd=obdd_extrema(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    alpha=0.8384754372266065293;dp_base=2**alpha;peer=1.2628;preprint=1.1199**2
    assert peer<dp_base and preprint<peer
    malformed=malformed_count();assert malformed==6
    result={
      "run":"BOUNDED-OCCURRENCE-TRANSFER-FIREWALL-REFEREE288",
      "timestamp_pacific":"2026-11-02T04:48:00-08:00",
      "status":"KNOWN_PUBLISHED_ALGORITHM_PLUS_PROVED_EXACT_TARGET_WRAPPER_AND_COMPUTATIONAL_CONTROLS",
      "P_vs_NP":"OPEN",
      "obstruction":"A target-specific forward/reverse representation cannot be treated as necessary decision work when a paid source-aware algorithm can decide the original directly without constructing that representation.",
      "theorem":"After a strict O(N)-record grammar and occurrence scan, every valid target original is an instance of d=4 bounded-occurrence CNF-SAT. Therefore the published Peng-Xiao exact algorithm gives a uniform deterministic target decider in O*(1.2628^n) time. This is O*(2^(0.336626166 n)), strictly below the project DP upper point O*(2^(0.838475437 n)). The transfer uses the same original source and constructs no C_F, OBDD, cofactor DAG, semantic cache or assignment-recovery key.",
      "numerics":{"peer_reviewed_d4_base":peer,"peer_reviewed_binary_exponent":math.log2(peer),
        "lspv1_iterated_DP_base":dp_base,"lspv1_binary_exponent":alpha,
        "base_ratio_DP_over_peer":dp_base/peer,
        "newer_preprint_d4_base":preprint,"newer_preprint_binary_exponent":math.log2(preprint)},
      "scope_caveat":"O* hides polynomial factors and the adopted paper does not supply a native FLMV machine trace here. This run makes no polynomial-space claim for the adopted implementation. LSPV1's slower DP point has an explicit polynomial-peak argument, so the two are distinct time-space upper points.",
      "falsifiers":["the 35-gate F9 evaluator is necessary before deciding the source","the 52-node best-order F9 OBDD is necessary before deciding the source","the 2^0.838475n projection algorithm is a current universal decision-time frontier for the target","cofactor equality or semantic representative discovery is mandatory work for every exact target decider"],
      "charged_wrapper":{"grammar_and_occurrence":"one full source scan; validate encoding, three distinct same-sign literals, duplicate-free clauses, exact two occurrences per sign and n:m relation; O(N) word operations with hash/sort costs declared by implementation","guest":"one paid invocation of the published d=4 exact SAT algorithm on the unchanged original after authentication","decision_recurrence":"T_target(F) <= T_grammar(N)+T_occurrence(N)+T_d4SAT(F)+T_output; published high-level bound O*(1.2628^n)","peak":"S_target <= S_parser+S_occurrence+S_d4SAT+O(log n) output. S_d4SAT is not silently declared polynomial and must be retained in any FLMV comparison.","excluded_free_work":"no C_F/PG/Tseitin/OBDD/cofactor/equality/cache/witness oracle is acquired"},
      "fixtures":fixture_data,"F9_same_original":{"common_pins":common,"x1_0_SAT_models":c0,"x1_1_UNSAT_models":c1,"UNSAT_complete_leaf_cover":cover,"obdd":obdd,"su_modes":su_modes(F9,9)},
      "malformed_rejected":malformed,
      "literature":[{"query":"bounded occurrence 3-SAT exact algorithm 4 occurrences per variable","finding":"Peng-Xiao IJCAI 2023 / TCS 2025 gives O*(1.2628^n) for d=4"},{"query":"3-SAT deterministic 1.3303 HSSW","finding":"Makino-Tamaki-Yamamoto gives O~(1.3303^n), a weaker generic bypass"},{"query":"project 1.2628 1.2721 Wahlstrom bounded occurrences","finding":"no indexed project hit; absence is not novelty evidence"},{"query":"github.com/openai SAT solver DPLL","finding":"no relevant indexed OpenAI implementation hit; absence is not evidence"}],
      "explicit_gap":"This is an exponential upper algorithm adopted from prior literature, not a polynomial target solver, decision lower bound, arbitrary-A power-short Phi(A), canonical-child theorem, or strict same-machine numerical FLMV transfer. It does not prove P=NP or P!=NP."
    }
    p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"run":result["run"],"models":{k:v["models"] for k,v in fixture_data.items()},"F9_pins":[c0,c1],"F9_OBDD":obdd,"bases":result["numerics"],"ok":True},sort_keys=True))

if __name__=="__main__":main()
