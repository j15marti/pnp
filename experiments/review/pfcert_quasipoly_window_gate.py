#!/usr/bin/env python3
"""Bounded exact-arithmetic checks for CC-0004.

Finite tests validate formulas and hostile controls only; they do not prove
the asymptotic theorems or construct a PFCERT verifier.
"""
from __future__ import annotations

import json
import math
import signal
from pathlib import Path


def timeout(_signum, _frame):
    raise TimeoutError("25-second cooperative budget exceeded")


signal.signal(signal.SIGALRM, timeout)
signal.alarm(25)

window_cases = []
for c in range(1, 7):
    for d in range(1, 6):
        a = math.isqrt(c * d) + 1
        while a * a <= c * d:
            a += 1
        for r in range(2, 17):
            # m=2^r, n=m^a.  Source time is 2^(c r^2); a degree-d
            # universal simulation needs exponent c*d*r^2, whereas
            # t(n)=2^((a r)^2).
            source_exp = c * r * r
            simulated_exp = d * source_exp
            window_exp = (a * r) ** 2
            assert window_exp > simulated_exp
            window_cases.append((c, d, a, r, window_exp - simulated_exp))

tree_cases = []
for k in range(1, 11):
    n = 2**k
    logn = k
    T = n**logn
    nodes = 2 * T - 1
    # Recursive full binary checkpoint tree: F(1)=1, F(T)=1+2F(T/2).
    f = 1
    size = 1
    while size < T:
        f = 1 + 2 * f
        size *= 2
    assert f == nodes
    tree_cases.append({"n": n, "T_bits": T.bit_length(), "nodes_bits": nodes.bit_length()})

acquirer_cases = []
for kappa in range(0, 6):
    for v in range(0, 5):
        for r in range(3, 15):
            M = 2**r
            w = kappa * r
            q = M**v
            b = q
            reset = b * max(1, math.ceil(math.log2(b + 2)))
            candidates = 2 ** (w + 1) - 1
            total = candidates * (q + reset + w + r) + w
            assert candidates == sum(2**j for j in range(w + 1))
            assert total >= candidates * q
            acquirer_cases.append((kappa, v, r, total.bit_length()))

# The smallest selector hostile control: the admissible list contains both
# Boolean endpoints.  Either fixed selector is wrong for one true endpoint.
selector_failures = []
accepted = (0, 1)
for selector in accepted:
    for true_endpoint in accepted:
        if selector != true_endpoint:
            selector_failures.append({"selector": selector, "truth": true_endpoint})
assert selector_failures == [
    {"selector": 0, "truth": 1},
    {"selector": 1, "truth": 0},
]

# Dirty-state control and explicit clear repair for one persistent cell.
dirty_failures = 0
reset_successes = 0
for width in range(1, 19):
    state = 0
    outcomes = []
    for candidate in range(1 << width):
        outcomes.append(state == 0 and candidate == (1 << width) - 1)
        state = 1
    if not any(outcomes):
        dirty_failures += 1
    outcomes = []
    state = 0
    for candidate in range(1 << width):
        state = 0
        outcomes.append(state == 0 and candidate == (1 << width) - 1)
        state = 1
    if sum(outcomes) == 1 and outcomes[-1]:
        reset_successes += 1
assert dirty_failures == 18 and reset_successes == 18

result = {
    "run_id": "CC-0004",
    "status": "COMPUTATIONAL_FORMULA_CHECK_ONLY",
    "window_padding_cases": len(window_cases),
    "minimum_window_exponent_margin": min(x[-1] for x in window_cases),
    "checkpoint_tree_cases": tree_cases,
    "reset_aware_acquirer_cases": len(acquirer_cases),
    "selector_hostile_failures": selector_failures,
    "dirty_state_failures": dirty_failures,
    "explicit_reset_successes": reset_successes,
    "interpretation": (
        "Exact integers confirm the padding inequality, full checkpoint-tree "
        "count, reset-aware enumeration count, and two-endpoint selector controls. "
        "No finite test establishes an asymptotic lower bound or a PFCERT verifier."
    ),
}

signal.alarm(0)
print(json.dumps(result, indent=2, sort_keys=True))
