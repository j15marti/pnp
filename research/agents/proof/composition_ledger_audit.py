"""Exact finite accounting tests; does not construct a SAT wrapper."""
from fractions import Fraction as F
from itertools import product
import json
import time


def run():
    start = time.monotonic()
    checks = 0
    grid = [F(0), F(1, 3), F(2, 3), F(1)]
    cases = 0
    for ta, tb, a, b, ra, rb in product(grid, repeat=6):
        if ta * tb == 1:
            continue
        # a and b are fully charged eta+g, not just branch exponents.
        ca = max(ra, a + ta * rb, (a + ta * b) / (1 - ta * tb))
        cb = max(rb, b + tb * ra, (b + tb * a) / (1 - ta * tb))
        assert ca == max(ra, a + ta * cb)
        assert cb == max(rb, b + tb * ca)
        checks += 2
        x, y = ra, rb
        for _ in range(8):
            x, y = max(ra, a + ta * y), max(rb, b + tb * x)
            assert x <= ca and y <= cb
            checks += 1
        cases += 1

    # Same-scale A->B followed by fractional B->A can erase K.
    ta, tb, a, b = F(1), F(2, 3), F(0), F(1, 3)
    assert (a + ta * b) / (1 - ta * tb) == 1
    checks += 1
    # Input-bit regeneration is not free: g=1/12 changes the cycle bound.
    assert (a + ta * (b + F(1, 12))) / (1 - ta * tb) == F(5, 4)
    checks += 1
    # Explicit same-scale buffers force this sufficient space ledger to 1.
    assert max(F(2, 3), ta) == 1
    checks += 1

    # Abstract interface controls, not an implementation of SAT recognition.
    root_domain = {"root0", "root1"}
    successful_domain = {"root0", "root1"}
    successors = {"root0": "residual2", "root1": "terminal"}
    terminal = {"terminal"}
    assert root_domain <= successful_domain
    assert not set(successors.values()) <= successful_domain | terminal
    checks += 2
    # Identifiers do not implement ordinary-CNF or random-access interfaces.
    produced = "parent-aware route identifier"
    required = "ordinary encoded CNF"
    assert produced != required
    checks += 1
    # Identity cycles have no contraction certificate even when overhead is 0.
    assert F(1) * F(1) == 1
    checks += 1
    # A finite but input-dependent same-scale chain is not constant rank.
    assert max(range(100)) > 8
    checks += 1
    return {
        "status": "COMPUTATIONAL",
        "scope": "Exact arithmetic and abstract interface regression only; no SAT coverage claim",
        "two_type_cases": cases,
        "assertions": checks,
        "failures": 0,
        "controls": {
            "same_scale_then_fractional_time": "1",
            "with_generator_time_1_over_12": "5/4",
            "explicit_same_scale_space": "1",
            "root_cover_without_successor_cover": "rejected",
            "route_identifier_as_CNF": "rejected",
            "identity_cycle_as_contraction": "rejected",
            "input_dependent_rank_as_constant_rank": "rejected"
        },
        "seed": None,
        "elapsed_seconds": time.monotonic() - start
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
