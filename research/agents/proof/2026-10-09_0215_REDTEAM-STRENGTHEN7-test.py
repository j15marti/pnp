#!/usr/bin/env python3
"""Bounded red-team checks for EXTREME-1 and the ARC6 fallback collision.

Semantics only.  Python containers are not a random-access-machine space
certificate.  Every invocation is guarded by a 25-second alarm.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import signal
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def timeout(*_: object) -> None:
    raise TimeoutError("25-second REDTEAM-STRENGTHEN7 budget exceeded")


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula)


def extreme1(formula: Formula) -> dict[int, bool] | None:
    vs = variables(formula)
    for base in (False, True):
        assignment = {v: base for v in vs}
        if satisfies(formula, assignment):
            return assignment
        bad = next(clause for clause in formula
                   if not any(assignment[abs(lit)] == (lit > 0)
                              for lit in clause))
        for lit in bad:
            candidate = dict(assignment)
            candidate[abs(lit)] = not base
            if satisfies(formula, candidate):
                return candidate
    return None


def p0(x: int, y: int, z: int) -> Formula:
    return ((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z))


def guard(source: Formula, q: int) -> tuple[Formula, int]:
    m = len(source)
    h, r = q + 1, q + 2
    out = list(source) + [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        out.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        out.extend(p0(h, 2 * q + 2 * j + 1, 2 * q + 2 * j + 2))
    return tuple(out), 2 * q + 2 * m + 2


def proper_guard(source: Formula, q: int) -> tuple[Formula, int]:
    m = len(source)
    h, r = q + 1, q + 2
    old_max = 2 * q + 2 * m + 2
    zp, zm = old_max + 1, old_max + 2
    out = list(source)
    out += [(h, -r, zp), (h, -r, -zp),
            (-h, r, zm), (-h, r, -zm)]
    for v in range(1, q + 1):
        out.extend(p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        out.extend(p0(h, 2 * q + 2 * j + 1, 2 * q + 2 * j + 2))
    return tuple(out), old_max + 2


def isolate(source: Formula, q: int) -> tuple[Formula, int]:
    out: list[Clause] = []
    nxt = q
    for clause in source:
        clone_clause: list[int] = []
        gadgets: list[Clause] = []
        for lit in clause:
            y, z, w = nxt + 1, nxt + 2, nxt + 3
            nxt += 3
            x = abs(lit)
            clone_clause.append(y if lit > 0 else -y)
            gadgets += [(-x, y, z), (-x, y, -z),
                        (x, -y, w), (x, -y, -w)]
        out.append(tuple(clone_clause))
        out.extend(gadgets)
    return tuple(out), nxt


def old_embedding(source: Formula, q: int) -> tuple[Formula, int]:
    iso, qi = isolate(source, q)
    inner, qinner = proper_guard(iso, qi)
    return guard(inner, qinner)


def force_literal(lit: int, u: int, v: int) -> Formula:
    return tuple((lit, su * u, sv * v)
                 for su, sv in itertools.product((-1, 1), repeat=2))


def shield(source: Formula, q: int) -> tuple[Formula, int, tuple[int, ...], tuple[int, ...]]:
    out = list(source)
    forced_true: list[int] = []
    forced_false: list[int] = []
    nxt = q
    for desired in (True, True, False, False):
        t, u, v = nxt + 1, nxt + 2, nxt + 3
        nxt += 3
        out.extend(force_literal(t if desired else -t, u, v))
        (forced_true if desired else forced_false).append(t)
    return tuple(out), nxt, tuple(forced_true), tuple(forced_false)


def balanced_shield(source: Formula, q: int) -> tuple[Formula, int]:
    """Replace each source bit by an exactly-one positive pair."""
    mapped: list[Clause] = []
    for clause in source:
        mapped.append(tuple(4 * (abs(lit) - 1) + (1 if lit > 0 else 2)
                            for lit in clause))
    for i in range(q):
        p, n, a, b = 4 * i + 1, 4 * i + 2, 4 * i + 3, 4 * i + 4
        mapped.extend([
            (p, n, a), (p, n, -a),
            (-p, -n, b), (-p, -n, -b),
        ])
    return tuple(mapped), 4 * q


def nae2_shield(source: Formula, q: int) -> tuple[Formula, int]:
    """Two disjoint NAE triples force at least two bits of each polarity."""
    a, b, c, d, e, f = range(q + 1, q + 7)
    return tuple(source) + (
        (a, b, c), (-a, -b, -c),
        (d, e, f), (-d, -e, -f),
    ), q + 6


def brute_sat(formula: Formula) -> bool:
    vs = variables(formula)
    for values in itertools.product((False, True), repeat=len(vs)):
        if satisfies(formula, dict(zip(vs, values))):
            return True
    return False


def force_gadget_truth_table() -> int:
    checks = 0
    for positive in (False, True):
        lit = 1 if positive else -1
        formula = force_literal(lit, 2, 3)
        for t, u, v in itertools.product((False, True), repeat=3):
            got = satisfies(formula, {1: t, 2: u, 3: v})
            assert got == (t if positive else not t)
            checks += 1
    return checks


def main() -> None:
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(25)
    started = time.perf_counter()

    source: Formula = ((-1, -2, -3),)
    embedded, qembedded = old_embedding(source, 3)
    old_witness = extreme1(embedded)
    assert old_witness is not None
    assert all(not value for value in old_witness.values())

    shielded, qshield, forced_true, forced_false = shield(source, 3)
    assert brute_sat(source) == brute_sat(shielded)
    assert extreme1(shielded) is None
    shielded_embedded, qshielded_embedded = old_embedding(shielded, qshield)
    assert extreme1(shielded_embedded) is None

    balanced, qbalanced = balanced_shield(source, 3)
    assert brute_sat(source) == brute_sat(balanced)
    assert extreme1(balanced) is None
    balanced_embedded, qbalanced_embedded = old_embedding(balanced, qbalanced)
    assert extreme1(balanced_embedded) is None

    nae2, qnae2 = nae2_shield(source, 3)
    assert brute_sat(source) == brute_sat(nae2)
    assert extreme1(nae2) is None
    nae2_embedded, qnae2_embedded = old_embedding(nae2, qnae2)
    assert extreme1(nae2_embedded) is None
    # One NAE block is insufficient: a weight-one model is accepted.
    one_nae: Formula = ((1, 2, 3), (-1, -2, -3))
    assert extreme1(one_nae) is not None

    # Test SAT-equivalence of the shield on every proper one-clause formula
    # over variables 1,2,3, including all eight sign patterns.
    shield_equivalence_checks = 0
    balanced_equivalence_checks = 0
    nae2_equivalence_checks = 0
    for signs in itertools.product((-1, 1), repeat=3):
        candidate = (tuple(signs[i] * (i + 1) for i in range(3)),)
        candidate_shield, _, _, _ = shield(candidate, 3)
        assert brute_sat(candidate) == brute_sat(candidate_shield)
        assert extreme1(candidate_shield) is None
        shield_equivalence_checks += 1
        candidate_balanced, _ = balanced_shield(candidate, 3)
        assert brute_sat(candidate) == brute_sat(candidate_balanced)
        assert extreme1(candidate_balanced) is None
        balanced_equivalence_checks += 1
        candidate_nae2, _ = nae2_shield(candidate, 3)
        assert brute_sat(candidate) == brute_sat(candidate_nae2)
        assert extreme1(candidate_nae2) is None
        nae2_equivalence_checks += 1

    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL finite semantic checks",
        "force_gadget_truth_table_checks": force_gadget_truth_table(),
        "old_embedding_counterexample": {
            "source": source,
            "source_variables": 3,
            "embedded_variables": qembedded,
            "embedded_clauses": len(embedded),
            "extreme1_accepts_all_false": True,
        },
        "shield_candidate": {
            "shielded_source_variables": qshield,
            "shielded_source_clauses": len(shielded),
            "forced_true_variables": forced_true,
            "forced_false_variables": forced_false,
            "extreme1_declines_before_embedding": True,
            "embedded_variables": qshielded_embedded,
            "embedded_clauses": len(shielded_embedded),
            "extreme1_declines_after_embedding": True,
            "one_clause_equivalence_checks": shield_equivalence_checks,
        },
        "balanced_exact_one_shield_candidate": {
            "shielded_source_variables": qbalanced,
            "shielded_source_clauses": len(balanced),
            "embedded_variables": qbalanced_embedded,
            "embedded_clauses": len(balanced_embedded),
            "extreme1_declines_before_embedding": True,
            "extreme1_declines_after_embedding": True,
            "one_clause_equivalence_checks": balanced_equivalence_checks,
            "every_model_weight_interval": [3, 9],
        },
        "two_nae_block_shield": {
            "classification": "PROVED/EXACT symbolically; finite instance checked",
            "shielded_source_variables": qnae2,
            "shielded_source_clauses": len(nae2),
            "embedded_variables": qnae2_embedded,
            "embedded_clauses": len(nae2_embedded),
            "extreme1_declines_before_embedding": True,
            "extreme1_declines_after_embedding": True,
            "one_clause_equivalence_checks": nae2_equivalence_checks,
            "one_nae_block_insufficient_control": True,
        },
        "limitations": [
            "Finite checks do not replace ARC6's symbolic universal old-portfolio theorem, reused with source F and Q.",
            "Python assignment dictionaries are not a writable-space certificate.",
            "The larger forced-constant and exact-one alternatives are not separately promoted; the two-NAE shield composes with ARC6's proved universal map.",
        ],
    }
    result["seconds"] = time.perf_counter() - started
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name(
        "2026-10-09_0215_REDTEAM-STRENGTHEN7-results.json"
    )
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
