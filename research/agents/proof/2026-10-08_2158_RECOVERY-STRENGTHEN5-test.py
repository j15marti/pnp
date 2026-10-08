#!/usr/bin/env python3
"""Bounded checks for recovered phase-macro and recursive-closure ledgers."""
import json, math, signal, time
from fractions import Fraction

signal.alarm(25)
t0 = time.perf_counter()

def fixed_point(r, eta, theta):
    return max(r, eta / (1 - theta))

rows = []
for r_num in range(1, 9):
    for eta_num in range(0, 9):
        for theta_num in range(1, 8):
            r = Fraction(r_num, 8)
            eta = Fraction(eta_num, 8)
            theta = Fraction(theta_num, 8)
            target = fixed_point(r, eta, theta)
            k = Fraction(19, 3)  # arbitrary starting exponent K
            seq = [k]
            for _ in range(256):
                k = max(r, eta + theta * k)
                seq.append(k)
            assert abs(float(k - target)) < 1e-12
            dist = [abs(x - target) for x in seq]
            assert all(dist[i + 1] <= dist[i] for i in range(len(dist) - 1))
            rows.append({"r": str(r), "eta": str(eta), "theta": str(theta),
                         "fixed_point": str(target)})

# A same-scale typed edge is not by itself an obstruction: A(N)->B(N),
# then B(N)->A(N^theta).  The complete phase contracts by theta.
phase_rows = []
for theta in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
    eta = 1 - theta
    for e in range(8, 21):
        n = 2 ** e
        child = math.ceil(n ** float(theta))
        multiplicity = max(1, math.floor(n ** float(eta)))
        executed_volume = multiplicity * child
        # Rounding allows a constant factor; exponent remains one.
        assert executed_volume <= 2 * n
        assert child < n
        phase_rows.append({"n": n, "theta": str(theta), "eta": str(eta),
                           "largest_exit_child": child,
                           "executed_exit_volume": executed_volume})

# Deduplication cannot replace multiplicity charging.
mult_rows = []
for e in range(10, 31, 5):
    n = 2 ** e
    h = Fraction(3, 5)
    eta = Fraction(3, 5)
    child = math.ceil(n ** float(h))
    q = math.floor(n ** float(eta))
    unique_volume = child
    executed_volume = q * child
    assert executed_volume > n
    mult_rows.append({"n": n, "unique_volume": unique_volume,
                      "executed_volume": executed_volume,
                      "executed_over_n": executed_volume / n})

result = {
    "status": "COMPUTATIONAL",
    "passed": True,
    "scalar_parameter_rows": len(rows),
    "phase_rows": phase_rows,
    "multiplicity_rows": mult_rows,
    "conclusions": [
        "The scalar recursion converges to max(r,eta/(1-theta)) independently of the starting K.",
        "A phase may contain a scale-one typed edge while every complete phase contracts.",
        "Executed duplicate children must be charged with multiplicity; address deduplication is not execution deduplication.",
        "The test validates recurrence algebra only, not existence of an all-input SAT phase compiler or a low-space implementation."
    ],
    "seconds": time.perf_counter() - t0
}
print(json.dumps(result, indent=2))
