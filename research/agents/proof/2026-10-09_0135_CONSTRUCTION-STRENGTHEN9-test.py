#!/usr/bin/env python3
"""Bounded audit of checkpoint batches and Construction9 control families.

Exhaustively enumerates total deterministic transition maps on at most five
states.  It compares:

  true      : f^(l1+l2)(start) == accept,
  independent: (exists z R_l1(start,z)) AND
               (exists y R_l2(y,accept)),
  coupled   : exists z [R_l1(start,z) AND R_l2(z,accept)].

The independent expression is the proposed parallel child batch with the
shared checkpoint omitted.  The coupled expression is the repaired formula.
Finite evidence only; the symbolic equivalence is proved in the report.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import signal
import time
from pathlib import Path


def step(f: tuple[int, ...], x: int, length: int) -> int:
    for _ in range(length):
        x = f[x]
    return x


def is_single_cycle(f: tuple[int, ...]) -> bool:
    """Strong connectivity for a total functional digraph."""
    q = len(f)
    seen = set()
    x = 0
    for _ in range(q):
        if x in seen:
            break
        seen.add(x)
        x = f[x]
    return len(seen) == q and x == 0


def mixed_window_formula(n: int) -> tuple[tuple[int, int, int], ...]:
    clauses = []
    for i in range(n):
        window = (i + 1, (i + 1) % n + 1, (i + 2) % n + 1)
        clauses.append(window)
        clauses.append(tuple(-x for x in window))
    return tuple(clauses)


def satisfies(clauses: tuple[tuple[int, ...], ...], bits: tuple[int, ...]) -> bool:
    return all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in clauses)


def brute_sat(clauses: tuple[tuple[int, ...], ...]) -> bool:
    variables = sorted({abs(x) for c in clauses for x in c})
    pos = {v: i for i, v in enumerate(variables)}
    return any(
        all(any(((mask >> pos[abs(x)]) & 1) == (x > 0) for x in c)
            for c in clauses)
        for mask in range(1 << len(variables))
    )


def gf2_rank(rows: list[int]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)


def connected_variables(clauses: tuple[tuple[int, ...], ...]) -> bool:
    vertices = {abs(x) for c in clauses for x in c}
    if not vertices:
        return True
    graph = {v: set() for v in vertices}
    for c in clauses:
        vs = {abs(x) for x in c}
        for u in vs:
            graph[u].update(vs - {u})
    seen = set()
    stack = [next(iter(vertices))]
    while stack:
        v = stack.pop()
        if v not in seen:
            seen.add(v)
            stack.extend(graph[v] - seen)
    return seen == vertices


def balanced_lifted_cross(k: int) -> tuple[tuple[int, int, int], ...]:
    """Recovery8 sign-balanced family; x=1 is a singleton Krom backdoor."""
    out = []
    z = 2 * k + 2
    for i in range(k):
        a = 2 + i
        for lit in (a, -a):
            out.extend(((1, lit, z), (1, lit, -z)))
            z += 1
    for i in range(k):
        b = 2 + k + i
        for lit in (b, -b):
            out.extend(((-1, lit, z), (-1, lit, -z)))
            z += 1
    return tuple(out)


def restrict(clauses: tuple[tuple[int, ...], ...], var: int, value: int):
    residual = []
    for clause in clauses:
        if any(abs(x) == var and (x > 0) == bool(value) for x in clause):
            continue
        residual.append(tuple(x for x in clause if abs(x) != var))
    return tuple(residual)


def variable_components(clauses: tuple[tuple[int, ...], ...]):
    vertices = {abs(x) for c in clauses for x in c}
    graph = {v: set() for v in vertices}
    for clause in clauses:
        vs = {abs(x) for x in clause}
        for u in vs:
            graph[u].update(vs - {u})
    parts = []
    while vertices:
        todo = [next(iter(vertices))]
        seen = set()
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend(graph[v] - seen)
        vertices -= seen
        parts.append(tuple(c for c in clauses if any(abs(x) in seen for x in c)))
    return tuple(parts)


def main() -> None:
    signal.alarm(24)
    started = time.monotonic()
    total_cases = 0
    independent_false_positives = 0
    coupled_mismatches = 0
    strongly_connected_false_positives = 0
    first_false_positive = None
    first_strong_false_positive = None
    digest = hashlib.sha256()

    for q in range(1, 6):
        for f in itertools.product(range(q), repeat=q):
            strong = is_single_cycle(f)
            for start in range(q):
                for accept in range(q):
                    for l1 in range(1, 4):
                        for l2 in range(1, 4):
                            total_cases += 1
                            mid = step(f, start, l1)
                            truth = step(f, mid, l2) == accept
                            first_child = True  # z=f^l1(start) always exists.
                            second_child = any(
                                step(f, y, l2) == accept for y in range(q)
                            )
                            independent = first_child and second_child
                            coupled = any(
                                step(f, start, l1) == z
                                and step(f, z, l2) == accept
                                for z in range(q)
                            )
                            if coupled != truth:
                                coupled_mismatches += 1
                            if independent and not truth:
                                independent_false_positives += 1
                                witness = {
                                    "states": q,
                                    "transition": list(f),
                                    "start": start,
                                    "accept": accept,
                                    "first_length": l1,
                                    "second_length": l2,
                                    "actual_checkpoint": mid,
                                    "spliced_second_start": next(
                                        y for y in range(q)
                                        if step(f, y, l2) == accept
                                    ),
                                }
                                if first_false_positive is None:
                                    first_false_positive = witness
                                if strong:
                                    strongly_connected_false_positives += 1
                                    if first_strong_false_positive is None:
                                        first_strong_false_positive = witness
                                digest.update(
                                    json.dumps(witness, sort_keys=True).encode()
                                )

    assert first_false_positive is not None
    assert first_strong_false_positive is not None
    assert coupled_mismatches == 0

    mixed_rows = []
    for n in range(6, 102, 2):
        clauses = mixed_window_formula(n)
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
        assert all({x > 0 for c in clauses for x in c if abs(x) == v} == {False, True}
                   for v in range(1, n + 1))
        alternating = tuple(i % 2 for i in range(n))
        assert satisfies(clauses, alternating)
        differences = []
        for i in range(n):
            changed = list(alternating)
            changed[i] ^= 1
            changed[(i + 1) % n] ^= 1
            assert satisfies(clauses, tuple(changed))
            differences.append((1 << i) | (1 << ((i + 1) % n)))
        changed = list(alternating)
        for i in (0, 1, 2):
            changed[i] ^= 1
        assert satisfies(clauses, tuple(changed))
        differences.append(0b111)
        assert gf2_rank(differences) == n

        min_retained = 10**9
        for pivot in range(1, n + 1):
            retained = tuple(c for c in clauses if all(abs(x) != pivot for x in c))
            assert len(retained) == 2 * (n - 3)
            assert connected_variables(retained)
            min_retained = min(min_retained, len(retained))

        # Along least-variable selector descent, clauses disjoint from the
        # assigned prefix survive regardless of the chosen truth values.
        lower_volume_clauses = 0
        prefix_steps = n // 6
        for assigned_count in range(1, prefix_steps + 1):
            assigned = set(range(1, assigned_count + 1))
            untouched = sum(all(abs(x) not in assigned for x in c) for c in clauses)
            assert untouched >= n
            lower_volume_clauses += untouched
        mixed_rows.append({
            "variables": n,
            "clauses": len(clauses),
            "affine_hull_rank": n,
            "minimum_retained_clauses_after_one_pivot": min_retained,
            "selector_prefix_steps": prefix_steps,
            "selector_untouched_clause_volume_lower_bound": lower_volume_clauses,
        })

    krom_rows = []
    for k in range(1, 51):
        clauses = balanced_lifted_cross(k)
        assert all(any(abs(x) == 1 for x in clause) for clause in clauses)
        branches = [restrict(clauses, 1, b) for b in (0, 1)]
        assert all(all(len(clause) <= 2 for clause in branch) for branch in branches)
        parts = [part for branch in branches for part in variable_components(branch)]
        assert len(parts) == 2 * k
        assert max(len({abs(x) for c in part for x in c}) for part in parts) == 3
        # Each component contains the four clauses generated from y and -y;
        # setting y either way falsifies one complementary pair.
        for part in parts:
            assert not brute_sat(part)
        krom_rows.append({"k": k, "clauses": len(clauses), "components": len(parts),
                          "maximum_component_variables": 3})

    result = {
        "status": "PASS_INDEPENDENT_CHECKPOINT_BATCH_FALSIFIED",
        "scope": "Exhaustive total deterministic maps with 1..5 states and segment lengths 1..3.",
        "total_cases": total_cases,
        "independent_false_positives": independent_false_positives,
        "strongly_connected_false_positives": strongly_connected_false_positives,
        "coupled_mismatches": coupled_mismatches,
        "smallest_false_positive": first_false_positive,
        "smallest_strongly_connected_false_positive": first_strong_false_positive,
        "false_positive_digest_sha256": digest.hexdigest(),
        "mixed_window_rows": mixed_rows,
        "strong_krom_control_rows": krom_rows,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "limitations": "Finite corroboration only; no unrestricted wrapper lower bound.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_name(
        "2026-10-09_0135_CONSTRUCTION-STRENGTHEN9-results.json"
    ).write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
