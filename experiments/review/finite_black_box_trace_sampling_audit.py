#!/usr/bin/env python3
"""Finite checks for the black-box trace-sampling non-certification lemma.

The theorem itself is elementary and does not depend on these measurements.
The experiment checks exact finite detection counts, seeded randomized sampling,
and hostile semantic-preserving program wrappers with an explicit cost ledger.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

SEED = 20261013
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-13_finite_black_box_trace_sampling.json"


def semantic_value(bits: tuple[int, ...], family: str) -> int:
    n = len(bits)
    if family == "2SAT":
        return int(any(bits))
    if family == "Horn":
        return int(all(bits))
    if family == "affine":
        return sum(bits) & 1
    if family == "bounded_treewidth":
        return int(all(bits[i] == bits[i + 1] for i in range(n - 1)))
    if family == "independent_product":
        h = n // 2
        return int(any(bits[:h]) and any(bits[h:]))
    if family == "padded":
        return int(any(bits[: max(1, n // 2)]))
    if family == "redundant":
        return int(any(bits) or any(bits))
    if family == "alternate_encoding":
        return int(any(reversed(bits)))
    raise ValueError(family)


def observed_run(
    bits: tuple[int, ...],
    family: str,
    wrapper: str,
    hidden: tuple[int, ...] | None,
) -> dict:
    """Return decision, declared trace observation, and all charged costs."""
    n = len(bits)
    decision = semantic_value(bits, family)
    trace = [f"family:{family}", f"wrapper:{wrapper}"]
    wrapper_cost = {
        "DIRECT": 0,
        "COPY": n,
        "DEAD": n,
        "DELAY": 2 * n,
        "INTERP": 3 * n,
        "RECOMP": 2 * n,
    }[wrapper]
    if wrapper in {"COPY", "INTERP"}:
        trace.append("copy")
    if wrapper in {"DEAD", "DELAY"}:
        trace.append("dead")
    if wrapper == "RECOMP":
        trace.append("recompute")
    if hidden is not None and bits == hidden:
        # The observable trace changes, but the one-bit decision does not.
        trace.append("needle-derived-tag")
        wrapper_cost += n + 1
    return {
        "decision": decision,
        "trace": trace,
        "cost": {
            "input_read": n,
            "needle_comparison": 0 if hidden is None else n,
            "semantic_decision_upper_bound": 2 * n + 1,
            "wrapper": wrapper_cost,
            "extraction": 0,
            "reconstruction": 0,
            "output": 1,
        },
    }


def exhaustive_counts() -> list[dict]:
    rows: list[dict] = []
    for n in range(2, 6):
        m = 1 << n
        for q in range(0, min(4, m - 1) + 1):
            query_sets = 0
            detected_pairs = 0
            missed_pairs = 0
            for query in itertools.combinations(range(m), q):
                query_sets += 1
                qset = set(query)
                for hidden in range(m):
                    if hidden in qset:
                        detected_pairs += 1
                    else:
                        missed_pairs += 1
            total = query_sets * m
            expected_detected = math.comb(m, q) * q
            assert detected_pairs == expected_detected
            assert detected_pairs + missed_pairs == total
            rows.append(
                {
                    "n": n,
                    "M": m,
                    "q": q,
                    "query_sets": query_sets,
                    "detected_pairs": detected_pairs,
                    "missed_pairs": missed_pairs,
                    "detection_fraction": detected_pairs / total if total else 0.0,
                    "exact_q_over_M": q / m,
                }
            )
    return rows


def randomized_counts(rng: random.Random) -> list[dict]:
    rows: list[dict] = []
    trials = 4000
    for n in (8, 10, 12):
        m = 1 << n
        for q in (1, 2, 4, 8, 16):
            hits = 0
            inclusion = [0] * m
            for _ in range(trials):
                query = rng.sample(range(m), q)
                hidden = rng.randrange(m)
                hits += int(hidden in query)
                for x in query:
                    inclusion[x] += 1
            least_seen = min(inclusion)
            rows.append(
                {
                    "n": n,
                    "M": m,
                    "q": q,
                    "trials": trials,
                    "hits": hits,
                    "empirical_detection": hits / trials,
                    "q_over_M": q / m,
                    "least_queried_point_frequency": least_seen / trials,
                    "averaging_bound_verified": least_seen / trials <= q / m,
                }
            )
            assert least_seen / trials <= q / m
    return rows


def hostile_wrapper_checks(rng: random.Random) -> dict:
    families = [
        "2SAT",
        "Horn",
        "affine",
        "bounded_treewidth",
        "independent_product",
        "padded",
        "redundant",
        "alternate_encoding",
    ]
    wrappers = ["DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP"]
    checked = 0
    queried_transcript_failures = 0
    semantic_failures = 0
    hidden_trace_failures = 0
    maximum_charged_cost = 0
    examples = []
    for n in range(4, 9):
        universe = list(itertools.product((0, 1), repeat=n))
        hidden = rng.choice(universe)
        queried = rng.sample([x for x in universe if x != hidden], min(12, len(universe) - 1))
        for family in families:
            for wrapper in wrappers:
                for bits in universe:
                    base = observed_run(bits, family, wrapper, None)
                    needle = observed_run(bits, family, wrapper, hidden)
                    checked += 1
                    if base["decision"] != needle["decision"]:
                        semantic_failures += 1
                    if bits in queried and base["trace"] != needle["trace"]:
                        queried_transcript_failures += 1
                    if bits == hidden and base["trace"] == needle["trace"]:
                        hidden_trace_failures += 1
                    maximum_charged_cost = max(
                        maximum_charged_cost, sum(needle["cost"].values())
                    )
                if len(examples) < 8:
                    examples.append(
                        {
                            "n": n,
                            "family": family,
                            "wrapper": wrapper,
                            "hidden": "".join(map(str, hidden)),
                            "queried_count": len(queried),
                            "base_hidden": observed_run(hidden, family, wrapper, None),
                            "needle_hidden": observed_run(hidden, family, wrapper, hidden),
                        }
                    )
    assert semantic_failures == 0
    assert queried_transcript_failures == 0
    assert hidden_trace_failures == 0
    return {
        "families": families,
        "wrappers": wrappers,
        "cases_checked": checked,
        "semantic_failures": semantic_failures,
        "queried_transcript_failures": queried_transcript_failures,
        "hidden_trace_failures": hidden_trace_failures,
        "maximum_charged_cost_in_finite_grid": maximum_charged_cost,
        "cost_interpretation": (
            "The needle program adds one O(n) equality check and a local trace-only "
            "event; preprocessing, decision, wrapper, extraction, reconstruction, "
            "and output costs are all charged."
        ),
        "examples": examples,
    }


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    payload = {
        "experiment": "FINITE-BLACK-BOX-TRACE-SAMPLING-NONCERTIFICATION1",
        "seed": SEED,
        "status": "COMPUTATIONAL finite verification; theorem proved separately",
        "exhaustive": exhaustive_counts(),
        "randomized": randomized_counts(rng),
        "hostile_wrappers": hostile_wrapper_checks(rng),
    }
    payload["elapsed_seconds"] = time.perf_counter() - started
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    payload["prewrite_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(
        {
            "output": str(OUT.relative_to(ROOT)),
            "elapsed_seconds": payload["elapsed_seconds"],
            "exhaustive_rows": len(payload["exhaustive"]),
            "randomized_rows": len(payload["randomized"]),
            "hostile_cases": payload["hostile_wrappers"]["cases_checked"],
            "failures": {
                key: value
                for key, value in payload["hostile_wrappers"].items()
                if key.endswith("failures")
            },
        },
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
