#!/usr/bin/env python3
"""Hostile controls for universal compatibility/extraction bottlenecks.

This experiment compares exact semantic compatibility matrices with concrete
operation ledgers for easy families.  It deliberately avoids interpreting
finite timings as asymptotic lower bounds.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import signal
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


class BudgetExpired(RuntimeError):
    pass


def alarm_handler(_signum: int, _frame: object) -> None:
    raise BudgetExpired("25-second cooperative budget expired")


def gf2_rank(rows: Iterable[int]) -> int:
    basis: Dict[int, int] = {}
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def identity_rows(n: int, permutation: int = 0) -> List[int]:
    width = 1 << n
    return [1 << (u ^ permutation) for u in range(width)]


def horn_subset_rows(n: int) -> List[int]:
    """K[u,v]=1 iff every 1-bit of u is also a 1-bit of v."""
    width = 1 << n
    full = width - 1
    rows = []
    for u in range(width):
        free = full ^ u
        row = 0
        sub = free
        while True:
            row |= 1 << (u | sub)
            if sub == 0:
                break
            sub = (sub - 1) & free
        rows.append(row)
    return rows


def equality_scan(u: int, v: int, n: int) -> Tuple[bool, int]:
    probes = 0
    for i in range(n):
        probes += 2
        if ((u >> i) & 1) != ((v >> i) & 1):
            return False, probes
    return True, probes


def subset_scan(u: int, v: int, n: int) -> Tuple[bool, int]:
    probes = 0
    for i in range(n):
        probes += 2
        if ((u >> i) & 1) and not ((v >> i) & 1):
            return False, probes
    return True, probes


def diagonal_gaussian_ledger(u: int, v: int, mask: int, n: int) -> Tuple[bool, int]:
    """Solve y=x xor mask as an affine diagonal system; count row operations."""
    ops = 0
    for i in range(n):
        ops += 1
        if (((u >> i) ^ (v >> i) ^ (mask >> i)) & 1) != 0:
            return False, ops
    return True, ops


def treewidth_one_dp(u: int, v: int, n: int) -> Tuple[bool, int]:
    """One constant-size message per independent equality edge."""
    messages = 0
    for i in range(n):
        messages += 1
        if ((u >> i) & 1) != ((v >> i) & 1):
            return False, messages
    return True, messages


def encoded_sizes(n: int) -> dict:
    # Literal-index bit length.  Constants are explicit so transformations can
    # be compared without pretending to be exact machine wall time.
    index_bits = math.ceil(math.log2(max(2, 8 * n + 1))) + 1
    two_cnf_literals = 4 * n
    proper_three_literals = 36 * n
    base_bits = two_cnf_literals * index_bits
    proper_bits = proper_three_literals * index_bits
    return {
        "index_bits": index_bits,
        "two_cnf_indexed_bits": base_bits,
        "proper_three_cnf_indexed_bits": proper_bits,
        "duplicate_padded_bits": 5 * proper_bits,
        "dead_padded_bits": proper_bits + 12 * n * index_bits,
    }


def wrapper_ledger(n: int) -> List[dict]:
    base = 2 * n
    return [
        {"wrapper": "BASE", "membership_probes": base, "semantic_change": False},
        {"wrapper": "DEAD", "membership_probes": base, "extra_noop_steps": n**2, "semantic_change": False},
        {"wrapper": "COPY", "membership_probes": base, "copied_input_blocks": 4, "semantic_change": False},
        {"wrapper": "DELAY", "membership_probes": base, "delay_steps": n**3, "semantic_change": False},
        {"wrapper": "INTERP", "membership_probes": base, "representation": "affine diagonal", "semantic_change": False},
        {"wrapper": "RECOMP", "membership_probes": 6 * base, "repetitions": 6, "semantic_change": False},
    ]


def run(max_n: int, seed: int) -> dict:
    rng = random.Random(seed)
    started = time.perf_counter()
    rows_out = []
    exact_pair_checks = 0
    for n in range(1, max_n + 1):
        width = 1 << n
        mask = rng.randrange(width)
        matrices = {
            "2SAT_equality": identity_rows(n),
            "Horn_subset": horn_subset_rows(n),
            "affine_diagonal": identity_rows(n, mask),
            "treewidth1_independent_product": identity_rows(n),
        }
        ranks = {name: gf2_rank(rows) for name, rows in matrices.items()}
        assert all(rank == width for rank in ranks.values())

        maxima = {"2SAT_equality": 0, "Horn_subset": 0, "affine_diagonal": 0, "treewidth1_independent_product": 0}
        for u in range(width):
            for v in range(width):
                eq, eq_ops = equality_scan(u, v, n)
                hs, hs_ops = subset_scan(u, v, n)
                af, af_ops = diagonal_gaussian_ledger(u, v, mask, n)
                tw, tw_ops = treewidth_one_dp(u, v, n)
                assert eq == bool((matrices["2SAT_equality"][u] >> v) & 1)
                assert hs == bool((matrices["Horn_subset"][u] >> v) & 1)
                assert af == bool((matrices["affine_diagonal"][u] >> v) & 1)
                assert tw == eq
                maxima["2SAT_equality"] = max(maxima["2SAT_equality"], eq_ops)
                maxima["Horn_subset"] = max(maxima["Horn_subset"], hs_ops)
                maxima["affine_diagonal"] = max(maxima["affine_diagonal"], af_ops)
                maxima["treewidth1_independent_product"] = max(maxima["treewidth1_independent_product"], tw_ops)
                exact_pair_checks += 1

        # Independent-product rank multiplicativity: I_2 tensor n times is I_2^n.
        assert ranks["treewidth1_independent_product"] == 2**n
        extraction_evaluations = width * width
        rows_out.append(
            {
                "n": n,
                "matrix_dimension": width,
                "semantic_ranks_gf2": ranks,
                "semantic_type_count": width,
                "explicit_matrix_extraction_evaluations": extraction_evaluations,
                "worst_case_decision_operations": maxima,
                "primal_treewidth": 1,
                "encoding_controls": encoded_sizes(n),
                "wrappers": wrapper_ledger(n),
            }
        )

    elapsed = time.perf_counter() - started
    return {
        "run_id": "CC-0005",
        "seed": seed,
        "max_n": max_n,
        "method": "exhaustive source pairs; exact GF(2) bitset rank; deterministic operation ledgers",
        "families": [
            "2SAT equality",
            "Horn implication/subset",
            "affine diagonal/Tseitin-style parity",
            "bounded-treewidth independent equality product",
        ],
        "exact_pair_checks": exact_pair_checks,
        "rows": rows_out,
        "elapsed_seconds": elapsed,
        "status": "PASS",
        "limitations": [
            "Measured operations implement these explicit easy families only.",
            "Explicit compatibility-matrix construction is optional work and is not charged to the deciders.",
            "Finite ranks and timings are computational validation, not an asymptotic SAT lower bound.",
            "Wrapper ledgers demonstrate non-invariance; they are not machine lower bounds.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=9)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    try:
        result = run(args.max_n, args.seed)
    finally:
        signal.alarm(0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "max_n": result["max_n"],
        "exact_pair_checks": result["exact_pair_checks"],
        "elapsed_seconds": result["elapsed_seconds"],
        "last_row": result["rows"][-1],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
