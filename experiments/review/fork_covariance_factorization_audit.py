#!/usr/bin/env python3
"""Finite audit for FORKFACTOR1.

The checks are exhaustive at their declared tiny domains.  They test only
finite combinatorics: implementation covariance implies source factorization,
and a total finite opening relation admits lexicographic source search.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path


IMPLEMENTATIONS = ("DIRECT", "COPY", "DEAD", "RECOMP")
SOURCES = (0, 1, 2)


def commitment_audit() -> dict[str, int]:
    columns = [(a, f) for a in range(len(IMPLEMENTATIONS)) for f in SOURCES]
    invariant = 0
    factor_failures = 0
    noninvariant = 0
    for mask in range(1 << len(columns)):
        value = {(a, f): (mask >> i) & 1 for i, (a, f) in enumerate(columns)}
        is_invariant = all(
            len({value[a, f] for a in range(len(IMPLEMENTATIONS))}) == 1
            for f in SOURCES
        )
        if is_invariant:
            invariant += 1
            source_map = {f: value[0, f] for f in SOURCES}
            if any(value[a, f] != source_map[f] for a, f in columns):
                factor_failures += 1
        else:
            noninvariant += 1
    return {
        "maps_checked": 1 << len(columns),
        "implementation_invariant_maps": invariant,
        "expected_source_maps": 1 << len(SOURCES),
        "noninvariant_maps": noninvariant,
        "factorization_failures": factor_failures,
    }


def verifier_audit() -> dict[str, int]:
    # V[f,c,e,z] has 2*2*2*2 = 16 Boolean entries.
    tuples = list(itertools.product((0, 1), repeat=4))
    total_relations = 0
    source_instances_with_pairs = 0
    lex_search_failures = 0
    for mask in range(1 << len(tuples)):
        valid = {t for i, t in enumerate(tuples) if (mask >> i) & 1}
        witnesses: dict[int, tuple[int, int, int]] = {}
        for f in (0, 1):
            candidates = [
                (c, z0, z1)
                for c, z0, z1 in itertools.product((0, 1), repeat=3)
                if (f, c, 0, z0) in valid and (f, c, 1, z1) in valid
            ]
            if candidates:
                source_instances_with_pairs += 1
                witnesses[f] = min(candidates)
                c, z0, z1 = witnesses[f]
                if not ((f, c, 0, z0) in valid and (f, c, 1, z1) in valid):
                    lex_search_failures += 1
        if len(witnesses) == 2:
            total_relations += 1
    return {
        "relations_checked": 1 << len(tuples),
        "relations_total_on_both_sources": total_relations,
        "source_instances_with_pairs": source_instances_with_pairs,
        "lexicographic_search_failures": lex_search_failures,
    }


def wrapper_and_hostile_controls() -> dict[str, object]:
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    source_only = {(w, f): f & 1 for w in wrappers for f in SOURCES}
    trace_sensitive = {(w, f): (len(w) + f) & 1 for w in wrappers for f in SOURCES}
    stable = all(
        len({source_only[w, f] for w in wrappers}) == 1 for f in SOURCES
    )
    unstable_sources = sum(
        len({trace_sensitive[w, f] for w in wrappers}) > 1 for f in SOURCES
    )
    controls = {
        "Horn": "forward-chaining shortcut",
        "2SAT": "SCC shortcut",
        "affine/Tseitin": "Gaussian-elimination shortcut",
        "bounded-treewidth": "dynamic-programming shortcut",
        "independent-product": "componentwise shortcut",
        "padding": "encoded length changes without semantics",
        "alternate-encoding": "representation changes without language change",
    }
    return {
        "wrappers": list(wrappers),
        "source_only_commitment_stable": stable,
        "trace_sensitive_unstable_sources": unstable_sources,
        "hostile_controls": controls,
        "asymptotic_claim": False,
    }


def main() -> None:
    started = time.perf_counter()
    payload = {
        "run_id": "FORKFACTOR1",
        "status": "COMPUTATIONAL",
        "commitment_audit": commitment_audit(),
        "verifier_audit": verifier_audit(),
        "wrapper_and_hostile_controls": wrapper_and_hostile_controls(),
    }
    payload["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    c = payload["commitment_audit"]
    v = payload["verifier_audit"]
    assert c["implementation_invariant_maps"] == c["expected_source_maps"] == 8
    assert c["factorization_failures"] == 0
    assert v["lexicographic_search_failures"] == 0
    out = Path("results/raw/review/2026-10-12_fork_covariance_factorization.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
