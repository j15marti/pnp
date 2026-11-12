#!/usr/bin/env python3
"""Finite exact audit of the ATC2 selector encoding and clause-coverage DP.

The compiler follows ATC2's ``selector_encoding``: densely relabel occurring
original variables; create one selector per literal occurrence; add pairwise
exclusions and selector-to-literal implications; add one odd-parity row per
clause.  The DP is a separate global controller for this particular image.

For an m-clause CNF, a DP state is the subset of clauses already satisfied.
Each original variable has two transitions, adding its positive or negative
occurrence mask.  This yields 2**m * poly(input length) time, including witness
reconstruction.  Finite tests below do not establish an asymptotic lower bound.

Only new output files are created.  Existing output paths are never overwritten.
Python 3.10+, standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SEED = 20261111
ATC2_REPORT = {
    "path": "research/explorations/sat-composition/2026-11-11_AFFINE_TABLE_COMPOSITION2/compatibility_continuation.tex",
    "git_blob_sha": "3809296b0a5f6ea85fc03bf1d8441b04e3017585",
}
ATC2_CODE = {
    "path": "experiments/sat_composition/2026-11-11_dependent_compatibility/composition_solver.py",
    "git_blob_sha": "575a6aec2c49e21452f1d6b28d6aca87a8c66f85",
    "functions": ["selector_encoding", "solve_cnf_via_selectors"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_cnf(n: int, clauses) -> tuple[tuple[int, ...], ...]:
    clauses = tuple(tuple(clause) for clause in clauses)
    if n < 0 or any(type(lit) is not int or lit == 0 or abs(lit) > n
                    for clause in clauses for lit in clause):
        raise ValueError("Invalid explicit CNF universe or literal")
    return clauses


def literal_value(literal: int, assignment: int) -> bool:
    value = bool((assignment >> (abs(literal) - 1)) & 1)
    return value if literal > 0 else not value


def cnf_value(clauses, assignment: int) -> bool:
    return all(any(literal_value(lit, assignment) for lit in clause)
               for clause in clauses)


def gf2_rank(rows) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


@dataclass(frozen=True)
class SelectorEncoding:
    declared_n: int
    source: tuple[tuple[int, ...], ...]
    identifiers: tuple[int, ...]
    dense_source: tuple[tuple[int, ...], ...]
    groups: tuple[tuple[int, ...], ...]
    horn_groups: tuple[tuple[tuple[int, int], ...], ...]
    rows: tuple[tuple[int, int], ...]
    encoded_n: int

    @property
    def horn(self) -> tuple[tuple[int, int], ...]:
        return tuple(clause for group in self.horn_groups for clause in group)


def selector_encoding(n: int, clauses) -> SelectorEncoding:
    """Exact ATC2 construction, preserving its occurring-variable convention."""
    source = validate_cnf(n, clauses)
    identifiers = tuple(sorted({abs(lit) for clause in source for lit in clause}))
    rename = {old: new + 1 for new, old in enumerate(identifiers)}
    dense = tuple(tuple(rename[abs(lit)] * (1 if lit > 0 else -1)
                        for lit in clause) for clause in source)
    next_name = len(identifiers) + 1
    groups, horn_groups, rows = [], [], []
    for clause in dense:
        selectors = tuple(range(next_name, next_name + len(clause)))
        next_name += len(clause)
        horn = tuple((-a, -b) for a, b in itertools.combinations(selectors, 2))
        horn += tuple((-selector, literal)
                      for selector, literal in zip(selectors, clause))
        groups.append(selectors)
        horn_groups.append(horn)
        rows.append((sum(1 << (name - 1) for name in selectors), 1))
    return SelectorEncoding(n, source, identifiers, dense, tuple(groups),
                            tuple(horn_groups), tuple(rows), next_name - 1)


def dense_outer(encoding: SelectorEncoding, assignment: int) -> int:
    return sum(((assignment >> (old - 1)) & 1) << new
               for new, old in enumerate(encoding.identifiers))


def encoded_value(encoding: SelectorEncoding, assignment: int) -> bool:
    return cnf_value(encoding.horn, assignment) and all(
        ((mask & assignment).bit_count() & 1) == rhs
        for mask, rhs in encoding.rows)


def lift_witness(encoding: SelectorEncoding, outer: int) -> int:
    require(cnf_value(encoding.source, outer), "Cannot lift a false source witness")
    result = dense_outer(encoding, outer)
    for clause, selectors in zip(encoding.source, encoding.groups):
        for literal, selector in zip(clause, selectors):
            if literal_value(literal, outer):
                result |= 1 << (selector - 1)
                break
        else:
            raise AssertionError("Source clause has no true literal")
    require(encoded_value(encoding, result), "Lifted witness fails encoding")
    return result


def clause_coverage_dp(n: int, clauses) -> dict:
    """Solve CNF and reconstruct one complete original-variable assignment.

    DP layer i stores exactly the attainable satisfied-clause masks after the
    first i variables.  Backpointers retain one assignment per reachable state.
    All attempted transitions are counted, including duplicate state insertions.
    """
    clauses = validate_cnf(n, clauses)
    positive, negative = [0] * n, [0] * n
    for j, clause in enumerate(clauses):
        for literal in clause:
            masks = positive if literal > 0 else negative
            masks[abs(literal) - 1] |= 1 << j
    layers: list[dict[int, tuple[int, int] | None]] = [{0: None}]
    transitions = 0
    for i in range(n):
        following: dict[int, tuple[int, int]] = {}
        for covered in layers[-1]:
            for value, addition in ((0, negative[i]), (1, positive[i])):
                transitions += 1
                following.setdefault(covered | addition, (covered, value))
        layers.append(following)
    target = (1 << len(clauses)) - 1
    witness = None
    if target in layers[-1]:
        witness, state = 0, target
        for i in range(n, 0, -1):
            previous, value = layers[i][state]
            witness |= value << (i - 1)
            state = previous
        require(state == 0 and cnf_value(clauses, witness), "DP reconstruction failed")
    return {
        "satisfiable": witness is not None,
        "witness_mask": witness,
        "witness_values": None if witness is None else [(witness >> i) & 1 for i in range(n)],
        "layer_state_counts": [len(layer) for layer in layers],
        "attempted_transitions": transitions,
        "peak_states": max(map(len, layers)),
    }


def projection_by_local_enumeration(encoding: SelectorEncoding, outer: int,
                                    counters: dict, forced: dict[int, int] | None = None) -> bool:
    """Check exact projection by all selector patterns separately per clause.

    Once outer variables are fixed, distinct selector blocks do not interact.
    Thus the conjunction has an extension iff every block has a local extension.
    This avoids a Cartesian enumeration while checking every local possibility.
    """
    forced = {} if forced is None else forced
    dense = dense_outer(encoding, outer)
    answers = []
    for clause, selectors, horn, (mask, rhs) in zip(
            encoding.source, encoding.groups, encoding.horn_groups, encoding.rows):
        counters["local_clause_checks"] += 1
        accepted = 0
        for pattern in range(1 << len(selectors)):
            counters["local_selector_patterns"] += 1
            candidate = dense | sum(((pattern >> t) & 1) << (selector - 1)
                                    for t, selector in enumerate(selectors))
            if any(((candidate >> (selector - 1)) & 1) != value
                   for selector, value in forced.items() if selector in selectors):
                continue
            if cnf_value(horn, candidate) and ((candidate & mask).bit_count() & 1) == rhs:
                accepted += 1
        if not forced:
            expected = sum(literal_value(literal, outer) for literal in clause)
            require(accepted == expected, "Selector patterns are not precisely true-literal choices")
        answers.append(accepted > 0)
    return all(answers)


def check_case(label: str, n: int, clauses, counters: dict) -> dict:
    clauses = validate_cnf(n, clauses)
    encoding = selector_encoding(n, clauses)
    dp = clause_coverage_dp(n, clauses)
    brute_models = [a for a in range(1 << n) if cnf_value(clauses, a)]
    require(dp["satisfiable"] == bool(brute_models), label + ": DP/exhaustive mismatch")
    require(all(sum(lit > 0 for lit in clause) <= 1 and len(clause) == 2
                for clause in encoding.horn), label + ": non-Horn/non-binary clause")
    literal_count = sum(map(len, clauses))
    expected_horn = sum(len(c) + len(c) * (len(c) - 1) // 2 for c in clauses)
    require(encoding.encoded_n == len(encoding.identifiers) + literal_count, "Variable count")
    require(len(encoding.horn) == expected_horn, "Horn clause count")
    rank = gf2_rank(mask for mask, _ in encoding.rows)
    nonempty = sum(bool(clause) for clause in clauses)
    require(rank == nonempty, "Disjoint-row rank mismatch")
    if all(len(clause) == 3 for clause in clauses):
        require(encoding.encoded_n == len(encoding.identifiers) + 3 * len(clauses), "3-CNF variable count")
        require(len(encoding.horn) == 6 * len(clauses), "3-CNF Horn count")
        require(rank == len(clauses), "3-CNF rank count")
        counters["exact_3cnf_count_checks"] += 1
    for outer in range(1 << n):
        counters["outer_assignments"] += 1
        possible = projection_by_local_enumeration(encoding, outer, counters)
        require(possible == cnf_value(clauses, outer), label + ": projection mismatch")
    encoded_witness = None
    if dp["satisfiable"]:
        encoded_witness = lift_witness(encoding, dp["witness_mask"])
        counters["lifted_witnesses"] += 1
    counters["cases"] += 1
    counters["sat_cases" if brute_models else "unsat_cases"] += 1
    return {
        "label": label, "declared_original_variables": n,
        "occurring_original_variables": len(encoding.identifiers),
        "clauses": clauses, "clause_count": len(clauses),
        "literal_occurrences": literal_count, "exhaustive_model_count": len(brute_models),
        "encoded_variables": encoding.encoded_n, "horn_binary_clauses": len(encoding.horn),
        "affine_rows": len(encoding.rows), "affine_rank": rank,
        "encoded_witness_mask": encoded_witness, "dp": dp,
    }


def proper_three_clauses(n: int) -> list[tuple[int, int, int]]:
    return [tuple(sign * variable for sign, variable in zip(signs, variables))
            for variables in itertools.combinations(range(1, n + 1), 3)
            for signs in itertools.product((-1, 1), repeat=3)]


def targeted_degree_audit(sat_encoding: SelectorEncoding, sat_outer: int,
                          unsat_clauses) -> dict:
    """Exact finite tests of an AND cube and a zero acceptance restriction."""
    lifted = lift_witness(sat_encoding, sat_outer)
    chosen = [next(selector for selector in group
                   if (lifted >> (selector - 1)) & 1)
              for group in sat_encoding.groups]
    width = len(chosen)
    base = dense_outer(sat_encoding, sat_outer)
    truth_table = []
    for point in range(1 << width):
        assignment = base | sum(((point >> j) & 1) << (selector - 1)
                                for j, selector in enumerate(chosen))
        require(cnf_value(sat_encoding.horn, assignment), "AND cube leaves Horn models")
        acceptance = int(all(((assignment & mask).bit_count() & 1) == rhs
                             for mask, rhs in sat_encoding.rows))
        require(acceptance == int(point == (1 << width) - 1), "Acceptance is not AND on cube")
        truth_table.append(acceptance)
    coefficients = truth_table[:]
    for bit in range(width):
        for mask in range(1 << width):
            if mask & (1 << bit):
                coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
    support = [mask for mask, coefficient in enumerate(coefficients) if coefficient]
    degree = max((mask.bit_count() for mask in support), default=0)
    require(width == 5 and support == [31] and degree == 5, "AND5 algebraic-degree mismatch")

    unsat_encoding = selector_encoding(3, unsat_clauses)
    horn_models = accepting_models = 0
    per_outer = []
    for outer in range(1 << 3):
        options = [([None] + [selector for literal, selector in zip(clause, selectors)
                              if literal_value(literal, outer)])
                   for clause, selectors in zip(unsat_encoding.source, unsat_encoding.groups)]
        current = 0
        for choices in itertools.product(*options):
            assignment = dense_outer(unsat_encoding, outer)
            assignment |= sum(1 << (selector - 1) for selector in choices if selector is not None)
            require(cnf_value(unsat_encoding.horn, assignment), "Generated non-Horn model")
            acceptance = int(all(((assignment & mask).bit_count() & 1) == rhs
                                 for mask, rhs in unsat_encoding.rows))
            require(acceptance == 0, "Unsatisfiable source has accepting Horn model")
            accepting_models += acceptance
            current += 1
        horn_models += current
        per_outer.append(current)
    require(horn_models == 6912 and per_outer == [864] * 8, "Full Horn-model count mismatch")
    return {
        "sat_and_cube": {
            "source_outer_witness_mask": sat_outer, "chosen_selector_ids": chosen,
            "fixed_other_selectors": 0, "cube_dimension": width,
            "horn_points_checked": 1 << width, "acceptance_truth_table": truth_table,
            "anf_nonzero_monomial_masks": support, "anf_degree": degree,
            "restricted_degree_lower_bound_from_cube": degree,
            "restricted_degree_upper_bound_from_affine_indicator": len(sat_encoding.rows),
        },
        "unsat_acceptance_restriction": {
            "source": "All eight proper 3-clauses on three variables",
            "enumeration": "For each outer assignment, each selector group is None or one selector whose source literal is true",
            "outer_assignments": 8, "horn_models_per_outer_assignment": per_outer,
            "horn_models_enumerated": horn_models, "accepting_horn_models": accepting_models,
            "acceptance_is_identically_zero_on_horn_models": True,
            "restricted_acceptance_degree": 0,
            "zero_function_degree_convention": "Use 0 as a nonnegative degree bound for the zero function",
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=root / "results/raw/review/2026-11-11_COMPATIBILITY_CORE_RETRY/selector_dp.json")
    args = parser.parse_args()
    output = args.out.resolve()
    cnf_output = output.with_name("dead_prefix.cnf")
    if output.exists() or cnf_output.exists():
        raise FileExistsError("Refusing to overwrite an immutable result or sample")
    started = time.perf_counter()
    counters = dict.fromkeys(("cases", "sat_cases", "unsat_cases", "outer_assignments",
                             "local_clause_checks", "local_selector_patterns",
                             "lifted_witnesses", "exact_3cnf_count_checks"), 0)
    records = []
    clauses3 = proper_three_clauses(3)
    for subset in range(1 << len(clauses3)):
        formula = [clause for j, clause in enumerate(clauses3) if (subset >> j) & 1]
        records.append(check_case(f"all_proper3_subsets_{subset:03d}", 3, formula, counters))
    exhaustive_summary = dict(counters)
    require(exhaustive_summary["cases"] == 256, "Exhaustive case count")
    require(exhaustive_summary["sat_cases"] == 255 and exhaustive_summary["unsat_cases"] == 1,
            "Exhaustive proper-three truth-table count")
    rng = random.Random(SEED)
    for n in (4, 5):
        catalog = proper_three_clauses(n)
        for index in range(64):
            formula = rng.sample(catalog, index % (2 * n + 7))
            records.append(check_case(f"seeded_n{n}_{index:02d}", n, formula, counters))
    controls = [
        ("empty_universe_true", 0, []),
        ("empty_clause_false", 0, [()]),
        ("contradictory_units", 1, [(1,), (-1,)]),
        ("tautology", 2, [(1, -1)]),
        ("repeated_literal_unsat", 2, [(1, 1, -2), (-1,), (2,)]),
        ("width_five", 5, [(1, 2, 3, 4, 5), (-1, -2, -3, -4, -5)]),
        ("sparse_identifiers", 7, [(2, -7), (7,), (-2,)]),
        ("complete_proper3_n4", 4, proper_three_clauses(4)),
        ("complete_proper3_n5", 5, proper_three_clauses(5)),
    ]
    for label, n, formula in controls:
        records.append(check_case(label, n, formula, counters))
    dead_clauses = ((1, 2, 3), (-1, 4, 5), (-1, 4, -5),
                    (-1, -4, 5), (-1, -4, -5))
    dead_record = check_case("five_clause_dead_prefix", 5, dead_clauses, counters)
    records.append(dead_record)
    dead_encoding = selector_encoding(5, dead_clauses)
    first_selector = dead_encoding.groups[0][0]
    prefix_outer = 1  # x=1; all remaining original variables zero.
    prefix_witness = dense_outer(dead_encoding, prefix_outer) | (1 << (first_selector - 1))
    require(cnf_value(dead_encoding.horn, prefix_witness), "Prefix Horn feasibility")
    first_row, first_rhs = dead_encoding.rows[0]
    require(((prefix_witness & first_row).bit_count() & 1) == first_rhs, "Prefix affine feasibility")
    continuation_counters = {"local_clause_checks": 0, "local_selector_patterns": 0}
    continuations = [outer for outer in range(1 << 5)
                     if projection_by_local_enumeration(dead_encoding, outer,
                                                        continuation_counters,
                                                        {first_selector: 1})]
    require(not continuations, "Dead prefix unexpectedly extends")
    require(dead_record["exhaustive_model_count"] == 12, "Dead-prefix source model count")
    degree_audits = targeted_degree_audit(dead_encoding, dead_record["dp"]["witness_mask"], clauses3)
    cnf_text = ("c Five-clause compatible-prefix control; 1=x 2=y 3=z 4=a 5=b\n"
                "c Selecting literal x in clause 1 is locally feasible but cannot extend.\n"
                "p cnf 5 5\n" + "".join(" ".join(map(str, clause)) + " 0\n" for clause in dead_clauses))
    elapsed = time.perf_counter() - started
    result = {
        "marker": "COMPATIBILITY_SELECTOR_DP_20261111_VERIFIED_V1",
        "status": "PASS", "proof_status": "Finite implementation verification; P versus NP remains open",
        "provenance": {
            "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
            "platform": platform.platform(), "random_seed": SEED,
            "script_path": str(Path(__file__).resolve()),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_report": ATC2_REPORT, "source_compiler": ATC2_CODE,
            "execution_seconds_before_serialization": elapsed,
        },
        "method": {
            "exhaustive_family": "All 256 subsets of eight signed proper 3-clauses on variables 1,2,3",
            "additional_cases": "64 seeded cases each on four and five variables; nine hostile controls; one dead-prefix control",
            "projection_check": "Every original assignment; every selector pattern separately per clause, using the disjoint-support factorization",
            "compiler_variable_convention": "n in n+3m counts occurring original variables, matching ATC2 dense relabelling; an empty formula has n=0",
            "controller": "Clause-coverage DP; two transitions per prior state; all transitions charged; full predecessor witness reconstruction",
            "limitations": "Finite checks, not an asymptotic lower bound or a proof-assistant verification; state counts are not Turing-machine instruction counts",
        },
        "exhaustive_3variable_summary": exhaustive_summary,
        "all_cases_summary": counters,
        "mismatches": [],
        "targeted_degree_audits": degree_audits,
        "dead_prefix": {
            "source_variable_names": ["x", "y", "z", "a", "b"],
            "cnf_path": str(cnf_output),
            "cnf_sha256": hashlib.sha256(cnf_text.encode()).hexdigest(),
            "source_model_count": dead_record["exhaustive_model_count"],
            "dp_witness": dead_record["dp"],
            "forced_selector": first_selector, "forced_selector_value": 1,
            "locally_feasible_prefix_encoded_witness": prefix_witness,
            "prefix_requirement": "All Horn clauses and first affine row only; later selector rows not yet imposed",
            "full_continuation_outer_assignment_count": len(continuations),
            "continuation_original_assignments_checked": 32,
            "continuation_check_counters": continuation_counters,
        },
        "cases": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with cnf_output.open("x", encoding="utf-8") as handle:
        handle.write(cnf_text)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"status": result["status"], "output": str(output),
                      "script_sha256": result["provenance"]["script_sha256"],
                      "seconds": elapsed, "summary": counters,
                      "exhaustive_3variable_summary": exhaustive_summary,
                      "dead_prefix_source_models": 12,
                      "dead_prefix_continuations": len(continuations)}, indent=2))


if __name__ == "__main__":
    main()
