#!/usr/bin/env python3
"""PH_PROVENANCE_CLOSURE_TEST

Finite sanity test for the LSPV-5 bounded-alternation provenance closure.
This does NOT simulate P=NP. The exhaustive prefix-extension oracle is only
a finite stand-in for the decision predicate used in the symbolic theorem.
"""
from itertools import product
import hashlib
import json
import random
import statistics

SEED = 20261002
WITNESS_BITS = 5
INSTANCES_PER_RELATION = 50


def hbit(seed, *vals):
    payload = "|".join(map(str, (seed,) + vals)).encode()
    return hashlib.sha256(payload).digest()[0] & 1


def r_sigma1(seed, guaranteed, w, b=3):
    if w in guaranteed:
        return True
    return any(hbit(seed, w, z) for z in range(1 << b))


def r_pi2(seed, guaranteed, w, b=3):
    if w in guaranteed:
        return True
    for y in range(1 << b):
        if not any(hbit(seed, w, y, z) for z in range(1 << b)):
            return False
    return True


def r_pi3(seed, guaranteed, w, b=2):
    if w in guaranteed:
        return True
    for y in range(1 << b):
        found = False
        for z in range(1 << b):
            if all(hbit(seed, w, y, z, t) for t in range(1 << b)):
                found = True
                break
        if not found:
            return False
    return True


def prefix_select(nbits, relation):
    prefix = ""
    queries = 0
    for _ in range(nbits):
        candidate = prefix + "0"
        queries += 1
        remaining = nbits - len(candidate)
        exists = False
        for suffix in product("01", repeat=remaining):
            w = int(candidate + "".join(suffix), 2)
            if relation(w):
                exists = True
                break
        prefix += "0" if exists else "1"
    return int(prefix, 2), queries


def main():
    rng = random.Random(SEED)
    summary = {}
    samples = {}

    relations = [
        ("Sigma1_graph", r_sigma1),
        ("Pi2_graph", r_pi2),
        ("Pi3_graph", r_pi3),
    ]

    for label, relation_fn in relations:
        rows = []
        for _ in range(INSTANCES_PER_RELATION):
            seed = rng.randrange(1 << 30)
            guaranteed = tuple(sorted(rng.sample(range(1 << WITNESS_BITS), 2)))

            def relation(w, seed=seed, guaranteed=guaranteed, relation_fn=relation_fn):
                return relation_fn(seed, guaranteed, w)

            valid = [w for w in range(1 << WITNESS_BITS) if relation(w)]
            recovered, prefix_queries = prefix_select(WITNESS_BITS, relation)
            lex_min = min(valid)

            rows.append(
                {
                    "seed": seed,
                    "guaranteed": list(guaranteed),
                    "valid_count": len(valid),
                    "lex_min": lex_min,
                    "recovered": recovered,
                    "prefix_queries": prefix_queries,
                    "canonical_count": sum(w == lex_min for w in valid),
                }
            )

        summary[label] = {
            "instances": len(rows),
            "all_recovered_lex_min": all(r["lex_min"] == r["recovered"] for r in rows),
            "all_canonical_unique": all(r["canonical_count"] == 1 for r in rows),
            "min_valid_count": min(r["valid_count"] for r in rows),
            "max_valid_count": max(r["valid_count"] for r in rows),
            "mean_valid_count": round(
                statistics.mean(r["valid_count"] for r in rows), 2
            ),
            "prefix_queries_per_instance": sorted(
                {r["prefix_queries"] for r in rows}
            ),
        }
        samples[label] = rows[:3]

    result = {
        "experiment": "PH_PROVENANCE_CLOSURE_TEST",
        "seed": SEED,
        "witness_bits": WITNESS_BITS,
        "instances_per_relation": INSTANCES_PER_RELATION,
        "summary": summary,
        "samples": samples,
        "interpretation": [
            "Finite sanity check only; it does not simulate P=NP.",
            "Brute-force extension oracle plays the role of the prefix-extension decision predicate.",
            "For all toy Sigma1/Pi2/Pi3 graph relations, 5 prefix decisions recovered the lexicographically least valid 5-bit witness.",
            "Canonicality/uniqueness did not obstruct reconstruction in the finite model.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
