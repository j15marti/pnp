#!/usr/bin/env python3
"""Exact bridges from affine-table factors and CNF to closure/parity solving.

Requires only sibling affine_table.py and closure_parity.py and Python 3.10+.
This research solver has no universal polynomial runtime guarantee.
Resource exhaustion or an unsupported table returns UNRESOLVED, never UNSAT.
"""
from __future__ import annotations

import argparse
import itertools
import json

from affine_table import Interface, dot, rref
from closure_parity import solve_2cnf_affine, solve_horn_affine
from seed_parity import solve_2cnf_affine_seeds, solve_horn_affine_seeds


def run_backend(kind, n, clauses, equations, strategy, term_cap, seed_cap):
    if strategy == "polynomial":
        solver = solve_2cnf_affine if kind == "2cnf" else solve_horn_affine
        return solver(n, clauses, equations, term_cap=term_cap)
    if strategy == "seeds":
        solver = solve_2cnf_affine_seeds if kind == "2cnf" else solve_horn_affine_seeds
        return solver(n, clauses, equations, seed_cap=seed_cap)
    raise ValueError("Unknown exact backend")


def dependency_equations(rows):
    """Basis of the exact homogeneous dependencies among the listed forms."""
    echelon = {}
    dependencies = []
    for index, original in enumerate(rows):
        row, names = original, 1 << index
        for pivot in sorted(echelon):
            if (row >> pivot) & 1:
                basis_row, basis_names = echelon[pivot]
                row ^= basis_row
                names ^= basis_names
        if row:
            pivot = (row & -row).bit_length() - 1
            echelon[pivot] = (row, names)
        else:
            dependencies.append((names, 0))
    return tuple(dependencies)


def bijunctive_encoding(arity, table):
    """Exact 2CNF encoding of an explicit relation, or None if non-bijunctive.

    Compute all entailed unary/binary clauses and check their conjunction on
    every table entry. This is polynomial in the ALREADY EXPLICIT table size.
    """
    if len(table) != 1 << arity:
        raise ValueError("Malformed explicit table")
    accepted = [point for point, value in enumerate(table) if value]
    if not accepted:
        return [()]
    clauses = []
    for width in (1, 2):
        for scope in itertools.combinations(range(arity), width):
            seen = {sum(((point >> variable) & 1) << j
                        for j, variable in enumerate(scope)) for point in accepted}
            for forbidden in range(1 << width):
                if forbidden not in seen:
                    clauses.append(tuple(-(variable + 1) if (forbidden >> j) & 1
                                         else variable + 1
                                         for j, variable in enumerate(scope)))
    for point, desired in enumerate(table):
        actual = all(any(bool((point >> (abs(lit) - 1)) & 1) == (lit > 0)
                         for lit in clause) for clause in clauses)
        if actual != bool(desired):
            return None
    return clauses


