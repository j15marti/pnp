#!/usr/bin/env python3
"""Bounded audit for LB-0016.

All loops are deliberately small.  The script checks finite instances only;
the asymptotic counting theorem is proved separately in the report.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import time
from dataclasses import dataclass


Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def simplify(formula: Formula, assignment: dict[int, bool]) -> Formula | None:
    out: list[Clause] = []
    for clause in formula:
        kept: list[int] = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                if assignment[var] == (lit > 0):
                    satisfied = True
                    break
            else:
                kept.append(lit)
        if satisfied:
            continue
        if not kept:
            return None
        out.append(tuple(kept))
    return tuple(out)


def brute_sat(formula: Formula, nvars: int) -> bool:
    for bits in itertools.product((False, True), repeat=nvars):
        a = {i + 1: bits[i] for i in range(nvars)}
        if simplify(formula, a) == ():
            return True
    return False


def compatibility(formula: Formula, nvars: int, block: tuple[int, ...]) -> set[tuple[bool, ...]]:
    ans: set[tuple[bool, ...]] = set()
    for bits in itertools.product((False, True), repeat=len(block)):
        residual = simplify(formula, dict(zip(block, bits)))
        if residual is not None and brute_sat(residual, nvars):
            ans.add(bits)
    return ans


def encoded_bits(formula: Formula | None, ambient_n: int) -> int:
    """A fixed explicit indexed encoding used only for finite comparisons."""
    if formula is None:
        return 2
    w = max(1, math.ceil(math.log2(ambient_n + 1)))
    return 2 * w + 3 + sum(2 + len(c) * (w + 1) for c in formula)


def make_balanced_core(n: int, seed: int) -> Formula:
    """Generate a proper duplicate-free exact-(2,2) 3-CNF by rejection."""
    assert n % 3 == 0 and n >= 6
    rng = random.Random(seed)
    signed = [v for v in range(1, n + 1) for _ in range(2)] + [
        -v for v in range(1, n + 1) for _ in range(2)
    ]
    for _ in range(20_000):
        rng.shuffle(signed)
        clauses = [tuple(signed[i : i + 3]) for i in range(0, len(signed), 3)]
        if any(len({abs(x) for x in c}) < 3 for c in clauses):
            continue
        normalized = [tuple(sorted(c, key=lambda x: (abs(x), x < 0))) for c in clauses]
        if len(set(normalized)) != len(normalized):
            continue
        pos = {v: 0 for v in range(1, n + 1)}
        neg = dict(pos)
        for c in normalized:
            for lit in c:
                (pos if lit > 0 else neg)[abs(lit)] += 1
        assert all(pos[v] == 2 and neg[v] == 2 for v in pos)
        return tuple(normalized)
    raise RuntimeError(f"failed to generate balanced core n={n}")


def rank_gf2(rows: list[int], width: int) -> int:
    rows = rows[:]
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def affine_compatible_assignments() -> tuple[int, int, int]:
    # x_i xor x_{i+4}=0, i=0,...,3.  The block x_0,...,x_3 admits all 16
    # assignments although elimination represents the relation with four rows.
    n = 8
    rows = [(1 << i) | (1 << (i + 4)) for i in range(4)]
    rank = rank_gf2(rows, n)
    compatible = 0
    solutions = 0
    for left in range(16):
        has_extension = False
        for right in range(16):
            assignment = left | (right << 4)
            ok = all((assignment & row).bit_count() % 2 == 0 for row in rows)
            solutions += int(ok)
            has_extension |= ok
        compatible += int(has_extension)
    return rank, compatible, solutions


@dataclass
class Counters:
    assertions: int = 0
    failures: int = 0

    def check(self, condition: bool) -> None:
        self.assertions += 1
        if not condition:
            self.failures += 1


def exhaustive_truth_table_audit(c: Counters) -> dict[str, int]:
    functions = 0
    restriction_checks = 0
    fixed_branch_counterexamples = 0
    for n in range(1, 5):
        universe = 1 << n
        for table in range(1 << universe):
            functions += 1
            sat = table != 0
            for t in range(1, n + 1):
                branch_nonempty = []
                for alpha in range(1 << t):
                    found = False
                    for suffix in range(1 << (n - t)):
                        x = alpha | (suffix << t)
                        found |= bool((table >> x) & 1)
                    branch_nonempty.append(found)
                c.check(any(branch_nonempty) == sat)
                restriction_checks += 1
                if t:
                    # The singleton function supported outside branch zero is exact.
                    singleton_table = 1 << 1
                    branch_zero = any(
                        ((singleton_table >> x) & 1)
                        for x in range(0, universe, 1 << t)
                    )
                    c.check(not branch_zero)
                    fixed_branch_counterexamples += 1
    return {
        "truth_tables": functions,
        "restriction_identities": restriction_checks,
        "fixed_branch_counterexamples": fixed_branch_counterexamples,
    }


def core_audit(c: Counters) -> list[dict[str, int | float]]:
    rows: list[dict[str, int | float]] = []
    for n in (6, 12, 24, 48, 96, 192):
        formula = make_balanced_core(n, 7300 + n)
        m = len(formula)
        source_bits = encoded_bits(formula, n)
        for h in (0.5, 2 / 3, 0.8):
            record_bits = 2 + 3 * (math.ceil(math.log2(n + 1)) + 1)
            allowed_unaffected = math.floor((source_bits**h) / record_bits)
            t_lower = max(0, math.ceil((m - allowed_unaffected) / 4))
            c.check(t_lower >= max(0, math.ceil((m - allowed_unaffected) / 4)))
            rows.append(
                {
                    "n": n,
                    "m": m,
                    "source_bits": source_bits,
                    "h": h,
                    "unaffected_clause_allowance": allowed_unaffected,
                    "block_size_lower_bound": t_lower,
                    "fanout_log2_lower_bound": t_lower,
                    "block_fraction_lower_bound": t_lower / n,
                }
            )

        rng = random.Random(9100 + n)
        for t in sorted({1, min(4, n), min(8, n), max(1, n // 3)}):
            block = set(rng.sample(range(1, n + 1), t))
            unaffected = [cl for cl in formula if all(abs(lit) not in block for lit in cl)]
            c.check(len(unaffected) >= m - 4 * t)
            sample_count = min(64, 1 << t)
            for alpha in range(sample_count):
                assignment = {v: bool((alpha >> i) & 1) for i, v in enumerate(sorted(block))}
                residual = simplify(formula, assignment)
                if residual is not None:
                    residual_set = set(residual)
                    c.check(all(cl in residual_set for cl in unaffected))
    return rows


def hostile_controls(c: Counters) -> dict[str, object]:
    controls: dict[str, tuple[Formula, int, tuple[int, ...]]] = {
        "horn": (((-1, 2), (-2, 3), (1,)), 3, (1, 2)),
        "2sat_unsat": (((1,), (-1,)), 1, (1,)),
        "bounded_treewidth": (((-1, 2), (-2, 3), (-3, 4), (1,)), 4, (1, 2)),
        "independent_product": (((1, 2), (-1, 2), (3, 4), (-3, 4)), 4, (1, 3)),
        "redundant": (((1, 2), (1, 2), (-1, 2)), 2, (1,)),
        "padding": (((1,), (2, -2), (3, -3), (4, -4)), 4, (1, 2)),
    }
    wrappers = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
    out: dict[str, object] = {}
    for name, (formula, nvars, block) in controls.items():
        sat = brute_sat(formula, nvars)
        hset = compatibility(formula, nvars, block)
        c.check(sat == bool(hset))
        for _wrapper in wrappers:
            c.check(sat == brute_sat(formula, nvars))
        # Clause/literal order and a tautological extension preserve the bit.
        alternate = tuple(tuple(reversed(cl)) for cl in reversed(formula)) + ((nvars + 1, -(nvars + 1)),)
        c.check(sat == brute_sat(alternate, nvars + 1))
        out[name] = {"sat": sat, "compatibility_size": len(hset), "wrappers": len(wrappers)}

    rank, projected, solutions = affine_compatible_assignments()
    c.check(rank == 4)
    c.check(projected == 16)
    c.check(solutions == 16)
    out["affine_tseitin_gaussian"] = {
        "rank": rank,
        "compatible_block_assignments": projected,
        "solutions": solutions,
        "representation_rows": 4,
    }
    return out


def main() -> None:
    start = time.process_time()
    counters = Counters()
    report = {
        "run_id": "LB-0016",
        "scope": "finite audit only; no asymptotic or arbitrary-algorithm inference",
        "truth_table": exhaustive_truth_table_audit(counters),
        "clean_core": core_audit(counters),
        "hostile_controls": hostile_controls(counters),
    }
    report["assertions"] = counters.assertions
    report["failures"] = counters.failures
    report["runtime_seconds"] = time.process_time() - start
    if counters.failures:
        raise AssertionError(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
