"""DT2WIDTH1: finite check of Lemma DT2-WIDTH on small random 3-CNFs.

Lemma: if every leaf of a depth-r decision tree is certified by unit
propagation (UP) + free exact 2-SAT on the width<=2 skeleton, then the
formula has a resolution refutation of width <= r+3.  Equivalently
  rmin(F) >= w(F) - 3,
where rmin is the minimum depth of such a tree and w(F) the minimum
resolution refutation width.  This script computes both exactly for
small n and reports any violation (a violation would falsify the lemma).
COMPUTATIONAL only; finite n proves nothing asymptotic.
Usage: python -I twosat_depth_vs_width.py SEED N_VARS DENSITY TRIALS
"""
import sys, random, itertools, time
from functools import lru_cache

def gen(rng, n, m):
    allc = []
    for t in itertools.combinations(range(n), 3):
        for s in range(8):
            allc.append(tuple((v, (s >> i) & 1) for i, v in enumerate(t)))
    return rng.sample(allc, m)

def to_masks(cl):  # (posmask, negmask); pol 1 = positive
    p = q = 0
    for v, pol in cl:
        if pol: p |= 1 << v
        else: q |= 1 << v
    return (p, q)

def width_refutable(F, n, w):
    """Width-w resolution: saturate clauses of width <= w; True iff empty derived."""
    S = set(c for c in F if bin(c[0]|c[1]).count('1') <= w)
    frontier = list(S)
    while frontier:
        new = []
        Sl = list(S)
        for a in frontier:
            for b in Sl:
                piv = (a[0] & b[1]) | (a[1] & b[0])
                if piv == 0 or piv & (piv - 1): continue  # need exactly one clash
                p = (a[0] | b[0]) & ~piv; q = (a[1] | b[1]) & ~piv
                if bin(p | q).count('1') > w: continue
                r = (p, q)
                if r == (0, 0): return True
                if r not in S:
                    S.add(r); new.append(r)
        frontier = new
    return False

def min_width(F, n):
    for w in range(3, n + 1):
        if width_refutable(F, n, w): return w
    return None

def certified(F, n, a1, a0):
    """UP + free 2-SAT on width<=2 skeleton (3-clauses not charged)."""
    while True:
        changed = False; two = []
        for p, q in F:
            if p & a1 or q & a0: continue  # satisfied
            p2, q2 = p & ~a0, q & ~a1      # remaining literals
            k = bin(p2 | q2).count('1')
            if k == 0: return True
            if k == 1:
                if p2: a1 |= p2
                else: a0 |= q2
                changed = True
            elif k == 2: two.append((p2, q2))
        if not changed: break
    # 2-SAT on 'two' via brute force over involved vars (n small)
    vs = 0
    for p, q in two: vs |= p | q
    idx = [i for i in range(n) if vs >> i & 1]
    if not idx: return False
    for bits in range(1 << len(idx)):
        x = 0
        for j, i in enumerate(idx):
            if bits >> j & 1: x |= 1 << i
        if all((p & x) or (q & ~x) for p, q in two): return False
    return True

def min_depth(F, n):
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def D(a1, a0):
        if certified(F, n, a1, a0): return 0
        best = n
        for v in range(n):
            b = 1 << v
            if (a1 | a0) & b: continue
            d = 1 + max(D(a1, a0 | b), D(a1 | b, a0))
            if d < best:
                best = d
                if best == 1: break
        return best
    return D(0, 0)

def main():
    seed, n, dens, T = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed); m = int(dens * n); t0 = time.time()
    print(f"DT2WIDTH1 seed={seed} n={n} m={m} density={dens} trials={T}")
    viol = 0; rows = []
    for k in range(T):
        F = [to_masks(c) for c in gen(rng, n, m)]
        sat = any(all((p & x) or (q & ~x) for p, q in F) for x in range(1 << n))
        w = None if sat else min_width(F, n)
        if w is None:
            print(f"trial {k}: SAT (no refutation)"); continue
        r = min_depth(F, n)
        ok = r >= w - 3
        viol += (not ok)
        print(f"trial {k}: w={w} rmin={r} rmin>=w-3:{ok}")
    print(f"violations={viol} runtime={time.time()-t0:.2f}s")

if __name__ == '__main__':
    main()
