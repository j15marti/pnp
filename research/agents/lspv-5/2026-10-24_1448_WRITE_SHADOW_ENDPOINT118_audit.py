#!/usr/bin/env python3
"""Exact finite audit for WRITE-SHADOW-ENDPOINT118.

This checks three finite/symbolic components only:
  1. the exact FLMV rational endpoint at c=241/200;
  2. dense-memory versus sparse-written-address simulation on every trace
     of length at most four over four addresses and one-bit values;
  3. a fixed-template parity-chain SAT/UNSAT control in which every source
     field is label-sensitive although a streaming policy uses zero
     work-memory writes (finite control is not charged as work memory).

It does not prove an asymptotic SAT lower bound.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def sparse_trace_audit() -> tuple[int, int]:
    addresses = range(4)
    actions = [("r", a, None) for a in addresses]
    actions += [("w", a, b) for a in addresses for b in (0, 1)]
    traces = 0
    assertions = 0
    for length in range(5):
        for trace in product(actions, repeat=length):
            traces += 1
            dense = [0] * 4
            sparse: dict[int, int] = {}
            written_addresses: set[int] = set()
            writes = 0
            dense_reads: list[int] = []
            sparse_reads: list[int] = []
            for op, address, value in trace:
                if op == "r":
                    dense_reads.append(dense[address])
                    sparse_reads.append(sparse.get(address, 0))
                    assertions += 1
                else:
                    assert value is not None
                    writes += 1
                    written_addresses.add(address)
                    dense[address] = value
                    if value == 0:
                        sparse.pop(address, None)
                    else:
                        sparse[address] = value
                    assertions += 1
                assert len(sparse) <= len(written_addresses) <= writes
                assertions += 2
            assert dense_reads == sparse_reads
            assert {i: v for i, v in enumerate(dense) if v != 0} == sparse
            assertions += 2
    return traces, assertions


def parity_chain_audit() -> tuple[int, int, dict[str, int]]:
    """Exhaustively checks the parity endpoint for 1 <= q <= 12.

    The formula has z_0=0, z_q=0 and enforces
    z_i = z_(i-1) XOR b_i.  It is SAT iff XOR_i b_i = 0.
    A streaming policy reads each b_i, toggles one finite-control state,
    and performs no work-memory writes.
    """
    vectors = 0
    assertions = 0
    label_counts = {"SAT": 0, "UNSAT": 0}
    for q in range(1, 13):
        for bits in product((0, 1), repeat=q):
            vectors += 1
            parity = 0
            reads = 0
            work_writes = 0
            for bit in bits:
                parity ^= bit
                reads += 1
            sat = parity == 0
            label_counts["SAT" if sat else "UNSAT"] += 1
            assert reads == q
            assert work_writes == 0
            assertions += 2
            for i in range(q):
                flipped = list(bits)
                flipped[i] ^= 1
                assert (sum(flipped) % 2 == 0) != sat
                assertions += 1
    return vectors, assertions, label_counts


def main() -> None:
    c = Fraction(241, 200)
    b = beta(c)
    assert b == Fraction(11642479, 23232400)
    assert c > Fraction(6, 5)
    assert b > Fraction(1, 2)
    endpoint_assertions = 3

    traces, trace_assertions = sparse_trace_audit()
    vectors, parity_assertions, labels = parity_chain_audit()
    result = {
        "run": "WRITE-SHADOW-ENDPOINT118",
        "status": "PASS",
        "proof_status": "COMPUTATIONAL finite controls plus exact rational arithmetic",
        "flmv": {
            "c": "241/200",
            "beta": "11642479/23232400",
            "strict_time_slack_over_6_5": str(c - Fraction(6, 5)),
            "strict_space_slack_over_1_2": str(b - Fraction(1, 2)),
        },
        "sparse_memory": {
            "addresses": 4,
            "trace_max_length": 4,
            "traces_exhausted": traces,
            "assertions": trace_assertions,
        },
        "parity_chain": {
            "q_range": [1, 12],
            "vectors_exhausted": vectors,
            "label_counts": labels,
            "input_reads_per_vector": "q",
            "work_memory_writes_per_vector": 0,
            "assertions": parity_assertions,
        },
        "assertions_total": endpoint_assertions + trace_assertions + parity_assertions,
        "limitations": [
            "Finite traces and parity vectors do not prove an asymptotic lower bound.",
            "The zero-write control uses a fixed promised template and finite control.",
            "The sparse-memory theorem still requires the separately proved log-word RAM simulation.",
        ],
    }
    destination = Path(__file__).with_name(
        "2026-10-24_1448_WRITE_SHADOW_ENDPOINT118_results.json"
    )
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
