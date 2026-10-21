#!/usr/bin/env python3
"""Finite controls for PADDING-THRESHOLD-FIREWALL51.

Checks canonical copy padding, unique Tseitin extension, threshold-exponent
drift, and the corresponding apparent ARC exponent drift.  This does not
compute arbitrary KT or prove a complexity-class separation.
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


def random_circuit(m: int, g: int) -> list[tuple]:
    gates = []
    for j in range(g):
        available = m + j
        kind = RNG.choice(("NOT", "AND", "OR", "XOR"))
        x = RNG.randrange(available)
        if kind == "NOT":
            gates.append((kind, x))
        else:
            gates.append((kind, x, RNG.randrange(available)))
    return gates


def add_copy_chain(m: int, gates: list[tuple], depth: int) -> list[tuple]:
    out = list(gates)
    source = m + len(out) - 1
    for _ in range(depth):
        out.append(("COPY", source))
        source += 1
    return out


def strip_copy_chain(m: int, gates: list[tuple]) -> tuple[list[tuple], int]:
    out = list(gates)
    removed = 0
    while out and out[-1][0] == "COPY":
        expected_source = m + len(out) - 2
        if out[-1][1] != expected_source:
            break
        out.pop()
        removed += 1
    return out, removed


def lit_value(lit: int, assignment: tuple[int, ...]) -> bool:
    value = bool(assignment[abs(lit) - 1])
    return value if lit > 0 else not value


def cnf_value(clauses: list[tuple[int, ...]], assignment: tuple[int, ...]) -> bool:
    return all(any(lit_value(lit, assignment) for lit in clause)
               for clause in clauses)


def circuit_cnf(m: int, gates: list[tuple]) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for j, gate in enumerate(gates):
        z = m + j + 1
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
    clauses.append((m + len(gates),))
    return clauses


# 1. Canonical copy padding preserves the primary function, has a unique trace,
# and is syntactically removable by linear backward gate inspection.
circuit_instances = 0
for _ in range(140):
    m = RNG.randint(1, 4)
    g = RNG.randint(1, 4)
    base = random_circuit(m, g)
    base_truth = {
        primary: eval_circuit(primary, base)[-1]
        for primary in itertools.product((0, 1), repeat=m)
    }
    for depth in range(0, 7):
        padded = add_copy_chain(m, base, depth)
        stripped, removed = strip_copy_chain(m, padded)
        require(stripped == base and removed == depth,
                "canonical copy chain did not strip exactly")
        clauses = circuit_cnf(m, padded)
        model_count = 0
        for assignment in itertools.product((0, 1), repeat=m + len(padded)):
            primary = assignment[:m]
            trace = eval_circuit(primary, padded)
            expected = bool(trace[-1]) and assignment[m:] == trace[m:]
            got = cnf_value(clauses, assignment)
            require(got == expected, "padded Tseitin trace mismatch")
            assignment_checks += 1
            model_count += int(got)
        require(model_count == sum(base_truth.values()),
                "copy padding changed model count")
        for primary, output in base_truth.items():
            require(eval_circuit(primary, padded)[-1] == output,
                    "copy padding changed circuit function")
        circuit_instances += 1


# 2. Exact threshold-drift exponents.  If the padded source has size
# N'=n^a and a padding-equivariant target has KT <= n^beta, then the
# proposed k=241 threshold has exponent 6a/(5k) in n.
k = 241
betas = [
    Fraction(0), Fraction(1, 1000), Fraction(1, 241),
    Fraction(1, 100), Fraction(1, 10), Fraction(1, 2),
    Fraction(1), Fraction(2), Fraction(5),
]
threshold_cases = []
for beta in betas:
    boundary = Fraction(5 * k, 6) * beta
    a = math.floor(boundary) + 1
    padded_threshold_exp = Fraction(6 * a, 5 * k)
    require(padded_threshold_exp > beta,
            "chosen polynomial padding did not overtake KT exponent")
    if a > 1:
        require(Fraction(6 * (a - 1), 5 * k) <= beta,
                "padding exponent was not minimal")
    threshold_cases.append({
        "beta": str(beta),
        "minimal_integer_padding_power": a,
        "threshold_exponent": str(padded_threshold_exp),
    })


# 3. Apparent ARC exponent drift on a padded promise family.
arc_cases = 0
for core_time_exp in (
    Fraction(6, 5), Fraction(241, 200), Fraction(2),
    Fraction(3), Fraction(10),
):
    for target_exp in (
        Fraction(1), Fraction(1, 2), Fraction(1, 10),
        Fraction(1, 100), Fraction(1, 1000),
    ):
        a = math.floor(core_time_exp / target_exp) + 1
        require(core_time_exp / a < target_exp,
                "padding did not reduce apparent exponent")
        arc_cases += 1


# 4. A simple indexed-extension control: appending deterministic zeros is
# recoverable in both directions and contributes no source entropy.
indexed_extension_cases = 0
for base_length in (1, 2, 3, 7, 16, 31, 64, 127):
    for extension in (0, 1, 2, 5, 17, 64, 257):
        base = tuple(RNG.randrange(2) for _ in range(base_length))
        padded = base + (0,) * extension
        for i in range(len(padded)):
            direct = base[i] if i < base_length else 0
            require(padded[i] == direct, "indexed padding decoder mismatch")
        require(padded[:base_length] == base, "base target not recoverable")
        indexed_extension_cases += 1


summary = {
    "run_id": "PADDING-THRESHOLD-FIREWALL51",
    "status": "PASS",
    "assertions": checks,
    "assignment_equivalence_checks": assignment_checks,
    "circuit_padding_instances": circuit_instances,
    "threshold_cases": threshold_cases,
    "arc_exponent_cases": arc_cases,
    "indexed_extension_cases": indexed_extension_cases,
    "scope": (
        "Finite controls for semantic copy padding, threshold drift and "
        "promise-family exponent drift; not arbitrary KT or a separation."
    ),
}
print(json.dumps(summary, indent=2, sort_keys=True))
