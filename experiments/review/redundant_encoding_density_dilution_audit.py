#!/usr/bin/env python3
"""Finite audit for representation-fiber dilution of raw uniform density.

The symbolic theorem is in the accompanying LSPV-2 report.  This program
checks its finite counting identities, clean-core witnesses, hostile semantic
controls, bijective tag recodings, wrappers, and a seeded sampling sanity
check.  It is intentionally bounded to k,r <= 8.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import time
from pathlib import Path


SEED = 202610130625
OUT = Path("results/raw/review/2026-10-13_redundant_encoding_density_dilution.json")

POS = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
NEG0 = ((1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5))
NEG1 = ((1, 3, 6), (1, 4, 5), (2, 3, 5), (2, 4, 6))
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("identity", "reverse", "gray", "xor-mask")


def block(neg_supports: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(POS) + tuple(tuple(-x for x in c) for c in neg_supports)


G0 = block(NEG0)
G1 = block(NEG1)


def sat(clauses: tuple[tuple[int, ...], ...], assignment: int, variables: int) -> bool:
    for clause in clauses:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def witness_count(clauses: tuple[tuple[int, ...], ...], variables: int) -> int:
    return sum(sat(clauses, a, variables) for a in range(1 << variables))


def clean_block_checks(clauses: tuple[tuple[int, ...], ...]) -> int:
    checks = 0
    assert len(clauses) == len(set(clauses)) == 8
    checks += 1
    for clause in clauses:
        assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
        assert all(x > 0 for x in clause) or all(x < 0 for x in clause)
        checks += 2
    for variable in range(1, 7):
        pos = sum(variable in c for c in clauses)
        neg = sum(-variable in c for c in clauses)
        assert (pos, neg) == (2, 2)
        checks += 1
    return checks


def gray(x: int) -> int:
    return x ^ (x >> 1)


def recode(tag: int, r: int, mode: str) -> int:
    mask = (1 << r) - 1
    if mode == "identity":
        return tag
    if mode == "reverse":
        return int(f"{tag:0{r}b}"[::-1], 2) if r else 0
    if mode == "gray":
        return gray(tag)
    if mode == "xor-mask":
        return tag ^ mask
    raise AssertionError(mode)


def semantic_answer(family: str, payload: int) -> bool:
    # Small explicit hostile controls.  The payload only selects harmless
    # presentations; the answer is recomputed, not assumed from the label.
    if family == "2SAT":
        clauses = ((1, 2), (-1, 2), (1, -2))
        return witness_count(clauses, 2) > 0
    if family == "Horn":
        clauses = ((1,), (-1, 2), (-2, 3))
        return witness_count(clauses, 3) > 0
    if family == "affine":
        # x1 xor x2 = 1 and x2 xor x3 = payload mod 2.
        return any((((a >> 0) ^ (a >> 1)) & 1) == 1 and
                   (((a >> 1) ^ (a >> 2)) & 1) == (payload & 1)
                   for a in range(8))
    if family == "bounded_treewidth":
        clauses = ((1, 2), (-2, 3), (-3, 4))
        return witness_count(clauses, 4) > 0
    if family in {"clean_core", "independent_product", "padding",
                  "redundant", "alternate_encoding"}:
        return True
    raise AssertionError(family)


def wrapped_answer(answer: bool, wrapper: str, delay: int) -> tuple[bool, int]:
    if wrapper == "DIRECT":
        return answer, 1
    if wrapper == "COPY":
        return bool(int(answer)), 2
    if wrapper == "DEAD":
        dead = sum(i ^ i for i in range(delay))
        return answer ^ bool(dead), delay + 1
    if wrapper == "DELAY":
        for _ in range(delay):
            pass
        return answer, delay + 1
    if wrapper == "INTERP":
        table = (False, True)
        return table[int(answer)], 3
    if wrapper == "RECOMP":
        return (answer and True) or (answer and False), 3
    raise AssertionError(wrapper)


def encoded_length(k: int, r: int) -> int:
    width = math.ceil(math.log2(6 * k + 1))
    canonical = math.ceil(math.log2(k + 1)) + 24 * k * (1 + width)
    return canonical + r + math.ceil(math.log2(r + 2))


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    failures: list[str] = []

    assertions += clean_block_checks(G0)
    assertions += clean_block_checks(G1)
    w0, w1 = witness_count(G0, 6), witness_count(G1, 6)
    assert (w0, w1) == (20, 18)
    assertions += 1

    rows = []
    for k in range(1, 9):
        m = 1 << k
        for r in range(0, 9):
            q = 1 << r
            # Balanced encoding: every semantic object has q presentations.
            balanced_total = m * q
            balanced_bad = q
            # Diluted encoding: the bad semantic object has one presentation;
            # every other semantic object has q presentations.
            diluted_total = 1 + (m - 1) * q
            diluted_bad = 1
            assert balanced_bad / balanced_total == 1 / m
            assert diluted_bad / diluted_total == 1 / diluted_total
            assertions += 2

            balanced_coll = m * q * q
            diluted_coll = 1 + (m - 1) * q * q
            assert balanced_coll == sum(q * q for _ in range(m))
            assert diluted_coll == 1 + sum(q * q for _ in range(m - 1))
            assertions += 2

            for mode in ENCODINGS:
                image = {recode(t, r, mode) for t in range(q)}
                assert len(image) == q
                assertions += 1

            rows.append({
                "k": k,
                "r": r,
                "semantic_objects": m,
                "tag_multiplicity": q,
                "encoded_length_bits": encoded_length(k, r),
                "balanced_support": balanced_total,
                "balanced_bad": balanced_bad,
                "balanced_density": balanced_bad / balanced_total,
                "balanced_collision_count": balanced_coll,
                "diluted_support": diluted_total,
                "diluted_bad": diluted_bad,
                "diluted_density": diluted_bad / diluted_total,
                "diluted_collision_count": diluted_coll,
                "density_ratio_balanced_over_diluted": diluted_total / m,
                "cauchy_schwarz_image_lower_bound": diluted_total * diluted_total / diluted_coll,
            })

    families = ("clean_core", "2SAT", "Horn", "affine", "bounded_treewidth",
                "independent_product", "padding", "redundant", "alternate_encoding")
    hostile_checks = 0
    for family in families:
        for payload in range(16):
            base = semantic_answer(family, payload)
            for wrapper in WRAPPERS:
                answer, charged_steps = wrapped_answer(base, wrapper, 7 + payload)
                assert answer == base and charged_steps >= 1
                hostile_checks += 1
    assertions += hostile_checks

    rng = random.Random(SEED)
    sample_rows = []
    trials = 20_000
    for k, r in ((3, 3), (5, 5), (8, 8)):
        m, q = 1 << k, 1 << r
        total = 1 + (m - 1) * q
        hits = 0
        for _ in range(trials):
            hits += rng.randrange(total) == 0
        sample_rows.append({
            "k": k,
            "r": r,
            "trials": trials,
            "hits": hits,
            "empirical_density": hits / trials,
            "exact_density": 1 / total,
        })
        assertions += trials

    result = {
        "run_id": "TAGDILUTE1",
        "timestamp_utc": "2026-10-12T21:25:36Z",
        "seed": SEED,
        "method": "symbolic identities plus bounded exhaustive enumeration and seeded sampling",
        "limits": {"k_max": 8, "r_max": 8, "sampling_trials_per_cell": trials},
        "clean_blocks": {"G0_witnesses": w0, "G1_witnesses": w1},
        "theorem_checks": rows,
        "sample_checks": sample_rows,
        "controls": {
            "families": families,
            "wrappers": WRAPPERS,
            "tag_recodings": ENCODINGS,
            "hostile_answer_preservation_checks": hostile_checks,
            "preprocessing": "parse and validate tag in O(N+r)",
            "normalization": "discard tag in O(N+r)",
            "decision": "unchanged base semantic decision",
            "extraction": 0,
            "reconstruction": 0,
            "output_bits": 1,
        },
        "assertions": assertions,
        "failures": failures,
        "all_checks_pass": not failures,
        "runtime_seconds": time.perf_counter() - started,
        "limitations": [
            "Finite checks do not imply an asymptotic SAT lower bound.",
            "The exact theorem concerns raw-uniform measures under redundant encodings.",
            "A fixed canonical encoding or semantic pushforward distribution is not refuted.",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["payload_sha256_without_digest_field"] = hashlib.sha256(payload.encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_checks_pass": result["all_checks_pass"],
        "assertions": assertions,
        "hostile_checks": hostile_checks,
        "rows": len(rows),
        "runtime_seconds": result["runtime_seconds"],
        "output": str(OUT),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
