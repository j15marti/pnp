#!/usr/bin/env python3
"""Cross-format and total-parser checks for the repaired CNF1 adapter.

Every test is deterministic and deliberately small.  This validates byte-level
claims; it is not evidence for an all-input SAT construction.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time

MAGIC = b"CNF1"


class BadCNF1(ValueError):
    pass


def uleb(x: int) -> bytes:
    if x < 0:
        raise ValueError(x)
    out = bytearray()
    while True:
        b = x & 127
        x >>= 7
        out.append(b | (128 if x else 0))
        if not x:
            return bytes(out)


def read_uleb(data: bytes, p: int, cap: int | None = None) -> tuple[int, int]:
    """Read canonical ULEB, optionally rejecting as soon as value exceeds cap."""
    start = p
    value = shift = 0
    while True:
        if p >= len(data):
            raise BadCNF1("truncated ULEB")
        b = data[p]
        p += 1
        value |= (b & 127) << shift
        if cap is not None and value > cap:
            raise BadCNF1("integer exceeds cap")
        if not b & 128:
            break
        shift += 7
        if shift > 7 * len(data):
            raise BadCNF1("overlong ULEB")
    if data[start:p] != uleb(value):
        raise BadCNF1("noncanonical ULEB")
    return value, p


def zz(lit: int) -> int:
    """Repository convention: positive odd, negative even."""
    if lit == 0:
        raise ValueError("zero literal")
    return 2 * abs(lit) - (1 if lit > 0 else 0)


def unzz(z: int) -> int:
    if z == 0:
        raise BadCNF1("zero literal code")
    u = (z + 1) // 2
    return u if z & 1 else -u


def old_arc4_zz(lit: int) -> int:
    return 2 * lit if lit > 0 else -2 * lit - 1


def layout(q: int) -> tuple[int, int]:
    if q < 1:
        raise ValueError(q)
    b = 1
    while q > 1 << (7 * b - 3):
        b += 1
    return b, 1 << (7 * b - 3)


def padded(clauses: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Add one fixed-layout tautology per variable, giving a dense exact max."""
    if not clauses:
        return []
    q = max(abs(lit) for clause in clauses for lit in clause)
    return clauses + [(v, -v, v) for v in range(1, q + 1)]


def encode_exact3(clauses: list[tuple[int, int, int]], old: bool = False) -> bytes:
    if not clauses:
        return MAGIC + uleb(0) + uleb(0)
    clauses = padded(clauses)
    q = max(abs(lit) for clause in clauses for lit in clause)
    b, a = layout(q)
    out = bytearray(MAGIC + uleb(a + q) + uleb(len(clauses)))
    enc = old_arc4_zz if old else zz
    for clause in clauses:
        out += uleb(3)
        for lit in clause:
            z = uleb(enc((a + abs(lit)) if lit > 0 else -(a + abs(lit))))
            assert len(z) == b
            out += z
    return bytes(out)


def parse_total(data: bytes) -> list[tuple[int, ...]]:
    """Total parser for the dense CNF1 language used by the endpoint bridge.

    The polynomial density guard is part of this precise language.  It bounds
    integers before they can require super-logarithmic live arithmetic.
    """
    n = len(data)
    if not data.startswith(MAGIC):
        raise BadCNF1("bad magic")
    maxvar, p = read_uleb(data, 4, cap=128 * n)
    count, p = read_uleb(data, p, cap=n)
    clauses: list[tuple[int, ...]] = []
    seen = 0
    for _ in range(count):
        width, p = read_uleb(data, p, cap=n)
        clause = []
        for _ in range(width):
            z, p = read_uleb(data, p, cap=2 * maxvar)
            lit = unzz(z)
            if abs(lit) > maxvar:
                raise BadCNF1("literal exceeds header")
            seen = max(seen, abs(lit))
            clause.append(lit)
        clauses.append(tuple(clause))
    if p != n:
        raise BadCNF1("trailing data")
    if seen != maxvar:
        raise BadCNF1("header is not attained maximum")
    return clauses


