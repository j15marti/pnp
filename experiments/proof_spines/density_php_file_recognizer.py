#!/usr/bin/env python3
"""Independent model of the ARC-0005 file-first density-gated recognizer.

The accepted language is deliberately narrow.  A file is a canonical DIMACS
CNF with one header, then a nonempty block of positive clauses of a common
width, then a block of sorted, duplicate-free negative binary clauses.
The first pass stores only counters, the previous edge, and one clause.  Only
after the exact balanced-density gate succeeds does the second pass allocate
O(n) arrays and verify the full rectangular pigeonhole incidence structure.

This is an independent reimplementation, not recovery of the implementation
claimed by ARC-0005-ORBIT.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import tempfile
import time
from dataclasses import asdict, dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Optional


class Reject(Exception):
    pass


@dataclass
class FirstPass:
    file_bytes: int
    declared_n: int
    declared_m: int
    p: int
    h: int
    e: int
    max_token_chars: int
    density_lhs: int
    density_rhs: int


@dataclass
class Recognition:
    outcome: str
    value: Optional[bool]
    reason: str
    first_pass: Optional[FirstPass]
    arrays_allocated_after_gate: bool
    allocated_integer_cells: int


def _token_stream(path: Path, max_chars: int) -> Iterable[str]:
    """Yield ASCII whitespace-delimited tokens with an O(log M) token buffer."""
    buf = bytearray()
    with path.open("rb") as src:
        while True:
            chunk = src.read(4096)
            if not chunk:
                break
            for byte in chunk:
                if byte in b" \t\r\n":
                    if buf:
                        try:
                            yield buf.decode("ascii")
                        except UnicodeDecodeError as exc:
                            raise Reject("non-ASCII token") from exc
                        buf.clear()
                else:
                    buf.append(byte)
                    # Numeric tokens have at most max_chars digits and one sign;
                    # the two header words have length at most three.
                    if len(buf) > max(max_chars + 1, 3):
                        raise Reject("oversized token")
        if buf:
            try:
                yield buf.decode("ascii")
            except UnicodeDecodeError as exc:
                raise Reject("non-ASCII token") from exc


def _integer_token(token: str, max_chars: int) -> int:
    raw = token[1:] if token.startswith("-") else token
    if not raw or len(raw) > max_chars or not raw.isdigit():
        raise Reject("literal token")
    return int(token)


def first_pass(path: Path) -> FirstPass:
    file_bytes = path.stat().st_size
    max_chars = max(1, len(str(max(1, file_bytes))))
    tokens = iter(_token_stream(path, max_chars))
    try:
        header = [next(tokens) for _ in range(4)]
    except StopIteration as exc:
        raise Reject("header") from exc
    if header[:2] != ["p", "cnf"]:
        raise Reject("header")
    if not header[2].isdigit() or not header[3].isdigit():
        raise Reject("header integers")
    declared_n, declared_m = int(header[2]), int(header[3])
    if declared_n < 1 or declared_m < 1 or declared_n > file_bytes:
        raise Reject("empty or oversized declaration")

    p = h = e = 0
    clauses = 0
    edge_mode = False
    previous_edge: Optional[tuple[int, int]] = None
    clause_len = 0
    clause_sign = 0
    previous_positive = 0
    edge_values: list[int] = []  # capped at two entries
    for token in tokens:
        value = _integer_token(token, max_chars)
        if value != 0:
            clause_len += 1
            sign = 1 if value > 0 else -1
            if clause_sign and sign != clause_sign:
                raise Reject("mixed-sign clause")
            clause_sign = sign
            if sign > 0:
                if edge_mode or value <= previous_positive:
                    raise Reject("positive clause order or duplicate")
                previous_positive = value
            else:
                if clause_len > 2:
                    raise Reject("negative clause width")
                edge_values.append(-value)
            continue

        if clause_len == 0:
            raise Reject("empty clause outside accepted domain")
        clauses += 1
        if clause_sign > 0 and not edge_mode:
            if h == 0:
                h = clause_len
            if clause_len != h:
                raise Reject("row width")
            p += 1
        else:
            edge_mode = True
            if clause_sign >= 0 or clause_len != 2:
                raise Reject("clause type or block order")
            edge = (edge_values[0], edge_values[1])
            if edge[0] >= edge[1]:
                raise Reject("edge literal order or loop")
            if previous_edge is not None and edge <= previous_edge:
                raise Reject("edge order or duplicate")
            previous_edge = edge
            e += 1
        clause_len = 0
        clause_sign = 0
        previous_positive = 0
        edge_values.clear()
    if clause_len:
        raise Reject("clause terminator")

    if clauses != declared_m or p < 2 or h < 2:
        raise Reject("count or minimum dimension")
    if declared_n != p * h:
        raise Reject("n != p h")
    if not (h <= 2 * p and p <= 2 * h):
        raise Reject("balance gate")
    if e != h * p * (p - 1) // 2:
        raise Reject("edge count")
    lhs, rhs = 32 * e * e, declared_n**3
    if lhs < rhs:
        raise Reject("density gate")
    return FirstPass(file_bytes, declared_n, declared_m, p, h, e,
                     max_chars, lhs, rhs)


def recognize(path: Path) -> Recognition:
    try:
        fp = first_pass(path)
    except (OSError, UnicodeError, Reject) as exc:
        return Recognition("FAIL", None, str(exc), None, False, 0)

    n, p, h = fp.declared_n, fp.p, fp.h
    # All variable-indexed allocation is below the successful density gate.
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    degree = [0] * (n + 1)
    row_of = [-1] * (n + 1)
    allocated_cells = 4 * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    try:
        tokens = iter(_token_stream(path, fp.max_token_chars))
        for _ in range(4):
            next(tokens)
        row = 0
        edge_mode = False
        clause: list[int] = []
        for token in tokens:
            value = _integer_token(token, fp.max_token_chars)
            if value != 0:
                clause.append(value)
                continue
            if all(x > 0 for x in clause) and not edge_mode:
                for v in clause:
                    if v < 1 or v > n or row_of[v] != -1:
                        raise Reject("row incidence")
                    row_of[v] = row
                row += 1
            else:
                edge_mode = True
                a, b = -clause[0], -clause[1]
                if a < 1 or b > n:
                    raise Reject("edge label")
                degree[a] += 1
                degree[b] += 1
                union(a, b)
            clause.clear()
        if row != p or any(row_of[v] < 0 for v in range(1, n + 1)):
            raise Reject("row cover")

        roots = [find(v) for v in range(1, n + 1)]
        pairs = sorted((roots[v - 1], row_of[v]) for v in range(1, n + 1))
        allocated_cells += n + 2 * n
        components: dict[int, list[int]] = {}
        for root, row_id in pairs:
            components.setdefault(root, []).append(row_id)
        if len(components) != h:
            raise Reject("component count")
        expected_rows = list(range(p))
        for root, rows in components.items():
            if size[find(root)] != p or rows != expected_rows:
                raise Reject("component/row profile")
        if any(degree[v] != p - 1 for v in range(1, n + 1)):
            raise Reject("degree")
    except (OSError, UnicodeError, Reject) as exc:
        return Recognition("FAIL", None, str(exc), fp, True, allocated_cells)
    return Recognition("VALUE", p <= h, "rectangular PHP certificate", fp,
                       True, allocated_cells)


def write_php(path: Path, p: int, h: int, permutation: Optional[list[int]] = None) -> None:
    n = p * h
    perm = permutation or list(range(1, n + 1))
    if sorted(perm) != list(range(1, n + 1)):
        raise ValueError("permutation")
    rows = []
    for r in range(p):
        rows.append(sorted(perm[r * h:(r + 1) * h]))
    edges = []
    for col in range(h):
        for a, b in combinations(range(p), 2):
            edges.append(tuple(sorted((perm[a * h + col], perm[b * h + col]))))
    edges.sort()
    clauses = rows + [[-a, -b] for a, b in edges]
    with path.open("wt", encoding="ascii", newline="") as out:
        out.write(f"p cnf {n} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")


def brute_force_dimacs(path: Path) -> bool:
    clauses: list[list[int]] = []
    n = 0
    with path.open("rt", encoding="ascii") as src:
        header = src.readline().split()
        n = int(header[2])
        for line in src:
            clauses.append([int(x) for x in line.split()[:-1]])
    for bits in product((False, True), repeat=n):
        if all(any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses):
            return True
    return False


def mutate_lines(source: Path, target: Path, transform) -> None:
    lines = source.read_text(encoding="ascii").splitlines()
    target.write_text("\n".join(transform(lines)) + "\n", encoding="ascii")


def run_suite(output: Path) -> dict:
    started = time.perf_counter()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25s")))
    signal.alarm(25)
    cases = []
    hostile = []
    with tempfile.TemporaryDirectory(prefix="density_php_") as tmp:
        root = Path(tmp)
        for p in range(2, 5):
            for h in range(2, 5):
                if not (h <= 2 * p and p <= 2 * h):
                    continue
                path = root / f"php_{p}_{h}.cnf"
                permutation = list(range(1, p * h + 1))[::-1]
                write_php(path, p, h, permutation)
                rec = recognize(path)
                brute = brute_force_dimacs(path) if p * h <= 12 else (p <= h)
                assert rec.outcome == "VALUE" and rec.value == brute == (p <= h)
                assert rec.arrays_allocated_after_gate
                assert rec.first_pass and rec.first_pass.density_lhs >= rec.first_pass.density_rhs
                cases.append({"p": p, "h": h, "value": rec.value,
                              "brute_force": brute, "bytes": path.stat().st_size})

        base = root / "base.cnf"
        write_php(base, 4, 4, list(range(1, 17))[::-1])
        transforms = {
            "duplicate_edge": lambda x: x + [x[-1]],
            "edge_out_of_order": lambda x: x[:-2] + [x[-1], x[-2]],
            "delete_edge": lambda x: x[:-1],
            "duplicate_row_variable": lambda x: x[:2] + [x[1]] + x[3:],
            "comment_padding": lambda x: x[:1] + ["c padding"] + x[1:],
            "wrong_header_n": lambda x: [x[0].replace("p cnf 16", "p cnf 17")] + x[1:],
            "oversized_label": lambda x: x[:1] + ["999999999999999999 2 3 4 0"] + x[2:],
        }
        for name, fn in transforms.items():
            target = root / f"bad_{name}.cnf"
            mutate_lines(base, target, fn)
            rec = recognize(target)
            assert rec.outcome == "FAIL"
            hostile.append({"name": name, "reason": rec.reason,
                            "allocated_after_gate": rec.arrays_allocated_after_gate})

        # Independent-product escape: two valid PHP(2,2) blocks under one
        # header are not one rectangular certificate and must not be merged.
        prod = root / "independent_product.cnf"
        prod.write_text(
            "p cnf 8 8\n1 2 0\n3 4 0\n5 6 0\n7 8 0\n"
            "-1 -3 0\n-2 -4 0\n-5 -7 0\n-6 -8 0\n",
            encoding="ascii",
        )
        rec = recognize(prod)
        assert rec.outcome == "FAIL" and not rec.arrays_allocated_after_gate
        hostile.append({"name": "independent_product", "reason": rec.reason,
                        "allocated_after_gate": rec.arrays_allocated_after_gate})

        # Exact countercontrol: the count/balance gate must reject before arrays.
        unbalanced = root / "unbalanced.cnf"
        write_php(unbalanced, 2, 8)
        rec = recognize(unbalanced)
        assert rec.outcome == "FAIL" and not rec.arrays_allocated_after_gate
        hostile.append({"name": "unbalanced_2_8", "reason": rec.reason,
                        "allocated_after_gate": rec.arrays_allocated_after_gate})

        large = []
        for p, h in [(24, 24), (25, 24), (48, 48), (49, 48)]:
            path = root / f"large_{p}_{h}.cnf"
            write_php(path, p, h)
            t0 = time.perf_counter()
            rec = recognize(path)
            elapsed = time.perf_counter() - t0
            assert rec.outcome == "VALUE" and rec.value == (p <= h)
            assert rec.first_pass and rec.allocated_integer_cells <= 7 * (p * h + 1)
            large.append({"p": p, "h": h, "bytes": path.stat().st_size,
                          "seconds": round(elapsed, 6),
                          "allocated_integer_cells": rec.allocated_integer_cells,
                          "density_lhs": rec.first_pass.density_lhs,
                          "density_rhs": rec.first_pass.density_rhs})

    signal.alarm(0)
    result = {
        "run_id": "RSR-0005",
        "status": "COMPUTATIONAL",
        "model": "canonical two-pass DIMACS; immutable reread; arrays only after density gate",
        "seed": None,
        "randomized": False,
        "exhaustive_small_parameter_cells": len(cases),
        "small_cases": cases,
        "hostile_controls": hostile,
        "large_cases": large,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "limitations": [
            "independent reimplementation, not recovered ARC-0005-ORBIT source",
            "accepts only a canonical balanced rectangular-PHP subset",
            "finite runs do not prove asymptotic or all-CNF coverage",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_suite(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
