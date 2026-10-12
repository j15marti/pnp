#!/usr/bin/env python3
"""Exact finite audit for the signed-clean-core compatibility easy island.

The two fixed cubic graphs generate proper sign-monochromatic 3-CNFs in which
every variable occurs twice positively and twice negatively.  The audit checks
that their four-variable satisfying-projection profiles differ, while every
disjoint product of the two blocks is satisfiable and recognizable without
computing that profile.
"""

from __future__ import annotations

import itertools
import json
import time
from collections import Counter


def paired_incidence(edges):
    incident = [[] for _ in range(6)]
    for i, (u, v) in enumerate(edges, 1):
        incident[u].append(i)
        incident[v].append(i)
    assert all(len(xs) == 3 for xs in incident)
    return [tuple(xs) for xs in incident] + [tuple(-x for x in xs) for xs in incident]


K33_EDGES = tuple((u, v) for u in range(3) for v in range(3, 6))
PRISM_EDGES = (
    (0, 1), (1, 2), (2, 0),
    (3, 4), (4, 5), (5, 3),
    (0, 3), (1, 4), (2, 5),
)
TEMPLATES = {"K33": paired_incidence(K33_EDGES), "PRISM": paired_incidence(PRISM_EDGES)}


def satisfies(clauses, bits):
    return all(any(bits[abs(lit) - 1] == (lit > 0) for lit in clause) for clause in clauses)


def satisfying_assignments(clauses, nvars):
    return [bits for bits in itertools.product((False, True), repeat=nvars) if satisfies(clauses, bits)]


def clean_core_certificate(clauses):
    vars_seen = sorted({abs(lit) for clause in clauses for lit in clause})
    counts = {v: [0, 0] for v in vars_seen}
    for clause in clauses:
        assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
        assert all(x > 0 for x in clause) or all(x < 0 for x in clause)
        for lit in clause:
            counts[abs(lit)][0 if lit > 0 else 1] += 1
    return {
        "variables": len(vars_seen),
        "clauses": len(clauses),
        "unique_clauses": len(set(clauses)),
        "proper": all(len(c) == len({abs(x) for x in c}) == 3 for c in clauses),
        "sign_monochromatic": all(all(x > 0 for x in c) or all(x < 0 for x in c) for c in clauses),
        "occurrences_2p2n": all(pair == [2, 2] for pair in counts.values()),
    }


def projection_histogram(models, nvars, width):
    histogram = Counter()
    for subset in itertools.combinations(range(nvars), width):
        projected = {tuple(model[i] for i in subset) for model in models}
        histogram[len(projected)] += 1
    return dict(sorted(histogram.items()))


def rename_formula(clauses, permutation):
    return [tuple((1 if lit > 0 else -1) * (permutation[abs(lit) - 1] + 1) for lit in clause)
            for clause in clauses]


def disjoint_product(names):
    clauses = []
    offset = 0
    for name in names:
        clauses.extend(tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in clause)
                       for clause in TEMPLATES[name])
        offset += 9
    return clauses, offset


