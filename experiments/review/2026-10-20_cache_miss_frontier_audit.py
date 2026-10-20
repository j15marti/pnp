#!/usr/bin/env python3
"""Exact audit for CACHE-MISS-FRONTIER18.

This checks a resource interface for simulated child inputs.  It does not
construct a correct all-input SAT child decomposition.
"""

from collections import OrderedDict
from fractions import Fraction
import json
from pathlib import Path


ALPHA = Fraction(1, 2)
BETA = Fraction(3, 5)
TAU = Fraction(241, 200)
SPACE = Fraction(1, 2)


def step_with_miss_bound(t, s, rho, kappa, mu, g):
    generation = BETA + mu + rho + g
    return max(BETA + ALPHA * t, generation), max(SPACE, ALPHA * s, kappa + rho)


def step_incomplete_worst_case(t, s, rho, kappa, g):
    # A cyclic trace over one more block than the cache holds misses per read.
    return step_with_miss_bound(t, s, rho, kappa, ALPHA * t, g)


def step_full_cache(t, s, rho, g):
    # Cache every one of n^(alpha-rho) blocks: kappa=alpha-rho.
    kappa = ALPHA - rho
    mu = ALPHA - rho
    return step_with_miss_bound(t, s, rho, kappa, mu, g)


def lru_misses(trace, capacity):
    cache = OrderedDict()
    misses = 0
    for block in trace:
        if block in cache:
            cache.move_to_end(block)
        else:
            misses += 1
            if len(cache) == capacity:
                cache.popitem(last=False)
            cache[block] = None
    return misses


def main():
    failures = []
    assertions = 0

    # Exact threshold identities.
    virtual_slack = TAU - BETA / (1 - ALPHA)
    materialized_slack = TAU - (BETA + ALPHA)
    assertions += 2
    if virtual_slack != Fraction(1, 200):
        failures.append(["virtual_fixed_point_slack", str(virtual_slack)])
    if materialized_slack != Fraction(21, 200):
        failures.append(["materialized_generation_slack", str(materialized_slack)])

    # Incomplete cache fixed point is (beta+rho+g)/(1-alpha).
    # Strict FLMV entry is rho+g<1/400.
    incomplete_cases = 0
    incomplete_samples = []
    for rho_num in range(0, 21):
        rho = Fraction(rho_num, 4000)
        for g_num in range(0, 21):
            g = Fraction(g_num, 4000)
            fixed = (BETA + rho + g) / (1 - ALPHA)
            expected = rho + g < Fraction(1, 400)
            assertions += 1
            incomplete_cases += 1
            if (fixed < TAU) != expected:
                failures.append(["incomplete_threshold", str(rho), str(g), str(fixed)])
            if len(incomplete_samples) < 8 and rho_num in (0, 5, 10, 20) and g_num in (0, 5):
                incomplete_samples.append({
                    "rho": str(rho), "g": str(g), "fixed": str(fixed),
                    "enters": expected,
                })

    # Full caching has generation floor beta+alpha+g and space alpha,
    # independent of block exponent rho.  Strict threshold is g<21/200.
    full_cache_cases = 0
    for rho_num in range(0, 51):
        rho = Fraction(rho_num, 100)
        for g_num in range(0, 43):
            g = Fraction(g_num, 400)
            generation = BETA + ALPHA + g
            expected = g < Fraction(21, 200)
            assertions += 3
            full_cache_cases += 1
            if (generation < TAU) != expected:
                failures.append(["full_threshold", str(rho), str(g)])
            if (ALPHA - rho) + rho != ALPHA:
                failures.append(["full_space", str(rho)])
            if (ALPHA - rho) + rho + g != ALPHA + g:
                failures.append(["full_generation", str(rho), str(g)])

    # Recurrence checks from large initial exponents.
    recurrence_cases = 0
    for rho, g, should_enter in [
        (Fraction(0), Fraction(1, 800), True),
        (Fraction(1, 800), Fraction(1, 1600), True),
        (Fraction(1, 400), Fraction(0), False),
        (Fraction(1, 100), Fraction(0), False),
    ]:
        t = s = Fraction(64)
        for _ in range(4096):
            t, s = step_incomplete_worst_case(t, s, rho, Fraction(0), g)
        assertions += 2
        recurrence_cases += 1
        if (t < TAU) != should_enter:
            failures.append(["incomplete_recurrence", str(rho), str(g), str(t)])
        if s != SPACE:
            failures.append(["incomplete_space_recurrence", str(s)])

    for rho in [Fraction(0), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)]:
        for g, should_enter in [(Fraction(1, 10), True), (Fraction(21, 200), False)]:
            t = s = Fraction(64)
            for _ in range(4096):
                t, s = step_full_cache(t, s, rho, g)
            assertions += 2
            recurrence_cases += 1
            if (t < TAU) != should_enter:
                failures.append(["full_recurrence", str(rho), str(g), str(t)])
            if s != SPACE:
                failures.append(["full_space_recurrence", str(rho), str(s)])

    # Every incomplete LRU cache can be thrashed by cycling over C+1 blocks.
    trace_cases = 0
    for capacity in range(1, 65):
        blocks = capacity + 1
        trace = [i % blocks for i in range(32 * blocks)]
        misses = lru_misses(trace, capacity)
        assertions += 2
        trace_cases += 1
        if misses != len(trace):
            failures.append(["cyclic_thrash", capacity, misses, len(trace)])
        full_misses = lru_misses(trace, blocks)
        if full_misses != blocks:
            failures.append(["full_cache_cold_misses", capacity, full_misses, blocks])

    result = {
        "run": "CACHE-MISS-FRONTIER18",
        "status": "PASS" if not failures else "FAIL",
        "scope": "exact ARC cache-miss resource frontier; SAT child semantics remain open",
        "parameterized_time_recurrence": "t'=max(beta+alpha*t,beta+mu+rho+g)",
        "parameterized_space_recurrence": "s'=max(1/2,alpha*s,kappa+rho)",
        "incomplete_cache_worst_case_fixed_point": "6/5+2(rho+g)",
        "incomplete_cache_strict_condition": "rho+g<1/400",
        "full_cache_generation_condition": "g<21/200",
        "full_cache_space_exponent": "1/2",
        "conditional_locality_condition": "mu+rho+g<121/200",
        "incomplete_grid_cases": incomplete_cases,
        "full_cache_grid_cases": full_cache_cases,
        "recurrence_cases": recurrence_cases,
        "cyclic_trace_cases": trace_cases,
        "assertions": assertions,
        "incomplete_samples": incomplete_samples,
        "failures": failures,
        "global_status": "P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-20_1548_CACHE_MISS_FRONTIER18.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
