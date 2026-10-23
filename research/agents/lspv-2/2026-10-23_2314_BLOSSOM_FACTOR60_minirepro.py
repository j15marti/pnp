#!/usr/bin/env python3
"""BLOSSOM-FACTOR60 independent small nonbipartite factor reproduction.
Requires: pip install networkx. Prints exact K4 pin and both-label controls.
No SAT solver is used; negative small cases are checked by brute force.
"""
import itertools
import networkx as nx

EDGES = list(itertools.combinations(range(4), 2))
SUPPORTS = [tuple(i + 1 for i, (a, b) in enumerate(EDGES) if v in (a, b))
            for v in range(4)]


def matching_factor(supports, pins):
    incidences = {}
    for v, triple in enumerate(supports):
        for x in triple:
            incidences.setdefault(x, []).append(v)
    nxt = len(supports)
    for x, sites in incidences.items():
        if len(sites) == 1:
            sites.append(nxt)
            nxt += 1
        assert len(sites) == 2
    required, graph, slots = set(), nx.Graph(), {}
    for v in range(nxt):
        touching = [x for x, endpoints in incidences.items() if v in endpoints]
        fixed = sum(pins[x] for x in touching if x in pins)
        free = sum(x not in pins for x in touching)
        lo, hi = ((1, 2) if v < len(supports) else (0, 1))
        lo, hi = max(0, lo - fixed), min(free, hi - fixed)
        if lo > hi:
            return None, {"reason": "interval"}
        slots[v] = [('slot', v, j) for j in range(hi)]
        graph.add_nodes_from(slots[v])
        required.update(slots[v][:lo])
    for x, (u, v) in incidences.items():
        if x in pins:
            continue
        a, b = ('stub', x, 0), ('stub', x, 1)
        required.update((a, b))
        graph.add_edge(a, b, weight=2)
        for stub, endpoint in ((a, u), (b, v)):
            for slot in slots[endpoint]:
                graph.add_edge(stub, slot, weight=1 + int(slot in required))
    matching = nx.max_weight_matching(graph, weight='weight')
    optimum = sum(graph[u][v]['weight'] for u, v in matching)
    ledger = {"reason": "ok" if optimum == len(required) else "shortfall",
              "required": len(required), "optimum": optimum,
              "nodes": graph.number_of_nodes(), "edges": graph.number_of_edges()}
    if optimum != len(required):
        return None, ledger
    mate = {u: v for a, b in matching for u, v in ((a, b), (b, a))}
    solution = dict(pins)
    for x in incidences:
        if x not in solution:
            solution[x] = int(mate[('stub', x, 0)][0] == 'slot')
            assert (mate[('stub', x, 1)][0] == 'slot') == bool(solution[x])
    assert all(1 <= sum(solution[x] for x in triple) <= 2 for triple in supports)
    return solution, ledger


def exhaustive_label(supports, defects):
    n = max(x for triple in supports for x in triple)
    for bits in itertools.product((0, 1), repeat=n):
        val = {i + 1: bits[i] for i in range(n)}
        if all(1 <= sum(val[x] for x in triple) <= 2 for triple in supports) and \
           all(any(val[abs(lit)] == (lit > 0) for lit in clause)
               for clause in defects):
            return val
    return None


def witness_defects(supports):
    triple = supports[0]
    six = []
    for bits in itertools.product((0, 1), repeat=3):
        if 1 <= sum(bits) <= 2:
            six.append(tuple(-x if bit else x for x, bit in zip(triple, bits)))
    other = min(set(x for s in supports for x in s) - set(triple))
    sat = six[:-1] + [(triple[0], triple[1], other)]
    return sat, six


def solve_by_witnesses(supports, defects):
    for choice in itertools.product(*defects):
        pins = {}
        for literal in choice:
            x, v = abs(literal), int(literal > 0)
            if x in pins and pins[x] != v:
                break
            pins[x] = v
        else:
            sol, _ = matching_factor(supports, pins)
            if sol is not None:
                assert all(any(sol[abs(l)] == int(l > 0) for l in c)
                           for c in defects)
                return sol
    return None

if __name__ == '__main__':
    pins = {1: 0, 2: 0, 3: 1, 4: 0, 5: 1}
    miss, bad = matching_factor(SUPPORTS, pins)
    assert miss is None and bad['reason'] == 'shortfall'
    repaired = pins.copy()
    repaired[2] = 1
    good, yes = matching_factor(SUPPORTS, repaired)
    assert good and yes['reason'] == 'ok'
    sat, unsat = witness_defects(SUPPORTS)
    assert solve_by_witnesses(SUPPORTS, sat)
    assert solve_by_witnesses(SUPPORTS, unsat) is None
    assert exhaustive_label(SUPPORTS, sat)
    assert exhaustive_label(SUPPORTS, unsat) is None
    print({'K4_unsat_pins': bad, 'K4_sat_pins': yes,
           'same_size_sat_clauses': len(sat),
           'same_size_unsat_clauses': len(unsat), 'checks': 'PASS'})
