#!/usr/bin/env python3
"""Exact Boolean elimination + witness lift; no packages, randomness or SAT oracle.
Run: timeout 25s python3 audit.py source079.t5 > results.json
Logical counters are not physical bit-machine costs or peak bytes.
"""
import sys, json, hashlib, time
from itertools import product
from collections import Counter, deque

C = range(5)
R = {(a,b) for a,b in product(C, repeat=2) if (b-a)%5 in (1,3)}
stats = Counter()

def factor(u,v):
    return ((u,v), set(R))

def accepts(f, assignment):
    stats['factor_probes'] += 1
    scope, table = f
    return tuple(assignment[v] for v in scope) in table

def solve(vertices, factors):
    """Exhaustive domain branching with recomputed arc consistency."""
    def rec(dom):
        stats['search_nodes'] += 1
        changed = True
        while changed:
            changed = False
            for scope, table in factors:
                valid = []
                for row in table:
                    stats['support_rows'] += 1
                    if all(row[i] in dom[v] for i,v in enumerate(scope)):
                        valid.append(row)
                if not valid:
                    return None
                for i,v in enumerate(scope):
                    nd = dom[v] & {row[i] for row in valid}
                    if not nd: return None
                    if nd != dom[v]: dom[v] = nd; changed = True
        undecided = [v for v in vertices if len(dom[v]) > 1]
        if not undecided: return {v:next(iter(dom[v])) for v in vertices}
        v = min(undecided, key=lambda v:(len(dom[v]),v))
        for a in sorted(dom[v]):
            child = {u:set(d) for u,d in dom.items()}
            child[v] = {a}
            ans = rec(child)
            if ans is not None: return ans
            stats['failed_children'] += 1
        return None
    dom = {v:set(C) for v in vertices}
    if vertices: dom[min(vertices)] = {0}  # common translation symmetry
    return rec(dom)

def contract(vertices, factors):
    live = set(vertices); factors = [(s,set(t)) for s,t in factors]
    records = []; supports = Counter()
    while live:
        stats['candidate_scans'] += len(live)
        neigh = {v:set() for v in live}
        for scope,_ in factors:
            for v in scope: neigh[v].update(set(scope)-{v})
        eligible = [v for v in live if len(neigh[v]) <= 2]
        if not eligible: break
        v = min(eligible); boundary = tuple(sorted(neigh[v]))
        incident = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        choice = {}
        for row in product(C, repeat=len(boundary)):
            a = dict(zip(boundary,row))
            for c in C:
                stats['elimination_trials'] += 1
                a[v] = c
                if all(accepts(f,a) for f in incident):
                    choice[row] = c; break
        records.append((v,boundary,choice))
        factors.append((boundary,set(choice)))
        if len(boundary)==2: supports[len(choice)] += 1
        live.remove(v)
    return sorted(live), factors, records, supports

def lift(witness, records):
    out = dict(witness)
    for v,boundary,choice in reversed(records):
        stats['lift_steps'] += 1
        out[v] = choice[tuple(out[u] for u in boundary)]
    return out

def check_edges(n,edges,w):
    assert set(w)==set(range(n)) and all(w[v] in C for v in w)
    for u,v in edges:
        stats['original_arc_checks'] += 1
        assert (w[u],w[v]) in R

def graph_audit(n,edges):
    assert all(u!=v for u,v in edges)
    pairs = {frozenset((u,v)) for u,v in edges}
    assert len(pairs)==len(edges)
    adj = {v:set() for v in range(n)}
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    seen={0}; queue=deque([0])
    while queue:
        u=queue.popleft()
        for v in adj[u]-seen: seen.add(v); queue.append(v)
    assert len(seen)==n
    girth=n+1
    for a,b in edges:
        dist={a:0}; queue=deque([a])
        while queue:
            u=queue.popleft()
            for v in adj[u]:
                if {u,v}=={a,b} or v in dist: continue
                dist[v]=dist[u]+1; queue.append(v)
        if b in dist: girth=min(girth,dist[b]+1)
    return girth

def path_audit():
    rows=words=0
    for length in range(1,9):
        for signs in product((-1,1),repeat=length):
            words+=1
            supports={}
            for start in C:
                routes={start:(start,)}
                for sign in signs:
                    nex={}
                    for a,route in routes.items():
                        for delta in (1,3):
                            b=(a+sign*delta)%5
                            nex.setdefault(b,route+(b,))
                    routes=nex
                assert len(routes)==min(5,length+1)
                for end,route in routes.items():
                    assert all(((route[i+1]-route[i])*s)%5 in (1,3)
                               for i,s in enumerate(signs))
                    supports[start,end]=route; rows+=1
            if length in (2,3): assert len(supports) not in (10,25)
    # Smallest literal suppression failure: ++ length two.
    two={(a,c) for a,b,c in product(C,repeat=3) if (a,b) in R and (b,c) in R}
    assert len(two)==15 and (0,2) in two and (0,2) not in R
    assert (0,3) in R and (0,3) not in two
    return {'orientation_words':words,'verified_endpoint_witnesses':rows,
            'smallest_failure':{'path':'++','endpoint_pair':[0,2],
             'lost_by_single_forward_arc':True,'spurious_forward_pair':[0,3]}}

def main():
    began=time.monotonic(); raw=open(sys.argv[1],'rb').read()
    assert hashlib.sha256(raw).hexdigest()=='0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac'
    lines=raw.decode('ascii').splitlines(); header=lines[0].split()
    assert header[:2]==['p','t5']; n,m=map(int,header[2:])
    assert lines[1:n+1]==['v '+str(i) for i in range(n)]
    edges=[tuple(map(int,line.split()[1:])) for line in lines[n+1:]]
    assert len(edges)==m and all(0<=v<n for e in edges for v in e)
    girth=graph_audit(n,edges); assert girth==8
    assert solve(list(range(n)),[factor(*e) for e in edges]) is None
    no_counters=dict(stats); trials=[]; support_total=Counter()
    for missing in edges:
        kept=[e for e in edges if e!=missing]
        assert graph_audit(n,kept) >= girth  # also checks connectivity
        live,fs,recs,supports=contract(range(n),[factor(*e) for e in kept])
        answer=solve(live,fs); assert answer is not None
        w=lift(answer,recs); check_edges(n,kept,w)
        assert (w[missing[0]],w[missing[1]]) not in R
        # Independent direct original-source solve; not a reused kernel answer.
        direct=solve(list(range(n)),[factor(*e) for e in kept])
        assert direct is not None; check_edges(n,kept,direct)
        support_total.update(supports)
        trials.append({'missing':missing,'kernel_vertices':len(live),
                       'eliminated':len(recs),'binary_supports':dict(supports),
                       'witness':[w[i] for i in range(n)]})
    out={'revision':'ARC-STRENGTHEN-T5-HEREDITY-v1','source_sha256':hashlib.sha256(raw).hexdigest(),
         'source_bytes':len(raw),'vertices':n,'arcs':m,'girth':girth,
         'direct_UNSAT':True,'deletions_checked':len(trials),
         'kernel_vertex_range':[min(x['kernel_vertices'] for x in trials),max(x['kernel_vertices'] for x in trials)],
         'binary_support_histogram':dict(support_total),'path_audit':path_audit(),
         'original_UNSAT_counters':no_counters,'all_logical_counters':dict(stats),
         'deletion_witnesses':trials,'elapsed_seconds':time.monotonic()-began,
         'physical_bit_trace':False,'asymptotic_contraction':'OPEN','P_vs_NP':'OPEN'}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__': main()
