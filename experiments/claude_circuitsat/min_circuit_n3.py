"""Exact minimum B2 circuit size C(f) for all 3-variable Boolean functions (truth tables 0..255).
Method: BFS over deduplicated sets of computed functions (inputs + gates), level k = k gates.
cost(f)=first level whose state-set contains f. Complete when all 256 are found.
Runtime-chunked: level counts printed; stops at --maxlevel. Complement-normalised: we work with
normal functions (f(000)=0) and all 16 binary ops; negation is free in B2."""
import json, sys, time
FULL = 0xFF
X = [0xF0, 0xCC, 0xAA]
def ops(a, b):
    na, nb = FULL ^ a, FULL ^ b
    r = set()
    for x in (a, na):
        for y in (b, nb):
            r.add(x & y)
    r2 = set(r)
    for v in r: r2.add(FULL ^ v)
    r2.add(a ^ b); r2.add(FULL ^ (a ^ b))
    return r2
def main(maxlevel):
    t0 = time.time()
    cost = {0: 0, FULL: 0}
    for x in X:
        cost[x] = 0; cost[FULL ^ x] = 0
    level = {frozenset(X)}
    for k in range(1, maxlevel + 1):
        nxt = set()
        for S in level:
            L = sorted(S)
            for i in range(len(L)):
                for j in range(i + 1, len(L)):
                    for v in ops(L[i], L[j]):
                        if v in S or (FULL ^ v) in S: continue
                        # store state up to complement of the new function
                        nv = min(v, FULL ^ v)
                        nxt.add(S | {nv})
        for S in nxt:
            for v in S:
                for w in (v, FULL ^ v):
                    cost.setdefault(w, k)
        level = nxt
        print(k, len(level), len(cost), round(time.time() - t0, 1), flush=True)
        if len(cost) == 256: break
        if time.time() - t0 > 25: print("time budget"); break
    hist = {}
    for f, c in cost.items(): hist[c] = hist.get(c, 0) + 1
    json.dump({"found": len(cost), "hist": hist, "cost": {str(f): c for f, c in cost.items()},
               "AND3": cost.get(0x80), "XOR3": cost.get(0x96), "MAJ3": cost.get(0xE8)},
              open("min_circuit_n3_results.json", "w"))
    print(hist, cost.get(0x80), cost.get(0x96), cost.get(0xE8))
main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
