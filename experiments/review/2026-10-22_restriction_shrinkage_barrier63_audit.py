#!/usr/bin/env python3
"""Finite checks for RESTRICTION-SHRINKAGE-BARRIER63.

The proof is combinatorial; this script only checks the implementation-facing
identities on deterministic bounded-occurrence 3-CNF fixtures.
"""

from __future__ import annotations

import itertools
import json
import math
import random


def eval_clause(clause, assignment):
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def sat(formula, n, fixed=None):
    fixed = fixed or {}
    free = [v for v in range(n) if v not in fixed]
    for bits in itertools.product((False, True), repeat=len(free)):
        a = dict(fixed)
        a.update(zip(free, bits))
        if all(eval_clause(c, a) for c in formula):
            return True
    return False


def restrict(formula, fixed):
    out = []
    for clause in formula:
        reduced = []
        satisfied = False
        for lit in clause:
            v = abs(lit) - 1
            if v not in fixed:
                reduced.append(lit)
            elif fixed[v] == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(reduced))
    return out


def bounded_formula(n, seed):
    """Construct a 3-CNF with occurrence at most four and distinct vars/clause."""
    rng = random.Random(seed)
    stubs = [v for v in range(n) for _ in range(4)]
    assert len(stubs) % 3 == 0
    for _ in range(10000):
        rng.shuffle(stubs)
        groups = [stubs[i:i + 3] for i in range(0, len(stubs), 3)]
        if all(len(set(g)) == 3 for g in groups):
            return [tuple((v + 1) if rng.getrandbits(1) else -(v + 1) for v in g)
                    for g in groups]
    raise RuntimeError("failed to generate bounded-occurrence fixture")


def main():
    checks = 0
    fixtures = 0
    max_ratio = 0.0
    semantic_branches = 0
    for n in (6, 9, 12):
        for seed in range(30):
            formula = bounded_formula(n, seed + 1000 * n)
            fixtures += 1
            m = len(formula)
            occurrence = [0] * n
            for clause in formula:
                for lit in clause:
                    occurrence[abs(lit) - 1] += 1
            assert max(occurrence) <= 4
            checks += n + 1

            # A conservative fixed-width encoding proxy sufficient for the
            # exponent check: three signed variable identifiers per clause.
            record_bits = 3 * (math.ceil(math.log2(n)) + 1)
            N = m * record_bits
            r_cap = min(n, int(math.floor(0.6 * math.log2(N))))
            for r in range(r_cap + 1):
                chosen = tuple(range(r))
                touched = sum(any(abs(lit) - 1 in chosen for lit in clause)
                              for clause in formula)
                assert touched <= 4 * r
                checks += 1
                max_ratio = max(max_ratio, touched / max(1, 4 * r))

                parent_sat = sat(formula, n)
                branch_or = False
                for bits in itertools.product((False, True), repeat=r):
                    fixed = dict(zip(chosen, bits))
                    child = restrict(formula, fixed)
                    untouched = sum(not any(abs(lit) - 1 in chosen for lit in c)
                                    for c in formula)
                    assert len(child) >= untouched >= m - 4 * r
                    checks += 2
                    branch_or |= sat(child, n, fixed)
                    semantic_branches += 1
                assert parent_sat == branch_or
                checks += 1

    result = {
        "status": "finite_audit_only_no_class_separation",
        "fixtures": fixtures,
        "checks": checks,
        "semantic_branches": semantic_branches,
        "max_touched_over_4r": max_ratio,
        "failures": 0,
        "theorem_checked": [
            "touched clauses <= Delta*r with Delta=4",
            "every restricted child retains >= M-Delta*r clauses",
            "SAT(F) iff OR_alpha SAT(F|alpha)",
            "r<=floor(0.6 log2 N) for exhaustive Q<=N^0.6 branching",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
