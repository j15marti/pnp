#!/usr/bin/env python3
"""Bounded controls for the ARC-STRENGTHEN3 zero-child degeneracy."""

from __future__ import annotations

import itertools
import json
import signal
import time
from fractions import Fraction as F
from pathlib import Path


def sat(formula: tuple[tuple[int, ...], ...], nvars: int) -> bool:
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)
               for clause in formula):
            return True
    return False


def zero_child_phase(formula: tuple[tuple[int, ...], ...], nvars: int):
    """Run the exact local decider and issue no queries."""
    return sat(formula, nvars), ()


def dummy_child_phase(formula: tuple[tuple[int, ...], ...], nvars: int):
    """Issue a constant tautology, ignore it, and run the same local decider."""
    child = ((1, -1),)
    child_answer = sat(child, 1)
    assert child_answer
    return sat(formula, nvars), (child,)


def main() -> None:
    signal.alarm(25)
    started = time.perf_counter()
    checks = 0

    h, eta, r, p = F(1, 2), F(3, 5), F(6, 5), F(1, 2)
    C = max(r, eta / (1 - h))
    P = max(p, h)
    assert (C, P) == (r, p) == (F(6, 5), F(1, 2))
    checks += 1

    # All 256 subsets of the eight full clauses on three variables.
    full_clauses = []
    for signs in itertools.product((-1, 1), repeat=3):
        full_clauses.append(tuple(signs[i] * (i + 1) for i in range(3)))
    for mask in range(1 << len(full_clauses)):
        formula = tuple(full_clauses[i] for i in range(8) if mask & (1 << i))
        expected = sat(formula, 3)
        answer0, children0 = zero_child_phase(formula, 3)
        answer1, children1 = dummy_child_phase(formula, 3)
        assert answer0 == expected and children0 == ()
        assert answer1 == expected and len(children1) == 1
        checks += 2

    # General parameter controls: whenever the local floors dominate the
    # recursive fixed point, the zero-child witness has exactly the endpoint
    # exponents.  This is arithmetic only, not a SAT upper bound.
    dominating = 0
    for hi in range(1, 10):
        hh = F(hi, 10)
        for ei in range(0, 11):
            ee = F(ei, 10)
            for ri in range(1, 21):
                rr = F(ri, 10)
                if rr >= ee / (1 - hh):
                    assert max(rr, ee / (1 - hh)) == rr
                    dominating += 1
                    checks += 1

    result = {
        "status": "PASS",
        "checks": checks,
        "runtime_seconds": time.perf_counter() - started,
        "finite_formulas": 256,
        "zero_child_semantic_checks": 256,
        "positive_dummy_child_checks": 256,
        "dominating_parameter_rows": dominating,
        "target": {
            "h": str(h), "eta": str(eta), "r": str(r), "p": str(p),
            "composed_time": str(C), "composed_space": str(P),
        },
        "conclusion": (
            "Finite controls witness the q=0 and ignored-q=1 degeneracies; "
            "the existential equivalence is established symbolically, not by testing."
        ),
    }
    out = Path(__file__).with_name(
        "2026-10-08_2220_REDTEAM-STRENGTHEN3-results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
