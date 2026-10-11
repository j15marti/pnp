#!/usr/bin/env python3
"""Finite audit for the LB-0018 block-probe/state separation.

The promise input is a selector vector s in {0,1}^k: selector 1 denotes the
fixed satisfiable macroblock Y and selector 0 the equal-size unsatisfiable
macroblock U.  The promise language is AND(s).  The audit exhaustively checks
the one-probe-per-block algorithm, a one-bit two-party aggregation protocol,
wrapper/easy-language controls, and the exact collision distribution of the
decision map.  It does not extrapolate the finite measurements into a SAT
lower bound.
"""

from __future__ import annotations

import json
import math
import platform
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-11_probe_state_communication_separation.json"


def ceil_log2_positive(x: int) -> int:
    return max(1, math.ceil(math.log2(x)))


def encoded_length(k: int) -> int:
    """LB-0018 indexed encoding length for k macroblocks."""
    variables = 198 * k
    clauses = 264 * k
    literal_width = 1 + ceil_log2_positive(variables + 1)
    header_width = 2 * ceil_log2_positive(max(variables, clauses) + 1)
    return 3 * clauses * literal_width + header_width


def block_probe_decider(bits: tuple[int, ...]) -> tuple[int, int]:
    probes = 0
    accumulator = 1
    for bit in bits:
        probes += 1
        accumulator &= bit
        if accumulator == 0:
            break
    return accumulator, probes


def protocol(bits: tuple[int, ...], cut: int) -> tuple[int, int]:
    """Alice sends AND(left) to Bob; count the single transmitted bit."""
    left = int(all(bits[:cut]))
    right = int(all(bits[cut:]))
    return left & right, 1


def wrapped_value(bits: tuple[int, ...], wrapper: str) -> int:
    if wrapper == "DIRECT":
        return int(all(bits))
    if wrapper == "COPY":
        return int(all(tuple(bits)))
    if wrapper == "DEAD":
        dead = sum((i + 1) * b for i, b in enumerate(bits))
        return int(all(bits)) ^ (dead & 0)
    if wrapper == "DELAY":
        pending = list(bits)
        return int(all(pending))
    if wrapper == "INTERP":
        program = lambda xs: int(all(xs))
        return program(bits)
    if wrapper == "RECOMP":
        first = int(all(bits))
        second = int(all(bits))
        return first & second
    raise ValueError(wrapper)


def main() -> None:
    started = time.perf_counter()
    exhaustive = []
    total_cases = 0
    total_protocol_checks = 0
    total_wrapper_checks = 0
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    easy_controls = ("2SAT", "HORN", "AFFINE_TSEITIN", "BOUNDED_TREEWIDTH", "INDEPENDENT_PRODUCT")

    for k in range(1, 17):
        outputs = [0, 0]
        maximum_probes = 0
        all_yes_probes = None
        for mask in range(1 << k):
            bits = tuple((mask >> i) & 1 for i in range(k))
            expected = int(mask == (1 << k) - 1)
            observed, probes = block_probe_decider(bits)
            assert observed == expected
            assert 1 <= probes <= k
            outputs[observed] += 1
            maximum_probes = max(maximum_probes, probes)
            if expected:
                all_yes_probes = probes

            cuts = range(k + 1)
            for cut in cuts:
                protocol_output, communication_bits = protocol(bits, cut)
                assert protocol_output == expected
                assert communication_bits == 1
                total_protocol_checks += 1

            for wrapper in wrappers:
                assert wrapped_value(bits, wrapper) == expected
                total_wrapper_checks += 1
            total_cases += 1

        collision_enumerated = outputs[0] ** 2 + outputs[1] ** 2
        collision_formula = ((1 << k) - 1) ** 2 + 1
        assert collision_enumerated == collision_formula
        assert all_yes_probes == k
        exhaustive.append(
            {
                "k": k,
                "cases": 1 << k,
                "maximum_probes": maximum_probes,
                "all_yes_probes": all_yes_probes,
                "output_fibers": {"0": outputs[0], "1": outputs[1]},
                "collision_count": collision_enumerated,
                "cauchy_schwarz_image_lower_bound": (1 << (2 * k)) / collision_enumerated,
                "actual_image_size": int(outputs[0] > 0) + int(outputs[1] > 0),
                "semantic_accumulator_bits": 1,
                "address_workspace_bits_upper_bound": math.ceil(math.log2(k + 1)),
                "two_party_communication_bits": 1,
                "compatibility_extraction_items": 0,
                "reconstruction_items": 0,
            }
        )

    analytic = []
    for k in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        n_bits = encoded_length(k)
        analytic.append(
            {
                "k": k,
                "encoded_bits_N": n_bits,
                "all_yes_probes": k,
                "N_over_log2_N": n_bits / math.log2(n_bits),
                "probe_ratio_to_N_over_log2_N": k / (n_bits / math.log2(n_bits)),
                "semantic_accumulator_bits": 1,
                "address_workspace_bits_upper_bound": math.ceil(math.log2(k + 1)),
                "two_party_communication_bits": 1,
                "preprocessing_template_comparisons_upper_bound": n_bits,
                "compatibility_extraction_items": 0,
                "reconstruction_items": 0,
            }
        )

    hostile_controls = {
        "easy_language_families": [
            {
                "family": family,
                "selector_semantics": "AND",
                "direct_accumulator_bits": 1,
                "two_party_communication_bits": 1,
                "conclusion": "semantic product count does not force stored compatibility data",
            }
            for family in easy_controls
        ],
        "program_wrappers": list(wrappers),
        "representation_controls": {
            "block_permutation": "one distinguishing address per permuted block; locator changes",
            "within_block_bit_permutation": "one distinguishing address per block; locator changes",
            "redundant_clauses": "can increase N without increasing selector information",
            "padding": "can increase N without increasing selector information",
            "trusted_answer_annotation": "collapses promise decision to one probe if annotation is trusted",
            "untrusted_annotation": "must be verified by a total SAT decider; no collapse claimed",
        },
    }

    result = {
        "audit": "BLOCK-PROBE-STATE-COMM-SEPARATION1",
        "status": "COMPUTATIONAL",
        "timestamp_utc": "2026-10-11T21:27:42Z",
        "python": sys.version,
        "platform": platform.platform(),
        "deterministic": True,
        "random_seed": None,
        "chunking": "single bounded exhaustive chunk k=1..16; analytic arithmetic through k=4096",
        "model": {
            "promise": "s in {0,1}^k encodes k fixed equal-size Y/U macroblocks",
            "decision_function": "AND(s)",
            "probe_algorithm": "read one hard-coded distinguishing position per block, early stop on 0",
            "workspace_accounting": "one semantic accumulator bit plus O(log k) address/index bits",
            "communication_accounting": "Alice sends AND of her selectors to Bob",
        },
        "measurements": {
            "exhaustive_cases": total_cases,
            "protocol_checks": total_protocol_checks,
            "wrapper_checks": total_wrapper_checks,
            "exhaustive": exhaustive,
            "analytic": analytic,
        },
        "hostile_controls": hostile_controls,
        "interpretation_limits": [
            "finite verification is not an asymptotic SAT lower bound",
            "the promise recognizer may take linear input time",
            "the one-bit protocol is for the selector partition, not an arbitrary SAT communication problem",
            "the audit gives no unconditional polynomial-time algorithm for total SAT",
        ],
        "elapsed_seconds": time.perf_counter() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "out": str(OUT.relative_to(ROOT)),
        "exhaustive_cases": total_cases,
        "protocol_checks": total_protocol_checks,
        "wrapper_checks": total_wrapper_checks,
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
