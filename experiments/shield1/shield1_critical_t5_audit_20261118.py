#!/usr/bin/env python3
"""Exact finite audit of arc-critical T5 CSPs, reproducible Python stdlib.
Canonical sources: at most one oriented arc per unordered pair. All label
vectors are enumerated modulo global rotation, with x_0=0.
Usage: python shield1_critical_t5_audit.py [--max-n 5]
"""
import argparse
import itertools
import json
from collections import Counter

A = (1, 3)

def R(a, b):
    return (b-a) % 5 in A


def connected_after_removing_vertex(n, edges, removed):
    alive = [v for v in range(n) if v != removed]
    if not alive:
        return True
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if removed not in (u, v):
            adj[u].append(v)
            adj[v].append(u)
    seen = {alive[0]}
    todo = [alive[0]]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == len(alive)


def biconnected(n, edges):
    return all(connected_after_removing_vertex(n, edges, k) for k in range(n))


def girth(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    out = n + 1
    for root in range(n):
        distance = [-1] * n
        parent = [-1] * n
        distance[root] = 0
        Q = [root]
        for u in Q:
            for v in adj[u]:
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent[v] = u
                    Q.append(v)
                elif parent[u] != v:
                    out = min(out, distance[u]+distance[v]+1)
    return out if out <= n else None


def run(n):
    pairs = list(itertools.combinations(range(n), 2))
    labels = [(0,)+tail for tail in itertools.product(range(5), repeat=n-1)]
    U = (1 << len(labels)) - 1
    masks = {}
    diffs = {}
    for u, v in pairs:
        for a, b in ((u, v), (v, u)):
            mask = 0
            for i, x in enumerate(labels):
                if R(x[a], x[b]):
                    mask |= 1 << i
            masks[(a, b)] = mask
        dd = [0]*5
        for i, x in enumerate(labels):
            dd[(x[v]-x[u])%5] |= 1 << i
        diffs[(u, v)] = dd
    stats = Counter()
    endpoint_sets = Counter()
    edge_counts = Counter()
    min_girth = n+1
    max_girth = 0
    example = None
    fail = []
    for options in itertools.product((0, 1, 2), repeat=len(pairs)):
        edges = [p if t==1 else (p[1],p[0]) for p,t in zip(pairs, options) if t]
        if len(edges) < n:
            continue
        em = [masks[e] for e in edges]
        pre = [U]
        for x in em:
            pre.append(pre[-1] & x)
        if pre[-1]:
            continue
        suf = [0] * (len(em)+1)
        suf[-1] = U
        for k in range(len(em)-1, -1, -1):
            suf[k] = suf[k+1] & em[k]
        w = [pre[k]&suf[k+1] for k in range(len(em))]
        if any(not z for z in w):
            continue
        if not connected_after_removing_vertex(n, edges, None):
            stats['excluded_disconnected_minimal_unsat'] += 1
            continue
        stats['critical'] += 1
        edge_counts[len(edges)] += 1
        if not biconnected(n, edges):
            fail.append(('not_biconnected', edges))
        gg = girth(n, edges)
        min_girth = min(min_girth, gg or 999)
        max_girth = max(max_girth, gg or 0)
        edge_witnesses = {}
        for (u,v),m in zip(edges,w):
            a,b = min(u,v),max(u,v)
            support0 = {d for d in range(5) if m & diffs[(a,b)][d]}
            support = frozenset(((d if (u,v)==(a,b) else -d)%5) for d in support0)
            endpoint_sets[''.join(map(str, sorted(support)))] += 1
            if not support.issubset({0,2,4}):
                fail.append(('endpoint_constraint', edges, (u,v), sorted(support)))
            witness_idx = (m & -m).bit_length()-1
            x = labels[witness_idx]
            if not all(R(x[p], x[q]) for p,q in edges if (p,q)!=(u,v)):
                fail.append(('witness_invalid', edges, x))
            if R(x[u],x[v]):
                fail.append(('witness_satisfies_missing_arc', edges, x))
            edge_witnesses[f'{u}->{v}'] = {'labels': list(x), 'endpoint_diffs': sorted(support)}
        if example is None:
            example = {'edges': edges, 'girth': gg, 'deleted_edge_witnesses': edge_witnesses}
    return {'n':n,'source_graphs_considered':3**len(pairs),
            'critical_count':stats['critical'],
            'excluded_disconnected_minimal_unsat':stats['excluded_disconnected_minimal_unsat'],
            'critical_by_arc_count':dict(sorted(edge_counts.items())),
            'endpoint_support_by_critical_arc':dict(sorted(endpoint_sets.items())),
            'minimum_girth': None if not stats['critical'] else min_girth,
            'maximum_girth': None if not stats['critical'] else max_girth,
            'first_critical_example':example,
            'failed_invariants':fail}


def path_supports():
    """All 2^k path sign words, pin first and last labels, k=1..5."""
    table = {}
    for k in range(1,6):
        counts = Counter()
        for word in itertools.product((1,-1), repeat=k):
            supports = {0}
            for sign in word:
                # traverse from source endpoint to target endpoint
                increments = (1,3) if sign==1 else (2,4)
                supports = {(s+d)%5 for s in supports for d in increments}
            counts[len(supports)] += 1
        table[k] = dict(sorted(counts.items()))
    return table



def direct_4_vertex_control():
    """Independent full 5^4 checker, no gauge/bitsets."""
    h = [(0,2),(0,3),(1,2),(3,1),(3,2)]
    omitted = {}
    for edge in h:
        support = Counter()
        actual = []
        for x in itertools.product(range(5), repeat=4):
            if all(R(x[u],x[v]) for u,v in h if (u,v)!=edge):
                support[(x[edge[1]]-x[edge[0]])%5] += 1
                actual.append(x)
        omitted[f'{edge[0]}->{edge[1]}'] = {'count':len(actual),
                        'difference_counts': dict(sorted(support.items()))}
    h_count = sum(all(R(x[u],x[v]) for u,v in h)
                  for x in itertools.product(range(5), repeat=4))
    assert h_count == 0
    assert [v['count'] for v in omitted.values()] == [10,10,10,10,5]
    assert omitted['3->2']['difference_counts'] == {2:5}
    return {'unsat_source_model_count': h_count,
            'source':h, 'deleted_arc_checks':omitted}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n',type=int,default=5)
    a = ap.parse_args()
    if not 3 <= a.max_n <= 5:
        raise SystemExit('3 <= max_n <= 5 required for full enumeration')
    output = {'relation':'(b-a) mod 5 in {1,3}', 'gauge':'x_0=0',
              'path_word_support_sizes':path_supports(),
              'direct_full_assignment_control':direct_4_vertex_control(),
              'graphs':[run(n) for n in range(3,a.max_n+1)]}
    print(json.dumps(output, sort_keys=True, indent=2))
    assert not any(x['failed_invariants'] for x in output['graphs'])

if __name__ == '__main__':
    main()
