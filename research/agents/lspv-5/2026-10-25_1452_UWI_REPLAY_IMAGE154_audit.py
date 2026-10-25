#!/usr/bin/env python3
"""Finite audit for the UWI short-seed replay lemma.

This is an operation-counted logical model, not a claim about Python's
physical switching cost and not an asymptotic lower-bound experiment.
Every generated CNF is satisfiable by construction.  The replay procedure
does not receive the seed; it enumerates seeds bounded by the encoded input
length and compares ordinary encodings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class Counters:
    candidates: int = 0
    generator_steps: int = 0
    source_reads: int = 0
    generated_writes: int = 0
    comparison_reads: int = 0
    counter_writes: int = 0
    verifier_literal_reads: int = 0


def step(x: int) -> int:
    return (1103515245 * x + 12345) & 0x7FFFFFFF


def witness_bits(n: int, seed: int, ctr: Optional[Counters] = None) -> list[int]:
    x = seed ^ (n * 0x45D9F3B)
    out: list[int] = []
    for _ in range(n):
        x = step(x)
        out.append((x >> 12) & 1)
        if ctr:
            ctr.generator_steps += 1
            ctr.generated_writes += 1
    return out


def generate(n: int, m: int, seed: int, ctr: Optional[Counters] = None) -> tuple[bytes, list[int]]:
    """Generate a canonical planted proper 3-CNF and one witness."""
    w = witness_bits(n, seed, ctr)
    x = seed ^ (m * 0x9E3779B1)
    clauses: list[tuple[int, int, int]] = []
    for j in range(m):
        chosen: list[int] = []
        while len(chosen) < 3:
            x = step(x)
            v = 1 + (x % n)
            if v not in chosen:
                chosen.append(v)
            if ctr:
                ctr.generator_steps += 1
        lits: list[int] = []
        for v in chosen:
            x = step(x)
            sign = 1 if ((x >> 9) & 1) else -1
            lits.append(sign * v)
            if ctr:
                ctr.generator_steps += 1
        # Force one deterministic literal true under the planted witness.
        pivot = j % 3
        v = abs(lits[pivot])
        lits[pivot] = v if w[v - 1] else -v
        clauses.append(tuple(lits))
    body = [f"p cnf {n} {m}\n"]
    body.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    encoded = "".join(body).encode("ascii")
    if ctr:
        ctr.generated_writes += len(encoded) * 8
    return encoded, w


def parse(data: bytes) -> tuple[int, int, list[tuple[int, ...]]]:
    lines = data.decode("ascii").splitlines()
    tag, kind, ns, ms = lines[0].split()
    assert (tag, kind) == ("p", "cnf")
    n, m = int(ns), int(ms)
    clauses = []
    for line in lines[1:]:
        vals = tuple(map(int, line.split()))
        assert vals[-1] == 0
        clauses.append(vals[:-1])
    assert len(clauses) == m
    return n, m, clauses


def verify(data: bytes, witness: Iterable[int], ctr: Optional[Counters] = None) -> bool:
    n, _, clauses = parse(data)
    w = list(witness)
    if len(w) != n:
        return False
    for clause in clauses:
        ok = False
        for lit in clause:
            if ctr:
                ctr.verifier_literal_reads += 1
            bit = w[abs(lit) - 1]
            if (lit > 0 and bit) or (lit < 0 and not bit):
                ok = True
                break
        if not ok:
            return False
    return True


def replay(data: bytes, ctr: Counters) -> tuple[Optional[int], Optional[list[int]]]:
    """Fixed-policy replay: public index=(n,m), seeds 0..N inclusive."""
    n, m, _ = parse(data)
    limit = len(data) * 8 + 2  # at most N+2 seeds, hence O(log N) seed bits
    for seed in range(limit):
        ctr.candidates += 1
        ctr.counter_writes += max(1, limit.bit_length())
        candidate, witness = generate(n, m, seed, ctr)
        upto = min(len(candidate), len(data))
        matched = True
        for i in range(upto):
            ctr.source_reads += 8
            ctr.comparison_reads += 16
            if candidate[i] != data[i]:
                matched = False
                break
        if matched and len(candidate) == len(data) and candidate == data:
            assert verify(data, witness, ctr)
            return seed, witness
    return None, None


def unsat_control() -> bytes:
    lines = ["p cnf 3 8\n"]
    for mask in range(8):
        lits = []
        for i in range(3):
            # Clause falsified by the assignment equal to mask.
            bit = (mask >> i) & 1
            lits.append(-(i + 1) if bit else (i + 1))
        lines.append(" ".join(map(str, lits)) + " 0\n")
    return "".join(lines).encode("ascii")


def exhaustive_sat(data: bytes) -> bool:
    n, _, _ = parse(data)
    for mask in range(1 << n):
        if verify(data, [(mask >> i) & 1 for i in range(n)]):
            return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    cases = []
    total_assertions = 0
    for n, m, seed in [(6, 18, 0), (8, 28, 3), (10, 40, 9), (12, 52, 17)]:
        data, planted = generate(n, m, seed)
        assert seed < len(data) * 8 + 2
        assert verify(data, planted)
        ctr = Counters()
        recovered_seed, recovered = replay(data, ctr)
        assert recovered_seed is not None and recovered is not None
        assert verify(data, recovered)
        matches = []
        for s in range(len(data) * 8 + 2):
            candidate, w = generate(n, m, s)
            if candidate == data:
                assert verify(data, w)
                matches.append(s)
        total_assertions += 5 + len(matches)
        cases.append({
            "n": n,
            "m": m,
            "chosen_seed": seed,
            "encoded_bits_N": len(data) * 8,
            "eligible_seed_bits_ceiling": (len(data) * 8 + 1).bit_length(),
            "first_recovered_seed": recovered_seed,
            "all_matching_seeds": matches,
            "witness_verified": True,
            "logical_counters": asdict(ctr),
        })

    u = unsat_control()
    assert not exhaustive_sat(u)
    uctr = Counters()
    us, uw = replay(u, uctr)
    assert us is None and uw is None
    total_assertions += 3

    result = {
        "run_id": "UWI-REPLAY-IMAGE154",
        "status": "COMPUTATIONAL",
        "model": "deterministic logical operation counters over canonical ASCII CNF",
        "seed_rule": "enumerate 0 <= seed < N+2; seed description length O(log N)",
        "cases": cases,
        "unsat_control": {
            "encoded_bits_N": len(u) * 8,
            "exhaustive_sat": False,
            "replay_match": False,
            "logical_counters": asdict(uctr),
        },
        "assertions": total_assertions,
        "limitations": [
            "finite tests do not prove asymptotics",
            "logical counters are not physical switching measurements",
            "the formal replay lemma, not this program, proves the asymptotic upper bound",
            "H is defined only on SAT inputs; the UNSAT case is a false-match control",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, indent=2) + "\n"
    result["payload_sha256_without_self_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"assertions": total_assertions, "cases": len(cases), "unsat_match": False}))


if __name__ == "__main__":
    main()
