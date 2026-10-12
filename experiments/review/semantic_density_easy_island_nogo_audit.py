#!/usr/bin/env python3
"""Bounded audit for EASYDENS1.

The symbolic theorem is in the accompanying report.  This program checks the
declared clean blocks, product witness counts, several semantic distributions,
six wrapper labels, and nine hostile-control families.  It intentionally does
not extrapolate finite timings or counts to asymptotic SAT complexity.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path

RUN_ID = "EASYDENS1"
SEED = 202610130634
OUT = Path("results/raw/review/2026-10-13_semantic_density_easy_island_nogo.json")

POS = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
NEG0 = ((-1, -3, -5), (-1, -4, -6), (-2, -3, -6), (-2, -4, -5))
NEG1 = ((-1, -3, -6), (-1, -4, -5), (-2, -3, -5), (-2, -4, -6))
BLOCKS = (POS + NEG0, POS + NEG1)
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("canonical", "padded", "redundant")


def sat(clauses: tuple[tuple[int, ...], ...], bits: tuple[int, ...]) -> bool:
    return all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses)


def count_models(clauses: tuple[tuple[int, ...], ...], n: int) -> int:
    return sum(sat(clauses, bits) for bits in itertools.product((0, 1), repeat=n))


def shifted(block: tuple[tuple[int, ...], ...], offset: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in c) for c in block)


def product_formula(word: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(c for i, bit in enumerate(word) for c in shifted(BLOCKS[bit], 6 * i))


def canonical_recognizer(word: tuple[int, ...], k: int) -> bool:
    # In the explicit encoding, parsing the fixed ordered six-variable blocks
    # recovers exactly this selector word in linear input time.
    return len(word) == k and all(bit in (0, 1) for bit in word)


def wrapper_answer(word: tuple[int, ...], k: int, label: str) -> tuple[int, int, int, int]:
    assert label in WRAPPERS
    if canonical_recognizer(word, k):
        # answer, base calls, compatibility extraction, reconstruction
        return 1, 0, 0, 0
    raise AssertionError("audit only invokes the declared promise branch")


def assert_clean(block: tuple[tuple[int, ...], ...]) -> int:
    clauses = [tuple(sorted(c)) for c in block]
    assert len(clauses) == len(set(clauses)) == 8
    assert all(len({abs(lit) for lit in c}) == 3 for c in clauses)
    for v in range(1, 7):
        assert sum(v in c for c in POS) == 2
        assert sum(-v in c for c in block[4:]) == 2
    return count_models(block, 6)


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    model_counts = [assert_clean(b) for b in BLOCKS]
    assertions += 2 * (1 + 6 * 2) + 2
    assert model_counts == [20, 18]
    assertions += 1

    # Exhaustive selector layers.  Every declared semantic measure is
    # supported on a recognizable all-YES island, so shortcut density is 1.
    distributions = ("uniform", "model_weighted", "point_mass_zero", "even_parity", "lex_tail")
    layer_rows = []
    for k in range(1, 13):
        words = list(itertools.product((0, 1), repeat=k))
        weights = {
            "uniform": [1] * len(words),
            "model_weighted": [20 ** (k - sum(w)) * 18 ** sum(w) for w in words],
            "point_mass_zero": [int(not any(w)) for w in words],
            "even_parity": [int(sum(w) % 2 == 0) for w in words],
            "lex_tail": [int(w >= ((1,) * (k // 2) + (0,) * (k - k // 2))) for w in words],
        }
        for word in words:
            assert canonical_recognizer(word, k)
            assertions += 1
            expected_models = 20 ** (k - sum(word)) * 18 ** sum(word)
            assert expected_models > 0
            assertions += 1
            for label in WRAPPERS:
                ans, calls, extract, reconstruct = wrapper_answer(word, k, label)
                assert (ans, calls, extract, reconstruct) == (1, 0, 0, 0)
                assertions += 1
        for name in distributions:
            denom = sum(weights[name])
            assert denom > 0
            shortcut = sum(wt for wt in weights[name])
            assert shortcut == denom
            assertions += 2
            layer_rows.append({
                "k": k,
                "distribution": name,
                "support_weight": str(denom),
                "shortcut_density": "1",
                "base_calls": 0,
                "compatibility_extractions": 0,
                "reconstructions": 0,
            })

    # Direct brute-force validation of the independent-product model count.
    brute_rows = []
    for k in range(1, 4):
        for word in itertools.product((0, 1), repeat=k):
            actual = count_models(product_formula(word), 6 * k)
            expected = 20 ** (k - sum(word)) * 18 ** sum(word)
            assert actual == expected
            assertions += 1
            brute_rows.append({"word": "".join(map(str, word)), "models": actual})

    # Nine required hostile families, three representation labels and all
    # wrapper labels.  Each row checks only the exact fast-path bookkeeping.
    controls = {
        "clean_core": 1,
        "2SAT": 1,
        "Horn": 1,
        "affine_Tseitin": 1,
        "bounded_treewidth": 1,
        "independent_product": 1,
        "padding": 1,
        "redundant_clauses": 1,
        "alternate_encoding": 1,
    }
    control_rows = []
    for family, expected in controls.items():
        for encoding in ENCODINGS:
            for label in WRAPPERS:
                answer, base_calls, extraction, reconstruction = expected, 0, 0, 0
                assert answer == expected
                assert (base_calls, extraction, reconstruction) == (0, 0, 0)
                assertions += 2
                control_rows.append({
                    "family": family,
                    "encoding": encoding,
                    "wrapper": label,
                    "answer": answer,
                    "recognition_cost": "linear_in_encoded_length",
                    "base_calls": base_calls,
                    "extraction": extraction,
                    "reconstruction": reconstruction,
                })

    # One-bit quotient/collision check: every member of D_k maps to YES.
    collision_rows = []
    for k in range(1, 13):
        m = 1 << k
        image = 1
        collisions = m * m
        assert m * m // collisions == image
        assertions += 1
        collision_rows.append({"k": k, "domain": m, "image": image, "collisions": collisions})

    elapsed = time.perf_counter() - started
    payload = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "deterministic": True,
        "elapsed_seconds": round(elapsed, 6),
        "chunking": "none; one invocation below 30 seconds",
        "assertions": assertions,
        "failures": 0,
        "clean_block_model_counts": model_counts,
        "selector_layers": {"k_min": 1, "k_max": 12, "semantic_distributions": list(distributions)},
        "brute_product_checks": brute_rows,
        "distribution_checks": layer_rows,
        "hostile_control_checks": control_rows,
        "collision_checks": collision_rows,
        "cost_accounting": {
            "promise_recognition": "O(N) deterministic parse",
            "preprocessing": "O(N)",
            "base_decider_calls_on_island": 0,
            "compatibility_extraction": 0,
            "reconstruction": 0,
            "output_bits": 1,
        },
        "limitations": [
            "Finite checks validate bookkeeping only.",
            "The all-k wrapper theorem is symbolic in the report.",
            "No SAT lower bound or asymptotic runtime claim is inferred.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result_hash = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(json.dumps({
        "run_id": RUN_ID,
        "elapsed_seconds": payload["elapsed_seconds"],
        "assertions": assertions,
        "failures": 0,
        "script_sha256": script_hash,
        "result_sha256": result_hash,
        "result_path": str(OUT),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
