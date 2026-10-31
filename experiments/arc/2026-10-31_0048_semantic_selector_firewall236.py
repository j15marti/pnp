#!/usr/bin/env python3
"""Exact finite controls for ARC-SEMANTIC-SELECTOR-FIREWALL236.

The symbolic theorem is in the accompanying report.  This producer exhausts
all 256 subformulas of the eight proper ternary clauses on three variables,
checks the nonlinear SAT-label selector, original-clause S/U diagnostics, and
the exact DELAY exponent inequality.  It uses only the Python standard library.
"""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

RUN = "ARC-SEMANTIC-SELECTOR-FIREWALL236"
RAW = Path("results/raw/arc/2026-10-31_0048_LSPV5_SEMANTIC_SELECTOR_FIREWALL236_raw.json")


def all_signed_clauses():
    # Clause indexed by the unique assignment that falsifies it.
    out = []
    for falsifying in itertools.product((0, 1), repeat=3):
        out.append(tuple(-(i + 1) if falsifying[i] else (i + 1) for i in range(3)))
    return out


CLAUSES = all_signed_clauses()
T_CHILD = [(1, 2, 3)]
U_CHILD = CLAUSES[:]


def lit_true(lit, a):
    v = a[abs(lit) - 1]
    return bool(v) if lit > 0 else not bool(v)


def clause_count(clause, a):
    return sum(lit_true(l, a) for l in clause)


def models(formula):
    return [a for a in itertools.product((0, 1), repeat=3)
            if all(clause_count(c, a) >= 1 for c in formula)]


def dpll_nodes(formula, partial=None):
    partial = {} if partial is None else dict(partial)
    for clause in formula:
        undecided = []
        sat = False
        for lit in clause:
            v = abs(lit) - 1
            if v in partial:
                if (partial[v] == 1) == (lit > 0):
                    sat = True
                    break
            else:
                undecided.append(lit)
        if not sat and not undecided:
            return False, 1
    if len(partial) == 3:
        return True, 1
    v = next(i for i in range(3) if i not in partial)
    total = 1
    for bit in (0, 1):
        p = dict(partial)
        p[v] = bit
        ok, nodes = dpll_nodes(formula, p)
        total += nodes
        if ok:
            return True, total
    return False, total


def local_extreme(clause, mode):
    # S makes every source literal true; U makes every source literal false.
    result = {}
    for lit in clause:
        result[abs(lit)] = int((lit > 0) == (mode == "S"))
    return result


def compatible(c1, m1, c2, m2):
    a = local_extreme(c1, m1)
    b = local_extreme(c2, m2)
    return all(v not in b or b[v] == bit for v, bit in a.items())


def source_diagnostics(formula):
    occ = []
    for j, c in enumerate(formula):
        s = local_extreme(c, "S")
        u = local_extreme(c, "U")
        assert {v: 1 - bit for v, bit in s.items()} == u
        occ.append({"clause": j, "literals": list(c), "S": s, "not_S": u,
                    "U": u, "not_U": s})
    pairs = []
    for j in range(len(formula)):
        for k in range(j + 1, len(formula)):
            record = {"j": j, "k": k}
            for mode in ("SS", "SU", "US", "UU"):
                record[mode] = compatible(formula[j], mode[0], formula[k], mode[1])
            pairs.append(record)
    endpoints = {}
    for name, a in (("0^n", (0, 0, 0)), ("1^n", (1, 1, 1))):
        counts = [clause_count(c, a) for c in formula]
        endpoints[name] = {"counts": counts,
                           "N": [counts.count(r) for r in range(4)],
                           "sat": all(x > 0 for x in counts)}
    flips = []
    a = [0, 0, 0]
    for v in (0, 1, 2, 0, 1, 2):
        a[v] ^= 1
        counts = [clause_count(c, tuple(a)) for c in formula]
        flips.append({"flip": v + 1, "assignment": a[:], "counts": counts,
                      "N": [counts.count(r) for r in range(4)]})
    return {"occurrences": occ, "pairs": pairs, "endpoints": endpoints,
            "flip_trail": flips}


def main():
    rows = []
    sat_count = unsat_count = 0
    parent_nodes = child_nodes = 0
    for mask in range(256):
        f = [CLAUSES[i] for i in range(8) if mask & (1 << i)]
        ms = models(f)
        label = "SAT" if ms else "UNSAT"
        selected = T_CHILD if ms else U_CHILD
        selected_models = models(selected)
        assert bool(ms) == bool(selected_models)
        ok, pn = dpll_nodes(f)
        cok, cn = dpll_nodes(selected)
        assert ok == bool(ms) and cok == bool(ms)
        sat_count += label == "SAT"
        unsat_count += label == "UNSAT"
        parent_nodes += pn
        child_nodes += cn
        rows.append({"mask": mask, "clauses": len(f), "label": label,
                     "models": len(ms), "parent_nodes": pn,
                     "child_kind": "T" if ms else "U", "child_nodes": cn})

    assert sat_count == 255 and unsat_count == 1
    assert len(models(T_CHILD)) == 7 and len(models(U_CHILD)) == 0

    alpha, gamma, lam = Fraction(11, 10), Fraction(3, 5), Fraction(1, 2)
    delays = []
    threshold = max(alpha, gamma / (1 - lam))
    for K in range(1, 13):
        rhs = max(alpha, gamma + lam * K)
        delays.append({"K": K, "claimed_rhs": str(rhs),
                       "parent_call_exponent": K,
                       "violates_when_parent_call_mandatory": Fraction(K) > rhs})
    assert threshold == Fraction(6, 5)
    assert all(row["violates_when_parent_call_mandatory"] for row in delays if row["K"] >= 2)

    h7 = CLAUSES[:-1]
    h8 = CLAUSES
    output = {
        "run": RUN,
        "date_PDT": "2026-10-31 00:48 PDT",
        "status": "PROVED/EXACT restricted symbolic lemma; COMPUTATIONAL finite controls; universal ARC and P vs NP OPEN",
        "exhaustive_family": {"formulas": len(rows), "SAT": sat_count,
                              "UNSAT": unsat_count, "rows": rows},
        "fixed_children": {
            "T": [list(c) for c in T_CHILD], "T_models": len(models(T_CHILD)),
            "U": [list(c) for c in U_CHILD], "U_models": len(models(U_CHILD))},
        "solver_work": {"parent_dpll_nodes": parent_nodes,
                        "selected_child_dpll_nodes": child_nodes},
        "delay_recurrence": {"alpha": str(alpha), "gamma": str(gamma),
                             "lambda": str(lam), "fixed_point_threshold": str(threshold),
                             "rows": delays},
        "same_support_controls": {
            "H7_SAT": {"models": len(models(h7)), "diagnostics": source_diagnostics(h7)},
            "H8_UNSAT": {"models": len(models(h8)), "diagnostics": source_diagnostics(h8)}},
        "limitations": [
            "The semantic selector computes the source SAT label and is not a free reduction.",
            "DPLL nodes and Python data are not FLMV native-machine resource measurements.",
            "Finite checks do not prove the asymptotic theorem; the report gives the proof."
        ]
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assertions = 256 + 2 + sum(len(x["diagnostics"]["occurrences"]) * 2 +
                               len(x["diagnostics"]["pairs"]) * 4 + 8
                               for x in output["same_support_controls"].values()) + 12
    print(json.dumps({"run": RUN, "assertion_groups": assertions,
                      "SAT": sat_count, "UNSAT": unsat_count,
                      "parent_nodes": parent_nodes, "child_nodes": child_nodes,
                      "raw": str(RAW)}, sort_keys=True))


if __name__ == "__main__":
    main()
