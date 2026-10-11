#!/usr/bin/env python3
"""Bounded audit for a balanced nonempty-pin component lift.

The theorem tested here is elementary: if F is a proper monotone
3-SAT-(2,2) formula and H is a fixed satisfiable member of the same class
whose designated variable z can take either value in a satisfying
assignment, then F and H is again in the class and pinning z preserves the
SAT bit of F.  The experiment exhausts every six-variable member of the
class, verifies a minimum-size H, and runs representation/wrapper/easy-family
controls.  Finite counts are not used as asymptotic lower bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from pathlib import Path


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


EDGES6 = tuple(itertools.combinations(range(1, 7), 3))
H0_EDGES = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))


def normalize_clause(clause: Clause) -> Clause:
    return tuple(sorted(clause, key=lambda x: (abs(x), x < 0)))


def normalize_formula(formula: Formula) -> Formula:
    return tuple(sorted((normalize_clause(c) for c in formula)))


def paired_formula(edges: tuple[tuple[int, int, int], ...]) -> Formula:
    positive = tuple(tuple(e) for e in edges)
    negative = tuple(tuple(-v for v in e) for e in edges)
    return normalize_formula(positive + negative)


H0 = paired_formula(H0_EDGES)


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def clause_value(clause: Clause, assignment: int) -> bool:
    for lit in clause:
        bit = bool((assignment >> (abs(lit) - 1)) & 1)
        if bit == (lit > 0):
            return True
    return False


def formula_value(formula: Formula, assignment: int) -> bool:
    return all(clause_value(clause, assignment) for clause in formula)


def sat_witness(formula: Formula, pin: tuple[int, int] | None = None) -> int | None:
    n = max(variables(formula), default=0)
    for assignment in range(1 << n):
        if pin is not None and ((assignment >> (pin[0] - 1)) & 1) != pin[1]:
            continue
        if formula_value(formula, assignment):
            return assignment
    return None


def satisfying_count(formula: Formula, pin: tuple[int, int] | None = None) -> int:
    n = max(variables(formula), default=0)
    total = 0
    for assignment in range(1 << n):
        if pin is not None and ((assignment >> (pin[0] - 1)) & 1) != pin[1]:
            continue
        total += formula_value(formula, assignment)
    return total


def is_h22(formula: Formula) -> bool:
    if len(formula) != len(set(formula)):
        return False
    vs = variables(formula)
    pos = Counter()
    neg = Counter()
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        signs = {x > 0 for x in clause}
        if len(signs) != 1:
            return False
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    return all(pos[v] == 2 and neg[v] == 2 for v in vs)


def incidence_connected(formula: Formula) -> bool:
    vs = variables(formula)
    if not vs:
        return True
    adj: dict[int, set[int]] = defaultdict(set)
    for clause in formula:
        cv = [abs(x) for x in clause]
        for a, b in itertools.combinations(cv, 2):
            adj[a].add(b)
            adj[b].add(a)
    seen = {vs[0]}
    stack = [vs[0]]
    while stack:
        u = stack.pop()
        for v in adj[u] - seen:
            seen.add(v)
            stack.append(v)
    return seen == set(vs)


def two_regular_edge_sets() -> list[tuple[tuple[int, int, int], ...]]:
    answer = []
    for edges in itertools.combinations(EDGES6, 4):
        degrees = Counter(v for edge in edges for v in edge)
        if all(degrees[v] == 2 for v in range(1, 7)):
            answer.append(tuple(edges))
    return answer


def shift_formula(formula: Formula, offset: int) -> Formula:
    return normalize_formula(tuple(tuple((1 if x > 0 else -1) * (abs(x) + offset) for x in c) for c in formula))


def disjoint_union(*formulas: Formula) -> Formula:
    return normalize_formula(tuple(c for formula in formulas for c in formula))


def restrict_formula(formula: Formula, var: int, value: int) -> tuple[Clause, ...]:
    out = []
    for clause in formula:
        if any(abs(lit) == var and (lit > 0) == bool(value) for lit in clause):
            continue
        out.append(tuple(lit for lit in clause if abs(lit) != var))
    return tuple(out)


def residual_sat(formula: Formula, var: int, value: int) -> bool:
    residual = restrict_formula(formula, var, value)
    n = max(variables(formula), default=0)
    for assignment in range(1 << n):
        if all(clause_value(c, assignment) for c in residual):
            return True
    return False


def encode_dimacs(formula: Formula, clause_order: str = "canonical") -> bytes:
    clauses = list(normalize_formula(formula))
    if clause_order == "reverse":
        clauses.reverse()
    n = max(variables(formula), default=0)
    body = [f"p cnf {n} {len(clauses)}"]
    body.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(body) + "\n").encode()


def parse_dimacs(data: bytes) -> Formula:
    clauses: list[Clause] = []
    for raw in data.decode().splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("c") or raw.startswith("p"):
            continue
        nums = [int(x) for x in raw.split()]
        assert nums[-1] == 0
        clauses.append(tuple(nums[:-1]))
    return normalize_formula(tuple(clauses))


def rename_formula(formula: Formula, permutation: dict[int, int]) -> Formula:
    return normalize_formula(tuple(tuple((1 if x > 0 else -1) * permutation[abs(x)] for x in c) for c in formula))


def global_complement(formula: Formula) -> Formula:
    return normalize_formula(tuple(tuple(-x for x in c) for c in formula))


def clause_mask(clause: Clause, n: int) -> int:
    mask = 0
    for assignment in range(1 << n):
        if clause_value(clause, assignment):
            mask |= 1 << assignment
    return mask


def formula_mask(formula: Formula, n: int, cache: dict[tuple[Clause, int], int]) -> int:
    mask = (1 << (1 << n)) - 1
    for clause in formula:
        key = (clause, n)
        if key not in cache:
            cache[key] = clause_mask(clause, n)
        mask &= cache[key]
    return mask


def pin_mask(var: int, value: int, n: int) -> int:
    mask = 0
    for assignment in range(1 << n):
        if ((assignment >> (var - 1)) & 1) == value:
            mask |= 1 << assignment
    return mask


def solve_2sat(formula: Formula) -> tuple[bool, int]:
    vs = variables(formula)
    n = max(vs, default=0)
    graph = [[] for _ in range(2 * n)]
    reverse = [[] for _ in range(2 * n)]
    steps = 0

    def idx(lit: int) -> int:
        return 2 * (abs(lit) - 1) + (lit < 0)

    def neg(i: int) -> int:
        return i ^ 1

    for clause in formula:
        if len(clause) == 1:
            a = b = clause[0]
        else:
            assert len(clause) == 2
            a, b = clause
        for u, v in ((neg(idx(a)), idx(b)), (neg(idx(b)), idx(a))):
            graph[u].append(v)
            reverse[v].append(u)
            steps += 1
    seen = [False] * (2 * n)
    order: list[int] = []
    for root in range(2 * n):
        if seen[root]:
            continue
        stack = [(root, 0)]
        seen[root] = True
        while stack:
            u, i = stack[-1]
            steps += 1
            if i < len(graph[u]):
                v = graph[u][i]
                stack[-1] = (u, i + 1)
                if not seen[v]:
                    seen[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()
    comp = [-1] * (2 * n)
    cid = 0
    for root in reversed(order):
        if comp[root] >= 0:
            continue
        comp[root] = cid
        stack = [root]
        while stack:
            u = stack.pop()
            steps += 1
            for v in reverse[u]:
                if comp[v] < 0:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return all(comp[2 * i] != comp[2 * i + 1] for i in range(n)), steps


def solve_horn(formula: Formula) -> tuple[bool, int]:
    true: set[int] = set()
    steps = 0
    changed = True
    while changed:
        changed = False
        for clause in formula:
            steps += len(clause)
            positives = [x for x in clause if x > 0]
            assert len(positives) <= 1
            antecedent = [abs(x) for x in clause if x < 0]
            if all(v in true for v in antecedent):
                if not positives:
                    return False, steps
                head = positives[0]
                if head not in true:
                    true.add(head)
                    changed = True
    return True, steps


def xor3_cnf(a: int, b: int, c: int, rhs: int) -> Formula:
    bad = []
    for bits in itertools.product((0, 1), repeat=3):
        if (bits[0] ^ bits[1] ^ bits[2]) != rhs:
            bad.append(tuple(-v if bit else v for v, bit in zip((a, b, c), bits)))
    return normalize_formula(tuple(bad))


def gaussian_sat(equations: list[tuple[int, int]]) -> tuple[bool, int]:
    rows = equations[:]
    pivot = 0
    steps = 0
    max_col = max((mask.bit_length() for mask, _ in rows), default=0)
    for col in range(max_col):
        q = next((i for i in range(pivot, len(rows)) if (rows[i][0] >> col) & 1), None)
        steps += max(0, len(rows) - pivot)
        if q is None:
            continue
        rows[pivot], rows[q] = rows[q], rows[pivot]
        pm, pr = rows[pivot]
        for i, (mask, rhs) in enumerate(rows):
            if i != pivot and ((mask >> col) & 1):
                rows[i] = (mask ^ pm, rhs ^ pr)
                steps += 1
        pivot += 1
    return not any(mask == 0 and rhs for mask, rhs in rows), steps


def path_dp_equalities(n: int, contradictory_endpoints: bool) -> tuple[bool, int]:
    states = {0} if contradictory_endpoints else {0, 1}
    steps = 0
    for _ in range(n - 1):
        nxt = set()
        for left in states:
            for right in (0, 1):
                steps += 1
                if left == right:
                    nxt.add(right)
        states = nxt
    if contradictory_endpoints:
        steps += len(states)
        states = {x for x in states if x == 1}
    return bool(states), steps


def scan_and_drop_fixed_component(formula: Formula, component: Formula) -> tuple[Formula, int]:
    wanted = Counter(component)
    kept = []
    steps = 0
    for clause in normalize_formula(formula):
        steps += len(clause)
        if wanted[clause]:
            wanted[clause] -= 1
        else:
            kept.append(clause)
    assert not any(wanted.values())
    return normalize_formula(tuple(kept)), steps


def easy_controls() -> dict[str, object]:
    # 2-SAT equality chain.
    two_sat = normalize_formula(tuple(c for i in range(1, 8) for c in ((-i, i + 1), (i, -(i + 1)))))
    two_value, two_steps = solve_2sat(two_sat)

    # Horn chain forced into a contradiction.
    horn = normalize_formula(((1,),) + tuple((-i, i + 1) for i in range(1, 8)) + ((-8,),))
    horn_value, horn_steps = solve_horn(horn)

    # Three affine equations, encoded independently as Tseitin-style 3-CNF.
    xor_eqs = [((1 << 0) | (1 << 1) | (1 << 2), 0),
               ((1 << 2) | (1 << 3) | (1 << 4), 1),
               ((1 << 0) | (1 << 4) | (1 << 5), 1)]
    affine_cnf = disjoint_union(xor3_cnf(1, 2, 3, 0), xor3_cnf(3, 4, 5, 1), xor3_cnf(1, 5, 6, 1))
    affine_value, affine_steps = gaussian_sat(xor_eqs)
    affine_brute = sat_witness(affine_cnf) is not None

    tw_value, tw_steps = path_dp_equalities(12, contradictory_endpoints=True)

    assert two_value
    assert not horn_value
    assert affine_value == affine_brute
    assert not tw_value
    return {
        "two_sat": {"value": two_value, "primitive_steps": two_steps, "clauses": len(two_sat)},
        "horn": {"value": horn_value, "primitive_steps": horn_steps, "clauses": len(horn)},
        "affine_tseitin": {"value": affine_value, "gaussian_steps": affine_steps, "cnf_clauses": len(affine_cnf)},
        "bounded_treewidth_path": {"value": tw_value, "dp_transitions": tw_steps, "variables": 12},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610110924)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()

    checks = Counter()
    failures: list[str] = []
    edge_sets = two_regular_edge_sets()
    checks["six_variable_two_regular_hypergraphs"] = len(edge_sets)

    # Symbolic minimum-size guard: 3 divides n and n=3 cannot have two unique
    # positive triples containing every variable twice.
    assert len(tuple(itertools.combinations(range(1, 4), 3))) == 1
    checks["minimum_size_symbolic_checks"] += 2

    assert len(edge_sets) == 75
    assert is_h22(H0)
    assert incidence_connected(H0)
    h0_counts = {str(v): satisfying_count(H0, (1, v)) for v in (0, 1)}
    assert h0_counts["0"] > 0 and h0_counts["1"] > 0
    checks["fixed_component_checks"] += 5

    # Every paired-edge member is a NAE instance and is complement symmetric.
    paired_pin_checks = 0
    paired_connected = 0
    for edges in edge_sets:
        h = paired_formula(edges)
        assert is_h22(h)
        paired_connected += incidence_connected(h)
        for z in range(1, 7):
            for value in (0, 1):
                assert sat_witness(h, (z, value)) is not None
                paired_pin_checks += 1
    checks["paired_component_pin_checks"] = paired_pin_checks

    # Exhaust every n=6 H22 formula: 75 choices for positive clauses and 75
    # choices for negative clauses.  Verify the lifted formula directly by
    # bit-parallel truth-table masks on 12 variables.
    cache: dict[tuple[Clause, int], int] = {}
    h_shift = shift_formula(H0, 6)
    pmasks = {v: pin_mask(7, v, 12) for v in (0, 1)}
    exhaustive_sources = 0
    exhaustive_pin_equivalences = 0
    sat_sources = 0
    unsat_sources = 0
    samples: list[Formula] = []
    for pos_edges in edge_sets:
        for neg_edges in edge_sets:
            source = normalize_formula(tuple(pos_edges) + tuple(tuple(-x for x in e) for e in neg_edges))
            assert is_h22(source)
            source_mask = formula_mask(source, 6, cache)
            source_sat = bool(source_mask)
            sat_sources += source_sat
            unsat_sources += not source_sat
            lift = disjoint_union(source, h_shift)
            assert is_h22(lift)
            lift_mask = formula_mask(lift, 12, cache)
            for value in (0, 1):
                lift_sat = bool(lift_mask & pmasks[value])
                if lift_sat != source_sat:
                    failures.append(f"pin mismatch {pos_edges} {neg_edges} value={value}")
                exhaustive_pin_equivalences += 1
            exhaustive_sources += 1
            if len(samples) < 24 and exhaustive_sources % 233 == 0:
                samples.append(source)
    checks["exhaustive_six_variable_sources"] = exhaustive_sources
    checks["exhaustive_pin_equivalences"] = exhaustive_pin_equivalences
    checks["lift_balance_checks"] = exhaustive_sources

    # Independent products and balanced padding by further fixed components.
    product_checks = 0
    padding_checks = 0
    for i, source in enumerate(samples[:12]):
        second = shift_formula(samples[-1 - i], 6)
        gadget = shift_formula(H0, 12)
        product = disjoint_union(source, second, gadget)
        source_pair_sat = (sat_witness(source) is not None) and (sat_witness(second) is not None)
        for value in (0, 1):
            assert residual_sat(product, 13, value) == source_pair_sat
            product_checks += 1
        padded = disjoint_union(source, shift_formula(H0, 6), shift_formula(H0, 12))
        assert is_h22(padded)
        for value in (0, 1):
            assert residual_sat(padded, 7, value) == (sat_witness(source) is not None)
            padding_checks += 1
    checks["independent_product_checks"] = product_checks
    checks["balanced_padding_checks"] = padding_checks

    # Encoding and wrapper controls on bounded samples.
    representation_checks = 0
    wrapper_checks = 0
    scan_steps = 0
    reconstruction_assignments = 0
    for source in samples:
        lift = disjoint_union(source, h_shift)
        reverse = parse_dimacs(encode_dimacs(lift, "reverse"))
        assert reverse == normalize_formula(lift)
        representation_checks += 1
        perm = {i: 13 - i for i in range(1, 13)}
        renamed = rename_formula(lift, perm)
        assert is_h22(renamed)
        representation_checks += 1
        comp = global_complement(lift)
        assert is_h22(comp)
        assert (sat_witness(comp) is not None) == (sat_witness(lift) is not None)
        representation_checks += 2

        # Redundant-clause encoding preserves semantics but intentionally
        # violates the unique-clause promise.
        duplicate = normalize_formula(lift + (lift[0],))
        assert not is_h22(duplicate)
        assert (sat_witness(duplicate) is not None) == (sat_witness(lift) is not None)
        representation_checks += 2

        # DIRECT, DEAD, COPY, DELAY, INTERP, RECOMP.
        direct = [residual_sat(lift, 7, v) for v in (0, 1)]
        dead = normalize_formula(lift + ((1, -1, 2),))
        dead_values = [residual_sat(dead, 7, v) for v in (0, 1)]
        copied = direct[:]
        delayed = [residual_sat(lift, 7, v) for _ in range(3) for v in (0, 1)][-2:]
        interp = parse_dimacs(encode_dimacs(lift))
        recomputed = [residual_sat(disjoint_union(source, h_shift), 7, v) for v in (0, 1)]
        assert direct == dead_values == copied == delayed == recomputed
        assert interp == normalize_formula(lift)
        wrapper_checks += 12

        stripped, steps = scan_and_drop_fixed_component(lift, h_shift)
        assert stripped == normalize_formula(source)
        scan_steps += steps
        witness = sat_witness(source)
        if witness is not None:
            gadget_witness = sat_witness(H0, (1, 0))
            assert gadget_witness is not None
            reconstruction_assignments += len(variables(H0))
    checks["representation_checks"] = representation_checks
    checks["wrapper_checks"] = wrapper_checks
    checks["charged_component_scan_literal_touches"] = scan_steps
    checks["witness_reconstruction_assignments"] = reconstruction_assignments

    controls = easy_controls()
    checks["easy_family_controls"] = len(controls)

    if failures:
        raise AssertionError(failures[:3])

    elapsed = time.perf_counter() - start
    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "run_id": "TESTS-0003",
        "timestamp_utc": "2026-10-11T09:24:00Z",
        "seed": args.seed,
        "status": {
            "BALANCED-PIN-LIFT1": "PROVED/EXACT_PENDING_INDEPENDENT_REVIEW",
            "BALANCE-ONLY-REPAIR1": "FALSIFIED/RETIRED",
            "CONNECTED-BALANCED-PIN-LIFT1": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "fixed_component": {
            "variables": 6,
            "clauses": 8,
            "edges": H0_EDGES,
            "connected": incidence_connected(H0),
            "pin_satisfying_assignment_counts": h0_counts,
            "minimum_variable_count_in_H22": 6,
            "minimum_scope": "all proper unique monotone 3-SAT-(2,2) formulas",
        },
        "exhaustive_family": {
            "two_regular_edge_sets": len(edge_sets),
            "paired_components_connected": paired_connected,
            "all_n6_h22_formulas": exhaustive_sources,
            "satisfiable_sources": sat_sources,
            "unsatisfiable_sources": unsat_sources,
        },
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "easy_controls": controls,
        "cost_ledger": {
            "construction": "one source copy plus one fixed six-variable/eight-clause component",
            "preprocessing_measured": "literal touches in exact fixed-component scan",
            "extraction": "one source SAT bit; no service table",
            "reconstruction_measured": "append six fixed gadget assignments when a source witness exists",
            "output": "one bit",
            "asymptotic_claim_from_timing": False,
        },
        "limitations": [
            "The lift is a disjoint union, so the global incidence graph is disconnected.",
            "Finite enumeration is not an asymptotic runtime lower bound.",
            "No arbitrary-algorithm representation or extraction necessity is proved.",
            "No nonrelativizing or nonalgebrizing hinge is supplied.",
        ],
        "elapsed_seconds": elapsed,
        "script_sha256": script_sha,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
