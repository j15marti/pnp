#!/usr/bin/env python3
"""Audit SHARED-INTERFACE-TABLE92.

The source is a J by K Boolean compatibility table, K=2^h.  The
parent is satisfiable iff some column is all one.  We verify the source
semantics, an equal-metadata CNF encoding, proper-3CNF conversion, the
full-degree coefficient, and exact deterministic decision-tree depth on
small instances.  Only the finite checks are computational; the report
contains the symbolic proofs.
"""

from __future__ import annotations

import functools
import itertools
import json
import random
import time

SEED = 20261023


def table_label(bits: tuple[int, ...], j: int, k: int) -> bool:
    return any(all(bits[row * k + col] for row in range(j)) for col in range(k))


def fresh(counter: list[int]) -> int:
    counter[0] += 1
    return counter[0]


def proper3_clause(clause: tuple[int, ...], counter: list[int]) -> list[tuple[int, int, int]]:
    """Standard equisatisfiable conversion of one nonempty clause."""
    length = len(clause)
    if length == 1:
        lit = clause[0]
        a, b = fresh(counter), fresh(counter)
        return [(lit, a, b), (lit, a, -b), (lit, -a, b), (lit, -a, -b)]
    if length == 2:
        a = fresh(counter)
        return [(clause[0], clause[1], a), (clause[0], clause[1], -a)]
    if length == 3:
        return [clause]
    out: list[tuple[int, int, int]] = []
    y = fresh(counter)
    out.append((clause[0], clause[1], y))
    for index in range(2, length - 2):
        next_y = fresh(counter)
        out.append((-y, clause[index], next_y))
        y = next_y
    out.append((-y, clause[-2], clause[-1]))
    return out


def encode(bits: tuple[int, ...], j: int, h: int) -> tuple[list[tuple[int, ...]], list[tuple[int, int, int]], int]:
    """Fixed-metadata CNF: cell signs carry the table; structure is fixed."""
    k = 1 << h
    assert len(bits) == j * k
    wide: list[tuple[int, ...]] = []
    next_var = h
    for row in range(j):
        for col in range(k):
            next_var += 1
            cell = next_var
            bit = bits[row * k + col]
            wide.append((cell if bit else -cell,))
            mismatch = []
            for position in range(h):
                selector = position + 1
                mismatch.append(-selector if ((col >> position) & 1) else selector)
            wide.append(tuple(mismatch + [cell]))
    counter = [next_var]
    proper: list[tuple[int, int, int]] = []
    for clause in wide:
        proper.extend(proper3_clause(clause, counter))
    return wide, proper, counter[0]


def eval_cnf(cnf: list[tuple[int, ...]], assignment: dict[int, bool]) -> bool:
    return all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause) for clause in cnf)


def wide_sat(bits: tuple[int, ...], j: int, h: int) -> bool:
    k = 1 << h
    wide, _, _ = encode(bits, j, h)
    # Cell variables are forced by their unit clauses; enumerate only S.
    for col in range(k):
        assignment = {position + 1: bool((col >> position) & 1) for position in range(h)}
        for index, bit in enumerate(bits):
            assignment[h + index + 1] = bool(bit)
        if eval_cnf(wide, assignment):
            return True
    return False


def simplify(cnf: tuple[tuple[int, ...], ...], lit: int) -> tuple[tuple[int, ...], ...] | None:
    out = []
    for clause in cnf:
        if lit in clause:
            continue
        reduced = tuple(x for x in clause if x != -lit)
        if not reduced:
            return None
        out.append(reduced)
    return tuple(out)


def dpll(cnf: list[tuple[int, ...]]) -> bool:
    @functools.lru_cache(maxsize=None)
    def solve(state: tuple[tuple[int, ...], ...]) -> bool:
        if not state:
            return True
        while True:
            unit = next((c[0] for c in state if len(c) == 1), None)
            if unit is None:
                break
            reduced = simplify(state, unit)
            if reduced is None:
                return False
            state = reduced
            if not state:
                return True
        literals = {x for clause in state for x in clause}
        pure = next((x for x in literals if -x not in literals), None)
        if pure is not None:
            reduced = simplify(state, pure)
            return False if reduced is None else solve(reduced)
        lit = min(state, key=len)[0]
        left = simplify(state, lit)
        if left is not None and solve(left):
            return True
        right = simplify(state, -lit)
        return right is not None and solve(right)

    normalized = tuple(sorted((tuple(sorted(c)) for c in cnf), key=lambda c: (len(c), c)))
    return solve(normalized)


def full_degree_coefficient(j: int, k: int) -> int:
    m = j * k
    coefficient = 0
    for mask in range(1 << m):
        bits = tuple((mask >> i) & 1 for i in range(m))
        if table_label(bits, j, k):
            coefficient += -1 if ((m - mask.bit_count()) & 1) else 1
    return coefficient


