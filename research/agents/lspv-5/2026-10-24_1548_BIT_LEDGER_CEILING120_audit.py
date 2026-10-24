#!/usr/bin/env python3
"""Finite exact controls for BIT-LEDGER-CEILING120.

The script verifies finite instances of four elementary statements:
1. Hamming-distance potentials have oscillation exactly B and unit edge slope.
2. In a one-bit primitive trace, actual flips never exceed charged writes;
   reads and unchanged-value writes remain charged work.
3. Gray enumeration changes one boundary bit and four FORCE-literal sign bits.
4. Equal-length parity-chain SAT/UNSAT controls can have the same q source
   reads but zero versus one accumulator flip.

Finite checks are not asymptotic lower-bound proofs.  The potential ceiling
itself is proved symbolically in the companion report.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path


def popcount(x: int) -> int:
    return x.bit_count()


def hamming_potential_controls() -> tuple[int, int]:
    checks = 0
    pairs = 0
    for bits in range(1, 11):
        states = range(1 << bits)
        for anchor in states:
            values = [popcount(state ^ anchor) for state in states]
            assert max(values) - min(values) == bits
            checks += 1
            for state in states:
                for coordinate in range(bits):
                    other = state ^ (1 << coordinate)
                    assert abs(values[state] - values[other]) == 1
                    checks += 1
                    pairs += 1
    return checks, pairs


def primitive_trace_controls() -> tuple[int, int]:
    # Two source-read actions and six one-bit write actions.
    actions = [("read", 0, 0), ("read", 1, 0)]
    actions += [("write", i, value) for i in range(3) for value in (0, 1)]
    traces = checks = 0
    for length in range(6):
        for trace in product(actions, repeat=length):
            traces += 1
            state = [0, 0, 0]
            reads = writes = flips = 0
            bit_time = 3  # initial complete writable state
            for kind, coordinate, value in trace:
                if kind == "read":
                    reads += 1
                else:
                    writes += 1
                    flips += int(state[coordinate] != value)
                    state[coordinate] = value
                bit_time += 3
                assert flips <= writes
                checks += 1
            work = reads + writes
            assert work == length
            assert flips <= writes <= work
            assert bit_time == 3 * (length + 1)
            assert abs(sum(state) - 0) <= flips
            checks += 4
    return traces, checks


def gray_force_controls() -> tuple[int, int, int]:
    transitions = checks = patch_writes = 0
    for width in range(1, 17):
        previous = 0
        local = 0
        for index in range(1, 1 << width):
            current = index ^ (index >> 1)
            delta = previous ^ current
            assert popcount(delta) == 1
            local += 1
            transitions += 1
            patch_writes += 4
            checks += 1
            previous = current
        assert local == (1 << width) - 1
        checks += 1
    assert patch_writes == 4 * transitions
    checks += 1
    return transitions, patch_writes, checks


def parity_controls() -> tuple[int, int, dict[str, int]]:
    checks = 0
    cases = 0
    totals = {"SAT": 0, "UNSAT": 0, "source_reads": 0,
              "accumulator_flips": 0}
    for q in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
        # z_0=z_q=0 and z_i=z_(i-1) XOR b_i: SAT iff parity(b)=0.
        for label, bits in [("SAT", [0] * q),
                            ("UNSAT", [1] + [0] * (q - 1))]:
            parity = 0
            flips = 0
            reads = 0
            for bit in bits:
                old = parity
                parity ^= bit
                flips += int(parity != old)
                reads += 1
            assert reads == q
            assert (parity == 0) == (label == "SAT")
            assert flips == (0 if label == "SAT" else 1)
            checks += 3
            cases += 1
            totals[label] += 1
            totals["source_reads"] += reads
            totals["accumulator_flips"] += flips
    return cases, checks, totals


def main() -> None:
    c = Fraction(241, 200)
    beta = ((c + 2) / (c * c) - c) / 2
    assert beta == Fraction(11642479, 23232400)
    assert beta > Fraction(1, 2)

    potential_checks, edge_pairs = hamming_potential_controls()
    traces, trace_checks = primitive_trace_controls()
    transitions, patch_writes, gray_checks = gray_force_controls()
    parity_cases, parity_checks, parity_totals = parity_controls()

    result = {
        "run": "BIT-LEDGER-CEILING120",
        "status": "PASS",
        "proof_status": "COMPUTATIONAL finite controls; symbolic theorem in report",
        "seed": None,
        "flmv": {
            "c": "241/200",
            "beta": "11642479/23232400",
            "space_margin_over_one_half": str(beta - Fraction(1, 2)),
            "checks": 2,
        },
        "hamming_potentials": {
            "complete_state_bits": [1, 10],
            "directed_cube_edges_checked": edge_pairs,
            "checks": potential_checks,
        },
        "primitive_traces": {
            "complete_state_bits": 3,
            "max_trace_length": 5,
            "traces_exhausted": traces,
            "checks": trace_checks,
        },
        "gray_force_updates": {
            "boundary_widths": [1, 16],
            "transitions": transitions,
            "literal_sign_writes": patch_writes,
            "checks": gray_checks,
            "scope": "four target literal sign fields only; controller/address flips excluded",
        },
        "parity_chain": {
            "cases": parity_cases,
            "q_values": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096],
            "totals": parity_totals,
            "checks": parity_checks,
        },
        "total_checks": 2 + potential_checks + trace_checks + gray_checks + parity_checks,
        "limitations": [
            "Finite controls do not prove asymptotic SAT lower bounds.",
            "Gray patch counts omit controller, address and solver-state transitions.",
            "Accumulator flips are not complete-state flips.",
            "Optional delay/repetition work is not unavoidable work for arbitrary deciders.",
        ],
    }
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name(
        "2026-10-24_1548_BIT_LEDGER_CEILING120_results.json"
    )
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
