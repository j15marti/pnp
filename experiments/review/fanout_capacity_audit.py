#!/usr/bin/env python3
"""Audit the exact fanout-capacity formula and the SIGNCUBE-ERASURE6 ledger.

The enumerator is deliberately model-local: a source driver and every inserted
buffer can each drive at most k terminal loads.  It does not model placement,
wire length, capacitance, transistor nets, or energy.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def b_min(loads: int, capacity: int) -> int:
    if loads < 1 or capacity < 2:
        raise ValueError("loads >= 1 and capacity >= 2 required")
    return max(0, math.ceil((loads - capacity) / (capacity - 1)))


def brute_min(loads: int, capacity: int) -> int:
    """Enumerate buffer counts until aggregate rooted-tree capacity suffices."""
    for buffers in range(loads + 1):
        # root + buffers supply capacity; each buffer input consumes one slot.
        if capacity * (buffers + 1) >= loads + buffers:
            return buffers
    raise AssertionError("unreachable")


def slope(xs: list[int], ys: list[int]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def signcube_row(d: int) -> dict:
    n = 2**d + 1
    m = d * 2 ** (d + 1)
    g = 3 * m + n - 2
    pin = 6 * m + n - 3
    pout = g
    edges = 6 * m + n - 2
    nets = 3 * m + 2 * n - 2
    singleton_nets = 3 * m - 1
    non_singleton_nets = 2 * n - 1
    buffers = edges - singleton_nets - 2 * non_singleton_nets
    assert buffers == 3 * m - 3 * n + 1
    core_mos = 18 * m + 2 * n - 8
    buffered_mos = core_mos + 4 * buffers
    return {
        "d": d,
        "n": n,
        "m": m,
        "primitive_library": "INV=2 MOS; OR2=6 MOS; AND2=6 MOS; BUF2=4 MOS proxy",
        "raw": {
            "G": g,
            "P_in": pin,
            "P_out": pout,
            "E": edges,
            "W": nets,
            "fanout2_buffers": buffers,
            "nominal_core_MOS": core_mos,
            "nominal_buffered_MOS": buffered_mos,
        },
        "buffer_completed": {
            "G": g + buffers,
            "P_in": pin + buffers,
            "P_out": pout + buffers,
            "E": edges + buffers,
            "W": nets + buffers,
        },
        "normalized": {
            "G": 0,
            "P_in": 0,
            "P_out": 0,
            "E": 1,
            "W": 1,
            "nominal_core_MOS": 0,
            "output_driver_MOS": None,
        },
        "execution": {
            "canonical_text_probe_reads": 3 * m,
            "semantic_certificate_probe_reads": [12, 24, 56, 136, 328, 776][d - 1],
            "source_one_way_tape_cells_crossed": [48, 218, 780, 2448, 7058, 19220][d - 1],
            "cache_replay_transfers": 0,
            "conservative_live_bits": [28, 35, 41, 48, 54, 60][d - 1],
        },
        "physical": {
            "wirelength": None,
            "placed_area": None,
            "transistor_nets": None,
            "measured_energy": None,
        },
    }


def main() -> None:
    formula_checks = 0
    for capacity in range(2, 9):
        for loads in range(1, 257):
            assert b_min(loads, capacity) == brute_min(loads, capacity)
            formula_checks += 1

    rows = [signcube_row(d) for d in range(1, 7)]
    expected_buffers = [4, 34, 118, 334, 862, 2110]
    expected_mos = [70, 290, 874, 2330, 5818, 13946]
    expected_buffered_mos = [86, 426, 1346, 3666, 9266, 22386]
    for row, b, mos, bmos in zip(rows, expected_buffers, expected_mos, expected_buffered_mos):
        assert row["raw"]["fanout2_buffers"] == b
        assert row["raw"]["nominal_core_MOS"] == mos
        assert row["raw"]["nominal_buffered_MOS"] == bmos

    ms = [r["m"] for r in rows]
    trend = {
        "timestamp_kst": "2026-10-19T11:48:00+09:00",
        "report": "FANOUT-CAPACITY-CONSERVATION6",
        "same_library_semantics_model": True,
        "slopes_loglog_vs_m": {
            "raw_G": slope(ms, [r["raw"]["G"] for r in rows]),
            "raw_W": slope(ms, [r["raw"]["W"] for r in rows]),
            "raw_nominal_core_MOS": slope(ms, [r["raw"]["nominal_core_MOS"] for r in rows]),
            "buffered_nominal_MOS": slope(ms, [r["raw"]["nominal_buffered_MOS"] for r in rows]),
            "canonical_text_probe_reads": slope(ms, [r["execution"]["canonical_text_probe_reads"] for r in rows]),
            "normalized_connected_nets": 0.0,
        },
        "rows": rows,
        "strongest_pattern": "Exact fanout completion adds linear declared-library cost, while extensional normalization remains one connected net; neither yields routed or arbitrary-machine lower bounds.",
        "falsifier": "A legal k-load buffer forest serving d sinks with fewer than max(0,ceil((d-k)/(k-1))) buffers, or a SIGNCUBE row contradicting the stated structural fanout partition.",
        "null_policy": "Unknown physical quantities remain null, never zero.",
    }
    result = {
        "report": "FANOUT-CAPACITY-CONSERVATION6",
        "theorem": "B_k(d)=max(0,ceil((d-k)/(k-1))) for a root driver and 1-input k-load buffers",
        "formula_checks": formula_checks,
        "signcube_rows_checked": len(rows),
        "unexpected_failures": 0,
        "trend": trend,
    }
    out = Path("results_local")
    out.mkdir(exist_ok=True)
    (out / "2026-10-19_1148_FANOUT_CAPACITY_CONSERVATION6.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    (out / "2026-10-19_1148_WIRE_SWITCH_TREND6.json").write_text(
        json.dumps(trend, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "formula_checks": formula_checks,
        "signcube_rows_checked": len(rows),
        "slopes": trend["slopes_loglog_vs_m"],
        "unexpected_failures": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
