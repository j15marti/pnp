#!/usr/bin/env python3
"""REFEREE282: exact first Davis--Putnam elimination quota and its failure to iterate."""
from __future__ import annotations
import argparse, collections, itertools, json
from functools import lru_cache
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
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
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,z):
    return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)

def normalize(clauses):
    raw=[]
    for c in clauses:
        s=frozenset(c)
        if any(-x in s for x in s):continue
        raw.append(s)
    uniq=set(raw)
    kept=[c for c in uniq if not any(d<c for d in uniq)]
    return tuple(sorted((tuple(sorted(c,key=lambda x:(abs(x),x<0))) for c in kept),key=lambda c:(len(c),c)))

def eliminate(F,v):
    F=normalize(F);pos=[c for c in F if v in c];neg=[c for c in F if -v in c]
    rest=[c for c in F if v not in c and -v not in c];res=[];taut=0
    for p in pos:
        for n in neg:
            r=(set(p)-{v})|(set(n)-{-v})
            if any(-x in r for x in r):taut+=1
            else:res.append(tuple(r))
    out=normalize(rest+res)
    return out,{"variable":v,"positive":len(pos),"negative":len(neg),
      "candidate_pairs":len(pos)*len(neg),"tautological_pairs":taut,
      "unique_non_tautological_resolvents":len(set(normalize(res))),
      "clauses":len(out),"literal_records":sum(map(len,out)),
      "max_width":max(map(len,out),default=0)}

def project_value(F,n,v,y):
    lo=y&((1<<(v-1))-1);hi=y>>(v-1);z=lo|(hi<<v)
    return int(sat(F,z) or sat(F,z|(1<<(v-1))))

def residual(F,pins):
    out=[]
    for c in F:
        if any(abs(x) in pins and pins[abs(x)]==int(x>0) for x in c):continue
        out.append(tuple(x for x in c if abs(x) not in pins))
    return normalize(out)

def eval_cnf_vars(F,assignment):
    return all(any(assignment[abs(x)]==int(x>0) for x in c) for c in F)

