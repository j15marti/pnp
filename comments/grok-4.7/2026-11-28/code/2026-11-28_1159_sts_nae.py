#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28 1153 KST: NAE on Steiner triple systems.
Checks (all exact, integer arithmetic):
 (1) STS property of each constructed system;
 (2) exact identity  #monochromatic lines = (1/2)(s - v/2)^2 + v(v-4)/24  for every 2-colouring
     (exhaustive for v <= 21, random sample above), hence UNSAT for v >= 7;
 (3) the multilinear polynomial identity  sum_L [(1-x)(1-y)(1-z) + xyz] = (1/2)(s-v/2)^2 + v(v-4)/24
     modulo x_i^2 = x_i, checked coefficient by coefficient with Fractions;
 (4) width<=2 RUP: no guard of <=2 literals yields a UP conflict (no first width-2 RUP clause);
 (5) width-3 RUP: number of 3-literal guards giving a UP conflict on a non-clause triple;
 (6) bucket boundary of every variable = v-1 (primal graph complete);
 (7) pair joins of two intersecting lines: every 2-variable projection is all of {0,1}^2.
Usage: python3 2026-11-28_1159_sts_nae.py   (deterministic; seed fixed)
"""
import itertools, random
from fractions import Fraction
random.seed(20261128)

def bose(v):  # v = 6t+3
    n = v // 3  # 2t+1, odd
    half = (n + 1) // 2  # inverse of 2 mod n
    idx = lambda x, i: x + n * i
    T = []
    for x in range(n):
        T.append((idx(x,0), idx(x,1), idx(x,2)))
    for x in range(n):
        for y in range(x+1, n):
            m = ((x + y) * half) % n
            for i in range(3):
                T.append((idx(x,i), idx(y,i), idx(m,(i+1)%3)))
    return T

def pg(m):  # PG(m,2): points = nonzero vectors of F2^{m+1}
    pts = list(range(1, 2**(m+1)))
    T = set()
    for a in pts:
        for b in pts:
            if a < b:
                c = a ^ b
                T.add(tuple(sorted((a,b,c))))
    T = sorted(T)
    rel = {p: i for i, p in enumerate(pts)}
    return [tuple(rel[p] for p in t) for t in T]

def ag(m):  # AG(m,3): lines x+y+z = 0 in F3^m
    pts = list(itertools.product(range(3), repeat=m))
    rel = {p: i for i, p in enumerate(pts)}
    T = set()
    for a in pts:
        for b in pts:
            if a < b:
                c = tuple((-x - y) % 3 for x, y in zip(a, b))
                T.add(tuple(sorted((rel[a], rel[b], rel[c]))))
    return sorted(T)

def stinson(v, maxit=10**7):  # Stinson hill-climbing for any admissible v
    while True:
        live = {x: set(range(v)) - {x} for x in range(v)}  # live pairs
        other = {}  # (x,y) -> z for the block containing x,y
        blocks = set(); nb = v*(v-1)//6; it = 0
        while len(blocks) < nb and it < maxit:
            it += 1
            xs = [x for x in range(v) if live[x]]
            x = random.choice(xs)
            y, z = random.sample(sorted(live[x]), 2)
            if z in live[y]:
                pass
            else:
                w = other[(y, z)]
                b = tuple(sorted((y, z, w)))
                blocks.discard(b)
                for p, q in ((y,z),(y,w),(z,w)):
                    live[p].add(q); live[q].add(p)
                    other.pop((p,q), None); other.pop((q,p), None)
            b = tuple(sorted((x, y, z)))
            blocks.add(b)
            for p, q, r in ((x,y,z),(x,z,y),(y,z,x)):
                live[p].discard(q); live[q].discard(p)
                other[(p,q)] = r; other[(q,p)] = r
        if len(blocks) == nb:
            return sorted(blocks)

def check_sts(v, T):
    cnt = {}
    for t in T:
        assert len(set(t)) == 3
        for p in itertools.combinations(sorted(t), 2):
            cnt[p] = cnt.get(p, 0) + 1
    assert len(T) == v*(v-1)//6
    assert len(cnt) == v*(v-1)//2 and all(c == 1 for c in cnt.values())
    return True

def mono_identity(v, T, exhaustive_limit=21, samples=20000):
    masks = [(1<<a)|(1<<b)|(1<<c) for a,b,c in T]
    full = 0
    ok = True; mn = None
    rng = range(1 << v) if v <= exhaustive_limit else (random.getrandbits(v) for _ in range(samples))
    for x in rng:
        mono = 0
        for m in masks:
            k = x & m
            if k == 0 or k == m: mono += 1
        s = bin(x).count('1')
        rhs = Fraction(1,2)*(Fraction(s) - Fraction(v,2))**2 + Fraction(v*(v-4),24)
        if rhs != mono: ok = False
        mn = mono if mn is None else min(mn, mono)
    return ok, mn, (v <= exhaustive_limit)

def poly_identity(v, T):
    # multilinear polys as dict frozenset->Fraction
    def add(P, mon, c):
        P[mon] = P.get(mon, 0) + c
        if P[mon] == 0: del P[mon]
    L = {}
    for (a,b,c) in T:
        # (1-a)(1-b)(1-c) + abc = 1 - e1 + e2
        add(L, frozenset(), Fraction(1))
        for u in (a,b,c): add(L, frozenset([u]), Fraction(-1))
        for u,w in ((a,b),(a,c),(b,c)): add(L, frozenset([u,w]), Fraction(1))
    R = {}
    # (1/2)(s - v/2)^2 + v(v-4)/24, with x_i^2 = x_i
    h = Fraction(v,2)
    add(R, frozenset(), Fraction(1,2)*h*h + Fraction(v*(v-4),24))
    for i in range(v):
        add(R, frozenset([i]), Fraction(1,2)*(1 - 2*h))  # x_i^2 = x_i and -2h x_i
    for i in range(v):
        for j in range(i+1, v):
            add(R, frozenset([i,j]), Fraction(1))  # (1/2)*2 x_i x_j
    return L == R

def up_conflict(v, occ, T, guard):
    """NAE unit propagation. guard: dict var->0/1. returns (conflict, assignment)."""
    a = dict(guard); queue = list(guard)
    while queue:
        u = queue.pop()
        for t in occ[u]:
            vals = [a.get(w) for w in t]
            known = [w for w in t if w in a]
            if len(known) == 3:
                if vals[0] == vals[1] == vals[2]: return True, a
            elif len(known) == 2:
                p, q = known
                if a[p] == a[q]:
                    r = [w for w in t if w not in a][0]
                    a[r] = 1 - a[p]; queue.append(r)
    # final full check
    for t in T:
        if all(w in a for w in t) and a[t[0]] == a[t[1]] == a[t[2]]: return True, a
    return False, a

def rup_scan(v, T, width, limit=None):
    occ = {i: [] for i in range(v)}
    for t in T:
        for u in t: occ[u].append(t)
    lines = set(T)
    conflicts = 0; tested = 0; maxforced = 0
    for S in itertools.combinations(range(v), width):
        for vals in itertools.product((0,1), repeat=width):
            tested += 1
            c, a = up_conflict(v, occ, T, dict(zip(S, vals)))
            maxforced = max(maxforced, len(a) - width)
            if c and not (width == 3 and tuple(sorted(S)) in lines and len(set(vals)) == 1):
                conflicts += 1
        if limit and tested >= limit: break
    return tested, conflicts, maxforced

def pair_join_check(T):
    # two lines sharing one point: every pair of the 5 vars has full projection
    from collections import defaultdict
    by = defaultdict(list)
    for t in T:
        for u in t: by[u].append(t)
    checked = 0
    for u, ls in by.items():
        for l1, l2 in itertools.combinations(ls[:4], 2):
            V = sorted(set(l1) | set(l2))
            sols = [x for x in itertools.product((0,1), repeat=len(V))
                    if all(len({x[V.index(w)] for w in l}) == 2 for l in (l1, l2))]
            for i, j in itertools.combinations(range(len(V)), 2):
                if len({(x[i], x[j]) for x in sols}) != 4: return False, checked
            checked += 1
    return True, checked

def main():
    systems = [("PG(2,2)=Fano", 7, pg(2)), ("AG(2,3)", 9, ag(2)), ("Bose", 9, bose(9)),
               ("Stinson", 13, stinson(13)), ("PG(3,2)", 15, pg(3)), ("Bose", 15, bose(15)),
               ("Stinson", 19, stinson(19)), ("Bose", 21, bose(21)), ("Stinson", 25, stinson(25)),
               ("AG(3,3)", 27, ag(3)), ("PG(4,2)", 31, pg(4)), ("Stinson", 31, stinson(31)),
               ("Stinson", 43, stinson(43)), ("PG(5,2)", 63, pg(5))]
    print("name | v | lines | STS ok | poly identity | mono identity (exh?) | min mono | v(v-4)/24 | "
          "w<=2 RUP tested/conflicts/maxforced | w=3 RUP tested/new-conflicts | bucket boundary | pair-joins full")
    for name, v, T in systems:
        check_sts(v, T)
        pid = poly_identity(v, T)
        ok, mn, exh = mono_identity(v, T)
        t1 = rup_scan(v, T, 1); t2 = rup_scan(v, T, 2)
        w2 = (t1[0] + t2[0] + 1, t1[1] + t2[1], max(t1[2], t2[2]))
        w3 = rup_scan(v, T, 3) if v <= 31 else ("skip", "skip", "skip")
        bnd = min(len({w for t in T if u in t for w in t} - {u}) for u in range(v))
        pj = pair_join_check(T)
        print(f"{name} | {v} | {len(T)} | True | {pid} | {ok} ({'exh' if exh else 'sample'}) | {mn} | "
              f"{Fraction(v*(v-4),24)} | {w2[0]}/{w2[1]}/{w2[2]} | {w3[0]}/{w3[1]} | {bnd} | {pj[0]} ({pj[1]} pairs)")

if __name__ == "__main__":
    main()
