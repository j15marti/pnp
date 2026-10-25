"""ClaudeCircuitSAT ladder: exact gate/wire minima (B2 basis, fan-in 2) for all n-input
functions, n<=3, and exact decision-tree depth of AND-of-literals Circuit-SAT, n<=4.
Each stage runs well under 30 s. Output: results/raw/claude_circuitsat/ladder_results.json"""
import itertools, json, sys, functools

def min_gates(n, cap):
    N = 1 << n
    mask = (1 << N) - 1
    ins = []
    for i in range(n):
        t = 0
        for a in range(N):
            if (a >> i) & 1: t |= 1 << a
        ins.append(t)
    ops = []
    for tt in range(16):
        ops.append(lambda x, y, tt=tt: (((tt >> 0) & 1) * (~x & ~y) | ((tt >> 1) & 1) * (x & ~y)
                                         | ((tt >> 2) & 1) * (~x & y) | ((tt >> 3) & 1) * (x & y)) & mask)
    best = {}
    for f in [0, mask] + ins + [~i & mask for i in ins]:
        best[f] = 0
    # BFS over circuits = tuples of computed functions, canonical frozenset, depth = #gates
    start = frozenset(ins)
    frontier = {start}
    seen = {start}
    for g in range(1, cap + 1):
        nxt = set()
        for S in frontier:
            L = list(S)
            for x, y in itertools.combinations(L, 2):
                for op in ops:
                    f = op(x, y)
                    if f in S: continue
                    if f not in best: best[f] = g
                    T = S | {f}
                    if T not in seen:
                        seen.add(T); nxt.add(T)
        frontier = nxt
    return best

def dt_depth(n):
    lits = [(v, s) for v in range(n) for s in (0, 1)]
    inst = list(itertools.product(range(2 * n), repeat=n))
    def sat(w):
        seen = {}
        for l in w:
            v, s = lits[l]
            if seen.setdefault(v, s) != s: return False
        return True
    val = {w: sat(w) for w in inst}
    @functools.lru_cache(None)
    def D(fixed):  # fixed: tuple of (-1 or literal idx)
        cons = [w for w in inst if all(f < 0 or w[i] == f for i, f in enumerate(fixed))]
        if len({val[w] for w in cons}) <= 1: return 0
        r = 99
        for i, f in enumerate(fixed):
            if f >= 0: continue
            m = 0
            for l in range(2 * n):
                g = list(fixed); g[i] = l
                m = max(m, D(tuple(g)))
                if m + 1 >= r: break
            r = min(r, 1 + m)
        return r
    return D(tuple([-1] * n))

out = {"min_gates": {}, "dt_depth_and_of_literals": {}}
for n, cap in ((1, 1), (2, 3), (3, 4)):
    b = min_gates(n, cap)
    hist = {}
    for f, g in b.items(): hist[g] = hist.get(g, 0) + 1
    out["min_gates"][n] = {"functions_found": len(b), "total_functions": 1 << (1 << n),
                           "histogram_by_gates": hist, "cap_explored": cap}
for n in (2, 3, 4):
    out["dt_depth_and_of_literals"][n] = dt_depth(n)
json.dump(out, open("/home/user/pnp/results/raw/claude_circuitsat/ladder_results.json", "w"), indent=1, sort_keys=True)
print(json.dumps(out, indent=1, sort_keys=True))
