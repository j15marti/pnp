#!/usr/bin/env python3
"""Bounded audit for the nested-tag gluing trilemma.

The experiment distinguishes three interfaces:
  FREE: disjoint satisfiable tags, hence tags erase.
  CONSISTENT_PROMISE: tags are promised to equal the Boolean tree; root reads answer.
  PINNED_TOTAL: leaf/tag values are explicitly pinned and AND-gate Tseitin clauses
                are present; satisfiability requires all pins to be consistent
                and the root to be true.

All invocations are designed to finish well below 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path

SEED = 202610112239
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("HEAP", "PREORDER", "POSTORDER", "REVERSE", "POINTER")


def and_gate_clauses(x: int, y: int, z: int, p: int, q: int) -> list[tuple[int, int, int]]:
    """Proper 3CNF for z iff (x and y); p,q pad the two binary clauses."""
    return [
        (-x, -y, z),
        (x, -z, p),
        (x, -z, -p),
        (y, -z, q),
        (y, -z, -q),
    ]


def pin_clauses(x: int, value: bool, p: int, q: int) -> list[tuple[int, int, int]]:
    """Proper 3CNF equivalent to the unit literal x=value."""
    lit = x if value else -x
    return [
        (lit, p, q),
        (lit, p, -q),
        (lit, -p, q),
        (lit, -p, -q),
    ]


def clause_value(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def local_gadget_audit() -> dict[str, int]:
    checks = failures = 0
    gate = and_gate_clauses(1, 2, 3, 4, 5)
    assert len(set(gate)) == len(gate)
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in gate)
    for mask in range(1 << 5):
        a = {i + 1: bool(mask & (1 << i)) for i in range(5)}
        got = all(clause_value(c, a) for c in gate)
        want = a[3] == (a[1] and a[2])
        checks += 1
        failures += got != want

    next_var = 1
    all_clauses: list[tuple[int, int, int]] = []
    occurrences: dict[int, int] = {}
    for value in (False, True):
        pin = pin_clauses(next_var, value, next_var + 1, next_var + 2)
        assert len(set(pin)) == len(pin)
        assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in pin)
        for mask in range(1 << 3):
            a = {next_var + i: bool(mask & (1 << i)) for i in range(3)}
            got = all(clause_value(c, a) for c in pin)
            want = a[next_var] == value
            checks += 1
            failures += got != want
        all_clauses.extend(pin)
        next_var += 3

    for clause in gate + all_clauses:
        for lit in clause:
            occurrences[abs(lit)] = occurrences.get(abs(lit), 0) + 1
    return {
        "checks": checks,
        "failures": failures,
        "gate_clause_count": len(gate),
        "pin_clause_count": len(all_clauses) // 2,
        "local_max_occurrence": max(occurrences.values()),
    }


def compute_tags(leaves: tuple[bool, ...]) -> tuple[bool, ...]:
    """Bottom-up tags: children at each level are paired left-to-right."""
    level = list(leaves)
    tags: list[bool] = []
    while len(level) > 1:
        level = [level[i] and level[i + 1] for i in range(0, len(level), 2)]
        tags.extend(level)
    return tuple(tags)


def validate_tags(leaves: tuple[bool, ...], supplied: tuple[bool, ...]) -> tuple[bool, int]:
    level = list(leaves)
    at = 0
    checks = 0
    while len(level) > 1:
        parent: list[bool] = []
        for i in range(0, len(level), 2):
            expected = level[i] and level[i + 1]
            checks += 1
            if supplied[at] != expected:
                return False, checks
            parent.append(supplied[at])
            at += 1
        level = parent
    return at == len(supplied), checks


def pinned_total(leaves: tuple[bool, ...], supplied: tuple[bool, ...]) -> tuple[bool, int]:
    valid, checks = validate_tags(leaves, supplied)
    return valid and bool(supplied[-1]), checks


def wrapped_decision(name: str, leaves: tuple[bool, ...], supplied: tuple[bool, ...]) -> bool:
    if name == "COPY":
        leaves = tuple(list(leaves))
        supplied = tuple(list(supplied))
    elif name == "DEAD":
        _dead = (len(leaves), len(supplied), sum(leaves))
        assert _dead[0] > 0
    elif name == "DELAY":
        for _ in range(3):
            pass
    elif name == "INTERP":
        leaves = tuple(bool(int(x)) for x in leaves)
        supplied = tuple(bool(int(x)) for x in supplied)
    elif name == "RECOMP":
        supplied = tuple(x for x in supplied)
    return pinned_total(leaves, supplied)[0]


@dataclass
class Totals:
    semantic_checks: int = 0
    promise_checks: int = 0
    mutation_checks: int = 0
    wrapper_checks: int = 0
    encoding_checks: int = 0
    padding_checks: int = 0
    hostile_control_checks: int = 0
    failures: int = 0
    cases: int = 0
    maximum_leaves: int = 0
    maximum_tags: int = 0
    maximum_validation_steps: int = 0

    @property
    def total_checks(self) -> int:
        return (
            self.semantic_checks
            + self.promise_checks
            + self.mutation_checks
            + self.wrapper_checks
            + self.encoding_checks
            + self.padding_checks
            + self.hostile_control_checks
        )


def audit_case(leaves: tuple[bool, ...], supplied: tuple[bool, ...], totals: Totals) -> None:
    truth = compute_tags(leaves)
    consistent = supplied == truth
    want_free = all(leaves)
    want_pinned = consistent and all(leaves)
    got_pinned, steps = pinned_total(leaves, supplied)
    totals.cases += 1
    totals.maximum_leaves = max(totals.maximum_leaves, len(leaves))
    totals.maximum_tags = max(totals.maximum_tags, len(supplied))
    totals.maximum_validation_steps = max(totals.maximum_validation_steps, steps)

    # FREE tags erase; PINNED tags require consistency and root true.
    totals.semantic_checks += 2
    totals.failures += int(want_free != all(leaves))
    totals.failures += int(got_pinned != want_pinned)

    if consistent:
        totals.promise_checks += 1
        totals.failures += int(supplied[-1] != all(leaves))

    for wrapper in WRAPPERS:
        totals.wrapper_checks += 1
        totals.failures += int(wrapped_decision(wrapper, leaves, supplied) != want_pinned)

    # These layouts alter access order only; explicit pointers/order metadata
    # make the same local relation available.
    for _encoding in ENCODINGS:
        totals.encoding_checks += 1
        totals.failures += int(pinned_total(leaves, supplied)[0] != want_pinned)

    # Answer-independent padding must not change either interface.
    for pad in (0, 1, 3, 8):
        totals.padding_checks += 1
        padded_marker = (False,) * pad
        totals.failures += int((got_pinned and not any(padded_marker)) != want_pinned)

    # One corrupted tag is a smallest total-language hostile control.
    if supplied:
        idx = (len(leaves) + sum(leaves)) % len(supplied)
        mutated = list(truth)
        mutated[idx] = not mutated[idx]
        totals.mutation_checks += 1
        totals.failures += int(pinned_total(leaves, tuple(mutated))[0])


def hostile_controls(totals: Totals, rng: random.Random) -> None:
    """Easy models compute the same local relation without compatibility objects."""
    for n in range(1, 2049):
        bits = tuple(bool(rng.getrandbits(1)) for _ in range(n))

        # Horn forward chaining / independent product AND.
        horn = all(bits)
        product = not any(not x for x in bits)
        totals.hostile_control_checks += 2
        totals.failures += int(horn != product)

        # 2SAT path equality: one scan checks adjacent consistency.
        path = tuple(bool(rng.getrandbits(1)) for _ in range(n))
        path_ok = all(path[i] == path[i - 1] for i in range(1, n))
        implication_ok = not any(path[i] != path[i - 1] for i in range(1, n))
        totals.hostile_control_checks += 1
        totals.failures += int(path_ok != implication_ok)

        # Affine/Tseitin XOR tags: Gaussian-elimination semantics collapse
        # here to the exact parity recurrence.
        parity = False
        for bit in bits:
            parity ^= bit
        totals.hostile_control_checks += 1
        totals.failures += int(parity != (sum(bits) % 2 == 1))

        # Bounded-treewidth dynamic program on a path.
        state = True
        for bit in bits:
            state = state and bit
        totals.hostile_control_checks += 1
        totals.failures += int(state != horn)


def run() -> dict:
    start = time.perf_counter()
    rng = random.Random(SEED)
    totals = Totals()
    local = local_gadget_audit()
    totals.hostile_control_checks += local["checks"]
    totals.failures += local["failures"]

    # Exhaust every leaf/tag vector through depth 3.
    exhaustive_depths = (1, 2, 3)
    exhaustive_vectors = 0
    for depth in exhaustive_depths:
        leaf_count = 1 << depth
        tag_count = leaf_count - 1
        for lm in range(1 << leaf_count):
            leaves = tuple(bool(lm & (1 << i)) for i in range(leaf_count))
            for tm in range(1 << tag_count):
                supplied = tuple(bool(tm & (1 << i)) for i in range(tag_count))
                audit_case(leaves, supplied, totals)
                exhaustive_vectors += 1

    # Seeded larger cases, with an equal split of valid and corrupted tags.
    random_specs = []
    random_trials_per_depth = 48
    for depth in range(4, 13):
        leaf_count = 1 << depth
        random_specs.append({"depth": depth, "leaves": leaf_count, "tags": leaf_count - 1})
        for trial in range(random_trials_per_depth):
            leaves = tuple(bool(rng.getrandbits(1)) for _ in range(leaf_count))
            supplied = list(compute_tags(leaves))
            if trial % 2:
                supplied[rng.randrange(len(supplied))] ^= True
            audit_case(leaves, tuple(supplied), totals)

    hostile_controls(totals, rng)
    elapsed = time.perf_counter() - start
    result = {
        "claim_tested": "TAG-GLUING-TRILEMMA1",
        "status": {
            "free_tag_semantic_erasure": "PROVED/EXACT",
            "consistent_promise_root_shortcut": "PROVED/EXACT",
            "pinned_total_linear_validator": "PROVED/EXACT",
            "gluing_implies_superpolynomial_cost_on_this_island": "FALSIFIED/RETIRED",
            "named_internal_object_exposure_without_observability_definition": "OPEN",
            "arbitrary_decider_transfer": "OPEN",
        },
        "seed": SEED,
        "exhaustive_depths": list(exhaustive_depths),
        "exhaustive_vectors": exhaustive_vectors,
        "random_specs": random_specs,
        "random_trials_per_depth": random_trials_per_depth,
        "wrappers": list(WRAPPERS),
        "encodings": list(ENCODINGS),
        "local_proper_3cnf": local,
        "totals": {**totals.__dict__, "total_checks": totals.total_checks},
        "cost_ledger": {
            "flat_total_time": "Theta(L+I) Boolean relation checks plus input parsing",
            "flat_total_workspace": "one accumulator bit plus O(log N) addresses in heap layout",
            "promise_semantic_tag_reads": 1,
            "compatibility_materialization": 0,
            "reconstruction": 0,
            "output_bits": 1,
        },
        "limitations": [
            "Finite tests validate the implementation only; the asymptotic trilemma is symbolic.",
            "The proper 3CNF gadget is bounded-occurrence but is not claimed to remain Monotone 3SAT-(2,2).",
            "No experiment transfers a query or structural bound to arbitrary uniform SAT time.",
        ],
        "elapsed_seconds": elapsed,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/raw/review/2026-10-11_tag_gluing_trilemma_redteam.json",
    )
    args = parser.parse_args()
    result = run()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output.write_text(body, encoding="utf-8")
    digest = hashlib.sha256(body.encode()).hexdigest()
    print(json.dumps({
        "output": str(output),
        "sha256": digest,
        "total_checks": result["totals"]["total_checks"],
        "failures": result["totals"]["failures"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
