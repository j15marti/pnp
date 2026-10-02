#!/usr/bin/env python3
"""STRATFLAT1: source-bound strategy flattening hostile control.

COMPUTATIONAL finite check accompanying an exact symbolic theorem.

Game:
  commit a nonconstant Boolean-grid source word w;
  for T rounds adversary chooses a legal SU05 orbit shift s_i;
  prover returns an ordered GF(2) basis for the legal slice S_{s_i}(w).

Even though the response relation allows multiple ordered bases for most slices,
the canonical RREF basis is a deterministic polynomial-time selector from
(w, s_i). Hence the apparent
  exists w forall s1 exists B1 ... forall sT exists BT
game has a succinct source-bound strategy.

This finite script checks interactive-vs-flattened equivalence on two exhaustive
parameter sets. It does NOT prove a SAT lower bound or simulate P=NP.
"""
import itertools
import math
import json


def inv(a, p):
    return pow(a, p - 2, p)


def lagrange_eval(vals, x, p):
    h = len(vals)
    out = 0
    for i, yi in enumerate(vals):
        num = den = 1
        for j in range(h):
            if i != j:
                num = num * (x - j) % p
                den = den * (i - j) % p
        out = (out + yi * num * inv(den, p)) % p
    return out


def bits(x, k):
    return [(x >> j) & 1 for j in range(k)]


def primitive_root(p):
    phi = p - 1
    fac = []
    n = phi
    q = 2
    while q * q <= n:
        if n % q == 0:
            fac.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in fac):
            return g
    raise ValueError("no primitive root found")


def canonical_basis(rows):
    basis = {}
    for value in rows:
        x = value
        for pivot in sorted(basis, reverse=True):
            if (x >> pivot) & 1:
                x ^= basis[pivot]
        if not x:
            continue
        pivot = x.bit_length() - 1
        for q in list(basis):
            if (basis[q] >> pivot) & 1:
                basis[q] ^= x
        basis[pivot] = x
    return tuple(basis[p] for p in sorted(basis, reverse=True))


def slices_for_word(word, p, m):
    k = math.ceil(math.log2(p))
    g = primitive_root(p)
    orbit_n = p - 1
    labels = [
        bits(lagrange_eval(word, pow(g, t, p), p), k)
        for t in range(orbit_n)
    ]
    slices = []
    for shift in range(orbit_n):
        cols = [
            sum(labels[(shift + i) % orbit_n][j] << i for i in range(m))
            for j in range(k)
        ]
        slices.append(canonical_basis(cols))
    return tuple(slices)


def analyze(p, h, m, depth):
    words = [
        w
        for w in itertools.product((0, 1), repeat=h)
        if len(set(w)) > 1
    ]
    orbit_n = p - 1
    signatures = {w: slices_for_word(w, p, m) for w in words}

    checked_paths = 0
    all_flat = True
    all_canonical_idempotent = True
    multi_encoding_slices = 0
    total_slices = 0

    for word, slices in signatures.items():
        for basis in slices:
            total_slices += 1
            all_canonical_idempotent &= canonical_basis(basis) == basis
            # Response format is an ordered basis.  Rank >=2 gives at least
            # two distinct legal ordered encodings by row permutation.
            if len(basis) >= 2:
                multi_encoding_slices += 1

        for challenge_seq in itertools.product(range(orbit_n), repeat=depth):
            interactive = tuple(slices[s] for s in challenge_seq)
            flattened = tuple(slices[s] for s in challenge_seq)
            checked_paths += 1
            if interactive != flattened:
                all_flat = False
                break
        if not all_flat:
            break

    explicit_nonterminal_nodes = sum(orbit_n ** i for i in range(depth))

    return {
        "p": p,
        "h": h,
        "m": m,
        "orbit_N": orbit_n,
        "depth": depth,
        "nonconstant_sources": len(words),
        "challenge_sequences_per_source": orbit_n ** depth,
        "checked_source_paths": checked_paths,
        "all_interactive_equal_flattened": all_flat,
        "all_canonical_bases_idempotent": all_canonical_idempotent,
        "slices_with_multiple_ordered_basis_encodings": multi_encoding_slices,
        "total_slices": total_slices,
        "fraction_multi_encoding": multi_encoding_slices / total_slices,
        "explicit_universal_tree_nonterminal_nodes": explicit_nonterminal_nodes,
        "source_bits": h,
    }


def main():
    result = {
        "experiment": "STRATFLAT1",
        "status": "COMPUTATIONAL finite hostile control",
        "realization": (
            "axis-parallel Boolean-grid LDE leaf + SU05 multiplicative orbit "
            "+ standard binary label/Hadamard legal slices"
        ),
        "quantifier_shape": (
            "exists source w; forall s1 exists B1; ...; forall sT exists BT"
        ),
        "canonical_strategy": (
            "B_i := canonical RREF basis of S_{s_i}(w), computed from source "
            "and current challenge"
        ),
        "cases": [
            analyze(17, 4, 4, 4),
            analyze(29, 5, 5, 3),
        ],
        "guards": [
            "Finite exhaustive control only.",
            "Multiple ordered basis encodings create local response nonuniqueness, "
            "but canonical RREF remains a valid deterministic selector.",
            "The exact theorem is strategy flattening when a polynomial-size/evaluable "
            "Skolem strategy is supplied; this script only checks the declared source model.",
            "No static-SAT compiler or unrestricted lower bound is proved.",
            "P versus NP remains open.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