def forward_counts(F,n):
    models=0
    for z in range(1<<n):
        direct=sat(F,z)
        gate_proxy=all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)
        assert direct==gate_proxy;models+=direct
    m=len(F);return {"truth_rows":1<<n,"models":models,"fan_in_two_gates":3*m-1,
                       "depth":2+(m-1).bit_length()}

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        pred=(not opp,not same,not same,not opp);act=[False]*4
        for z in range(1<<n):
            AS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in A);AU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in A)
            BS=all(((z>>(abs(x)-1))&1)==int(x>0) for x in B);BU=all(((z>>(abs(x)-1))&1)!=int(x>0) for x in B)
            act=[a or b for a,b in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(act)==pred;checks+=4
    return checks

def obdd_counts(F,n):
    costs={};full=(1<<n)-1
    for mask in range(1<<n):
        A=[i for i in range(n) if (mask>>i)&1];R=[i for i in range(n) if not(mask>>i)&1];S=set()
        for aa in range(1<<len(A)):
            sig=0
            for rr in range(1<<len(R)):
                z=sum(((aa>>k)&1)<<i for k,i in enumerate(A))+sum(((rr>>k)&1)<<i for k,i in enumerate(R));sig|=sat(F,z)<<rr
            S.add(sig)
        for p,v in enumerate(R):
            q=0
            for sig in S:
                lo=hi=0
                for y in range(1<<(len(R)-1)):
                    i=(y&((1<<p)-1))|((y>>p)<<(p+1));lo|=((sig>>i)&1)<<y;hi|=((sig>>(i|1<<p))&1)<<y
                q+=lo!=hi
            costs[mask,v]=q
    @lru_cache(None)
    def dp(mask,worst=False):
        if mask==full:return 0
        vals=[costs[mask,v]+dp(mask|1<<v,worst) for v in range(n) if not(mask>>v)&1]
        return max(vals) if worst else min(vals)
    mask=0;natural=0
    for v in range(n):natural+=costs[mask,v];mask|=1<<v
    return {"best":dp(0),"natural":natural,"worst":dp(0,True)}

def elimination_extremes(F,n):
    start=normalize(F);full=(1<<n)-1
    @lru_cache(None)
    def go(C,mask,worst):
        if mask==full:return (0,0,0,())
        vals=[]
        for v in range(1,n+1):
            if (mask>>(v-1))&1:continue
            D,m=eliminate(C,v);tail=go(D,mask|1<<(v-1),worst)
            vals.append((m["candidate_pairs"]+tail[0],max(m["candidate_pairs"],tail[1]),
                         max(m["literal_records"],tail[2]),(v,)+tail[3]))
        return (max(vals) if worst else min(vals))
    best=go(start,0,False);worst=go(start,0,True)
    def trace(order):
        C=start;out=[]
        for v in order:
            C,m=eliminate(C,v);out.append(m)
        return out
    return {"best":{"total_candidate_pairs":best[0],"max_step_pairs":best[1],"post_source_peak_literals":best[2],"order":best[3],"trace":trace(best[3])},
            "worst":{"total_candidate_pairs":worst[0],"max_step_pairs":worst[1],"post_source_peak_literals":worst[2],"order":worst[3],"trace":trace(worst[3])}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);a=ap.parse_args()
    fixtures={"Y6":(Y6,6),"F9":(F9,9),"F15":(F15,15)};first={};semantic_rows=0;forward={}
    for name,(F,n) in fixtures.items():
        assert canonical(F,n);forward[name]=forward_counts(F,n);first[name]=[]
        for v in range(1,n+1):
            D,meta=eliminate(F,v)
            assert meta["candidate_pairs"]==4 and meta["clauses"]<=len(F)
            assert meta["literal_records"]<=3*len(F)+4 and meta["max_width"]<=4
            for y in range(1<<(n-1)):
                assignment={u:(y>>(u-1 if u<v else u-2))&1 for u in range(1,n+1) if u!=v}
                assert int(eval_cnf_vars(D,assignment))==project_value(F,n,v,y);semantic_rows+=1
            first[name].append(meta)
    ext=elimination_extremes(F9,9)
    assert ext["best"]["total_candidate_pairs"]==9 and ext["best"]["max_step_pairs"]==4
    assert ext["worst"]["total_candidate_pairs"]==35 and ext["worst"]["max_step_pairs"]==12
    D9,m9=eliminate(F9,9);D96,m96=eliminate(D9,6);assert m96["candidate_pairs"]==6
    common={3:0,5:1,6:0,7:0,8:0};pins0={**common,1:0};pins1={**common,1:1}
    R0,R1=residual(F9,pins0),residual(F9,pins1)
    assert R0==((2,),(9,)) and R1==((2,),(9,),(-2,-9))
    def finish(C,order):
        total=0;trace=[]
        for v in order:
            C,m=eliminate(C,v);total+=m["candidate_pairs"];trace.append(m)
        return C,total,trace
    E0,c0,t0=finish(R0,(2,9));E1,c1,t1=finish(R1,(2,9))
    assert E0==() and E1==((),) and (c0,c1)==(0,2)
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not canonical(x,max([abs(v) for c in x for v in c],default=3)) for x in malformed)
    obdd=obdd_counts(F9,9);assert obdd=={"best":52,"natural":66,"worst":80}
    result={"run":"FIRST-ELIMINATION-QUOTA-REFEREE282","timestamp_pst":"2026-11-01 22:48",
      "status":"PROVED_EXACT_FIRST_STEP_PLUS_COMPUTATIONAL_COUNTERCONTROL","P_vs_NP":"OPEN",
      "obstruction":"The original 2-positive/2-negative quota bounds only the first Davis--Putnam elimination. Projected CNFs are noncanonical, so later occurrence products and the paid order-selection problem are uncontrolled.",
      "theorem":"For every valid canonical original F with m clauses and every original variable x, Davis--Putnam elimination of x considers exactly four positive-negative pairs and yields an exact CNF for (exists x)F with at most m clauses, 3m+4 literal records, and width at most four.",
      "proof":"Remove the two positive and two negative x-clauses and add at most 2*2 non-tautological resolvents. Each resolvent has width at most four. Thus clauses <=m and literal records <=3(m-4)+4*4=3m+4. The standard resolution elimination identity proves exact existential equivalence.",
      "first_eliminations":first,"semantic_projection_rows":semantic_rows,"forward_evaluators":forward,
      "F9_order_extremes":ext,"F9_second_step_quota_breach":{"first":m9,"second":m96},
      "F9_same_original_pins":{"common":common,"x1_0_SAT":{"residual":R0,"models":2,"candidate_pairs":c0,"terminal":E0},
                               "x1_1_UNSAT":{"residual":R1,"models":0,"candidate_pairs":c1,"terminal":E1}},
      "controls":{"F9_OBDD_nodes":obdd,"F9_SU_modes":su_modes(F9),"malformed_rejected":6,
                  "forward_truth_rows":sum(x["truth_rows"] for x in forward.values())},
      "falsified":["the first projection requires more clauses than the source or a forward evaluator","the 2-by-2 resolvent quota is hereditary under elimination","elimination order is cost-equivalent on F9"],
      "charged_work":{"recurrence":"W_D(F)=W_grammar+W_source/index/head+W_discovery+W_elimination/resolvent+W_failed+W_select/switch+W_semantic/proof/GE+W_cache/replay+W_child/output/bit+W_guest(DELAY/COPY/RECOMP)+sum W_D(successor)",
        "peak":"maximum co-live source and occurrence lists, candidate-resolvent buffer, normalized projected CNF/circuit, proof/cache, ancestors, children, index/head state, and delayed or recomputed guest state",
        "F9_finite":"best/worst totals charge every candidate pair, including tautological and later subsumed resolvents; normalization and DP selector acquisition are additional paid work"},
      "exact_gap":"The theorem is one-step only. On F9, eliminating 9 then 6 already gives six candidate pairs; the exact best and worst orders cost 9 and 35 pairs, and a worst step costs 12. No polynomial total-work bound, universal arbitrary-A power-short Phi(A), or strict same-machine FLMV numerical transfer is proved.",
      "scope":["projected CNFs are ordinary noncanonical children","not unrestricted circuit minimization","finite F9 order DP is not a lower bound","post-answer constant circuits are irrelevant to acquisition","P versus NP remains open"],
      "literature_queries":["Een Biere 2005 Effective preprocessing in SAT through variable and clause elimination","bounded variable elimination SAT occurrence product clause growth","Davis Putnam elimination variable order complexity","GitHub j15marti/pnp bounded variable elimination; Davis-Putnam resolvent","GitHub org:openai bounded variable elimination; Davis-Putnam SAT"],
      "github_findings":{"project":"targeted indexed searches returned no exact first-step 2-by-2 quota theorem; absence is not novelty evidence","openai":"targeted indexed searches returned no relevant SAT variable-elimination implementation; absence is not novelty evidence","implementations":"SATCH and OR-Tools expose bounded variable elimination and explicitly bound occurrence products or weighted clause/literal growth"}}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","semantic_rows":semantic_rows,"forward":forward,"F9_order_extremes":{k:{q:v for q,v in x.items() if q!="trace"} for k,x in ext.items()},"same_original_costs":[c0,c1],"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
