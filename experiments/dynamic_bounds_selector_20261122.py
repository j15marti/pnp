"""Audit selection information on the pinned synchronized-cycle semantics."""
from itertools import product
from collections import Counter
import json


def decision(top, bottom):
    relations = {"A": {(0, 0), (1, 1), (1, 0)}, "C": {(0, 1), (1, 0)}}
    current = {(0, 0), (1, 1)}
    for a, b in zip(top, bottom):
        edge = relations[a] & relations[b]
        current = {(x, z) for x, y in current for u, z in edge if y == u}
    return any(x == y for x, y in current)


def audit(t):
    width = t.bit_length() - 1
    assert 1 << width == t
    counts = Counter()
    indices = Counter()
    payloads = set()
    records = set()
    for top in product("AC", repeat=t):
        counts["SAT" if decision(top, "A" * t) else "UNSAT"] += 1
        index = int("".join("1" if x == "C" else "0" for x in top[:width]), 2)
        indices[index] += 1
        payloads.add("0")
        record = format(index, f"0{width}b") + "0"
        assert int(record[:width], 2) == index
        records.add(record)
    assert len(set(indices.values())) == 1
    assert len(payloads) == 1 and len(records) == t
    return {"t": t, "inputs": 2**t, "labels": dict(counts),
            "obligation_entropy_bits": width, "payload_entropy_bits": 0,
            "selected_events": 1, "index_bits": width,
            "indexed_record_bits": width + 1}


if __name__ == "__main__":
    print(json.dumps([audit(t) for t in (4, 8)], indent=2))
