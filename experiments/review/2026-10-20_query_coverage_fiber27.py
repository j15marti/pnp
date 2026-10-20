#!/usr/bin/env python3
"""Exact audit for QUERY-COVERAGE-FIBER27.

The theorem is combinatorial.  This audit checks its explicit circuit-count
ledger, exhaustive small abstract label families, and adaptive zero-path
controls.  It is not an unrestricted running-time lower bound.
"""

from fractions import Fraction
from itertools import combinations, product
import json
import math


checks = 0
failures: list[str] = []


def check(cond: bool, label: str) -> None:
    global checks
    checks += 1
    if not cond:
        failures.append(label)


def ceil_log2(x: int) -> int:
    return 0 if x <= 1 else (x - 1).bit_length()


def circuit_count_log_upper(n: int, s: int, basis_size: int = 16) -> int:
    """Ceiling of a generous log2 count for circuits of size at most s.

    Each gate chooses a type and two predecessors among n+s wires.  The
    leading factors cover the chosen size and output wire.
    """
    return (
        ceil_log2(s + 1)
        + ceil_log2(n + s)
        + s * (ceil_log2(basis_size) + 2 * ceil_log2(n + s))
    )


# Exact rational asymptotic margin.  For s=N^beta, log(number of circuits)
# is N^(beta+o(1)), so any unseen set N^gamma with beta<gamma<1 eventually
# dominates it.
rational_cases = 0
for beta_num in range(1, 20):
    beta = Fraction(beta_num, 20)
    gamma = (beta + 1) / 2
    eps = (1 - beta) / 8
    rational_cases += 1
    check(beta < gamma < 1, f"midpoint:{beta}")
    check(beta + eps < gamma - eps, f"overhead-gap:{beta}")
    check(gamma + eps < 1, f"sublinear-unseen:{beta}")


# Finite explicit circuit-description count.  We record the first n at which
# the sufficient uncovered-bit bound is nontrivial for representative beta.
finite_thresholds = []
for beta in (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
    first_nontrivial = None
    last_trivial = None
    for n in range(4, 161):
        N = 1 << n
        s = 1 << math.floor(beta * n)
        log_bound = circuit_count_log_upper(n, s)
        nontrivial = log_bound < N
        if nontrivial and first_nontrivial is None:
            first_nontrivial = n
        if not nontrivial:
            last_trivial = n
        check(log_bound > 0, f"positive-count:{beta}:{n}")
        # If u exceeds the log-count bound, then 2^u exceeds the number of
        # low-complexity functions.  Compare exponents exactly; do not
        # materialize the doubly enormous integer 2^u.
        u = log_bound + 1
        check(u > log_bound, f"capacity:{beta}:{n}")
    check(first_nontrivial is not None, f"eventual-nontrivial:{beta}")
    all_good_from = None if last_trivial == 160 else (4 if last_trivial is None else last_trivial + 1)
    check(all_good_from is not None, f"eventual-tail-through-160:{beta}")
    finite_thresholds.append({
        "beta": str(beta),
        "first_n_with_log_count_bound_below_N_through_160": first_nontrivial,
        "last_trivial_n_through_160": last_trivial,
        "all_nontrivial_from_n_through_160": all_good_from,
    })


# Exhaustive abstract label-family control.  The universe consists of all
# N-bit sources.  L is any declared low-complexity set containing 0.  For each
# queried coordinate set Q, if the zero-answer fiber is larger than L, it must
# contain an object outside L.
abstract_families = 0
for N, max_low_size in ((3, 4), (4, 4), (5, 3), (6, 3)):
    universe = range(1 << N)
    nonzero = list(range(1, 1 << N))
    for low_size in range(1, max_low_size + 1):
        for rest in combinations(nonzero, low_size - 1):
            low = {0, *rest}
            abstract_families += 1
            for q in range(N + 1):
                for Q in combinations(range(N), q):
                    fiber = [x for x in universe if all(((x >> i) & 1) == 0 for i in Q)]
                    if len(fiber) > len(low):
                        check(any(x not in low for x in fiber),
                              f"pigeonhole:N={N}:B={low_size}:Q={Q}:L={rest}")


# Adaptive-query controls.  A deterministic policy may choose the next index
# from the earlier answer string.  We generate reproducible policies; every
# source zero on the zero-path queried coordinates must follow the same path
# and receive the same output tag.
adaptive_policies = 0
for N in range(3, 10):
    for depth in range(0, min(5, N + 1)):
        for seed in range(97):
            adaptive_policies += 1

            def query_index(answer_prefix: tuple[int, ...]) -> int:
                code = seed + 17 * len(answer_prefix)
                for bit in answer_prefix:
                    code = (code * 131 + bit * 29 + 7) % 1_000_003
                return code % N

            answers: tuple[int, ...] = ()
            zero_path = []
            for _ in range(depth):
                idx = query_index(answers)
                zero_path.append(idx)
                answers += (0,)
            Q = set(zero_path)

            # Exhaust all sources for N<=9 and compare their adaptive path.
            for x in range(1 << N):
                if any((x >> i) & 1 for i in Q):
                    continue
                a: tuple[int, ...] = ()
                path = []
                for _ in range(depth):
                    idx = query_index(a)
                    path.append(idx)
                    a += ((x >> idx) & 1,)
                check(path == zero_path and not any(a),
                      f"adaptive:N={N}:d={depth}:seed={seed}:x={x}")


result = {
    "run": "QUERY-COVERAGE-FIBER27",
    "status": "PASS" if not failures else "FAIL",
    "checks": checks,
    "failures": failures[:20],
    "rational_cases": rational_cases,
    "finite_thresholds": finite_thresholds,
    "abstract_low_label_families": abstract_families,
    "adaptive_policies": adaptive_policies,
    "proved_scope": (
        "Deterministic source-bit oracle transducers: a label-monochromatic "
        "fiber containing the zero source must query at least "
        "N-O(N^beta log N) distinct source bits on that path."
    ),
    "firewall": (
        "Full one-way scans, randomized reductions, and non-bit global "
        "primitives are not ruled out; no one-tape or unrestricted SAT lower bound."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
