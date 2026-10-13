#!/usr/bin/env python3
"""Exact finite audit of the field-trace quadratic firewall.

For K=GF(2^r), Q(x,y)=xy maps K^2 onto K.  Every nonzero scalar
component Tr(lambda Q) has a nonsingular alternating polar form, yet
Q(1,b)=b gives a uniform selector.  This program verifies irreducibility,
all nonzero component ranks, and all selectors for r<=8.
"""

from __future__ import annotations

import hashlib
import json
import time


MAX_R = 8


def degree(p: int) -> int:
    return p.bit_length() - 1


def poly_mod(a: int, modulus: int) -> int:
    md = degree(modulus)
    while degree(a) >= md:
        a ^= modulus << (degree(a) - md)
    return a


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def mul(a: int, b: int, modulus: int, r: int) -> int:
    out = 0
    x = a
    y = b
    while y:
        if y & 1:
            out ^= x
        y >>= 1
        x <<= 1
        if x >> r:
            x ^= modulus
    return out & ((1 << r) - 1)


def square(a: int, modulus: int, r: int) -> int:
    return mul(a, a, modulus, r)


def is_irreducible(modulus: int, r: int) -> bool:
    if degree(modulus) != r or not (modulus & 1):
        return False
    x = poly_mod(2, modulus)
    power = x
    for i in range(1, r + 1):
        power = square(power, modulus, r)
        if i <= r // 2 and poly_gcd(power ^ x, modulus) != 1:
            return False
    return power == x


def first_irreducible(r: int) -> int:
    for low in range(1, 1 << r, 2):
        candidate = (1 << r) | low
        if is_irreducible(candidate, r):
            return candidate
    raise AssertionError("no irreducible polynomial found")


def trace(a: int, modulus: int, r: int) -> int:
    total = 0
    x = a
    for _ in range(r):
        total ^= x
        x = square(x, modulus, r)
    assert total in (0, 1)
    return total


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        x = row
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def polar_rows(lam: int, modulus: int, r: int) -> list[int]:
    """Matrix for Tr(lam*(x*y'+x'*y)) on K x K."""
    rows = [0] * (2 * r)
    basis = [1 << i for i in range(r)]
    for i in range(2 * r):
        xi, yi = (basis[i], 0) if i < r else (0, basis[i - r])
        for j in range(2 * r):
            xj, yj = (basis[j], 0) if j < r else (0, basis[j - r])
            value = trace(mul(lam, mul(xi, yj, modulus, r) ^ mul(xj, yi, modulus, r), modulus, r), modulus, r)
            rows[i] |= value << j
    return rows


def main() -> None:
    start = time.perf_counter()
    checks = 0
    records = []
    for r in range(1, MAX_R + 1):
        modulus = first_irreducible(r)
        assert is_irreducible(modulus, r)
        checks += 1
        ranks = []
        for lam in range(1, 1 << r):
            rank = gf2_rank(polar_rows(lam, modulus, r))
            assert rank == 2 * r
            ranks.append(rank)
            checks += 1
        for b in range(1 << r):
            assert mul(1, b, modulus, r) == b
            checks += 1
        # Nondegeneracy of the field trace pairing, checked directly.
        for a in range(1, 1 << r):
            assert any(trace(mul(a, z, modulus, r), modulus, r) for z in range(1 << r))
            checks += 1
        records.append({
            "r": r,
            "modulus": modulus,
            "component_count": (1 << r) - 1,
            "all_component_ranks": sorted(set(ranks)),
            "selector_count": 1 << r,
            "max_selector_bit_weight_in_basis": 1 + r,
        })
    result = {
        "run_id": "FIELDTRACEFW1",
        "tested_r": [1, MAX_R],
        "records": records,
        "assertions": checks,
        "elapsed_seconds": time.perf_counter() - start,
        "status": "COMPUTATIONAL",
        "symbolic_identity": "Q(1,b)=b; beta_lambda((x,y),(x',y'))=Tr(lambda*(x*y'+x'*y))",
        "limitation": "Finite checks validate r<=8; the general theorem is the displayed finite-field argument, not a measured runtime inference.",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_sha256_without_self_hash"] = hashlib.sha256(payload).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
