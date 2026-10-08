#!/usr/bin/env python3
"""Bounded exact checks for the indexed-3CNF -> fixed-layout CNF1 adapter."""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time


MAGIC = b"CNF1"


def uleb(x: int) -> bytes:
    assert x >= 0
    out = bytearray()
    while True:
        y = x & 0x7F
        x >>= 7
        out.append(y | (0x80 if x else 0))
        if not x:
            return bytes(out)


def zigzag(lit: int) -> int:
    assert lit != 0
    return 2 * lit if lit > 0 else -2 * lit - 1


def choose_layout(q: int) -> tuple[int, int]:
    assert q >= 1
    b = 1
    while q > (1 << (7 * b - 3)):
        b += 1
    return b, 1 << (7 * b - 3)


def rename(lit: int, offset: int) -> int:
    v = offset + abs(lit)
    return v if lit > 0 else -v


def serialize(clauses: list[tuple[int, int, int]], q: int) -> tuple[bytes, int, int]:
    b, offset = choose_layout(q)
    out = bytearray(MAGIC)
    out += uleb(offset + q)
    out += uleb(len(clauses))
    for clause in clauses:
        out += uleb(3)
        for lit in clause:
            z = uleb(zigzag(rename(lit, offset)))
            assert len(z) == b
            out += z
    return bytes(out), b, offset


def addressed_byte(
    clauses: list[tuple[int, int, int]], q: int, pos: int
) -> int:
    """Compute one target byte using only its address and one literal query."""
    b, offset = choose_layout(q)
    header = MAGIC + uleb(offset + q) + uleb(len(clauses))
    if pos < len(header):
        return header[pos]
    rel = pos - len(header)
    rec = 1 + 3 * b
    clause_index, within = divmod(rel, rec)
    if clause_index >= len(clauses):
        raise IndexError(pos)
    if within == 0:
        return 3
    literal_index, literal_byte = divmod(within - 1, b)
    lit = clauses[clause_index][literal_index]
    return uleb(zigzag(rename(lit, offset)))[literal_byte]


def sat(clauses: list[tuple[int, int, int]], q: int) -> bool:
    for bits in itertools.product((False, True), repeat=q):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses):
            return True
    return False


def renamed_sat(clauses: list[tuple[int, int, int]], q: int, offset: int) -> bool:
    renamed = [tuple(rename(l, offset) for l in c) for c in clauses]
    for bits in itertools.product((False, True), repeat=q):
        values = {offset + i + 1: bits[i] for i in range(q)}
        if all(any(values[abs(lit)] == (lit > 0) for lit in c) for c in renamed):
            return True
    return False


def main() -> None:
    started = time.monotonic()
    rng = random.Random(0xA7C2026)
    boundary_q = [1, 2, 8, 16, 17, 127, 2048, 2049, 16384, 100_000]
    boundary_checks = 0
    address_checks = 0
    semantic_checks = 0
    total_bytes = 0
    digest = hashlib.sha256()

    for q in boundary_q:
        clauses = []
        for _ in range(97):
            clause = []
            for _ in range(3):
                v = rng.randint(1, q)
                clause.append(v if rng.getrandbits(1) else -v)
            clauses.append(tuple(clause))
        data, b, offset = serialize(clauses, q)
        assert offset >= q
        assert offset <= 128 * q if q > 1 else offset <= 16
        assert all(
            len(uleb(zigzag(rename(lit, offset)))) == b
            for clause in clauses
            for lit in clause
        )
        rebuilt = bytes(addressed_byte(clauses, q, i) for i in range(len(data)))
        assert rebuilt == data
        boundary_checks += 1
        address_checks += len(data)
        total_bytes += len(data)
        digest.update(data)

    for q in range(1, 9):
        for _ in range(40):
            clauses = []
            for _ in range(rng.randint(0, 12)):
                clause = tuple(
                    (v if rng.getrandbits(1) else -v)
                    for v in (rng.randint(1, q) for _ in range(3))
                )
                clauses.append(clause)
            data, _, offset = serialize(clauses, q)
            assert sat(clauses, q) == renamed_sat(clauses, q, offset)
            assert bytes(addressed_byte(clauses, q, i) for i in range(len(data))) == data
            semantic_checks += 1
            address_checks += len(data)
            total_bytes += len(data)
            digest.update(data)

    elapsed = time.monotonic() - started
    result = {
        "status": "PASS",
        "seed": "0xa7c2026",
        "boundary_families": boundary_checks,
        "semantic_instances": semantic_checks,
        "addressed_bytes_checked": address_checks,
        "serialized_bytes_checked": total_bytes,
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(elapsed, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
