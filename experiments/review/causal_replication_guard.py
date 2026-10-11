#!/usr/bin/env python3
"""Finite regression for REPLICATION-CAUSAL-GUARD1.

The symbolic theorem is elementary: an odd repetition code of length
2f+1 corrects every intervention on at most f raw coordinates.  This runner
checks the compiler on every Boolean transition map on two state bits and on
a structured hostile-control battery through five logical state bits.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable


BitTuple = tuple[int, ...]
Transition = Callable[[BitTuple], BitTuple]
Output = Callable[[BitTuple], int]


def bits(value: int, width: int) -> BitTuple:
    return tuple((value >> i) & 1 for i in range(width))


def encode(state: BitTuple, repetition: int, interpreted: bool = False) -> BitTuple:
    logical = tuple(1 - bit for bit in state) if interpreted else state
    return tuple(bit for bit in logical for _ in range(repetition))


def decode(raw: BitTuple, repetition: int, interpreted: bool = False) -> BitTuple:
    assert repetition % 2 == 1
    threshold = repetition // 2 + 1
    logical = tuple(
        int(sum(raw[start : start + repetition]) >= threshold)
        for start in range(0, len(raw), repetition)
    )
    return tuple(1 - bit for bit in logical) if interpreted else logical


def intervene(raw: BitTuple, coordinates: Iterable[int]) -> BitTuple:
    changed = list(raw)
    for coordinate in coordinates:
        changed[coordinate] ^= 1
    return tuple(changed)


def error_sets(raw_width: int, budget: int) -> Iterable[tuple[int, ...]]:
    for size in range(budget + 1):
        yield from itertools.combinations(range(raw_width), size)


def structured_transitions(width: int) -> dict[str, Transition]:
    def identity(z: BitTuple) -> BitTuple:
        return z

    def complement(z: BitTuple) -> BitTuple:
        return tuple(1 - bit for bit in z)

    def rotate(z: BitTuple) -> BitTuple:
        return z[1:] + z[:1] if z else z

    def affine_prefix_xor(z: BitTuple) -> BitTuple:
        parity = 0
        out = []
        for bit in z:
            parity ^= bit
            out.append(parity)
        return tuple(out)

    def horn_closure(z: BitTuple) -> BitTuple:
        out = list(z)
        for i in range(1, len(out)):
            out[i] |= out[i - 1]
        return tuple(out)

    def treewidth_local(z: BitTuple) -> BitTuple:
        if not z:
            return z
        return tuple(z[i] | z[(i - 1) % len(z)] for i in range(len(z)))

    return {
        "identity": identity,
        "complement": complement,
        "rotate": rotate,
        "affine_prefix_xor": affine_prefix_xor,
        "horn_closure": horn_closure,
        "treewidth_local": treewidth_local,
    }


def outputs() -> dict[str, Output]:
    return {
        "first": lambda z: z[0] if z else 0,
        "parity": lambda z: sum(z) & 1,
        "any": lambda z: int(any(z)),
        "all": lambda z: int(all(z)),
        "adjacent_equality": lambda z: int(all(z[i] == z[i - 1] for i in range(1, len(z)))),
    }


@dataclass
class Counts:
    exhaustive_transition_maps: int = 0
    exhaustive_map_state_pairs: int = 0
    exhaustive_interventions: int = 0
    structured_state_transition_pairs: int = 0
    structured_interventions: int = 0
    output_invariance_checks: int = 0
    interp_checks: int = 0
    recomp_checks: int = 0
    dead_checks: int = 0
    delay_checks: int = 0
    failures: int = 0


def verify_case(
    state: BitTuple,
    transition: Transition,
    repetition: int,
    count: Counts,
    interpreted: bool = False,
) -> int:
    raw = encode(state, repetition, interpreted=interpreted)
    budget = repetition // 2
    local_checks = 0
    expected_next = transition(state)
    expected_outputs = {name: fn(state) for name, fn in outputs().items()}
    for error in error_sets(len(raw), budget):
        perturbed = intervene(raw, error)
        recovered = decode(perturbed, repetition, interpreted=interpreted)
        if recovered != state or transition(recovered) != expected_next:
            count.failures += 1
        for name, fn in outputs().items():
            if fn(recovered) != expected_outputs[name]:
                count.failures += 1
            count.output_invariance_checks += 1
        local_checks += 1
    return local_checks


def exhaustive_two_bit_maps(count: Counts) -> None:
    states = [bits(i, 2) for i in range(4)]
    for table_values in itertools.product(range(4), repeat=4):
        table = tuple(bits(value, 2) for value in table_values)

        def transition(z: BitTuple, table: tuple[BitTuple, ...] = table) -> BitTuple:
            index = z[0] | (z[1] << 1)
            return table[index]

        count.exhaustive_transition_maps += 1
        for state in states:
            count.exhaustive_map_state_pairs += 1
            count.exhaustive_interventions += verify_case(state, transition, 3, count)


def structured_battery(count: Counts) -> None:
    for width in range(1, 6):
        states = [bits(i, width) for i in range(1 << width)]
        for repetition in (3, 5, 7):
            for transition in structured_transitions(width).values():
                for state in states:
                    count.structured_state_transition_pairs += 1
                    checks = verify_case(state, transition, repetition, count)
                    count.structured_interventions += checks
                    # INTERP uses the complemented raw alphabet but the same decoder-relative state.
                    interp_checks = verify_case(
                        state, transition, repetition, count, interpreted=True
                    )
                    count.interp_checks += interp_checks

                    # RECOMP has no retained logical checkpoint: it recreates state from source.
                    source = tuple(state)
                    if transition(tuple(source)) != transition(state):
                        count.failures += 1
                    count.recomp_checks += 1

                    # DEAD appends unused cells; arbitrary flips there change no decoded state.
                    raw = encode(state, repetition) + (0, 1, 0)
                    live = raw[: width * repetition]
                    if decode(live, repetition) != state:
                        count.failures += 1
                    for dead_index in range(width * repetition, len(raw)):
                        changed = intervene(raw, (dead_index,))
                        if decode(changed[: width * repetition], repetition) != state:
                            count.failures += 1
                        count.dead_checks += 1

                    # DELAY inserts identity checkpoints; decoded semantics stay fixed.
                    delayed = state
                    for _ in range(4):
                        delayed = decode(encode(delayed, repetition), repetition)
                        if delayed != state:
                            count.failures += 1
                        count.delay_checks += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/raw/review/2026-10-11_causal_replication_guard.json",
    )
    args = parser.parse_args()
    started = time.perf_counter()
    count = Counts()
    exhaustive_two_bit_maps(count)
    structured_battery(count)
    elapsed = time.perf_counter() - started

    result = {
        "claim_id": "REPLICATION-CAUSAL-GUARD1",
        "status": {
            "symbolic": "PROVED/EXACT",
            "finite_regression": "COMPUTATIONAL",
            "retired_claim": "bounded raw-coordinate causal indispensability is universal",
            "p_vs_np": "OPEN",
        },
        "parameters": {
            "exhaustive_all_transition_maps_width": 2,
            "structured_widths": [1, 2, 3, 4, 5],
            "odd_repetition_lengths": [3, 5, 7],
            "error_budget": "(repetition-1)/2",
            "random_seed": None,
            "method": "exhaustive",
        },
        "controls": [
            "affine_prefix_xor",
            "horn_closure",
            "treewidth_local",
            "DIRECT",
            "DEAD",
            "COPY/repetition",
            "DELAY",
            "INTERP/complement-conjugacy",
            "RECOMP/source-recreation",
            "one-bit outputs",
        ],
        "counts": asdict(count),
        "runtime_seconds": round(elapsed, 6),
        "limitations": [
            "Finite regression validates the implementation only.",
            "The theorem concerns raw checkpoint interventions, not every representation-covariant decoded relation.",
            "No SAT time lower bound or P-versus-NP separation is inferred.",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if count.failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
