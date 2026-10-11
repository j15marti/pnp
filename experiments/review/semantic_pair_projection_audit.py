#!/usr/bin/env python3
"""Finite audit for SEMCOMP-EXTRACT1 and PAIR-PROJECTION-NOGLUE1.

The exhaustive n=6 clean-core search is a finite diagnostic.  The Tseitin
parity assertions instantiate the symbolic no-gluing family from the report.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import time
from collections import defaultdict
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def canonical(cnf: CNF) -> CNF:
    clauses = [tuple(sorted(clause, key=lambda lit: (abs(lit), lit < 0))) for clause in cnf]
    return tuple(sorted(clauses, key=lambda clause: tuple((abs(lit), lit < 0) for lit in clause)))


def assert_h22(cnf: CNF, n: int) -> None:
    assert len(cnf) == 4 * n // 3
    assert len(set(cnf)) == len(cnf)
    for clause in cnf:
        assert len(clause) == 3 and len(set(map(abs, clause))) == 3
        assert all(lit > 0 for lit in clause) or all(lit < 0 for lit in clause)
    for v in range(1, n + 1):
        assert sum(v in clause for clause in cnf) == 2
        assert sum(-v in clause for clause in cnf) == 2


def satisfies(cnf: CNF, assignment: int) -> bool:
    for clause in cnf:
        if not any(bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def solution_mask(cnf: CNF, nvars: int) -> int:
    mask = 0
    for a in range(1 << nvars):
        if satisfies(cnf, a):
            mask |= 1 << a
    return mask


def projected_original_mask(cnf: CNF, total_vars: int, original_n: int) -> int:
    mask = 0
    low = (1 << original_n) - 1
    for a in range(1 << total_vars):
        if satisfies(cnf, a):
            mask |= 1 << (a & low)
    return mask


def pair_signature_from_mask(mask: int, n: int) -> tuple[int, ...]:
    sig: list[int] = []
    for i in range(n):
        for bit in (0, 1):
            sig.append(int(any(((a >> i) & 1) == bit for a in range(1 << n) if (mask >> a) & 1)))
    for i in range(n):
        for j in range(i + 1, n):
            for bi in (0, 1):
                for bj in (0, 1):
                    sig.append(int(any(
                        ((a >> i) & 1) == bi and ((a >> j) & 1) == bj
                        for a in range(1 << n) if (mask >> a) & 1
                    )))
    return tuple(sig)


def projection_signature(mask: int, n: int, k: int) -> tuple[int, ...]:
    sig: list[int] = []
    for scope in itertools.combinations(range(n), k):
        for values in itertools.product((0, 1), repeat=k):
            sig.append(int(any(
                all(((a >> v) & 1) == b for v, b in zip(scope, values))
                for a in range(1 << n) if (mask >> a) & 1
            )))
    return tuple(sig)


def xor_gate(a: int, b: int, c: int) -> tuple[Clause, ...]:
    return ((a, b, -c), (a, -b, c), (-a, b, c), (-a, -b, -c))


def pin_proper(lit: int, p: int, q: int) -> tuple[Clause, ...]:
    return ((lit, p, q), (lit, p, -q), (lit, -p, q), (lit, -p, -q))


def parity_tseitin(n: int, parity: int) -> tuple[CNF, int]:
    assert n >= 2 and parity in (0, 1)
    clauses: list[Clause] = []
    prev = 1
    next_var = n + 1
    for x in range(2, n + 1):
        out = next_var
        next_var += 1
        clauses.extend(xor_gate(prev, x, out))
        prev = out
    p, q = next_var, next_var + 1
    clauses.extend(pin_proper(prev if parity else -prev, p, q))
    return tuple(clauses), q


def h22_designs(n: int) -> list[tuple[Clause, ...]]:
    assert (4 * n) % 3 == 0
    edges = list(itertools.combinations(range(1, n + 1), 3))
    need = 2 * n // 3
    designs = []
    for chosen in itertools.combinations(edges, need):
        degree = [0] * (n + 1)
        for edge in chosen:
            for v in edge:
                degree[v] += 1
        if all(degree[v] == 2 for v in range(1, n + 1)):
            designs.append(tuple(chosen))
    return designs


def exhaustive_h22_pair_search(n: int) -> dict:
    designs = h22_designs(n)
    buckets: dict[tuple[int, ...], list[tuple[int, CNF]]] = defaultdict(list)
    formulas = 0
    satisfiable = 0
    collisions = 0
    witness = None
    for pos in designs:
        for neg0 in designs:
            cnf = canonical(tuple(pos) + tuple(tuple(-v for v in edge) for edge in neg0))
            assert_h22(cnf, n)
            formulas += 1
            mask = solution_mask(cnf, n)
            if not mask:
                continue
            satisfiable += 1
            sig = pair_signature_from_mask(mask, n)
            for old_mask, old_cnf in buckets[sig]:
                collisions += 1
                if old_mask & mask == 0 and witness is None:
                    witness = {
                        "formula_a": old_cnf,
                        "formula_b": cnf,
                        "solutions_a": old_mask.bit_count(),
                        "solutions_b": mask.bit_count(),
                        "signature_bits": len(sig),
                    }
                    break
            buckets[sig].append((mask, cnf))
    return {
        "n": n,
        "designs": len(designs),
        "formulas": formulas,
        "satisfiable_formulas": satisfiable,
        "pair_signature_buckets": len(buckets),
        "same_signature_pair_comparisons": collisions,
        "disjoint_solution_pair": witness,
    }


def random_h22(n: int, rng: random.Random) -> CNF:
    pos = [v for v in range(1, n + 1) for _ in range(2)]
    neg = [-v for v in range(1, n + 1) for _ in range(2)]
    while True:
        rng.shuffle(pos)
        rng.shuffle(neg)
        clauses = [tuple(pos[i:i + 3]) for i in range(0, 2 * n, 3)]
        clauses += [tuple(neg[i:i + 3]) for i in range(0, 2 * n, 3)]
        if all(len(set(map(abs, c))) == 3 for c in clauses):
            cnf = canonical(tuple(clauses))
            if len(set(cnf)) != len(cnf):
                continue
            assert_h22(cnf, n)
            return cnf


def sampled_h22_pair_search(n: int, samples: int, seed: int) -> dict:
    rng = random.Random(seed)
    buckets: dict[tuple[int, ...], list[tuple[int, CNF]]] = defaultdict(list)
    comparisons = 0
    witness = None
    for _ in range(samples):
        cnf = random_h22(n, rng)
        mask = solution_mask(cnf, n)
        if not mask:
            continue
        sig = pair_signature_from_mask(mask, n)
        for old_mask, old_cnf in buckets[sig]:
            comparisons += 1
            if old_mask & mask == 0:
                witness = {
                    "formula_a": old_cnf,
                    "formula_b": cnf,
                    "solutions_a": old_mask.bit_count(),
                    "solutions_b": mask.bit_count(),
                    "signature_bits": len(sig),
                }
                break
        buckets[sig].append((mask, cnf))
        if witness is not None:
            break
    return {
        "n": n,
        "requested_samples": samples,
        "generated_samples": sum(len(v) for v in buckets.values()),
        "pair_signature_buckets": len(buckets),
        "same_signature_pair_comparisons": comparisons,
        "disjoint_solution_pair": witness,
    }


def run(max_parity_n: int, h22_samples: int, h22_pair_samples: int, seed: int) -> dict:
    started = time.perf_counter()
    parity_checks = 0
    parity_rows = []
    for n in range(3, max_parity_n + 1):
        even, total_even = parity_tseitin(n, 0)
        odd, total_odd = parity_tseitin(n, 1)
        assert total_even == total_odd == 2 * n + 1
        even_mask = projected_original_mask(even, total_even, n)
        odd_mask = projected_original_mask(odd, total_odd, n)
        assert even_mask & odd_mask == 0
        assert (even_mask | odd_mask) == (1 << (1 << n)) - 1
        for k in (1, 2):
            se = projection_signature(even_mask, n, k)
            so = projection_signature(odd_mask, n, k)
            assert se == so and all(se)
            parity_checks += len(se) * 2 + 2
        parity_rows.append({
            "n": n,
            "clauses_each": len(even),
            "variables_each": total_even,
            "solutions_each": even_mask.bit_count(),
            "pair_signature_all_ones": True,
            "disjoint_original_solution_sets": True,
        })

    clean_exhaustive = exhaustive_h22_pair_search(6)
    clean_sampled_pair = sampled_h22_pair_search(9, h22_pair_samples, seed ^ 0xBEEF)

    rng = random.Random(seed)
    random_checks = 0
    random_rows = []
    for n in (6, 9, 12):
        for _ in range(h22_samples):
            cnf = random_h22(n, rng)
            mask = solution_mask(cnf, n)
            sig = pair_signature_from_mask(mask, n)
            assert len(sig) == 2 * n + 4 * (n * (n - 1) // 2)
            random_checks += len(sig) + 1
            random_rows.append({"n": n, "sat": bool(mask), "solutions": mask.bit_count(), "signature_ones": sum(sig)})

    return {
        "run_id": "MODELBRIDGE-0005",
        "status": "PASS",
        "theorems_checked": ["SEMCOMP-EXTRACT1", "PAIR-PROJECTION-NOGLUE1"],
        "scope": "finite audit; symbolic extraction and parity proofs are in the report",
        "parameters": {
            "max_parity_n": max_parity_n,
            "h22_samples_per_size": h22_samples,
            "h22_pair_samples": h22_pair_samples,
            "seed": seed,
        },
        "parity": {
            "checks": parity_checks,
            "rows": parity_rows,
        },
        "clean_core_exhaustive": clean_exhaustive,
        "clean_core_sampled_pair_search": clean_sampled_pair,
        "clean_core_random": {
            "checks": random_checks,
            "rows": random_rows,
        },
        "global_status": "P versus NP remains OPEN",
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-parity-n", type=int, default=10)
    parser.add_argument("--h22-samples", type=int, default=12)
    parser.add_argument("--h22-pair-samples", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.max_parity_n, args.h22_samples, args.h22_pair_samples, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
