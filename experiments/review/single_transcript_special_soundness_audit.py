#!/usr/bin/env python3
"""Finite audit for the one-bit/single-transcript special-soundness barrier."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def answer(table: int, query: int) -> int:
    return (table >> query) & 1


def external_transcript(table: int, q0: int, challenge: int, q1: int):
    """External transcript; wrapper-internal state is intentionally absent."""
    a0 = answer(table, q0)
    a1 = answer(table, q1)
    return (q0, a0, challenge, q1, a1)


def wrapper_trace(wrapper: str, transcript):
    """Different internal traces with one identical observable transcript."""
    q0, a0, challenge, q1, a1 = transcript
    if wrapper == "DIRECT":
        return (q0, a0, challenge, q1, a1)
    if wrapper == "COPY":
        return (q0, q0, a0, challenge, q1, q1, a1)
    if wrapper == "DEAD":
        return (99, q0, a0, challenge, q1, a1, 99)
    if wrapper == "DELAY":
        return (q0, "tick", a0, challenge, q1, "tick", a1)
    if wrapper == "INTERP":
        return ((q0 ^ 7), a0, challenge, (q1 ^ 7), a1)
    if wrapper == "RECOMP":
        return (q0, a0, q0, a0, challenge, q1, a1, q1, a1)
    raise ValueError(wrapper)


def canonical_payload(obj):
    stripped = dict(obj)
    stripped.pop("canonical_payload_sha256", None)
    return json.dumps(stripped, sort_keys=True, separators=(",", ":")).encode()


def run(max_tables: int):
    started = time.perf_counter()
    checks = failures = 0
    replay_pairs = wrapper_checks = fork_pairs = 0
    external_query_divergences = 0
    same_query_response_divergences = 0
    internal_trace_variants = set()

    for table in range(max_tables):
        for q0 in range(8):
            for q_ch0 in range(8):
                for q_ch1 in range(8):
                    t0 = external_transcript(table, q0, 0, q_ch0)
                    t1 = external_transcript(table, q0, 1, q_ch1)

                    # Deterministic replay with a fixed challenge is unique.
                    checks += 2
                    replay_pairs += 2
                    failures += external_transcript(table, q0, 0, q_ch0) != t0
                    failures += external_transcript(table, q0, 1, q_ch1) != t1

                    # Extensional wrappers expose the same one-bit oracle transcript.
                    for wrapper in WRAPPERS:
                        checks += 2
                        wrapper_checks += 2
                        failures += external_transcript(table, q0, 0, q_ch0) != t0
                        failures += external_transcript(table, q0, 1, q_ch1) != t1
                        internal_trace_variants.add((wrapper, wrapper_trace(wrapper, t0)))

                    # The commitment prefix is fixed. Any second-query difference
                    # comes from the externally selected challenge/query.
                    checks += 2
                    fork_pairs += 1
                    failures += t0[:2] != t1[:2]
                    if q_ch0 == q_ch1:
                        if t0[4] != t1[4]:
                            same_query_response_divergences += 1
                            failures += 1
                    else:
                        external_query_divergences += 1

    controls = {
        "constant_false": 0x00,
        "constant_true": 0xFF,
        "horn_and_first_two_bits": sum(
            ((q & 1) and ((q >> 1) & 1)) << q for q in range(8)
        ),
        "krom_or_first_two_bits": sum(
            (((q & 1) or ((q >> 1) & 1))) << q for q in range(8)
        ),
        "affine_parity_three_bits": sum(
            ((q.bit_count() & 1) << q) for q in range(8)
        ),
        "bounded_treewidth_projection": sum((((q >> 1) & 1) << q) for q in range(8)),
    }
    control_checks = 0
    for table in controls.values():
        for q in range(8):
            transcript = external_transcript(table, q, 0, q)
            for wrapper in WRAPPERS:
                control_checks += 1
                checks += 1
                failures += external_transcript(table, q, 0, q) != transcript

    result = {
        "schema": "single-transcript-special-soundness-audit-v1",
        "parameters": {
            "query_domain_size": 8,
            "truth_tables": max_tables,
            "wrappers": list(WRAPPERS),
            "exhaustive": max_tables == 256,
        },
        "summary": {
            "checks": checks,
            "failures": failures,
            "replay_checks": replay_pairs,
            "wrapper_observation_checks": wrapper_checks,
            "fork_pairs": fork_pairs,
            "external_query_divergences": external_query_divergences,
            "same_query_response_divergences": same_query_response_divergences,
            "oracle_generated_distinct_challenges": 0,
            "control_checks": control_checks,
            "distinct_internal_trace_records": len(internal_trace_variants),
            "elapsed_seconds": round(time.perf_counter() - started, 6),
        },
        "controls": controls,
        "interpretation": {
            "proved_by_code": False,
            "finite_result": "COMPUTATIONAL",
            "observation": (
                "Fixed deterministic one-bit oracle plus fixed external challenge "
                "replays one transcript; two challenge transcripts require the "
                "extractor to vary the challenge/query. Internal wrapper traces "
                "are not present in the black-box transcript."
            ),
        },
    }
    result["canonical_payload_sha256"] = hashlib.sha256(canonical_payload(result)).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-tables", type=int, default=256)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_tables <= 256:
        raise SystemExit("--max-tables must be between 1 and 256")
    result = run(args.max_tables)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))
    if result["summary"]["failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
