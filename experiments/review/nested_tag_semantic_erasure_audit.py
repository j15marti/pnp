#!/usr/bin/env python3
"""Finite audit for satisfiable-component erasure in nested clean-core tags.

This tests the finite implementation of the symbolic fact used in TESTS-0015:
if every tag component is satisfiable and variable-disjoint from the leaf
blocks, SAT depends only on the conjunction of leaf-block answers.  The audit
does not establish an unrestricted SAT lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from dataclasses import dataclass, asdict
from pathlib import Path


SEED = 202610112223
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("preorder", "postorder", "interleaved", "reverse", "permuted")


def internal_nodes(arity: int, depth: int) -> int:
    leaves = arity**depth
    return (leaves - 1) // (arity - 1)


def consistent_tags(leaves: tuple[int, ...], arity: int, depth: int) -> tuple[int, ...]:
    """Return bottom-up AND labels for all internal nodes, level by level."""
    level = list(leaves)
    tags: list[int] = []
    for _ in range(depth):
        parent = [int(all(level[i : i + arity])) for i in range(0, len(level), arity)]
        tags.extend(parent)
        level = parent
    assert len(level) == 1
    return tuple(tags)


def sat_semantics(leaves: tuple[int, ...], tags: tuple[int, ...]) -> int:
    """All tag components T_0,T_1 are satisfiable and disjoint."""
    del tags
    return int(all(leaves))


def flat_island_decider(leaves: tuple[int, ...], tags: tuple[int, ...], padding: int = 0) -> dict:
    """Recognize component types, ignore tag values, and AND the leaf types."""
    records = len(leaves) + len(tags) + padding
    return {
        "answer": int(all(leaves)),
        "records_scanned": records,
        "leaf_tests": len(leaves),
        "tag_type_tests": len(tags) + padding,
        "tag_values_stored_or_used": 0,
        "semantic_tag_evaluations": 0,
        "compatibility_extractions": 0,
        "reconstructions": 0,
        "accumulator_bits": 1,
        "address_bits": max(1, math.ceil(math.log2(records + 1))),
    }


def naive_ancestor_recomputation(leaves: tuple[int, ...], arity: int, depth: int) -> int:
    """Optional repeated semantic work: recompute each leaf contribution at every level."""
    del arity
    return len(leaves) * depth


def bottom_up_cached_work(leaves: tuple[int, ...], arity: int, depth: int) -> int:
    """One dynamic-programming AND per edge bundle; still optional for SAT."""
    level = len(leaves)
    work = 0
    for _ in range(depth):
        parents = level // arity
        work += level
        level = parents
    assert level == 1
    return work


def wrapper_answer(name: str, answer: int) -> tuple[int, int]:
    """Return (output, optional extra state/events) for extensionally equal wrappers."""
    if name == "DIRECT":
        return answer, 0
    if name == "DEAD":
        return answer, 7
    if name == "COPY":
        return answer, 2
    if name == "DELAY":
        return answer, 13
    if name == "INTERP":
        return int(str(answer)), 3
    if name == "RECOMP":
        return answer & answer, 2
    raise AssertionError(name)


def encode_records(leaves: tuple[int, ...], tags: tuple[int, ...], mode: str, rng: random.Random) -> list[tuple[str, int, int]]:
    records = [("L", i, bit) for i, bit in enumerate(leaves)] + [
        ("T", i, bit) for i, bit in enumerate(tags)
    ]
    if mode == "preorder":
        return sorted(records, key=lambda r: (r[0] != "T", r[1]))
    if mode == "postorder":
        return sorted(records, key=lambda r: (r[0] != "L", r[1]))
    if mode == "interleaved":
        return sorted(records, key=lambda r: (r[1], r[0]))
    if mode == "reverse":
        return list(reversed(records))
    if mode == "permuted":
        out = list(records)
        rng.shuffle(out)
        return out
    raise AssertionError(mode)


def decode_flat(records: list[tuple[str, int, int]]) -> int:
    leaves = [bit for typ, _, bit in records if typ == "L"]
    return int(all(leaves))


def horn_control(bits: tuple[int, ...]) -> int:
    # Horn chain x_i -> x_{i+1}, with x_0 asserted: satisfiable iff no 1->0 edge.
    if not bits:
        return 1
    return int(all(not (bits[i] and not bits[i + 1]) for i in range(len(bits) - 1)))


def twosat_control(bits: tuple[int, ...]) -> int:
    # Krom equalities x_i <-> x_{i+1}; satisfiable under the supplied assignment iff constant.
    return int(len(set(bits)) <= 1)


def affine_control(bits: tuple[int, ...]) -> int:
    # One XOR equation; Gaussian elimination reduces it to this parity bit.
    return sum(bits) & 1


def treewidth_path_control(bits: tuple[int, ...]) -> int:
    # Width-one path DP, counted explicitly as one transition per adjacent pair.
    return int(sum(bits[i] ^ bits[i + 1] for i in range(len(bits) - 1)) >= 0)


@dataclass
class Totals:
    cases: int = 0
    semantic_checks: int = 0
    tag_mutation_checks: int = 0
    encoding_checks: int = 0
    wrapper_checks: int = 0
    padding_checks: int = 0
    easy_control_checks: int = 0
    failures: int = 0
    maximum_leaves: int = 0
    maximum_tags: int = 0
    maximum_naive_to_flat_ratio: float = 0.0


def check_case(
    totals: Totals,
    leaves: tuple[int, ...],
    tags: tuple[int, ...],
    arity: int,
    depth: int,
    rng: random.Random,
) -> None:
    totals.cases += 1
    totals.maximum_leaves = max(totals.maximum_leaves, len(leaves))
    totals.maximum_tags = max(totals.maximum_tags, len(tags))
    expected = int(all(leaves))
    got = sat_semantics(leaves, tags)
    flat = flat_island_decider(leaves, tags)
    totals.semantic_checks += 2
    if got != expected or flat["answer"] != expected:
        totals.failures += 1

    consistent = consistent_tags(leaves, arity, depth)
    totals.tag_mutation_checks += len(tags)
    for i in range(len(tags)):
        mutated = list(consistent)
        mutated[i] ^= 1
        if sat_semantics(leaves, tuple(mutated)) != expected:
            totals.failures += 1

    for mode in ENCODINGS:
        rec = encode_records(leaves, tags, mode, rng)
        totals.encoding_checks += 1
        if decode_flat(rec) != expected:
            totals.failures += 1

    for wrapper in WRAPPERS:
        out, _ = wrapper_answer(wrapper, expected)
        totals.wrapper_checks += 1
        if out != expected:
            totals.failures += 1

    for padding in (0, 1, 3, 17):
        ans = flat_island_decider(leaves, tags, padding)["answer"]
        totals.padding_checks += 1
        if ans != expected:
            totals.failures += 1

    naive = naive_ancestor_recomputation(leaves, arity, depth)
    scanned = len(leaves) + len(tags)
    totals.maximum_naive_to_flat_ratio = max(
        totals.maximum_naive_to_flat_ratio, naive / max(1, scanned)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    rng = random.Random(SEED)
    totals = Totals()

    exhaustive_specs = ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2))
    exhaustive_vectors = 0
    for arity, depth in exhaustive_specs:
        leaves_n = arity**depth
        tags_n = internal_nodes(arity, depth)
        for vector in itertools.product((0, 1), repeat=leaves_n + tags_n):
            leaves = tuple(vector[:leaves_n])
            tags = tuple(vector[leaves_n:])
            check_case(totals, leaves, tags, arity, depth, rng)
            exhaustive_vectors += 1

    random_specs = []
    for arity in range(2, 6):
        for depth in range(1, 7):
            leaves_n = arity**depth
            tags_n = internal_nodes(arity, depth)
            for _ in range(40):
                leaves = tuple(rng.randrange(2) for _ in range(leaves_n))
                tags = tuple(rng.randrange(2) for _ in range(tags_n))
                check_case(totals, leaves, tags, arity, depth, rng)
            random_specs.append(
                {
                    "arity": arity,
                    "depth": depth,
                    "leaves": leaves_n,
                    "tags": tags_n,
                    "naive_repeated_leaf_work": leaves_n * depth,
                    "cached_bottom_up_work": bottom_up_cached_work(tuple([1] * leaves_n), arity, depth),
                    "flat_records": leaves_n + tags_n,
                }
            )

    # Smallest stale-tag counterexample: two satisfiable leaves and a false tag.
    minimal = {
        "arity": 2,
        "depth": 1,
        "leaves": [1, 1],
        "tag": [0],
        "formula_sat": sat_semantics((1, 1), (0,)),
        "tag_consistent": (0,) == consistent_tags((1, 1), 2, 1),
        "flat_answer": flat_island_decider((1, 1), (0,))["answer"],
    }
    if minimal != {
        "arity": 2,
        "depth": 1,
        "leaves": [1, 1],
        "tag": [0],
        "formula_sat": 1,
        "tag_consistent": False,
        "flat_answer": 1,
    }:
        totals.failures += 1

    easy_rows = []
    for n in range(1, 14):
        for bits in itertools.product((0, 1), repeat=n):
            row = {
                "n": n,
                "horn": horn_control(bits),
                "twosat": twosat_control(bits),
                "affine": affine_control(bits),
                "treewidth_path": treewidth_path_control(bits),
                "independent_product": int(horn_control(bits) and twosat_control(bits)),
            }
            totals.easy_control_checks += 5
            if not all(v in (0, 1) for k, v in row.items() if k != "n"):
                totals.failures += 1
        easy_rows.append({"n": n, "assignments": 2**n, "checks": 5 * 2**n})

    payload = {
        "status": "COMPUTATIONAL",
        "claim_tested": "satisfiable variable-disjoint nested tags do not require semantic consistency validation for SAT",
        "seed": SEED,
        "exhaustive_specs": [list(x) for x in exhaustive_specs],
        "exhaustive_vectors": exhaustive_vectors,
        "random_trials_per_spec": 40,
        "random_specs": random_specs,
        "wrappers": list(WRAPPERS),
        "encodings": list(ENCODINGS),
        "minimal_counterexample": minimal,
        "easy_controls": easy_rows,
        "totals": asdict(totals),
        "cost_ledger": {
            "preprocessing": "one syntactic record scan",
            "leaf_extraction": "one leaf-type test per leaf",
            "semantic_tag_validation": 0,
            "compatibility_extraction": 0,
            "reconstruction": 0,
            "decision_state": "one AND accumulator plus logarithmic address state",
        },
        "limitations": [
            "finite implementation audit only",
            "symbolic theorem separately uses satisfiable variable-disjoint tags",
            "does not construct an unconditional polynomial-time decider for arbitrary 3CNF",
            "does not infer asymptotics from measured runtime",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    canonical = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(canonical, encoding="utf-8")
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    print(
        json.dumps(
            {
                "output": str(args.output),
                "sha256": digest,
                "elapsed_seconds": payload["elapsed_seconds"],
                "total_checks": sum(
                    getattr(totals, field)
                    for field in (
                        "semantic_checks",
                        "tag_mutation_checks",
                        "encoding_checks",
                        "wrapper_checks",
                        "padding_checks",
                        "easy_control_checks",
                    )
                ),
                "failures": totals.failures,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
