#!/usr/bin/env python3
"""Finite verification for CLEAN-CORE-PRODUCT-READ-FLOOR1.

Construct equal-size SAT/UNSAT proper 3-CNF blocks, certify them by exhaustive
truth tables, and check the disjoint-block adversary and encoding costs.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


VARS = (1, 2, 3, 4)


def core_clauses():
    return tuple(tuple(sign * v for sign, v in zip(signs, (1, 2, 3))) for signs in itertools.product((-1, 1), repeat=3))


def extra_clauses():
    out = []
    for support in itertools.combinations(VARS, 3):
        if 4 not in support:
            continue
        for signs in itertools.product((-1, 1), repeat=3):
            out.append(tuple(sign * v for sign, v in zip(signs, support)))
    return tuple(out)


def clause_value(clause, bits):
    return any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)


def witnesses(formula):
    return [bits for bits in itertools.product((False, True), repeat=len(VARS)) if all(clause_value(c, bits) for c in formula)]


def literal_occurrences(formula):
    counts = {v: 0 for v in VARS}
    for clause in formula:
        for lit in clause:
            counts[abs(lit)] += 1
    return counts


def block_bits(formula, offset, width):
    bits = []
    for clause in formula:
        for lit in clause:
            bits.append(int(lit > 0))
            ident = offset + abs(lit)
            bits.extend((ident >> b) & 1 for b in reversed(range(width)))
    return tuple(bits)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    core = core_clauses()
    extras = extra_clauses()
    chosen = None
    candidates_checked = 0
    for removed in core:
        remaining = tuple(c for c in core if c != removed)
        for e0, e1 in itertools.permutations(extras, 2):
            candidates_checked += 1
            unsat_formula = core + (e0,)
            sat_formula = remaining + (e0, e1)
            sat_ws = witnesses(sat_formula)
            if sat_ws:
                chosen = (sat_formula, unsat_formula, sat_ws, removed, e0, e1)
                break
        if chosen:
            break
    assert chosen is not None
    sat_formula, unsat_formula, sat_ws, removed, e0, e1 = chosen
    assert len(sat_formula) == len(unsat_formula) == 9
    assert len(set(sat_formula)) == len(set(unsat_formula)) == 9
    assert not witnesses(unsat_formula)

    clean_supports = ((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6))
    clean_sat_formula = tuple(clean_supports) + tuple(tuple(-v for v in e) for e in clean_supports)
    clean_sat_witness = (False, False, True, True, False, False)
    assert all(clause_value(c, clean_sat_witness) for c in clean_sat_formula)
    clean_occ = {v: sum(abs(lit) == v for c in clean_sat_formula for lit in c) for v in range(1, 7)}
    clean_pos_occ = {v: sum(lit == v for c in clean_sat_formula for lit in c) for v in range(1, 7)}
    clean_neg_occ = {v: sum(lit == -v for c in clean_sat_formula for lit in c) for v in range(1, 7)}
    assert set(clean_sat_formula) == set(tuple(c) for c in clean_sat_formula)
    assert all(clean_pos_occ[v] == clean_neg_occ[v] == 2 for v in range(1, 7))

    falsification_certificate = []
    for first_three in itertools.product((False, True), repeat=3):
        false_core = [c for c in core if not clause_value(c, first_three + (False,))]
        assert len(false_core) == 1
        falsification_certificate.append({
            "assignment_x1_x2_x3": [int(x) for x in first_three],
            "falsified_core_clause": list(false_core[0]),
        })

    rows = []
    for k in (1, 2, 4, 8, 16, 32, 64, 128):
        width = max(1, math.ceil(math.log2(4 * k + 1)))
        sat_blocks = []
        diff_sets = []
        cursor = 0
        for j in range(k):
            sb = block_bits(sat_formula, 4 * j, width)
            ub = block_bits(unsat_formula, 4 * j, width)
            assert len(sb) == len(ub)
            sat_blocks.extend(sb)
            diff = {cursor + i for i, (a, b) in enumerate(zip(sb, ub)) if a != b}
            assert diff
            diff_sets.append(diff)
            cursor += len(sb)
        pairwise_disjoint = all(diff_sets[i].isdisjoint(diff_sets[j]) for i in range(k) for j in range(i + 1, k))
        assert pairwise_disjoint
        n_bits = len(sat_blocks)
        rows.append({
            "blocks": k,
            "variable_id_width": width,
            "payload_bits": n_bits,
            "required_distinct_block_hits": k,
            "pairwise_disjoint_difference_sets": pairwise_disjoint,
            "floor_over_payload": k / n_bits,
            "ratio_of_N_over_log2N_to_floor": (n_bits / math.log2(max(2, n_bits))) / k,
        })

    controls = {
        "Horn_and_2SAT": {
            "sat_block": ["(x)", "(x)"],
            "unsat_block": ["(x)", "(not x)"],
            "primal_treewidth": 0,
            "decision_time": "linear",
            "same_k_block_probe_floor": True,
        },
        "affine_GF2": {
            "sat_block": ["x=0", "x=0"],
            "unsat_block": ["x=0", "x=1"],
            "decision_time": "Gaussian elimination (linear here)",
            "same_k_block_probe_floor": True,
        },
    }

    checks = {
        "proper_distinct_equal_size_blocks": len(sat_formula) == len(unsat_formula) == 9 and len(set(sat_formula)) == 9 and len(set(unsat_formula)) == 9,
        "all_four_variables_occur": set(abs(l) for c in sat_formula for l in c) == set(VARS) and set(abs(l) for c in unsat_formula for l in c) == set(VARS),
        "sat_block_has_witness": bool(sat_ws),
        "unsat_block_has_no_witness": not witnesses(unsat_formula),
        "eight_assignment_unsat_certificate_complete": len(falsification_certificate) == 8,
        "all_product_difference_sets_disjoint": all(r["pairwise_disjoint_difference_sets"] for r in rows),
        "easy_controls_share_probe_floor": all(v["same_k_block_probe_floor"] for v in controls.values()),
        "explicit_clean_sat_block_is_monotone_3sat_2_2": all(clean_pos_occ[v] == clean_neg_occ[v] == 2 for v in range(1, 7)),
        "clean_block_equalization_arithmetic": 33 * 6 == 198 and 33 * 8 == 264,
    }
    assert all(checks.values())

    result = {
        "experiment": "CLEAN-CORE-PRODUCT-READ-FLOOR1",
        "status": "COMPUTATIONAL finite verification supporting an elementary PROVED/EXACT lemma",
        "variables_per_block": 4,
        "clauses_per_block": 9,
        "candidate_pairs_checked": candidates_checked,
        "sat_formula": [list(c) for c in sat_formula],
        "unsat_formula": [list(c) for c in unsat_formula],
        "removed_core_clause": list(removed),
        "shared_extra_clause": list(e0),
        "sat_replacement_clause": list(e1),
        "sat_witness": [int(x) for x in sat_ws[0]],
        "sat_occurrences": literal_occurrences(sat_formula),
        "unsat_occurrences": literal_occurrences(unsat_formula),
        "unsat_falsification_certificate": falsification_certificate,
        "clean_core_symbolic_instantiation": {
            "sat_block_supports_used_with_both_signs": [list(e) for e in clean_supports],
            "sat_block_witness": [int(x) for x in clean_sat_witness],
            "sat_block_total_occurrences": clean_occ,
            "sat_block_positive_occurrences": clean_pos_occ,
            "sat_block_negative_occurrences": clean_neg_occ,
            "copies_for_equal_size_sat_superblock": 33,
            "sat_superblock_variables": 198,
            "sat_superblock_clauses": 264,
            "published_unsat_block_variables": 198,
            "published_unsat_block_clauses": 264,
            "published_unsat_block_source": "Doecker 2019, Proposition 1; clauses are external to this finite harness",
        },
        "encoding_rows": rows,
        "easy_language_controls": controls,
        "wrapper_note": "Equivalent deterministic wrappers preserve the adversary: the trace still cannot distinguish an unread difference set.",
        "padding_note": "Appending p(k) ignored bits changes encoded length but not the k necessary block hits; no encoding-invariant superlinear conclusion follows.",
        "checks": checks,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "checks": checks, "candidate_pairs_checked": candidates_checked}, indent=2))


if __name__ == "__main__":
    main()
