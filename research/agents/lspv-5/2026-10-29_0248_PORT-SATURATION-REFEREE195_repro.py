#!/usr/bin/env python3
"""PORT-SATURATION-REFEREE195 exact finite controls.

Stdlib only. Exhaustively checks the 15-variable strict exact-(2,2) source U,
all valid same-sign single-occurrence swaps, the explicit SAT witness after
one swap, and the port-identification degree overflow.
"""
from collections import Counter
from itertools import combinations
import json

U_TEXT = (
    "-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;"
    "4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;"
    "-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;"
    "-5 -12 15;-1 13 14"
)


def parse(text):
    return tuple(tuple(int(x) for x in clause.split()) for clause in text.split(";"))


def holds(formula, assignment):
    return all(
        any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
        for clause in formula
    )


def sat_witness(formula, n):
    return next((a for a in range(1 << n) if holds(formula, a)), None)


def proper_exact22(formula, n):
    counts = Counter(lit for clause in formula for lit in clause)
    return (
        len(formula) * 3 == 4 * n
        and all(len(clause) == 3 and len({abs(x) for x in clause}) == 3 for clause in formula)
        and len({tuple(sorted(clause)) for clause in formula}) == len(formula)
        and all(counts[v] == counts[-v] == 2 for v in range(1, n + 1))
    )


def connected(formula, n):
    incidence = {v: set() for v in range(1, n + 1)}
    for ci, clause in enumerate(formula):
        for lit in clause:
            incidence[abs(lit)].add(ci)
    seen_v, seen_c, todo = {1}, set(), [1]
    while todo:
        v = todo.pop()
        for ci in incidence[v]:
            if ci in seen_c:
                continue
            seen_c.add(ci)
            for lit in formula[ci]:
                w = abs(lit)
                if w not in seen_v:
                    seen_v.add(w)
                    todo.append(w)
    return len(seen_v) == n and len(seen_c) == len(formula)


def swap_occurrences(formula, left, right):
    (i, p), (j, q) = left, right
    out = [list(clause) for clause in formula]
    out[i][p], out[j][q] = out[j][q], out[i][p]
    return tuple(tuple(clause) for clause in out)


def equality_gadget(a, b, u):
    return (
        (-a, b, u),
        (-a, b, -u),
        (a, -b, u),
        (a, -b, -u),
    )


def run():
    u = parse(U_TEXT)
    assert proper_exact22(u, 15)
    assert connected(u, 15)
    assert sat_witness(u, 15) is None

    positions = [(i, p) for i in range(len(u)) for p in range(3)]
    attempted_same_sign = 0
    valid_exact22 = 0
    connected_valid = 0
    sat_after_swap = 0
    first = None
    for left, right in combinations(positions, 2):
        x, y = u[left[0]][left[1]], u[right[0]][right[1]]
        if (x > 0) != (y > 0) or abs(x) == abs(y):
            continue
        attempted_same_sign += 1
        g = swap_occurrences(u, left, right)
        if not proper_exact22(g, 15):
            continue
        valid_exact22 += 1
        if connected(g, 15):
            connected_valid += 1
        witness = sat_witness(g, 15)
        if witness is not None:
            sat_after_swap += 1
            if first is None:
                first = {
                    "left_zero_based_clause_slot": list(left),
                    "right_zero_based_clause_slot": list(right),
                    "swapped_literals": [x, y],
                    "changed_clauses": [list(g[left[0]]), list(g[right[0]])],
                    "witness_decimal": witness,
                    "witness_true_variables": [
                        v for v in range(1, 16) if (witness >> (v - 1)) & 1
                    ],
                    "connected": connected(g, 15),
                }

    assert first is not None
    assert first["swapped_literals"] == [-1, -8]
    assert first["witness_decimal"] == 736
    explicit = swap_occurrences(u, (0, 0), (1, 1))
    assert proper_exact22(explicit, 15) and connected(explicit, 15)
    assert holds(explicit, 736)

    # Two individually exact-(2,2) equality gadgets sharing the port b=2.
    # Each has b twice positive and twice negative; identification doubles it.
    joined = equality_gadget(1, 2, 3) + equality_gadget(2, 4, 5)
    counts = Counter(lit for clause in joined for lit in clause)
    assert counts[2] == counts[-2] == 4
    assert all(counts[v] == counts[-v] == 2 for v in (1, 3, 4, 5))
    assert connected(joined, 5)

    # A variable-wide gauge flip is a bijective renaming and preserves UNSAT.
    gauge_controls = 0
    for v in range(1, 16):
        flipped = tuple(
            tuple(-lit if abs(lit) == v else lit for lit in clause) for clause in u
        )
        assert proper_exact22(flipped, 15)
        assert connected(flipped, 15)
        assert sat_witness(flipped, 15) is None
        gauge_controls += 1

    return {
        "status": "PASS",
        "source": "LSPV-3 W1/U strict exact-(2,2) source",
        "source_variables": 15,
        "source_clauses": 20,
        "source_assignments_exhausted": 1 << 15,
        "source_sat": False,
        "same_sign_swap_pairs_attempted": attempted_same_sign,
        "valid_exact22_swaps": valid_exact22,
        "connected_valid_swaps": connected_valid,
        "sat_after_one_valid_swap": sat_after_swap,
        "first_sat_swap": first,
        "port_identification_control": {
            "two_exact22_equality_modules": True,
            "identified_port": 2,
            "positive_occurrences": counts[2],
            "negative_occurrences": counts[-2],
            "strict_exact22_after_identification": False,
        },
        "gauge_flip_unsat_controls": gauge_controls,
        "limitations": [
            "Finite enumeration is computational evidence for this explicit source.",
            "The all-size port-saturation lemma is proved separately by occurrence counting.",
            "No runtime lower bound or arbitrary-SAT contraction follows.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
