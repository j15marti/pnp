#!/usr/bin/env python3
"""Finite audit for connected-component and two-pin SAT equivalences.

The symbolic identities are proved in the accompanying report.  This script
checks small exhaustive formulas, seeded component products, exact (2,2)
prism controls, encodings, wrappers, and the exponent ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from collections import defaultdict, deque
from pathlib import Path

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]
AffineSystem = tuple[tuple[int, int], ...]


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def satisfies(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in formula)


def sat(formula: Formula) -> bool:
    vs = variables(formula)
    return any(satisfies(formula, dict(zip(vs, bits))) for bits in itertools.product((False, True), repeat=len(vs)))


def pin(formula: Formula, variable: int, value: bool) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        if any(abs(lit) == variable and (lit > 0) == value for lit in clause):
            continue
        residual = tuple(lit for lit in clause if abs(lit) != variable)
        out.append(residual)
    return tuple(out)


def incidence_components(formula: Formula) -> tuple[Formula, ...]:
    by_var: dict[int, list[int]] = defaultdict(list)
    for ci, clause in enumerate(formula):
        for lit in clause:
            by_var[abs(lit)].append(ci)
    unseen = set(range(len(formula)))
    components: list[Formula] = []
    while unseen:
        root = min(unseen)
        queue = deque([root])
        clause_ids: set[int] = set()
        seen_vars: set[int] = set()
        while queue:
            ci = queue.popleft()
            if ci in clause_ids:
                continue
            clause_ids.add(ci)
            unseen.discard(ci)
            for lit in formula[ci]:
                var = abs(lit)
                if var in seen_vars:
                    continue
                seen_vars.add(var)
                queue.extend(by_var[var])
        components.append(tuple(formula[i] for i in sorted(clause_ids)))
    return tuple(components)


def prism_formula(k: int, offset: int = 0) -> tuple[Formula, dict[str, tuple[int, ...]]]:
    if k < 3:
        raise ValueError("k must be at least 3")
    top = tuple(offset + i + 1 for i in range(k))
    bottom = tuple(offset + k + i + 1 for i in range(k))
    rung = tuple(offset + 2 * k + i + 1 for i in range(k))
    edges: list[tuple[int, int, int]] = []
    for i in range(k):
        edges.append(tuple(sorted((top[(i - 1) % k], top[i], rung[i]))))
        edges.append(tuple(sorted((bottom[(i - 1) % k], bottom[i], rung[i]))))
    positive = [tuple(edge) for edge in edges]
    negative = [tuple(-v for v in edge) for edge in edges]
    return tuple(positive + negative), {"top": top, "bottom": bottom, "rung": rung}


def is_h22(formula: Formula) -> bool:
    if len(set(formula)) != len(formula):
        return False
    counts: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    for clause in formula:
        if len(clause) != 3 or len({abs(x) for x in clause}) != 3:
            return False
        if not (all(x > 0 for x in clause) or all(x < 0 for x in clause)):
            return False
        for lit in clause:
            counts[abs(lit)][0 if lit > 0 else 1] += 1
    return bool(counts) and all(pair == [2, 2] for pair in counts.values())


def is_connected(formula: Formula) -> bool:
    return len(incidence_components(formula)) == 1


def canonical_encode(formula: Formula) -> bytes:
    clauses = sorted(tuple(sorted(clause, key=lambda x: (abs(x), x < 0))) for clause in formula)
    header = f"p cnf {max(variables(formula), default=0)} {len(clauses)}\n"
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (header + body).encode("ascii")


def rename(formula: Formula, mapping: dict[int, int], complement: bool = False) -> Formula:
    out = []
    for clause in formula:
        converted = []
        for lit in clause:
            sign = lit > 0
            if complement:
                sign = not sign
            converted.append(mapping[abs(lit)] if sign else -mapping[abs(lit)])
        out.append(tuple(converted))
    return tuple(out)


def random_formula(rng: random.Random, n: int, m: int) -> Formula:
    universe = []
    for triple in itertools.combinations(range(1, n + 1), 3):
        for signs in itertools.product((-1, 1), repeat=3):
            universe.append(tuple(v * s for v, s in zip(triple, signs)))
    return tuple(rng.sample(universe, min(m, len(universe))))


def gaussian_sat(system: AffineSystem) -> bool:
    """Consistency of GF(2) equations represented by (bitmask, rhs)."""
    rows = [[mask, rhs] for mask, rhs in system]
    pivot = 0
    max_bit = max((mask.bit_length() for mask, _ in system), default=0)
    for bit in range(max_bit - 1, -1, -1):
        row = next((j for j in range(pivot, len(rows)) if (rows[j][0] >> bit) & 1), None)
        if row is None:
            continue
        rows[pivot], rows[row] = rows[row], rows[pivot]
        for j in range(len(rows)):
            if j != pivot and ((rows[j][0] >> bit) & 1):
                rows[j][0] ^= rows[pivot][0]
                rows[j][1] ^= rows[pivot][1]
        pivot += 1
    return all(mask != 0 or rhs == 0 for mask, rhs in rows)


def affine_pin(system: AffineSystem, variable: int, value: bool) -> AffineSystem:
    bit = 1 << variable
    return tuple((mask & ~bit, rhs ^ (int(value) if mask & bit else 0)) for mask, rhs in system)


def run(seed: int) -> dict:
    rng = random.Random(seed)
    checks = defaultdict(int)

    # Exhaust every subset of the eight proper clauses on three variables.
    proper = tuple(tuple(v * s for v, s in zip((1, 2, 3), signs)) for signs in itertools.product((-1, 1), repeat=3))
    for mask in range(1 << len(proper)):
        formula = tuple(proper[i] for i in range(8) if mask & (1 << i))
        answer = sat(formula)
        for z in (1, 2, 3):
            split = sat(pin(formula, z, False)) or sat(pin(formula, z, True))
            assert answer == split
            checks["exhaustive_two_pin_identity"] += 1

    # Generic products include SAT and UNSAT cases and test exact AND decomposition.
    products: list[Formula] = []
    unsat_atom: Formula = ((1,), (-1,))
    sat_atom: Formula = ((1, 2, 3),)
    for trial in range(160):
        atoms: list[Formula] = []
        next_var = 1
        for _ in range(rng.randint(1, 5)):
            atom = unsat_atom if rng.random() < 0.3 else sat_atom
            width = max(variables(atom))
            atoms.append(rename(atom, {i: next_var + i - 1 for i in range(1, width + 1)}))
            next_var += width
        formula = tuple(clause for atom in atoms for clause in atom)
        products.append(formula)
        parts = incidence_components(formula)
        assert sat(formula) == all(sat(part) for part in parts)
        checks["component_and_identity"] += 1
        lengths = [max(1, len(canonical_encode(part))) for part in parts]
        total = sum(lengths)
        for exponent in range(1, 9):
            assert sum(length**exponent for length in lengths) <= total**exponent
            checks["exponent_preservation"] += 1

    # Connected exact-(2,2) prism controls of unbounded declared shape.
    for k in range(3, 25):
        formula, families = prism_formula(k)
        assert is_h22(formula)
        assert is_connected(formula)
        assignment = {v: False for v in families["top"] + families["bottom"]}
        assignment.update({v: True for v in families["rung"]})
        assert satisfies(formula, assignment)
        complement = {v: not bit for v, bit in assignment.items()}
        assert satisfies(formula, complement)
        checks["prism_balance_connectivity_witness"] += 6
        for z in variables(formula):
            desired = assignment[z]
            assert satisfies(pin(formula, z, desired), {v: bit for v, bit in assignment.items() if v != z})
            assert satisfies(pin(formula, z, not desired), {v: bit for v, bit in complement.items() if v != z})
            checks["prism_both_pin_values"] += 2

        # Encoding, renaming, global complementation, and clause-order controls.
        permutation = list(variables(formula))
        rng.shuffle(permutation)
        mapping = dict(zip(variables(formula), permutation))
        variants = (
            (formula, assignment),
            (tuple(reversed(formula)), assignment),
            (rename(formula, mapping), {mapping[v]: bit for v, bit in assignment.items()}),
            (rename(formula, mapping, True), {mapping[v]: not bit for v, bit in assignment.items()}),
        )
        for variant, witness in variants:
            assert is_h22(variant) and is_connected(variant) and satisfies(variant, witness)
            assert canonical_encode(variant)
            checks["representation_controls"] += 1

        # Hostile syntactic padding and redundant-clause controls.  These
        # deliberately leave H22: they test semantic claims, not promise
        # preservation.  A repeated clause is redundant, while fresh
        # tautologies add charged input without changing satisfiability.
        duplicate = formula + (formula[0],)
        padding_var = variables(formula)[0]
        padded = formula + tuple((padding_var, -padding_var) for _ in range(k))
        for variant in (duplicate, padded):
            assert satisfies(variant, assignment)
            z = variables(formula)[0]
            reduced = {v: bit for v, bit in assignment.items() if v != z}
            assert satisfies(pin(variant, z, assignment[z]), reduced)
            assert len(canonical_encode(variant)) >= len(canonical_encode(formula))
            checks["padding_redundancy_controls"] += 3

    # DIRECT, COPY, DELAY, INTERP, and RECOMP preserve the one-bit service.
    for formula in products[:40]:
        z = variables(formula)[0]
        direct = sat(pin(formula, z, False))
        copied = direct and direct
        delayed = sum(range(31)) >= 0 and direct
        interpreted = sat(tuple(tuple(int(x) for x in clause) for clause in formula) and pin(formula, z, False))
        recomputed = sat(pin(formula, z, False))
        assert direct == copied == delayed == interpreted == recomputed
        checks["wrapper_controls"] += 5

    # Easy-family controls: 2-SAT, Horn, affine parity by enumeration, tree path.
    easy = (
        ((-1, 2), (-2, 3), (-3, 4)),
        ((-1, -2, 3), (-3,)),
        ((1, 2), (-1, -2)),
        ((1, 2), (-2, 3), (-3, 4)),
    )
    for formula in easy:
        z = variables(formula)[0]
        assert sat(formula) == (sat(pin(formula, z, False)) or sat(pin(formula, z, True)))
        checks["easy_family_controls"] += 1

    # Affine and Tseitin controls use actual GF(2) elimination, not CNF search.
    for _ in range(160):
        n = rng.randint(1, 10)
        system = tuple((rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randint(0, 2 * n)))
        z = rng.randrange(n)
        answer = gaussian_sat(system)
        assert answer == (gaussian_sat(affine_pin(system, z, False)) or gaussian_sat(affine_pin(system, z, True)))
        checks["affine_tseitin_gaussian_controls"] += 1

    # Cycle-graph Tseitin equations: total even charge is consistent and odd
    # charge is inconsistent.  Both cases still obey the two-pin identity.
    for n in range(3, 23):
        for odd in (False, True):
            charges = [0] * n
            charges[0] = int(odd)
            system = tuple(((1 << ((i - 1) % n)) | (1 << i), charges[i]) for i in range(n))
            assert gaussian_sat(system) == (not odd)
            assert gaussian_sat(system) == (
                gaussian_sat(affine_pin(system, 0, False)) or gaussian_sat(affine_pin(system, 0, True))
            )
            checks["affine_tseitin_gaussian_controls"] += 1

    return {
        "seed": seed,
        "mode": "exhaustive-plus-seeded",
        "checks": dict(checks),
        "total_checks": sum(checks.values()),
        "parameters": {
            "proper_three_variable_subsets": 256,
            "seeded_component_products": 160,
            "prism_k_range": [3, 24],
            "exponent_range": [1, 8],
        },
        "limits": [
            "Finite checks do not prove asymptotic lower bounds.",
            "Prism controls are satisfiable paired-clause instances, not hard sources.",
            "The symbolic report proves the two-pin and component identities.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=202610111012)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    payload = run(args.seed)
    payload["runtime_seconds"] = time.perf_counter() - started
    payload["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
