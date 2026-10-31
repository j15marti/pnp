#!/usr/bin/env python3
"""Source-only RUP and guard checks for NONMONOTONE-GUARDED-CACHE267.
This compact control is distinct from the full 15-source producer/verifier in
the archive. It uses no external dependencies, SAT libraries or answer oracle.
"""
from itertools import product


def up(clauses, assumptions=()):
    a = {}
    for lit in assumptions:
        v, b = abs(lit), lit > 0
        if v in a and a[v] != b:
            return None
        a[v] = b
    while True:
        changed = False
        for clause in clauses:
            vals = [a.get(abs(l)) == (l > 0) if abs(l) in a else None
                    for l in clause]
            if True in vals:
                continue
            unknown = [lit for lit, v in zip(clause, vals) if v is None]
            if not unknown:
                return None
            if len(unknown) == 1:
                lit = unknown[0]
                v, b = abs(lit), lit > 0
                if v in a and a[v] != b:
                    return None
                if v not in a:
                    a[v] = b
                    changed = True
        if not changed:
            return a


def rup(source, clause):
    return up(source, [-lit for lit in clause]) is None


def sat_models(source, n):
    return [
        bits for bits in product((0, 1), repeat=n)
        if all(any(bool(bits[abs(lit)-1]) == (lit > 0)
                   for lit in c) for c in source)
    ]


def assert_guard(source, decisions, guard, learned, n):
    assert set(guard) <= set(decisions)
    assert rup(source, learned)
    assert all(any(bool(bits[abs(lit)-1]) == (lit > 0)
                   for lit in learned)
               for bits in sat_models(source, n))


def demo():
    # (-a or b) and (-b or c); d is an unconstrained variable.
    f = [(-1, 2), (-2, 3)]
    assert up(f, [1, -4])[3]
    assert up(f, [1, 4])[3]  # incomparable branch, a-guard survives
    assert not up(f, [-1, 4]).get(3, False)
    learned = (-1, 3)
    assert_guard(f, [1, -4], [1], learned, 4)
    assert rup(f, learned)
    assert not rup([(-1, 2)], learned)   # deleted source reason
    assert rup(f + [(4,)], learned)      # source additions are safe

    # Independent SAT/UNSAT controls from exactly the same source grammar.
    cube = []
    for bits in product((0, 1), repeat=3):
        cube.append(tuple(-(i+1) if bit else i+1
                          for i, bit in enumerate(bits)))
    sat, unsat = cube[:-1], cube
    assert len(sat_models(sat, 3)) == 1
    assert len(sat_models(unsat, 3)) == 0
    for clauses in (sat, unsat):
        for c in clauses:
            assert rup(clauses, c)
    print("PASS: source-RUP, nonmonotone guard, invalidation, same-source SAT and UNSAT")


if __name__ == "__main__":
    demo()
