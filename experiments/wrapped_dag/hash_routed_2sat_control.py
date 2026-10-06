#!/usr/bin/env python3
"""
Hash-routed WRAPPED-DAG hostile control on planted 2-SAT.

Purpose:
  Demonstrate that very high route diversity can coexist with exact
  polynomial-time computation on an easy SAT family.

This is a computational control, not an asymptotic lower bound.
"""

from hashlib import blake2b
import math
import random
import json


def lit_var(l):
    return abs(l) - 1


def sat2(clauses, n, assign=None):
    assign = {} if assign is None else dict(assign)

    simplified = []
    for clause in clauses:
        live = []
        satisfied = False
        for lit in clause:
            v = lit_var(lit)
            if v in assign:
                val = assign[v]
                if (lit > 0 and val) or (lit < 0 and not val):
                    satisfied = True
                    break
            else:
                live.append(lit)
        if satisfied:
            continue
        if not live:
            return False
        simplified.append(tuple(live))

    g = [[] for _ in range(2 * n)]
    gr = [[] for _ in range(2 * n)]

    def idx(lit):
        v = lit_var(lit)
        return 2 * v + (0 if lit > 0 else 1)

    def add_imp(a, b):
        ia, ib = idx(a), idx(b)
        g[ia].append(ib)
        gr[ib].append(ia)

    for clause in simplified:
        if len(clause) == 1:
            a = clause[0]
            add_imp(-a, a)
        else:
            a, b = clause
            add_imp(-a, b)
            add_imp(-b, a)

    seen = [False] * (2 * n)
    order = []

    for start in range(2 * n):
        if seen[start]:
            continue
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            v, i = stack[-1]
            if i < len(g[v]):
                w = g[v][i]
                stack[-1] = (v, i + 1)
                if not seen[w]:
                    seen[w] = True
                    stack.append((w, 0))
            else:
                order.append(v)
                stack.pop()

    comp = [-1] * (2 * n)
    cid = 0
    for start in reversed(order):
        if comp[start] != -1:
            continue
        stack = [start]
        comp[start] = cid
        while stack:
            v = stack.pop()
            for w in gr[v]:
                if comp[w] == -1:
                    comp[w] = cid
                    stack.append(w)
        cid += 1

    for v in range(n):
        if comp[2 * v] == comp[2 * v + 1]:
            return False
    return True


def make_planted_2sat(n, m, seed=42):
    rng = random.Random(seed)
    planted = [bool(rng.randrange(2)) for _ in range(n)]
    clauses = []

    def eval_lit(lit):
        v = abs(lit) - 1
        return planted[v] if lit > 0 else not planted[v]

    for _ in range(m):
        i, j = rng.sample(range(n), 2)
        while True:
            a = (i + 1) * (1 if rng.randrange(2) else -1)
            b = (j + 1) * (1 if rng.randrange(2) else -1)
            if eval_lit(a) or eval_lit(b):
                clauses.append((a, b))
                break

    return clauses, planted


def run_wrapper(clauses, n, seed_int):
    assign = {}
    h = seed_int.to_bytes(8, "big")
    parent = sat2(clauses, n, assign)
    route = []
    calls = 1

    while len(assign) < n:
        unassigned = [v for v in range(n) if v not in assign]
        hh = blake2b(
            h + repr(sorted(assign.items())).encode("utf-8"),
            digest_size=8,
        ).digest()

        v = unassigned[int.from_bytes(hh, "big") % len(unassigned)]

        test = dict(assign)
        test[v] = False
        b0 = sat2(clauses, n, test)
        calls += 1

        bit = False if b0 == parent else True
        assign[v] = bit
        route.append((v, bit))

        h = blake2b(
            hh + bytes([v % 256, int(bit), int(b0), int(parent)]),
            digest_size=8,
        ).digest()

    return {
        "variable_order": tuple(v for v, _ in route),
        "assignment_bits": tuple(bit for _, bit in route),
        "sat_calls": calls,
        "final_sat": sat2(clauses, n, assign),
    }


def main():
    seeds = 4096
    rows = []

    for n in (8, 10, 12):
        clauses, planted = make_planted_2sat(n, 4 * n, seed=42)
        routes = set()
        correctness = 0
        calls = set()

        for seed in range(seeds):
            out = run_wrapper(clauses, n, seed)
            routes.add(out["variable_order"])
            calls.add(out["sat_calls"])
            correctness += int(out["final_sat"])

        rows.append(
            {
                "n": n,
                "seeds": seeds,
                "distinct_variable_order_routes": len(routes),
                "sat_calls_per_run": sorted(calls),
                "correct_runs": correctness,
                "max_possible_variable_orders": math.factorial(n),
            }
        )

    result = {
        "status": "COMPUTATIONAL_CONTROL",
        "claim": (
            "High hash-directed route diversity can coexist with exact "
            "polynomial-time computation on planted 2-SAT."
        ),
        "rows": rows,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
