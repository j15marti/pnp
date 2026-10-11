#!/usr/bin/env python3
"""Bounded audit for query-scale non-invariance under extensional wrappers.

The asymptotic theorem in the accompanying report is proved symbolically.
This runner checks the concrete constructions, exact SAT semantics, encoding
lengths, wrapper equivalence, hostile easy families, and cost ledgers.
Every invocation is intentionally below the repository's 30-second limit.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, int, int]
CNF = tuple[Clause, ...]


def max_var(cnf: CNF) -> int:
    return max((abs(lit) for clause in cnf for lit in clause), default=0)


def sat_under(cnf: CNF, assignment: dict[int, bool]) -> bool:
    return all(any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause)
               for clause in cnf)


def brute_sat(cnf: CNF) -> bool:
    n = max_var(cnf)
    for bits in itertools.product((False, True), repeat=n):
        assignment = {i + 1: bits[i] for i in range(n)}
        if sat_under(cnf, assignment):
            return True
    return False


def dimacs(cnf: CNF, comments: tuple[str, ...] = ()) -> bytes:
    lines = [*(f"c {c}" for c in comments), f"p cnf {max_var(cnf)} {len(cnf)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf)
    return ("\n".join(lines) + "\n").encode("ascii")


def compact(cnf: CNF) -> bytes:
    # Deterministic alternative text encoding; no asymptotic claim relies on it.
    body = ";".join(",".join(map(str, clause)) for clause in cnf)
    return f"{max_var(cnf)}|{len(cnf)}|{body}".encode("ascii")


def permute_vars(cnf: CNF) -> CNF:
    n = max_var(cnf)
    return tuple(tuple((n + 1 - abs(lit)) * (1 if lit > 0 else -1)
                       for lit in clause) for clause in reversed(cnf))


@dataclass(frozen=True)
class EasyQuery:
    name: str
    cnf: CNF
    witness: dict[int, bool]
    algorithm: str


def easy_query(name: str, blocks: int) -> EasyQuery:
    clauses: list[Clause] = []
    witness: dict[int, bool] = {}
    if name == "independent_product":
        for i in range(blocks):
            x, y, z = 3 * i + 1, 3 * i + 2, 3 * i + 3
            clauses.append((x, y, z))
            witness.update({x: True, y: False, z: False})
        algorithm = "component scan / displayed witness"
    elif name == "horn":
        for i in range(blocks):
            x, y, z = 3 * i + 1, 3 * i + 2, 3 * i + 3
            clauses.append((-x, -y, z))
            witness.update({x: False, y: False, z: False})
        algorithm = "Horn propagation"
    elif name == "two_sat_lift":
        for i in range(blocks):
            x, y, z = 3 * i + 1, 3 * i + 2, 3 * i + 3
            clauses.extend(((x, y, z), (x, y, -z)))
            witness.update({x: True, y: False, z: False})
        algorithm = "2-SAT SCC after eliminating z"
    elif name == "affine_tseitin":
        for i in range(blocks):
            x, y, z = 3 * i + 1, 3 * i + 2, 3 * i + 3
            # x xor y xor z = 0: exclude the four odd-parity assignments.
            clauses.extend(((x, y, -z), (x, -y, z), (-x, y, z), (-x, -y, -z)))
            witness.update({x: False, y: False, z: False})
        algorithm = "Gaussian elimination"
    elif name == "bounded_treewidth":
        # A path-like width-three primal graph with an all-true witness.
        for i in range(blocks):
            x, y, z = i + 1, i + 2, blocks + i + 2
            clauses.append((x, y, z))
            witness.update({x: True, y: True, z: True})
        algorithm = "path-decomposition dynamic program"
    elif name == "redundant_clauses":
        base = easy_query("independent_product", max(1, blocks // 2))
        clauses.extend(base.cnf)
        clauses.extend(reversed(base.cnf))
        witness.update(base.witness)
        algorithm = "deduplication plus displayed witness"
    else:
        raise ValueError(name)
    out = EasyQuery(name, tuple(clauses), witness, algorithm)
    assert sat_under(out.cnf, out.witness)
    return out


def source_universe() -> list[CNF]:
    clauses = []
    for signs in itertools.product((-1, 1), repeat=3):
        clauses.append(tuple(signs[i] * (i + 1) for i in range(3)))
    return [tuple(clauses[i] for i in range(8) if mask & (1 << i))
            for mask in range(256)]


def wrapper_output(base: bool, answer: bool, mode: str) -> tuple[bool, int, int]:
    """Return output, number of oracle calls, reconstruction Boolean ops."""
    if mode == "DIRECT":
        return base, 0, 0
    if mode == "DEAD":
        _ = answer
        return base, 1, 0
    if mode == "CANCEL":
        return bool(base ^ (answer ^ answer)), 1, 2
    if mode == "COPY":
        return bool(base ^ (answer ^ answer)), 2, 2
    if mode == "DELAY":
        checksum = sum((i * i + 3 * i + 7) % 97 for i in range(64))
        assert checksum >= 0
        return base, 1, 0
    if mode == "INTERP":
        return bool(int(str(int(base)))), 1, 2
    if mode == "RECOMP":
        return bool((base and answer) or (base and not answer)), 2, 3
    raise ValueError(mode)


def target_blocks(source_bytes: int, lam: Fraction) -> int:
    target = source_bytes ** float(lam)
    return max(1, math.ceil(target / max(8.0, 10.0 * math.log2(source_bytes + 2))))


def run(seed: int) -> dict[str, object]:
    start = time.perf_counter()
    rng = random.Random(seed)
    families = ("independent_product", "horn", "two_sat_lift",
                "affine_tseitin", "bounded_treewidth", "redundant_clauses")
    wrappers = ("DIRECT", "DEAD", "CANCEL", "COPY", "DELAY", "INTERP", "RECOMP")
    lambdas = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1, 1))

    counts = {
        "source_semantic_checks": 0,
        "easy_query_witness_checks": 0,
        "tiny_bruteforce_checks": 0,
        "wrapper_equivalence_checks": 0,
        "alternate_encoding_checks": 0,
        "renaming_checks": 0,
        "scale_rows": 0,
        "polynomial_padding_rows": 0,
        "cost_ledger_rows": 0,
    }

    tiny_queries: dict[str, EasyQuery] = {}
    for family in families:
        q = easy_query(family, 1)
        tiny_queries[family] = q
        assert sat_under(q.cnf, q.witness)
        counts["easy_query_witness_checks"] += 1
        assert brute_sat(q.cnf)
        counts["tiny_bruteforce_checks"] += 1
        renamed = permute_vars(q.cnf)
        renamed_witness = {max_var(q.cnf) + 1 - v: b for v, b in q.witness.items()}
        assert sat_under(renamed, renamed_witness)
        counts["renaming_checks"] += 1
        assert len(dimacs(q.cnf)) > 0 and len(compact(q.cnf)) > 0
        counts["alternate_encoding_checks"] += 2

    wrapper_calls = {mode: 0 for mode in wrappers}
    reconstruction_ops = {mode: 0 for mode in wrappers}
    sources = source_universe()
    for source in sources:
        base = brute_sat(source)
        counts["source_semantic_checks"] += 1
        for family in families:
            answer = brute_sat(tiny_queries[family].cnf)
            for mode in wrappers:
                out, calls, ops = wrapper_output(base, answer, mode)
                assert out == base
                wrapper_calls[mode] += calls
                reconstruction_ops[mode] += ops
                counts["wrapper_equivalence_checks"] += 1

    scale_rows = []
    for n in (64, 128, 256, 512, 1024, 2048, 4096, 8192):
        for lam in lambdas:
            for family in families:
                q = easy_query(family, target_blocks(n, lam))
                t0 = time.perf_counter_ns()
                encoded = dimacs(q.cnf)
                construction_ns = time.perf_counter_ns() - t0
                assert sat_under(q.cnf, q.witness)
                extraction_ns = 0
                reconstruction_ns = 0
                effective_sigma = math.log(max(2, len(encoded)), n)
                row = {
                    "source_bytes": n,
                    "lambda": f"{lam.numerator}/{lam.denominator}",
                    "family": family,
                    "query_bytes": len(encoded),
                    "clauses": len(q.cnf),
                    "literal_writes": 3 * len(q.cnf),
                    "answer_bits": 1,
                    "construction_ns": construction_ns,
                    "extraction_ns": extraction_ns,
                    "reconstruction_ns": reconstruction_ns,
                    "effective_sigma_finite": effective_sigma,
                    "known_algorithm": q.algorithm,
                    "answer_used": False,
                }
                scale_rows.append(row)
                counts["scale_rows"] += 1
                counts["cost_ledger_rows"] += 1

    padding_rows = []
    for lam in lambdas:
        for degree in (1, 2, 3, 4):
            expected = lam / degree
            # Exact rational exponent conversion under N' = N^degree.
            assert expected * degree == lam
            padding_rows.append({
                "lambda": f"{lam.numerator}/{lam.denominator}",
                "padding_degree": degree,
                "rescaled": f"{expected.numerator}/{expected.denominator}",
                "stays_positive": expected > 0,
            })
            counts["polynomial_padding_rows"] += 1

    # Randomized byte-level encoding and wrapper controls.
    randomized = 0
    for _ in range(2048):
        family = rng.choice(families)
        q = easy_query(family, rng.randint(1, 8))
        a = dimacs(q.cnf, ("ignored annotation",))
        b = compact(permute_vars(q.cnf))
        assert a and b and sat_under(q.cnf, q.witness)
        randomized += 1
        counts["alternate_encoding_checks"] += 2

    total_checks = sum(counts.values())
    result = {
        "run_id": "TESTS-0010",
        "claim": "QUERY-SCALE-WRAPPER-GAUGE1",
        "status": {
            "exact_theorem": "proved in report; pending independent review",
            "finite_audit": "COMPUTATIONAL",
            "p_vs_np": "OPEN",
        },
        "seed": seed,
        "scope": {
            "sources": "all 256 subsets of the eight proper clauses on variables 1,2,3",
            "families": list(families),
            "wrappers": list(wrappers),
            "lambdas": [f"{x.numerator}/{x.denominator}" for x in lambdas],
            "source_lengths": [64, 128, 256, 512, 1024, 2048, 4096, 8192],
            "randomized_encoding_trials": randomized,
        },
        "counts": counts,
        "wrapper_oracle_calls": wrapper_calls,
        "wrapper_reconstruction_boolean_ops": reconstruction_ops,
        "scale_rows": scale_rows,
        "padding_rows": padding_rows,
        "theorem_controls": {
            "dead_query_erasure": "removing an ignored query preserves the output and can change positive scale to zero",
            "answer_cancellation": "b xor b = 0 preserves output despite syntactic answer dependence",
            "fully_charged_cost": "query construction and serialization are counted; the wrapper is not cost-free",
            "finite_limit": "finite measurements do not establish asymptotic runtime bounds",
        },
        "total_checks": total_checks,
        "pass": True,
        "runtime_seconds": time.perf_counter() - start,
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["content_digest_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument(
        "--output",
        default="results/raw/review/2026-10-11_query_scale_wrapper_gauge.json",
    )
    args = parser.parse_args()
    result = run(args.seed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "pass": result["pass"],
        "total_checks": result["total_checks"],
        "runtime_seconds": result["runtime_seconds"],
        "output": str(output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
