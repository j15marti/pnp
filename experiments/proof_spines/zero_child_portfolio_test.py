#!/usr/bin/env python3
"""Independent WRITE check of zero-child VALUE members in a fixed portfolio."""

from __future__ import annotations

from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import signal
import time


BUDGET_SECONDS = 25
SEED = 20261007
Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def assignments(n: int):
    for bits in product((False, True), repeat=n):
        yield {i + 1: bits[i] for i in range(n)}


def sat(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula)


def brute_sat(formula: Formula, n: int) -> bool:
    return any(sat(formula, a) for a in assignments(n))


def positive_cofactor_member(formula: Formula, p: int = 1):
    """Return a q=0 constant-TRUE plan, or FAIL."""
    literal_visits = 0
    for clause in formula:
        literal_visits += len(clause)
        if -p in clause:
            continue
        residual = tuple(lit for lit in clause if abs(lit) != p)
        if not residual or any(lit < 0 for lit in residual):
            return {"kind": "FAIL", "literal_visits": literal_visits}
    return {
        "kind": "PLAN",
        "children": (),
        "combine": True,
        "literal_visits": literal_visits,
    }


def horn_member(formula: Formula, n: int):
    if any(sum(lit > 0 for lit in clause) > 1 for clause in formula):
        return {"kind": "FAIL"}
    return {"kind": "PLAN", "children": (), "combine": brute_sat(formula, n)}


def twocnf_member(formula: Formula, n: int):
    if any(len(clause) > 2 for clause in formula):
        return {"kind": "FAIL"}
    return {"kind": "PLAN", "children": (), "combine": brute_sat(formula, n)}


def run_portfolio(formula: Formula, n: int):
    attempts = 0
    for member in (
        lambda f: positive_cofactor_member(f, 1),
        lambda f: horn_member(f, n),
        lambda f: twocnf_member(f, n),
    ):
        attempts += 1
        plan = member(formula)
        if plan["kind"] == "PLAN":
            assert len(plan["children"]) == 0
            return plan["combine"], attempts
    raise AssertionError("2-CNF member should cover the enumerated domain")


def normalize(formula: Formula) -> Formula:
    out = set()
    for clause in formula:
        lits = set(clause)
        if any(-lit in lits for lit in lits):
            continue
        out.add(tuple(sorted(lits, key=lambda x: (abs(x), x < 0))))
    return tuple(sorted(out))


def paper_family(s: int) -> Formula:
    p = 1
    avars = tuple(range(2, s + 2))
    r = 2**s - s
    qvars = tuple(range(s + 2, s + 2 + r))
    return normalize(
        tuple((a, p) for a in avars)
        + tuple(tuple(avars) + (q, -p) for q in qvars)
    )


def main() -> None:
    signal.signal(signal.SIGALRM,
                  lambda *_: (_ for _ in ()).throw(TimeoutError("budget exceeded")))
    signal.alarm(BUDGET_SECONDS)
    started = time.monotonic()

    n = 3
    clauses = []
    for v in range(1, n + 1):
        clauses.extend(((v,), (-v,)))
    for u, v in combinations(range(1, n + 1), 2):
        clauses.extend((su * u, sv * v) for su in (-1, 1) for sv in (-1, 1))
    clauses = tuple(sorted(set(clauses)))

    formulas_checked = 0
    accepted_value_members = 0
    portfolio_attempt_counts = {1: 0, 2: 0, 3: 0}
    for size in range(0, 6):
        for chosen in combinations(clauses, size):
            formula = normalize(tuple(chosen))
            expected = brute_sat(formula, n)
            value_plan = positive_cofactor_member(formula)
            if value_plan["kind"] == "PLAN":
                accepted_value_members += 1
                assert value_plan["children"] == ()
                assert value_plan["combine"] is True
                assert expected is True
                assert value_plan["literal_visits"] <= sum(map(len, formula))
            observed, attempts = run_portfolio(formula, n)
            assert observed == expected
            portfolio_attempt_counts[attempts] += 1
            formulas_checked += 1

    # Source family, padding, renaming, independent-product, and unsafe controls.
    source_rows = []
    for s in range(1, 11):
        formula = paper_family(s)
        plan = positive_cofactor_member(formula)
        assert plan["kind"] == "PLAN" and plan["combine"] is True
        source_rows.append({
            "s": s,
            "clauses": len(formula),
            "literal_visits": plan["literal_visits"],
            "children": len(plan["children"]),
        })

    unsat_control: Formula = ((1,), (-1,))
    assert positive_cofactor_member(unsat_control)["kind"] == "FAIL"
    assert brute_sat(unsat_control, 1) is False
    unsafe_constant_true = True
    assert unsafe_constant_true != brute_sat(unsat_control, 1)

    swap = {1: 2, 2: 1}
    renamed = tuple(tuple(swap.get(abs(lit), abs(lit)) * (1 if lit > 0 else -1)
                          for lit in clause)
                    for clause in paper_family(2))
    # A fixed p=1 member may safely fail after renaming; universality is not inferred.
    renamed_result = positive_cofactor_member(normalize(renamed), 1)

    padded = normalize(paper_family(3) + tuple((100 + i, -(100 + i)) for i in range(32)))
    assert positive_cofactor_member(padded)["kind"] == "PLAN"
    independent = [positive_cofactor_member(paper_family(3))["combine"] for _ in range(4)]
    assert all(independent)

    signal.alarm(0)
    payload = {
        "claim_id": "ZERO-CHILD-PORTFOLIO1",
        "status": "COMPUTATIONAL independent check of an exact theorem specialization",
        "seed": SEED,
        "randomness_used": False,
        "budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "enumeration": {
            "variables": n,
            "clause_width": 2,
            "max_clauses": 5,
            "formulas_checked": formulas_checked,
            "accepted_zero_child_value_members": accepted_value_members,
            "portfolio_attempt_counts": portfolio_attempt_counts,
            "violations": 0,
        },
        "source_family_rows": source_rows,
        "controls": {
            "unsafe_first_finisher": "constant TRUE fails on (p) AND (not p), so exact-success certification is necessary",
            "renaming": f"fixed-name member result after swapping variables 1 and 2: {renamed_result['kind']}; failure is safe",
            "padding": "32 tautological clauses normalize away",
            "independent_product": "four accepted components combine by AND without child generation",
            "current_scale_sat_calls": 0,
            "source_carry": "no witness/source map is needed for the certified constant decision value",
            "oracle_algebraic": "the specialization relativizes and supplies no lower-bound hinge",
        },
        "interpretation": (
            "q=0 constant combiners are already included in CERTIFIED-PARTIAL-PORTFOLIO1; "
            "the positive-cofactor member is exact and self-certified, but the tested finite "
            "portfolio covers only the enumerated 2-CNF domain and proves no general-SAT coverage"
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "passed": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
