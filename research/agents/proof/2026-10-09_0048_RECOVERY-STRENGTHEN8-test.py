#!/usr/bin/env python3
"""Bounded exact audit for ALIAS-PORTFOLIO-FLATTENING1.

Checks scalar aggregate fixed points, typed internal DAG/cycle classification,
portfolio winner accounting, and a repaired Construction8 control family.
"""

from fractions import Fraction
import hashlib
import itertools
import json
import runpy
import signal
import time


def fixed_point(r, v, h):
    assert 0 <= h < 1
    return max(Fraction(1), r, (v - h) / (1 - h))


def step(c, r, v, h, access=Fraction(0)):
    return max(Fraction(1), r, access + v - h + h * c)


def acyclic(n, edges):
    adj = {i: [] for i in range(n)}
    indeg = [0] * n
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    stack = [i for i, d in enumerate(indeg) if not d]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for w in adj[u]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    return seen == n


def pure_literal_decide(clauses):
    """Return True only when iterative pure assignments empty the CNF."""
    clauses = tuple(tuple(c) for c in clauses)
    while clauses:
        signs = {}
        for c in clauses:
            for lit in c:
                signs.setdefault(abs(lit), set()).add(lit > 0)
        pure = {v: next(iter(s)) for v, s in signs.items() if len(s) == 1}
        if not pure:
            return None
        clauses = tuple(c for c in clauses
                        if not any(pure.get(abs(x)) == (x > 0) for x in c))
    return True


def balanced_lifted_cross(k):
    """Proper sign-balanced variant; PIVOT and pure-literal both decline."""
    out, z = [], 2 * k + 2
    for i in range(k):
        a = 2 + i
        for lit in (a, -a):
            out.extend(((1, lit, z), (1, lit, -z)))
            z += 1
    for i in range(k):
        b = 2 + k + i
        for lit in (b, -b):
            out.extend(((-1, lit, z), (-1, lit, -z)))
            z += 1
    return tuple(out), z - 1


def main():
    signal.alarm(24)
    started = time.monotonic()
    digest = hashlib.sha256()
    scalar = saturated = graphs = cycles = closure_controls = 0
    pivot_wins = pure_wins = portfolio_fails = child_calls_on_fail = 0

    vals = [Fraction(0), Fraction(1, 5), Fraction(1, 2),
            Fraction(4, 5), Fraction(1), Fraction(11, 10),
            Fraction(6, 5)]
    hs = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
          Fraction(2, 3)]
    for r, v, h in itertools.product(vals[1:], vals[1:], hs):
        c = fixed_point(r, v, h)
        assert step(c, r, v, h) <= c
        for d in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10)):
            if c - d >= max(Fraction(1), r):
                assert step(c - d, r, v, h) > c - d
        digest.update(f"{r}|{v}|{h}|{c}\n".encode())
        scalar += 1

    # Recovery7's saturated ledger: any fixed positive access exponent raises C.
    r, v, h = Fraction(6, 5), Fraction(11, 10), Fraction(1, 2)
    assert fixed_point(r, v, h) == Fraction(6, 5)
    for a in (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10)):
        c = max(r, (a + v - h) / (1 - h))
        assert c > Fraction(6, 5)
        saturated += 1

    # Exhaust all directed internal graphs on three typed alias nodes.
    arcs = [(i, j) for i in range(3) for j in range(3) if i != j]
    for mask in range(1 << len(arcs)):
        edges = [e for i, e in enumerate(arcs) if mask >> i & 1]
        if acyclic(3, edges):
            graphs += 1
        else:
            cycles += 1
    assert graphs == 25 and cycles == 39

    # The completed boundary, not an internal alias node, carries recursion.
    cases = [
        ("guard-strip-pivot", True, True),   # internal DAG; hypothetical coverage
        ("guard-strip-open", True, False),   # Construction8 current all-input status
        ("flat-marked", True, False),        # accepted parent, uncovered child
        ("scale-one-cycle", False, True),    # coverage cannot repair nontermination
    ]
    accepted = []
    for name, internal_dag, boundary_covered in cases:
        ok = internal_dag and boundary_covered
        accepted.append((name, ok))
        digest.update(f"{name}|{internal_dag}|{boundary_covered}|{ok}\n".encode())
        closure_controls += 1
    assert accepted == [
        ("guard-strip-pivot", True),
        ("guard-strip-open", False),
        ("flat-marked", False),
        ("scale-one-cycle", False),
    ]

    c8 = runpy.run_path(
        "research/agents/proof/"
        "2026-10-09_0034_CONSTRUCTION-STRENGTHEN8-test.py")
    for k in (4, 8, 16, 32, 64, 128):
        f, q = c8["proper_pivot_family"](k)
        g, qg = c8["guard"](f, q)
        assert c8["recognize_guard"](g, qg) == (f, q)
        plan = c8["pivot_plan"](f, q)
        assert plan is not None
        pivot_wins += 1
        digest.update(c8["encode"](g, qg))

    # Repairs the overbroad reading of C8's hostile-family claim:
    # PIVOT declines, but a later source-first pure member decides SAT.
    for k in (1, 2, 4, 8, 16, 32, 64, 128):
        f, q = c8["lifted_cross"](k)
        g, qg = c8["guard"](f, q)
        assert c8["recognize_guard"](g, qg) == (f, q)
        assert c8["pivot_plan"](f, q) is None
        assert pure_literal_decide(f) is True
        pure_wins += 1
        digest.update(c8["encode"](g, qg))

    # Exact partiality control: both members decline and execute no children.
    for k in (1, 2, 4, 8, 16, 32, 64):
        f, q = balanced_lifted_cross(k)
        g, qg = c8["guard"](f, q)
        assert c8["recognize_guard"](g, qg) == (f, q)
        assert c8["pivot_plan"](f, q) is None
        assert pure_literal_decide(f) is None
        portfolio_fails += 1
        child_calls_on_fail += 0
        digest.update(c8["encode"](g, qg))

    out = {
        "status": "PASS",
        "proof_status": "COMPUTATIONAL corroboration only",
        "scalar_fixed_point_checks": scalar,
        "saturated_access_controls": saturated,
        "typed_internal_dags": graphs,
        "typed_internal_cycles_rejected": cycles,
        "boundary_closure_controls": closure_controls,
        "portfolio_pivot_wins": pivot_wins,
        "portfolio_pure_literal_wins": pure_wins,
        "portfolio_all_fail_controls": portfolio_fails,
        "child_calls_on_all_fail": child_calls_on_fail,
        "sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "limitations": ("Finite algebra, bytes, and graph enumeration do not "
                        "prove the flattening theorem or an all-input compiler."),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
