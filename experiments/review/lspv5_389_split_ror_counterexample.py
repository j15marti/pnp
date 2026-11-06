#!/usr/bin/env python3
"""Search minimal split-CNF counterexamples to side-unit ROR normalization.

The left side uses variables b,x; the right side b,y.  We enumerate
non-tautological width-at-most-two clause sets.  A strict Resolution step is
legal only when the parents have exactly one complementary variable and the
resolvent is non-tautological.  Provenance masks must be disjoint, so every
accepted full-mask result is a source-once tree.
"""

from __future__ import annotations

import itertools
import json
import resource
import time
from pathlib import Path

B, X, Y = 1, 2, 3


def all_clauses(vars_):
    out = []
    lits = [v for z in vars_ for v in (z, -z)]
    for width in (1, 2):
        for c in itertools.combinations(lits, width):
            if any(-l in c for l in c):
                continue
            out.append(frozenset(c))
    return sorted(set(out), key=lambda c: (len(c), tuple(sorted(c))))


def sat(formula, variables):
    models = []
    for bits in itertools.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, bits))
        if all(any(a[abs(l)] == (l > 0) for l in c) for c in formula):
            models.append(a)
    return models


def resolve(a, b):
    pivots = [v for v in (B, X, Y) if (v in a and -v in b) or (-v in a and v in b)]
    if len(pivots) != 1:
        return None
    p = pivots[0]
    r = (a | b) - {p, -p}
    if any(-l in r for l in r):
        return None
    return frozenset(r)


def closure(sources):
    n = len(sources)
    dp = [dict() for _ in range(1 << n)]
    for i, c in enumerate(sources):
        dp[1 << i][c] = ("src", i)
    for size in range(2, n + 1):
        for mask in range(1, 1 << n):
            if mask.bit_count() != size:
                continue
            anchor = mask & -mask
            sub = (mask - 1) & mask
            while sub:
                other = mask ^ sub
                if other and (sub & anchor):
                    for ca, cb in itertools.product(dp[sub], dp[other]):
                        r = resolve(ca, cb)
                        if r is not None and r not in dp[mask]:
                            dp[mask][r] = (sub, ca, other, cb)
                sub = (sub - 1) & mask
    return dp


def tree(dp, mask, clause, sources):
    rec = dp[mask][clause]
    if rec[0] == "src":
        return {"source": rec[1], "clause": sorted(clause)}
    ma, ca, mb, cb = rec
    return {
        "clause": sorted(clause),
        "left": tree(dp, ma, ca, sources),
        "right": tree(dp, mb, cb, sources),
    }


def is_mus(formula, variables):
    if sat(formula, variables):
        return False
    return all(sat(formula[:i] + formula[i + 1 :], variables) for i in range(len(formula)))


def search(require_mus=False):
    left_candidates = all_clauses((B, X))
    right_candidates = all_clauses((B, Y))
    tested = 0
    for total in range(4, 11):
        for nl in range(2, total - 1):
            nr = total - nl
            if nr < 2:
                continue
            for left in itertools.combinations(left_candidates, nl):
                lm = sat(left, (B, X))
                if not lm or any(not m[B] for m in lm):
                    continue
                ldp = closure(left)
                lunit = frozenset({B}) in ldp[(1 << nl) - 1]
                for right in itertools.combinations(right_candidates, nr):
                    rm = sat(right, (B, Y))
                    if not rm or any(m[B] for m in rm):
                        continue
                    tested += 1
                    rdp = closure(right)
                    runit = frozenset({-B}) in rdp[(1 << nr) - 1]
                    if lunit and runit:
                        continue
                    sources = tuple(left) + tuple(right)
                    if require_mus and not is_mus(sources, (B, X, Y)):
                        continue
                    gdp = closure(sources)
                    full = (1 << total) - 1
                    if frozenset() in gdp[full]:
                        return {
                            "tested_semantic_pairs": tested,
                            "require_mus": require_mus,
                            "total_sources": total,
                            "left_sources": [sorted(c) for c in left],
                            "right_sources": [sorted(c) for c in right],
                            "left_models": [{str(k): int(v) for k, v in m.items()} for m in lm],
                            "right_models": [{str(k): int(v) for k, v in m.items()} for m in rm],
                            "left_full_outcomes": [sorted(c) for c in ldp[(1 << nl) - 1]],
                            "right_full_outcomes": [sorted(c) for c in rdp[(1 << nr) - 1]],
                            "left_target_present": lunit,
                            "right_target_present": runit,
                            "global_tree": tree(gdp, full, frozenset(), sources),
                        }
    return None


def main():
    start = time.perf_counter()
    result = search(require_mus=False)
    mus_result = search(require_mus=True)
    if result is None:
        raise SystemExit("no unrestricted counterexample in searched scope")
    result.update({
        "status": "COMPUTATIONAL_COUNTEREXAMPLE",
        "scope": "distinct non-tautological width<=2 clauses over left {b,x}, right {b,y}",
        "wall_seconds": time.perf_counter() - start,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    })
    out = Path("results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_COUNTEREXAMPLE389.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "unrestricted_counterexample": result,
        "mus_counterexample": mus_result,
        "mus_search_scope": "same width<=2 universe, total sources 4..10",
    }
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
