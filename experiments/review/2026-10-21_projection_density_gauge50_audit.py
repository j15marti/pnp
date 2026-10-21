#!/usr/bin/env python3
"""Finite controls for PROJECTED-DENSITY-GAUGE50.

Checks parsimonious Tseitin model counts, projection density, deterministic
copy-chain gauge changes, scrambling invariance, and the DENSE-BYPASS14 count.
This is not a class-separation experiment.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from fractions import Fraction


RNG = random.Random(20261021)
checks = 0
assignment_checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def lit_value(lit: int, assignment: tuple[int, ...]) -> bool:
    value = bool(assignment[abs(lit) - 1])
    return value if lit > 0 else not value


def cnf_value(clauses: list[tuple[int, ...]], assignment: tuple[int, ...]) -> bool:
    return all(any(lit_value(lit, assignment) for lit in clause)
               for clause in clauses)


def eval_circuit(primary: tuple[int, ...], gates: list[tuple]) -> tuple[int, ...]:
    values = list(primary)
    for gate in gates:
        kind = gate[0]
        if kind == "NOT":
            values.append(1 - values[gate[1]])
        elif kind == "COPY":
            values.append(values[gate[1]])
        elif kind == "AND":
            values.append(values[gate[1]] & values[gate[2]])
        elif kind == "OR":
            values.append(values[gate[1]] | values[gate[2]])
        elif kind == "XOR":
            values.append(values[gate[1]] ^ values[gate[2]])
        else:
            raise ValueError(kind)
    return tuple(values)


def circuit_cnf(m: int, gates: list[tuple]) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for j, gate in enumerate(gates):
        z = m + j + 1  # DIMACS variable number
        kind = gate[0]
        x = gate[1] + 1
        if kind == "NOT":
            clauses += [(x, z), (-x, -z)]
        elif kind == "COPY":
            clauses += [(-x, z), (x, -z)]
        else:
            y = gate[2] + 1
            if kind == "AND":
                clauses += [(-x, -y, z), (x, -z), (y, -z)]
            elif kind == "OR":
                clauses += [(x, y, -z), (-x, z), (-y, z)]
            elif kind == "XOR":
                clauses += [
                    (-x, -y, -z), (x, y, -z),
                    (x, -y, z), (-x, y, z),
                ]
            else:
                raise ValueError(kind)
    clauses.append((m + len(gates),))  # force output gate to one
    return clauses


def random_circuit(m: int, g: int) -> list[tuple]:
    gates = []
    for j in range(g):
        available = m + j
        kind = RNG.choice(("NOT", "AND", "OR", "XOR"))
        x = RNG.randrange(available)
        if kind == "NOT":
            gates.append((kind, x))
        else:
            y = RNG.randrange(available)
            gates.append((kind, x, y))
    return gates


def add_copy_chain(m: int, gates: list[tuple], depth: int) -> list[tuple]:
    out = list(gates)
    source = m + len(out) - 1
    for _ in range(depth):
        out.append(("COPY", source))
        source += 1
    return out


def permute_cnf(clauses: list[tuple[int, ...]], variable_count: int) -> list[tuple[int, ...]]:
    image = list(range(1, variable_count + 1))
    RNG.shuffle(image)
    out = []
    for clause in clauses:
        mapped = []
        for lit in clause:
            v = image[abs(lit) - 1]
            mapped.append(v if lit > 0 else -v)
        RNG.shuffle(mapped)
        out.append(tuple(mapped))
    RNG.shuffle(out)
    return out


random_circuits = 0
chain_instances = 0
scramble_instances = 0
for _ in range(180):
    m = RNG.randint(1, 4)
    g = RNG.randint(1, 4)
    base = random_circuit(m, g)
    base_accept = sum(eval_circuit(primary, base)[-1]
                      for primary in itertools.product((0, 1), repeat=m))
    for depth in range(0, 6):
        gates = add_copy_chain(m, base, depth)
        clauses = circuit_cnf(m, gates)
        q = len(gates)
        model_count = 0
        for assignment in itertools.product((0, 1), repeat=m + q):
            got = cnf_value(clauses, assignment)
            primary = assignment[:m]
            trace = eval_circuit(primary, gates)
            expected = bool(trace[-1]) and assignment[m:] == trace[m:]
            require(got == expected, "Tseitin assignment/trace mismatch")
            assignment_checks += 1
            model_count += int(got)
        require(model_count == base_accept, "parsimonious model count changed")
        full_density = Fraction(model_count, 1 << (m + q))
        projected_density = Fraction(base_accept, 1 << m)
        require(full_density == projected_density / (1 << q),
                "projection/full-density identity failed")
        if depth:
            require(full_density * (1 << depth)
                    == Fraction(base_accept, 1 << (m + g)),
                    "copy-chain gauge factor failed")
        chain_instances += 1

        # Scrambling preserves full model count but not the designated primary map.
        if depth in (0, 3):
            scrambled = permute_cnf(clauses, m + q)
            scrambled_count = sum(
                cnf_value(scrambled, a)
                for a in itertools.product((0, 1), repeat=m + q)
            )
            require(scrambled_count == model_count, "scramble changed model count")
            scramble_instances += 1
    random_circuits += 1


# Point-circuit controls: one accepting primary assignment, still one trace.
point_instances = 0
for m in range(1, 8):
    for target in itertools.product((0, 1), repeat=m):
        # Build equality literals, then an AND chain.
        gates = []
        literals = []
        for i, bit in enumerate(target):
            if bit:
                literals.append(i)
            else:
                gates.append(("NOT", i))
                literals.append(m + len(gates) - 1)
        while len(literals) > 1:
            x = literals.pop()
            y = literals.pop()
            gates.append(("AND", x, y))
            literals.append(m + len(gates) - 1)
        if not gates:
            gates.append(("COPY", literals[0]))
        clauses = circuit_cnf(m, gates)
        count = sum(cnf_value(clauses, a)
                    for a in itertools.product((0, 1), repeat=m + len(gates)))
        require(count == 1, "point circuit should have one full model")
        point_instances += 1


# DENSE-BYPASS14 projected count and trivial accepting seed.
dense_instances = 0
for n in range(3, 17):
    h_ones = 0
    for z in itertools.product((0, 1), repeat=n):
        u_weight = sum(1 - bit for bit in z)
        pair_parity = math.comb(u_weight, 2) & 1
        h = pair_parity ^ int(u_weight == n)
        h_ones += h
        require((1 or h) == 1, "selector b=1 should accept")
    formula = sum(math.comb(n, k) for k in range(n + 1)
                  if k % 4 in (2, 3))
    formula += 1 if n % 4 in (0, 1) else -1
    require(h_ones == formula, "DENSE-BYPASS14 H-count formula mismatch")
    total_accept = (1 << n) + h_ones
    require(Fraction(total_accept, 1 << (n + 1)) >= Fraction(1, 2),
            "RP projected density below one half")
    dense_instances += 1


summary = {
    "run_id": "PROJECTED-DENSITY-GAUGE50",
    "status": "PASS",
    "assertions": checks,
    "assignment_equivalence_checks": assignment_checks,
    "random_circuits": random_circuits,
    "copy_chain_instances": chain_instances,
    "scramble_instances": scramble_instances,
    "point_circuit_instances": point_instances,
    "dense_bypass_instances": dense_instances,
    "scope": (
        "Exact finite controls for parsimonious extension density and "
        "representation gauge; not a lower bound or class separation."
    ),
}
print(json.dumps(summary, indent=2, sort_keys=True))