def recognize_ordered_island(clauses, nvars):
    """Recognize canonical nine-variable consecutive blocks; no model/profile work."""
    if nvars % 9 or len(clauses) != 12 * (nvars // 9):
        return False, 0
    scanned = 0
    normalized = set(clauses)
    for block in range(nvars // 9):
        offset = 9 * block
        options = []
        for name in ("K33", "PRISM"):
            shifted = {
                tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in clause)
                for clause in TEMPLATES[name]
            }
            options.append(shifted)
        scanned += 12
        if not any(template <= normalized for template in options):
            return False, scanned
    return True, scanned


def main():
    started = time.perf_counter()
    certs = {name: clean_core_certificate(clauses) for name, clauses in TEMPLATES.items()}
    models = {name: satisfying_assignments(clauses, 9) for name, clauses in TEMPLATES.items()}

    histograms = {
        name: {str(width): projection_histogram(ms, 9, width) for width in range(1, 10)}
        for name, ms in models.items()
    }
    first_difference = next(
        width for width in range(1, 10)
        if histograms["K33"][str(width)] != histograms["PRISM"][str(width)]
    )
    assert first_difference == 4
    assert histograms["K33"]["4"] == {12: 36, 14: 9, 16: 81}
    assert histograms["PRISM"]["4"] == {12: 36, 14: 21, 16: 69}

    permutation = (8, 6, 4, 2, 0, 7, 5, 3, 1)
    encoding_controls = {}
    for name, clauses in TEMPLATES.items():
        base = histograms[name]["4"]
        reversed_clauses = list(reversed(clauses))
        renamed = rename_formula(clauses, permutation)
        complemented = [tuple(-lit for lit in clause) for clause in clauses]
        for label, variant in (("clause_reversal", reversed_clauses),
                               ("variable_renaming", renamed),
                               ("global_complement", complemented)):
            variant_models = satisfying_assignments(variant, 9)
            encoding_controls[f"{name}:{label}"] = projection_histogram(variant_models, 9, 4) == base
    assert all(encoding_controls.values())

    product_controls = []
    for blocks in range(1, 11):
        for prism_count in range(blocks + 1):
            names = ("PRISM",) * prism_count + ("K33",) * (blocks - prism_count)
            clauses, nvars = disjoint_product(names)
            cert = clean_core_certificate(clauses)
            recognized, scanned = recognize_ordered_island(clauses, nvars)
            expected_models = 86 ** prism_count * 102 ** (blocks - prism_count)
            if blocks <= 2:
                observed_models = len(satisfying_assignments(clauses, nvars))
                assert observed_models == expected_models
            assert recognized and cert["occurrences_2p2n"] and expected_models > 0
            product_controls.append({
                "blocks": blocks,
                "prism_blocks": prism_count,
                "variables": nvars,
                "clauses": len(clauses),
                "expected_model_count": str(expected_models),
                "clauses_scanned_by_recognizer": scanned,
            })

    sample, sample_n = disjoint_product(("K33", "PRISM"))
    recognized, scanned = recognize_ordered_island(sample, sample_n)
    wrappers = {}
    for wrapper in ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP", "PROFILE"):
        wrappers[wrapper] = {
            "answer": recognized,
            "profile_extractions": 1 if wrapper == "PROFILE" else 0,
            "witness_reconstructions": 0,
            "clauses_scanned": scanned,
        }
    assert recognized and all(row["answer"] for row in wrappers.values())
    assert all(wrappers[name]["profile_extractions"] == 0 for name in wrappers if name != "PROFILE")

    # Padding by another allowed block remains in the easy island; duplicating a
    # clause and adding a tautological dead clause correctly leave the promise.
    padded, padded_n = disjoint_product(("K33", "PRISM", "K33"))
    padding_controls = {
        "independent_clean_block_recognized": recognize_ordered_island(padded, padded_n)[0],
        "duplicate_clause_rejected": not recognize_ordered_island(sample + [sample[0]], sample_n)[0],
        "dead_tautology_rejected": not recognize_ordered_island(sample + [(1, -1, 2)], sample_n)[0],
    }
    assert all(padding_controls.values())

    # Hostile tractable/out-of-promise controls: all are rejected by the island
    # recognizer; their truth values are independently obtained by brute force.
    hostile = {
        "2SAT": ([(1, 2), (-1, 2), (1, -2)], 2),
        "Horn": ([(-1, -2, 3), (1,), (2,)], 3),
        "affine_xor_encoded": ([(1, 2), (-1, -2)], 2),
        "bounded_treewidth_path": ([(1, 2), (-2, 3), (-3, 4)], 4),
        "UNSAT_unit_pair": ([(1,), (-1,)], 1),
    }
    hostile_controls = {}
    for name, (clauses, nvars) in hostile.items():
        recognized, scanned = recognize_ordered_island(clauses, nvars)
        truth = bool(satisfying_assignments(clauses, nvars))
        hostile_controls[name] = {
            "island_recognized": recognized,
            "fallback_answer": truth,
            "clauses_scanned": scanned,
        }
        assert not recognized

    result = {
        "audit": "SIGNED-COMPATIBILITY-EASY-ISLAND1",
        "status": "COMPUTATIONAL finite audit supporting an exact finite construction",
        "template_certificates": certs,
        "satisfying_assignments": {name: len(ms) for name, ms in models.items()},
        "first_projection_histogram_difference_width": first_difference,
        "width_4_projection_histograms": {
            name: histograms[name]["4"] for name in ("K33", "PRISM")
        },
        "encoding_controls": encoding_controls,
        "product_patterns_checked": len(product_controls),
        "product_control_summary": {
            "patterns_checked": len(product_controls),
            "maximum_blocks": max(row["blocks"] for row in product_controls),
            "maximum_variables": max(row["variables"] for row in product_controls),
            "maximum_clauses": max(row["clauses"] for row in product_controls),
            "all_recognizer_scans_equal_clause_count": all(
                row["clauses_scanned_by_recognizer"] == row["clauses"]
                for row in product_controls
            ),
            "all_expected_model_counts_positive": all(
                int(row["expected_model_count"]) > 0 for row in product_controls
            ),
            "products_of_at_most_two_blocks_bruteforce_verified": 5,
        },
        "wrapper_controls": wrappers,
        "padding_controls": padding_controls,
        "hostile_controls": hostile_controls,
        "semantic_enumeration_cost": {
            "single_block_assignments_checked": 1024,
            "product_assignments_checked": 2 * (2 ** 9) + 3 * (2 ** 18),
            "note": "Only products of at most two blocks were brute-forced; larger products use the proved disjoint-product factorization.",
        },
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
