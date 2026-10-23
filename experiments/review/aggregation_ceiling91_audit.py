#!/usr/bin/env python3
"""Finite audit for AGGREGATION-CEILING91.

Checks the guarded activation CNF against its source read-once AND/OR
semantics, exact encoding counts, full multilinear degree, and exact
deterministic decision-tree depth on small instances.  Finite evidence only.
"""

from __future__ import annotations

import functools
import itertools
import json
import time


def tree_shape(p, gates):
    """Balanced full tree on p=1,2,4 leaves, gates in preorder."""
    gate_iter = iter(gates)

    def rec(lo, hi):
        if hi - lo == 1:
            return ("leaf", lo)
        op = next(gate_iter)
        mid = (lo + hi) // 2
        return (op, rec(lo, mid), rec(mid, hi))

    return rec(0, p)


def eval_tree(tree, values):
    if tree[0] == "leaf":
        return values[tree[1]]
    a = eval_tree(tree[1], values)
    b = eval_tree(tree[2], values)
    return (a and b) if tree[0] == "and" else (a or b)


def count_nodes(tree):
    if tree[0] == "leaf":
        return 1, 0, 0
    l = count_nodes(tree[1])
    r = count_nodes(tree[2])
    return (
        1 + l[0] + r[0],
        (1 if tree[0] == "and" else 0) + l[1] + r[1],
        (1 if tree[0] == "or" else 0) + l[2] + r[2],
    )


def guarded_cnf(tree, p, q, bits):
    next_var = 1
    z = []
    for _ in range(p):
        row = list(range(next_var, next_var + q + 1))
        next_var += q + 1
        z.append(row)

    activation = {}

    def allocate(node):
        nonlocal next_var
        activation[id(node)] = next_var
        next_var += 1
        if node[0] != "leaf":
            allocate(node[1])
            allocate(node[2])

    allocate(tree)
    clauses = [[activation[id(tree)]]]

    def emit(node):
        a = activation[id(node)]
        if node[0] == "leaf":
            j = node[1]
            clauses.append([-a, z[j][0]])
            clauses.append([-a, -z[j][q]])
            for i in range(1, q + 1):
                if bits[j * q + i - 1]:
                    clauses.append([-a, -z[j][i - 1], z[j][i]])
                else:
                    clauses.append([-a, -z[j][i - 1], -z[j][i]])
            return
        al = activation[id(node[1])]
        ar = activation[id(node[2])]
        if node[0] == "and":
            clauses.extend([[-a, al], [-a, ar]])
        else:
            clauses.append([-a, al, ar])
        emit(node[1])
        emit(node[2])

    emit(tree)
    return clauses, next_var - 1


def dpll_sat(clauses):
    clauses = tuple(tuple(c) for c in clauses)

    def rec(current):
        current = [list(c) for c in current]
        while True:
            if any(len(c) == 0 for c in current):
                return False
            if not current:
                return True
            unit = next((c[0] for c in current if len(c) == 1), None)
            if unit is None:
                break
            nxt = []
            for c in current:
                if unit in c:
                    continue
                nxt.append([x for x in c if x != -unit])
            current = nxt
        lit = min(current, key=len)[0]
        for chosen in (lit, -lit):
            nxt = []
            for c in current:
                if chosen in c:
                    continue
                nxt.append([x for x in c if x != -chosen])
            if rec(nxt):
                return True
        return False

    return rec(clauses)


def source_value(tree, p, q, bits):
    leaf_values = []
    for j in range(p):
        block = bits[j * q : (j + 1) * q]
        leaf_values.append(not all(block))
    return bool(eval_tree(tree, leaf_values))


def truth_table(tree, p, q):
    m = p * q
    return tuple(
        int(source_value(tree, p, q, tuple((mask >> i) & 1 for i in range(m))))
        for mask in range(1 << m)
    )


def full_degree_coefficient(table, m):
    return sum(
        ((-1) ** (m - mask.bit_count())) * table[mask]
        for mask in range(1 << m)
    )


def exact_decision_depth(table, m):
    full = (1 << (1 << m)) - 1

    @functools.lru_cache(None)
    def rec(zero_mask, one_mask):
        possible = []
        for x in range(1 << m):
            if (x & zero_mask) or ((~x) & one_mask):
                continue
            possible.append(table[x])
        if not possible or all(v == possible[0] for v in possible):
            return 0
        best = m + 1
        assigned = zero_mask | one_mask
        for i in range(m):
            bit = 1 << i
            if assigned & bit:
                continue
            best = min(best, 1 + max(rec(zero_mask | bit, one_mask), rec(zero_mask, one_mask | bit)))
        return best

    del full
    return rec(0, 0)


def main():
    started = time.time()
    counters = {
        "artifact": "AGGREGATION_CEILING91",
        "assertions": 0,
        "failures": 0,
        "cnf_semantic_cases": 0,
        "sat_cases": 0,
        "unsat_cases": 0,
        "exact_decision_tree_cases": 0,
        "full_degree_checks": 0,
    }

    def check(cond, label):
        counters["assertions"] += 1
        if not cond:
            counters["failures"] += 1
            raise AssertionError(label)

    suites = []
    for p, qmax in ((1, 7), (2, 5), (4, 3)):
        internal = p - 1
        patterns = list(itertools.product(("and", "or"), repeat=internal))
        for q in range(1, qmax + 1):
            for gates in patterns:
                suites.append((p, q, gates))

    for p, q, gates in suites:
        tree = tree_shape(p, gates)
        nodes, i_and, i_or = count_nodes(tree)
        check(nodes == 2 * p - 1, "node count")
        check(i_and + i_or == p - 1, "internal count")
        expected_vars = p * q + 3 * p - 1
        expected_clauses = 1 + 2 * i_and + i_or + p * (q + 2)
        for raw in range(1 << (p * q)):
            bits = tuple((raw >> i) & 1 for i in range(p * q))
            clauses, nvars = guarded_cnf(tree, p, q, bits)
            got = dpll_sat(clauses)
            want = source_value(tree, p, q, bits)
            check(got == want, "guarded CNF semantics")
            check(nvars == expected_vars, "variable count")
            check(len(clauses) == expected_clauses, "clause count")
            check(max(map(len, clauses)) <= 3, "width at most three")
            counters["cnf_semantic_cases"] += 1
            counters["sat_cases" if got else "unsat_cases"] += 1

        m = p * q
        if m <= 8:
            table = truth_table(tree, p, q)
            coeff = full_degree_coefficient(table, m)
            check(coeff != 0, "full degree coefficient")
            counters["full_degree_checks"] += 1
            depth = exact_decision_depth(table, m)
            check(depth == m, "exact deterministic query depth")
            counters["exact_decision_tree_cases"] += 1

    counters["elapsed_seconds"] = round(time.time() - started, 6)
    counters["scope"] = "finite audit only; symbolic proof establishes the exact asymptotic query statement"
    print(json.dumps(counters, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
