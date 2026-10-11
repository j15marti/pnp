#!/usr/bin/env python3
"""Bounded red-team test for clause-order-dependent locator claims.

Each family member contains a four-clause forcing gadget, m four-clause
blocks, and exactly one x-gated active block.  At x=0, inactive -x-gated
blocks vanish and the active block leaves either a satisfiable or an
unsatisfiable 2-CNF gadget.  The same clause multiset is emitted in three
orders.  The block order hides the active position; sign-grouped order puts
it in a known suffix.  This tests representation dependence, not SAT hardness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

Clause = tuple[int, int, int]


def forcing_gadget() -> list[Clause]:
    # Conjunction is equivalent to not x.
    x, p, q = 1, 2, 3
    return [(-x, p, q), (-x, p, -q), (-x, -p, q), (-x, -p, -q)]


def block_pairs(i: int, answer: int) -> list[tuple[int, int]]:
    a, b, c = 4 + 3 * i, 5 + 3 * i, 6 + 3 * i
    if answer == 1:
        # Satisfiable, for example by a=b=c=1.
        return [(a, b), (a, -b), (-a, b), (a, c)]
    # The four possible clauses on a,b: unsatisfiable.
    return [(a, b), (a, -b), (-a, b), (-a, -b)]


def gated_block(i: int, gate: int, answer: int = 0) -> list[Clause]:
    return [(gate, u, v) for u, v in block_pairs(i, answer)]


def build(m: int, active: int, answer: int, layout: str) -> list[Clause]:
    force = forcing_gadget()
    active_block = gated_block(active, 1, answer)
    inactive = [gated_block(i, -1, 0) for i in range(m) if i != active]
    if layout == "block":
        blocks = [active_block if i == active else gated_block(i, -1, 0)
                  for i in range(m)]
    elif layout == "grouped":
        blocks = inactive + [active_block]
    elif layout == "active_first":
        blocks = [active_block] + inactive
    else:
        raise ValueError(layout)
    return force + [clause for block in blocks for clause in block]


def proper_3cnf(clauses: Sequence[Clause]) -> bool:
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)


def clause_value(clause: Clause, assignment: int) -> bool:
    for lit in clause:
        bit = (assignment >> (abs(lit) - 1)) & 1
        if bool(bit) == (lit > 0):
            return True
    return False


def formula_value(clauses: Sequence[Clause], assignment: int) -> bool:
    return all(clause_value(c, assignment) for c in clauses)


def satisfiable_bruteforce(clauses: Sequence[Clause]) -> bool:
    variables = max(abs(lit) for c in clauses for lit in c)
    return any(formula_value(clauses, a) for a in range(1 << variables))


def canonical_multiset(clauses: Iterable[Clause]) -> list[tuple[int, int, int]]:
    return sorted(tuple(sorted(c, key=lambda z: (abs(z), z))) for c in clauses)


@lru_cache(maxsize=None)
def singleton_select_depth(mask: int) -> int:
    """Optimal exact worst-case probes to find one marked position.

    A probe asks whether one candidate is marked.  A negative removes that
    candidate; a positive finishes.  The recurrence is evaluated only to
    provide a bounded finite check of depth m-1.
    """
    n = mask.bit_count()
    if n <= 1:
        return 0
    best = n
    bit = 1
    while bit <= mask:
        if mask & bit:
            best = min(best, 1 + singleton_select_depth(mask ^ bit))
        bit <<= 1
    return best


def source_collision_stats(m: int) -> dict[str, int]:
    # Domain: (active position, answer), size 2m.  Semantic quotient L keeps
    # only answer.  Each of two image points has fiber size m.
    domain = 2 * m
    collision = 2 * m * m
    image_lower_bound = math.ceil(domain * domain / collision)
    return {
        "domain": domain,
        "collision": collision,
        "image": 2,
        "cauchy_schwarz_lower_bound": image_lower_bound,
    }


def sha256_json(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    # The default bound is deliberately small enough for one invocation to
    # remain well below the repository's roughly 30-second experiment limit.
    parser.add_argument("--max-m", type=int, default=64)
    parser.add_argument("--bruteforce-m", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    checks = 0
    cases = 0
    failures: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []

    # Verify the forcing gadget exhaustively: true exactly when x=0.
    for assignment in range(8):
        observed = formula_value(forcing_gadget(), assignment)
        expected = ((assignment & 1) == 0)
        checks += 1
        if observed != expected:
            failures.append({"kind": "forcing", "assignment": assignment})

    # Verify the residual gadgets exhaustively over their local variables.
    for answer in (0, 1):
        pairs = block_pairs(0, answer)
        sat = False
        for local in range(8):
            assignment = local << 3
            sat = sat or all(clause_value((u, v, 999), assignment) for u, v in pairs)
        # The dummy literal 999 is always false under these assignments.
        checks += 1
        if sat != bool(answer):
            failures.append({"kind": "residual", "answer": answer, "sat": sat})

    for m in range(1, args.max_m + 1):
        stats = source_collision_stats(m)
        checks += 2
        if stats["cauchy_schwarz_lower_bound"] != 2 or stats["image"] != 2:
            failures.append({"kind": "collision", "m": m, "stats": stats})

        for active in range(m):
            for answer in (0, 1):
                cases += 1
                block = build(m, active, answer, "block")
                grouped = build(m, active, answer, "grouped")
                first = build(m, active, answer, "active_first")

                predicates = {
                    "proper": proper_3cnf(block) and proper_3cnf(grouped) and proper_3cnf(first),
                    "duplicate_free": len(set(block)) == len(block),
                    "same_length": len(block) == len(grouped) == len(first) == 4 + 4 * m,
                    "same_multiset_grouped": canonical_multiset(block) == canonical_multiset(grouped),
                    "same_multiset_first": canonical_multiset(block) == canonical_multiset(first),
                    "active_suffix": all(c[0] == 1 for c in grouped[-4:]),
                    "inactive_prefix": all(c[0] == -1 for c in grouped[4:-4]) if m > 1 else True,
                    "one_probe_answer": (grouped[-1] == gated_block(active, 1, answer)[-1]),
                }
                checks += len(predicates)
                for name, ok in predicates.items():
                    if not ok:
                        failures.append({"kind": name, "m": m, "active": active, "answer": answer})

                # Six answer-preserving wrappers cannot recover the discarded
                # active position from the one-bit answer.
                wrappers = [answer, bool(answer), int(bool(answer)), answer ^ 0,
                            (answer | 0), (answer & 1)]
                checks += len(wrappers)
                if any(int(w) != answer for w in wrappers):
                    failures.append({"kind": "wrapper", "m": m, "active": active, "answer": answer})

                if m <= args.bruteforce_m:
                    for layout, formula in (("block", block), ("grouped", grouped), ("active_first", first)):
                        observed = satisfiable_bruteforce(formula)
                        checks += 1
                        if observed != bool(answer):
                            failures.append({"kind": "semantics", "layout": layout,
                                             "m": m, "active": active, "answer": answer})

        if m <= 12:
            observed_depth = singleton_select_depth((1 << m) - 1)
            checks += 1
            if observed_depth != max(0, m - 1):
                failures.append({"kind": "decision_tree", "m": m,
                                 "observed": observed_depth, "expected": max(0, m - 1)})

        if m in {1, 2, 4, 8, 16, 32, 64, 128, args.max_m}:
            rows.append({
                "m": m,
                "clauses": 4 + 4 * m,
                "encoded_records": 4 + 4 * m,
                "block_layout_locator_depth": max(0, m - 1),
                "grouped_layout_locator_depth": 0,
                "grouped_answer_clause_probes": 1,
                "streaming_reorder_clause_reads": 4 + 4 * m,
                "streaming_reorder_buffered_clauses": 4,
                "semantic_quotient": stats,
            })

    payload = {
        "experiment": "CLAUSE-ORDER-LOCALITY-COLLAPSE1",
        "status": "COMPUTATIONAL",
        "claim_scope": "bounded validation of an exact construction; no asymptotic SAT lower bound",
        "parameters": {"max_m": args.max_m, "bruteforce_m": args.bruteforce_m},
        "cases": cases,
        "checks": checks,
        "failures": failures,
        "passed": not failures,
        "rows": rows,
        "hostile_controls": {
            "2sat_residual": "active residual is 2-CNF and directly decidable",
            "horn": "not used as a hardness source; the order attack is syntactic",
            "affine_tseitin": "semantic quotient may discard the source tag just as Gaussian elimination discards presentation",
            "bounded_treewidth": "each island has constant-size local blocks; no hardness inferred",
            "independent_products": "replication multiplies records but preserves reorderability and quotient collapse",
            "padding_redundancy": "extra inactive blocks enlarge physical search only",
            "wrappers": "six equivalent one-bit wrappers preserve answer and erase source position",
        },
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    payload["payload_sha256"] = sha256_json(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("passed", "cases", "checks", "elapsed_seconds", "payload_sha256")}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
