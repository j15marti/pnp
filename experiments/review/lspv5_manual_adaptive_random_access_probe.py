#!/usr/bin/env python3
"""Finite controls for a restricted oblivious-address lower bound.
This is NOT a random-access SAT lower bound or an FLMV simulation.
"""
import json

res = {"tag":"RAM-FIXED-TRACE-2026-11-09", "model":"read-only index table with M independent Boolean cells; address tape in binary", "scenarios":[],"checks":0, "failures":0}

def check(b, label):
    res["checks"] += 1
    if not b:
        res["failures"] += 1
        raise AssertionError(label)

for d in range(1, 10):
    m = 1 << d
    omitted_cell_adversaries = 0
    exact_reuse_cases = 0
    spurious_marginal_states = 0
    corrupted_reuse_cases = 0
    for j in range(m):
        zero_table = [0] * m
        flipped_table = zero_table.copy()
        flipped_table[j] = 1
        schedule = tuple(i for i in range(m) if i != j)
        transcript0 = tuple(zero_table[i] for i in schedule)
        transcript1 = tuple(flipped_table[i] for i in schedule)
        check(transcript0 == transcript1, "two tables indistinguishable")
        check(zero_table[j] != flipped_table[j], "index answers differ")
        omitted_cell_adversaries += 1
        table = zero_table.copy()
        table[j] = 1
        check(table[j] == 1, "exact same-source write/read")
        exact_reuse_cases += 1
        other = j ^ 1
        check(table[other] == 0, "corrupt same-address assumption control")
        corrupted_reuse_cases += 1
    for w in range(m):
        for r in range(m):
            observed = int(w == r)
            check(observed in (0, 1), "Boolean table read")
            if w != r:
                check(observed == 0, "off-diagonal spurious abstract read")
                spurious_marginal_states += 1
            else:
                check(observed == 1, "diagonal is legal concrete execution")
    res["scenarios"].append({"address_bits":d,"table_cells":m,"omitted_cell_witnesses":omitted_cell_adversaries,"exact_read_after_write":exact_reuse_cases,"corruption_checks":corrupted_reuse_cases,"marginal_spurious_off_diagonal":spurious_marginal_states,"input_bits_m_plus_d":m+d})
res["total_omitted_cell_witnesses"] = sum(s["omitted_cell_witnesses"] for s in res["scenarios"])
res["total_marginal_spurious_states"] = sum(s["marginal_spurious_off_diagonal"] for s in res["scenarios"])
print(json.dumps(res,indent=2))
