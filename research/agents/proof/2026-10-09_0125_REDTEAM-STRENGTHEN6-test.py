#!/usr/bin/env python3
"""Independent byte/model audit of ARC-STRENGTHEN6.

Finite corroboration only.  Uses repaired positive-odd/negative-even DENSE-CNF1.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import signal
import time

ARC6_PATH = "research/agents/proof/2026-10-09_0112_ARC-STRENGTHEN6-test.py"
ARC6_RESULTS = "research/agents/proof/2026-10-09_0112_ARC-STRENGTHEN6-results.json"
spec = importlib.util.spec_from_file_location("arc6", ARC6_PATH)
arc6 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(arc6)


def recognize_guard(clauses, qg):
    """Construction8 exact G grammar, including derived counts and order."""
    clauses = tuple(tuple(c) for c in clauses)
    c = len(clauses)
    if qg < 4 or qg % 2 or c < 7:
        return None
    L = (qg - 2) // 2
    m = c - 4 * L - 2
    q = L - m
    if q < 1 or m < 1 or 5 * m + 4 * q + 2 != c:
        return None
    source = clauses[:m]
    if any(len(d) != 3 or len({abs(x) for x in d}) != 3 for d in source):
        return None
    if any(abs(x) > q for d in source for x in d):
        return None
    if max(abs(x) for d in source for x in d) != q:
        return None
    h, r = q + 1, q + 2
    suffix = [(h, -r), (-h, r)]
    for v in range(1, q + 1):
        suffix.extend(arc6.p0(h, v, q + 2 + v))
    for j in range(1, m + 1):
        a = 2 * q + 2 * j + 1
        suffix.extend(arc6.p0(h, a, a + 1))
    return (source, q) if clauses[m:] == tuple(suffix) else None


def parity_scan(clauses):
    """The load-bearing full-eight-mask and incomplete-mask behavior."""
    masks = {}
    for c in clauses:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return "UNKNOWN"
        order = tuple(sorted(abs(x) for x in c))
        signs = tuple(next(x > 0 for x in c if abs(x) == v) for v in order)
        masks.setdefault(order, set()).add(signs)
    if any(len(v) == 8 for v in masks.values()):
        return "FALSE"
    return "UNKNOWN" if any(len(v) not in (4,) for v in masks.values()) else "STAR"


def sign_balanced(clauses, q):
    signs = {v: set() for v in range(1, q + 1)}
    for c in clauses:
        for x in c:
            signs[abs(x)].add(x > 0)
    return all(s == {False, True} for s in signs.values())


def main():
    signal.alarm(24)
    started = time.monotonic()
    assert [(x, arc6.zz(x), arc6.uleb(arc6.zz(x)).hex())
            for x in (64, -64, 65, -65)] == [
        (64, 127, "7f"), (-64, 128, "8001"),
        (65, 129, "8101"), (-65, 130, "8201")]

    base = [tuple(signs[i] * (i + 1) for i in range(3))
            for signs in itertools.product((-1, 1), repeat=3)]
    rows = []
    pivots = isolated_raw_pairs = 0
    digest = hashlib.sha256()

    for mask in (1, 3, 15, 255):
        source = tuple(base[i] for i in range(8) if mask >> i & 1)
        isolated, qi = arc6.isolate(source, 3)
        transformed, qt, _ = arc6.proper_guard(isolated, qi)
        nested, qn = arc6.guard(transformed, qt)

        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3
                   for c in transformed)
        assert sign_balanced(transformed, qt)
        assert parity_scan(transformed) == "UNKNOWN"
        assert recognize_guard(transformed, qt) is None
        assert recognize_guard(nested, qn) == (transformed, qt)

        nbits = 8 * len(arc6.encode(transformed, qt))
        cap = math.floor(math.sqrt(nbits) * math.log2(nbits + 2))
        checked = 0
        min_child = None
        if mask in (1, 3):
            for pivot in range(1, qt + 1):
                residual, raw = arc6.dp(transformed, pivot)
                largest = max(8 * len(arc6.encode(c))
                              for c in arc6.components(residual))
                assert largest > cap
                min_child = largest if min_child is None else min(min_child, largest)
                isolated_raw_pairs += raw
                pivots += 1
                checked += 1

        blob = arc6.encode(transformed, qt)
        digest.update(blob)
        rows.append({
            "source_mask": mask,
            "source_clauses": len(source),
            "variables": qt,
            "clauses": len(transformed),
            "encoded_bits": nbits,
            "cap_bits": cap,
            "pivots_checked": checked,
            "minimum_largest_child_bits": min_child,
        })

    with open(ARC6_RESULTS, encoding="utf-8") as fh:
        prior = json.load(fh)
    assert prior["clause_isolated_pivots"] == pivots == 152
    # ARC6 recorded raw pairs only for its 2,858 basic pivots, not these 152.
    recorded_raw = prior["raw_resolution_pairs_counted"]
    corrected_total_raw = recorded_raw + isolated_raw_pairs

    result = {
        "status": "PASS_WITH_ACCOUNTING_CORRECTION",
        "rows": rows,
        "isolated_pivot_evaluations": pivots,
        "isolated_raw_resolution_pairs": isolated_raw_pairs,
        "arc6_recorded_basic_raw_pairs": recorded_raw,
        "corrected_total_raw_pairs_for_all_3010_pivots": corrected_total_raw,
        "raw_pair_undercount_in_arc6_summary": isolated_raw_pairs,
        "aggregate_sha256": digest.hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "scope": "Finite byte/grammar audit; universal claims use symbolic proofs.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
