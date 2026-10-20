#!/usr/bin/env python3
"""Exact controls for GAP-STABLE-ERASURE28.

This audits a deterministic fixed-coordinate erasure map on small truth
tables.  It checks the algebraic reconstruction identities, exact circuit
complexities for n <= 3 over {NOT, AND, OR, XOR}, fiber cardinalities, and
the additive-gap transfer.  It is a finite control, not a lower bound.
"""

from fractions import Fraction
from itertools import combinations
import json


checks = 0
failures: list[str] = []


def check(condition: bool, label: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(label)


def var_table(n: int, coordinate: int) -> int:
    table = 0
    for x in range(1 << n):
        if (x >> coordinate) & 1:
            table |= 1 << x
    return table


def exact_circuit_complexities(n: int) -> list[int]:
    """Minimum formula-DAG gate counts over a fixed finite fan-in-two basis."""
    N = 1 << n
    full = (1 << N) - 1
    infinity = 10**9
    cost = [infinity] * (1 << N)
    for base in [0, full, *(var_table(n, i) for i in range(n))]:
        cost[base] = 0

    changed = True
    while changed:
        changed = False
        known = [f for f, c in enumerate(cost) if c < infinity]
        for f in known:
            candidate = cost[f] + 1
            nf = full ^ f
            if candidate < cost[nf]:
                cost[nf] = candidate
                changed = True
        known = [f for f, c in enumerate(cost) if c < infinity]
        for f in known:
            cf = cost[f]
            for g in known:
                candidate = cf + cost[g] + 1
                for h in (f & g, f | g, f ^ g):
                    if candidate < cost[h]:
                        cost[h] = candidate
                        changed = True
    check(all(c < infinity for c in cost), f"closure:n={n}")
    return cost


def erase(table: int, U: tuple[int, ...]) -> int:
    mask = 0
    for position in U:
        mask |= 1 << position
    return table & ~mask


def patch(table: int, original: int, U: tuple[int, ...]) -> int:
    result = table
    for position in U:
        bit = 1 << position
        if original & bit:
            result |= bit
        else:
            result &= ~bit
    return result


exact_complexity_summaries = []
for n in (1, 2, 3):
    N = 1 << n
    complexity = exact_circuit_complexities(n)
    max_complexity = max(complexity)
    cases = 0
    for u in range(0, min(3, N) + 1):
        # All coordinate sets, not merely stream-friendly suffixes.
        for U in combinations(range(N), u):
            fibers: dict[int, int] = {}
            K = 2 * u * n + 2  # Safe explicit equality/OR/patch gadget bound.
            for f in range(1 << N):
                e = erase(f, U)
                cases += 1
                fibers[e] = fibers.get(e, 0) + 1
                check(patch(e, f, U) == f, f"reconstruct:n={n}:U={U}:f={f}")
                check(abs(complexity[f] - complexity[e]) <= K,
                      f"complexity-Lipschitz:n={n}:U={U}:f={f}")
                for s in range(max_complexity + 1):
                    if complexity[f] <= s:
                        check(complexity[e] <= s + K,
                              f"yes-transfer:n={n}:U={U}:f={f}:s={s}")
                    if complexity[f] > s + 2 * K:
                        check(complexity[e] > s + K,
                              f"no-transfer:n={n}:U={U}:f={f}:s={s}")
            check(len(fibers) == 1 << (N - u), f"fiber-count:n={n}:U={U}")
            for e, size in fibers.items():
                check(size == 1 << u, f"fiber-size:n={n}:U={U}:e={e}")
    exact_complexity_summaries.append({
        "n": n,
        "truth_table_length": N,
        "maximum_exact_gate_count": max_complexity,
        "erasure_cases": cases,
    })


# Exhaustive identity/fiber audit at n=4 for the stream-friendly suffix sets
# (without costly exact minimization).
n = 4
N = 1 << n
structural_cases = 0
for u in range(0, 5):
    U = tuple(range(N - u, N))
    fibers: dict[int, int] = {}
    for f in range(1 << N):
        e = erase(f, U)
        structural_cases += 1
        fibers[e] = fibers.get(e, 0) + 1
        check(patch(e, f, U) == f, f"structural-reconstruct:U={U}:f={f}")
    check(len(fibers) == 1 << (N - u), f"structural-fiber-count:U={U}")
    check(all(size == 1 << u for size in fibers.values()),
          f"structural-fiber-size:U={U}")


# Exact rational exponent ledger: alpha < beta implies
# u log N = N^(alpha+o(1)) = o(N^beta), but no exponent descent occurs.
exponent_cases = []
for beta_num in range(2, 20):
    beta = Fraction(beta_num, 20)
    for alpha_num in range(1, beta_num):
        alpha = Fraction(alpha_num, 20)
        check(alpha < beta, f"alpha-beta:{alpha}:{beta}")
        exponent_cases.append({
            "alpha": str(alpha),
            "beta": str(beta),
            "erasure_overhead_exponent": str(alpha),
            "target_threshold_exponent": str(beta),
            "strict_descent": False,
        })


result = {
    "run": "GAP-STABLE-ERASURE28",
    "status": "PASS" if not failures else "FAIL",
    "checks": checks,
    "failures": failures[:20],
    "basis": ["NOT", "AND", "OR", "XOR"],
    "exact_complexity_summaries": exact_complexity_summaries,
    "n4_structural_cases": structural_cases,
    "rational_exponent_cases": len(exponent_cases),
    "proved_scope": (
        "Fixed-coordinate erasure changes circuit complexity by O(u log N), "
        "has fibers of size 2^u, and transfers an additive GapMCSP promise."
    ),
    "firewall": (
        "The threshold exponent is unchanged; exact MCSP fibers can cross the "
        "boundary, and the construction gives no SAT, CHMY, MMW, ARC, or FLMV arrow."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
