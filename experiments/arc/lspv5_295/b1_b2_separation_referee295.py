#!/usr/bin/env python3
"""Finite audit for REFEREE295: a B1/B2 separation for Resolution+Weakening.

The exponential Tseitin lower bound is a literature theorem and is not re-proved
here.  This program checks the elementary constructive pieces used around it:
the explicit CNF encoding, valid SAT sentinels, malformed rejection, and the
universal blocking-clause Resolution+Weakening refutation.
"""

from __future__ import annotations

import argparse
import json
import time
import tracemalloc
from dataclasses import dataclass
from typing import Iterable

Clause = frozenset[int]


@dataclass(frozen=True)
class CNF:
    nvars: int
    clauses: tuple[Clause, ...]


def unary(value: int) -> str:
    if value < 1:
        raise ValueError("unary fields are positive")
    return "1" * value + "0"


def encode_cnf(formula: CNF) -> str:
    """Binary encoding: 1^n0 1^m0; then 1^r0 and sign+1^index0."""
    if formula.nvars < 1 or not formula.clauses:
        raise ValueError("this audit encoding requires n,m >= 1")
    out = [unary(formula.nvars), unary(len(formula.clauses))]
    for clause in formula.clauses:
        if not clause:
            raise ValueError("empty source clauses are excluded by this encoding")
        out.append(unary(len(clause)))
        seen: set[int] = set()
        for lit in sorted(clause, key=lambda z: (abs(z), z < 0)):
            idx = abs(lit)
            if idx < 1 or idx > formula.nvars or idx in seen:
                raise ValueError("bad or duplicate variable in clause")
            seen.add(idx)
            out.append("1" if lit < 0 else "0")
            out.append(unary(idx))
    return "".join(out)


def decode_cnf(bits: str) -> CNF:
    if not bits or any(ch not in "01" for ch in bits):
        raise ValueError("not a nonempty binary string")
    pos = 0

    def read_unary() -> int:
        nonlocal pos
        start = pos
        while pos < len(bits) and bits[pos] == "1":
            pos += 1
        if pos == start or pos >= len(bits) or bits[pos] != "0":
            raise ValueError("malformed unary field")
        pos += 1
        return pos - start - 1

    nvars = read_unary()
    nclauses = read_unary()
    clauses: list[Clause] = []
    for _ in range(nclauses):
        width = read_unary()
        lits: list[int] = []
        seen: set[int] = set()
        for _ in range(width):
            if pos >= len(bits):
                raise ValueError("missing sign")
            sign = bits[pos]
            pos += 1
            idx = read_unary()
            if idx > nvars or idx in seen:
                raise ValueError("out-of-range or duplicate variable")
            seen.add(idx)
            lits.append(-idx if sign == "1" else idx)
        clauses.append(frozenset(lits))
    if pos != len(bits):
        raise ValueError("trailing bits")
    return CNF(nvars, tuple(clauses))


def sentinel(k: int) -> CNF:
    return CNF(1, tuple(frozenset({1}) for _ in range(k)))


def assignment_satisfies(formula: CNF, mask: int) -> bool:
    def value(lit: int) -> bool:
        bit = bool(mask & (1 << (abs(lit) - 1)))
        return bit if lit > 0 else not bit

    return all(any(value(lit) for lit in clause) for clause in formula.clauses)


def exact_sat(formula: CNF) -> tuple[bool, int | None]:
    for mask in range(1 << formula.nvars):
        if assignment_satisfies(formula, mask):
            return True, mask
    return False, None


def blocking_clause(bits: tuple[int, ...]) -> Clause:
    # The unique assignment ``bits`` falsifies this clause.
    return frozenset((-(i + 1) if bit else i + 1) for i, bit in enumerate(bits))


def clause_falsified(clause: Clause, bits: tuple[int, ...]) -> bool:
    for lit in clause:
        bit = bool(bits[abs(lit) - 1])
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return False
    return True


def all_bits(n: int) -> Iterable[tuple[int, ...]]:
    for mask in range(1 << n):
        yield tuple((mask >> i) & 1 for i in range(n))


def build_blocking_refutation(formula: CNF) -> dict:
    sat, _ = exact_sat(formula)
    if sat:
        raise ValueError("blocking refutation requires UNSAT input")
    nodes: list[dict] = []
    current: dict[tuple[int, ...], tuple[int, Clause]] = {}
    for bits in all_bits(formula.nvars):
        source_idx = next(
            i for i, clause in enumerate(formula.clauses) if clause_falsified(clause, bits)
        )
        result = blocking_clause(bits)
        node_id = len(nodes)
        nodes.append(
            {
                "id": node_id,
                "rule": "weakening",
                "source": source_idx,
                "result": sorted(result),
            }
        )
        current[bits] = (node_id, result)

    for pivot_idx in range(formula.nvars - 1, -1, -1):
        nxt: dict[tuple[int, ...], tuple[int, Clause]] = {}
        for prefix in all_bits(pivot_idx):
            left_id, left = current[prefix + (0,)]
            right_id, right = current[prefix + (1,)]
            pivot = pivot_idx + 1
            expected = frozenset((left | right) - {pivot, -pivot})
            node_id = len(nodes)
            nodes.append(
                {
                    "id": node_id,
                    "rule": "resolution",
                    "parents": [left_id, right_id],
                    "pivot": pivot,
                    "result": sorted(expected),
                }
            )
            nxt[prefix] = (node_id, expected)
        current = nxt
    final_id, final_clause = current[()]
    assert not final_clause
    return {"nodes": nodes, "final": final_id, "cost": len(nodes)}


