"""TWOSATDEC protocol audit: density dependence of the exact-layer UNSAT rate and
of the minimum decision depth r such that free exact 2-SAT certifies UNSAT.
Same certificate semantics as TWOSATDEC: every assignment of the r variables,
after unit propagation, yields an empty clause or an UNSAT width<=2 skeleton.
Seeded, deterministic. Usage: python twosatdec_density_audit.py"""
import itertools, random, sys, time

def clauses_list(q):
    out = []
    for a, b, c in itertools.combinations(range(q), 3):
        for s in range(8):
            out.append(((a, s & 1), (b, (s >> 1) & 1), (c, (s >> 2) & 1)))
    return out

def up(cls, asg):
    asg = dict(asg)
    while True:
        changed = False; live = []
        for cl in cls:
            sat = False; rest = []
            for v, p in cl:
                if v in asg:
                    if asg[v] == p: sat = True; break
                else: rest.append((v, p))
            if sat: continue
            if not rest: return None, None
            if len(rest) == 1:
                asg[rest[0][0]] = rest[0][1]; changed = True
            live.append(tuple(rest))
        if not changed: return live, asg

def dpll(cls, asg=()):
    live, a = up(cls, asg)
    if live is None: return False
    if not live: return True
    v = live[0][0][0]
    return dpll(live, ((v, 1),)) or dpll(live, ((v, 0),))

def twosat_unsat(live):
    two = [c for c in live if len(c) == 2]
    if not two: return False
    g = {}
    for (u, pu), (w, pw) in two:
        g.setdefault((u, 1 - pu), []).append((w, pw))
        g.setdefault((w, 1 - pw), []).append((u, pu))
    vs = {v for c in two for v, _ in c}
    def reach(s):
        seen = {s}; st = [s]
        while st:
            x = st.pop()
            for y in g.get(x, ()):
                if y not in seen: seen.add(y); st.append(y)
        return seen
    for v in vs:
        if (v, 0) in reach((v, 1)) and (v, 1) in reach((v, 0)): return True
    return False

def certifies(cls, S):
    for bits in itertools.product((0, 1), repeat=len(S)):
        live, _ = up(cls, tuple(zip(S, bits)))
        if live is None: continue
        if not twosat_unsat(live): return False
    return True

def min_depth(cls, q, rmax):
    for r in range(rmax + 1):
        for S in itertools.combinations(range(q), r):
            if certifies(cls, S): return r
    return None  # > rmax

def main():
    seed = 20261120; rng = random.Random(seed)
    print(f"seed {seed}")
    t0 = time.time()
    for dens in (3.5, 4.27, 6.0):
        for q in (12, 16, 20, 24):
            L = clauses_list(q); t = int(dens * q); N = 12
            uns = 0; depths = []
            for _ in range(N):
                F = rng.sample(L, t)
                if not dpll(F):
                    uns += 1
                    if dens == 6.0: depths.append(min_depth(F, q, 3))
            ds = ",".join("%s" % ("4+" if d is None else d) for d in depths)
            print(f"dens={dens} q={q} t={t} N={N} UNSAT={uns} mindepth[r<=3]={ds} elapsed={time.time()-t0:.1f}s")
            sys.stdout.flush()
main()
