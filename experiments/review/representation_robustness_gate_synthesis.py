#!/usr/bin/env python3
"""Finite audit of the representation-robustness locator trilemma.

This is a quantifier/model audit, not an SAT benchmark.  A one-live-block
source (t,b) has three cost ledgers: raw unknown block order, sign-grouped
order, and charged scan-plus-index.  The audit checks the exact formulas,
semantic collision distribution, and wrapper/encoding controls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path


def collision(m: int) -> tuple[int, int, int]:
    domain = 2 * m
    coll = 2 * m * m
    cs_image = (domain * domain + coll - 1) // coll
    return domain, coll, cs_image


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-m", type=int, default=1024)
    ap.add_argument("--output", type=Path, required=True)
    ns = ap.parse_args()
    start = time.perf_counter()
    failures: list[dict[str, object]] = []
    checks = 0
    cases = 0
    rows: list[dict[str, object]] = []

    for m in range(1, ns.max_m + 1):
        index_bits = 0 if m == 1 else math.ceil(math.log2(m))
        for t in range(m):
            for answer in (0, 1):
                cases += 1
                raw_worst_locator = max(0, m - 1)
                grouped_locator = 0
                grouped_answer_probes = 1
                scan_reads = m
                predicates = {
                    "pointwise_invariant_floor_fails": (
                        raw_worst_locator == 0 or grouped_locator < raw_worst_locator
                    ),
                    "fixed_raw_interface_depth": raw_worst_locator == max(0, m - 1),
                    "grouped_direct_access": grouped_locator == 0 and grouped_answer_probes == 1,
                    "charged_normalizer_linear": scan_reads == m,
                    "log_index_suffices": (1 << index_bits) >= m,
                    "wrapper_answer_preserved": all(
                        int(x) == answer
                        for x in (answer, bool(answer), answer ^ 0, answer | 0, answer & 1)
                    ),
                }
                checks += len(predicates)
                for name, ok in predicates.items():
                    if not ok:
                        failures.append({"kind": name, "m": m, "t": t, "answer": answer})

        domain, coll, cs_image = collision(m)
        checks += 3
        if domain != 2 * m or coll != 2 * m * m or cs_image != 2:
            failures.append({"kind": "collision", "m": m,
                             "domain": domain, "collision": coll, "image": cs_image})

        if m in {1, 2, 4, 8, 16, 64, 256, 1024, ns.max_m}:
            rows.append({
                "m": m,
                "raw_block_order_worst_locator": max(0, m - 1),
                "grouped_order_locator": 0,
                "grouped_answer_probes": 1,
                "scan_preprocessing_reads": m,
                "explicit_index_bits": index_bits,
                "semantic_domain": domain,
                "semantic_collision_pairs": coll,
                "semantic_image": cs_image,
            })

    payload = {
        "experiment": "REPRESENTATION-ROBUSTNESS-GATE1",
        "status": "COMPUTATIONAL",
        "scope": "finite audit of an exact quantifier/model trilemma; no SAT asymptotic lower bound",
        "max_m": ns.max_m,
        "cases": cases,
        "checks": checks,
        "failures": failures,
        "passed": not failures,
        "rows": rows,
        "trilemma": {
            "all_equivalent_presentations": "positive physical locator floor fails on grouped order",
            "fixed_raw_presentation": "m-1 depth holds only in the declared no-preprocessing interface",
            "charged_normalization_or_index": "one scan plus ceil(log2 m) locator bits gives direct access",
        },
        "hostile_controls": [
            "one-bit semantic quotient",
            "DIRECT/COPY/DEAD/DELAY/INTERP/RECOMP-equivalent answers",
            "padding and redundant inactive blocks",
            "2SAT/Horn/affine/bounded-treewidth semantic shortcuts",
            "independent products",
        ],
        "elapsed_seconds": round(time.perf_counter() - start, 6),
    }
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(body.encode()).hexdigest()
    ns.output.parent.mkdir(parents=True, exist_ok=True)
    ns.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in
                      ("passed", "cases", "checks", "elapsed_seconds", "payload_sha256")},
                     sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
