#!/usr/bin/env python3
"""
Tiny quantifier sanity check for wrapper-as-SAT.

A seed selects one of four deterministic wrapper routes.
Three routes return the correct endpoint 1; one route returns 0.

Plain existential SAT over the seed asks whether ANY good route exists.
Universal wrapper correctness asks whether ALL routes are good.
The two properties differ.
"""

import itertools
import json

def endpoint(s0, s1):
    # Three good routes, one deliberately bad route.
    return 0 if (s0, s1) == (1, 1) else 1

rows = []
for s0, s1 in itertools.product([0, 1], repeat=2):
    rows.append({"seed": [s0, s1], "endpoint": endpoint(s0, s1)})

result = {
    "routes": rows,
    "exists_good_route": any(r["endpoint"] == 1 for r in rows),
    "all_routes_good": all(r["endpoint"] == 1 for r in rows),
    "interpretation": (
        "Existential SAT over route variables accepts because at least one "
        "consistent good route exists, even though universal route correctness fails."
    ),
}
print(json.dumps(result, indent=2))
