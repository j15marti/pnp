#!/usr/bin/env python3
"""Exact minimum Resolution refutation width for the same odd-charge Tseitin 3-CNFs.
Saturates all resolvents of width <= w (w = 3,4,...) until the empty clause appears.
Clause = (posmask, negmask).  One graph per invocation (< 30 s).
Usage: python3 tseitin_width.py GRAPHNAME OUT.json"""
import sys, json, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
from tseitin_tree_vs_gauss import GRAPHS, tseitin

def to_lits(m, cv):  # forbidden assignment -> clause that excludes it
    pos = m & ~cv; neg = m & cv   # var=0 forbidden -> literal x ; var=1 forbidden -> literal ~x
    return (pos, neg)

def refutable_in_width(n, clauses, w):
    S = set(clauses); frontier = list(S)
    while frontier:
        new = []
        cur = list(S)
        for (p1,n1) in frontier:
            for (p2,n2) in cur:
                clash = (p1 & n2) | (n1 & p2)
                if clash == 0 or clash & (clash-1): continue
                p = (p1|p2) & ~clash; q = (n1|n2) & ~clash
                if p & q: continue
                if bin(p|q).count("1") > w: continue
                c = (p,q)
                if c not in S:
                    if p == 0 and q == 0: return True
                    S.add(c); new.append(c)
        frontier = new
    return False

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    edges = GRAPHS[name]; nv = 1+max(max(e) for e in edges)
    cl = [to_lits(m,cv) for m,cv in tseitin(edges, [1]+[0]*(nv-1))]
    t0 = time.time(); w = 3
    while not refutable_in_width(len(edges), cl, w): w += 1
    res = dict(graph=name, min_resolution_width=w, seconds=round(time.time()-t0,2))
    json.dump(res, open(out,"w")); print(json.dumps(res))
