#!/usr/bin/env python3
"""Finite hostile-control audit for a proposed 2^(k-x) SAT lower bound.

The program is deliberately dependency-free.  It builds several CNF families,
computes exact primal treewidth for the small instances used here, and compares
the resulting table scale 2^(tw+1) with direct semantic decision procedures.
This is a falsification audit, not an asymptotic SAT benchmark.
"""

from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
from functools import lru_cache
from pathlib import Path


Clause = tuple[int, ...]


def dense_horn(n: int, unsat: bool = False) -> list[Clause]:
    clauses = [(-i, -j, k) for i, j, k in itertools.combinations(range(1, n + 1), 3)]
    if unsat:
        clauses += [(1,), (2,), (-3,)]
    return clauses


def equality_2sat_path(n: int) -> list[Clause]:
    clauses: list[Clause] = []
    for i in range(1, n):
        clauses += [(-i, i + 1), (i, -(i + 1))]
    return clauses


def xor_chain(rounds: int) -> tuple[list[Clause], int, list[tuple[int, int]]]:
    """Encode s_i = s_(i-1) XOR x_i; return CNF and GF(2) row masks."""
    # Variables: s_0=1, x_i=2i, s_i=2i+1.  Pin s_0=0 and s_r=1.
    clauses: list[Clause] = [(-1,)]
    equations: list[tuple[int, int]] = [(1 << 0, 0)]
    for i in range(1, rounds + 1):
        a, b, z = 2 * i - 1, 2 * i, 2 * i + 1
        clauses += [(a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z)]
        equations.append(((1 << (a - 1)) | (1 << (b - 1)) | (1 << (z - 1)), 0))
    clauses.append((2 * rounds + 1,))
    equations.append((1 << (2 * rounds), 1))
    return clauses, 2 * rounds + 1, equations


