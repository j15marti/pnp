#!/usr/bin/env python3
"""Independent audit for the exact-overlap promise decider.

Clauses are tuples of (variable, sign) pairs.  sign=1 denotes a positive
literal and sign=0 a negated literal.  A falsifying assignment therefore fixes
the variable to 0 for sign=1 and to 1 for sign=0.
"""

from __future__ import annotations

import itertools
import json
import random
from dataclasses import dataclass, asdict


SEED = 202610192048


def all_proper_clauses(n: int, k: int):
    for variables in itertools.combinations(range(n), k):
        for signs in itertools.product((0, 1), repeat=k):
            yield tuple(zip(variables, signs))


def clause_false(clause, assignment: int) -> bool:
    for var, sign in clause:
        value = (assignment >> var) & 1
        literal_value = value if sign else 1 - value
        if literal_value:
            return False
    return True


def is_unsat(formula, n: int) -> bool:
    return all(any(clause_false(c, a) for c in formula) for a in range(1 << n))


def normalized_overlap(formula, k: int) -> int:
    total = 0
    for left, right in itertools.combinations(formula, 2):
        req = {}
        compatible = True
        for var, sign in left + right:
            falsifying_value = 0 if sign else 1
            old = req.get(var)
            if old is not None and old != falsifying_value:
                compatible = False
                break
            req[var] = falsifying_value
        if compatible:
            total += 1 << (2 * k - len(req))
    return total


def direct_overlap(formula, n: int) -> int:
    result = 0
    false_sets = [
        {a for a in range(1 << n) if clause_false(c, a)} for c in formula
    ]
    for i, j in itertools.combinations(range(len(formula)), 2):
        result += len(false_sets[i] & false_sets[j])
    return result


@dataclass
class Counts:
    exhaustive_formulas: int = 0
    random_formulas: int = 0
    assignments_checked: int = 0
    pair_terms_checked: int = 0
    theorem_failures: int = 0
    normalization_failures: int = 0
    duplicate_clause_formulas: int = 0


def check_formula(formula, n: int, k: int, counts: Counts, exhaustive: bool):
    if exhaustive:
        counts.exhaustive_formulas += 1
    else:
        counts.random_formulas += 1
    counts.assignments_checked += 1 << n
    counts.pair_terms_checked += len(formula) * (len(formula) - 1) // 2
    if len(set(formula)) < len(formula):
        counts.duplicate_clause_formulas += 1
    q = normalized_overlap(formula, k)
    unsat = is_unsat(formula, n)
    if unsat != (q == (1 << k)):
        counts.theorem_failures += 1
        raise AssertionError((n, k, formula, unsat, q))
    w = direct_overlap(formula, n)
    # Avoid negative exponents: compare after multiplying by 2^(max(0,2k-n)).
    if n >= 2 * k:
        normalized_ok = w == q * (1 << (n - 2 * k))
    else:
        normalized_ok = w * (1 << (2 * k - n)) == q
    if not normalized_ok:
        counts.normalization_failures += 1
        raise AssertionError((n, k, w, q))


def run():
    rng = random.Random(SEED)
    counts = Counts()
    exhaustive_cases = []
    for k, ns in ((1, range(1, 5)), (2, range(2, 5)), (3, (3,))):
        m = (1 << k) + 1
        for n in ns:
            clauses = list(all_proper_clauses(n, k))
            local = 0
            for indices in itertools.combinations_with_replacement(range(len(clauses)), m):
                formula = tuple(clauses[i] for i in indices)
                check_formula(formula, n, k, counts, True)
                local += 1
            exhaustive_cases.append({"n": n, "k": k, "formulas": local})

    random_cases = []
    for k, ns, trials in ((3, range(4, 9), 2000), (4, range(4, 8), 500)):
        m = (1 << k) + 1
        for n in ns:
            clauses = list(all_proper_clauses(n, k))
            for _ in range(trials):
                formula = tuple(rng.choice(clauses) for _ in range(m))
                check_formula(formula, n, k, counts, False)
            random_cases.append({"n": n, "k": k, "formulas": trials})

    result = {
        "run_id": "OVERLAP-PROMISE-DECIDER4",
        "seed": SEED,
        "status": "PASS" if not counts.theorem_failures and not counts.normalization_failures else "FAIL",
        "claim": "For m=2^k+1 proper width-k clauses, UNSAT iff normalized_overlap=2^k.",
        "normalized_overlap": "sum over compatible pairs of 2^(2k-|union of variables|)",
        "exhaustive_cases": exhaustive_cases,
        "random_cases": random_cases,
        "counts": asdict(counts),
        "scope": {
            "general_3sat": False,
            "mcsp_transfer": False,
            "arc_transfer": False,
            "p_vs_np": "OPEN",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
