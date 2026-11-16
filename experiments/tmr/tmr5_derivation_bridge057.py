#!/usr/bin/env python3
"""TMR-5/057 red-team control for the worst-case derivation-cost bridge.

Revision tmr5-derivation-bridge057.v1.  Deterministic, no randomness.
Finite COMPUTATIONAL illustration only; the asymptotic statements are the
KNOWN THEOREMS of Tseitin/Urquhart/Ben-Sasson--Wigderson cited in the report.

For each instance it computes, exactly:
  * min resolution refutation WIDTH, by width-bounded saturation
    (complete: a width<=w refutation exists iff bottom is in the width<=w
    closure, since every clause of such a refutation lies in the closure);
  * min TREE-LIKE resolution refutation size (number of nodes), via the exact
    falsified-clause decision-tree DP over partial assignments;
  * the node count of a fixed-order DPLL run, checked >= the tree-like minimum
    (the legitimate "min over derivations lower-bounds R-shaped executions");
  * for Tseitin, the exact XOR row operations of GF(2) Gaussian elimination,
    a polynomial algorithm that is NOT a resolution derivation.
Usage: python3 -I tmr5_derivation_bridge057.py OUT.json
"""
import itertools, json, sys, time
from functools import lru_cache

REV = "tmr5-derivation-bridge057.v1"

def tseitin(vertices, edges, charge):
    """edges: list of (u,v); variable i+1 is edge i. charge: dict v->0/1."""
    clauses = []
    rows = []
    for v in vertices:
        inc = [i + 1 for i, e in enumerate(edges) if v in e]
        rows.append((inc, charge[v]))
        for bits in itertools.product([0, 1], repeat=len(inc)):
            if sum(bits) % 2 != charge[v]:  # forbid this local assignment
                clauses.append(tuple(-x if b else x for x, b in zip(inc, bits)))
    return clauses, rows

def php(p, h):
    var = lambda i, j: i * h + j + 1
    cl = [tuple(var(i, j) for j in range(h)) for i in range(p)]
    for j in range(h):
        for a, b in itertools.combinations(range(p), 2):
            cl.append((-var(a, j), -var(b, j)))
    return cl

def to_mask(cl):
    pos = neg = 0
    for l in cl:
        if l > 0: pos |= 1 << l
        else: neg |= 1 << -l
    return (pos, neg)

def popc(x): return bin(x).count("1")

def min_width(clauses, nvars, wmax, budget):
    init = {to_mask(c) for c in clauses}
    w0 = max(popc(p) + popc(n) for p, n in init)
    out = {"initial_width": w0, "tested": []}
    for w in range(w0, wmax + 1):
        t0 = time.time()
        S = set(init); frontier = list(S); found = False; aborted = False
        bylit = {}
        def add_index(c):
            p, n = c
            for v in range(1, nvars + 1):
                if p >> v & 1: bylit.setdefault((v, 1), []).append(c)
                if n >> v & 1: bylit.setdefault((v, 0), []).append(c)
        for c in S: add_index(c)
        steps = 0
        while frontier and not found:
            c = frontier.pop(); p, n = c
            for v in range(1, nvars + 1):
                for sgn, other in ((1, 0), (0, 1)):
                    if not ((p if sgn else n) >> v & 1): continue
                    for d in list(bylit.get((v, other), [])):
                        steps += 1
                        rp = (p | d[0]) & ~(1 << v); rn = (n | d[1]) & ~(1 << v)
                        if rp & rn: continue
                        if popc(rp) + popc(rn) > w: continue
                        r = (rp, rn)
                        if r in S: continue
                        S.add(r); add_index(r); frontier.append(r)
                        if r == (0, 0): found = True; break
                    if found: break
                if found: break
            if time.time() - t0 > budget: aborted = True; break
        out["tested"].append({"w": w, "refuted": found, "aborted": aborted,
                              "closure_clauses": len(S), "resolution_attempts": steps,
                              "seconds": round(time.time() - t0, 3)})
        if found: out["min_width"] = w; return out
        if aborted: out["min_width"] = None; out["lower_bound_width"] = w; return out
    out["min_width"] = None; out["lower_bound_width"] = wmax + 1
    return out

def min_treelike(clauses, nvars):
    masks = [to_mask(c) for c in clauses]
    sys.setrecursionlimit(10000)
    @lru_cache(maxsize=None)
    def f(t, fa):  # t: vars set true, fa: vars set false
        for p, n in masks:
            if (p & ~fa) == 0 and (n & ~t) == 0:
                return 1  # leaf: some initial clause falsified
        assigned = t | fa; best = None
        for v in range(1, nvars + 1):
            if assigned >> v & 1: continue
            s = 1 + f(t | 1 << v, fa) + f(t, fa | 1 << v)
            if best is None or s < best: best = s
        return best
    r = f(0, 0)
    return r, f.cache_info().currsize

