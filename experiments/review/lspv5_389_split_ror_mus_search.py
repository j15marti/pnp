#!/usr/bin/env python3
"""Exhaustive MUS split search with two private variables per side.

Enumerates width-at-most-two clause sets over {b,x1,x2} that minimally entail
b.  Pairs them with sign/variable-renamed copies minimally entailing not-b and
tests strict source-once Resolution on the union.  Every invocation is bounded
to a supplied maximum side size so stages can be checkpointed under 30 s.
"""

from __future__ import annotations

import argparse
import itertools
import json
import resource
import time
from functools import lru_cache
from pathlib import Path


def all_clauses(vars_, max_width):
    lits = [v for z in vars_ for v in (z, -z)]
    out = []
    for w in range(1, max_width + 1):
        for c in itertools.combinations(lits, w):
            if not any(-l in c for l in c):
                out.append(tuple(sorted(c)))
    return tuple(sorted(set(out), key=lambda c: (len(c), c)))


def models(formula, vars_):
    ans = []
    for bits in itertools.product((0, 1), repeat=len(vars_)):
        a = dict(zip(vars_, bits))
        if all(any(a[abs(l)] == (l > 0) for l in c) for c in formula):
            ans.append(a)
    return ans


def minimal_entails_b(formula, vars_):
    ms = models(formula, vars_)
    if not ms or any(m[1] == 0 for m in ms):
        return False
    for i in range(len(formula)):
        if not any(m[1] == 0 for m in models(formula[:i] + formula[i + 1 :], vars_)):
            return False
    return True


def resolve(a, b):
    vars_ = {abs(l) for l in a | b}
    ps = [v for v in vars_ if (v in a and -v in b) or (-v in a and v in b)]
    if len(ps) != 1:
        return None
    p = ps[0]
    r = (a | b) - {p, -p}
    if any(-l in r for l in r):
        return None
    return frozenset(r)


@lru_cache(maxsize=None)
def closure_tuple(sources_tuple):
    sources = tuple(frozenset(c) for c in sources_tuple)
    n = len(sources)
    dp = [set() for _ in range(1 << n)]
    for i, c in enumerate(sources):
        dp[1 << i].add(c)
    for size in range(2, n + 1):
        for mask in range(1, 1 << n):
            if mask.bit_count() != size:
                continue
            anchor = mask & -mask
            sub = (mask - 1) & mask
            while sub:
                other = mask ^ sub
                if other and sub & anchor:
                    for a in dp[sub]:
                        for b in dp[other]:
                            r = resolve(a, b)
                            if r is not None:
                                dp[mask].add(r)
                sub = (sub - 1) & mask
    return tuple(tuple(sorted(c)) for c in dp[-1])


def rename_right(formula):
    # b sign flips; left private 2,3 map to right private 4,5.
    def f(l):
        s = 1 if l > 0 else -1
        v = abs(l)
        if v == 1:
            return -s
        return s * (v + 2)
    return tuple(tuple(sorted(f(l) for l in c)) for c in formula)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-side", type=int, default=5)
    ap.add_argument("--max-width", type=int, default=2)
    ap.add_argument("--pair-limit", type=int, default=0)
    args = ap.parse_args()
    started = time.perf_counter()
    universe = all_clauses((1, 2, 3), args.max_width)
    pool = []
    enum_counts = {}
    for n in range(2, args.max_side + 1):
        count = 0
        for fs in itertools.combinations(universe, n):
            if minimal_entails_b(fs, (1, 2, 3)):
                full = closure_tuple(fs)
                pool.append((fs, (1,) in full, full))
                count += 1
        enum_counts[str(n)] = count

    pair_tests = 0
    witness = None
    # Test smaller combined sources first, then lexicographically.
    ordered = sorted(pool, key=lambda z: (len(z[0]), z[0]))
    for left, lunit, lout in ordered:
        for rbase, runit_pos, rout_pos in ordered:
            if lunit and runit_pos:
                continue
            pair_tests += 1
            right = rename_right(rbase)
            combined = left + right
            full = closure_tuple(combined)
            if () in full:
                witness = {
                    "left": left,
                    "right": right,
                    "left_unit": lunit,
                    "right_unit": runit_pos,
                    "left_full_outcomes": lout,
                    "right_base_full_outcomes": rout_pos,
                    "global_full_outcomes": full,
                }
                break
            if args.pair_limit and pair_tests >= args.pair_limit:
                break
        if witness is not None or (args.pair_limit and pair_tests >= args.pair_limit):
            break

    record = {
        "status": "COMPUTATIONAL",
        "scope": f"MUS split width<={args.max_width} CNF; two private variables per side; distinct clauses",
        "max_width": args.max_width,
        "max_side": args.max_side,
        "candidate_universe": len(universe),
        "minimal_entailing_pool": len(pool),
        "minimal_entailing_counts": enum_counts,
        "pair_tests": pair_tests,
        "pair_limit": args.pair_limit,
        "counterexample": witness,
        "wall_seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = Path(f"results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS389_w{args.max_width}_s{args.max_side}.json")
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
