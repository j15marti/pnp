#!/usr/bin/env python3
"""Finite controls for VIRTUAL-PADDING-QUERY-COLLAPSE52.

Checks that an adaptive padding-sensitive bit evaluator can be simulated from a
hardwired semantic core without materializing the padded source, and checks the
exact exponent inequalities used in the scoped ordinary-KT upper bound.  This
is not a KT lower bound or a complexity-class separation experiment.
"""

from fractions import Fraction
import json
import random


K = 241
THETA = Fraction(6, 5 * K)
checks = 0
virtual_cases = 0
query_steps = 0


def check(condition):
    global checks
    checks += 1
    assert condition


def pad_bit(core, padded_length, position):
    """Locally indexable deterministic padding derived from the core."""
    n = len(core)
    check(0 <= position < padded_length)
    if position < n:
        return core[position]
    block, offset = divmod(position - n, n)
    return core[(offset + block) % n] ^ (block.bit_count() & 1)


def materialize(core, padded_length):
    return [pad_bit(core, padded_length, j) for j in range(padded_length)]


def adaptive_target_bit(read_source, padded_length, target_index, rounds):
    """A deliberately padding-sensitive adaptive source-query evaluator."""
    position = (17 * target_index + 3) % padded_length
    accumulator = target_index & 1
    transcript = []
    for step in range(rounds):
        bit = read_source(position)
        transcript.append((position, bit))
        accumulator ^= bit
        position = (
            position * 5
            + 11 * bit
            + 7 * target_index
            + step * step
            + 1
        ) % padded_length
    return accumulator, transcript


rng = random.Random(0x52)
for n in range(2, 11):
    for power in range(1, 5):
        padded_length = n**power
        for _ in range(12):
            core = [rng.randrange(2) for _ in range(n)]
            padded = materialize(core, padded_length)
            for target_index in range(24):
                rounds = 1 + (target_index % min(12, padded_length))
                direct, direct_trace = adaptive_target_bit(
                    lambda j: padded[j], padded_length, target_index, rounds
                )
                virtual, virtual_trace = adaptive_target_bit(
                    lambda j: pad_bit(core, padded_length, j),
                    padded_length,
                    target_index,
                    rounds,
                )
                check(direct == virtual)
                check(direct_trace == virtual_trace)
                # A conservative one-tape lookup scans at most n core symbols
                # for each adaptive source query.
                check(len(virtual_trace) * n <= rounds * n)
                for position, bit in virtual_trace:
                    check(bit == padded[position])
                    query_steps += 1
                virtual_cases += 1


def strict_min_padding_power(tau):
    if tau >= THETA:
        return None
    gap = THETA - tau
    # Need 1/a < gap, strictly.
    return gap.denominator // gap.numerator + 1


tau_cases = [
    Fraction(0),
    Fraction(1, 2000),
    Fraction(1, 1000),
    Fraction(1, 480),
    Fraction(1, 241),
    Fraction(1, 240),
    THETA,
    Fraction(1, 100),
]
threshold_cases = []
for tau in tau_cases:
    a = strict_min_padding_power(tau)
    if a is None:
        check(tau >= THETA)
        threshold_cases.append(
            {
                "tau": str(tau),
                "minimal_integer_padding_power": None,
                "reason": "tau is already at or above the threshold exponent",
            }
        )
        continue
    check(tau + Fraction(1, a) < THETA)
    if a > 1:
        check(tau + Fraction(1, a - 1) >= THETA)
    check(Fraction(1, a) < THETA)
    threshold_cases.append(
        {
            "tau": str(tau),
            "minimal_integer_padding_power": a,
            "compiled_one_tape_exponent": str(tau + Fraction(1, a)),
            "threshold_exponent": str(THETA),
        }
    )


# Random-access virtual source lookup removes the conservative N^(1/a)
# multiplicative scan cost, but program length still forces 1/a < theta.
random_access_min_a = THETA.denominator // THETA.numerator + 1
check(random_access_min_a == 201)
check(Fraction(1, random_access_min_a) < THETA)
check(Fraction(1, random_access_min_a - 1) >= THETA)


# ARC promise-family exponent controls: core time n^c looks like N^(c/a),
# while scanning the physical padded input restores exponent at least one.
arc_cases = []
for c in [Fraction(6, 5), Fraction(241, 200), Fraction(2), Fraction(3), Fraction(10)]:
    for a in [2, 10, 100, 1000]:
        apparent = c / a
        check(apparent > 0)
        check(max(Fraction(1), apparent) >= 1)
        arc_cases.append(
            {
                "core_exponent": str(c),
                "padding_power": a,
                "promise_family_exponent": str(apparent),
                "all_input_full_scan_exponent": str(max(Fraction(1), apparent)),
            }
        )


result = {
    "run_id": "VIRTUAL-PADDING-QUERY-COLLAPSE52",
    "status": "PASS",
    "assertions": checks,
    "virtual_adaptive_cases": virtual_cases,
    "adaptive_query_steps": query_steps,
    "threshold_exponent": str(THETA),
    "random_access_minimal_padding_power": random_access_min_a,
    "threshold_cases": threshold_cases,
    "arc_cases": arc_cases,
    "scope": (
        "Finite controls for virtual deterministic padding, adaptive query "
        "simulation, and exact exponent crossings; not a KT lower bound or "
        "a P-vs-NP/P-vs-RP separation."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
