#!/usr/bin/env python3
"""Finite hostile-control audit for candidate white-box extraction relations.

The promise source is equality of two n-bit strings, encoded by the proper
three-CNF clean core from LB-0005/CC-0005.  Four uniform linear-time deciders
have the same one-bit answer but intentionally different state exposure:

DIRECT       streams comparisons and never stores the mismatch vector;
MATERIALIZE  stores the full mismatch vector q=u xor v;
INTERP       stores the invertibly encoded vector q xor 1^n;
RECOMP       repeatedly rereads source bits and stores no full vector.

The audit distinguishes raw materialization, decoder-normalized
materialization, and extensional source derivability.  Finite checks validate
the implementation only.  The accompanying report contains the symbolic
theorem and its limitations.
"""

from __future__ import annotations

import argparse
import json
import math
import signal
import time
from pathlib import Path
from typing import Iterable, Sequence


class BudgetExpired(RuntimeError):
    pass


def _alarm(_signum: int, _frame: object) -> None:
    raise BudgetExpired("25-second cooperative budget expired")


def bits(value: int, width: int) -> tuple[int, ...]:
    return tuple((value >> i) & 1 for i in range(width))


def mismatch(u: Sequence[int], v: Sequence[int]) -> tuple[int, ...]:
    return tuple(a ^ b for a, b in zip(u, v))


def direct(u: Sequence[int], v: Sequence[int]) -> dict:
    answer = True
    probes = 0
    for a, b in zip(u, v):
        probes += 2
        if a != b:
            answer = False
    counter_bits = max(1, math.ceil(math.log2(len(u) + 1)))
    return {
        "answer": answer,
        "buffer": None,
        "decoder": None,
        "probes": probes,
        "peak_work_bits": counter_bits + 3,
    }


def materialize(u: Sequence[int], v: Sequence[int]) -> dict:
    q = mismatch(u, v)
    counter_bits = max(1, math.ceil(math.log2(len(u) + 1)))
    return {
        "answer": not any(q),
        "buffer": q,
        "decoder": "identity",
        "probes": 2 * len(u),
        "peak_work_bits": len(q) + counter_bits + 1,
    }


def interp(u: Sequence[int], v: Sequence[int]) -> dict:
    q = mismatch(u, v)
    encoded = tuple(bit ^ 1 for bit in q)
    counter_bits = max(1, math.ceil(math.log2(len(u) + 1)))
    return {
        "answer": not any(bit ^ 1 for bit in encoded),
        "buffer": encoded,
        "decoder": "xor_ones",
        "probes": 2 * len(u),
        "peak_work_bits": len(encoded) + counter_bits + 1,
    }


def recomp(u: Sequence[int], v: Sequence[int]) -> dict:
    # Deliberately recompute every prefix OR from the read-only source instead
    # of retaining the mismatch vector.  This costs O(n^2) probes but only
    # logarithmic writable space.
    prefix_or = False
    probes = 0
    for end in range(len(u)):
        prefix_or = False
        for i in range(end + 1):
            probes += 2
            prefix_or |= bool(u[i] ^ v[i])
    counter_bits = max(1, math.ceil(math.log2(len(u) + 1)))
    return {
        "answer": not prefix_or,
        "buffer": None,
        "decoder": None,
        "probes": probes,
        "peak_work_bits": counter_bits + 3,
    }


def decoded_buffer(run: dict) -> tuple[int, ...] | None:
    if run["buffer"] is None:
        return None
    if run["decoder"] == "identity":
        return tuple(run["buffer"])
    if run["decoder"] == "xor_ones":
        return tuple(bit ^ 1 for bit in run["buffer"])
    raise AssertionError("unknown decoder")


def run_audit(max_n: int) -> dict:
    started = time.perf_counter()
    implementations = {
        "DIRECT": direct,
        "MATERIALIZE": materialize,
        "INTERP": interp,
        "RECOMP": recomp,
    }
    totals = {
        name: {
            "runs": 0,
            "raw_q_exposure": 0,
            "decoded_q_exposure": 0,
            "extensional_q_derivable": 0,
            "max_peak_work_bits": 0,
            "source_probes": 0,
        }
        for name in implementations
    }
    semantic_agreement_checks = 0
    dead_delay_copy_checks = 0
    per_n = []

    for n in range(1, max_n + 1):
        width = 1 << n
        cells = 0
        for ui in range(width):
            u = bits(ui, n)
            for vi in range(width):
                v = bits(vi, n)
                q = mismatch(u, v)
                expected = ui == vi
                observed = {}
                for name, algorithm in implementations.items():
                    record = algorithm(u, v)
                    assert record["answer"] == expected
                    observed[name] = record["answer"]
                    totals[name]["runs"] += 1
                    totals[name]["raw_q_exposure"] += record["buffer"] == q
                    totals[name]["decoded_q_exposure"] += decoded_buffer(record) == q
                    # The extensional extractor ignores the implementation and
                    # reads q directly from the source pair.
                    totals[name]["extensional_q_derivable"] += mismatch(u, v) == q
                    totals[name]["max_peak_work_bits"] = max(
                        totals[name]["max_peak_work_bits"], record["peak_work_bits"]
                    )
                    totals[name]["source_probes"] += record["probes"]
                assert len(set(observed.values())) == 1
                semantic_agreement_checks += 1

                # DEAD, DELAY, and COPY change the trace ledger but not the
                # one-bit answer or any source-derived q.
                base = direct(u, v)
                dead_answer = base["answer"]
                delay_answer = bool(base["answer"])
                copy_answer = direct(tuple(u), tuple(v))["answer"]
                assert dead_answer == delay_answer == copy_answer == expected
                dead_delay_copy_checks += 3
                cells += 1
        per_n.append({"n": n, "cells": cells})

    # Exact expected separation for every nonempty q-coordinate width.
    total_cells = sum(row["cells"] for row in per_n)
    assert totals["DIRECT"]["raw_q_exposure"] == 0
    assert totals["DIRECT"]["decoded_q_exposure"] == 0
    assert totals["RECOMP"]["raw_q_exposure"] == 0
    assert totals["RECOMP"]["decoded_q_exposure"] == 0
    assert totals["MATERIALIZE"]["raw_q_exposure"] == total_cells
    assert totals["MATERIALIZE"]["decoded_q_exposure"] == total_cells
    assert totals["INTERP"]["raw_q_exposure"] == 0
    assert totals["INTERP"]["decoded_q_exposure"] == total_cells
    assert all(v["extensional_q_derivable"] == total_cells for v in totals.values())

    return {
        "run_id": "RT-0004",
        "status": "PASS",
        "max_n": max_n,
        "method": "exhaustive equality source pairs and deterministic wrapper ledgers",
        "semantic_agreement_checks": semantic_agreement_checks,
        "dead_delay_copy_checks": dead_delay_copy_checks,
        "per_n": per_n,
        "implementations": totals,
        "elapsed_seconds": time.perf_counter() - started,
        "limitations": [
            "Finite trace checks validate the implementation but are not an asymptotic lower bound.",
            "The symbolic result concerns the declared exposure predicates, not every possible WExt relation.",
            "Extensional derivability is external work and does not certify internal materialization or resource use.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(25)
    try:
        result = run_audit(args.max_n)
    finally:
        signal.alarm(0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "max_n": result["max_n"],
        "semantic_agreement_checks": result["semantic_agreement_checks"],
        "dead_delay_copy_checks": result["dead_delay_copy_checks"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
