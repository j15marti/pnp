#!/usr/bin/env python3
"""Exact minimum DAG-resolution refutation size (number of derived clauses) for tiny UNSAT CNFs.
Free-strategy-choice minimum: iterative deepening over SETS of derived clauses (BFS by size k).
Each run < 30 s; instances chunked by name argument. Strategy search cost is NOT charged (by design)."""
import sys, json, itertools, time
def res(a, b):
    out = []
    for l in a:
        if -l in b:
            c = (a - {l}) | (b - {-l})
            if not any(-x in c for x in c): out.append(frozenset(c))
    return out
def subsumed_reduce(c): return c
def min_dag(clauses, kmax=14, tlimit=25):
    base = [frozenset(c) for c in clauses]; t0 = time.time()
    # frontier: sets of derived clauses (canonical); minimal refutation has no useless clauses
    layer = {frozenset()}
    for k in range(1, kmax+1):
        nxt = set()
        for D in layer:
            pool = base + list(D)
            for i in range(len(pool)):
                for j in range(i+1, len(pool)):
                    for r in res(pool[i], pool[j]):
                        if r in D or r in base: continue
                        if not r: return k, time.time()-t0
                        nxt.add(D | {r})
            if time.time()-t0 > tlimit: return None, time.time()-t0
        layer = nxt
        if time.time()-t0 > tlimit: return None, time.time()-t0
    return None, time.time()-t0
def php(p, h):
    v = lambda i, j: i*h+j+1
    cl = [[v(i,j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for i in range(p):
            for i2 in range(i+1,p): cl.append([-v(i,j), -v(i2,j)])
    return cl
def xor_cycle(n):  # Tseitin on cycle C_n, odd total charge: x_i xor x_{i+1} = c_i
    cl=[]
    for i in range(n):
        a=i+1; b=(i+1)%n+1; c = 1 if i==0 else 0  # parity: sum c odd
        # a xor b = c
        if c: cl += [[a,b],[-a,-b]]
        else: cl += [[a,-b],[-a,b]]
    return cl
INST = {
 "all2": lambda: [[1,2],[1,-2],[-1,2],[-1,-2]],
 "PHP_3_2": lambda: php(3,2),
 "TseitinCycle3": lambda: xor_cycle(3),
 "TseitinCycle4": lambda: xor_cycle(4),
 "chain_unit_n3": lambda: [[1],[-1,2],[-2,3],[-3]],
}
if __name__ == "__main__":
    out = {}
    for name in sys.argv[1:]:
        k, t = min_dag(INST[name]())
        out[name] = {"min_derived_clauses": k, "seconds": round(t,2)}
    print(json.dumps(out))
