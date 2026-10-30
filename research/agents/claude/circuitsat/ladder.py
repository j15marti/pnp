"""Exact small-n ladder for circuit-SAT wire counts (B2 basis, fan-in 2).
Per n: C(n)=max over n-var functions of min circuit gates (iterative deepening),
L(n)=max min formula leaves (DP), U(n)=min gates of a circuit with exactly one
satisfying assignment (and wires = 2*gates). Chunked: run `ladder.py N`."""
import sys, json, itertools
n = int(sys.argv[1]); R = 1 << n; M = (1 << R) - 1
ops = [lambda a,b,c=c: sum(((c>>(2*x+y))&1)<<k for k,(x,y) in [(0,(0,0))]) for c in []]
def apply(c, a, b):
    # c: 4-bit table over (a,b); bitwise on truth tables
    r = 0
    if c & 1: r |= ~a & ~b
    if c & 2: r |= ~a & b
    if c & 4: r |= a & ~b
    if c & 8: r |= a & b
    return r & M
# non-degenerate binary ops (depend on both args): exclude 0,15,3,5,10,12
OPS = [c for c in range(16) if c not in (0,15,3,5,10,12)]
inputs = []
for i in range(n):
    t = 0
    for x in range(R):
        if (x >> i) & 1: t |= 1 << x
    inputs.append(t)
# formula size DP over truth tables
INF = 99
L = {0:0, M:0}
for t in inputs: L[t] = 1; L[M ^ t] = 1
for ft in range(1<<R): L.setdefault(ft, INF)
changed = True
while changed:
    changed = False
    items = [(k,v) for k,v in L.items() if v < INF]
    for a,la in items:
        for b,lb in items:
            for c in OPS:
                r = apply(c,a,b); s = la+lb
                if s < L[r]: L[r] = s; changed = True
Lmax = max(L.values())
# min circuit gates by iterative deepening on sets of computed functions
best = {}
def dfs(avail, depth, limit):
    for f in avail: best.setdefault(f, 99)
    return
def circ_sizes():
    sizes = {}
    base = frozenset([0, M] + inputs)
    level = {base}; seen = {base}
    for k in range(0, 8):
        for st in level:
            for f in st: sizes.setdefault(f, k)
        if len(sizes) == 1 << R: return sizes, k
        nxt = set()
        for st in level:
            lst = list(st)
            for i,a in enumerate(lst):
                for b in lst[i+1:]:
                    for c in OPS:
                        r = apply(c,a,b)
                        if r not in st:
                            ns = st | {r}
                            if ns not in seen: seen.add(ns); nxt.add(ns)
        level = nxt
    return sizes, None
sizes, k = circ_sizes()
Cmax = max(sizes.values())
uniq = [f for f in sizes if bin(f).count("1") == 1]
U = min(sizes[f] for f in uniq)
out = dict(n=n, max_formula_leaves=Lmax, max_circuit_gates=Cmax,
           min_gates_unique_sat=U, wires_unique_sat=2*U,
           formula_leaves_unique_sat=max(L[f] for f in uniq))
print(json.dumps(out)); open(f"ladder_n{n}.json","w").write(json.dumps(out))
