#!/usr/bin/env python3
"""Exact finite controls for the SU05 univariate orbit/Hadamard leaf model.

This is a computational model of one declared SU05 Eq. (7) + Hadamard
realization. It is NOT a transcription of every bit-level choice inside the
vMS local extractor, and finite results are not asymptotic theorems.

For a Boolean vector b on grid points 0,...,h-1:
  1. interpolate the unique degree < h polynomial f over F_p;
  2. for each nonzero v form orbit values f(alpha^(i+1) v), i=0,...,m-1;
  3. binary-label the field values and let the Hadamard seed range over all
     binary linear functionals, producing subspace S_v = im(B_v);
  4. compute the exact rank of degree <= 2 Boolean features on union_v S_v.

No randomness is used.
"""

from collections import Counter
import json
import sys


def factor(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_roots(p):
    fac = factor(p - 1)
    return [
        a for a in range(2, p)
        if all(pow(a, (p - 1) // q, p) != 1 for q in fac)
    ]


def lagrange_eval_coeffs(h, x, p):
    coeff = []
    for t in range(h):
        num = 1
        den = 1
        for s in range(h):
            if s == t:
                continue
            num = num * (x - s) % p
            den = den * (t - s) % p
        coeff.append(num * pow(den, p - 2, p) % p)
    return coeff


def precompute_lagrange(p, h, m, alpha):
    used = set()
    for v in range(1, p):
        a = v
        for _ in range(m):
            a = a * alpha % p
            used.add(a)
    return {x: lagrange_eval_coeffs(h, x, p) for x in used}


def eval_mask(mask, coeff, p):
    total = 0
    while mask:
        bit = mask & -mask
        i = bit.bit_length() - 1
        total += coeff[i]
        mask ^= bit
    return total % p


def gf2_basis(vectors):
    basis = {}
    for x in vectors:
        y = x
        while y:
            lead = y.bit_length() - 1
            if lead in basis:
                y ^= basis[lead]
            else:
                basis[lead] = y
                break
    return list(basis.values())


def phi2(x, m):
    out = 1
    pos = 1
    bits = [(x >> i) & 1 for i in range(m)]
    for b in bits:
        if b:
            out |= 1 << pos
        pos += 1
    for i in range(m):
        for j in range(i + 1, m):
            if bits[i] and bits[j]:
                out |= 1 << pos
            pos += 1
    return out


def quadratic_rows_for_subspace(basis, m):
    # For a linear r-space it suffices to evaluate 0, b_i, and b_i+b_j:
    # these rows span all degree <=2 evaluations on the subspace.
    points = [0] + list(basis)
    for i in range(len(basis)):
        for j in range(i + 1, len(basis)):
            points.append(basis[i] ^ basis[j])
    return [phi2(x, m) for x in points]


def gf2_rank(rows):
    basis = {}
    for x in rows:
        y = x
        while y:
            lead = y.bit_length() - 1
            if lead in basis:
                y ^= basis[lead]
            else:
                basis[lead] = y
                break
    return len(basis)


def product_rank(p, h, m, alpha, mask, lagrange=None):
    if lagrange is None:
        lagrange = precompute_lagrange(p, h, m, alpha)
    k = (p - 1).bit_length()
    rows = []
    powers = [pow(alpha, i + 1, p) for i in range(m)]
    for v in range(1, p):
        columns = [0] * k
        for i, apow in enumerate(powers):
            x = apow * v % p
            value = eval_mask(mask, lagrange[x], p)
            for bit in range(k):
                if (value >> bit) & 1:
                    columns[bit] |= 1 << i
        block_basis = gf2_basis(columns)
        rows.extend(quadratic_rows_for_subspace(block_basis, m))
    return gf2_rank(rows)


def exhaustive_case(p, h, m, all_primitive_roots=False):
    roots = primitive_roots(p)
    if not all_primitive_roots:
        roots = roots[:1]
    M = 1 + m + m * (m - 1) // 2
    results = []
    for alpha in roots:
        lagrange = precompute_lagrange(p, h, m, alpha)
        dist = Counter()
        bad = []
        for mask in range(1, (1 << h) - 1):
            rank = product_rank(p, h, m, alpha, mask, lagrange)
            dist[rank] += 1
            if rank < M and len(bad) < 10:
                bad.append({"mask": mask, "rank": rank})
        results.append({
            "alpha": alpha,
            "M": M,
            "distribution": dict(sorted(dist.items())),
            "bad_examples": bad,
        })
    return {
        "p": p, "h": h, "m": m,
        "nonconstant_patterns": (1 << h) - 2,
        "all_primitive_roots": all_primitive_roots,
        "results": results,
    }


def selected_case(p, h, m):
    M = 1 + m + m * (m - 1) // 2
    alpha = primitive_roots(p)[0]
    lagrange = precompute_lagrange(p, h, m, alpha)
    masks = {
        "singleton": 1,
        "two_adjacent": 3,
        "alternating": sum(1 << i for i in range(0, h, 2)),
        "first_half": (1 << (h // 2)) - 1,
        "structured_mod7": sum(
            1 << i for i in range(h) if (i * i + 3 * i + 1) % 7 < 3
        ),
    }
    return {
        "p": p, "h": h, "m": m, "alpha": alpha, "M": M,
        "ranks": {
            name: product_rank(p, h, m, alpha, mask, lagrange)
            for name, mask in masks.items()
        },
    }


def main():
    result = {
        "status": "COMPUTATIONAL",
        "model": "declared SU05 Eq.(7) univariate orbit + standard binary-label Hadamard inner code",
        "seed": None,
        "limitations": [
            "Finite experiments only.",
            "Not a proof of the all-parameter nonconstant-leaf conjecture.",
            "Not a full transcription of every bit-level choice in the vMS local extractor.",
        ],
        "exhaustive": [
            exhaustive_case(17, 4, 4),
            exhaustive_case(29, 5, 5),
            exhaustive_case(37, 6, 6),
            exhaustive_case(43, 7, 7),
            exhaustive_case(53, 8, 8),
            exhaustive_case(31, 6, 8, all_primitive_roots=True),
        ],
        "selected_large": [
            selected_case(257, 16, 16),
            selected_case(257, 16, 32),
            selected_case(257, 32, 32),
            selected_case(257, 64, 64),
        ],
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
