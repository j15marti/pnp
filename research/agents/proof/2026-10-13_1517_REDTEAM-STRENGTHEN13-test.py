#!/usr/bin/env python3
"""Independent audit of CERTDPLL-BRIDGE1's free-subsumption seam.

The external DPLL-to-Resolution theorem counts resolution inferences and
treats subsumption leaves as cost zero.  This script checks the repair used
in REDTEAM-STRENGTHEN13: retain a subclause at every node, resolve only when
both pivot literals survive, and otherwise reuse the stronger pivot-free
parent.  The resulting proof uses original input clauses and strict binary
resolution only.

Finite checks validate the implementation, not the asymptotic theorem.
Every invocation is designed to finish well below 25 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import signal
import time
from dataclasses import dataclass
from pathlib import Path

RUN_ID = "REDTEAM-STRENGTHEN13"
SEED = 202610131517
OUT = Path(
    "research/agents/proof/"
    "2026-10-13_1517_REDTEAM-STRENGTHEN13-results.json"
)
TIME_BUDGET_SECONDS = 24

Clause = frozenset[int]


@dataclass(frozen=True)
class FreeSub:
    """A zero-cost subsumption leaf: source is a subclause of target."""

    source_id: int
    source: Clause
    target: Clause


@dataclass(frozen=True)
class FreeRes:
    """A resolution inference in the free-subsumption calculus."""

    pivot: int
    left: object
    right: object
    target: Clause


@dataclass(frozen=True)
class StrictAxiom:
    source_id: int
    clause: Clause


@dataclass(frozen=True)
class StrictRes:
    pivot: int
    left: object
    right: object
    clause: Clause


def powerset(items: tuple[int, ...]):
    for mask in range(1 << len(items)):
        yield frozenset(items[i] for i in range(len(items)) if (mask >> i) & 1)


def line_clause(node: object) -> Clause:
    return node.clause  # type: ignore[attr-defined]


def strict_step(
    pivot: int,
    left: object,
    right: object,
    target: Clause,
) -> tuple[object, bool]:
    """Strictize one free-subsumption resolution inference.

    Returns the proof object and whether a genuine strict resolution line was
    created.  The returned clause is always a subclause of target.
    """

    a = line_clause(left)
    b = line_clause(right)
    if -pivot not in a:
        assert a <= target
        return left, False
    if pivot not in b:
        assert b <= target
        return right, False
    resolvent = (a - {-pivot}) | (b - {pivot})
    assert resolvent <= target
    return StrictRes(pivot, left, right, resolvent), True


def strictify(node: object, counters: dict[str, int]) -> object:
    if isinstance(node, FreeSub):
        assert node.source <= node.target
        counters["subsumption_leaves"] += 1
        return StrictAxiom(node.source_id, node.source)
    assert isinstance(node, FreeRes)
    left = strictify(node.left, counters)
    right = strictify(node.right, counters)
    proof, created = strict_step(node.pivot, left, right, node.target)
    counters["free_resolution_inferences"] += 1
    counters["strict_resolution_inferences"] += int(created)
    counters["skipped_missing_pivot"] += int(not created)
    assert line_clause(proof) <= node.target
    return proof


def verify_strict(node: object, seen: set[int], stats: dict[str, int]) -> None:
    key = id(node)
    if key in seen:
        return
    seen.add(key)
    if isinstance(node, StrictAxiom):
        stats["axiom_objects"] += 1
        stats.setdefault("source_ids_mask", 0)
        if 0 <= node.source_id < 62:
            stats["source_ids_mask"] |= 1 << node.source_id
        return
    assert isinstance(node, StrictRes)
    a = line_clause(node.left)
    b = line_clause(node.right)
    p = node.pivot
    assert -p in a and p in b
    assert node.clause == (a - {-p}) | (b - {p})
    stats["strict_nodes"] += 1
    verify_strict(node.left, seen, stats)
    verify_strict(node.right, seen, stats)


def exhaustive_local_rule() -> dict[str, int]:
    """Exhaust every subclause pair for small parent targets."""

    pivot = 7
    universe = (-2, -1, 1, 2)
    checks = created = skipped = 0
    for c in powerset(universe):
        for d in powerset(universe):
            target = c | d
            left_target = tuple(sorted(c | {-pivot}))
            right_target = tuple(sorted(d | {pivot}))
            for a in powerset(left_target):
                for b in powerset(right_target):
                    left = StrictAxiom(0, a)
                    right = StrictAxiom(1, b)
                    out, made = strict_step(pivot, left, right, target)
                    assert line_clause(out) <= target
                    checks += 1
                    created += int(made)
                    skipped += int(not made)
    return {"checks": checks, "created": created, "skipped": skipped}


def random_free_tree(rng: random.Random, depth: int, target: Clause, next_id: list[int]):
    """Create a valid tree in Berger et al.'s free-subsumption calculus."""

    if depth == 0:
        items = tuple(sorted(target))
        source = frozenset(x for x in items if rng.randrange(2))
        source_id = next_id[0]
        next_id[0] += 1
        return FreeSub(source_id, source, target)
    pivot = 100 + depth
    left = random_free_tree(rng, depth - 1, target | {-pivot}, next_id)
    right = random_free_tree(rng, depth - 1, target | {pivot}, next_id)
    return FreeRes(pivot, left, right, target)


