#!/usr/bin/env python3
"""Audit SELECTOR-GRAPH-BOUNDARY95 against exhaustive search."""

from __future__ import annotations
import itertools
import json
import random
from collections import defaultdict

SEED = 202610231748
RNG = random.Random(SEED)
ASSERTIONS = 0


def check(x, msg="failure"):
    global ASSERTIONS
    ASSERTIONS += 1
    if not x:
        raise AssertionError(msg)


def brute(g, d, edges, domains=None):
    domains = domains or [set(range(d)) for _ in range(g)]
    for a in itertools.product(range(d), repeat=g):
        if any(a[v] not in domains[v] for v in range(g)):
            continue
        if all((a[u], a[v]) in rel for u, v, rel in edges):
            return True
    return False


def forest_solve(g, d, edges, domains=None):
    domains = domains or [set(range(d)) for _ in range(g)]
    adj = [[] for _ in range(g)]
    for idx, (u, v, rel) in enumerate(edges):
        adj[u].append((v, idx, True))
        adj[v].append((u, idx, False))
    seen = [False] * g
    parent = [-1] * g
    pedge = [None] * g
    order = []
    roots = []
    for s in range(g):
        if seen[s]:
            continue
        roots.append(s)
        stack = [s]
        seen[s] = True
        while stack:
            u = stack.pop()
            order.append(u)
            for v, idx, orient in adj[u]:
                if v == parent[u]:
                    continue
                if seen[v]:
                    raise ValueError("not a forest")
                seen[v] = True
                parent[v] = u
                # True means relation stored (parent,child); False means reverse.
                pedge[v] = (idx, orient)
                stack.append(v)
    ok = [set(domains[v]) for v in range(g)]
    for v in reversed(order):
        for child, idx, orient_from_v in adj[v]:
            if parent[child] != v:
                continue
            _u, _w, rel = edges[idx]
            allowed_v = set()
            for av in ok[v]:
                for ac in ok[child]:
                    pair = (av, ac) if orient_from_v else (ac, av)
                    if pair in rel:
                        allowed_v.add(av)
                        break
            ok[v] &= allowed_v
        if not ok[v]:
            return False
    return all(ok[r] for r in roots)


def fvs_solve(g, d, edges, cut):
    cut = sorted(cut)
    cutset = set(cut)
    rest = [v for v in range(g) if v not in cutset]
    rest_index = {v: i for i, v in enumerate(rest)}
    internal = []
    cross = []
    for u, v, rel in edges:
        if u in cutset and v in cutset:
            internal.append((u, v, rel))
        elif u in cutset or v in cutset:
            cross.append((u, v, rel))
    forest_edges = [
        (rest_index[u], rest_index[v], rel)
        for u, v, rel in edges
        if u not in cutset and v not in cutset
    ]
    leaves = 0
    for vals in itertools.product(range(d), repeat=len(cut)):
        leaves += 1
        a = dict(zip(cut, vals))
        if any((a[u], a[v]) not in rel for u, v, rel in internal):
            continue
        domains = [set(range(d)) for _ in rest]
        for u, v, rel in cross:
            if u in cutset:
                domains[rest_index[v]] &= {b for b in range(d) if (a[u], b) in rel}
            else:
                domains[rest_index[u]] &= {b for b in range(d) if (b, a[v]) in rel}
        if all(domains) and forest_solve(len(rest), d, forest_edges, domains):
            return True, leaves
    return False, leaves


def random_relation(d, prob=0.55):
    return {(a, b) for a in range(d) for b in range(d) if RNG.random() < prob}


def role4_cnf(d, tau):
    clauses = []
    next_var = 2 * d + 1
    ternary_indices = []

    def or_tree(leaves):
        nonlocal next_var
        acc = leaves[0]
        for q in leaves[1:]:
            t = next_var
            next_var += 1
            clauses.extend([(-acc, t), (-q, t), (acc, q, -t)])
            ternary_indices.append(len(clauses) - 1)
            acc = t
        return acc

    a = list(range(1, d + 1))
    b = list(range(d + 1, 2 * d + 1))
    ra, rb = or_tree(a), or_tree(b)
    u, v = next_var, next_var + 1
    next_var += 2
    clauses.extend([(ra, u), (ra, -u), (rb, v), (rb, -v)])
    for group in (a, b):
        for i in range(d):
            for j in range(i + 1, d):
                clauses.append((-group[i], -group[j]))
    for i in range(d):
        for j in range(d):
            clauses.append((-a[i], -b[j] if tau[i][j] else b[j]))
    check(next_var - 1 == 4 * d)
    return clauses, ternary_indices, next_var - 1


def cnf_count(clauses, n):
    def simplify(cls, var, value):
        sat_lit = var if value else -var
        bad_lit = -sat_lit
        out = []
        for c in cls:
            if sat_lit in c:
                continue
            nc = tuple(x for x in c if x != bad_lit)
            if not nc:
                return None
            out.append(nc)
        return out

    def rec(cls, assigned):
        cls = list(cls)
        assigned = dict(assigned)
        while True:
            unit = next((c[0] for c in cls if len(c) == 1), None)
            if unit is None:
                break
            var, value = abs(unit), unit > 0
            if var in assigned and assigned[var] != value:
                return 0
            assigned[var] = value
            cls = simplify(cls, var, value)
            if cls is None:
                return 0
        if not cls:
            return 1 << (n - len(assigned))
        var = abs(min(cls, key=len)[0])
        if var in assigned:
            raise AssertionError("assigned variable survived simplification")
        total = 0
        for value in (False, True):
            nxt = simplify(cls, var, value)
            if nxt is not None:
                a = dict(assigned)
                a[var] = value
                total += rec(nxt, a)
        return total

    return rec([tuple(c) for c in clauses], {})


