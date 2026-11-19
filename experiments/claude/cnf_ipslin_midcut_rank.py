"""Exact middle-cut rank (mod p lower bound + float cross-check) of the sorted first-falsified
IPS_LIN' certificate, natural order, ratio 6, n in {16,...,24}; cuts k=n/2-1..n/2+1.
Reuses cnf_ipslin_roabp_width.py (same instance generator and seeds). Usage: python3 -I this.py OUT.json"""
import json, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cnf_ipslin_roabp_width as W
out = {"meta": {"python": sys.version.split()[0], "numpy": np.__version__, "ratio": 6.0}, "rows": []}; t0 = time.time()
for n in [16, 18, 20, 22, 24]:
    for seed in range(4):
        m = int(round(6.0 * n)); rng = np.random.default_rng(10_000 * n + seed); cl = W.random_cnf(n, m, rng)
        order = list(range(n)); cc = sorted(cl, key=lambda c: max(v for v, _ in c))
        J = W.first_falsified(n, cc, order)
        if (J < 0).any():
            out["rows"].append({"n": n, "seed": seed, "sat": True, "solutions": int((J < 0).sum())}); print(n, seed, 'SAT skipped', flush=True); continue
        ks = [n // 2] if n >= 24 else [n // 2 - 1, n // 2, n // 2 + 1]
        res = [[k, *W.cut_rank(J, n, k, m)] for k in ks]
        row = {"n": n, "m": m, "seed": seed, "cuts[k,distinct,rank_p,rank_float]": res, "two_pow_half_n": 2 ** (n // 2)}
        out["rows"].append(row); print(row, f"{time.time()-t0:.1f}s", flush=True)
        del J
out["meta"]["seconds"] = round(time.time() - t0, 2); json.dump(out, open(sys.argv[1], "w"), indent=1)
