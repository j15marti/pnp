#!/usr/bin/env python3
"""Elliptic-curve Schur-square versus binary-Hadamard projection controls.

STATUS: COMPUTATIONAL.

This models an ECDSA-like cyclic point orbit P,2P,3P,... on an elliptic curve
over F_p.  It compares:

1. the field-level AG evaluation code C_L(D,tO), whose Schur square is
   controlled by the divisor product law L(tO)L(tO) subset L(2tO);

2. a Boolean projection control closer to SU/Hadamard: take one codeword
   f(P_i), slide length-m windows along the cyclic subgroup, and apply all
   binary Hadamard coordinates to the integer labels of field symbols.

The second stage is NOT the exact vMS binary encoder.  Its purpose is to test
whether genus-1 multiplicative closure survives a natural Booleanization.
"""

from __future__ import annotations

import json
import random

SEED = 1


def inv(a, p):
    return pow(a % p, p - 2, p)


def ec_add(P, Q, p, a):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        if y1 % p == 0:
            return None
        lam = (3 * x1 * x1 + a) * inv(2 * y1, p) % p
    else:
        lam = (y2 - y1) * inv(x2 - x1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return x3, y3


def ec_mul(n, P, p, a):
    R = None
    Q = P
    while n:
        if n & 1:
            R = ec_add(R, Q, p, a)
        Q = ec_add(Q, Q, p, a)
        n >>= 1
    return R


def rank_mod(matrix, p):
    A = [[x % p for x in row] for row in matrix]
    if not A:
        return 0
    r = 0
    rows, cols = len(A), len(A[0])
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        iv = inv(A[r][c], p)
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                q = A[i][c]
                A[i] = [(A[i][j] - q * A[r][j]) % p for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def gf2_rank(rows):
    basis = {}
    for x in rows:
        y = x
        while y:
            h = y.bit_length() - 1
            if h in basis:
                y ^= basis[h]
            else:
                basis[h] = y
                break
    return len(basis)


def basis_L_tO(t):
    """Basis x^i and x^i y with pole orders 2i and 2i+3 <= t."""
    out = [("x", i) for i in range(t // 2 + 1)]
    if t >= 3:
        out += [("xy", i) for i in range((t - 3) // 2 + 1)]
    return out


def eval_basis(basis, points, p):
    G = []
    for kind, i in basis:
        row = []
        for x, y in points:
            v = pow(x, i, p)
            if kind == "xy":
                v = v * y % p
            row.append(v)
        G.append(row)
    return G


def schur_square_rows(G, p):
    return [
        [G[i][j] * G[k][j] % p for j in range(len(G[0]))]
        for i in range(len(G))
        for k in range(i, len(G))
    ]


def phi2(bits):
    z = 1
    pos = 1
    m = len(bits)
    for b in bits:
        if b:
            z |= 1 << pos
        pos += 1
    for i in range(m):
        for j in range(i + 1, m):
            if bits[i] & bits[j]:
                z |= 1 << pos
            pos += 1
    return z


def hadamard_window_rank(values, m, p):
    width = (p - 1).bit_length()
    rows = []
    N = len(values)
    for s in range(N):
        window = [values[(s + i) % N] for i in range(m)]
        for coord in range(1 << width):
            bits = [((v & coord).bit_count() & 1) for v in window]
            rows.append(phi2(bits))
    return gf2_rank(rows)


def main():
    rng = random.Random(SEED)

    # E: y^2 = x^3 + 4x + 20 over F_29.
    # P=(0,7) has order 37, giving a long ECDSA-like cyclic orbit.
    p, a, b = 29, 4, 20
    P = (0, 7)
    order = 37
    orbit = [ec_mul(i, P, p, a) for i in range(1, order)]

    out = {
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "curve": {"p": p, "a": a, "b": b, "P": list(P), "order": order},
        "scope_guard": [
            "Field-level stage is an exact one-point elliptic AG-code control.",
            "Binary stage uses integer-label Hadamard coordinates, not exact vMS Booleanization.",
            "Finite experiments are not asymptotic theorems."
        ],
        "field_level": [],
        "binary_projection": [],
    }

    for t in range(2, 9):
        B = basis_L_tO(t)
        G = eval_basis(B, orbit, p)
        out["field_level"].append({
            "t": t,
            "dimension": rank_mod(G, p),
            "schur_square_dimension": rank_mod(schur_square_rows(G, p), p),
            "riemann_roch_upper_bound_dim_L_2tO": 2 * t,
        })

    for t in range(2, 7):
        B = basis_L_tO(t)
        G = eval_basis(B, orbit, p)
        for m in (6, 8, 10):
            M = 1 + m + m * (m - 1) // 2
            ranks = []
            for _ in range(10):
                coeffs = [rng.randrange(p) for _ in G]
                vals = [
                    sum(coeffs[i] * G[i][j] for i in range(len(G))) % p
                    for j in range(len(orbit))
                ]
                ranks.append(hadamard_window_rank(vals, m, p))
            out["binary_projection"].append({
                "t": t,
                "m": m,
                "M": M,
                "trials": 10,
                "ranks": ranks,
                "distinct_ranks": sorted(set(ranks)),
            })

    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
