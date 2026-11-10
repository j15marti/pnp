#!/usr/bin/env python3
"""Exhaustive control for LSPV-5/470 proper-projection parity witness.

This is an independent finite model of a relational abstraction precision
claim.  It is not an implementation of the historical R_mix341 checker.
"""

from __future__ import annotations

import itertools
import json
import sys


def relation(m: int, parity: int) -> tuple[tuple[int, ...], ...]:
    if not isinstance(m, int) or m < 1:
        raise ValueError("m must be a positive integer")
    if parity not in (0, 1):
        raise ValueError("parity must be 0 or 1")
    return tuple(
        bits
        for bits in itertools.product((0, 1), repeat=m + 1)
        if sum(bits) % 2 == parity
    )


def project(rel: tuple[tuple[int, ...], ...], mask: int) -> frozenset[tuple[int, ...]]:
    d = len(rel[0])
    if mask < 0 or mask >= 1 << d:
        raise ValueError("projection mask outside coordinate universe")
    idx = tuple(i for i in range(d) if mask & (1 << i))
    return frozenset(tuple(row[i] for i in idx) for row in rel)


def safe_first_use_charge(
    rel: tuple[tuple[int, ...], ...], m: int, weight: int
) -> int:
    if not isinstance(weight, int) or weight <= 0:
        raise ValueError("weight must be a positive integer")
    guarded = [row for row in rel if all(row[i] == 1 for i in range(m))]
    if not guarded:
        raise AssertionError("guard unexpectedly unreachable")
    # history bit h is the final coordinate: h=1 means already paid.
    return min(0 if row[-1] else weight for row in guarded)


def run() -> dict[str, object]:
    assertion_groups = 0
    projection_checks = 0
    extension_checks = 0
    rows: list[dict[str, object]] = []
    weight = 7

    for m in range(1, 10):
        d = m + 1
        r0, r1 = relation(m, 0), relation(m, 1)
        assertion_groups += 1
        assert len(r0) == len(r1) == 1 << m

        for mask in range((1 << d) - 1):  # every proper coordinate subset
            p0, p1 = project(r0, mask), project(r1, mask)
            k = mask.bit_count()
            projection_checks += 1
            assert p0 == p1
            assert len(p0) == 1 << k
            assertion_groups += 2

            omitted = d - k
            for partial in p0:
                for rel in (r0, r1):
                    idx = tuple(i for i in range(d) if mask & (1 << i))
                    count = sum(tuple(row[i] for i in idx) == partial for row in rel)
                    assert count == 1 << (omitted - 1)
                    extension_checks += 1

        # The full relation does distinguish parity classes.
        full = (1 << d) - 1
        assert project(r0, full) != project(r1, full)
        assertion_groups += 1

        guarded = []
        charges = []
        histories = []
        for q, rel in enumerate((r0, r1)):
            g = tuple(row for row in rel if all(row[i] == 1 for i in range(m)))
            assert len(g) == 1
            guarded.append(g[0])
            histories.append(g[0][-1])
            charges.append(safe_first_use_charge(rel, m, weight))
            assertion_groups += 2
        assert histories[0] != histories[1]
        assert sorted(charges) == [0, weight]
        assertion_groups += 2

        union = tuple(sorted(set(r0) | set(r1)))
        assert len(union) == 1 << d
        assert safe_first_use_charge(union, m, weight) == 0
        assertion_groups += 2

        rows.append(
            {
                "premises": m,
                "coordinates": d,
                "states_per_parity": len(r0),
                "proper_projection_count": (1 << d) - 1,
                "guarded_history_by_parity": histories,
                "guarded_safe_charge_by_parity": charges,
                "joined_safe_charge": 0,
                "symbolic_relation": "xor(p_1,...,p_m,h)=q",
            }
        )

    malformed_rejections = 0
    malformed = [
        lambda: relation(0, 0),
        lambda: relation(-1, 0),
        lambda: relation(2, 2),
        lambda: safe_first_use_charge(relation(2, 0), 2, 0),
        lambda: project(relation(2, 0), 1 << 3),
    ]
    for thunk in malformed:
        try:
            thunk()
        except ValueError:
            malformed_rejections += 1
    assert malformed_rejections == len(malformed)
    assertion_groups += 1

    # Native-like two-premise control, with coordinates (p1,p2,h).
    even = relation(2, 0)
    odd = relation(2, 1)
    binary_control = {
        "even": ["".join(map(str, row)) for row in even],
        "odd": ["".join(map(str, row)) for row in odd],
        "guarded_even": "110",
        "guarded_odd": "111",
        "all_pairwise_projections_equal_full": all(
            project(even, mask) == project(odd, mask)
            and len(project(even, mask)) == 4
            for mask in (0b011, 0b101, 0b110)
        ),
    }
    assert binary_control["all_pairwise_projections_equal_full"]
    assertion_groups += 1

    return {
        "status": "PASS",
        "scope": "finite relational precision control; not historical R_mix341",
        "m_range": [1, 9],
        "weight": weight,
        "assertion_groups": assertion_groups,
        "proper_projection_checks": projection_checks,
        "partial_extension_checks": extension_checks,
        "malformed_rejections": malformed_rejections,
        "binary_control": binary_control,
        "rows": rows,
        "limitations": [
            "No historical accepted-byte checker executed.",
            "No proof-search, runtime, space, or evidence-size lower bound follows.",
            "The full correlation has a compact one-equation parity representation.",
        ],
    }


if __name__ == "__main__":
    json.dump(run(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
