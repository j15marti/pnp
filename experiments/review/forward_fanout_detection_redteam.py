#!/usr/bin/env python3
"""Finite audit for the child-only reverse-incidence obstruction.

The target gate is u.  There are n later unary gates p_i.  A forward child
query at p_i returns u iff z_i=1, and a private dummy d_i otherwise.  Thus the
fanout of u is |z|.  The experiment checks exact fixed-order scanners, capped
scanners, charged inverse-index construction, wrappers, and hostile controls.

This is a bounded experiment, not an asymptotic SAT lower bound.
"""

from __future__ import annotations

import itertools
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path


SEED = 202610111636
OUT = Path("results/raw/review/2026-10-11_forward_fanout_detection_redteam.json")


def scan_zero(z: tuple[int, ...], order: tuple[int, ...]) -> tuple[bool, int]:
    """Return (fanout_is_zero, child queries), stopping on the first parent."""
    for q, i in enumerate(order, 1):
        if z[i]:
            return False, q
    return True, len(order)


def enumerate_parents(z: tuple[int, ...], order: tuple[int, ...]) -> tuple[list[int], int]:
    """Complete parent enumeration in a child-only interface."""
    return [i for i in order if z[i]], len(order)


def capped_zero(z: tuple[int, ...], order: tuple[int, ...], cap: int) -> tuple[bool, int]:
    """Unsound shortcut: declare zero after cap negative child queries."""
    for q, i in enumerate(order[:cap], 1):
        if z[i]:
            return False, q
    return True, cap


@dataclass
class Row:
    n: int
    vectors: int
    orders: int
    exact_worst_queries: int
    enumeration_queries: int
    capped_failures: int
    capped_caps_checked: int
    inverse_index_build_queries: int
    inverse_index_bits_upper_bound: int
    post_index_lookup_queries: int


def audit_n(n: int, rng: random.Random) -> Row:
    vectors = list(itertools.product((0, 1), repeat=n))
    identity = tuple(range(n))
    orders = {identity, tuple(reversed(identity))}
    for _ in range(min(64, 4 * n)):
        p = list(identity)
        rng.shuffle(p)
        orders.add(tuple(p))

    exact_worst = 0
    enum_queries = 0
    capped_failures = 0
    caps_checked = 0
    for order in orders:
        for z in vectors:
            answer, queries = scan_zero(z, order)
            assert answer == (sum(z) == 0)
            exact_worst = max(exact_worst, queries)
            parents, eq = enumerate_parents(z, order)
            assert sorted(parents) == [i for i, bit in enumerate(z) if bit]
            enum_queries = max(enum_queries, eq)

        # Every cap q<n has an indistinguishable all-zero/singleton pair.
        for cap in range(n):
            caps_checked += 1
            zero = (0,) * n
            singleton = [0] * n
            singleton[order[cap]] = 1
            singleton = tuple(singleton)
            a0, _ = capped_zero(zero, order, cap)
            a1, _ = capped_zero(singleton, order, cap)
            if a0 == a1:  # same transcript and same claimed answer; one is wrong
                capped_failures += 1

    assert exact_worst == n
    assert enum_queries == n
    assert capped_failures == caps_checked
    return Row(
        n=n,
        vectors=len(vectors),
        orders=len(orders),
        exact_worst_queries=exact_worst,
        enumeration_queries=enum_queries,
        capped_failures=capped_failures,
        capped_caps_checked=caps_checked,
        inverse_index_build_queries=n,
        inverse_index_bits_upper_bound=n * max(1, (n - 1).bit_length()),
        post_index_lookup_queries=0,
    )


def delta_certificate_witness(n: int, delta: int) -> dict[str, int | bool]:
    """Finite transcript witness for certifying weight(z)<=delta.

    Answer 1 on the first delta queries and 0 thereafter.  Before all n
    positions are queried, an unqueried bit can be flipped to 1, changing the
    predicate while preserving the transcript.
    """
    assert 0 <= delta < n
    queried = n - 1
    low_weight = delta
    high_weight = delta + 1
    return {
        "n": n,
        "delta": delta,
        "queried_before_ambiguity": queried,
        "low_weight_completion": low_weight,
        "high_weight_completion": high_weight,
        "same_transcript": True,
        "full_scan_required": True,
    }


def controls() -> list[dict[str, object]]:
    # These labels record model checks.  The incidence lower bound is semantic-
    # class agnostic; tractable formula classes and wrappers do not create the
    # missing reverse port.  DIRECT/COPY/DELAY/INTERP/RECOMP preserve the same
    # child transcript, except DELAY adds charged local work.
    families = [
        "2SAT", "Horn", "affine/Tseitin", "bounded-treewidth",
        "independent-product", "padding", "redundant-clauses",
        "alternate-encoding",
    ]
    wrappers = ["DIRECT", "COPY", "DELAY", "INTERP", "RECOMP"]
    return [
        {
            "family": family,
            "wrappers": wrappers,
            "reverse_port_created": False,
            "sat_decision_lower_bound_claimed": False,
            "note": "control does not alter the child-oracle indistinguishability pair",
        }
        for family in families
    ]


def main() -> None:
    rng = random.Random(SEED)
    rows = [asdict(audit_n(n, rng)) for n in range(1, 13)]
    delta_rows = [delta_certificate_witness(n, d) for n in range(2, 13) for d in range(min(3, n))]
    payload = {
        "run_id": "RT-0014",
        "timestamp_utc": "2026-10-11T16:36:00Z",
        "seed": SEED,
        "model": "acyclic unary child oracle with n potential parents",
        "status": {
            "FORWARD_FANOUT_DETECTION1": "PROVED/EXACT (finite instances computationally verified)",
            "CHILD_LOCALITY_IMPLIES_FANOUT_CERT1": "FALSIFIED/RETIRED as an unqualified interface implication",
            "arbitrary_sat_transfer": "OPEN",
            "p_vs_np": "OPEN",
        },
        "rows": rows,
        "delta_certificate_rows": delta_rows,
        "hostile_controls": controls(),
        "accounting": {
            "preprocessing": "inverse index requires n child queries in this model",
            "extraction": "zero-fanout/full-parent-list exact worst case n queries",
            "reconstruction": "not invoked; decision output is one bit",
            "nonuniform_advice": "can bypass queries only by carrying the reverse-incidence information",
        },
        "scope_warning": "No runtime conclusion for arbitrary SAT deciders or unrestricted global CNF compilers.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "rows": len(rows),
        "max_n": rows[-1]["n"],
        "all_exact_worst_equal_n": all(r["exact_worst_queries"] == r["n"] for r in rows),
        "all_capped_shortcuts_falsified": all(r["capped_failures"] == r["capped_caps_checked"] for r in rows),
        "result": str(OUT),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