def verify_refutation(formula: CNF, proof: dict) -> bool:
    derived: list[Clause] = []
    for expected_id, node in enumerate(proof["nodes"]):
        if node.get("id") != expected_id:
            return False
        result = frozenset(node["result"])
        if node["rule"] == "weakening":
            source = node.get("source")
            if not isinstance(source, int) or not (0 <= source < len(formula.clauses)):
                return False
            if not formula.clauses[source].issubset(result):
                return False
        elif node["rule"] == "resolution":
            parents = node.get("parents", [])
            if len(parents) != 2 or any(not (0 <= p < expected_id) for p in parents):
                return False
            left, right = (derived[p] for p in parents)
            pivot = node.get("pivot")
            if pivot not in left or -pivot not in right:
                return False
            if result != frozenset((left | right) - {pivot, -pivot}):
                return False
        else:
            return False
        derived.append(result)
    return (
        proof.get("cost") == len(derived)
        and proof.get("final") == len(derived) - 1
        and bool(derived)
        and not derived[-1]
    )


def run_audit(max_n: int = 5, envelope_n: int = 100) -> dict:
    tracemalloc.start()
    start = time.perf_counter_ns()

    # SAT and malformed controls.
    sentinels = []
    for k in range(1, 17):
        f = sentinel(k)
        bits = encode_cnf(f)
        decoded = decode_cnf(bits)
        sat, witness = exact_sat(decoded)
        assert decoded == f and sat and witness == 1
        assert len(bits) == 6 * k + 3
        sentinels.append({"k": k, "length": len(bits), "sat": sat, "witness": witness})

    malformed = {
        "nonbinary": "10x",
        "unterminated": "111",
        "out_of_range": encode_cnf(sentinel(1))[:-2] + "110",  # index 2 with n=1
        "trailing": encode_cnf(sentinel(1)) + "0",
    }
    malformed_rejected = {}
    for name, bits in malformed.items():
        try:
            decode_cnf(bits)
            malformed_rejected[name] = False
        except ValueError:
            malformed_rejected[name] = True
    assert all(malformed_rejected.values())

    # UNSAT both-label control and a sweep of complete blocking formulas.
    four_clause_unsat = CNF(
        2,
        (
            frozenset({1, 2}),
            frozenset({1, -2}),
            frozenset({-1, 2}),
            frozenset({-1, -2}),
        ),
    )
    assert exact_sat(four_clause_unsat) == (False, None)
    f4_proof = build_blocking_refutation(four_clause_unsat)
    assert verify_refutation(four_clause_unsat, f4_proof)
    assert f4_proof["cost"] == 7

    sweeps = []
    for n in range(1, max_n + 1):
        formula = CNF(n, tuple(blocking_clause(bits) for bits in all_bits(n)))
        proof = build_blocking_refutation(formula)
        ok = verify_refutation(formula, proof)
        expected = (1 << (n + 1)) - 1
        assert ok and proof["cost"] == expected
        sweeps.append(
            {
                "nvars": n,
                "source_clauses": 1 << n,
                "proof_cost": proof["cost"],
                "expected": expected,
                "verified": ok,
            }
        )

    # Symbolic delayed-sentinel domination.  No delay is executed.
    envelope = []
    for N in range(10, envelope_n + 1):
        k = (N - 3) // 6
        L = 6 * k + 3
        assert 1 <= k and L <= N and L > N - 6
        universal_log2_bound = N + 1  # Wbar <= 2^(N+1)-1
        delay_log2 = L * L
        dominates = delay_log2 >= universal_log2_bound
        assert dominates
        envelope.append(
            {
                "N": N,
                "sentinel_k": k,
                "sentinel_length": L,
                "delay_log2": delay_log2,
                "universal_W_log2_upper": universal_log2_bound,
                "dominates": dominates,
            }
        )

    elapsed_ns = time.perf_counter_ns() - start
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "claim": "finite constructive audit for B1/B2 separation",
        "calculus": "source-axiom Resolution plus Weakening; unit inference weights",
        "encoding": "unary-delimited binary CNF encoding",
        "sat_sentinels": sentinels,
        "malformed_rejected": malformed_rejected,
        "unsat_f4": {
            "sat": False,
            "proof_cost": f4_proof["cost"],
            "verified": True,
        },
        "blocking_sweep": sweeps,
        "envelope_checks": {
            "N_min": 10,
            "N_max": envelope_n,
            "count": len(envelope),
            "all_dominate": all(row["dominates"] for row in envelope),
            "first": envelope[0],
            "last": envelope[-1],
        },
        "charged_audit": {
            "elapsed_ns": elapsed_ns,
            "peak_traced_bytes": peak_bytes,
            "includes": [
                "encoding",
                "parsing",
                "SAT/UNSAT enumeration",
                "proof construction",
                "rule verification",
                "malformed checks",
                "symbolic envelope arithmetic",
            ],
            "excludes": [
                "the literature Tseitin lower-bound proof",
                "the deliberately specified delay (represented symbolically only)",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--envelope-n", type=int, default=100)
    args = parser.parse_args()
    print(json.dumps(run_audit(args.max_n, args.envelope_n), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
