#!/usr/bin/env python3
"""Exact B2 circuit-size synthesis via SAT (Kojevnikov-Kulikov-Yaroslavtsev style).
Usage: exact_synth.py FAMILY n r   -> prints JSON {family,n,inputs,r,result}
FAMILY: unit (unit clauses only, 2n inputs) | w2 (all nonempty clauses of width<=2)
Result SAT => size<=r circuit exists (verified by simulation); UNSAT => no size-r circuit
(so no smaller either, since a gate may be a copy of a wire).  Single call is meant to run <=30s."""
import sys, json, itertools, time
from pysat.solvers import Cadical153

def clauses_of(family, n):
    lits = [(v, s) for v in range(n) for s in (0, 1)]  # s=1: positive
    cl = [(l,) for l in lits]
    if family == "w2":
        cl += [(a, b) for a, b in itertools.combinations(lits, 2) if a[0] != b[0]]
    return cl

def sat_fn(cl, n):
    N = len(cl); tt = []
    for row in range(1 << N):
        sel = [cl[i] for i in range(N) if row >> i & 1]
        ok = any(all(any(((a >> v) & 1) == s for v, s in c) for c in sel) for a in range(1 << n))
        tt.append(1 if ok else 0)
    return tt

def synth(tt, N, r):
    R = len(tt); top = N + r; cnt = [0]
    def nv(): cnt[0] += 1; return cnt[0]
    x = {}
    for i in range(N, top):
        for t in range(R): x[i, t] = nv()
    f = {(i, p, q): nv() for i in range(N, top) for p in (0, 1) for q in (0, 1)}
    s = {(i, j, k): nv() for i in range(N, top) for j in range(i) for k in range(j + 1, i)}
    C = []
    def val(j, t):  # literal true-ness of node j on row t: returns (const or var)
        return (t >> j) & 1 if j < N else None
    for i in range(N, top):
        C.append([s[i, j, k] for j in range(i) for k in range(j + 1, i)])
        # every gate except the last must be used
        if i < top - 1:
            C.append([s[g, j, k] for g in range(i + 1, top) for j in range(g) for k in range(j + 1, g) if i in (j, k)])
        for j in range(i):
            for k in range(j + 1, i):
                for t in range(R):
                    for p in (0, 1):
                        for q in (0, 1):
                            c = [-s[i, j, k]]
                            ok = True
                            for node, bit in ((j, p), (k, q)):
                                if node < N:
                                    if ((t >> node) & 1) != bit: ok = False
                                else:
                                    c.append(-x[node, t] if bit else x[node, t])
                            if not ok: continue
                            c1 = c + [-f[i, p, q], x[i, t]]
                            c2 = c + [f[i, p, q], -x[i, t]]
                            C += [c1, c2]
    for t in range(R):
        C.append([x[top - 1, t] if tt[t] else -x[top - 1, t]])
    S = Cadical153(bootstrap_with=C)
    ok = S.solve()
    if not ok: return False
    m = set(l for l in S.get_model() if l > 0)
    # verify by simulation
    gates = {}
    for i in range(N, top):
        (j, k), = [(j, k) for (ii, j, k), v in s.items() if ii == i and v in m]
        tab = {(p, q): int(f[i, p, q] in m) for p in (0, 1) for q in (0, 1)}
        gates[i] = (j, k, tab)
    for t in range(R):
        v = {j: (t >> j) & 1 for j in range(N)}
        for i in range(N, top):
            j, k, tab = gates[i]; v[i] = tab[v[j], v[k]]
        assert v[top - 1] == tt[t], "simulation mismatch"
    return True

if __name__ == "__main__":
    fam, n, r = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    cl = clauses_of(fam, n); N = len(cl)
    t0 = time.time(); res = synth(sat_fn(cl, n), N, r)
    print(json.dumps({"family": fam, "n": n, "inputs": N, "r": r, "size_le_r_exists": res, "secs": round(time.time() - t0, 2)}))
