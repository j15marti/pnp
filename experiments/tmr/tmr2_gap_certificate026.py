#!/usr/bin/env python3
"""TMR-2 MCSP gap-cylinder and query-randomization finite verifier.
Only finite exact truth-table enumeration; NOT a TM compiler or a P-vs-NP proof.
"""
import json
import math
from collections import Counter


def wires(n):
    length = 1 << n
    mask = (1 << length) - 1
    projections = [sum(((i >> v) & 1) << i for i in range(length)) for v in range(n)]
    return set([0, mask] + projections)


def circuits_at_most_one_gate(n):
    mask = (1 << (1 << n)) - 1
    inputs = wires(n)
    out = set(inputs)
    for a in inputs:
        out.add(mask ^ a)
        for b in inputs:
            out.add(a & b)
            out.add(a | b)
    return out


def hamming_ball_volume(n_bits, radius):
    return sum(math.comb(n_bits, j) for j in range(radius + 1))


def accepting_certificate_depths(yes_tables, far_tables, n_bits):
    """Exhaust every source coordinate subset via downward subset zeta transform."""
    size = 1 << n_bits
    mask_all = size - 1
    depths = {}
    for x in sorted(yes_tables):
        possible_bad = bytearray(size)
        for y in far_tables:
            zero_agreement = (~(x ^ y)) & mask_all
            possible_bad[zero_agreement] = 1
        for bit in range(n_bits):
            jump = 1 << bit
            for block in range(0, size, 2 * jump):
                for low in range(block, block + jump):
                    possible_bad[low] |= possible_bad[low + jump]
        # A mask Q is a sufficient accepting certificate iff no promised NO
        # agrees with x on all queried coordinates in Q.
        best = min(q.bit_count() for q in range(size) if not possible_bad[q])
        for q in range(size):
            if q.bit_count() < best:
                assert possible_bad[q], "shorter accepting certificate found"
        depths[str(x)] = best
    return depths


def expand_ignored_inputs(table, n, t):
    nbits = 1 << n
    return sum(table << (z * nbits) for z in range(1 << t))


def normalized_padding_checks():
    total = 0
    for n in (2, 3):
        nbits = 1 << n
        for s in (0, 1):
            old_yes = wires(n) if s == 0 else circuits_at_most_one_gate(n)
            new_yes = wires(n + 1) if s == 0 else circuits_at_most_one_gate(n + 1)
            for f in range(1 << nbits):
                d = min((f ^ g).bit_count() for g in old_yes)
                expanded = expand_ignored_inputs(f, n, 1)
                d2 = min((expanded ^ g).bit_count() for g in new_yes)
                assert d2 == 2 * d, (n, s, f, d, d2)
                total += 1
    return total


def main():
    n, N, eps_num, eps_den = 4, 16, 1, 4
    threshold_dist = N * eps_num // eps_den
    yes = wires(n)
    assert len(yes) == n + 2 == 6
    yes1 = circuits_at_most_one_gate(n)
    assert len(yes1) >= len(yes)
    far = [f for f in range(1 << N) if min((f ^ g).bit_count() for g in yes) >= threshold_dist]
    depths = accepting_certificate_depths(yes, far, N)
    assert depths[str(0)] == 13
    # For every 12-observation set on the all-zero table, the four unseen
    # coordinates form an actual far-NO completion (not merely a count).
    combinatorial_controls = 0
    for unseen in range(1 << N):
        if unseen.bit_count() != threshold_dist:
            continue
        assert unseen in far
        combinatorial_controls += 1
    assert combinatorial_controls == math.comb(16, 4) == 1820
    volume = hamming_ball_volume(N, threshold_dist - 1)
    D0 = n + 2
    assert volume == 697 and D0 * volume < (1 << N)
    derived_lower = math.ceil(N - math.log2(D0 * volume))
    assert all(d >= derived_lower for d in depths.values())
    delta = 0.05
    q = math.ceil((math.log(D0) + math.log(1 / delta)) / (eps_num / eps_den))
    assert D0 * math.exp(-q * eps_num / eps_den) <= delta
    maximum_exact_union_bound = max(
        sum((1 - (y ^ g).bit_count() / N) ** q for g in yes) for y in far
    )
    assert maximum_exact_union_bound <= delta
    padding_checks = normalized_padding_checks()
    result = {
        "model": "fan-in-two AND/OR unary NOT; free constants and variables; circuit gate bound s=0",
        "n": n, "N": N, "epsilon": eps_num / eps_den,
        "yes_count": D0, "one_gate_yes_count": len(yes1),
        "far_no_count": len(far), "near_or_yes_count": (1 << N) - len(far),
        "radius": threshold_dist - 1, "ball_volume": volume,
        "counting_depth_lower_bound": derived_lower,
        "accepting_depths_all_six_yes_tables": depths,
        "all_zero_exact_deterministic_promise_depth": depths[str(0)],
        "adversarial_unseen_four_bit_sets_checked": combinatorial_controls,
        "randomized_samples_with_replacement_q": q,
        "randomized_error_target": delta,
        "largest_exact_union_bound_over_all_far_no": maximum_exact_union_bound,
        "ignored_input_padding_distance_equalities_checked": padding_checks,
        "failed_assertions": 0,
        "scope": "COMPUTATIONAL finite evidence; theoretical all-n proofs reported separately",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
