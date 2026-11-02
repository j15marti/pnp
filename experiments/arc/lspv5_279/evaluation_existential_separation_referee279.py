#!/usr/bin/env python3
"""REFEREE279: exact finite F9 evaluation/OBDD audit.

This program deliberately separates three problems:
  (i) evaluate the F9 Boolean function on an assignment,
  (ii) compile it into an OBDD for a declared order, and
  (iii) decide whether the authenticated CNF has some satisfying assignment.
It establishes only restricted finite/query/representation facts.
"""
from __future__ import annotations

import argparse
import collections
import functools
import itertools
import json
from pathlib import Path

F9 = ((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
      (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6 = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15 = ((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
       (7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15 = ((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),
       (7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15 = P15 + tuple(tuple(-x for x in c) for c in N15)

SAT_PINS = {1:0,3:0,5:1,6:0,7:0,8:0}
UNSAT_PINS = {1:1,3:0,5:1,6:0,7:0,8:0}

def canonical(F, n):
    if not F or n % 3 or 3*len(F) != 4*n:
        return False
    if len({tuple(sorted(c)) for c in F}) != len(F):
        return False
    q = collections.Counter()
    for c in F:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False
        if any(abs(x) < 1 or abs(x) > n for x in c):
            return False
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        q.update(c)
    return all(q[v] == q[-v] == 2 for v in range(1,n+1))

def sat(F, a):
    return all(any(a[abs(x)] == int(x > 0) for x in c) for c in F)

def assignments(F, pins=None):
    pins = pins or {}
    n = max(abs(x) for c in F for x in c)
    free = [v for v in range(1,n+1) if v not in pins]
    out = []
    for bits in itertools.product((0,1), repeat=len(free)):
        a = dict(pins); a.update(zip(free,bits))
        if sat(F,a): out.append(a)
    return out

def f9_table():
    return tuple(int(sat(F9,{i+1:(x>>i)&1 for i in range(9)})) for x in range(512))

def residual_pair_cost(table, S, i, n=9):
    """Number of distinct essential residual pairs at the next OBDD level."""
    prefix = [j for j in range(n) if (S>>j)&1]
    rest = [j for j in range(n) if not ((S>>j)&1) and j != i]
    seen = set()
    for a in range(1<<len(prefix)):
        base = sum(((a>>k)&1)<<j for k,j in enumerate(prefix))
        lo, hi = [], []
        for b in range(1<<len(rest)):
            y = base + sum(((b>>k)&1)<<j for k,j in enumerate(rest))
            lo.append(table[y]); hi.append(table[y|(1<<i)])
        lo, hi = tuple(lo), tuple(hi)
        if lo != hi: seen.add((lo,hi))
    return len(seen)

def obdd_extrema(table):
    n = 9
    cost = {(S,i):residual_pair_cost(table,S,i,n)
            for S in range(1<<n) for i in range(n) if not ((S>>i)&1)}
    mn = {0:(0,())}; mx = {0:(0,())}
    for k in range(n):
        for S in (z for z in range(1<<n) if z.bit_count()==k):
            for i in range(n):
                if (S>>i)&1: continue
                T = S|(1<<i); c = cost[S,i]
                cand = (mn[S][0]+c, mn[S][1]+(i+1,))
                if T not in mn or cand[0] < mn[T][0]: mn[T] = cand
                cand = (mx[S][0]+c, mx[S][1]+(i+1,))
                if T not in mx or cand[0] > mx[T][0]: mx[T] = cand
    def order_size(order):
        S = 0; z = 0
        for v in order:
            z += cost[S,v-1]; S |= 1<<(v-1)
        return z
    full = (1<<n)-1
    return {"minimum_nodes":mn[full][0], "minimum_order":mn[full][1],
            "maximum_nodes":mx[full][0], "maximum_order":mx[full][1],
            "natural_order_nodes":order_size(tuple(range(1,10))),
            "subset_extension_costs":len(cost)}

def decision_tree_metrics(table):
    n = 9
    @functools.lru_cache(None)
    def D(mask,bits):
        vals = {table[x] for x in range(1<<n) if x&mask == bits}
        if len(vals)==1: return 0
        return 1 + min(max(D(mask|1<<i,bits),D(mask|1<<i,bits|1<<i))
                       for i in range(n) if not ((mask>>i)&1))
    @functools.lru_cache(None)
    def D1(mask,bits):
        xs = [x for x in range(1<<n) if x&mask == bits]
        ones = [x for x in xs if table[x]]
        if not ones or len(ones)==len(xs): return 0
        choices=[]
        for i in range(n):
            if (mask>>i)&1: continue
            kids=[]
            for z in (0,1):
                if any(((x>>i)&1)==z for x in ones):
                    kids.append(D1(mask|1<<i,bits|(z<<i)))
            choices.append(1+max(kids))
        return min(choices)
    cert = {0:[],1:[]}
    for x,v in enumerate(table):
        best=n+1
        for mask in range(1<<n):
            if mask.bit_count()>=best: continue
            if all(w==v for y,w in enumerate(table) if y&mask==x&mask):
                best=mask.bit_count()
        cert[v].append(best)
    return {"D_evaluate":D(0,0), "D1_evaluate":D1(0,0),
            "certificate_histogram":{
              str(v):{str(k):q.count(k) for k in sorted(set(q))}
              for v,q in cert.items()},
            "accepting_certificate_max":max(cert[1]),
            "rejecting_certificate_max":max(cert[0])}

def su_modes(F):
    n=max(abs(x) for c in F for x in c); checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        pred=(not opp,not same,not same,not opp); act=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A); AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B); BU=all(a[abs(x)]!=int(x>0) for x in B)
            act=[u or v for u,v in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(act)==pred; checks+=4
    return checks

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); args=ap.parse_args()
    assert canonical(F9,9) and canonical(Y6,6) and canonical(F15,15)
    table=f9_table(); assert sum(table)==70
    obdd=obdd_extrema(table); dt=decision_tree_metrics(table)
    assert obdd["minimum_nodes"]==52 and obdd["maximum_nodes"]==80
    assert obdd["natural_order_nodes"]==66 and dt["D_evaluate"]==dt["D1_evaluate"]==9
    controls={"F9_models":len(assignments(F9)),"Y6_models":len(assignments(Y6)),
      "F15_models":len(assignments(F15)),"same_original_SAT_models":len(assignments(F9,SAT_PINS)),
      "same_original_UNSAT_models":len(assignments(F9,UNSAT_PINS)),
      "UNSAT_completion_leaves":2**3,"F9_SU_modes":su_modes(F9)}
    assert controls=={"F9_models":70,"Y6_models":20,"F15_models":1032,
      "same_original_SAT_models":2,"same_original_UNSAT_models":0,
      "UNSAT_completion_leaves":8,"F9_SU_modes":264}
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not canonical(x,max([abs(v) for c in x for v in c],default=3)) for x in malformed)
    controls["malformed_rejected"]=6
    out={
      "run":"EVALUATION-EXISTENTIAL-SEPARATION-REFEREE279",
      "status":"PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL",
      "P_vs_NP":"OPEN",
      "exact_obstruction":"Forward-circuit, OBDD, and assignment-query costs concern evaluating f_F(x); SAT asks whether any x makes f_F(x)=1. No paid uniform reduction from an evaluation representation lower bound to existential source-decision work is supplied.",
      "falsifiable_hypotheses":[
        "A large OBDD under one order forces large work for every compiler or SAT decider.",
        "The exact assignment-evaluation query depth of F9 lower-bounds source SAT decision on authenticated F9.",
        "Post-solution minimization of an UNSAT formula's zero function supplies a uniform UNSAT algorithm.",
        "A finite F9 separation yields an all-input ARC or numerical FLMV transfer."],
      "obdd":obdd,"decision_tree":dt,"controls":controls,
      "restricted_family_consequence":{
        "source":"t disjoint renamed F9 copies; valid canonical but disconnected",
        "bad_order_width_lower":"2^t after reading all designated x1 variables",
        "grouped_order_nodes_upper":"52t",
        "assignment_evaluation_query_lower":"at least 8t on an accepting input by the product of per-block 8-bit accepting certificates",
        "assignment_evaluation_query_upper":"9t by evaluating every block",
        "recognized_SAT_decision":"one fixed F9 witness per block plus paid source authentication and 12t original-clause checks; O(t) word work",
        "scope":"representation/evaluation separation only; not connected and not an all-input target solver"},
      "charged_recurrence":"W_D(F)=W_grammar+W_source/index/head+W_discover+W_select/switch/failed+W_deduce/GE/proof+W_cache/replay+W_child/output/access+W_guest+sum_all_evaluated_children W_D(Q).",
      "peak_space":"maximum simultaneously live writable/index/head/cache/proof/ancestor/child/guest objects; OBDD tables and truth tables are offline experiment storage, not free solver state",
      "finite_work":{"truth_rows":512,"obdd_subset_extension_costs":obdd["subset_extension_costs"],
        "decision_subproblems_upper":3**9,"all_orders_covered_by_subset_DP":362880},
      "wrappers":{"DELAY":"adds time with zero source-data XOR","COPY":"must charge trace writes but cannot strengthen the semantic lower bound","RECOMP":"trades cache space for paid rereads","logical_XOR":"offline only"},
      "large_controls":{"U198":"inherited authenticated UNSAT; not reproved","V198":"inherited checked SAT witness; not reproved"},
      "limitations":["finite/restricted result","disjoint t-copy family is not the requested connected obstruction family","no all-input polynomial controller","no arbitrary-A power shortening","no strict same-machine FLMV transfer"]}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","obdd":obdd,"decision_tree":dt,"controls":controls,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__": main()
