#!/usr/bin/env python3
"""Exact orbit-capacity certificate and full 12-variable SAT projection check.
Finite combinatorics only. No FLMV machine-resource measurements.
"""
import itertools
import json
import math
from fractions import Fraction

def choose(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0

def capacity(a, u, h, t, positive):
    if positive:
        return choose(3 - t, u) * choose(a - 3 + t, h)
    return choose(3 - t, u - t) * choose(a - 3 + t, h - (3 - t))

def construction():
    p = ["p0", "p1", "p2"]
    a = ["a" + str(i) for i in range(9)]
    positive = [tuple(p)]
    positive += [(p[0],a[0],a[1]), (p[1],a[2],a[3]), (p[2],a[4],a[5])]
    positive += [(a[0],a[6],a[7]), (a[1],a[6],a[8]),
                 (a[2],a[7],a[8]), (a[3],a[4],a[5])]
    negative = [(a[0],a[1],a[2]), (a[3],a[4],a[5])]
    negative += [(p[0],a[0],a[6]), (p[0],a[1],a[7]),
                 (p[1],a[2],a[8]), (p[1],a[3],a[6]),
                 (p[2],a[4],a[7]), (p[2],a[5],a[8])]
    return p, a, positive, negative

def main():
    a = 9
    counts = {"P0":4,"P1":3,"P2":0,"P3":0,
              "N0":2,"N1":6,"N2":0,"N3":0}
    assert sum(t * counts["P"+str(t)] for t in range(4)) == 3
    assert sum(t * counts["N"+str(t)] for t in range(4)) == 6
    assert sum((3-t) * counts["P"+str(t)] for t in range(4)) == 18
    assert sum((3-t) * counts["N"+str(t)] for t in range(4)) == 18

    ratios = {}
    for u in (1,2):
        for h in range(10):
            numer = sum(counts["P"+str(t)] * capacity(a,u,h,t,True)
                      + counts["N"+str(t)] * capacity(a,u,h,t,False)
                        for t in range(4))
            denom = 3 * choose(a,h)
            ratios["u"+str(u)+"_h"+str(h)] = {
                "capacity":numer, "orbit_count":denom,
                "ratio":str(Fraction(numer,denom))}
    minratio = min(Fraction(x["ratio"]) for x in ratios.values())
    assert minratio == Fraction(83,63)
    assert ratios["u1_h5"]["ratio"] == "83/63"

    p, aux, positive, negative = construction()
    names = p + aux
    assert len(positive) == len(negative) == 8
    assert len({frozenset(c) for c in positive}) == 8
    assert len({frozenset(c) for c in negative}) == 8
    signed_degrees = {v:[0,0] for v in names}
    for sign, clauses in enumerate((positive,negative)):
        for clause in clauses:
            assert len(clause) == len(set(clause)) == 3
            for v in clause: signed_degrees[v][sign] += 1
    assert all(x == [2,2] for x in signed_degrees.values())
    negative_supports = {frozenset(c) for c in negative}
    assert any(frozenset(c) not in negative_supports for c in positive)

    models = {}
    inner_models = {}
    for bits in itertools.product((0,1), repeat=len(names)):
        x = dict(zip(names,bits))
        if all(any(not x[v] for v in c) for c in negative) and \
           all(any(x[v] for v in c) for c in positive[1:]):
            port = "".join(str(x[v]) for v in p)
            inner_models[port] = inner_models.get(port,0)+1
            if any(x[v] for v in positive[0]):
                models[port] = models.get(port,0)+1
    assert len(inner_models) == 8
    assert sum(models.values()) == 331
    assert models == {"001":60,"010":79,"011":32,"100":61,
                      "101":40,"110":41,"111":18}
    result = {"status":"COMPUTATIONAL exact finite check",
              "a":a, "minimum_ratio":str(minratio),
              "histogram":counts,"orbit_ratios":ratios,
              "k":12,"m":16,"full_sat_models":sum(models.values()),
              "full_port_counts":models,"inner_port_counts":inner_models,
              "caution":"Not an equality gadget; no machine-time lower bound."}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__ == "__main__":
    main()
