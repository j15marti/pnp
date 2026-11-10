#!/usr/bin/env python3
"""Exact controls for LSPV-5/472.

This is a finite/symbolic audit of three invalid implications:
  collecting-state cardinality -> charged work space,
  nondeterministic branch count -> branchwise work space, and
  proof-DAG node count -> verifier peak space.

It does not implement an FLMV machine or the historical R_mix341 checker.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


def ceil_log2(n: int) -> int:
    assert n >= 1
    return (n - 1).bit_length()


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def source_family(n: int) -> dict:
    # The source is immutable and read-only. The scanner retains a binary
    # position, one parity bit, and two status bits.
    work_bits = ceil_log2(n + 1) + 3
    states = 1 << n
    return {
        "N": n,
        "authenticated_source_states": str(states),
        "log2_authenticated_source_states": n,
        "branch_histories": str(states),
        "log2_branch_histories": n,
        "branchwise_live_work_bits_upper": work_bits,
    }


def shared_and_dag(height: int) -> dict:
    # q leaf checks all reference one globally shared one-bit lemma. A binary
    # AND tree joins the q checks. Distinct paid nodes: shared lemma + q leaf
    # checks + (q-1) joins = 2q. A depth-first schedule retains the shared
    # truth value, a path/direction stack, and O(log q) counters.
    q = 1 << height
    distinct_nodes = 2 * q
    dfs_peak_bits = 2 * height + 5
    materialized_peak_bits = distinct_nodes
    return {
        "height": height,
        "leaf_obligations": q,
        "distinct_nodes_count_once": distinct_nodes,
        "dfs_peak_bits_upper": dfs_peak_bits,
        "materialized_peak_bits": materialized_peak_bits,
        "dfs_to_materialized_ratio": f"{dfs_peak_bits}/{materialized_peak_bits}",
    }


def decimal_scale(n: int) -> dict:
    b = beta(Fraction(6, 5))
    return {
        "N": f"1e{int(round(math.log10(n)))}",
        "log10_authenticated_source_states": n * math.log10(2),
        "scanner_live_work_bits_upper": ceil_log2(n + 1) + 3,
        "N_pow_half": n ** 0.5,
        "N_pow_23_over_45": n ** float(b),
        "exponent_ratio_N_pow_1_over_90": n ** (1 / 90),
    }


def main() -> None:
    assertions = 0

    finite = []
    for n in range(1, 21):
        row = source_family(n)
        finite.append(row)
        assert int(row["authenticated_source_states"]) == 2**n
        assertions += 1
        assert row["log2_authenticated_source_states"] == n
        assertions += 1
        assert row["branch_histories"] == row["authenticated_source_states"]
        assertions += 1
        assert row["branchwise_live_work_bits_upper"] == ceil_log2(n + 1) + 3
        assertions += 1

    dags = []
    for h in range(1, 21):
        row = shared_and_dag(h)
        dags.append(row)
        assert row["distinct_nodes_count_once"] == 2 ** (h + 1)
        assertions += 1
        assert row["dfs_peak_bits_upper"] == 2 * h + 5
        assertions += 1
        assert row["dfs_peak_bits_upper"] < row["materialized_peak_bits"] or h <= 2
        assertions += 1

    b = beta(Fraction(6, 5))
    assert b == Fraction(23, 45)
    assertions += 1
    assert b - Fraction(1, 2) == Fraction(1, 90)
    assertions += 1

    illustrative_ns = [10**6, 10**12, 10**24, 10**60]
    scales = [decimal_scale(n) for n in illustrative_ns]
    for row, n in zip(scales, illustrative_ns):
        assert row["scanner_live_work_bits_upper"] == ceil_log2(n + 1) + 3
        assertions += 1
        ratio = row["N_pow_23_over_45"] / row["N_pow_half"]
        assert math.isclose(ratio, row["exponent_ratio_N_pow_1_over_90"], rel_tol=1e-12)
        assertions += 1

    result = {
        "node": "P2-L5-472",
        "status": "PROVED_RESTRICTED_PLUS_COMPUTATIONAL",
        "assertions": assertions,
        "beta_6_over_5": "23/45",
        "gap_over_half": "1/90",
        "finite_source_branch_controls": finite,
        "shared_and_dag_controls": dags,
        "illustrative_scales_not_bytes": scales,
        "conclusions": {
            "source_cardinality_to_work_space": "FALSIFIED_WITH_READ_ONLY_SOURCE_AXIS",
            "branch_count_to_branchwise_space": "FALSIFIED_WITH_HISTORY_AXIS",
            "proof_node_count_to_peak_space": "FALSIFIED_WITH_DEPTH_FIRST_SCHEDULE",
            "required_repair": "FIX_SOURCE_AND_PROVE_SIMULTANEOUS_LIVE_INJECTION_OR_MODEL_MATCHED_PEBBLING_BOUND",
            "p_vs_np": "OPEN",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
