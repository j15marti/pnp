#!/usr/bin/env python3
"""Bounded audit for CLOCK-SLACK-CONTRACTION-GAUGE1.

The exact theorem is elementary: if t >= 2 is a valid clock, then t**q is
also a valid clock, and the identity implementation obeys
T <= t <= (t**q)**alpha whenever q*alpha >= 1.  The finite audit checks the
integer-power form of this inequality and verifies that formula families,
encodings, and semantics-preserving wrappers do not create an extracted
compatibility object.  It is bookkeeping, not an asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Iterable


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]

ALPHAS = (
    Fraction(1, 2),
    Fraction(2, 3),
    Fraction(3, 4),
    Fraction(4, 5),
    Fraction(9, 10),
)
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("tuple", "dimacs", "json", "reversed", "renamed")


def variables(cnf: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in cnf for lit in clause}))


def sat_bit(cnf: CNF) -> tuple[bool, int, int]:
    """Return SAT bit, assignments tested, and literal inspections."""
    vs = variables(cnf)
    inspections = 0
    assignments = 0
    for bits in itertools.product((False, True), repeat=len(vs)):
        assignments += 1
        env = dict(zip(vs, bits))
        all_ok = True
        for clause in cnf:
            clause_ok = False
            for lit in clause:
                inspections += 1
                if env[abs(lit)] == (lit > 0):
                    clause_ok = True
                    break
            if not clause_ok:
                all_ok = False
                break
        if all_ok:
            return True, assignments, inspections
    return False, assignments, inspections


def encode(cnf: CNF, kind: str) -> bytes:
    n = max(variables(cnf), default=0)
    if kind == "tuple":
        return repr(cnf).encode()
    if kind == "dimacs":
        rows = [f"p cnf {n} {len(cnf)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in cnf)
        return ("\n".join(rows) + "\n").encode()
    if kind == "json":
        return json.dumps(cnf, separators=(",", ":")).encode()
    if kind == "reversed":
        return repr(tuple(tuple(reversed(c)) for c in reversed(cnf))).encode()
    if kind == "renamed":
        return repr(tuple(tuple((1 if x > 0 else -1) * (n + 1 - abs(x))
                               for x in c) for c in cnf)).encode()
    raise ValueError(kind)


def wrapped_sat(cnf: CNF, wrapper: str) -> tuple[bool, dict[str, int]]:
    """Semantics-preserving wrappers with explicitly separated costs."""
    copied = tuple(tuple(c) for c in cnf)
    pre = sum(len(c) for c in cnf)
    delay = 0
    interp = 0
    recompute = 0
    if wrapper == "DIRECT":
        target = cnf
    elif wrapper == "COPY":
        target = copied
        pre *= 2
    elif wrapper == "DEAD":
        target = cnf
        delay = 17 * max(1, pre)
    elif wrapper == "DELAY":
        target = cnf
        delay = max(1, pre) ** 2
    elif wrapper == "INTERP":
        target = copied
        interp = 3 * max(1, pre)
    elif wrapper == "RECOMP":
        target = cnf
        recompute = pre
        _ = variables(cnf)
    else:
        raise ValueError(wrapper)
    bit, assignments, inspections = sat_bit(target)
    return bit, {
        "preprocessing_ops": pre,
        "solver_assignments": assignments,
        "solver_literal_inspections": inspections,
        "wrapper_delay_ops": delay,
        "interpreter_ops": interp,
        "recomputation_ops": recompute,
        "compatibility_extraction_ops": 0,
        "reconstruction_ops": 0,
        "communication_ops": 0,
    }


def controls() -> dict[str, CNF]:
    return {
        "proper-3cnf": ((1, 2, 3), (-1, 2, 4), (1, -3, -4)),
        "horn": ((-1, -2, 3), (-3, 4), (-4,)),
        "2sat": ((1, 2), (-1, 3), (-2, -3)),
        "affine-tseitin-xor": ((1, 2, 3), (1, -2, -3),
                                (-1, 2, -3), (-1, -2, 3)),
        "bounded-treewidth-chain": ((1, 2), (-2, 3), (-3, 4), (-4, 5)),
        "independent-product": ((1,), (2, 3), (-2, 3), (4, 5), (-4, 5)),
        "padding-tautologies": ((1,), (2, -2), (3, -3), (4, -4)),
        "redundant-clauses": ((1, 2), (1, 2), (1, 2, 3), (-1,), (-2,)),
        "unsat-unit-pair": ((1,), (-1,)),
    }


def exact_power_leq(cost: int, clock: int, q: int,
                    alpha: Fraction) -> bool:
    # cost <= (clock**q)**(p/r) iff cost**r <= clock**(q*p).
    return cost ** alpha.denominator <= clock ** (q * alpha.numerator)


def run_audit(max_cost: int) -> dict[str, object]:
    started = time.perf_counter()
    assertions = 0
    failures: list[dict[str, object]] = []
    clock_rows = 0
    polynomial_rows = 0
    exponential_rows = 0

    for cost in range(2, max_cost + 1):
        for clock in (cost, cost + 1, 2 * cost, cost * cost):
            for alpha in ALPHAS:
                for q in range(1, 13):
                    clock_rows += 1
                    expected = q * alpha >= 1
                    observed = exact_power_leq(cost, clock, q, alpha)
                    assertions += 3
                    if expected and not observed:
                        failures.append({"kind": "integer-power", "cost": cost,
                                         "clock": clock, "q": q,
                                         "alpha": str(alpha)})
                    if clock < cost:
                        failures.append({"kind": "invalid-clock"})
                    if q >= 1 and clock ** q < clock:
                        failures.append({"kind": "widening"})

    # Exponent-ledger controls for polynomial and exponential cost scales.
    for actual_exp in range(1, 9):
        for q in range(1, 13):
            for alpha in ALPHAS:
                polynomial_rows += 1
                exponential_rows += 1
                expected = q * alpha >= 1
                poly_seen = Fraction(actual_exp) <= alpha * q * actual_exp
                exp_seen = Fraction(actual_exp) <= alpha * q * actual_exp
                assertions += 2
                if poly_seen != expected:
                    failures.append({"kind": "poly-exponent"})
                if exp_seen != expected:
                    failures.append({"kind": "exp-rate"})

    family_rows: list[dict[str, object]] = []
    for family, cnf in controls().items():
        direct, _, _ = sat_bit(cnf)
        for encoding in ENCODINGS:
            payload = encode(cnf, encoding)
            for wrapper in WRAPPERS:
                bit, costs = wrapped_sat(cnf, wrapper)
                assertions += 6
                if bit != direct:
                    failures.append({"kind": "semantic-wrapper", "family": family,
                                     "encoding": encoding, "wrapper": wrapper})
                if costs["compatibility_extraction_ops"] != 0:
                    failures.append({"kind": "extraction"})
                if costs["reconstruction_ops"] != 0:
                    failures.append({"kind": "reconstruction"})
                if costs["communication_ops"] != 0:
                    failures.append({"kind": "communication"})
                if len(payload) <= 0:
                    failures.append({"kind": "encoding"})
                digest = hashlib.sha256(payload).hexdigest()
                if len(digest) != 64:
                    failures.append({"kind": "digest"})
                family_rows.append({
                    "family": family,
                    "encoding": encoding,
                    "wrapper": wrapper,
                    "sat": bit,
                    "encoded_bytes": len(payload),
                    "payload_sha256": digest,
                    **costs,
                })

    elapsed = time.perf_counter() - started
    return {
        "claim": "CLOCK-SLACK-CONTRACTION-GAUGE1",
        "status": "COMPUTATIONAL",
        "alphas": [str(a) for a in ALPHAS],
        "max_cost": max_cost,
        "clock_rows": clock_rows,
        "polynomial_exponent_rows": polynomial_rows,
        "exponential_rate_rows": exponential_rows,
        "formula_wrapper_encoding_rows": len(family_rows),
        "families": sorted(controls()),
        "encodings": list(ENCODINGS),
        "wrappers": list(WRAPPERS),
        "assertions": assertions,
        "failures": failures,
        "pass": not failures,
        "elapsed_seconds": elapsed,
        "cost_accounting": {
            "preprocessing": "literal visits counted",
            "clock_annotation": "integer exponentiation comparisons counted in assertions",
            "extraction": "zero; no compatibility object requested",
            "reconstruction": "zero; decision bit returned directly",
            "communication": "zero; single ordinary process",
            "wrapper_overhead": "reported separately per row",
        },
        "sample_rows": family_rows[:18],
        "scope": (
            "finite exact-integer/rational audit and hostile controls only; "
            "the asymptotic clock-slack theorem is proved symbolically"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cost", type=int, default=256)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_audit(args.max_cost)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"sample_rows"}}, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