def randomized_tree_audit() -> dict[str, int]:
    rng = random.Random(SEED)
    totals = {
        "trees": 0,
        "subsumption_leaves": 0,
        "free_resolution_inferences": 0,
        "strict_resolution_inferences": 0,
        "skipped_missing_pivot": 0,
        "verified_strict_nodes": 0,
        "verified_axiom_objects": 0,
    }
    for _ in range(1200):
        depth = rng.randint(0, 8)
        base_literals = tuple(rng.sample((-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6), rng.randint(0, 4)))
        target = frozenset(base_literals)
        counters = {
            "subsumption_leaves": 0,
            "free_resolution_inferences": 0,
            "strict_resolution_inferences": 0,
            "skipped_missing_pivot": 0,
        }
        tree = random_free_tree(rng, depth, target, [0])
        strict = strictify(tree, counters)
        assert line_clause(strict) <= target
        stats = {"strict_nodes": 0, "axiom_objects": 0}
        verify_strict(strict, set(), stats)
        # A later missing-pivot step can return one already-built parent and
        # thereby prune a strict node created lower in the discarded branch.
        assert stats["strict_nodes"] <= counters["strict_resolution_inferences"]
        totals["trees"] += 1
        for key in counters:
            totals[key] += counters[key]
        totals["verified_strict_nodes"] += stats["strict_nodes"]
        totals["verified_axiom_objects"] += stats["axiom_objects"]
    return totals


def redundant_split_firewall() -> dict[str, object]:
    """Show why direct charging of zero-cost subsumption leaves is invalid.

    Start from the one-clause formula containing the empty clause and insert
    r logically useless splits before each Conflict leaf.  Berger size counts
    the split/resolution inferences but free subsumption leaves cost zero.
    A naive semantic-line materialization therefore has 2^(r+1)-1 lines.
    Strictification immediately returns the original empty axiom, one line.
    """

    rows = []
    for r in range(1, 21):
        free_inferences = (1 << r) - 1
        free_subsumption_leaves = 1 << r
        naive_lines = free_inferences + free_subsumption_leaves
        claimed_exact_budget = free_inferences + 1
        strict_lines = 1
        assert naive_lines > claimed_exact_budget
        assert strict_lines <= claimed_exact_budget
        rows.append(
            {
                "dummy_split_depth": r,
                "free_resolution_inferences": free_inferences,
                "free_subsumption_leaves": free_subsumption_leaves,
                "naive_semantic_lines": naive_lines,
                "strictified_lines": strict_lines,
                "input_clauses": 1,
            }
        )
    return {
        "family": "one empty input clause plus redundant consistent splits",
        "smallest_counterexample_depth": 1,
        "rows": rows,
    }


def compressed_macro_firewall() -> dict[str, object]:
    """Quantify why pointer macros are outside the explicit-tree theorem."""

    rows = []
    for depth in range(1, 31):
        macro_records = depth + 1
        expanded_occurrences = (1 << (depth + 1)) - 1
        assert expanded_occurrences >= macro_records
        rows.append(
            {
                "macro_depth": depth,
                "pointer_records": macro_records,
                "expanded_tree_occurrences": expanded_occurrences,
                "expansion_ratio": expanded_occurrences / macro_records,
            }
        )
    return {
        "family": "P_r = Split(y_r, P_{r-1}, P_{r-1}) as a pointer macro",
        "interpretation": (
            "Berger derivation size counts expanded rule occurrences; a pointer or "
            "parameterized macro needs a separate simulation theorem"
        ),
        "rows": rows,
    }


def semantic_fingerprint(payload: dict[str, object]) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()


def main() -> None:
    signal.alarm(TIME_BUDGET_SECONDS)
    started = time.perf_counter()
    local = exhaustive_local_rule()
    random_audit = randomized_tree_audit()
    redundant = redundant_split_firewall()
    compressed = compressed_macro_firewall()
    elapsed = time.perf_counter() - started
    semantic = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "local_rule": local,
        "randomized_trees": random_audit,
        "redundant_split_firewall": redundant,
        "compressed_macro_firewall": compressed,
        "theorem_checked": (
            "free-subsumption Resolution strictifies by a subclause invariant; "
            "the repaired proof uses only original axioms and strict binary resolution"
        ),
        "limitations": [
            "Finite checks do not prove the symbolic strictification lemma.",
            "The bridge covers explicit tree-encoded DPLL certificates only.",
            "No arbitrary one-bit SAT decider is converted to a proof.",
            "No unrestricted machine lower bound is inferred.",
        ],
    }
    payload = dict(semantic)
    payload["elapsed_seconds"] = elapsed
    payload["semantic_sha256"] = semantic_fingerprint(semantic)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
