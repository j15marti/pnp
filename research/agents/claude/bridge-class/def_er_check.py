"""Exhaustive check: every two-input extension of Extended Resolution is one DEF node of R_mix341.

For each of the 16 Boolean functions g(a,b) we build the Tseitin defining clauses of z <-> g(a,b)
(one clause per row of the truth table: (a!=va) v (b!=vb) v (z==g(va,vb))), and check
(1) conservativity/uniqueness: every (a,b) has exactly one z satisfying all clauses, equal to g(a,b);
(2) Cook's ER extension z <-> (l1 AND l2), for all 4 literal sign patterns, is one of the 16 gates.
The inequality W_mix(F) <= L_ER(F) itself is structural (each ER line maps to at most one paid
node) and is proved in the report, not tested here. Runs in < 1 s.
"""
import itertools, json, sys

def clauses(g):
    cl = []
    for va, vb in itertools.product((0, 1), repeat=2):
        out = g[(va, vb)]
        cl.append(((0, 1 - va), (1, 1 - vb), (2, out)))  # (var index, required value) literals
    return cl

def sat(cl, asg):
    return all(any(asg[v] == val for v, val in c) for c in cl)

checks = 0
gates = []
for bits in itertools.product((0, 1), repeat=4):
    g = dict(zip(itertools.product((0, 1), repeat=2), bits))
    cl = clauses(g)
    for va, vb in itertools.product((0, 1), repeat=2):
        zs = [z for z in (0, 1) if sat(cl, (va, vb, z))]
        assert zs == [g[(va, vb)]], (bits, va, vb, zs)
        checks += 1
    gates.append(bits)

for s1, s2 in itertools.product((0, 1), repeat=2):  # l1 = a if s1 else not a
    bits = tuple(int((va if s1 else 1 - va) and (vb if s2 else 1 - vb))
                 for va, vb in itertools.product((0, 1), repeat=2))
    assert bits in gates
    checks += 1

res = {"gates": len(gates), "checks": checks, "status": "PASS"}
json.dump(res, sys.stdout); print()
