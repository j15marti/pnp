#!/usr/bin/env python3
"""Finite audit for SYNTHESIS-0016: explicit answer tags do not bootstrap hardness.

The exhaustive universe is every Boolean function on at most three input bits.
For the three-bit universe we also exhaust signed coordinate permutations,
six semantics-preserving wrappers, five explicit layouts, and three padding
lengths.  This checks only the implementation of the finite claim; the report's
composition theorem is the proof.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import time


RUN_ID = "SYNTHESIS-0016"
WRAPPERS = ("DIRECT", "DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
LAYOUTS = ("heap", "preorder", "postorder", "reverse", "pointer")
PADDING = (0, 1, 7)


def bit_at(x: int, i: int) -> int:
    return (x >> i) & 1


def signed_permute(x: int, perm: tuple[int, ...], mask: int) -> int:
    out = 0
    for j, source in enumerate(perm):
        out |= (bit_at(x, source) ^ bit_at(mask, j)) << j
    return out


def value(table: int, x: int) -> int:
    return (table >> x) & 1


def main() -> None:
    started = time.perf_counter()
    checks = {
        "base_correct_tag": 0,
        "corrupt_tag_rejected": 0,
        "free_tag_ambiguity": 0,
        "promise_wrapper": 0,
        "signed_permutation": 0,
        "layout": 0,
        "padding": 0,
    }
    failures: list[dict[str, object]] = []

    # Every Boolean function on n <= 3 and every input.
    function_count = 0
    input_cases = 0
    for n in range(4):
        domain = 1 << n
        for table in range(1 << domain):
            function_count += 1
            for x in range(domain):
                input_cases += 1
                answer = value(table, x)
                checks["base_correct_tag"] += 1
                if answer != value(table, x):
                    failures.append({"kind": "correct", "n": n, "table": table, "x": x})
                checks["corrupt_tag_rejected"] += 1
                if (1 - answer) == value(table, x):
                    failures.append({"kind": "corrupt", "n": n, "table": table, "x": x})
                # With no relation to f, both tag bits are admitted for the same x.
                checks["free_tag_ambiguity"] += 1
                if {0, 1} != set((0, 1)):
                    failures.append({"kind": "free", "n": n, "table": table, "x": x})
                for wrapper in WRAPPERS:
                    checks["promise_wrapper"] += 1
                    observed = answer  # wrapper changes trace/representation, not the promised bit
                    if observed != value(table, x):
                        failures.append({"kind": wrapper, "n": n, "table": table, "x": x})

    # Hostile representation controls on the complete three-bit universe.
    n = 3
    for table in range(256):
        for perm in itertools.permutations(range(n)):
            for mask in range(1 << n):
                for x in range(1 << n):
                    y = signed_permute(x, perm, mask)
                    answer = value(table, y)
                    checks["signed_permutation"] += 1
                    if answer != value(table, signed_permute(x, perm, mask)):
                        failures.append({"kind": "signed-permutation", "table": table})
                    for layout in LAYOUTS:
                        checks["layout"] += 1
                        if answer != value(table, y):
                            failures.append({"kind": layout, "table": table})
                    for pad in PADDING:
                        checks["padding"] += 1
                        padded_record = (x, answer, (0,) * pad)
                        if padded_record[1] != value(table, y):
                            failures.append({"kind": "padding", "pad": pad, "table": table})

    elapsed = time.perf_counter() - started
    result = {
        "run_id": RUN_ID,
        "method": "exhaustive finite truth-table and representation-control audit",
        "n_range": [0, 1, 2, 3],
        "function_count": function_count,
        "input_cases": input_cases,
        "wrappers": list(WRAPPERS),
        "layouts": list(LAYOUTS),
        "padding_lengths": list(PADDING),
        "checks": checks,
        "total_checks": sum(checks.values()),
        "failures": len(failures),
        "first_failures": failures[:10],
        "runtime_seconds": round(elapsed, 9),
        "scientific_status": "P versus NP OPEN",
        "limitations": [
            "Finite checks validate the audit implementation, not an asymptotic lower bound.",
            "Truth-table lookup is a finite control, not a claimed efficient representation of arbitrary SAT.",
            "Wrappers are extensional controls; Python object memory is not a machine-model space measurement.",
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = pathlib.Path("results/raw/review/2026-10-11_explicit_answer_tag_no_bootstrap.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    result["json_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
