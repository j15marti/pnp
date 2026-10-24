#!/usr/bin/env python3
"""Exact audit for the affine excess-nullity parameter K.

An instance consists of disjoint affine components.  Each source variable
has an affine expression in the component's basis bits, and the components
are coupled by unit/binary clauses.  The generic algorithm fixes all but one
basis bit per component and solves the resulting 2-CNF.  A hybrid policy
instead solves components independently when the binary-clause interaction
graph is edgeless.

Standard library only; deterministic seed; designed to finish in <30 s.
"""
from __future__ import annotations

import itertools
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

SEED = 202610241048
RAW = Path("AFFINE_EXCESS_NULLITY111_raw.json")


@dataclass(frozen=True)
class Expr:
    component: int
    constant: int
    coeffs: tuple[int, ...]


@dataclass
class Instance:
    dims: list[int]
    exprs: list[Expr]
    clauses: list[tuple[int, ...]]  # signed 1-based variable ids


def eval_lit(lit: int, values: list[int]) -> bool:
    value = bool(values[abs(lit) - 1])
    return value if lit > 0 else not value


def eval_source(inst: Instance, bases: list[tuple[int, ...]]) -> bool:
    values = []
    for e in inst.exprs:
        val = e.constant
        for a, b in zip(e.coeffs, bases[e.component]):
            val ^= a & b
        values.append(val)
    return all(any(eval_lit(lit, values) for lit in clause)
               for clause in inst.clauses)


def brute_decide(inst: Instance) -> bool:
    spaces = [list(itertools.product((0, 1), repeat=d)) for d in inst.dims]
    return any(eval_source(inst, list(bases))
               for bases in itertools.product(*spaces))


