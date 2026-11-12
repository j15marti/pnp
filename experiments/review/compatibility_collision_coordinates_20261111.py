#!/usr/bin/env python3
"""Exhaustive coordinate audit for compatible adaptive collision chains.

The verified producer supplies the Feistel permutation and gate-to-proper-3CNF
compiler. This script tests a new theorem-sized object: ordered collision chains
are parametrized by one output label and one orientation bit per stage. A global
compatibility formula can kill forward prefixes without forcing source-first
witness construction to backtrack.

This is finite COMPUTATIONAL evidence. It does not measure H, enumerate programs,
establish a lower bound, or settle P versus NP. One invocation is under 30 seconds.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
DEPENDENCY = HERE.with_name("witness_amplifier_controls_20261111.py")
SPEC = importlib.util.spec_from_file_location("verified_collision_producer", DEPENDENCY)
assert SPEC is not None and SPEC.loader is not None
PRODUCER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRODUCER)

# Label order: z1[0], z1[1], z1[2], z2[0], z2[1], z2[2].
# The first four clauses express z1[0] == z2[0]. The last four
# express z2[0] == 1. The padding uses the other label bits, so
# this source formula itself is proper 3-CNF and uses all six bits.
SOURCE_CLAUSES = (
    (-1, 4, 2), (-1, 4, -2),
    (1, -4, 3), (1, -4, -3),
    (4, 5, 6), (4, 5, -6), (4, -5, 6), (4, -5, -6),
)
HALF_WIDTH = 2
DEPTH = 2
ROUNDS = 4
OUTPUT_WIDTH = 2 * HALF_WIDTH - 1
SEED = [1, 0, 1]


def source_truth(labels: tuple[int, ...]) -> bool:
    assert len(labels) == DEPTH * OUTPUT_WIDTH
    return all(
        any(labels[abs(lit) - 1] == int(lit > 0) for lit in clause)
        for clause in SOURCE_CLAUSES
    )


def key_of(previous_u: list[int], previous_v: list[int]) -> list[int]:
    return [
        previous_u[i % len(previous_u)]
        ^ previous_v[(i + 1) % len(previous_v)]
        for i in range(HALF_WIDTH)
    ]


def lift(
    labels: tuple[int, ...],
    orientations: tuple[int, ...] | None = None,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Uniform lift; source formula truth is never queried by this algorithm."""
    assert len(labels) == DEPTH * OUTPUT_WIDTH
    if orientations is None:
        orientations = (0,) * DEPTH
    assert len(orientations) == DEPTH
    previous_u, previous_v = list(SEED), list(reversed(SEED))
    chain = []
    for i in range(DEPTH):
        label = list(labels[i * OUTPUT_WIDTH:(i + 1) * OUTPUT_WIDTH])
        bit = orientations[i]
        key = key_of(previous_u, previous_v)
        u = PRODUCER.permute(label + [bit], key, ROUNDS, inverse=True)
        v = PRODUCER.permute(label + [1 - bit], key, ROUNDS, inverse=True)
        chain.append((tuple(u), tuple(v)))
        previous_u, previous_v = u, v
    return tuple(chain)


