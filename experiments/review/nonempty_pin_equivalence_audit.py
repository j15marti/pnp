#!/usr/bin/env python3
"""Finite audit for NONEMPTY-PIN-EQUIVALENCE1.

The symbolic theorem is proved in the accompanying LB-0010 report.  This
script checks the clean pin-lift gadget, residual compilation, proper-3-CNF
re-encoding, and hostile representation controls on bounded instances.  It
does not infer an asymptotic lower bound from finite data.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def eval_cnf(cnf: CNF, bits: tuple[bool, ...]) -> bool:
    return all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in cnf)


def sat(cnf: CNF, nvars: int) -> bool:
    return any(eval_cnf(cnf, bits) for bits in itertools.product((False, True), repeat=nvars))


def restrict_cnf(cnf: CNF, rho: dict[int, bool]) -> CNF:
    out: list[Clause] = []
    for clause in cnf:
        residual: list[int] = []
        satisfied = False
        for lit in clause:
            var = abs(lit)
            if var not in rho:
                residual.append(lit)
            elif rho[var] == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return tuple(out)


def normalize_clause(clause: Clause) -> Clause | None:
    seen: set[int] = set()
    out: list[int] = []
    for lit in clause:
        if -lit in seen:
            return None
        if lit not in seen:
            seen.add(lit)
            out.append(lit)
    return tuple(out)


def to_proper_3cnf(cnf: CNF, nvars: int) -> tuple[CNF, int]:
    """Linear equisatisfiable conversion for clauses of width at most three."""
    out: list[Clause] = []
    fresh = nvars
    for raw in cnf:
        clause = normalize_clause(raw)
        if clause is None:
            continue
        if len(clause) == 3:
            if len({abs(x) for x in clause}) != 3:
                raise AssertionError("normalization left repeated variables")
            out.append(clause)
        elif len(clause) == 2:
            fresh += 1
            x, y = clause
            out.extend(((x, y, fresh), (x, y, -fresh)))
        elif len(clause) == 1:
            fresh += 2
            x = clause[0]
            a, b = fresh - 1, fresh
            out.extend(((x, a, b), (x, a, -b), (x, -a, b), (x, -a, -b)))
        elif len(clause) == 0:
            fresh += 3
            a, b, c = fresh - 2, fresh - 1, fresh
            for signs in itertools.product((1, -1), repeat=3):
                out.append((signs[0] * a, signs[1] * b, signs[2] * c))
        else:
            raise ValueError("input clause width exceeds three")
    result = tuple(out)
    for clause in result:
        assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
    return result, fresh


def pin_lift(cnf: CNF, nvars: int, anchor: int) -> tuple[CNF, int, int]:
    """Attach a monotone, source-connected two-clause slack gadget.

    G_x(F) = F and (z or a or b) and (-z or -x or -c).
    Pinning z to either Boolean value leaves an independently satisfiable
    residual factor, so SAT(G_x(F)|z=v) iff SAT(F).
    """
    if not 1 <= anchor <= nvars:
        raise ValueError("anchor must be a source variable")
    z, a, b, c = nvars + 1, nvars + 2, nvars + 3, nvars + 4
    lifted = cnf + ((z, a, b), (-z, -anchor, -c))
    return lifted, nvars + 4, z


def validate_lift(cnf: CNF, source_clause_count: int, anchor: int, z: int) -> None:
    if len(cnf) != len(set(cnf)):
        raise AssertionError("duplicate clause")
    for clause in cnf:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            raise AssertionError("not proper 3-CNF")
    added = cnf[source_clause_count:]
    assert len(added) == 2
    assert all(x > 0 for x in added[0]) and all(x < 0 for x in added[1])
    assert z in added[0] and -z in added[1]
    assert -anchor in added[1]


def gamma_length(x: int) -> int:
    if x < 1:
        return 1
    return 2 * int(math.log2(x)) + 1


def canonical_proper3_bits(cnf: CNF, nvars: int) -> int:
    width = max(1, math.ceil(math.log2(nvars + 1)))
    return gamma_length(nvars + 1) + gamma_length(len(cnf) + 1) + len(cnf) * 3 * (width + 1)


def signed_proper_clauses_three_vars() -> tuple[Clause, ...]:
    return tuple(tuple(sign * (i + 1) for i, sign in enumerate(signs))
                 for signs in itertools.product((1, -1), repeat=3))


def cyclic_cubic_bipartite(r: int) -> list[tuple[int, int]]:
    return sorted((u, (u + shift) % r) for u in range(r) for shift in (0, 1, 2))


def paired_h22(r: int) -> tuple[CNF, int]:
    edges = cyclic_cubic_bipartite(r)
    at_u = [[] for _ in range(r)]
    at_w = [[] for _ in range(r)]
    for var, (u, w) in enumerate(edges, 1):
        at_u[u].append(var)
        at_w[w].append(var)
    clauses: list[Clause] = []
    for inc in at_u + at_w:
        clause = tuple(sorted(inc))
        clauses.extend((clause, tuple(-x for x in clause)))
    return tuple(sorted(clauses)), len(edges)


def rename(cnf: CNF, permutation: dict[int, int]) -> CNF:
    return tuple(tuple((1 if lit > 0 else -1) * permutation[abs(lit)] for lit in clause)
                 for clause in cnf)


def complement(cnf: CNF) -> CNF:
    return tuple(tuple(-lit for lit in clause) for clause in cnf)


def run(seed: int, random_formulas: int) -> dict:
    started = time.perf_counter()
    rng = random.Random(seed)
    counts = {
        "exhaustive_pin_equivalences": 0,
        "proper3_reencoding_equivalences": 0,
        "clean_h22_pin_equivalences": 0,
        "random_pin_equivalences": 0,
        "encoding_length_checks": 0,
        "wrapper_checks": 0,
        "direct_recomp_checks": 0,
        "independent_product_checks": 0,
        "easy_source_shortcut_checks": 0,
    }
    max_length_ratio = 0.0

    base_clauses = signed_proper_clauses_three_vars()
    for mask in range(1 << len(base_clauses)):
        source = tuple(base_clauses[i] for i in range(len(base_clauses)) if (mask >> i) & 1)
        source_sat = sat(source, 3)
        for anchor in (1, 2, 3):
            lifted, n_lifted, z = pin_lift(source, 3, anchor)
            validate_lift(lifted, len(source), anchor, z)
            assert sat(lifted, n_lifted) == source_sat
            for value in (False, True):
                residual = restrict_cnf(lifted, {z: value})
                residual_sat = sat(residual, n_lifted)
                assert residual_sat == source_sat
                counts["exhaustive_pin_equivalences"] += 1

                encoded, n_encoded = to_proper_3cnf(residual, n_lifted)
                assert sat(encoded, n_encoded) == source_sat
                counts["proper3_reencoding_equivalences"] += 1

                # DIRECT returns the bit; RECOMP rebuilds the same coordinate.
                assert sat(restrict_cnf(lifted, {z: value}), n_lifted) == residual_sat
                assert sat(restrict_cnf(lifted, {z: value}), n_lifted) == residual_sat
                counts["direct_recomp_checks"] += 2

            source_bits = canonical_proper3_bits(source, 3)
            lifted_bits = canonical_proper3_bits(lifted, n_lifted)
            assert lifted_bits <= 8 * source_bits + 256
            max_length_ratio = max(max_length_ratio, lifted_bits / max(1, source_bits))
            counts["encoding_length_checks"] += 1

        if mask % 17 == 0:
            lifted, n_lifted, z = pin_lift(source, 3, 1)
            truth = source_sat

            shuffled = list(lifted)
            rng.shuffle(shuffled)
            assert sat(restrict_cnf(tuple(shuffled), {z: False}), n_lifted) == truth
            counts["wrapper_checks"] += 1

            variables = list(range(1, n_lifted + 1))
            image = variables[:]
            rng.shuffle(image)
            perm = dict(zip(variables, image))
            renamed = rename(lifted, perm)
            assert sat(restrict_cnf(renamed, {perm[z]: False}), n_lifted) == truth
            counts["wrapper_checks"] += 1

            comp = complement(lifted)
            assert sat(restrict_cnf(comp, {z: True}), n_lifted) == truth
            counts["wrapper_checks"] += 1

            copied = lifted + lifted
            assert sat(restrict_cnf(copied, {z: False}), n_lifted) == truth
            counts["wrapper_checks"] += 1

            dead_var = n_lifted + 1
            dead = lifted + ((dead_var, -dead_var, dead_var + 1),)
            assert sat(restrict_cnf(dead, {z: False}), n_lifted + 2) == truth
            counts["wrapper_checks"] += 1

            serialized = json.dumps(lifted)
            interpreted = tuple(tuple(int(x) for x in clause) for clause in json.loads(serialized))
            assert sat(restrict_cnf(interpreted, {z: False}), n_lifted) == truth
            counts["wrapper_checks"] += 1

    # Exact H_(2,2) controls from cubic bipartite paired clauses.
    for r in (3, 4):
        source, nvars = paired_h22(r)
        source_sat = sat(source, nvars)
        for anchor in range(1, min(nvars, 6) + 1):
            lifted, n_lifted, z = pin_lift(source, nvars, anchor)
            validate_lift(lifted, len(source), anchor, z)
            for value in (False, True):
                assert sat(restrict_cnf(lifted, {z: value}), n_lifted) == source_sat
                counts["clean_h22_pin_equivalences"] += 1

    # Seeded proper-3-CNF controls on four variables.
    universe = []
    for variables in itertools.combinations(range(1, 5), 3):
        for signs in itertools.product((1, -1), repeat=3):
            universe.append(tuple(v * s for v, s in zip(variables, signs)))
    for _ in range(random_formulas):
        source = tuple(rng.sample(universe, rng.randint(1, min(18, len(universe)))))
        truth = sat(source, 4)
        anchor = rng.randint(1, 4)
        lifted, n_lifted, z = pin_lift(source, 4, anchor)
        for value in (False, True):
            assert sat(restrict_cnf(lifted, {z: value}), n_lifted) == truth
            counts["random_pin_equivalences"] += 1

    # Independent products preserve conjunction and do not force a joint table.
    samples = [tuple(base_clauses[i] for i in range(8) if (mask >> i) & 1)
               for mask in range(0, 256, 17)]
    for left, right0 in zip(samples, reversed(samples)):
        shift = 3
        right = tuple(tuple((1 if lit > 0 else -1) * (abs(lit) + shift) for lit in clause)
                      for clause in right0)
        product = left + right
        truth = sat(left, 3) and sat(right0, 3)
        lifted, n_lifted, z = pin_lift(product, 6, 1)
        assert sat(restrict_cnf(lifted, {z: False}), n_lifted) == truth
        counts["independent_product_checks"] += 1

    # Easy semantic controls: unit/Horn, 2-CNF equality, and affine parity CNF.
    easy_sources: list[tuple[CNF, int]] = [
        (((1,), (-1, 2), (-2, 3)), 3),
        (((-1, 2), (1, -2), (-2, 3), (2, -3)), 3),
        (((1, 2, 3), (1, -2, -3), (-1, 2, -3), (-1, -2, 3)), 3),
        (((1,), (-1,)), 1),
    ]
    for source, nvars in easy_sources:
        truth = sat(source, nvars)
        lifted, n_lifted, z = pin_lift(source, nvars, 1)
        for value in (False, True):
            assert sat(restrict_cnf(lifted, {z: value}), n_lifted) == truth
            counts["easy_source_shortcut_checks"] += 1

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "LB-0010",
        "seed": seed,
        "status": "COMPUTATIONAL",
        "claim_checked": "NONEMPTY-PIN-EQUIVALENCE1 finite regression",
        "exhaustive": "all 256 subsets of the eight signed proper clauses on three variables, all three anchors, both pin values",
        "random_formulas": random_formulas,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "max_observed_lift_to_source_bit_ratio": max_length_ratio,
        "seconds": elapsed,
        "limitations": [
            "Finite tests do not prove asymptotic hardness.",
            "The symbolic theorem, not this audit, proves linear interreducibility.",
            "The pin-lift leaves degree-one slack variables and is not itself H_(2,2).",
        ],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610110912)
    parser.add_argument("--random-formulas", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed, args.random_formulas)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("sha256=" + hashlib.sha256(payload.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
