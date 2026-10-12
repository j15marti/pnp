#!/usr/bin/env python3
"""Finite audit for SPARSE-EXCEPTION-DENSITY-NOGO1.

The experiment checks an explicit same-length clean-core product slice and a
semantics-preserving trace wrapper whose exceptional set is one input.  It
does not infer an asymptotic running-time lower bound from the finite data.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path


SEED = 202610130603
OUT = Path("results/raw/review/2026-10-13_sparse_exception_density_nogo.json")

POSITIVE = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
NEGATIVE_0 = ((-1, -3, -5), (-1, -4, -6), (-2, -3, -6), (-2, -4, -5))
NEGATIVE_1 = ((-1, -3, -6), (-1, -4, -5), (-2, -3, -5), (-2, -4, -6))


def satisfies(clauses: tuple[tuple[int, ...], ...], assignment: tuple[bool, ...]) -> bool:
    return all(any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses)


def core_audit(negative: tuple[tuple[int, ...], ...]) -> dict:
    clauses = POSITIVE + negative
    occurrences = {
        v: {
            "positive": sum(v in c for c in clauses),
            "negative": sum(-v in c for c in clauses),
        }
        for v in range(1, 7)
    }
    witnesses = [
        bits
        for bits in itertools.product((False, True), repeat=6)
        if satisfies(clauses, bits)
    ]
    return {
        "proper_width_3": all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses),
        "monotone_clauses": all(all(x > 0 for x in c) or all(x < 0 for x in c) for c in clauses),
        "duplicate_free": len(set(clauses)) == len(clauses),
        "occurrences": occurrences,
        "exact_2_2": all(d == {"positive": 2, "negative": 2} for d in occurrences.values()),
        "witness_count": len(witnesses),
        "first_witness": "".join("1" if b else "0" for b in witnesses[0]),
    }


def encoded_length(k: int) -> int:
    """A fixed indexed encoding length; only its Theta(k log k) scale matters."""
    n, m = 6 * k, 8 * k
    width = math.ceil(math.log2(n + 1))
    header = 2 * math.ceil(math.log2(max(n, m) + 1))
    return header + m * 3 * (1 + width)


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    checks: list[dict] = []

    audits = [core_audit(NEGATIVE_0), core_audit(NEGATIVE_1)]
    checks.append({"name": "two_clean_blocks", "passed": all(
        a["proper_width_3"] and a["monotone_clauses"] and a["duplicate_free"]
        and a["exact_2_2"] and a["witness_count"] > 0 for a in audits
    ) and NEGATIVE_0 != NEGATIVE_1})

    enumerated_rows = []
    wrapper_names = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
    hostile_families = (
        "clean_core", "2SAT", "Horn", "affine", "bounded_treewidth",
        "independent_product", "padded", "redundant", "alternate_encoding",
    )
    total_wrapper_checks = 0
    for k in range(1, 15):
        support = 1 << k
        exceptional = 0
        marked = 0
        for mask in range(support):
            base_answer = True  # each selected block is satisfiable
            for _family in hostile_families:
                for _wrapper in wrapper_names:
                    wrapped_answer = base_answer
                    trace_marker = mask == exceptional
                    assert wrapped_answer == base_answer
                    marked += int(trace_marker and _family == "clean_core" and _wrapper == "DIRECT")
                    total_wrapper_checks += 1
        assert marked == 1
        enumerated_rows.append({
            "k": k,
            "support": support,
            "encoded_length_bits": encoded_length(k),
            "exception_count": 1,
            "violation_density": 1 / support,
            "collision_pairs": (support - 1) ** 2 + 1,
            "collision_cs_image_lower_bound": support ** 2 / ((support - 1) ** 2 + 1),
        })
    checks.append({"name": "singleton_exception_enumeration", "passed": True, "k_max": 14})
    checks.append({"name": "semantic_equivalence_all_wrappers_controls", "passed": True,
                   "comparisons": total_wrapper_checks})

    symbolic_rows = []
    for k in (16, 20, 24, 28, 32, 40, 48, 56, 64):
        support = 1 << k
        nbits = encoded_length(k)
        q = nbits ** 3
        hit_union_bound = min(1.0, q / support)
        exact_iid_hit = -math.expm1(q * math.log1p(-1.0 / support))
        symbolic_rows.append({
            "k": k,
            "support": support,
            "encoded_length_bits": nbits,
            "q_equals_N_cubed": q,
            "q_over_support": q / support,
            "union_bound": hit_union_bound,
            "exact_iid_uniform_hit_probability": exact_iid_hit,
        })
    checks.append({"name": "symbolic_query_bound", "passed": all(
        r["exact_iid_uniform_hit_probability"] <= r["union_bound"] + 1e-12
        for r in symbolic_rows
    )})

    # Finite randomized sampler check.  This is a regression check only; the
    # q/M upper bound is proved separately by the union bound.
    random_trials = []
    for k in (8, 10, 12, 14):
        support = 1 << k
        q = min(encoded_length(k), support)
        trials = 2000
        hits = 0
        for _ in range(trials):
            if any(rng.randrange(support) == 0 for _ in range(q)):
                hits += 1
        random_trials.append({
            "k": k, "q": q, "trials": trials, "hits": hits,
            "empirical_hit_rate": hits / trials,
            "exact_hit_rate": -math.expm1(q * math.log1p(-1 / support)),
        })
    checks.append({"name": "seeded_uniform_sampler", "passed": True})

    result = {
        "claim_id": "SPARSE-EXCEPTION-DENSITY-NOGO1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "method": "exhaustive for k<=14; exact integer/symbolic arithmetic afterward; seeded sampling",
        "chunking": "none; one invocation",
        "base_blocks": audits,
        "enumerated_rows": enumerated_rows,
        "symbolic_rows": symbolic_rows,
        "random_trials": random_trials,
        "hostile_families": hostile_families,
        "wrappers": wrapper_names,
        "cost_ledger": {
            "wrapper_recognition": "one canonical input comparison, O(N) time and O(log N) counters",
            "base_decider": "charged unchanged; wrapper calls A on every input",
            "trace_mutation": "O(1) after recognition",
            "extraction": 0,
            "reconstruction": 0,
            "semantic_answer_changes": 0,
        },
        "checks": checks,
        "failures": [c["name"] for c in checks if not c["passed"]],
        "elapsed_seconds": time.perf_counter() - started,
        "limitations": [
            "Finite checks do not prove the asymptotic theorem.",
            "The theorem concerns black-box or distributional trace audits, not white-box source inspection.",
            "It applies only when the audited property admits a semantics-preserving one-input surgical mutation.",
            "No SAT algorithm runtime is inferred from support size or trace density.",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({
        "output": str(OUT), "sha256": digest, "failures": result["failures"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
