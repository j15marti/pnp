#!/usr/bin/env python3
"""Finite audit for SOURCE-CHANNEL-COMPLETENESS57.

Checks a restricted transcript-counting theorem, forced proper-3CNF source
recovery, shared-circuit gate counts/traces, an UNSAT control, and the real
DOUBLE_WRAPPER root.  No complexity-class conclusion is asserted.
"""

from collections import Counter, defaultdict
from itertools import product
import json
import math
import random


WRAPPER_ROOT = [
    (-12, -1, 13), (-10, 1, 9), (-9, -2, 11), (-8, -1, 6),
    (-6, 1, 8), (-4, 1, 3), (-4, 2, 5), (-2, 6, 7),
    (-2, 10, 11), (-2, 12, 13), (-1, 10, 11), (-1, 13, 14),
    (1, 4, 5), (2, 3, 5), (2, 6, 8), (2, 13, 14),
    (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14),
]


def false_row_clause(variables, row):
    """The unique proper clause on variables that is false on row."""
    return tuple(v if bit == 0 else -v for v, bit in zip(variables, row))


def forced_formula(bits):
    """Seven blocked rows per triple plus one redundant cross-triple bridge."""
    n = len(bits)
    assert n >= 6 and n % 3 == 0
    triples = [tuple(range(i + 1, i + 4)) for i in range(0, n, 3)]
    clauses = []
    for triple in triples:
        target = tuple(bits[v - 1] for v in triple)
        for row in product((0, 1), repeat=3):
            if row != target:
                clauses.append(false_row_clause(triple, row))
    # Boundary j uses the last variable of the left triple and first two of
    # the right triple.  Hence every variable gets at most one bridge use.
    for left, right in zip(triples, triples[1:]):
        support = (left[2], right[0], right[1])
        clause = tuple(v if bits[v - 1] else -v for v in support)
        clauses.append(clause)
    return clauses


def eval_clause(clause, values):
    return any((values[abs(lit)] if lit > 0 else 1 - values[abs(lit)])
               for lit in clause)


def eval_formula(clauses, values):
    return all(eval_clause(c, values) for c in clauses)


def recover_forced_assignment(clauses):
    """Recover the unique source from seven-clause same-support blocks."""
    by_support = defaultdict(list)
    for clause in clauses:
        support = tuple(sorted(abs(x) for x in clause))
        if len(set(support)) != 3:
            return None
        by_support[support].append(clause)
    recovered = {}
    blocks = 0
    for support, group in by_support.items():
        if len(group) != 7:
            continue
        blocked = set()
        for clause in group:
            signs = {abs(lit): lit > 0 for lit in clause}
            blocked.add(tuple(0 if signs[v] else 1 for v in support))
        if len(blocked) != 7:
            return None
        missing = next(iter(set(product((0, 1), repeat=3)) - blocked))
        for v, bit in zip(support, missing):
            if v in recovered and recovered[v] != bit:
                return None
            recovered[v] = bit
        blocks += 1
    all_vars = {abs(x) for c in clauses for x in c}
    if blocks == 0 or set(recovered) != all_vars:
        return None
    values = recovered
    if not eval_formula(clauses, values):
        return None
    return recovered


def permute_formula(clauses, permutation, rng):
    out = []
    for clause in clauses:
        out.append(tuple((1 if lit > 0 else -1) * permutation[abs(lit)]
                         for lit in clause))
    rng.shuffle(out)
    for i in range(len(out)):
        row = list(out[i])
        rng.shuffle(row)
        out[i] = tuple(row)
    return out


def build_shared_circuit(clauses, n):
    """Build all n NOT gates, two ORs/clause, and an AND chain."""
    gates = []

    def gate(op, a, b=None):
        wire = n + len(gates) + 1
        gates.append((wire, op, a, b))
        return wire

    neg = {v: gate("NOT", v) for v in range(1, n + 1)}
    outputs = []
    for clause in clauses:
        wires = [lit if lit > 0 else neg[-lit] for lit in clause]
        outputs.append(gate("OR", gate("OR", wires[0], wires[1]), wires[2]))
    out = outputs[0]
    for w in outputs[1:]:
        out = gate("AND", out, w)
    return gates, out


def eval_circuit(gates, output, values):
    state = dict(values)
    trace = []
    for wire, op, a, b in gates:
        if op == "NOT":
            value = 1 - state[a]
        elif op == "OR":
            value = state[a] | state[b]
        elif op == "AND":
            value = state[a] & state[b]
        else:
            raise AssertionError(op)
        state[wire] = value
        trace.append(value)
    return state[output], tuple(trace)


def transcript_bound_trials(rng, trials=800):
    """Arbitrary transcript partitions and h candidate equality probes."""
    assertions = 0
    worst_ratio = 0.0
    for _ in range(trials):
        n = rng.randint(3, 12)
        q = rng.randint(0, min(4, n))
        b = rng.randint(1, 3)
        t = rng.randint(0, 3)
        h = rng.randint(1, min(8, 1 << n))
        cap = 1 << (q + b * t)
        transcript = [rng.randrange(cap) for _ in range(1 << n)]
        candidates = {
            z: set(rng.sample(range(1 << n), min(h, 1 << n)))
            for z in set(transcript)
        }
        successes = sum(a in candidates[z] for a, z in enumerate(transcript))
        upper = min(1 << n, h * cap)
        assert successes <= upper
        assertions += 1
        worst_ratio = max(worst_ratio, successes / max(1, upper))
    return assertions, worst_ratio


