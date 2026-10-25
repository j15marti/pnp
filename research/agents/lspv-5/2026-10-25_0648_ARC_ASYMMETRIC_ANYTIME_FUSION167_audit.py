#!/usr/bin/env python3
"""Finite audit for ARC-ASYMMETRIC-ANYTIME-FUSION167.

The schedule is online and is never given the final stream length M.  For a
fixed rational theta=p/q in (0,1), epoch k has capacity ceil(2**(p*k/q)).
The audit checks schedule bounds and exact scoped SAT/UNSAT joins through two
genuine recursive levels.  Event counters are logical Python events, not an
FLMV primitive trace.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterator, List, Sequence, Set, Tuple


HERE = Path(__file__).resolve().parent
Clause = Tuple[int, ...]
Formula = List[Clause]


def dpll(formula: Formula) -> bool:
    def rec(cs: Formula) -> bool:
        while True:
            if not cs:
                return True
            if any(not c for c in cs):
                return False
            units = [c[0] for c in cs if len(c) == 1]
            if not units:
                break
            lit = units[0]
            nxt: Formula = []
            for c in cs:
                if lit in c:
                    continue
                nc = tuple(x for x in c if x != -lit)
                if not nc:
                    return False
                nxt.append(nc)
            cs = nxt
        lit = cs[0][0]
        for chosen in (lit, -lit):
            nxt = []
            bad = False
            for c in cs:
                if chosen in c:
                    continue
                nc = tuple(x for x in c if x != -chosen)
                if not nc:
                    bad = True
                    break
                nxt.append(nc)
            if not bad and rec(nxt):
                return True
        return False
    return rec(list(formula))


def equality_path(n: int, sat: bool) -> Formula:
    f: Formula = [(1,)]
    for x in range(1, n):
        f.extend([(-x, x + 1), (x, -(x + 1))])
    f.append((n if sat else -n,))
    return f


def disconnected_control() -> Formula:
    a = equality_path(3, True)
    b = [tuple((1 if x > 0 else -1) * (abs(x) + 10) for x in c)
         for c in equality_path(3, False)]
    return a + b


@dataclass(frozen=True)
class Record:
    opens: Tuple[int, ...]
    clause: Clause
    closes: Tuple[int, ...]


@dataclass
class Block:
    left: Tuple[int, ...]
    right: Tuple[int, ...]
    clauses: Formula


def scoped_records(f: Formula) -> List[Record]:
    first: Dict[int, int] = {}
    last: Dict[int, int] = {}
    for i, c in enumerate(f):
        for v in map(abs, c):
            first.setdefault(v, i)
            last[v] = i
    return [Record(tuple(sorted(v for v, j in first.items() if j == i)), c,
                   tuple(sorted(v for v, j in last.items() if j == i)))
            for i, c in enumerate(f)]


def all_assignments(names):
    yield from itertools.product((False, True), repeat=len(names))


def assignment_dict(names, values):
    return dict(zip(names, values))


def child_formula(block: Block, alpha, beta) -> Formula:
    a = assignment_dict(block.left, alpha)
    for v, val in zip(block.right, beta):
        if v in a:
            assert a[v] == val
        a[v] = val
    return list(block.clauses) + [(v if val else -v,) for v, val in sorted(a.items())]


def encode_cnf(f: Formula) -> str:
    n = max((abs(x) for c in f for x in c), default=0)
    out = f"{n:016b}{len(f):016b}"
    for c in f:
        out += f"{len(c):02b}"
        for lit in c:
            out += ("1" if lit < 0 else "0") + f"{abs(lit):016b}"
    return out


def decode_cnf(bits: str) -> Formula:
    n, m = int(bits[:16], 2), int(bits[16:32], 2)
    p = 32
    out: Formula = []
    for _ in range(m):
        width = int(bits[p:p + 2], 2)
        p += 2
        c = []
        for _ in range(width):
            sign = bits[p] == "1"
            v = int(bits[p + 1:p + 17], 2)
            p += 17
            assert 0 < v <= n
            c.append(-v if sign else v)
        out.append(tuple(c))
    assert p == len(bits)
    return out


def ceil_qroot_pow2(exponent: int, q: int) -> int:
    """Smallest integer b with b**q >= 2**exponent."""
    target = 1 << exponent
    lo, hi = 1, 1 << ((exponent + q - 1) // q)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** q >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


def cap_for_epoch(k: int, theta: Fraction) -> int:
    return ceil_qroot_pow2(theta.numerator * k, theta.denominator)


@dataclass
class Producer:
    records: Sequence[Record]
    pc: int = 0

    def next(self):
        if self.pc == len(self.records):
            return None
        rec = self.records[self.pc]
        self.pc += 1
        return rec


@dataclass
class Stats:
    producer_record_reads: int = 0
    eof_tests: int = 0
    counter_updates: int = 0
    epoch_tests: int = 0
    capacity_tests: int = 0
    blocks: int = 0
    child_calls: int = 0
    child_bits_written: int = 0
    child_bits_read: int = 0
    changed_one_writes: int = 0
    unchanged_zero_writes: int = 0
    max_block_records: int = 0
    max_child_bits: int = 0
    max_active_producers: int = 0
    max_counter_bits: int = 0
    calls_by_depth: Dict[int, int] = field(default_factory=dict)


def asymmetric_blocks(records: Sequence[Record], theta: Fraction,
                      stats: Stats) -> Iterator[Tuple[Producer, Block]]:
    p = Producer(records)
    live: Set[int] = set()
    clauses: Formula = []
    left: Tuple[int, ...] = tuple()
    seen = 0
    k = 0
    epoch_end = 2
    cap = cap_for_epoch(k, theta)

    def emit_block():
        nonlocal clauses
        if not clauses:
            return None
        stats.blocks += 1
        stats.max_block_records = max(stats.max_block_records, len(clauses))
        block = Block(left, tuple(sorted(live)), clauses)
        clauses = []
        return block

    while True:
        stats.eof_tests += 1
        rec = p.next()
        if rec is None:
            block = emit_block()
            if block is not None:
                yield p, block
            break
        stats.producer_record_reads += 1
        seen += 1
        stats.counter_updates += 1
        stats.max_counter_bits = max(stats.max_counter_bits, seen.bit_length())
        if not clauses:
            left = tuple(sorted(live))
        live.update(rec.opens)
        clauses.append(rec.clause)
        live.difference_update(rec.closes)
        stats.epoch_tests += 1
        stats.capacity_tests += 1
        at_epoch_end = seen + 1 == epoch_end
        if len(clauses) == cap or at_epoch_end:
            block = emit_block()
            assert block is not None
            yield p, block
        if at_epoch_end:
            k += 1
            epoch_end <<= 1
            cap = cap_for_epoch(k, theta)
    assert not live


def asymmetric_decide(formula: Formula, depth: int, theta: Fraction,
                      stats: Stats, active: int = 0) -> bool:
    stats.calls_by_depth[depth] = stats.calls_by_depth.get(depth, 0) + 1
    stats.max_active_producers = max(stats.max_active_producers, active + 1)
    reachable: Set[Tuple[bool, ...]] = {tuple()}
    expected_left: Tuple[int, ...] = tuple()
    for producer, block in asymmetric_blocks(scoped_records(formula), theta, stats):
        assert block.left == expected_left
        saved_pc = producer.pc
        nxt: Set[Tuple[bool, ...]] = set()
        for alpha in reachable:
            amap = assignment_dict(block.left, alpha)
            for beta in all_assignments(block.right):
                bmap = assignment_dict(block.right, beta)
                if any(amap[v] != bmap[v] for v in set(amap) & set(bmap)):
                    continue
                child = child_formula(block, alpha, beta)
                bits = encode_cnf(child)
                stats.child_calls += 1
                stats.child_bits_written += len(bits)
                stats.child_bits_read += len(bits)
                stats.changed_one_writes += bits.count("1")
                stats.unchanged_zero_writes += bits.count("0")
                stats.max_child_bits = max(stats.max_child_bits, len(bits))
                parsed = decode_cnf(bits)
                assert parsed == child
                ok = dpll(parsed) if depth == 1 else asymmetric_decide(
                    parsed, depth - 1, theta, stats, active + 1)
                assert producer.pc == saved_pc
                if ok:
                    nxt.add(beta)
        reachable = nxt
        expected_left = block.right
        if not reachable:
            break
    return tuple() in reachable


def schedule_counts(m: int, theta: Fraction) -> Tuple[int, int]:
    cur = 0
    sizes: List[int] = []
    k = 0
    epoch_end = 2
    cap = cap_for_epoch(k, theta)
    for seen in range(1, m + 1):
        cur += 1
        at_epoch_end = seen + 1 == epoch_end
        if cur == cap or at_epoch_end:
            sizes.append(cur)
            cur = 0
        if at_epoch_end:
            k += 1
            epoch_end <<= 1
            cap = cap_for_epoch(k, theta)
    if cur:
        sizes.append(cur)
    return len(sizes), max(sizes)


def main() -> None:
    thetas = [Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2)]
    checks = 0
    schedule_rows = []
    selected = {1, 2, 3, 7, 16, 31, 64, 255, 1024, 4096}
    for theta in thetas:
        for m in range(1, 4097):
            blocks, max_block = schedule_counts(m, theta)
            th = float(theta)
            ctheta = 2 ** (1 - th) / (2 ** (1 - th) - 1)
            q_bound = math.ceil(ctheta * m ** (1 - th) + math.log2(m) + 1)
            b_bound = math.ceil(m ** th) + 1
            assert blocks <= q_bound
            assert max_block <= b_bound
            checks += 2
            if m in selected:
                schedule_rows.append({"theta": str(theta), "M": m,
                                      "blocks": blocks, "max_block": max_block,
                                      "q_bound": q_bound, "b_bound": b_bound})

    cases = []
    for n in range(2, 5):
        cases.append((f"equality_{n}_sat", equality_path(n, True), True))
        cases.append((f"equality_{n}_unsat", equality_path(n, False), False))
    cases.append(("disconnected_sat_unsat", disconnected_control(), False))

    semantic_rows = []
    for theta in (Fraction(1, 3), Fraction(1, 2)):
        for depth in (1, 2):
            for name, formula, expected in cases:
                stats = Stats()
                got = asymmetric_decide(formula, depth, theta, stats)
                assert dpll(formula) == expected == got
                assert stats.max_active_producers == depth
                assert stats.child_bits_written == (
                    stats.changed_one_writes + stats.unchanged_zero_writes)
                checks += 3
                semantic_rows.append({
                    "theta": str(theta), "depth": depth, "name": name,
                    "expected": expected, "root_records": len(scoped_records(formula)),
                    "stats": {**{k: v for k, v in vars(stats).items()
                                  if k != "calls_by_depth"},
                              "calls_by_depth": {str(k): v for k, v in
                                                 sorted(stats.calls_by_depth.items())}},
                })

    out = {
        "run_id": "ARC_ASYMMETRIC_ANYTIME_FUSION167",
        "status": "COMPUTATIONAL",
        "random_seed": None,
        "theta_values": [str(x) for x in thetas],
        "exhaustive_schedule_lengths": [1, 4096],
        "schedule_rows": schedule_rows,
        "semantic_cases": len(semantic_rows),
        "semantic_rows": semantic_rows,
        "assertion_groups": checks,
        "failures": 0,
        "limitations": [
            "finite schedule checks do not prove the geometric-sum theorem",
            "finite ordinary-CNF Horn/2SAT and affine-semantic controls only",
            "logical event counters are not FLMV primitive traces",
            "does not construct the all-input scoped normalizer",
            "does not prove ARC-EDGE-90 or P versus NP",
        ],
    }
    path = HERE / "2026-10-25_0648_ARC_ASYMMETRIC_ANYTIME_FUSION167_results.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"schedule_instances": len(thetas) * 4096,
                      "semantic_cases": len(semantic_rows),
                      "assertion_groups": checks, "failures": 0,
                      "output": str(path)}))


if __name__ == "__main__":
    main()
