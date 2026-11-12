#!/usr/bin/env python3
"""Exact polynomial terminal test for independent affine 2-SAT coordinates.

Each factor is an affine_table.Interface: [A_i x=b_i] AND f_i(L_i x).
If every table has at most two inputs and the distinct nonconstant coordinate
forms are independent modulo the combined affine core, their values are jointly
surjective.  The remaining problem is ordinary 2-SAT, solved by SCCs.

Dependent coordinates return UNRESOLVED; they are never treated as independent.
No large joined table, SAT oracle, or semantic equivalence oracle is used.

Run reproducible independent checks with:
  python independent_2sat.py small --out independent_2sat_small.json
  python independent_2sat.py wide --out independent_2sat_wide.json
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

from affine_table import Interface, basis, dot, rref


def _scc_2sat(variable_count: int, clauses: list[tuple[int, ...]]):
    """Iterative Kosaraju algorithm. Return one assignment or None if UNSAT."""
    graph = [[] for _ in range(2 * variable_count)]
    reverse = [[] for _ in range(2 * variable_count)]

    def vertex(literal):
        return 2 * (abs(literal) - 1) + int(literal < 0)

    def edge(u, v):
        graph[u].append(v)
        reverse[v].append(u)

    for clause in clauses:
        if not clause:
            return None
        if len(clause) == 1:
            a = vertex(clause[0])
            edge(a ^ 1, a)
        elif len(clause) == 2:
            a, b = map(vertex, clause)
            edge(a ^ 1, b)
            edge(b ^ 1, a)
        else:
            raise ValueError("The implication solver accepts only 2-CNF")

    seen = [False] * len(graph)
    order = []
    for start in range(len(graph)):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            node, pos = stack[-1]
            if pos == len(graph[node]):
                order.append(node)
                stack.pop()
                continue
            other = graph[node][pos]
            stack[-1] = (node, pos + 1)
            if not seen[other]:
                seen[other] = True
                stack.append((other, 0))

    component = [-1] * len(graph)
    component_id = 0
    for start in reversed(order):
        if component[start] != -1:
            continue
        component[start] = component_id
        stack = [start]
        while stack:
            node = stack.pop()
            for other in reverse[node]:
                if component[other] == -1:
                    component[other] = component_id
                    stack.append(other)
        component_id += 1
    if any(component[2 * j] == component[2 * j + 1]
           for j in range(variable_count)):
        return None
    values = tuple(component[2 * j] > component[2 * j + 1]
                   for j in range(variable_count))
    if not all(any(values[abs(lit) - 1] == (lit > 0) for lit in c)
               for c in clauses):
        raise AssertionError("The SCC assignment failed its 2-CNF verification")
    return values


def decide_independent_2sat(factors):
    """Return (True/False/None, diagnostics), with None meaning UNRESOLVED.

    This sufficient terminal test is polynomial in the explicit input size.
    A SAT result includes a lifted assignment to the original variables.
    """
    factors = tuple(factors)
    n = factors[0].n if factors else 0
    details = {"ambient_variables": n, "factors": len(factors),
               "status": None, "reason": None}
    if n < 0 or any(f.n != n for f in factors):
        raise ValueError("All factors must share one nonnegative ambient dimension")
    for f in factors:
        if len(f.table) != 1 << f.width:
            raise ValueError("Malformed factor truth table")
        if any(m < 0 or m >> n or b not in (0, 1) for m, b in f.equations):
            raise ValueError("Malformed affine equation")
        if any(m < 0 or m >> n for m in f.forms):
            raise ValueError("Malformed coordinate form")
    core = rref(row for f in factors for row in f.equations)
    if core is None:
        details.update(status="UNSAT", reason="inconsistent_affine_core")
        return False, details
    details["affine_rank"] = len(core)
    if any(f.width > 2 for f in factors):
        details.update(status="UNRESOLVED", reason="factor_has_more_than_two_coordinates")
        return None, details

    reduced = []
    row_to_variable = {}
    distinct_rows = []
    for factor in factors:
        coordinates = []
        for mask in factor.forms:
            shift = 0
            for pivot_mask, rhs in core:
                pivot = (pivot_mask & -pivot_mask).bit_length() - 1
                if (mask >> pivot) & 1:
                    mask ^= pivot_mask
                    shift ^= rhs
            if mask:
                if mask not in row_to_variable:
                    row_to_variable[mask] = len(distinct_rows)
                    distinct_rows.append(mask)
                index = row_to_variable[mask]
            else:
                index = None
            coordinates.append((index, shift))
        reduced.append((factor.table, coordinates))

    rank = len(basis(distinct_rows))
    details.update(distinct_coordinates=len(distinct_rows), coordinate_rank=rank)
    if rank != len(distinct_rows):
        details.update(status="UNRESOLVED", reason="coordinate_dependencies_remain")
        return None, details

    clauses = []
    for table, coordinates in reduced:
        used = sorted({index for index, _ in coordinates if index is not None})
        local_index = {v: j for j, v in enumerate(used)}
        for assignment in range(1 << len(used)):
            table_index = 0
            for j, (index, shift) in enumerate(coordinates):
                value = shift if index is None else (((assignment >> local_index[index]) & 1) ^ shift)
                table_index |= value << j
            if not table[table_index]:
                clause = tuple(-(index + 1) if (assignment >> j) & 1 else index + 1
                               for j, index in enumerate(used))
                clauses.append(clause)
    details["translated_clauses"] = len(clauses)
    values = _scc_2sat(len(distinct_rows), clauses)
    if values is None:
        details.update(status="UNSAT", reason="two_sat_contradiction")
        return False, details

    # Independence modulo the core guarantees this lift is consistent.
    lift = rref((*core, *((row, int(value)) for row, value in zip(distinct_rows, values))))
    if lift is None:
        raise AssertionError("Independent coordinate values failed to lift")
    witness = sum(rhs << ((mask & -mask).bit_length() - 1) for mask, rhs in lift)
    if not all(f.accepts(witness) for f in factors):
        raise AssertionError("The lifted witness failed the original factor checks")
    details.update(status="SAT", reason="independent_coordinates_reduce_to_two_sat",
                   witness_hex=hex(witness))
    return True, details


def _independent_accepts(factor, assignment):
    """Semantic checker using direct coordinate sums, not producer row reduction."""
    def parity(mask):
        return sum((assignment >> j) & 1 for j in range(factor.n) if (mask >> j) & 1) % 2
    if any(parity(mask) != rhs for mask, rhs in factor.equations):
        return False
    argument = sum(parity(mask) << j for j, mask in enumerate(factor.forms))
    return bool(factor.table[argument])


def _brute_answer(factors):
    n = factors[0].n if factors else 0
    return any(all(_independent_accepts(f, x) for f in factors) for x in range(1 << n))


def _factor_record(factor):
    return {"n": factor.n, "equations": factor.equations,
            "forms": factor.forms, "table": factor.table}


def _two_clause_factor(n, clause, coordinate_forms=None):
    """Build a factor directly from one clause over supplied coordinate names."""
    names = sorted({abs(literal) for literal in clause})
    if len(names) > 2:
        raise ValueError("Two-variable clauses only")
    forms = tuple((1 << (j - 1)) if coordinate_forms is None else coordinate_forms[j - 1]
                  for j in names)
    positions = {name: j for j, name in enumerate(names)}
    table = tuple(any(bool((z >> positions[abs(literal)]) & 1) == (literal > 0)
                      for literal in clause) for z in range(1 << len(names)))
    return Interface(n, (), forms, table)


def verify_small(seed):
    rng = random.Random(seed)
    cases = []
    assertions = 0

    def check(label, factors, must_resolve=False, must_unresolved=False):
        nonlocal assertions
        expected = _brute_answer(factors)
        result, details = decide_independent_2sat(factors)
        if result is not None:
            assert result == expected, (label, factors, expected, details)
        if must_resolve:
            assert result is not None, (label, factors, details)
        if must_unresolved:
            assert result is None, (label, factors, details)
        if result:
            witness = int(details["witness_hex"], 16)
            assert all(_independent_accepts(f, witness) for f in factors)
        assertions += 1
        cases.append({"label": label, "factors": [_factor_record(f) for f in factors],
                      "brute_force_answer": expected, "answer": result, "details": details})

    # Exhaust all subsets of non-tautological unit and binary clauses on two variables.
    possible = [(1,), (-1,), (2,), (-2,),
                (1, 2), (1, -2), (-1, 2), (-1, -2)]
    for mask in range(1 << len(possible)):
        factors = [_two_clause_factor(2, clause) for j, clause in enumerate(possible)
                   if (mask >> j) & 1]
        check(f"all_two_variable_2cnf_{mask}", factors, must_resolve=True)

    # Every pair of arbitrary Boolean relations on the same two coordinates.
    for a in range(16):
        for b in range(16):
            factors = [Interface(2, (), (1, 2), tuple(bool((mask >> z) & 1) for z in range(4)))
                       for mask in (a, b)]
            check(f"all_two_factor_tables_{a}_{b}", factors, must_resolve=True)

    # Construct independent coordinates modulo random affine cores, including shifts,
    # repeated coordinates, constant coordinates, and arbitrary local tables.
    for case in range(240):
        n = rng.randrange(1, 8)
        invertible = [1 << j for j in range(n)]
        for _ in range(6 * n):
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                invertible[a] ^= invertible[b]
        fixed = rng.randrange(n + 1)
        eqs = tuple((invertible[j], rng.randrange(2)) for j in range(fixed))
        factors = [Interface(n, eqs, (), (True,))]
        for _ in range(rng.randrange(1, 9)):
            k = rng.randrange(3)
            forms = []
            for _ in range(k):
                choices = [0] + invertible[fixed:]
                mask = rng.choice(choices)
                for j in range(fixed):
                    if rng.randrange(2):
                        mask ^= invertible[j]
                forms.append(mask)
            table = tuple(bool(rng.randrange(2)) for _ in range(1 << k))
            factors.append(Interface(n, (), tuple(forms), table))
        check(f"random_independent_{case}", factors, must_resolve=True)

    # Arbitrary affine factors may be dependent. Every resolved output is checked
    # by exhaustive enumeration; unresolved is explicitly retained as a third result.
    for case in range(240):
        n = rng.randrange(1, 8)
        anchor = rng.randrange(1 << n)
        factors = []
        for _ in range(rng.randrange(1, 9)):
            k = rng.randrange(3)
            eqs = []
            for _ in range(rng.randrange(3)):
                row = rng.randrange(1 << n)
                rhs = (row & anchor).bit_count() % 2
                if rng.randrange(20) == 0:
                    rhs ^= 1
                eqs.append((row, rhs))
            forms = tuple(rng.randrange(1 << n) for _ in range(k))
            table = tuple(bool(rng.randrange(2)) for _ in range(1 << k))
            factors.append(Interface(n, tuple(eqs), forms, table))
        check(f"random_arbitrary_{case}", factors)

    # If dependencies were discarded, all three unary factors would be satisfiable
    # independently, although x=0, y=0, x XOR y=1 are inconsistent together.
    for rhs in (0, 1):
        factors = [Interface(2, (), (1,), (True, False)),
                   Interface(2, (), (2,), (True, False)),
                   Interface(2, (), (3,), (not rhs, bool(rhs)))]
        check(f"dependent_coordinate_control_{rhs}", factors, must_unresolved=True)

    # These factors are already intrinsically width two: each permits three of
    # four coordinate patterns, with full affine hull and no nonzero period.
    # Their coordinate sets include x, y, and x XOR y, hence have rank two, not three.
    normalized_dependency = [
        Interface(2, (), (1, 2), (False, True, True, True)),  # excludes x=y=0
        Interface(2, (), (1, 3), (True, True, True, False)),  # excludes x=1,y=0
        Interface(2, (), (2, 3), (True, True, True, False)),  # excludes x=0,y=1
    ]
    check("normalized_width_two_dependency_sat", normalized_dependency, must_unresolved=True)
    check("normalized_width_two_dependency_unsat", normalized_dependency +
          [Interface(2, (), (1, 2), (True, True, True, False))], must_unresolved=True)

    return {"stage": "small", "assertions": assertions, "failures": 0,
            "exhaustive_2cnf_formulas": 256, "exhaustive_table_pairs": 256,
            "random_independent": 240, "random_arbitrary": 240,
            "resolved_sat": sum(c["answer"] is True for c in cases),
            "resolved_unsat": sum(c["answer"] is False for c in cases),
            "unresolved": sum(c["answer"] is None for c in cases), "cases": cases}


def verify_wide(seed):
    n = 1000
    results = []
    assertions = 0
    for label, coordinate_forms in (
        ("ordinary_2sat", tuple(1 << j for j in range(n))),
        ("invertible_affine_2sat", tuple((1 << j) ^ (1 << (j + 1)) for j in range(n - 1))
                                      + (1 << (n - 1),)),
    ):
        clauses = [(1,)] + [(-j, j + 1) for j in range(1, n)]
        for contradiction in (False, True):
            actual = clauses + ([(-n,)] if contradiction else [])
            factors = [_two_clause_factor(n, clause, coordinate_forms) for clause in actual]
            result, details = decide_independent_2sat(factors)
            assert result is (not contradiction), details
            assert details["distinct_coordinates"] == n
            assert details["coordinate_rank"] == n
            if result:
                witness = int(details["witness_hex"], 16)
                assert all(_independent_accepts(f, witness) for f in factors)
            assertions += 1
            results.append({"label": label, "variables": n, "clauses": actual,
                            "coordinate_recipe": "unit vectors" if label == "ordinary_2sat"
                            else "q_j=x_j XOR x_(j+1) for j<n; q_n=x_n",
                            "expected_answer": not contradiction, "answer": result,
                            "details": details})
    return {"stage": "wide", "assertions": assertions, "failures": 0, "cases": results,
            "explanation": "1000 independent coordinates, <=2 inputs per factor, no joined exponential table."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("small", "wide"))
    parser.add_argument("--seed", type=int, default=20261111)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    result = {"small": verify_small, "wide": verify_wide}[args.stage](args.seed)
    result.update(seed=args.seed, status="COMPUTATIONAL",
                  elapsed_seconds=time.perf_counter() - started,
                  limitation="Finite exact comparisons; independence is a sufficient condition, not a universal SAT theorem.",
                  source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__), Path(__file__).with_name("affine_table.py"))})
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}, indent=2))
