"""Minimal CNF helpers for hostile-control experiments."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def evaluate_cnf(formula: Sequence[Sequence[int]], assignment: Sequence[bool]) -> bool:
    """Evaluate a CNF. Literals use 1-based variables; negative means negated."""
    for clause in formula:
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var == 0 or var > len(assignment):
                raise ValueError("literal variable out of assignment range")
            value = bool(assignment[var - 1])
            satisfied |= value if lit > 0 else not value
        if not satisfied:
            return False
    return True


def all_negative_horn(hyperedges: Iterable[Sequence[int]]) -> CNF:
    """Put the trivially satisfiable all-negative Horn signing on hyperedges."""
    return tuple(tuple(-int(v) for v in edge) for edge in hyperedges)


def signed_cnf(
    hyperedges: Sequence[Sequence[int]],
    signs: Sequence[Sequence[bool]],
) -> CNF:
    if len(hyperedges) != len(signs):
        raise ValueError("one sign row is required per hyperedge")
    clauses: list[Clause] = []
    for edge, sign_row in zip(hyperedges, signs):
        if len(edge) != len(sign_row):
            raise ValueError("sign row length must match hyperedge")
        clauses.append(
            tuple(int(v) if positive else -int(v) for v, positive in zip(edge, sign_row))
        )
    return tuple(clauses)


def incidence_cut_profile(
    hyperedges: Sequence[Sequence[int]],
    ordering: Sequence[int],
) -> list[int]:
    """Unsigned number of hyperedges straddling each cut of a variable order."""
    pos = {int(v): i for i, v in enumerate(ordering)}
    if len(pos) != len(ordering):
        raise ValueError("ordering must not repeat variables")
    profile = []
    for cut in range(len(ordering) - 1):
        count = 0
        for edge in hyperedges:
            positions = [pos[int(v)] for v in edge]
            if min(positions) <= cut < max(positions):
                count += 1
        profile.append(count)
    return profile
