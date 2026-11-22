#!/usr/bin/env python3
"""Audit the first-passage code and its charges; no SAT or TM timing rerun."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

RAW = Path(__file__).resolve().parents[1] / "results/raw/dynamic_construction_dihedral_choice_20261121.json"
EXPECTED = "64a245505508743a41f9c3ee849ba5fa65c10a38e3837541e8cb1ce8ffeb789f"


def codes(m):
    return ["0" * m] + ["0" * i + "1" for i in range(m)]


def check(k, m):
    records = codes(m)
    assert len(set(records)) == m + 1
    assert all(not b.startswith(a) for a in records for b in records if a != b)
    weights = [k] + [1] * m
    mean = Fraction(sum(len(s)*v for s, v in zip(records, weights)), k+m)
    assert mean == Fraction(2*k*m+m*(m+1), 2*(k+m))
    entropy = math.log2(k+m) - k/(k+m)*math.log2(k)
    assert entropy <= float(mean) + 1e-12
    return {"m": m, "code": records, "mean_events": str(mean), "entropy_bits": entropy}


def main():
    data = RAW.read_bytes()
    assert sha256(data).hexdigest() == EXPECTED
    source = json.loads(data)
    diffs = source["star_difference_offsets_zero_based"]
    offsets = list(map(min, diffs))
    assert all(max(left) < min(right) for left, right in zip(diffs, diffs[1:]))
    n_bits = next(x["N"] for x in source["records"] if x["name"] == "star-center")
    k = len(diffs)
    weights = [k] + [1]*k
    probes = [offsets[-1]] + offsets
    mean_transitions = Fraction(sum(w*(x+1) for w, x in zip(weights, probes)), 2*k)
    rows = [check(k, m) for m in range(k+1)]
    checks = 0
    for size in range(1, 49):
        for remaining in range(size + 1):
            check(size, remaining)
            checks += 1
    return dict(source_sha256=EXPECTED, N=n_bits, first_read_offsets=offsets,
                expected_transition_floor=str(mean_transitions),
                expected_span_sum_floor_in_cells=str(n_bits*mean_transitions),
                residuals=rows, exact_parameter_pairs=checks,
                status="COMPUTATIONAL arithmetic and physical-layout check")


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
