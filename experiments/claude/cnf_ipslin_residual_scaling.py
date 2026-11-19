"""Exact upper-bound decomposition for the sorted first-falsified certificate at the middle
x-cut k=n/2 (natural order, clauses sorted by last variable): W_k <= i_k + S_k, where
i_k = #distinct first-falsified prefix-internal clauses over prefixes, S_k = #distinct
residual sets {crossing clauses not satisfied by prefix a} over prefixes a that falsify
no internal clause. Also reports surviving prefix count. Usage: python3 -I ... OUT.json"""
import json, sys, time
import numpy as np
from importlib.util import spec_from_file_location, module_from_spec
def random_cnf(n, m, rng):
    return [[(int(a), int(b)) for a, b in zip(rng.choice(n, 3, replace=False), rng.integers(0, 2, 3))] for _ in range(m)]
out = {"meta": {"python": sys.version.split()[0], "numpy": np.__version__}, "rows": []}; t0 = time.time()
for ratio in [4.26, 6.0]:
  for n in range(16, 41, 4):
    for seed in range(3):
        m = int(round(ratio * n)); rng = np.random.default_rng(10_000 * n + seed); cl = random_cnf(n, m, rng)
        k = n // 2; N = 1 << k; idx = np.arange(N, dtype=np.int64)
        bit = lambda v: (idx >> (k - 1 - v)) & 1
        inside = [c for c in cl if max(v for v, _ in c) < k]; inside.sort(key=lambda c: max(v for v, _ in c))
        cross = [c for c in cl if min(v for v, _ in c) < k <= max(v for v, _ in c)]
        J = np.full(N, -1, dtype=np.int64)
        for j, c in enumerate(inside):
            f = np.ones(N, bool)
            for v, s in c: f &= bit(v) != s
            J[(J < 0) & f] = j
        surv = J < 0
        R = np.zeros((N, len(cross)), dtype=np.uint8)
        for t, c in enumerate(cross):
            sat = np.zeros(N, bool)
            for v, s in c:
                if v < k: sat |= bit(v) == s
            R[:, t] = ~sat
        S = int(np.unique(np.packbits(R[surv], axis=1), axis=0).shape[0]) if surv.any() else 0
        i_k = int(np.unique(J[~surv]).size)
        row = {"ratio": ratio, "n": n, "m": m, "seed": seed, "k": k, "internal": len(inside), "crossing": len(cross),
               "i_k": i_k, "surviving_prefixes": int(surv.sum()), "S_k": S, "bound": i_k + S, "two_pow_k": N}
        out["rows"].append(row); print(row, f"{time.time()-t0:.1f}s", flush=True)
out["meta"]["seconds"] = round(time.time() - t0, 2); json.dump(out, open(sys.argv[1], "w"), indent=1)