def dpll_nodes(clauses, nvars):
    """Fixed order x1,x2,... no propagation; returns tree size; its tree IS a
    tree-like resolution refutation shape (for UNSAT input)."""
    masks = [to_mask(c) for c in clauses]
    def rec(t, fa, v):
        for p, n in masks:
            if (p & ~fa) == 0 and (n & ~t) == 0: return 1
        if v > nvars: raise AssertionError("satisfying assignment: not UNSAT")
        return 1 + rec(t | 1 << v, fa, v + 1) + rec(t, fa | 1 << v, v + 1)
    return rec(0, 0, 1)

def gauss_gf2(rows, nvars):
    eqs = []
    for inc, b in rows:
        m = 0
        for x in inc: m |= 1 << x
        eqs.append([m, b])
    ops = 0; r = 0
    for v in range(1, nvars + 1):
        piv = next((i for i in range(r, len(eqs)) if eqs[i][0] >> v & 1), None)
        if piv is None: continue
        eqs[r], eqs[piv] = eqs[piv], eqs[r]
        for i in range(len(eqs)):
            if i != r and eqs[i][0] >> v & 1:
                eqs[i][0] ^= eqs[r][0]; eqs[i][1] ^= eqs[r][1]; ops += 1
        r += 1
    inconsistent = any(m == 0 and b == 1 for m, b in eqs)
    return inconsistent, ops

def brute_unsat(clauses, nvars):
    masks = [to_mask(c) for c in clauses]
    for a in range(1 << nvars):
        t = a << 1; fa = ((1 << (nvars + 1)) - 2) & ~t
        if all((p & t) or (n & fa) for p, n in masks): return False
    return True

def graphs():
    G = {}
    G["K4"] = (list(range(4)), list(itertools.combinations(range(4), 2)))
    G["K33"] = (list(range(6)), [(a, b) for a in range(3) for b in range(3, 6)])
    G["prism"] = (list(range(6)), [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)])
    G["cube_Q3"] = (list(range(8)), [(a, b) for a in range(8) for b in range(a+1, 8) if bin(a ^ b).count("1") == 1])
    return G

def main(outpath):
    res = {"revision": REV, "seed": None, "instances": [], "assertions": 0}
    A = 0
    budget = 8.0
    for name, (V, E) in graphs().items():
        charge = {v: (1 if v == V[0] else 0) for v in V}  # odd total charge => UNSAT
        cl, rows = tseitin(V, E, charge)
        nv = len(E)
        unsat = brute_unsat(cl, nv); assert unsat; A += 1
        incons, ops = gauss_gf2(rows, nv); assert incons; A += 1
        rec = {"family": "tseitin_odd", "graph": name, "vars": nv, "clauses": len(cl),
               "brute_unsat": unsat, "gf2_inconsistent": incons, "gf2_row_xor_ops": ops}
        rec["width"] = min_width(cl, nv, 8, budget)
        if nv <= 12:
            t0 = time.time(); tl, states = min_treelike(cl, nv)
            rec["min_treelike_size"] = tl; rec["treelike_dp_states"] = states
            rec["treelike_seconds"] = round(time.time() - t0, 3)
            d = dpll_nodes(cl, nv); rec["fixed_order_dpll_nodes"] = d
            assert d >= tl; A += 1
        res["instances"].append(rec); print(name, rec["width"].get("min_width"), rec.get("min_treelike_size"), ops, flush=True)
    for p in (3, 4):
        h = p - 1; cl = php(p, h); nv = p * h
        assert brute_unsat(cl, nv); A += 1
        rec = {"family": "php", "pigeons": p, "holes": h, "vars": nv, "clauses": len(cl)}
        rec["width"] = min_width(cl, nv, 8, budget)
        t0 = time.time(); tl, states = min_treelike(cl, nv)
        rec["min_treelike_size"] = tl; rec["treelike_dp_states"] = states
        d = dpll_nodes(cl, nv); rec["fixed_order_dpll_nodes"] = d; assert d >= tl; A += 1
        rec["counting_decider_ops"] = p + h  # compare #pigeons > #holes from the header
        res["instances"].append(rec); print("php", p, rec["width"].get("min_width"), tl, flush=True)
    # soundness control: a SAT Tseitin (even charge) must NOT be refuted
    V, E = graphs()["K4"]; cl, rows = tseitin(V, E, {v: 0 for v in V})
    assert not brute_unsat(cl, len(E)); A += 1
    assert not gauss_gf2(rows, len(E))[0]; A += 1
    w = min_width(cl, len(E), 6, budget); assert w["min_width"] is None; A += 1
    res["sat_control_K4_even"] = {"refuted": False, "width_probe": w}
    res["assertions"] = A
    with open(outpath, "w") as f: json.dump(res, f, indent=1, sort_keys=True)
    print("assertions", A, "failures 0")

if __name__ == "__main__":
    main(sys.argv[1])
