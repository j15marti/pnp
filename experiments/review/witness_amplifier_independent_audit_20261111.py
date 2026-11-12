#!/usr/bin/env python3
"""Independent finite audit of the November 11 witness-amplifier controls.

No producer module is imported. This checks the exported DIMACS/witness,
proper gate templates including aliased inputs, and an independently written
four-bit Feistel recurrence with its ANF degrees. It does not measure H(F)
or establish a lower bound. One invocation must finish within 30 seconds.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


def satisfies(clauses, assignment):
    return all(
        any(assignment[abs(lit)] == (lit > 0) for lit in clause)
        for clause in clauses
    )


def check_export(repo: Path):
    rawdir = repo / "results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS"
    cnf = rawdir / "nested_feistel_h2_k2.cnf"
    lines = cnf.read_text().splitlines()
    header = lines[0].split()
    assert header[:2] == ["p", "cnf"]
    nvars, nclauses = map(int, header[2:])
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        assert values[-1] == 0
        clause = values[:-1]
        assert len(clause) == 3
        assert len({abs(v) for v in clause}) == 3
        assert all(1 <= abs(v) <= nvars for v in clause)
        clauses.append(clause)
    assert len(clauses) == nclauses
    assert {abs(v) for c in clauses for v in c} == set(range(1, nvars + 1))

    witness = json.loads(
        (rawdir / "nested_feistel_h2_k2_witness.json").read_text()
    )
    assert len(witness) == nvars
    assert {abs(v) for v in witness} == set(range(1, nvars + 1))
    assignment = {abs(v): v > 0 for v in witness}
    assert satisfies(clauses, assignment)

    # The declared compiler allocates its two shared padding variables last.
    padding_variants = 0
    for p, q in itertools.product((False, True), repeat=2):
        variant = assignment | {nvars - 1: p, nvars: q}
        assert satisfies(clauses, variant)
        padding_variants += 1

    producer = json.loads((rawdir / "witness_amplifier_controls.json").read_text())
    cnf_sha = hashlib.sha256(cnf.read_bytes()).hexdigest()
    assert cnf_sha == producer["feistel"]["chain_cases"][1]["cnf_sha256"]
    producer_path = repo / "experiments/review/witness_amplifier_controls_20261111.py"
    producer_sha = hashlib.sha256(producer_path.read_bytes()).hexdigest()
    assert producer_sha == producer["code_sha256"]
    return {
        "variables": nvars,
        "clauses": nclauses,
        "all_clauses_proper": True,
        "all_variables_used": True,
        "witness_valid": True,
        "padding_variants_valid": padding_variants,
        "cnf_sha256": cnf_sha,
        "producer_code_sha256": producer_sha,
        "recorded_hashes_match": True,
    }


def proper_padding(clauses):
    result = []
    for clause in clauses:
        deduplicated = set(clause)
        if any(-lit in deduplicated for lit in deduplicated):
            continue
        c = tuple(sorted(deduplicated))
        if len(c) == 3:
            result.append(c)
        elif len(c) == 2:
            result.extend((c + (4,), c + (-4,)))
        elif len(c) == 1:
            result.extend(c + (p, q) for p in (4, -4) for q in (5, -5))
        else:
            raise AssertionError(c)
    return result


def check_gate_templates():
    templates = {
        "xor": [(1, 2, -3), (-1, -2, -3), (1, -2, 3), (-1, 2, 3)],
        "and": [(-1, -2, 3), (1, -3), (2, -3)],
        "or": [(1, 2, -3), (-1, 3), (-2, 3)],
    }
    truth_checks = alias_checks = 0
    for op, clauses in templates.items():
        padded = proper_padding(clauses)
        assert all(len(c) == 3 and len({abs(v) for v in c}) == 3 for c in padded)
        for a, b, z, p, q in itertools.product((0, 1), repeat=5):
            wanted = (a ^ b) if op == "xor" else ((a & b) if op == "and" else (a | b))
            values = {1: a, 2: b, 3: z, 4: p, 5: q}
            assert satisfies(padded, values) == (z == wanted)
            truth_checks += 1

        # The h=3 initial key contains an XOR whose two inputs alias.
        collapsed = [
            tuple((1 if v > 0 else -1) if abs(v) == 2 else v for v in c)
            for c in clauses
        ]
        padded_alias = proper_padding(collapsed)
        assert all(len(c) == 3 and len({abs(v) for v in c}) == 3 for c in padded_alias)
        for a, z, p, q in itertools.product((0, 1), repeat=4):
            wanted = 0 if op == "xor" else a
            values = {1: a, 3: z, 4: p, 5: q}
            assert satisfies(padded_alias, values) == (z == wanted)
            alias_checks += 1
    return {
        "proper_gate_truth_checks": truth_checks,
        "aliased_input_gate_checks": alias_checks,
        "mismatches": 0,
    }


def independent_round_2(right, key, rnd):
    a, b = right
    return (
        a ^ (a & b) ^ key[rnd % 2] ^ (rnd % 2),
        b ^ (a & b) ^ key[(rnd + 1) % 2] ^ ((rnd + 1) % 2),
    )


def independent_permutation_4(value, key):
    left = (value & 1, (value >> 1) & 1)
    right = ((value >> 2) & 1, (value >> 3) & 1)
    for rnd in range(4):
        f = independent_round_2(right, key, rnd)
        left, right = right, tuple(left[i] ^ f[i] for i in range(2))
    return left + right


def check_independent_permutation():
    rows = []
    input_checks = 0
    for key in ((0, 0), (0, 1), (1, 0), (1, 1)):
        table = [independent_permutation_4(x, key) for x in range(16)]
        assert len(set(table)) == 16
        degrees = []
        for coordinate in range(4):
            coefficients = [value[coordinate] for value in table]
            for bit in range(4):
                for mask in range(16):
                    if mask & (1 << bit):
                        coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
            degree = max(
                (mask.bit_count() for mask, c in enumerate(coefficients) if c),
                default=0,
            )
            degrees.append(degree)
        collision_count = sum(
            1 for x in range(16) for y in range(16)
            if x != y and table[x][:-1] == table[y][:-1]
        )
        assert collision_count == 16
        assert max(degrees[:-1]) > 1
        rows.append({
            "key": list(key),
            "coordinate_ANF_degrees": degrees,
            "ordered_nontrivial_truncated_collisions": collision_count,
        })
        input_checks += 16
    return {
        "input_checks": input_checks,
        "keys_exhausted": 4,
        "all_maps_bijective": True,
        "all_truncated_maps_nonlinear": True,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or (
        args.repo / "results/raw/review/2026-11-11_WITNESS_AMPLIFIER_CONTROLS/independent_audit.json"
    )
    if output.exists():
        raise FileExistsError("Append-only raw output already exists: " + str(output))
    started = time.monotonic()
    result = {
        "status": "COMPUTATIONAL",
        "method": "Independent exact checks; no producer import",
        "random_seed": None,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "export": check_export(args.repo),
        "gate_templates": check_gate_templates(),
        "four_bit_permutation": check_independent_permutation(),
        "scope": (
            "Checks one exported 201-variable CNF and independent local truth tables. "
            "Does not enumerate all assignments to all auxiliary variables, measure H, "
            "or audit the separate closure-seed theorem."
        ),
    }
    result["elapsed_seconds"] = time.monotonic() - started
    assert result["elapsed_seconds"] < 30
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

