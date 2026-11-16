#!/usr/bin/env python3
"""TMR-5/058 worst-case derivation-cost bridge red team: exact finite controls.

Revision tmr5-worstcase-bridge058.v1. Deterministic, exhaustive, no random seed.
For strict 3-CNF Tseitin (odd charge, 3-regular graphs) and PHP^{m+1}_m:
  (1) exact minimum tree-like resolution refutation size via minimum
      decision-tree leaves of the falsified-clause search problem
      (L(F)=1 if empty clause in F, else min_x L(F|x=0)+L(F|x=1));
      size in clauses of an optimal regular tree-like refutation = 2L-1;
  (2) an explicit, independently checked GF(2) linear refutation of Tseitin;
  (3) an explicit, independently checked cutting-planes refutation of PHP
      (Cook-Coullard-Turan style rounding), with exact line count.
COMPUTATIONAL only: finite sizes, no asymptotic claim. General (DAG)
resolution minimum size is NOT computed.
"""
import json, sys, time, itertools
from functools import lru_cache
from fractions import Fraction

REV = "tmr5-worstcase-bridge058.v1"

def simplify(clauses, var, val):
    out = []
    for c in clauses:
        if (var if val else -var) in c:
            continue
        out.append(frozenset(l for l in c if abs(l) != var))
    return frozenset(out)

def min_tree_leaves(clauses):
    @lru_cache(maxsize=None)
    def L(F):
        if frozenset() in F:
            return 1
        if not F:
            raise ValueError("satisfiable branch reached: formula is SAT")
        vs = sorted({abs(l) for c in F for l in c})
        best = None
        for v in vs:
            a = L(simplify(F, v, 0))
            if best is not None and a >= best:
                continue
            b = L(simplify(F, v, 1))
            if best is None or a + b < best:
                best = a + b
        return best
    r = L(frozenset(frozenset(c) for c in clauses))
    return r, L.cache_info().currsize

def tseitin(edges, nverts, charge):
    var = {e: i + 1 for i, e in enumerate(edges)}
    clauses, rows = [], []
    for v in range(nverts):
        inc = [var[e] for e in edges if v in e]
        for bits in itertools.product([0, 1], repeat=len(inc)):
            if sum(bits) % 2 != charge[v]:  # forbid this local assignment
                clauses.append([(-x if b else x) for x, b in zip(inc, bits)])
        rows.append((frozenset(inc), charge[v]))
    return clauses, rows, len(edges)

def brute_unsat(clauses, n):
    for a in itertools.product([0, 1], repeat=n):
        if all(any((a[abs(l) - 1] == 1) == (l > 0) for l in c) for c in clauses):
            return False
    return True

def gf2_refute(rows):
    """Sum all vertex parity rows: each edge appears twice -> 0 = sum charges.
    Returns number of row additions and checks the derivation."""
    acc, rhs, adds, maxw = frozenset(), 0, 0, 0
    for i, (s, b) in enumerate(rows):
        acc = acc ^ s if i else s
        rhs ^= b
        adds += 1 if i else 0
        maxw = max(maxw, len(acc))
    assert acc == frozenset() and rhs == 1, "not a refutation"
    return adds, maxw

def php(m):
    var = {}
    for i in range(m + 1):
        for j in range(m):
            var[(i, j)] = len(var) + 1
    cl = [[var[(i, j)] for j in range(m)] for i in range(m + 1)]
    for j in range(m):
        for i, k in itertools.combinations(range(m + 1), 2):
            cl.append([-var[(i, j)], -var[(k, j)]])
    return cl, var

def cp_php_refutation(m, var):
    """Lines are (coef dict, rhs) meaning sum coef*x >= rhs over 0/1 vars
    with axioms 0<=x<=1. Every line is checked as a valid CP step."""
    lines = 0
    def add(a, b):
        d = dict(a[0])
        for k, v in b[0].items():
            d[k] = d.get(k, 0) + v
        return ({k: v for k, v in d.items() if v}, a[1] + b[1])
    def scale(a, c):
        return ({k: v * c for k, v in a[0].items()}, a[1] * c)
    def divide(a, c):
        assert all(v % c == 0 for v in a[0].values())
        return ({k: v // c for k, v in a[0].items()}, -((-a[1]) // c))  # ceil
    total = ({}, 0)
    for j in range(m):
        # hole j: derive -sum_{i<=k} x_ij >= -1 inductively
        h = ({var[(0, j)]: -1}, -1)  # from axiom x<=1
        lines += 1
        for k in range(1, m + 1):
            acc = scale(h, k - 1) if k > 1 else ({}, 0)
            for i in range(k):
                acc = add(acc, ({var[(i, j)]: -1, var[(k, j)]: -1}, -1))  # clause axiom
                lines += 1
            if k == 1:
                h = acc
            else:
                h = divide(acc, k)
                lines += 2
            assert h == ({var[(i, j)]: -1 for i in range(k + 1)}, -1), (j, k, h)
        total = add(total, h)
        lines += 1
    for i in range(m + 1):
        total = add(total, ({var[(i, j)]: 1 for j in range(m)}, 1))
        lines += 1
    assert total[0] == {} and total[1] == 1, total  # 0 >= 1
    return lines

def main():
    t0 = time.time()
    res = {"revision": REV, "mode": "exhaustive deterministic", "python": sys.version.split()[0],
           "tseitin": [], "php": []}
    graphs = {
        "K4": ([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], 4),
        "K33": ([(a, b) for a in range(3) for b in range(3, 6)], 6),
        "prism": ([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)], 6),
        "Q3": ([(a, a ^ (1 << t)) for a in range(8) for t in range(3) if a < a ^ (1 << t)], 8),
    }
    for name, (E, nv) in graphs.items():
        ch = [1] + [0] * (nv - 1)
        cl, rows, n = tseitin(E, nv, ch)
        assert all(len(c) == 3 for c in cl)
        uns = brute_unsat(cl, n)
        Lv, states = min_tree_leaves(cl)
        adds, maxw = gf2_refute(rows)
        res["tseitin"].append({"graph": name, "vars": n, "clauses": len(cl), "strict3": True,
            "brute_unsat": uns, "min_treelike_leaves": Lv, "min_treelike_size": 2 * Lv - 1,
            "memo_states": states, "gf2_row_additions": adds, "gf2_max_row_weight": maxw})
    for m in range(1, 4):
        cl, var = php(m)
        uns = brute_unsat(cl, len(var))
        Lv, states = min_tree_leaves(cl)
        cp = cp_php_refutation(m, var)
        res["php"].append({"m": m, "vars": len(var), "clauses": len(cl), "brute_unsat": uns,
            "min_treelike_leaves": Lv, "min_treelike_size": 2 * Lv - 1, "memo_states": states,
            "cp_lines_checked": cp})
    for m in range(4, 9):  # CP only (tree-like DP too large)
        cl, var = php(m)
        res["php"].append({"m": m, "vars": len(var), "clauses": len(cl),
                           "cp_lines_checked": cp_php_refutation(m, var)})
    # control: satisfiable even-charge Tseitin must be rejected by the DP
    cl, rows, n = tseitin(graphs["K4"][0], 4, [0, 0, 0, 0])
    try:
        min_tree_leaves(cl); ok = False
    except ValueError:
        ok = True
    res["control_even_K4_SAT_rejected"] = ok and not brute_unsat(cl, n)
    assert res["control_even_K4_SAT_rejected"]
    res["all_unsat_verified"] = all(r.get("brute_unsat", True) for r in res["tseitin"] + res["php"])
    assert res["all_unsat_verified"]
    res["seconds"] = round(time.time() - t0, 2)
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
