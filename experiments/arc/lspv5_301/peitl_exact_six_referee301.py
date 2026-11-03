#!/usr/bin/env python3
"""Exact Rmix341 cost audit for authentic rsmu_4_6_1.cnf.

The lower certificate exhausts a deliberately stronger relaxation of every
six-node proof topology allowed by SOURCE-EXCESS-EULER349.  Optimizer work is
reported separately and is not charged to W_R.
"""

from __future__ import annotations

import hashlib
import json
import platform
import resource
import time
from functools import lru_cache
from pathlib import Path

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


INPUT = Path("results/raw/arc/lspv5_300_peitl/rsmu_4_6_1.cnf")
OUT = Path("results/raw/arc/2026-11-02_1848_LSPV5_PEITL_EXACT_SIX_REFEREE301_raw.json")


def source_tree_states(clauses, n):
    m = len(clauses)
    clause_alias, affine_alias = aliases(n)
    bank = [dict() for _ in range(1 << m)]
    for i, clause in enumerate(clauses):
        table = clause_tt(clause, n)
        bank[1 << i][table] = ("SOURCE", i)
    combine_tests = generated = 0
    for count in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != count:
                continue
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if left & least and right:
                    for a in bank[left]:
                        for b in bank[right]:
                            combine_tests += 1
                            made = mixed_combine(a, b, n, clause_alias, affine_alias)
                            generated += len(made)
                            for out, op in made.items():
                                bank[whole].setdefault(out, (op, left, a, right, b))
                left = (left - 1) & whole
    return bank, clause_alias, affine_alias, combine_tests, generated


def relaxed_unicycle_search(clauses, n):
    """Exhaust all source-once unicyclic six-node DAGs, with free aliases."""
    m = len(clauses)
    full = (1 << m) - 1
    trees, clause_alias, affine_alias, tree_tests, tree_generated = source_tree_states(clauses, n)
    source_tables = [clause_tt(c, n) for c in clauses]
    root_tests = generated = 0

    @lru_cache(None)
    def extend(shared_table, exclusive_mask):
        indices = [i for i in range(m) if exclusive_mask >> i & 1]
        atom_tables = [shared_table] + [source_tables[i] for i in indices]
        atom_count = len(atom_tables)
        bank = [dict() for _ in range(1 << atom_count)]
        for i, table in enumerate(atom_tables):
            bank[1 << i][table] = ("ATOM", i)
        for count in range(2, atom_count + 1):
            for whole in range(1, 1 << atom_count):
                if whole.bit_count() != count:
                    continue
                least = whole & -whole
                left = (whole - 1) & whole
                while left:
                    right = whole ^ left
                    if left & least and right:
                        for a in bank[left]:
                            for b in bank[right]:
                                for out, op in mixed_combine(
                                    a, b, n, clause_alias, affine_alias
                                ).items():
                                    bank[whole].setdefault(out, (op, left, a, right, b))
                    left = (left - 1) & whole
        return bank[-1]

    for shared_mask in range(1, full + 1):
        rest = full ^ shared_mask
        tail_mask = rest
        while True:
            cycle_rest = rest ^ tail_mask
            left_only = cycle_rest
            while True:
                right_only = cycle_rest ^ left_only
                if left_only <= right_only:
                    for shared_table in trees[shared_mask]:
                        left_outputs = extend(shared_table, left_only)
                        right_outputs = extend(shared_table, right_only)
                        for left_table in left_outputs:
                            for right_table in right_outputs:
                                root_tests += 1
                                made = mixed_combine(
                                    left_table, right_table, n, clause_alias, affine_alias
                                )
                                generated += len(made)
                                for cycle_table in made:
                                    if 0 in extend(cycle_table, tail_mask):
                                        return {
                                            "contradiction_found": True,
                                            "shared_mask": shared_mask,
                                            "left_only": left_only,
                                            "right_only": right_only,
                                            "tail_mask": tail_mask,
                                            "shared_table": shared_table,
                                            "left_table": left_table,
                                            "right_table": right_table,
                                            "cycle_table": cycle_table,
                                        }
                if left_only == 0:
                    break
                left_only = (left_only - 1) & cycle_rest
            if tail_mask == 0:
                break
            tail_mask = (tail_mask - 1) & rest
    return {
        "contradiction_found": False,
        "root_pair_tests": root_tests,
        "generated_cycle_outputs": generated,
        "tree_combine_tests": tree_tests,
        "tree_generated_outputs": tree_generated,
        "full_tree_terminal_functions": len(trees[full]),
        "full_tree_contains_false": 0 in trees[full],
        "extend_cache": extend.cache_info()._asdict(),
        "relaxations": [
            "free exact clause aliases",
            "free exact affine aliases",
            "AND3 whenever output essential support is at most three",
        ],
    }


def canonical_clause(values):
    return tuple(sorted(set(values), key=lambda x: (abs(x), x < 0)))


def resolve(left, right, pivot):
    if pivot not in left or -pivot not in right:
        raise ValueError("pivot polarity absent")
    raw = (set(left) | set(right)) - {pivot, -pivot}
    if any(-lit in raw for lit in raw):
        raise ValueError("tautological resolvent")
    return canonical_clause(raw)


