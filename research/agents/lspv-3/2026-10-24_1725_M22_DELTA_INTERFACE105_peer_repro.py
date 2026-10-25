#!/usr/bin/env python3
"""M22-DELTA-INTERFACE105 finite named-boundary and exchange-axiom reproducer.

Stdlib only. Reads source-level signed support sets, no SAT oracle.
The assertions are finite calculations, not asymptotic complexity claims or
physical FLMV resource measurements.
"""
import itertools
import collections
import json
import sys


def delta(R):
    R = set(R)
    if not R:
        return False
    for x in R:
        for y in R:
            diff = x ^ y
            es = [1 << i for i in range(diff.bit_length()) if diff & (1 << i)]
            for e in es:
                # f=e means one toggle, not two cancellations.
                if (x ^ e) not in R and not any(
                        (x ^ e ^ f) in R for f in es if f != e):
                    return False
    return True


def relation(P, Q, k):
    P, Q = set(P), set(Q)
    assert len(P) == len(Q) == 2 * k // 3
    assert all(len(S) == len(set(S)) == 3 for S in P | Q)
    assert all(sum(v in S for S in P) == 2 and
               sum(v in S for S in Q) == 2 for v in range(k))
    H = P & Q
    X = P - H
    Z = Q - H
    d1 = {v for S in X for v in S}
    d2 = {v for S in Z for v in S}
    assert d1 == d2
    D = sorted(d1)
    assert all(sum(v in S for S in H) <= 1 for v in D)
    assert all(sum(v in S for S in H) == 2 for v in range(k) if v not in D)
    core, full, witnesses = set(), set(), []
    for a in range(1 << k):
        b = sum(((a >> v) & 1) << i for i, v in enumerate(D))
        if all(0 < sum((a >> v) & 1 for v in S) < 3 for S in H):
            core.add(b)
        if all(any((a >> v) & 1 for v in S) for S in P) and all(
                any(not ((a >> v) & 1) for v in S) for S in Q):
            full.add(b)
            witnesses.append(a)
    return len(X), len(D), core, full, witnesses


def supports(words, names):
    return [tuple(sorted(names.index(c) for c in word)) for word in words]


def run():
    T = tuple(itertools.combinations(range(6), 3))
    B = [C for C in itertools.combinations(T, 4)
         if all(sum(v in S for S in C) == 2 for v in range(6))]
    assert len(B) == 75
    ledger = collections.Counter()
    cached = {}
    core_bad = root_bad = 0
    for P in B:
        for Q in B:
            q, d, core, root, witnesses = relation(P, Q, 6)
            assert witnesses
            keys = [(d, tuple(sorted(core))), (d, tuple(sorted(root)))]
            for key in keys:
                if key not in cached:
                    cached[key] = delta(key[1])
            good_core, good_root = [cached[key] for key in keys]
            core_bad += not good_core
            root_bad += not good_root
            ledger[(q, d, good_root)] += 1
    assert core_bad == 0 and root_bad == 5550
    assert sum(ledger.values()) == 5625
    assert ledger[(0, 0, True)] == 75
    assert ledger[(2, 5, False)] == 540
    assert ledger[(2, 6, False)] == 720
    assert ledger[(3, 6, False)] == 1680
    assert ledger[(4, 6, False)] == 2610

    # Minimal connected six-name target. Every signed clause is proper.
    names = "abcuvw"
    P = supports(["abu", "abv", "cuw", "cvw"], names)
    Q = supports(["abu", "abw", "cuv", "cvw"], names)
    q, d, core, root, witnesses = relation(P, Q, 6)
    assert (q, d, len(core), len(root)) == (2, 6, 36, 24)
    assert delta(core) and not delta(root)
    x = (1 << names.index("a")) | (1 << names.index("c"))
    y = (1 << names.index("u")) | (1 << names.index("v"))
    e = (1 << names.index("a"))
    assert x in root and y in root and (x ^ e) not in root
    for f in [1 << names.index(z) for z in "cuv"]:
        assert (x ^ e ^ f) not in root

    # Connected k=9 source. The hidden x3 is the SAME original name.
    names = "123456789"
    P = supports(["123", "345", "124", "567", "689", "789"], names)
    Q = supports(["123", "345", "125", "489", "678", "679"], names)
    q9, d9, core9, root9, witnesses9 = relation(P, Q, 9)
    assert (q9, d9, len(core9), len(root9), len(witnesses9)) == (4, 8, 224, 68, 98)
    assert delta(core9) and not delta(root9)

    # Canonical in-target SAT anchor Y, witness 111000.
    P = supports(["123", "145", "246", "356"], "123456")
    Q = supports(["124", "136", "235", "456"], "123456")
    qY, dY, coreY, rootY, witnessesY = relation(P, Q, 6)
    assert (qY, dY, len(witnessesY)) == (4, 6, 20)
    assert 7 in witnessesY and delta(coreY) and not delta(rootY)

    output = {
        "report": "M22-DELTA-INTERFACE105",
        "run_date": "2026-10-24 America/Los_Angeles",
        "six_name_support_families": 75,
        "six_name_valid_sources": 5625,
        "within_target": 5550,
        "fully_paired_outside_target": 75,
        "paired_core_delta_failures": 0,
        "full_joined_boundary_delta_failures": 5550,
        "strata": [{"q": q, "boundary_size": d, "full_is_delta": z, "count": count}
                   for (q, d, z), count in sorted(ledger.items())],
        "cached_unique_boundary_relations": len(cached),
        "minimal_join": {"q": 2, "core": 36, "joined": 24,
                         "x": x, "y": y, "delta_exchange_fails_at_e": e},
        "connected_nine": {"q": q9, "core": 224, "joined": 68, "models": 98},
        "anchor_Y_models": 20,
        "physical_FLMV_machine_bit_work": "not measured",
        "actual_state_flips": "not measured",
        "peak_simultaneous_writable_bits": "not measured",
        "bit_time": "not measured"}
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", encoding="utf8") as f:
            json.dump(output, f, indent=2, sort_keys=True)
            f.write("\n")
    print(json.dumps(output, sort_keys=True))
    return output


if __name__ == "__main__":
    run()
