#!/usr/bin/env python3
"""Finite source-level audit; requires networkx==3.5. Not a tape simulator.

Run: python experiments/dynamic_redteam_blossom_audit_20261122.py
Emits deterministic JSON. Exhaustive enumeration is only the test oracle.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import hashlib
import inspect
import json
import platform
import networkx as nx
import networkx.algorithms.matching as matching_module


def clauses_from_graph(q, edges, b):
    incidence = [[] for _ in range(q)]
    for x, (u, v) in enumerate(edges, 1):
        assert u != v
        incidence[u].append(x)
        incidence[v].append(x)
    assert all(len(s) == 3 for s in incidence)
    return [tuple(-x if bit else x for x, bit in zip(s, bits))
            for s, demand in zip(incidence, b)
            for bits in product((0, 1), repeat=3) if sum(bits) != demand]


def recognise(rows):
    # Construct allowed masks by removing each clause's unique false row.
    tables = {}
    for row in rows:
        if len(row) != 3 or any(type(x) is not int or x == 0 for x in row):
            return None
        scope = tuple(sorted(abs(x) for x in row))
        if len(set(scope)) != 3:
            return None
        signs = {abs(x): int(x < 0) for x in row}
        forbidden = sum(signs[x] << i for i, x in enumerate(scope))
        tables[scope] = tables.get(scope, 255) & ~(1 << forbidden)
    if not tables:
        return None
    scopes, b, occurrences = sorted(tables), [], defaultdict(list)
    for v, scope in enumerate(scopes):
        allowed = tables[scope]
        demand = next((k for k in (1, 2) if allowed ==
                       sum(1 << mask for mask in range(8) if mask.bit_count() == k)), None)
        if demand is None:
            return None
        b.append(demand)
        for x in scope:
            occurrences[x].append(v)
    if any(len(vs) != 2 for vs in occurrences.values()):
        return None
    return scopes, b, occurrences


def solve(rows):
    admitted = recognise(rows)
    if admitted is None:
        return {'label': 'UNKNOWN'}
    scopes, b, occurrences = admitted
    H = nx.Graph()
    for v, scope in enumerate(scopes):
        for x in scope:
            H.add_node(('port', v, x))
        for j in range(3-b[v]):
            dummy = ('dummy', v, j)
            H.add_edges_from((dummy, ('port', v, x)) for x in scope)
    for x, (u, v) in sorted(occurrences.items()):
        H.add_edge(('port', u, x), ('port', v, x))
    pairs = nx.max_weight_matching(H, maxcardinality=True)
    assert nx.is_matching(H, pairs)
    result = {'label': 'SAT' if 2*len(pairs) == len(H) else 'UNSAT',
              'gadget_vertices': len(H), 'gadget_edges': H.number_of_edges(),
              'matching_size': len(pairs)}
    if result['label'] == 'SAT':
        partner = {}
        for a, z in pairs:
            partner[a] = z
            partner[z] = a
        values = {x: int(partner[('port', u, x)] == ('port', v, x))
                  for x, (u, v) in occurrences.items()}
        assert all(sum(values[x] for x in scope) == k for scope, k in zip(scopes, b))
        assert all(any(values[abs(z)] == int(z > 0) for z in row) for row in rows)
        result['true_variables'] = sorted(x for x in values if values[x])
    return result


def truth_table(q, edges):
    counts = Counter()
    for bits in product((0, 1), repeat=len(edges)):
        degree = [0]*q
        for selected, (u, v) in zip(bits, edges):
            degree[u] += selected
            degree[v] += selected
        counts[tuple(degree)] += 1
    return counts


def encoded_size(c, d):
    r = max(3, c+1 if c % 2 == 0 else c+2)
    n0, m0 = d+(10*c+1)*r+2, (20*c+4)*r
    n, m = n0+m0+3, 2*m0+4
    w = n.bit_length()
    return dict(c=c, d=d, r=r, n=n, m=m, w=w,
                N=3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w)


def run():
    assert nx.__version__ == '3.5'
    # New full demand sweep, not the peer's K4/prism/parallel/K3,3 suite.
    edges = sorted({tuple(sorted(e)) for i in range(5) for e in
                    [(i, (i+1)%5), (i, i+5), (i+5, (i+2)%5+5)]})
    counts = truth_table(10, edges)
    cases = []
    for b in product((1, 2), repeat=10):
        rows = clauses_from_graph(10, edges, b)
        answer = solve(rows)
        expected = 'SAT' if counts[b] else 'UNSAT'
        assert answer['label'] == expected
        cases.append(dict(demands=b, source_models=counts[b], **answer))

    # Three odd lobes attached to one vertex: a connected even-order
    # cubic graph with a size-one Tutte obstruction.
    base = [e for e in combinations(range(4), 2) if e != (0, 1)]
    base += [(0, 4), (1, 4)]
    star = [(u+5*j, v+5*j) for j in range(3) for u, v in base]
    star += [(4+5*j, 15) for j in range(3)]
    graph = nx.Graph(star)
    assert nx.is_connected(graph)
    assert all(deg == 3 for _, deg in graph.degree())
    deleted = graph.copy()
    deleted.remove_node(15)
    odd_components = sorted(sorted(s) for s in nx.connected_components(deleted))
    assert [len(s) for s in odd_components] == [5, 5, 5]
    controls = []
    for name, b in [('odd_lobes_one', [1]*16),
                    ('odd_lobes_two', [2]*16),
                    ('repaired_demands', [2 if v in (4, 9) else 1 for v in range(16)])]:
        ans = solve(clauses_from_graph(16, star, b))
        assert ans['label'] == ('SAT' if name == 'repaired_demands' else 'UNSAT')
        controls.append(dict(name=name, demands=b, **ans))
    # Explicit source SAT witness: first two unsubsumed lobes use the
    # subdividing vertex twice; the final lobe uses its bridge.
    chosen = {(0,4),(1,4),(2,3),(5,9),(6,9),(7,8),(10,12),(11,13),(14,15)}
    chosen = {tuple(sorted(e)) for e in chosen}
    explicit = [int(tuple(sorted(e)) in chosen) for e in star]
    degrees = [0]*16
    for selected, (u,v) in zip(explicit, star):
        degrees[u] += selected
        degrees[v] += selected
    assert degrees == [2 if v in (4,9) else 1 for v in range(16)]

    # Coincident supports are outside admission, including a SAT example.
    alias = []
    for b in [(1,1), (1,2)]:
        rows = clauses_from_graph(2, [(0,1)]*3, b)
        assert solve(rows)['label'] == 'UNKNOWN'
        models = sum(all(any(bits[abs(z)-1] == int(z > 0) for z in row) for row in rows)
                     for bits in product((0,1), repeat=3))
        assert models == (3 if b == (1,1) else 0)
        alias.append(dict(demands=b, fast_path='UNKNOWN', fallback_models=models))
    original = clauses_from_graph(16, star, [1]*16)
    renamed = [tuple((1 if z>0 else -1)*(101+7*abs(z)) for z in reversed(row))
               for row in reversed(original)]
    renamed += renamed[:3]
    assert solve(renamed)['label'] == 'UNSAT'
    assert solve([(1,1,2)])['label'] == 'UNKNOWN'
    module_path = Path(inspect.getsourcefile(matching_module))
    return dict(target='DYNAMIC-MATCHING-EXECUTABLE-AUDIT1',
                peer_revision='5c68647aae3b7e5295990235bc8313732edeb04b',
                python=platform.python_version(), networkx=nx.__version__,
                matching_module_sha256=hashlib.sha256(module_path.read_bytes()).hexdigest(),
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                mode='deterministic exhaustive demand sweep; no random seed',
                petersen_edges=edges, cases=cases, case_count=len(cases),
                sat=sum(c['label']=='SAT' for c in cases),
                unsat=sum(c['label']=='UNSAT' for c in cases),
                source_assignments_enumerated=1 << len(edges),
                odd_lobes_edges=star, odd_components_after_delete_15=odd_components,
                controls=controls, explicit_repair_true_variables=[i+1 for i,x in enumerate(explicit) if x],
                alias_controls=alias, transformed_unsat='PASS',
                encodings={'petersen':encoded_size(50,15), 'odd_lobes':encoded_size(80,24)},
                limitations='Source-level blossom library audit only. No compiled-image parser, target SAT run, formal kernel, memory benchmark, or Turing-machine timing.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
