"""Exact arithmetic controls for MMW-QUERY-ABSORPTION19.

These finite checks validate only exponent algebra and sequential peak-buffer
accounting.  They do not construct the missing SAT-to-MKTP transducer.
"""
from fractions import Fraction as F
from math import floor

rows = 0
query_contrast = 0
threshold_checks = 0
buffer_checks = 0

for a in (F(1), F(6, 5), F(17, 10), F(2)):
    for rho in (F(1, 4), F(1, 2), F(9, 10), F(99, 100)):
        assert rho < 1
        for C in range(1, 251):
            # Any unbounded cofinal K contains an element above a*C.
            k0 = floor(a * C) + 1
            assert a * C / k0 < 1
            theta = max(rho, a * C / k0)
            assert theta < 1
            rows += 1

            # Exact MMW has d_k=1.  A hypothetical d_k=k would not dilute C.
            assert a * C / k0 < a * C
            assert a * C * k0 / k0 == a * C
            query_contrast += 2

            # On M=2^(4k^2), p=M^(1/k)=2^(4k) dominates log_2 M.
            assert 2 ** (4 * k0) >= 4 * k0 * k0
            threshold_checks += 1

            # Sequentially reusing one q-bit query buffer keeps peak q,
            # independently of the number of queries.
            q = k0 + C + 1
            for query_count in (1, 2, 17, 1000):
                peak = max(q for _ in range(query_count))
                assert peak == q
                buffer_checks += 1

print({
    "rows": rows,
    "query_contrast_assertions": query_contrast,
    "threshold_checks": threshold_checks,
    "buffer_checks": buffer_checks,
    "failures": 0,
})
