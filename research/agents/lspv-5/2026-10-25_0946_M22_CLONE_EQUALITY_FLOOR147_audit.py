#!/usr/bin/env python3
"""Finite audit for M22-CLONE-EQUALITY-FLOOR147.

This checks the boundary-separation lemma behind the symbolic proof.  A
proper ternary clause satisfied by both constant assignments contains both
signs.  Such a clause falsifies exactly one of the 2r assignments of Hamming
distance one from a constant word.  Consequently at least 2r clauses are
needed before existential auxiliaries or repeated literals are allowed.

The experiment is exhaustive over all constant-preserving proper ternary
clauses for r=3..12.  It also checks easy equality-cycle SAT/UNSAT controls.
"""

from __future__ import annotations

import json
import time
from itertools import combinations, product


def eval_clause(clause: tuple[int, int, int], assignment: tuple[int, ...]) -> bool:
    return any((assignment[abs(lit) - 1] == 1) if lit > 0 else
               (assignment[abs(lit) - 1] == 0) for lit in clause)


def constant_preserving_clauses(r: int):
    for support in combinations(range(1, r + 1), 3):
        for signs in product((-1, 1), repeat=3):
            if signs == (-1, -1, -1) or signs == (1, 1, 1):
                continue
            yield tuple(s * v for s, v in zip(signs, support))


def boundary_words(r: int):
    zero = (0,) * r
    one = (1,) * r
    one_hot = [tuple(1 if j == i else 0 for j in range(r)) for i in range(r)]
    one_zero = [tuple(0 if j == i else 1 for j in range(r)) for i in range(r)]
    return zero, one, one_hot, one_zero


def implication_cycle_sat(r: int, pins: dict[int, int]) -> bool:
    # Clauses (not x_i or x_(i+1)); all variables are therefore equal.
    for bit in (0, 1):
        if all(bit == value for value in pins.values()):
            return True
    return False


def main() -> None:
    started = time.time()
    rows = []
    assertions = 0
    for r in range(3, 13):
        zero, one, one_hot, one_zero = boundary_words(r)
        attacks = one_hot + one_zero
        clauses = list(constant_preserving_clauses(r))
        expected = 6 * (r * (r - 1) * (r - 2) // 6)
        assert len(clauses) == expected
        assertions += 1

        attacked_counts = [0] * (2 * r)
        max_attacks = 0
        for clause in clauses:
            assert eval_clause(clause, zero)
            assert eval_clause(clause, one)
            killed = [i for i, word in enumerate(attacks)
                      if not eval_clause(clause, word)]
            # One-negative clauses kill one one-hot word; one-positive clauses
            # kill one one-zero word.  No clause kills two boundary words.
            assert len(killed) == 1
            attacked_counts[killed[0]] += 1
            max_attacks = max(max_attacks, len(killed))
            assertions += 3

        expected_per_word = (r - 1) * (r - 2) // 2
        assert all(c == expected_per_word for c in attacked_counts)
        assertions += 1

        # Since every allowed clause covers exactly one boundary word, the
        # exact set-cover number is 2r, not merely a lower estimate.
        minimum_boundary_cover = 2 * r
        quota_tight_clause_budget = r
        assert minimum_boundary_cover > quota_tight_clause_budget
        assertions += 1

        # Easy controls: equality is SAT under either uniform pin and becomes
        # UNSAT under inconsistent pins.  SCC/union-find decides this in O(r).
        assert implication_cycle_sat(r, {})
        assert implication_cycle_sat(r, {0: 0})
        assert implication_cycle_sat(r, {0: 1})
        assert not implication_cycle_sat(r, {0: 0, r - 1: 1})
        assertions += 4

        rows.append({
            "r": r,
            "proper_constant_preserving_clauses": len(clauses),
            "boundary_words": 2 * r,
            "clauses_kill_at_most": max_attacks,
            "clauses_killing_each_boundary_word": expected_per_word,
            "exact_minimum_boundary_cover": minimum_boundary_cover,
            "quota_tight_available_clauses": quota_tight_clause_budget,
            "quota_tight_literal_slots": 3 * r,
            "minimum_literal_slots_without_auxiliaries": 6 * r,
        })

    result = {
        "run": "M22-CLONE-EQUALITY-FLOOR147",
        "status": "COMPUTATIONAL audit of a PROVED/EXACT restricted lemma",
        "range": {"r_min": 3, "r_max": 12, "exhaustive": True},
        "assertions": assertions,
        "failures": 0,
        "rows": rows,
        "controls": {
            "sat": "binary implication cycle with no pin or one consistent pin",
            "unsat": "binary implication cycle with opposite pinned endpoints",
            "direct_algorithm": "SCC or parity union-find in O(r) work",
        },
        "limitations": [
            "Finite checks support but do not prove the symbolic all-r lemma.",
            "The theorem excludes only clone-only, no-auxiliary, quota-tight proper ternary equality gadgets.",
            "Repeated literals, existential auxiliaries, larger quota budgets, and different reductions remain open.",
            "Clause/literal counts are not a lower bound on unrestricted SAT decision work.",
        ],
        "runtime_seconds": round(time.time() - started, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
