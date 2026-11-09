#!/usr/bin/env python3
"""Exact finite controls for the LSPV-5/457 affine-projection lemma.

This is an independent verifier, not the historical R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import time


def one_hot_tuple(labels: tuple[int, ...], q: int) -> int:
    out = 0
    for i, a in enumerate(labels):
        out |= 1 << (i * q + a)
    return out


def boundary_sets(q: int, b: int, eps: tuple[int, ...], charge: int):
    universe = []
    valid = []
    for labels in itertools.product(range(q), repeat=b):
        word = one_hot_tuple(labels, q)
        universe.append(word)
        if sum(eps[i] * labels[i] for i in range(b)) % q == charge % q:
            valid.append(word)
    return valid, universe


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


def affine_dimension(points: list[int]) -> int:
    if not points:
        return -1
    base = points[0]
    return gf2_rank([x ^ base for x in points[1:]])


def parity(x: int) -> int:
    return x.bit_count() & 1


def separating_row(valid: list[int], universe: list[int], n: int):
    for mask in range(1, 1 << n):
        value = parity(mask & valid[0])
        if all(parity(mask & x) == value for x in valid) and any(
            parity(mask & x) != value for x in universe
        ):
            return mask, value
    return None


def exhaustive_equation_controls(valid: list[int], universe: list[int], n: int):
    equations = [(mask, c) for mask in range(1 << n) for c in (0, 1)]
    containing = []
    bad_single = 0
    for mask, c in equations:
        if all(parity(mask & x) == c for x in valid):
            containing.append((mask, c))
            if not all(parity(mask & x) == c for x in universe):
                bad_single += 1

    # Any projection of a two-row affine system is described by at most two
    # affine equations on visible coordinates. Enumerate every such pair that
    # contains S. Because each member of `containing` already contains U, the
    # pair must contain U as well; still replay the intersection explicitly.
    pairs = 0
    bad_pairs = 0
    for i, e1 in enumerate(containing):
        for e2 in containing[i:]:
            pairs += 1
            if any(
                not (
                    parity(e1[0] & x) == e1[1]
                    and parity(e2[0] & x) == e2[1]
                )
                for x in universe
            ):
                bad_pairs += 1
    return {
        "all_equations": len(equations),
        "equations_containing_valid_set": len(containing),
        "bad_single_equations": bad_single,
        "equation_pairs_containing_valid_set": pairs,
        "bad_equation_pairs": bad_pairs,
    }


def nonlinear_mod3_extension(labels: tuple[int, ...], eps: tuple[int, ...], charge: int):
    # Existential state witnesses for s_{i+1}=s_i+eps_i*a_i (mod 3), s_0=0.
    states = [0]
    for e, a in zip(eps, labels):
        states.append((states[-1] + e * a) % 3)
    return states[-1] == charge % 3, tuple(states)


def run():
    started = time.time()
    checks = 0
    odd_cases = []
    for b in (3, 4, 5):
        q = 3
        eps = tuple(1 if i % 2 == 0 else -1 for i in range(b))
        valid, universe = boundary_sets(q, b, eps, charge=1)
        dv = affine_dimension(valid)
        du = affine_dimension(universe)
        assert dv == du == b * (q - 1)
        assert separating_row(valid, universe, b * q) is None
        checks += 3
        odd_cases.append(
            {
                "q": q,
                "b": b,
                "eps": eps,
                "charge": 1,
                "valid_count": len(valid),
                "universe_count": len(universe),
                "affine_dimension_valid": dv,
                "affine_dimension_universe": du,
            }
        )

    valid, universe = boundary_sets(3, 3, (1, -1, 1), charge=1)
    exhaustive = exhaustive_equation_controls(valid, universe, 9)
    assert exhaustive["bad_single_equations"] == 0
    assert exhaustive["bad_equation_pairs"] == 0
    checks += exhaustive["all_equations"] + exhaustive["equation_pairs_containing_valid_set"]

    hostile = []
    for q, b, eps, charge in [
        (2, 3, (1, 1, 1), 1),
        (3, 2, (1, -1), 1),
    ]:
        s, u = boundary_sets(q, b, eps, charge)
        witness = separating_row(s, u, q * b)
        assert witness is not None
        checks += 1
        hostile.append(
            {
                "q": q,
                "b": b,
                "affine_dimension_valid": affine_dimension(s),
                "affine_dimension_universe": affine_dimension(u),
                "separating_mask": witness[0],
                "separating_constant": witness[1],
            }
        )

    eps = (1, -1, 1, -1)
    accepted = rejected = 0
    witness_hash = hashlib.sha256()
    for labels in itertools.product(range(3), repeat=4):
        ok, states = nonlinear_mod3_extension(labels, eps, 1)
        expected = sum(eps[i] * labels[i] for i in range(4)) % 3 == 1
        assert ok == expected
        witness_hash.update(bytes(labels + states))
        accepted += int(ok)
        rejected += int(not ok)
        checks += 1
    assert accepted == 27 and rejected == 54

    result = {
        "status": "PASS",
        "scope": "pure affine GF(2) auxiliary systems only; not R_mix341",
        "theorem_under_test": (
            "if aff(S)=aff(U), R={(x,y):Ax+By=c}, and every s in S has a lift, "
            "then every u in U has a lift"
        ),
        "odd_modulus_cases": odd_cases,
        "exhaustive_q3_b3_projected_equations": exhaustive,
        "hostile_boundary_controls": hostile,
        "nonlinear_mod3_state_control": {
            "b": 4,
            "accepted_valid_tuples": accepted,
            "rejected_wrong_tuples": rejected,
            "witness_stream_sha256": witness_hash.hexdigest(),
            "meaning": "nonlinear state transitions evade the affine projection lemma",
        },
        "checks": checks,
        "elapsed_seconds": round(time.time() - started, 6),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "python": sys.version.split()[0],
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    run()
