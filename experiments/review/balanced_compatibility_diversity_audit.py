#!/usr/bin/env python3
"""Finite audit for BALANCED-COMPATIBILITY-DIVERSITY-NO-COST1.

The fixed 198-variable unsatisfiable clean-core block is used only through
Doecker's proved certificate parameters (198 variables, 264 clauses).  This
script does not claim to re-verify that large unsatisfiability certificate.
It exhaustively verifies the six-variable blocks and the finite bookkeeping
instances k=1,...,14.
"""

from __future__ import annotations

import itertools
import json
import math
import time


POS = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
NEG_S = POS
NEG_G0 = ((0, 2, 4), (0, 3, 5), (1, 2, 5), (1, 3, 4))
NEG_G1 = ((0, 2, 5), (0, 3, 4), (1, 2, 4), (1, 3, 5))


def satisfies(bits: tuple[int, ...], neg: tuple[tuple[int, ...], ...]) -> bool:
    return all(any(bits[i] for i in c) for c in POS) and all(
        any(not bits[i] for i in c) for c in neg
    )


def compatible(partial: tuple[int | None, ...], neg: tuple[tuple[int, ...], ...]) -> int:
    holes = [i for i, x in enumerate(partial) if x is None]
    for fill in itertools.product((0, 1), repeat=len(holes)):
        bits = list(partial)
        for i, value in zip(holes, fill):
            bits[i] = value
        if satisfies(tuple(int(x) for x in bits), neg):
            return 1
    return 0


def clean_block(neg: tuple[tuple[int, ...], ...]) -> bool:
    clauses = ((1, c) for c in POS)
    signed = list(clauses) + [(-1, c) for c in neg]
    if len(set(signed)) != 8:
        return False
    for v in range(6):
        if sum(v in c for c in POS) != 2 or sum(v in c for c in neg) != 2:
            return False
    return all(len(set(c)) == 3 for _, c in signed)


def encoded_length(k: int) -> int:
    n = 198 + 6 * k
    m = 264 + 8 * k
    width = math.ceil(math.log2(n + 1))
    header = 32 + 2 * width
    return header + 3 * m * (1 + width)


def encode(k: int, b: int, u: tuple[int, ...], scheme: str) -> str:
    payload = "".join(map(str, u))
    if scheme == "plain":
        return f"E:{k:02d}:{b}:{payload}"
    if scheme == "tagged":
        return f"TAG{(k * 7) % 97:02d}:E:{k:02d}:{b}:{payload}:PAD{'x' * k}"
    if scheme == "renamed":
        # Fixed bijective renaming of the two payload block names.
        return f"R:{k:02d}:{b}:{''.join('B' if x else 'A' for x in u)}"
    raise ValueError(scheme)


def recognize(encoded: str, scheme: str) -> int:
    fields = encoded.split(":")
    if scheme == "plain":
        return int(fields[2])
    if scheme == "tagged":
        return int(fields[3])
    if scheme == "renamed":
        return int(fields[2])
    raise ValueError(scheme)


def main() -> None:
    started = time.perf_counter()
    beta = (0, None, 0, None, 0, None)
    empty = (None,) * 6
    blocks = {"S": NEG_S, "G0": NEG_G0, "G1": NEG_G1}

    block_results = {}
    for name, neg in blocks.items():
        sats = [bits for bits in itertools.product((0, 1), repeat=6) if satisfies(bits, neg)]
        profile = tuple(
            compatible(p, neg) for p in itertools.product((None, 0, 1), repeat=6)
        )
        block_results[name] = {
            "clean": clean_block(neg),
            "satisfying_assignments": len(sats),
            "beta_compatible": compatible(beta, neg),
            "empty_compatible": compatible(empty, neg),
            "profile_sha_surrogate": sum((i + 1) * x for i, x in enumerate(profile)),
        }

    assert all(v["clean"] for v in block_results.values())
    assert satisfies((0, 0, 1, 1, 0, 0), NEG_S)
    assert satisfies((0, 0, 1, 0, 1, 1), NEG_G0)
    assert satisfies((0, 0, 1, 0, 1, 1), NEG_G1)
    assert compatible(beta, NEG_G0) == 1
    assert compatible(beta, NEG_G1) == 0

    disagreements = 0
    for partial in itertools.product((None, 0, 1), repeat=6):
        disagreements += compatible(partial, NEG_G0) != compatible(partial, NEG_G1)
    assert disagreements > 0

    layers = []
    schemes = ("plain", "tagged", "renamed")
    total_wrapper_checks = 0
    for k in range(1, 15):
        yes_fingerprints = set()
        yes = no = 0
        per_scheme_lengths = {scheme: set() for scheme in schemes}
        for u in itertools.product((0, 1), repeat=k):
            fingerprint = tuple(1 - bit for bit in u)
            yes_fingerprints.add(fingerprint)
            for b in (0, 1):
                yes += b
                no += 1 - b
                for scheme in schemes:
                    encoded = encode(k, b, u, scheme)
                    per_scheme_lengths[scheme].add(len(encoded))
                    assert recognize(encoded, scheme) == b
                    total_wrapper_checks += 1
        assert yes == no == 2**k
        assert len(yes_fingerprints) == 2**k
        assert all(len(lengths) == 1 for lengths in per_scheme_lengths.values())
        layers.append(
            {
                "k": k,
                "formulas": 2 ** (k + 1),
                "yes": yes,
                "no": no,
                "distinct_yes_probe_fingerprints": len(yes_fingerprints),
                "distinct_full_compatibility_functions_proved": 2**k + 1,
                "variables": 198 + 6 * k,
                "clauses": 264 + 8 * k,
                "declared_binary_encoding_bits": encoded_length(k),
                "wrapper_fallback_calls_on_layer": 0,
                "compatibility_queries_on_layer": 0,
                "extraction_steps_on_layer": 0,
                "reconstruction_steps_on_layer": 0,
            }
        )

    result = {
        "claim": "BALANCED-COMPATIBILITY-DIVERSITY-NO-COST1",
        "status": "COMPUTATIONAL finite audit; asymptotic statement proved separately",
        "large_unsat_block": {
            "source": "Doecker, Monotone 3-Sat-(2,2) is NP-complete, Proposition 1",
            "variables": 198,
            "clauses": 264,
            "unsatisfiability_rechecked_here": False,
        },
        "six_variable_blocks": block_results,
        "g0_g1_partial_assignment_disagreements": disagreements,
        "layers": layers,
        "encoding_schemes": list(schemes),
        "wrapper_checks": total_wrapper_checks,
        "elapsed_seconds": time.perf_counter() - started,
        "seed": None,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
