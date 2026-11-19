#!/usr/bin/env python3
"""Seeded min-conflicts/tabu local search collecting ONE-FALSE assignments for the native
strict-C 150/176 girth-10 source: complete Z5 assignments violating exactly one physical
clause j.  Such an assignment certifies that j is necessary in F (F - j is SAT), hence j
belongs to every UNSAT subformula of F that... (precisely: j lies in every UNSAT subset
S of F, because S - j is a subset of the satisfiable F - j).  Every recorded witness is
re-verified directly on the original predicate.  Resumable: merges into onefalse.json.

Usage: python3.13 -I strict_c_girth10_onefalse_search.py SEED SECONDS
"""
import importlib.util
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mus", os.path.join(HERE, "strict_c_girth10_core_mus.py"))
mus = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mus)
C = mus.C


def main():
    seed, secs = int(sys.argv[1]), float(sys.argv[2])
    n, clauses, sha = mus.source()
    m = len(clauses)
    occ = [[] for _ in range(n)]
    for j, t in enumerate(clauses):
        for v in t:
            occ[v].append(j)
    rng = random.Random(seed)
    w = [rng.randrange(5) for _ in range(n)]
    sat = [C(*(w[v] for v in t)) for t in clauses]
    false = set(j for j in range(m) if not sat[j])
    tabu = [0] * n
    path = os.path.join(mus.OUT, "onefalse.json")
    os.makedirs(mus.OUT, exist_ok=True)
    rec = json.load(open(path)) if os.path.exists(path) else {"source_sha256": sha, "witness": {}, "runs": []}
    found = rec["witness"]
    t0 = time.time()
    steps = 0
    best = m
    while time.time() - t0 < secs:
        steps += 1
        if len(false) == 1:
            j = next(iter(false))
            if str(j) not in found:
                assert all(C(*(w[v] for v in clauses[k])) for k in range(m) if k != j)
                assert not C(*(w[v] for v in clauses[j]))
                found[str(j)] = list(w)
        if len(false) == 0:
            raise SystemExit("SAT assignment found: contradicts prior UNSAT classification")
        best = min(best, len(false))
        j = rng.choice(tuple(false))
        bestd, moves = None, []
        for v in clauses[j]:
            if tabu[v] > steps:
                continue
            old = w[v]
            for c in range(5):
                if c == old:
                    continue
                w[v] = c
                d = 0
                for k in occ[v]:
                    d += (not C(*(w[u] for u in clauses[k]))) - (not sat[k])
                if bestd is None or d < bestd:
                    bestd, moves = d, [(v, c)]
                elif d == bestd:
                    moves.append((v, c))
            w[v] = old
        if not moves or rng.random() < 0.05:
            v = rng.choice(clauses[j])
            c = rng.randrange(5)
        else:
            v, c = rng.choice(moves)
        w[v] = c
        tabu[v] = steps + 3
        for k in occ[v]:
            sat[k] = C(*(w[u] for u in clauses[k]))
            if sat[k]:
                false.discard(k)
            else:
                false.add(k)
    rec["runs"].append({"seed": seed, "seconds": secs, "steps": steps, "best_false": best,
                        "covered_after": len(found)})
    json.dump(rec, open(path, "w"), sort_keys=True)
    print(f"seed={seed} steps={steps} best={best} covered={len(found)}/{m}")


if __name__ == "__main__":
    main()
