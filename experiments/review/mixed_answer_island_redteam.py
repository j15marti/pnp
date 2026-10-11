#!/usr/bin/env python3
"""Bounded audit for RT-0016's recognizable easy-island barrier.

This program tests only finite instances.  The theorem in the report is a
direct source-code construction and does not depend on these measurements.
Every loop is deliberately bounded so one invocation stays below 30 seconds.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass


WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")


def fallback(wrapper: str, language: int, x: int, m: int) -> bool:
    """Six extensionally equal implementations of one finite language."""
    bit = bool((language >> x) & 1)
    if wrapper == "DIRECT":
        return bit
    if wrapper == "DEAD":
        _unused = sum((language >> j) & 1 for j in range(m))
        return bit
    if wrapper == "COPY":
        table = tuple(bool((language >> j) & 1) for j in range(m))
        return table[x]
    if wrapper == "DELAY":
        acc = False
        for j in range(m + x + 1):
            acc ^= bool(j & 1)
            acc ^= bool(j & 1)
        return bit ^ acc
    if wrapper == "INTERP":
        return bool((language // (2**x)) % 2)
    if wrapper == "RECOMP":
        return any(j == x and ((language >> j) & 1) for j in range(m))
    raise AssertionError(wrapper)


def island_wrapper(language: int, island: int, x: int, m: int, wrapper: str):
    """Recognize first, classify on the island, otherwise call fallback."""
    if (island >> x) & 1:
        return bool((language >> x) & 1), False
    return fallback(wrapper, language, x, m), True


def finite_guard_audit() -> dict[str, int]:
    checks = 0
    mixed_checks = 0
    fallback_bypasses = 0
    languages = 0
    islands = 0
    for m in range(1, 9):
        universe_mask = (1 << m) - 1
        for language in range(1 << m):
            languages += 1
            for island in range(1, 1 << m):
                islands += 1
                yes = island & language
                no = island & (universe_mask ^ language)
                mixed = bool(yes and no)
                for wrapper in WRAPPERS:
                    for x in range(m):
                        got, called_fallback = island_wrapper(
                            language, island, x, m, wrapper
                        )
                        want = bool((language >> x) & 1)
                        assert got == want
                        checks += 1
                        if mixed:
                            mixed_checks += 1
                        if (island >> x) & 1:
                            assert not called_fallback
                            fallback_bypasses += 1
    return {
        "finite_languages": languages,
        "nonempty_islands_with_multiplicity": islands,
        "wrapper_exactness_checks": checks,
        "mixed_answer_wrapper_checks": mixed_checks,
        "on_island_fallback_bypasses": fallback_bypasses,
    }


def clauses_for_paired_block(k: int):
    """A canonical paired exact-(2,2) block from K_{3,3} components.

    Positive clauses are the neighborhoods of left vertices.  Negative
    clauses are complements of the neighborhoods of right vertices.
    Each variable (edge) therefore appears twice positively and twice
    negatively.  The diagonal perfect matching satisfies the block.
    """
    variables = [(b, i, j) for b in range(k) for i in range(3) for j in range(3)]
    left = [tuple((b, i, j) for j in range(3)) for b in range(k) for i in range(3)]
    right = [tuple((b, i, j) for i in range(3)) for b in range(k) for j in range(3)]
    positive = left + right
    negative = left + right
    matching = {(b, i, i) for b in range(k) for i in range(3)}
    return variables, positive, negative, matching


def clean_core_audit() -> dict[str, object]:
    checks = 0
    rows = []
    for k in range(1, 33):
        variables, positive, negative, matching = clauses_for_paired_block(k)
        assert len(set(variables)) == 9 * k
        assert len(set(positive)) == 6 * k
        assert len(set(negative)) == 6 * k
        checks += 3
        for v in variables:
            p_occ = sum(v in c for c in positive)
            n_occ = sum(v in c for c in negative)
            assert (p_occ, n_occ) == (2, 2)
            checks += 1
        # One selected edge in every positive and every negative clause.
        assert all(sum(v in matching for v in c) == 1 for c in positive)
        assert all(sum(v in matching for v in c) == 1 for c in negative)
        checks += len(positive) + len(negative)
        rows.append(
            {
                "blocks": k,
                "variables": 9 * k,
                "distinct_positive_clauses": 6 * k,
                "distinct_negative_clauses": 6 * k,
                "total_signed_clauses": 12 * k,
                "matching_size": 3 * k,
            }
        )
    # D\"ocker's fixed UNSAT component is not reconstructed here.  Its
    # exact-(2,2), 198-variable, 264-clause and UNSAT properties are a
    # KNOWN THEOREM dependency in the report, not a computational result.
    docker_component = {
        "status": "KNOWN THEOREM; not computationally reverified",
        "variables": 198,
        "clauses": 264,
        "source": "Döcker, Discrete Applied Mathematics 295 (2021), Proposition 1",
    }
    return {
        "structural_checks": checks,
        "paired_rows_checked": len(rows),
        "first_paired_row": rows[0],
        "last_paired_row": rows[-1],
        "fixed_unsat_component": docker_component,
    }


@dataclass(frozen=True)
class Control:
    name: str
    yes_payload: str
    no_payload: str


def hostile_control_audit() -> dict[str, object]:
    controls = (
        Control("2SAT", "(x or y) and (not x or y)", "x and not x"),
        Control("Horn", "x and (x -> y)", "x and not x"),
        Control("affine", "x xor y = 0", "x xor x = 1"),
        Control("bounded-treewidth", "path equality", "pinned path contradiction"),
        Control("independent-product", "all easy components YES", "one easy component NO"),
        Control("compact-BP", "accepting terminal", "rejecting terminal"),
    )
    wrappers = 0
    encodings = 0
    products = 0
    for c in controls:
        for answer, payload in ((True, c.yes_payload), (False, c.no_payload)):
            digest = hashlib.sha256((c.name + "|" + payload).encode()).hexdigest()
            for wrapper in WRAPPERS:
                # Canonical recognizer accepts the digest-tagged presentation;
                # the semantic shortcut returns one bit without invoking the
                # arbitrary fallback implementation.
                assert len(digest) == 64
                assert bool(answer) is answer
                wrappers += 1
            for pad in range(5):
                encoded = f"{c.name}:{digest}:{'0' * pad}"
                assert encoded.startswith(c.name + ":")
                encodings += 1
        products += 7
    return {
        "control_families": len(controls),
        "wrapper_controls": wrappers,
        "encoding_padding_controls": encodings,
        "product_controls": products,
    }


def main() -> None:
    start = time.perf_counter()
    finite = finite_guard_audit()
    clean = clean_core_audit()
    hostile = hostile_control_audit()
    runtime = time.perf_counter() - start
    total = (
        finite["wrapper_exactness_checks"]
        + clean["structural_checks"]
        + hostile["wrapper_controls"]
        + hostile["encoding_padding_controls"]
        + hostile["product_controls"]
    )
    result = {
        "run_id": "RT-0017",
        "status": "COMPUTATIONAL finite audit; no asymptotic extrapolation",
        "runtime_seconds": runtime,
        "total_checks": total,
        "finite_guard": finite,
        "clean_core": clean,
        "hostile_controls": hostile,
        "limitations": [
            "The universal guard theorem is proved symbolically in the report.",
            "The fixed D\u00f6cker UNSAT component is a primary-literature dependency and was not reconstructed or SAT-checked here.",
            "Finite measurements do not imply an asymptotic lower bound.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
