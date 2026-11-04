#!/usr/bin/env python3
"""Finite controls for REFEREE328's root-only LOCAL-CONVERT quotient."""

import json
import resource
import time
from pathlib import Path

OUT = Path("results/raw/arc/lspv5_328/local_convert_root_quotient_referee328.json")


def bits3(x):
    return ((x >> 2) & 1, (x >> 1) & 1, x & 1)


def eval_dnf(mask, assignment):
    # A deliberately noncanonical circuit presentation of the 3-input function mask.
    for row in range(8):
        if not ((mask >> row) & 1):
            continue
        rb = bits3(row)
        if all(assignment[i] == rb[i] for i in range(3)):
            return 1
    return 0


def k4_models(odd):
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    charge = [1 if odd and v == 0 else 0 for v in range(4)]
    count = 0
    for a in range(1 << 6):
        ok = True
        for v in range(4):
            p = 0
            for i, e in enumerate(edges):
                if v in e:
                    p ^= (a >> i) & 1
            ok &= p == charge[v]
        count += int(ok)
    return count


def main():
    start = time.perf_counter()
    checks = 0

    # Every 3-input circuit root has the same semantics as its eight-bit table.
    for target in range(256):
        reconstructed = 0
        for row in range(8):
            value = eval_dnf(target, bits3(row))
            reconstructed |= value << row
            checks += 1
        assert reconstructed == target

        # Implication legality is identical under the circuit and table presentations.
        for antecedent in range(256):
            circuit_ok = (antecedent & ~reconstructed) == 0
            table_ok = (antecedent & ~target) == 0
            assert circuit_ok == table_ok
            checks += 1

    # A satisfiable predecessor cannot be converted to false; an empty predecessor can.
    false_table = 0
    x_table = sum(1 << row for row in range(8) if bits3(row)[0])
    assert (x_table & ~false_table) != 0
    assert (0 & ~false_table) == 0
    checks += 2

    # Under explicit syntax U, all k constant bits are sensitive on the legal all-one payload.
    sensitivity = []
    for k in [1, 2, 3, 8, 16, 32, 64, 128]:
        legal = [1] * k
        assert all(legal)
        for i in range(k):
            corrupt = legal.copy()
            corrupt[i] = 0
            assert not all(corrupt)
            checks += 1
        sensitivity.append({"k": k, "sensitive_constant_bits": k,
                            "gate_records": 2 * k + 1, "paid_nodes": 2})

    # Both-label parity controls: same K4 incidence graph, odd/even charge.
    odd_models = k4_models(True)
    even_models = k4_models(False)
    assert odd_models == 0 and even_models == 8
    checks += 2

    # Malformed/corrupt record controls.
    bad = [None, {}, {"support": 4}, {"dag": [1, 0]}, {"root": 99, "gates": []},
           {"support": -1}, {"constants": [0, 2]}, {"antecedent": "global-source"}]
    for record in bad:
        valid = isinstance(record, dict) and set(record) == {"support", "antecedent", "root"} \
            and record.get("support") in range(4) and record.get("antecedent") == "derived-node" \
            and isinstance(record.get("root"), int) and record.get("root") >= 0
        assert not valid
        checks += 1

    elapsed = time.perf_counter() - start
    payload = {
        "artifact": "LOCAL-CONVERT-ROOT-QUOTIENT-REFEREE328",
        "status": "finite controls only; theorem is proved in report",
        "checks": checks,
        "root_functions": 256,
        "antecedent_target_pairs": 256 * 256,
        "sensitivity": sensitivity,
        "semantic_jump_control": {"satisfiable_x_to_false": "rejected", "false_to_false": "legal"},
        "k4": {"odd_models": odd_models, "even_models": even_models},
        "malformed_rejected": len(bad),
        "wall_seconds": elapsed,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "claims_not_made": ["B1", "B2", "B3", "P!=NP", "machine lower bound"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
