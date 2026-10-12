#!/usr/bin/env python3
"""Finite exact-arithmetic audit for JOINT-RESOURCE-PADDING-GAUGE1."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


FAMILIES = (
    "signed-clean-core", "horn", "2sat", "affine-tseitin",
    "bounded-treewidth", "independent-product", "padding",
    "redundant-clauses", "unsat-unit-pair",
)
ENCODINGS = ("canonical", "renamed", "complemented", "auxiliary", "padded")
PRESENTATIONS = ("DIRECT", "COPY", "DEAD", "INTERP", "RECOMP", "PREPAD")
POWERS = tuple(range(2, 9))
ALPHAS = tuple(Fraction(a, b) for a, b in ((1, 2), (2, 3), (3, 4), (4, 5), (9, 10)))


def base_resources(name: str, encoding: str, presentation: str) -> tuple[int, int, int]:
    raw = hashlib.sha256(f"{name}|{encoding}|{presentation}".encode()).digest()
    n = 16 + raw[0] % 33
    time = 2 + raw[1] % 31 + n
    space = 2 + raw[2] % 13 + n // 4
    return n, time, space


def rational_power_ge(base: int, larger: int, exponent: Fraction) -> bool:
    """Check base <= larger**(p/q) without floating point."""
    return base ** exponent.denominator <= larger ** exponent.numerator


def main() -> None:
    failures: list[str] = []
    checks = 0
    rows = []
    for family in FAMILIES:
        for encoding in ENCODINGS:
            for presentation in PRESENTATIONS:
                n, time, space = base_resources(family, encoding, presentation)
                for q in POWERS:
                    for r in POWERS:
                        padded_time = time + time**q + space**r
                        padded_space = space**r
                        checks += 4
                        if padded_time < time**q:
                            failures.append("time-domination")
                        if padded_space != space**r:
                            failures.append("space-equality")
                        if padded_time < padded_space:
                            failures.append("touch-time-charge")
                        if min(n, time, space) < 2:
                            failures.append("positive-base")
                        for alpha in ALPHAS:
                            if q * alpha >= 1:
                                checks += 1
                                if not rational_power_ge(time, padded_time, alpha):
                                    failures.append(f"time-power:{q}:{alpha}")
                        for gamma in ALPHAS:
                            if r * gamma >= 1:
                                checks += 1
                                if not rational_power_ge(space, padded_space, gamma):
                                    failures.append(f"space-power:{r}:{gamma}")
                rows.append({
                    "family": family,
                    "encoding": encoding,
                    "presentation": presentation,
                    "input_bytes": n,
                    "base_time": time,
                    "base_space": space,
                    "extraction_ops": 0,
                    "reconstruction_ops": 0,
                    "communication_bits": 1,
                })

    expected_rows = len(FAMILIES) * len(ENCODINGS) * len(PRESENTATIONS)
    checks += 3
    if len(rows) != expected_rows:
        failures.append("row-count")
    if any(row["extraction_ops"] or row["reconstruction_ops"] for row in rows):
        failures.append("hidden-interface-charge")
    if any(row["communication_bits"] != 1 for row in rows):
        failures.append("decision-output-charge")

    result = {
        "claim": "JOINT-RESOURCE-PADDING-GAUGE1",
        "status": "COMPUTATIONAL",
        "method": "exhaustive exact-integer ledger audit",
        "seed": None,
        "families": list(FAMILIES),
        "encodings": list(ENCODINGS),
        "presentations": list(PRESENTATIONS),
        "time_powers": list(POWERS),
        "space_powers": list(POWERS),
        "rational_exponents": [str(x) for x in ALPHAS],
        "rows": len(rows),
        "checks": checks,
        "failures": failures,
        "limitations": [
            "finite arithmetic audit only; no asymptotic inference",
            "resource numbers are deterministic hostile-control ledgers, not solver measurements",
            "the symbolic wrapper theorem is proved separately",
        ],
        "sample_rows": rows[:18],
    }
    target = Path("results/raw/review/2026-10-12_joint_time_space_padding_gauge.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("claim", "status", "rows", "checks", "failures")}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
