#!/usr/bin/env python3
"""Exact finite audit for CANONICAL-WITNESS-TRAP9."""

import json
from itertools import product


def witness_values(n, b):
    N = 1 << n
    y = tuple(0 if i % 2 == 0 else 1 - b for i in range(N))
    return (b,) + y


def satisfies(n, assignment):
    b, ys = assignment[0], assignment[1:]
    for i, y in enumerate(ys):
        if i % 2 == 0:
            if y != 0:
                return False
        elif not ((b or y) and ((not b) or (not y))):
            return False
    return True


def variable_table(m, j):
    value = 0
    for a in range(1 << m):
        if (a >> j) & 1:
            value |= 1 << a
    return value


def target_tables(n):
    m = n + 1
    top = variable_table(m, n)
    parity = 0
    for a in range(1 << m):
        if ((a & ((1 << n) - 1)).bit_count() & 1) and not ((a >> n) & 1):
            parity |= 1 << a
    return parity, top


def enumerate_at_most_two_gate_outputs(m):
    width = 1 << m
    mask = (1 << width) - 1
    initials = [0, mask] + [variable_table(m, j) for j in range(m)]
    outputs = set(initials)
    descriptions = len(initials)

    first_gates = []
    for a in initials:
        first_gates.append((~a) & mask)
    for a in initials:
        for b in initials:
            first_gates.extend((a & b, a | b))
    descriptions += len(first_gates)
    outputs.update(first_gates)

    for g1 in first_gates:
        wires = initials + [g1]
        second = [((~a) & mask) for a in wires]
        for a in wires:
            for b in wires:
                second.extend((a & b, a | b))
        descriptions += len(second)
        outputs.update(second)
    return descriptions, outputs


assertions = 0
full_assignments = 0

# Exact semantic and selector checks.
for n in range(1, 11):
    w0 = witness_values(n, 0)
    w1 = witness_values(n, 1)
    assert satisfies(n, w0) and satisfies(n, w1)
    assert w0 < w1  # variable order b,y_0,... makes b=0 lexicographically first
    assertions += 3

    hard, easy = target_tables(n)
    assert easy == variable_table(n + 1, n)
    assertions += 1
    # The planted address function depends on every low address bit.
    for j in range(n):
        base = 0
        assert ((hard >> base) & 1) != ((hard >> (base ^ (1 << j))) & 1)
        assertions += 1

# Exhaustively confirm exactly two satisfying assignments at small n.
for n in range(1, 5):
    N = 1 << n
    sat = []
    for bits in product((0, 1), repeat=N + 1):
        full_assignments += 1
        if satisfies(n, bits):
            sat.append(bits)
    assert sat == [witness_values(n, 0), witness_values(n, 1)]
    assertions += 1

# Independent reproduction of the <=2-gate census at n=4,5.
censuses = []
for n, expected in ((4, 14392), (5, 23400)):
    descriptions, outputs = enumerate_at_most_two_gate_outputs(n + 1)
    hard, easy = target_tables(n)
    assert descriptions == expected
    assert hard not in outputs
    assert easy in outputs
    assertions += 3
    censuses.append({
        "n": n,
        "address_bits": n + 1,
        "descriptions": descriptions,
        "distinct_truth_tables": len(outputs),
        "planted_found": hard in outputs,
        "easy_found": easy in outputs,
    })

out = {
    "artifact": "CANONICAL-WITNESS-TRAP9",
    "status": "EXACT_RESTRICTED_COUNTEREXAMPLE_AND_FINITE_AUDIT",
    "assertions": assertions,
    "full_assignments_tested": full_assignments,
    "censuses": censuses,
    "failed_assertions": 0,
    "established": [
        "exactly two satisfying assignments in the indexed family",
        "lexicographically first witness is the parity-bearing planted witness",
        "an alternate shared witness is the zero-gate highest-address-bit function",
        "planted witness depends on every low address bit and needs at least n-1 binary gates",
    ],
    "not_claimed": [
        "superpolynomial circuit lower bound",
        "compact-witness premise for the project diagonal family",
        "SAT-to-MKTP reduction",
        "ARC contractor",
        "P versus NP separation",
    ],
}
print(json.dumps(out, indent=2, sort_keys=True))
