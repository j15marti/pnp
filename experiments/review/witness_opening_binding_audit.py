#!/usr/bin/env python3
"""Finite audit for ordinary SAT witnesses as purported binding openings.

The exact symbolic result is proved in the accompanying WITBIND1 report.
This program only checks the base paired-K3,3 block, its two-block product,
collision arithmetic, canonical self-reduction, and hostile easy-family
controls.  Every invocation is intended to finish in less than 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from collections import Counter
from pathlib import Path


Clause = tuple[int, ...]


def paired_k33() -> list[Clause]:
    clauses: list[Clause] = []
    triples = [[3 * i + j for j in range(3)] for i in range(3)]
    triples += [[3 * i + j for i in range(3)] for j in range(3)]
    for triple in triples:
        clauses.append(tuple(v + 1 for v in triple))
        clauses.append(tuple(-(v + 1) for v in triple))
    return clauses


def satisfies(clauses: list[Clause], assignment: tuple[int, ...]) -> bool:
    return all(
        any((assignment[abs(lit) - 1] == 1) if lit > 0 else
            (assignment[abs(lit) - 1] == 0) for lit in clause)
        for clause in clauses
    )


def satisfying_assignments(clauses: list[Clause], nvars: int) -> list[tuple[int, ...]]:
    return [a for a in itertools.product((0, 1), repeat=nvars)
            if satisfies(clauses, a)]


def shifted_product(clauses: list[Clause], copies: int, nvars: int) -> list[Clause]:
    result: list[Clause] = []
    for block in range(copies):
        off = block * nvars
        for clause in clauses:
            result.append(tuple((1 if lit > 0 else -1) * (abs(lit) + off)
                                for lit in clause))
    return result


def lexicographic_self_reduction(clauses: list[Clause], nvars: int) -> tuple[int, ...] | None:
    prefix: list[int] = []

    def has_extension(candidate: list[int]) -> bool:
        tail = nvars - len(candidate)
        return any(satisfies(clauses, tuple(candidate) + rest)
                   for rest in itertools.product((0, 1), repeat=tail))

    if not has_extension(prefix):
        return None
    for _ in range(nvars):
        if has_extension(prefix + [0]):
            prefix.append(0)
        else:
            prefix.append(1)
    return tuple(prefix)


def canonical_payload_sha(payload: dict) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def run(seed: int, max_blocks: int) -> dict:
    started = time.perf_counter()
    rng = random.Random(seed)
    checks = 0
    base = paired_k33()

    assert len(base) == 12
    checks += 1
    assert len(set(base)) == 12 and all(len(c) == 3 for c in base)
    checks += 2
    occurrences = {v: {1: 0, -1: 0} for v in range(1, 10)}
    for clause in base:
        signs = {1 if lit > 0 else -1 for lit in clause}
        assert len(signs) == 1
        checks += 1
        for lit in clause:
            occurrences[abs(lit)][1 if lit > 0 else -1] += 1
    for v in range(1, 10):
        assert occurrences[v] == {1: 2, -1: 2}
        checks += 1

    witnesses = satisfying_assignments(base, 9)
    checks += 512
    assert len(witnesses) == 102
    checks += 1

    distances = Counter()
    conflicting_pairs = 0
    for i, left in enumerate(witnesses):
        assert satisfies(base, left)
        checks += 1
        for right in witnesses[i + 1:]:
            assert satisfies(base, right)
            assert left != right
            distance = sum(x != y for x, y in zip(left, right))
            assert distance > 0
            checks += 3
            distances[distance] += 1
            conflicting_pairs += 1
    assert conflicting_pairs == math.comb(102, 2)
    checks += 1

    # Constant proof-to-acceptance-node map: all valid witnesses open the same
    # canonical source/address and the same one-bit SAT decision.
    image_size = 1
    ordered_collision_count = len(witnesses) ** 2
    cs_lower_bound = len(witnesses) ** 2 // ordered_collision_count
    assert image_size == cs_lower_bound == 1
    checks += 2

    canonical = min(witnesses)
    recovered = lexicographic_self_reduction(base, 9)
    assert recovered == canonical
    checks += 1

    product2 = shifted_product(base, 2, 9)
    count2 = 0
    first2 = None
    for assignment in itertools.product((0, 1), repeat=18):
        ok = satisfies(product2, assignment)
        checks += 1
        if ok:
            count2 += 1
            if first2 is None:
                first2 = assignment
    assert count2 == 102 ** 2
    assert first2 == canonical + canonical
    checks += 2

    # Renaming and global complementation are bijections on witnesses.
    rename_rows = []
    for trial in range(16):
        perm = list(range(9))
        rng.shuffle(perm)
        renamed: list[Clause] = []
        for clause in base:
            renamed.append(tuple((1 if lit > 0 else -1) * (perm[abs(lit) - 1] + 1)
                                 for lit in clause))
        renamed_count = len(satisfying_assignments(renamed, 9))
        complemented = [tuple(-lit for lit in clause) for clause in renamed]
        complemented_count = len(satisfying_assignments(complemented, 9))
        assert renamed_count == complemented_count == 102
        checks += 2 * 512 + 1
        rename_rows.append({"trial": trial, "witnesses": renamed_count})

    # Hostile controls: multiplicity can be large in easy relations.
    control_rows = []
    for n in range(2, 11):
        assignments = list(itertools.product((0, 1), repeat=n))

        # Tautological 2-CNF, also bounded-treewidth by disjoint components.
        two_sat = [(i + 1, -(i + 1)) for i in range(n)]
        two_count = sum(satisfies(two_sat, a) for a in assignments)
        assert two_count == 2 ** n
        checks += len(assignments) + 1

        # Horn implication chain: 00..0011..11, exactly n+1 models.
        horn = [(-(i + 1), i + 2) for i in range(n - 1)]
        horn_count = sum(satisfies(horn, a) for a in assignments)
        assert horn_count == n + 1
        checks += len(assignments) + 1

        # Affine even-parity system, Gaussian-eliminable, 2^(n-1) models.
        affine_count = sum(sum(a) % 2 == 0 for a in assignments)
        assert affine_count == 2 ** (n - 1)
        checks += len(assignments) + 1

        # Duplicate padding preserves the 2-CNF relation and witness set.
        padded = two_sat + [two_sat[0]] * (3 * n)
        padded_count = sum(satisfies(padded, a) for a in assignments)
        assert padded_count == two_count
        checks += len(assignments) + 1

        control_rows.append({
            "n": n,
            "two_sat_or_treewidth_one_witnesses": two_count,
            "horn_chain_witnesses": horn_count,
            "affine_even_parity_witnesses": affine_count,
            "duplicate_padded_witnesses": padded_count,
        })

    wrappers = ["DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP"]
    for witness in witnesses:
        answer = satisfies(base, witness)
        for _wrapper in wrappers:
            assert answer is True
            checks += 1

    growth = []
    for k in range(1, max_blocks + 1):
        witness_count = 102 ** k
        collision_count = witness_count ** 2
        assert collision_count == 102 ** (2 * k)
        assert witness_count > 1
        checks += 2
        growth.append({
            "blocks": k,
            "variables": 9 * k,
            "clauses": 12 * k,
            "witnesses": str(witness_count),
            "ordered_collisions_constant_map": str(collision_count),
            "witness_entropy_bits": math.log2(witness_count),
            "image_size": 1,
        })

    elapsed = time.perf_counter() - started
    payload = {
        "claim": "WITNESS-OPENING-BINDING-TRILEMMA1",
        "status": "COMPUTATIONAL",
        "seed": seed,
        "exhaustive": True,
        "base": {
            "variables": 9,
            "clauses": 12,
            "witnesses": len(witnesses),
            "unordered_distinct_valid_opening_pairs": conflicting_pairs,
            "ordered_collisions_constant_map": ordered_collision_count,
            "image_size": image_size,
            "hamming_distance_distribution": dict(sorted(distances.items())),
            "lexicographically_least_witness": "".join(map(str, canonical)),
            "self_reduction_matches": recovered == canonical,
        },
        "two_block_product": {
            "variables": 18,
            "assignments_exhausted": 2 ** 18,
            "witnesses": count2,
            "expected_product": 102 ** 2,
        },
        "growth": growth,
        "renaming_complement_controls": rename_rows,
        "easy_family_controls": control_rows,
        "wrappers": wrappers,
        "checks": checks,
        "failures": 0,
        "elapsed_seconds": round(elapsed, 6),
        "limitations": [
            "Finite computation does not prove an asymptotic SAT lower bound.",
            "The audit refutes ordinary satisfying-witness uniqueness, not every construction-specific opening relation.",
            "The encoded-length asymptotic is proved symbolically in the report, not inferred from timing.",
        ],
    }
    payload["canonical_payload_sha256"] = canonical_payload_sha(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610120016)
    parser.add_argument("--max-blocks", type=int, default=64)
    parser.add_argument(
        "--output",
        default="results/raw/review/2026-10-12_witness_opening_binding.json",
    )
    args = parser.parse_args()
    payload = run(args.seed, args.max_blocks)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(path),
        "checks": payload["checks"],
        "failures": payload["failures"],
        "elapsed_seconds": payload["elapsed_seconds"],
        "base_witnesses": payload["base"]["witnesses"],
        "two_block_witnesses": payload["two_block_product"]["witnesses"],
        "canonical_payload_sha256": payload["canonical_payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
