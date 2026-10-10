#!/usr/bin/env python3
"""Finite hostile controls for the MODEL_BRIDGE terminal-token theorem.

The program checks only finite semantics.  Resource conclusions in the report
are symbolic consequences of the declared machine composition, not empirical
lower bounds.
"""

from __future__ import annotations

import argparse
import itertools
import json
import signal
import time
from pathlib import Path

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]

YES_TOKEN: CNF = ((1,),)
NO_TOKEN: CNF = ((),)


def variables(formula: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def eval_formula(formula: CNF, assignment: dict[int, bool]) -> bool:
    return all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
               for clause in formula)


def exact_sat(formula: CNF) -> tuple[bool, tuple[int, ...] | None]:
    vs = variables(formula)
    for bits in itertools.product((0, 1), repeat=len(vs)):
        assignment = {v: bool(bit) for v, bit in zip(vs, bits)}
        if eval_formula(formula, assignment):
            return True, bits
    return False, None


def terminal_token(formula: CNF) -> CNF:
    value, _ = exact_sat(formula)
    return YES_TOKEN if value else NO_TOKEN


def sat_witness_or_source(formula: CNF) -> tuple[str, object]:
    value, witness = exact_sat(formula)
    if value:
        return ("VALUE", witness)
    return ("SOURCE_CARRY", formula)


def candidate_clauses(n: int) -> list[Clause]:
    literals = [lit for v in range(1, n + 1) for lit in (v, -v)]
    out: list[Clause] = [(lit,) for lit in literals]
    for a, b in itertools.combinations(literals, 2):
        if a != -b:
            out.append(tuple(sorted((a, b), key=lambda z: (abs(z), z < 0))))
    return out


def formulas(n: int, max_clauses: int) -> list[CNF]:
    clauses = candidate_clauses(n)
    out: list[CNF] = [tuple()]
    for width in range(1, max_clauses + 1):
        out.extend(tuple(choice) for choice in itertools.combinations(clauses, width))
    return out


def rename(formula: CNF, offset: int) -> CNF:
    return tuple(tuple((abs(lit) + offset) * (1 if lit > 0 else -1)
                       for lit in clause) for clause in formula)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variables", type=int, default=4)
    parser.add_argument("--max-clauses", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    signal.alarm(25)
    started = time.time()
    fs = formulas(args.variables, args.max_clauses)
    failures: list[dict[str, object]] = []
    counts = {"sat": 0, "unsat": 0, "source_carry": 0}

    for index, formula in enumerate(fs):
        value, _ = exact_sat(formula)
        counts["sat" if value else "unsat"] += 1
        token = terminal_token(formula)
        token_value, _ = exact_sat(token)
        if token_value != value or token not in (YES_TOKEN, NO_TOKEN):
            failures.append({"kind": "token", "index": index})
        kind, _payload = sat_witness_or_source(formula)
        if kind == "SOURCE_CARRY":
            counts["source_carry"] += 1
            if value:
                failures.append({"kind": "bad_source_carry", "index": index})

    # Padding control: tautological clauses change representation length but not
    # the fixed semantic token.  The test intentionally permits tautologies.
    padding_checks = 0
    for formula in fs[::max(1, len(fs) // 97)]:
        base = terminal_token(formula)
        for p in (1, 2, 4, 8):
            padded = formula + tuple((100 + j, -(100 + j)) for j in range(p))
            if terminal_token(padded) != base:
                failures.append({"kind": "padding", "padding": p})
            padding_checks += 1

    # Independent-product control: the token for disjoint conjunction is the
    # conjunction of truth values, not evidence of cheap acquisition.
    product_checks = 0
    sample = fs[::max(1, len(fs) // 31)]
    for left, right in zip(sample, reversed(sample)):
        joined = left + rename(right, args.variables + 10)
        lv, _ = exact_sat(left)
        rv, _ = exact_sat(right)
        tv, _ = exact_sat(terminal_token(joined))
        if tv != (lv and rv):
            failures.append({"kind": "product"})
        product_checks += 1

    # Symbolic exponent ledger for a wrapper making N^q calls on N^c inputs to
    # an N^K solver.  At current scale c=1, q+cK retains K.  A fixed terminal
    # token has child exponent zero but still pays its generator exponent K.
    ledger = []
    for k in range(1, 9):
        for q, c in ((0, 1), (1, 1), (0, 0.5), (0, 0)):
            ledger.append({
                "K": k,
                "query_exponent": q,
                "child_scale": c,
                "direct_call_exponent": q + c * k,
                "terminal_token_output_exponent": 0,
                "terminal_token_generation_exponent": k,
            })

    payload = {
        "status": "PASS" if not failures else "FAIL",
        "method": "deterministic exhaustive finite CNF semantics plus symbolic exponent ledger",
        "variables": args.variables,
        "max_clauses": args.max_clauses,
        "formula_count": len(fs),
        "counts": counts,
        "padding_checks": padding_checks,
        "product_checks": product_checks,
        "ledger": ledger,
        "failures": failures,
        "elapsed_seconds": round(time.time() - started, 6),
        "limitation": (
            "Finite semantics and exact arithmetic only; this is not an "
            "asymptotic runtime lower bound or proof-assistant verification."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "formula_count": payload["formula_count"],
        "counts": counts,
        "padding_checks": padding_checks,
        "product_checks": product_checks,
        "elapsed_seconds": payload["elapsed_seconds"],
        "failure_count": len(failures),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
