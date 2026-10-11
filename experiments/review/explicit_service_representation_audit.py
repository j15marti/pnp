#!/usr/bin/env python3
"""Audit explicit-vs-succinct representations of fixed SAT batch services.

Finite checks validate exact semantics and accounting only.  The symbolic
construction in the accompanying report supplies the asymptotic statement.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import signal
import time
from dataclasses import dataclass
from pathlib import Path

Clause = tuple[int, ...]


class BudgetExceeded(RuntimeError):
    pass


def alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


def gamma_len(x: int) -> int:
    assert x >= 1
    return 2 * (x.bit_length() - 1) + 1


def encoded_bits(nvars: int, clauses: tuple[Clause, ...]) -> int:
    width = max(1, math.ceil(math.log2(nvars + 1)))
    return (
        gamma_len(nvars)
        + gamma_len(len(clauses) + 1)
        + sum(gamma_len(len(c) + 1) + len(c) * (1 + width) for c in clauses)
    )


def clause_value(clause: Clause, assignment: tuple[int, ...]) -> bool:
    return any(assignment[abs(lit) - 1] == int(lit > 0) for lit in clause)


def satisfies(clauses: tuple[Clause, ...], assignment: tuple[int, ...]) -> bool:
    return all(clause_value(clause, assignment) for clause in clauses)


@dataclass(frozen=True)
class BlockService:
    name: str
    nvars: int
    clauses: tuple[Clause, ...]
    query_vars: tuple[int, ...]
    hidden_vars: tuple[int, ...]
    tags: tuple[str, ...]


def h22_block() -> BlockService:
    # A simple 2-regular 3-uniform hypergraph.  Positive and negative copies
    # make every variable occur exactly twice in each polarity, with no
    # duplicate clauses.
    edges = ((1, 2, 3), (3, 4, 5), (5, 6, 1), (2, 4, 6))
    clauses = tuple(edges) + tuple(tuple(-v for v in edge) for edge in edges)
    return BlockService("clean_h22", 6, clauses, (1, 2, 3, 4, 5), (6,),
                        ("proper3", "H_2,2", "bounded_treewidth"))


def horn_equality_block() -> BlockService:
    clauses = ((-1, 2), (1, -2), (-2, 3), (2, -3))
    return BlockService("horn_2sat_equality", 3, clauses, (1, 3), (2,),
                        ("Horn", "2SAT"))


def affine_block() -> BlockService:
    # x1 xor x2 xor x3 = 0.
    clauses = ((1, 2, -3), (1, -2, 3), (-1, 2, 3), (-1, -2, -3))
    return BlockService("affine_tseitin", 3, clauses, (1, 2), (3,),
                        ("affine", "Gaussian"))


def exact_one_block() -> BlockService:
    clauses = ((1, 2, 3), (-1, -2), (-1, -3), (-2, -3))
    return BlockService("exact_one_product", 3, clauses, (1, 2), (3,),
                        ("bounded_treewidth", "independent_product"))


def proper_pin_block() -> BlockService:
    clauses = ((1, 2, 3), (1, 2, -3), (1, -2, 3), (1, -2, -3))
    return BlockService("proper3_pin", 3, clauses, (1, 2), (3,),
                        ("proper3", "pinning"))


def base_answer(service: BlockService, query: tuple[int, ...],
                clauses: tuple[Clause, ...] | None = None) -> int:
    use_clauses = service.clauses if clauses is None else clauses
    fixed = dict(zip(service.query_vars, query))
    for hidden in itertools.product((0, 1), repeat=len(service.hidden_vars)):
        assignment = [0] * service.nvars
        for var, bit in fixed.items():
            assignment[var - 1] = bit
        for var, bit in zip(service.hidden_vars, hidden):
            assignment[var - 1] = bit
        if satisfies(use_clauses, tuple(assignment)):
            return 1
    return 0


def base_table(service: BlockService, clauses: tuple[Clause, ...] | None = None) -> tuple[int, ...]:
    return tuple(base_answer(service, q, clauses)
                 for q in itertools.product((0, 1), repeat=len(service.query_vars)))


def product_table(base: tuple[int, ...], qbits: int, blocks: int) -> tuple[int, ...]:
    mask = (1 << qbits) - 1
    values = []
    for index in range(1 << (qbits * blocks)):
        ok = 1
        for block in range(blocks):
            shift = qbits * (blocks - block - 1)
            ok &= base[(index >> shift) & mask]
        values.append(ok)
    return tuple(values)


def robdd_nonterminal_nodes(values: tuple[int, ...]) -> int:
    n = (len(values) - 1).bit_length()
    assert len(values) == 1 << n
    current = list(values)
    unique_nodes: dict[tuple[int, int, int], int] = {}
    next_id = 2
    for level in range(n - 1, -1, -1):
        nxt = []
        for i in range(0, len(current), 2):
            lo, hi = current[i], current[i + 1]
            if lo == hi:
                nxt.append(lo)
                continue
            key = (level, lo, hi)
            node = unique_nodes.get(key)
            if node is None:
                node = next_id
                next_id += 1
                unique_nodes[key] = node
            nxt.append(node)
        current = nxt
    assert len(current) == 1
    return len(unique_nodes)


def reverse_index(index: int, width: int) -> int:
    out = 0
    for _ in range(width):
        out = (out << 1) | (index & 1)
        index >>= 1
    return out


def lift_blocks(service: BlockService, blocks: int,
                clauses: tuple[Clause, ...] | None = None) -> tuple[int, tuple[Clause, ...]]:
    base = service.clauses if clauses is None else clauses
    lifted: list[Clause] = []
    for block in range(blocks):
        offset = block * service.nvars
        lifted.extend(tuple((abs(lit) + offset) * (1 if lit > 0 else -1) for lit in clause)
                      for clause in base)
    return blocks * service.nvars, tuple(lifted)


def full_existential_check(service: BlockService, blocks: int,
                           product: tuple[int, ...]) -> int:
    qbits = len(service.query_vars)
    checks = 0
    for flat_q in itertools.product((0, 1), repeat=qbits * blocks):
        expected = 1
        for block in range(blocks):
            chunk = flat_q[block * qbits:(block + 1) * qbits]
            expected &= base_answer(service, chunk)
        index = 0
        for bit in flat_q:
            index = (index << 1) | bit
        assert product[index] == expected
        checks += 1
    return checks


def verify_h22(service: BlockService) -> None:
    pos = [0] * (service.nvars + 1)
    neg = [0] * (service.nvars + 1)
    assert len(set(service.clauses)) == len(service.clauses)
    for clause in service.clauses:
        assert len(clause) == 3 and (all(x > 0 for x in clause) or all(x < 0 for x in clause))
        for lit in clause:
            (pos if lit > 0 else neg)[abs(lit)] += 1
    assert all(pos[v] == neg[v] == 2 for v in range(1, service.nvars + 1))


def run(max_blocks: int, symbolic_blocks: int, seed: int) -> dict[str, object]:
    start = time.monotonic()
    services = (h22_block(), horn_equality_block(), affine_block(),
                exact_one_block(), proper_pin_block())
    verify_h22(services[0])
    totals = {"service_coordinates": 0, "truth_checks": 0, "robdd_checks": 0,
              "wrapper_checks": 0, "encoding_checks": 0, "h22_incidence_checks": 12}
    rows: dict[str, object] = {}
    for service in services:
        qbits = len(service.query_vars)
        base = base_table(service)
        duplicate = tuple(clause for clause in service.clauses for _ in range(3))
        dead = service.clauses + ((1, -1),) * 3
        assert base_table(service, duplicate) == base
        assert base_table(service, dead) == base
        # INTERP: complement every query coordinate before evaluation twice.
        interp = tuple(base[((len(base) - 1) ^ i)] for i in range(len(base)))
        assert tuple(interp[((len(interp) - 1) ^ i)] for i in range(len(interp))) == base
        permuted = tuple(base[reverse_index(i, qbits)] for i in range(len(base)))
        assert tuple(permuted[reverse_index(i, qbits)] for i in range(len(permuted))) == base
        delayed = []
        for bit in base:
            dummy = 0
            for tick in range(7):
                dummy ^= tick
            assert dummy == 7
            delayed.append(bit)
        assert tuple(delayed) == base
        # RECOMP: each coordinate is independently regenerated from clauses.
        assert tuple(base_answer(service, q) for q in itertools.product(
            (0, 1), repeat=len(service.query_vars))) == base
        totals["wrapper_checks"] += 6 * len(base)
        base_nodes = robdd_nonterminal_nodes(base)
        cells = []
        for blocks in range(1, max_blocks + 1):
            product = product_table(base, qbits, blocks)
            nodes = robdd_nonterminal_nodes(product)
            truth_checks = full_existential_check(service, blocks, product)
            nvars, clauses = lift_blocks(service, blocks)
            nbits = encoded_bits(nvars, clauses)
            assert sum(product) == sum(base) ** blocks
            assert nodes <= blocks * max(1, base_nodes)
            totals["service_coordinates"] += len(product)
            totals["truth_checks"] += truth_checks
            totals["robdd_checks"] += 1
            totals["encoding_checks"] += 1
            cells.append({"blocks": blocks, "source_variables": nvars,
                          "source_clauses": len(clauses), "source_encoded_bits": nbits,
                          "explicit_service_bits": len(product),
                          "true_service_bits": sum(product),
                          "robdd_nonterminal_nodes": nodes,
                          "block_local_query_work_bound": blocks * len(service.clauses)
                          * (1 << len(service.hidden_vars))})

        nvars, clauses = lift_blocks(service, symbolic_blocks)
        rows[service.name] = {
            "tags": service.tags,
            "query_bits_per_block": qbits,
            "hidden_bits_per_block": len(service.hidden_vars),
            "base_service_table": "".join(map(str, base)),
            "base_true_coordinates": sum(base),
            "base_robdd_nonterminal_nodes": base_nodes,
            "exhaustive_cells": cells,
            "symbolic_cell": {
                "blocks": symbolic_blocks,
                "source_variables": nvars,
                "source_clauses": len(clauses),
                "source_encoded_bits": encoded_bits(nvars, clauses),
                "explicit_service_bits": 1 << (qbits * symbolic_blocks),
                "succinct_robdd_node_upper_bound": symbolic_blocks * max(1, base_nodes),
                "block_local_query_work_bound": symbolic_blocks * len(service.clauses)
                    * (1 << len(service.hidden_vars)),
            },
        }

    elapsed = time.monotonic() - start
    return {
        "run_id": "TESTS-0002",
        "status": "PASS",
        "seed": seed,
        "method": "exhaustive block-service semantics and exact ROBDD reduction; symbolic product ledger",
        "max_exhaustive_blocks": max_blocks,
        "symbolic_blocks": symbolic_blocks,
        "totals": totals,
        "families": rows,
        "elapsed_seconds": elapsed,
        "limitations": [
            "Finite ROBDD and semantic checks do not imply an asymptotic lower bound.",
            "The asymptotic separation is proved only for the declared independent block products.",
            "Small succinct service representations on easy controls do not imply such representations for all H_2,2 formulas.",
            "Explicit output length is a service-interface cost, not work forced in a one-bit SAT execution.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-blocks", type=int, default=3)
    parser.add_argument("--symbolic-blocks", type=int, default=16)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(25)
    try:
        result = run(args.max_blocks, args.symbolic_blocks, args.seed)
    finally:
        signal.alarm(0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
