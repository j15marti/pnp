#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE297 raw JSON."""

from __future__ import annotations

import json
import math
import sys
from decimal import Decimal, getcontext


getcontext().prec = 100


def expected(n: int, q: Decimal) -> Decimal:
    if q == 1:
        return Decimal(1)
    r = (1 - q) / q
    total, rd, choose = Decimal(1), Decimal(1), 1
    for d in range(1, n + 1):
        rd *= r
        choose = choose * (n - d + 1) // d
        total += Decimal(choose) * rd / (1 + rd)
    return total


def sci(x: Decimal, digits: int = 12) -> str:
    return f"{x:.{digits}E}" if x else "0"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verifier RAW.json")
    with open(sys.argv[1], "r", encoding="utf-8") as fh:
        data = json.load(fh)

    checks = 0
    ctl = data["logical_controls"]
    assert ctl["unique_sat_models"] == 1; checks += 1
    assert ctl["unsat_sibling_models"] == 0; checks += 1
    assert ctl["unsat_resolution_derived_nodes"] == 1; checks += 1
    assert ctl["malformed_rejected"] == 6; checks += 1

    assert len(data["rows"]) == 60; checks += 1
    for row in data["rows"]:
        q = Decimal(row["effective_q"])
        n = int(row["n"])
        val = expected(n, q)
        low = (q ** (-n) + 1) / 2
        high = q ** (-n)
        assert sci(val) == row["exact_expected_unique_checks"]; checks += 1
        assert sci(low) == row["lower_bound"]; checks += 1
        assert sci(high) == row["upper_bound_iid"]; checks += 1
        assert low <= val <= high; checks += 1

    assert len(data["thresholds"]) == 10; checks += 1
    for row in data["thresholds"]:
        q = Decimal(row["effective_q"])
        n = int(row["first_n_expected_rank_over_1e6"])
        assert expected(n, q) > Decimal(1_000_000); checks += 1
        assert n == 1 or expected(n - 1, q) <= Decimal(1_000_000); checks += 1

    assert data["status"]["expected_rank_theorem"] == "PROVED/EXACT"; checks += 1
    assert data["status"]["B3"] == "OPEN"; checks += 1
    assert data["status"]["P_vs_NP"] == "OPEN"; checks += 1
    print(json.dumps({"verified": True, "independent_assertion_groups": checks}, indent=2))


if __name__ == "__main__":
    main()

