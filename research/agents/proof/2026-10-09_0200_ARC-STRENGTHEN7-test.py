#!/usr/bin/env python3
"""Bounded checks for ARC-STRENGTHEN7.

Finite exhaustive semantics and explicit-family accounting only.  This does
not prove all-input coverage or a random-access machine workspace theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import signal
import time
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def deadline(*_: object) -> None:
    raise TimeoutError("25-second ARC-STRENGTHEN7 budget exceeded")


def uleb(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def zigzag(lit: int) -> int:
    return 2 * abs(lit) - (1 if lit > 0 else 0)


def encode_cnf(formula: Formula) -> bytes:
    out = bytearray(b"CNF1")
    out += uleb(max((abs(x) for c in formula for x in c), default=0))
    out += uleb(len(formula))
    for clause in formula:
        out += uleb(len(clause))
        for lit in clause:
            out += uleb(zigzag(lit))
    return bytes(out)


def bits(formula: Formula) -> int:
    return 8 * len(encode_cnf(formula))


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(x) for c in formula for x in c}))


def restrict(formula: Formula, var: int, value: bool) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        if any(abs(lit) == var and (lit > 0) == value for lit in clause):
            continue
        out.append(tuple(lit for lit in clause if abs(lit) != var))
    return tuple(out)


def is_horn(formula: Formula) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in formula)


def is_dual_horn(formula: Formula) -> bool:
    return all(sum(lit < 0 for lit in clause) <= 1 for clause in formula)


def horn_sat(formula: Formula) -> bool:
    """Forward-chaining Horn-SAT, independent of brute-force truth tables."""
    if not is_horn(formula):
        raise ValueError("not Horn")
    rules: list[tuple[frozenset[int], int | None]] = []
    for clause in formula:
        if not clause:
            return False
        head = next((lit for lit in clause if lit > 0), None)
        body = frozenset(-lit for lit in clause if lit < 0)
        rules.append((body, head))
    true: set[int] = set()
    changed = True
    while changed:
        changed = False
        for body, head in rules:
            if body <= true:
                if head is None:
                    return False
                if head not in true:
                    true.add(head)
                    changed = True
    return True


def dual_horn_sat(formula: Formula) -> bool:
    return horn_sat(tuple(tuple(-lit for lit in clause) for clause in formula))


def brute_sat(formula: Formula) -> bool:
    vs = variables(formula)
    for vals in itertools.product((False, True), repeat=len(vs)):
        a = dict(zip(vs, vals))
        if all(any(a[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula):
            return True
    return False


def strong_horn_vars_brute(formula: Formula) -> list[int]:
    return [v for v in variables(formula)
            if all(is_horn(restrict(formula, v, b)) for b in (False, True))]


def strong_dual_vars_brute(formula: Formula) -> list[int]:
    return [v for v in variables(formula)
            if all(is_dual_horn(restrict(formula, v, b)) for b in (False, True))]


def strong_horn_vars_scan(formula: Formula) -> list[int]:
    bad = next((c for c in formula if sum(x > 0 for x in c) >= 2), None)
    if bad is None:
        return list(variables(formula))
    candidates = [x for x in bad if x > 0]
    if len(candidates) >= 3:
        return []
    return [x for x in candidates if all(
        sum(lit > 0 for lit in c) <= 1 or
        (sum(lit > 0 for lit in c) == 2 and x in c)
        for c in formula)]


def strong_dual_vars_scan(formula: Formula) -> list[int]:
    negated = tuple(tuple(-lit for lit in clause) for clause in formula)
    return strong_horn_vars_scan(negated)


def strong_krom_vars(formula: Formula) -> list[int]:
    return [v for v in variables(formula)
            if all(max((len(c) for c in restrict(formula, v, b)), default=0) <= 2
                   for b in (False, True))]


def full_width_clauses(n: int) -> tuple[Clause, ...]:
    return tuple(
        tuple(sign * var for sign, var in zip(signs, support))
        for support in itertools.combinations(range(1, n + 1), 3)
        for signs in itertools.product((-1, 1), repeat=3)
    )


def proper_clauses(n: int) -> tuple[Clause, ...]:
    """All nonempty, non-tautological clauses of width at most n."""
    out: list[Clause] = []
    for states in itertools.product((-1, 0, 1), repeat=n):
        clause = tuple(sign * (i + 1) for i, sign in enumerate(states) if sign)
        if clause:
            out.append(clause)
    return tuple(out)


def satisfies(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
               for clause in formula)


def extreme1_witness(formula: Formula) -> dict[int, bool] | None:
    """Find a model within Hamming distance one of an extreme assignment.

    The first clause falsified by an extreme assignment has width at most
    three, so it supplies every possible one-flip repair candidate.  This is
    the source-level constant-candidate rule used by the promoted terminal.
    """
    vs = variables(formula)
    for base in (False, True):
        assignment = {v: base for v in vs}
        if satisfies(formula, assignment):
            return assignment
        first_bad = next(c for c in formula if not any(
            assignment[abs(lit)] == (lit > 0) for lit in c
        ))
        for lit in first_bad:
            candidate = dict(assignment)
            candidate[abs(lit)] = not base
            if satisfies(formula, candidate):
                return candidate
    return None


def components(formula: Formula) -> list[Formula]:
    if not formula:
        return []
    clause_vars = [{abs(x) for x in c} for c in formula]
    remaining = set(range(len(formula)))
    out: list[Formula] = []
    while remaining:
        seed = remaining.pop()
        indices = {seed}
        support = set(clause_vars[seed])
        changed = True
        while changed:
            changed = False
            for j in tuple(remaining):
                if support & clause_vars[j]:
                    remaining.remove(j)
                    indices.add(j)
                    support |= clause_vars[j]
                    changed = True
        out.append(tuple(formula[j] for j in sorted(indices)))
    return out


def dp_eliminate(formula: Formula, var: int) -> tuple[Formula, int]:
    pos = [c for c in formula if var in c]
    neg = [c for c in formula if -var in c]
    keep = [c for c in formula if var not in c and -var not in c]
    raw_pairs = len(pos) * len(neg)
    resolvents: set[Clause] = set()
    for a in pos:
        for b in neg:
            lits = set(a) | set(b)
            lits.discard(var)
            lits.discard(-var)
            if any(-lit in lits for lit in lits):
                continue
            resolvents.add(tuple(sorted(lits, key=lambda z: (abs(z), z < 0))))
    return tuple(dict.fromkeys(keep + sorted(resolvents))), raw_pairs


def strict_family(k: int) -> Formula:
    """Connected family accepted by singleton dual-Horn, not old easy guards."""
    x = 1
    clauses: list[Clause] = []
    nxt = 2
    for _ in range(k):
        a, b, c = range(nxt, nxt + 3)
        nxt += 3
        clauses.extend([
            (a, b, c),
            (x, -a, b),
            (-x, -b, c),
            (-c, a, b),
        ])
    return tuple(clauses)


def exhaustive_semantics() -> dict[str, int]:
    clauses = full_width_clauses(4)
    checked = horn_accept = dual_accept = mismatches = 0
    for m in range(1, 5):
        for formula in itertools.combinations(clauses, m):
            checked += 1
            hs = strong_horn_vars_scan(formula)
            ds = strong_dual_vars_scan(formula)
            hb = strong_horn_vars_brute(formula)
            db = strong_dual_vars_brute(formula)
            mismatches += int(hs != hb) + int(ds != db)
            truth = brute_sat(formula)
            if hs and not is_horn(formula):
                horn_accept += 1
                x = hs[0]
                answer = any(horn_sat(restrict(formula, x, b)) for b in (False, True))
                mismatches += int(answer != truth)
            if ds and not is_dual_horn(formula):
                dual_accept += 1
                x = ds[0]
                answer = any(dual_horn_sat(restrict(formula, x, b)) for b in (False, True))
                mismatches += int(answer != truth)
    assert checked == 41448 and mismatches == 0
    return {
        "formulas_checked": checked,
        "nontrivial_strong_horn_accepts": horn_accept,
        "nontrivial_strong_dual_accepts": dual_accept,
        "structural_or_semantic_mismatches": mismatches,
    }


def mixed_width_semantics() -> dict[str, int]:
    clauses = proper_clauses(3)
    checked = scan_mismatches = semantic_mismatches = extreme_accepts = 0
    for m in range(0, 5):
        for formula in itertools.combinations(clauses, m):
            checked += 1
            scan_mismatches += int(
                strong_horn_vars_scan(formula) != strong_horn_vars_brute(formula)
            )
            scan_mismatches += int(
                strong_dual_vars_scan(formula) != strong_dual_vars_brute(formula)
            )
            witness = extreme1_witness(formula)
            if witness is not None:
                extreme_accepts += 1
                semantic_mismatches += int(not satisfies(formula, witness))
                semantic_mismatches += int(not brute_sat(formula))
    assert checked == 17902
    assert scan_mismatches == 0 and semantic_mismatches == 0
    return {
        "formulas_checked_including_empty_formula": checked,
        "strong_backdoor_scan_mismatches": scan_mismatches,
        "extreme1_accepts": extreme_accepts,
        "extreme1_semantic_mismatches": semantic_mismatches,
    }


def family_audit() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for k in (2, 4, 8, 16, 32, 64):
        formula = strict_family(k)
        n = bits(formula)
        cap = math.floor(math.sqrt(n) * math.log2(n + 2))
        signs = {v: set() for v in variables(formula)}
        for clause in formula:
            for lit in clause:
                signs[abs(lit)].add(lit > 0)
        dvars = strong_dual_vars_scan(formula)
        assert 1 in dvars
        assert not strong_krom_vars(formula)
        assert not strong_horn_vars_scan(formula)
        assert not is_horn(formula) and not is_dual_horn(formula)
        assert all(s == {False, True} for s in signs.values())
        witness = extreme1_witness(formula)
        assert witness is not None and satisfies(formula, witness)
        branch_components = [components(restrict(formula, 1, b)) for b in (False, True)]
        max_terminal = max(bits(c) for branch in branch_components for c in branch)
        assert max_terminal <= cap
        branch_answers = [all(dual_horn_sat(c) for c in branch)
                          for branch in branch_components]
        pivot_x, pairs_x = dp_eliminate(formula, 1)
        local_var = 2
        pivot_local, pairs_local = dp_eliminate(formula, local_var)
        largest_x = max((bits(c) for c in components(pivot_x)), default=0)
        largest_local = max((bits(c) for c in components(pivot_local)), default=0)
        rows.append({
            "k": k,
            "input_bits": n,
            "cap_bits": cap,
            "maximum_terminal_component_bits": max_terminal,
            "terminal_components_b0": len(branch_components[0]),
            "terminal_components_b1": len(branch_components[1]),
            "branch_answers": branch_answers,
            "extreme1_witness_found": witness is not None,
            "pivot_x_raw_pairs": pairs_x,
            "pivot_x_largest_component_bits": largest_x,
            "pivot_local_raw_pairs": pairs_local,
            "pivot_local_largest_component_bits": largest_local,
            "pivot_x_exceeds_cap": largest_x > cap,
            "pivot_local_exceeds_cap": largest_local > cap,
        })
    assert all(row["pivot_x_exceeds_cap"] for row in rows)
    assert all(row["pivot_local_exceeds_cap"] for row in rows)
    return rows


def hostile_control() -> dict[str, object]:
    formula: Formula = (
        (-1, -2, -3),
        (-1, -2, -4),
        (1, -3, -4),
        (2, 3, 4),
    )
    return {
        "formula": formula,
        "sat": brute_sat(formula),
        "strong_horn": strong_horn_vars_scan(formula),
        "strong_dual_horn": strong_dual_vars_scan(formula),
        "strong_krom": strong_krom_vars(formula),
        "extreme1_accepts": extreme1_witness(formula) is not None,
    }


def residual_edge_controls() -> dict[str, object]:
    formula: Formula = ((1,), (-1,), (1, 2))
    residuals = [restrict(formula, 1, b) for b in (False, True)]
    duplicate_source: Formula = ((1, 2), (2,))
    duplicate_residual = restrict(duplicate_source, 1, False)
    return {
        "empty_clause_source": formula,
        "residuals": residuals,
        "both_residuals_contain_empty_clause": all(tuple() in r for r in residuals),
        "duplicate_source": duplicate_source,
        "duplicate_residual_raw_multiset": duplicate_residual,
        "duplicate_residual_has_two_copies": duplicate_residual.count((2,)) == 2,
    }


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL finite checks",
        "timeout_seconds": 25,
        "exhaustive": exhaustive_semantics(),
        "mixed_width_exhaustive": mixed_width_semantics(),
        "strict_family": family_audit(),
        "hostile_control": hostile_control(),
        "residual_edge_controls": residual_edge_controls(),
        "empty_formula_sat": horn_sat(tuple()),
        "empty_clause_unsat": horn_sat((tuple(),)),
        "limitations": [
            "Finite tests do not prove all-input coverage or asymptotic resource bounds.",
            "The strict-family proof, not the sampled rows, establishes asymptotic PIVOT failure.",
            "Python allocation is not evidence for random-access-machine workspace.",
            "components() intentionally uses linear derived state; its rows are not a workspace certificate.",
            "The promoted EXTREME-1 rule uses only constant many source scans and O(log N) pointers.",
        ],
    }
    assert result["hostile_control"]["strong_horn"] == []
    assert result["hostile_control"]["strong_dual_horn"] == []
    assert result["hostile_control"]["strong_krom"] == []
    assert result["residual_edge_controls"]["both_residuals_contain_empty_clause"]
    assert result["residual_edge_controls"]["duplicate_residual_has_two_copies"]
    result["seconds"] = time.perf_counter() - started
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name(
        "2026-10-09_0200_ARC-STRENGTHEN7-results.json"
    )
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
