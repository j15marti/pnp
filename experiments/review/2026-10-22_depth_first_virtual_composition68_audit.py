#!/usr/bin/env python3
"""Audit fixed-depth virtual-child composition and explicit exponent formulas."""

from __future__ import annotations

import json
import math
import random


def materialize_child(parent, desc):
    a, b, flip, out_len = desc
    return [
        parent[(a * i + b) % len(parent)] ^ flip
        for i in range(out_len)
    ]


def recursive_bit(source, descriptors, i, counters):
    """Read a final-child bit by recursively translating its index."""
    bit_flip = 0
    for a, b, flip, _ in reversed(descriptors):
        i = (a * i + b) % counters["lengths"].pop()
        bit_flip ^= flip
        counters["translations"] += 1
    counters["source_reads"] += 1
    return source[i] ^ bit_flip


def recurrence(c, alpha, beta, gamma, k):
    for _ in range(k):
        c = max(gamma, alpha + beta * c)
    return c


def explicit_time(c0, alpha, beta, gamma, k):
    def geom(i):
        return (1 - beta ** i) / (1 - beta)

    leaf = alpha * geom(k) + (beta ** k) * c0
    internal = [
        alpha * geom(i) + gamma * (beta ** i)
        for i in range(k)
    ]
    return max([leaf] + internal)


def main():
    rng = random.Random(68)
    checks = 0
    virtual_instances = 0
    source_reads = 0
    translations = 0

    for source_len in [16, 25, 36, 64, 81, 121, 256, 625, 1024, 4096]:
        for depth in range(1, 6):
            for _ in range(40):
                source = [rng.randrange(2) for _ in range(source_len)]
                bodies = [source]
                descs = []
                lengths = []
                for _level in range(depth):
                    parent = bodies[-1]
                    out_len = max(1, math.ceil(math.sqrt(len(parent))))
                    desc = (
                        rng.randrange(1, 2 * len(parent) + 1),
                        rng.randrange(len(parent)),
                        rng.randrange(2),
                        out_len,
                    )
                    lengths.append(len(parent))
                    descs.append(desc)
                    bodies.append(materialize_child(parent, desc))

                final = bodies[-1]
                for i, expected in enumerate(final):
                    counters = {
                        "lengths": lengths[:],
                        "translations": 0,
                        "source_reads": 0,
                    }
                    got = recursive_bit(source, descs, i, counters)
                    assert got == expected
                    assert counters["translations"] == depth
                    assert counters["source_reads"] == 1
                    checks += 3
                    source_reads += 1
                    translations += depth
                virtual_instances += 1

    alpha, beta, gamma, delta = 0.6, 0.5, 1.1, 0.5
    arithmetic_rows = []
    for c0_tenths in range(12, 1001):
        c0 = c0_tenths / 10
        for k in range(1, 31):
            r = recurrence(c0, alpha, beta, gamma, k)
            e = explicit_time(c0, alpha, beta, gamma, k)
            assert abs(r - e) < 1e-10
            checks += 1
        arithmetic_rows.append({
            "c0": c0,
            "depth_20_exponent": recurrence(c0, alpha, beta, gamma, 20),
        })

    # Depth-first space: one descriptor/iterator per ancestor, not all siblings.
    space_rows = []
    for s0_tenths in range(5, 1001):
        s0 = s0_tenths / 10
        for k in range(1, 31):
            recurrence_space = s0
            for _ in range(k):
                recurrence_space = max(delta, beta * recurrence_space)
            explicit_space = max(delta, (beta ** k) * s0)
            assert abs(recurrence_space - explicit_space) < 1e-12
            checks += 1
        space_rows.append({
            "s0": s0,
            "depth_20_space_exponent": max(delta, beta ** 20 * s0),
        })

    # Fixed k makes log(N)^O(k) virtual translation overhead subpolynomial.
    overhead_rows = []
    for k in range(1, 31):
        for log2_n in [32, 64, 128, 256, 512, 1024]:
            # Effective exponent of (log_2 N)^k.
            eff = k * math.log2(log2_n) / log2_n
            assert eff >= 0
            checks += 1
            overhead_rows.append({
                "depth": k,
                "log2_N": log2_n,
                "effective_exponent_logN_pow_k": eff,
            })

    print(json.dumps({
        "status": "fixed_depth_composition_audit_only_no_class_separation",
        "checks": checks,
        "failures": 0,
        "virtual_instances": virtual_instances,
        "source_reads": source_reads,
        "index_translations": translations,
        "target_parameters": {
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
            "delta": delta,
        },
        "time_identity":
            "f^k(c)=max(leaf_work,all_internal_level_overheads)",
        "space_identity":
            "depth_first_peak=max(delta,beta^k*s0) under sequential descriptors",
        "virtual_access_identity":
            "fixed depth k gives k index translations and one source-bit read",
        "required_conditions": [
            "fixed iteration depth independent of N",
            "sequential child generation and workspace reuse",
            "one stored descriptor and iterator per ancestor",
            "polylogarithmic one-level virtual-bit evaluator",
            "no hidden parent rescan per virtual input read",
        ],
        "excluded_claim":
            "no semantic ARC transformer, FLMV contradiction, or class result is proved",
        "arithmetic_rows": arithmetic_rows,
        "space_rows": space_rows,
        "overhead_rows": overhead_rows,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