def decode(chain) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Forward evaluation validates a chain and recovers all coordinates."""
    assert len(chain) == DEPTH
    previous_u, previous_v = list(SEED), list(reversed(SEED))
    labels, orientations = [], []
    for tu, tv in chain:
        u, v = list(tu), list(tv)
        key = key_of(previous_u, previous_v)
        pu = PRODUCER.permute(u, key, ROUNDS)
        pv = PRODUCER.permute(v, key, ROUNDS)
        assert u != v
        assert pu[:-1] == pv[:-1]
        assert pu[-1] != pv[-1]
        labels.extend(pu[:-1])
        orientations.append(pu[-1])
        previous_u, previous_v = u, v
    return tuple(labels), tuple(orientations)


def compile_compatible_chain():
    """Producer's exact chain, with output wires exposed for source clauses."""
    circuit = PRODUCER.CircuitCNF()
    seed = [circuit.var(True) for _ in SEED]
    for bad in itertools.product((0, 1), repeat=len(SEED)):
        if list(bad) != SEED:
            circuit.raw.append(tuple(-v if bit else v for v, bit in zip(seed, bad)))
    seed_clauses = tuple(circuit.raw)
    previous_u, previous_v = seed, list(reversed(seed))
    stages, output_labels = [], []
    for _ in range(DEPTH):
        u = [circuit.var(True) for _ in range(2 * HALF_WIDTH)]
        v = [circuit.var(True) for _ in range(2 * HALF_WIDTH)]
        key = circuit.key(previous_u, previous_v, HALF_WIDTH)
        pu = circuit.feistel(u, key, ROUNDS)
        pv = circuit.feistel(v, key, ROUNDS)
        output_labels.extend(pu[:-1])
        for a, b in zip(pu[:-1], pv[:-1]):
            circuit.raw.extend(((-a, b), (a, -b)))
        differences = [circuit.gate("xor", a, b) for a, b in zip(u, v)]
        any_difference = differences[0]
        for x in differences[1:]:
            any_difference = circuit.gate("or", any_difference, x)
        circuit.raw.append((any_difference,))
        stages.append((u, v))
        previous_u, previous_v = u, v
    for clause in SOURCE_CLAUSES:
        circuit.raw.append(tuple(
            output_labels[abs(lit) - 1] * (1 if lit > 0 else -1)
            for lit in clause
        ))
    clauses = circuit.proper()
    return circuit, seed, stages, output_labels, seed_clauses, clauses


def complete_for_chain(circuit, seed, stages, chain):
    primary = dict(zip(seed, SEED))
    for (uw, vw), (u, v) in zip(stages, chain):
        primary.update(zip(uw, u))
        primary.update(zip(vw, v))
    return circuit.complete(primary)


