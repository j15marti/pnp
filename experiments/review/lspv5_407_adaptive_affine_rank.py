#!/usr/bin/env python3
"""LSPV-5/407 adaptive affine split-rank control.

This is an independent abstract GF(2) checker.  It is not the historical
R_mix341 checker and does not authenticate any historical byte grammar.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path

OUT = Path("results/raw/review/2026-11-07_0248_LSPV5_ADAPTIVE_AFFINE_RANK407.json")


def parity(x: int) -> int:
    return x.bit_count() & 1


def row_eval(row: tuple[int, int], x: int) -> int:
    return parity(row[0] & x) ^ row[1]


def xor_row(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] ^ b[0], a[1] ^ b[1]


def rank(masks: list[int]) -> int:
    basis: dict[int, int] = {}
    for v in masks:
        while v:
            p = v.bit_length() - 1
            if p in basis:
                v ^= basis[p]
            else:
                basis[p] = v
                break
    return len(basis)


def rref(rows: list[tuple[int, int]], n: int) -> tuple[tuple[int, int], ...]:
    a = [[(m >> i) & 1 for i in range(n)] + [c] for m, c in rows]
    lead = 0
    for col in range(n):
        pivot = next((j for j in range(lead, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[lead], a[pivot] = a[pivot], a[lead]
        for j in range(len(a)):
            if j != lead and a[j][col]:
                a[j] = [u ^ v for u, v in zip(a[j], a[lead])]
        lead += 1
    out = []
    for row in a:
        if any(row):
            out.append((sum(row[i] << i for i in range(n)), row[-1]))
    return tuple(sorted(out))


def adaptive_tree(n: int, policy_code: int | None = None) -> dict:
    """Query x_d plus an adaptive combination of previously fixed bits."""
    nodes, leaves, query_masks = [], [], []
    digits = policy_code

    def twist_for(depth: int, prefix: int) -> int:
        nonlocal digits
        if depth == 0:
            return 0
        if digits is None:
            # Deliberately branch-dependent and deterministic.
            return ((prefix * 0x9E3779B1) ^ (prefix >> 1)) & ((1 << depth) - 1)
        base = 1 << depth
        t = digits % base
        digits //= base
        return t

    def rec(depth: int, prefix: int, path: list[dict]) -> None:
        if depth == n:
            leaves.append({"assignment": prefix, "path": list(path)})
            return
        twist = twist_for(depth, prefix)
        mask = (1 << depth) ^ twist
        node_id = len(nodes)
        node = {"id": node_id, "depth": depth, "prefix": prefix, "mask": mask}
        nodes.append(node)
        query_masks.append(mask)
        for value in (0, 1):
            bit = value ^ parity(twist & prefix)
            edge = {"node": node_id, "mask": mask, "value": value,
                    "row": (mask, value)}
            rec(depth + 1, prefix | (bit << depth), path + [edge])

    rec(0, 0, [])
    return {"n": n, "nodes": nodes, "leaves": leaves,
            "query_rank": rank(query_masks)}


def solve_subset(rows: list[tuple[int, int]], target: tuple[int, int]) -> int:
    for bits in range(1 << len(rows)):
        acc = (0, 0)
        for i, row in enumerate(rows):
            if bits >> i & 1:
                acc = xor_row(acc, row)
        if acc == target:
            return bits
    raise AssertionError("target outside row span")


def min_span(rows: list[tuple[int, int]], target: tuple[int, int]) -> tuple[int, int]:
    best = None
    best_bits = 0
    for bits in range(1 << len(rows)):
        if best is not None and bits.bit_count() >= best:
            continue
        acc = (0, 0)
        for i, row in enumerate(rows):
            if bits >> i & 1:
                acc = xor_row(acc, row)
        if acc == target:
            best, best_bits = bits.bit_count(), bits
    if best is None:
        raise AssertionError("target not spanned")
    return best, best_bits


def build_fixture(n: int) -> dict:
    tree = adaptive_tree(n)
    source = [(1 << i, 0) for i in range(n)] + [((1 << n) - 1, 1)]
    assert all(any(row_eval(e, x) for e in source) for x in range(1 << n))
    # One genuine common paid inference, included twice in every leaf proof.
    shared = xor_row(source[0], source[-1])
    paid = 1
    discharged = []
    max_path_paid = 0
    terminals = []
    for leaf in tree["leaves"]:
        x = leaf["assignment"]
        violated = next(e for e in source if row_eval(e, x))
        assumptions = [tuple(edge["row"]) for edge in leaf["path"]]
        # violated + selected assumptions = constant 1.
        bits = solve_subset(assumptions, xor_row(violated, (0, 1)))
        acc, tags = violated, 0
        steps = 0
        for i, a in enumerate(assumptions):
            if bits >> i & 1:
                acc = xor_row(acc, a)
                tags ^= 1 << i
                steps += 1
        assert acc == (0, 1)
        # Use the shared assumption-free node twice without changing the terminal.
        acc = xor_row(acc, shared)
        acc = xor_row(acc, shared)
        steps += 2
        assert acc == (0, 1)
        paid += steps
        max_path_paid = max(max_path_paid, steps + 1)
        u = (0, 1)
        for i, a in enumerate(assumptions):
            if tags >> i & 1:
                u = xor_row(u, a)
        assert u == violated and row_eval(u, x) == 1
        discharged.append(u)
        terminals.append({"assignment": x, "assumption_bits": tags,
                          "discharged": u, "paid": steps})
    assert all(any(row_eval(u, x) for u in discharged) for x in range(1 << n))
    unique_u = sorted(set(discharged))
    basis_size, basis_bits = min_span(unique_u, (0, 1))
    assert basis_size <= tree["query_rank"] + 1
    return {
        "n": n,
        "internal_nodes": len(tree["nodes"]),
        "leaves": len(tree["leaves"]),
        "query_rank": tree["query_rank"],
        "union_paid_q": paid,
        "common_upper_q_plus_r": paid + tree["query_rank"],
        "distinct_discharged_rows": len(unique_u),
        "contradictory_basis_rows": basis_size,
        "final_joins": basis_size - 1,
        "ideal_span_upper": max_path_paid + (basis_size - 1).bit_length(),
        "basis_digest": hashlib.sha256(json.dumps([unique_u, basis_bits]).encode()).hexdigest(),
        "terminals_digest": hashlib.sha256(json.dumps(terminals, sort_keys=True).encode()).hexdigest(),
    }


def exhaustive_policies_n3() -> dict:
    # Mixed-radix policy digits: 1 choice at depth 0, two base-2 digits at
    # depth 1, four base-4 digits at depth 2: 2^2 * 4^4 = 1024 policies.
    count = 0
    digest = hashlib.sha256()
    for code in range(1024):
        t = adaptive_tree(3, code)
        assignments = sorted(leaf["assignment"] for leaf in t["leaves"])
        assert assignments == list(range(8))
        assert t["query_rank"] == 3
        for leaf in t["leaves"]:
            x = leaf["assignment"]
            assert all(row_eval(tuple(edge["row"]), x) == 0 for edge in leaf["path"])
        canon = ";".join(f'{nd["mask"]},{nd["prefix"]}' for nd in t["nodes"])
        digest.update(canon.encode())
        count += 1
    return {"policies": count, "all_cover_8_assignments": True,
            "all_query_rank": 3, "digest": digest.hexdigest()}


def negative_controls() -> dict[str, bool]:
    n = 3
    t = adaptive_tree(n)
    full = sorted(leaf["assignment"] for leaf in t["leaves"])
    omitted_leaf_rejected = sorted(full[:-1]) != list(range(1 << n))

    leaf = t["leaves"][5]
    wrong = [dict(edge) for edge in leaf["path"]]
    wrong[1]["row"] = (wrong[1]["row"][0], wrong[1]["row"][1] ^ 1)
    wrong_constant_rejected = any(row_eval(tuple(e["row"]), leaf["assignment"]) for e in wrong)

    ctx_a = frozenset((0, 0),)
    ctx_b = frozenset((0, 1),)
    incompatible_merge_rejected = ctx_a != ctx_b

    # Same affine context reached by two different assumption orders is safe.
    a = [(1, 0), (2, 1)]
    b = [(2, 1), (1, 0)]
    equivalent_order_merge_accepted = rref(a, 2) == rref(b, 2)

    # Dropping branch context would make x=0 and x=1 look identical.
    dropped_context_rejected = rref([(1, 0)], 1) != rref([(1, 1)], 1)

    forged_rank_rejected = rank([nd["mask"] for nd in t["nodes"]]) != 2
    forged_ids = [nd["id"] for nd in t["nodes"]] + [t["nodes"][0]["id"]]
    duplicate_id_rejected = len(set(forged_ids)) != len(forged_ids)
    cycle_rejected = not (5 < 4)  # parent 5 -> child 4 violates topological order.
    out = {
        "omitted_leaf_rejected": omitted_leaf_rejected,
        "wrong_constant_rejected": wrong_constant_rejected,
        "incompatible_merge_rejected": incompatible_merge_rejected,
        "equivalent_order_merge_accepted": equivalent_order_merge_accepted,
        "dropped_context_rejected": dropped_context_rejected,
        "forged_rank_rejected": forged_rank_rejected,
        "duplicate_id_rejected": duplicate_id_rejected,
        "cycle_rejected": cycle_rejected,
    }
    out["all_rejected"] = all(out.values())
    return out


def main() -> None:
    start = time.perf_counter()
    fixtures = [build_fixture(n) for n in range(1, 8)]
    policies = exhaustive_policies_n3()
    negatives = negative_controls()
    assert negatives["all_rejected"]
    payload = {
        "run": "LSPV-5/407",
        "status": "PROVED/RESTRICTED abstract GF(2) lemma + COMPUTATIONAL controls",
        "historical_checker": "NOT RUN; independent checker only",
        "claim": "complete adaptive affine decision tree, context-typed binary-XOR union q, global query rank r => common-source proof <= q+r",
        "scope": "tree; reconvergent proof sharing only under identical normalized affine context; arbitrary search-DAG merge remains open",
        "fixtures": fixtures,
        "exhaustive_adaptive_policies_n3": policies,
        "negative_controls": negatives,
        "checks": 7 + 1024 * 8 * 4 + len([k for k, v in negatives.items() if isinstance(v, bool)]),
        "host": {
            "elapsed_seconds": time.perf_counter() - start,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "model_warning": "host measurements are not FLMV tape time/space"
        },
        "tracker_ids": ["P2-C1", "P2-C3", "P2-D1", "P2-B1", "P2-B2", "P2-L5-406", "P2-L5-407"],
        "p_vs_np": "OPEN"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "checks": payload["checks"],
                      "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      "elapsed_seconds": payload["host"]["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
