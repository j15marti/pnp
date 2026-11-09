#!/usr/bin/env python3
"""Independent replay verifier for the compact LSPV-5/449 certificate."""

from __future__ import annotations

import json
import sys
from itertools import combinations, product


def C(xs):
    out = frozenset(xs)
    assert not any(-x in out for x in out)
    return out


def resolve(a, b, p):
    assert p in a and -p in b
    out = (a - {p}) | (b - {-p})
    assert not any(-x in out for x in out)
    return out


def expected_sources():
    src = {C((1, 2, 3)), C((4, 5, 6))}
    for group in ((1, 2, 3), (4, 5, 6)):
        src |= {C((-a, -b)) for a, b in combinations(group, 2)}
    gates = []
    q = 7
    terms = []
    for i in range(3):
        row = []
        for j in range(3):
            gates.append((q, i + 1, j + 4)); row.append(q); q += 1
        terms.append(row)
    for k in range(3):
        bucket = [terms[i][j] for i in range(3) for j in range(3) if (i + j) % 3 == k]
        gates.append((q, -bucket[0], -bucket[1])); n12 = q; q += 1
        gates.append((q, n12, -bucket[2])); q += 1
    assert q == 22
    for out, a, b in gates:
        assert abs(a) != abs(b) and abs(a) < out and abs(b) < out
        src |= {C((-out, a)), C((-out, b)), C((out, -a, -b))}
    return src, gates


def replay(data, mutate=None):
    lines = json.loads(json.dumps(data["certificate"]))
    if mutate == "pivot":
        next(x for x in lines if x["kind"] == "RES")["pivot"] = 999
    elif mutate == "parent":
        next(x for x in lines if x["kind"] == "RES")["left"] = 999
    elif mutate == "clause":
        next(x for x in lines if x["kind"] == "RES")["clause"] = [999]
    expected, gates = expected_sources()
    seen, actual_sources = [], set()
    for i, line in enumerate(lines):
        assert line["id"] == i
        clause = C(line["clause"])
        if line["kind"] == "SOURCE":
            assert "left" not in line and "right" not in line and "pivot" not in line
            actual_sources.add(clause)
        else:
            l, r, p = line["left"], line["right"], line["pivot"]
            assert 0 <= l < i and 0 <= r < i
            assert resolve(seen[l], seen[r], p) == clause
        seen.append(clause)
    assert actual_sources == expected and len(actual_sources) == 53
    expected_targets = {C((-17, -19, -21)), C((17, 19)), C((17, 21)), C((19, 21))}
    got_targets = set()
    for key, idx in data["compact_target_line_ids"].items():
        parsed = C(json.loads(key.replace("(", "[").replace(")", "]")))
        assert seen[idx] == parsed
        got_targets.add(parsed)
    assert got_targets == expected_targets
    return len(seen), len(gates)


def main(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    lines, gates = replay(data)
    rejects = 0
    for mutation in ("pivot", "parent", "clause"):
        try:
            replay(data, mutation)
        except (AssertionError, IndexError, KeyError):
            rejects += 1
    assert rejects == 3
    print(json.dumps({"status": "PASS", "certificate_lines": lines,
                      "gates": gates, "source_facets_and_inputs": 53,
                      "negative_rejections": rejects,
                      "scope": "independent typed packet replay; not historical R_mix341"}, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2026-11-08_1849_LSPV5_ONEHOT_MOD3_RESOLUTION_PACKET449_RAW.json")
