#!/usr/bin/env python3
"""Independent direct checker for strict_c_selector_adversary_raw.json.

Uses an explicit adjacency matrix and does not import producer functions.
Same-author independent implementation; peer review remains pending.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path

R = (
    (0, 1, 0, 1, 0),
    (0, 0, 1, 0, 1),
    (1, 0, 0, 1, 0),
    (0, 1, 0, 0, 1),
    (1, 0, 1, 0, 0),
)


def c_value(a, b, c):
    return (R[a][b] and R[b][c] and R[c][a]) or (
        R[a][c] and R[c][b] and R[b][a]
    )


path = Path(sys.argv[1] if len(sys.argv) > 1 else "strict_c_selector_adversary_raw.json")
data = json.loads(path.read_text())
clauses = data["clauses"]
checks = 0
selector = set()
for item in data["deletion_witnesses"]:
    assignment = item["assignment"]
    failed = []
    assert len(assignment) == data["source"]["total_variables"]
    for i, (h, u, v) in enumerate(clauses):
        checks += 1
        if not c_value(assignment[h], assignment[u], assignment[v]):
            failed.append(i)
    assert failed == [item["omitted_clause"]]
    assert list(item["omitted_edge"]) == clauses[item["omitted_clause"]][1:]
    assert item["unique_refutable_block"] == item["omitted_clause"]
    selector.add(item["unique_refutable_block"])

assert selector == set(range(len(clauses)))
assert sum(c_value(*row) for row in itertools.product(range(5), repeat=3)) == 30
for entry in data["minimal_catalogue_recheck"]:
    assert entry["distance_filter"][0] is False

print(
    json.dumps(
        {
            "status": "PASS",
            "strict_C_deletion_witnesses": len(data["deletion_witnesses"]),
            "strict_C_clause_checks": checks,
            "unique_selector_blocks": len(selector),
            "raw_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "peer_review": "PENDING; separate implementation by same author",
        },
        indent=2,
        sort_keys=True,
    )
)
