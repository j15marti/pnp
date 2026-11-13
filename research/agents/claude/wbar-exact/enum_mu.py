"""Enumerate all minimally unsatisfiable exact-3-CNFs on n=4 variables up to
isomorphism (variable permutations x sign flips, |G| = 384).

Structure used (elementary, proved in the report): an exact-3 clause on 4
variables falsifies exactly the two assignments of an edge of the 4-cube Q4
(they differ only in the absent variable). Hence an exact-3-CNF on 4 variables
is a set of Q4 edges, it is unsatisfiable iff the edges cover all 16 vertices,
and it is minimally unsatisfiable iff it is a minimal edge cover, i.e. a
spanning forest of stars K_{1,k} (k >= 1). The clause symmetry group equals
Aut(Q4). Runtime: a few seconds."""
import itertools, json, sys
n, A = 4, 16
edges = []          # (u, w) with u < w, w = u | bit
for u in range(A):
    for v in range(n):
        if not (u >> v) & 1:
            edges.append((u, u | (1 << v)))
eid = {e: i for i, e in enumerate(edges)}
def E(a, b): return eid[(min(a, b), max(a, b))]
nbr = [[u ^ (1 << v) for v in range(n)] for u in range(A)]
covers = []
def rec(unassigned, emask):
    if not unassigned:
        covers.append(emask); return
    v = (unassigned & -unassigned).bit_length() - 1
    rest = unassigned & ~(1 << v)
    free = [w for w in nbr[v] if (rest >> w) & 1]
    # v is a centre with leaf set L (|L| >= 1)
    for k in range(1, len(free) + 1):
        for L in itertools.combinations(free, k):
            m = emask; r = rest
            for w in L: m |= 1 << E(v, w); r &= ~(1 << w)
            rec(r, m)
    # v is a leaf of centre u with at least one further leaf
    for u in free:
        r0 = rest & ~(1 << u)
        others = [w for w in nbr[u] if (r0 >> w) & 1]
        for k in range(1, len(others) + 1):
            for L in itertools.combinations(others, k):
                m = emask | (1 << E(u, v)); r = r0
                for w in L: m |= 1 << E(u, w); r &= ~(1 << w)
                rec(r, m)
rec((1 << A) - 1, 0)
# Aut(Q4) acting on edges, via byte lookup tables
def vmap(x, perm, flip):
    y = 0
    for v in range(n):
        if (x >> v) & 1: y |= 1 << perm[v]
    return y ^ flip
tables = []
for perm in itertools.permutations(range(n)):
    for flip in range(A):
        img = [E(vmap(a, perm, flip), vmap(b, perm, flip)) for a, b in edges]
        tabs = []
        for byte in range(4):
            t = [0] * 256
            for val in range(256):
                m = 0
                for j in range(8):
                    if (val >> j) & 1: m |= 1 << img[8 * byte + j]
                t[val] = m
            tabs.append(t)
        tables.append(tabs)
def canon(m):
    b0, b1, b2, b3 = m & 255, (m >> 8) & 255, (m >> 16) & 255, (m >> 24) & 255
    return min(t0[b0] | t1[b1] | t2[b2] | t3[b3] for t0, t1, t2, t3 in tables)
classes = {}
for m in covers:
    c = canon(m)
    classes[c] = classes.get(c, 0) + 1
def to_clauses(m):  # edge (u, u|bit v) -> clause falsified exactly there
    out = []
    for i, (a, b) in enumerate(edges):
        if (m >> i) & 1:
            free = (a ^ b).bit_length() - 1
            pos = neg = 0
            for v in range(n):
                if v == free: continue
                if (a >> v) & 1: neg |= 1 << v     # var true in falsifier -> negative literal
                else: pos |= 1 << v
            out.append([pos, neg])
    return out
keys = sorted(classes, key=lambda c: (bin(c).count("1"), c))
out = {"n": n, "mu_labelled": len(covers), "mu_iso_classes": len(keys),
       "formulas": [{"edge_mask": c, "orbit_size": classes[c],
                     "clauses": to_clauses(c)} for c in keys]}
json.dump(out, open(sys.argv[1], "w"))
print("labelled MU:", len(covers), "iso classes:", len(keys),
      "orbit sum check:", sum(classes.values()) == len(covers),
      "clause counts:", sorted({bin(c).count('1') for c in keys}))
