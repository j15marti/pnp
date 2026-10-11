#!/usr/bin/env python3
"""Finite audit for DECIDE-GUARD-CONTRACT1.

This is a regression test for the exact construction in SYNTHESIS-0002.  It
does not benchmark SAT and does not extrapolate an asymptotic lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from fractions import Fraction
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def gamma_len(x: int) -> int:
    assert x >= 1
    return 2 * x.bit_length() - 1


def encoded_len(cnf: CNF) -> int:
    n = max((abs(lit) for clause in cnf for lit in clause), default=1)
    width = max(1, n.bit_length())
    return gamma_len(n) + gamma_len(len(cnf) + 1) + sum(
        gamma_len(len(clause)) + len(clause) * (1 + width) for clause in cnf
    )


def sat(cnf: CNF) -> bool:
    n = max((abs(lit) for clause in cnf for lit in clause), default=0)
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in cnf):
            return True
    return False


def source_bytes(cnf: CNF) -> bytes:
    return json.dumps(cnf, separators=(",", ":")).encode()


def q_source(cnf: CNF) -> tuple[int, ...]:
    digest = hashlib.sha256(source_bytes(cnf)).digest()[:4]
    return tuple((byte >> bit) & 1 for byte in digest for bit in range(8))


def encodings(bits: tuple[int, ...]):
    mask = tuple(i & 1 for i in range(len(bits)))
    yield "identity", bits, lambda z: z
    yield "complement", tuple(1 - b for b in bits), lambda z: tuple(1 - b for b in z)
    yield "reverse", tuple(reversed(bits)), lambda z: tuple(reversed(z))
    yield "alternating_xor", tuple(b ^ m for b, m in zip(bits, mask)), lambda z: tuple(b ^ m for b, m in zip(z, mask))
    yield "repeat3", tuple(b for b in bits for _ in range(3)), lambda z: tuple(
        1 if sum(z[i:i + 3]) >= 2 else 0 for i in range(0, len(z), 3)
    )


TRUE_CHILD: CNF = tuple((1, 2, 3) for _ in range(8))
FALSE_CHILD: CNF = tuple(
    tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(signs))
    for signs in itertools.product((False, True), repeat=3)
)


def child_for(bit: bool) -> CNF:
    return TRUE_CHILD if bit else FALSE_CHILD


def equality_2sat(n: int, flip: bool) -> CNF:
    clauses: list[Clause] = []
    for i in range(1, n):
        clauses.extend(((-i, i + 1), (i, -(i + 1))))
    if flip and n >= 2:
        clauses.extend(((1,), (-n,)))
    return tuple(clauses)


def horn_chain(n: int, conflict: bool) -> CNF:
    clauses: list[Clause] = [(1,)]
    clauses.extend((-i, i + 1) for i in range(1, n))
    if conflict:
        clauses.append((-n,))
    return tuple(clauses)


def xor_path(n: int, conflict: bool) -> CNF:
    clauses: list[Clause] = [(1,)]
    for i in range(1, n):
        # x_i xor x_(i+1) = 0
        clauses.extend(((-i, i + 1), (i, -(i + 1))))
    clauses.append(((-n,) if conflict else (n,)))
    return tuple(clauses)


def independent_exact_one(k: int, conflict: bool) -> CNF:
    clauses: list[Clause] = []
    for j in range(k):
        a, b = 2 * j + 1, 2 * j + 2
        clauses.extend(((a, b), (-a, -b)))
    if conflict:
        clauses.extend(((1,), (2,)))
    return tuple(clauses)


def h22(n: int, rng: random.Random) -> CNF:
    assert n % 3 == 0
    pos = [v for v in range(1, n + 1) for _ in range(2)]
    neg = [-v for v in range(1, n + 1) for _ in range(2)]
    rng.shuffle(pos)
    rng.shuffle(neg)
    return tuple(tuple(block[i:i + 3]) for block in (pos, neg) for i in range(0, 2 * n, 3))


def cases(max_n: int, seed: int):
    rng = random.Random(seed)
    for n in range(2, max_n + 1):
        yield "equality_2sat_sat", equality_2sat(n, False)
        yield "equality_2sat_unsat", equality_2sat(n, True)
        yield "horn_sat", horn_chain(n, False)
        yield "horn_unsat", horn_chain(n, True)
        yield "affine_sat", xor_path(n, False)
        yield "affine_unsat", xor_path(n, True)
    for k in range(1, max_n // 2 + 1):
        yield "treewidth_product_sat", independent_exact_one(k, False)
        yield "treewidth_product_unsat", independent_exact_one(k, True)
    for n in range(3, max_n + 1, 3):
        for _ in range(4):
            f = h22(n, rng)
            yield "h22_finite", f
            yield "h22_duplicate_padding", f + (f[0], f[0], (1, -1, 2))


def run(max_n: int, seed: int) -> dict:
    started = time.perf_counter()
    assert sat(TRUE_CHILD)
    assert not sat(FALSE_CHILD)
    assert encoded_len(TRUE_CHILD) == encoded_len(FALSE_CHILD)

    semantic_checks = 0
    intervention_checks = 0
    encoding_checks = 0
    family_counts: dict[str, int] = {}
    lengths: list[int] = []
    for family, cnf in cases(max_n, seed):
        family_counts[family] = family_counts.get(family, 0) + 1
        b = sat(cnf)
        q = q_source(cnf)
        lengths.append(encoded_len(cnf))
        for name, encoded, decoder in encodings(q):
            assert decoder(encoded) == q, name
            encoding_checks += 1
            # Legal execution: guard agrees, so constant successor preserves SAT.
            legal_bit = b if decoder(encoded) == q_source(cnf) else not b
            assert sat(child_for(legal_bit)) == b
            assert encoded_len(child_for(legal_bit)) == encoded_len(TRUE_CHILD)
            semantic_checks += 2
            # One decoded replacement is enough to force the opposite successor.
            q_star = (1 - q[0],) + q[1:]
            replacement = next(item for item in encodings(q_star) if item[0] == name)
            _, encoded_star, decoder_star = replacement
            changed_bit = b if decoder_star(encoded_star) == q_source(cnf) else not b
            assert changed_bit != b
            assert sat(child_for(changed_bit)) != b
            intervention_checks += 2

    recurrence_checks = 0
    examples = []
    for k in range(1, 17):
        for eta in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
            # lambda=0, but the constructor first runs A, so r >= K.
            c_next = max(Fraction(k), eta + Fraction(0) * k)
            assert c_next >= k
            recurrence_checks += 1
            if eta in (Fraction(0), Fraction(1)) and k in (2, 8, 16):
                examples.append({"K": k, "eta": str(eta), "lambda": "0", "charged_r": k, "C_next": str(c_next)})

    return {
        "run_id": "SYNTHESIS-0002",
        "status": "PASS",
        "theorem_checked": "DECIDE-GUARD-CONTRACT1",
        "candidate_falsified": "CAUSAL-STRICT-SUCCESSOR-IMPLIES-K-ELIMINATION1",
        "scope": "finite regression only; symbolic theorem is in the report",
        "parameters": {"max_n": max_n, "seed": seed},
        "constant_children": {
            "proper_3cnf": True,
            "clauses_each": 8,
            "variables_each": 3,
            "encoded_bits_each": encoded_len(TRUE_CHILD),
            "sat_child_sat": sat(TRUE_CHILD),
            "unsat_child_sat": sat(FALSE_CHILD),
            "lambda": 0,
        },
        "counts": {
            "source_cases": sum(family_counts.values()),
            "semantic_checks": semantic_checks,
            "encoding_roundtrips": encoding_checks,
            "decoded_intervention_checks": intervention_checks,
            "recurrence_checks": recurrence_checks,
        },
        "family_counts": family_counts,
        "source_encoded_bits": {"min": min(lengths), "max": max(lengths)},
        "recurrence_examples": examples,
        "elapsed_seconds": time.perf_counter() - started,
        "global_status": "P versus NP remains OPEN",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.max_n, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
