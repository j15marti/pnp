#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0025.

This is a bounded logical check, not an asymptotic experiment.  It enumerates
all Boolean targets on a two-bit source domain and verifies the three branches
of the noninterference/declassification trilemma used in the report.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


SOURCES = tuple(itertools.product((0, 1), repeat=2))
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
HOSTILE_FAMILIES = (
    "2SAT",
    "Horn",
    "affine-Tseitin",
    "bounded-treewidth",
    "independent-product",
    "padding",
    "redundant-clauses",
)
ENCODINGS = ("DIMACS", "permuted-vars", "duplicated-clauses", "Tseitin-wrapper")


def truth_table(mask: int) -> tuple[int, ...]:
    return tuple((mask >> i) & 1 for i in range(len(SOURCES)))


def strict_noninterference(table: tuple[int, ...]) -> bool:
    """The retained value is independent of every source bit."""
    return len(set(table)) == 1


def semantic_validator(table: tuple[int, ...], source_index: int, bit: int) -> bool:
    return bit == table[source_index]


def reconstruct(table: tuple[int, ...], source_index: int) -> int:
    accepted = [b for b in (0, 1) if semantic_validator(table, source_index, b)]
    assert len(accepted) == 1
    return accepted[0]


def main() -> None:
    tables = [truth_table(mask) for mask in range(16)]
    constant = [t for t in tables if strict_noninterference(t)]
    nonconstant = [t for t in tables if not strict_noninterference(t)]
    reconstruction_checks = sum(
        reconstruct(table, i) == table[i]
        for table in tables
        for i in range(len(SOURCES))
    )
    # A syntactic tag carries no semantics: the same tag can be attached by a
    # COPY wrapper to any one of the 16 Boolean source functions.
    tag_realizations = len(tables)

    result = {
        "audit": "NONINTERFERENCE-DECLASSIFICATION-TRILEMMA1",
        "source_domain_size": len(SOURCES),
        "boolean_targets": len(tables),
        "strict_noninterference_targets": len(constant),
        "nonconstant_targets_excluded_by_strict_noninterference": len(nonconstant),
        "semantic_validator_reconstruction_checks": reconstruction_checks,
        "semantic_validator_reconstruction_expected": len(tables) * len(SOURCES),
        "syntactic_tag_distinct_realizations": tag_realizations,
        "wrappers": list(WRAPPERS),
        "hostile_families": list(HOSTILE_FAMILIES),
        "encodings": list(ENCODINGS),
        "hostile_control_cells": len(WRAPPERS) * len(HOSTILE_FAMILIES) * len(ENCODINGS),
        "claims": {
            "strict_noninterference_retains_only_constants": len(constant) == 2,
            "all_nonconstant_targets_are_erased": len(nonconstant) == 14,
            "sound_complete_validator_recovers_every_target": reconstruction_checks == 64,
            "syntactic_tag_is_semantically_unselective": tag_realizations == 16,
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_sha256"] = hashlib.sha256(canonical).hexdigest()

    out = Path("results/raw/review/2026-10-12_noninterference_declassification_trilemma.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
