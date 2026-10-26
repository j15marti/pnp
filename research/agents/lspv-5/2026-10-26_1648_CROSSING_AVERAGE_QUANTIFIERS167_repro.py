#!/usr/bin/env python3
"""Finite controls for CROSSING-AVERAGE-QUANTIFIERS167.

This checks the exact shortest-code average for distinct nonempty words,
the conservative m/(4B) lower bound used in the proof, the double-average
common-input step, and an explicit counterexample to summing per-cut maxima.
No external dependencies or randomness are used.
"""

from itertools import combinations, product
from math import ceil, log2
import json


def min_nonempty_total_length(alphabet: int, count: int) -> int:
    """Exact minimum total length of count distinct nonempty A-ary words."""
    assert alphabet >= 2 and count >= 1
    left = count
    length = 1
    total = 0
    while left:
        take = min(left, alphabet ** length)
        total += take * length
        left -= take
        length += 1
    return total


def brute_min_total(alphabet: int, count: int, max_length: int = 4) -> int:
    words = []
    for length in range(1, max_length + 1):
        words.extend(product(range(alphabet), repeat=length))
    return min(sum(len(w) for w in subset) for subset in combinations(words, count))


def cyclic_cost_matrix(alphabet: int, m: int, cuts: int):
    count = 2 ** m
    lengths = []
    length = 1
    while len(lengths) < count:
        lengths.extend([length] * min(alphabet ** length, count - len(lengths)))
        length += 1
    matrix = [[lengths[(a + g) % count] for a in range(count)] for g in range(cuts)]
    row_totals = [sum(matrix[g][a] for g in range(cuts)) for a in range(count)]
    return lengths, row_totals


def main():
    checks = 0

    brute_cases = []
    for alphabet, count in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4)]:
        exact = min_nonempty_total_length(alphabet, count)
        brute = brute_min_total(alphabet, count)
        assert exact == brute
        checks += 1
        brute_cases.append({"alphabet": alphabet, "count": count, "minimum_total": exact})

    code_bound_cases = 0
    tightest_ratio = None
    for alphabet in range(2, 65):
        B = ceil(log2(alphabet))
        for m in range(1, 17):
            count = 2 ** m
            total = min_nonempty_total_length(alphabet, count)
            # The report proves average length >= m/(4B).
            assert 4 * B * total >= m * count
            ratio = (total / count) / (m / (4 * B))
            tightest_ratio = ratio if tightest_ratio is None else min(tightest_ratio, ratio)
            checks += 1
            code_bound_cases += 1

    double_average_cases = 0
    weakest_double_ratio = None
    for alphabet in [2, 3, 4, 5, 8, 16]:
        B = ceil(log2(alphabet))
        for m in range(1, 9):
            for cuts in [1, 2, 3, 7, 17]:
                lengths, rows = cyclic_cost_matrix(alphabet, m, cuts)
                count = 2 ** m
                total_all = sum(rows)
                assert total_all == cuts * sum(lengths)
                assert max(rows) * count >= total_all
                assert 4 * B * max(rows) >= cuts * m
                ratio = max(rows) / (cuts * m / (4 * B))
                weakest_double_ratio = ratio if weakest_double_ratio is None else min(weakest_double_ratio, ratio)
                checks += 3
                double_average_cases += 1

    # Falsifier for the invalid quantifier jump: every cut has a high-cost
    # input, but no single input bears the sum of per-cut maxima.
    D = 32
    H = 32
    max_only = [[H if a == g else 1 for a in range(D)] for g in range(D)]
    per_cut_max_sum = sum(max(row) for row in max_only)
    per_input_totals = [sum(max_only[g][a] for g in range(D)) for a in range(D)]
    assert per_cut_max_sum == D * H
    assert max(per_input_totals) == H + D - 1
    assert max(per_input_totals) < per_cut_max_sum
    checks += 3

    result = {
        "run_id": "CROSSING-AVERAGE-QUANTIFIERS167",
        "status": "COMPUTATIONAL supporting a separate exact proof",
        "randomness": "none",
        "assertion_groups": checks,
        "failures": 0,
        "brute_shortest_code_cases": brute_cases,
        "code_bound_cases": code_bound_cases,
        "tightest_observed_ratio_to_m_over_4B": tightest_ratio,
        "double_average_cases": double_average_cases,
        "weakest_observed_double_average_ratio": weakest_double_ratio,
        "max_only_countercontrol": {
            "cuts": D,
            "inputs": D,
            "high_cost": H,
            "sum_of_per_cut_maxima": per_cut_max_sum,
            "largest_single_input_total": max(per_input_totals),
            "invalid_inference_falsified": True,
        },
        "scope": "abstract complete crossing-sequence code lengths and quantifiers; not measured machine time and not a full-SAT lower bound",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
