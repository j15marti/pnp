#!/usr/bin/env python3
"""Bounded checks for RECOVERY-STRENGTHEN6.

This tests only exact finite properties of the flat marked grammar and the
reported exponent arithmetic.  It is not evidence for an all-input SAT
compiler or for a bit-machine workspace bound.
"""

from __future__ import annotations

import itertools
import hashlib
import json
import math
import signal
import time
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]
MAGIC: Clause = (1, -1, 1, -1)
CUT_END: Clause = (1, -1, 1)


def uleb(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def zigzag(x: int) -> int:
    if x == 0:
        raise ValueError("zero literal")
    return 2 * abs(x) - (1 if x > 0 else 0)


def encode_cnf(f: Formula) -> bytes:
    out = bytearray(b"CNF1")
    out += uleb(max((abs(x) for c in f for x in c), default=0))
    out += uleb(len(f))
    for c in f:
        out += uleb(len(c))
        for lit in c:
            out += uleb(zigzag(lit))
    return bytes(out)


def bits(f: Formula) -> int:
    return 8 * len(encode_cnf(f))


def cut_marker(v: int) -> Clause:
    return (1, -1, v)


def block_marker(lo: int, hi: int) -> Clause:
    return (2, -2, lo, -lo, hi)


def is_block_marker(c: Clause) -> Optional[Tuple[int, int]]:
    if len(c) == 5 and c[:2] == (2, -2) and c[3] == -c[2] and 3 <= c[2] <= c[4]:
        return c[2], c[4]
    return None


def restrict_clause(c: Clause, a: Dict[int, bool]) -> Optional[Clause]:
    out: List[int] = []
    for lit in c:
        v = abs(lit)
        if v not in a:
            out.append(lit)
        elif a[v] == (lit > 0):
            return None
    return tuple(out)


def analyze_flat(f: Formula) -> dict:
    n = bits(f)
    if not f or f[0] != MAGIC:
        return {"status": "UNKNOWN", "reason": "missing magic", "input_bits": n}
    i = 1
    cut: List[int] = []
    while i < len(f) and f[i] != CUT_END:
        c = f[i]
        if len(c) != 3 or c[:2] != (1, -1) or c[2] < 3:
            return {"status": "UNKNOWN", "reason": "bad cut", "input_bits": n}
        cut.append(c[2])
        i += 1
    if i == len(f):
        return {"status": "UNKNOWN", "reason": "missing terminator", "input_bits": n}
    i += 1
    cutset = set(cut)
    global_clauses: List[Clause] = []
    while i < len(f) and is_block_marker(f[i]) is None:
        if any(abs(x) not in cutset for x in f[i]):
            return {"status": "UNKNOWN", "reason": "bad global", "input_bits": n}
        global_clauses.append(f[i])
        i += 1
    blocks: List[Formula] = []
    while i < len(f):
        interval = is_block_marker(f[i])
        if interval is None:
            return {"status": "UNKNOWN", "reason": "bad block", "input_bits": n}
        lo, hi = interval
        i += 1
        data: List[Clause] = []
        while i < len(f) and is_block_marker(f[i]) is None:
            av = {abs(x) for x in f[i]}
            if any(v not in cutset and not (lo <= v <= hi) for v in av):
                return {"status": "UNKNOWN", "reason": "cross block", "input_bits": n}
            if all(v in cutset for v in av):
                return {"status": "UNKNOWN", "reason": "cut-only block", "input_bits": n}
            data.append(f[i])
            i += 1
        blocks.append(tuple(data))
    if len(cut) > math.floor(math.log2(max(2, n)) / 10):
        return {"status": "UNKNOWN", "reason": "cut budget", "input_bits": n}
    if len(blocks) > math.floor(math.sqrt(n)):
        return {"status": "UNKNOWN", "reason": "block budget", "input_bits": n}
    cap = math.floor(math.sqrt(n) * math.log2(max(2, n)))
    children: List[Formula] = []
    for assignment in itertools.product((False, True), repeat=len(cut)):
        a = dict(zip(cut, assignment))
        if any(restrict_clause(c, a) == () for c in global_clauses):
            continue
        for block in blocks:
            residual = tuple(rc for c in block if (rc := restrict_clause(c, a)) is not None)
            if () in residual:
                continue
            if residual:
                if bits(residual) > cap:
                    return {"status": "UNKNOWN", "reason": "child budget", "input_bits": n}
                children.append(residual)
    return {
        "status": "ANSWER",
        "input_bits": n,
        "cap_bits": cap,
        "child_bits": [bits(c) for c in children],
        "children": children,
    }


def unmarked_child(width: int) -> Formula:
    # Encoded size grows linearly while all variables remain in one interval.
    return tuple((4 + (j % 3), -(4 + ((j + 1) % 3)), 6) for j in range(width))


def padded_parent(child: Formula, repetitions: int) -> Formula:
    hi = max(abs(x) for c in child for x in c)
    return (
        MAGIC,
        cut_marker(3),
        CUT_END,
        *((3, -3),) * repetitions,
        block_marker(4, hi),
        *child,
    )


def accepted_flat_witness(child: Formula) -> Tuple[Formula, dict, int]:
    # Find charged inert padding by doubling.  Acceptance is checked with the
    # exact CNF1 bit length and exact square-root/log cap.
    repetitions = 1
    while True:
        parent = padded_parent(child, repetitions)
        result = analyze_flat(parent)
        if result["status"] == "ANSWER":
            return parent, result, repetitions
        if result["reason"] not in {"cut budget", "child budget"}:
            raise AssertionError(result)
        repetitions *= 2


def deadline(*_: object) -> None:
    raise TimeoutError("25-second RECOVERY-STRENGTHEN6 test budget exceeded")


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()

    # Exact scalar closure and exact FLMV margin used by the current ARC spine.
    r = Fraction(11, 10)
    eta = Fraction(3, 5)
    h = Fraction(1, 2)
    fixed_point = max(r, eta / (1 - h))
    assert fixed_point == Fraction(6, 5)
    c = Fraction(1201, 1000)
    d = Fraction(1, 2) * ((c + 2) / (c * c) - c)
    assert c > fixed_point and d > Fraction(1, 2)

    rows = []
    for width in (8, 16, 32, 64, 128, 256):
        child = unmarked_child(width)
        child_n = bits(child)

        trivial = padded_parent(child, 0)
        trivial_result = analyze_flat(trivial)
        if width >= 32:
            assert trivial_result["status"] == "UNKNOWN"
            assert trivial_result["reason"] == "child budget"

        parent, result, repetitions = accepted_flat_witness(child)
        assert result["status"] == "ANSWER"
        assert len(result["children"]) == 2  # same child under both cut values
        assert result["children"][0] == child == result["children"][1]
        assert all(analyze_flat(cn)["reason"] == "missing magic" for cn in result["children"])
        parent_n = bits(parent)
        assert child_n <= result["cap_bits"]
        rows.append(
            {
                "width": width,
                "child_bits": child_n,
                "parent_bits": parent_n,
                "padding_clauses": repetitions,
                "executed_children": len(result["children"]),
                "child_over_sqrt_parent_log_parent": child_n
                / (math.sqrt(parent_n) * math.log2(parent_n)),
                "parent_over_child_squared": parent_n / (child_n * child_n),
                "successor_status": "UNKNOWN: missing magic",
            }
        )

    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL finite checks",
        "seconds": time.perf_counter() - started,
        "timeout_seconds": 25,
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scalar_fixed_point": str(fixed_point),
        "flmv_c": str(c),
        "flmv_d": str(d),
        "flat_nonclosure_cases": len(rows),
        "rows": rows,
        "limitations": [
            "Finite accepted parents do not prove an all-input compiler.",
            "The flat parser emits ordinary children; it does not test a new hereditary grammar.",
            "Python memory is not evidence for a random-access bit-machine space bound.",
        ],
    }
    destination = Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
