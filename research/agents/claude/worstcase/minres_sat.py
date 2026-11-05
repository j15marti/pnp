"""Exact minimum DAG-resolution refutation size via SAT (Peitl-Szeider style):
ask 'is there a refutation with exactly K derived clauses (last = empty)?' for K=1,2,...
Chunked: each (instance,K) call is an independent SAT call, global budget ~25s per invocation."""
import itertools, json, random, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType

def refutable_in(clauses, n, K):
    m = len(clauses); T = m + K
    vid = {}
    def v(*k):
        if k not in vid: vid[k] = len(vid) + 1
        return vid[k]
    lits = [l for x in range(1, n+1) for l in (x, -x)]
    S = Cadical153(); add = S.add_clause
    for t, c in enumerate(clauses):
        for l in lits: add([v('m', t, l)] if l in c else [-v('m', t, l)])
    for j in range(m, T):
        L = [v('L', j, i) for i in range(j)]; R = [v('R', j, i) for i in range(j)]
        P = [v('P', j, x) for x in range(1, n+1)]
        for grp in (L, R, P):
            add(grp)
            for a, b in itertools.combinations(grp, 2): add([-a, -b])
        for i in range(j):
            for k in range(j):
                if i == k:
                    add([-v("L", j, i), -v("R", j, k)]); continue
                for x in range(1, n+1):
                    pre = [-v('L', j, i), -v('R', j, k), -v('P', j, x)]
                    add(pre + [v('m', i, x)]); add(pre + [v('m', k, -x)])
                    for l in lits:
                        if abs(l) == x:
                            add(pre + [-v('m', j, l)]); continue
                        a, b, c = v('m', j, l), v('m', i, l), v('m', k, l)
                        add(pre + [-a, b, c]); add(pre + [a, -b]); add(pre + [a, -c])
    for j in range(m, T):
        for x in range(1, n+1): add([-v('m', j, x), -v('m', j, -x)])   # no tautologies
    for l in lits: add([-v('m', T-1, l)])
    r = S.solve(); S.delete(); return r

def min_refutation(clauses, n, kmax=30, deadline=None):
    for K in range(1, kmax+1):
        if deadline and time.time() > deadline: return None
        if refutable_in(clauses, n, K): return K
    return None
