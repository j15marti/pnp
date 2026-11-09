#!/usr/bin/env python3
"""Exact finite audit of branch-join polarity in a common-literal domain.

This is an independent semantic control, not an R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path


VARS = ("x", "y")
VALS = tuple(dict(zip(VARS, bits)) for bits in itertools.product((0, 1), repeat=2))


def key(v):
    return tuple(v[x] for x in VARS)


def literals(v):
    return frozenset((x, bool(v[x])) for x in VARS)


def alpha(states):
    """All literals true in every represented state (must/common facts)."""
    states = tuple(states)
    if not states:
        return frozenset((x, b) for x in VARS for b in (False, True))
    out = literals(states[0])
    for v in states[1:]:
        out &= literals(v)
    return out


def gamma(facts):
    """Models satisfying the facts conjunctively."""
    return frozenset(key(v) for v in VALS if facts <= literals(v))


def sat_clause(v, clause):
    return any(bool(v[x]) == sign for x, sign in clause)


def models(cnf, assumptions=()):
    return tuple(
        v
        for v in VALS
        if all(sat_clause(v, c) for c in cnf)
        and all(bool(v[x]) == sign for x, sign in assumptions)
    )


def nonempty_subsets(items):
    for mask in range(1, 1 << len(items)):
        yield tuple(items[i] for i in range(len(items)) if mask & (1 << i))


def main():
    start = time.perf_counter()
    # F is x <-> y, encoded as (not x or y) and (x or not y).
    cnf = ((('x', False), ('y', True)), (('x', True), ('y', False)))
    all_models = models(cnf)
    branch0 = models(cnf, (("x", False),))
    branch1 = models(cnf, (("x", True),))
    assert {key(v) for v in all_models} == {(0, 0), (1, 1)}
    assert {key(v) for v in branch0} == {(0, 0)}
    assert {key(v) for v in branch1} == {(1, 1)}

    learned0 = frozenset({("y", False)})
    learned1 = frozenset({("y", True)})
    correct_join = learned0 & learned1
    bad_pool = learned0 | learned1
    assert gamma(correct_join) >= {key(v) for v in all_models}
    assert gamma(bad_pool) == frozenset()
    assert not ({key(v) for v in all_models} <= gamma(bad_pool))

    pairs = 0
    exact_join_identity = 0
    bad_pool_unsound = 0
    for s0 in nonempty_subsets(VALS):
        for s1 in nonempty_subsets(VALS):
            pairs += 1
            a0, a1 = alpha(s0), alpha(s1)
            concrete_union = {key(v) for v in s0} | {key(v) for v in s1}
            sound_join = a0 & a1
            assert alpha(tuple({key(v): v for v in s0 + s1}.values())) == sound_join
            assert concrete_union <= gamma(sound_join)
            exact_join_identity += 1
            pooled = a0 | a1
            if not concrete_union <= gamma(pooled):
                bad_pool_unsound += 1

    elapsed = time.perf_counter() - start
    result = {
        "status": "PASS",
        "scope": "two-variable common-literal abstract domain; semantic control only",
        "formula": "(not x or y) and (x or not y)",
        "formula_models": [list(key(v)) for v in all_models],
        "branch_x0_models": [list(key(v)) for v in branch0],
        "branch_x1_models": [list(key(v)) for v in branch1],
        "branch_local_learned": [["not y"], ["y"]],
        "correct_join_facts": [],
        "correct_join_gamma": [list(v) for v in sorted(gamma(correct_join))],
        "bad_conjunctive_pool_gamma": [],
        "ordered_nonempty_subset_pairs": pairs,
        "join_identity_checks": exact_join_identity,
        "bad_pool_unsound_pairs": bad_pool_unsound,
        "assertion_groups": 9 + 2 * pairs,
        "wall_seconds": elapsed,
        "limitations": [
            "not the historical R_mix341 parser or checker",
            "no proof-minimum or machine-time lower bound",
            "finite replay supports the separately stated symbolic lattice theorem",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_sha256_without_self_hash"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results/raw/arc/2026-11-09_0844_LSPV5_463_ABSTRACT_BRANCH_JOIN_RAW.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
