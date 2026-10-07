#!/usr/bin/env python3
"""Exact arithmetic checks for the polynomial-regime self-improvement audit.

Run: timeout 30s python polynomial_regime_bridge_test.py OUTPUT.json
The analytic claims are proved in main6.tex; this program checks representative
parameter grids and records the arithmetic without treating them as theorems.
"""

from __future__ import annotations

import hashlib
import json
import signal
import sys
import time
from fractions import Fraction
from pathlib import Path


def fs(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    signal.signal(
        signal.SIGALRM,
        lambda *_: (_ for _ in ()).throw(TimeoutError("25-second budget")),
    )
    signal.alarm(25)
    started = time.perf_counter()
    checks = 0

    # Williams Theorem 1.1 with a polynomial N^K algorithm on N=2^(alpha*n)
    # has beta=K*alpha and output exponent beta-alpha=(K-1)*alpha.
    theorem_11_rows = []
    for K in range(2, 9):
        for alpha in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)):
            beta = K * alpha
            output = beta - alpha
            assert output == (K - 1) * alpha
            assert beta >= alpha
            checks += 2
            theorem_11_rows.append(
                {"K": K, "alpha": fs(alpha), "beta": fs(beta), "beta_minus_alpha": fs(output)}
            )

    # The known hybrid min(n^K, 2^k n) does not meet the premise
    # exists c>1 forall epsilon>0: O(c^k+n^(1+epsilon)).  Write c=2^d,
    # choose k/(log_2 n)=x=2epsilon, and choose epsilon small enough that
    # d*x<1.  Then the hybrid exponent is 1+2epsilon while the proposed
    # right side has exponent 1+epsilon.
    hybrid_rows = []
    for K in range(2, 9):
        for d in (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4), Fraction(8), Fraction(16)):
            epsilon = min(Fraction(K - 1, 4), Fraction(1, 8 * max(d, 1)), Fraction(1, 32))
            x = 2 * epsilon
            hybrid = min(Fraction(K), 1 + x)
            claimed_rhs = max(d * x, 1 + epsilon)
            assert 1 + x < K or 1 + x == K
            assert d * x < 1
            assert hybrid > claimed_rhs
            checks += 3
            hybrid_rows.append(
                {
                    "K": K,
                    "log2_c": fs(d),
                    "epsilon": fs(epsilon),
                    "k_over_log2_n": fs(x),
                    "hybrid_size_exponent": fs(hybrid),
                    "target_rhs_exponent": fs(claimed_rhs),
                }
            )

    # A fixed alpha does not give a polynomial bound in the encoded size M
    # throughout the subexponential circuit regime M=2^(r*n), r -> 0.
    density_rows = []
    for K in (2, 3, 5, 8):
        for alpha in (Fraction(1, 4), Fraction(1, 16)):
            previous = None
            for j in (2, 4, 8, 16, 32):
                r = alpha / j
                exponent_in_M = (K - 1) * alpha / r
                assert exponent_in_M == (K - 1) * j
                if previous is not None:
                    assert exponent_in_M > previous
                previous = exponent_in_M
                checks += 2
                density_rows.append(
                    {
                        "K": K,
                        "alpha": fs(alpha),
                        "r_logM_over_inputs": fs(r),
                        "derived_M_exponent": fs(exponent_in_M),
                    }
                )

    # BATCHFRONTIER1 envelope: C=max(2-beta,1+omega),
    # sigma=max(beta,omega).  Its sum is never below 2.
    frontier_rows = []
    grid = [Fraction(i, 16) for i in range(17)]
    minimum = None
    minimizers = []
    for block_exp in grid:
        for table_exp in grid:
            C = max(2 - block_exp, 1 + table_exp)
            sigma = max(block_exp, table_exp)
            total = C + sigma
            assert total >= 2
            checks += 1
            if minimum is None or total < minimum:
                minimum = total
                minimizers = [(block_exp, table_exp)]
            elif total == minimum:
                minimizers.append((block_exp, table_exp))
    frontier_rows = [
        {"block_exponent": fs(b), "table_exponent": fs(w)}
        for b, w in minimizers
    ]

    # Forward-tree ledger.  When leaf length is N^b, an N^K leaf solver
    # contributes q+bK.  At b=0 (meaning N^o(1)), K disappears.
    tree_rows = []
    for K in range(2, 9):
        for q in (Fraction(1), Fraction(3, 2), Fraction(7, 4)):
            for b in (Fraction(0), Fraction(1, 8), Fraction(1, 4)):
                g = Fraction(5, 4)
                time_exp = max(g, q + b * K)
                if b == 0:
                    assert time_exp == max(g, q)
                checks += 1
                tree_rows.append(
                    {"K": K, "q": fs(q), "leaf_exponent": fs(b), "g": fs(g), "time": fs(time_exp)}
                )

    elapsed = time.perf_counter() - started
    result = {
        "status": "COMPUTATIONAL",
        "checks": checks,
        "seconds": elapsed,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "theorem_11_rows": theorem_11_rows,
        "hybrid_gate_rows": hybrid_rows,
        "fixed_alpha_density_rows": density_rows,
        "batchfrontier_minimum_sum": fs(minimum),
        "batchfrontier_minimizers": frontier_rows,
        "forward_tree_rows": tree_rows,
        "limitations": [
            "The asymptotic gates are proved separately; this is a finite exact-arithmetic regression.",
            "No row constructs a general SAT improvement or proves P versus NP.",
            "The Williams transfer uses fixed constants; an input-dependent alpha requires a new uniform theorem.",
        ],
    }
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + "\n")
    print(
        {
            "status": result["status"],
            "checks": checks,
            "seconds": elapsed,
            "batchfrontier_minimum_sum": result["batchfrontier_minimum_sum"],
            "hybrid_witnesses": len(hybrid_rows),
        }
    )


if __name__ == "__main__":
    main()
