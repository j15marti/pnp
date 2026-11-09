#!/usr/bin/env python3
"""Exhaustive finite red-team of branch-local alpha renaming at DAG joins.

This is an independent model, not the historical R_mix341 checker.  A paid
definition occurrence has an immutable origin.  Each branch may enumerate its
live origins in a different order.  The script compares three joins:

* naive: identify equal branch-local canonical names;
* blind: put every branch in a disjoint namespace;
* provenance: identify exactly equal immutable origins.

The last construction is the name-identity component required by a global
nominal/orbit abstraction.  Rule semantics and context discharge are separate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import resource
import time
from pathlib import Path


def partial_permutations(n: int):
    for k in range(1, n + 1):
        yield from itertools.permutations(range(n), k)


def local_names(branch):
    return {origin: index for index, origin in enumerate(branch)}


def analyze_pair(left, right, weights):
    lm = local_names(left)
    rm = local_names(right)
    union = set(left) | set(right)
    shared = set(left) & set(right)

    by_local = {}
    for side, branch, mapping in (("L", left, lm), ("R", right, rm)):
        for origin in branch:
            by_local.setdefault(mapping[origin], []).append((side, origin))

    collision = any(len({origin for _, origin in entries}) > 1
                    for entries in by_local.values())
    split = any(lm[origin] != rm[origin] for origin in shared)

    true_cost = sum(weights[o] for o in union)
    # The naive syntactic cost assigns one representative weight per local
    # name.  Equal weights make any collision an unambiguous undercount.
    naive_cost = len(by_local)
    blind_cost = len(left) + len(right)
    provenance_cost = len(union)

    provenance_same_iff_same_origin = True
    provenance_names = {origin: index for index, origin in enumerate(sorted(union))}
    for a in union:
        for b in union:
            if (provenance_names[a] == provenance_names[b]) != (a == b):
                provenance_same_iff_same_origin = False

    return {
        "collision": collision,
        "split": split,
        "shared": bool(shared),
        "true_cost": true_cost,
        "naive_cost": naive_cost,
        "blind_cost": blind_cost,
        "provenance_cost": provenance_cost,
        "provenance_same_iff_same_origin": provenance_same_iff_same_origin,
    }


def run(n: int):
    weights = [1] * n
    branches = list(partial_permutations(n))
    counts = {
        "pairs": 0,
        "collision_pairs": 0,
        "split_pairs": 0,
        "naive_undercount_pairs": 0,
        "blind_overcount_pairs": 0,
        "provenance_cost_failures": 0,
        "provenance_identity_failures": 0,
    }
    witnesses = {}
    for left in branches:
        for right in branches:
            a = analyze_pair(left, right, weights)
            counts["pairs"] += 1
            if a["collision"]:
                counts["collision_pairs"] += 1
                witnesses.setdefault("collision", {"left": left, "right": right, **a})
            if a["split"]:
                counts["split_pairs"] += 1
                witnesses.setdefault("split", {"left": left, "right": right, **a})
            if a["naive_cost"] < a["true_cost"]:
                counts["naive_undercount_pairs"] += 1
                witnesses.setdefault("naive_undercount", {"left": left, "right": right, **a})
            if a["blind_cost"] > a["true_cost"]:
                counts["blind_overcount_pairs"] += 1
                witnesses.setdefault("blind_overcount", {"left": left, "right": right, **a})
            if a["provenance_cost"] != a["true_cost"]:
                counts["provenance_cost_failures"] += 1
            if not a["provenance_same_iff_same_origin"]:
                counts["provenance_identity_failures"] += 1

    explicit = {
        "private_collision": {
            "left": [0],
            "right": [1],
            "definitions": {"0": "u := x", "1": "v := not x"},
            "claim": "both local names are a0 although the origins and definitions differ",
            "analysis": analyze_pair((0,), (1,), weights),
        },
        "shared_split": {
            "left": [0, 1],
            "right": [1, 2],
            "shared_origin": 1,
            "claim": "origin 1 is local a1 on the left and a0 on the right",
            "analysis": analyze_pair((0, 1), (1, 2), weights),
        },
        "blind_duplicate": {
            "left": [0],
            "right": [0],
            "claim": "disjoint branch namespaces charge one shared origin twice",
            "analysis": analyze_pair((0,), (0,), weights),
        },
    }
    return {"n": n, "branch_count": len(branches), "counts": counts,
            "witnesses": witnesses, "explicit_controls": explicit}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if not 2 <= args.n <= 7:
        raise SystemExit("n must be between 2 and 7")
    started = time.perf_counter()
    result = run(args.n)
    result["status"] = "PASS" if (
        result["counts"]["collision_pairs"] > 0
        and result["counts"]["split_pairs"] > 0
        and result["counts"]["naive_undercount_pairs"] > 0
        and result["counts"]["blind_overcount_pairs"] > 0
        and result["counts"]["provenance_cost_failures"] == 0
        and result["counts"]["provenance_identity_failures"] == 0
    ) else "FAIL"
    result["scope"] = (
        "finite origin/renaming model only; not an execution of the authoritative "
        "R_mix341 checker and not a proof of rule-semantic or context compatibility"
    )
    result["resource_ledger"] = {
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": platform.python_version(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256_before_self_hash"] = hashlib.sha256(canonical).hexdigest()
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], **result["counts"],
                      "output": args.output}, sort_keys=True))


if __name__ == "__main__":
    main()
