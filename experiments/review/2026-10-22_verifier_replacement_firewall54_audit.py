#!/usr/bin/env python3
"""Finite controls for VERIFIER-REPLACEMENT-FIREWALL54.

The general replacement lemma is proved in the accompanying report.  These
checks only validate representative balanced decorators, structural contrasts,
and the deterministic-trace density accounting used in the Circuit-SAT audit.
They do not prove a complexity-class separation or derandomization.
"""

from itertools import combinations
import json
import random


checks = 0
acceptance_checks = 0
certificate_flip_checks = 0
residual_checks = 0
trace_checks = 0


def check(condition):
    global checks
    checks += 1
    assert condition


def gf2_rank(columns):
    basis = {}
    for value in columns:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def syndrome(columns, assignment):
    out = 0
    for j, column in enumerate(columns):
        if (assignment >> j) & 1:
            out ^= column
    return out


def minimum_balanced_rank(columns, n):
    return min(
        gf2_rank([columns[j] for j in subset])
        for subset in combinations(range(2 * n), n)
    )


def find_matrix(n, target, rng):
    for trial in range(1, 10001):
        columns = [rng.randrange(1, 1 << n) for _ in range(2 * n)]
        if gf2_rank(columns) == n and minimum_balanced_rank(columns, n) >= target:
            return columns, trial
    raise AssertionError((n, target))


def hard_decorator(columns, u, v):
    """Balanced decorator PARITY(u) xor [Hv=0]."""
    return (u.bit_count() & 1) ^ int(syndrome(columns, v) == 0)


def simple_decorator(random_tape):
    return random_tape & 1


rng = random.Random(202610220248)
matrix_results = []
matrices = {}
for n, target in [(3, 1), (4, 2), (5, 2), (6, 3)]:
    columns, trials = find_matrix(n, target, rng)
    matrices[n] = columns
    rank_h = gf2_rank(columns)
    min_lambda = n + 1
    for subset_tuple in combinations(range(2 * n), n):
        subset = set(subset_tuple)
        left = [columns[j] for j in range(2 * n) if j in subset]
        right = [columns[j] for j in range(2 * n) if j not in subset]
        lam = gf2_rank(left) + gf2_rank(right) - rank_h
        check(lam >= 0)
        min_lambda = min(min_lambda, lam)
        residual_checks += 1
    matrix_results.append(
        {
            "n": n,
            "search_trials": trials,
            "minimum_balanced_rank": minimum_balanced_rank(columns, n),
            "minimum_residual_log_width": min_lambda,
            "minimum_residual_width": 1 << min_lambda,
        }
    )


# Language replacement controls.  For each deterministic predicate D(x), both
# decorated verifiers have no accepting tape on NO inputs and exactly half of
# their tapes accept on YES inputs, despite sharply different representations.
predicate_results = []
for name, predicate in [
    ("parity", lambda x: x.bit_count() & 1),
    ("majority4", lambda x: int(x.bit_count() >= 2)),
    ("mod3zero", lambda x: int(x % 3 == 0)),
]:
    n = 3
    columns = matrices[n]
    u_bits = 2 * n
    v_bits = 2 * n
    hard_yes = 0
    simple_yes = 0
    for x in range(16):
        d = predicate(x)
        hard_count = 0
        simple_count = 0
        for tape in range(1 << (u_bits + v_bits)):
            v = tape & ((1 << v_bits) - 1)
            u = tape >> v_bits
            hard_value = d & hard_decorator(columns, u, v)
            simple_value = d & simple_decorator(tape)
            hard_count += hard_value
            simple_count += simple_value
            check((not d and not hard_value and not simple_value) or d)
            acceptance_checks += 1
        expected = d * (1 << (u_bits + v_bits - 1))
        check(hard_count == expected)
        check(simple_count == expected)
        hard_yes += hard_count
        simple_yes += simple_count
    check(hard_yes == simple_yes)
    predicate_results.append(
        {"predicate": name, "aggregate_accepting_tapes_each_verifier": hard_yes}
    )


# Positive-certificate contrast on the hard decorator versus projection r_0.
# Every accepting hard assignment is sensitive to every u bit, whereas fixing
# the single bit r_0=1 certifies the simple decorator.
n = 3
columns = matrices[n]
for v in range(1 << (2 * n)):
    for u in range(1 << (2 * n)):
        if hard_decorator(columns, u, v):
            for bit in range(2 * n):
                check(not hard_decorator(columns, u ^ (1 << bit), v))
                certificate_flip_checks += 1
for tape in range(1 << (4 * n)):
    if tape & 1:
        check(simple_decorator(tape) == 1)
check(certificate_flip_checks > 0)


# Deterministic Tseitin/copy traces preserve projected accepting inputs but
# lower density in the full variable cube by one factor of two per forced bit.
trace_density_results = []
primary_bits = 4
for forced_bits in range(1, 7):
    accepted_projected = 0
    accepted_full = 0
    satisfying_traces = 0
    for primary in range(1 << primary_bits):
        accepts = primary & 1
        accepted_projected += accepts
        expected_trace = []
        state = (primary >> 1) & 1
        for j in range(forced_bits):
            state ^= (primary >> ((j + 2) % primary_bits)) & 1
            expected_trace.append(state)
        expected_trace_word = sum(bit << j for j, bit in enumerate(expected_trace))
        local_trace_count = 0
        for trace in range(1 << forced_bits):
            valid = trace == expected_trace_word
            local_trace_count += valid
            accepted_full += accepts & valid
            trace_checks += 1
        check(local_trace_count == 1)
        satisfying_traces += local_trace_count
    check(satisfying_traces == (1 << primary_bits))
    check(accepted_full == accepted_projected == (1 << (primary_bits - 1)))
    full_density_denominator = 1 << (primary_bits + forced_bits)
    check(accepted_full * (1 << (forced_bits + 1)) == full_density_denominator)
    trace_density_results.append(
        {
            "forced_trace_bits": forced_bits,
            "projected_acceptance_density": "1/2",
            "full_assignment_density": f"1/{1 << (forced_bits + 1)}",
        }
    )


result = {
    "run_id": "VERIFIER-REPLACEMENT-FIREWALL54",
    "status": "PASS",
    "assertions": checks,
    "acceptance_tape_checks": acceptance_checks,
    "positive_certificate_flip_checks": certificate_flip_checks,
    "balanced_cut_checks": residual_checks,
    "deterministic_trace_assignment_checks": trace_checks,
    "matrix_results": matrix_results,
    "predicate_results": predicate_results,
    "trace_density_results": trace_density_results,
    "scope": (
        "Finite regression controls for verifier replacement and representation "
        "density. General claims are proved separately. No P-vs-NP or P-vs-RP "
        "conclusion follows from these experiments."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
