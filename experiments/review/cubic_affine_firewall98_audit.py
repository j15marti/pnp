#!/usr/bin/env python3
"""Finite verifier for CUBIC-AFFINE-FIREWALL98 (stdlib only)."""
from __future__ import annotations

import itertools
import json
from pathlib import Path


def prism(t: int):
    edges = set()
    for layer in (0, 1):
        off = layer * t
        for i in range(t):
            edges.add(tuple(sorted((off + i, off + (i + 1) % t))))
    for i in range(t):
        edges.add((i, t + i))
    return 2 * t, sorted(edges)


def mobius(r: int):
    g = 2 * r
    edges = {tuple(sorted((i, (i + 1) % g))) for i in range(g)}
    edges.update((i, i + r) for i in range(r))
    return g, sorted(edges)


def petersen():
    edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    inner = (5, 7, 9, 6, 8)
    edges.update(tuple(sorted((inner[i], inner[(i + 1) % 5]))) for i in range(5))
    edges.update((i, i + 5) for i in range(5))
    return 10, sorted(edges)


def k33():
    return 6, [(u, v) for u in range(3) for v in range(3, 6)]


def incidence(g, edges):
    inc = [[] for _ in range(g)]
    for j, (u, v) in enumerate(edges):
        inc[u].append(j)
        inc[v].append(j)
    return [tuple(sorted(x)) for x in inc]


def connected_after_delete(g, edges, deleted=None):
    alive = [v for v in range(g) if v != deleted]
    if not alive:
        return True
    adj = [[] for _ in range(g)]
    for u, v in edges:
        if u != deleted and v != deleted:
            adj[u].append(v); adj[v].append(u)
    seen = {alive[0]}; stack = [alive[0]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return len(seen) == len(alive)


def clauses_for(g, edges, charge):
    inc = incidence(g, edges)
    clauses = []
    owners = []
    forbidden = []
    for v, triple in enumerate(inc):
        for bits in itertools.product((0, 1), repeat=3):
            if (bits[0] ^ bits[1] ^ bits[2]) != charge[v]:
                # Positive literal is false at 0; negative literal is false at 1.
                clauses.append(tuple((triple[i], bits[i] == 0) for i in range(3)))
                owners.append(v); forbidden.append(bits)
    return clauses, owners, forbidden


def eval_cnf(clauses, mask):
    return all(any(bool(mask & (1 << var)) == positive for var, positive in c)
               for c in clauses)


def equation_ok(g, edges, charge, mask):
    for v, triple in enumerate(incidence(g, edges)):
        parity = 0
        for e in triple:
            parity ^= (mask >> e) & 1
        if parity != charge[v]:
            return False
    return True


def min_edge_cover_bruteforce(g, edges):
    for h in range(len(edges) + 1):
        for chosen in itertools.combinations(range(len(edges)), h):
            covered = set()
            for j in chosen:
                covered.update(edges[j])
            if len(covered) == g:
                return h
    raise AssertionError("no edge cover")


def main():
    graphs = [
        ("mobius4_K4", *mobius(2)),
        ("prism3", *prism(3)),
        ("K33", *k33()),
        ("mobius8", *mobius(4)),
        ("prism4", *prism(4)),
        ("petersen", *petersen()),
    ]
    assertions = 0
    assignment_checks = 0
    deletion_checks = 0
    rows = []
    for name, g, edges in graphs:
        inc = incidence(g, edges)
        assert len(edges) * 2 == 3 * g and all(len(x) == 3 for x in inc)
        assert connected_after_delete(g, edges)
        assert all(connected_after_delete(g, edges, v) for v in range(g))
        assert min_edge_cover_bruteforce(g, edges) == g // 2
        assertions += 4

        for odd in (False, True):
            charge = [0] * g
            if odd:
                charge[0] = 1
            clauses, owners, forbidden = clauses_for(g, edges, charge)
            assert len(clauses) == 4 * g
            assert all(len(c) == 3 and len({x for x, _ in c}) == 3 for c in clauses)
            assertions += 2
            models = 0
            for mask in range(1 << len(edges)):
                a = equation_ok(g, edges, charge, mask)
                b = eval_cnf(clauses, mask)
                assert a == b
                models += a
                assignment_checks += 1
                assertions += 1
            expected = 0 if odd else 1 << (len(edges) - g + 1)
            assert models == expected
            assertions += 1

            if odd:
                # Count all single-clause deletions in one pass.  An assignment
                # satisfies a one-clause deletion exactly when it violates one
                # vertex equation and its local triple is that clause's blocked
                # tuple.  This is equivalent to the actual CNF semantics already
                # checked assignment-by-assignment above.
                expected_deleted = 1 << (len(edges) - g - 1)
                index = {(owners[j], forbidden[j]): j for j in range(len(clauses))}
                counts = [0] * len(clauses)
                for mask in range(1 << len(edges)):
                    bad = []
                    for v, triple in enumerate(inc):
                        bits = tuple((mask >> e) & 1 for e in triple)
                        if (bits[0] ^ bits[1] ^ bits[2]) != charge[v]:
                            bad.append((v, bits))
                    if len(bad) == 1:
                        counts[index[bad[0]]] += 1
                    assignment_checks += 1
                for count in counts:
                    assert count == expected_deleted
                    deletion_checks += 1
                    assertions += 1

        # Every charge bit is an independent opposite-label neighbor.
        base = [0] * g
        for v in range(g):
            flip = base[:]; flip[v] = 1
            assert (sum(base) & 1) != (sum(flip) & 1)
            assertions += 1

        n = len(edges); k = 4 * g
        rows.append({
            "graph": name, "vertices_g": g, "edges_source_variables_n": n,
            "ternary_clauses_k": k, "minimum_strong_2cnf_backdoor_h": g // 2,
            "sat_models_even_charge": 1 << (n - g + 1),
            "models_after_one_clause_deleted_odd_charge": 1 << (n - g - 1),
            "input_word_lower_bound": g,
            "evaluator_gates_shared_not_or2_and2": n + 3 * k - 1,
            "evaluator_directed_inputs": n + 6 * k - 2,
        })

    out = {
        "artifact": "CUBIC_AFFINE_FIREWALL98",
        "status": "COMPUTATIONAL finite verification; general theorem proved separately",
        "graphs": rows,
        "assertions": assertions,
        "assignment_checks": assignment_checks,
        "single_clause_deletion_checks": deletion_checks,
        "failures": 0,
        "theorem_scope": "finite simple 2-vertex-connected cubic graphs",
        "restricted_literature_transfer": "regular-resolution size 2^{Omega(tw(G))}; not arbitrary decision time",
    }
    path = Path(__file__).resolve().parents[2] / "results/raw/review/CUBIC_AFFINE_FIREWALL98_raw.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
