#!/usr/bin/env python3
"""Independent finite controls for LSPV-5/423.

This checks only elementary representation lemmas used to audit LSPV-1/492.
It does not replay Lean or prove Pang's asymptotic proof-complexity theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
import math


def encode_nat(n: int) -> list[bool]:
    assert isinstance(n, int) and n >= 0
    return [True] * n + [False]


def frame(bits: list[bool]) -> list[bool]:
    out = [False]
    for bit in reversed(bits):
        out = [True, bit] + out
    return out


def encode_list(enc, xs) -> list[bool]:
    if not xs:
        return [False]
    return [True] + frame(enc(xs[0])) + encode_list(enc, xs[1:])


def literal_code(lit: int) -> int:
    v = abs(lit) - 1
    return 2 * v + (1 if lit > 0 else 0)


def canonical_clause(clause: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted({literal_code(lit) for lit in clause}))


def canonical_formula(clauses: list[tuple[int, ...]]) -> list[list[int]]:
    return [list(c) for c in sorted({canonical_clause(c) for c in clauses})]


def encode_cnf(n: int, clauses: list[tuple[int, ...]]) -> list[bool]:
    body = encode_list(lambda c: encode_list(encode_nat, c), canonical_formula(clauses))
    return encode_nat(n) + body


def strict3(n: int, clauses: list[tuple[int, ...]]) -> bool:
    return (
        isinstance(n, int)
        and n >= 0
        and all(
            len(c) == 3
            and all(isinstance(x, int) and not isinstance(x, bool) and 0 < abs(x) <= n for x in c)
            and len({abs(x) for x in c}) == 3
            for c in clauses
        )
    )


def model_count(n: int, clauses: list[tuple[int, ...]]) -> int:
    total = 0
    for assignment in product((False, True), repeat=n):
        if all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses):
            total += 1
    return total


def clause_universe_size(n: int) -> int:
    return 8 * math.comb(n, 3)


def collision_union_bound(n: int) -> Fraction:
    m = 8 * n
    return Fraction(math.comb(m, 2), clause_universe_size(n))


def closed_collision_bound(n: int) -> Fraction:
    return Fraction(3 * (8 * n - 1), (n - 1) * (n - 2))


def length_bound(n: int, m: int) -> int:
    return n + 2 + m * (24 * n + 16)


def all_proper_clauses(n: int) -> list[tuple[int, int, int]]:
    out = []
    for vs in combinations(range(1, n + 1), 3):
        for signs in product((-1, 1), repeat=3):
            out.append(tuple(v * s for v, s in zip(vs, signs)))
    return out


def main() -> None:
    checks = 0
    # Directly reconstruct the exact clauses-per-draw universe in Pang F(n,3,8n).
    for n in range(3, 10):
        assert len(all_proper_clauses(n)) == clause_universe_size(n)
        checks += 1

    collision_rows = []
    for n in range(3, 10001):
        u = collision_union_bound(n)
        assert u == closed_collision_bound(n)
        checks += 1
        if n >= 6:
            assert u <= Fraction(48, n)
            checks += 1
        if n in (3, 6, 10, 100, 1000, 10000):
            collision_rows.append({"n": n, "union_bound": float(u), "closed_form": str(u)})

    # Exact reconstruction of OpenAI's unary/framed Finset encoding, including
    # deduplication.  Deterministic distinct samples exercise the strict 3-CNF path.
    encoding_rows = []
    for n in range(3, 10):
        universe = all_proper_clauses(n)
        m = min(8 * n, len(universe))
        clauses = universe[-m:]
        actual = len(encode_cnf(n, clauses))
        bound = length_bound(n, m)
        assert strict3(n, clauses)
        assert actual <= bound
        checks += 3
        duplicate = clauses + [clauses[0]]
        assert encode_cnf(n, duplicate) == encode_cnf(n, clauses)
        checks += 1
        encoding_rows.append({"n": n, "m": m, "actual_bits": actual, "bound_bits": bound})

    # The Pang density m=8n has L <= 192n^2+129n+2 under this exact encoding.
    for n in range(3, 10001):
        assert length_bound(n, 8 * n) == 192 * n * n + 129 * n + 2
        checks += 1

    # SAT/UNSAT and malformed-input controls.
    cube = [tuple(v if (mask >> (v - 1)) & 1 else -v for v in (1, 2, 3)) for mask in range(8)]
    assert model_count(3, cube) == 0
    assert model_count(3, cube[:-1]) == 1
    assert model_count(3, []) == 8
    checks += 3
    malformed = [
        [(1, 1, 2)],
        [(1, 2, 0)],
        [(1, 2, 4)],
        [(1, 2)],
        [(1, 2, 3, 4)],
        [(True, 2, 3)],
    ]
    for bad in malformed:
        assert not strict3(3, bad)
        checks += 1

    # Symbolic algebra behind the O(1/n) collision estimate.
    # 48(n-1)(n-2) - 3n(8n-1) = 24n^2 - 141n + 96 > 0 for n >= 6.
    for n in range(6, 10001):
        assert 24 * n * n - 141 * n + 96 > 0
        checks += 1

    out = {
        "status": "FINITE REPRESENTATION CONTROLS; no Lean or Pang theorem replay",
        "checks": checks,
        "collision_bound": "Pr[duplicate] <= C(8n,2)/(8*C(n,3)) = 3(8n-1)/((n-1)(n-2)) <= 48/n for n>=6",
        "encoding_bound": "L <= n+2+m(24n+16); for m=8n, L <= 192n^2+129n+2",
        "collision_rows": collision_rows,
        "encoding_rows": encoding_rows,
        "sat_unsat_controls": {"full_cube_models": 0, "seven_cube_models": 1, "empty_models": 8},
        "malformed_rejections": len(malformed),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
