#!/usr/bin/env python3
"""Independent finite audit of the representative-maintenance lemma."""

from __future__ import annotations

import itertools
import json
import random
from dataclasses import dataclass, asdict


SEED = 202610192148


def maintain_word(witnesses, source, nbits, counters):
    """Keep one witness agreeing with the source prefix, or reject forever."""
    current = witnesses[0] if witnesses else None
    for t in range(nbits):
        if current is None:
            continue
        selected = None
        for candidate in witnesses:
            counters.candidate_trials += 1
            if ((candidate >> t) & 1) != ((source >> t) & 1):
                continue
            agree = True
            for j in range(t):
                counters.prefix_bit_comparisons += 1
                if ((candidate >> j) & 1) != ((current >> j) & 1):
                    agree = False
                    break
            if agree:
                selected = candidate
                break
        current = selected
    return current


OPS = ("AND", "OR", "NOT")


def circuit_descriptions(n, s):
    """All ordered fan-in-two AND/OR/NOT descriptions of at most s gates."""
    for output in range(n):
        yield (), output
    layer = [()]
    for gate_count in range(1, s + 1):
        nxt = []
        available = n + gate_count - 1
        for prefix in layer:
            for op in OPS:
                arity = 1 if op == "NOT" else 2
                for inputs in itertools.product(range(available), repeat=arity):
                    gate = (op, inputs[0], -1 if arity == 1 else inputs[1])
                    desc = prefix + (gate,)
                    nxt.append(desc)
                    for output in range(n + gate_count):
                        yield desc, output
        layer = nxt


def circuit_bit(n, desc, output, assignment):
    values = [(assignment >> i) & 1 for i in range(n)]
    for op, a, b in desc:
        if op == "NOT":
            values.append(1 - values[a])
        elif op == "AND":
            values.append(values[a] & values[b])
        else:
            values.append(values[a] | values[b])
    return values[output]


def truth_table(n, circuit):
    desc, output = circuit
    table = 0
    for assignment in range(1 << n):
        table |= circuit_bit(n, desc, output, assignment) << assignment
    return table


def maintain_circuit(circuits, n, source, counters):
    current = circuits[0] if circuits else None
    for t in range(1 << n):
        if current is None:
            continue
        selected = None
        source_bit = (source >> t) & 1
        for candidate in circuits:
            counters.candidate_trials += 1
            counters.circuit_bit_evaluations += 1
            if circuit_bit(n, *candidate, t) != source_bit:
                continue
            agree = True
            for j in range(t):
                counters.prefix_bit_comparisons += 1
                counters.circuit_bit_evaluations += 2
                if circuit_bit(n, *candidate, j) != circuit_bit(n, *current, j):
                    agree = False
                    break
            if agree:
                selected = candidate
                break
        current = selected
    return current


@dataclass
class Counters:
    generic_families: int = 0
    generic_sources: int = 0
    circuit_sources: int = 0
    candidate_trials: int = 0
    prefix_bit_comparisons: int = 0
    circuit_bit_evaluations: int = 0
    failures: int = 0


def run():
    rng = random.Random(SEED)
    counters = Counters()

    # Exhaust all witness families over three-bit outputs, including empty.
    universe = list(range(1 << 3))
    for family_mask in range(1 << len(universe)):
        witnesses = [w for w in universe if (family_mask >> w) & 1]
        counters.generic_families += 1
        for source in universe:
            counters.generic_sources += 1
            result = maintain_word(witnesses, source, 3, counters)
            expected = source in witnesses
            if (result is not None) != expected or (result is not None and result != source):
                counters.failures += 1
                raise AssertionError((witnesses, source, result))

    circuit_cases = []
    for n, s, sources in (
        (2, 1, list(range(1 << (1 << 2)))),
        (3, 2, list(range(1 << (1 << 3)))),
        (4, 2, rng.sample(range(1 << (1 << 4)), 64)),
    ):
        circuits = list(circuit_descriptions(n, s))
        yes_tables = {truth_table(n, c) for c in circuits}
        before = asdict(counters)
        for source in sources:
            counters.circuit_sources += 1
            result = maintain_circuit(circuits, n, source, counters)
            expected = source in yes_tables
            if (result is not None) != expected:
                counters.failures += 1
                raise AssertionError((n, s, source, expected, result))
            if result is not None and truth_table(n, result) != source:
                counters.failures += 1
                raise AssertionError((n, s, source, truth_table(n, result)))
        after = asdict(counters)
        circuit_cases.append({
            "n": n,
            "s": s,
            "descriptions": len(circuits),
            "semantic_yes_tables": len(yes_tables),
            "sources_checked": len(sources),
            "candidate_trials": after["candidate_trials"] - before["candidate_trials"],
            "prefix_bit_comparisons": after["prefix_bit_comparisons"] - before["prefix_bit_comparisons"],
            "circuit_bit_evaluations": after["circuit_bit_evaluations"] - before["circuit_bit_evaluations"],
        })

    result = {
        "run_id": "REPRESENTATIVE-MAINTENANCE-CEILING5",
        "seed": SEED,
        "status": "PASS" if counters.failures == 0 else "FAIL",
        "generic_exhaustion": {
            "output_bits": 3,
            "all_witness_families": counters.generic_families,
            "all_family_source_pairs": counters.generic_sources,
        },
        "circuit_cases": circuit_cases,
        "totals": asdict(counters),
        "theorem_scope": {
            "space": "two witness descriptors plus enumerator, evaluator and counters",
            "update_time": "linear in witness-class size times prefix length and evaluation cost",
            "mmw_poly_update": False,
            "p_vs_np": "OPEN",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
