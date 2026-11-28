#!/usr/bin/env python3
"""Evaluate the linear-threshold theorem for AG(2t)-n (Grok 2026-11-28 1603 KST).

s4(n) = max{m : m(m-1) <= 2(n-1)}         (Sidon bound: an m-set with m > s4
                                             contains 4 distinct points, XOR 0)
s6(n) = max{m : C(m,3) <= n(3m-7)/2}        (m > s6 => 6 distinct points, XOR 0)
Greedy: from an m-set one extracts >= ceil((m - s4)/4) disjoint zero-sum 4-sets.
Theorem (NO side): with M = n/2 (size of a majority colour class),
  t even : t/2 <= ceil((M - s4)/4)
  t odd  : M > s6  and (t-3)/2 <= ceil((M - 6 - s4)/4)   (t >= 3)
implies AG(2t)-n is UNSAT.  YES side (Proposition 1): t >= n/4 - 1 => SAT.
This script prints, for k = 3..14, the largest t certified NO by the theorem,
the YES threshold n/4, and the quadratic T2 bound (n > 4t^2 + 2t - 2).
"""
from math import comb, ceil, isqrt
def s4(n):
    m = 1
    while (m + 1) * m <= 2 * (n - 1): m += 1
    return m
def s6(n):
    m, best = 3, 2
    while m <= n:
        if comb(m, 3) * 2 <= n * (3 * m - 7): best = m
        m += 1
    return best
def q(m, n):
    a = s4(n)
    return 0 if m <= a else -(-(m - a) // 4)
def certified_no(t, n):
    M = n // 2
    if t % 2 == 0: return t // 2 <= q(M, n)
    if t < 3: return False
    return M > s6(n) and (t - 3) // 2 <= q(M - 6, n)
rows = []
print("k   n     s4   s6   maxNO_t(theorem)  YES_for_t>=n/4  T2_quadratic_max_t  NO-set-is-interval")
for k in range(3, 15):
    n = 1 << k
    no = [t for t in range(2, n) if certified_no(t, n)]
    mx = max(no) if no else None
    interval = (no == list(range(2, mx + 1))) if no else None
    tq = max([t for t in range(2, n) if n > 4 * t * t + 2 * t - 2], default=None)
    print(f"{k:<3} {n:<5} {s4(n):<4} {s6(n):<4} {str(mx):<17} {n//4:<15} {str(tq):<19} {interval}")
