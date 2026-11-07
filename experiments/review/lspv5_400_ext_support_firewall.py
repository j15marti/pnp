#!/usr/bin/env python3
"""Independent finite checker for the corrected PC+Ext support hypotheses.

This does not implement R_mix341.  It checks only the syntactic hypotheses
stated in Definition 4 of Impagliazzo--Mouli--Pitassi (CCC 2023), together
with the 2026 ECCC author correction requiring disjoint variable sets.
"""

from __future__ import annotations

import json
import resource
import time
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Ext:
    out: int
    support: tuple[int, ...]
    uses_extension: bool = False


def validate(exts: tuple[Ext, ...], kappa: int) -> dict:
    if kappa < 0:
        raise ValueError("negative kappa")
    outs: set[int] = set()
    support_sets: list[set[int]] = []
    repeated_input_count = 0
    for e in exts:
        if e.out <= 0:
            raise ValueError("nonpositive output id")
        if e.out in outs:
            raise ValueError("output not globally fresh")
        outs.add(e.out)
        if not e.support:
            raise ValueError("empty support")
        if any(v <= 0 for v in e.support):
            raise ValueError("nonpositive input id")
        repeated_input_count += len(e.support) - len(set(e.support))
        s = set(e.support)
        if len(s) > kappa:
            raise ValueError("arity exceeds kappa")
        support_sets.append(s)

    conflicts = [
        (i, j, sorted(support_sets[i] & support_sets[j]))
        for i, j in combinations(range(len(exts)), 2)
        if support_sets[i] & support_sets[j]
    ]
    recursive = [i for i, e in enumerate(exts) if e.uses_extension]
    return {
        "count": len(exts),
        "kappa": kappa,
        "original_only": not recursive,
        "recursive_indices": recursive,
        "pairwise_disjoint": not conflicts,
        "conflicts": conflicts,
        "repeated_input_count": repeated_input_count,
        "max_disjoint_subset": maximum_disjoint_subset(support_sets),
    }


def maximum_disjoint_subset(supports: list[set[int]]) -> int:
    best = 0
    n = len(supports)
    for mask in range(1 << n):
        if mask.bit_count() <= best:
            continue
        used: set[int] = set()
        ok = True
        for i, s in enumerate(supports):
            if mask >> i & 1:
                if used & s:
                    ok = False
                    break
                used |= s
        if ok:
            best = mask.bit_count()
    return best


def expect_reject(fn, label: str, rejected: list[str]) -> None:
    try:
        fn()
    except ValueError:
        rejected.append(label)
        return
    raise AssertionError(f"corruption accepted: {label}")


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    rejected: list[str] = []

    # Pairwise-disjoint arity-two original-variable definitions.
    disjoint = tuple(Ext(10_000 + i, (2 * i + 1, 2 * i + 2)) for i in range(8))
    d = validate(disjoint, 2)
    assert d["original_only"] and d["pairwise_disjoint"]
    assert d["max_disjoint_subset"] == 8
    assertions += 3

    # Star overlap: every support is a 2-junta, but all share x_1.
    star = tuple(Ext(20_000 + i, (1, i + 2)) for i in range(8))
    s = validate(star, 2)
    assert s["original_only"] and not s["pairwise_disjoint"]
    assert len(s["conflicts"]) == 28
    assert s["max_disjoint_subset"] == 1
    assertions += 4

    # A recursive/nested definition is outside Definition 4 even if fan-in is 2.
    nested = (
        Ext(30_001, (101, 102)),
        Ext(30_002, (103, 104)),
        Ext(30_003, (30_001, 30_002), uses_extension=True),
    )
    n = validate(nested, 2)
    assert not n["original_only"] and n["recursive_indices"] == [2]
    assertions += 2

    # Large numerical IDs and repeated inputs: duplicate inputs collapse as support.
    large_repeat = (Ext(2**61 + 1, (2**60 + 3, 2**60 + 3)),)
    r = validate(large_repeat, 1)
    assert r["pairwise_disjoint"] and r["repeated_input_count"] == 1
    assertions += 2

    expect_reject(lambda: validate((Ext(1, (2,)), Ext(1, (3,))), 1),
                  "duplicate-output", rejected)
    expect_reject(lambda: validate((Ext(0, (2,)),), 1),
                  "nonpositive-output", rejected)
    expect_reject(lambda: validate((Ext(1, ()),), 1),
                  "empty-support", rejected)
    expect_reject(lambda: validate((Ext(1, (2, 3)),), 1),
                  "arity-overflow", rejected)
    expect_reject(lambda: validate((Ext(1, (-2,)),), 1),
                  "nonpositive-input", rejected)
    expect_reject(lambda: validate(tuple(), -1),
                  "negative-kappa", rejected)
    assertions += len(rejected)

    summary = {
        "status": "PASS",
        "scope": "finite syntactic hypothesis firewall; not authoritative R_mix341 execution",
        "paper_model": "nonrecursive z_j-Q_j(original variables), kappa-juntas",
        "author_correction": "extension supports must be pairwise disjoint",
        "disjoint_control": d,
        "star_overlap_control": s,
        "nested_control": n,
        "large_repeat_control": r,
        "assertions": assertions,
        "corruptions_rejected": rejected,
        "elapsed_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
