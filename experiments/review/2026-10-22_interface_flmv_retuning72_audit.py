#!/usr/bin/env python3
"""Exact and finite audit for INTERFACE-FLMV-RETUNING72."""

from fractions import Fraction
import random


def d(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def boundary(beta: float) -> float:
    lo, hi = 1.0, 1.6
    for _ in range(180):
        mid = (lo + hi) / 2
        value = ((mid + 2) / (mid * mid) - mid) / 2
        if value > beta:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def step(c, s, alpha, beta, eta, sigma):
    time_overhead = max(1 + sigma, alpha + eta)
    return max(time_overhead, alpha + beta * c), max(beta, beta * s)


def main():
    beta = Fraction(101, 200)
    sigma = Fraction(1, 10)
    alpha = 1 - beta + sigma
    c_safe = Fraction(12021, 10000)
    eta_safe = Fraction(6071, 10000)
    block_safe = Fraction(3929, 10000)
    rho_safe = Fraction(2021, 10000)
    fixed = alpha / (1 - beta)

    assert alpha == Fraction(119, 200)
    assert alpha + beta == Fraction(11, 10)
    assert fixed == Fraction(119, 99)
    assert c_safe - fixed == Fraction(79, 990000)
    assert d(c_safe) == Fraction(1465012114739, 2890088820000)
    assert d(c_safe) - beta == Fraction(5517260639, 2890088820000)
    assert alpha + eta_safe == c_safe
    assert 1 + alpha - block_safe == c_safe
    assert 1 + rho_safe == c_safe
    assert d(c_safe) > beta

    root_half = boundary(0.5)
    root_retuned = boundary(float(beta))
    assert abs(root_half - 1.2055694304005904) < 1e-14
    assert root_retuned > float(c_safe)

    # Largest beta (numerically) retaining sigma=0.1 on the strict interface frontier.
    lo, hi = 0.5, 0.52
    for _ in range(180):
        mid = (lo + hi) / 2
        frontier = (boundary(mid) - 1) * (1 - mid)
        if frontier > 0.1:
            lo = mid
        else:
            hi = mid
    beta_cap = (lo + hi) / 2
    assert abs(beta_cap - 0.5061384798932702) < 1e-14

    checks = 15
    rng = random.Random(72)
    for _ in range(100_000):
        c = Fraction(rng.randrange(1203, 40001), 1000)
        s = Fraction(rng.randrange(506, 40001), 1000)
        prev_distance = c - fixed if c > fixed else Fraction(0)
        for _depth in range(40):
            c2, s2 = step(c, s, alpha, beta, eta_safe, sigma)
            assert c2 == max(c_safe, alpha + beta * c)
            assert s2 == max(beta, beta * s)
            if c > fixed and alpha + beta * c >= c_safe:
                assert c2 - fixed == beta * (c - fixed)
            c, s = c2, s2
            checks += 3
        assert c <= c_safe + Fraction(1, 10**6)
        assert s == beta
        checks += 2

    print({
        "checks": checks,
        "failures": 0,
        "beta": str(beta),
        "sigma": str(sigma),
        "alpha": str(alpha),
        "time_fixed_point": str(fixed),
        "c_safe": str(c_safe),
        "flmv_space_margin": str(d(c_safe) - beta),
        "eta_safe": str(eta_safe),
        "block_safe": str(block_safe),
        "rho_safe": str(rho_safe),
        "numeric_beta_cap_for_sigma_point_1": beta_cap,
        "numeric_boundary_at_beta": root_retuned,
    })


if __name__ == "__main__":
    main()
