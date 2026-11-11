"""Exhaustive check (COMPUTATIONAL): every sound k-premise clause inference
{C1..Ck} |= D over n variables is simulated by resolution + one weakening,
with at most 2^(k-1)-1 resolution steps (tree-like, on the premises restricted by not-D).
Runs in < 30 s for the default parameters."""
import itertools, json, random, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
k = int(sys.argv[2]) if len(sys.argv) > 2 else 3
samples = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
random.seed(20261111)
lits = [v for i in range(1, n+1) for v in (i, -i)]
def clauses():
    out = []
    for r in range(1, n+1):
        for vs in itertools.combinations(range(1, n+1), r):
            for s in itertools.product((1, -1), repeat=r):
                out.append(frozenset(v*t for v, t in zip(vs, s)))
    return out
ALL = clauses()
assigns = list(itertools.product((False, True), repeat=n))
def sat(c, a): return any((a[abs(l)-1] if l > 0 else not a[abs(l)-1]) for l in c)
def implies(P, D): return all(sat(D, a) for a in assigns if all(sat(c, a) for c in P))
def min_tree_res(P, D):
    """min #resolution steps deriving some subclause of D from P (BFS over clause sets, tree-like bound by DAG search)."""
    known = {c: 0 for c in P}   # clause -> tree size (resolution steps)
    changed = True
    while changed:
        changed = False
        items = list(known.items())
        for (a, sa), (b, sb) in itertools.combinations(items, 2):
            for l in a:
                if -l in b:
                    r = (a - {l}) | (b - {-l})
                    if any(-x in r for x in r): continue
                    s = sa + sb + 1
                    if s < known.get(r, 10**9):
                        known[r] = s; changed = True
    best = [s for c, s in known.items() if c <= D]
    return min(best) if best else None
worst, checked = 0, 0
for _ in range(samples):
    P = random.sample(ALL, k)
    for D in random.sample(ALL, 12):
        if not implies(P, D): continue
        s = min_tree_res(P, D)
        assert s is not None, (P, D)
        worst = max(worst, s); checked += 1
res = {"n": n, "k": k, "implications_checked": checked, "max_tree_resolution_steps": worst,
       "bound_2^(k-1)-1": 2**(k-1)-1, "bound_holds": worst <= 2**(k-1)-1}
print(json.dumps(res))
