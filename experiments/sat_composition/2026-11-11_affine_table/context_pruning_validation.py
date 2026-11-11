#!/usr/bin/env python3
"""Independent finite checks for context pruning and Fourier stabilizers."""
from itertools import product
import json


def dot(a, b):
    return (a & b).bit_count() & 1


def basis(vectors):
    rows = {}
    for x in vectors:
        while x:
            p = x.bit_length() - 1
            if p in rows:
                x ^= rows[p]
            else:
                rows[p] = x
                break
    return tuple(rows[p] for p in sorted(rows, reverse=True))


def forms_for_excluded_pattern(a):
    if not 1 <= a < 8:
        raise ValueError("A satisfying three-clause pattern is nonzero")
    result = basis(b for b in range(8) if dot(a, b) == 0)
    assert len(result) == 2
    return result


def walsh(values):
    transform = list(values)
    stride = 1
    while stride < len(transform):
        for start in range(0, len(transform), 2 * stride):
            for j in range(start, start + stride):
                a, b = transform[j], transform[j + stride]
                transform[j], transform[j + stride] = a + b, a - b
        stride *= 2
    return transform


def validate_stabilizers(max_dimension=4):
    checked = 0
    for k in range(max_dimension + 1):
        size = 1 << k
        for mask in range(1 << size):
            values = [(mask >> x) & 1 for x in range(size)]
            frequencies = basis(a for a, c in enumerate(walsh(values)) if c)
            for delta in range(size):
                direct = all(values[x] == values[x ^ delta] for x in range(size))
                fourier = all(dot(a, delta) == 0 for a in frequencies)
                assert direct == fourier, (k, mask, delta)
            checked += 1
    return checked


def nae(a, b, c):
    return not (a == b == c)


def main():
    pruning_checks = 0
    for a in range(1, 8):
        p, q = forms_for_excluded_pattern(a)
        for y in range(8):
            actual = bool(dot(p, y) or dot(q, y))
            expected = y not in (0, a)
            assert actual == expected
            pruning_checks += 1
    reduction_checks = 0
    for a, b, c in product((False, True), repeat=3):
        reduced = any(nae(a, b, u) and nae(not u, c, False)
                      for u in (False, True))
        assert reduced == (a or b or c)
        reduction_checks += 1
    print(json.dumps({
        "status": "PASS",
        "all_nonzero_pruned_patterns_assignment_checks": pruning_checks,
        "3sat_to_nae3sat_clause_assignment_checks": reduction_checks,
        "all_boolean_tables_stabilizer_checks_through_dimension_4":
            validate_stabilizers(),
    }, indent=2))


if __name__ == "__main__":
    main()
