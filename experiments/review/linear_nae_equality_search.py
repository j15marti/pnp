#!/usr/bin/env python3
"""Search for signed NAE-3 equality gadgets with linear clause supports.

The distinguished variables are a=0 and b=1.  Auxiliary variables begin at 2.
Every clause uses three distinct variables.  A sign pattern is canonicalized
modulo simultaneous complementation of all three literals, since NAE is
invariant under that operation.  The search requires any two clause supports
to intersect in at most one variable.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Clause:
    support: tuple[int, int, int]
    signs: tuple[int, int, int]
    sat_mask: int
    bad_mask: int


def make_clauses(nvars: int) -> list[Clause]:
    clauses: list[Clause] = []
    full = (1 << (1 << nvars)) - 1
    for support in itertools.combinations(range(nvars), 3):
        # Fix the first sign to zero to quotient by global literal complement.
        for tail in itertools.product((0, 1), repeat=2):
            signs = (0, tail[0], tail[1])
            bad = 0
            for assignment in range(1 << nvars):
                vals = tuple(((assignment >> v) & 1) ^ s for v, s in zip(support, signs))
                if vals[0] == vals[1] == vals[2]:
                    bad |= 1 << assignment
            clauses.append(Clause(support, signs, full ^ bad, bad))
    return clauses


def popcount(x: int) -> int:
    return x.bit_count()


def search(naux: int, max_clauses: int, require_constant_fiber: bool) -> dict:
    nvars = 2 + naux
    clauses = make_clauses(nvars)
    full = (1 << (1 << nvars)) - 1
    equal0 = equal1 = unequal = 0
    for assignment in range(1 << nvars):
        a = assignment & 1
        b = (assignment >> 1) & 1
        bit = 1 << assignment
        if a != b:
            unequal |= bit
        elif a == 0:
            equal0 |= bit
        else:
            equal1 |= bit

    # A clause can participate only if it does not by itself destroy either
    # equal row.  This is a weak but inexpensive pruning condition.
    useful = [c for c in clauses if c.sat_mask & equal0 and c.sat_mask & equal1]
    violations: dict[int, list[int]] = {a: [] for a in range(1 << nvars) if (unequal >> a) & 1}
    for idx, c in enumerate(useful):
        for assignment in violations:
            if (c.bad_mask >> assignment) & 1:
                violations[assignment].append(idx)

    nodes = 0
    solution: list[int] | None = None
    solution_counts: tuple[int, int] | None = None

    def dfs(remaining: int, chosen: list[int], last: int) -> bool:
        nonlocal nodes, solution, solution_counts
        nodes += 1
        r0 = remaining & equal0
        r1 = remaining & equal1
        if not r0 or not r1:
            return False
        bad_remaining = remaining & unequal
        if not bad_remaining:
            c0, c1 = popcount(r0), popcount(r1)
            if require_constant_fiber and c0 != c1:
                return False
            solution = chosen.copy()
            solution_counts = (c0, c1)
            return True
        if len(chosen) >= max_clauses:
            return False

        # Pick the uncovered unequal assignment with the fewest compatible
        # clauses after the current canonical index.
        supports = [set(useful[i].support) for i in chosen]
        candidates_by_assignment = []
        x = bad_remaining
        while x:
            lsb = x & -x
            assignment = lsb.bit_length() - 1
            candidates = []
            for idx in violations[assignment]:
                if idx <= last:
                    continue
                s = set(useful[idx].support)
                if all(len(s & t) <= 1 for t in supports):
                    candidates.append(idx)
            if not candidates:
                return False
            candidates_by_assignment.append((len(candidates), assignment, candidates))
            x ^= lsb
        _, _, candidates = min(candidates_by_assignment)

        # Prefer clauses eliminating the most currently uncovered unequal rows.
        candidates.sort(key=lambda i: popcount(useful[i].bad_mask & bad_remaining), reverse=True)
        for idx in candidates:
            if dfs(remaining & useful[idx].sat_mask, chosen + [idx], idx):
                return True
        return False

    found = dfs(full, [], -1)
    encoded = []
    if found and solution is not None:
        for idx in solution:
            c = useful[idx]
            encoded.append({"support": list(c.support), "signs": list(c.signs)})
    return {
        "naux": naux,
        "nvars": nvars,
        "max_clauses": max_clauses,
        "require_constant_fiber": require_constant_fiber,
        "candidate_clauses": len(useful),
        "nodes": nodes,
        "found": found,
        "fiber_counts": list(solution_counts) if solution_counts else None,
        "clauses": encoded,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-aux", type=int, default=2)
    parser.add_argument("--max-aux", type=int, default=7)
    parser.add_argument("--max-clauses", type=int, default=10)
    parser.add_argument("--no-constant-fiber", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    for naux in range(args.min_aux, args.max_aux + 1):
        row = search(naux, args.max_clauses, not args.no_constant_fiber)
        rows.append(row)
        print(json.dumps(row, sort_keys=True))
        if row["found"]:
            break
    payload = {"search": rows}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
