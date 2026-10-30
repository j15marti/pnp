#!/usr/bin/env python3
"""Finite controls for LSPV-5 STREAMING-JOIN-FRONTIER-REFEREE209.

Counts logical table bits.  These are not native Python or TM space measurements.
"""
from __future__ import annotations

import itertools
import json
import math
import random
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Child:
    peak: int
    out: int


def all_live_peak(order: tuple[Child, ...], parent_out: int, scratch: int = 0) -> int:
    prefix = 0
    peak = 0
    for c in order:
        peak = max(peak, prefix + c.peak)
        prefix += c.out
    return max(peak, prefix + parent_out + scratch)


def all_live_opt(children: tuple[Child, ...], parent_out: int, scratch: int = 0):
    order = tuple(sorted(children, key=lambda c: c.peak - c.out, reverse=True))
    return all_live_peak(order, parent_out, scratch), order


def all_live_bruteforce(children: tuple[Child, ...], parent_out: int, scratch: int = 0):
    vals = [(all_live_peak(p, parent_out, scratch), p) for p in itertools.permutations(children)]
    return min(vals, key=lambda z: z[0])


def stream_peak_equal_output(order: tuple[Child, ...], table_bits: int, local_scratch: int = 0) -> int:
    """Pointwise intersection: reuse first output as accumulator, discard later outputs."""
    if not order:
        return table_bits + local_scratch
    peak = order[0].peak
    for c in order[1:]:
        peak = max(peak, table_bits + c.peak)
    return max(peak, table_bits + local_scratch)


def stream_opt_equal_output(children: tuple[Child, ...], table_bits: int, local_scratch: int = 0):
    # The child with largest peak is the unique relevant first-choice priority.
    order = tuple(sorted(children, key=lambda c: c.peak, reverse=True))
    return stream_peak_equal_output(order, table_bits, local_scratch), order


def stream_bruteforce(children: tuple[Child, ...], table_bits: int, local_scratch: int = 0):
    vals = [(stream_peak_equal_output(p, table_bits, local_scratch), p)
            for p in itertools.permutations(children)]
    return min(vals, key=lambda z: z[0])


def mask_true(w: int) -> int:
    return (1 << (1 << w)) - 1


def mask_literal(w: int, var: int, positive: bool) -> int:
    m = 0
    for a in range(1 << w):
        bit = (a >> var) & 1
        if bool(bit) == positive:
            m |= 1 << a
    return m


def run():
    started = time.perf_counter()
    rng = random.Random(2091748)

    # Local exchange theorem: descending (peak-output) is optimal for all-live joins.
    all_live_trials = 0
    for arity in range(1, 8):
        for _ in range(120):
            children = tuple(Child(rng.randint(1, 30), rng.randint(1, 12)) for _ in range(arity))
            # A valid child peak includes its output.
            children = tuple(Child(max(c.peak, c.out), c.out) for c in children)
            parent_out = rng.randint(1, 12)
            scratch = rng.randint(0, 7)
            got, _ = all_live_opt(children, parent_out, scratch)
            want, _ = all_live_bruteforce(children, parent_out, scratch)
            assert got == want
            all_live_trials += 1

    # Streaming fold: largest peak first is optimal when every child output has B bits.
    stream_trials = 0
    for arity in range(1, 8):
        for _ in range(120):
            B = rng.randint(1, 20)
            children = tuple(Child(rng.randint(B, 5 * B), B) for _ in range(arity))
            scratch = rng.randint(0, B)
            got, _ = stream_opt_equal_output(children, B, scratch)
            want, _ = stream_bruteforce(children, B, scratch)
            assert got == want
            stream_trials += 1

    # Exact high-fanout star formulas.
    star_rows = []
    for h in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
        for w in [1, 2, 4, 8, 12]:
            B = 1 << w
            children = tuple(Child(B, B) for _ in range(h))
            live, _ = all_live_opt(children, B)
            stream, _ = stream_opt_equal_output(children, B)
            assert live == (h + 1) * B
            assert stream == (B if h == 1 else 2 * B)
            star_rows.append({"h": h, "w": w, "B": B,
                              "all_live_bits": live, "stream_bits": stream,
                              "ratio": live / stream})

    # Both answer classes on a common-interface star.  Each child table is generated,
    # intersected, and discarded.  No answer bit is supplied.
    semantic_rows = []
    for w in range(1, 13):
        full = mask_true(w)
        pos = mask_literal(w, 0, True)
        neg = mask_literal(w, 0, False)
        for h in [2, 3, 5, 8, 16, 32]:
            sat_children = [pos] + [full] * (h - 1)
            unsat_children = [pos, neg] + [full] * (h - 2)
            for label, tables, expected in [("SAT", sat_children, True),
                                            ("UNSAT", unsat_children, False)]:
                acc = tables[0]
                peak_tables = 1
                for tab in tables[1:]:
                    peak_tables = max(peak_tables, 2)
                    acc &= tab
                assert bool(acc) == expected
                if expected:
                    witness = (acc & -acc).bit_length() - 1
                    assert all((tab >> witness) & 1 for tab in tables)
                semantic_rows.append({"w": w, "h": h, "label": label,
                                      "valid_assignments": acc.bit_count(),
                                      "peak_live_tables": peak_tables})

    # Balanced b-ary equal-table recurrence, contrasting sibling retention with folding.
    balanced = []
    for b in [2, 3, 4, 8]:
        for depth in range(0, 9):
            B = 64
            all_peak = B
            stream_peak = B
            for _ in range(depth):
                cs_all = tuple(Child(all_peak, B) for _ in range(b))
                cs_stream = tuple(Child(stream_peak, B) for _ in range(b))
                all_peak, _ = all_live_opt(cs_all, B)
                stream_peak, _ = stream_opt_equal_output(cs_stream, B)
            expected_all = B if depth == 0 else B * (depth * (b - 1) + 2)
            expected_stream = B * (depth + 1)
            assert all_peak == expected_all
            assert stream_peak == expected_stream
            balanced.append({"branching": b, "depth": depth,
                             "all_live_bits": all_peak, "stream_bits": stream_peak})

    # Polynomial-exponent ledger for h=N^mu, B=N^beta.
    exponent_rows = []
    for mu in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for beta in [0.0, 0.25, 0.5, 1.0]:
            exponent_rows.append({"mu": mu, "beta": beta,
                                  "time": mu + beta,
                                  "all_live_space": mu + beta,
                                  "stream_space": beta})

    out = {
        "run_id": "STREAMING-JOIN-FRONTIER-REFEREE209",
        "status": "COMPUTATIONAL finite controls for a proved symbolic theorem",
        "seed": 2091748,
        "all_live_order_trials": all_live_trials,
        "stream_order_trials": stream_trials,
        "star_rows": star_rows,
        "semantic_rows": semantic_rows,
        "balanced_rows": balanced,
        "exponent_rows": exponent_rows,
        "elapsed_seconds": time.perf_counter() - started,
        "notes": [
            "Counts are logical explicit-table bits, not Python heap or TM cells.",
            "Streaming applies only to an associative pointwise common-interface fold.",
            "No general SAT coverage or lower bound is asserted."
        ]
    }
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
