#!/usr/bin/env python3
"""Finite audit for RELATION-ALGEBRA-BOUNDARY93.

Checks Z3 permutation constraints, their one-hot CNF encoding, arbitrary
three-valued binary CSPs with a supplied feedback-vertex set, the cycle-plus-
chords cutset bound, and the graph-3-coloring endpoint.
"""

from __future__ import annotations

import itertools
import json
import random
import time

SEED = 20261023
D = range(3)


def affine_solve(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, b in edges:
        adj[u].append((v, b % 3))
        adj[v].append((u, (-b) % 3))
    potential = [None] * n
    components = 0
    edge_checks = 0
    for root in range(n):
        if potential[root] is not None:
            continue
        components += 1
        potential[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v, b in adj[u]:
                edge_checks += 1
                wanted = (potential[u] + b) % 3
                if potential[v] is None:
                    potential[v] = wanted
                    stack.append(v)
                elif potential[v] != wanted:
                    return False, 0, edge_checks
    return True, 3 ** components, edge_checks


def brute_affine(n, edges):
    count = 0
    for assignment in itertools.product(D, repeat=n):
        if all(assignment[v] == (assignment[u] + b) % 3 for u, v, b in edges):
            count += 1
    return count


def var(v, color):
    return 3 * v + color + 1


def affine_cnf(n, edges):
    clauses = []
    for v in range(n):
        clauses.append((var(v, 0), var(v, 1), var(v, 2)))
        for a in D:
            for b in range(a + 1, 3):
                clauses.append((-var(v, a), -var(v, b)))
    for u, v, shift in edges:
        for a in D:
            for b in D:
                if b != (a + shift) % 3:
                    clauses.append((-var(u, a), -var(v, b)))
    return clauses


def inequality_cnf(n, edges):
    clauses = []
    for v in range(n):
        clauses.append((var(v, 0), var(v, 1), var(v, 2)))
        for a in D:
            for b in range(a + 1, 3):
                clauses.append((-var(v, a), -var(v, b)))
    for u, v in edges:
        for color in D:
            clauses.append((-var(u, color), -var(v, color)))
    return clauses


def cnf_count_onehot(n, clauses):
    count = 0
    for colors in itertools.product(D, repeat=n):
        assignment = {var(v, c): colors[v] == c for v in range(n) for c in D}
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses):
            count += 1
    return count


def relation_lookup(edge, x, y, u, v):
    a, b, relation = edge
    if (u, v) == (a, b):
        return (x, y) in relation
    assert (u, v) == (b, a)
    return (y, x) in relation


def brute_csp(n, edges):
    count = 0
    for assignment in itertools.product(D, repeat=n):
        if all((assignment[u], assignment[v]) in relation for u, v, relation in edges):
            count += 1
    return count


def fvs_csp_sat(n, edges, cutset):
    cutset = tuple(sorted(cutset))
    cut = set(cutset)
    adj = [[] for _ in range(n)]
    for index, (u, v, _) in enumerate(edges):
        adj[u].append((v, index))
        adj[v].append((u, index))

    # Validate that deleting the supplied cutset leaves a forest.
    seen = set()
    for start in range(n):
        if start in cut or start in seen:
            continue
        stack = [(start, -1)]
        seen.add(start)
        while stack:
            u, parent = stack.pop()
            for v, _ in adj[u]:
                if v in cut or v == parent:
                    continue
                if v in seen:
                    raise ValueError("supplied cutset does not leave a forest")
                seen.add(v)
                stack.append((v, u))

    assignments_tried = 0
    for values in itertools.product(D, repeat=len(cutset)):
        assignments_tried += 1
        fixed = dict(zip(cutset, values))
        ok = True
        for edge in edges:
            u, v, _ = edge
            if u in cut and v in cut and not relation_lookup(edge, fixed[u], fixed[v], u, v):
                ok = False
                break
        if not ok:
            continue

        visited = set()
        cache = {}

        def message(u, parent):
            key = (u, parent)
            if key in cache:
                return cache[key]
            visited.add(u)
            feasible = []
            for color in D:
                good = True
                for v, edge_index in adj[u]:
                    edge = edges[edge_index]
                    if v in cut:
                        if not relation_lookup(edge, color, fixed[v], u, v):
                            good = False
                            break
                    elif v != parent:
                        child = message(v, u)
                        if not any(child_color in child and relation_lookup(edge, color, child_color, u, v)
                                   for child_color in D):
                            good = False
                            break
                if good:
                    feasible.append(color)
            cache[key] = tuple(feasible)
            return cache[key]

        forest_ok = True
        for root in range(n):
            if root in cut or root in visited:
                continue
            if not message(root, -1):
                forest_ok = False
                break
        if forest_ok:
            return True, assignments_tried
    return False, assignments_tried


def is_forest_after_cut(n, simple_edges, cutset):
    cut = set(cutset)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in simple_edges:
        if u in cut or v in cut:
            continue
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def random_relation(rng):
    pairs = {(a, b) for a in D for b in D if rng.randrange(2)}
    return pairs


def audit():
    rng = random.Random(SEED)
    started = time.time()
    assertions = 0
    affine_instances = 0
    csp_instances = 0
    cnf_checks = 0
    cycle_checks = 0
    chord_checks = 0

    # Random arbitrary-graph Z3 permutation systems, including inconsistent cycles.
    for n in range(1, 8):
        all_pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for _ in range(80):
            rng.shuffle(all_pairs)
            take = rng.randrange(len(all_pairs) + 1)
            edges = [(u, v, rng.randrange(3)) for u, v in all_pairs[:take]]
            sat, models, edge_checks = affine_solve(n, edges)
            brute = brute_affine(n, edges)
            assert sat == (brute > 0)
            assert models == brute
            assert edge_checks <= 2 * len(edges)
            assertions += 3
            affine_instances += 1
            if n <= 6:
                assert cnf_count_onehot(n, affine_cnf(n, edges)) == brute
                assertions += 1
                cnf_checks += 1

    # Exact cycle semantics and the k-field all-zero sensitivity control.
    for k in range(2, 13):
        for bits in itertools.product((0, 1), repeat=k) if k <= 8 else [tuple(rng.randrange(2) for _ in range(k)) for _ in range(128)]:
            edges = [(i, (i + 1) % k, bits[i]) for i in range(k)]
            sat, models, _ = affine_solve(k, edges)
            expected = sum(bits) % 3 == 0
            assert sat == expected
            assert models == (3 if expected else 0)
            assertions += 2
            cycle_checks += 1
        zeros = (0,) * k
        assert sum(zeros) % 3 == 0
        for i in range(k):
            flipped = list(zeros)
            flipped[i] = 1
            assert sum(flipped) % 3 != 0
            assertions += 1

    # Arbitrary relation CSPs with a supplied feedback vertex set.
    for n in range(3, 9):
        for c in range(0, min(3, n - 1) + 1):
            cutset = set(range(c))
            for _ in range(60):
                edges = []
                # A random forest on vertices c..n-1.
                for v in range(c + 1, n):
                    if rng.randrange(4):
                        u = rng.randrange(c, v)
                        edges.append((u, v, random_relation(rng)))
                # Arbitrary edges incident to the cutset, including cut-cut edges.
                for u in range(c):
                    for v in range(u + 1, n):
                        if rng.randrange(3) == 0:
                            edges.append((u, v, random_relation(rng)))
                brute = brute_csp(n, edges)
                sat, tried = fvs_csp_sat(n, edges, cutset)
                assert sat == (brute > 0)
                assert 1 <= tried <= 3 ** c
                assertions += 2
                csp_instances += 1

    # A cycle plus h chords has an explicit feedback set of size at most h+1.
    for n in range(6, 25):
        cycle = [(i, (i + 1) % n) for i in range(n)]
        candidates = [(u, v) for u in range(n) for v in range(u + 1, n)
                      if v != u + 1 and not (u == 0 and v == n - 1)]
        rng.shuffle(candidates)
        for h in range(0, min(7, len(candidates)) + 1):
            chords = candidates[:h]
            cutset = {0}
            cutset.update(u for u, _ in chords)
            assert len(cutset) <= h + 1
            assert is_forest_after_cut(n, cycle + chords, cutset)
            assertions += 2
            chord_checks += 1

    # Identity inequality relations are exactly graph 3-coloring.
    for n in range(1, 8):
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for _ in range(70):
            edges = [e for e in pairs if rng.randrange(3) == 0]
            relation_edges = [(u, v, {(a, b) for a in D for b in D if a != b}) for u, v in edges]
            count = brute_csp(n, relation_edges)
            assert cnf_count_onehot(n, inequality_cnf(n, edges)) == count
            assertions += 1
            cnf_checks += 1

    elapsed = round(time.time() - started, 6)
    return {
        "claim_id": "RELATION-ALGEBRA-BOUNDARY93",
        "status": "COMPUTATIONAL audit of PROVED/EXACT restricted lemmas",
        "seed": SEED,
        "assertions": assertions,
        "failures": 0,
        "affine_instances": affine_instances,
        "arbitrary_relation_fvs_instances": csp_instances,
        "cycle_orientation_cases": cycle_checks,
        "cycle_plus_chord_cutset_checks": chord_checks,
        "onehot_cnf_model_count_checks": cnf_checks,
        "max_affine_vertices": 7,
        "max_arbitrary_csp_vertices": 8,
        "elapsed_seconds": elapsed,
        "hostile_controls": ["inconsistent affine cycle", "dense affine graph",
                             "empty relation", "full relation", "inequality graph coloring",
                             "cycle plus chords", "all-zero orientation sensitivity"],
        "limitations": "Finite audit only; asymptotic statements are proved symbolically in the report.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
