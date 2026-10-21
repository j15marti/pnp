"""Exact-rational check: the generic KT ceiling KT(R(x)) <= n + T(n) cannot by itself
exclude HIGH targets at threshold p(M)=M^(6/(5k)), because M <= T(n) forces p(M) <= T(n).
Contrast with padded, index-local targets (padding firewall 51) where t_idx = O(log a)."""
from fractions import Fraction as F
k = 241
eps = F(6, 5*k)
bad = 0; checked = 0
for c in range(1, 41):            # reduction time n^c
    for m in range(1, c+1):        # output length n^m <= time n^c
        # exponent of p(M) vs exponent of ceiling max(1,c)
        p_exp = eps*m; ceil_exp = max(1, c)
        checked += 1
        assert p_exp < ceil_exp     # threshold strictly below the generic ceiling: no contradiction
# index-local (firewall) case: ceiling exponent 1 (n + O(log a)), threshold exponent eps*a
for a in range(1, 2000):
    crossed = eps*a > 1
    assert crossed == (a > F(5*k, 6)); checked += 1
print("OK", checked, "cases; first crossing a =", int(F(5*k,6))+1)
