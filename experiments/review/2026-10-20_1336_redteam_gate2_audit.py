"""Red-team audit of ARC_HISTORY_INPUT_GATE2 (runtime << 30s).
(1) Exact crossover of the Shannon counting floor vs sqrt(N), explicit basis constants.
(2) Contraction recurrence t'<=max(1.1,e,0.6+g+t/2): iteration counts and robustness to g>0.
"""
import math, json
from fractions import Fraction

def log2_circuits(s, n):
    # fan-in-2, all 16 binary gate types, inputs from s-1 earlier gates + n index bits + 2 constants,
    # one designated output among s gates: log2 of number of descriptions (upper bound)
    m = s + n + 2
    return s * (4 + 2 * math.log2(m)) + math.log2(s)

def smin(N):
    n = max(1, math.ceil(math.log2(N)))
    lo, hi = 1, N
    while lo < hi:
        mid = (lo + hi) // 2
        if log2_circuits(mid, n) >= N: hi = mid
        else: lo = mid + 1
    return lo  # any s' < lo has fewer than 2^N descriptions => some x needs >= lo gates

rows = []
cross = None
for e in range(4, 41):
    N = 2 ** e
    s = smin(N)
    r = s / math.sqrt(N)
    rows.append((N, s, round(r, 3), round(s * math.log2(N) / N, 3)))
    if cross is None and s > math.sqrt(N): cross = N
# finer crossover scan
fine = None
for N in range(16, 200000):
    if smin(N) > math.sqrt(N): fine = N; break

# recurrence
def iterate(t0, e=1.1, g=0.0, eps=0.0, steps=60):
    t = t0; out = []
    for j in range(steps):
        t = max(1.1, e, 0.6 + g + t / 2 + eps)
        out.append(t)
    return out
rec = {}
for g in (0.0, 0.01, 0.05, 0.1, 0.2, 0.3):
    seq = iterate(3.0, g=g)
    rec[str(g)] = {"limit": round(seq[-1], 6), "fixed_point": round(max(1.1, 2 * (0.6 + g)), 6)}
# per-level poly-log/ constant overhead eps: fixed point shifts to 2*(0.6+eps)
rec_eps = {str(eps): round(iterate(3.0, eps=eps)[-1], 6) for eps in (0.0, 0.01, 0.05)}
# levels needed from t0=3 to within 0.01 of limit 1.2
levels = next(j for j, t in enumerate(iterate(3.0)) if t <= 1.21) + 1
# depth needed for child size to reach constant: N^(2^-j) <= 2 needs j >= log2 log2 N
depth_const = {str(e): math.ceil(math.log2(e)) for e in (10, 20, 40, 100, 1000)}
# the contraction multiplies calls: total N^{0.6} per level, but q-product across levels
# (q_j children of size N^{2^-j}) -- check geometric sum is dominated by top level
tot = {}
for j in range(1, 8):
    # level j: number of nodes = prod_{i<=j} N^{0.6*2^{-(i-1)}} -> exponent 0.6*(2-2^{1-j}); each of size exponent 2^{-j}; work exponent per node  t=1 (read) 
    nodes = 0.6 * (2 - 2 ** (1 - j))
    tot[j] = round(nodes + 2 ** -j, 4)
res = dict(rows=rows[:6] + rows[-3:], crossover_pow2=cross, crossover_fine=fine,
           recurrence_g=rec, recurrence_eps=rec_eps, levels_to_1p21=levels, tree_total_exponents=tot,
           depth_to_constant_size=depth_const)
json.dump(res, open("results/summaries/2026-10-20_1336_redteam_gate2_audit.json", "w"), indent=1)
print(json.dumps(res, indent=1))
