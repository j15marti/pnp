#!/usr/bin/env python3
"""Reproducible toy models for Schur-square / SU-Hadamard image geometry.

Status: computational controls only. This does not implement the exact vMS PCP-LDE
construction and must not be cited as an asymptotic theorem about that construction.

Run:
    python experiments/product_span/schur_image_models.py
"""

import itertools
import json
import random
from collections import Counter


SEED = 1


def rank_mod(matrix, p):
    A = [[x % p for x in row] for row in matrix]
    if not A:
        return 0
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                q = A[i][c]
                A[i] = [(A[i][j] - q * A[r][j]) % p for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def gf2_rank_bitsets(rows):
    basis = {}
    rank = 0
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in basis:
                x ^= basis[h]
            else:
                basis[h] = x
                rank += 1
                break
    return rank


def gf2_basis(vectors):
    basis = {}
    for x in vectors:
        y = x
        while y:
            h = y.bit_length() - 1
            if h in basis:
                y ^= basis[h]
            else:
                basis[h] = y
                break
    return list(basis.values())


def span_elements(basis):
    out = [0]
    for b in basis:
        out += [x ^ b for x in out]
    return out


def phi2(x, m):
    """Bitset for (1, x_i, x_i x_j) with i<j."""
    z = 1
    pos = 1
    bits = [(x >> i) & 1 for i in range(m)]
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


def quadratic_feature_rank(points, m):
    return gf2_rank_bitsets([phi2(x, m) for x in points])


def union_subspace_quadratic_rank(block_bases, m):
    rows = []
    for basis in block_bases:
        for x in span_elements(basis):
            rows.append(phi2(x, m))
    return gf2_rank_bitsets(rows)


def grs_generator(p, n, k):
    xs = list(range(1, n + 1))
    return [[pow(x, d, p) for x in xs] for d in range(k)]


def schur_square_rows(G, p):
    out = []
    for i in range(len(G)):
        for j in range(i, len(G)):
            out.append([(G[i][t] * G[j][t]) % p for t in range(len(G[0]))])
    return out


def random_full_rank_code(p, n, k, rng):
    while True:
        G = [[rng.randrange(p) for _ in range(n)] for _ in range(k)]
        if rank_mod(G, p) == k:
            return G


def random_k_subspace(m, k, rng):
    while True:
        B = gf2_basis([rng.getrandbits(m) for _ in range(k)])
        if len(B) == k:
            return B


def cyclic_shift(x, m, s):
    s %= m
    if not s:
        return x
    mask = (1 << m) - 1
    return ((x << s) & mask) | (x >> (m - s))


def coordinate_window_basis(m, k, t):
    return [1 << ((t + i) % m) for i in range(k)]


def label_window_subspaces(labels, m, k):
    """Hadamard-block model.

    labels[t] is the k-bit binary label of the t-th outer symbol.
    A length-m window gives an m x k matrix B_t.  As the Hadamard
    seed j ranges over F_2^k, the binary output block is im(B_t).
    """
    N = len(labels)
    blocks = []
    for t in range(N):
        cols = []
        for bit in range(k):
            v = 0
            for i in range(m):
                if (labels[(t + i) % N] >> bit) & 1:
                    v |= 1 << i
            cols.append(v)
        blocks.append(gf2_basis(cols))
    return blocks


def rm1_square_rank(r):
    n = 1 << r
    rows = [(1 << n) - 1]
    for i in range(r):
        row = 0
        for x in range(n):
            if (x >> i) & 1:
                row |= 1 << x
        rows.append(row)
    products = []
    for i in range(len(rows)):
        for j in range(i, len(rows)):
            products.append(rows[i] & rows[j])
    return gf2_rank_bitsets(products)


def main():
    rng = random.Random(SEED)
    out = {
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "limitations": [
            "Toy structural controls only.",
            "Does not implement the exact vMS PCP verifier or its reachable proof set.",
            "Finite rank data are not asymptotic theorems."
        ],
    }

    # Structured evaluation codes versus random codes.
    grs = []
    random_codes = []
    for p, n, k in [(13, 11, 4), (17, 13, 5), (29, 20, 6)]:
        G = grs_generator(p, n, k)
        grs.append({
            "p": p, "n": n, "k": k,
            "square_rank": rank_mod(schur_square_rows(G, p), p),
            "expected_2k_minus_1": min(n, 2 * k - 1),
        })
        ranks = []
        for _ in range(200):
            R = random_full_rank_code(p, n, k, rng)
            ranks.append(rank_mod(schur_square_rows(R, p), p))
        random_codes.append({
            "p": p, "n": n, "k": k, "trials": 200,
            "distribution": dict(sorted(Counter(ranks).items())),
            "max_possible": min(n, k * (k + 1) // 2),
        })
    out["grs"] = grs
    out["random_codes"] = random_codes

    # Exact Reed-Muller/Hadamard control: RM(1,r)^2 = RM(2,r).
    out["rm1_square"] = [
        {
            "r": r,
            "square_rank": rm1_square_rank(r),
            "expected": 1 + r + r * (r - 1) // 2,
        }
        for r in range(2, 7)
    ]

    # Random union of Hadamard block subspaces.
    random_blocks = []
    for m, k in [(12, 3), (16, 4), (20, 5)]:
        blocks = [random_k_subspace(m, k, rng) for _ in range(20)]
        rank_by_blocks = []
        for b in [1, 2, 3, 4, 5, 8, 10, 12, 14, 16, 20]:
            rank_by_blocks.append(
                [b, union_subspace_quadratic_rank(blocks[:b], m)]
            )
        random_blocks.append({
            "m": m, "k": k,
            "M": 1 + m + m * (m - 1) // 2,
            "one_block_expected": 1 + k + k * (k - 1) // 2,
            "rank_by_blocks": rank_by_blocks,
        })
    out["random_hadamard_blocks"] = random_blocks

    # Strongly aligned cyclic coordinate windows.
    cyclic_coordinate = []
    for m, k in [(16, 3), (20, 4), (24, 5), (32, 5)]:
        blocks = [coordinate_window_basis(m, k, t) for t in range(m)]
        cyclic_coordinate.append({
            "m": m, "k": k,
            "M": 1 + m + m * (m - 1) // 2,
            "rank": union_subspace_quadratic_rank(blocks, m),
            "exact_when_k_le_m_over_2": 1 + m * k,
        })
    out["cyclic_coordinate_windows"] = cyclic_coordinate

    # Cyclic shifts of a random base subspace.
    cyclic_random = []
    for m, k in [(16, 3), (20, 4), (24, 5), (32, 5)]:
        B = random_k_subspace(m, k, rng)
        blocks = [[cyclic_shift(v, m, t) for v in B] for t in range(m)]
        cyclic_random.append({
            "m": m, "k": k,
            "M": 1 + m + m * (m - 1) // 2,
            "rank": union_subspace_quadratic_rank(blocks, m),
        })
    out["cyclic_random_base_subspace"] = cyclic_random

    # More faithful sliding-label Hadamard model.
    sliding = []
    for m, k, N in [(12, 3, 60), (16, 4, 64), (20, 5, 100), (24, 5, 100)]:
        random_labels = [rng.randrange(1 << k) for _ in range(N)]
        random_subspaces = label_window_subspaces(random_labels, m, k)
        periodic_labels = [1 << (t % k) for t in range(N)]
        periodic_subspaces = label_window_subspaces(periodic_labels, m, k)
        sliding.append({
            "m": m, "k": k, "N": N,
            "M": 1 + m + m * (m - 1) // 2,
            "random_label_rank": union_subspace_quadratic_rank(random_subspaces, m),
            "periodic_aligned_rank": union_subspace_quadratic_rank(periodic_subspaces, m),
            "single_block_dimension": 1 + k + k * (k - 1) // 2,
        })
    out["sliding_label_blocks"] = sliding

    # Nonlinear validity constraints can defeat an ambient-rank test.
    ambient = list(range(8))
    valid = []
    for a, b in itertools.product([0, 1], repeat=2):
        c = a & b
        valid.append(a | (b << 1) | (c << 2))
    out["validity_constraint_control"] = {
        "ambient_F2_3_quadratic_rank": quadratic_feature_rank(ambient, 3),
        "valid_graph_c_eq_ab_rank": quadratic_feature_rank(valid, 3),
        "explicit_relation": "c + a*b = 0 on the valid set",
        "point_count": len(valid),
    }

    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
