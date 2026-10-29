#!/usr/bin/env python3
"""Independent finite controls for CONNECTED-INTERFACE-REFEREE186.

Standard library only.  The exhaustive statements here are computational;
the report contains the separate symbolic proofs and scope firewalls.
"""
from __future__ import annotations

import hashlib
import itertools as it
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


def cycle_scopes(n: int):
    assert n >= 3 and n % 3 == 0
    return [(i, (i + 1) % n, (i + 2) % n) for i in range(n)] + [
        (i, i + 1, i + 2) for i in range(0, n, 3)
    ]


def exact22_signings(n: int):
    scopes = cycle_scopes(n)
    occurrences = [[] for _ in range(n)]
    for ci, scope in enumerate(scopes):
        for li, v in enumerate(scope):
            occurrences[v].append((ci, li))
    assert all(len(x) == 4 for x in occurrences)
    choices = [tuple(it.combinations(slots, 2)) for slots in occurrences]
    for selected in it.product(*choices):
        positive = {slot for pair in selected for slot in pair}
        yield [
            tuple((v + 1) if (ci, li) in positive else -(v + 1)
                  for li, v in enumerate(scope))
            for ci, scope in enumerate(scopes)
        ]


def sat_witness(clauses, n: int):
    for mask in range(1 << n):
        if all(any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0)
                   for lit in clause) for clause in clauses):
            return mask
    return None


def exhaustive_cycle(n: int):
    total = sat = unsat = 0
    witness_checksum = 0
    for clauses in exact22_signings(n):
        total += 1
        witness = sat_witness(clauses, n)
        if witness is None:
            unsat += 1
        else:
            sat += 1
            witness_checksum = (witness_checksum * 1315423911 + witness) % (1 << 64)
        counts = Counter(lit for clause in clauses for lit in clause)
        assert all(counts[v] == counts[-v] == 2 for v in range(1, n + 1))
    assert total == 6 ** n and unsat == 0
    return {"n": n, "signings": total, "sat": sat, "unsat": unsat,
            "witness_checksum_mod_2^64": witness_checksum}


def elimination_identity():
    checked = 0
    by_t = {}
    for t in range(1, 5):
        local = 0
        for bits in it.product((False, True), repeat=4 * t):
            A = [bits[4 * i] or bits[4 * i + 1] for i in range(t)]
            B = [bits[4 * i + 2] or bits[4 * i + 3] for i in range(t)]
            existential = any(
                all(z or a for a in A) and all((not z) or b for b in B)
                for z in (False, True)
            )
            compact = all(A) or all(B)
            resolvents = all(a or b for a in A for b in B)
            assert existential == compact == resolvents
            local += 1
        by_t[str(t)] = local
        checked += local
    assert checked == 69904
    return {"assignments": checked, "by_t": by_t}


def cross_module_control():
    # One boundary name y=0 and eight singleton labels.  Four clauses each
    # touch y and two distinct modules.  This is connected, but deliberately
    # violates the theorem's no-cross-module-private-names hypothesis.
    clauses = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (0, 7, 8)]
    b = 1
    k = 8
    assert k > 4 * b
    return {
        "boundary_size": b,
        "nominal_singleton_modules": k,
        "clauses": clauses,
        "connected": True,
        "violated_hypothesis": "each clause may contain private names from only one module",
        "k_gt_4b": True,
    }


def terminal_grammar_control():
    all_eight = list(it.product(*[(v, -v) for v in (1, 2, 3)]))
    assert sat_witness(all_eight, 3) is None
    counts = Counter(lit for clause in all_eight for lit in clause)
    per_variable = {str(v): {"positive": counts[v], "negative": counts[-v]}
                    for v in (1, 2, 3)}
    assert all(x == {"positive": 4, "negative": 4} for x in per_variable.values())
    return {
        "clauses": len(all_eight),
        "unsat": True,
        "occurrences": per_variable,
        "strict_exact22": False,
    }


def grid_control(L: int):
    def vid(kind, r, c):
        return kind * L * L + (r % L) * L + (c % L) + 1
    clauses = []
    for r in range(L):
        for c in range(L):
            A = vid(0, r, c)
            clauses += [
                (A, vid(1, r, c), vid(2, r, c)),
                (A, vid(1, r + 1, c), vid(2, r, c)),
                (-A, -vid(1, r, c), -vid(2, r, c + 1)),
                (-A, -vid(1, r + 1, c), -vid(2, r, c + 1)),
            ]
    counts = Counter(lit for clause in clauses for lit in clause)
    n = 3 * L * L
    assert all(counts[v] == counts[-v] == 2 for v in range(1, n + 1))
    # A=1, B=C=0 satisfies all displayed formulas.
    def value(v):
        return v <= L * L
    assert all(any(value(abs(lit)) == (lit > 0) for lit in clause) for clause in clauses)
    return {"L": L, "variables": n, "clauses": len(clauses),
            "exact22": True, "explicit_witness": "A=1,B=C=0"}


def replay_archive(archive_dir: Path):
    expected_path = archive_dir / "results.json"
    proc = subprocess.run([sys.executable, str(archive_dir / "audit.py")],
                          check=True, capture_output=True, text=True)
    actual = json.loads(proc.stdout)
    expected = json.loads(expected_path.read_text())
    assert actual == expected
    return {
        "exact_json_match": True,
        "results_sha256": hashlib.sha256(expected_path.read_bytes()).hexdigest(),
        "boundary_subsets_checked": actual["boundary_subsets_checked"],
        "local_discovery_checks": actual["local_discovery_checks"],
        "truth_table_comparisons": actual["truth_table_comparisons"],
    }


def main():
    archive_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = {
        "run_id": "CONNECTED-INTERFACE-REFEREE186",
        "status": "PASS",
        "cycle_exact22_exhaustive": [exhaustive_cycle(3), exhaustive_cycle(6)],
        "elimination_identity": elimination_identity(),
        "cross_module_hypothesis_control": cross_module_control(),
        "terminal_grammar_control": terminal_grammar_control(),
        "grid_controls": [grid_control(L) for L in (2, 3, 4, 5, 6)],
        "limitations": [
            "Finite enumeration does not prove asymptotic claims.",
            "The cross-module control intentionally violates a theorem hypothesis.",
            "Syntactic width or hitting-set size is not a SAT runtime lower bound.",
            "The experiment runs on Python/RAM and is not a native tape ledger.",
        ],
    }
    if archive_dir:
        result["archive_replay"] = replay_archive(archive_dir)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
