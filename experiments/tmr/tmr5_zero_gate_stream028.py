#!/usr/bin/env python3
"""TMR-5/023: independent one-pass, length-blind, zero-gate MCSP recognizer.
The implementation uses Python integers for finite testing only; symbolic proof
provides the charged one-work-tape finite-alphabet implementation.
"""
import json
import random


def stream_zero_gate(bits):
    """No advance length; update candidate projection flags as bits arrive."""
    j = 0
    alive = []
    prefix_zero = True
    prefix_one = True
    steps = 0
    for value in bits:
        assert value in (0, 1)
        if j and j.bit_count() == 1:
            # The newly introduced input bit is zero on all prior indices.
            alive.append(prefix_zero)
        for i in range(len(alive)):
            alive[i] = alive[i] and (value == ((j >> i) & 1))
            steps += 1
        prefix_zero &= value == 0
        prefix_one &= value == 1
        j += 1
    if j < 2 or (j & (j - 1)):
        return None, steps  # Invalid length for n >= 1
    return bool(prefix_zero or prefix_one or any(alive)), steps


def independent_direct(bits):
    N = len(bits)
    if N < 2 or N & (N - 1):
        return None
    if all(b == 0 for b in bits) or all(b == 1 for b in bits):
        return True
    return any(all(bits[j] == ((j >> i) & 1) for j in range(N))
               for i in range(N.bit_length() - 1))


def main():
    case_count = 0
    yes_count = 0
    no_count = 0
    total_comparisons = 0
    by_n = []
    for n in range(1, 5):
        N = 1 << n
        count = 0
        positives = 0
        for word in range(1 << N):
            bits = [(word >> j) & 1 for j in range(N)]
            got, cost = stream_zero_gate(iter(bits))
            expected = independent_direct(bits)
            assert got == expected, (N, word, got, expected)
            count += 1
            positives += int(got)
            total_comparisons += cost
        case_count += count
        yes_count += positives
        no_count += count - positives
        by_n.append({"n": n, "N": N, "checked": count, "yes": positives,
                     "no": count - positives})
    rng = random.Random(20261114)
    random_checks = 1024
    for _ in range(random_checks):
        N = 32
        bits = [rng.randrange(2) for _ in range(N)]
        got, cost = stream_zero_gate(iter(bits))
        assert got == independent_direct(bits)
        total_comparisons += cost
    invalid_checks = 0
    for N in range(0, 31):
        if N not in (2, 4, 8, 16):
            got, _ = stream_zero_gate(iter([0] * N))
            assert got is None
            invalid_checks += 1
    result = {"study": "TMR5-ZEROGATE-STREAM28", "seed": 20261114,
              "model": "exact threshold-0 MCSP; free constants and input wires; one-pass source",
              "exhaustive_cases": case_count, "yes_cases": yes_count,
              "no_cases": no_count, "per_n": by_n,
              "random_32bit_cases": random_checks,
              "invalid_length_checks": invalid_checks,
              "candidate_bit_comparisons": total_comparisons,
              "failed_assertions": 0,
              "caution": "Python proxy, not native finite-alphabet TM execution; symbolic simulation separately proved"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
