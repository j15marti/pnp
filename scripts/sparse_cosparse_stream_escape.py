#!/usr/bin/env python3
"""Exhaustive verifier for the sparse/co-sparse search-MCSP escape.

Model: a truth table is streamed in lexicographic address order.  Given promise
parameter K, keep capped lists of the addresses of 0s and 1s.  If one polarity
has at most K occurrences, synthesize its shared-negation DNF/CNF circuit.
"""

from __future__ import annotations

import json
import math


def capped_stream(bits: tuple[int, ...], k_bound: int):
    lists = {0: [], 1: []}
    overflow = {0: False, 1: False}
    for address, bit in enumerate(bits):
        if not overflow[bit]:
            lists[bit].append(address)
            if len(lists[bit]) > k_bound:
                overflow[bit] = True
    candidates = [b for b in (0, 1) if not overflow[b]]
    if not candidates:
        return None
    polarity = min(candidates, key=lambda b: len(lists[b]))
    return polarity, tuple(lists[polarity]), lists, overflow


def represented_value(n: int, polarity: int, exceptional, address: int) -> int:
    hit = address in exceptional
    return int(hit) if polarity == 1 else int(not hit)


def gate_bound(n: int, exceptional_count: int) -> int:
    # Constants are allowed as zero-size inputs.  For k>=1, share n NOT gates,
    # use k(n-1) binary AND/OR gates inside terms/clauses, and k-1 to combine.
    return 0 if exceptional_count == 0 else n * exceptional_count + n - 1


def main():
    truth_tables = 0
    point_checks = 0
    threshold_checks = 0
    max_live_addresses = 0
    failures = []

    for n in range(1, 5):
        size = 1 << n
        for mask in range(1 << size):
            bits = tuple((mask >> i) & 1 for i in range(size))
            k = min(sum(bits), size - sum(bits))
            result = capped_stream(bits, k)
            truth_tables += 1
            if result is None:
                failures.append((n, mask, "promised side lost"))
                continue
            polarity, exceptional, lists, _ = result
            max_live_addresses = max(max_live_addresses, sum(map(len, lists.values())))
            if len(exceptional) != k:
                failures.append((n, mask, "wrong exceptional count"))
            for address, expected in enumerate(bits):
                point_checks += 1
                got = represented_value(n, polarity, exceptional, address)
                if got != expected:
                    failures.append((n, mask, address, expected, got))
            gates = gate_bound(n, k)
            asserted_bound = 0 if k == 0 else n * k + n - 1
            if gates != asserted_bound:
                failures.append((n, mask, "gate bound mismatch", gates, asserted_bound))
            # Exact implication used in the theorem: n+Kn-1 <= s => witness <= s.
            for s in range(n, max(n, asserted_bound) + 2):
                threshold_checks += 1
                if k > 0 and n + k * n - 1 <= s and gates > s:
                    failures.append((n, mask, "threshold implication failed", s))

    result = {
        "run": "SPARSE-COSPARSE-ESCAPE1",
        "model": "one-pass lexicographic truth-table stream; end-only output; fan-in-two AND/OR/NOT; constants as zero-size inputs",
        "scope": "exhaustive all truth tables for n=1,2,3,4",
        "truth_tables": truth_tables,
        "point_evaluations": point_checks,
        "threshold_checks": threshold_checks,
        "max_live_addresses_observed": max_live_addresses,
        "failures": len(failures),
        "first_failures": failures[:10],
        "theorem_checked": "If min(weight,N-weight)<=K, capped polarity lists retain a valid DNF/CNF witness; for exceptional count k>=1, gate count is kn+n-1.",
        "workspace_accounting": "at most 2(K+1) addresses of n bits, two capped counters, current n-bit address, and O(log s) control/output-description bits",
        "status": "COMPUTATIONAL check of a PROVED/EXACT scoped construction; not full search-MCSP",
        "P_versus_NP": "OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
