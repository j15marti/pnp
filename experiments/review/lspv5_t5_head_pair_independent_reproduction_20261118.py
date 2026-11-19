#!/usr/bin/env python3
"""Independent reproduction of the separated-head exact-one T5 theorem.

No code is imported from the candidate package.  The package's critical
formula/witness JSON is treated only as input evidence and is rechecked with
the independently declared T5 relation below.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import tracemalloc
from collections import defaultdict, deque
from pathlib import Path

WINS = ({1, 3}, {2, 4}, {0, 3}, {1, 4}, {0, 2})


def R(a: int, b: int) -> bool:
    return b in WINS[a]


def Q(a: int, b: int, c: int) -> bool:
    return R(a, b) != R(a, c)


def verify(clauses, assignment) -> bool:
    return all(Q(assignment[h], assignment[u], assignment[v]) for h, u, v in clauses)


def gadget() -> list[tuple[int, int, int]]:
    # Heads 0,1; tails 2=00, 3=01, 4=10, 5=11.
    return [
        (0, 2, 4), (0, 4, 3), (0, 3, 5),
        (1, 2, 3), (1, 3, 4), (1, 4, 5),
    ]


def build_components(heads, tails, clauses):
    """Return component incidences (component, parity, head), or odd cycle."""
    by_head = {h: defaultdict(list) for h in heads}
    for h, u, v in clauses:
        by_head[h][u].append(v)
        by_head[h][v].append(u)
    incidences = defaultdict(list)
    component_count = 0
    edge_scans = 0
    for h in heads:
        side = {}
        for root in by_head[h]:
            if root in side:
                continue
            cid = component_count
            component_count += 1
            side[root] = 0
            q = deque([root])
            while q:
                u = q.popleft()
                incidences[u].append((cid, side[u], h))
                for v in by_head[h][u]:
                    edge_scans += 1
                    if v in side:
                        if side[v] == side[u]:
                            return None, component_count, edge_scans
                    else:
                        side[v] = side[u] ^ 1
                        q.append(v)
    return incidences, component_count, edge_scans


def solve_2cnf(nvars, clauses):
    """Clauses contain (variable, required Boolean value) literals."""
    g = [[] for _ in range(2 * nvars)]
    gr = [[] for _ in range(2 * nvars)]
    arcs = 0

    def node(x, value):
        return 2 * x + value

    def add(a, b):
        nonlocal arcs
        g[a].append(b)
        gr[b].append(a)
        arcs += 1

    for clause in clauses:
        if len(clause) == 1:
            x, a = clause[0]
            add(node(x, 1 - a), node(x, a))
        elif len(clause) == 2:
            (x, a), (y, b) = clause
            add(node(x, 1 - a), node(y, b))
            add(node(y, 1 - b), node(x, a))
        else:
            raise AssertionError("not 2-CNF")

    seen = bytearray(2 * nvars)
    order = []
    for root in range(2 * nvars):
        if seen[root]:
            continue
        seen[root] = 1
        stack = [(root, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(g[u]):
                v = g[u][i]
                stack[-1] = (u, i + 1)
                if not seen[v]:
                    seen[v] = 1
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()
    comp = [-1] * (2 * nvars)
    cc = 0
    for root in reversed(order):
        if comp[root] >= 0:
            continue
        comp[root] = cc
        stack = [root]
        while stack:
            u = stack.pop()
            for v in gr[u]:
                if comp[v] < 0:
                    comp[v] = cc
                    stack.append(v)
        cc += 1
    if any(comp[2 * x] == comp[2 * x + 1] for x in range(nvars)):
        return None, arcs
    return [int(comp[2 * x + 1] > comp[2 * x]) for x in range(nvars)], arcs


def solve_separated(n, heads, clauses):
    """Exact solver for separated heads, with <=2 components per follower."""
    heads = tuple(heads)
    hset = set(heads)
    tails = tuple(v for v in range(n) if v not in hset)
    assert all(h in hset and u not in hset and v not in hset and len({h, u, v}) == 3
               for h, u, v in clauses)
    inc, ncomp, bfs_scans = build_components(heads, tails, clauses)
    stats = {"head_trials": 0, "selector_patterns": 0, "color_tests": 0,
             "two_sat_clauses": 0, "two_sat_arcs": 0, "bfs_edge_scans": bfs_scans,
             "source_verifications": 0, "component_count": ncomp}
    if inc is None:
        return "UNSAT", None, stats, "odd parity"
    degree = max((len(inc[t]) for t in tails), default=0)
    stats["max_follower_component_degree"] = degree
    if degree > 2:
        return "UNSUPPORTED", None, stats, "degree guard"
    if not heads:
        return "SAT", [0] * n, stats, "empty"
    for rest in itertools.product(range(5), repeat=len(heads) - 1):
        stats["head_trials"] += 1
        assignment = [None] * n
        for h, c in zip(heads, (0,) + rest):
            assignment[h] = c
        cnf = []
        for tail in tails:
            factors = inc[tail]
            for selectors in itertools.product(range(2), repeat=len(factors)):
                stats["selector_patterns"] += 1
                possible = False
                for color in range(5):
                    stats["color_tests"] += 1
                    if all(R(assignment[h], color) == bool(s ^ parity)
                           for (cid, parity, h), s in zip(factors, selectors)):
                        possible = True
                        break
                if not possible:
                    # Forbid exactly this selector tuple.
                    cnf.append(tuple((cid, 1 - s) for (cid, _, _), s in zip(factors, selectors)))
                    stats["two_sat_clauses"] += 1
        bits, arcs = solve_2cnf(ncomp, cnf)
        stats["two_sat_arcs"] += arcs
        if bits is None:
            continue
        for tail in tails:
            colors = [c for c in range(5)
                      if all(R(assignment[h], c) == bool(bits[cid] ^ parity)
                             for cid, parity, h in inc[tail])]
            assert colors
            assignment[tail] = colors[0]
        stats["source_verifications"] += len(clauses)
        assert verify(clauses, assignment)
        return "SAT", assignment, stats, "verified"
    return "UNSAT", None, stats, "all head tuples"


def truth_masks(n, clauses):
    masks = set()
    for a in itertools.product(range(5), repeat=n):
        mask = 0
        for i, (h, u, v) in enumerate(clauses):
            if Q(a[h], a[u], a[v]):
                mask |= 1 << i
        masks.add(mask)
    sat = bytearray(1 << len(clauses))
    for mask in masks:
        sub = mask
        while True:
            sat[sub] = 1
            if sub == 0:
                break
            sub = (sub - 1) & mask
    return sat, len(masks)


def incidence_girth(n, clauses):
    """Girth of the variable-clause bipartite incidence graph."""
    N = n + len(clauses)
    g = [[] for _ in range(N)]
    for i, clause in enumerate(clauses):
        cnode = n + i
        for v in clause:
            g[v].append(cnode)
            g[cnode].append(v)
    best = N + 1
    for s in range(N):
        dist = [-1] * N
        parent = [-1] * N
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)
                elif parent[u] != v:
                    best = min(best, dist[u] + dist[v] + 1)
    return None if best == N + 1 else best


def main():
    tracemalloc.start()
    checks = 0

    # Full-signature lemma and six-clause gadget, all prescribed head colors.
    signatures = {}
    for a, b in itertools.product(range(5), repeat=2):
        s = {(int(R(a, c)), int(R(b, c))) for c in range(5)}
        expected = ((b - a) % 5) in (2, 3)
        assert (len(s) == 4) == expected
        signatures[f"{a},{b}"] = sorted(s)
        checks += 1

    # Sharp local boundary at follower degree three.  For heads (0,1,2),
    # the five possible follower colors induce exactly the Boolean graph of
    # y = NOR(x,z).  It is not Horn, dual-Horn, bijunctive, affine, 0-valid,
    # or 1-valid.  Schaefer therefore classifies the unrestricted CSP over
    # this relation as NP-complete; the Q grammar's typed-wiring transfer is
    # deliberately left separate.
    rel012 = {tuple(int(R(h, c)) for h in (0, 1, 2)) for c in range(5)}
    expected_nor = {(x, int(not (x or z)), z) for x, z in itertools.product(range(2), repeat=2)}
    assert rel012 == expected_nor
    closure_witnesses = {
        "and": (((1, 0, 0), (0, 0, 1)), (0, 0, 0)),
        "or": (((1, 0, 0), (0, 1, 0)), (1, 1, 0)),
        "majority": (((1, 0, 0), (0, 0, 1), (0, 1, 0)), (0, 0, 0)),
        "xor3": (((1, 0, 0), (1, 0, 1), (0, 0, 1)), (0, 0, 0)),
    }
    for inputs, output in closure_witnesses.values():
        assert all(x in rel012 for x in inputs) and output not in rel012
        checks += 1
    assert (0, 0, 0) not in rel012 and (1, 1, 1) not in rel012
    non_bijunctive_triples = 0
    for hs in itertools.product(range(5), repeat=3):
        relation = {tuple(int(R(h, c)) for h in hs) for c in range(5)}
        if any(tuple(int(x + y + z >= 2) for x, y, z in zip(a, b, c)) not in relation
               for a, b, c in itertools.product(relation, repeat=3)):
            non_bijunctive_triples += 1
    assert non_bijunctive_triples == 60
    checks += 3
    G = gadget()
    gadget_models = {}
    for a, b in itertools.product(range(5), repeat=2):
        count = 0
        for tail_values in itertools.product(range(5), repeat=4):
            assignment = [a, b] + list(tail_values)
            count += verify(G, assignment)
        assert (count > 0) == (((b - a) % 5) in (2, 3))
        gadget_models[f"{a},{b}"] = count
        checks += 1

    # Complete small-grammar audit against direct T5 truth masks.
    small = []
    for heads, tails in ((2, 4), (3, 3)):
        n = heads + tails
        clauses = [(h, u, v) for h in range(heads)
                   for u, v in itertools.combinations(range(heads, n), 2)]
        sat, mask_count = truth_masks(n, clauses)
        supported = matched = parity_feasible = unsupported = 0
        for subset in range(1 << len(clauses)):
            source = [c for i, c in enumerate(clauses) if (subset >> i) & 1]
            status, witness, _, reason = solve_separated(n, range(heads), source)
            if status == "UNSUPPORTED":
                unsupported += 1
                continue
            supported += 1
            parity_feasible += reason != "odd parity"
            assert (status == "SAT") == bool(sat[subset]), (heads, tails, subset, status)
            if witness is not None:
                assert verify(source, witness)
            matched += 1
            checks += 1
        small.append({"heads": heads, "tails": tails, "clauses": len(clauses),
                      "systems": 1 << len(clauses), "supported": supported,
                      "unsupported": unsupported, "matched": matched,
                      "parity_feasible_supported": parity_feasible,
                      "direct_truth_masks": mask_count})

    # Candidate critical formula and every provided deletion witness.
    raw_path = Path("library_inputs/t5_head_pair/extracted/HEAD_PAIR_RAW.json")
    raw = json.loads(raw_path.read_text())
    crit = raw["minimal_triangle_critical"]
    clauses = [tuple(x) for x in crit["clauses"]]
    status, witness, critical_stats, reason = solve_separated(crit["n"], range(3), clauses)
    assert status == "UNSAT" and witness is None and reason == "all head tuples"
    checks += 1
    deletion_checks = 0
    for item in crit["deletions"]:
        omitted = item["deleted_index"]
        a = item["witness"]
        false = [i for i, c in enumerate(clauses) if not Q(*(a[v] for v in c))]
        assert false == [omitted]
        source = clauses[:omitted] + clauses[omitted + 1:]
        s2, a2, _, _ = solve_separated(crit["n"], range(3), source)
        assert s2 == "SAT" and verify(source, a2)
        deletion_checks += len(clauses) + len(source)
        checks += 2

    # All four-variable induced subsystems of the 15-variable core.
    induced = 0
    for vertices in itertools.combinations(range(crit["n"]), 4):
        V = set(vertices)
        sub = [c for c in clauses if set(c) <= V]
        if sub:
            # Direct enumeration on only the selected four values.
            ok = any(all(Q(a[vertices.index(h)], a[vertices.index(u)], a[vertices.index(v)])
                         for h, u, v in sub)
                     for a in itertools.product(range(5), repeat=4))
            assert ok
        induced += 1
        checks += 1

    # The claimed high-girth transfer fails for this gadget: a fixed 4-cycle
    # is already present inside one six-clause copy.
    gadget_incidence_girth = incidence_girth(6, G)
    critical_incidence_girth = incidence_girth(crit["n"], clauses)
    assert gadget_incidence_girth == critical_incidence_girth == 4
    checks += 2

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = {
        "status": "PASS",
        "method": "independent T5 predicate, independent components/2-SAT solver, direct truth-mask audit",
        "checks": checks,
        "full_signature_offsets": [d for d in range(5) if len(signatures[f"0,{d}"]) == 4],
        "gadget_positive_head_pairs": sum(v > 0 for v in gadget_models.values()),
        "gadget_model_counts": gadget_models,
        "degree_three_boundary": {
            "heads": [0, 1, 2],
            "relation": sorted(rel012),
            "exact_function": "middle_bit = NOR(first_bit, third_bit)",
            "non_bijunctive_ordered_head_triples": non_bijunctive_triples,
            "ordered_head_triples_total": 125,
            "closure_counterexamples": closure_witnesses,
            "unrestricted_boolean_csp_status": "NP-complete by Schaefer dichotomy",
            "typed_Q_wiring_transfer": "OPEN"
        },
        "small_grammar_exhaustion": small,
        "critical_core": {
            "n": crit["n"], "m": len(clauses), "status": status,
            "all_deletions_reproduced": len(crit["deletions"]),
            "direct_deletion_clause_checks": deletion_checks,
            "induced_four_vertex_subsystems": induced,
            "head_trials": critical_stats["head_trials"],
            "two_sat_clauses": critical_stats["two_sat_clauses"],
            "two_sat_arcs": critical_stats["two_sat_arcs"],
        },
        "girth_firewall": {
            "single_six_clause_gadget_incidence_girth": gadget_incidence_girth,
            "minimal_15_clause_core_incidence_girth": critical_incidence_girth,
            "conclusion": "the C5 head-graph reduction has a fixed incidence 4-cycle inside every edge gadget"
        },
        "space_metrics": {
            "tracemalloc_peak_python_heap_bytes": peak,
            "ru_maxrss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "definition": "empirical Python allocation/RSS metrics, not a machine-independent complexity-space bound"
        },
        "script_sha256": script_hash,
        "limitations": [
            "finite exhaustive checks do not prove an unrestricted lower bound",
            "the exact solver is exponential in the number of head-only variables",
            "the pair-gadget reduction has incidence girth four even when its head interaction graph has large girth",
            "C5-homomorphism hardness does not establish critical-deletion witness-search hardness"
        ]
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
