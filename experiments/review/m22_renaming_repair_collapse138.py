#!/usr/bin/env python3
"""Audit the canonical slotwise M22 repair after pinning.

The repair substitutes a fresh variable into every incident slot of the
pinned variable.  It restores syntax exactly, but is only alpha-renaming of
the unpinned parent and therefore erases branch information.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
from collections import Counter
from pathlib import Path

Y_POS = {(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)}
Y_NEG = {(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)}


def clauses_from_supports(pos, neg):
    return [normalize_clause(s) for s in sorted(pos)] + [normalize_clause(tuple(-v for v in s)) for s in sorted(neg)]


def normalize_clause(c):
    return tuple(sorted(tuple(c), key=abs))


def normalize_formula(clauses):
    return sorted(normalize_clause(c) for c in clauses)


Y = clauses_from_supports(Y_POS, Y_NEG)


def support(c):
    return tuple(sorted(abs(x) for x in c))


def validate_m22(clauses):
    clauses = [normalize_clause(c) for c in clauses]
    if len(set(clauses)) != len(clauses):
        return False, "duplicate_clause"
    deg = Counter()
    vs = set()
    for c in clauses:
        if len(c) != 3:
            return False, "nonternary"
        if len({abs(x) for x in c}) != 3:
            return False, "repeated_variable"
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False, "mixed_sign"
        for x in c:
            deg[(abs(x), x > 0)] += 1
            vs.add(abs(x))
    if any(deg[(v, True)] != 2 or deg[(v, False)] != 2 for v in vs):
        return False, "wrong_quota"
    return True, "ok"


def paired(clauses):
    p = {support(c) for c in clauses if c[0] > 0}
    n = {support(c) for c in clauses if c[0] < 0}
    return p == n


def assignments(clauses):
    vs = sorted({abs(x) for c in clauses for x in c})
    out = []
    for bits in itertools.product((0, 1), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if all(any(bool(a[abs(x)]) == (x > 0) for x in c) for c in clauses):
            out.append(a)
    return out


def simplify(clauses, fixed):
    out = []
    for c in clauses:
        rem = []
        sat = False
        for lit in c:
            v = abs(lit)
            if v not in fixed:
                rem.append(lit)
            elif bool(fixed[v]) == (lit > 0):
                sat = True
                break
        if not sat:
            out.append(tuple(rem))
    return out


def rename_formula(clauses, old, fresh):
    return [tuple((fresh if x > 0 else -fresh) if abs(x) == old else x for x in c)
            for c in clauses]


def slot_repair(clauses, old, bit, fresh):
    """Repair the branch record-by-record while preserving co-literal pairs."""
    residual = simplify(clauses, {old: bit})
    repaired = [tuple(c) for c in residual if len(c) == 3]
    short = [tuple(c) for c in residual if len(c) == 2]
    # False incident literals leave two binary records; refill their slots.
    false_sign = -1 if bit else 1
    for c in short:
        repaired.append(tuple(c) + (false_sign * fresh,))
    # True incident literals deleted two records; reintroduce them with fresh.
    true_sign = 1 if bit else -1
    for c in clauses:
        if true_sign * old in c:
            repaired.append(tuple((true_sign * fresh) if abs(x) == old else x for x in c))
    return repaired


def relation(clauses, retained, fixed=None):
    fixed = {} if fixed is None else dict(fixed)
    all_vs = sorted({abs(x) for c in clauses for x in c})
    hidden = [v for v in all_vs if v not in retained and v not in fixed]
    out = set()
    for rb in itertools.product((0, 1), repeat=len(retained)):
        ra = dict(zip(retained, rb))
        ok = False
        for hb in itertools.product((0, 1), repeat=len(hidden)):
            a = dict(fixed); a.update(ra); a.update(dict(zip(hidden, hb)))
            if all(any(bool(a[abs(x)]) == (x > 0) for x in c) for c in clauses):
                ok = True
                break
        if ok:
            out.add(rb)
    return out


def balanced_families_6():
    triples = list(itertools.combinations(range(1, 7), 3))
    out = []
    for fam in itertools.combinations(triples, 4):
        deg = Counter(v for s in fam for v in s)
        if all(deg[v] == 2 for v in range(1, 7)):
            out.append(frozenset(fam))
    return out


def parse_doecker(path):
    lines = [ln for ln in Path(path).read_text().splitlines() if not ln.lstrip().startswith("#")]
    return [tuple(c) for c in ast.literal_eval("\n".join(lines))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doecker-source", default="DOECKER61_original_source.txt")
    ap.add_argument("--output", default="m22_renaming_repair_collapse138_results.json")
    args = ap.parse_args()

    fams = balanced_families_6()
    repair_cases = 0
    repair_failures = 0
    model_count_failures = 0
    pair_status_failures = 0
    for p in fams:
        for q in fams:
            f = clauses_from_supports(p, q)
            base_models = len(assignments(f))
            for old in range(1, 7):
                for bit in (0, 1):
                    repair_cases += 1
                    fresh = 7
                    g = slot_repair(f, old, bit, fresh)
                    rho = rename_formula(f, old, fresh)
                    if normalize_formula(g) != normalize_formula(rho) or not validate_m22(g)[0]:
                        repair_failures += 1
                    if len(assignments(g)) != base_models:
                        model_count_failures += 1
                    if paired(g) != paired(f):
                        pair_status_failures += 1

    y_one = []
    for old in range(1, 7):
        retained = [v for v in range(1, 7) if v != old]
        proj = relation(Y, retained)
        for bit in (0, 1):
            br = relation(Y, retained, {old: bit})
            assert br <= proj
            y_one.append({"variable": old, "bit": bit, "branch": len(br),
                          "projection": len(proj), "extra_from_erased_branch": len(proj - br)})

    y_two = []
    for old1 in range(1, 7):
        for old2 in range(1, 7):
            if old2 == old1:
                continue
            retained = [v for v in range(1, 7) if v not in (old1, old2)]
            proj = relation(Y, retained)
            for b1 in (0, 1):
                for b2 in (0, 1):
                    br = relation(Y, retained, {old1: b1, old2: b2})
                    assert br <= proj
                    y_two.append({"variables": [old1, old2], "bits": [b1, b2],
                                  "branch": len(br), "projection": len(proj),
                                  "extra_from_erased_branches": len(proj - br)})

    u = parse_doecker(args.doecker_source)
    u_ok, _ = validate_m22(u)
    u_repair_failures = 0
    for old in range(1, 199):
        for bit in (0, 1):
            g = slot_repair(u, old, bit, 199)
            if normalize_formula(g) != normalize_formula(rename_formula(u, old, 199)) or not validate_m22(g)[0]:
                u_repair_failures += 1

    branch_budget = []
    k = 24
    for d in range(0, 9):
        B = 2 ** d
        psi = B * (2 ** k)  # every repaired child restores k active variables
        r = k - (k + d)
        assert psi == 2 ** (k + d) and r == -d
        branch_budget.append({"k": k, "d": d, "children": B,
                              "repaired_active_variables_each": k,
                              "Psi_if_independently_completed": psi,
                              "R_search": r,
                              "isomorphic_child_types_after_cache": 1})

    result = {
        "run": "M22_RENAMING_REPAIR_COLLAPSE138",
        "status": "PROVED/EXACT symbolic identity; COMPUTATIONAL finite audits",
        "anchor_Y": {
            "valid_m22": validate_m22(Y)[0],
            "fully_paired": paired(Y),
            "models": len(assignments(Y)),
            "witness_111000": any(tuple(a[v] for v in range(1, 7)) == (1, 1, 1, 0, 0, 0)
                                    for a in assignments(Y)),
        },
        "complete_k6": {
            "balanced_support_families": len(fams),
            "formulas": len(fams) ** 2,
            "one_pin_repair_cases": repair_cases,
            "repair_identity_or_grammar_failures": repair_failures,
            "model_count_failures": model_count_failures,
            "pair_status_failures": pair_status_failures,
        },
        "Y_boundary_semantics": {
            "one_level_cases": len(y_one),
            "one_level_strict_collapses": sum(x["extra_from_erased_branch"] > 0 for x in y_one),
            "one_level": y_one,
            "two_level_cases": len(y_two),
            "two_level_strict_collapses": sum(x["extra_from_erased_branches"] > 0 for x in y_two),
            "two_level_min_extra": min(x["extra_from_erased_branches"] for x in y_two),
            "two_level_max_extra": max(x["extra_from_erased_branches"] for x in y_two),
        },
        "doecker_fixture": {
            "valid_m22": u_ok,
            "variables": 198,
            "clauses": len(u),
            "one_pin_repair_cases": 396,
            "repair_identity_or_grammar_failures": u_repair_failures,
            "unsat_label": "imported from Doecker; not recomputed",
        },
        "independent_completion_budget": branch_budget,
        "limitations": [
            "slot repair is deliberately support-faithful and uses one fresh alias",
            "general semantic gadgets using more variables/clauses remain open",
            "finite checks are not asymptotic time lower bounds",
            "logical operations are not FLMV physical bit-step measurements",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