def resolution_witness(clauses):
    lines = [canonical_clause(c) for c in clauses]
    steps = [
        (0, 4, 2, (1, -3, 4)),
        (2, 5, -3, (-1, 2, -4)),
        (0, 7, 1, (2, -4)),
        (2, 6, -1, (-3, 4)),
        (3, 8, -2, (-4,)),
        (1, 9, 3, (4,)),
        (10, 11, -4, ()),
    ]
    certificate = []
    for left, right, pivot, expected in steps:
        got = resolve(lines[left], lines[right], pivot)
        expected = canonical_clause(expected)
        if got != expected:
            raise AssertionError((left, right, pivot, got, expected))
        lines.append(got)
        certificate.append({
            "left_line": left + 1,
            "right_line": right + 1,
            "pivot": pivot,
            "clause": got,
        })
    if lines[-1] != ():
        raise AssertionError("witness does not end in contradiction")
    return certificate


def reject_corruptions(clauses, certificate):
    def check(cert):
        lines = [canonical_clause(c) for c in clauses]
        for step in cert:
            left = step["left_line"] - 1
            right = step["right_line"] - 1
            if left >= len(lines) or right >= len(lines):
                return False
            try:
                got = resolve(lines[left], lines[right], step["pivot"])
            except ValueError:
                return False
            if got != canonical_clause(step["clause"]):
                return False
            lines.append(got)
        return bool(lines) and lines[-1] == ()

    corrupt = []
    a = json.loads(json.dumps(certificate)); a[0]["pivot"] = 4; corrupt.append(a)
    b = json.loads(json.dumps(certificate)); b[2]["left_line"] = 2; corrupt.append(b)
    c = json.loads(json.dumps(certificate)); c[4]["clause"] = [4]; corrupt.append(c)
    corrupt.append(certificate[:-1])
    return [not check(cert) for cert in corrupt]


def main():
    started = time.perf_counter()
    raw = INPUT.read_bytes()
    n, clauses = parse_dimacs(raw.decode())
    models = model_count(clauses, n)
    deletions = [model_count(clauses[:i] + clauses[i + 1 :], n) for i in range(len(clauses))]
    flips = sign_flip_counts(clauses, n)
    search = relaxed_unicycle_search(clauses, n)
    proof = resolution_witness(clauses)
    corrupted = reject_corruptions(clauses, proof)
    malformed = malformed_controls()
    odd_n, odd = parity_cnf_k4((1, 0, 0, 0))
    even_n, even = parity_cnf_k4((0, 0, 0, 0))
    parity = {"odd_models": model_count(odd, odd_n), "even_models": model_count(even, even_n)}
    assertions = {
        "authentic_sha256": hashlib.sha256(raw).hexdigest()
        == "47b47e154831555f1d66fd39ef90f4b439830a34627e4b4947329616469a2ccf",
        "source_unsat": models == 0,
        "clause_minimal": all(x > 0 for x in deletions),
        "all_occurrence_sign_flips_sat": all(x > 0 for x in flips),
        "floor_tree_excluded": not search["full_tree_contains_false"],
        "unicycle_excluded": not search["contradiction_found"],
        "seven_node_resolution_upper": len(proof) == 7 and proof[-1]["clause"] == (),
        "all_corruptions_rejected": all(corrupted),
        "all_malformed_rejected": all(malformed.values()),
        "parity_both_labels": parity == {"odd_models": 0, "even_models": 8},
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    result = {
        "claim_id": "PEITL-EXACT-SIX-REFEREE301",
        "status": {
            "source_excess_topology": "PROVED/EXACT",
            "six_node_relaxed_exclusion": "COMPUTATIONAL exhaustive finite",
            "seven_node_upper": "PROVED by syntactic Resolution replay",
            "mixed_minimum": "PROVED/EXACT in fixed source-independent-VARDEF Rmix341",
            "B1_B2_B3": "OPEN",
        },
        "input": {
            "path": str(INPUT),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "variables": n,
            "clauses": len(clauses),
            "signed_clauses": clauses,
            "models": models,
            "deletion_model_counts": deletions,
            "sign_flip_model_counts": flips,
        },
        "fixed_calculus": "Rmix341 source-independent zero-premise VARDEF; unit binary RES/AND3/XOR; exact paid unary CONVERT",
        "topology_identity": "q-(mu-1)=beta+u+2*d0 for r=mu=6; q=6 gives (beta,u,d0)=(0,1,0) or (1,0,0)",
        "unary_class": "excluded because granting its exact representation conversion for free reduces to the already-exhausted five-binary-node tree relaxation",
        "unicycle_search": search,
        "resolution_upper_certificate": proof,
        "exact_mixed_cost": 7,
        "malformed_controls": malformed,
        "corrupted_proof_rejections": corrupted,
        "parity_controls": parity,
        "assertions": assertions,
        "optimizer_cost_note": "free best proof selection is granted; enumeration work is external certification, not part of W_R",
        "resource_ledger": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "python": platform.python_version(),
            "all_phase_note": "materializes truth tables, tree banks, extension cache, controls and JSON; no machine lower-bound or sublinear-space claim",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(OUT), "exact_mixed_cost": 7, "assertions": assertions, "search": search}, indent=2))


if __name__ == "__main__":
    main()
