#!/usr/bin/env python3
"""Independent LSPV-5 referee for the Horn/affine mixed-interface gate.

Standard library only.  The two eight-clause sources have identical size and
component labels.  One has the unique model 101; the other is UNSAT.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction


def clause_forbidden_by(a):
    """Proper clause false exactly at the 3-bit tuple a."""
    return tuple((i + 1) if bit == 0 else -(i + 1) for i, bit in enumerate(a))


ALL = list(itertools.product((0, 1), repeat=3))
UNSAT = [clause_forbidden_by(a) for a in ALL]
# Omit C_101 and duplicate C_000.  The unique model is 101; both endpoints fail.
SAT = [clause_forbidden_by(a) for a in ALL if a != (1, 0, 1)]
SAT.append(clause_forbidden_by((0, 0, 0)))


def lit_true(lit, a):
    v = a[abs(lit) - 1]
    return bool(v) if lit > 0 else not bool(v)


def eval_clause(c, a):
    return any(lit_true(l, a) for l in c)


def source_models(clauses):
    return [a for a in ALL if all(eval_clause(c, a) for c in clauses)]


def occurrence_record(j, k, lit):
    # S makes the signed literal true, U makes it false.  Inversion swaps them.
    s = 1 if lit > 0 else 0
    u = 1 - s
    return {
        "clause": j,
        "position": k,
        "variable": abs(lit),
        "sign": "+" if lit > 0 else "-",
        "S_target": s,
        "invert_S_is_U": u,
        "U_target": u,
        "invert_U_is_S": s,
    }


def pair_matrix(cj, ck):
    same, opposite = [], []
    sj = {abs(l): (l > 0) for l in cj}
    sk = {abs(l): (l > 0) for l in ck}
    for v in sorted(set(sj) & set(sk)):
        (same if sj[v] == sk[v] else opposite).append(v)
    predicted = {
        "SS": not opposite,
        "SU": not same,
        "US": not same,
        "UU": not opposite,
    }
    # Exact enumeration of coherent assignments realizing each all-literal mode.
    realized = {}
    for mode in ("SS", "SU", "US", "UU"):
        want_j = mode[0] == "S"
        want_k = mode[1] == "S"
        witnesses = []
        for a in ALL:
            okj = all(lit_true(l, a) == want_j for l in cj)
            okk = all(lit_true(l, a) == want_k for l in ck)
            if okj and okk:
                witnesses.append("".join(map(str, a)))
        realized[mode] = {"feasible": bool(witnesses), "witnesses": witnesses}
        assert bool(witnesses) == predicted[mode]
    return {"same_polarity_shared": same, "opposite_polarity_shared": opposite,
            "predicted": predicted, "enumerated": realized}


def endpoint_and_trail(clauses):
    # 000 -> 100 -> 101 -> 111 and its complete complement trail.
    trail = [(0, 0, 0), (1, 0, 0), (1, 0, 1), (1, 1, 1)]
    out = []
    for a in trail:
        counts = [sum(lit_true(l, a) for l in c) for c in clauses]
        out.append({
            "assignment": "".join(map(str, a)),
            "complement": "".join(str(1 - x) for x in a),
            "true_literal_counts": counts,
            "N0_N1_N2_N3": [counts.count(r) for r in range(4)],
            "formula_sat": all(v > 0 for v in counts),
        })
    return out


def interface_rows(clauses):
    rows = []
    for a in ALL:
        # y is the signed-occurrence falsity indicator.
        y = tuple(int(not lit_true(l, a)) for c in clauses for l in c)
        h = all(not all(y[3*j + k] for k in range(3)) for j in range(len(clauses)))
        # E is true by construction for this coherent y.  There are 2^(3m) t extensions.
        rows.append({"x": "".join(map(str, a)), "coherent_y": "".join(map(str, y)),
                     "H_on_y": h, "E_on_x_y": True,
                     "join": h, "source": all(eval_clause(c, a) for c in clauses),
                     "t_extensions_if_join": (1 << (3 * len(clauses))) if h else 0})
        assert h == all(eval_clause(c, a) for c in clauses)
    return rows


def simplify(clauses, assignment, ctr):
    out = []
    for c in clauses:
        nc = []
        sat = False
        for lit in c:
            ctr["literal_tests"] += 1
            v = abs(lit)
            if v in assignment:
                val = assignment[v]
                if (lit > 0 and val) or (lit < 0 and not val):
                    sat = True
                    break
            else:
                nc.append(lit)
        if not sat:
            if not nc:
                return None
            out.append(tuple(nc))
    return out


def dpll(clauses, nvars):
    ctr = {"nodes": 0, "branches": 0, "unit_assignments": 0, "literal_tests": 0}

    def rec(cs, a):
        ctr["nodes"] += 1
        while True:
            sc = simplify(cs, a, ctr)
            if sc is None:
                return None
            if not sc:
                return dict(a)
            units = [c[0] for c in sc if len(c) == 1]
            if not units:
                cs = sc
                break
            changed = False
            for lit in units:
                v, val = abs(lit), lit > 0
                if v in a and a[v] != val:
                    return None
                if v not in a:
                    a[v] = val
                    ctr["unit_assignments"] += 1
                    changed = True
            cs = sc
            if not changed:
                break
        v = next(i for i in range(1, nvars + 1) if i not in a)
        ctr["branches"] += 1
        for val in (False, True):
            b = dict(a); b[v] = val
            w = rec(cs, b)
            if w is not None:
                return w
        return None

    witness = rec(list(clauses), {})
    return {"sat": witness is not None, "witness": witness, **ctr}


def mixed_cnf(clauses):
    """Literal-for-literal reconstruction of T(F) using x=1..3, then y,t."""
    m = len(clauses)
    out, hpart, epart = [], [], []
    for j, c in enumerate(clauses):
        ys = [4 + 3*j + k for k in range(3)]
        h = tuple(-y for y in ys)
        out.append(h); hpart.append(h)
        for k, lit in enumerate(c):
            y = ys[k]
            t = 4 + 3*m + 3*j + k
            x = abs(lit)
            # b=1 for positive source occurrence, b=0 for negative.
            ds = [(x, y), (-x, -y)] if lit > 0 else [(-x, y), (x, -y)]
            for d in ds:
                for st in (t, -t):
                    q = (d[0], d[1], st)
                    out.append(q); epart.append(q)
    return out, hpart, epart, 3 + 6*m


def source_audit(name, clauses):
    models = source_models(clauses)
    mix, hpart, epart, nv = mixed_cnf(clauses)
    occurrence = [occurrence_record(j + 1, k + 1, lit)
                  for j, c in enumerate(clauses) for k, lit in enumerate(c)]
    pairs = []
    for j in range(len(clauses)):
        for k in range(j + 1, len(clauses)):
            pairs.append({"clauses": [j + 1, k + 1], **pair_matrix(clauses[j], clauses[k])})
    # Exact pointwise theorem and component nonemptiness.
    rows = interface_rows(clauses)
    assert sum(r["join"] for r in rows) == len(models)
    # Give explicit component witnesses instead of misusing three-variable enumeration.
    h_witness = {abs(l): False for c in hpart for l in c}
    assert all(any((l > 0 and h_witness[abs(l)]) or (l < 0 and not h_witness[abs(l)]) for l in c) for c in hpart)
    # E witness: x=0; y determined; t=0.
    e_assignment = {i: False for i in range(1, nv + 1)}
    for j, c in enumerate(clauses):
        for k, lit in enumerate(c):
            y = 4 + 3*j + k
            e_assignment[y] = bool(lit > 0)  # falsity of literal at x=0
    assert all(any((l > 0 and e_assignment[abs(l)]) or (l < 0 and not e_assignment[abs(l)]) for l in c) for c in epart)
    return {
        "name": name,
        "n": 3, "m": len(clauses), "clauses": [list(c) for c in clauses],
        "models": ["".join(map(str, a)) for a in models],
        "component_labels": {"H": "SAT", "E": "SAT", "H_and_E": "SAT" if models else "UNSAT"},
        "mixed_counts": {"variables": nv, "clauses": len(mix), "H_clauses": len(hpart),
                         "E_clauses": len(epart), "sat_extensions": len(models) * (1 << (3*len(clauses)))},
        "occurrence_targets": occurrence,
        "pair_extreme_matrices": pairs,
        "endpoint_flip_trail": endpoint_and_trail(clauses),
        "interface_join_rows": rows,
        "source_dpll": dpll(clauses, 3),
        "mixed_dpll": dpll(mix, nv),
        "forbidden_cubes": [{"source_clause": j + 1,
                              "assignment": "".join(str(int(l < 0)) for l in c),
                              "proof": "the indexed original clause is false on exactly this complete cube"}
                             for j, c in enumerate(clauses)],
    }


def flmv_envelope(c):
    """Exact Theorem 5.7 envelope with a certified infinite-tail stop."""
    f, best, rows = Fraction(1), Fraction(0), []
    for k in range(1, 1000):
        f = c * f / (1 + f)
        arithmetic = (1 / f - c) / k
        cap = c ** (-k)
        d = min(arithmetic, cap)
        rows.append((k, f, arithmetic, cap, d))
        best = max(best, d)
        if best > 0 and c ** (-(k + 1)) < best:
            return best, [r[0] for r in rows if r[4] == best], k, c ** (-(k + 1))
    raise AssertionError("tail certificate not reached")


def main():
    sat = source_audit("equal_size_unique_101_SAT", SAT)
    unsat = source_audit("equal_size_all8_UNSAT", UNSAT)
    assert sat["models"] == ["101"]
    assert unsat["models"] == []
    assert sat["m"] == unsat["m"] == 8
    assert sat["mixed_counts"]["variables"] == unsat["mixed_counts"]["variables"] == 51
    assert sat["mixed_counts"]["clauses"] == unsat["mixed_counts"]["clauses"] == 104
    assert sat["component_labels"]["H"] == unsat["component_labels"]["H"] == "SAT"
    assert sat["component_labels"]["E"] == unsat["component_labels"]["E"] == "SAT"
    assert sat["source_dpll"]["sat"] and not unsat["source_dpll"]["sat"]
    assert sat["mixed_dpll"]["sat"] and not unsat["mixed_dpll"]["sat"]
    flmv = []
    for c in (Fraction(6, 5), Fraction(241, 200), Fraction(7, 5),
              Fraction(3, 2), Fraction(8, 5)):
        d, ks, last, tail = flmv_envelope(c)
        flmv.append({"c": str(c), "d_star": str(d), "maximizing_k": ks,
                     "explicit_through_k": last, "remaining_tail_cap": str(tail),
                     "tail_strictly_below_best": tail < d})
    assert flmv[0]["d_star"] == "23/45"
    assert flmv[1]["d_star"] == "11642479/23232400"
    result = {
        "run": "MIXED-COMPATIBILITY-REFEREE241",
        "timestamp_pdt": "2026-10-31 05:48 PDT",
        "status": "PASS",
        "proof_status": "PROVED/EXACT interface lemma and restricted reduction referee; COMPUTATIONAL finite controls; universal ARC and P versus NP OPEN",
        "enumeration": "exhaustive over all 2^3 original assignments; exact complete UP-DPLL on both source and mixed formulas",
        "seed": None,
        "falsified_rule": "SAT(H) and SAT(E) imply SAT(H and E)",
        "scope_guard": "does not lower-bound controllers that inspect the source or compute the shared-interface join",
        "sources": [sat, unsat],
        "charged_join_controller": {
            "scan_original_clauses": 16,
            "component_solver_calls": 4,
            "coherent_interface_rows_examined": 16,
            "witness_or_coverage_checks": 16,
            "note": "finite exact counterexample accounting only; not native FLMV transitions"
        },
        "independent_flmv_envelope": flmv,
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
