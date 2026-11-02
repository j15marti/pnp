#!/usr/bin/env python3
"""Independent no-import-style verifier for REFEREE298 raw output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def sat_clause(clause: list[int], bits: list[bool]) -> bool:
    return any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)


def chain(n: int, sat_neighbor: bool = False) -> list[list[int]]:
    out = [[1]]
    out += [[-i, i + 1] for i in range(1, n)]
    out += [[n] if sat_neighbor else [-n]]
    return out


def deletion_assignment(n: int, deleted: int) -> list[bool]:
    if deleted == 0:
        return [False] * n
    if deleted == n:
        return [True] * n
    return [i <= deleted for i in range(1, n + 1)]


def verify(raw: dict) -> dict:
    assertions = 0
    assert raw["run"] == "HORN-CHAIN-STREAM-FRONTIER-REFEREE298"; assertions += 1
    assert raw["theorem"]["minimum_DAG_cost"] == "W_Rmix341(F_n)=n"; assertions += 1
    assert raw["theorem"]["minimum_live_record_capacity"] == 3; assertions += 1
    for row in raw["cases"]:
        n = row["n"]
        sources = chain(n)
        assert len(sources) == n + 1 == row["source_clauses_m"]; assertions += 1
        for deleted in range(n + 1):
            bits = deletion_assignment(n, deleted)
            assert not sat_clause(sources[deleted], bits); assertions += 1
            for j, clause in enumerate(sources):
                if j != deleted:
                    assert sat_clause(clause, bits); assertions += 1
        assert all(sat_clause(c, [True] * n) for c in chain(n, True)); assertions += 1
        assert row["W_Rmix341"] == n; assertions += 1
        assert row["proof_stats"]["root_source_count"] == n + 1; assertions += 1
        assert row["proof_stats"]["source_arity_lower_bound"] == n; assertions += 1
        assert row["schedule"]["source_loads"] == n + 1; assertions += 1
        assert row["schedule"]["inference_steps"] == n; assertions += 1
        assert row["Q_min_load_plus_infer"] == 2 * n + 1; assertions += 1
        assert row["peak_live_records_min"] == 3; assertions += 1
        if n == 64:
            proof = row["proof"]
            assert len(proof) == n; assertions += 1
            known = {f"S{i}": tuple(c) for i, c in enumerate(row["sources"])}
            masks = {f"S{i}": 1 << i for i in range(n + 1)}
            for node in proof:
                p, q = node["parents"]
                pivot = node["pivot"]
                a, b = known[p], known[q]
                if pivot not in a:
                    a, b = b, a
                assert pivot in a and -pivot in b; assertions += 1
                expected = tuple(dict.fromkeys([x for x in a if x != pivot] + [x for x in b if x != -pivot]))
                assert tuple(node["clause"]) == expected; assertions += 1
                known[node["id"]] = expected
                masks[node["id"]] = masks[p] | masks[q]
            assert known[proof[-1]["id"]] == (); assertions += 1
            assert masks[proof[-1]["id"]].bit_count() == n + 1; assertions += 1
    assert raw["controls"]["malformed_rejected"] == 8; assertions += 1
    assert raw["controls"]["corrupted_proofs_rejected"] == 3; assertions += 1
    assert raw["classification"]["B2"] == "OPEN for Rmix341"; assertions += 1
    assert raw["classification"]["B3"] == "OPEN for Rmix341"; assertions += 1
    assert raw["classification"]["P_vs_NP"] == "OPEN"; assertions += 1
    return {"passed": True, "independent_assertion_groups": assertions}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(json.loads(args.raw.read_text()))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
