"""Minimal depth r of a 'free exact 2-SAT' certificate (TWOSATDEC protocol) on
random 3-CNF at fixed supra-threshold density, as n grows.

Certificate (as in TWOSATDEC notes): a set R of r variables such that every
assignment of R, after unit propagation, yields an empty clause or an
unsatisfiable width<=2 skeleton (width-3 survivors ignored).
Usage: python -I twosat_backdoor_depth_growth.py DELTA SEED N_PER n1 n2 ...
"""
import sys, random, itertools, json, time

def gen(n, m, rng):
    cls = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        cls.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return cls

def up(cls, assign):
    a = dict(assign)
    while True:
        changed = False; out = []
        for c in cls:
            sat = False; rest = []
            for l in c:
                v = a.get(abs(l))
                if v is None: rest.append(l)
                elif v == (l > 0): sat = True; break
            if sat: continue
            if not rest: return None
            if len(rest) == 1:
                a[abs(rest[0])] = rest[0] > 0; changed = True; break
            out.append(tuple(rest))
        if not changed: return out

def twosat_unsat(cls, n):
    two = [c for c in cls if len(c) == 2]
    g = {}
    for x, y in two:
        g.setdefault(-x, []).append(y); g.setdefault(-y, []).append(x)
    # Kosaraju-free: check x ->* -x and -x ->* x via BFS (small n)
    def reach(s, t):
        st = [s]; seen = {s}
        while st:
            u = st.pop()
            if u == t: return True
            for w in g.get(u, ()):
                if w not in seen: seen.add(w); st.append(w)
        return False
    vs = {abs(l) for c in two for l in c}
    return any(reach(v, -v) and reach(-v, v) for v in vs)

def certifies(cls, n, R):
    for bits in itertools.product((False, True), repeat=len(R)):
        red = up(cls, zip(R, bits))
        if red is None: continue
        if not twosat_unsat(red, n): return False
    return True

def sat(cls, n):
    def dpll(a):
        red = up(cls, a.items())
        if red is None: return False
        if not red: return True
        # recover propagated assignment by re-running cheaply: branch on first var
        v = abs(red[0][0])
        for b in (True, False):
            b2 = dict(a); b2[v] = b
            if dpll(b2): return True
        return False
    return dpll({})

def min_r(cls, n, rmax):
    for r in range(0, rmax + 1):
        for R in itertools.combinations(range(1, n + 1), r):
            if certifies(cls, n, R): return r
    return None

if __name__ == "__main__":
    delta = float(sys.argv[1]); seed = int(sys.argv[2]); N = int(sys.argv[3])
    ns = [int(x) for x in sys.argv[4:]]
    rng = random.Random(seed); res = {"delta": delta, "seed": seed, "N": N, "rows": []}
    for n in ns:
        t0 = time.time(); m = int(round(delta * n)); rs = []; unsat = 0
        for _ in range(N):
            f = gen(n, m, rng)
            if sat(f, n): continue
            unsat += 1; rs.append(min_r(f, n, 6))
        row = {"n": n, "m": m, "unsat": unsat, "min_r": rs, "secs": round(time.time() - t0, 2)}
        res["rows"].append(row); print(json.dumps(row), flush=True)
    print(json.dumps(res))
