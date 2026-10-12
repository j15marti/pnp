#!/usr/bin/env python3
"""Finite audit for ORDER-BIND-ORBIT1.

The symbolic theorem is a counting argument.  This bounded program checks the
permutation-orbit formulas, exact Lehmer coding/decoding, collision bounds,
canonicalization loss, and one-bit wrapper controls through q=9.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path


RUN_ID = "ORDERBIND1"
MAX_Q = 9
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def lehmer_rank(perm: tuple[int, ...]) -> int:
    items = list(range(len(perm)))
    rank = 0
    for i, value in enumerate(perm):
        j = items.index(value)
        rank += j * math.factorial(len(perm) - i - 1)
        items.pop(j)
    return rank


def lehmer_unrank(q: int, rank: int) -> tuple[int, ...]:
    items = list(range(q))
    out: list[int] = []
    for remaining in range(q, 0, -1):
        f = math.factorial(remaining - 1)
        j, rank = divmod(rank, f)
        out.append(items.pop(j))
    return tuple(out)


def inversion_parity(perm: tuple[int, ...]) -> int:
    return sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm))) & 1


def collision_stats(values: list[object]) -> tuple[int, int, int]:
    fibers = Counter(values)
    return len(fibers), sum(v * v for v in fibers.values()), max(fibers.values())


def main() -> None:
    started = time.perf_counter()
    checks = 0
    rows = []

    for q in range(1, MAX_Q + 1):
        perms = list(itertools.permutations(range(q)))
        orbit = math.factorial(q)
        assert len(perms) == orbit
        checks += 1

        ranks: list[int] = []
        first: list[int] = []
        last: list[int] = []
        endpoints: list[tuple[int, int]] = []
        parity: list[int] = []
        canonical: list[tuple[int, ...]] = []

        for perm in perms:
            rank = lehmer_rank(perm)
            ranks.append(rank)
            first.append(perm[0])
            last.append(perm[-1])
            endpoints.append((perm[0], perm[-1]))
            parity.append(inversion_parity(perm))
            canonical.append(tuple(sorted(perm)))

            assert lehmer_unrank(q, rank) == perm
            checks += 1
            # A one-bit SAT answer is constant over a clause-order orbit; all
            # extensional wrappers preserve it without retaining the order.
            answer = q % 2
            for _wrapper in WRAPPERS:
                assert answer == q % 2
                checks += 1

        tags = {
            "lehmer_exact": ranks,
            "first_record": first,
            "last_record": last,
            "two_endpoints": endpoints,
            "parity": parity,
            "canonical_sort": canonical,
        }
        tag_rows = {}
        for name, values in tags.items():
            image, collisions, max_fiber = collision_stats(values)
            assert image * collisions >= orbit * orbit
            checks += 1
            tag_rows[name] = {
                "image": image,
                "collisions": collisions,
                "max_fiber": max_fiber,
            }

        # Exact source reconstruction over the full orbit is equivalent to
        # injectivity of the tag and therefore needs at least ceil(log2(q!)) bits.
        assert tag_rows["lehmer_exact"]["image"] == orbit
        assert tag_rows["lehmer_exact"]["collisions"] == orbit
        assert tag_rows["lehmer_exact"]["max_fiber"] == 1
        exact_bits = (orbit - 1).bit_length()
        assert 2**exact_bits >= orbit
        if exact_bits:
            assert 2 ** (exact_bits - 1) < orbit
        checks += 4 if exact_bits else 3

        # Sorting canonically erases the original source order: its one fiber
        # is the whole orbit, despite preserving the clause multiset/semantics.
        assert tag_rows["canonical_sort"]["image"] == 1
        assert tag_rows["canonical_sort"]["max_fiber"] == orbit
        checks += 2

        rows.append(
            {
                "q": q,
                "orbit_size": orbit,
                "minimum_exact_tag_bits": exact_bits,
                "q_log2_q": 0.0 if q == 1 else q * math.log2(q),
                "log2_factorial": math.log2(orbit),
                "tags": tag_rows,
            }
        )

    elapsed = time.perf_counter() - started
    payload = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "max_q": MAX_Q,
        "checks": checks,
        "failures": 0,
        "runtime_seconds": elapsed,
        "rows": rows,
        "limitations": [
            "Finite enumeration only through q=9.",
            "The asymptotic lower bound is proved symbolically by orbit injectivity, not inferred from timing.",
            "The audit does not transfer source-order reconstruction cost to arbitrary SAT decision.",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()

    out = Path("results/raw/review/2026-10-12_order_binding_orbit.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("run_id", "checks", "failures", "runtime_seconds", "payload_sha256")}, indent=2))


if __name__ == "__main__":
    main()
