#!/usr/bin/env python3
"""Finite audit for ARC-STREAM-SCOPE-FUSION164.

The experiment checks exact online scoped-block composition at one and two
genuine recursive levels.  Every recursive child is serialized as an ordinary
proper-3CNF bit string and parsed back before use.  The stream object is
one-shot and raises if replayed.

Finite checks support only the COMPUTATIONAL claims in the accompanying
report.  The exponent ledger is proved symbolically there.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Set, Tuple

Clause = Tuple[int, int, int]
Formula = List[Clause]


def proper_clause(c: Clause) -> bool:
    return len(c) == 3 and all(x != 0 for x in c) and len({abs(x) for x in c}) == 3


def check_formula(f: Formula) -> None:
    assert all(proper_clause(c) for c in f)


def simplify(f: Formula, assignment: Dict[int, bool]) -> Tuple[bool, List[Tuple[int, ...]]]:
    out: List[Tuple[int, ...]] = []
    for c in f:
        kept: List[int] = []
        satisfied = False
        for lit in c:
            v = abs(lit)
            if v in assignment:
                if assignment[v] == (lit > 0):
                    satisfied = True
                    break
            else:
                kept.append(lit)
        if satisfied:
            continue
        if not kept:
            return False, []
        out.append(tuple(kept))
    return True, out


def dpll(f: Formula) -> bool:
    """Small exact DPLL used only as the leaf guest in the finite audit."""
    clauses: List[Tuple[int, ...]] = [tuple(c) for c in f]

    def rec(cs: List[Tuple[int, ...]], a: Dict[int, bool]) -> bool:
        while True:
            if not cs:
                return True
            if any(len(c) == 0 for c in cs):
                return False
            units = [c[0] for c in cs if len(c) == 1]
            if not units:
                break
            lit = units[0]
            v, val = abs(lit), lit > 0
            if v in a and a[v] != val:
                return False
            a = dict(a)
            a[v] = val
            nxt: List[Tuple[int, ...]] = []
            for c in cs:
                if lit in c:
                    continue
                nc = tuple(x for x in c if x != -lit)
                if not nc:
                    return False
                nxt.append(nc)
            cs = nxt
        lit = cs[0][0]
        for val in (lit > 0, lit < 0):
            v = abs(lit)
            if v in a and a[v] != val:
                continue
            aa = dict(a)
            aa[v] = val
            nxt: List[Tuple[int, ...]] = []
            bad = False
            chosen = v if val else -v
            for c in cs:
                if chosen in c:
                    continue
                nc = tuple(x for x in c if x != -chosen)
                if not nc:
                    bad = True
                    break
                nxt.append(nc)
            if not bad and rec(nxt, aa):
                return True
        return False

    return rec(clauses, {})


def eq_edge(x: int, y: int, fresh: int) -> Tuple[Formula, int]:
    """Proper-3CNF realization of x == y using two private padding names."""
    z, w = fresh, fresh + 1
    return [(-x, y, z), (-x, y, -z), (x, -y, w), (x, -y, -w)], fresh + 2


def pin(lit: int, fresh: int) -> Tuple[Formula, int]:
    """Proper-3CNF realization of the unit literal lit."""
    a, b = fresh, fresh + 1
    return [
        (lit, a, b),
        (lit, a, -b),
        (lit, -a, b),
        (lit, -a, -b),
    ], fresh + 2


def equality_path(n: int, sat: bool) -> Formula:
    assert n >= 2
    fresh = n + 1
    f, fresh = pin(1, fresh)
    for i in range(1, n):
        g, fresh = eq_edge(i, i + 1, fresh)
        f.extend(g)
    g, fresh = pin(n if sat else -n, fresh)
    f.extend(g)
    check_formula(f)
    return f


def disconnected_control() -> Formula:
    a = equality_path(3, True)
    shift = 100
    b = [tuple((1 if x > 0 else -1) * (abs(x) + shift) for x in c) for c in equality_path(3, False)]
    f = a + b
    check_formula(f)
    return f


@dataclass(frozen=True)
class Record:
    opens: Tuple[int, ...]
    clause: Clause
    closes: Tuple[int, ...]


def scoped_records(f: Formula) -> List[Record]:
    first: Dict[int, int] = {}
    last: Dict[int, int] = {}
    for i, c in enumerate(f):
        for v in map(abs, c):
            first.setdefault(v, i)
            last[v] = i
    records: List[Record] = []
    for i, c in enumerate(f):
        records.append(
            Record(
                tuple(sorted(v for v, j in first.items() if j == i)),
                c,
                tuple(sorted(v for v, j in last.items() if j == i)),
            )
        )
    return records


class OneShot:
    def __init__(self, records: Sequence[Record]):
        self._records = list(records)
        self.declared_count = len(records)
        self.iterations = 0
        self.records_read = 0

    def __iter__(self) -> Iterator[Record]:
        self.iterations += 1
        if self.iterations != 1:
            raise RuntimeError("scoped stream replayed")
        for rec in self._records:
            self.records_read += 1
            yield rec


@dataclass
class Block:
    left: Tuple[int, ...]
    right: Tuple[int, ...]
    clauses: Formula


def stream_blocks(stream: OneShot) -> Iterator[Block]:
    cap = max(1, math.ceil(math.sqrt(stream.declared_count)))
    live: Set[int] = set()
    left: Tuple[int, ...] = tuple()
    clauses: Formula = []
    for rec in stream:
        if not clauses:
            left = tuple(sorted(live))
        live.update(rec.opens)
        clauses.append(rec.clause)
        live.difference_update(rec.closes)
        if len(clauses) == cap:
            yield Block(left, tuple(sorted(live)), clauses)
            clauses = []
    if clauses:
        yield Block(left, tuple(sorted(live)), clauses)
    assert not live


def encode_cnf(f: Formula) -> str:
    check_formula(f)
    n = max((abs(x) for c in f for x in c), default=0)
    assert n < 2**16 and len(f) < 2**32
    bits = f"{n:032b}{len(f):032b}"
    for c in f:
        for lit in c:
            bits += ("1" if lit < 0 else "0") + f"{abs(lit):016b}"
    return bits


def decode_cnf(bits: str) -> Formula:
    assert len(bits) >= 64
    n, m = int(bits[:32], 2), int(bits[32:64], 2)
    assert len(bits) == 64 + 51 * m
    f: Formula = []
    p = 64
    for _ in range(m):
        c: List[int] = []
        for _ in range(3):
            sign = bits[p] == "1"
            v = int(bits[p + 1 : p + 17], 2)
            p += 17
            assert 0 < v <= n
            c.append(-v if sign else v)
        f.append(tuple(c))  # type: ignore[arg-type]
    check_formula(f)
    return f


def all_assignments(names: Sequence[int]) -> Iterator[Tuple[bool, ...]]:
    yield from itertools.product((False, True), repeat=len(names))


def assignment_dict(names: Sequence[int], values: Sequence[bool]) -> Dict[int, bool]:
    return dict(zip(names, values))


def child_formula(block: Block, alpha: Tuple[bool, ...], beta: Tuple[bool, ...]) -> Formula:
    assignments = assignment_dict(block.left, alpha)
    for v, val in zip(block.right, beta):
        if v in assignments:
            assert assignments[v] == val
        assignments[v] = val
    fresh = max([abs(x) for c in block.clauses for x in c] + list(assignments) + [0]) + 1
    out = list(block.clauses)
    for v in sorted(assignments):
        g, fresh = pin(v if assignments[v] else -v, fresh)
        out.extend(g)
    check_formula(out)
    return out


@dataclass
class Stats:
    stream_instances: int = 0
    stream_records: int = 0
    stream_replays: int = 0
    block_count: int = 0
    child_calls: int = 0
    leaf_calls: int = 0
    max_width: int = 0
    max_buffered_clauses: int = 0
    max_child_clauses: int = 0
    max_child_bits: int = 0
    serialized_child_bits: int = 0
    calls_by_depth: Dict[int, int] = field(default_factory=dict)


def fused_decide(f: Formula, depth: int, stats: Stats) -> bool:
    assert depth >= 1
    stats.calls_by_depth[depth] = stats.calls_by_depth.get(depth, 0) + 1
    stream = OneShot(scoped_records(f))
    stats.stream_instances += 1
    reachable: Set[Tuple[bool, ...]] = {tuple()}
    expected_left: Tuple[int, ...] = tuple()
    for block in stream_blocks(stream):
        stats.block_count += 1
        stats.max_width = max(stats.max_width, len(block.left), len(block.right))
        stats.max_buffered_clauses = max(stats.max_buffered_clauses, len(block.clauses))
        assert block.left == expected_left
        nxt: Set[Tuple[bool, ...]] = set()
        for alpha in reachable:
            amap = assignment_dict(block.left, alpha)
            for beta in all_assignments(block.right):
                bmap = assignment_dict(block.right, beta)
                if any(amap[v] != bmap[v] for v in set(amap) & set(bmap)):
                    continue
                child = child_formula(block, alpha, beta)
                bits = encode_cnf(child)
                parsed = decode_cnf(bits)
                assert parsed == child
                stats.child_calls += 1
                stats.serialized_child_bits += len(bits)
                stats.max_child_bits = max(stats.max_child_bits, len(bits))
                stats.max_child_clauses = max(stats.max_child_clauses, len(child))
                if depth == 1:
                    stats.leaf_calls += 1
                    ok = dpll(parsed)
                else:
                    ok = fused_decide(parsed, depth - 1, stats)
                if ok:
                    nxt.add(beta)
        reachable = nxt
        expected_left = block.right
        if not reachable:
            break
    stats.stream_records += stream.records_read
    stats.stream_replays += max(0, stream.iterations - 1)
    return tuple() in reachable


def main() -> None:
    cases: List[Tuple[str, Formula, bool]] = []
    for n in range(2, 6):
        cases.append((f"equality_path_{n}_sat", equality_path(n, True), True))
        cases.append((f"equality_path_{n}_unsat", equality_path(n, False), False))
    cases.append(("disconnected_sat_plus_unsat", disconnected_control(), False))

    rows = []
    total_checks = 0
    for depth in (1, 2):
        for name, formula, expected in cases:
            direct = dpll(formula)
            assert direct == expected
            stats = Stats()
            got = fused_decide(formula, depth, stats)
            assert got == expected
            assert stats.stream_replays == 0
            total_checks += 4  # direct, fused label, no replay, proper roundtrips
            rows.append(
                {
                    "name": name,
                    "depth": depth,
                    "expected": expected,
                    "clauses": len(formula),
                    "variables": len({abs(x) for c in formula for x in c}),
                    "stats": {
                        **{k: v for k, v in vars(stats).items() if k != "calls_by_depth"},
                        "calls_by_depth": {str(k): v for k, v in sorted(stats.calls_by_depth.items())},
                    },
                }
            )

    result = {
        "run_id": "ARC_STREAM_SCOPE_FUSION164",
        "status": "COMPUTATIONAL",
        "exhaustive_parameter_grid": {
            "path_lengths": [2, 3, 4, 5],
            "labels": ["SAT", "UNSAT"],
            "depths": [1, 2],
            "extra_controls": ["disconnected SAT+UNSAT"],
        },
        "random_seed": None,
        "total_assertion_groups": total_checks,
        "failures": 0,
        "rows": rows,
        "limitations": [
            "finite proper-3CNF controls only",
            "Python object work is not a RAM bit-operation measurement",
            "does not construct the all-input scoped normalizer",
            "does not prove ARC-EDGE-90",
        ],
    }
    out = Path(__file__).with_name("2026-10-25_0348_ARC_STREAM_SCOPE_FUSION164_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"failures": 0, "rows": len(rows), "assertion_groups": total_checks, "output": str(out)}))


if __name__ == "__main__":
    main()
