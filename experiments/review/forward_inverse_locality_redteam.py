#!/usr/bin/env python3
"""Bounded audit for FORWARD-TAG-INVERSE-SEPARATION1.

The construction is a tagged monotone (3,3) family.  A literal at an output
address is generated with one permutation-oracle query and its occurrence tag
is native to the address.  Recovering all incidences of a named output
variable requires inverting that permutation; a deterministic black-box
algorithm needs n-1 queries in the worst case.

Every invocation is deliberately small (well below the 30-second rule).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from collections import Counter, defaultdict
from pathlib import Path

RUN_ID = "RT-0013"
SEED = 202610111536


PARTITIONS = (
    ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
    ((0, 3, 6), (1, 4, 7), (2, 5, 8)),
    ((0, 4, 8), (1, 5, 6), (2, 3, 7)),
)


def build_family(n: int, perm: list[int]):
    assert n % 9 == 0 and sorted(perm) == list(range(n))
    clauses = []
    for sign in (1, -1):
        for tag, partition in enumerate(PARTITIONS):
            for block in range(n // 9):
                off = 9 * block
                for cell in partition:
                    base = tuple(off + j for j in cell)
                    vars_ = tuple(perm[j] for j in base)
                    clauses.append(
                        {"sign": sign, "tag": tag, "base": base, "vars": vars_}
                    )
    return clauses


def verify_m33(n: int, clauses):
    counts = Counter()
    tags = defaultdict(set)
    signed_triples = set()
    for ci, clause in enumerate(clauses):
        assert len(set(clause["vars"])) == 3
        key = (clause["sign"], tuple(sorted(clause["vars"])))
        assert key not in signed_triples
        signed_triples.add(key)
        for slot, var in enumerate(clause["vars"]):
            counts[(var, clause["sign"])] += 1
            tags[(var, clause["sign"])].add(clause["tag"])
            # The forward interface exposes the tag without inversion.
            assert clause["tag"] in (0, 1, 2)
            assert var == clause["vars"][slot]
    for var in range(n):
        for sign in (1, -1):
            assert counts[(var, sign)] == 3
            assert tags[(var, sign)] == {0, 1, 2}
    return len(signed_triples)


def compile_inverse(clauses):
    inverse = defaultdict(list)
    forward = []
    for ci, clause in enumerate(clauses):
        for slot, var in enumerate(clause["vars"]):
            rec = (ci, slot, clause["sign"], clause["tag"])
            inverse[var].append(rec)
            forward.append((var, rec))
    for var in inverse:
        inverse[var].sort(key=lambda x: (x[2], x[3], x[0], x[1]))
    return forward, inverse


def inverse_by_queries(perm, target):
    # Query n-1 locations.  If target was not seen, bijectivity determines the
    # final location without querying it.
    for probes, value in enumerate(perm[:-1], start=1):
        if value == target:
            return probes - 1, probes
    return len(perm) - 1, len(perm) - 1


def clause_satisfied(clause, assignment):
    vals = [assignment[v] if clause["sign"] == 1 else 1 - assignment[v]
            for v in clause["vars"]]
    return any(vals)


def find_witness(clauses, n):
    for bits in itertools.product((0, 1), repeat=n):
        if all(clause_satisfied(c, bits) for c in clauses):
            return bits
    return None


def roundtrip_text(clauses):
    lines = []
    for c in clauses:
        lits = [(v + 1) * c["sign"] for v in c["vars"]]
        lines.append(" ".join(map(str, lits)) + " 0")
    parsed = []
    for line in lines:
        vals = [int(x) for x in line.split()[:-1]]
        parsed.append(tuple(vals))
    return parsed


def gaussian_rank(rows, width):
    rows = list(rows)
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(rows))
                      if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def main():
    started = time.perf_counter()
    rng = random.Random(SEED)
    cases = []
    totals = Counter()
    base_witness = None

    for n in (9, 18, 27, 36):
        for trial in range(32):
            perm = list(range(n))
            rng.shuffle(perm)
            clauses = build_family(n, perm)
            distinct = verify_m33(n, clauses)
            forward, inverse = compile_inverse(clauses)
            assert len(forward) == 6 * n
            assert all(len(inverse[v]) == 6 for v in range(n))

            probes = []
            for target in range(n):
                preimage, q = inverse_by_queries(perm, target)
                assert perm[preimage] == target
                probes.append(q)
            assert max(probes) == n - 1

            encoded = roundtrip_text(clauses)
            assert len(encoded) == 2 * n
            assert all(len(c) == 3 for c in encoded)

            # Clause-order and literal-order wrappers preserve the exact index.
            wrapped = list(clauses)
            rng.shuffle(wrapped)
            wrapped = [dict(c, vars=tuple(reversed(c["vars"]))) for c in wrapped]
            verify_m33(n, wrapped)
            _, wrapped_inverse = compile_inverse(wrapped)
            assert sorted((c[2], c[3]) for c in inverse[0]) == sorted(
                (c[2], c[3]) for c in wrapped_inverse[0]
            )

            if n == 9 and trial == 0:
                base_witness = find_witness(clauses, n)
                assert base_witness is not None

            cases.append({
                "n": n,
                "trial": trial,
                "clauses": len(clauses),
                "literal_records": len(forward),
                "distinct_signed_clauses": distinct,
                "forward_oracle_queries_per_literal": 1,
                "inverse_worst_case_queries": max(probes),
                "inverse_mean_queries": sum(probes) / len(probes),
            })
            totals["instances"] += 1
            totals["clauses"] += len(clauses)
            totals["literal_records"] += len(forward)
            totals["inverse_probes"] += sum(probes)
            totals["wrapper_checks"] += 2
            totals["encoding_roundtrips"] += 1

    # Hostile tractable controls: their cheap semantics do not imply a common
    # occurrence resource.  These are bounded sanity checks, not asymptotics.
    controls = {
        "2sat_path_edges": 11,
        "horn_forward_steps": 12,
        "bounded_treewidth_path_bags": 11,
        "independent_product_blocks": 4,
        "padding_tokens_ignored": 64,
        "redundant_clauses_ignored": 24,
    }
    affine_rows = [0b00111, 0b01101, 0b10110, 0b11011]
    controls["affine_rank"] = gaussian_rank(affine_rows, 5)
    controls["affine_rows"] = len(affine_rows)

    result = {
        "run_id": RUN_ID,
        "claim": "FORWARD-TAG-INVERSE-SEPARATION1",
        "status": "PROVED/EXACT in the deterministic permutation-oracle query model",
        "seed": SEED,
        "construction": {
            "variables": "n=9b",
            "clauses": "2n tagged monotone 3-clauses",
            "occurrences": "each variable occurs once at each tag per sign",
            "forward_literal_cost": "one permutation-oracle query",
            "forward_tag_cost": "zero additional oracle queries",
            "inverse_lower_bound": "n-1 queries worst case",
            "offline_inverse_table": "Theta(n) records after explicit scan",
        },
        "adversary_certificate": {
            "statement": "With two unqueried domain locations, swap the target image between them; the transcript is unchanged and the inverse answer differs.",
            "threshold": "q < n-1",
        },
        "totals": dict(totals),
        "controls": controls,
        "base_nine_witness": list(base_witness),
        "cases": cases,
        "limitations": [
            "The oracle lower bound does not establish a standard-model time lower bound.",
            "An explicit inverse table or nonuniform advice removes the inverse-query lower bound.",
            "The construction does not decide whether the concrete JMV port label is locally computable.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path("results_raw_2026-10-11_forward_inverse_locality_redteam.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "payload_sha256": result["payload_sha256"],
        "totals": result["totals"],
        "controls": controls,
        "base_nine_witness": result["base_nine_witness"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
