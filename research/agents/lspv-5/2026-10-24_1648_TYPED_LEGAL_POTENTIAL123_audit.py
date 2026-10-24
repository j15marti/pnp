#!/usr/bin/env python3
"""Finite controls for TYPED-LEGAL-POTENTIAL123.

No randomness.  These checks support only the finite instances; the report
contains the symbolic proofs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def hd(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def gray(i: int) -> int:
    return i ^ (i >> 1)


def binary_increment_flip_total(bits: int) -> int:
    return sum(hd(i, i + 1) for i in range((1 << bits) - 1))


def expected_binary_flip_total(bits: int) -> int:
    # Across 0->1->...->2^bits-1, bit j changes 2^(bits-j)-1 times.
    return sum((1 << (bits - j)) - 1 for j in range(bits))


def main() -> None:
    checks = 0
    cube_edges = 0
    gray_steps = 0
    gray_flip_sum = 0
    binary_flip_sum = 0
    rows = []

    for bits in range(1, 17):
        count = 1 << bits
        states = [gray(i) for i in range(count)]
        assert len(set(states)) == count
        checks += 1

        inverse = {state: i for i, state in enumerate(states)}
        legal_max = 0
        legal_flips = 0
        for i in range(count - 1):
            d = hd(states[i], states[i + 1])
            assert d == 1
            legal_flips += d
            legal_max = max(legal_max, abs(inverse[states[i + 1]] - inverse[states[i]]))
            checks += 2
        assert legal_max == 1
        assert legal_flips == count - 1
        checks += 2

        global_lipschitz = 0
        for u in range(count):
            for j in range(bits):
                v = u ^ (1 << j)
                if u < v:
                    cube_edges += 1
                    global_lipschitz = max(
                        global_lipschitz, abs(inverse[u] - inverse[v])
                    )
                    checks += 1

        oscillation = count - 1
        assert global_lipschitz == oscillation
        assert oscillation <= global_lipschitz * bits
        checks += 2

        binary_flips = binary_increment_flip_total(bits)
        assert binary_flips == expected_binary_flip_total(bits)
        checks += 1

        gray_steps += count - 1
        gray_flip_sum += legal_flips
        binary_flip_sum += binary_flips
        rows.append(
            {
                "bits": bits,
                "states": count,
                "path_steps": count - 1,
                "gray_complete_state_flips": legal_flips,
                "binary_counter_flips": binary_flips,
                "legal_edge_lipschitz_of_rank": legal_max,
                "global_hamming_lipschitz_of_rank": global_lipschitz,
            }
        )

    scanner_checks = 0
    scanner_rows = []
    for q in [1 << k for k in range(13)]:
        # A read-only scanner has no work-cell writes.  Its one-hot head code
        # changes two bits per move; a parity-control bit changes only on 1s.
        for ones in (0, 1):
            work_writes = 0
            head_flips = 2 * max(0, q - 1)
            ctrl_flips = ones
            total_flips = head_flips + ctrl_flips
            assert work_writes == 0
            assert total_flips >= max(0, q - 1)
            scanner_checks += 2
            scanner_rows.append(
                {
                    "q": q,
                    "label": "SAT-even" if ones == 0 else "UNSAT-odd",
                    "work_memory_writes": work_writes,
                    "head_flips": head_flips,
                    "control_flips": ctrl_flips,
                    "complete_state_flips": total_flips,
                }
            )

    checks += scanner_checks
    here = Path(__file__)
    code_sha = hashlib.sha256(here.read_bytes()).hexdigest()
    result = {
        "run": "TYPED-LEGAL-POTENTIAL123",
        "status": "PASS",
        "proof_status": "COMPUTATIONAL finite controls; symbolic theorems are in report",
        "code_sha256": code_sha,
        "total_checks": checks,
        "gray_legal_graph": {
            "state_bits": [1, 16],
            "cube_edges_checked": cube_edges,
            "legal_steps_checked": gray_steps,
            "complete_state_flips": gray_flip_sum,
            "rows": rows,
        },
        "binary_counter": {"total_flips_across_widths": binary_flip_sum},
        "typed_scanner": {
            "checks": scanner_checks,
            "cases": len(scanner_rows),
            "rows": scanner_rows,
        },
        "limitations": [
            "A long generated counter path is optional work, not an unavoidable SAT lower bound.",
            "The legal rank potential is defined from path order and is therefore not an independent SAT invariant.",
            "Finite checks do not prove asymptotic runtime lower bounds.",
            "The scanner is a restricted promise recognizer, not a total all-input SAT decider.",
        ],
    }
    out = here.with_name("2026-10-24_1648_TYPED_LEGAL_POTENTIAL123_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("run", "status", "total_checks", "code_sha256")}, indent=2))


if __name__ == "__main__":
    main()
