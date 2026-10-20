#!/usr/bin/env python3
"""Exact audit for INJECTIVE-THRESHOLD-BARRIER25.

This is not a P-vs-NP experiment.  It checks the rational exponent
inequalities used in the counting proof and small finite controls for the
explicit low-complexity source family.
"""

from fractions import Fraction
import json
import math


def ceil_log2(x: int) -> int:
    if x <= 1:
        return 0
    return (x - 1).bit_length()


checks = 0
failures: list[str] = []


def check(condition: bool, label: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(label)


# Symbolic exponent audit.  If p=a*beta' and p<beta, put
# gamma=(p+beta)/2 and eps=(beta-p)/8.  The proof needs enough room for
# both polynomial/logarithmic overheads:
#
#   p+eps < gamma-eps < gamma+eps < beta.
valid_triples = 0
boundary_triples = 0
for a_num in range(2, 9):
    a = Fraction(a_num, 4)
    for beta_num in range(1, 20):
        beta = Fraction(beta_num, 20)
        for beta_prime_num in range(1, 20):
            beta_prime = Fraction(beta_prime_num, 20)
            p = a * beta_prime
            if p < beta:
                valid_triples += 1
                gap = beta - p
                gamma = (p + beta) / 2
                eps = gap / 8
                check(p < gamma < beta, f"midpoint:{a},{beta},{beta_prime}")
                check(p + eps < gamma - eps,
                      f"lower-overhead:{a},{beta},{beta_prime}")
                check(gamma + eps < beta,
                      f"upper-overhead:{a},{beta},{beta_prime}")
                check(gap > 0, f"positive-gap:{a},{beta},{beta_prime}")
            elif p == beta:
                boundary_triples += 1
                # The strict theorem deliberately says nothing here.
                check(not (p < beta), f"strict-boundary:{a},{beta},{beta_prime}")


# Finite capacity controls for three representative strict-slack points.
# N=2^n, M=2^m with m=ceil(a*n), target circuit size s=2^floor(beta'*m).
# A generous encoding bound for all fan-in-2 circuits of size <=s is used:
# log2(number of circuits) <= log2(s+1)+log2(m+s)
#   + s*(4+2*log2(m+s)).
# The source family has 2^h members, h=2^floor(gamma*n), and each member
# has a DNF of at most h*(2n+1) gates.
finite_cases = [
    (Fraction(1), Fraction(4, 5), Fraction(3, 5)),
    (Fraction(1), Fraction(3, 4), Fraction(1, 2)),
    (Fraction(3, 2), Fraction(4, 5), Fraction(1, 2)),
]
finite_thresholds = []
for a, beta, beta_prime in finite_cases:
    p = a * beta_prime
    gamma = (p + beta) / 2
    first_good = None
    last_bad = None
    for n in range(16, 801):
        m = math.ceil(a * n)
        s_exp = math.floor(beta_prime * m)
        h_exp = math.floor(gamma * n)
        s = 1 << s_exp
        h = 1 << h_exp
        log_count_upper = (
            ceil_log2(s + 1)
            + ceil_log2(m + s)
            + s * (4 + 2 * ceil_log2(m + s))
        )
        source_gate_upper = h * (2 * n + 1)
        target_capacity_ok = h > log_count_upper
        source_yes_ok = source_gate_upper < (1 << math.floor(beta * n))
        good = target_capacity_ok and source_yes_ok
        if good and first_good is None:
            first_good = n
        if not good:
            last_bad = n
        check(log_count_upper > 0, f"positive-count-bound:{a},{n}")
    check(first_good is not None, f"eventual-capacity:{a},{beta},{beta_prime}")
    eventual_threshold = None if last_bad == 800 else (16 if last_bad is None else last_bad + 1)
    check(eventual_threshold is not None,
          f"eventual-tail-through-800:{a},{beta},{beta_prime}")
    finite_thresholds.append({
        "a": str(a),
        "beta": str(beta),
        "beta_prime": str(beta_prime),
        "first_good_n_through_800": first_good,
        "last_bad_n_through_800": last_bad,
        "all_good_from_n_through_800": eventual_threshold,
    })


# Small exhaustive control: every prefix-supported truth table is computed by
# its canonical DNF.  Variables are ordered by the binary representation of
# the truth-table index.
small_dnf_instances = 0
for n in (2, 3):
    N = 1 << n
    for h in range(1, min(6, N) + 1):
        for z in range(1 << h):
            small_dnf_instances += 1
            for x in range(N):
                expected = ((z >> x) & 1) if x < h else 0
                dnf = 0
                for i in range(h):
                    if ((z >> i) & 1) == 0:
                        continue
                    term = 1
                    for bit in range(n):
                        xi = (x >> bit) & 1
                        ii = (i >> bit) & 1
                        term &= int(xi == ii)
                    dnf |= term
                check(dnf == expected, f"dnf:n={n},h={h},z={z},x={x}")


result = {
    "artifact": "INJECTIVE-THRESHOLD-BARRIER25",
    "status": "PASS" if not failures else "FAIL",
    "checks": checks,
    "failures": failures[:20],
    "valid_strict_parameter_triples": valid_triples,
    "boundary_triples_excluded": boundary_triples,
    "finite_thresholds": finite_thresholds,
    "small_dnf_instances": small_dnf_instances,
    "scope": (
        "Exponent algebra, a generous circuit-description count, and small "
        "DNF controls only; no unrestricted algorithmic lower bound."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))

raise SystemExit(0 if not failures else 1)
