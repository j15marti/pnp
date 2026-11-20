"""EXACTLAYER-DEGENERACY1 audit (TWOSATDEC97).

Stage A: Monte Carlo P(UNSAT) on the TWOSATDEC exact layer t=floor(3.5 q),
uniform t-subset of the M=8*C(q,3) proper 3-clauses (same model as TWOSATDEC).
Stage B: pilot at density t=round(4.26 q): fraction of UNSAT formulas whose
depth-r free-2-SAT closure certificate exists, r=0..3 (same certificate rule).
Usage: python3 exactlayer_degeneracy_audit.py A|B
"""
import sys, random, time, itertools, json
from math import comb
from pysat.solvers import Glucose3

SEED = 20261120

def decode(idx, q):
    tri, signs = divmod(idx, 8)
    # unrank lexicographic triple a<b<c
    a = 0
    while True:
        c_ = comb(q - a - 1, 2)
        if tri < c_: break
        tri -= c_; a += 1
    b = a + 1
    while True:
        c_ = q - b - 1
        if tri < c_: break
        tri -= c_; b += 1
    c = b + 1 + tri
    lits = []
    for k, v in enumerate((a, b, c)):
        pol = (signs >> k) & 1
        lits.append((v + 1) if pol else -(v + 1))
    return lits

def sample(rng, q, t):
    M = 8 * comb(q, 3)
    return [decode(i, q) for i in rng.sample(range(M), t)]

def is_sat(cnf):
    with Glucose3(bootstrap_with=cnf) as s:
        return s.solve()

def unitprop(cnf, assign):
    a = dict(assign); cl = [list(c) for c in cnf]
    changed = True
    while changed:
        changed = False; out = []
        for c in cl:
            if any(a.get(abs(l)) == (l > 0) for l in c): continue
            r = [l for l in c if abs(l) not in a]
            if not r: return None
            if len(r) == 1:
                a[abs(r[0])] = r[0] > 0; changed = True
            out.append(r)
        cl = out
    return cl

def twosat_unsat(cl):
    # cl all width<=2 and nonempty; check UNSAT via solver (exact)
    return not is_sat(cl)

def certifies(cnf, S):
    for bits in itertools.product((False, True), repeat=len(S)):
        rest = unitprop(cnf, zip(S, bits))
        if rest is None: continue
        if any(len(c) > 2 for c in rest): return False
        if not rest or not twosat_unsat(rest): return False
    return True

def stage_a():
    rng = random.Random(SEED); out = {}
    for q, N in [(20, 3000), (30, 3000), (40, 3000), (50, 3000), (60, 3000), (80, 3000), (100, 3000)]:
        t = int(3.5 * q); t0 = time.time()
        u = sum(1 for _ in range(N) if not is_sat(sample(rng, q, t)))
        out[q] = dict(t=t, N=N, unsat=u, p=u / N, exp16=16 * u / N, sec=round(time.time() - t0, 2))
        print(q, out[q], flush=True)
    return out

def stage_b():
    rng = random.Random(SEED + 1); out = {}
    for q, N, rmax in [(14, 80, 4), (18, 80, 4), (22, 60, 4), (26, 60, 4)]:
        t = round(4.26 * q); t0 = time.time(); uns = []
        for _ in range(N):
            f = sample(rng, q, t)
            if not is_sat(f): uns.append(f)
        mind = []
        for f in uns:
            d = None
            for r in range(rmax + 1):
                if any(certifies(f, S) for S in itertools.combinations(range(1, q + 1), r)):
                    d = r; break
            mind.append(d)
        out[q] = dict(t=t, N=N, unsat=len(uns), rmax=rmax,
                      mindepth_hist={str(k): mind.count(k) for k in sorted(set(mind), key=lambda x: (x is None, x))},
                      sec=round(time.time() - t0, 2))
        print(q, out[q], flush=True)
    return out

if __name__ == '__main__':
    st = sys.argv[1]
    res = stage_a() if st == 'A' else stage_b()
    print(json.dumps({'stage': st, 'seed': SEED if st == 'A' else SEED + 1, 'results': res}))
