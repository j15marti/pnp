#!/usr/bin/env python3
"""Exclude the one-zero-premise-DEF cost-8 class for rsmu_5_7_1.

The fixed source-independent VARDEF rule charges one fresh-variable gate
instruction and exposes authenticated local CNF slots.  At q=8, minimality
and the source-excess identity force a tree whose DEF node is a leaf, so only
one slot can occur in the contradiction ancestry.  We strengthen the rule by
allowing that leaf to be *any* non-tautological clause containing the fresh
variable and at most two original variables.  This covers every CNF slot of
every local two-input Boolean gate, independent of the chosen finite basis.

The tree search also grants free exact clause/affine aliases and AND3 whenever
the output truth function has essential support at most three.  Therefore a
negative result is a valid lower certificate for the actual one-DEF class.
Optimizer work is external certification and is not charged to W_R.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
import resource
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from experiments.arc.lspv5_300.peitl_mixed_floor_referee300 import (
    aliases,
    clause_tt,
    malformed_controls,
    mixed_combine,
    model_count,
    parity_cnf_k4,
    parse_dimacs,
    sign_flip_counts,
)
from experiments.arc.lspv5_302.peitl_seven_node_exclusion_referee302 import (
    resolution_witness,
)


INPUT = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
OUT = Path("results/raw/arc/2026-11-02_2048_LSPV5_PEITL_ONE_DEF_EXCLUSION_REFEREE303_raw.json")


def canonical_clause(values):
    values = set(values)
    if 0 in values or any(-lit in values for lit in values):
        raise ValueError("not a non-tautological clause")
    return tuple(sorted(values, key=lambda x: (abs(x), x < 0)))


def all_relaxed_def_slots(original_n: int, fresh: int):
    """All clauses with fresh and zero, one, or two original variables."""
    slots = set()
    for fresh_sign in (fresh, -fresh):
        for arity in range(3):
            for variables in itertools.combinations(range(1, original_n + 1), arity):
                for signs in itertools.product((1, -1), repeat=arity):
                    slots.add(canonical_clause((fresh_sign,) + tuple(s * v for s, v in zip(signs, variables))))
    return sorted(slots, key=lambda c: (len(c), c))


def tree_search_with_extra_leaf(source_clauses, n, extra_clause, clause_alias, affine_alias, combine_cache):
    leaves = list(source_clauses) + [extra_clause]
    m = len(leaves)
    bank = [set() for _ in range(1 << m)]
    for i, clause in enumerate(leaves):
        bank[1 << i].add(clause_tt(clause, n))
    pair_tests = generated = 0

    def combine(a, b):
        key = (a, b) if a <= b else (b, a)
        if key not in combine_cache:
            combine_cache[key] = tuple(mixed_combine(a, b, n, clause_alias, affine_alias))
        return combine_cache[key]

    for count in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != count:
                continue
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if right and left & least:
                    for a in bank[left]:
                        for b in bank[right]:
                            pair_tests += 1
                            made = combine(a, b)
                            generated += len(made)
                            bank[whole].update(made)
                left = (left - 1) & whole
    return {
        "contains_false": 0 in bank[-1],
        "terminal_functions": len(bank[-1]),
        "pair_tests": pair_tests,
        "generated_outputs": generated,
        "states_total": sum(len(x) for x in bank),
    }


def main():
    started = time.perf_counter()
    raw = INPUT.read_bytes()
    original_n, clauses = parse_dimacs(raw.decode())
    n = original_n + 1
    fresh = n
    slots = all_relaxed_def_slots(original_n, fresh)
    clause_alias, affine_alias = aliases(n)
    combine_cache = {}
    cases = []
    contradiction_slots = []
    totals = {"pair_tests": 0, "generated_outputs": 0, "states_total": 0}
    for slot in slots:
        result = tree_search_with_extra_leaf(
            clauses, n, slot, clause_alias, affine_alias, combine_cache
        )
        cases.append({"slot": slot, **result})
        for key in totals:
            totals[key] += result[key]
        if result["contains_false"]:
            contradiction_slots.append(slot)

    deletions = [model_count(clauses[:i] + clauses[i + 1 :], original_n) for i in range(len(clauses))]
    flips = sign_flip_counts(clauses, original_n)
    malformed = malformed_controls()
    odd_n, odd = parity_cnf_k4((1, 0, 0, 0))
    even_n, even = parity_cnf_k4((0, 0, 0, 0))
    parity = {"odd_models": model_count(odd, odd_n), "even_models": model_count(even, even_n)}
    upper = resolution_witness(clauses)
    assertions = {
        "authentic_sha256": hashlib.sha256(raw).hexdigest()
        == "6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6",
        "source_unsat": model_count(clauses, original_n) == 0,
        "clause_minimal": all(x > 0 for x in deletions),
        "all_occurrence_sign_flips_sat": all(x > 0 for x in flips),
        "all_102_relaxed_def_slots_enumerated": len(slots) == 102,
        "one_def_tree_class_excluded": not contradiction_slots,
        "nine_node_resolution_upper": len(upper) == 9 and upper[-1]["clause"] == (),
        "all_malformed_rejected": all(malformed.values()),
        "parity_both_labels": parity == {"odd_models": 0, "even_models": 8},
    }
    if not all(assertions.values()):
        raise AssertionError({"assertions": assertions, "contradiction_slots": contradiction_slots})

    result = {
        "claim_id": "PEITL-ONE-DEF-EXCLUSION-REFEREE303",
        "status": {
            "topology_reduction": "PROVED/EXACT",
            "one_def_relaxed_tree_exclusion": "COMPUTATIONAL exhaustive finite",
            "remaining_cost8_class": "OPEN: bicyclic binary ancestry",
            "mixed_interval": "PROVED 8 <= W_Rmix341 <= 9; cost 8 only if bicyclic",
            "B1_B2_B3": "OPEN",
        },
        "input": {
            "path": str(INPUT),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "variables": original_n,
            "clauses": clauses,
            "deletion_model_counts": deletions,
            "sign_flip_model_counts": flips,
        },
        "fixed_calculus": "Rmix341 source-independent zero-premise VARDEF; unit binary RES/AND3/XOR; exact paid unary CONVERT",
        "topology_identity": "q-(mu-1)=beta+u+2*d0; q=8, mu=7, d0=1 forces beta=u=0 and seven binary nodes; connected ancestry is a tree with the DEF node as a leaf",
        "def_relaxation": "the unique used DEF edge may carry any non-tautological clause containing fresh variable 6 and at most two original variables; 102 slots cover every local two-input gate defining clause",
        "operation_relaxations": [
            "free exact clause aliases",
            "free exact affine aliases",
            "AND3 whenever output essential support is at most three",
        ],
        "slot_count": len(slots),
        "contradiction_slots": contradiction_slots,
        "aggregate_search": {**totals, "combine_cache_entries": len(combine_cache)},
        "cases": cases,
        "resolution_upper_certificate": upper,
        "malformed_controls": malformed,
        "parity_controls": parity,
        "assertions": assertions,
        "optimizer_cost_note": "free best proof selection is granted; enumeration work is external certification, not part of W_R",
        "resource_ledger": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": platform.python_version(),
            "all_phase_note": "materializes 64-bit truth tables, 102 subset-DP banks sequentially, shared operation cache, controls and JSON; no machine lower-bound or sublinear-space claim",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(OUT),
        "assertions": assertions,
        "slot_count": len(slots),
        "aggregate_search": result["aggregate_search"],
        "terminal_range": [min(x["terminal_functions"] for x in cases), max(x["terminal_functions"] for x in cases)],
        "resources": result["resource_ledger"],
    }, indent=2))


if __name__ == "__main__":
    main()
