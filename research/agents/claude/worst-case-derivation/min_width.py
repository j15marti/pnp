"""Exact minimum resolution refutation width for small UNSAT CNFs.
Width-bounded saturation: closure of the clause set under resolution keeping only
resolvents of width <= w (initial clauses always kept). The smallest w for which
the empty clause appears is exactly the minimum refutation width w(F |- bot)
(standard; Ben-Sasson--Wigderson 2001). Each instance is capped at ~5 s so the
whole run stays under 30 s. Output: JSON on stdout."""
import itertools, json, random, sys, time

def php(m, n):  # m pigeons, n holes, var p(i,j) = i*n+j+1
    v = lambda i, j: i*n + j + 1
    cls = [frozenset(v(i, j) for j in range(n)) for i in range(m)]
    for j in range(n):
        for a, b in itertools.combinations(range(m), 2):
            cls.append(frozenset((-v(a, j), -v(b, j))))
    return cls

def tseitin(edges, charge):  # odd total charge -> UNSAT
    var = {e: k+1 for k, e in enumerate(edges)}
    nodes = sorted({x for e in edges for x in e})
    cls = []
    for u in nodes:
        inc = [var[e] for e in edges if u in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge[u]:  # forbid assignments with wrong parity
                cls.append(frozenset(x if s == 0 else -x for x, s in zip(inc, signs)))
    return cls

def random3(n, m, seed):
    r = random.Random(seed)
    return [frozenset(x*r.choice((1, -1)) for x in r.sample(range(1, n+1), 3)) for _ in range(m)]

def is_unsat(cls, n):
    for a in itertools.product([False, True], repeat=n):
        if all(any((l > 0) == a[abs(l)-1] for l in c) for c in cls):
            return False
    return True

def refutable_at(cls, w, deadline):
    S = set(cls); frontier = list(S)
    while frontier:
        new = []
        Sl = list(S)
        for c in frontier:
            for d in Sl:
                for l in c:
                    if -l in d:
                        r = (c - {l}) | (d - {-l})
                        if any(-x in r for x in r) or len(r) > w or r in S:
                            continue
                        if not r:
                            return True
                        S.add(r); new.append(r)
                        break
            if time.time() > deadline:
                return None
        frontier = new
    return False

def min_width(cls, n, budget=5.0):
    deadline = time.time() + budget
    w0 = max(len(c) for c in cls)
    for w in range(w0, n+1):
        r = refutable_at(cls, w, deadline)
        if r is None:
            return None, w0
        if r:
            return w, w0
    return None, w0

out = []
def run(name, cls, n):
    t = time.time()
    unsat = is_unsat(cls, n) if n <= 20 else None
    w, w0 = min_width(cls, n)
    out.append(dict(name=name, vars=n, clauses=len(cls), initial_width=w0, unsat=unsat,
                    min_ref_width=w, seconds=round(time.time()-t, 2),
                    status="EXACT" if w is not None else "UNDETERMINED(timeout; only widths below the last tried value excluded)"))

for k in (2, 3, 4):
    run(f"PHP_{k+1}^{k}", php(k+1, k), (k+1)*k)
K4 = [(a, b) for a, b in itertools.combinations(range(4), 2)]
run("Tseitin_K4_odd", tseitin(K4, {0: 1, 1: 0, 2: 0, 3: 0}), 6)
cyc = [(i, (i+1) % 6) for i in range(6)] + [(0, 3), (1, 4), (2, 5)]   # K_{3,3}-like 3-regular
run("Tseitin_3reg6_odd", tseitin(cyc, {i: int(i == 0) for i in range(6)}), 9)
for seed in range(40):
    cls = random3(12, 70, seed)
    if is_unsat(cls, 12):
        run(f"rand3_n12_m70_seed{seed}", cls, 12)
        if sum(o['name'].startswith('rand3') for o in out) >= 3:
            break
json.dump(out, sys.stdout, indent=1)
