#!/usr/bin/env python3
"""Test split MUS gadgets obtained by weakening a known non-ROR MU formula."""

from __future__ import annotations

import itertools
import json
import resource
import time
from pathlib import Path


BASE = (
    (2, 3),
    (4, 5),
    (-2, -4),
    (-2, -5),
    (-3, -4),
    (-3, -5),
)


def resolve(a, b):
    ps = [v for v in {abs(l) for l in a | b}
          if (v in a and -v in b) or (-v in a and v in b)]
    if len(ps) != 1:
        return None
    p = ps[0]
    r = (a | b) - {p, -p}
    if any(-l in r for l in r):
        return None
    return frozenset(r)


def closure(sources, keep_trace=False):
    n = len(sources)
    dp = [dict() for _ in range(1 << n)]
    for i, c in enumerate(sources):
        dp[1 << i][frozenset(c)] = ("src", i)
    pair_tests = 0
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
                            pair_tests += 1
                            r = resolve(a, b)
                            if r is not None and r not in dp[mask]:
                                dp[mask][r] = (sub, a, other, b) if keep_trace else None
                sub = (sub - 1) & mask
    return dp, pair_tests


def proof(dp, mask, clause):
    rec = dp[mask][clause]
    if rec[0] == "src":
        return {"source": rec[1], "clause": sorted(clause)}
    ma, a, mb, b = rec
    return {"clause": sorted(clause), "left": proof(dp, ma, a), "right": proof(dp, mb, b)}


def sat(formula, variables):
    out = []
    for bits in itertools.product((0, 1), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if all(any(a[abs(l)] == (l > 0) for l in c) for c in formula):
            out.append(a)
    return out


def map_right(c):
    return tuple((1 if l > 0 else -1) * (abs(l) + 4) for l in c)


def main():
    start = time.perf_counter()
    base_dp, base_pairs = closure(BASE)
    base_ror = frozenset() in base_dp[(1 << len(BASE)) - 1]
    base_models = sat(BASE, (2, 3, 4, 5))
    base_deletions = [len(sat(BASE[:i] + BASE[i + 1 :], (2, 3, 4, 5))) for i in range(6)]
    tested = []
    witness = None
    for li in range(6):
        left = tuple(c + ((1,) if i == li else ()) for i, c in enumerate(BASE))
        ldp, _ = closure(left)
        lunit = frozenset({1}) in ldp[-1]
        for ri in range(6):
            right_base = tuple(map_right(c) for c in BASE)
            right = tuple(c + ((-1,) if i == ri else ()) for i, c in enumerate(right_base))
            rdp, _ = closure(right)
            runit = frozenset({-1}) in rdp[-1]
            sources = left + right
            gdp, pairs = closure(sources, keep_trace=True)
            empty = frozenset() in gdp[-1]
            tested.append({"left_weakened": li, "right_weakened": ri,
                           "left_unit": lunit, "right_unit": runit,
                           "global_ror": empty, "pair_tests": pairs})
            if empty and (not lunit or not runit):
                witness = {"left_weakened": li, "right_weakened": ri,
                           "left": left, "right": right,
                           "left_unit": lunit, "right_unit": runit,
                           "global_proof": proof(gdp, (1 << 12) - 1, frozenset())}
                break
        if witness:
            break
    record = {
        "status": "COMPUTATIONAL",
        "base_formula": BASE,
        "base_models": len(base_models),
        "base_deletion_model_counts": base_deletions,
        "base_full_source_ror": base_ror,
        "base_pair_tests": base_pairs,
        "tested": tested,
        "counterexample": witness,
        "wall_seconds": time.perf_counter() - start,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = Path("results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS_GADGET389.json")
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
