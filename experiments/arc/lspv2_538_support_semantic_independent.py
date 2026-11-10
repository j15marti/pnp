#!/usr/bin/env python3
"""LSPV-2/538 independent truth-functional check. NOT the native historical checker."""
from itertools import product
import json

rows = []
for x0, x1, x2, x12 in product((0, 1), repeat=4):
    # Odd-charge cubic Tseitin vertex, source clauses ANDed.
    premises = bool(x0 ^ x2 ^ x12)
    # The accepted mutated AND3 node says support is string "012", table is 90.
    pos = x0 + 2*x1 + 4*x2
    claimed = bool((90 >> pos) & 1)
    rows.append({"x0": x0, "x1": x1, "x2": x2, "x12": x12,
                 "premises": premises, "claimed": claimed,
                 "mismatch": premises != claimed})
assert len(rows) == 16
assert sum(z["mismatch"] for z in rows) == 8
assert any(z["x0"] == z["x1"] == z["x2"] == 0 and
           z["x12"] == 1 and z["premises"] and not z["claimed"] for z in rows)
print(json.dumps({"id":"LSPV2-538-independent-original-variable-replay",
                  "assignments":16, "semantic_mismatches":8,
                  "scope":"mathematical countermodel only; does not run native checker"},
                 sort_keys=True))
