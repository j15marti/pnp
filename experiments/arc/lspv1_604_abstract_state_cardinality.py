#!/usr/bin/env python3
"""LSPV-1/604: Exhaustive finite MAY-state cardinality control.

No native R_mix341 checker is simulated. Directed graphs contain all 3 states,
all six non-loop directed positions, and each position independently absent or
cost 0, 1, or 2. Compare Dijkstra with complete simple-path enumeration.
"""
import heapq
import itertools
import json

N=3
ARCS=tuple((i,j) for i in range(N) for j in range(N) if i!=j)
ALPHABET=(None,0,1,2)
assert len(ARCS)==6

def dijkstra(adj,s,g):
    dist={s:0}
    heap=[(0,s)]
    while heap:
        cost,u=heapq.heappop(heap)
        if cost!=dist.get(u):
            continue
        if u==g:
            return cost
        for v,w in adj[u]:
            nxt=cost+w
            if nxt<dist.get(v,float('inf')):
                dist[v]=nxt
                heapq.heappush(heap,(nxt,v))
    return None

def enumerate_simple_paths(adj,s,g):
    best=None
    def walk(u,seen,cost):
        nonlocal best
        if u==g:
            best=cost if best is None else min(best,cost)
            return
        for v,w in adj[u]:
            if v not in seen:
                walk(v,seen|{v},cost+w)
    walk(s,{s},0)
    return best

summary={"directed_states":N,"edge_positions":len(ARCS),
         "edge_values":["absent",0,1,2],"graphs":0,"start_goal_pairs":0,
         "reachable":0,"unreachable":0,"max_distance":0,
         "max_bound":2*(N-1),"distance_histogram":{},"mismatch_count":0,
         "bound_violation_count":0}
for choices in itertools.product(ALPHABET,repeat=len(ARCS)):
    adj=[[] for _ in range(N)]
    for (u,v),w in zip(ARCS,choices):
        if w is not None:
            adj[u].append((v,w))
    summary["graphs"]+=1
    for s in range(N):
        for g in range(N):
            if s==g:
                continue
            summary["start_goal_pairs"]+=1
            d=dijkstra(adj,s,g)
            p=enumerate_simple_paths(adj,s,g)
            if d!=p:
                summary["mismatch_count"]+=1
            if d is None:
                summary["unreachable"]+=1
                continue
            summary["reachable"]+=1
            summary["max_distance"]=max(summary["max_distance"],d)
            summary["distance_histogram"][str(d)]=summary["distance_histogram"].get(str(d),0)+1
            if d>2*(N-1):
                summary["bound_violation_count"]+=1
assert summary["mismatch_count"]==0
assert summary["bound_violation_count"]==0
assert summary["graphs"]==4096
assert summary["start_goal_pairs"]==24576

tight=[]
for m in range(2,11):
    graph=[[(i+1,1)] if i<m-1 else [] for i in range(m)]
    observed=dijkstra(graph,0,m-1)
    assert observed==m-1
    tight.append({"state_count":m,"minimum":observed,"bound":m-1})
summary["unit_weight_tight_chains"]=tight

summary["zero_cost_may_shortcut"]={"states":5,"true_chain_cost":4,
    "may_distance":dijkstra([[(1,1),(4,0)],[(2,1)],[(3,1)],[(4,1)],[]],0,4)}
assert summary["zero_cost_may_shortcut"]["may_distance"]==0
print(json.dumps(summary,indent=2,sort_keys=True))
