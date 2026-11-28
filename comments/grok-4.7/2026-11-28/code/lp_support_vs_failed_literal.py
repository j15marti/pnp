#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 (KST): weighted positive-support rule on pure CNF
vs failed-literal probing (Blair-Jeroslow-Lowe 1986: LP relaxation of a clause
set is infeasible iff unit resolution refutes it).

Checks, on random 3-CNF (n=40, m=184, the RANDOM-3CNF-40 shape) and small
controls:
  (1) for every literal w: LP(F, w=1) infeasible  <=>  UP(F & w) conflicts;
  (2) iterated failed-literal closure size (what the weighted-support rule can
      at most acquire on such charts);
  (3) contrast: PHP(3->2) with pairwise AMO is LP-feasible and UP-stable at
      root, but adding the clique (exact-one-style) inequalities makes the LP
      infeasible -> the exact-one lanes use integer rounding, not LP;
  (4) spot-check of T3 a_k=(2^k+2(-1)^k)/3 by enumeration.
Deterministic seeds; scipy HiGHS LP.
"""
import itertools, json, random, sys
import numpy as np
from scipy.optimize import linprog

def rand3cnf(n, m, rng):
    F = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        F.append(tuple(v if rng.random() < .5 else -v for v in vs))
    return F

def up(F, assign):
    """assign: dict var->bool. returns (conflict, assign')"""
    a = dict(assign)
    changed = True
    while changed:
        changed = False
        for C in F:
            unk = []; sat = False
            for l in C:
                v = abs(l)
                if v in a:
                    if a[v] == (l > 0): sat = True; break
                else: unk.append(l)
            if sat: continue
            if not unk: return True, a
            if len(unk) == 1:
                l = unk[0]; a[abs(l)] = l > 0; changed = True
    return False, a

def lp_feasible(F, n, fixed, extra_le=()):
    """clause sum_{l in C} lit >= 1, lit(x)=x or 1-x; 0<=x<=1; fixed vars.
    extra_le: list of (vars, rhs) meaning sum x_v <= rhs."""
    A = []; b = []
    for C in F:
        row = np.zeros(n); const = 0
        for l in C:
            if l > 0: row[l - 1] += 1
            else: row[-l - 1] -= 1; const += 1
        # row.x + const >= 1  ->  -row.x <= const-1
        A.append(-row); b.append(const - 1)
    for vs, r in extra_le:
        row = np.zeros(n)
        for v in vs: row[v - 1] = 1
        A.append(row); b.append(r)
    bounds = [(0, 1)] * n
    for v, val in fixed.items():
        bounds[v - 1] = (1, 1) if val else (0, 0)
    res = linprog(np.zeros(n), A_ub=np.array(A), b_ub=np.array(b),
                  bounds=bounds, method="highs")
    return res.status == 0

def failed_literal_closure(F, n):
    a = {}; units = []; rounds = 0; probes = 0
    while True:
        rounds += 1; new = False
        c, a = up(F, a)
        if c: return {"refuted": True, "units": units, "probes": probes}
        for v in range(1, n + 1):
            if v in a: continue
            for val in (True, False):
                probes += 1
                c, _ = up(F, {**a, v: val})
                if c:
                    a[v] = not val; units.append(-v if val else v); new = True
                    c2, a = up(F, a)
                    if c2: return {"refuted": True, "units": units, "probes": probes}
                    break
        if not new: return {"refuted": False, "units": units, "probes": probes,
                            "assigned_after_closure": len(a)}

def pair_probe_closure(F, n, max_rounds=50):
    """Learn binary clauses (-l1 v -l2) whenever UP(F & l1 & l2) conflicts,
    then rerun single failed-literal closure on F + learned binaries.
    Counts UP calls (each is an O(|F|)-pass routine)."""
    G = list(F); learned = []; calls = 0
    lits = [v for v in range(1, n + 1)] + [-v for v in range(1, n + 1)]
    for r in range(max_rounds):
        new = 0
        Gs = set(tuple(sorted(C)) for C in G)
        for l1, l2 in itertools.combinations(lits, 2):
            if abs(l1) == abs(l2): continue
            cl = tuple(sorted((-l1, -l2)))
            if cl in Gs: continue
            calls += 1
            c, _ = up(G, {abs(l1): l1 > 0, abs(l2): l2 > 0})
            if c:
                G.append(cl); Gs.add(cl); learned.append(cl); new += 1
        fl = failed_literal_closure(G, n)
        if fl["refuted"] or new == 0:
            return {"rounds": r + 1, "learned_binaries": len(learned),
                    "up_calls": calls, "final_failed_literal": fl}
    return {"rounds": max_rounds, "learned_binaries": len(learned),
            "up_calls": calls, "final_failed_literal": fl, "capped": True}

def dpll(F, a=None):
    c, a = up(F, a or {})
    if c: return None
    vs = {abs(l) for C in F for l in C} - set(a)
    if not vs: return a
    # branch on most frequent unassigned var
    cnt = {}
    for C in F:
        if any(abs(l) in a and a[abs(l)] == (l > 0) for l in C): continue
        for l in C:
            if abs(l) not in a: cnt[abs(l)] = cnt.get(abs(l), 0) + 1
    v = max(cnt, key=cnt.get) if cnt else min(vs)
    for val in (True, False):
        r = dpll(F, {**a, v: val})
        if r is not None: return r
    return None

def experiment(seed, n=40, m=184):
    rng = random.Random(seed)
    F = rand3cnf(n, m, rng)
    agree = disagree = up_conf = 0
    for v in range(1, n + 1):
        for val in (True, False):
            c, _ = up(F, {v: val})
            lpok = lp_feasible(F, n, {v: val})
            if c == (not lpok): agree += 1
            else: disagree += 1
            up_conf += c
    root_c, _ = up(F, {})
    model = dpll(F)
    ppc = pair_probe_closure(F, n)
    return {"seed": seed, "n": n, "m": m, "root_up_conflict": root_c,
            "root_lp_feasible": lp_feasible(F, n, {}),
            "literal_probes": 2 * n, "agree": agree, "disagree": disagree,
            "failed_literals_at_root": up_conf,
            "failed_literal_closure": failed_literal_closure(F, n),
            "pair_probe_closure": ppc,
            "dpll_status": "SAT" if model is not None else "UNSAT",
            "soundness_vs_model": (None if model is None else
                not ppc["final_failed_literal"]["refuted"])}

def php32():
    # x[p][h], p in 0..2, h in 0..1 -> var 1+2p+h
    var = lambda p, h: 1 + 2 * p + h
    F = [(var(p, 0), var(p, 1)) for p in range(3)]
    for h in range(2):
        for p, q in itertools.combinations(range(3), 2):
            F.append((-var(p, h), -var(q, h)))
    n = 6
    c, _ = up(F, {})
    clique = [([var(p, h) for p in range(3)], 1) for h in range(2)]
    fl = failed_literal_closure(F, n)
    return {"clauses": len(F), "root_up_conflict": c,
            "lp_pairwise_feasible": lp_feasible(F, n, {}),
            "lp_with_clique_cuts_feasible": lp_feasible(F, n, {}, clique),
            "failed_literal_closure": fl}

def php(m):
    """PHP(m+1 -> m), pairwise AMO per hole; var(p,h)=1+m*p+h."""
    var = lambda p, h: 1 + m * p + h
    F = [tuple(var(p, h) for h in range(m)) for p in range(m + 1)]
    for h in range(m):
        for p, q in itertools.combinations(range(m + 1), 2):
            F.append((-var(p, h), -var(q, h)))
    n = m * (m + 1)
    clique = [([var(p, h) for p in range(m + 1)], 1) for h in range(m)]
    fl = failed_literal_closure(F, n)
    out = {"m": m, "vars": n, "clauses": len(F),
           "root_up_conflict": up(F, {})[0],
           "lp_pairwise_feasible": lp_feasible(F, n, {}),
           "lp_with_clique_cuts_feasible": lp_feasible(F, n, {}, clique),
           "failed_literal_refutes": fl["refuted"],
           "failed_literal_units": len(fl["units"])}
    if m <= 4:
        pp = pair_probe_closure(F, n)
        out["pair_probe_refutes"] = pp["final_failed_literal"]["refuted"]
        out["pair_probe_learned"] = pp["learned_binaries"]
    return out

def ak_check(K=10):
    out = []
    for k in range(K + 1):
        cnt = sum(1 for s in itertools.product((1, -1), repeat=k) if sum(s) % 3 == 0)
        out.append({"k": k, "enum": cnt, "formula": (2 ** k + 2 * (-1) ** k) // 3,
                    "ok": cnt == (2 ** k + 2 * (-1) ** k) // 3})
    return out

if __name__ == "__main__":
    seeds = list(range(20261128, 20261128 + 12))
    res = {"random3cnf": [experiment(s) for s in seeds],
           "random3cnf_dense_n30_m180": [experiment(s, 30, 180) for s in seeds[:6]],
           "php32_pairwise_vs_clique": php32(),
           "php_family": [php(m) for m in range(2, 7)], "T3_ak_check": ak_check()}
    tot = sum(r["agree"] + r["disagree"] for r in res["random3cnf"] + res["random3cnf_dense_n30_m180"])
    dis = sum(r["disagree"] for r in res["random3cnf"] + res["random3cnf_dense_n30_m180"])
    res["summary"] = {"total_literal_probes": tot, "lp_up_disagreements": dis}
    json.dump(res, sys.stdout, indent=1)