def two_sat(num_vars: int, clauses: list[tuple[int, ...]]) -> bool:
    """SCC decision for clauses of length at most two."""
    graph = [[] for _ in range(2 * num_vars)]
    reverse = [[] for _ in range(2 * num_vars)]

    def node(lit: int) -> int:
        v = abs(lit) - 1
        return 2 * v + (0 if lit > 0 else 1)

    def neg(x: int) -> int:
        return x ^ 1

    for clause in clauses:
        if not clause:
            return False
        a = clause[0]
        b = clause[0] if len(clause) == 1 else clause[1]
        na, nb = node(a), node(b)
        for u, v in ((neg(na), nb), (neg(nb), na)):
            graph[u].append(v)
            reverse[v].append(u)

    seen = [False] * (2 * num_vars)
    order: list[int] = []

    def dfs1(start: int) -> None:
        stack = [(start, 0)]
        seen[start] = True
        while stack:
            u, j = stack[-1]
            if j < len(graph[u]):
                v = graph[u][j]
                stack[-1] = (u, j + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

    for u in range(2 * num_vars):
        if not seen[u]:
            dfs1(u)

    comp = [-1] * (2 * num_vars)
    cid = 0
    for start in reversed(order):
        if comp[start] >= 0:
            continue
        comp[start] = cid
        stack = [start]
        while stack:
            u = stack.pop()
            for v in reverse[u]:
                if comp[v] < 0:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return all(comp[2 * v] != comp[2 * v + 1] for v in range(num_vars))


def substitute_child(inst: Instance, excess_values: tuple[int, ...]):
    offsets = []
    cursor = 0
    for d in inst.dims:
        offsets.append(cursor)
        cursor += max(d - 1, 0)
    rep_id = {}
    for i, d in enumerate(inst.dims):
        if d:
            rep_id[i] = len(rep_id) + 1

    transformed: list[tuple[int, ...]] = []
    for clause in inst.clauses:
        out: list[int] = []
        satisfied = False
        for lit in clause:
            e = inst.exprs[abs(lit) - 1]
            val = e.constant
            for j in range(max(inst.dims[e.component] - 1, 0)):
                val ^= e.coeffs[j] & excess_values[offsets[e.component] + j]
            if inst.dims[e.component] == 0 or e.coeffs[-1] == 0:
                truth = bool(val)
                truth = truth if lit > 0 else not truth
                if truth:
                    satisfied = True
                    break
            else:
                # Source variable = val XOR representative bit.
                positive_when_rep_one = (val == 0)
                if lit < 0:
                    positive_when_rep_one = not positive_when_rep_one
                out.append(rep_id[e.component] if positive_when_rep_one
                           else -rep_id[e.component])
        if satisfied:
            continue
        if len(out) == 2 and out[0] == -out[1]:
            continue
        if len(out) == 2 and out[0] == out[1]:
            out.pop()
        transformed.append(tuple(out))
    return len(rep_id), transformed


def excess_decide(inst: Instance):
    k = sum(max(d - 1, 0) for d in inst.dims)
    scc_calls = 0
    for excess in itertools.product((0, 1), repeat=k):
        nv, clauses = substitute_child(inst, excess)
        scc_calls += 1
        if two_sat(nv, clauses):
            return True, {"K": k, "children": scc_calls, "scc_calls": scc_calls}
    return False, {"K": k, "children": scc_calls, "scc_calls": scc_calls}


def interaction_edges(inst: Instance) -> set[tuple[int, int]]:
    edges = set()
    for clause in inst.clauses:
        comps = {inst.exprs[abs(lit) - 1].component for lit in clause}
        if len(comps) == 2:
            a, b = sorted(comps)
            edges.add((a, b))
    return edges


def local_component_decide(inst: Instance) -> bool:
    """Exact only when no clause crosses affine components."""
    if interaction_edges(inst):
        raise ValueError("cross-component clause")
    by_comp = [[] for _ in inst.dims]
    for clause in inst.clauses:
        cset = {inst.exprs[abs(lit) - 1].component for lit in clause}
        if not cset:
            return False
        by_comp[next(iter(cset))].append(clause)
    for i, d in enumerate(inst.dims):
        ok = False
        for basis in itertools.product((0, 1), repeat=d):
            bases = [tuple(0 for _ in range(dd)) for dd in inst.dims]
            bases[i] = basis
            # Only component-i clauses are evaluated.
            values = []
            for e in inst.exprs:
                val = e.constant
                for a, b in zip(e.coeffs, bases[e.component]):
                    val ^= a & b
                values.append(val)
            if all(any(eval_lit(lit, values) for lit in cl)
                   for cl in by_comp[i]):
                ok = True
                break
        if not ok:
            return False
    return True


def make_random(rng: random.Random) -> Instance:
    c = rng.randint(1, 4)
    dims = [rng.randint(0, 3) for _ in range(c)]
    exprs: list[Expr] = []
    for i, d in enumerate(dims):
        count = rng.randint(max(1, d), max(2, d + 2))
        # Ensure each basis direction is represented by a variable.
        for j in range(d):
            coeff = tuple(1 if x == j else 0 for x in range(d))
            exprs.append(Expr(i, rng.randrange(2), coeff))
        for _ in range(count - d):
            exprs.append(Expr(i, rng.randrange(2),
                              tuple(rng.randrange(2) for _ in range(d))))
    clauses = []
    for _ in range(rng.randint(0, min(18, 2 * len(exprs) + 2))):
        width = rng.choice((1, 2))
        ids = [rng.randrange(1, len(exprs) + 1) for _ in range(width)]
        clauses.append(tuple(v if rng.randrange(2) else -v for v in ids))
    return Instance(dims, exprs, clauses)


def coloring_instance(vertices: int, edges: list[tuple[int, int]]) -> Instance:
    dims = [2] * vertices
    exprs: list[Expr] = []
    for i in range(vertices):
        # x1=a, x2=b, x3=1+a+b: odd parity.
        exprs.extend((Expr(i, 0, (1, 0)), Expr(i, 0, (0, 1)),
                      Expr(i, 1, (1, 1))))
    clauses: list[tuple[int, ...]] = []
    for v in range(vertices):
        ids = [3 * v + j for j in (1, 2, 3)]
        clauses.extend((-ids[a], -ids[b]) for a in range(3)
                       for b in range(a + 1, 3))
    for u, v in edges:
        for color in range(3):
            clauses.append((-(3 * u + color + 1), -(3 * v + color + 1)))
    return Instance(dims, exprs, clauses)


def graph_3colorable(vertices: int, edges: list[tuple[int, int]]) -> bool:
    return any(all(color[u] != color[v] for u, v in edges)
               for color in itertools.product(range(3), repeat=vertices))


def easy_large_k(q: int, unsat: bool) -> Instance:
    dims = [2] * q
    exprs = []
    clauses = []
    for i in range(q):
        base = len(exprs) + 1
        exprs.extend((Expr(i, 0, (1, 0)), Expr(i, 0, (0, 1))))
        clauses.append((base, base + 1))
    if unsat:
        clauses.extend(((1,), (-1,),))
    return Instance(dims, exprs, clauses)


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    checks = 0
    random_records = []
    labels = {"SAT": 0, "UNSAT": 0}
    for idx in range(500):
        inst = make_random(rng)
        total_dim = sum(inst.dims)
        if total_dim > 11:
            continue
        want = brute_decide(inst)
        got, ledger = excess_decide(inst)
        assert got == want
        checks += 1
        labels["SAT" if want else "UNSAT"] += 1
        if len(random_records) < 12:
            random_records.append({"id": idx, "dims": inst.dims,
                                   "clauses": len(inst.clauses),
                                   "label": "SAT" if want else "UNSAT",
                                   **ledger})

    # Exhaust all labelled graphs through four vertices and compare the
    # nullity-two affine/NAND encoding with direct 3-colour enumeration.
    graph_checks = 0
    graph_labels = {"SAT": 0, "UNSAT": 0}
    for v in range(1, 5):
        possible = [(i, j) for i in range(v) for j in range(i + 1, v)]
        for mask in range(1 << len(possible)):
            edges = [e for bit, e in enumerate(possible) if mask >> bit & 1]
            inst = coloring_instance(v, edges)
            want = graph_3colorable(v, edges)
            got, ledger = excess_decide(inst)
            assert got == want
            assert ledger["K"] == v
            graph_checks += 1
            graph_labels["SAT" if want else "UNSAT"] += 1
    checks += graph_checks

    # Adaptive/hybrid switching: K is large, but an edgeless component
    # interaction graph permits exact independent local decisions.
    easy_controls = []
    for q in (8, 64, 512):
        for unsat in (False, True):
            inst = easy_large_k(q, unsat)
            assert sum(max(d - 1, 0) for d in inst.dims) == q
            assert not interaction_edges(inst)
            got = local_component_decide(inst)
            assert got is (not unsat)
            checks += 3
            easy_controls.append({
                "q": q, "K": q, "label": "UNSAT" if unsat else "SAT",
                "selected_rule": "independent-component local enumeration",
                "local_states_tested_upper_bound": 4 * q,
                "generic_excess_children_upper_bound": f"2^{q}",
                "peak_live_words_bound": 8 * q + len(inst.clauses),
            })

    elapsed = time.perf_counter() - start
    out = {
        "run_id": "AFFINE-EXCESS-NULLITY111",
        "status": "COMPUTATIONAL corroboration of symbolic upper-bound theorem",
        "seed": SEED,
        "python": "standard library",
        "checks": checks,
        "failures": 0,
        "elapsed_seconds": round(elapsed, 6),
        "random_instances": sum(labels.values()),
        "random_labels": labels,
        "sample_random_ledgers": random_records,
        "graph_encoding": {
            "graphs_checked": graph_checks,
            "vertex_range": [1, 4],
            "labels": graph_labels,
            "endpoint": "odd-XOR3 plus NAND encodes 3-colouring",
        },
        "adaptive_easy_controls": easy_controls,
        "limitations": [
            "Finite tests do not prove asymptotic complexity.",
            "The solver policy is a restricted constructive upper bound.",
            "K is structural and is not an unrestricted time lower bound.",
        ],
    }
    RAW.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