def solve_affine_tables(factors, term_cap=None, strategy="polynomial", seed_cap=None):
    """Solve affine cores plus explicitly bijunctive tables, with a full lift.

    Every <=2-coordinate table qualifies. Larger already-materialized tables
    are recognized exactly. All unary observations are included, repairing
    the historical binary-only observation error documented in ARC228.
    """
    factors = tuple(factors)
    n = factors[0].n if factors else 0
    if n < 0 or any(f.n != n for f in factors):
        raise ValueError("Factors must have the same nonnegative dimension")
    for factor in factors:
        if len(factor.table) != 1 << factor.width:
            raise ValueError("Malformed table length")
        if any(mask < 0 or mask >> n or rhs not in (0, 1)
               for mask, rhs in factor.equations):
            raise ValueError("Malformed affine equation")
        if any(mask < 0 or mask >> n for mask in factor.forms):
            raise ValueError("Malformed coordinate form")
    details = {"ambient_variables": n, "factors": len(factors),
               "local_assignments_scanned": 0}
    core = rref(row for factor in factors for row in factor.equations)
    if core is None:
        return {"status": "UNSAT", "witness": None,
                "reason": "inconsistent_affine_core", "bridge": details}
    details["affine_core_rank"] = len(core)
    row_to_name, rows, clauses = {}, [], []
    for factor_index, factor in enumerate(factors):
        coordinates = []
        for mask in factor.forms:
            shift = 0
            for pivot_mask, rhs in core:
                pivot = (pivot_mask & -pivot_mask).bit_length() - 1
                if (mask >> pivot) & 1:
                    mask ^= pivot_mask
                    shift ^= rhs
            name = None
            if mask:
                if mask not in row_to_name:
                    row_to_name[mask] = len(rows)
                    rows.append(mask)
                name = row_to_name[mask]
            coordinates.append((name, shift))
        used = sorted({name for name, _ in coordinates if name is not None})
        positions = {name: j for j, name in enumerate(used)}
        local_table = []
        for point in range(1 << len(used)):
            argument = sum((shift if name is None else
                            (((point >> positions[name]) & 1) ^ shift)) << j
                           for j, (name, shift) in enumerate(coordinates))
            local_table.append(bool(factor.table[argument]))
        details["local_assignments_scanned"] += len(local_table)
        local_clauses = bijunctive_encoding(len(used), local_table)
        if local_clauses is None:
            details["unsupported_factor"] = factor_index
            return {"status": "UNRESOLVED", "witness": None,
                    "reason": "explicit_table_is_not_bijunctive", "bridge": details}
        for clause in local_clauses:
            clauses.append(tuple((used[abs(literal) - 1] + 1) *
                                 (1 if literal > 0 else -1) for literal in clause))

    # Observe EVERY coordinate used by a unary or binary clause. Other forms
    # can be existentially omitted; their values do not affect the encoding.
    observed = sorted({abs(literal) - 1 for clause in clauses for literal in clause})
    renaming = {old: new + 1 for new, old in enumerate(observed)}
    rows = [rows[index] for index in observed]
    clauses = [tuple(renaming[abs(lit) - 1] * (1 if lit > 0 else -1)
                     for lit in clause) for clause in clauses]
    dependencies = dependency_equations(rows)
    details.update(observed_coordinates=len(rows), dependency_rank=len(dependencies),
                   coordinate_rank=len(rows) - len(dependencies),
                   translated_clauses=len(clauses))
    answer = run_backend("2cnf", len(rows), clauses, dependencies,
                         strategy, term_cap, seed_cap)
    answer["bridge"] = details
    if answer["status"] == "SAT":
        coordinate_model = answer["witness"]
        lifted = rref((*core, *((row, (coordinate_model >> j) & 1)
                               for j, row in enumerate(rows))))
        if lifted is None:
            raise AssertionError("Exact coordinate image failed witness lifting")
        witness = sum(rhs << ((mask & -mask).bit_length() - 1)
                      for mask, rhs in lifted)
        if not all(factor.accepts(witness) for factor in factors):
            raise AssertionError("Lifted model fails an original factor")
        answer["coordinate_witness"] = coordinate_model
        answer["witness"] = witness
    return answer


def selector_encoding(n, clauses):
    """Exact arbitrary-CNF to Horn2CNF plus disjoint odd-selector equations.

    Variable identifiers are relabeled densely before any integer bitmask is
    allocated, so a sparse large DIMACS identifier cannot inflate memory.
    """
    clauses = tuple(tuple(clause) for clause in clauses)
    if n < 0 or any(not isinstance(lit, int) or lit == 0 or abs(lit) > n
                    for clause in clauses for lit in clause):
        raise ValueError("Invalid CNF input")
    identifiers = sorted({abs(lit) for clause in clauses for lit in clause})
    renaming = {old: new + 1 for new, old in enumerate(identifiers)}
    original = [tuple(renaming[abs(lit)] * (1 if lit > 0 else -1)
                      for lit in clause) for clause in clauses]
    next_name = len(identifiers) + 1
    horn, equations = [], []
    for clause in original:
        selectors = list(range(next_name, next_name + len(clause)))
        next_name += len(clause)
        equations.append((sum(1 << (name - 1) for name in selectors), 1))
        horn.extend((-a, -b) for a, b in itertools.combinations(selectors, 2))
        horn.extend((-selector, literal) for selector, literal in zip(selectors, clause))
    return next_name - 1, horn, equations, identifiers, original


