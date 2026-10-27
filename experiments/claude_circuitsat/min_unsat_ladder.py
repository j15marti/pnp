"""Exact ladder: minimal wires/gates of a *reduced* UNSAT circuit on n inputs.
Gates: NOT (fan-in 1) or any of the 10 binary gates depending on both args (fan-in 2, distinct wires).
Reduced UNSAT: output (last gate) is identically 0, every input lies in the output cone.
Search: Dijkstra over states = frozenset of (truth_table, cone_mask); cost = wires (edges).
Usage: python min_unsat_ladder.py n [maxcost]
"""
import sys, json, itertools, heapq, time
n = int(sys.argv[1]); maxcost = int(sys.argv[2]) if len(sys.argv) > 2 else 12
N = 1 << n; FULL = (1 << N) - 1
def var(i):
    return sum(1 << a for a in range(N) if (a >> i) & 1)
# nondegenerate binary gates as 4-bit tables
def dep(t):
    f = lambda x, y: (t >> (2 * x + y)) & 1
    return any(f(0, y) != f(1, y) for y in (0, 1)) and any(f(x, 0) != f(x, 1) for x in (0, 1))
BIN = [t for t in range(16) if dep(t)]
def ap(t, a, b):
    r = 0
    for k in range(N):
        if (t >> (2 * ((a >> k) & 1) + ((b >> k) & 1))) & 1: r |= 1 << k
    return r
start = frozenset((var(i), 1 << i) for i in range(n))
allm = (1 << n) - 1
pq = [(0, 0, sorted(start), None)]; seen = {start: 0}; t0 = time.time()
best = None
cnt = 0
while pq:
    c, g, st, _ = heapq.heappop(pq); st = frozenset(st)
    if seen.get(st, 1e9) < c: continue
    if c > maxcost: break
    ws = sorted(st)
    nxt = []
    for (a, ma) in ws:
        nxt.append((1, FULL ^ a, ma))
    for (a, ma), (b, mb) in itertools.combinations(ws, 2):
        for t in BIN:
            nxt.append((2, ap(t, a, b), ma | mb))
            if a != b: nxt.append((2, ap(t, b, a), ma | mb))
    for w, f, m in nxt:
        if f == 0 and m == allm:
            best = (c + w, g + 1); break
        ns = frozenset(st | {(f, m)})
        if ns == st: continue
        nc = c + w
        if nc < seen.get(ns, 1e9) and nc <= maxcost:
            seen[ns] = nc; heapq.heappush(pq, (nc, g + 1, sorted(ns), None))
    if best: break
    if time.time() - t0 > 25: print("timeout"); break
print(json.dumps({"n": n, "min_wires": best[0] if best else None, "gates_on_witness": best[1] if best else None, "states": len(seen), "secs": round(time.time() - t0, 1)}))