def dead_clique_wrapper(n: int) -> list[Clause]:
    # Each added clause is tautological but contributes edge {i,j} to the
    # conventional syntactic primal graph.
    return [(1,)] + [(i, -i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]


def primal_graph(clauses: list[Clause], n: int) -> tuple[int, ...]:
    adj = [0] * n
    for clause in clauses:
        variables = sorted({abs(lit) - 1 for lit in clause})
        for a, b in itertools.combinations(variables, 2):
            adj[a] |= 1 << b
            adj[b] |= 1 << a
    return tuple(adj)


def exact_treewidth(adjacency: tuple[int, ...]) -> int:
    """Exact elimination search; suitable for the <=9 vertex audit instances."""
    n = len(adjacency)

    @lru_cache(maxsize=None)
    def solve(state: tuple[int, ...], live: int) -> int:
        if live == 0:
            return -1
        best = n
        vbits = live
        while vbits:
            bit = vbits & -vbits
            v = bit.bit_length() - 1
            vbits ^= bit
            neighbors = state[v] & (live ^ bit)
            degree = neighbors.bit_count()
            if degree < best:
                nxt = list(state)
                nb = neighbors
                while nb:
                    ubit = nb & -nb
                    u = ubit.bit_length() - 1
                    nb ^= ubit
                    nxt[u] = (nxt[u] | (neighbors ^ ubit)) & ~bit
                nxt[v] = 0
                tail = solve(tuple(nxt), live ^ bit)
                best = min(best, max(degree, tail))
        return best

    return max(0, solve(adjacency, (1 << n) - 1))


def horn_forward_chain(clauses: list[Clause], n: int) -> dict[str, object]:
    rules: list[tuple[tuple[int, ...], int | None]] = []
    scanned = 0
    for clause in clauses:
        scanned += len(clause)
        positives = [lit for lit in clause if lit > 0]
        if len(positives) > 1:
            raise ValueError("non-Horn clause")
        antecedent = tuple(sorted({-lit for lit in clause if lit < 0}))
        rules.append((antecedent, positives[0] if positives else None))

    remaining = [len(a) for a, _ in rules]
    watch: list[list[int]] = [[] for _ in range(n + 1)]
    for rid, (antecedent, _) in enumerate(rules):
        for variable in antecedent:
            watch[variable].append(rid)

    facts: set[int] = set()
    queue: list[int] = []
    firings = 0
    for rid, (_, head) in enumerate(rules):
        if remaining[rid] == 0:
            firings += 1
            if head is None:
                return {"sat": False, "scanned_literals": scanned, "rule_firings": firings, "facts": 0}
            if head not in facts:
                facts.add(head)
                queue.append(head)

    cursor = 0
    while cursor < len(queue):
        fact = queue[cursor]
        cursor += 1
        for rid in watch[fact]:
            remaining[rid] -= 1
            if remaining[rid] == 0:
                firings += 1
                head = rules[rid][1]
                if head is None:
                    return {"sat": False, "scanned_literals": scanned, "rule_firings": firings, "facts": len(facts)}
                if head not in facts:
                    facts.add(head)
                    queue.append(head)
    return {"sat": True, "scanned_literals": scanned, "rule_firings": firings, "facts": len(facts)}


def brute_sat(clauses: list[Clause], n: int) -> bool:
    for bits in range(1 << n):
        if all(any(((bits >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in c) for c in clauses):
            return True
    return False


def gf2_consistent(equations: list[tuple[int, int]], n: int) -> tuple[bool, int]:
    rows = [[mask, rhs] for mask, rhs in equations]
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(rows)) if (rows[r][0] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and ((rows[r][0] >> col) & 1):
                rows[r][0] ^= rows[rank][0]
                rows[r][1] ^= rows[rank][1]
        rank += 1
    consistent = not any(mask == 0 and rhs for mask, rhs in rows)
    return consistent, rank


def record_case(name: str, clauses: list[Clause], n: int, decision: bool, method: str) -> dict[str, object]:
    tw = exact_treewidth(primal_graph(clauses, n))
    brute = brute_sat(clauses, n)
    assert brute == decision, (name, brute, decision)
    return {
        "family": name,
        "variables_k": n,
        "clauses": len(clauses),
        "literal_occurrences": sum(map(len, clauses)),
        "exact_primal_treewidth_w": tw,
        "x_equals_k_minus_w_minus_1": n - tw - 1,
        "nominal_table_scale_2_pow_w_plus_1": 1 << (tw + 1),
        "sat": decision,
        "decision_method": method,
    }


def run() -> dict[str, object]:
    cases: list[dict[str, object]] = []
    wrapper_checks = 0
    for n in range(3, 10):
        sat_cnf = dense_horn(n)
        sat_result = horn_forward_chain(sat_cnf, n)
        cases.append(record_case("dense_horn_sat", sat_cnf, n, bool(sat_result["sat"]), "linear Horn forward chaining"))

        unsat_cnf = dense_horn(n, unsat=True)
        unsat_result = horn_forward_chain(unsat_cnf, n)
        cases.append(record_case("dense_horn_unsat", unsat_cnf, n, bool(unsat_result["sat"]), "linear Horn forward chaining"))

        dead = dead_clique_wrapper(n)
        cases.append(record_case("dead_tautology_clique", dead, n, True, "unit clause plus deleted tautologies"))

        copied = sat_cnf + list(sat_cnf)
        copy_result = horn_forward_chain(copied, n)
        assert copy_result["sat"] == sat_result["sat"]
        wrapper_checks += 1

        perm = {i: n + 1 - i for i in range(1, n + 1)}
        permuted = [tuple((1 if lit > 0 else -1) * perm[abs(lit)] for lit in clause) for clause in sat_cnf]
        assert horn_forward_chain(permuted, n)["sat"] == sat_result["sat"]
        assert exact_treewidth(primal_graph(permuted, n)) == n - 1
        wrapper_checks += 2

    for n in range(3, 10):
        path = equality_2sat_path(n)
        cases.append(record_case("equality_2sat_path", path, n, True, "2SAT implication graph control"))

    affine_checks = 0
    for rounds in range(2, 5):
        cnf, n, equations = xor_chain(rounds)
        consistent, rank = gf2_consistent(equations, n)
        cases.append(record_case("affine_xor_chain", cnf, n, consistent, f"GF(2) elimination rank={rank}"))
        affine_checks += 1

    dense = [c for c in cases if c["family"] in {"dense_horn_sat", "dense_horn_unsat", "dead_tautology_clique"}]
    assert all(c["exact_primal_treewidth_w"] == c["variables_k"] - 1 for c in dense)
    assert all(c["nominal_table_scale_2_pow_w_plus_1"] == 1 << c["variables_k"] for c in dense)
    assert all(c["exact_primal_treewidth_w"] == 1 for c in cases if c["family"] == "equality_2sat_path")
    assert all(c["exact_primal_treewidth_w"] == 2 for c in cases if c["family"] == "affine_xor_chain")

    return {
        "schema": "TREEWIDTH-2K2X-AUDIT-v1",
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "claim_under_test": "Every deterministic SAT decider requires Omega(2^(k-x)) work when x=k-(tw(F)+1).",
        "verdict": "FALSIFIED: 2^(tw+1) is a table scale for a decomposition-DP realization, not an all-algorithm lower bound.",
        "case_count": len(cases),
        "wrapper_checks": wrapper_checks,
        "affine_gaussian_checks": affine_checks,
        "max_variables_exact_tw": max(int(c["variables_k"]) for c in cases),
        "max_nominal_table_scale": max(int(c["nominal_table_scale_2_pow_w_plus_1"]) for c in cases),
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
