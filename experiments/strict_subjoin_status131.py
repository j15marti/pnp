#!/usr/bin/env python3
"""Independent audit for STRICT-SUBJOIN-STATUS131.

The declared source language consists of signed exact-one constraints on
four Boolean variables.  This script checks the matched pair from
EXACTONE-JOIN-CYCLE95, every strict module subset, every module partition,
the exact two-half boundary relations, all eight signings of the fourth
module, and renaming/order controls.

Finite results are computational checks.  The report contains the symbolic
minimal-UNSAT and adaptive transcript proofs.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Iterable, Sequence

Assignment = tuple[int, int, int, int]
Literal = tuple[int, bool]  # variable index 0..3, negated?
Module = tuple[Literal, Literal, Literal]


VARS = (0, 1, 2, 3)  # a,b,c,d
TRIPLES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


def module(triple: Sequence[int], signs: Sequence[int] = (0, 0, 0)) -> Module:
    return tuple((v, bool(s)) for v, s in zip(triple, signs))  # type: ignore[return-value]


def lit_value(a: Assignment, lit: Literal) -> int:
    value = a[lit[0]]
    return value ^ int(lit[1])


def exact_one(a: Assignment, mod: Module) -> bool:
    return sum(lit_value(a, lit) for lit in mod) == 1


def solutions(mods: Sequence[Module]) -> list[Assignment]:
    return [
        a
        for a in itertools.product((0, 1), repeat=4)
        if all(exact_one(a, mod) for mod in mods)
    ]


def set_partitions(items: tuple[int, ...]) -> Iterable[tuple[tuple[int, ...], ...]]:
    if not items:
        yield ()
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        yield ((first,),) + part
        for i in range(len(part)):
            yield part[:i] + (tuple(sorted((first,) + part[i])),) + part[i + 1 :]


def canonical_partition(part: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in part), key=lambda b: (b[0], len(b), b)))


def boundary_relation(mods: Sequence[Module], indices: Sequence[int]) -> set[Assignment]:
    return set(solutions([mods[i] for i in indices]))


def renamed(mods: Sequence[Module], perm: Sequence[int]) -> list[Module]:
    return [tuple((perm[v], neg) for v, neg in mod) for mod in mods]  # type: ignore[list-item]


def main() -> None:
    checks = 0
    positive = [module(t) for t in TRIPLES]
    signed = positive[:3] + [module(TRIPLES[3], (1, 0, 0))]

    pos_solutions = solutions(positive)
    sig_solutions = solutions(signed)
    assert not pos_solutions
    assert sig_solutions == [(1, 0, 0, 0)]
    checks += 2

    subset_rows = []
    for mask in range(1 << 4):
        idx = tuple(i for i in range(4) if mask & (1 << i))
        pos_count = len(solutions([positive[i] for i in idx]))
        sig_count = len(solutions([signed[i] for i in idx]))
        if mask != 0b1111:
            assert pos_count > 0 and sig_count > 0
            checks += 2
        subset_rows.append({
            "mask": f"{mask:04b}",
            "indices": [i + 1 for i in idx],
            "positive_models": pos_count,
            "signed_models": sig_count,
            "positive_sat": bool(pos_count),
            "signed_sat": bool(sig_count),
        })

    # Every partition into at least two blocks receives the all-YES vector
    # on both labels when only block-SAT bits are exposed.
    parts = {
        canonical_partition(p)
        for p in set_partitions((0, 1, 2, 3))
        if len(p) >= 2
    }
    partition_rows = []
    for part in sorted(parts):
        pvec = tuple(bool(solutions([positive[i] for i in block])) for block in part)
        svec = tuple(bool(solutions([signed[i] for i in block])) for block in part)
        assert pvec == svec == (True,) * len(part)
        checks += 2
        partition_rows.append({
            "blocks": [[i + 1 for i in block] for block in part],
            "positive_statuses": list(pvec),
            "signed_statuses": list(svec),
        })

    # The exact named relations of the two halves do distinguish the pair.
    left_pos = boundary_relation(positive, (0, 1))
    right_pos = boundary_relation(positive, (2, 3))
    left_sig = boundary_relation(signed, (0, 1))
    right_sig = boundary_relation(signed, (2, 3))
    assert left_pos == left_sig
    assert len(left_pos) == len(right_pos) == len(right_sig) == 3
    assert len(left_pos & right_pos) == 0
    assert len(left_sig & right_sig) == 1
    checks += 5

    # All eight fourth-module signings: record full labels and determine
    # whether every strict subjoin remains satisfiable.  This is a hostile
    # control, not an assumed invariant; some two-negation variants fail it.
    signing_rows = []
    for bits in itertools.product((0, 1), repeat=3):
        mods = positive[:3] + [module(TRIPLES[3], bits)]
        full_count = len(solutions(mods))
        strict_min = 16
        unsat_strict_masks = []
        for mask in range(1 << 4):
            if mask == 0b1111:
                continue
            idx = [i for i in range(4) if mask & (1 << i)]
            c = len(solutions([mods[i] for i in idx]))
            strict_min = min(strict_min, c)
            if c == 0:
                unsat_strict_masks.append(f"{mask:04b}")
            checks += 1
        signing_rows.append({
            "fourth_signs": list(bits),
            "full_models": full_count,
            "full_sat": bool(full_count),
            "minimum_strict_models": strict_min,
            "all_strict_subjoins_sat": not unsat_strict_masks,
            "unsat_strict_masks": unsat_strict_masks,
        })

    # Exhaust all 24 source-name permutations and 24 module orders for the
    # two distinguished labels.  SAT labels and strict-subjoin property are
    # invariant.
    permutation_cases = 0
    for perm in itertools.permutations(VARS):
        for order in itertools.permutations(range(4)):
            for base, expected in ((positive, False), (signed, True)):
                mods0 = renamed(base, perm)
                mods = [mods0[i] for i in order]
                assert bool(solutions(mods)) is expected
                checks += 1
                for omit in range(4):
                    assert solutions([mods[i] for i in range(4) if i != omit])
                    checks += 1
                permutation_cases += 1

    # Adaptive restricted-policy transcript: any sequence of strict subset
    # SAT queries receives YES on both sources.  Exhaust all query sequences
    # of lengths 0..3 over the 15 strict masks as a finite control; the proof
    # in the report handles unbounded adaptive sequences.
    strict_masks = tuple(range(15))
    transcript_sequences = 0
    for length in range(4):
        for seq in itertools.product(strict_masks, repeat=length):
            p_answers = []
            s_answers = []
            for mask in seq:
                idx = [i for i in range(4) if mask & (1 << i)]
                p_answers.append(bool(solutions([positive[i] for i in idx])))
                s_answers.append(bool(solutions([signed[i] for i in idx])))
            assert p_answers == s_answers == [True] * length
            checks += 1
            transcript_sequences += 1

    # Direct source-aware control: the pair differs in exactly one literal
    # sign field.  A promise recognizer can read it and decide this pair.
    differing_fields = sum(
        int(lit_p != lit_s)
        for mod_p, mod_s in zip(positive, signed)
        for lit_p, lit_s in zip(mod_p, mod_s)
    )
    assert differing_fields == 1
    checks += 1

    result = {
        "run_id": "STRICT-SUBJOIN-STATUS131",
        "status": "COMPUTATIONAL finite audit; symbolic theorem in report",
        "checks": checks,
        "matched_pair": {
            "positive_full_models": len(pos_solutions),
            "signed_full_models": len(sig_solutions),
            "differing_literal_sign_fields": differing_fields,
        },
        "all_strict_subjoins_sat": True,
        "strict_subset_rows": subset_rows,
        "partition_count": len(parts),
        "partition_rows": partition_rows,
        "two_half_relation": {
            "left_size": len(left_pos),
            "positive_right_size": len(right_pos),
            "signed_right_size": len(right_sig),
            "positive_intersection": len(left_pos & right_pos),
            "signed_intersection": len(left_sig & right_sig),
        },
        "fourth_module_signings": signing_rows,
        "renaming_order_label_cases": permutation_cases,
        "adaptive_sequences_length_at_most_3": transcript_sequences,
        "limitations": [
            "Strict-subjoin SAT-bit oracle model only.",
            "Source-aware direct sign inspection distinguishes the pair cheaply.",
            "Finite tests do not imply asymptotic lower bounds.",
        ],
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["prehash_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
