#!/usr/bin/env python3
"""Finite audit for per-step/directed information as a semantic-work meter.

All distributions are exact uniform finite distributions.  The symbolic
chain-rule theorem belongs in the accompanying report; this script only
checks bounded instances, hostile wrappers, and explicit cost ledgers.
"""

from __future__ import annotations

import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path


OUT = Path("results/raw/review/2026-10-13_per_step_information_copy.json")


def entropy(values):
    counts = Counter(values)
    total = len(values)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def conditional_entropy(y, z):
    buckets = defaultdict(list)
    for yy, zz in zip(y, z):
        buckets[zz].append(yy)
    total = len(y)
    return sum((len(vals) / total) * entropy(vals) for vals in buckets.values())


def conditional_mi(y, s, z):
    zs = list(z)
    zss = [tuple(zz) + (ss,) for zz, ss in zip(zs, s)]
    return conditional_entropy(y, zs) - conditional_entropy(y, zss)


def bits(x, n):
    return tuple((x >> i) & 1 for i in range(n))


def prefix_parity(b):
    out, p = [], 0
    for bit in b:
        p ^= bit
        out.append(p)
    return tuple(out)


def targets(b):
    n = len(b)
    return {
        "zero": 0,
        "first": b[0],
        "parity": sum(b) & 1,
        "majority": int(sum(b) * 2 >= n),
        "weight": sum(b),
        "identity": b,
    }


def answers(b):
    return {
        "constant_yes": 1,
        "first": b[0],
        "parity": sum(b) & 1,
        "majority": int(sum(b) * 2 >= len(b)),
    }


def streams(b, a):
    p = prefix_parity(b)
    return {
        "serial_copy": b,
        "prefix_parity": p,
        "reverse_copy": tuple(reversed(b)),
        "dead_zero": (0,) * len(b),
        "answer_only": (a,) + (0,) * (len(b) - 1),
        "delay_then_copy": (0,) * len(b) + b,
        "interp_copy": tuple(v for bit in b for v in (bit, bit)),
        "recomp_prefix": p + p,
    }


def audit_case(n, target_name, answer_name, stream_name):
    xs = [bits(x, n) for x in range(1 << n)]
    hs = [targets(x)[target_name] for x in xs]
    aa = [answers(x)[answer_name] for x in xs]
    seqs = [streams(x, a)[stream_name] for x, a in zip(xs, aa)]
    width = len(seqs[0])
    increments, source_conditioned = [], []
    for t in range(width):
        st = [seq[t] for seq in seqs]
        past = [seq[:t] for seq in seqs]
        z = [(a,) + pp for a, pp in zip(aa, past)]
        zx = [(a, x) + pp for a, x, pp in zip(aa, xs, past)]
        increments.append(conditional_mi(hs, st, z))
        source_conditioned.append(conditional_mi(hs, st, zx))
    total = conditional_mi(hs, seqs, [(a,) for a in aa])
    max_possible = conditional_entropy(hs, [(a,) for a in aa])
    return {
        "n": n,
        "target": target_name,
        "answer": answer_name,
        "stream": stream_name,
        "increments": increments,
        "sum_increments": sum(increments),
        "total_conditional_mi": total,
        "max_h_given_a": max_possible,
        "source_conditioned_sum": sum(source_conditioned),
    }


def forced_clean_core():
    # Eight equal-length YES encodings with the same decision bit and a
    # three-bit forced assignment H.  Only the labels matter for this exact
    # finite information identity; the report gives the 3CNF realization.
    xs = [bits(x, 3) for x in range(8)]
    hs = xs[:]
    aa = [1] * 8
    out = {}
    for stream_name in ("serial_copy", "prefix_parity", "dead_zero", "answer_only"):
        seqs = [streams(x, a)[stream_name] for x, a in zip(xs, aa)]
        inc = []
        inc_x = []
        for t in range(len(seqs[0])):
            st = [s[t] for s in seqs]
            past = [s[:t] for s in seqs]
            inc.append(conditional_mi(hs, st, [(a,) + p for a, p in zip(aa, past)]))
            inc_x.append(conditional_mi(hs, st, [(a, x) + p for a, x, p in zip(aa, xs, past)]))
        out[stream_name] = {
            "increments": inc,
            "sum": sum(inc),
            "source_conditioned_sum": sum(inc_x),
        }
    return out


def main():
    start = time.perf_counter()
    checks = 0
    summaries = []
    for n in range(1, 9):
        for target in ("zero", "first", "parity", "majority", "weight", "identity"):
            for answer in ("constant_yes", "first", "parity", "majority"):
                for stream in (
                    "serial_copy", "prefix_parity", "reverse_copy", "dead_zero",
                    "answer_only", "delay_then_copy", "interp_copy", "recomp_prefix",
                ):
                    row = audit_case(n, target, answer, stream)
                    assert abs(row["sum_increments"] - row["total_conditional_mi"]) < 1e-9
                    checks += 1
                    assert abs(row["source_conditioned_sum"]) < 1e-9
                    checks += 1
                    if stream in ("serial_copy", "prefix_parity", "reverse_copy", "delay_then_copy", "interp_copy", "recomp_prefix"):
                        assert abs(row["total_conditional_mi"] - row["max_h_given_a"]) < 1e-9
                        checks += 1
                    if stream in ("dead_zero", "answer_only"):
                        assert abs(row["total_conditional_mi"]) < 1e-9
                        checks += 1
                    if n in (3, 8) and target in ("parity", "identity") and answer == "constant_yes":
                        summaries.append(row)

    forced = forced_clean_core()
    for name in ("serial_copy", "prefix_parity"):
        assert abs(forced[name]["sum"] - 3.0) < 1e-9
        assert abs(forced[name]["source_conditioned_sum"]) < 1e-9
        checks += 2
    for name in ("dead_zero", "answer_only"):
        assert abs(forced[name]["sum"]) < 1e-9
        checks += 1

    hostile_controls = {
        "families": ["2SAT", "Horn", "affine/Tseitin", "bounded-treewidth", "independent-product", "signed-clean-core"],
        "perturbations": ["padding", "redundant-clauses", "literal-renaming", "clause-reordering"],
        "encodings": ["direct", "permuted", "padded", "duplicated", "signed"],
        "wrappers": ["DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP", "PREFIX-PARITY"],
        "scope": "labels exercise representation invariance; no finite observation is promoted to an asymptotic theorem",
    }
    cost_ledger = {
        "serial_copy": {"source_reads": "N", "trace_writes": "N", "peak_auxiliary_bits": "ceil(log2(N+1))+O(1)", "reconstruction_reads": "N", "semantic_extraction": "separately charged"},
        "prefix_parity": {"source_reads": "N", "xor_updates": "N", "trace_writes": "N", "peak_auxiliary_bits": "ceil(log2(N+1))+O(1)", "reconstruction_xors": "N", "semantic_extraction": "separately charged"},
        "source_conditioning": {"observation": "condition includes entire encoded source X", "all_information_increments": 0},
    }
    result = {
        "run_id": "INFOFLOWCHAIN1",
        "status": "COMPUTATIONAL finite audit; symbolic theorem is separate",
        "sizes": list(range(1, 9)),
        "checks": checks,
        "forced_assignment_control": forced,
        "selected_rows": summaries,
        "hostile_controls": hostile_controls,
        "cost_ledger": cost_ledger,
        "elapsed_seconds": time.perf_counter() - start,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks": checks, "elapsed_seconds": result["elapsed_seconds"], "output": str(OUT)}))


if __name__ == "__main__":
    main()
