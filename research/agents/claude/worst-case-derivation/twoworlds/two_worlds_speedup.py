#!/usr/bin/env python3
"""WCD-TWOWORLDS-0001: apply the checkpoint speedup to a SAT machine in each world and
test for a contradiction with the nondeterministic time hierarchy.

World A (P = NP side): SAT in DTISP[n^c, n^s], 1 <= c, 0 <= s <= c.
  Scheme k (k-1 checkpoint levels, then k-1 slowdowns), for any a >= 1:
    NTIME[n^a] <= DTISP[n^{ac}, n^{as}] <= Sigma_k TIME[n^{a(c+(k-1)s)/k}]
               <= NTIME[n^{a c^{k-1} (c+(k-1)s)/k}]
  Contradiction iff  c^(k-1) * (c + (k-1) s) < k.
World B (P != NP side): every SAT machine has time n^{c(n)} with c(n) unbounded.
  The same scheme at input scale n needs c(n)^(k-1) (c(n) + (k-1) s) < k, checked below.

Exact rational arithmetic for the grid; bisection for frontiers. Runs in about a second.
"""
import json, sys, time
from fractions import Fraction as Fr
T0 = time.time()
KS = range(2, 13)

def contradicted(c, s, k): return c ** (k - 1) * (c + (k - 1) * s) < k
def any_k(c, s): return [k for k in KS if contradicted(c, s, k)]

def cmax(s, k):
    lo, hi = Fr(1), Fr(3)
    for _ in range(60):
        mid = (lo + hi) / 2
        if contradicted(mid, s, k): lo = mid
        else: hi = mid
    return float(lo)

def main():
    out = {"id": "WCD-TWOWORLDS-0001"}
    # 1. frontier of World A: largest contradicted time exponent at each space exponent
    fr = {}
    for s in [Fr(0), Fr(1, 4), Fr(1, 2), Fr(11642479, 23232400), Fr(3, 4), Fr(9, 10), Fr(99, 100)]:
        best = max(((cmax(s, k), k) for k in KS))
        fr[str(round(float(s), 4))] = {"c_max": round(best[0], 5), "best_k": best[1]}
    out["worldA_frontier_c_max_by_space"] = fr
    # 2. exact grid: where is World A contradicted?  (c, s) on a grid with s <= c
    G = 200; hit = 0; tot = 0; hit_s_ge_1 = 0; hit_c_ge = 0; diag = 0
    cap = Fr(14423, 10000)                       # just above 3^(1/3) = 1.44225
    for i in range(0, 2 * G + 1):                # c in [1, 3]
        c = 1 + Fr(i, G)
        for j in range(0, 3 * G + 1):            # s in [0, 3]
            s = Fr(j, G)
            if s > c: continue
            tot += 1
            if any_k(c, s):
                hit += 1
                if s >= 1: hit_s_ge_1 += 1
                if c >= cap: hit_c_ge += 1
                if s == c: diag += 1
    out["worldA_grid"] = {"points": tot, "contradicted": hit,
                          "contradicted_with_s_ge_1": hit_s_ge_1,
                          "contradicted_with_c_ge_1.4423": hit_c_ge,
                          "contradicted_with_s_eq_c": diag}
    # 3. corpus FLMV box corner against this naive scheme
    c0, s0 = Fr(241, 200), Fr(11642479, 23232400)
    out["corpus_box_corner"] = {"c": float(c0), "s": float(s0), "contradicted_by_naive_scheme_k": any_k(c0, s0),
        "k2_value_vs_2": float(c0 * (c0 + s0)), "k3_value_vs_3": float(c0 ** 2 * (c0 + 2 * s0))}
    # 4. World B: local exponent c(n) for sample superpolynomial bounds; scheme needs c(n) < 3^(1/3) at s = 0
    import math
    wb = {}
    for name, cfun in {"n^(log2 log2 n)": lambda L: math.log2(L), "n^(log2 n)": lambda L: L,
                       "2^(n^0.1)": lambda L: 2 ** (0.1 * L) / L}.items():
        # L = log2 n ; smallest L >= 2 from which c(n) >= 3^(1/3) for good (all are increasing past it)
        L = 2.0
        while cfun(L) < 3 ** (1 / 3) or cfun(L + 1) < 3 ** (1 / 3): L += 0.5
        wb[name] = {"log2_n_from_which_no_scheme_applies": L}
    out["worldB_no_contradiction_beyond"] = wb
    out["known_ceilings"] = {"naive_scheme_max_c": round(3 ** (1 / 3), 5), "Williams_2cos(pi/7)": round(2 * math.cos(math.pi / 7), 5)}
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()

if __name__ == "__main__": main()
