#!/usr/bin/env python3
"""Reproduce ORACLE-CLOSURE-FIREWALL185 finite controls.

The script has no third-party dependencies and is deterministic.  It checks:
  * the quantifier-vacuity control for target-dependent Boolean oracles;
  * existential elimination of z from the selector family for t=1..4;
  * a linear fan-in-two circuit and its full Tseitin encoding;
  * physical serialized sizes for selector, projection, circuit, and Tseitin CNF;
  * context dilution for a pass-through transformation.

Finite checks are evidence only.  The symbolic claims in the accompanying report
are proved separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


Clause = Tuple[int, ...]


def truth(assignment: int, variable: int) -> bool:
    return bool((assignment >> (variable - 1)) & 1)


def eval_lit(lit: int, values: Dict[int, bool]) -> bool:
    value = values[abs(lit)]
    return value if lit > 0 else not value


def eval_cnf(clauses: Sequence[Clause], values: Dict[int, bool]) -> bool:
    return all(any(eval_lit(lit, values) for lit in clause) for clause in clauses)


def selector_clauses(t: int) -> Tuple[int, List[Clause]]:
    z = 4 * t + 1
    clauses: List[Clause] = []
    for i in range(t):
        clauses.append((z, 4 * i + 1, 4 * i + 2))
    for j in range(t):
        clauses.append((-z, 4 * j + 3, 4 * j + 4))
    return z, clauses


def projection_clauses(t: int) -> List[Clause]:
    return [
        (4 * i + 1, 4 * i + 2, 4 * j + 3, 4 * j + 4)
        for i in range(t)
        for j in range(t)
    ]


@dataclass(frozen=True)
class Gate:
    out: int
    op: str
    left: int
    right: int


def balanced_reduce(op: str, wires: List[int], next_id: int) -> Tuple[int, List[Gate], int]:
    """Return a balanced fan-in-two reduction; a singleton needs no gate."""
    gates: List[Gate] = []
    layer = list(wires)
    while len(layer) > 1:
        nxt: List[int] = []
        it = iter(layer)
        for left in it:
            try:
                right = next(it)
            except StopIteration:
                nxt.append(left)
                break
            gates.append(Gate(next_id, op, left, right))
            nxt.append(next_id)
            next_id += 1
        layer = nxt
    return layer[0], gates, next_id


def factored_circuit(t: int) -> Tuple[List[Gate], int]:
    next_id = 4 * t + 1
    gates: List[Gate] = []
    a_wires: List[int] = []
    b_wires: List[int] = []
    for i in range(t):
        gates.append(Gate(next_id, "OR", 4 * i + 1, 4 * i + 2))
        a_wires.append(next_id)
        next_id += 1
    for j in range(t):
        gates.append(Gate(next_id, "OR", 4 * j + 3, 4 * j + 4))
        b_wires.append(next_id)
        next_id += 1
    a_root, more, next_id = balanced_reduce("AND", a_wires, next_id)
    gates.extend(more)
    b_root, more, next_id = balanced_reduce("AND", b_wires, next_id)
    gates.extend(more)
    gates.append(Gate(next_id, "OR", a_root, b_root))
    return gates, next_id


def eval_circuit(gates: Sequence[Gate], root: int, input_values: Dict[int, bool]) -> Dict[int, bool]:
    values = dict(input_values)
    for gate in gates:
        if gate.op == "OR":
            values[gate.out] = values[gate.left] or values[gate.right]
        elif gate.op == "AND":
            values[gate.out] = values[gate.left] and values[gate.right]
        else:
            raise ValueError(gate.op)
    assert root in values
    return values


def tseitin_clauses(gates: Sequence[Gate], root: int) -> List[Clause]:
    clauses: List[Clause] = []
    for gate in gates:
        y, x, w = gate.out, gate.left, gate.right
        if gate.op == "OR":
            clauses.extend(((-x, y), (-w, y), (x, w, -y)))
        elif gate.op == "AND":
            clauses.extend(((x, -y), (w, -y), (-x, -w, y)))
        else:
            raise ValueError(gate.op)
    clauses.append((root,))
    return clauses


def dimacs(num_vars: int, clauses: Sequence[Clause]) -> bytes:
    rows = [f"p cnf {num_vars} {len(clauses)}\n"]
    rows.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(rows).encode("ascii")


def circuit_serialization(num_inputs: int, gates: Sequence[Gate], root: int) -> bytes:
    rows = [f"p circuit {num_inputs} {len(gates)}\n"]
    rows.extend(f"{g.out} {g.op} {g.left} {g.right}\n" for g in gates)
    rows.append(f"o {root}\n")
    return "".join(rows).encode("ascii")


def input_values(t: int, assignment: int) -> Dict[int, bool]:
    return {v: truth(assignment, v) for v in range(1, 4 * t + 1)}


def oracle_vacuity_control() -> dict:
    checks = 0
    per_n = []
    for n in range(1, 4):
        domain = 1 << n
        languages = 1 << domain
        for language in range(languages):
            for x in range(domain):
                answer = (language >> x) & 1
                # One-query skeleton with an input-dependent constant oracle.
                target_dependent_oracle = {0: answer}
                assert target_dependent_oracle[0] == answer
                checks += 1
                # A fixed language oracle queried at x also decides L, but only
                # relative to that oracle.
                fixed_language_oracle = lambda q, lang=language: (lang >> q) & 1
                assert fixed_language_oracle(x) == answer
                checks += 1
        per_n.append({"input_bits": n, "domain": domain, "languages": languages})
    return {"checks": checks, "per_n": per_n}


def gate_truth_table_control() -> int:
    checks = 0
    for op in ("OR", "AND"):
        for x in (False, True):
            for w in (False, True):
                expected = x or w if op == "OR" else x and w
                for y in (False, True):
                    gate = Gate(3, op, 1, 2)
                    clauses = tseitin_clauses([gate], 3)[:-1]
                    got = eval_cnf(clauses, {1: x, 2: w, 3: y})
                    assert got == (y == expected)
                    checks += 1
    return checks


def family_exhaustive() -> dict:
    total_assignments = 0
    rows = []
    for t in range(1, 5):
        z, selector = selector_clauses(t)
        projection = projection_clauses(t)
        gates, root = factored_circuit(t)
        tseitin = tseitin_clauses(gates, root)
        assert len(gates) == 4 * t - 1
        assert len(tseitin) == 12 * t - 2
        assert sum(map(len, tseitin)) == 28 * t - 6
        for assignment in range(1 << (4 * t)):
            inp = input_values(t, assignment)
            exists_z = any(eval_cnf(selector, {**inp, z: bool(zval)}) for zval in (0, 1))
            projection_value = eval_cnf(projection, inp)
            circuit_values = eval_circuit(gates, root, inp)
            circuit_value = circuit_values[root]
            tseitin_value = eval_cnf(tseitin, circuit_values)
            assert exists_z == projection_value == circuit_value == tseitin_value
            total_assignments += 1
        rows.append(
            {
                "t": t,
                "assignments": 1 << (4 * t),
                "selector_clauses": len(selector),
                "projection_clauses": len(projection),
                "circuit_gates": len(gates),
                "tseitin_clauses": len(tseitin),
                "tseitin_literal_occurrences": sum(map(len, tseitin)),
            }
        )
    assert total_assignments == 69904
    return {"assignments": total_assignments, "rows": rows}


def size_table() -> List[dict]:
    rows = []
    for t in (1, 2, 4, 8, 16, 32, 64, 128):
        z, selector = selector_clauses(t)
        projection = projection_clauses(t)
        gates, root = factored_circuit(t)
        tseitin = tseitin_clauses(gates, root)
        rows.append(
            {
                "t": t,
                "selector_dimacs_bytes": len(dimacs(z, selector)),
                "projection_dimacs_bytes": len(dimacs(4 * t, projection)),
                "circuit_bytes": len(circuit_serialization(4 * t, gates, root)),
                "tseitin_dimacs_bytes": len(dimacs(root, tseitin)),
                "projection_over_selector": len(dimacs(4 * t, projection)) / len(dimacs(z, selector)),
                "circuit_over_selector": len(circuit_serialization(4 * t, gates, root)) / len(dimacs(z, selector)),
                "tseitin_over_selector": len(dimacs(root, tseitin)) / len(dimacs(z, selector)),
            }
        )
    return rows


def context_dilution() -> List[dict]:
    t = 4
    z, selector = selector_clauses(t)
    projection = projection_clauses(t)
    rows = []
    for k in (0, 10, 100, 1000, 5000):
        context = [(z + i + 1,) for i in range(k)]
        parent = projection + context
        child = selector + context
        num_vars = z + k
        parent_bytes = len(dimacs(num_vars, parent))
        child_bytes = len(dimacs(num_vars, child))
        rows.append(
            {
                "context_clauses": k,
                "parent_projection_bytes": parent_bytes,
                "child_selector_bytes": child_bytes,
                "child_over_parent": child_bytes / parent_bytes,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).read_bytes()
    result = {
        "run_id": "ORACLE-CLOSURE-FIREWALL185",
        "deterministic": True,
        "random_seed": None,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "oracle_vacuity": oracle_vacuity_control(),
        "gate_truth_table_checks": gate_truth_table_control(),
        "family_exhaustive": family_exhaustive(),
        "physical_size_table": size_table(),
        "context_dilution": context_dilution(),
        "limitations": [
            "Finite checks do not establish an all-input SAT transformation.",
            "The circuit serialization is an explicit audit format, not a claim of canonical minimality.",
            "Context dilution refutes only pass-through fixed-power shrink claims.",
        ],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
