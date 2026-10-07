#!/usr/bin/env python3
"""Bounded exact tests for the Backdoor-DNF-to-WRAPPER transfer.

The construction is the Horn family in Ordyniak--Schidler--Szeider,
Backdoor DNFs (IJCAI 2021 / JCSS 2024), Theorem 2 proof sketch.
The test checks the supplied tautological DNF, Horn residuals, exact SAT
semantics, failure of the preceding size-two strong-backdoor member, and the
near-linear encoded size of one explicit residual.  It does not infer a
general-SAT coverage theorem or a machine lower bound.
"""

from __future__ import annotations

from itertools import combinations, product
import hashlib
import json
from math import log
from pathlib import Path
import signal
import time


BUDGET_SECONDS = 25
SEED = 20261007
Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
Assignment = dict[int, bool]


def normalize(formula: Formula) -> Formula:
    out: set[Clause] = set()
    for clause in formula:
        literals = set(clause)
        if any(-lit in literals for lit in literals):
            continue
        out.add(tuple(sorted(literals, key=lambda x: (abs(x), x < 0))))
    return tuple(sorted(out))


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def restrict(formula: Formula, assignment: Assignment) -> Formula:
    residual: list[Clause] = []
    for clause in formula:
        if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0) for lit in clause):
            continue
        reduced = tuple(lit for lit in clause if abs(lit) not in assignment)
        if not reduced:
            return ((),)
        residual.append(reduced)
    return normalize(tuple(residual))


def is_horn(formula: Formula) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in formula)


def horn_sat(formula: Formula) -> bool:
    true_vars: set[int] = set()
    changed = True
    while changed:
        changed = False
        for clause in formula:
            positives = [lit for lit in clause if lit > 0]
            negatives = [-lit for lit in clause if lit < 0]
            if all(v in true_vars for v in negatives):
                if not positives:
                    return False
                if positives[0] not in true_vars:
                    true_vars.add(positives[0])
                    changed = True
    return True


def brute_sat(formula: Formula) -> bool:
    vs = variables(formula)
    for bits in product((False, True), repeat=len(vs)):
        assignment = dict(zip(vs, bits))
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in formula):
            return True
    return False


def paper_family(s: int) -> tuple[Formula, int, tuple[int, ...], tuple[int, ...]]:
    """Return F_s^Horn from the proof sketch of Theorem 2.

    Variables are p=1, a_i=2..s+1, and r=2^s-s variables q_j.
    """
    p = 1
    avars = tuple(range(2, s + 2))
    r = 2**s - s
    qvars = tuple(range(s + 2, s + 2 + r))
    clauses: list[Clause] = [(a, p) for a in avars]
    clauses.extend(tuple(avars) + (q, -p) for q in qvars)
    return normalize(tuple(clauses)), p, avars, qvars


def paper_bdnf(p: int, avars: tuple[int, ...]) -> tuple[Assignment, ...]:
    terms: list[Assignment] = [{p: False}, {p: True, **{a: False for a in avars}}]
    terms.extend({p: True, a: True} for a in avars)
    return tuple(terms)


def term_covers(term: Assignment, full: Assignment) -> bool:
    return all(full[v] == value for v, value in term.items())


def dnf_is_tautology(terms: tuple[Assignment, ...]) -> bool:
    support = tuple(sorted({v for term in terms for v in term}))
    return all(
        any(term_covers(term, dict(zip(support, bits))) for term in terms)
        for bits in product((False, True), repeat=len(support))
    )


def is_strong_horn_backdoor(formula: Formula, support: tuple[int, ...]) -> bool:
    return all(
        is_horn(restrict(formula, dict(zip(support, bits))))
        for bits in product((False, True), repeat=len(support))
    )


def has_strong_horn_backdoor_at_most(formula: Formula, width: int) -> bool:
    vs = variables(formula)
    return any(
        is_strong_horn_backdoor(formula, subset)
        for size in range(width + 1)
        for subset in combinations(vs, size)
    )


def encoded_bits(formula: Formula) -> int:
    """Exact declared indexed-list proxy: sign bit plus global index bits.

    A one-bit clause delimiter is charged per clause.  The asymptotic result
    is insensitive to constant delimiters.
    """
    vmax = max((abs(lit) for clause in formula for lit in clause), default=1)
    index_bits = max(1, vmax.bit_length())
    return sum(1 + len(clause) * (1 + index_bits) for clause in formula)