def exact_decision_depth(j: int, k: int) -> int:
    m = j * k

    @functools.lru_cache(maxsize=None)
    def solve(known: int, values: int) -> int:
        seen = None
        for mask in range(1 << m):
            if (mask & known) != values:
                continue
            bits = tuple((mask >> i) & 1 for i in range(m))
            label = table_label(bits, j, k)
            if seen is None:
                seen = label
            elif seen != label:
                break
        else:
            return 0
        best = m + 1
        for index in range(m):
            flag = 1 << index
            if known & flag:
                continue
            d0 = solve(known | flag, values)
            d1 = solve(known | flag, values | flag)
            best = min(best, 1 + max(d0, d1))
        return best

    return solve(0, 0)


def audit() -> dict:
    rng = random.Random(SEED)
    started = time.time()
    assertions = 0
    exhaustive_tables = 0
    randomized_tables = 0
    proper3_checks = 0
    depth_cases = []
    degree_cases = []

    for j, h in [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2)]:
        k = 1 << h
        m = j * k
        for mask in range(1 << m):
            bits = tuple((mask >> i) & 1 for i in range(m))
            expected = table_label(bits, j, k)
            assert wide_sat(bits, j, h) == expected
            assertions += 1
            exhaustive_tables += 1
            if m <= 8:
                _, proper, _ = encode(bits, j, h)
                assert dpll(proper) == expected
                assertions += 1
                proper3_checks += 1

    for j, h in [(2, 3), (3, 2), (3, 3), (4, 2)]:
        k = 1 << h
        m = j * k
        controls = [
            tuple(0 for _ in range(m)),
            tuple(1 for _ in range(m)),
        ]
        good_col = rng.randrange(k)
        controls.append(tuple(1 if (i % k) == good_col else 0 for i in range(m)))
        controls.append(tuple(0 if (i % k) == (i // k) % k else 1 for i in range(m)))
        samples = controls + [tuple(rng.randrange(2) for _ in range(m)) for _ in range(96)]
        for bits in samples:
            expected = table_label(bits, j, k)
            assert wide_sat(bits, j, h) == expected
            assertions += 1
            randomized_tables += 1
            _, proper, _ = encode(bits, j, h)
            assert dpll(proper) == expected
            assertions += 1
            proper3_checks += 1

    # Hidden-source control: each row is individually feasible, intersection empty.
    hidden = (1, 0, 0, 1)
    assert any(hidden[:2]) and any(hidden[2:]) and not table_label(hidden, 2, 2)
    assertions += 3

    for j, k in [(1, 2), (2, 2), (3, 2), (1, 4), (2, 4)]:
        coefficient = full_degree_coefficient(j, k)
        assert coefficient != 0
        assertions += 1
        degree_cases.append({"J": j, "K": k, "M": j * k, "full_coefficient": coefficient})
        depth = exact_decision_depth(j, k)
        assert depth == j * k
        assertions += 1
        depth_cases.append({"J": j, "K": k, "M": j * k, "exact_depth": depth})

    # Exact clause/variable count formulas for the fixed-metadata proper-3CNF map.
    count_cases = []
    for j in range(1, 5):
        for h in range(1, 6):
            k = 1 << h
            m = j * k
            bits = tuple((i * 7 + j + h) & 1 for i in range(m))
            wide, proper, variables = encode(bits, j, h)
            a_h = 1 if h == 1 else (0 if h == 2 else h - 2)
            c_h = 2 if h == 1 else (1 if h == 2 else h - 1)
            expected_variables = h + m * (3 + a_h)
            expected_clauses = m * (4 + c_h)
            assert len(wide) == 2 * m
            assert variables == expected_variables
            assert len(proper) == expected_clauses
            assert all(len(c) == 3 for c in proper)
            assertions += 4
            count_cases.append({"J": j, "h": h, "K": k, "M": m,
                                "variables": variables, "clauses": len(proper)})

    return {
        "claim_id": "SHARED-INTERFACE-TABLE92",
        "status": "COMPUTATIONAL audit of PROVED/EXACT symbolic lemmas",
        "seed": SEED,
        "assertions": assertions,
        "failures": 0,
        "exhaustive_tables": exhaustive_tables,
        "randomized_control_tables": randomized_tables,
        "proper3_satisfiability_checks": proper3_checks,
        "degree_cases": degree_cases,
        "decision_depth_cases": depth_cases,
        "count_cases": count_cases,
        "hostile_controls": ["all-zero", "all-one", "single-good-column",
                             "one-zero-per-column", "hidden-shared-interface"],
        "elapsed_seconds": round(time.time() - started, 6),
        "limitations": "Finite checks validate implementation only; proofs are symbolic in the report.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
