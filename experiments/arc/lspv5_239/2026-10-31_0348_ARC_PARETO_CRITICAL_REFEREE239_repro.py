#!/usr/bin/env python3
"""Exact ARC/FLMV baseline Pareto boundary and hostile SAT controls.

All arithmetic that supports the theorem is Fraction arithmetic.  Decimal
output is presentation only.  This program is intentionally small and runs in
one sub-30-second chunk.
"""
from fractions import Fraction as F
import json


def poly(c):
    return 5*c**3 + 10*c**2 - 11*c - 10


def h(c):
    return F(1) - F(3, 5)/c


def d1(c):
    return F(2)/c - c


def d2(c):
    return (c + 2 - c**3)/(2*c**2)


def d3(c):
    return (c**2 + c + 2 - c**4)/(3*c**3)


def bisect_root(lo, hi, steps=160):
    assert poly(lo) < 0 < poly(hi)
    for _ in range(steps):
        mid = (lo + hi)/2
        if poly(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def clause_true_count(clause, assignment):
    return sum(assignment[abs(l)-1] == (l > 0) for l in clause)


def sat(formula, assignment):
    return all(clause_true_count(c, assignment) > 0 for c in formula)


def extreme(clause, mode):
    # mode S means every literal true; U means every literal false.
    truth = mode == "S"
    return [[abs(l), int((l > 0) == truth)] for l in clause]


def compatible(c, d, a, b):
    req = {}
    for v, z in extreme(c, a) + extreme(d, b):
        if v in req and req[v] != z:
            return False
        req[v] = z
    return True


def source_control(name, formula, expected):
    n = max(abs(l) for c in formula for l in c)
    models = 0
    complement_checks = 0
    endpoint = {}
    gray = []
    for mask in range(1 << n):
        a = [(mask >> i) & 1 for i in range(n)]
        b = [1-x for x in a]
        tc = [clause_true_count(c, a) for c in formula]
        uc = [clause_true_count(c, b) for c in formula]
        for x, y in zip(tc, uc):
            assert x + y == 3
            complement_checks += 1
        models += int(all(x > 0 for x in tc))
    assert (models > 0) == expected
    for label, a in [("0^n", [0]*n), ("1^n", [1]*n)]:
        vals = [clause_true_count(c, a) for c in formula]
        endpoint[label] = {"counts": vals,
                           "categories": [vals.count(k) for k in range(4)],
                           "sat": all(v > 0 for v in vals)}
    for i in range(min(1 << n, 16)):
        g = i ^ (i >> 1)
        a = [(g >> k) & 1 for k in range(n)]
        vals = [clause_true_count(c, a) for c in formula]
        gray.append({"step": i, "assignment": a,
                     "categories": [vals.count(k) for k in range(4)]})
    clauses = []
    for j, c in enumerate(formula, 1):
        clauses.append({"source_clause": j, "literals": c,
                        "S": extreme(c, "S"), "invert_S": extreme(c, "U"),
                        "U": extreme(c, "U"), "invert_U": extreme(c, "S"),
                        "occurrences": [
                            {"x_i_j": [abs(l), j], "literal": l,
                             "sign": "+" if l > 0 else "-",
                             "S_value": int(l > 0), "U_value": int(l < 0)}
                            for l in c]})
    pairs = []
    for i in range(len(formula)):
        for j in range(i+1, len(formula)):
            modes = {m: compatible(formula[i], formula[j], m[0], m[1])
                     for m in ("SS", "SU", "US", "UU")}
            # Independent brute force over all source variables.
            brute = {}
            for m in modes:
                ok = False
                for mask in range(1 << n):
                    a = [(mask >> k) & 1 for k in range(n)]
                    ok |= (clause_true_count(formula[i], a) == (3 if m[0] == "S" else 0)
                           and clause_true_count(formula[j], a) == (3 if m[1] == "S" else 0))
                brute[m] = ok
            assert modes == brute
            pairs.append({"source_clauses": [i+1, j+1], "modes": modes})
    return {"name": name, "expected_sat": expected, "models": models,
            "complement_checks": complement_checks, "endpoints": endpoint,
            "gray_flip_trail": gray, "clause_extremes": clauses,
            "pair_compatibility": pairs}


def main():
    lo0, hi0 = F(1204607, 1000000), F(1204608, 1000000)
    assert poly(lo0) < 0 < poly(hi0)
    lo, hi = bisect_root(lo0, hi0)

    # At the isolated root, FLMV k=2 beats k=1, k=3, and the entire k>=4 tail.
    # The following endpoint/derivative checks are exact certificates on [lo0,hi0].
    q13 = lambda c: -c**4 + c**2 + 4*c - 4       # 6 c^3 (d2-d3)
    q13p = lambda c: -4*c**3 + 2*c + 4
    qtail = lambda c: c**3 + 2*c**2 - c**5 - 2  # 2 c^4 (d2-c^-4)
    qtailp = lambda c: 3*c**2 + 4*c - 5*c**4
    assert q13(hi0) > 0 and q13p(lo0) < 0 and q13p(hi0) < 0
    assert qtail(hi0) > 0 and qtailp(lo0) < 0 and qtailp(hi0) < 0
    assert d2(lo0) > d1(lo0) and d2(hi0) > d1(hi0)
    # Baseline rational witnesses from the peer computation.
    c_pass, lam_pass = F(6023, 5000), F(5019, 10000)
    assert F(3, 5)/(1-lam_pass) < c_pass and lam_pass < d2(c_pass)
    lam_fail = F(251, 500)
    assert lam_fail > h(hi)  # above the global algebraic supremum

    h7 = [[(i if (mask >> (i-1)) & 1 else -i) for i in (1,2,3)]
          for mask in range(7)]
    h8 = [[(i if (mask >> (i-1)) & 1 else -i) for i in (1,2,3)]
          for mask in range(8)]
    controls = [source_control("H7 SAT", h7, True),
                source_control("H8 UNSAT", h8, False)]

    out = {
        "run": "ARC-PARETO-CRITICAL-REFEREE239",
        "status": "PROVED/EXACT conditional arithmetic; COMPUTATIONAL hostile controls; universal ARC and P versus NP OPEN",
        "machine_scope": "conditional ARC recurrence plus actual FLMV envelope; no compiler constructed",
        "root_polynomial": "5*c^3+10*c^2-11*c-10",
        "coarse_root_isolation": [str(lo0), str(hi0)],
        "coarse_polynomial_signs": [str(poly(lo0)), str(poly(hi0))],
        "critical_c_decimal": format(float((lo+hi)/2), ".15f"),
        "critical_lambda_decimal": format(float(h((lo+hi)/2)), ".15f"),
        "critical_lambda_interval": [str(h(lo)), str(h(hi))],
        "exact_formula": "lambda_crit=1-3/(5*c_crit); feasible iff lambda<lambda_crit (baseline recurrence, lambda>=1/2)",
        "k2_formula": "d_2(c)=(c+2-c^3)/(2c^2)",
        "k2_competitor_certificates": {
            "d2_minus_d1_numerator": "(c-1)^2(c+2)",
            "six_cubed_d2_minus_d3": "-c^4+c^2+4c-4",
            "two_c4_d2_minus_cminus4": "c^3+2c^2-c^5-2",
            "q13_at_upper": str(q13(hi0)),
            "qtail_at_upper": str(qtail(hi0))
        },
        "rational_controls": {
            "lambda_5019_over_10000_passes_at_c_6023_over_5000": True,
            "lambda_251_over_500_exceeds_global_supremum": True,
            "pass_Kstar": str(F(3,5)/(1-lam_pass)),
            "pass_d2": str(d2(c_pass))
        },
        "hostile_original_clause_controls": controls,
        "limitations": [
            "This optimizes only the declared baseline conditional recurrence.",
            "It proves no all-input hereditary SAT child and no native-machine resource bound.",
            "Strict FLMV inequalities mean lambda_crit is a supremum, not an attained endpoint."
        ]
    }
    with open("2026-10-31_0348_ARC_PARETO_CRITICAL_REFEREE239_raw.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({k: out[k] for k in ("run", "critical_c_decimal", "critical_lambda_decimal", "rational_controls")}, indent=2))


if __name__ == "__main__":
    main()
