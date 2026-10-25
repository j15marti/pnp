"""Exact minimum AND-gate counts (fan-in 2, free negation on wires, i.e. AIG) for all
Boolean functions on n<=3 inputs, via BFS over sets of available signals (canonical frozensets).
Wires = 2*gates (+1 output edge). Also: min gates for functions with exactly one satisfying point."""
import json, sys, itertools
n = int(sys.argv[1]); N = 1 << n; M = (1 << N) - 1
ins = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    ins.append(t)
def norm(s):  # signals up to negation
    return min(s, M ^ s)
start = frozenset(norm(t) for t in ins)
best = {}  # function(norm) -> min gates
for s in start: best[s] = 0
frontier = {start}; seen = {start}; k = 0
while frontier and k < 8:
    k += 1; nxt = set()
    for S in frontier:
        L = list(S)
        sig = L + [M ^ a for a in L]
        for a, b in itertools.combinations(sig, 2):
            g = norm(a & b)
            if g in (0,) or g in S: continue
            S2 = S | {g}
            if S2 not in seen:
                seen.add(S2); nxt.add(S2)
                if g not in best: best[g] = k
    frontier = nxt
    if len(best) >= (1 << (N - 1)) + 1 - 0 and False: break
    print("k", k, "states", len(seen), "funcs", len(best), file=sys.stderr)
# functions up to negation incl. constant 0 (norm 0)
cnt = {}
for f, g in best.items(): cnt[g] = cnt.get(g, 0) + 1
uniq = {}
for f, g in best.items():
    pc = bin(f).count("1"); pc = min(pc, N - pc)
    if pc == 1: uniq[g] = uniq.get(g, 0) + 1
print(json.dumps({"n": n, "functions_up_to_negation_found": len(best), "expected": (1 << N) // 2,
                  "count_by_min_gates": cnt, "unique_point_functions_by_min_gates": uniq}))
