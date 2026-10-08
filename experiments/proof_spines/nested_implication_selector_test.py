#!/usr/bin/env python3
"""Bounded exact tests for fixed-depth nested implication selection.

The implementation follows the r_k hierarchy: r_1 is unit propagation and
r_{k+1} repeatedly sets a literal l when r_k detects a contradiction after
setting l false.  This is a finite test harness, not asymptotic evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import signal
import time
from functools import lru_cache
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def canon(clauses) -> CNF:
    out = set()
    for raw in clauses:
        c = frozenset(raw)
        if any(-x in c for x in c):
            continue
        out.add(tuple(sorted(c, key=lambda x: (abs(x), x < 0))))
    return tuple(sorted(out, key=lambda c: (len(c), c)))


def set_lit(f: CNF, lit: int) -> CNF:
    out = []
    for c in f:
        if lit in c:
            continue
        out.append(tuple(x for x in c if x != -lit))
    return canon(out)


def unit_reduce(f: CNF):
    cur = f
    while True:
        if any(len(c) == 0 for c in cur):
            return cur, True
        unit = next((c[0] for c in cur if len(c) == 1), None)
        if unit is None:
            return cur, False
        cur = set_lit(cur, unit)


@lru_cache(maxsize=None)
def rk_conflict(f: CNF, k: int) -> bool:
    cur, bad = unit_reduce(f)
    if bad:
        return True
    if k <= 1 or not cur:
        return False
    while True:
        lits = sorted({x for c in cur for x in c} | {-x for c in cur for x in c},
                      key=lambda x: (abs(x), x < 0))
        forced = None
        for lit in lits:
            if rk_conflict(set_lit(cur, -lit), k - 1):
                forced = lit
                break
        if forced is None:
            return False
        cur, bad = unit_reduce(set_lit(cur, forced))
        if bad:
            return True


def implies_k(a: CNF, b: CNF, k: int) -> bool:
    for c in b:
        trial = a
        for lit in c:
            trial = set_lit(trial, -lit)
        if not rk_conflict(trial, k):
            return False
    return True


def eval_cnf(f: CNF, assignment: tuple[bool, ...]) -> bool:
    for c in f:
        if not any((lit > 0) == assignment[abs(lit) - 1] for lit in c):
            return False
    return True


def models(f: CNF, n: int):
    return {a for a in itertools.product((False, True), repeat=n) if eval_cnf(f, a)}


def sink_representatives(frontier: list[CNF], k: int):
    q = len(frontier)
    g = [[j for j in range(q) if i != j and implies_k(frontier[i], frontier[j], k)]
         for i in range(q)]
    index = 0
    stack = []
    on_stack = set()
    indices = [-1] * q
    low = [0] * q
    comps = []

    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in g[v]:
            if indices[w] < 0:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in range(q):
        if indices[v] < 0:
            visit(v)
    cid = {v: i for i, c in enumerate(comps) for v in c}
    sinks = []
    for i, c in enumerate(comps):
        if not any(cid[w] != i for v in c for w in g[v]):
            sinks.append(min(c))
    return sorted(sinks), g


def all_clauses(n: int, max_width=None):
    result = []
    max_width = n if max_width is None else max_width
    for states in itertools.product((-1, 0, 1), repeat=n):
        c = tuple((i + 1) * s for i, s in enumerate(states) if s)
        if c and len(c) <= max_width:
            result.append(c)
    return result


def random_cnf(rng, n, count, width, horn=False):
    clauses = []
    for _ in range(count):
        w = rng.randint(1, min(width, n))
        vs = rng.sample(range(1, n + 1), w)
        if horn:
            pos = rng.choice(vs + [None])
            clauses.append(tuple(v if v == pos else -v for v in vs))
        else:
            clauses.append(tuple(v if rng.randrange(2) else -v for v in vs))
    return canon(clauses)


def rename(f: CNF, perm, flips):
    return canon((perm[abs(x) - 1] * (1 if x > 0 else -1) * flips[abs(x) - 1]
                  for x in c) for c in f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=20261007)
    ap.add_argument("--budget", type=int, default=25)
    args = ap.parse_args()
    signal.alarm(args.budget)
    started = time.time()
    rng = random.Random(args.seed)
    checks = 0

    # Smallest standard strict witness searched by source clause count.
    a = canon([
        (1, 2, 3), (1, 2, -3), (1, -2, 3), (1, -2, -3), (4,)
    ])
    b = canon([(1,)])
    strict = {
        "k1_implies": implies_k(a, b, 1),
        "k2_implies": implies_k(a, b, 2),
        "semantic_implies": models(a, 4) <= models(b, 4),
    }
    assert strict == {"k1_implies": False, "k2_implies": True, "semantic_implies": True}
    k1_keep, _ = sink_representatives([a, b], 1)
    k2_keep, _ = sink_representatives([a, b], 2)
    assert k1_keep == [0, 1] and k2_keep == [1]
    strict.update(k1_retained=k1_keep, k2_retained=k2_keep)
    checks += 5

    # Exhaustive check that no <=3-clause source over three variables gives
    # this k=2-not-k=1 implication to a unit target.
    clauses3 = all_clauses(3)
    smaller_witnesses = 0
    exhaustive_sources = 0
    for size in range(1, 4):
        for cs in itertools.combinations(clauses3, size):
            f = canon(cs)
            exhaustive_sources += 1
            for lit in range(1, 4):
                target = canon([(lit,)])
                if implies_k(f, target, 2) and not implies_k(f, target, 1):
                    smaller_witnesses += 1
                target = canon([(-lit,)])
                if implies_k(f, target, 2) and not implies_k(f, target, 1):
                    smaller_witnesses += 1
    assert smaller_witnesses == 0
    checks += exhaustive_sources * 6

    random_stats = {"portfolios": 0, "edges_k1": 0, "edges_k2": 0, "k2_only": 0}
    for _ in range(160):
        n = rng.randint(2, 4)
        q = rng.randint(2, 6)
        fs = [random_cnf(rng, n, rng.randint(1, 7), 3) for _ in range(q)]
        allm = [models(f, n) for f in fs]
        for k in (1, 2):
            keep, g = sink_representatives(fs, k)
            union_before = set().union(*allm)
            union_after = set().union(*(allm[i] for i in keep))
            assert union_before == union_after
            checks += 1
            for i in range(q):
                for j in g[i]:
                    assert allm[i] <= allm[j]
                    checks += 1
                    random_stats[f"edges_k{k}"] += 1
        for i in range(q):
            for j in range(q):
                if i != j and implies_k(fs[i], fs[j], 2) and not implies_k(fs[i], fs[j], 1):
                    random_stats["k2_only"] += 1
        random_stats["portfolios"] += 1

    # UC_1 and UC_2 controls: all enumerated implicates of random Horn and
    # 2-CNF sources must be found at their known fixed levels.
    class_stats = {"horn_formulas": 0, "horn_implicates": 0,
                   "two_cnf_formulas": 0, "two_cnf_implicates": 0}
    for _ in range(90):
        n = rng.randint(2, 4)
        clauses = all_clauses(n)
        h = random_cnf(rng, n, rng.randint(1, 8), n, horn=True)
        hm = models(h, n)
        for c in clauses:
            target = canon([c])
            if hm <= models(target, n):
                assert implies_k(h, target, 1)
                class_stats["horn_implicates"] += 1
                checks += 1
        class_stats["horn_formulas"] += 1

        t = random_cnf(rng, n, rng.randint(1, 8), 2)
        tm = models(t, n)
        for c in clauses:
            target = canon([c])
            if tm <= models(target, n):
                assert implies_k(t, target, 2)
                class_stats["two_cnf_implicates"] += 1
                checks += 1
        class_stats["two_cnf_formulas"] += 1

    # Correct complete-assignment antichain: each residual is a conjunction
    # of unit clauses.  Every fixed-depth sound implication selector retains all.
    antichain = {}
    for n in range(1, 8):
        fs = [canon([((i + 1) if bit else -(i + 1),) for i, bit in enumerate(bits)])
              for bits in itertools.product((False, True), repeat=n)]
        for k in (1, 2):
            keep, g = sink_representatives(fs, k)
            assert len(keep) == len(fs)
            assert sum(map(len, g)) == 0
            checks += len(fs) * (len(fs) - 1)
        antichain[str(n)] = len(fs)

    # Padding and signed-renaming invariance.
    invariance = 0
    for _ in range(80):
        f = random_cnf(rng, 4, rng.randint(2, 7), 3)
        g = random_cnf(rng, 4, rng.randint(1, 5), 3)
        perm = rng.sample(range(1, 5), 4)
        flips = [rng.choice((-1, 1)) for _ in range(4)]
        for k in (1, 2):
            assert implies_k(f, g, k) == implies_k(rename(f, perm, flips), rename(g, perm, flips), k)
            padded = canon(list(f) + [(5, -5)])
            assert implies_k(f, g, k) == implies_k(padded, g, k)
            invariance += 2
            checks += 2

    out = {
        "claim": "NESTED-IMPLICATION-SELECT1",
        "status": "COMPUTATIONAL checks of a PROVED/EXACT fixed-k theorem",
        "seed": args.seed,
        "budget_seconds": args.budget,
        "elapsed_seconds": round(time.time() - started, 6),
        "checks": checks,
        "strict_k2_over_k1": strict,
        "minimality_search": {
            "variables": 3,
            "source_clause_count_at_most": 3,
            "sources": exhaustive_sources,
            "unit_targets_per_source": 6,
            "smaller_witnesses": smaller_witnesses,
        },
        "random_exact_frontiers": random_stats,
        "known_class_controls": class_stats,
        "complete_assignment_antichain_retained": antichain,
        "renaming_and_tautology_padding_checks": invariance,
        "current_scale_sat_calls": 0,
        "interpretation": "Fixed depth two strictly extends RUP and is complete on the tested Horn/2-CNF controls; exact pruning still has no universal density, and no asymptotic conclusion is inferred.",
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
