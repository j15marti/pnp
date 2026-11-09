#!/usr/bin/env python3
"""Build exact branching/context controls for LSPV-5 run 453.

This deliberately defines a proposed BRANCH_CTX control calculus.  It does
not add split, discharge, weakening, or context rules to historical R_mix341.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import resource
import time


def node(i, rule, clause, context, antecedents=None, pivot=None, split=None):
    out = {
        "id": i,
        "rule": rule,
        "clause": clause,
        "context": context,
        "antecedents": antecedents or [],
    }
    if pivot is not None:
        out["pivot"] = pivot
    if split is not None:
        out["split"] = split
    return out


def valid_packet():
    # F = {a, not-a or b, not-a or not-b}.  The source a is shared by both
    # branches and counted once.  Both branch contradictions are explicit.
    nodes = [
        node(0, "SOURCE", [1], []),
        node(1, "SOURCE", [-1, 2], []),
        node(2, "SOURCE", [-1, -2], []),
        node(3, "ASSUME", [2], [2]),
        node(4, "RES", [-2], [], [0, 2], pivot=1),
        node(5, "RES", [], [2], [4, 3], pivot=2),
        node(6, "ASSUME", [-2], [-2]),
        node(7, "RES", [2], [], [0, 1], pivot=1),
        node(8, "RES", [], [-2], [7, 6], pivot=2),
        node(9, "SPLIT_AND", [], [], [5, 8], split=2),
    ]
    return {
        "calculus": "BRANCH_CTX_PROPOSED_CONTROL",
        "historical_R_mix341_extension": False,
        "root": 9,
        "nodes": nodes,
        "ledger": {
            "source_nodes": 3,
            "paid_distinct_nodes": 7,
            "weighted_span": 3,
            "root_source_ancestors": [0, 1, 2],
            "shared_source": 0,
            "shared_source_direct_uses": 2,
        },
    }


def mutation(label, packet, expected_code, note):
    return {
        "label": label,
        "expected": "REJECT",
        "expected_code": expected_code,
        "note": note,
        "packet": packet,
    }


def mutations(base):
    out = []

    p = copy.deepcopy(base)
    p["nodes"][9]["antecedents"] = [5]
    out.append(mutation(
        "omitted_AND_case", p, "SPLIT_ARITY",
        "A split refutation cannot discharge only the b branch.",
    ))

    p = copy.deepcopy(base)
    p["nodes"][9]["antecedents"] = [5, 5]
    out.append(mutation(
        "cross_branch_false_reuse", p, "SPLIT_CONTEXT",
        "The contradiction under context {b} cannot also discharge {not b}.",
    ))

    p = copy.deepcopy(base)
    p["root"] = 5
    out.append(mutation(
        "undischarged_root_assumption", p, "ROOT_CONTEXT",
        "A branch-local contradiction is not an empty-context refutation.",
    ))

    p = copy.deepcopy(base)
    p["nodes"][4]["antecedents"] = [9, 2]
    out.append(mutation(
        "cyclic_or_forward_dependency", p, "FORWARD_REFERENCE",
        "A proof dependency graph must be acyclic even if search revisits states.",
    ))

    p = copy.deepcopy(base)
    p["ledger"]["paid_distinct_nodes"] = 8
    out.append(mutation(
        "double_count_shared_node", p, "LEDGER",
        "The union of distinct paid nodes is charged once.",
    ))

    p = copy.deepcopy(base)
    p["nodes"] = p["nodes"][1:]
    out.append(mutation(
        "implicit_source_oracle", p, "MISSING_REFERENCE",
        "Removing source a while retaining references makes ancestry unauthenticated.",
    ))

    one = {
        "calculus": "BRANCH_CTX_PROPOSED_CONTROL",
        "historical_R_mix341_extension": False,
        "root": 3,
        "nodes": [
            node(0, "SOURCE", [1], []),
            node(1, "ASSUME", [-1], [-1]),
            node(2, "RES", [], [-1], [0, 1], pivot=1),
            node(3, "SPLIT_AND", [], [], [2], split=1),
        ],
        "ledger": {},
    }
    out.append(mutation(
        "satisfiable_source_one_branch_false", one, "SPLIT_ARITY",
        "F={a} is satisfiable; F,not-a is false, but that one branch proves no refutation.",
    ))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    t0 = time.perf_counter()

    base = valid_packet()
    payload = {
        "artifact": "LSPV5-BRANCH-CONTEXT-AND-JOIN453",
        "status": "PRODUCED_FOR_INDEPENDENT_VERIFICATION",
        "scope": (
            "proposed explicit-context branching control plus semantic source-cover "
            "transfer; not historical R_mix341 grammar or checker"
        ),
        "claim": {
            "classification": "PROVED-RESTRICTED",
            "statement": (
                "In any sound, acyclic, source-explicit branching proof DAG whose "
                "root has empty context, every semantic source cover remains in the "
                "root ancestry. With maximum inference indegree a>1, r required "
                "sources imply q>=ceil((r-1)/(a-1)) paid nodes, even with sharing."
            ),
            "assumptions": [
                "all source uses are explicit authenticated source nodes",
                "context reuse is allowed only into a superset context",
                "split discharge is an AND hyperedge with both complementary cases",
                "the dependency graph is acyclic",
                "all paid inference/discharge nodes have indegree at most a",
                "soundness holds in each recorded context",
            ],
            "not_claimed": [
                "historical R_mix341 contains SPLIT_AND or context discharge",
                "a lower bound for the full mixed calculus",
                "B3",
                "P versus NP",
            ],
        },
        "valid": base,
        "mutations": mutations(base),
        "resources": {
            "producer_seconds": time.perf_counter() - t0,
            "producer_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_before_resource_hash"] = hashlib.sha256(canonical).hexdigest()
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
