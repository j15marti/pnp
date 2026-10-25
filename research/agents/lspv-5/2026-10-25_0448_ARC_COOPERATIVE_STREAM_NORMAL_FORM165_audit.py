#!/usr/bin/env python3
"""Finite audit for ARC-COOPERATIVE-STREAM-NORMAL-FORM165.

This is a logical/counter audit, not a literal FLMV machine emulator.  It
checks that a headerless deterministic stream can be consumed once while its
program counter is retained across recursive child calls, and contrasts this
with restart-from-origin block access.  Exact SAT semantics and ordinary-child
serialization are delegated to the independently published FUSION164 audit.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Sequence, Set, Tuple


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "2026-10-25_0348_ARC_STREAM_SCOPE_FUSION164_audit.py"
SPEC = importlib.util.spec_from_file_location("fusion164", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
fusion = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = fusion
SPEC.loader.exec_module(fusion)


@dataclass
class HeaderlessProducer:
    """Explicit deterministic producer state; no output-count header."""

    records: Sequence[object]
    pc: int = 0
    transitions: int = 0
    eof_tests: int = 0
    resume_count: int = 0

    def step(self):
        self.eof_tests += 1
        if self.pc == len(self.records):
            return None
        rec = self.records[self.pc]
        self.pc += 1
        self.transitions += 1
        return rec


@dataclass
class AuditStats:
    producers: int = 0
    emitted_records: int = 0
    eof_tests: int = 0
    resumes: int = 0
    blocks: int = 0
    children: int = 0
    serialized_child_bits: int = 0
    max_block_clauses: int = 0
    max_active_producers: int = 0
    max_pc_bits: int = 0
    calls_by_depth: Dict[int, int] = field(default_factory=dict)


def certified_upper_bound(m: int) -> int:
    """A public computable upper bound, deliberately not an exact header."""
    assert m >= 1
    return 1 << math.ceil(math.log2(m + 1))


def headerless_blocks(records: Sequence[object], upper: int, stats: AuditStats):
    assert len(records) <= upper
    cap = max(1, math.ceil(math.sqrt(upper)))
    producer = HeaderlessProducer(records)
    stats.producers += 1
    live: Set[int] = set()
    left: Tuple[int, ...] = tuple()
    clauses = []
    while True:
        rec = producer.step()
        if rec is None:
            break
        stats.emitted_records += 1
        if not clauses:
            left = tuple(sorted(live))
        live.update(rec.opens)
        clauses.append(rec.clause)
        live.difference_update(rec.closes)
        if len(clauses) == cap:
            producer.resume_count += 1
            stats.resumes += 1
            stats.blocks += 1
            stats.max_block_clauses = max(stats.max_block_clauses, len(clauses))
            yield producer, fusion.Block(left, tuple(sorted(live)), clauses)
            clauses = []
    if clauses:
        stats.blocks += 1
        stats.max_block_clauses = max(stats.max_block_clauses, len(clauses))
        yield producer, fusion.Block(left, tuple(sorted(live)), clauses)
    assert not live
    stats.eof_tests += producer.eof_tests
    stats.max_pc_bits = max(stats.max_pc_bits, max(1, producer.pc.bit_length()))
    assert producer.transitions == len(records)


def cooperative_decide(formula, depth: int, stats: AuditStats, active: int = 0) -> bool:
    assert depth >= 1
    stats.calls_by_depth[depth] = stats.calls_by_depth.get(depth, 0) + 1
    stats.max_active_producers = max(stats.max_active_producers, active + 1)
    records = fusion.scoped_records(formula)
    upper = certified_upper_bound(len(records))
    reachable: Set[Tuple[bool, ...]] = {tuple()}
    expected_left: Tuple[int, ...] = tuple()
    for producer, block in headerless_blocks(records, upper, stats):
        assert block.left == expected_left
        saved_pc = producer.pc
        nxt: Set[Tuple[bool, ...]] = set()
        for alpha in reachable:
            amap = fusion.assignment_dict(block.left, alpha)
            for beta in fusion.all_assignments(block.right):
                bmap = fusion.assignment_dict(block.right, beta)
                if any(amap[v] != bmap[v] for v in set(amap) & set(bmap)):
                    continue
                child = fusion.child_formula(block, alpha, beta)
                bits = fusion.encode_cnf(child)
                parsed = fusion.decode_cnf(bits)
                assert parsed == child
                stats.children += 1
                stats.serialized_child_bits += len(bits)
                if depth == 1:
                    ok = fusion.dpll(parsed)
                else:
                    ok = cooperative_decide(parsed, depth - 1, stats, active + 1)
                # Parent producer is suspended: its entire logical state is
                # retained and must be identical after the child returns.
                assert producer.pc == saved_pc
                if ok:
                    nxt.add(beta)
        reachable = nxt
        expected_left = block.right
        if not reachable:
            break
    return tuple() in reachable


def restart_prefix_visits(m: int, cap: int) -> Tuple[int, List[int]]:
    """Events emitted when block j is obtained by restarting at position 0."""
    assert m >= 1 and cap >= 1
    q = math.ceil(m / cap)
    prefixes = [min(j * cap, m) for j in range(1, q + 1)]
    return sum(prefixes), prefixes


def main() -> None:
    cases = []
    for n in range(2, 6):
        cases.append((f"equality_{n}_sat", fusion.equality_path(n, True), True))
        cases.append((f"equality_{n}_unsat", fusion.equality_path(n, False), False))
    cases.append(("disconnected_sat_unsat", fusion.disconnected_control(), False))

    rows: List[dict] = []
    assertions = 0
    for depth in (1, 2):
        for name, formula, expected in cases:
            records = fusion.scoped_records(formula)
            upper = certified_upper_bound(len(records))
            cap = math.ceil(math.sqrt(upper))
            replay, prefixes = restart_prefix_visits(len(records), cap)
            stats = AuditStats()
            got = cooperative_decide(formula, depth, stats)
            direct = fusion.dpll(formula)
            assert direct == expected == got
            assert stats.max_active_producers == depth
            assert stats.emitted_records >= len(records)
            assert replay == sum(prefixes)
            assert replay >= len(records)
            assertions += 6
            rows.append({
                "name": name,
                "depth": depth,
                "expected": expected,
                "root_records": len(records),
                "certified_upper_bound": upper,
                "block_capacity": cap,
                "root_restart_prefixes": prefixes,
                "root_restart_record_visits": replay,
                "root_cooperative_record_visits": len(records),
                "stats": {
                    **{k: v for k, v in vars(stats).items() if k != "calls_by_depth"},
                    "calls_by_depth": {str(k): v for k, v in sorted(stats.calls_by_depth.items())},
                },
            })

    symbolic = []
    for m in (16, 64, 256, 1024, 4096):
        cap = math.isqrt(m)
        replay, _ = restart_prefix_visits(m, cap)
        exact = m * (m // cap + 1) // 2
        assert cap * cap == m and replay == exact
        symbolic.append({
            "M": m,
            "B": cap,
            "cooperative_visits": m,
            "restart_visits": replay,
            "restart_over_cooperative": replay / m,
        })
        assertions += 2

    result = {
        "run_id": "ARC_COOPERATIVE_STREAM_NORMAL_FORM165",
        "status": "COMPUTATIONAL",
        "random_seed": None,
        "cases": len(rows),
        "assertion_groups": assertions,
        "failures": 0,
        "symbolic_square_cases": symbolic,
        "rows": rows,
        "limitations": [
            "finite proper-3CNF affine/2SAT-semantic controls only",
            "Python object counters are not FLMV primitive traces",
            "producer records are prebuilt for the finite audit",
            "does not construct an all-input favorable normalizer",
            "does not prove ARC-EDGE-90 or P versus NP",
        ],
    }
    out = HERE / "2026-10-25_0448_ARC_COOPERATIVE_STREAM_NORMAL_FORM165_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(rows), "assertion_groups": assertions, "failures": 0, "output": str(out)}))


if __name__ == "__main__":
    main()