def enumerate_forward_valid_chains():
    """Enumerate all valid ordered pairs by forward evaluation, not inversion."""
    words = list(itertools.product((0, 1), repeat=2 * HALF_WIDTH))
    prefixes = [()]
    candidate_pair_checks = 0
    valid_prefix_counts = []
    second_stage_keys = set()
    for stage in range(DEPTH):
        next_prefixes = []
        for prefix in prefixes:
            if prefix:
                previous_u, previous_v = map(list, prefix[-1])
            else:
                previous_u, previous_v = list(SEED), list(reversed(SEED))
            key = key_of(previous_u, previous_v)
            if stage == 1:
                second_stage_keys.add(tuple(key))
            images = {
                word: tuple(PRODUCER.permute(list(word), key, ROUNDS))
                for word in words
            }
            assert len(set(images.values())) == len(words)
            for u, v in itertools.product(words, repeat=2):
                candidate_pair_checks += 1
                if u != v and images[u][:-1] == images[v][:-1]:
                    next_prefixes.append(prefix + ((u, v),))
        prefixes = next_prefixes
        valid_prefix_counts.append(len(prefixes))
    return set(prefixes), candidate_pair_checks, valid_prefix_counts, second_stage_keys


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/raw/review/2026-11-11_COMPATIBILITY_CORE_RETRY/collision_coordinates.json",
    )
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(f"Append-only result already exists: {args.out}")
    started = time.perf_counter()
    circuit, seed, stages, label_wires, seed_clauses, clauses = compile_compatible_chain()
    assert all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in SOURCE_CLAUSES)
    assert set(abs(lit) for c in SOURCE_CLAUSES for lit in c) == set(range(1, 7))
    seed_accepts = []
    for seed_bits in itertools.product((0, 1), repeat=3):
        if PRODUCER.satisfies(seed_clauses, dict(zip(seed, seed_bits))):
            seed_accepts.append(seed_bits)
    assert seed_accepts == [tuple(SEED)]

    parameter_images = set()
    fixed_orientation_images = set()
    accepted_primary = set()
    source_model_count = 0
    parameter_checks = proper_checks = proper_accepts = raw_checks = 0
    fixed_lift_projection_checks = 0
    compatibility_by_prefix = {}
    all_labels = list(itertools.product((0, 1), repeat=DEPTH * OUTPUT_WIDTH))
    for labels in all_labels:
        expected = source_truth(labels)
        assert expected == bool(labels[0] and labels[3])
        source_model_count += int(expected)
        fixed_chain = lift(labels)
        assert decode(fixed_chain) == (labels, (0, 0))
        fixed_orientation_images.add(fixed_chain)
        fixed_lift_projection_checks += 1
        for orientations in itertools.product((0, 1), repeat=DEPTH):
            chain = lift(labels, orientations)
            assert decode(chain) == (labels, orientations)
            assert chain not in parameter_images
            parameter_images.add(chain)
            parameter_checks += 1
            assignment = complete_for_chain(circuit, seed, stages, chain)
            assert tuple(assignment[w] for w in label_wires) == labels
            assert PRODUCER.satisfies(circuit.raw, assignment) == expected
            raw_checks += 1
            for padding_bits in itertools.product((0, 1), repeat=2):
                padded_assignment = dict(assignment)
                padded_assignment.update(zip(circuit.padding, padding_bits))
                compiled = PRODUCER.satisfies(clauses, padded_assignment)
                assert compiled == expected
                proper_checks += 1
                proper_accepts += int(compiled)
            prefix = chain[:1]
            compatibility_by_prefix.setdefault(prefix, 0)
            compatibility_by_prefix[prefix] += int(expected)
            if expected:
                accepted_primary.add(chain)

    forward_chains, pair_checks, prefix_counts, second_stage_keys = enumerate_forward_valid_chains()
    assert forward_chains == parameter_images
    forward_decode_checks = 0
    for chain in forward_chains:
        labels, orientations = decode(chain)
        assert lift(labels, orientations) == chain
        assert (chain in accepted_primary) == source_truth(labels)
        forward_decode_checks += 1

    dead_prefixes = [p for p, count in compatibility_by_prefix.items() if count == 0]
    live_completion_counts = sorted(count for count in compatibility_by_prefix.values() if count)
    assert len(dead_prefixes) == 8
    assert live_completion_counts == [8] * 8
    naive_labels = (0,) * (DEPTH * OUTPUT_WIDTH)
    naive_chain = lift(naive_labels)
    naive_assignment = complete_for_chain(circuit, seed, stages, naive_chain)
    assert naive_chain[:1] in dead_prefixes
    assert not PRODUCER.satisfies(clauses, naive_assignment)
    compatible_labels = (1, 0, 0, 1, 0, 0)
    compatible_chain = lift(compatible_labels)
    compatible_assignment = complete_for_chain(circuit, seed, stages, compatible_chain)
    assert PRODUCER.satisfies(clauses, compatible_assignment)
    assert source_truth(decode(compatible_chain)[0])

    dimacs = f"p cnf {circuit.nvars} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    result = {
        "status": "COMPUTATIONAL",
        "claim_tested": "Bijection between adaptive ordered collision chains and output-label/orientation coordinates; exact compatibility pullback.",
        "script": str(HERE.relative_to(ROOT)),
        "script_sha256": hashlib.sha256(HERE.read_bytes()).hexdigest(),
        "dependency": str(DEPENDENCY.relative_to(ROOT)),
        "dependency_sha256": hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
        "random_seed": None,
        "parameters": {
            "half_width": HALF_WIDTH, "permutation_bits": 2 * HALF_WIDTH,
            "output_label_bits_per_stage": OUTPUT_WIDTH,
            "depth": DEPTH, "rounds": ROUNDS,
            "source_label_bits": DEPTH * OUTPUT_WIDTH,
            "orientation_bits": DEPTH,
        },
        "source_formula": {
            "clauses": SOURCE_CLAUSES,
            "proper_3cnf": True,
            "all_six_variables_used": True,
            "equivalent_condition": "z1[0] = z2[0] = 1",
            "assignments_exhausted": len(all_labels),
            "satisfying_assignments": source_model_count,
        },
        "coordinate_audit": {
            "parameter_strings_exhausted": parameter_checks,
            "distinct_valid_primary_chains": len(parameter_images),
            "inverse_decode_checks": parameter_checks,
            "forward_enumeration_candidate_pair_checks": pair_checks,
            "forward_valid_prefix_counts": prefix_counts,
            "forward_valid_chains": len(forward_chains),
            "forward_decode_and_reencode_checks": forward_decode_checks,
            "forward_and_coordinate_sets_equal": True,
            "distinct_second_stage_keys": sorted(second_stage_keys),
            "fixed_orientation_lift_projection_checks": fixed_lift_projection_checks,
            "fixed_orientation_image_count": len(fixed_orientation_images),
            "all_orientation_image_count": len(parameter_images),
            "compatible_primary_chains": len(accepted_primary),
            "orientations_per_satisfying_source_assignment": 2 ** DEPTH,
        },
        "cnf_audit": {
            "variables": circuit.nvars, "clauses": len(clauses),
            "primary_variables_including_seed": len(circuit.inputs),
            "gate_count": len(circuit.gates),
            "seed_assignment_checks": 8,
            "accepted_seed_assignments": seed_accepts,
            "all_clauses_three_distinct_variables": all(
                len(c) == 3 and len(set(map(abs, c))) == 3 for c in clauses
            ),
            "all_variables_used": set(abs(lit) for c in clauses for lit in c)
            == set(range(1, circuit.nvars + 1)),
            "raw_completion_checks": raw_checks,
            "proper_completion_checks_all_padding_values": proper_checks,
            "accepted_proper_completions": proper_accepts,
            "compatibility_equivalence_mismatches": 0,
            "dimacs_sha256": hashlib.sha256(dimacs.encode()).hexdigest(),
            "gate_completion_scope": "All chain-valid primary assignments and all four padding values; gate values are completed deterministically by the previously truth-checked producer. This is not brute force over all auxiliary assignments.",
        },
        "dead_prefix_control": {
            "oriented_first_prefixes": len(compatibility_by_prefix),
            "dead_oriented_first_prefixes": len(dead_prefixes),
            "extendible_oriented_first_prefixes": len(live_completion_counts),
            "compatible_completions_per_extendible_prefix": live_completion_counts,
            "dead_unoriented_first_labels": 4,
            "extendible_unoriented_first_labels": 4,
            "naive_all_zero_labels": naive_labels,
            "naive_all_zero_orientations": [0, 0],
            "naive_chain": naive_chain,
            "naive_chain_valid_before_compatibility": True,
            "naive_first_prefix_has_no_compatible_continuation": True,
            "naive_completed_cnf_satisfies": False,
            "source_first_compatible_labels": compatible_labels,
            "source_first_compatible_chain": compatible_chain,
            "source_first_completed_cnf_satisfies": True,
        },
        "limitations": [
            "Finite exhaustive parameter case only; the general bijection requires a separate mathematical proof.",
            "Reuse of the verified producer is explicit and its exact code hash is recorded.",
            "No H measurement, no program enumeration, no asymptotic lower bound, and no P-versus-NP conclusion.",
            "Dead prefixes refute all-prefix totality, not the polynomial source-first extension algorithm.",
            "Fixed orientation produces one chain per source assignment; all orientations produce four.",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"], "output": str(args.out),
        "parameter_strings": parameter_checks, "compatible_primary_chains": len(accepted_primary),
        "proper_completion_checks": proper_checks, "cnf_variables": circuit.nvars,
        "cnf_clauses": len(clauses), "dead_oriented_prefixes": len(dead_prefixes),
        "mismatches": 0, "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
