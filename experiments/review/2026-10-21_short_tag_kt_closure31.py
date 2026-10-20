#!/usr/bin/env python3
"""Finite audit for SHORT-TAG-KT-CLOSURE31.

This checks only the bit-level composition used in the theorem.  It does not
estimate minimum KT complexity.  The theorem's upper bound comes from an
explicit program: hardwire the short tag and the canonical-template selector,
then compute the requested source/code coordinate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import asdict, dataclass


def canonical_source(label: int, r: int) -> bytes:
    """Two distinct, uniformly indexable template families."""
    core = b"SATCORE:" if label else b"UNSATCORE:"
    return core + b"|" + (b"+abc;" * r)


def tag_bytes(tag: tuple[int, ...]) -> bytes:
    return bytes(tag)


def materialize(kind: str, source: bytes, tag: tuple[int, ...]) -> bytes:
    h = len(tag)
    m = len(source)
    if kind == "raw_append":
        return source + tag_bytes(tag)
    if kind == "repeat_expand":
        code = bytes(tag[j % h] if h else 0 for j in range(m))
        return source + code
    if kind == "xor2_expand":
        code = bytes((tag[j % h] ^ tag[(3 * j + 1) % h]) if h else 0 for j in range(m))
        return source + code
    if kind == "quadratic_address_expand":
        code = bytes(tag[(j * j + j + 1) % h] if h else 0 for j in range(2 * m))
        return source + code
    raise ValueError(kind)


def indexed_bit(kind: str, source: bytes, tag: tuple[int, ...], j: int) -> int:
    """Direct indexed generator matching materialize, without storing output."""
    m = len(source)
    h = len(tag)
    if j < m:
        return source[j]
    q = j - m
    if kind == "raw_append":
        return tag[q]
    if kind == "repeat_expand":
        return tag[q % h] if h else 0
    if kind == "xor2_expand":
        return (tag[q % h] ^ tag[(3 * q + 1) % h]) if h else 0
    if kind == "quadratic_address_expand":
        return tag[(q * q + q + 1) % h] if h else 0
    raise ValueError(kind)


@dataclass
class Audit:
    max_tag_bits: int = 9
    targets_checked: int = 0
    indexed_bits_checked: int = 0
    label_separation_checks: int = 0
    length_checks: int = 0
    failures: int = 0


def check(cond: bool, audit: Audit, field: str) -> None:
    setattr(audit, field, getattr(audit, field) + 1)
    if not cond:
        audit.failures += 1
        raise AssertionError(field)


def run() -> dict:
    audit = Audit()
    kinds = ("raw_append", "repeat_expand", "xor2_expand", "quadratic_address_expand")
    rows = []
    for h in range(audit.max_tag_bits + 1):
        r = 2 * h + 3
        per_h_targets = 0
        per_h_bits = 0
        for tag in itertools.product((0, 1), repeat=h):
            for kind in kinds:
                targets = []
                for label in (0, 1):
                    source = canonical_source(label, r)
                    target = materialize(kind, source, tag)
                    targets.append(target)
                    audit.targets_checked += 1
                    per_h_targets += 1
                    expected_length = {
                        "raw_append": len(source) + h,
                        "repeat_expand": 2 * len(source),
                        "xor2_expand": 2 * len(source),
                        "quadratic_address_expand": 3 * len(source),
                    }[kind]
                    check(len(target) == expected_length, audit, "length_checks")
                    for j, bit in enumerate(target):
                        check(indexed_bit(kind, source, tag, j) == bit, audit, "indexed_bits_checked")
                        per_h_bits += 1
                check(targets[0] != targets[1], audit, "label_separation_checks")
        rows.append({
            "tag_bits": h,
            "payload_parameter_r": r,
            "tags_exhausted": 1 << h,
            "targets_checked": per_h_targets,
            "indexed_bits_checked": per_h_bits,
        })

    theorem_ledger = {
        "ordinary_KT_measure": "program description c plus worst-case indexed output time t",
        "short_tag_bound": "KT(x||z) <= KT(x)+|z|+O(log(M+|z|))+indexing overhead",
        "local_expansion_bound": "KT(x||E(z)) <= c_x+|z|+R(M,|z|)+O(log L)",
        "threshold_consequence": "if c_x+t_x+|z|+R=polylog(L), then for fixed k it is below L^(1/k+o(1))",
        "semantic_firewall": "the target program hardwires z; the cost of discovering z is irrelevant to target KT unless the reduction model separately charges it",
        "scope": "upper bound and finite evaluator audit only; no SAT-to-MKTP reduction and no ARC contractor",
    }
    payload = {
        "run_id": "SHORT-TAG-KT-CLOSURE31",
        "audit": asdict(audit),
        "encoders": list(kinds),
        "rows": rows,
        "theorem_ledger": theorem_ledger,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_digest_field"] = hashlib.sha256(canonical).hexdigest()
    return payload


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
