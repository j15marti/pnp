#!/usr/bin/env python3
"""Finite audit for ARC-M22-HEREDITARY-MARGIN171.

All exhaustive loops are deliberately tiny.  The script checks exact endpoint
arithmetic, the fixed M22 instance Y, two levels of a deliberately growing
domain-restoration operator, a neutral three-port gadget, and two-level joins
of arbitrary binary relations.  These checks establish only the finite claims
recorded in the accompanying report.
"""

from fractions import Fraction
from itertools import product
import json
import time


def sat_clause(clause, assignment):
    return any((assignment[abs(lit) - 1] == 1) if lit > 0
               else (assignment[abs(lit) - 1] == 0) for lit in clause)


def models(formula, nvars):
    return [a for a in product((0, 1), repeat=nvars)
            if all(sat_clause(c, a) for c in formula)]


def m22_audit(formula):
    clauses = [tuple(c) for c in formula]
    variables = sorted({abs(lit) for c in clauses for lit in c})
    unique = len(clauses) == len(set(clauses))
    proper = all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
    monotone = all(all(x > 0 for x in c) or all(x < 0 for x in c) for c in clauses)
    counts = {v: [0, 0] for v in variables}
    for c in clauses:
        for lit in c:
            counts[abs(lit)][0 if lit > 0 else 1] += 1
    balanced = all(pair == [2, 2] for pair in counts.values())
    clause_set = set(clauses)
    fully_paired = all(tuple(-x for x in c) in clause_set for c in clauses)
    complement_pairs = sum(tuple(-x for x in c) in clause_set for c in clauses) // 2
    return {
        "variables": len(variables), "clauses": len(clauses), "unique": unique,
        "proper": proper, "clausewise_monotone": monotone,
        "exact_2_2": balanced, "fully_paired": fully_paired,
        "complement_pairs": complement_pairs,
    }


def shift_formula(formula, offset):
    return [tuple((abs(x) + offset) if x > 0 else -(abs(x) + offset) for x in c)
            for c in formula]


def three_copy_plus_y(formula, nvars, y):
    out = []
    for i in range(3):
        out.extend(shift_formula(formula, i * nvars))
    out.extend(shift_formula(y, 3 * nvars))
    return out, 3 * nvars + 6


def neutral_gplus_counts():
    # Ports x,y,z are variables 1,2,3; private a,b,c,d,e,f are 4..9.
    g = [(4, 2, 3), (1, 5, 6), (4, 7, 8), (5, 7, 9), (6, 8, 9),
         (-4, -5, -7), (-4, -6, -9), (-5, -6, -8), (-7, -8, -9)]
    counts = []
    for port in product((0, 1), repeat=3):
        count = 0
        for private in product((0, 1), repeat=6):
            if all(sat_clause(c, port + private) for c in g):
                count += 1
        counts.append(count)
    return counts


def relation(mask):
    return {(x, y) for x in (0, 1) for y in (0, 1)
            if mask & (1 << (2 * x + y))}


def compose(r, s):
    return {(x, z) for x in (0, 1) for z in (0, 1)
            if any((x, y) in r and (y, z) in s for y in (0, 1))}


def join_audit():
    rels = [relation(mask) for mask in range(16)]
    two_checks = 0
    four_checks = 0
    failures = []
    for r in rels:
        for s in rels:
            comp = compose(r, s)
            for x, z in product((0, 1), repeat=2):
                direct = any((x, y) in r and (y, z) in s for y in (0, 1))
                two_checks += 1
                if ((x, z) in comp) != direct:
                    failures.append("two")
    for r0 in rels:
        for r1 in rels:
            left = compose(r0, r1)
            for r2 in rels:
                for r3 in rels:
                    right = compose(r2, r3)
                    tree = compose(left, right)
                    for x, z in product((0, 1), repeat=2):
                        direct = any((x, a) in r0 and (a, b) in r1 and
                                     (b, c) in r2 and (c, z) in r3
                                     for a, b, c in product((0, 1), repeat=3))
                        four_checks += 1
                        if ((x, z) in tree) != direct:
                            failures.append("four")
    return two_checks, four_checks, failures


def fstr(x):
    return f"{x.numerator}/{x.denominator}"


def main():
    started = time.time()
    y = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
         (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6)]
    ya = m22_audit(y)
    ym = models(y, 6)
    assert ya == {"variables": 6, "clauses": 8, "unique": True,
                  "proper": True, "clausewise_monotone": True,
                  "exact_2_2": True, "fully_paired": False,
                  "complement_pairs": 0}
    assert len(ym) == 20 and (1, 1, 1, 0, 0, 0) in ym

    level1, n1 = three_copy_plus_y(y, 6, y)
    level2, n2 = three_copy_plus_y(level1, n1, y)
    l1 = m22_audit(level1)
    l2 = m22_audit(level2)
    assert (n1, len(level1), n2, len(level2)) == (24, 32, 78, 104)
    assert all(a["unique"] and a["proper"] and a["clausewise_monotone"] and
               a["exact_2_2"] and not a["fully_paired"]
               for a in (l1, l2))

    gcounts = neutral_gplus_counts()
    assert gcounts == [6, 16, 16, 16, 10, 23, 23, 23]

    two_checks, four_checks, join_failures = join_audit()
    assert not join_failures

    endpoint_t = Fraction(241, 200)
    endpoint_s = Fraction(11642479, 23232400)
    kappa_star = (endpoint_t - 1) / 4
    assert kappa_star == Fraction(41, 800)
    samples = []
    for kappa in [Fraction(0), Fraction(1, 100), Fraction(1, 20),
                  kappa_star, Fraction(3, 50), Fraction(1, 10)]:
        a = Fraction(1, 2) + 2 * kappa
        deep = a / (1 - Fraction(1, 2))
        assert deep == 1 + 4 * kappa
        depth_values = []
        for d in range(1, 13):
            finite = a * (1 - Fraction(1, 2) ** d) / (1 - Fraction(1, 2))
            assert finite < deep or deep == 0
            depth_values.append(fstr(finite))
        samples.append({"kappa": fstr(kappa), "a": fstr(a),
                        "limit_time_exponent": fstr(deep),
                        "strict_FLVM_time_entry": deep < endpoint_t,
                        "depth_1_to_12": depth_values})

    result = {
        "run_id": "ARC-M22-HEREDITARY-MARGIN171",
        "status": "COMPUTATIONAL finite audit; no all-input contraction claim",
        "exact_thresholds": {
            "FLMV_time": fstr(endpoint_t), "FLMV_space": fstr(endpoint_s),
            "kappa_strict_threshold": fstr(kappa_star),
            "kappa_1_20_limit": fstr(1 + 4 * Fraction(1, 20)),
            "time_margin_at_1_20": fstr(endpoint_t - Fraction(6, 5)),
        },
        "Y": {**ya, "model_count": len(ym), "witness_111000": True},
        "domain_restoration_growth_control": {
            "level0": {"variables": 6, "clauses": 8},
            "level1": {"variables": n1, "clauses": len(level1)},
            "level2": {"variables": n2, "clauses": len(level2)},
            "interpretation": "closure and label preservation do not imply contraction"
        },
        "neutral_Gplus_extension_counts_lexicographic_ports": gcounts,
        "join_controls": {"two_relation_endpoint_checks": two_checks,
                          "four_relation_two_level_endpoint_checks": four_checks,
                          "failures": len(join_failures)},
        "exponent_samples": samples,
        "elapsed_seconds": round(time.time() - started, 6),
    }
    with open("2026-10-25_1048_ARC_M22_HEREDITARY_MARGIN171_raw.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
