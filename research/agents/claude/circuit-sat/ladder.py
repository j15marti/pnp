"""Exact minimum B2 circuit size ladder (CLAUDE CIRCUITSAT-0001).
Gates: fan-in 2, any nondegenerate binary op (AND-type x8, XOR, XNOR).
Signals are stored modulo complement (complement is absorbed by the consuming gate).
Usage: python3 ladder.py N MAXGATES  -> JSON on stdout. Level-BFS over signal sets."""
import sys, json, itertools
n = int(sys.argv[1]); K = int(sys.argv[2])
N = 1 << n; FULL = (1 << N) - 1
def canon(t): return min(t, FULL ^ t)
inputs = []
for i in range(n):
    t = 0
    for a in range(N):
        if (a >> i) & 1: t |= 1 << a
    inputs.append(canon(t))
# ops on (a,b) after absorbing input complements: and-type with 4 polarity choices + xor
def combos(a, b):
    out = set()
    for pa in (0, 1):
        for pb in (0, 1):
            x = a ^ (FULL if pa else 0); y = b ^ (FULL if pb else 0)
            out.add(canon(x & y))
    out.add(canon(a ^ b))
    return out
best = {}  # canonical table -> min gates
for t in inputs: best[t] = 0
level = {frozenset(inputs)}
for g in range(1, K + 1):
    nxt = set()
    for st in level:
        sl = sorted(st)
        for a, b in itertools.combinations(sl, 2):
            for c in combos(a, b):
                if c in st: continue
                if c not in best: best[c] = g
                nxt.add(st | {c})
    level = nxt
    print(f"# n={n} gates={g} states={len(level)} funcs_found={len(best)}", file=sys.stderr)
cnt = {}
for t, g in best.items(): cnt[g] = cnt.get(g, 0) + 1
# functions up to complement: 2^(N-1) total
print(json.dumps({"n": n, "K": K, "classes_up_to_complement": 1 << (N - 1),
                  "found": len(best), "count_by_min_gates": cnt}))
