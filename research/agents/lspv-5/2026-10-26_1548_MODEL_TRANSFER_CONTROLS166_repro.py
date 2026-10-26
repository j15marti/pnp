#!/usr/bin/env python3
"""Finite controls for MODEL-TRANSFER-CONTROLS166.

No SAT lower bound is tested here.  The checks isolate machine-model
accounting, crossing-record completeness, and an abstract equality layout.
"""

from __future__ import annotations

import hashlib
import json
import math


checks = 0


def check(cond: bool) -> None:
    global checks
    checks += 1
    if not cond:
        raise AssertionError(f"failed check {checks}")


def logbits(x: int) -> int:
    return max(1, math.ceil(math.log2(x + 2)))


def conservative_simulation(n: int, t: int, s: int) -> dict[str, int]:
    # Constant-size control/delimiter slack is displayed, not optimized.
    footprint = n + s + logbits(t) + 8
    return {"N": n, "Tk": t, "Sk": s, "P1_upper": footprint,
            "T1_upper": t * footprint}


def abstract_exact22_layout(m: int) -> dict[str, int]:
    # One fixed-width sign record per logical equality bit on each side;
    # the middle gap has the same physical span.  This is a layout control,
    # not the unpublished CNF generator.
    width = max(4, logbits(m))
    left = [i * width for i in range(m)]
    right0 = 2 * m * width
    right = [right0 + i * width for i in range(m)]
    n = 3 * m * width

    # Indexed RAT: write two O(log N)-bit addresses and read two bits.
    rat_bit_steps = 2 * m * (logbits(n) + 1)

    # One sequential input head, O(log N) memory, shuttle from each left
    # record to its right mate and back to the next left record.
    pos = 0
    one_head_moves = 0
    for i in range(m):
        one_head_moves += abs(pos - left[i])
        pos = left[i]
        one_head_moves += abs(pos - right[i])
        pos = right[i]
        if i + 1 < m:
            one_head_moves += abs(pos - left[i + 1])
            pos = left[i + 1]

    # Two independently movable read-only heads: position the second head,
    # then scan both fixed-width streams monotonically.
    two_head_moves = right0 + 2 * m * width
    return {
        "m": m,
        "record_width": width,
        "N": n,
        "rat_bit_steps": rat_bit_steps,
        "one_head_moves": one_head_moves,
        "two_head_moves": two_head_moves,
    }


sim_rows = []
for n in (16, 64, 256, 1024):
    for t in (n, n * n):
        for s in (1, logbits(n), n):
            row = conservative_simulation(n, t, s)
            check(row["P1_upper"] >= n)
            check(row["P1_upper"] >= n + s)
            check(row["T1_upper"] == t * row["P1_upper"])
            sim_rows.append(row)


# Space-convention countercontrol: the same read-only-input computation can
# use no work cells in Mk, while M1 footprint is at least the entire input.
space_convention = []
for n in (8, 32, 128, 512, 2048):
    mk_work = 0
    m1_footprint = n
    check(mk_work == 0)
    check(m1_footprint >= n)
    space_convention.append({"N": n, "Mk_work": mk_work,
                             "M1_footprint": m1_footprint})


# Snapshot countercontrol.  Omitting the input-head coordinate/scanned symbol
# makes two configurations collide although their next outputs differ.
input_word = "01"
common = {"state": "q_read", "work_contents": "", "work_heads": ()}
c0 = dict(common, input_head=0, scanned=input_word[0])
c1 = dict(common, input_head=1, scanned=input_word[1])
weak0 = (c0["state"], c0["work_contents"], c0["work_heads"])
weak1 = (c1["state"], c1["work_contents"], c1["work_heads"])
full0 = weak0 + (c0["input_head"], c0["scanned"])
full1 = weak1 + (c1["input_head"], c1["scanned"])
check(weak0 == weak1)
check(c0["scanned"] != c1["scanned"])
check(full0 != full1)


layout_rows = []
for m in (2, 4, 8, 16, 32, 64, 128):
    row = abstract_exact22_layout(m)
    check(row["rat_bit_steps"] <= 4 * row["N"])
    check(row["two_head_moves"] <= 2 * row["N"])
    if m >= 4:
        check(row["one_head_moves"] > row["two_head_moves"])
    layout_rows.append(row)


result = {
    "run_id": "MODEL-TRANSFER-CONTROLS166",
    "status": {
        "simulation_inequalities": "upper-construction-only",
        "weak_snapshot_splicing": "falsified",
        "full_fixed-boundary_record_splicing": "not_falsified",
        "sequential_to_indexed_time_equivalence": "falsified",
        "p_vs_np": "OPEN",
    },
    "assertion_groups": checks,
    "simulation_rows": sim_rows,
    "space_convention_rows": space_convention,
    "snapshot_control": {
        "weak_records_equal": weak0 == weak1,
        "next_outputs": [c0["scanned"], c1["scanned"]],
        "full_records_equal": full0 == full1,
    },
    "abstract_equality_layout_rows": layout_rows,
    "limitations": [
        "The equality layout is not the exact22 CNF generator.",
        "Finite counts illustrate model discontinuity and prove no SAT runtime lower bound.",
        "The exact22 crossing theorem remains conditional here on the published locality construction.",
    ],
}
canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["canonical_sha256_before_hash_field"] = hashlib.sha256(canonical.encode()).hexdigest()
print(json.dumps(result, indent=2, sort_keys=True))
