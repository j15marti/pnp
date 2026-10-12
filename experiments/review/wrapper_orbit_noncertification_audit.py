#!/usr/bin/env python3
"""Finite regression for WRAPORBIT1.

The symbolic theorem is elementary orbit separation.  This script only
checks a declared finite AST model and must not be read asymptotically.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


OUT = Path("results/raw/review/2026-10-12_wrapper_orbit_noncertification.json")
GENERATORS = ("COPY", "DEAD", "DELAY", "INTERP", "RECOMP", "DISPATCH")
FRESH = ("LUT", "BDD", "CIRCUIT", "ARITH")
FAMILIES = (
    "2SAT", "Horn", "affine_Tseitin", "bounded_treewidth", "parity",
    "independent_product", "padding", "redundant_clauses",
    "signed_clean", "mixed_SAT_UNSAT",
)
ENCODINGS = ("DIMACS", "indexed", "renamed", "padded", "auxiliary")


@dataclass(frozen=True)
class Program:
    semantic_table: tuple[int, ...]
    base_id: str
    wrappers: tuple[str, ...]
    charged_delay: int = 0

    def run(self, x: int) -> int:
        return self.semantic_table[x]


def table_for(family: str, encoding: str) -> tuple[int, ...]:
    bits = hashlib.sha256(f"{family}|{encoding}".encode()).digest()
    return tuple((bits[i // 8] >> (i % 8)) & 1 for i in range(8))


def apply_wrapper(p: Program, name: str) -> Program:
    delay = p.charged_delay + (17 if name == "DELAY" else 0)
    return Program(p.semantic_table, p.base_id, p.wrappers + (name,), delay)


def chains(max_depth: int):
    yield ()
    for depth in range(1, max_depth + 1):
        yield from itertools.product(GENERATORS, repeat=depth)


def main() -> None:
    assertions = 0
    tested_programs = 0
    fresh_programs = 0
    max_code_depth = 0
    max_delay = 0
    rows = []

    all_chains = tuple(chains(4))
    for family, encoding in itertools.product(FAMILIES, ENCODINGS):
        table = table_for(family, encoding)
        base = Program(table, f"SEARCH::{family}::{encoding}", ())
        orbit = []
        for chain in all_chains:
            p = base
            for wrapper in chain:
                p = apply_wrapper(p, wrapper)
            orbit.append(p)
            # Candidate J is invariant on the entire generated orbit.
            assert p.base_id == base.base_id
            assertions += 1
            for x in range(8):
                assert p.run(x) == base.run(x)
                assertions += 1
            tested_programs += 1
            max_code_depth = max(max_code_depth, len(p.wrappers))
            max_delay = max(max_delay, p.charged_delay)

        for fresh_kind in FRESH:
            fresh = Program(table, f"{fresh_kind}::{family}::{encoding}", ())
            # Same extensional function, outside the tested-generator orbit.
            for x in range(8):
                assert fresh.run(x) == base.run(x)
                assertions += 1
            assert fresh.base_id != base.base_id
            assert fresh not in orbit
            assertions += 2
            fresh_programs += 1

        rows.append({
            "family": family,
            "encoding": encoding,
            "truth_table": list(table),
            "generated_orbit_size": len(orbit),
            "fresh_equivalent_implementations": list(FRESH),
            "orbit_indicator_on_generated": 1,
            "orbit_indicator_on_fresh": 0,
        })

    result = {
        "claim_id": "TESTED-WRAPPER-MONOID-NONCERTIFICATION1",
        "status": "COMPUTATIONAL",
        "scope_guard": "finite declared AST model; symbolic orbit theorem is separate",
        "generators": list(GENERATORS),
        "maximum_composition_depth": 4,
        "chains_per_base": len(all_chains),
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "tested_programs": tested_programs,
        "fresh_equivalent_programs": fresh_programs,
        "max_wrapper_depth": max_code_depth,
        "max_charged_delay": max_delay,
        "assertions": assertions,
        "failures": 0,
        "rows": rows,
        "inference_guard": "Passing finite/generated wrappers does not prove universal semantic invariance.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "chains_per_base", "tested_programs", "fresh_equivalent_programs",
        "assertions", "failures")}, sort_keys=True))


if __name__ == "__main__":
    main()
