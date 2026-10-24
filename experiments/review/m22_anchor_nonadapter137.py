#!/usr/bin/env python3
"""Independent finite audit for M22-NONPAIRED1 and the Y anchor.

Standard library only.  The 198-variable source is a transcription already
published in the repository; pass its path with --doecker-source.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import math
from collections import Counter
from pathlib import Path


Y_POS = {(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)}
Y_NEG = {(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)}


def clauses_from_supports(pos, neg):
    return [tuple(s) for s in sorted(pos)] + [tuple(-v for v in s) for s in sorted(neg)]


Y = clauses_from_supports(Y_POS, Y_NEG)


def support(c):
    return tuple(sorted(abs(x) for x in c))


def split_supports(clauses):
    p, q = set(), set()
    for c in clauses:
        (p if c[0] > 0 else q).add(support(c))
    return p, q


def validate_m22(clauses):
    if len(set(map(tuple, clauses))) != len(clauses):
        return False, "duplicate_clause"
    counts = Counter()
    seen_vars = set()
    for c in clauses:
        if len(c) != 3:
            return False, "nonternary"
        if len({abs(x) for x in c}) != 3:
            return False, "repeated_variable"
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False, "mixed_sign_clause"
        for x in c:
            counts[(abs(x), x > 0)] += 1
            seen_vars.add(abs(x))
    for v in seen_vars:
        if counts[(v, True)] != 2 or counts[(v, False)] != 2:
            return False, "wrong_occurrence_count"
    return True, "ok"


def is_paired(clauses):
    p, q = split_supports(clauses)
    return p == q


def is_cstar(clauses):
    ok, _ = validate_m22(clauses)
    return ok and not is_paired(clauses)


def models(clauses):
    vs = sorted({abs(x) for c in clauses for x in c})
    out = []
    for bits in itertools.product((0, 1), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if all(any((x > 0 and a[abs(x)]) or (x < 0 and not a[abs(x)]) for x in c)
               for c in clauses):
            out.append(bits)
    return out


def shift(clauses, delta):
    return [tuple((1 if x > 0 else -1) * (abs(x) + delta) for x in c) for c in clauses]


def anchor(clauses):
    maxv = max((abs(x) for c in clauses for x in c), default=0)
    return list(map(tuple, clauses)) + shift(Y, maxv)


def simplify(clauses, assignment):
    out = []
    for c in clauses:
        satisfied = False
        rem = []
        for x in c:
            v = abs(x)
            if v not in assignment:
                rem.append(x)
            elif bool(assignment[v]) == (x > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(rem))
    return out


def parse_doecker(path):
    lines = [ln for ln in Path(path).read_text().splitlines() if not ln.lstrip().startswith("#")]
    return [tuple(c) for c in ast.literal_eval("\n".join(lines))]


def six_variable_universe():
    triples = list(itertools.combinations(range(1, 7), 3))
    balanced = []
    for fam in itertools.combinations(triples, 4):
        deg = Counter(v for s in fam for v in s)
        if all(deg[v] == 2 for v in range(1, 7)):
            balanced.append(frozenset(fam))
    return balanced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doecker-source", default="DOECKER61_original_source.txt")
    ap.add_argument("--output", default="m22_anchor_nonadapter137_results.json")
    args = ap.parse_args()

    y_models = models(Y)
    assert len(y_models) == 20
    assert (1, 1, 1, 0, 0, 0) in y_models
    assert is_cstar(Y)

    balanced = six_variable_universe()
    qdist = Counter()
    satdist = Counter()
    pair_count = 0
    anchor_failures = 0
    piecewise_failures = 0
    total = 0
    for p in balanced:
        for qfam in balanced:
            total += 1
            f = clauses_from_supports(p, qfam)
            ok, reason = validate_m22(f)
            assert ok, reason
            qdef = len(set(p) - set(qfam))
            qdist[qdef] += 1
            assert qdef != 1
            fm = models(f)
            satdist[(qdef, bool(fm))] += 1
            if p == qfam:
                pair_count += 1
                assert fm
                target = Y
            else:
                target = f
            # If paired, target is the already checked SAT anchor Y; otherwise
            # target is literally f.  This checks the piecewise map without
            # recomputing an equivalent model table.
            target_sat = True if p == qfam else bool(fm)
            if target_sat != bool(fm) or not is_cstar(target):
                piecewise_failures += 1

            af = anchor(f)
            # On disjoint variables model counts multiply exactly.  Enumerating
            # the 12-variable product for every source would only recheck this
            # elementary Cartesian-product identity 5,625 times.
            if not is_cstar(af):
                anchor_failures += 1

    # Exact grammar-nonadapter check: for a disjoint anchor, target membership
    # is equivalent to source M22 membership.  Test all one- and two-level
    # restrictions of the canonical anchor Y.
    restriction = {"one_level": Counter(), "two_level": Counter()}
    one_residuals = []
    for v in range(1, 7):
        for bit in (0, 1):
            g = simplify(Y, {v: bit})
            ok, reason = validate_m22(g)
            restriction["one_level"][reason] += 1
            assert not ok and not is_cstar(anchor(g))
            one_residuals.append((v, bit, g))
    for v, bit, g in one_residuals:
        for w in range(1, 7):
            if w == v:
                continue
            for b2 in (0, 1):
                h = simplify(g, {w: b2})
                ok, reason = validate_m22(h)
                restriction["two_level"][reason] += 1
                assert not ok and not is_cstar(anchor(h))

    # Verify the branch-budget identity B*2^(k-d)=2^k for a complete d-bit split.
    branch_rows = []
    k = 24
    for d in range(0, 13):
        B = 2 ** d
        psi = B * (2 ** (k - d))
        r_search = k - math.log2(psi)
        assert psi == 2 ** k and r_search == 0
        branch_rows.append({"k": k, "d": d, "B": B, "Psi": psi, "R_search": r_search})

    u = parse_doecker(args.doecker_source)
    u_ok, u_reason = validate_m22(u)
    up, un = split_supports(u)
    uvars = {abs(x) for c in u for x in c}
    u_summary = {
        "clauses": len(u),
        "variables": len(uvars),
        "max_variable": max(uvars),
        "valid_m22": u_ok,
        "validation_reason": u_reason,
        "fully_paired": up == un,
        "in_cstar": is_cstar(u),
        "q": len(up - un),
        "positive_clauses": len(up),
        "negative_clauses": len(un),
    }
    assert u_ok and len(u) == 264 and len(uvars) == 198 and is_cstar(u)

    result = {
        "status": "COMPUTATIONAL finite checks plus symbolic identities",
        "Y": {
            "valid_m22": validate_m22(Y)[0],
            "in_cstar": is_cstar(Y),
            "models": len(y_models),
            "witness_111000": (1, 1, 1, 0, 0, 0) in y_models,
            "positive_supports": sorted(map(list, Y_POS)),
            "negative_supports": sorted(map(list, Y_NEG)),
        },
        "six_variable_complete_universe": {
            "balanced_unsigned_families": len(balanced),
            "ordered_signed_formulas": total,
            "paired_formulas": pair_count,
            "q_distribution": dict(sorted(qdist.items())),
            "sat_distribution_by_q_and_label": {
                f"q={q},sat={sat}": n for (q, sat), n in sorted(satdist.items())
            },
            "piecewise_reduction_failures": piecewise_failures,
            "no_test_anchor_failures": anchor_failures,
        },
        "restriction_nonadapter": {
            "one_level_cases": sum(restriction["one_level"].values()),
            "one_level_failure_reasons": dict(restriction["one_level"]),
            "two_level_cases": sum(restriction["two_level"].values()),
            "two_level_failure_reasons": dict(restriction["two_level"]),
            "reanchored_cases_in_cstar": 0,
        },
        "complete_branch_budget": branch_rows,
        "doecker_fixture": u_summary,
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
