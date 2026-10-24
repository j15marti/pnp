#!/usr/bin/env python3
"""Audit the exact port-degree interface of Doecker's 133-clause enforcer.

The source theorem gives a clause simulator S(v1,v2,v3) with 99 fresh
internal variables and 133 proper monotone clauses.  Each port occurrence is
used once and every fresh internal variable occurs twice in each sign.  This
script audits the consequence for actual pin residuals: the lift preserves
the padded residual's external signed-degree vector and therefore cannot
repair quota deficits created by pinning.

It does not reconstruct the 133 internal clauses or independently reprove the
enforcer's semantic theorem; those are imported from arXiv:1912.08032.
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
ENFORCER_INTERNAL_VARS = 99
ENFORCER_CLAUSES = 133


def normalize_clause(c):
    return tuple(sorted(tuple(c), key=abs))


def clauses_from_supports(pos, neg):
    return ([normalize_clause(s) for s in sorted(pos)]
            + [normalize_clause(tuple(-v for v in s)) for s in sorted(neg)])


Y = clauses_from_supports(Y_POS, Y_NEG)


def signed_degrees(clauses):
    deg = Counter()
    for c in clauses:
        for lit in c:
            deg[(abs(lit), lit > 0)] += 1
    return deg


def validate_m22(clauses):
    cs = [normalize_clause(c) for c in clauses]
    if len(set(cs)) != len(cs):
        return False, "duplicate_clause"
    vs = set()
    for c in cs:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False, "nonproper"
        if not (all(x > 0 for x in c) or all(x < 0 for x in c)):
            return False, "mixed"
        vs.update(abs(x) for x in c)
    d = signed_degrees(cs)
    if any(d[(v, True)] != 2 or d[(v, False)] != 2 for v in vs):
        return False, "wrong_quota"
    return True, "ok"


def assignments(clauses):
    vs = sorted({abs(x) for c in clauses for x in c})
    out = []
    for bits in itertools.product((0, 1), repeat=len(vs)):
        a = dict(zip(vs, bits))
        if all(any(bool(a[abs(x)]) == (x > 0) for x in c) for c in clauses):
            out.append(a)
    return out


def simplify(clauses, old, bit):
    out = []
    deleted = []
    for c in clauses:
        if any(abs(lit) == old and bool(bit) == (lit > 0) for lit in c):
            deleted.append(c)
            continue
        out.append(tuple(lit for lit in c if abs(lit) != old))
    return out, deleted


def padded_residuals(clauses, old, bit):
    residual, deleted = simplify(clauses, old, bit)
    binary = [c for c in residual if len(c) == 2]
    ternary = [c for c in residual if len(c) == 3]
    assert len(binary) == 2 and len(deleted) == 2
    assert all(len(c) == 3 for c in deleted)
    for picks in itertools.product((0, 1), repeat=2):
        padded = list(ternary)
        for c, pick in zip(binary, picks):
            padded.append(tuple(c) + (c[pick],))
        yield picks, padded, deleted


def externally_balanced(clauses):
    vs = {abs(x) for c in clauses for x in c}
    d = signed_degrees(clauses)
    return all(d[(v, True)] == 2 and d[(v, False)] == 2 for v in vs)


def dense_bits(k, m):
    """Declared project dense record layout: 3 header words, 3 literals/clause."""
    w = max(1, math.ceil(math.log2(k + 1)))
    return 3 * w + 2 + 3 * m * (w + 1)


def lift_sizes(k0, m0, levels=2):
    rows = []
    k, m = k0, m0
    for level in range(levels + 1):
        rows.append({"level": level, "active_variables": k, "clauses": m,
                     "dense_bits": dense_bits(k, m),
                     "external_deficit_persists": True})
        k, m = k + ENFORCER_INTERNAL_VARS * m, ENFORCER_CLAUSES * m
    return rows


def balanced_families_6():
    triples = list(itertools.combinations(range(1, 7), 3))
    out = []
    for fam in itertools.combinations(triples, 4):
        d = Counter(v for s in fam for v in s)
        if all(d[v] == 2 for v in range(1, 7)):
            out.append(frozenset(fam))
    return out


def parse_doecker(path):
    lines = [ln for ln in Path(path).read_text().splitlines()
             if not ln.lstrip().startswith("#")]
    return [tuple(c) for c in ast.literal_eval("\n".join(lines))]


def audit_source(formulas, variables):
    pin_cases = pad_cases = valid_after_lift = 0
    min_true_deficit = 10**9
    max_true_deficit = 0
    wrong_shapes = 0
    for f in formulas:
        for old in variables(f):
            for bit in (0, 1):
                pin_cases += 1
                options = list(padded_residuals(f, old, bit))
                if len(options) != 4:
                    wrong_shapes += 1
                for _, padded, deleted in options:
                    pad_cases += 1
                    if externally_balanced(padded):
                        valid_after_lift += 1
                    true_positive = bool(bit)
                    deleted_co = {abs(lit) for c in deleted for lit in c
                                  if abs(lit) != old}
                    d = signed_degrees(padded)
                    deficits = sum(d[(v, true_positive)] < 2 for v in deleted_co)
                    min_true_deficit = min(min_true_deficit, deficits)
                    max_true_deficit = max(max_true_deficit, deficits)
    return {
        "pin_cases": pin_cases,
        "binary_padding_options": pad_cases,
        "externally_balanced_after_enforcer_interface": valid_after_lift,
        "wrong_residual_shapes": wrong_shapes,
        "min_deleted-clause_true-sign_deficit_variables": min_true_deficit,
        "max_deleted-clause_true-sign_deficit_variables": max_true_deficit,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doecker-source", default="DOECKER61_original_source.txt")
    ap.add_argument("--output", default="m22_enforcer_port_firewall139_results.json")
    args = ap.parse_args()

    fams = balanced_families_6()
    k6 = [clauses_from_supports(p, q) for p in fams for q in fams]
    k6_audit = audit_source(k6, lambda _: range(1, 7))

    u = parse_doecker(args.doecker_source)
    u_vars = sorted({abs(x) for c in u for x in c})
    u_audit = audit_source([u], lambda _: u_vars)

    y_models = assignments(Y)
    y_sizes = lift_sizes(5, 6)
    u_sizes = lift_sizes(197, 262)

    result = {
        "run": "M22_ENFORCER_PORT_FIREWALL139",
        "status": "PROVED/EXACT interface consequence; COMPUTATIONAL exhaustive audits",
        "primary_source_interface": {
            "source": "Doecker arXiv:1912.08032, printed pp. 8-9",
            "fresh_internal_variables_per_source_clause": ENFORCER_INTERNAL_VARS,
            "output_clauses_per_source_clause": ENFORCER_CLAUSES,
            "each_port_occurrence_is_used_once": True,
            "each_fresh_internal_variable_degree": {"positive": 2, "negative": 2},
            "semantics": "S(v1,v2,v3) is satisfiable over fresh variables iff at least one port literal is true",
        },
        "anchor_Y": {
            "valid_m22": validate_m22(Y)[0],
            "models": len(y_models),
            "witness_111000": any(tuple(a[v] for v in range(1, 7)) == (1, 1, 1, 0, 0, 0)
                                    for a in y_models),
            "audit": audit_source([Y], lambda _: range(1, 7)),
            "one_and_two_lift_sizes_after_one_pin": y_sizes,
            "declared_two-branch_exhaustive_R_search_after_level1": 6 - (1 + y_sizes[1]["active_variables"]),
        },
        "complete_k6": {
            "balanced_support_families": len(fams),
            "formulas": len(k6),
            "audit": k6_audit,
        },
        "doecker_U": {
            "valid_m22": validate_m22(u)[0],
            "variables": len(u_vars),
            "clauses": len(u),
            "label": "UNSAT imported from Doecker; not recomputed",
            "audit": u_audit,
            "one_and_two_lift_sizes_after_one_pin": u_sizes,
            "declared_two-branch_exhaustive_R_search_after_level1": 198 - (1 + u_sizes[1]["active_variables"]),
        },
        "exact_consequence": [
            "the enforcer lift preserves every external variable's signed occurrence multiplicities",
            "pinning deletes two true-sign clauses and binary padding adds only false-sign occurrences",
            "therefore every padded pin residual retains at least one true-sign external quota deficit",
            "iterating the enforcer preserves that deficit while multiplying clauses by 133 per level",
        ],
        "limitations": [
            "the 133 internal clauses and semantic enforcer theorem are imported from the primary paper",
            "the experiment audits the exact port-degree interface, not a reconstructed internal gadget",
            "R_search is an optional exhaustive upper-budget identity, not necessary decision time",
            "logical counts are not FLMV primitive bit-step measurements",
            "a different semantic adapter that adds new external-port clauses remains open",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