def solve_cnf_via_selectors(n, clauses, term_cap=None, strategy="polynomial", seed_cap=None):
    size, horn, equations, identifiers, dense_original = selector_encoding(n, clauses)
    answer = run_backend("horn", size, horn, equations, strategy, term_cap, seed_cap)
    answer["selector_bridge"] = {"original_occurring_variables": len(identifiers),
                                 "encoded_variables": size,
                                 "horn_clauses": len(horn), "parity_rows": len(equations)}
    if answer["status"] == "SAT":
        encoded_model = answer["witness"]
        dense_model = encoded_model & ((1 << len(identifiers)) - 1)
        if not all(any(bool((dense_model >> (abs(lit) - 1)) & 1) == (lit > 0)
                       for lit in clause) for clause in dense_original):
            raise AssertionError("Selector model fails original CNF")
        answer["encoded_witness"] = encoded_model
        answer["witness"] = dense_model
        answer["original_assignment"] = {str(old): bool((dense_model >> j) & 1)
                                          for j, old in enumerate(identifiers)}
    return answer


def read_dimacs(path):
    n, expected, clauses, current = None, None, [], []
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                header = line.split()
                if n is not None or len(header) != 4 or header[:2] != ["p", "cnf"]:
                    raise ValueError("Expected one DIMACS CNF header")
                n, expected = map(int, header[2:])
                if n < 0 or expected < 0:
                    raise ValueError("Negative DIMACS dimensions")
                continue
            if n is None:
                raise ValueError("DIMACS clauses precede header")
            for token in line.split():
                literal = int(token)
                if literal:
                    if abs(literal) > n:
                        raise ValueError("DIMACS literal exceeds declared range")
                    current.append(literal)
                else:
                    clauses.append(tuple(current))
                    current = []
    if n is None or current or len(clauses) != expected:
        raise ValueError("Malformed DIMACS clause count or terminator")
    return n, clauses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["factors", "2cnf", "horn", "cnf"])
    parser.add_argument("input", help="JSON for factors/2cnf/horn; DIMACS for cnf")
    parser.add_argument("--term-cap", type=int, default=100000,
                        help="Cap on any temporary polynomial; default 100000")
    parser.add_argument("--strategy", choices=["polynomial", "seeds"], default="polynomial")
    parser.add_argument("--seed-cap", type=int, default=100000,
                        help="Maximum attempted seeds with the streaming strategy")
    parser.add_argument("--uncapped", action="store_true",
                        help="Allow complete finite computation, potentially exponential")
    args = parser.parse_args()
    cap = None if args.uncapped else args.term_cap
    seed_cap = None if args.uncapped else args.seed_cap
    if args.mode == "cnf":
        n, clauses = read_dimacs(args.input)
        result = solve_cnf_via_selectors(n, clauses, cap, args.strategy, seed_cap)
    else:
        with open(args.input, encoding="utf-8") as handle:
            data = json.load(handle)
        if args.mode == "factors":
            factors = [Interface(data["n"], tuple(map(tuple, f.get("equations", []))),
                                 tuple(f.get("forms", [])), tuple(f["table"]))
                       for f in data["factors"]]
            result = solve_affine_tables(factors, cap, args.strategy, seed_cap)
        else:
            result = run_backend(args.mode, data["n"], data["clauses"], data["equations"],
                                 args.strategy, cap, seed_cap)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
