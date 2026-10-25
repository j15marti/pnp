#!/usr/bin/env python3
"""Finite audit for ARC-ANYTIME-STREAM-FUSION166.

The online consumer is never told the stream length, a polynomial exponent, or
an output upper bound.  It closes blocks at power-of-two epoch boundaries and
uses capacity ceil(sqrt(epoch_start)).  Finite counters are logical Python
counters, not literal FLMV traces.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass, field
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


def assignment_dict(names, values):
    return dict(zip(names, values))


def all_assignments(names):
    yield from itertools.product((False, True), repeat=len(names))


def child_formula(block: Block, alpha, beta) -> Formula:
    a = assignment_dict(block.left, alpha)
    for v, val in zip(block.right, beta):
        if v in a:
            assert a[v] == val
        a[v] = val
    return list(block.clauses) + [(v if val else -v,) for v, val in sorted(a.items())]


def encode_cnf(f: Formula) -> str:
    n = max((abs(x) for c in f for x in c), default=0)
    bits = f"{n:016b}{len(f):016b}"
    for c in f:
        bits += f"{len(c):02b}"
        for lit in c:
            bits += ("1" if lit < 0 else "0") + f"{abs(lit):016b}"
    return bits


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


@dataclass
class Producer:
    records: Sequence[object]
    pc: int = 0
    steps: int = 0

    def next(self):
        self.steps += 1  # EOF tests are charged too.
        if self.pc == len(self.records):
            return None
        rec = self.records[self.pc]
        self.pc += 1
        return rec


@dataclass
class Stats:
    producers: int = 0
    emitted: int = 0
    eof_tests: int = 0
    blocks: int = 0
    epoch_flushes: int = 0
    capacity_flushes: int = 0
    child_calls: int = 0
    serialized_child_bits: int = 0
    max_block: int = 0
    max_active_producers: int = 0
    max_counter_bits: int = 0
    calls_by_depth: Dict[int, int] = field(default_factory=dict)


def cap_for_epoch(k: int) -> int:
    # ceil(sqrt(2**k)), computed with integer arithmetic.
    lo = 1 << k
    return math.isqrt(lo) if math.isqrt(lo) ** 2 == lo else math.isqrt(lo) + 1


def anytime_blocks(records: Sequence[object], stats: Stats) -> Iterator[Tuple[Producer, object]]:
    """Consume a stream without reading len(records) for scheduling."""
    p = Producer(records)
    stats.producers += 1
    live: Set[int] = set()
    clauses: List[object] = []
    left: Tuple[int, ...] = tuple()
    seen = 0
    k = 0
    epoch_end = 2  # 1-indexed positions in epoch 0 are [1,1].
    cap = cap_for_epoch(k)

    def emit_block():
        nonlocal clauses
        if not clauses:
            return None
        stats.blocks += 1
        stats.max_block = max(stats.max_block, len(clauses))
        block = Block(left, tuple(sorted(live)), clauses)
        clauses = []
        return block

    while True:
        rec = p.next()
        if rec is None:
            stats.eof_tests += 1
            block = emit_block()
            if block is not None:
                yield p, block
            break
        seen += 1
        stats.emitted += 1
        stats.max_counter_bits = max(stats.max_counter_bits, seen.bit_length())
        if not clauses:
            left = tuple(sorted(live))
        live.update(rec.opens)
        clauses.append(rec.clause)
        live.difference_update(rec.closes)

        at_epoch_end = seen + 1 == epoch_end
        at_capacity = len(clauses) == cap
        if at_capacity or at_epoch_end:
            if at_epoch_end:
                stats.epoch_flushes += 1
            else:
                stats.capacity_flushes += 1
            block = emit_block()
            assert block is not None
            yield p, block
        if at_epoch_end:
            k += 1
            epoch_end <<= 1
            cap = cap_for_epoch(k)
    assert not live


def anytime_decide(formula, depth: int, stats: Stats, active: int = 0) -> bool:
    assert depth >= 1
    stats.calls_by_depth[depth] = stats.calls_by_depth.get(depth, 0) + 1
    stats.max_active_producers = max(stats.max_active_producers, active + 1)
    records = scoped_records(formula)
    reachable: Set[Tuple[bool, ...]] = {tuple()}
    expected_left: Tuple[int, ...] = tuple()
    for producer, block in anytime_blocks(records, stats):
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
                parsed = decode_cnf(bits)
                assert parsed == child
                stats.child_calls += 1
                stats.serialized_child_bits += len(bits)
                if depth == 1:
                    ok = dpll(parsed)
                else:
                    ok = anytime_decide(parsed, depth - 1, stats, active + 1)
                assert producer.pc == saved_pc
                if ok:
                    nxt.add(beta)
        reachable = nxt
        expected_left = block.right
        if not reachable:
            break
    return tuple() in reachable


def schedule_counts(m: int) -> Tuple[int, int, List[int]]:
    """Independent length-only simulation of the online epoch schedule."""
    assert m >= 1
    sizes: List[int] = []
    cur = 0
    k = 0
    epoch_end = 2
    cap = cap_for_epoch(k)
    for seen in range(1, m + 1):
        cur += 1
        at_epoch_end = seen + 1 == epoch_end
        if cur == cap or at_epoch_end:
            sizes.append(cur)
            cur = 0
        if at_epoch_end:
            k += 1
            epoch_end <<= 1
            cap = cap_for_epoch(k)
    if cur:
        sizes.append(cur)
    return len(sizes), max(sizes), sizes


def main() -> None:
    checks = 0
    schedule_rows = []
    selected = {1, 2, 3, 4, 7, 8, 16, 31, 64, 255, 1024, 4096, 8192}
    # One checkpointable O(limit) stage checks every prefix length.  Recomputing
    # the entire schedule separately for all M would be quadratic and is not
    # part of the mathematical claim.
    cur = completed_blocks = completed_sum = completed_max = 0
    k = 0
    epoch_end = 2
    cap = cap_for_epoch(k)
    for m in range(1, 8193):
        cur += 1
        at_epoch_end = m + 1 == epoch_end
        if cur == cap or at_epoch_end:
            completed_blocks += 1
            completed_sum += cur
            completed_max = max(completed_max, cur)
            cur = 0
        if at_epoch_end:
            k += 1
            epoch_end <<= 1
            cap = cap_for_epoch(k)
        q = completed_blocks + (1 if cur else 0)
        b = max(completed_max, cur)
        # Elementary theorem bounds; constants are deliberately loose.
        q_bound = math.ceil((2 + math.sqrt(2)) * math.sqrt(m) + math.log2(m + 1) + 2)
        b_bound = math.ceil(math.sqrt(m)) + 1
        assert completed_sum + cur == m
        assert q <= q_bound
        assert b <= b_bound
        checks += 3
        if m in selected:
            q2, b2, sizes = schedule_counts(m)
            assert (q, b) == (q2, b2)
            schedule_rows.append({"M": m, "blocks": q, "max_block": b,
                                  "q_bound": q_bound, "b_bound": b_bound,
                                  "sizes": sizes})

    cases = []
    for n in range(2, 6):
        cases.append((f"equality_{n}_sat", equality_path(n, True), True))
        cases.append((f"equality_{n}_unsat", equality_path(n, False), False))
    cases.append(("disconnected_sat_unsat", disconnected_control(), False))

    semantic_rows = []
    for depth in (1, 2):
        for name, formula, expected in cases:
            direct = dpll(formula)
            stats = Stats()
            got = anytime_decide(formula, depth, stats)
            assert direct == expected == got
            assert stats.max_active_producers == depth
            assert stats.max_counter_bits <= max(1, stats.emitted.bit_length())
            checks += 3
            semantic_rows.append({
                "name": name, "depth": depth, "expected": expected,
                "root_records": len(scoped_records(formula)),
                "stats": {**{k: v for k, v in vars(stats).items() if k != "calls_by_depth"},
                          "calls_by_depth": {str(k): v for k, v in sorted(stats.calls_by_depth.items())}},
            })

    result = {
        "run_id": "ARC_ANYTIME_STREAM_FUSION166",
        "status": "COMPUTATIONAL",
        "random_seed": None,
        "exhaustive_schedule_lengths": [1, 8192],
        "schedule_rows": schedule_rows,
        "semantic_cases": len(semantic_rows),
        "semantic_rows": semantic_rows,
        "assertion_groups": checks,
        "failures": 0,
        "limitations": [
            "finite schedule verification does not prove the geometric-sum theorem",
            "finite ordinary-CNF Horn/2SAT/affine-semantic controls only",
            "Python counters are not FLMV primitive traces",
            "does not construct the all-input scoped normalizer",
            "does not prove ARC-EDGE-90 or P versus NP",
        ],
    }
    out = HERE / "2026-10-25_0548_ARC_ANYTIME_STREAM_FUSION166_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"schedule_lengths": 8192, "semantic_cases": len(semantic_rows),
                      "assertion_groups": checks, "failures": 0, "output": str(out)}))


if __name__ == "__main__":
    main()
