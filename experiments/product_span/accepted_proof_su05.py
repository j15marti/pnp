#!/usr/bin/env python3
"""Accepted-proof constraints through a toy LDE -> SU05 -> Hadamard map.

STATUS: COMPUTATIONAL.

This experiment is deliberately one step closer to vMS Theorem 24 than the
unconstrained Boolean-grid scans:
  1. choose a family Y of "accepted" Boolean proof strings;
  2. interpolate each y in Y to its canonical univariate low-degree extension
     over F_p on the grid 0,...,h-1;
  3. apply the exact SU05 Eq.(7) univariate natural-seed orbit control;
  4. apply the declared canonical Hadamard bit projection;
  5. compute rho = rank_F2 {1,g_i,g_i g_j}.

It is NOT the exact BGH+ robust PCP verifier used by vMS Lemma 18. The point is
to test whether generic local/ideal constraints on accepted proofs are enough
to force low output Schur-square rank. Finite outcomes are not theorems.
"""

from __future__ import annotations

import itertools
import json
import random

from pnp_lab.su05_eq7 import (
    lagrange_interpolate,
    natural_domain_product_span_rank,
)

SEED = 7


def hamming_ball(h: int, radius: int) -> list[list[int]]:
    out = []
    for mask in range(1 << h):
        if mask.bit_count() <= radius:
            out.append([(mask >> i) & 1 for i in range(h)])
    return out


def circuit_tableau_proofs() -> list[list[int]]:
    """Eight-bit graph of a small deterministic Boolean circuit."""
    out = []
    for a, b, c in itertools.product((0, 1), repeat=3):
        g1 = a & b
        g2 = b ^ c
        g3 = g1 | g2
        g4 = a ^ g3
        g5 = g4 & c
        out.append([a, b, c, g1, g2, g3, g4, g5])
    return out


def accepts_cnf(msg: list[int], clauses: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> bool:
    """A clause forbids one local pattern on its listed variables."""
    return all(tuple(msg[i] for i in idxs) != pat for idxs, pat in clauses)


def random_3local_family(h: int, clause_count: int, rng: random.Random):
    clauses = []
    for _ in range(clause_count):
        idxs = tuple(sorted(rng.sample(range(h), 3)))
        pat = tuple(rng.randrange(2) for _ in range(3))
        clauses.append((idxs, pat))
    family = []
    for mask in range(1 << h):
        msg = [(mask >> i) & 1 for i in range(h)]
        if accepts_cnf(msg, clauses):
            family.append(msg)
    return family, clauses


def rho_for_message(msg: list[int], p: int, m: int) -> int:
    coeffs = lagrange_interpolate(list(range(len(msg))), msg, p)
    return natural_domain_product_span_rank(coeffs, p, m)


def summarize_family(name: str, family: list[list[int]], p: int, m: int):
    M = 1 + m + m * (m - 1) // 2
    nonconstant = [y for y in family if any(y) and not all(y)]
    ranks = [rho_for_message(y, p, m) for y in nonconstant]
    return {
        "name": name,
        "h": len(family[0]) if family else None,
        "p": p,
        "m": m,
        "M": M,
        "accepted_count": len(family),
        "nonconstant_accepted_count": len(nonconstant),
        "min_individual_rho": min(ranks) if ranks else None,
        "max_individual_rho": max(ranks) if ranks else None,
        "all_nonconstant_individual_ranks_maximal": bool(ranks) and all(r == M for r in ranks),
    }


def main():
    rng = random.Random(SEED)
    results = {
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "scope_guard": [
            "Uses the exact SU05 Eq.(7) natural-seed univariate control already in the repository.",
            "Uses canonical univariate interpolation of Boolean proof strings.",
            "Does not implement the exact BGH+ PCP verifier from vMS Lemma 18.",
            "Finite data do not prove an asymptotic statement about vMS."
        ],
        "families": [],
    }

    # The 2026 Macaulay-basis paper gives exact ideals for these varieties.
    for h, p, m in [(7, 19, 10), (8, 23, 12)]:
        for radius in (1, 2):
            results["families"].append(
                summarize_family(
                    f"hamming_ball_le_{radius}",
                    hamming_ball(h, radius),
                    p,
                    m,
                )
            )

    # Deterministic computation-tableau style validity constraints.
    results["families"].append(
        summarize_family("small_circuit_tableau", circuit_tableau_proofs(), 23, 12)
    )

    # Random local-CSP accepted-proof families.
    for h, p, m in [(7, 19, 10), (8, 23, 12), (9, 31, 12)]:
        for q in (4, 8, 10):
            family, clauses = random_3local_family(h, q, rng)
            row = summarize_family(f"random_3local_q{q}", family, p, m)
            row["clauses"] = [
                {"indices": list(idxs), "forbidden_pattern": list(pat)}
                for idxs, pat in clauses
            ]
            results["families"].append(row)

    # Canonical/unique-proof stress controls.
    for h, p, m in [(9, 31, 12), (10, 37, 14)]:
        patterns = {
            "single_one": [1] + [0] * (h - 1),
            "alternating": [i & 1 for i in range(h)],
            "prefix_half": [int(i < h // 2) for i in range(h)],
            "period3": [int(i % 3 == 0) for i in range(h)],
        }
        for label, proof in patterns.items():
            results["families"].append(
                summarize_family(f"unique_{label}", [proof], p, m)
            )

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