def addressed_byte(clauses: list[tuple[int, int, int]], pos: int) -> int:
    if not clauses:
        data = MAGIC + uleb(0) + uleb(0)
        if pos >= len(data):
            raise IndexError(pos)
        return data[pos]
    clauses = padded(clauses)
    q = max(abs(lit) for clause in clauses for lit in clause)
    b, a = layout(q)
    head = MAGIC + uleb(a + q) + uleb(len(clauses))
    if pos < len(head):
        return head[pos]
    j, within = divmod(pos - len(head), 1 + 3 * b)
    if j >= len(clauses):
        raise IndexError(pos)
    if within == 0:
        return 3
    r, byte = divmod(within - 1, b)
    lit = clauses[j][r]
    renamed = a + abs(lit)
    renamed = renamed if lit > 0 else -renamed
    return uleb(zz(renamed))[byte]


def sat(clauses: list[tuple[int, ...]]) -> bool:
    q = max((abs(x) for c in clauses for x in c), default=0)
    return any(all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in clauses)
               for bits in itertools.product((False, True), repeat=q))


def expect_bad(data: bytes) -> None:
    try:
        parse_total(data)
    except BadCNF1:
        return
    raise AssertionError("malformed input accepted")


def main() -> None:
    started = time.monotonic()
    rng = random.Random(0x5ED7EA4)
    digest = hashlib.sha256()
    addressed = semantics = malformed = 0

    # Smallest direct witness: the old stream decodes with every sign reversed.
    witness = [(1, -2, 2)]
    old_decoded = parse_total(encode_exact3(witness, old=True))
    new_decoded = parse_total(encode_exact3(witness))
    assert old_decoded[0] == (-17, 18, -18)
    assert new_decoded[0] == (17, -18, 18)

    # Empty source has the unique exact-max header (0,0), not ARC4's old (17,0).
    assert encode_exact3([]) == b"CNF1\x00\x00"
    expect_bad(MAGIC + uleb(17) + uleb(0)); malformed += 1

    for q in [1, 2, 16, 17, 63, 64, 127, 2048, 2049, 8192]:
        trials = 12 if q <= 127 else 2
        for _ in range(trials):
            clauses = [tuple((v if rng.getrandbits(1) else -v)
                       for v in (rng.randint(1, q) for _ in range(3)))
                       for _ in range(rng.randint(1, 10))]
            # Ensure q is the attained maximum as required by the theorem.
            clauses[0] = (q, clauses[0][1], clauses[0][2])
            data = encode_exact3(clauses)
            decoded = parse_total(data)
            positions = (range(len(data)) if len(data) <= 2000 else
                         sorted({0, len(data) - 1, *(rng.randrange(len(data)) for _ in range(126))}))
            for i in positions:
                assert addressed_byte(clauses, i) == data[i]
            a = layout(q)[1]
            unshifted = [tuple((abs(x) - a) if x > 0 else -(abs(x) - a)
                               for x in c) for c in decoded]
            assert unshifted == padded(clauses)
            if q <= 8:
                assert sat(clauses) == sat(unshifted)
                semantics += 1
            addressed += len(positions)
            digest.update(data)

    malformed_inputs = [
        b"", b"CNF0\x00\x00", b"CNF1", b"CNF1\x80\x00\x00",
        b"CNF1\x00\x00\x00", MAGIC + uleb(1) + uleb(1) + uleb(1) + uleb(0),
        MAGIC + uleb(1) + uleb(1) + uleb(1) + uleb(3),
        MAGIC + uleb(999999) + uleb(0),
    ]
    for data in malformed_inputs:
        expect_bad(data); malformed += 1

    result = {
        "status": "PASS",
        "seed": "0x5ed7ea4",
        "old_arc4_decoded": old_decoded,
        "repaired_decoded": new_decoded,
        "addressed_bytes_checked": addressed,
        "semantic_instances": semantics,
        "malformed_inputs_rejected": malformed,
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
