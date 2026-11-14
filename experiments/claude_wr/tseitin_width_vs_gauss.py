#!/usr/bin/env python3
"""Exact minimum resolution WIDTH of odd-charge Tseitin CNFs on small graphs,
versus fully counted GF(2) Gaussian-elimination row operations.

Purpose (W_R(N) red team): the multisign-hypergraph reduction calculus with
resolution-type merge rule is DAG resolution. Ben-Sasson--Wigderson (2001):
size >= exp((w - w0)^2 / (16 n)) in their normalization. This script computes
the exact minimum width w* by width-bounded saturation (complete for width:
w* is the least w such that width-<=w resolution derives the empty clause),
and the exact number of XOR row operations a deterministic Gaussian
elimination performs. Each graph is an independent chunk with a wall-clock cap;
results are checkpointed per graph. Deterministic, no randomness.
"""
import itertools, json, sys, time

def graphs():
    G = {}
    G['C6'] = [(i, (i+1) % 6) for i in range(6)]
    G['K4'] = list(itertools.combinations(range(4), 2))
    G['prism'] = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
    G['K33'] = [(a, b) for a in range(3) for b in range(3, 6)]
    G['K5'] = list(itertools.combinations(range(5), 2))
    G['cube'] = [(a, b) for a in range(8) for b in range(8) if a < b and bin(a ^ b).count('1') == 1]
    G['petersen'] = [(i, (i+1) % 5) for i in range(5)] + [(5+i, 5+(i+2) % 5) for i in range(5)] + [(i, i+5) for i in range(5)]
    G['grid3x3'] = [((r*3+c), (r*3+c+1)) for r in range(3) for c in range(2)] + [((r*3+c), ((r+1)*3+c)) for r in range(2) for c in range(3)]
    return G

def tseitin(edges):
    V = sorted({v for e in edges for v in e})
    inc = {v: [i for i, e in enumerate(edges) if v in e] for v in V}
    charge = {v: (1 if v == V[0] else 0) for v in V}   # total charge odd -> UNSAT
    clauses = set()
    for v in V:
        xs = inc[v]
        for signs in itertools.product((0, 1), repeat=len(xs)):
            # forbid assignment `signs` whose parity != charge
            if sum(signs) % 2 != charge[v]:
                pos = neg = 0
                for x, s in zip(xs, signs):
                    if s: neg |= 1 << x   # forbid x=1 -> literal not-x
                    else: pos |= 1 << x
                clauses.add((pos, neg))
    return V, inc, charge, clauses

def width(c): return bin(c[0]).count('1') + bin(c[1]).count('1')

def derives_empty(clauses, w, deadline):
    S = {c for c in clauses if width(c) <= w}
    new = list(S)
    while new:
        if time.time() > deadline: return None
        nxt = []
        Sl = list(S)
        for c in new:
            if time.time() > deadline: return None
            for d in Sl:
                clash = (c[0] & d[1]) | (c[1] & d[0])
                if clash == 0 or clash & (clash - 1): continue  # need exactly one clashing var
                r = ((c[0] | d[0]) & ~clash, (c[1] | d[1]) & ~clash)
                if r[0] & r[1]: continue  # tautology
                if width(r) > w or r in S: continue
                if r == (0, 0): return True
                S.add(r); nxt.append(r); Sl.append(r)
        new = nxt
    return False

def gauss_rowops(edges, V, inc, charge):
    rows = []
    for v in V:
        m = 0
        for x in inc[v]: m |= 1 << x
        rows.append([m, charge[v]])
    ops = 0; r = 0
    for col in range(len(edges)):
        piv = next((i for i in range(r, len(rows)) if rows[i][0] >> col & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][0] >> col & 1:
                rows[i][0] ^= rows[r][0]; rows[i][1] ^= rows[r][1]; ops += 1
        r += 1
    inconsistent = any(m == 0 and b == 1 for m, b in rows)
    return ops, inconsistent

def main():
    # usage: script OUT.json GRAPHNAME   (one graph per invocation = one chunk; total cap 25 s)
    name = sys.argv[2]; E = graphs()[name]; cap = time.time() + 25
    out = {'source': 'experiments/claude_wr/tseitin_width_vs_gauss.py', 'total_cap_seconds': 25, 'graphs': {}}
    if True:
        V, inc, ch, cl = tseitin(E)
        t0 = time.time(); wstar = None; trace = []
        w0 = max(width(c) for c in cl)
        for w in range(w0, len(E) + 1):
            res = derives_empty(cl, w, cap)
            trace.append([w, res])
            if res is None: break
            if res: wstar = w; break
        ops, inc_ok = gauss_rowops(E, V, inc, ch)
        out['graphs'][name] = {'vertices': len(V), 'edges_vars': len(E), 'clauses': len(cl),
            'initial_width': w0, 'width_trace': trace, 'min_res_width': wstar,
            'min_res_width_lower_bound': (wstar if wstar else max([t[0]+1 for t in trace if t[1] is False] or [w0])),
            'gauss_row_xors': ops, 'gauss_detects_unsat': inc_ok, 'seconds': round(time.time() - t0, 3)}
        print(name, out['graphs'][name], flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1)

if __name__ == '__main__': main()