def main():
    rng = random.Random(570512)
    assertions = 0
    instance_count = 0
    primary_evaluations = 0
    trace_comparisons = 0
    max_occurrence = 0

    samples_by_n = {6: 32, 9: 28, 12: 24, 15: 20, 18: 16}
    for n, samples in samples_by_n.items():
        for _ in range(samples):
            bits = tuple(rng.getrandbits(1) for _ in range(n))
            clauses = forced_formula(bits)
            m = len(clauses)
            assert m == 8 * n // 3 - 1
            occurrences = Counter(abs(x) for c in clauses for x in c)
            assert max(occurrences.values()) <= 8
            max_occurrence = max(max_occurrence, max(occurrences.values()))
            assertions += 2

            permutation_values = list(range(1, n + 1))
            rng.shuffle(permutation_values)
            permutation = {i + 1: permutation_values[i] for i in range(n)}
            shuffled = permute_formula(clauses, permutation, rng)
            recovered = recover_forced_assignment(shuffled)
            expected = {permutation[i + 1]: bits[i] for i in range(n)}
            assert recovered == expected
            assertions += 1

            gates, output = build_shared_circuit(shuffled, n)
            assert len(gates) == 9 * n - 4
            assertions += 1

            if n <= 12:
                sources = product((0, 1), repeat=n)
            else:
                random_sources = {bits}
                for i in range(n):
                    flipped = list(bits)
                    flipped[i] ^= 1
                    random_sources.add(tuple(flipped))
                while len(random_sources) < 128:
                    random_sources.add(tuple(rng.getrandbits(1) for _ in range(n)))
                # Convert original coordinates to renamed circuit coordinates.
                sources = random_sources

            satisfying = 0
            for source_bits in sources:
                renamed = {permutation[i + 1]: source_bits[i] for i in range(n)}
                fvalue = int(eval_formula(shuffled, renamed))
                cvalue, trace = eval_circuit(gates, output, renamed)
                cvalue2, trace2 = eval_circuit(gates, output, renamed)
                assert fvalue == cvalue
                assert trace == trace2
                satisfying += fvalue
                primary_evaluations += 1
                trace_comparisons += 1
                assertions += 2
            if n <= 12:
                assert satisfying == 1
                assertions += 1
            instance_count += 1

    # UNSAT control: add the eighth blocked row to one forced triple.
    unsat_bits = (0, 1, 0, 1, 0, 1)
    unsat = forced_formula(unsat_bits)
    unsat.append(false_row_clause((1, 2, 3), unsat_bits[:3]))
    assert recover_forced_assignment(unsat) is None
    assert not any(eval_formula(unsat, {i + 1: row[i] for i in range(6)})
                   for row in product((0, 1), repeat=6))
    # An unguarded b OR F(z) accepts every formula when b=1.  A well-formedness
    # guard rejects every tape for this malformed/UNSAT control.
    assert any(b or eval_formula(unsat, {i + 1: z[i] for i in range(6)})
               for b in (0, 1) for z in product((0, 1), repeat=6))
    assert not any((recover_forced_assignment(unsat) is not None) and
                   (b or eval_formula(unsat, {i + 1: z[i] for i in range(6)}))
                   for b in (0, 1) for z in product((0, 1), repeat=6))
    assertions += 4

    # Real WRAPPER root: source evaluation and deterministic shared trace.
    wrapper_gates, wrapper_output = build_shared_circuit(WRAPPER_ROOT, 14)
    wrapper_sat = 0
    for row in product((0, 1), repeat=14):
        values = {i + 1: row[i] for i in range(14)}
        fvalue = int(eval_formula(WRAPPER_ROOT, values))
        cvalue, trace = eval_circuit(wrapper_gates, wrapper_output, values)
        cvalue2, trace2 = eval_circuit(wrapper_gates, wrapper_output, values)
        assert fvalue == cvalue
        assert trace == trace2
        wrapper_sat += fvalue
        assertions += 2
    assert wrapper_sat == 1948
    assertions += 1

    transcript_assertions, worst_ratio = transcript_bound_trials(rng)
    assertions += transcript_assertions

    # Exhaustive arithmetic check of the necessary source-query threshold.
    threshold_checks = 0
    for n in range(2, 41):
        for q in range(0, n + 1):
            for b in range(1, 6):
                for h in (1, 2, 3, 4, 8, 16):
                    threshold = (n - 1 - q - math.log2(h)) / b
                    for t in range(0, 12):
                        bound = min(1.0, h * 2 ** (q + b * t - n))
                        if t < threshold:
                            assert bound < 0.5
                        threshold_checks += 1
                        assertions += 1

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "forced_family": {
            "instances": instance_count,
            "n_values": sorted(samples_by_n),
            "clauses_formula": "m=8n/3-1",
            "shared_gate_formula": "g=9n-4",
            "max_variable_occurrence_observed": max_occurrence,
            "primary_evaluations": primary_evaluations,
            "trace_comparisons": trace_comparisons,
            "shuffle_and_rename_recovery": True,
        },
        "restricted_transcript_bound": {
            "formula": "success<=min(1,h*2^(q+bt-n))",
            "random_partition_trials": transcript_assertions,
            "worst_success_to_upper_ratio": worst_ratio,
            "threshold_checks": threshold_checks,
        },
        "unsat_control": {
            "global_satisfying_assignments": 0,
            "source_scanner_accepts": False,
            "unguarded_b_or_F_has_bypass": True,
            "guarded_verifier_accepts": False,
        },
        "actual_wrapper_root": {
            "variables": 14,
            "clauses": 20,
            "shared_circuit_gates_with_all_NOTs": len(wrapper_gates),
            "satisfying_sources": wrapper_sat,
            "deterministic_trace_per_source": True,
        },
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
