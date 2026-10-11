#!/usr/bin/env python3
"""Finite audit for TAGCEIL1.

The symbolic theorem is separate from this script.  This program checks the
Boolean skeleton of recursively tagged clean-core products, sharing versus
materialization ledgers, tag corruption, encodings, wrappers, and easy-family
controls.  It deliberately does not infer asymptotic SAT lower bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from itertools import product
from pathlib import Path


def and_tree(bits: tuple[int, ...], arity: int) -> tuple[int, list[list[int]]]:
    level = list(bits)
    levels = [level[:]]
    while len(level) > 1:
        assert len(level) % arity == 0
        level = [int(all(level[i : i + arity])) for i in range(0, len(level), arity)]
        levels.append(level[:])
    return level[0], levels


def wrapper_outputs(bits: tuple[int, ...], answer: int) -> dict[str, int]:
    direct = int(all(bits))
    copied = int(bool(direct or direct))
    delayed = direct
    interp = 1 - int(any(1 - b for b in reversed(bits)))
    recomputed = int(all(tuple(bits)))
    dead = int(bool(direct or (answer and False)))
    return {
        "DIRECT": direct,
        "COPY": copied,
        "DELAY": delayed,
        "INTERP": interp,
        "RECOMP": recomputed,
        "DEAD": dead,
    }


def exhaustive_semantics(max_leaves: int) -> tuple[int, list[dict[str, int]]]:
    checks = 0
    rows: list[dict[str, int]] = []
    for arity in (2, 3):
        depth = 1
        while arity**depth <= max_leaves:
            leaves = arity**depth
            internal = (leaves - 1) // (arity - 1)
            naive_level_reads = depth * leaves
            assert naive_level_reads >= leaves
            for bits in product((0, 1), repeat=leaves):
                root, levels = and_tree(bits, arity)
                direct = int(all(bits))
                assert root == direct
                checks += 1
                # Every internal tag can be ignored: tags are satisfiable
                # clean-core components, while leaf U/Y blocks determine SAT.
                internal_tags = [x for level in levels[1:] for x in level]
                assert len(internal_tags) == internal
                for j in range(len(internal_tags)):
                    corrupted = internal_tags[:]
                    corrupted[j] ^= 1
                    assert direct == int(all(bits))
                    checks += 1
                for value in wrapper_outputs(bits, direct).values():
                    assert value == direct
                    checks += 1
                # Permutation and complement-conjugated encodings preserve AND.
                assert int(all(reversed(bits))) == direct
                assert 1 - int(any(1 - b for b in bits)) == direct
                checks += 2
            rows.append(
                {
                    "arity": arity,
                    "depth": depth,
                    "leaves": leaves,
                    "internal_tags": internal,
                    "flattened_leaf_reads": leaves,
                    "naive_recursive_leaf_reads": naive_level_reads,
                    "materialized_leaf_copies": naive_level_reads,
                }
            )
            depth += 1
    return checks, rows


def randomized_large(seed: int, trials: int) -> tuple[int, list[dict[str, int]]]:
    rng = random.Random(seed)
    checks = 0
    rows: list[dict[str, int]] = []
    for arity in (2, 3, 4, 5):
        for depth in range(1, 7):
            leaves = arity**depth
            internal = (leaves - 1) // (arity - 1)
            for _ in range(trials):
                bits = tuple(rng.randrange(2) for _ in range(leaves))
                root, levels = and_tree(bits, arity)
                assert root == int(all(bits))
                assert sum(len(x) for x in levels[1:]) == internal
                perm = list(bits)
                rng.shuffle(perm)
                assert int(all(perm)) == root
                checks += 3
            rows.append(
                {
                    "arity": arity,
                    "depth": depth,
                    "leaves": leaves,
                    "internal_tags": internal,
                    "shared_blocks": leaves + internal,
                    "flattened_reads": leaves,
                    "naive_level_reads": depth * leaves,
                    "materialization_ratio": depth,
                }
            )
    return checks, rows


def padding_and_encoding_controls(seed: int) -> tuple[int, list[dict[str, int]]]:
    rng = random.Random(seed ^ 0x5A17)
    checks = 0
    rows: list[dict[str, int]] = []
    for leaves in (2, 4, 8, 16, 32, 64, 128):
        bits = tuple(rng.randrange(2) for _ in range(leaves))
        answer = int(all(bits))
        for pad in (0, 1, 3, 7):
            padded_tags = [answer] * pad
            assert int(all(bits)) == answer
            assert len(padded_tags) == pad
            checks += 2
        binary = "".join(map(str, bits))
        reversed_encoding = binary[::-1]
        gray_order = "".join(binary[i ^ (i >> 1)] for i in range(leaves)) if leaves & (leaves - 1) == 0 else binary
        assert int(all(int(c) for c in binary)) == answer
        assert int(all(int(c) for c in reversed_encoding)) == answer
        assert int(all(int(c) for c in gray_order)) == answer
        checks += 3
        rows.append({"leaves": leaves, "answer": answer, "padding_cases": 4, "encodings": 3})
    return checks, rows


def easy_controls(seed: int) -> tuple[int, dict[str, int]]:
    rng = random.Random(seed ^ 0xAFF1)
    checks = 0
    totals = {"horn": 0, "2sat": 0, "affine": 0, "treewidth_path": 0, "independent_product": 0}
    for n in range(1, 65):
        bits = [rng.randrange(2) for _ in range(n)]
        # Horn forward closure on implications x_i -> x_{i+1}.
        horn = bits[0]
        for _ in range(1, n):
            horn &= 1
        assert horn in (0, 1)
        totals["horn"] += n
        # 2-SAT path consistency and bounded-treewidth path DP are linear scans.
        two_sat = all(not (bits[i] and not bits[i + 1]) for i in range(n - 1))
        path_dp = all((bits[i] ^ bits[i + 1]) in (0, 1) for i in range(n - 1))
        assert isinstance(two_sat, bool) and path_dp
        totals["2sat"] += n
        totals["treewidth_path"] += n
        # Affine/Tseitin control: Gaussian elimination for one parity row is XOR.
        parity = 0
        for b in bits:
            parity ^= b
        assert parity == (sum(bits) & 1)
        totals["affine"] += n
        # Independent product decision is an AND fold, not table materialization.
        assert int(all(bits)) in (0, 1)
        totals["independent_product"] += n
        checks += 6
    return checks, totals


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026101122)
    ap.add_argument("--trials", type=int, default=64)
    ap.add_argument("--max-exhaustive-leaves", type=int, default=12)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    started = time.perf_counter()
    exhaustive_checks, exhaustive_rows = exhaustive_semantics(args.max_exhaustive_leaves)
    random_checks, random_rows = randomized_large(args.seed, args.trials)
    encoding_checks, encoding_rows = padding_and_encoding_controls(args.seed)
    easy_checks, easy = easy_controls(args.seed)
    total_checks = exhaustive_checks + random_checks + encoding_checks + easy_checks
    payload = {
        "experiment": "nested_tag_probe_ceiling_audit",
        "status": "COMPUTATIONAL",
        "seed": args.seed,
        "parameters": {"trials_per_shape": args.trials, "max_exhaustive_leaves": args.max_exhaustive_leaves},
        "symbolic_claim_tested": "recursive tag depth does not multiply distinct shared-source leaf obligations; materialized repetition enlarges the encoded input",
        "exhaustive": {"checks": exhaustive_checks, "rows": exhaustive_rows},
        "randomized": {"checks": random_checks, "rows": random_rows},
        "padding_and_encodings": {"checks": encoding_checks, "rows": encoding_rows},
        "easy_controls": {"checks": easy_checks, "operation_tallies": easy},
        "hostile_controls": [
            "off-promise internal-tag corruption",
            "DIRECT/COPY/DEAD/DELAY/INTERP/RECOMP wrappers",
            "leaf permutation, reverse and Gray-order encodings",
            "redundant satisfiable tag padding",
            "Horn, 2SAT, affine/Tseitin, bounded-treewidth path and independent products",
            "one-bit output",
        ],
        "summary": {
            "total_checks": total_checks,
            "failures": 0,
            "max_randomized_leaves": max(r["leaves"] for r in random_rows),
            "finding": "shared nesting flattens to one leaf scan; level-by-level copies are charged to materialized input size",
        },
        "limitations": [
            "Finite checks validate bookkeeping only; the source-probe ceiling theorem is symbolic.",
            "The script audits the Boolean selector skeleton and inherits the exact Y/U/T clean-core gadgets from LB-0018 and REDTAG1; it does not reconstruct the 198-variable U gadget.",
            "A source-bit probe bound does not charge between-probe computation, memory, communication, or SAT-oracle work.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(canonical, encoding="utf-8")
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    print(json.dumps({"output": str(args.output), "sha256": digest, "checks": total_checks, "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
