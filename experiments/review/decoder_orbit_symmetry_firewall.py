#!/usr/bin/env python3
"""Exhaustive audit for the source-orientation/decoder firewall.

The main control is the graph of the quadratic involution

    S(a,b,c) = (a,b,c xor (a and b)).

Its canonical forbidden-assignment CNF is invariant under swapping the input
and output blocks.  Therefore no variable-renaming-covariant decoder can
recover the originally designated input block from the untagged CNF.  The
relation nevertheless has a uniform linear-size witness map in both
directions.  This is a representation/decoder firewall, not a hardness claim.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from pathlib import Path


SEED = 23362026


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def shear(x: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = x
    return a, b, c ^ (a & b)


def forbid_assignment(bits: tuple[int, ...]) -> Clause:
    return tuple((i + 1) if bit == 0 else -(i + 1)
                 for i, bit in enumerate(bits))


def canonical_cnf(clauses: list[Clause] | tuple[Clause, ...]) -> CNF:
    return tuple(sorted(tuple(sorted(c, key=lambda z: (abs(z), z < 0)))
                        for c in clauses))


def shear_graph_cnf() -> CNF:
    clauses: list[Clause] = []
    for bits in itertools.product((0, 1), repeat=6):
        if tuple(bits[3:]) != shear(tuple(bits[:3])):
            clauses.append(forbid_assignment(tuple(bits)))
    return canonical_cnf(clauses)


def eval_cnf(cnf: CNF, assignment: tuple[int, ...]) -> bool:
    return all(any((assignment[abs(lit) - 1] == 1) == (lit > 0)
                   for lit in clause) for clause in cnf)


def rename_cnf(cnf: CNF, perm: tuple[int, ...], flips: tuple[int, ...]) -> CNF:
    out: list[Clause] = []
    for clause in cnf:
        moved = []
        for lit in clause:
            old = abs(lit) - 1
            sign = lit > 0
            if flips[old]:
                sign = not sign
            new = perm[old]
            moved.append((new + 1) if sign else -(new + 1))
        out.append(tuple(moved))
    return canonical_cnf(out)


def rename_assignment(assignment: tuple[int, ...], perm: tuple[int, ...],
                      flips: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(assignment)
    for old, bit in enumerate(assignment):
        out[perm[old]] = bit ^ flips[old]
    return tuple(out)


def inverse_assignment(assignment: tuple[int, ...], perm: tuple[int, ...],
                       flips: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(assignment)
    for old in range(len(assignment)):
        out[old] = assignment[perm[old]] ^ flips[old]
    return tuple(out)


def transported_set(block: frozenset[int], perm: tuple[int, ...]) -> frozenset[int]:
    return frozenset(perm[i] for i in block)


def equality_path_cnf(n: int) -> CNF:
    clauses = []
    for i in range(n - 1):
        a, b = i + 1, i + 2
        clauses.extend([(-a, b), (a, -b)])
    return canonical_cnf(clauses)


def automorphisms(cnf: CNF, n: int) -> list[tuple[int, ...]]:
    zero_flips = (0,) * n
    return [p for p in itertools.permutations(range(n))
            if rename_cnf(cnf, p, zero_flips) == cnf]


def source_control(kind: str, x: tuple[int, int, int]) -> bool:
    a, b, c = x
    if kind == "yes":
        return True
    if kind == "no":
        return False
    if kind == "horn":
        return (not a) or (b and c)
    if kind == "krom":
        return (a or b) and ((not b) or c)
    if kind == "affine":
        return (a ^ b ^ c) == 0
    if kind == "path":
        return not (a and b) and not (b and c)
    if kind == "product":
        return (a == b) and bool(c)
    if kind == "planted3":
        return bool(a or b or c)
    raise ValueError(kind)


def validate_metadata(perm: tuple[int, ...], flips: tuple[int, ...],
                      source_block: tuple[int, ...]) -> None:
    n = len(perm)
    if sorted(perm) != list(range(n)):
        raise ValueError("permutation is not bijective")
    if len(flips) != n or any(b not in (0, 1) for b in flips):
        raise ValueError("bad flip vector")
    if len(set(source_block)) != len(source_block) or any(i < 0 or i >= n for i in source_block):
        raise ValueError("bad source block")


def run() -> dict:
    start = time.perf_counter()
    rng = random.Random(SEED)
    assertions = 0
    cnf = shear_graph_cnf()
    assert len(cnf) == 56 and len(set(cnf)) == 56
    assertions += 2

    # Exact graph-of-function and involution checks.
    satisfying = []
    for bits in itertools.product((0, 1), repeat=6):
        expected = tuple(bits[3:]) == shear(tuple(bits[:3]))
        assert eval_cnf(cnf, tuple(bits)) == expected
        assertions += 1
        if expected:
            satisfying.append(tuple(bits))
    assert len(satisfying) == 8
    assertions += 1
    for x in itertools.product((0, 1), repeat=3):
        y = shear(x)
        assert shear(y) == x
        forward = [a for a in satisfying if a[:3] == x]
        backward = [a for a in satisfying if a[3:] == x]
        assert forward == [x + y]
        assert backward == [y + x]
        assertions += 3

    # The block swap is an automorphism.  Exhaustively compute all 6! variable
    # automorphisms of the canonical CNF to expose the source-block orbit.
    swap = (3, 4, 5, 0, 1, 2)
    assert rename_cnf(cnf, swap, (0,) * 6) == cnf
    assertions += 1
    autos = automorphisms(cnf, 6)
    source = frozenset({0, 1, 2})
    target = frozenset({3, 4, 5})
    source_orbit = {transported_set(source, p) for p in autos}
    assert source in source_orbit and target in source_orbit
    assert transported_set(source, swap) == target
    assertions += 3
    invariant_source = all(transported_set(source, p) == source for p in autos)
    assert not invariant_source
    assertions += 1

    # Krom affine path controls have the same endpoint-orientation obstruction.
    path_rows = []
    for n in range(2, 9):
        path = equality_path_cnf(n)
        autos_n = automorphisms(path, n)
        endpoint_orbit = {p[0] for p in autos_n}
        assert endpoint_orbit == {0, n - 1}
        assert len(autos_n) == 2
        for bit in (0, 1):
            a = (bit,) * n
            assert eval_cnf(path, a)
            assertions += 1
        assertions += 2
        path_rows.append({"n": n, "automorphisms": len(autos_n),
                          "source_endpoint_orbit": sorted(endpoint_orbit)})

    # Signed renaming and clause-shuffle controls.  The source-aware wrapper
    # retains the transformation metadata; a fixed positional parser does not.
    trials = 512
    metadata_recoveries = 0
    naive_block_hits = 0
    witness_checks = 0
    control_counts = {k: 0 for k in
                      ["yes", "no", "horn", "krom", "affine", "path", "product", "planted3"]}
    for t in range(trials):
        perm_list = list(range(6))
        rng.shuffle(perm_list)
        perm = tuple(perm_list)
        flips = tuple(rng.randrange(2) for _ in range(6))
        validate_metadata(perm, flips, (0, 1, 2))
        moved_cnf = rename_cnf(cnf, perm, flips)
        # A separate shuffle models arbitrary clause order; canonical semantics
        # are unchanged and the metadata-aware inverse does not inspect order.
        shuffled = list(moved_cnf)
        rng.shuffle(shuffled)
        moved_cnf = canonical_cnf(shuffled)
        x = tuple(rng.randrange(2) for _ in range(3))
        full = x + shear(x)
        moved = rename_assignment(full, perm, flips)
        assert eval_cnf(moved_cnf, moved)
        assert inverse_assignment(moved, perm, flips) == full
        assertions += 2
        metadata_recoveries += 1
        witness_checks += 1
        if transported_set(source, perm) == source:
            naive_block_hits += 1
        kind = list(control_counts)[t % len(control_counts)]
        control_counts[kind] += int(source_control(kind, x))

    assert metadata_recoveries == trials
    assert naive_block_hits < trials
    assertions += 2

    malformed = [
        ((0, 1, 2, 3, 4, 4), (0,) * 6, (0, 1, 2)),
        ((0, 1, 2, 3, 4), (0,) * 6, (0, 1, 2)),
        (tuple(range(6)), (0, 0, 0, 0, 0), (0, 1, 2)),
        (tuple(range(6)), (0, 0, 0, 0, 0, 2), (0, 1, 2)),
        (tuple(range(6)), (0,) * 6, (0, 0, 2)),
        (tuple(range(6)), (0,) * 6, (0, 1, 6)),
    ]
    rejected = 0
    for record in malformed:
        try:
            validate_metadata(*record)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)
    assertions += rejected

    elapsed = time.perf_counter() - start
    return {
        "run_id": "ORBITDECODERFW1",
        "status": "PASS",
        "seed": SEED,
        "assertions": assertions,
        "shear_cnf_variables": 6,
        "shear_cnf_clauses": len(cnf),
        "shear_graph_models": len(satisfying),
        "shear_automorphism_group_size": len(autos),
        "source_block_orbit_size": len(source_orbit),
        "source_block_invariant": invariant_source,
        "path_controls": path_rows,
        "signed_renaming_trials": trials,
        "metadata_recoveries": metadata_recoveries,
        "naive_positional_block_hits": naive_block_hits,
        "witness_checks": witness_checks,
        "source_control_satisfying_counts": control_counts,
        "malformed_metadata_rejected": rejected,
        "elapsed_seconds": elapsed,
        "method": "exhaustive truth tables and automorphism enumeration plus seeded signed-renaming controls",
        "limitations": [
            "The automorphism theorem refutes universal canonical orientation, not the explicit tagged HIERLIFT theorem.",
            "Failure of a target-only orientation decoder is not a witness-search lower bound.",
            "Metadata-aware source-to-target wrappers remain polynomial and fully charged.",
            "The experiment does not solve arbitrary nonlinear residuals or prove P != NP."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run()
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
