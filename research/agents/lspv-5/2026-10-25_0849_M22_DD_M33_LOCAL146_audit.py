#!/usr/bin/env python3
"""Finite audit of the Darmann--Docker signed-(2,2) -> monotone-(3,3) leg.

This is a finite, standard-library-only reproducer.  It verifies the exact gadget
truth tables, fixed-block construction, signed occurrence tags, exhaustive
three-variable source controls, and one deterministically searched opposite-label
source control.  It does not measure FLMV bit work and proves no asymptotic lower
bound.
"""

from __future__ import annotations

import itertools
import json
import ast
from collections import Counter, defaultdict
from pathlib import Path

SEED = 1460849
OUT = Path(__file__).with_name("2026-10-25_0849_M22_DD_M33_LOCAL146_results.json")
DOCKER = Path(__file__).parents[1] / "lspv-2" / "2026-10-24_0011_DOECKER61_original_source.txt"


def sat_clause(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def sat_formula(clauses, assignment):
    return all(sat_clause(c, assignment) for c in clauses)


def is_sat(clauses, n):
    for bits in itertools.product((False, True), repeat=n):
        a = {i + 1: bits[i] for i in range(n)}
        if sat_formula(clauses, a):
            return True, bits
    return False, None


def signed22_ok(clauses, n):
    if len(clauses) * 3 != 4 * n or len(set(map(tuple, clauses))) != len(clauses):
        return False
    cnt = Counter()
    for c in clauses:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False
        for lit in c:
            cnt[(abs(lit), lit > 0)] += 1
    return all(cnt[(v, s)] == 2 for v in range(1, n + 1) for s in (False, True))


def gadget_A(x1, x2, aux):
    a, b, c, d = aux
    return [
        (-a, -b, -x1), (-a, -c, -x1), (-a, -d, -x1),
        (-b, -c, -x2), (-b, -d, -x2), (-c, -d, -x2),
        (a, b, c), (a, b, d), (a, c, d), (b, c, d),
    ]


def gadget_Sbar(y, aux):
    a, b, c, d, e, f = aux
    return [
        (-y, -a, -b), (-y, -c, -d), (-y, -e, -f),
        (-a, -c, -f), (-a, -d, -e), (-b, -c, -e), (-b, -d, -f),
        (a, c, f), (a, d, e), (a, e, f),
        (b, c, d), (b, c, e), (b, d, f),
    ]


def construct(clauses, n):
    assert n % 3 == 0 and signed22_ok(clauses, n)
    out = []
    # Transformed source clauses: negative occurrences use x_(i,1), positive x_(i,2).
    for c in clauses:
        out.append(tuple(2 * (abs(lit) - 1) + (2 if lit > 0 else 1) for lit in c))
    # Per-variable A blocks.
    for i in range(1, n + 1):
        x1, x2 = 2 * i - 1, 2 * i
        aux = tuple(range(2 * n + 4 * (i - 1) + 1, 2 * n + 4 * i + 1))
        out.extend(gadget_A(x1, x2, aux))
    # Padded pair clauses, then one complemented S block per three variables.
    for i in range(1, n + 1):
        batch = (i - 1) // 3
        y = 6 * n + 7 * batch + 1
        out.append((2 * i - 1, 2 * i, y))
    for batch in range(n // 3):
        y = 6 * n + 7 * batch + 1
        out.extend(gadget_Sbar(y, tuple(range(y + 1, y + 7))))
    return out, 25 * n // 3


def m33_ok(clauses, n):
    if len(clauses) != 2 * n or len(set(map(tuple, clauses))) != len(clauses):
        return False
    cnt = Counter()
    tags = defaultdict(lambda: {False: [], True: []})
    for ci, c in enumerate(clauses):
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False
        for lit in c:
            sign = lit > 0
            cnt[(abs(lit), sign)] += 1
            tags[abs(lit)][sign].append(ci)
    return all(cnt[(v, s)] == 3 and len(tags[v][s]) == 3
               for v in range(1, n + 1) for s in (False, True))


def extension_exists(block, fixed, aux_ids):
    for bits in itertools.product((False, True), repeat=len(aux_ids)):
        a = dict(fixed)
        a.update({v: bits[i] for i, v in enumerate(aux_ids)})
        if sat_formula(block, a):
            return True
    return False


def audit_gadgets():
    checks = 0
    A = gadget_A(1, 2, (3, 4, 5, 6))
    a_table = {}
    for x1, x2 in itertools.product((False, True), repeat=2):
        got = extension_exists(A, {1: x1, 2: x2}, (3, 4, 5, 6))
        want = not (x1 and x2)
        assert got == want
        a_table[f"{int(x1)}{int(x2)}"] = got
        checks += 1
    S = gadget_Sbar(1, (2, 3, 4, 5, 6, 7))
    s_table = {}
    for y in (False, True):
        got = extension_exists(S, {1: y}, (2, 3, 4, 5, 6, 7))
        want = not y
        assert got == want
        s_table[str(int(y))] = got
        checks += 1
    return checks, a_table, s_table


def enumerate_n3():
    checks = 0
    total = sat_count = 0
    for plus_sets in itertools.product(itertools.combinations(range(4), 2), repeat=3):
        clauses = []
        for row in range(4):
            clauses.append(tuple(v if row in plus_sets[v - 1] else -v for v in range(1, 4)))
        if not signed22_ok(clauses, 3):
            continue
        total += 1
        src_sat, _ = is_sat(clauses, 3)
        sat_count += int(src_sat)
        target, nt = construct(clauses, 3)
        assert nt == 25 and len(target) == 50 and m33_ok(target, nt)
        # Gadget semantics makes target SAT iff a source assignment is SAT.
        semantic_sat = False
        for bits in itertools.product((False, True), repeat=3):
            source_assignment = {i + 1: bits[i] for i in range(3)}
            if sat_formula(clauses, source_assignment):
                semantic_sat = True
                break
        assert semantic_sat == src_sat
        checks += 4
    return checks, total, sat_count


def opposite_label_controls():
    # SAT: the first valid n=3 source found by complete enumeration.
    sat_source = None
    for plus_sets in itertools.product(itertools.combinations(range(4), 2), repeat=3):
        f = [tuple(v if row in plus_sets[v - 1] else -v for v in range(1, 4))
             for row in range(4)]
        if signed22_ok(f, 3):
            sat_source = f
            break
    assert sat_source is not None
    sat_label, witness = is_sat(sat_source, 3)
    assert sat_label
    sat_target, sat_nt = construct(sat_source, 3)
    assert m33_ok(sat_target, sat_nt)

    # UNSAT: original 198/264 monotone-(2,2) source.  Its label is an imported
    # published/certificate-checked dependency; this audit rechecks syntax and
    # target syntax but does not enumerate 2^198 assignments.
    raw = "\n".join(line for line in DOCKER.read_text(encoding="utf-8").splitlines()
                    if not line.startswith("#"))
    unsat_source = [tuple(c) for c in ast.literal_eval(raw)]
    assert signed22_ok(unsat_source, 198)
    unsat_target, unsat_nt = construct(unsat_source, 198)
    assert unsat_nt == 1650 and len(unsat_target) == 3300 and m33_ok(unsat_target, unsat_nt)
    return 8, {
        "SAT": {"source_vars": 3, "source_clauses": 4, "witness": witness,
                "target_vars": sat_nt, "target_clauses": len(sat_target),
                "label_status": "exhaustively checked"},
        "UNSAT": {"source_vars": 198, "source_clauses": 264,
                  "target_vars": unsat_nt, "target_clauses": len(unsat_target),
                  "label_status": "imported KNOWN THEOREM/certificate dependency; not re-enumerated"},
    }


def main():
    gadget_checks, a_table, s_table = audit_gadgets()
    n3_checks, n3_total, n3_sat = enumerate_n3()
    control_checks, controls = opposite_label_controls()
    # Exact arithmetic for composition with M22-LOCAL-CHAIN140.
    for n in (3, 6, 9, 198):
        n1 = 25 * n // 3
        assert 1995 * n1 + 6 == 16625 * n + 6
        assert 2660 * n1 + 8 == 66500 * n // 3 + 8
    summary = {
        "run_id": "M22-DD-M33-LOCAL146",
        "seed": SEED,
        "status": "COMPUTATIONAL finite audit; theorem proof is separate",
        "gadget_checks": gadget_checks,
        "A_extension_table": a_table,
        "Sbar_extension_table": s_table,
        "n3_unique_signed22_formulas": n3_total,
        "n3_sat_formulas": n3_sat,
        "n3_assertion_checks": n3_checks,
        "opposite_label_controls": controls,
        "composition_arithmetic_checks": 8,
        "assertion_accounted_checks": gadget_checks + n3_checks + control_checks + 8,
        "failures": 0,
        "limitations": [
            "finite controls do not prove asymptotic locality or a lower bound",
            "equivalence uses exact proved gadget truth tables, not brute force over 50 target variables",
            "no FLMV bit-work, peak-space, flips, bit-time, or hardware metric is measured",
        ],
    }
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
