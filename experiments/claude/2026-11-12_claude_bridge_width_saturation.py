"""Exact minimum resolution refutation WIDTH (complete width-bounded saturation)
for small PHP^{m}_{n} and odd-charge Tseitin formulas.
COMPUTATIONAL illustration of the Ben-Sasson--Wigderson size/width engine for
Wbar_Res(N); not a lower bound beyond the listed finite instances.
Runtime target: < 30 s total (instances chosen small)."""
import itertools, json, sys, time

def resolve_closure(clauses, w):
    """Saturate under resolution keeping only resolvents of width <= w.
    Returns True iff the empty clause is derived. Complete for width-w refutations
    (any width-w refutation uses only clauses of width <= w; initial clauses wider
    than w are kept as premises, matching the standard definition)."""
    S = set(frozenset(c) for c in clauses)
    frontier = list(S)
    while frontier:
        new = []
        cur = list(S)
        for a in frontier:
            for b in cur:
                for lit in a:
                    if -lit in b:
                        r = (a - {lit}) | (b - {-lit})
                        if any(-x in r for x in r):
                            continue
                        if len(r) <= w and r not in S:
                            if not r:
                                return True
                            S.add(r); new.append(r)
                        break
        frontier = new
    return False

def min_width(clauses, wmax=12):
    w0 = max(len(c) for c in clauses)
    for w in range(1, wmax + 1):
        if resolve_closure(clauses, max(w, 1)) and w >= 1:
            return w, w0
    return None, w0

def php(m, n):
    v = lambda i, j: i * n + j + 1
    cl = [[v(i, j) for j in range(n)] for i in range(m)]
    for j in range(n):
        for i, k in itertools.combinations(range(m), 2):
            cl.append([-v(i, j), -v(k, j)])
    return cl

def tseitin(edges, charge):
    idx = {e: t + 1 for t, e in enumerate(edges)}
    verts = sorted({x for e in edges for x in e})
    cl = []
    for u in verts:
        inc = [idx[e] for e in edges if u in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            # forbid assignments with parity != charge[u]
            if sum(signs) % 2 != charge[u]:
                cl.append([x if s == 0 else -x for x, s in zip(inc, signs)])
    return cl

K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
K33 = [(a,b) for a in range(3) for b in range(3,6)]
PRISM = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
def odd(nv): return {u: (1 if u == 0 else 0) for u in range(nv)}

out = {"instances": []}
t0 = time.time()
for name, F in [("PHP_3_2", php(3,2)), ("PHP_4_3", php(4,3)),
                ("Tseitin_K4_odd", tseitin(K4, odd(4)))]:
    # K3,3 / prism6 Tseitin exceeded the 30 s budget in pure Python and were dropped.
    w, w0 = min_width(F)
    nvars = max(abs(x) for c in F for x in c)
    out["instances"].append({"name": name, "vars": nvars, "clauses": len(F),
                             "initial_width": w0, "min_refutation_width": w})
    print(name, nvars, len(F), w0, w, f"{time.time()-t0:.2f}s", flush=True)
# hostile control: a satisfiable formula must never derive the empty clause
ctrl = tseitin(K4, {0:1,1:1,2:0,3:0})
out["control_even_charge_K4_refutable_at_width_8"] = resolve_closure(ctrl, 8)
out["seconds"] = round(time.time() - t0, 2)
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(out["control_even_charge_K4_refutable_at_width_8"], out["seconds"])
