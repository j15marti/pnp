#!/usr/bin/env python3
"""Exact finite audit of the Claude/TMR equality-family sign geometry.

Run from any directory with CPython 3.9+:
    python experiments/review/claude_tmr_eq_merge001.py

Only the Python standard library is used. The SAT oracle enumerates all
assignments by bitset truth tables. It evaluates the actual clauses and does
not use the equality, component-independence, sensitivity, or distance claims.
An independently implemented scalar assignment oracle checks selected cases.

The experiment concerns sign edits on a fixed valid proper-3-CNF incidence
pattern. It is not a physical Turing-machine simulation, a runtime lower bound,
or a proof of the all-n mathematical statements.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import time
from zoneinfo import ZoneInfo


RUN_ID = "CLAUDE_TMR_EQ_MERGE001"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "results/raw/review/2026-11-14_CLAUDE_TMR_EQ_MERGE001_RAW.json"


class Audit:
    def __init__(self) -> None:
        self.assertions = 0
        self.bitset_oracle_calls = 0
        self.scalar_oracle_calls = 0

    def require(self, condition: bool, message: str) -> None:
        self.assertions += 1
        if not condition:
            raise AssertionError(message)


def forcing_gadget(literal: int, u: int, v: int) -> tuple[tuple[int, int, int], ...]:
    """The four original clauses, without applying their claimed semantics."""
    return tuple((literal, su * u, sv * v) for su in (1, -1) for sv in (1, -1))


def equality_formula(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    """Two banks, matching the original E_n clause order.

    The shared variables have identifiers 1..n. Bank a's fresh auxiliaries
    have identifiers n+1..3n; bank b's have identifiers 3n+1..5n.
    """
    if len(a) != len(b) or not a or any(x not in (0, 1) for x in a + b):
        raise ValueError("a and b must be nonempty Boolean words of equal length")
    n = len(a)
    clauses: list[tuple[int, int, int]] = []
    for bank, word in enumerate((a, b)):
        for i, value in enumerate(word):
            literal = (i + 1) if value else -(i + 1)
            u = n + 2 * n * bank + 2 * i + 1
            clauses.extend(forcing_gadget(literal, u, u + 1))
    return tuple(clauses)


def component_coordinates(n: int, i: int) -> tuple[int, ...]:
    """The 24 sign coordinates belonging to component i, in bank order."""
    return tuple(range(12 * i, 12 * i + 12)) + tuple(range(12 * (n + i), 12 * (n + i) + 12))


def central_quadruples(n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(12 * g + 3 * clause for clause in range(4)) for g in range(2 * n))


class TruthTableOracle:
    """Generic exhaustive SAT oracle for a supplied proper-width-three CNF.

    Each integer bit corresponds to one complete assignment. For every
    supplied clause, all eight possible polarity mutations are evaluated
    directly from the literal truth tables. Evaluation intersects clause
    truth tables, without decomposition into formula components.
    """

    def __init__(self, clauses: tuple[tuple[int, int, int], ...], audit: Audit) -> None:
        self.clauses = clauses
        self.audit = audit
        self.variable_count = max(abs(lit) for clause in clauses for lit in clause)
        self.assignment_count = 1 << self.variable_count
        self.all_assignments = (1 << self.assignment_count) - 1
        self.coordinate_count = 3 * len(clauses)
        literal_tables: dict[int, int] = {}
        for variable in range(1, self.variable_count + 1):
            half_period = 1 << (variable - 1)
            table = ((1 << half_period) - 1) << half_period
            filled_width = 2 * half_period
            while filled_width < self.assignment_count:
                table |= table << filled_width
                filled_width *= 2
            literal_tables[variable] = table
            literal_tables[-variable] = self.all_assignments ^ table
        self.clause_tables: tuple[tuple[int, ...], ...] = tuple(
            tuple(
                literal_tables[-clause[0] if polarity & 1 else clause[0]]
                | literal_tables[-clause[1] if polarity & 2 else clause[1]]
                | literal_tables[-clause[2] if polarity & 4 else clause[2]]
                for polarity in range(8)
            )
            for clause in clauses
        )

    def sat(self, flipped_coordinates: tuple[int, ...] = ()) -> bool:
        self.audit.bitset_oracle_calls += 1
        changed: dict[int, int] = {}
        for coordinate in flipped_coordinates:
            if not 0 <= coordinate < self.coordinate_count:
                raise ValueError("sign coordinate outside the formula")
            clause_index, literal_index = divmod(coordinate, 3)
            changed[clause_index] = changed.get(clause_index, 0) ^ (1 << literal_index)
        survivors = self.all_assignments
        for clause_index, tables in enumerate(self.clause_tables):
            survivors &= tables[changed.get(clause_index, 0)]
            if not survivors:
                return False
        return True


def scalar_sat(
    clauses: tuple[tuple[int, int, int], ...],
    flipped_coordinates: tuple[int, ...],
    audit: Audit,
) -> bool:
    """Independent direct scalar truth-table implementation."""
    audit.scalar_oracle_calls += 1
    toggled = set(flipped_coordinates)
    mutated = tuple(
        tuple(-literal if 3 * j + k in toggled else literal for k, literal in enumerate(clause))
        for j, clause in enumerate(clauses)
    )
    variables = max(abs(literal) for clause in mutated for literal in clause)
    for assignment in range(1 << variables):
        accepted = True
        for clause in mutated:
            clause_true = False
            for literal in clause:
                value = (assignment >> (abs(literal) - 1)) & 1
                if bool(value) == (literal > 0):
                    clause_true = True
                    break
            if not clause_true:
                accepted = False
                break
        if accepted:
            return True
    return False


def cross_check(oracle: TruthTableOracle, flips: tuple[int, ...], audit: Audit) -> None:
    audit.require(
        oracle.sat(flips) == scalar_sat(oracle.clauses, flips, audit),
        f"bitset/scalar oracle disagreement: flips={flips}",
    )


def sensitivity_stage(audit: Audit) -> dict:
    records: list[dict] = []
    sources = mutations = 0
    for n in (1, 2, 3):
        words = tuple(product((0, 1), repeat=n))
        local_sources = local_mutations = 0
        by_distance: dict[int, dict[str, int]] = {}
        for a in words:
            for b in words:
                sources += 1
                local_sources += 1
                distance = sum(x != y for x, y in zip(a, b))
                clauses = equality_formula(a, b)
                oracle = TruthTableOracle(clauses, audit)
                base = oracle.sat()
                audit.require(base == (distance == 0), f"equality label failed at {a}, {b}")
                audit.require(
                    all(len(set(abs(x) for x in clause)) == 3 for clause in clauses),
                    "formula is not proper width three",
                )
                sensitive: list[int] = []
                for coordinate in range(24 * n):
                    result = oracle.sat((coordinate,))
                    mutations += 1
                    local_mutations += 1
                    if result != base:
                        sensitive.append(coordinate)
                    if n == 1:
                        audit.require(
                            result == scalar_sat(clauses, (coordinate,), audit),
                            "n=1 single-edit scalar disagreement",
                        )
                expected = 24 if distance == 1 else 0
                audit.require(len(sensitive) == expected, f"sensitivity failed at {a}, {b}")
                if distance == 1:
                    component = next(i for i in range(n) if a[i] != b[i])
                    audit.require(
                        tuple(sensitive) == component_coordinates(n, component),
                        "sensitive coordinate support differs from the isolated conflict",
                    )
                if n <= 2:
                    cross_check(oracle, (), audit)
                group = by_distance.setdefault(distance, {"sources": 0, "sensitivity": expected})
                group["sources"] += 1
        records.append({
            "n": n,
            "source_pairs": local_sources,
            "single_sign_mutations": local_mutations,
            "grouped_by_hamming_distance": by_distance,
        })
    return {
        "source_pairs": sources,
        "single_sign_mutations": mutations,
        "records": records,
        "scope": "All ordered a,b pairs for n=1,2,3; every sign coordinate, including auxiliaries.",
    }


def sat_radius_stage(audit: Audit) -> dict:
    records: list[dict] = []
    variants = 0
    for bit in (0, 1):
        a = (bit,)
        oracle = TruthTableOracle(equality_formula(a, a), audit)
        expected_neighbors = set(central_quadruples(1))
        found: list[tuple[int, ...]] = []
        shells: list[dict] = []
        for radius in range(5):
            shell_count = sat_count = unsat_count = 0
            for flips in combinations(range(24), radius):
                result = oracle.sat(flips)
                variants += 1
                shell_count += 1
                sat_count += int(result)
                unsat_count += int(not result)
                if not result:
                    found.append(flips)
                    cross_check(oracle, flips, audit)
                if radius < 4:
                    audit.require(result, "SAT diagonal has an UNSAT neighbor at distance below four")
            audit.require(
                unsat_count == (2 if radius == 4 else 0),
                f"unexpected UNSAT count at n=1 radius {radius}",
            )
            shells.append({"radius": radius, "variants": shell_count, "sat": sat_count, "unsat": unsat_count})
        audit.require(set(found) == expected_neighbors, "nearest UNSAT neighbors differ from central quadruples")
        records.append({
            "n": 1,
            "a": list(a),
            "b": list(a),
            "minimum_opposite_label_distance": 4,
            "nearest_opposite_label_count": len(found),
            "nearest_sign_edit_sets": found,
            "shells": shells,
        })
    return {
        "variants": variants,
        "records": records,
        "scope": "Every sign subset through radius four for both n=1 SAT diagonals.",
    }


def unsat_shell_stage(audit: Audit) -> dict:
    # Includes nonconflicting spectator components, so the oracle tests that
    # nearest edits cannot be wasted outside the conflicting components.
    cases = (
        ((0,), (1,)),
        ((0, 1), (1, 0)),
        ((0, 1, 0), (1, 0, 1)),
        ((0, 1, 0), (1, 1, 0)),
        ((0, 1, 0), (1, 0, 0)),
    )
    records: list[dict] = []
    variants = 0
    for a, b in cases:
        n = len(a)
        distance = sum(x != y for x, y in zip(a, b))
        conflicts = tuple(i for i in range(n) if a[i] != b[i])
        supports = tuple(set(component_coordinates(n, i)) for i in conflicts)
        oracle = TruthTableOracle(equality_formula(a, b), audit)
        audit.require(not oracle.sat(), "shell source must be UNSAT")
        shells: list[dict] = []
        nearest_count = 0
        nearest_examples: list[tuple[int, ...]] = []
        for radius in range(distance + 1):
            sat_count = shell_count = 0
            for flips in combinations(range(24 * n), radius):
                result = oracle.sat(flips)
                variants += 1
                shell_count += 1
                sat_count += int(result)
                if radius < distance:
                    audit.require(not result, "UNSAT source repaired below conflict count")
                if result:
                    audit.require(
                        radius == distance and all(len(set(flips) & support) == 1 for support in supports),
                        "nearest SAT neighbor does not edit exactly one coordinate per conflict",
                    )
                    nearest_count += 1
                    if len(nearest_examples) < 3:
                        nearest_examples.append(flips)
            audit.require(
                sat_count == (24 ** distance if radius == distance else 0),
                f"incorrect nearest-shell count for n={n}, d={distance}, radius={radius}",
            )
            shells.append({"radius": radius, "variants": shell_count, "sat": sat_count, "unsat": shell_count - sat_count})
        for flips in nearest_examples[:1]:
            cross_check(oracle, flips, audit)
        records.append({
            "n": n,
            "a": list(a),
            "b": list(b),
            "conflicting_components": conflicts,
            "minimum_opposite_label_distance": distance,
            "nearest_opposite_label_count": nearest_count,
            "expected_nearest_count": 24 ** distance,
            "nearest_examples": nearest_examples,
            "shells": shells,
        })
    return {
        "variants": variants,
        "records": records,
        "scope": "Complete sign neighborhoods through the predicted minimum distance for d=1,2,3, including spectator cases.",
    }


def packing_stage(audit: Audit) -> dict:
    sources = sat_sources = unsat_sources = block_count = 0
    summaries: list[dict] = []
    for n in (1, 2, 3):
        words = tuple(product((0, 1), repeat=n))
        local_sat_blocks = local_unsat_blocks = 0
        examples: list[dict] = []
        for a in words:
            for b in words:
                sources += 1
                distance = sum(x != y for x, y in zip(a, b))
                oracle = TruthTableOracle(equality_formula(a, b), audit)
                base = oracle.sat()
                if distance == 0:
                    sat_sources += 1
                    blocks = central_quadruples(n)
                    expected = 2 * n
                    local_sat_blocks += len(blocks)
                else:
                    unsat_sources += 1
                    conflicts = tuple(i for i in range(n) if a[i] != b[i])
                    supports = tuple(component_coordinates(n, i) for i in conflicts)
                    blocks = tuple(tuple(support[j] for support in supports) for j in range(24))
                    expected = 24
                    local_unsat_blocks += len(blocks)
                audit.require(len(blocks) == expected, "incorrect packing cardinality")
                occupied: set[int] = set()
                for block in blocks:
                    audit.require(bool(block), "empty sensitive block")
                    audit.require(not occupied.intersection(block), "sensitive blocks overlap")
                    occupied.update(block)
                    audit.require(oracle.sat(block) != base, "packing contains a nonsensitive block")
                    block_count += 1
                if a == words[0] and (b == words[0] or b == words[-1]):
                    examples.append({"a": a, "b": b, "blocks": blocks})
        summaries.append({
            "n": n,
            "sat_packing_blocks": local_sat_blocks,
            "unsat_packing_blocks": local_unsat_blocks,
            "examples": examples,
        })
    return {
        "source_pairs": sources,
        "sat_sources": sat_sources,
        "unsat_sources": unsat_sources,
        "sensitive_blocks_checked": block_count,
        "records": summaries,
        "scope": "Explicit disjoint lower-bound packings for all a,b with n=1,2,3. Upper bounds are symbolic, not found by finite packing optimization.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("all", "sensitivity", "sat-radius", "unsat-shells", "packings"), default="all")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    audit = Audit()
    stages = {
        "sensitivity": sensitivity_stage,
        "sat-radius": sat_radius_stage,
        "unsat-shells": unsat_shell_stage,
        "packings": packing_stage,
    }
    selected = tuple(stages) if args.stage == "all" else (args.stage,)
    results = {stage: stages[stage](audit) for stage in selected}
    elapsed = time.perf_counter() - started
    output = args.output
    if output is None:
        output = DEFAULT_OUTPUT if args.stage == "all" else DEFAULT_OUTPUT.with_name(DEFAULT_OUTPUT.stem + "_" + args.stage + ".json")
    raw = {
        "run_id": RUN_ID,
        "scientific_status": "COMPUTATIONAL",
        "executed_at_pacific": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "code_path": str(Path(__file__).resolve().relative_to(REPO_ROOT)),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "stage": args.stage,
        "randomness": "None; deterministic exhaustive enumeration and explicit witness constructions.",
        "input_model": "E_n proper 3-CNF with 5n variables, 8n clauses, 24n sign coordinates, two banks and fresh gadget auxiliaries. Only literal-sign bits mutate; incidence and encoding grammar stay fixed.",
        "oracle": "Generic exact Boolean truth-table bitsets over all 2^(5n) assignments; selected cases checked by an independent scalar assignment enumerator. No use of equality or gadget semantics inside either SAT oracle.",
        "results": results,
        "totals": {
            "assertions": audit.assertions,
            "failed_assertions": 0,
            "bitset_oracle_calls": audit.bitset_oracle_calls,
            "scalar_oracle_calls": audit.scalar_oracle_calls,
            "elapsed_seconds": round(elapsed, 6),
        },
        "limits": [
            "Finite enumerations support only the stated n<=3 cases. General all-n claims require the separate symbolic proofs.",
            "Block packing construction proves finite lower-bound witnesses; maximality is a symbolic argument, not exhaustive block-packing search.",
            "Truth-table computation is an external exact oracle. It is not a physical TM trace or a runtime/space claim for a SAT solver.",
            "The audit does not establish or refute P=NP and does not exclude any general polynomial-time SAT decider.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "code_sha256": raw["code_sha256"], "stage": args.stage, **raw["totals"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