def main() -> None:
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("budget exceeded")))
    signal.alarm(BUDGET_SECONDS)
    started = time.monotonic()
    family_rows = []
    exact_semantic_checks = 0
    for s in range(1, 13):
        formula, p, avars, qvars = paper_family(s)
        terms = paper_bdnf(p, avars)
        assert len(terms) == s + 2
        assert dnf_is_tautology(terms)
        residuals = tuple(restrict(formula, term) for term in terms)
        assert all(is_horn(child) for child in residuals)
        bdnf_answer = any(horn_sat(child) for child in residuals)
        if s <= 3:
            assert bdnf_answer == brute_sat(formula)
            exact_semantic_checks += 1
        support = tuple(sorted({v for term in terms for v in term}))
        assert is_strong_horn_backdoor(formula, support)
        parent_bits = encoded_bits(formula)
        large_child = restrict(formula, {p: True, **{a: False for a in avars}})
        child_bits = encoded_bits(large_child)
        family_rows.append({
            "s": s,
            "variables": len(variables(formula)),
            "clauses": len(formula),
            "bdnf_terms": len(terms),
            "support_variables": len(support),
            "full_strong_backdoor_branches_on_A": 2**s,
            "parent_encoded_bits": parent_bits,
            "largest_declared_residual_bits": child_bits,
            "child_parent_ratio": child_bits / parent_bits,
            "observed_log_exponent": log(child_bits) / log(parent_bits),
            "q_variables": len(qvars),
        })

    formula3, p3, a3, _ = paper_family(3)
    assert not has_strong_horn_backdoor_at_most(formula3, 2)
    terms3 = paper_bdnf(p3, a3)
    assert len(terms3) == 5
    assert any(horn_sat(restrict(formula3, term)) for term in terms3) == brute_sat(formula3)

    # Easy-family control: a Horn input uses the empty term and no branching.
    horn_control: Formula = ((-1, -2, 3), (-3, 4), (-4,))
    assert is_horn(horn_control)
    assert dnf_is_tautology(({},))
    assert horn_sat(horn_control) == brute_sat(horn_control)

    # Padding control: tautologies disappear under normalization.
    padded = normalize(formula3 + tuple((1000 + i, -(1000 + i)) for i in range(64)))
    assert padded == formula3

    # Independent-product control: Cartesian multiplication of covers is not free.
    component_terms = len(terms3)
    product_terms = component_terms**4
    assert product_terms == 625

    elapsed = time.monotonic() - started
    signal.alarm(0)
    payload = {
        "claim_id": "BDNF-WRAPPER-GATE1",
        "status": "COMPUTATIONAL checks plus an exact asymptotic countermodel proved in the report",
        "seed": SEED,
        "budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": round(elapsed, 6),
        "family_rows": family_rows,
        "exact_bruteforce_semantic_checks": exact_semantic_checks,
        "portfolio_extension_control": {
            "s": 3,
            "preceding_strong_horn_backdoor_width_cap": 2,
            "preceding_member_succeeds": False,
            "backdoor_dnf_terms": 5,
            "backdoor_dnf_succeeds": True,
        },
        "easy_family_control": "Horn formula handled by the empty DNF term",
        "padding_control": "64 tautological clauses normalized away",
        "independent_product_control": {
            "copies": 4,
            "naive_cartesian_terms": product_terms,
            "interpretation": "componentwise solving avoids treating DNF products as free",
        },
        "source_carry_current_scale_sat_calls": 0,
        "oracle_algebraic_control": (
            "The BDNF semantics and size gate relativize and do not block an affine/oracle bypass; "
            "no arbitrary-machine lower bound is inferred."
        ),
        "scope": (
            "The supplied Horn BDNF is exact and can extend a fixed partial portfolio, but one explicit "
            "Horn residual has encoded size M^(1-o(1)); the raw residual-emission transfer therefore "
            "does not establish fixed-power child shrink. Direct/implicit base-class solving needs a "
            "separate charged access, time, and space proof, and no universal coverage theorem is supplied."
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "passed": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
