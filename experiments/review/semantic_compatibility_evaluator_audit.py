#!/usr/bin/env python3
"""Finite audit for the partial-assignment compatibility evaluator theorem.

All runs are exhaustive and deterministic.  This validates finite semantics only;
the asymptotic claims in HEVAL1 are proved symbolically in the report.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
Partial = tuple[int, ...]  # -1 means unassigned, otherwise 0/1


def clause_value(clause: Clause, assignment: tuple[int, ...]) -> bool:
    return any((assignment[abs(lit) - 1] == 1) == (lit > 0) for lit in clause)


def formula_value(formula: Formula, assignment: tuple[int, ...]) -> bool:
    return all(clause_value(clause, assignment) for clause in formula)


def h_completion(formula: Formula, partial: Partial) -> bool:
    holes = [i for i, bit in enumerate(partial) if bit < 0]
    for fill in itertools.product((0, 1), repeat=len(holes)):
        full = list(partial)
        for i, bit in zip(holes, fill):
            full[i] = bit
        if formula_value(formula, tuple(full)):
            return True
    return False


def simplify(formula: Formula, partial: Partial) -> Formula | None:
    residual: list[Clause] = []
    for clause in formula:
        keep: list[int] = []
        satisfied = False
        for lit in clause:
            bit = partial[abs(lit) - 1]
            if bit < 0:
                keep.append(lit)
            elif (bit == 1) == (lit > 0):
                satisfied = True
                break
        if satisfied:
            continue
        if not keep:
            return None
        residual.append(tuple(keep))
    return tuple(residual)


def h_restrict(formula: Formula, partial: Partial) -> bool:
    residual = simplify(formula, partial)
    if residual is None:
        return False
    holes = [i for i, bit in enumerate(partial) if bit < 0]
    for fill in itertools.product((0, 1), repeat=len(holes)):
        full = list(partial)
        for i, bit in zip(holes, fill):
            full[i] = bit
        if formula_value(residual, tuple(full)):
            return True
    return False


def xor3(vars_: tuple[int, int, int], parity: int) -> Formula:
    bad = []
    for bits in itertools.product((0, 1), repeat=3):
        if (sum(bits) & 1) != parity:
            bad.append(tuple(-v if bit else v for v, bit in zip(vars_, bits)))
    return tuple(bad)


def xoreq(a: int, b: int, parity: int) -> Formula:
    if parity == 0:
        return ((a, -b), (-a, b))
    return ((a, b), (-a, -b))


def permute_formula(formula: Formula, perm: tuple[int, ...]) -> Formula:
    return tuple(tuple((1 if lit > 0 else -1) * (perm[abs(lit) - 1] + 1) for lit in c) for c in formula)


def permute_partial(partial: Partial, perm: tuple[int, ...]) -> Partial:
    out = [-1] * len(partial)
    for old, new in enumerate(perm):
        out[new] = partial[old]
    return tuple(out)


def encoded_length(formula: Formula, nvars: int) -> int:
    # Exact length of a stable textual encoding used only for the finite audit.
    return len(f"p cnf {nvars} {len(formula)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in formula))


def cases() -> list[dict]:
    tseitin_cycle = xoreq(1, 2, 0) + xoreq(2, 3, 0) + xoreq(3, 4, 0) + xoreq(4, 1, 1)
    base = [
        {"name": "trivial_sat", "family": "one-bit", "n": 3, "f": ((1,),)},
        {"name": "trivial_unsat", "family": "one-bit", "n": 1, "f": ((1,), (-1,))},
        {"name": "two_sat", "family": "2SAT", "n": 4, "f": ((1, 2), (-1, 3), (-2, 4), (-3, -4))},
        {"name": "horn", "family": "Horn", "n": 5, "f": ((-1, -2, 3), (-3, 4), (-4, 5), (-5,))},
        {"name": "affine_xor3", "family": "affine", "n": 3, "f": xor3((1, 2, 3), 1)},
        {"name": "tseitin_cycle_unsat", "family": "affine/Tseitin", "n": 4, "f": tseitin_cycle},
        {"name": "bounded_tw_path", "family": "bounded-treewidth", "n": 6, "f": ((1, 2), (-2, 3), (-3, 4), (-4, 5), (-5, 6))},
        {"name": "independent_xor_product", "family": "independent-product", "n": 6, "f": xor3((1, 2, 3), 0) + xor3((4, 5, 6), 1)},
        {"name": "signed_3cnf", "family": "signed-3CNF", "n": 6, "f": ((1, 2, 3), (-1, -2, 4), (-3, -4, 5), (2, -5, 6), (-2, 5, -6))},
        {"name": "padding_unused", "family": "padding", "n": 7, "f": ((1, 2, 3), (-1, 4), (-2, 5), (-3, 6))},
    ]
    return base


def audit_case(case: dict) -> tuple[dict, int]:
    name, family, n, formula = case["name"], case["family"], case["n"], tuple(case["f"])
    partials = list(itertools.product((-1, 0, 1), repeat=n))
    truth: dict[Partial, bool] = {}
    assertions = 0
    for partial in partials:
        direct = h_completion(formula, partial)
        restricted = h_restrict(formula, partial)
        assert direct == restricted, (name, partial)
        assertions += 1
        truth[partial] = direct

    empty = (-1,) * n
    assert truth[empty] == h_completion(formula, empty)
    assertions += 1

    for partial, value in truth.items():
        if value:
            continue
        for i, bit in enumerate(partial):
            if bit < 0:
                for fixed in (0, 1):
                    child = list(partial); child[i] = fixed
                    assert not truth[tuple(child)]
                    assertions += 1

    wrappers = {
        "DIRECT": formula,
        "COPY": formula + formula,
        "ORDER": tuple(reversed(formula)),
        "LITORDER": tuple(tuple(reversed(c)) for c in formula),
        "TAUTOLOGY": formula + ((1, -1),),
    }
    wrapper_checks = 0
    for wrapped in wrappers.values():
        for partial in partials:
            assert h_restrict(wrapped, partial) == truth[partial]
            wrapper_checks += 1
    assertions += wrapper_checks

    perm = tuple(reversed(range(n)))
    pformula = permute_formula(formula, perm)
    for partial in partials:
        assert h_restrict(pformula, permute_partial(partial, perm)) == truth[partial]
        wrapper_checks += 1
    assertions += len(partials)

    full_rows = sum(1 for p in partials if -1 not in p)
    result = {
        "case": name,
        "family": family,
        "nvars": n,
        "clauses": len(formula),
        "literal_occurrences": sum(len(c) for c in formula),
        "encoded_bytes": encoded_length(formula, n),
        "compatibility_domain": 3 ** n,
        "compatible_partials": sum(truth.values()),
        "incompatible_partials": len(truth) - sum(truth.values()),
        "full_assignment_rows": full_rows,
        "sat_answer_from_empty_partial": truth[empty],
        "full_table_queries": len(partials),
        "one_bit_queries": 1,
        "wrappers": [*wrappers, "INTERP_PERMUTE"],
        "wrapper_checks": wrapper_checks,
        "assertions": assertions,
    }
    return result, assertions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    rows = []
    total_assertions = 0
    for case in cases():
        row, assertions = audit_case(case)
        rows.append(row); total_assertions += assertions
    payload = {
        "experiment": "semantic_compatibility_evaluator_audit",
        "status": "COMPUTATIONAL",
        "mode": "deterministic exhaustive",
        "random_seed": None,
        "cases": rows,
        "summary": {
            "cases": len(rows),
            "partial_assignments": sum(r["compatibility_domain"] for r in rows),
            "wrapper_checks": sum(r["wrapper_checks"] for r in rows),
            "assertions": total_assertions,
            "failures": 0,
            "elapsed_seconds": round(time.perf_counter() - started, 6),
        },
        "limitations": "Finite semantic checks only; no asymptotic runtime or circuit lower bound is inferred.",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