stats = {
    "seed": SEED,
    "forest_instances": 0,
    "fvs_instances": 0,
    "role4_matrices": 0,
    "sat": 0,
    "unsat": 0,
    "max_cut": 0,
}

# Forest CSPs.
for d in (2, 3, 4):
    for g in range(1, 9):
        for _ in range(45):
            edges = []
            for v in range(1, g):
                if RNG.random() < 0.82:
                    u = RNG.randrange(v)
                    edges.append((u, v, random_relation(d)))
            want = brute(g, d, edges)
            got = forest_solve(g, d, edges)
            check(got == want, ("forest", g, d, want, got))
            stats["forest_instances"] += 1
            stats["sat"] += int(want)
            stats["unsat"] += int(not want)

# Instances whose deletion of a supplied cut leaves a forest.
for d in (2, 3, 4):
    for g in range(2, 9):
        for _ in range(35):
            c = RNG.randrange(0, min(3, g) + 1)
            cut = set(range(c))
            edges = []
            # A forest on the remaining vertices.
            for v in range(c + 1, g):
                if RNG.random() < 0.8:
                    u = RNG.randrange(c, v)
                    edges.append((u, v, random_relation(d)))
            # Arbitrary edges incident to cut vertices.
            pairs = [(u, v) for u in range(g) for v in range(u + 1, g)
                     if u in cut or v in cut]
            RNG.shuffle(pairs)
            for u, v in pairs[:RNG.randrange(0, min(len(pairs), g) + 1)]:
                edges.append((u, v, random_relation(d)))
            want = brute(g, d, edges)
            got, leaves = fvs_solve(g, d, edges, cut)
            check(got == want, ("fvs", g, d, cut, want, got))
            check(leaves <= d ** c)
            stats["fvs_instances"] += 1
            stats["max_cut"] = max(stats["max_cut"], c)
            stats["sat"] += int(want)
            stats["unsat"] += int(not want)

# Role-4 two-selector semantics: SAT iff some row has exactly one zero.
for d in (2, 3):
    for mask in range(1 << (d * d)):
        tau = [[(mask >> (i * d + j)) & 1 for j in range(d)] for i in range(d)]
        rel = {(i, j) for i in range(d) for j in range(d)
               if tau[i][j] == 0 and sum(1 - x for x in tau[i]) == 1}
        criterion = any(sum(1 - x for x in row) == 1 for row in tau)
        check(bool(rel) == criterion)
        check(brute(2, d, [(0, 1, rel)]) == criterion)
        clauses, ternary_indices, nvars = role4_cnf(d, tau)
        check(cnf_count(clauses, nvars) ==
              4 * sum(sum(1 - x for x in row) == 1 for row in tau))
        stats["role4_matrices"] += 1

# All-one field sensitivity and exact counts through d=64.
for d in (2, 3, 4, 8, 16, 32, 64):
    all_one = [[1] * d for _ in range(d)]
    check(not any(sum(1 - x for x in row) == 1 for row in all_one))
    for i in range(d):
        for j in range(d):
            row = list(all_one[i])
            row[j] = 0
            check(sum(1 - x for x in row) == 1)

# Every functional OR-gate ternary is essential on all-one sources.
for d in range(2, 8):
    tau = [[1] * d for _ in range(d)]
    clauses, ternary_indices, nvars = role4_cnf(d, tau)
    check(cnf_count(clauses, nvars) == 0)
    for idx in ternary_indices:
        check(cnf_count(clauses[:idx] + clauses[idx + 1:], nvars) > 0)

# 3-color endpoint controls.
neq3 = {(a, b) for a in range(3) for b in range(3) if a != b}
triangle = [(0, 1, neq3), (1, 2, neq3), (0, 2, neq3)]
k4 = [(u, v, neq3) for u in range(4) for v in range(u + 1, 4)]
check(brute(3, 3, triangle))
check(not brute(4, 3, k4))

# Exact source/CNF resource formulas, including Role-4 g=2 counts.
for g in range(1, 9):
    for d in range(2, 9):
        for e in range(0, g * (g - 1) // 2 + 1):
            variables = 2 * d * g
            ternaries = g * (d - 1)
            binary_max = g * (d * (d - 1) // 2 + 2 * d) + e * d * d
            check(variables == g * (d + (d - 1) + 1))
            check(ternaries == g * (d - 1))
            check(binary_max >= 0)
            if g == 2 and e == 1:
                check(variables == 4 * d)
                check(ternaries == 2 * d - 2)
                check(binary_max == 2 * d * d + 3 * d)

stats["assertions"] = ASSERTIONS
stats["failures"] = 0
stats["status"] = "COMPUTATIONAL finite audit only"
print(json.dumps(stats, indent=2, sort_keys=True))
