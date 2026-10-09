#!/usr/bin/env python3
"""Bounded checks for RECOVERY-STRENGTHEN9.

The program checks finite semantics and exponent arithmetic only.  It is not
evidence for an all-input compiler or for a RAM/Turing-machine space bound.
Every execution is stopped after 25 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import runpy
import signal
import time
from fractions import Fraction
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def deadline(*_: object) -> None:
    raise TimeoutError("25-second RECOVERY-STRENGTHEN9 test budget exceeded")


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def restrict(formula: Formula, var: int, value: bool) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        if any(abs(lit) == var and (lit > 0) == value for lit in clause):
            continue
        residual = tuple(lit for lit in clause if abs(lit) != var)
        out.append(residual)
    return tuple(out)


def brute_sat(formula: Formula) -> bool:
    vs = variables(formula)
    for values in itertools.product((False, True), repeat=len(vs)):
        assignment = dict(zip(vs, values))
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula):
            return True
    return False


def krom_sat(formula: Formula) -> bool:
    """Independent implication-graph 2-SAT solver with units/empty clauses."""
    if any(not clause for clause in formula):
        return False
    if any(len(clause) > 2 for clause in formula):
        raise ValueError("not Krom")
    graph: dict[int, list[int]] = {}
    reverse: dict[int, list[int]] = {}
    for var in variables(formula):
        graph[var] = []
        graph[-var] = []
        reverse[var] = []
        reverse[-var] = []

    def edge(a: int, b: int) -> None:
        graph[a].append(b)
        reverse[b].append(a)

    for clause in formula:
        a = clause[0]
        b = clause[-1]
        edge(-a, b)
        edge(-b, a)

    seen: set[int] = set()
    order: list[int] = []

    def dfs1(node: int) -> None:
        seen.add(node)
        for nxt in graph[node]:
            if nxt not in seen:
                dfs1(nxt)
        order.append(node)

    for node in graph:
        if node not in seen:
            dfs1(node)
    component: dict[int, int] = {}

    def dfs2(node: int, label: int) -> None:
        component[node] = label
        for nxt in reverse[node]:
            if nxt not in component:
                dfs2(nxt, label)

    for label, node in enumerate(reversed(order)):
        if node not in component:
            dfs2(node, label)
    return all(component[var] != component[-var] for var in variables(formula))


def strong_krom_vars(formula: Formula) -> list[int]:
    return [
        var for var in variables(formula)
        if all(max((len(c) for c in restrict(formula, var, bit)), default=0) <= 2
               for bit in (False, True))
    ]


def full_width_clauses(n: int) -> tuple[Clause, ...]:
    out: list[Clause] = []
    for support in itertools.combinations(range(1, n + 1), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            out.append(tuple(sign * var for sign, var in zip(signs, support)))
    return tuple(out)


def strong_krom_exhaustion() -> dict[str, object]:
    checked = accepted = accepted_unsat = mismatches = 0
    corpora = [
        (4, range(1, 5)),
        (3, range(1, 9)),
    ]
    for n, sizes in corpora:
        clauses = full_width_clauses(n)
        for size in sizes:
            for formula in itertools.combinations(clauses, size):
                checked += 1
                candidates = strong_krom_vars(formula)
                if not candidates:
                    continue
                accepted += 1
                var = candidates[0]
                branch_answer = any(krom_sat(restrict(formula, var, bit))
                                    for bit in (False, True))
                truth = brute_sat(formula)
                accepted_unsat += int(not truth)
                mismatches += int(branch_answer != truth)
    assert checked == 41703
    assert accepted == 37607
    assert accepted_unsat == 1
    assert mismatches == 0
    return {
        "formulas_checked": checked,
        "singleton_strong_krom_accepted": accepted,
        "accepted_unsat_controls": accepted_unsat,
        "semantic_mismatches": mismatches,
    }


def connected(formula: Formula) -> bool:
    vs = variables(formula)
    if not vs:
        return True
    adjacency = {v: set() for v in vs}
    for clause in formula:
        support = {abs(lit) for lit in clause}
        for u in support:
            adjacency[u].update(support - {u})
    reached = {vs[0]}
    frontier = [vs[0]]
    while frontier:
        u = frontier.pop()
        for v in adjacency[u] - reached:
            reached.add(v)
            frontier.append(v)
    return reached == set(vs)


def solution_masks(formula: Formula) -> set[int]:
    vs = variables(formula)
    out: set[int] = set()
    for mask in range(1 << len(vs)):
        assignment = {v: bool(mask & (1 << i)) for i, v in enumerate(vs)}
        if all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula):
            out.add(mask)
    return out


def affine_solutions(formula: Formula) -> bool:
    sols = solution_masks(formula)
    return all((a ^ b ^ c) in sols for a in sols for b in sols for c in sols)


def hostile_control() -> dict[str, object]:
    formula: Formula = (
        (-1, -2, -3),
        (-1, -2, -4),
        (1, -3, -4),
        (2, 3, 4),
    )
    signs = {v: set() for v in variables(formula)}
    for clause in formula:
        for lit in clause:
            signs[abs(lit)].add(lit > 0)
    result = {
        "formula": formula,
        "satisfying_assignments": len(solution_masks(formula)),
        "sign_balanced": all(s == {False, True} for s in signs.values()),
        "connected": connected(formula),
        "horn": all(sum(lit > 0 for lit in c) <= 1 for c in formula),
        "dual_horn": all(sum(lit < 0 for lit in c) <= 1 for c in formula),
        "affine_solution_set": affine_solutions(formula),
        "singleton_strong_krom_vars": strong_krom_vars(formula),
    }
    assert result == {
        "formula": formula,
        "satisfying_assignments": 9,
        "sign_balanced": True,
        "connected": True,
        "horn": False,
        "dual_horn": False,
        "affine_solution_set": False,
        "singleton_strong_krom_vars": [],
    }
    return result


def marker_nonclosure() -> dict[str, object]:
    parser_path = Path("experiments/proof_spines/hereditary_marker_closure_test.py")
    parser = runpy.run_path(parser_path)
    parent = (
        parser["MAGIC"],
        parser["CUT_END"],
        parser["block_marker"](3, 3),
        (-3,),
    )
    result = parser["analyze_flat"](parent)
    assert result["status"] == "ANSWER"
    assert result["input_bits"] == 184
    assert result["cap_bits"] == 102
    assert result["children"] == [((-3,),)]
    child = result["children"][0]
    child_result = parser["analyze_flat"](child)
    assert parser["bits"](child) == 64
    assert child_result["status"] == "UNKNOWN"
    assert child_result["reason"] == "missing magic"
    return {
        "parent_bits": result["input_bits"],
        "cap_bits": result["cap_bits"],
        "child_bits": parser["bits"](child),
        "emitted_children": len(result["children"]),
        "successor_status": "UNKNOWN: missing magic",
        "encoding_minimality_scope": (
            "current flat grammar: one nonempty block needs MAGIC, CUT_END, "
            "one block marker, and one minimum-size data unit"
        ),
    }


def ledger_checks() -> dict[str, object]:
    r = Fraction(6, 5)
    v = Fraction(11, 10)
    h = Fraction(1, 2)
    p = Fraction(1, 2)
    recursive = (v - h) / (1 - h)
    C = max(Fraction(1), r, recursive)
    assert C == Fraction(6, 5)
    assert h * (C - 1) + v == C
    terminal_c = Fraction(1)
    terminal_w = Fraction(11, 10)
    terminal_g = Fraction(1, 2)
    terminal_time = terminal_w + terminal_g * (terminal_c - 1)
    assert terminal_time == Fraction(11, 10) < C
    sequential_peak = max(p, terminal_g)
    retained_batch_peak = terminal_w
    assert sequential_peak == Fraction(1, 2)
    assert retained_batch_peak == Fraction(11, 10) > sequential_peak

    packed = []
    for N in (16, 64, 256, 1024, 4096, 16384):
        maximum = int(N ** float(h))
        volume = N ** float(v)
        count = max(1, int(volume // maximum))
        remainder = max(0.0, volume - count * maximum)
        work = count * (maximum ** float(C))
        if remainder:
            work += min(remainder, maximum) ** float(C)
        packed.append({"N": N, "ratio": work / (N ** float(C))})
    assert all(0.97 <= row["ratio"] <= 1.000000000001 for row in packed)
    return {
        "r": str(r), "v": str(v), "h": str(h), "p": str(p),
        "recursive_fixed_point": str(recursive),
        "closed_time_exponent": str(C),
        "recurrence_identity": str(h * (C - 1) + v),
        "linear_terminal_time_exponent": str(terminal_time),
        "sequential_terminal_peak": str(sequential_peak),
        "retained_terminal_batch_peak": str(retained_batch_peak),
        "max_packed_ratios": packed,
    }


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL finite checks",
        "timeout_seconds": 25,
        "marker_nonclosure": marker_nonclosure(),
        "strong_krom": strong_krom_exhaustion(),
        "hostile_control": hostile_control(),
        "ledger": ledger_checks(),
        "limitations": [
            "Finite exhaustive tests do not prove all-input acquisition or coverage.",
            "The recurrence test validates accounting, not a constructor.",
            "Python storage is not a same-machine sublinear-space proof.",
        ],
    }
    result["seconds"] = time.perf_counter() - started
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name(
        "2026-10-09_0146_RECOVERY-STRENGTHEN9-results.json"
    )
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
