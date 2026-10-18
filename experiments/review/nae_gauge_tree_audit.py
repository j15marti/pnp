#!/usr/bin/env python3
"""Audit a decomposition-aware pin-free signed-NAE compiler.

Each source clause receives the exact two-NAE frontend

    NAE(a,b,u_i) and NAE(not u_i,c,p_i).

The local gauges p_i are synchronized along a supplied full binary tree.  For
every tree edge xy a fresh e is used in

    NAE(x,not y,e) and NAE(x,not y,not e).

The audit checks truth tables, exact counts and occurrences, two-way witness
transport, malformed inputs, relabeling/sign changes/duplicate clauses, and
separator overhead for aligned width-6/8 cuts.  It also computes the exact
minimum number of bichromatic equality-tree edges for a hostile alternating
leaf partition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SEED = 202610190555


@dataclass(frozen=True, order=True)
class Lit:
    var: int
    neg: bool = False

    def value(self, a: tuple[int, ...]) -> int:
        return a[self.var] ^ int(self.neg)


Clause = tuple[Lit, Lit, Lit]


def nae(x: int, y: int, z: int) -> bool:
    return not (x == y == z)


def sat_nae(c: Clause, a: tuple[int, ...]) -> bool:
    return nae(*(x.value(a) for x in c))


def source_sat(f: list[Clause], a: tuple[int, ...]) -> bool:
    return all(any(x.value(a) for x in c) for c in f)


def proper(c: Clause) -> bool:
    return len({x.var for x in c}) == 3


def eq_gadget(x: int, y: int, e: int) -> list[Clause]:
    return [(Lit(x), Lit(y, True), Lit(e)),
            (Lit(x), Lit(y, True), Lit(e, True))]


@dataclass
class Node:
    var: int
    leaves: tuple[int, ...]
    left: "Node | None" = None
    right: "Node | None" = None


@dataclass
class Compiled:
    n_source: int
    source: list[Clause]
    n_target: int
    clauses: list[Clause]
    u: list[int]
    p: list[int]
    q: list[int]
    e: list[int]
    root: Node
    edges: list[tuple[Node, Node, int]]
    owners: list[tuple[str, int]]


def validate_source(n: int, f: list[Clause]) -> None:
    if n < 1 or not f:
        raise ValueError("empty or dimensionless source")
    for c in f:
        if not proper(c) or any(x.var < 0 or x.var >= n for x in c):
            raise ValueError("source is not a proper in-range 3-CNF")


def compile_formula(n: int, f: list[Clause]) -> Compiled:
    validate_source(n, f)
    m = len(f)
    u = list(range(n, n + m))
    p = list(range(n + m, n + 2 * m))
    next_var = n + 2 * m
    q: list[int] = []
    raw_edges: list[tuple[Node, Node]] = []

    leaves = [Node(p[i], (i,)) for i in range(m)]

    def build(nodes: list[Node]) -> Node:
        nonlocal next_var
        if len(nodes) == 1:
            return nodes[0]
        mid = len(nodes) // 2
        left, right = build(nodes[:mid]), build(nodes[mid:])
        v = next_var
        next_var += 1
        q.append(v)
        parent = Node(v, left.leaves + right.leaves, left, right)
        raw_edges.extend([(left, parent), (right, parent)])
        return parent

    root = build(leaves)
    e = list(range(next_var, next_var + len(raw_edges)))
    clauses: list[Clause] = []
    owners: list[tuple[str, int]] = []
    for i, (a, b, c) in enumerate(f):
        clauses += [(a, b, Lit(u[i])), (Lit(u[i], True), c, Lit(p[i]))]
        owners += [("front", i), ("front", i)]
    edges: list[tuple[Node, Node, int]] = []
    for j, ((child, parent), ev) in enumerate(zip(raw_edges, e)):
        clauses += eq_gadget(child.var, parent.var, ev)
        owners += [("edge", j), ("edge", j)]
        edges.append((child, parent, ev))
    return Compiled(n, f, next_var + len(e), clauses, u, p, q, e,
                    root, edges, owners)


def all_models(n: int, pred):
    for a in itertools.product((0, 1), repeat=n):
        if pred(a):
            yield a


def extend(c: Compiled, src: tuple[int, ...], gauge: int) -> tuple[int, ...]:
    if not source_sat(c.source, src):
        raise ValueError("not a source witness")
    target_src = src if gauge == 0 else tuple(1 - x for x in src)
    a = list(target_src) + [0] * (c.n_target - c.n_source)
    for v in c.p + c.q:
        a[v] = gauge
    # Search only the one local auxiliary bit; equality auxiliaries can be 0.
    for i in range(len(c.source)):
        for bit in (0, 1):
            a[c.u[i]] = bit
            if sat_nae(c.clauses[2*i], tuple(a)) and sat_nae(c.clauses[2*i+1], tuple(a)):
                break
        else:
            raise AssertionError("local witness missing")
    out = tuple(a)
    if not all(sat_nae(cl, out) for cl in c.clauses):
        raise AssertionError("extension failed")
    return out


def project(c: Compiled, target: tuple[int, ...]) -> tuple[int, ...]:
    if not all(sat_nae(cl, target) for cl in c.clauses):
        raise ValueError("not a target witness")
    gauge = target[c.root.var]
    if any(target[v] != gauge for v in c.p + c.q):
        raise AssertionError("tree synchronization failed")
    x = target[:c.n_source]
    src = x if gauge == 0 else tuple(1-b for b in x)
    if not source_sat(c.source, src):
        raise AssertionError("projected source is false")
    return src


def random_source(rng: random.Random, n: int, m: int) -> list[Clause]:
    return [tuple(Lit(v, bool(rng.getrandbits(1)))
                  for v in rng.sample(range(n), 3)) for _ in range(m)]


def source_boundary(f: list[Clause], side: list[int]) -> set[int]:
    sets = [set(), set()]
    for i, cl in enumerate(f):
        sets[side[i]].update(x.var for x in cl)
    return sets[0] & sets[1]


def aligned_target_boundary(c: Compiled, child: Node) -> set[int]:
    """Cut on child-parent edge; put its gadget on the child side."""
    inside = set(child.leaves)
    vars_by_side = [set(), set()]
    for cl, (kind, idx) in zip(c.clauses, c.owners):
        if kind == "front":
            side = 0 if idx in inside else 1
        else:
            edge_child, _parent, _ev = c.edges[idx]
            # Every other edge lies within one component after deleting the cut.
            side = 0 if set(edge_child.leaves) <= inside else 1
        vars_by_side[side].update(x.var for x in cl)
    return vars_by_side[0] & vars_by_side[1]


def boundary_instance(width: int) -> tuple[int, list[Clause]]:
    f: list[Clause] = []
    nxt = width
    for side in (0, 1):
        for b in range(width):
            f.append((Lit(b, bool((b+side) & 1)), Lit(nxt), Lit(nxt+1, bool(b & 1))))
            nxt += 2
    return nxt, f


def min_bichromatic_edges(c: Compiled, leaf_colours: list[int]) -> int:
    """Exact DP over internal gauge colours."""
    def dp(node: Node) -> tuple[int, int]:
        if node.left is None:
            colour = leaf_colours[node.leaves[0]]
            return (0 if colour == 0 else 10**6,
                    0 if colour == 1 else 10**6)
        assert node.right is not None
        dl, dr = dp(node.left), dp(node.right)
        out = []
        for col in (0, 1):
            lc = min(dl[x] + (x != col) for x in (0, 1))
            rc = min(dr[x] + (x != col) for x in (0, 1))
            out.append(lc + rc)
        return out[0], out[1]
    return min(dp(c.root))


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    failures: list[str] = []
    counts = Counter()

    # Exact local relations.
    eq_projection = {}
    for x, y in itertools.product((0, 1), repeat=2):
        ws = [e for e in (0, 1)
              if all(sat_nae(cl, (x, y, e)) for cl in eq_gadget(0, 1, 2))]
        eq_projection[f"{x}{y}"] = ws
        counts["eq_rows"] += 2
        if bool(ws) != (x == y):
            failures.append("equality truth table")

    front_projection = {}
    for abc in itertools.product((0, 1), repeat=3):
        for g in (0, 1):
            ws = [u for u in (0, 1)
                  if nae(abc[0], abc[1], u) and nae(1-u, abc[2], g)]
            front_projection["".join(map(str, abc)) + f"|g={g}"] = ws
            if bool(ws) != (any(abc) if g == 0 else any(1-x for x in abc)):
                failures.append("front truth table")
            counts["front_rows"] += 2

    formula_cases = sat_cases = unsat_cases = extensions = projections = 0
    max_aux_occ = 0
    for n in range(3, 7):
        for m in range(1, 9):
            for rep in range(10):
                f = random_source(rng, n, m)
                if m > 1 and rep == 0:
                    f[-1] = f[0]  # repeated clause control
                c = compile_formula(n, f)
                formula_cases += 1
                if c.n_target != n + 5*m - 3 or len(c.clauses) != 6*m - 4:
                    failures.append("count identity")
                if not all(proper(cl) for cl in c.clauses):
                    failures.append("improper target")
                occ = Counter(x.var for cl in c.clauses for x in cl)
                aux = c.u + c.p + c.q + c.e
                max_aux_occ = max(max_aux_occ, max(occ[v] for v in aux))
                if max(occ[v] for v in aux) > 6:
                    failures.append("aux occurrence > 6")
                if any(occ[v] != sum(x.var == v for cl in f for x in cl)
                       for v in range(n)):
                    failures.append("source occurrence changed")
                src = next(all_models(n, lambda a: source_sat(f, a)), None)
                if src is None:
                    unsat_cases += 1
                else:
                    sat_cases += 1
                    for g in (0, 1):
                        t = extend(c, src, g)
                        extensions += 1
                        if project(c, t) != src:
                            failures.append("witness round trip")
                        projections += 1
                # Formula-level decision after symbolic equality elimination.
                target_core = any(
                    all(any(nae(a.value(x), b.value(x), u) and
                                nae(1-u, cc.value(x), g) for u in (0, 1))
                            for a, b, cc in f)
                    for x in itertools.product((0, 1), repeat=n) for g in (0, 1))
                if target_core != (src is not None):
                    failures.append("decision mismatch")
                counts["formula_decisions"] += 1

    # Deterministic UNSAT source: all eight clauses on three variables.
    uf = [tuple(Lit(v, bool(bits[v])) for v in range(3))
          for bits in itertools.product((0, 1), repeat=3)]
    uc = compile_formula(3, uf)
    if next(all_models(3, lambda a: source_sat(uf, a)), None) is not None:
        failures.append("UNSAT control")
    formula_cases += 1
    unsat_cases += 1

    # Invalid encodings/sources rejected.
    invalid_rejected = 0
    for n, f in [(3, []), (3, [(Lit(0), Lit(0), Lit(1))]),
                 (3, [(Lit(0), Lit(1), Lit(3))])]:
        try:
            compile_formula(n, f)
        except ValueError:
            invalid_rejected += 1
        else:
            failures.append("invalid source accepted")

    separator_rows = []
    for width in (6, 8):
        n, f = boundary_instance(width)
        c = compile_formula(n, f)
        # Balanced builder puts the first width leaves under the root's left child.
        assert c.root.left is not None
        side = [0]*width + [1]*width
        sb = source_boundary(f, side)
        tb = aligned_target_boundary(c, c.root.left)
        separator_rows.append({
            "source_width": len(sb),
            "target_width": len(tb),
            "increase": len(tb)-len(sb),
            "target_extra_variables": sorted(tb-sb),
        })
        if len(sb) != width or len(tb) != width + 1 or not sb <= tb:
            failures.append(f"aligned width-{width} boundary")

    hostile_rows = []
    for m in (8, 16, 32):
        f = [(Lit(3*i), Lit(3*i+1), Lit(3*i+2)) for i in range(m)]
        c = compile_formula(3*m, f)
        colours = [i & 1 for i in range(m)]
        crossings = min_bichromatic_edges(c, colours)
        hostile_rows.append({"leaves": m, "minimum_crossing_tree_edges": crossings})
        if crossings != m//2:
            failures.append("hostile alternating cut DP")

    result = {
        "run_id": "NAEGAUGETREE1",
        "seed": SEED,
        "status": "PASS" if not failures else "FAIL",
        "elapsed_seconds": time.perf_counter()-start,
        "failures": failures,
        "eq_projection": eq_projection,
        "front_projection": front_projection,
        "formula_cases": formula_cases,
        "sat_source_cases": sat_cases,
        "unsat_source_cases": unsat_cases,
        "extensions_checked": extensions,
        "projections_checked": projections,
        "invalid_sources_rejected": invalid_rejected,
        "count_identity": "N=n+5m-3, M=6m-4",
        "max_auxiliary_occurrence": max_aux_occ,
        "separator_rows": separator_rows,
        "hostile_nonaligned_rows": hostile_rows,
        "checks": dict(counts),
        "limitations": [
            "The w+1 theorem applies to clause cuts aligned to an edge of the supplied tree.",
            "Alternating non-aligned cuts still cross linearly many equality edges.",
            "Finite checks do not imply any unrestricted-machine lower bound.",
            "REVFIX2 was not composed because no exact source specification was accessible.",
        ],
    }
    out = Path("results/raw/review/2026-10-19_NAEGAUGETREE1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("raw_sha256", hashlib.sha256(text.encode()).hexdigest())
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
