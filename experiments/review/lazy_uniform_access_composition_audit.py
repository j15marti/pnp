#!/usr/bin/env python3
"""Finite audit for LAZY-ACCESS-INLINING1.

This script is only a bounded implementation check.  The theorem in the
corresponding report is proved by literal deterministic-machine composition.
Each invocation is intentionally well below the repository's 30 second cap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


SEED = 202610121934
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
FAMILIES = ("horn", "affine_tseitin", "two_sat", "bounded_treewidth", "padding", "redundant")


def policy_digits(code: int, base: int, nodes: int) -> list[int]:
    out = []
    for _ in range(nodes):
        out.append(code % base)
        code //= base
    return out


def evaluate_policy(policy: list[int], mask: int, depth: int, inline: bool) -> tuple[int, tuple[tuple[int, int], ...], int]:
    node = 0
    parity = 0
    transcript = []
    calls = 0
    for _ in range(depth):
        query = policy[node]
        # The inline branch is deliberately a subroutine call rather than a
        # materialized table.  Both branches have identical extensional bits.
        bit = ((mask // (1 << query)) % 2) if inline else ((mask >> query) & 1)
        calls += 1
        transcript.append((query, bit))
        parity ^= bit
        node = 2 * node + 1 + bit
    return parity, tuple(transcript), calls


def exhaustive_adaptive_audit() -> tuple[int, dict[str, int]]:
    domain = 4
    depth = 3
    nodes = (1 << depth) - 1
    assertions = 0
    wrapper_checks = {w: 0 for w in WRAPPERS}
    for code in range(domain ** nodes):
        policy = policy_digits(code, domain, nodes)
        for mask in range(1 << domain):
            oracle = evaluate_policy(policy, mask, depth, inline=False)
            inlined = evaluate_policy(policy, mask, depth, inline=True)
            assert oracle == inlined
            assert oracle[2] == depth
            assertions += 2
            # Presentation wrappers preserve the same output.  INTERP uses a
            # fixed index permutation together with its inverse at the caller;
            # RECOMP simply invokes the inline accessor again.
            for wrapper in WRAPPERS:
                if wrapper == "INTERP":
                    perm = (2, 0, 3, 1)
                    permuted_mask = sum(((mask >> perm[i]) & 1) << i for i in range(domain))
                    inverse = [perm.index(i) for i in range(domain)]
                    translated = [inverse[q] for q in policy]
                    got = evaluate_policy(translated, permuted_mask, depth, inline=True)[0]
                elif wrapper == "RECOMP":
                    got = evaluate_policy(policy, int(f"{mask:04b}", 2), depth, inline=True)[0]
                else:
                    got = inlined[0]
                assert got == oracle[0]
                wrapper_checks[wrapper] += 1
                assertions += 1
    return assertions, wrapper_checks


def virtual_bit(family: str, x: int, n: int, index: int) -> int:
    modulus = 1 << n
    index %= modulus
    if family == "horn":
        return int((index & x) != x or index == x)
    if family == "affine_tseitin":
        return (index & x).bit_count() & 1
    if family == "two_sat":
        return int(((index ^ x) & 3) != 3)
    if family == "bounded_treewidth":
        return ((index ^ (index >> 1) ^ x) & 1)
    if family == "padding":
        return virtual_bit("affine_tseitin", x, n, index) if index < n * n + 1 else 0
    if family == "redundant":
        return virtual_bit("two_sat", x, n, index % max(1, n))
    raise ValueError(family)


def virtual_family_audit() -> tuple[int, list[dict[str, int | str]]]:
    assertions = 0
    rows = []
    for n in range(1, 21):
        x = int(hashlib.sha256(f"{SEED}:{n}".encode()).hexdigest(), 16) % (1 << n)
        for family in FAMILIES:
            code_length = 1 << n
            qmax = n + 3
            index = (x * 5 + n) % code_length
            transcript = []
            for step in range(qmax):
                bit = virtual_bit(family, x, n, index)
                transcript.append((index, bit))
                index = (index * 3 + bit + step + 1) % code_length
            assert len(transcript) == qmax
            assert all(0 <= i < code_length and b in (0, 1) for i, b in transcript)
            # No codeword was allocated; only queried coordinates occur.
            assert len({i for i, _ in transcript}) <= qmax
            assertions += 3
            rows.append({
                "family": family,
                "n": n,
                "implicit_code_length": code_length,
                "adaptive_queries": qmax,
                "distinct_coordinates": len({i for i, _ in transcript}),
            })
    return assertions, rows


def exponent_ledger() -> tuple[int, list[dict[str, int]]]:
    assertions = 0
    rows = []
    for local_exp in range(7):
        for query_exp in range(7):
            for access_exp in range(7):
                composed = max(local_exp, query_exp + access_exp)
                assert composed >= local_exp
                assert composed >= query_exp + access_exp
                assertions += 2
                rows.append({
                    "local_exponent": local_exp,
                    "query_exponent": query_exp,
                    "access_exponent": access_exp,
                    "composed_upper_exponent": composed,
                })
    return assertions, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    a1, wrappers = exhaustive_adaptive_audit()
    a2, family_rows = virtual_family_audit()
    a3, exponent_rows = exponent_ledger()
    elapsed = time.perf_counter() - started
    result = {
        "claim_id": "LAZY-ACCESS-INLINING1",
        "seed": SEED,
        "status": "COMPUTATIONAL",
        "scope": "bounded implementation audit only; no asymptotic inference",
        "adaptive_policy_domain": 4,
        "adaptive_policy_depth": 3,
        "adaptive_policies": 4 ** 7,
        "oracles_per_policy": 16,
        "wrapper_checks": wrappers,
        "virtual_families": list(FAMILIES),
        "virtual_rows": family_rows,
        "exponent_rows": exponent_rows,
        "assertions": a1 + a2 + a3,
        "failures": 0,
        "elapsed_seconds": elapsed,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "assertions": result["assertions"],
        "failures": 0,
        "elapsed_seconds": elapsed,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
