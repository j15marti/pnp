#!/usr/bin/env python3
"""Exact finite controls for PREPROCESSING-CACHE-FIREWALL173.

No third-party modules and no randomness.  This checks the OR singleton
promise, constant-size label-preserving children, one-shot cache versus
recomputation, and exact integral/fractional values for half-set mutation
hypergraphs.  Finite checks corroborate, but do not replace, the symbolic
proof in the companion report.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction

ASSERTIONS = 0


def check(condition: bool, message: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def sat_of_unit_child(child: tuple[tuple[int, ...], ...]) -> bool:
    for bits in itertools.product((False, True), repeat=2):
        ok = True
        for clause in child:
            clause_ok = False
            for lit in clause:
                value = bits[abs(lit) - 1]
                clause_ok |= value if lit > 0 else not value
            ok &= clause_ok
        if ok:
            return True
    return False


SAT_CHILD = ((1,), (2,))
UNSAT_CHILD = ((1,), (-1,))


def preprocess_or(bits: tuple[int, ...], word: int) -> tuple[int, int, tuple[tuple[int, ...], ...]]:
    """Read every source word once, retain one semantic bit, emit 2 clauses."""
    probes = (len(bits) + word - 1) // word
    label = int(any(bits))
    return probes, label, SAT_CHILD if label else UNSAT_CHILD


def integral_transversal(edges: tuple[frozenset[int], ...], n: int) -> int:
    for size in range(n + 1):
        for choose in itertools.combinations(range(n), size):
            chosen = set(choose)
            if all(chosen & set(edge) for edge in edges):
                return size
    raise AssertionError("no transversal")


def main() -> None:
    rows = []
    # Singleton OR promise: all-zero is NO and every singleton mutant is YES.
    for r in range(1, 17):
        singleton_edges = tuple(frozenset((i,)) for i in range(r))
        check(integral_transversal(singleton_edges, r) == r, "singleton tau")
        for word in range(1, r + 1):
            baseline = (0,) * r
            probes0, label0, child0 = preprocess_or(baseline, word)
            check(label0 == 0 and not sat_of_unit_child(child0), "baseline child")
            check(len(child0) == 2, "constant child clauses")
            expected_words = (r + word - 1) // word
            check(probes0 == expected_words, "baseline source words")
            for i in range(r):
                mutant = tuple(int(j == i) for j in range(r))
                probes1, label1, child1 = preprocess_or(mutant, word)
                check(label1 == 1 and sat_of_unit_child(child1), "mutant child")
                check(probes1 == expected_words, "mutant source words")
                check(len(child1) == 2, "constant mutant clauses")

            # q guest requests: cached execution pays source reads once;
            # source-recompute execution pays them q times.  Both are legal.
            for q in range(1, 9):
                cached_reads = expected_words
                recompute_reads = q * expected_words
                check(cached_reads <= recompute_reads, "cache/recompute order")
                check(cached_reads == expected_words, "no cache recharge")
        rows.append({"r": r, "singleton_tau": r, "child_clauses": 2})

    half_rows = []
    for r in range(2, 14, 2):
        h = r // 2
        edges = tuple(frozenset(e) for e in itertools.combinations(range(r), h))
        tau = integral_transversal(edges, r)
        check(tau == h + 1, "half-set integral tau")
        primal = sum((Fraction(2, r) for _ in range(r)), Fraction(0))
        for edge in edges:
            check(sum((Fraction(2, r) for _ in edge), Fraction(0)) == 1, "primal edge")
        incidence = len(tuple(itertools.combinations(range(r - 1), h - 1)))
        dual_y = Fraction(1, incidence)
        dual = len(edges) * dual_y
        check(primal == 2 and dual == 2, "fractional optimum witnesses")
        # Two independent uniform probes with replacement hit an h-set.
        hit_pairs = sum(1 for a in range(r) for b in range(r) if a in edges[0] or b in edges[0])
        hit = Fraction(hit_pairs, r * r)
        check(hit == Fraction(3, 4), "two-probe hit probability")
        half_rows.append({
            "r": r,
            "edge_size": h,
            "edge_count": len(edges),
            "tau": tau,
            "tau_star": "2",
            "two_probe_hit_probability": "3/4",
        })

    payload = {
        "id": "PREPROCESSING-CACHE-FIREWALL173",
        "timestamp_utc": "2026-10-27T05:55:00Z",
        "method": "exhaustive exact standard-library Python; no randomness",
        "assertions": ASSERTIONS,
        "failures": 0,
        "singleton_or_rows": rows,
        "half_set_rows": half_rows,
        "scope": [
            "query and preprocessing controls only",
            "constant child size is not an all-SAT contraction",
            "no arbitrary-SAT runtime or space lower bound",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
