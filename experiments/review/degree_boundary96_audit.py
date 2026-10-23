#!/usr/bin/env python3
"""Exact finite audit for DEGREE-BOUNDARY96.

Stdlib only.  All randomized controls use seed 202610231848.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path

SEED = 202610231848
rng = random.Random(SEED)


def degrees(n, edges):
    d = [0] * n
    for u, v in edges:
        assert 0 <= u < v < n
        d[u] += 1
        d[v] += 1
    return d


def components(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s]:
            continue
        stack = [s]
        seen[s] = True
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        out.append(comp)
    return out


def has_k4_component(n, edges):
    eset = set(edges)
    for comp in components(n, edges):
        if len(comp) != 4:
            continue
        if all((min(u, v), max(u, v)) in eset for u, v in itertools.combinations(comp, 2)):
            return True
    return False


def color_count(n, edges, stop_after=None):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    color = [-1] * n
    count = 0

    def rec(done):
        nonlocal count
        if stop_after is not None and count >= stop_after:
            return
        if done == n:
            count += 1
            return
        uncolored = [v for v in range(n) if color[v] < 0]
        v = max(uncolored, key=lambda x: (len({color[y] for y in adj[x] if color[y] >= 0}), len(adj[x])))
        forbidden = {color[y] for y in adj[v] if color[y] >= 0}
        for c in range(3):
            if c not in forbidden:
                color[v] = c
                rec(done + 1)
                color[v] = -1
    rec(0)
    return count


def one_hot_clauses(n, edges):
    # Variables are 0..3n-1; positive literal x is x+1, negative is -(x+1).
    clauses = []
    for v in range(n):
        xs = [3 * v + c for c in range(3)]
        clauses.append(tuple(x + 1 for x in xs))
        for a, b in itertools.combinations(xs, 2):
            clauses.append((-(a + 1), -(b + 1)))
    for u, v in edges:
        for c in range(3):
            clauses.append((-(3 * u + c + 1), -(3 * v + c + 1)))
    return clauses


def cnf_model_count(num_vars, clauses):
    ans = 0
    for mask in range(1 << num_vars):
        ok = True
        for clause in clauses:
            if not any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                ok = False
                break
        ans += ok
    return ans


COMMON = ((0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def block_family(p, flipped=None):
    # Edge-record 0 of each six-vertex block is the only varying record.
    edges = []
    special_indices = []
    for i in range(p):
        off = 6 * i
        special_indices.append(len(edges))
        special = (off, off + 1) if flipped == i else (off + 4, off + 5)
        edges.append(special)
        edges.extend((off + u, off + v) for u, v in COMMON)
    return 6 * p, tuple(edges), tuple(special_indices)


def all_graphs(n):
    pairs = list(itertools.combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield tuple(pairs[i] for i in range(len(pairs)) if (mask >> i) & 1)


def main():
    assertions = 0
    degree3_graphs = 0
    degree3_sat = 0
    degree3_unsat = 0
    exhaustive_by_n = {}
    for n in range(1, 7):
        kept = sat = unsat = 0
        for edges in all_graphs(n):
            if max(degrees(n, edges), default=0) > 3:
                continue
            kept += 1
            actual = color_count(n, edges, stop_after=1) > 0
            criterion = not has_k4_component(n, edges)
            assert actual == criterion
            assertions += 1
            sat += actual
            unsat += not actual
        exhaustive_by_n[str(n)] = {"degree_at_most_3": kept, "sat": sat, "unsat": unsat}
        degree3_graphs += kept
        degree3_sat += sat
        degree3_unsat += unsat

    # Parsimonious one-hot encoding on every graph through four vertices.
    cnf_graphs = cnf_assignments = 0
    for n in range(1, 5):
        for edges in all_graphs(n):
            cc = color_count(n, edges)
            clauses = one_hot_clauses(n, edges)
            mc = cnf_model_count(3 * n, clauses)
            assert cc == mc
            assert len(clauses) == 4 * n + 3 * len(edges)
            assertions += 2
            cnf_graphs += 1
            cnf_assignments += 1 << (3 * n)

    family_rows = []
    family_flips = 0
    for p in [1, 2, 3, 4, 8, 16, 32, 64]:
        n, base, slots = block_family(p)
        assert len(base) == 6 * p
        assert max(degrees(n, base)) == 3
        assert not has_k4_component(n, base)
        if p <= 8:
            assert color_count(n, base, stop_after=1) == 1
        assertions += 4
        for i in range(p):
            n2, alt, slots2 = block_family(p, i)
            assert n2 == n and len(alt) == len(base) and slots2 == slots
            diffs = [j for j, (x, y) in enumerate(zip(base, alt)) if x != y]
            assert diffs == [slots[i]]
            assert max(degrees(n, alt)) == 3
            assert has_k4_component(n, alt)
            if p <= 4:
                assert color_count(n, alt, stop_after=1) == 0
                assertions += 1
            assertions += 4
            family_flips += 1
        endpoint_bits = math.ceil(math.log2(n + 1))
        packed_word_bits = 2 * endpoint_bits
        encoded_bits = (len(base) + 2) * packed_word_bits
        family_rows.append({
            "p": p,
            "vertices": n,
            "edges": len(base),
            "max_degree": 3,
            "critical_packed_edge_words": p,
            "packed_word_bits": packed_word_bits,
            "encoded_bits": encoded_bits,
            "word_lower_bound_fraction": p / (len(base) + 2),
        })

    # Random degree-3 controls up to 18 vertices, compared with exact DSATUR.
    random_controls = 0
    for n in range(7, 19):
        for _ in range(80):
            pairs = list(itertools.combinations(range(n), 2))
            rng.shuffle(pairs)
            edges = []
            deg = [0] * n
            for u, v in pairs:
                if deg[u] < 3 and deg[v] < 3 and rng.random() < 0.12:
                    edges.append((u, v)); deg[u] += 1; deg[v] += 1
            actual = color_count(n, tuple(edges), stop_after=1) > 0
            assert actual == (not has_k4_component(n, tuple(edges)))
            assertions += 1
            random_controls += 1

    # Degree-four both-label endpoint controls (not evidence of NP-hardness).
    star = tuple((0, i) for i in range(1, 5))
    k5 = tuple(itertools.combinations(range(5), 2))
    assert max(degrees(5, star)) == 4 and color_count(5, star, stop_after=1) == 1
    assert max(degrees(5, k5)) == 4 and color_count(5, k5, stop_after=1) == 0
    assertions += 4

    out = {
        "run_id": "DEGREE-BOUNDARY96",
        "seed": SEED,
        "status": "COMPUTATIONAL implementation evidence only",
        "assertions": assertions,
        "failures": 0,
        "degree3_exhaustive": {
            "n_max": 6,
            "graphs": degree3_graphs,
            "sat": degree3_sat,
            "unsat": degree3_unsat,
            "by_n": exhaustive_by_n,
        },
        "one_hot_cnf": {"graphs": cnf_graphs, "boolean_assignments_checked": cnf_assignments},
        "critical_family": {"flips_checked": family_flips, "rows": family_rows},
        "random_degree3_controls": random_controls,
        "degree4_controls": {"sat_star_K1_4": True, "unsat_K5": True},
        "limitations": [
            "Finite tests do not prove Brooks theorem or NP-completeness.",
            "The lower bound is for explicit packed edge-record/bit queries, not unrestricted model-free time.",
            "No experiment establishes mandatory exponential continuation.",
        ],
    }
    out_path = Path("results/raw/review/DEGREE_BOUNDARY96_raw.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
