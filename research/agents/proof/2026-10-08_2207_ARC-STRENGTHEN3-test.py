#!/usr/bin/env python3
"""Exact arithmetic audit for ARC-STRENGTHEN3's relaxed phase contract."""

from __future__ import annotations

import json
import signal
import time
from fractions import Fraction as F
from pathlib import Path


def fixed_point(r: F, eta: F, h: F) -> F:
    assert F(0) <= h < F(1)
    return max(r, eta / (1 - h))


def iterate(seed: F, r: F, eta: F, h: F, rounds: int = 512) -> F:
    value = seed
    for _ in range(rounds):
        value = max(r, eta + h * value)
    return value


def d(c: F) -> F:
    return F(1, 2) * ((c + 2) / (c * c) - c)


def main() -> None:
    signal.alarm(25)
    started = time.monotonic()
    checks = 0

    h, eta, r, p = F(1, 2), F(3, 5), F(6, 5), F(1, 2)
    c = F(1201, 1000)
    C = fixed_point(r, eta, h)
    S = max(p, h)
    volume = eta + h
    assert (C, S, volume) == (F(6, 5), F(1, 2), F(11, 10)); checks += 1
    assert c > C and d(c) > S; checks += 1
    assert d(c) == F(1468676399, 2884802000); checks += 1
    assert d(c) - S == F(26275399, 2884802000); checks += 1

    # Exact fixed-point comparisons on a rational grid.  The finite iteration
    # need only be within 10^-20 of the symbolic limit after 512 rounds.
    for hi in range(1, 10):
        hh = F(hi, 10)
        for ei in range(0, 13):
            ee = F(ei, 10)
            for ri in range(0, 16):
                rr = F(ri, 10)
                target = fixed_point(rr, ee, hh)
                got = iterate(F(9), rr, ee, hh)
                assert abs(got - target) < F(1, 10**20)
                checks += 1

    # Conditional K elimination: arbitrary polynomial seed exponents converge
    # to the same fixed point; there is no K in the limiting expression.
    for seed in (F(0), F(6, 5), F(2), F(7), F(100)):
        got = iterate(seed, r, eta, h)
        assert abs(got - C) < F(1, 2**100)
        checks += 1

    # Hostile controls.
    assert eta + h > 1  # aggregate encoded volume is superlinear
    checks += 1
    rejected = False
    try:
        fixed_point(r, F(0), F(1))
    except AssertionError:
        rejected = True
    assert rejected
    checks += 1
    # If an n-bit transient scratch area is omitted from p, the declared
    # half-space bound is false.  The ledger must include peak local space.
    omitted_transient_space = F(1)
    assert max(p, h, omitted_transient_space) == 1
    checks += 1
    # Repeated identical calls count with multiplicity: removing eta would
    # incorrectly report only the local floor rather than the call term.
    assert eta / (1 - h) == r and eta != 0
    checks += 1

    elapsed = time.monotonic() - started
    result = {
        "status": "PASS",
        "checks": checks,
        "runtime_seconds": elapsed,
        "target": {
            "h": str(h), "eta": str(eta), "r": str(r), "p": str(p),
            "time_C": str(C), "space_S": str(S),
            "aggregate_volume_exponent": str(volume),
        },
        "flmv": {
            "c": str(c), "d_c": str(d(c)),
            "space_margin": str(d(c) - S),
        },
        "scope": "arithmetic recurrence audit; not evidence of a SAT phase",
    }
    out = Path(__file__).with_name("2026-10-08_2207_ARC-STRENGTHEN3-results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
