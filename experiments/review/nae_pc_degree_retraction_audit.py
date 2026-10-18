#!/usr/bin/env python3
"""Finite/symbolic audit for the pin-free NAE gauge PC retraction.

Polynomials are represented in the Boolean quotient
F[x_1,...,x_n]/<x_i^2-x_i>.  Multiplication therefore unions monomial
supports.  This checker does not search for PC refutations.  It checks every
signed source-clause pattern over several characteristics, the complete local
truth tables, the auxiliary Boolean-axiom images, the equality-chain images,
and the exact expanded-monomial growth of the degree-two substitution.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path


Poly = dict[tuple[str, ...], int]


def norm(poly: Poly, prime: int) -> Poly:
    return {m: c % prime for m, c in poly.items() if c % prime}


def const(value: int, prime: int) -> Poly:
    return norm({(): value}, prime)


def var(name: str, prime: int) -> Poly:
    return {(name,): 1 % prime}


def add(a: Poly, b: Poly, prime: int) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
    return norm(out, prime)


def neg(a: Poly, prime: int) -> Poly:
    return norm({m: -c for m, c in a.items()}, prime)


def sub(a: Poly, b: Poly, prime: int) -> Poly:
    return add(a, neg(b, prime), prime)


def mul(a: Poly, b: Poly, prime: int) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            # Boolean quotient: x^k = x for every positive k.
            m = tuple(sorted(set(ma).union(mb)))
            out[m] = out.get(m, 0) + ca * cb
    return norm(out, prime)


def one_minus(a: Poly, prime: int) -> Poly:
    return sub(const(1, prime), a, prime)


def literal(name: str, positive: bool, prime: int) -> Poly:
    x = var(name, prime)
    return x if positive else one_minus(x, prime)


def prod(parts: list[Poly], prime: int) -> Poly:
    out = const(1, prime)
    for p in parts:
        out = mul(out, p, prime)
    return out


def max_degree(p: Poly) -> int:
    return max((len(m) for m in p), default=-1)


def nae_axioms(a: Poly, b: Poly, c: Poly, prime: int) -> tuple[Poly, Poly]:
    all_one = prod([a, b, c], prime)
    all_zero = prod([one_minus(a, prime), one_minus(b, prime), one_minus(c, prime)], prime)
    return all_one, all_zero


def eval_lit(bit: int, positive: bool) -> int:
    return bit if positive else 1 - bit


def nae(a: int, b: int, c: int) -> bool:
    return not (a == b == c)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    primes = [2, 3, 5, 7, 11]
    checks = 0
    failures: list[dict[str, object]] = []
    field_rows: list[dict[str, object]] = []

    # Exhaust the three independent source-literal polarities.
    for prime in primes:
        local_checks = 0
        for signs in itertools.product([False, True], repeat=3):
            a = literal("x0", signs[0], prime)
            b = literal("x1", signs[1], prime)
            c = literal("x2", signs[2], prime)
            r = one_minus(a, prime)
            s = one_minus(b, prime)
            u = mul(r, s, prime)

            # First NAE(a,b,u): both forbidden-row polynomials vanish in the
            # Boolean quotient.
            f1, f0 = nae_axioms(a, b, u, prime)
            for label, got in (("first_all_one", f1), ("first_all_zero", f0)):
                checks += 1
                local_checks += 1
                if got:
                    failures.append({"prime": prime, "signs": signs, "identity": label, "value": got})

            # Second NAE(not u,c,z) under z=0: one axiom is zero and the
            # other is exactly the source-clause falsity polynomial.
            z0 = const(0, prime)
            g1, g0 = nae_axioms(one_minus(u, prime), c, z0, prime)
            source = prod([one_minus(a, prime), one_minus(b, prime), one_minus(c, prime)], prime)
            for label, got, want in (
                ("second_all_one", g1, const(0, prime)),
                ("second_all_zero", g0, source),
            ):
                checks += 1
                local_checks += 1
                if got != want:
                    failures.append({"prime": prime, "signs": signs, "identity": label, "got": got, "want": want})

            # Target Boolean axiom u^2-u maps into the source Boolean ideal.
            ub = sub(mul(u, u, prime), u, prime)
            checks += 1
            local_checks += 1
            if ub:
                failures.append({"prime": prime, "signs": signs, "identity": "u_boolean", "value": ub})

        # Equality-gadget clauses under z_i=z_{i+1}=e_i=0.
        zero = const(0, prime)
        one = const(1, prime)
        for third in (zero, one):
            q1, q0 = nae_axioms(zero, one, third, prime)
            for label, got in (("eq_all_one", q1), ("eq_all_zero", q0)):
                checks += 1
                local_checks += 1
                if got:
                    failures.append({"prime": prime, "identity": label, "third": third, "value": got})
        field_rows.append({"prime": prime, "checks": local_checks, "failures": sum(1 for x in failures if x.get("prime") == prime)})

    # Complete semantic clause truth table, all signed patterns and assignments.
    semantic_rows = 0
    for signs in itertools.product([False, True], repeat=3):
        for bits in itertools.product([0, 1], repeat=3):
            av, bv, cv = [eval_lit(bits[i], signs[i]) for i in range(3)]
            source_sat = bool(av or bv or cv)
            target_sat = any(nae(av, bv, u) and nae(1 - u, cv, 0) for u in (0, 1))
            checks += 1
            semantic_rows += 1
            if source_sat != target_sat:
                failures.append({"identity": "semantic_clause", "signs": signs, "bits": bits})

    # The substitution of d pairwise-disjoint u variables has exactly 4^d
    # expanded multilinear monomials and degree 2d over every tested field.
    expansion_rows: list[dict[str, int]] = []
    for prime in primes:
        acc = const(1, prime)
        for d in range(1, 9):
            factor = mul(one_minus(var(f"a{d}", prime), prime), one_minus(var(f"b{d}", prime), prime), prime)
            acc = mul(acc, factor, prime)
            row = {"prime": prime, "d": d, "monomials": len(acc), "expected_monomials": 4**d, "degree": max_degree(acc), "expected_degree": 2*d}
            expansion_rows.append(row)
            checks += 2
            if row["monomials"] != row["expected_monomials"] or row["degree"] != row["expected_degree"]:
                failures.append({"identity": "expansion", **row})

    script_path = Path(__file__)
    result = {
        "run_id": "NAEPC2D1",
        "status": "PASS" if not failures else "FAIL",
        "method": "exhaustive signed local identities plus exact Boolean-quotient arithmetic",
        "random_seed": None,
        "fields": primes,
        "field_rows": field_rows,
        "semantic_truth_rows": semantic_rows,
        "expansion_rows": expansion_rows,
        "assertions": checks,
        "failures": failures,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "limitations": [
            "Does not search for or minimize PC/PCR refutations.",
            "Checks the gauge-chain interface only; no FTNC, ONE3, NOT-ONE3, or REVFIX2 definition was available.",
            "Finite field checks support but do not replace the characteristic-free symbolic proof.",
        ],
        "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
