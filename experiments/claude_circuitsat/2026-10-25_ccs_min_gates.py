#!/usr/bin/env python3
"""ClaudeCircuitSAT ladder: exact minimum fan-in-2 circuit size (basis B2, free
negation absorbed in the 10 non-degenerate binary ops) for small n.
Each gate = 2 wires, so minimal wires among gates = 2*gates (+ output tap).
Chunked: n=2,3 full census; n=4 only targeted functions (depth-limited search)."""
import json, sys, time, itertools
def tt_inputs(n):
    N = 1 << n; M = (1 << N) - 1
    xs = []
    for i in range(n):
        v = 0
        for a in range(N):
            if (a >> i) & 1: v |= 1 << a
        xs.append(v)
    return xs, M
def ops(M):
    # 10 nondegenerate binary ops on (a,b) as functions of 4-bit table
    out = []
    for t in range(16):
        if t in (0, 15, 3, 12, 5, 10): continue  # const, a, ~a, b, ~b
        out.append(t)
    def ap(t, a, b):
        r = 0
        if t & 1: r |= ~a & ~b
        if t & 2: r |= a & ~b
        if t & 4: r |= ~a & b
        if t & 8: r |= a & b
        return r & M
    return out, ap
def census(n, maxg, tlimit):
    xs, M = tt_inputs(n); tl, ap = ops(M)
    level = {frozenset(xs)}; best = {}
    for x in xs: best[x] = 0; best[M ^ x] = 0  # negation free in B2 accounting
    best[0] = 0; best[M] = 0
    seen = set(level)
    t0 = time.time()
    for g in range(1, maxg + 1):
        new = set()
        for S in level:
            L = sorted(S)
            for a, b in itertools.combinations(L, 2):
                for t in tl:
                    f = ap(t, a, b)
                    if f in S: continue
                    S2 = S | {f}
                    if S2 in seen: continue
                    seen.add(S2); new.add(S2)
                    for h in (f, M ^ f):
                        if h not in best: best[h] = g
            if time.time() - t0 > tlimit: return best, g - 1, False
        level = new
        if len(best) == (1 << (1 << n)): return best, g, True
    return best, maxg, len(best) == (1 << (1 << n))
def and_n_gates(n, kmax):
    xs, M = tt_inputs(n); tl, ap = ops(M)
    target = M
    for x in xs: target &= x
    def dfs(S, k):
        if target in S or (M ^ target) in S: return True
        if k == 0: return False
        L = sorted(S)
        for a, b in itertools.combinations(L, 2):
            for t in tl:
                f = ap(t, a, b)
                if f in S: continue
                if dfs(S | {f}, k - 1): return True
        return False
    for k in range(0, kmax + 1):
        if dfs(frozenset(xs), k): return k
    return None
res = {}
for n in (2, 3):
    b, g, done = census(n, 9, 12)
    hist = {}
    for v in b.values(): hist[v] = hist.get(v, 0) + 1
    res[f"census_n{n}"] = {"gates_histogram": dict(sorted(hist.items())), "complete": done,
                           "max_gates": max(b.values()), "functions": len(b)}
    if n == 3:
        xs, M = tt_inputs(3)
        par = xs[0] ^ xs[1] ^ xs[2]
        maj = (xs[0] & xs[1]) | (xs[0] & xs[2]) | (xs[1] & xs[2])
        res["n3_parity_gates"] = b.get(par); res["n3_majority_gates"] = b.get(maj)
        res["n3_hardest"] = sorted(f for f, v in b.items() if v == max(b.values()))[:6]
res["and_n_min_gates"] = {n: and_n_gates(n, n) for n in range(1, 5)}
json.dump(res, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print(json.dumps(res, sort_keys=True))
