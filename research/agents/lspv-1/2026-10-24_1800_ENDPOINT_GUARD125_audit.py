#!/usr/bin/env python3
"""ARC-ENDPOINT-GUARD125: exact FLMV two-level endpoint vs retired cosine diagnostic.

No SAT algorithms or hard input lower bounds are inferred from this script.
The cosine predicate is deliberately classified as DEPRECATED, never as proof.
"""
from fractions import Fraction as Q
from math import cos, pi
from json import dump
from pathlib import Path


def beta(c: Q) -> Q:
    assert c >= 1
    return ((c + 2) / (c * c) - c) / 2


def flmv2(t: Q, s: Q) -> bool:
    """Exists c>max(1,t) with s<beta(c), assuming nonnegative exponents."""
    assert t >= 1 and s >= 0
    # beta strictly decreasing and continuous on c>0.
    return s < beta(t)


def legacy_cosine(t: Q, s: Q) -> bool:
    """Incorrect as an unrestricted SAT theorem; diagnostic ONLY."""
    return float(t + s) < 2 * cos(pi / 7)


def audit():
    controls = [
        (Q(3, 2), Q(1, 10), "old-only interior", False),
        (Q(7, 4), Q(1, 100), "old-only outside FLMV time range", False),
        (Q(21, 20), Q(4, 5), "FLMV-only", True),
        (Q(6, 5), Q(1, 2), "both", True),
        (Q(3, 2), Q(1, 36), "strict equality NOT excluded", False),
    ]
    rows = []
    for t, s, label, want in controls:
        actual = flmv2(t, s)
        assert actual == want, (label, t, s, actual)
        rows.append({"label": label, "t": str(t), "s": str(s),
                     "beta_t": str(beta(t)), "flmv2": actual,
                     "legacy_cosine": legacy_cosine(t, s)})
    assert rows[0]["legacy_cosine"] and not rows[0]["flmv2"]
    assert rows[1]["legacy_cosine"] and not rows[1]["flmv2"]
    assert not rows[2]["legacy_cosine"] and rows[2]["flmv2"]
    assert rows[3]["legacy_cosine"] and rows[3]["flmv2"]
    assert not rows[4]["flmv2"]
    categories = {"both": 0, "legacy_only": 0, "flmv_only": 0, "neither": 0}
    grid_checks = 0
    for i in range(0, 31):  # t=1,1.025,...,1.75
        t = Q(40 + i, 40)
        for j in range(0, 41):  # s=0,0.025,...,1
            s = Q(j, 40)
            a, b = flmv2(t, s), legacy_cosine(t, s)
            category = "both" if a and b else "flmv_only" if a else "legacy_only" if b else "neither"
            categories[category] += 1
            grid_checks += 1
    assert sum(categories.values()) == 31 * 41 == grid_checks
    assert categories["legacy_only"] > 0 and categories["flmv_only"] > 0
    result = {"claim_id": "ARC-ENDPOINT-GUARD125", "status": "COMPUTATIONAL; FLMV beta monotonicity proved symbolically in report",
              "grid_checks": grid_checks, "control_checks": len(controls),
              "categories": categories, "controls": rows,
              "scope": "two-level FLMV corollary only, not full FLMV hierarchy or P-vs-NP proof"}
    dest = Path(__file__).with_name("2026-10-24_1800_ENDPOINT_GUARD125_results.json")
    with dest.open("w", encoding="utf-8") as f:
        dump(result, f, indent=2, sort_keys=True)
    print(result)


if __name__ == "__main__":
    audit()
