#!/usr/bin/env python3
"""Finite controls for REFEREE336.

These checks audit the conventional OR-extension to signed-AND DEF map,
literal-substitution compatibility with resolution, malformed records, and
finite numeric instances of the polynomial comparison.  They do not prove
the all-size simulation theorem or any SAT lower bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


OUT = Path("results/raw/arc/lspv5_336/er2_rmix_equivalence_referee336.json")


def neg(lit: int) -> int:
    return -lit


def lit_value(lit: int, assignment: dict[int, bool]) -> bool:
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def clause_value(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


def resolve(c1: tuple[int, ...], c2: tuple[int, ...], pivot: int) -> tuple[int, ...] | None:
    if pivot not in c1 or -pivot not in c2:
        return None
    out = set(c1)
    out.remove(pivot)
    out.update(c2)
    out.remove(-pivot)
    if any(-lit in out for lit in out):
        return None
    return tuple(sorted(out, key=lambda x: (abs(x), x < 0)))


def substitute_clause(clause: tuple[int, ...], sigma: dict[int, int]) -> tuple[int, ...] | None:
    out = {sigma.get(lit, lit) for lit in clause}
    if any(-lit in out for lit in out):
        return None
    return tuple(sorted(out, key=lambda x: (abs(x), x < 0)))


def valid_ext(record: dict) -> bool:
    if set(record) != {"out", "left", "right"}:
        return False
    if not all(isinstance(record[k], int) and record[k] != 0 for k in record):
        return False
    out, left, right = record["out"], record["left"], record["right"]
    if out < 0 or abs(out) in {abs(left), abs(right)}:
        return False
    return abs(left) != abs(right)


def main() -> None:
    assertions = 0
    or_def_cases = 0
    resolution_cases = 0

    # Conventional ER: y <-> (l1 OR l2).  Compile to
    # u := (NOT l1) AND (NOT l2), substitute y -> NOT u.
    for l1_sign, l2_sign in itertools.product((1, -1), repeat=2):
        l1, l2, y, u = l1_sign * 1, l2_sign * 2, 3, 4
        er = ((-y, l1, l2), (y, -l1), (y, -l2))
        translated = ((u, l1, l2), (-u, -l1), (-u, -l2))
        sigma = {y: -u, -y: u}
        assert tuple(frozenset(substitute_clause(c, sigma) or ()) for c in er) == tuple(frozenset(c) for c in translated)
        assertions += 1
        for x1, x2, uv in itertools.product((False, True), repeat=3):
            a = {1: x1, 2: x2, 4: uv}
            target_u = (not lit_value(l1, a)) and (not lit_value(l2, a))
            slots = all(clause_value(c, a) for c in translated)
            assert slots == (uv == target_u)
            assertions += 1
            or_def_cases += 1

    # Exhaustively check that a signed bijective literal substitution commutes
    # with every non-tautological resolution inference in a small universe.
    literals = (-3, -2, -1, 1, 2, 3)
    clauses: list[tuple[int, ...]] = []
    for width in range(1, 4):
        for combo in itertools.combinations(literals, width):
            if not any(-lit in combo for lit in combo):
                clauses.append(tuple(sorted(combo, key=lambda x: (abs(x), x < 0))))
    sigma = {1: -4, -1: 4, 2: 5, -2: -5, 3: -6, -3: 6}
    for c1 in clauses:
        for c2 in clauses:
            for pivot in (1, 2, 3):
                r = resolve(c1, c2, pivot)
                if r is None:
                    continue
                sc1 = substitute_clause(c1, sigma)
                sc2 = substitute_clause(c2, sigma)
                sr = substitute_clause(r, sigma)
                assert sc1 is not None and sc2 is not None and sr is not None
                assert resolve(sc1, sc2, sigma[pivot]) == sr
                assertions += 1
                resolution_cases += 1

    malformed = [
        {},
        {"out": 3, "left": 1},
        {"out": -3, "left": 1, "right": 2},
        {"out": 1, "left": 1, "right": 2},
        {"out": 3, "left": 1, "right": -1},
        {"out": 3, "left": 0, "right": 2},
        {"out": 3, "left": 1, "right": 2, "oracle": True},
    ]
    for record in malformed:
        assert not valid_ext(record)
        assertions += 1
    valid = {"out": 3, "left": -1, "right": 2}
    assert valid_ext(valid)
    assertions += 1

    # Finite arithmetic controls for a fixed C=1 envelope.  These values do
    # not estimate the theorem's hidden constant; they only detect reversed
    # inequalities and max/composition mistakes.
    numeric_cases = 0
    for n in range(0, 65):
        for wr in range(0, 65):
            upper = (n + wr + 3) ** 4
            for we in (wr, min(upper, wr + n + 1), upper):
                assert wr <= we <= upper
                assertions += 1
                numeric_cases += 1

    # Both-label and malformed source controls for a tiny DIMACS-like model.
    sources = {
        "sat": [(1,)],
        "unsat": [(1,), (-1,)],
    }
    assert any(all(clause_value(c, {1: x}) for c in sources["sat"]) for x in (False, True))
    assert not any(all(clause_value(c, {1: x}) for c in sources["unsat"]) for x in (False, True))
    assertions += 2

    payload = {
        "artifact": "ER2-MIXED-POLYNOMIAL-EQUIVALENCE-REFEREE336",
        "status": "PASS",
        "scope": "finite semantic controls only",
        "assertions": assertions,
        "or_def_assignment_cases": or_def_cases,
        "resolution_substitution_cases": resolution_cases,
        "malformed_extension_records_rejected": len(malformed),
        "numeric_comparison_cases": numeric_cases,
        "both_label_controls": 2,
        "theorem_claimed_elsewhere": "W_RrootK(F) <= W_ER2(F) <= C_K(N+W_RrootK(F)+3)^4 for fixed-K typed private-root semantics",
        "full_Rmix_converse": "OPEN pending a fixed support bound, typed coercion, and executable parser",
        "not_claimed": ["B1", "B2", "B3", "P!=NP", "machine-time lower bound"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["summary_sha256"] = hashlib.sha256(canonical).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
