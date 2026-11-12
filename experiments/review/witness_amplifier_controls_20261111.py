#!/usr/bin/env python3
"""Exact controls for the witness-work amplification project.

This script audits a nonlinear adaptive collision-chain compiler and the
small-seed theorem on all intersection-closed families on three coordinates.
It does not measure H(F), enumerate all programs, or prove a runtime lower bound.
Each invocation is intended to finish in less than 30 seconds.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


def bits(value: int, width: int) -> list[int]:
    return [(value >> i) & 1 for i in range(width)]


def number(v: list[int]) -> int:
    return sum(x << i for i, x in enumerate(v))


def round_function(right: list[int], key: list[int], rnd: int) -> list[int]:
    h = len(right)
    return [
        right[i] ^ (right[(i + 1) % h] & right[(i + 2) % h])
        ^ key[(i + rnd) % h] ^ ((rnd + i) & 1)
        for i in range(h)
    ]


def permute(v: list[int], key: list[int], rounds: int, inverse: bool = False) -> list[int]:
    h = len(v) // 2
    left, right = v[:h], v[h:]
    order = range(rounds - 1, -1, -1) if inverse else range(rounds)
    for rnd in order:
        if inverse:
            f = round_function(left, key, rnd)
            left, right = [right[i] ^ f[i] for i in range(h)], left
        else:
            f = round_function(right, key, rnd)
            left, right = right, [left[i] ^ f[i] for i in range(h)]
    return left + right


class CircuitCNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.inputs: list[int] = []
        self.gates: list[tuple[int, str, int, int]] = []
        self.raw: list[tuple[int, ...]] = []
        self.constants: dict[int, int] = {}
        self.padding: tuple[int, int] | None = None

    def var(self, primary: bool = False) -> int:
        self.nvars += 1
        if primary:
            self.inputs.append(self.nvars)
        return self.nvars

    def constant(self, value: int) -> int:
        if value not in self.constants:
            v = self.var()
            self.constants[value] = v
            self.raw.append((v if value else -v,))
        return self.constants[value]

    def gate(self, op: str, a: int, b: int) -> int:
        z = self.var()
        self.gates.append((z, op, a, b))
        if op == "xor":
            self.raw.extend(((a, b, -z), (-a, -b, -z), (a, -b, z), (-a, b, z)))
        elif op == "and":
            self.raw.extend(((-a, -b, z), (a, -z), (b, -z)))
        elif op == "or":
            self.raw.extend(((a, b, -z), (-a, z), (-b, z)))
        else:
            raise ValueError(op)
        return z

    def key(self, prev_u: list[int], prev_v: list[int], h: int) -> list[int]:
        return [
            self.gate("xor", prev_u[i % len(prev_u)], prev_v[(i + 1) % len(prev_v)])
            for i in range(h)
        ]

    def feistel(self, wires: list[int], key: list[int], rounds: int) -> list[int]:
        h = len(wires) // 2
        left, right = wires[:h], wires[h:]
        for rnd in range(rounds):
            f = []
            for i in range(h):
                q = self.gate("and", right[(i + 1) % h], right[(i + 2) % h])
                q = self.gate("xor", right[i], q)
                q = self.gate("xor", q, key[(i + rnd) % h])
                q = self.gate("xor", q, self.constant((rnd + i) & 1))
                f.append(q)
            left, right = right, [self.gate("xor", left[i], f[i]) for i in range(h)]
        return left + right

    def proper(self) -> list[tuple[int, int, int]]:
        if self.padding is None:
            self.padding = self.var(), self.var()
        p, q = self.padding
        clauses: list[tuple[int, int, int]] = []
        for raw in self.raw:
            s = set(raw)
            if any(-x in s for x in s):
                continue
            c = tuple(sorted(s, key=lambda x: (abs(x), x)))
            if len(c) == 3:
                clauses.append(c)
            elif len(c) == 2:
                clauses.extend((c + (p,), c + (-p,)))
            elif len(c) == 1:
                clauses.extend((c + (p, q), c + (p, -q), c + (-p, q), c + (-p, -q)))
            else:
                raise AssertionError(("invalid gate clause", raw))
        assert all(len(c) == 3 and len({abs(v) for v in c}) == 3 for c in clauses)
        assert {abs(v) for c in clauses for v in c} == set(range(1, self.nvars + 1))
        return clauses

    def complete(self, primary: dict[int, int]) -> dict[int, int]:
        values = dict(primary)
        for bit, v in self.constants.items():
            values[v] = bit
        for z, op, a, b in self.gates:
            x, y = values[a], values[b]
            values[z] = (x ^ y) if op == "xor" else ((x & y) if op == "and" else (x | y))
        if self.padding:
            values[self.padding[0]] = values[self.padding[1]] = 0
        assert len(values) == self.nvars
        return values


def satisfies(clauses: list[tuple[int, ...]], assignment: dict[int, int]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in c) for c in clauses)


def make_chain(h: int, depth: int, rounds: int = 4):
    circuit = CircuitCNF()
    seed = [circuit.var(True) for _ in range(3)]
    seed_values = [1, 0, 1]
    for bad in itertools.product((0, 1), repeat=3):
        if list(bad) != seed_values:
            circuit.raw.append(tuple(-v if bit else v for v, bit in zip(seed, bad)))
    previous_u, previous_v = seed, list(reversed(seed))
    stages = []
    for _ in range(depth):
        u = [circuit.var(True) for _ in range(2 * h)]
        v = [circuit.var(True) for _ in range(2 * h)]
        key = circuit.key(previous_u, previous_v, h)
        pu, pv = circuit.feistel(u, key, rounds), circuit.feistel(v, key, rounds)
        for a, b in zip(pu[:-1], pv[:-1]):
            circuit.raw.append((-a, b))
            circuit.raw.append((a, -b))
        difference = [circuit.gate("xor", a, b) for a, b in zip(u, v)]
        any_difference = difference[0]
        for x in difference[1:]:
            any_difference = circuit.gate("or", any_difference, x)
        circuit.raw.append((any_difference,))
        stages.append((u, v))
        previous_u, previous_v = u, v
    clauses = circuit.proper()
    return circuit, seed, stages, clauses


def construct_witness(h: int, depth: int, rounds: int):
    previous_u, previous_v = [1, 0, 1], [1, 0, 1]
    chosen = []
    for _ in range(depth):
        key = [
            previous_u[i % len(previous_u)] ^ previous_v[(i + 1) % len(previous_v)]
            for i in range(h)
        ]
        u = permute([0] * (2 * h), key, rounds, inverse=True)
        v = permute([0] * (2 * h - 1) + [1], key, rounds, inverse=True)
        assert u != v
        assert permute(u, key, rounds)[:-1] == permute(v, key, rounds)[:-1]
        chosen.append((u, v))
        previous_u, previous_v = u, v
    return chosen


def semantic_chain(primary, seed, stages, h, rounds):
    if [primary[x] for x in seed] != [1, 0, 1]:
        return False
    previous_u = [primary[x] for x in seed]
    previous_v = list(reversed(previous_u))
    for uw, vw in stages:
        key = [
            previous_u[i % len(previous_u)] ^ previous_v[(i + 1) % len(previous_v)]
            for i in range(h)
        ]
        u, v = [primary[x] for x in uw], [primary[x] for x in vw]
        if u == v or permute(u, key, rounds)[:-1] != permute(v, key, rounds)[:-1]:
            return False
        previous_u, previous_v = u, v
    return True


def audit_feistel(outdir: Path):
    rounds = 4
    permutation_checks = 0
    for h in (2, 3, 4, 5):
        width = 2 * h
        for key in (bits(0, h), bits((1 << h) - 1, h), bits(2, h)):
            images = set()
            for x in range(1 << width):
                v = bits(x, width)
                image = permute(v, key, rounds)
                assert permute(image, key, rounds, inverse=True) == v
                images.add(number(image))
                permutation_checks += 1
            assert len(images) == 1 << width

    rows = []
    for h, depth in ((2, 1), (2, 2), (3, 2), (4, 3), (5, 4)):
        circuit, seed, stages, clauses = make_chain(h, depth, rounds)
        chosen = construct_witness(h, depth, rounds)
        primary = dict(zip(seed, (1, 0, 1)))
        for (uw, vw), (u, v) in zip(stages, chosen):
            primary.update(zip(uw, u))
            primary.update(zip(vw, v))
        assignment = circuit.complete(primary)
        assert satisfies(clauses, assignment)
        row = {
            "half_width": h, "output_width": 2 * h - 1, "depth": depth,
            "rounds": rounds, "variables": circuit.nvars, "clauses": len(clauses),
            "gate_count": len(circuit.gates), "inverse_calls": 2 * depth,
            "round_function_calls_to_find_collisions": 2 * depth * rounds,
            "generic_enumeration_evaluation_cap": depth * ((1 << (2 * h - 1)) + 1),
            "witness_valid": True,
        }
        rows.append(row)
        if (h, depth) == (2, 2):
            dimacs = f"p cnf {circuit.nvars} {len(clauses)}\n" + "".join(
                " ".join(map(str, c)) + " 0\n" for c in clauses
            )
            (outdir / "nested_feistel_h2_k2.cnf").write_text(dimacs)
            witness = [v if assignment[v] else -v for v in range(1, circuit.nvars + 1)]
            (outdir / "nested_feistel_h2_k2_witness.json").write_text(json.dumps(witness))
            row["cnf_sha256"] = hashlib.sha256(dimacs.encode()).hexdigest()

    # Exhaust all primary assignments on the smallest nonlinear instance.
    circuit, seed, stages, clauses = make_chain(2, 1, rounds)
    semantics_checks = sat_count = 0
    for mask in range(1 << len(circuit.inputs)):
        primary = dict(zip(circuit.inputs, bits(mask, len(circuit.inputs))))
        compiled = satisfies(clauses, circuit.complete(primary))
        expected = semantic_chain(primary, seed, stages, 2, rounds)
        assert compiled == expected
        semantics_checks += 1
        sat_count += compiled

    gate_truth_checks = 0
    for op in ("xor", "and", "or"):
        for a, b, z in itertools.product((0, 1), repeat=3):
            cc = CircuitCNF()
            x, y = cc.var(True), cc.var(True)
            out = cc.gate(op, x, y)
            wanted = (a ^ b) if op == "xor" else ((a & b) if op == "and" else (a | b))
            assert satisfies(cc.raw, {x: a, y: b, out: z}) == (z == wanted)
            gate_truth_checks += 1

    return {
        "permutation_inverse_checks": permutation_checks,
        "gate_truth_checks": gate_truth_checks,
        "exhaustive_primary_assignments": semantics_checks,
        "satisfying_primary_assignments": sat_count,
        "chain_cases": rows,
        "interpretation": "Fixed inverse-based witness algorithm; no H lower-bound measurement.",
    }


def audit_closure_seed():
    n = 3
    families = []
    for family_code in range(1, 1 << (1 << n)):
        family = [x for x in range(1 << n) if (family_code >> x) & 1]
        if all((x & y) in family for x in family for y in family):
            families.append(family)
    total = 0
    by_degree = {}
    for d in range(n + 1):
        monomials = [s for s in range(1 << n) if s.bit_count() <= d]
        cases = 0
        for family in families:
            closures = set()
            for seed in monomials:
                supersets = [x for x in family if (x & seed) == seed]
                if supersets:
                    closure = (1 << n) - 1
                    for x in supersets:
                        closure &= x
                    assert closure in family
                    closures.add(closure)
            for coefficient_code in range(1 << len(monomials)):
                def value(x):
                    answer = 0
                    for i, s in enumerate(monomials):
                        if (coefficient_code >> i) & 1 and (x & s) == s:
                            answer ^= 1
                    return answer
                assert any(value(x) for x in family) == any(value(x) for x in closures)
                cases += 1
        by_degree[str(d)] = cases
        total += cases
    return {
        "coordinates": n, "nonempty_intersection_closed_families": len(families),
        "cases_by_degree": by_degree, "family_polynomial_pairs": total,
        "mismatches": 0,
        "interpretation": "Finite audit of the small-seed theorem; symbolic proof is separate.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result = {
        "status": "COMPUTATIONAL",
        "seed": None,
        "method": "Deterministic exhaustive finite controls, exact Boolean arithmetic",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "feistel": audit_feistel(args.outdir),
        "closure_seed": audit_closure_seed(),
    }
    result["elapsed_seconds"] = time.monotonic() - started
    assert result["elapsed_seconds"] < 30, "Split the computation into smaller stages."
    target = args.outdir / "witness_amplifier_controls.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

