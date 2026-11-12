#!/usr/bin/env python3
"""LSPV-5/506 red team: exact (W, slot-area, byte-area) frontier WITH arbitrary
recomputation, on the paid-RES DAG of an accepted native-/386 packet.

Model (identical to LSPV-4/562-563 post-step convention, re-implemented
independently from the packet bytes, not from LSPV-4's PARENTS table):
  * SOURCE/DEF are read-only and free; only paid RES outputs occupy registers.
  * One step executes RES j whose paid parents are resident; any subset `keep`
    of the old residents survives (deletion free); peak = |keep U P_j| + 1 must be
    <= cap, or = cap+1 if j overwrites a parent p not kept with bytes(p)>=bytes(j).
  * post-step residents = keep U {j}; slot-area += |post|, byte-area += bytes(post).
  * Goal: the empty clause is produced. Every RES then has been executed >=1 time.
Exact layered search over the number of executions; layer w holds the minimum
area for each resident set. Run: python3 <this> <packet.json> <cap> <Wmax> <slot|byte>
"""
import json, sys, time
from itertools import combinations

def dag(path):
    R = json.load(open(path))["records"]
    res = [i for i, r in enumerate(R) if r["kind"] == "RES"]
    idx = {g: k for k, g in enumerate(res)}
    par = [sorted({idx[p] for p in R[g]["parents"] if p in idx}) for g in res]
    size = [len(json.dumps(R[g]["c"], separators=(",", ":"))) for g in res]
    return par, size

def subsets(bits):
    xs = [1 << i for i in range(64) if bits >> i & 1]
    out = []
    for k in range(len(xs) + 1):
        for c in combinations(xs, k):
            out.append(sum(c))
    return out

def frontier(par, size, cap, wmax, obj):
    n = len(par); sink = n - 1
    assert all(p < j for j in range(n) for p in par[j])
    pm = [sum(1 << p for p in ps) for ps in par]
    pop = lambda m: bin(m).count("1")
    byt = lambda m: sum(size[i] for i in range(n) if m >> i & 1)
    cost = (lambda m: (pop(m), byt(m))) if obj == "slot" else (lambda m: (byt(m), pop(m)))
    layer = {0: (0, 0)}; back = []; best = {}
    for w in range(1, wmax + 1):
        nxt = {}; bk = {}
        for S, c in layer.items():
            for j in range(n):
                if pm[j] & ~S:
                    continue
                for keep in subsets(S):
                    if keep >> j & 1:
                        continue
                    peak = pop(keep | pm[j]) + 1
                    if peak > cap:
                        if peak > cap + 1 or not any(
                                not keep >> p & 1 and size[p] >= size[j] for p in par[j]):
                            continue
                    post = keep | (1 << j)
                    d = cost(post); nc = (c[0] + d[0], c[1] + d[1])
                    if post not in nxt or nc < nxt[post]:
                        nxt[post] = nc; bk[post] = (S, j)
        back.append(bk); layer = nxt
        hits = [(c, S) for S, c in nxt.items() if S >> sink & 1]
        if hits:
            c, S = min(hits)
            tr = []; cur = S
            for b in reversed(back):
                prev, j = b[cur]; tr.append((j, cur)); cur = prev
            tr.reverse()
            best[w] = {"primary_secondary": list(c), "trace": [j for j, _ in tr],
                       "residents": [[i for i in range(n) if m >> i & 1] for _, m in tr]}
    return best

if __name__ == "__main__":
    path, cap, wmax, obj = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    t = time.time(); par, size = dag(path)
    b = frontier(par, size, cap, wmax, obj)
    print(json.dumps({"packet": path, "paid_res_nodes": len(par), "cap": cap, "objective": obj,
                      "seconds": round(time.time() - t, 2),
                      "frontier": {w: v["primary_secondary"] for w, v in b.items()},
                      "witness": b}))
