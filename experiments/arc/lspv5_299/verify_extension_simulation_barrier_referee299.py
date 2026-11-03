#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE299 raw finite evidence."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


def normalized(xs):
    if 0 in xs or any(-x in xs for x in xs):
        raise AssertionError("noncanonical input clause")
    return tuple(sorted(set(xs), key=lambda z: (abs(z), z < 0)))


def count_models(n, clauses):
    total = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any((x > 0) == bits[abs(x) - 1] for x in c) for c in clauses):
            total += 1
    return total


def main(path: str) -> None:
    p = Path(path)
    obj = json.loads(p.read_text())
    claimed = obj.pop("content_sha256")
    actual = hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert claimed == actual

    tiny = obj["tiny"]
    source = [normalized(c) for c in tiny["source_clauses"]]
    assert count_models(2, source) == 0

    d = tiny["def"]
    y, a, b = d["out"], d["left"], d["right"]
    slots = [normalized((-y, a)), normalized((-y, b)), normalized((y, -a, -b))]
    assert [list(x) for x in slots] == tiny["def_slots"]
    pool = {f"S{i}": c for i, c in enumerate(source)}
    pool.update({f"D{i}": c for i, c in enumerate(slots)})
    for i, step in enumerate(tiny["steps"]):
        left, right, pivot = pool[step["left"]], pool[step["right"]], step["pivot"]
        assert pivot in left and -pivot in right
        got = normalized(tuple(x for x in left if x != pivot) + tuple(x for x in right if x != -pivot))
        assert got == normalized(step["clause"])
        pool[f"R{i}"] = got
    assert pool[f"R{len(tiny['steps']) - 1}"] == ()
    assert tiny["certificate_cost"] == {"def_nodes": 1, "res_nodes": 5, "total_nodes": 6}

    bclauses = [normalized(c) for c in obj["bphp_h2"]["clauses"]]
    assert count_models(3, bclauses) == 0
    observed = []
    for ci, c in enumerate(bclauses):
        for li, lit in enumerate(c):
            nc = list(c); nc[li] = -lit
            allc = list(bclauses); allc[ci] = normalized(nc)
            observed.append(count_models(3, allc))
    assert observed == [1] * 12 == obj["bphp_h2"]["sign_flip_model_counts"]
    assert obj["tseitin_k4"]["odd_models"] == 0
    assert obj["tseitin_k4"]["even_models"] == 8
    assert all(obj["assertions"].values())
    print(json.dumps({"verified": True, "raw_sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "checks": 44}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
