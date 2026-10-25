#!/usr/bin/env python3
"""Independent standard-library reproducer for M22-EDGE-DEFECT-PUSH109.
Exhaustive small graph checks and connected 15-variable source.
Logical edge toggles are not physical FLMV-machine operations.
"""
import itertools
import json

H = [(0,6,7),(1,7,8),(2,8,9),(9,10,11),
     (6,12,13),(10,12,14),(11,13,14)]
P1 = [(0,3,4),(1,4,5),(2,3,5)]
Q1 = [(0,3,5),(1,3,4),(2,4,5)]

def repair(n, edges, forbidden, initial=None):
    adj = [[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        assert u != v
        adj[u].append(i)
        adj[v].append(i)
    assert all(len(a) in (2,3) for a in adj)
    bits = list(initial) if initial is not None else [0]*len(edges)
    flips = 0
    def bad(v):
        a = [bits[e] for e in adj[v]]
        return (len(set(a)) == 1) if len(a)==3 else (a[0]==a[1]==forbidden[v])
    def other(e,v):
        u,w = edges[e]
        return w if u == v else u
    while True:
        defects = [v for v in range(n) if bad(v)]
        if not defects:
            break
        before = len(defects)
        v = defects[0]
        seen = {v}
        previous = -1
        for _ in range(n+1):
            assert bad(v)
            e = next(e for e in adj[v] if e != previous)
            w = other(e,v)
            bits[e] ^= 1
            flips += 1
            assert not bad(v)
            if w in seen or not bad(w):
                assert not bad(w)
                break
            seen.add(w)
            v,previous = w,e
        else:
            raise AssertionError("nonterminating defect walk")
        assert sum(bad(v) for v in range(n)) < before
    return bits, flips

def clause_check(P,Q,assn):
    return (all(any(assn[v] for v in s) for s in P)
         and all(any(not assn[v] for v in s) for s in Q))

def core_extend(a):
    D = set(range(6))
    Z = set(range(6,15))
    edges = []
    for z in sorted(Z):
        uses = [i for i,s in enumerate(H) if z in s]
        assert len(uses)==2
        edges.append(tuple(uses))
    forbidden = {}
    for i,s in enumerate(H):
        exposed = [v for v in s if v in D]
        assert len(exposed)<=1
        if exposed:
            forbidden[i] = a[exposed[0]]
    bits, flips = repair(len(H),edges,forbidden)
    assn = dict(a)
    for z,bit in zip(sorted(Z),bits):
        assn[z] = bit
    assert all(0 < sum(assn[v] for v in s) < 3 for s in H)
    return assn, flips

def source_validation():
    P = set(H+P1)
    Q = set(H+Q1)
    V = set(v for s in P|Q for v in s)
    assert V==set(range(15))
    assert len(P)==len(Q)==10
    assert len(P&Q)==7 and len(P-Q)==len(Q-P)==3
    assert all(len(set(s))==3 for s in P|Q)
    assert all(sum(v in s for s in P)==2 and sum(v in s for s in Q)==2 for v in V)
    adjacency = {v:set() for v in V}
    for s in P|Q:
        for v in s: adjacency[v].update(set(s)-{v})
    reached={0}
    while True:
        nxt=reached|set().union(*(adjacency[v] for v in reached))
        if nxt==reached: break
        reached=nxt
    assert reached==V
    return P,Q

def graph_battery():
    out={}
    for n in range(3,7):
        choices=list(itertools.combinations(range(n),2))
        count=0
        for mask in range(1<<len(choices)):
            edges=[e for i,e in enumerate(choices) if mask>>i&1]
            degree=[sum(v in e for e in edges) for v in range(n)]
            if not all(d in (2,3) for d in degree): continue
            seen={0}
            while True:
                newer=seen|{v for e in edges for v in e if any(t in seen for t in e)}
                if newer==seen: break
                seen=newer
            if len(seen)!=n: continue
            deg2=[v for v in range(n) if degree[v]==2]
            for word in itertools.product((0,1),repeat=len(deg2)):
                forbid=dict(zip(deg2,word))
                bits,_=repair(n,edges,forbid)
                for v in range(n):
                    vals=[bits[i] for i,e in enumerate(edges) if v in e]
                    assert (len(set(vals))==2) if degree[v]==3 else not(vals[0]==vals[1]==forbid[v])
                count+=1
        out[n]=count
    assert out=={3:8,4:73,5:1004,6:20110}
    return out

def main():
    P,Q=source_validation()
    full=0
    for bits in itertools.product((0,1),repeat=15):
        a=dict(enumerate(bits))
        full+=clause_check(P,Q,a)
    assert full==1694
    cores=0
    residual=0
    max_flips=0
    for bits in itertools.product((0,1),repeat=6):
        a=dict(enumerate(bits))
        lifted,flips=core_extend(a)
        cores+=1
        max_flips=max(max_flips,flips)
        good=clause_check(P1,Q1,a)
        residual+=good
        if good: assert clause_check(P,Q,lifted)
    assert (cores,residual,max_flips)==(64,26,10)
    graph_cases=graph_battery()
    print(json.dumps({"run_id":"M22-EDGE-DEFECT-PUSH109",
        "source_k":15,"source_m":20,"source_in_C_star":True,
        "source_models":full,"paired_core_boundary_words":cores,
        "unmatched_boundary_models":residual,"max_logical_edge_flips":max_flips,
        "graph_cases":graph_cases,
        "exhaustive_graph_tests":sum(graph_cases.values()),
        "failures":0,
        "warning":"Not a general SAT or FLMV machine-resource lower bound"},
        sort_keys=True,indent=2))
if __name__=="__main__":
    main()
