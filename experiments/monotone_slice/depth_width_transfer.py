"""DEPTHWIDTH1: minimal depth r of free-2-SAT decision certificates on random
UNSAT 3-CNF at density 6 (above threshold), growing n.  Certificate semantics
match TWOSATDEC: an r-set S certifies iff every assignment of S, after unit
propagation, yields an empty clause or an unsatisfiable width<=2 skeleton.
Seed fixed; complete DPLL used to keep only UNSAT draws."""
import itertools, random, sys, time

def up(clauses, assign):
    a = dict(assign)
    while True:
        changed = False; rest = []
        for c in clauses:
            lits = []; sat = False
            for l in c:
                v = abs(l)
                if v in a:
                    if a[v] == (l > 0): sat = True; break
                else: lits.append(l)
            if sat: continue
            if not lits: return None, None
            if len(lits) == 1:
                a[abs(lits[0])] = lits[0] > 0; changed = True
            rest.append(lits)
        if not changed: return a, rest

def twosat_unsat(cl2):
    g = {}
    for c in cl2:
        x, y = (c[0], c[0]) if len(c) == 1 else c
        g.setdefault(-x, []).append(y); g.setdefault(-y, []).append(x)
    def reach(s, t):
        st, seen = [s], {s}
        while st:
            u = st.pop()
            if u == t: return True
            for w in g.get(u, []):
                if w not in seen: seen.add(w); st.append(w)
        return False
    vs = {abs(l) for c in cl2 for l in c}
    return any(reach(v, -v) and reach(-v, v) for v in vs)

def refuted(F, rho):
    a, rest = up(F, rho)
    if a is None: return True
    return twosat_unsat([c for c in rest if len(c) <= 2])

def sat(F, a=None):
    a, rest = up(F, a or {})
    if a is None: return False
    if not rest: return True
    v = abs(rest[0][0])
    return sat(F, {**a, v: True}) or sat(F, {**a, v: False})

def min_depth(F, n, rmax):
    for r in range(rmax + 1):
        for S in itertools.combinations(range(1, n + 1), r):
            if all(refuted(F, dict(zip(S, bits)))
                   for bits in itertools.product([False, True], repeat=r)):
                return r
    return None  # > rmax

def main():
    rng = random.Random(20261120); D = 6.0; rmax = 4; t0 = time.time()
    print("seed 20261120 density 6.0 rmax", rmax)
    for n in (8, 12, 16, 20, 24, 28, 32, 36):
        rs = []
        while len(rs) < 3:
            F = []
            for _ in range(int(D * n)):
                vs = rng.sample(range(1, n + 1), 3)
                F.append([v if rng.random() < .5 else -v for v in vs])
            if sat(F): continue
            rs.append(min_depth(F, n, rmax))
        print(f"n={n} m={int(D*n)} min_depth={rs} t={time.time()-t0:.1f}s"); sys.stdout.flush()
main()
