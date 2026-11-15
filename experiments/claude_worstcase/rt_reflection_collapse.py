#!/usr/bin/env python3
"""Reflection-system hardness-collapse control (CLAUDE-WCD-0001).

For odd-charge Tseitin formulas on small graphs compute
  (a) the exact minimum resolution refutation WIDTH by bounded-width
      saturation (width-w resolution closure; smallest w deriving the empty
      clause; input clauses of width deg(v) are always admitted), and
  (b) the exact bit-operation count of the GF(2) Gaussian-elimination
      certificate that the reflection system R_T replays (one fixed,
      T-provably sound algorithm; cost = clocked run length).
Deterministic: no random seed.  Pure Python 3, finishes in a few seconds.
"""
import itertools, json, sys, time

def tseitin(edges, nverts, charge):
    var = {e: i + 1 for i, e in enumerate(edges)}
    clauses = []
    for v in range(nverts):
        inc = [var[e] for e in edges if v in e]
        for signs in itertools.product([0, 1], repeat=len(inc)):
            # forbid assignments whose parity != charge[v]
            if sum(signs) % 2 != charge[v]:
                clauses.append(frozenset(x if s == 0 else -x for x, s in zip(inc, signs)))
    return len(edges), clauses

def min_res_width(nvars, clauses, wmax, budget_s=6.0):
    """Smallest w >= max input width s.t. width-w closure contains the empty
    clause.  Returns (w, status); status 'TIMEOUT' means undetermined."""
    t0 = time.time()
    winit = max(len(c) for c in clauses)
    for w in range(winit, wmax + 1):
        known = set(clauses); byvar = {}
        for c in known:
            for l in c: byvar.setdefault(l, []).append(c)
        frontier = list(known)
        while frontier:
            new = []
            for c in frontier:
                if time.time() - t0 > budget_s:
                    return None, "TIMEOUT"
                for l in c:
                    for d in list(byvar.get(-l, [])):
                        r = (c - {l}) | (d - {-l})
                        if len(r) > w or any(-x in r for x in r) or r in known:
                            continue
                        if not r:
                            return w, "EXACT"
                        known.add(r); new.append(r)
                        for x in r: byvar.setdefault(x, []).append(r)
            frontier = new
    return None, "NOT_REFUTED"

def gauss_cost(edges, nverts, charge):
    """Bit ops of GF(2) elimination on the vertex-parity system (augmented)."""
    m = len(edges)
    rows = []
    for v in range(nverts):
        r = 0
        for i, e in enumerate(edges):
            if v in e:
                r |= 1 << i
        rows.append((r, charge[v]))
    ops = 0; piv = 0
    rows = list(rows)
    for col in range(m):
        sel = None
        for k in range(piv, len(rows)):
            if rows[k][0] >> col & 1:
                sel = k; break
        if sel is None:
            continue
        rows[piv], rows[sel] = rows[sel], rows[piv]
        for k in range(len(rows)):
            if k != piv and rows[k][0] >> col & 1:
                rows[k] = (rows[k][0] ^ rows[piv][0], rows[k][1] ^ rows[piv][1])
                ops += m + 1
        piv += 1
    inconsistent = any(r == 0 and b == 1 for r, b in rows)
    return ops, inconsistent

def cycle(n): return [(i, (i + 1) % n) for i in range(n)], n
def wheel(n):
    e = [(i, (i + 1) % n) for i in range(n)] + [(i, n) for i in range(n)]
    return e, n + 1
def complete(n): return [(i, j) for i in range(n) for j in range(i + 1, n)], n
def kbip(a, b): return [(i, a + j) for i in range(a) for j in range(b)], a + b
def grid(r, c):
    idx = lambda i, j: i * c + j
    e = []
    for i in range(r):
        for j in range(c):
            if j + 1 < c: e.append((idx(i, j), idx(i, j + 1)))
            if i + 1 < r: e.append((idx(i, j), idx(i + 1, j)))
    return e, r * c

FAMILIES = [("C%d" % n, cycle(n)) for n in (3, 5, 8, 12)] + \
    [("W%d" % n, wheel(n)) for n in (3, 4)] + \
    [("K4", complete(4)), ("K33", kbip(3, 3)), ("Grid2x3", grid(2, 3))]

def main():
    out = []
    for name, (edges, nv) in FAMILIES:
        charge = [1] + [0] * (nv - 1)  # total charge odd -> UNSAT on connected graph
        nvars, cl = tseitin(edges, nv, charge)
        nbits = sum(len(c) for c in cl) * (nvars.bit_length() + 1)
        t = time.time()
        w, wstat = min_res_width(nvars, cl, wmax=nvars, budget_s=6.0)
        ops, inc = gauss_cost(edges, nv, charge)
        out.append(dict(graph=name, vertices=nv, edges=nvars, clauses=len(cl),
                        encoded_bits_est=nbits, max_input_width=max(len(c) for c in cl),
                        min_resolution_width=w, width_status=wstat, gauss_bitops=ops,
                        gauss_detects_unsat=inc, secs=round(time.time() - t, 3)))
        print(out[-1], flush=True)
    json.dump(dict(run="CLAUDE-WCD-0001", seed=None, results=out),
              open(sys.argv[1], "w"), indent=1)

if __name__ == "__main__":
    main()
