#!/usr/bin/env python3
"""Audit the unique-witness explicitness fork used in synthesis 45.

This verifies the connected proper-3CNF forced-witness family, deterministic
witness recovery, the exact description-counting fork, and the k=241
threshold arithmetic.  It does not compute KT or prove a class separation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


Clause = tuple[int, int, int]


def lit_value(lit: int, assignment: int) -> bool:
    bit = (assignment >> (abs(lit) - 1)) & 1
    return bool(bit) if lit > 0 else not bool(bit)


def satisfies(clauses: list[Clause], assignment: int) -> bool:
    return all(any(lit_value(lit, assignment) for lit in clause) for clause in clauses)


def true_lit(var: int, assignment: int) -> int:
    return var if ((assignment >> (var - 1)) & 1) else -var


def triple_gadget(base: int, assignment: int) -> list[Clause]:
    """All proper clauses on a triple except the clause falsified by assignment."""
    variables = (base + 1, base + 2, base + 3)
    clauses: list[Clause] = []
    for signs in range(8):
        clause = tuple(
            var if ((signs >> offset) & 1) else -var
            for offset, var in enumerate(variables)
        )
        if any(lit_value(lit, assignment) for lit in clause):
            clauses.append(clause)  # Exactly seven clauses survive.
    return clauses


def forced_formula(n: int, assignment: int) -> list[Clause]:
    assert n % 3 == 0
    clauses: list[Clause] = []
    triples = n // 3
    for block in range(triples):
        clauses.extend(triple_gadget(3 * block, assignment))
    # One redundant satisfied bridge between adjacent triples.  A middle
    # triple uses variables 1,2 on its incoming bridge and variable 3 on its
    # outgoing bridge, so every variable occurs in at most eight clauses.
    for block in range(triples - 1):
        left = 3 * block + 3
        right1 = 3 * (block + 1) + 1
        right2 = 3 * (block + 1) + 2
        clauses.append(
            (
                true_lit(left, assignment),
                true_lit(right1, assignment),
                true_lit(right2, assignment),
            )
        )
    return clauses


def recover_witness(n: int, clauses: list[Clause]) -> int | None:
    """Recover each triple from its seven local clauses; reject bad syntax."""
    expected_local = 7 * (n // 3)
    if len(clauses) != expected_local + n // 3 - 1:
        return None
    answer = 0
    for block in range(n // 3):
        lo, hi = 3 * block + 1, 3 * block + 3
        local = [c for c in clauses[:expected_local] if all(lo <= abs(x) <= hi for x in c)]
        if len(local) != 7:
            return None
        winners = []
        for pattern in range(8):
            assignment = pattern << (3 * block)
            if satisfies(local, assignment):
                winners.append(pattern)
        if len(winners) != 1:
            return None
        answer |= winners[0] << (3 * block)
    return answer


def recognize_forced_family(n: int, clauses: list[Clause]) -> int | None:
    """Return the witness exactly for canonical members of the forced family."""
    witness = recover_witness(n, clauses)
    if witness is None or forced_formula(n, witness) != clauses:
        return None
    return witness


def serialized_bits(n: int) -> int:
    clauses = 8 * n // 3 - 1
    label_bits = max(1, math.ceil(math.log2(n + 1)))
    return clauses * 3 * (label_bits + 1) + 3 * label_bits + 32


def connected_primal_graph(n: int, clauses: list[Clause]) -> bool:
    adjacency = [set() for _ in range(n)]
    for clause in clauses:
        vertices = [abs(lit) - 1 for lit in clause]
        for u in vertices:
            adjacency[u].update(v for v in vertices if v != u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u] - seen:
            seen.add(v)
            stack.append(v)
    return len(seen) == n


def p241(n: int) -> tuple[int, int, float]:
    source_n = serialized_bits(n)
    log2_m = 1.2 * math.log2(source_n)
    return source_n, max(math.ceil(log2_m), math.ceil(2 ** (log2_m / 241))), log2_m


def main() -> None:
    assertions = 0
    failures: list[str] = []
    formulas = 0
    assignments_checked = 0

    # Exhaustive uniqueness and syntactic recovery.
    for n in (3, 6, 9):
        for witness in range(1 << n):
            clauses = forced_formula(n, witness)
            formulas += 1
            assertions += 5
            if len(clauses) != 8 * n // 3 - 1:
                failures.append(f"clause count n={n} a={witness}")
            occurrences = [0] * n
            for clause in clauses:
                for lit in clause:
                    occurrences[abs(lit) - 1] += 1
            if max(occurrences) > 8:
                failures.append(f"degree n={n} a={witness} max={max(occurrences)}")
            if not connected_primal_graph(n, clauses):
                failures.append(f"connectivity n={n} a={witness}")
            if recognize_forced_family(n, clauses) != witness:
                failures.append(f"recovery n={n} a={witness}")

            corrupted = list(clauses)
            corrupted[0] = corrupted[1]
            if recognize_forced_family(n, corrupted) is not None:
                failures.append(f"corrupt recognition n={n} a={witness}")

            winners = []
            for candidate in range(1 << n):
                assignments_checked += 1
                if satisfies(clauses, candidate):
                    winners.append(candidate)
            assertions += 1
            if winners != [witness]:
                failures.append(f"uniqueness n={n} a={witness} winners={winners}")

    # Exact counting: descriptions shorter than n cannot name all 2^n
    # witness strings.  This proves existence only, not uniform selection.
    counting_cases = 0
    for n in range(1, 33):
        for description_bits in range(n):
            assertions += 1
            counting_cases += 1
            if not (1 << description_bits) < (1 << n):
                failures.append(f"counting n={n} s={description_bits}")

    # A concrete injective target control: first n target bits are the witness,
    # followed by zeros.  It preserves all 2^n distinct targets but cannot map
    # every SAT source to LOW at a budget p << n.
    injective_cases = 0
    for n in (3, 6, 9, 12):
        seen = set()
        for witness in range(1 << n):
            target_prefix = witness.to_bytes((n + 7) // 8, "little")
            seen.add(target_prefix)
        assertions += 1
        injective_cases += 1
        if len(seen) != 1 << n:
            failures.append(f"injectivity n={n}")

    # Exact exponent/finite threshold comparisons for representative sizes.
    threshold_rows = []
    for exponent in range(4, 21):
        n = 3 * (1 << exponent)
        source_n, threshold, log2_m = p241(n)
        assertions += 1
        if not n > threshold:
            failures.append(f"threshold n={n} N={source_n} p={threshold}")
        threshold_rows.append(
            {
                "witness_bits_n": n,
                "source_bits_N": source_n,
                "log2_target_M": log2_m,
                "p_241": threshold,
                "n_over_p": n / threshold,
            }
        )

    result = {
        "run": "UNIQUE-WITNESS-EXPLICITNESS-FORK45",
        "status": "PASS" if not failures else "FAIL",
        "formulas": formulas,
        "assignments_checked": assignments_checked,
        "counting_cases": counting_cases,
        "injective_cases": injective_cases,
        "threshold_rows": threshold_rows,
        "assertions": assertions,
        "failures": failures,
        "scope": (
            "forced-family recovery, counting, injectivity and exponent audit; "
            "not an exact KT computation or complexity-class lower bound"
        ),
        "global_status": "P versus NP OPEN; P versus RP OPEN",
    }
    Path("UNIQUE_WITNESS_EXPLICITNESS_FORK45_raw.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
